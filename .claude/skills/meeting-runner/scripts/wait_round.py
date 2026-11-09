#!/usr/bin/env python3
r"""wait_round.py: espera as personas entregarem a rodada N e narra cada chegada em uma linha.

Uso:
    wait_round.py <N> --reuniao reuniao.json [--root DIR] [--timeout SEG] [--poll SEG] [--source {mailbox,marker}]
                  [--sessions ARQUIVO] [--sessions-state "cmd" | --no-state | --list-json arquivo] [--once]

Sinal de fim (`--source`, padrão `mailbox`): a MENSAGEM da persona, `brza orchestration send --subject "fim-rodada-N"`,
com M >= N. O marcador `<!-- fim-rodada-M -->` como última linha não vazia do worklog continua como registro que o
`tally.py` lê, e vale como fallback silencioso: a persona chega por mensagem OU pelo marcador. `--source marker` é o
comportamento antigo (só o marcador): o fallback para chat sem Dispatch (`--via agent-launch` do `launch_persona.py`).

Mailbox: em laço, `brza orchestration check --wait --peek --timeout-ms <poll*1000> --json` (`--poll` padrão 15 s; `--peek`
não consome a caixa da coordenação; sem shell). Cada registro novo (dedupe pelo `id` PRÓPRIO da mensagem, ou, sem ele, pelo
hash do JSON da mensagem individual; o `delivery_id` é do lote e não vale) é atribuído à persona SÓ por duas vias exatas:
(1) o `dispatch_id` do registro (ou o remetente `dispatch:<id>`) igual ao do mapa de sessões (`--sessions`, padrão
`.sessions/sessions.jsonl` da raiz comum do git) ou ao `dispatch_id` da persona no manifesto (que sobrescreve o mapa);
(2) o token exato `persona:<slug>` (palavra inteira, o slug em maiúscula/minúscula exatas) no `body` ou no `subject`. NENHUMA
busca pelo nome ou pela sessão em texto livre. Mensagem sem atribuição sai como `mensagem sem remetente reconhecido:
<assunto>` e não conta. O padrão `fim-rodada-(\\d+)` se procura em qualquer string do registro; vale o maior M. A chegada por
mensagem CRUZA o worklog: sem o marcador N no fim dele, sai `⚠ <nome> avisou fim-rodada-N mas o worklog não termina no
marcador` (o `tally.py` precisa dele); a chegada só pelo marcador diz `(pelo marcador)`. Mensagem `worker_done`, `blocked`,
`question` ou `escalation` de uma persona imprime `<nome> enviou <tipo>: <assunto>` e não conta como chegada. `brza`
ausente, erro ou JSON ruim: aviso e queda para `marker`, sem derrubar. `check` que volta `ok` com a lista vazia por 5
chamadas seguidas, sem nenhuma mensagem na espera inteira, avisa UMA vez: "caixa vazia: confira se a coordenação tem um Run
ligado".

O marcador só vale como a última linha não vazia SEM recuo (`<!-- fim-rodada-M -->`); o `tally.py` recusa o recuado do mesmo
jeito. `--root` padrão: o topo do repositório git do cwd; sem nenhum worklog sob ele, avisa em stderr.

FORMATO DO JSON DO `check` NÃO SONDADO (só um Run vivo mostra; a P4a.0 confirma). A leitura assume só isto: o JSON, em
qualquer profundidade, tem objetos com a chave `subject` (o registro da mensagem). Por registro, lê de forma tolerante:
`type`|`kind`|`message_type`|`messageType` (tipo, com `-` virando `_`); `subject`|`title` (assunto); `from`|`sender`|
`from_handle`|`fromHandle`|`source` (remetente); `id`|`message_id`|`messageId` (dedupe); `dispatch_id`|`dispatchId`
(atribuição). O resto (corpo, payload, aninhados) entra pela busca de `body` e `subject` em qualquer profundidade.

O `state` de cada persona (o campo `state` de `brza sessions list --json`, que é o `chatStatus` da aba) vem de
`--sessions-state` (padrão `brza sessions list --json`), de `--list-json arquivo` (para teste) ou fica de fora com
`--no-state`; `brza` ausente ou JSON ruim não derruba a espera. Ele só aparece na linha final do timeout.

Saída, uma linha por chegada e, a cada 3 min sem chegada, a mesma linha de status:
    R2 · 4/6 — entregaram Lenha, Cinza, Tição, Fole; faltam Faísca (Grok, 5 min) e Fogareiro (Antigravity, 5 min)

Termina quando todos chegaram (código 0) ou no timeout (código 2), imprimindo quem falta e o `state`. Sem `--timeout`,
o teto é: 180 s até a primeira chegada; depois, 2 vezes a mediana das latências das chegadas, no mínimo 180 s.
`--once` olha uma vez, imprime a linha e sai com 0 (todos) ou 2.

Funções puras para teste: `scan`, `status_line`, `compute_timeout`, `extract_messages`, `attribute`, `run` (que recebe
`check_fn(timeout_ms) -> lista de registros`).
MORRE quando o `brza sessions wait` existir.
"""
import argparse
import hashlib
import json
import os
import re
import shlex
import statistics
import subprocess
import sys
import time

MARCADOR = re.compile(r"^<!-- fim-rodada-(\d+) -->$")
RUNTIME_NOME = {"claude": "Claude", "codex": "Codex", "grok": "Grok", "antigravity": "Antigravity"}
STATUS_A_CADA = 180
FIM = re.compile(r"fim-rodada-(\d+)")
TIPOS_AVISO = {"worker_done", "blocked", "question", "escalation"}
K_TIPO = ("type", "kind", "message_type", "messageType")
K_ASSUNTO = ("subject", "title")
K_REMETENTE = ("from", "sender", "from_handle", "fromHandle", "source")
K_ID = ("id", "message_id", "messageId")  # id PRÓPRIO da mensagem; o `delivery_id` é do lote e não vale
K_DISPATCH = ("dispatch_id", "dispatchId", "from_dispatch", "fromDispatch", "from_dispatch_id")
K_REMETENTE_ID = ("from", "sender", "from_handle", "fromHandle", "source")
CAIXA_VAZIA_APOS = 5  # chamadas seguidas ok com lista vazia, sem nenhuma mensagem na espera inteira


class CheckIndisponivel(Exception):
    """O `brza orchestration check` não rodou ou não devolveu JSON."""


def last_marker(path):
    """N do marcador que é a última linha não vazia do arquivo; None se não for ou se o arquivo não existe."""
    try:
        with open(path, encoding="utf-8") as f:
            linhas = [l.rstrip() for l in f if l.strip()]  # marcador recuado não vale (o `tally.py` também recusa)
    except OSError:
        return None
    m = MARCADOR.match(linhas[-1]) if linhas else None
    return int(m.group(1)) if m else None


def worklog_path(reuniao, p):
    return reuniao["worklog"].format(slug=p.get("slug") or p["nome"].lower(), nome=p["nome"], sessao=p.get("sessao", ""))


def scan(reuniao, n, root):
    """{nome: entregou?} pela última linha de cada worklog."""
    out = {}
    for p in reuniao["personas"]:
        m = last_marker(os.path.join(root, worklog_path(reuniao, p)))
        out[p["nome"]] = m is not None and m >= n
    return out


def _lista(itens):
    return itens[0] if len(itens) == 1 else ", ".join(itens[:-1]) + " e " + itens[-1]


def status_line(n, reuniao, chegaram, elapsed_s, states=None):
    """`R2 · 4/6 — entregaram A, B; faltam C (Grok, 5 min) e D (Codex, 5 min)`.

    `chegaram` é a lista de nomes na ordem de chegada; `states` ({nome: state}) acrescenta o state de quem falta."""
    pessoas = {p["nome"]: p for p in reuniao["personas"]}
    faltam = [nome for nome in pessoas if nome not in chegaram]
    total = len(pessoas)
    if not faltam:
        return f"R{n} · {total}/{total} — todos entregaram: {', '.join(chegaram)}"
    itens = []
    for nome in faltam:
        detalhe = [RUNTIME_NOME.get((pessoas[nome].get("runtime") or "").lower(), pessoas[nome].get("runtime") or "?")]
        if elapsed_s >= 60:
            detalhe.append(f"{int(elapsed_s // 60)} min")
        if states is not None:
            detalhe.append(f"state {states.get(pessoas[nome].get('sessao')) or '?'}")
        itens.append(f"{nome} ({', '.join(detalhe)})")
    entregaram = f"entregaram {', '.join(chegaram)}; " if chegaram else ""
    return f"R{n} · {len(chegaram)}/{total} — {entregaram}faltam {_lista(itens)}"


def compute_timeout(latencias):
    """180 s até a primeira chegada; depois 2 x a mediana das latências, no mínimo 180 s."""
    if not latencias:
        return 180.0
    return max(180.0, 2 * statistics.median(latencias))


def fetch_states(reuniao, list_json=None, cmd=None):
    """{sessao: state} de `brza sessions list --json`; {} se o comando ou o JSON falhar."""
    try:
        if list_json:
            with open(list_json, encoding="utf-8") as f:
                data = json.load(f)
        else:
            r = subprocess.run(shlex.split(cmd or "brza sessions list --json"), capture_output=True, text=True,
                               timeout=20)
            data = json.loads(r.stdout)
    except (OSError, ValueError, subprocess.SubprocessError):
        return {}
    sess = data.get("sessions", []) if isinstance(data, dict) else []
    nomes = {p.get("sessao") for p in reuniao["personas"]}
    out = {s.get("name"): s.get("state") for s in sess if s.get("name") in nomes}
    for p in reuniao["personas"]:  # sobrescrita do manifesto: a linha do list que traz a sessão da persona
        ids = {p.get("claude_session"), p.get("provider_session")} - {None, ""}
        for s in sess:
            if ids & {s.get("claude_session"), s.get("provider_session")}:
                out[p.get("sessao")] = s.get("state")
    return out


def _shallow(rec, chaves):
    for k in chaves:
        v = rec.get(k)
        if isinstance(v, (str, int)) and not isinstance(v, bool) and str(v):
            return str(v)
    return None


def extract_messages(data):
    """Os objetos com a chave `subject`, em qualquer profundidade do JSON do `check`."""
    achados = []
    if isinstance(data, dict):
        if "subject" in data:
            return [data]
        for v in data.values():
            achados += extract_messages(v)
    elif isinstance(data, list):
        for v in data:
            achados += extract_messages(v)
    return achados


def _strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _strings(v)


def _valores(obj, chaves):
    """Os valores escalares das `chaves`, em qualquer profundidade do registro."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in chaves and isinstance(v, (str, int)) and not isinstance(v, bool) and str(v):
                yield str(v)
            else:
                yield from _valores(v, chaves)
    elif isinstance(obj, list):
        for v in obj:
            yield from _valores(v, chaves)


def fim_numero(rec):
    """Maior M de `fim-rodada-M` em qualquer string do registro; None se não houver."""
    ms = [int(m) for t in _strings(rec) for m in FIM.findall(t)]
    return max(ms) if ms else None


def slug_de(p):
    return p.get("slug") or p["nome"].lower()


def token_persona(slug):
    """`persona:<slug>` como palavra inteira, com o slug em maiúscula/minúscula exatas."""
    return re.compile(r"(?<![\w:-])persona:" + re.escape(slug) + r"(?![\w-])")


def attribute(reuniao, rec, dispatch_map=None):
    """A persona dona do registro, e só por duas vias exatas (nunca por nome ou sessão em texto livre):
    1. o `dispatch_id` do registro (ou o remetente `dispatch:<id>`) IGUAL ao do mapa ou do manifesto;
    2. o token `persona:<slug>` no `body` ou no `subject`.
    Sem uma das duas, None: a mensagem não conta."""
    dispatch_map = dispatch_map or {}
    ids = set(_valores(rec, K_DISPATCH))
    ids |= {v[len("dispatch:"):] if v.startswith("dispatch:") else v for v in _valores(rec, K_REMETENTE_ID)}
    for p in reuniao["personas"]:
        d = p.get("dispatch_id") or dispatch_map.get(p.get("sessao"))
        if d and str(d) in ids:
            return p
    textos = list(_valores(rec, ("body", "subject")))
    for p in reuniao["personas"]:
        rx = token_persona(slug_de(p))
        if any(rx.search(t) for t in textos):
            return p
    return None


def check_brza(timeout_ms, brza="brza"):
    """Os registros novos do `brza orchestration check --wait --peek --json`; `CheckIndisponivel` se falhar."""
    argv = [brza, "orchestration", "check", "--peek", "--json"]
    if timeout_ms:
        argv += ["--wait", "--timeout-ms", str(int(timeout_ms))]
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout_ms / 1000 + 30)
        if r.returncode != 0:
            raise CheckIndisponivel(f"rc {r.returncode}: {(r.stderr or r.stdout).strip()[:200]}")
        return extract_messages(json.loads(r.stdout or "[]"))
    except (OSError, ValueError, subprocess.SubprocessError) as e:
        raise CheckIndisponivel(str(e)) from e


def raiz_padrao():
    """O topo do repositório git do cwd (`git rev-parse --show-toplevel`); sem git, o cwd."""
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return os.getcwd()


def sessions_file(root):
    r = subprocess.run(["git", "-C", root, "rev-parse", "--git-common-dir"], capture_output=True, text=True)
    base = os.path.dirname(os.path.abspath(os.path.join(root, r.stdout.strip()))) if r.returncode == 0 and \
        r.stdout.strip() else os.path.abspath(root)
    return os.path.join(base, ".sessions", "sessions.jsonl")


def dispatch_map(path):
    """{sessao: dispatch_id} da última linha `open` de cada sessão no mapa; {} se o mapa não existe.
    O `dispatch_id` da persona no manifesto sobrescreve o mapa (em `attribute`)."""
    out = {}
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if isinstance(row, dict) and row.get("event") == "open" and row.get("name"):
                    out[row["name"]] = row.get("dispatch_id")
    except OSError:
        pass
    return {k: v for k, v in out.items() if v}


def run(reuniao, n, root, *, timeout=None, poll=5.0, once=False, state_fn=None, clock=time.monotonic,
        sleep=time.sleep, out=None, source="marker", check_fn=None, dispatches=None):
    """O laço da espera. `clock`, `sleep`, `out` e `check_fn` se injetam nos testes. Devolve o código de saída (0 ou 2).

    `source="marker"` é o comportamento antigo; `mailbox` lê `check_fn(timeout_ms)` (padrão `check_brza`), com o marcador
    do worklog como fallback."""
    out = out or (lambda s: print(s, flush=True))
    check_fn = check_fn or check_brza
    t0 = clock()
    chegaram, latencias, ultima_linha, vistos = [], [], t0, set()
    caixa = {"vazias": 0, "recebidas": 0, "avisou": False}
    pessoas = {p["nome"]: p for p in reuniao["personas"]}

    def chegou(nome, agora, sufixo=""):
        nonlocal ultima_linha
        chegaram.append(nome)
        latencias.append(agora - t0)
        out(status_line(n, reuniao, chegaram, agora - t0) + sufixo)
        ultima_linha = agora

    def le_mensagens(agora, espera_s):
        try:
            registros = check_fn(espera_s * 1000)
        except (CheckIndisponivel, OSError) as e:
            out(f"aviso: brza orchestration check indisponível ({e}); sigo pelo marcador do worklog")
            return False
        if registros:
            caixa["vazias"], caixa["recebidas"] = 0, caixa["recebidas"] + len(registros)
        else:
            caixa["vazias"] += 1
            if caixa["vazias"] >= CAIXA_VAZIA_APOS and not caixa["recebidas"] and not caixa["avisou"]:
                caixa["avisou"] = True
                out("aviso: caixa vazia: confira se a coordenação tem um Run ligado "
                    "(`brza orchestration run-current`); sigo pelo marcador do worklog")
        for rec in registros:
            chave = _shallow(rec, K_ID) or "sha1:" + hashlib.sha1(
                json.dumps(rec, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()
            if chave in vistos:
                continue
            vistos.add(chave)
            p = attribute(reuniao, rec, dispatches)
            if p is None:
                out(f"mensagem sem remetente reconhecido: {_shallow(rec, K_ASSUNTO) or ''}")
                continue
            tipo = (_shallow(rec, K_TIPO) or "").lower().replace("-", "_")
            if tipo in TIPOS_AVISO:
                out(f"{p['nome']} enviou {tipo}: {_shallow(rec, K_ASSUNTO) or ''}")
                continue
            m = fim_numero(rec)
            if m is None or m < n or p["nome"] in chegaram:
                continue
            chegou(p["nome"], agora, " (pela mensagem)")
            if (last_marker(os.path.join(root, worklog_path(reuniao, p))) or 0) < n:
                out(f"⚠ {p['nome']} avisou fim-rodada-{n} mas o worklog não termina no marcador")
        return True

    mailbox = source == "mailbox"
    while True:
        agora = clock()
        espera = 0 if once else poll
        if mailbox:
            inicio = clock()
            mailbox = le_mensagens(agora, espera)
            if mailbox and not once and clock() - inicio < min(1.0, poll) and len(chegaram) < len(pessoas):
                sleep(1.0)  # `check --wait` que volta na hora sem registro não vira laço quente
            agora = clock()
        atual = scan(reuniao, n, root)
        for p in reuniao["personas"]:
            nome = p["nome"]
            if atual.get(nome) and nome not in chegaram:
                chegou(nome, agora, " (pelo marcador)" if source == "mailbox" else "")
        if len(chegaram) == len(reuniao["personas"]):
            return 0
        if once:
            out(status_line(n, reuniao, chegaram, agora - t0, state_fn() if state_fn else None))
            return 2
        limite = timeout if timeout is not None else compute_timeout(latencias)
        if agora - t0 >= limite:
            out(status_line(n, reuniao, chegaram, agora - t0, state_fn() if state_fn else None))
            return 2
        if agora - ultima_linha >= STATUS_A_CADA:
            out(status_line(n, reuniao, chegaram, agora - t0))
            ultima_linha = agora
        if not mailbox:
            sleep(poll)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Espera o fim da rodada: a mensagem da persona (mailbox) ou o marcador do worklog.")
    ap.add_argument("n", type=int)
    ap.add_argument("--reuniao", required=True)
    ap.add_argument("--root", help="padrão: o topo do repositório git do cwd")
    ap.add_argument("--timeout", type=float)
    ap.add_argument("--poll", type=float, help="segundos entre leituras (padrão 15 no mailbox, 5 no marker)")
    ap.add_argument("--source", choices=("mailbox", "marker"), default="mailbox")
    ap.add_argument("--sessions", help="mapa de sessões (padrão: .sessions/sessions.jsonl da raiz comum do git)")
    ap.add_argument("--sessions-state", help="comando que imprime o JSON do `brza sessions list --json`")
    ap.add_argument("--no-state", action="store_true")
    ap.add_argument("--list-json", help="arquivo com o JSON do list (para teste)")
    ap.add_argument("--once", action="store_true")
    a = ap.parse_args(argv)
    a.root = os.path.abspath(a.root) if a.root else raiz_padrao()
    path = a.reuniao if os.path.isabs(a.reuniao) or not os.path.isfile(os.path.join(a.root, a.reuniao)) \
        else os.path.join(a.root, a.reuniao)
    with open(path, encoding="utf-8") as f:
        reuniao = json.load(f)
    if not any(os.path.isfile(os.path.join(a.root, worklog_path(reuniao, p))) for p in reuniao["personas"]):
        print(f"aviso: nenhum worklog existe ainda sob {a.root}; se a raiz está certa, as personas ainda não gravaram",
              file=sys.stderr)
    state_fn = None if a.no_state else (lambda: fetch_states(reuniao, a.list_json, a.sessions_state))
    poll = a.poll or (15.0 if a.source == "mailbox" else 5.0)
    disp = dispatch_map(a.sessions or sessions_file(a.root)) if a.source == "mailbox" else None
    return run(reuniao, a.n, a.root, timeout=a.timeout, poll=poll, once=a.once, state_fn=state_fn, source=a.source,
               dispatches=disp)


if __name__ == "__main__":
    sys.exit(main())
