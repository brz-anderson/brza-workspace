#!/usr/bin/env python3
"""Hook de medição do workspace brza: grava uma linha JSON por evento em .measurements/measurements.jsonl.

Um modo por evento do Claude Code, no primeiro argumento:

- `subagent` (SubagentStop): soma, do transcript do subagente, os tokens por tipo, as chamadas à API e de ferramenta,
  a duração, o maior contexto de uma chamada e as negações de hook, estima o custo em US$ e registra a conta, o
  modelo, o esforço e a versão do plugin. Vale
  também para o `agent()` de workflow, que chega como `workflow-subagent`.
- `skill` (PostToolUse, matcher Skill): a skill que o modelo invocou e o momento — o começo da janela.
- `command` (UserPromptExpansion): a skill ou o comando digitado como `/nome`, que não passa pela ferramenta Skill.
- `turn` (Stop): o turno da sessão principal, medido como o subagente, com as skills e os agentes que rodaram nele. É
  o que fecha a janela da skill na sessão principal.
- `failure` (StopFailure): o turno que acabou em erro de API, como o limite de uso (`rate_limit`, o 429).
- `mcp` (PostToolUse e PostToolUseFailure, matcher mcp__.*): a duração e o servidor de cada chamada MCP.

Só mede: nunca bloqueia nem escreve fora de .measurements/. O `resume_guard.py` grava no mesmo log a linha `guard`.
Cada transcript é lido a partir de onde a leitura anterior parou (estado em .measurements/state.json): a retomada de
um subagente mede só o trecho novo, e cada turno mede só o próprio trecho.
"""

import json
import os
import sys
import time
from datetime import datetime, timezone

try:
    import fcntl
except ImportError:  # fora do Unix o estado fica sem trava
    fcntl = None

# US$ por milhão de tokens, por modelo, da documentação da API em 2026-10-12: escrita de cache de 5 min a 1,25x a
# entrada e de 1 h a 2x; leitura de cache a 0,05x no Opus 5.5, 0,025x no Fable 5.1 e 0,1x nos demais. A chave é o id do
# modelo até a versão, casado pelo começo do nome no transcript (`claude-haiku-4-5-20251001`, `claude-opus-5-5-high`);
# modelo fora da tabela fica sem custo (None) em vez de herdar o preço de outra versão da família. Estimativa e
# abaixo do real: o transcript grava o output_tokens do início de cada mensagem, não o final, então a saída sai
# subcontada (entrada e cache valem). O custo pesa quase todo no cache.
PRICES = {
    "claude-opus-5-5": {"input": 4.0, "cache_write_5m": 5.0, "cache_write_1h": 8.0, "cache_read": 0.20, "output": 20.0},
    "claude-sonnet-5-5": {"input": 2.0, "cache_write_5m": 2.5, "cache_write_1h": 4.0, "cache_read": 0.20, "output": 10.0},
    "claude-haiku-4-5": {"input": 1.0, "cache_write_5m": 1.25, "cache_write_1h": 2.0, "cache_read": 0.10, "output": 5.0},
    "claude-fable-5-1": {"input": 10.0, "cache_write_5m": 12.5, "cache_write_1h": 20.0, "cache_read": 0.25, "output": 50.0},
    # O Haiku 5.5 cobra pelo tamanho do prompt de cada pedido (entrada, leitura e escrita de cache somadas): acima de
    # 100 mil tokens, o pedido inteiro vai à segunda tabela, mesmo com parte dele em cache. Da página de preços em
    # 2026-10-19.
    "claude-haiku-5-5": {"input": 0.10, "cache_write_5m": 0.125, "cache_write_1h": 0.20, "cache_read": 0.01, "output": 0.50,
                         "long_prompt": {"over": 100_000, "input": 0.50, "cache_write_5m": 0.625, "cache_write_1h": 1.0,
                                         "cache_read": 0.05, "output": 2.50}},
}
TOKEN_FIELDS = ("input", "cache_write", "cache_write_5m", "cache_write_1h", "cache_read", "output")


def request_cost(price, tokens):
    """US$ de um pedido à API do Claude pela tabela do modelo. O preço sai pedido a pedido porque o do Haiku 5.5 depende
    do tamanho do prompt de cada um. Sem a divisão 5m/1h, a escrita de cache é cobrada como 5m."""
    long = price.get("long_prompt")
    if long and tokens.get("input", 0) + tokens.get("cache_read", 0) + tokens.get("cache_write", 0) > long["over"]:
        price = long
    unsplit = tokens.get("cache_write", 0) - tokens.get("cache_write_5m", 0) - tokens.get("cache_write_1h", 0)
    return (tokens.get("input", 0) * price["input"]
            + (tokens.get("cache_write_5m", 0) + max(unsplit, 0)) * price["cache_write_5m"]
            + tokens.get("cache_write_1h", 0) * price["cache_write_1h"]
            + tokens.get("cache_read", 0) * price["cache_read"] + tokens.get("output", 0) * price["output"]) / 1e6


# A raiz é a do workspace, e não o diretório da sessão: sessão aberta no brza-studio também carrega este hook, pelo
# --settings da função do ~/.zshrc, que passa a BRZA_WORKSPACE. Sem ela vale o CLAUDE_PROJECT_DIR e, por último, o
# diretório onde o script mora. MEASURE_DIR existe só para teste.
ROOT = (os.environ.get("MEASURE_DIR") or os.environ.get("BRZA_WORKSPACE") or os.environ.get("CLAUDE_PROJECT_DIR")
        or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DIR = os.path.join(ROOT, ".measurements")
LOG = os.path.join(DIR, "measurements.jsonl")
STATE = os.path.join(DIR, "state.json")
LOCK = os.path.join(DIR, "state.lock")
# Diretório de configuração da conta que abriu a sessão: o adm-claude do ~/.zshrc passa CLAUDE_CONFIG_DIR.
CONFIG_DIR = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude")


def now():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def account():
    """A conta do Claude Code pelo diretório de configuração: `.claude`, ou `.claude-adm` quando a `adm-claude` do
    `~/.zshrc` põe o `CLAUDE_CONFIG_DIR`. Cada conta tem o próprio limite semanal."""
    return os.path.basename(os.path.normpath(os.environ.get("CLAUDE_CONFIG_DIR") or "~/.claude"))


def bridge_session():
    """O link da sessão no claude.ai (`session_…`), que vai no trailer `Claude-Session` e no rodapé do PR. O `/clear`
    troca o `session_id` mas mantém o link, e é por este campo que a linha chega à conversa que o PR cita. None na
    sessão aberta sem controle remoto."""
    return os.environ.get("CLAUDE_CODE_BRIDGE_SESSION_ID") or None


def write(line):
    os.makedirs(DIR, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")


def price_of(model):
    """Tabela de preço do modelo, pelo id até a versão, ou None se o modelo não estiver na tabela."""
    return next((table for prefix, table in PRICES.items() if model and model.startswith(prefix)), None)


def plugin_version(name, cwd):
    """Versão instalada do plugin de um nome com escopo (`fixfy:architect` → a do `fixfy`), ou None.

    Lê o installed_plugins.json da conta: a instalação de projeto cujo caminho contém o cwd ganha da de usuário. Sessão
    aberta com --plugin-dir carrega outra cópia, que este registro não enxerga."""
    if not name or ":" not in name:
        return None
    plugin = name.split(":", 1)[0]
    try:
        with open(os.path.join(CONFIG_DIR, "plugins", "installed_plugins.json"), encoding="utf-8") as f:
            installed = json.load(f).get("plugins", {})
    except (OSError, ValueError):
        return None
    best, best_len = None, -1
    for key, entries in installed.items():
        if key.split("@", 1)[0] != plugin:
            continue
        for entry in entries:
            path = entry.get("projectPath")
            if entry.get("scope") == "project" and path and cwd and (cwd == path or cwd.startswith(path + os.sep)):
                if len(path) > best_len:
                    best, best_len = entry.get("version"), len(path)
            elif entry.get("scope") == "user" and best_len < 0:
                best, best_len = entry.get("version"), 0
    return best


class State:
    """Onde parou a leitura de cada transcript, em bytes, sob trava: dois hooks podem fechar ao mesmo tempo."""

    def __enter__(self):
        os.makedirs(DIR, exist_ok=True)
        self.lock = open(LOCK, "w")
        if fcntl:
            fcntl.flock(self.lock, fcntl.LOCK_EX)
        try:
            with open(STATE, encoding="utf-8") as f:
                self.data = json.load(f)
        except (OSError, ValueError):
            self.data = {}
        return self

    def save(self):
        with open(STATE + ".tmp", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=1)
        os.replace(STATE + ".tmp", STATE)

    def __exit__(self, *_):
        self.lock.close()


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(b.get("text", "") for b in content if isinstance(b, dict))
    return ""


def only_tool_results(content):
    return isinstance(content, list) and content and all(
        isinstance(b, dict) and b.get("type") == "tool_result" for b in content)


def settle(path, step=0.25, limit=3.0):
    """Espera o transcript parar de crescer: o evento chega antes de as últimas mensagens irem para o disco, e o
    agente de workflow de uma resposta só foi lido sem ela."""
    size, waited = os.path.getsize(path), 0.0
    while waited < limit:
        time.sleep(step)
        waited += step
        current = os.path.getsize(path)
        if current == size:
            return
        size = current


def read_from(path, offset):
    """As linhas completas do transcript a partir do byte `offset`, e o byte onde a próxima leitura começa."""
    settle(path)
    with open(path, "rb") as f:
        f.seek(offset)
        raw = f.read()
    end = raw.rfind(b"\n") + 1  # a última linha pode estar pela metade: fica para a próxima leitura
    return raw[:end].decode("utf-8", errors="replace").splitlines(), offset + end


def measure(lines):
    usage = {}  # requestId → maior valor visto de cada campo (a mensagem chega em pedaços)
    # requestId → modelo que atendeu o pedido. O turno pode trocar de modelo no meio (o /model, ou a troca automática
    # de conta), e precificá-lo inteiro pelo último subconta o turno que começa em Fable e acaba em Opus.
    request_model = {}
    tools, denials, skills, agents = set(), [], [], []
    start = end = model = effort = None
    prompts = 0
    # O relógio abre na primeira mensagem do trecho — o pedido, ou o que retoma o subagente. Antes dela vêm o
    # tool_result que fechou a execução anterior e registros de sistema com o horário dela; contá-los poria a espera
    # entre as duas na duração.
    opened = False
    for raw in lines:
        try:
            e = json.loads(raw)
        except ValueError:
            continue
        kind = e.get("type")
        msg = e.get("message") or {}
        if kind == "user" and not only_tool_results(msg.get("content")):
            prompts += 1
        if not opened:
            opened = kind == "assistant" or (kind == "user" and not only_tool_results(msg.get("content")))
        ts = e.get("timestamp")
        if ts and opened:
            start = start or ts
            end = ts
        if kind == "assistant":
            if msg.get("model") != "<synthetic>":  # a mensagem de erro que o próprio Claude Code escreve
                model = msg.get("model") or model
                effort = e.get("effort") or effort
            u = msg.get("usage") or {}
            key = e.get("requestId") or msg.get("id") or e.get("uuid")
            if msg.get("model") and msg.get("model") != "<synthetic>":
                request_model.setdefault(key, msg.get("model"))
            current = usage.setdefault(key, {})
            cache = u.get("cache_creation") or {}
            for field, value in (
                ("input", u.get("input_tokens")),
                ("cache_write_5m", cache.get("ephemeral_5m_input_tokens")),
                ("cache_write_1h", cache.get("ephemeral_1h_input_tokens")),
                ("cache_write", u.get("cache_creation_input_tokens")),
                ("cache_read", u.get("cache_read_input_tokens")),
                ("output", u.get("output_tokens")),
            ):
                current[field] = max(current.get(field, 0), value or 0)
            for b in msg.get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("id") not in tools:
                    tools.add(b.get("id"))
                    entry = b.get("input") or {}
                    if b.get("name") == "Skill":
                        skills.append(entry.get("skill") or entry.get("command"))
                    elif b.get("name") in ("Agent", "Task"):
                        agents.append(entry.get("subagent_type") or "general-purpose")
        elif kind == "user":
            for b in msg.get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("is_error"):
                    t = text_of(b.get("content"))
                    if e.get("toolDenialKind") or ("PreToolUse" in t and "hook" in t):
                        denials.append(t.strip()[:240])
    total = {k: sum(r.get(k, 0) for r in usage.values()) for k in TOKEN_FIELDS}
    # Cada pedido sai pelo preço do modelo que o atendeu; o pedido sem modelo próprio fica com o do trecho. Basta um
    # pedido sem preço para o custo ficar nulo, como antes: custo parcial passaria por custo inteiro.
    by_model = {}
    for key, r in usage.items():
        m = request_model.get(key) or model
        price = price_of(m)
        entry = by_model.setdefault(m, {"api_calls": 0, "cost": 0.0 if price else None})
        entry["api_calls"] += 1
        if price and entry["cost"] is not None:
            entry["cost"] += request_cost(price, r)
    costs = [v["cost"] for v in by_model.values()]
    cost = sum(costs) if costs and None not in costs else None
    duration = None
    if start and end:
        t0 = datetime.fromisoformat(start.replace("Z", "+00:00"))
        t1 = datetime.fromisoformat(end.replace("Z", "+00:00"))
        duration = round((t1 - t0).total_seconds())
    return {
        "model": model,
        "effort": effort,
        "duration_s": duration,
        "api_calls": len(usage),
        "tool_calls": len(tools),
        "tokens": total,
        # O contexto da chamada mais cheia: acima de 200 mil, cada chamada relê o excedente do cache.
        "max_context": max((r.get("input", 0) + r.get("cache_read", 0) + r.get("cache_write", 0)
                            for r in usage.values()), default=0),
        "estimated_cost_usd": round(cost, 2) if cost is not None else None,
        # Só no trecho que trocou de modelo: `model` continua sendo o último, e a divisão diz quanto foi de cada um.
        **({"models": {m: {"api_calls": v["api_calls"],
                           "estimated_cost_usd": round(v["cost"], 2) if v["cost"] is not None else None}
                       for m, v in by_model.items()}} if len(by_model) > 1 else {}),
        "denials": len(denials),
        "denial_reasons": denials,
    }, {"prompts": prompts, "skills": skills, "agents": agents}


def effort_of(p):
    """Esforço em vigor quando o hook roda, pelo campo comum `effort` do payload — reserva para o transcript sem ele."""
    effort = p.get("effort")
    return effort.get("level") if isinstance(effort, dict) else effort


def agent_transcript(p):
    if p.get("agent_transcript_path"):
        return p["agent_transcript_path"]
    agent, main_path = p.get("agent_id"), p.get("transcript_path")
    if agent and main_path:
        return os.path.join(os.path.splitext(main_path)[0], "subagents", f"agent-{agent}.jsonl")
    return None


def subagent(p):
    path = agent_transcript(p)
    line = {"event": "subagent", "timestamp": now(), "session_id": p.get("session_id"),
            "bridge_session_id": bridge_session(), "agent_type": p.get("agent_type"), "agent_id": p.get("agent_id"),
            "cwd": p.get("cwd"), "account": account()}
    if not path or not os.path.exists(path):
        if not p.get("agent_type"):
            return  # subagente interno do Claude Code (sem tipo e sem transcript): não é uso medido
        line["error"] = f"transcript não encontrado: {path}"
        line["payload_fields"] = sorted(p.keys())
        write(line)
        return
    with State() as state:
        offset = state.data.get(path, 0)
        lines, end = read_from(path, offset)
        measured, _ = measure(lines)
        # Trecho sem chamada à API não avança a leitura: o que ainda não chegou ao disco fica para o próximo evento.
        if measured["api_calls"]:
            state.data[path] = end
            state.save()
        else:
            line["error"] = "trecho sem chamada à API: o transcript ainda não tinha a resposta"
    line.update(measured)
    line["effort"] = line["effort"] or effort_of(p)
    line["segment"] = "resume" if offset else "first"
    try:
        with open(path.replace(".jsonl", ".meta.json"), encoding="utf-8") as f:
            meta = json.load(f)
        line["agent_type"] = line["agent_type"] or meta.get("agentType")
        line["description"] = meta.get("description")
        line["requested_model"] = meta.get("model")  # o `model` do Agent, quando a chamada o sobrepôs
        line["request_shape"] = meta.get("requestShape")
        line["spawn_depth"] = meta.get("spawnDepth")
        line["workflow_phase"] = meta.get("workflowPhase")
    except (OSError, ValueError):
        pass
    # Agente de workflow mora em subagents/workflows/<runId>/: o runId soma o custo do workflow inteiro.
    parent = os.path.dirname(path)
    line["workflow"] = os.path.basename(parent) if os.path.basename(os.path.dirname(parent)) == "workflows" else None
    line["plugin_version"] = plugin_version(line["agent_type"], p.get("cwd"))
    write(line)


def skill(p):
    entry = p.get("tool_input") or {}
    name = entry.get("skill") or entry.get("command")
    write({"event": "skill", "timestamp": now(), "session_id": p.get("session_id"),
           "bridge_session_id": bridge_session(), "cwd": p.get("cwd"), "skill": name, "args": entry.get("args"),
           "agent_id": p.get("agent_id"), "plugin_version": plugin_version(name, p.get("cwd"))})


def command(p):
    name = p.get("command_name")
    write({"event": "command", "timestamp": now(), "session_id": p.get("session_id"),
           "bridge_session_id": bridge_session(), "cwd": p.get("cwd"), "command": name,
           "args": (p.get("command_args") or "")[:500] or None, "source": p.get("command_source"),
           "expansion_type": p.get("expansion_type"), "plugin_version": plugin_version(name, p.get("cwd"))})


def turn(p):
    path = p.get("transcript_path")
    if not path or not os.path.exists(path):
        return
    with State() as state:
        offset = state.data.get(path, 0)
        lines, end = read_from(path, offset)
        measured, seen = measure(lines)
        if not measured["api_calls"]:
            return  # turno sem chamada ao modelo (comando local, /clear): fica para o próximo, sem avançar a leitura
        state.data[path] = end
        state.save()
    line = {"event": "turn", "timestamp": now(), "session_id": p.get("session_id"),
            "bridge_session_id": bridge_session(), "cwd": p.get("cwd"), "account": account()}
    line.update(measured)
    line["effort"] = line["effort"] or effort_of(p)
    # Interrupção pelo usuário não dispara Stop: o turno interrompido cai no trecho do seguinte, com a espera entre
    # os dois na duração. Mais de um pedido no trecho é o sinal.
    line["prompts"] = seen["prompts"]
    line["segment"] = "resume" if offset else "first"
    line["skills"] = seen["skills"]
    line["agents"] = seen["agents"]
    line["plugin_versions"] = {n.split(":", 1)[0]: plugin_version(n, p.get("cwd"))
                               for n in seen["skills"] + seen["agents"] if n and ":" in n}
    write(line)


def failure(p):
    write({"event": "failure", "timestamp": now(), "session_id": p.get("session_id"),
           "bridge_session_id": bridge_session(), "cwd": p.get("cwd"), "agent_id": p.get("agent_id"),
           "agent_type": p.get("agent_type"), "error": p.get("error"), "error_details": p.get("error_details"),
           "effort": effort_of(p)})


def mcp(p):
    tool = p.get("tool_name") or ""
    server = p.get("mcp_server")
    # O campo mcp_server chegou na v2.1.274; antes dele, o servidor sai do nome mcp__<servidor>__<ferramenta>.
    server = server.get("name") if isinstance(server, dict) else (tool.split("__") + [None, None])[1]
    failed = p.get("hook_event_name") == "PostToolUseFailure"
    write({"event": "mcp", "timestamp": now(), "session_id": p.get("session_id"),
           "bridge_session_id": bridge_session(), "cwd": p.get("cwd"), "agent_id": p.get("agent_id"), "tool": tool,
           "server": server, "duration_ms": p.get("duration_ms"), "failed": failed,
           "error": str(p.get("error"))[:240] if failed and p.get("error") else None})


MODES = {"subagent": subagent, "skill": skill, "command": command, "turn": turn, "failure": failure, "mcp": mcp}


def main():
    try:
        p = json.load(sys.stdin)
        MODES[sys.argv[1]](p)
    except Exception as error:  # o hook mede; nunca derruba a chamada medida
        try:
            write({"event": "hook_error", "timestamp": now(), "mode": (sys.argv[1:] or [None])[0], "error": repr(error)})
        except Exception:
            pass
    sys.exit(0)


if __name__ == "__main__":
    main()
