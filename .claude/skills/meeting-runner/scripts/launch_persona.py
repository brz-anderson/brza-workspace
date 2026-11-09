#!/usr/bin/env python3
"""launch_persona.py: abre as sessões das personas da reunião, com modelo e esforço e o ciclo de vida dos workers do Orca.

Uso:
    launch_persona.py <reuniao.json> [persona ...] [--via {worker-start,hybrid,agent-launch}] [--dry-run]
                      [--root DIR] [--sessions ARQUIVO]
    launch_persona.py <reuniao.json> --release [persona ...] [--dry-run]       # worker-release
    launch_persona.py <reuniao.json> --keep-open [persona ...] [--dry-run]     # worker-keep-open
    launch_persona.py <reuniao.json> --stop [persona ...] [--dry-run]          # worker-stop (quem não respondeu)
    launch_persona.py <reuniao.json> --send [persona ...|todas] --message "<texto>" [--dry-run]   # send v1

`--root` padrão: o topo do repositório git do cwd (`git rev-parse --show-toplevel`; sem git, o cwd); o manifesto relativo
resolve contra ele. Rodar da raiz do worktree, da pasta da reunião ou da pasta da skill dá o mesmo resultado.

ATENÇÃO, quem cria o Run das personas: com abertura em paralelo, cada `worker-start` sem Run ligado pode criar um Run
próprio; confira na sonda P4a.0 e, se preciso, rode `brza orchestration run-create` antes. (Ponto para o plano.)

Generaliza o `launch.py` da reunião do MCP remoto. Lê o manifesto (docstring do `tally.py`) e, por persona (nome, slug
ou sessão; sem nomes, todas), usa `<dir>/<prompt>` (padrão `prompt-<slug>.txt`); se não existir, gera uma linha a partir
de um molde e a grava. O molde traz os dois comandos de `brza orchestration send`, os dois com `--body "persona:<slug>"` (é por esse token que
o `wait_round.py` reconhece o remetente): `fim-rodada-N`, ao fechar cada rodada, e o `worker_done` do ENCERRAMENTO,
quando a coordenação mandar. Sem `--to`: o worker sem `--to` já fala com a coordenação; `--to <coordenacao>` entra só se
o manifesto tiver a chave opcional `coordenacao` (handle `run:<id>` ou `dispatch:<id>`).

A via (`--via`, padrão `worker-start`, a via A do PLN-017 R6):
  - `worker-start`: `brza orchestration worker-start --spec-file <prompt> --agent <runtime> [--model m --effort e]
    --worktree path:<checkout absoluto> --json`, por `subprocess` sem shell. O worker fecha sozinho ~2 min depois do
    `worker_done` aceito, com o botão "manter aberta" no chat. O worker não tem título de chat: o nome da persona vai só
    ao mapa. O recibo bruto vai a `<dir>/launch-<slug>.log`.
  - `hybrid`: primeiro o `agent launch --surface chat` de hoje (via `brza sessions`, que grava o `chat` no mapa) e depois
    `worker-start --terminal orca_session_id:<chat> --spec-file <prompt> --json` sobre esse chat. A sonda P4a.0 decide
    se o worker-start aceita um terminal já aberto (hybrid) ou se fica o `worker-start` puro.
  - `agent-launch`: o comportamento de antes, intacto: sem ciclo de vida; só para testar o resto da skill.
  `brza sessions` e o `--wait` dele só entram em `hybrid` e `agent-launch`; modelo e esforço seguem as regras de
  `settings()`: nunca "-" ou nulo, nunca ao Antigravity (o chat dele recusa modelo explícito; o mapa guarda "-").

Formato do recibo do `worker-start --json`: NÃO foi sondado (só um Run vivo mostra; a P4a.0 confirma). A leitura é
tolerante: busca recursiva, em qualquer profundidade, pelas chaves `dispatch_id`, `dispatchId` e o par `dispatch`/`id`
(dispatch_id); `orca_session_id`, `orcaSessionId`, `agentSessionId`, `sessionId`, `terminal`, `terminalHandle`, `handle`
(orca_session_id, a primeira que existir, nessa ordem). Recibo que não é JSON cai para uma busca por texto
`dispatch_id: x`. Não achou: grava `null` no mapa e avisa em stderr com o caminho do log.

O mapa (`.sessions/sessions.jsonl` da raiz comum do git, uma linha JSON por evento) ganha, por persona, uma linha
`{"event":"open","at","name":<sessao>,"via","dispatch_id","orca_session_id","model","effort","title"}`; usa o `record` do
`brza-sessions` quando carrega (`~/Projects/brza-workflow/packages/client/bin/brza-sessions`; `BRZA_SESSIONS_BIN`
sobrescreve), senão acrescenta direto. `--sessions` fixa o arquivo e dispensa o `record`.

`--release`/`--keep-open`/`--stop`: roda `brza orchestration worker-release|worker-keep-open|worker-stop --dispatch <id>`,
com o `dispatch_id` da persona no manifesto (sobrescrita) ou, senão, o da última linha `open` do mapa. `--release` vale só
para worker "settled" (que mandou `worker_done`); quem não respondeu ao encerramento se para com `--stop`. Este script
não fecha sessão por conta própria.

`--send`: `brza orchestration send --to dispatch:<id> --subject rodada --body <--message>`, o envio v1 para persona aberta
como worker (que não tem chat para o `brza sessions send`). Sem `shell`; `--dry-run` só imprime.

A linha `open` da via `worker-start` NÃO tem `chat`, `claude_session` nem `provider_session`: o script avisa em stderr. O
`tally.py` e o `wait_round.py` aceitam, por persona no manifesto, os campos opcionais `claude_session`,
`provider_session` e `dispatch_id` como sobrescrita do mapa.

`--dry-run` imprime, por via, os comandos exatos e o que gravaria no mapa, sem executar nada nem gravar o prompt.

MORRE quando o `brza sessions open` ganhar a via (`--via`, `--model`, `--effort`, o prompt-file e o recibo no mapa,
R1.2 e R6 do PLN-017): some o patch do `brza`, o `record` e a extração do recibo; sobra a leitura do manifesto e do
prompt.
"""
import argparse
import importlib.machinery
import importlib.util
import json
import os
import re
import shlex
import subprocess
import sys
from datetime import datetime

DEFAULT_BIN = os.path.expanduser("~/Projects/brza-workflow/packages/client/bin/brza-sessions")
MOLDE = ("Você é uma persona desta reunião: {nome}, {papel}. Tema: {tema}. Leia o briefing ({briefing}) e o arquivo "
         "da sua persona ({persona_md}) e faça a rodada 1 conforme o pedido que a coordenação mandar; o seu worklog "
         "é {worklog}; prazo {prazo}; responda em português do Brasil. "
         "Ao fechar cada rodada N, depois de gravar o marcador no worklog, avise a coordenação (troque N pelo número "
         "da rodada): brza orchestration send{to} --subject \"fim-rodada-N\" --body \"persona:{slug}\". "
         "O `worker_done` que o preâmbulo do Orca pede é o do ENCERRAMENTO, quando a coordenação mandar: "
         "brza orchestration send{to} --type worker_done --outcome succeeded --subject \"encerrado\" "
         "--body \"persona:{slug}\".")
AVISO_MAPA = ("aviso: {nome}: a linha `open` do mapa não tem `chat`, `claude_session` nem `provider_session` (o worker não "
              "tem chat): `brza sessions send/list` e a medição do tally.py NÃO acharão esta persona até a sonda P4a.0; "
              "enquanto isso, o envio vai por `launch_persona.py --send` e a medição por `claude_session`/"
              "`provider_session` na persona do manifesto")
VIAS = ("worker-start", "hybrid", "agent-launch")
DISPATCH_KEYS = (("dispatch_id",), ("dispatchId",), ("dispatch", "id"))
SESSION_KEYS = (("orca_session_id",), ("orcaSessionId",), ("agentSessionId",), ("sessionId",), ("terminal",),
                ("terminalHandle",), ("handle",))


def dash(v):
    return None if v in (None, "", "-") else v


def settings(p):
    """(agent, model, effort) que valem na abertura; model/effort None quando não vão ao `brza agent launch`."""
    agent = (p.get("runtime") or "claude").lower()
    if agent == "antigravity":
        return agent, None, None
    model = dash(p.get("modelo"))
    return agent, model, (dash(p.get("esforco")) if model else None)


def prompt_path(reuniao, p, root):
    return os.path.join(root, reuniao.get("dir", "."), p.get("prompt") or f"prompt-{p['slug']}.txt")


def prompt_text(reuniao, p):
    slug = p.get("slug") or p["nome"].lower()
    d = reuniao.get("dir", ".")
    return MOLDE.format(
        nome=p["nome"], slug=slug, papel=p.get("papel") or "persona", tema=reuniao.get("tema") or reuniao.get("id"),
        briefing=os.path.join(d, reuniao.get("briefing") or "briefing.md"), persona_md=os.path.join(d, "personas", f"{slug}.md"),
        worklog=reuniao["worklog"].format(slug=slug, nome=p["nome"], sessao=p.get("sessao", "")),
        prazo=reuniao.get("fim") or "o combinado",
        to=f" --to {reuniao['coordenacao']}" if reuniao.get("coordenacao") else "")


def title_for(reuniao, p, agent, model, effort):
    rotulo = " ".join(x for x in (model, effort) if x) or agent
    nome_reuniao = (reuniao.get("id") or "").removeprefix("reuniao-")
    return p.get("title") or f"Reunião {nome_reuniao}: {p['nome']} ({rotulo})"


def session_argv(reuniao, p, root):
    agent, model, effort = settings(p)
    return ["brza sessions", p["sessao"], "--agent", agent, "--title", title_for(reuniao, p, agent, model, effort),
            "--checkout", reuniao.get("checkout") or ".", "--prompt-file", prompt_path(reuniao, p, root), "--wait"]


def agent_launch_extra(p):
    agent, model, effort = settings(p)
    return (["--model", model] if model else []) + (["--effort", effort] if effort else [])


def checkout_abs(reuniao, root):
    """O `checkout` do manifesto é relativo à RAIZ COMUM do repositório (como no `brza sessions --checkout`), não ao
    worktree em que o script roda: `.worktrees/playground` junto do worktree dobraria o caminho."""
    co = reuniao.get("checkout") or "."
    return co if os.path.isabs(co) else os.path.abspath(os.path.join(common_root(root), co))


def log_path(reuniao, p, root):
    return os.path.join(root, reuniao.get("dir", "."), f"launch-{p.get('slug') or p['nome'].lower()}.log")


def worker_start_argv(reuniao, p, root, via="worker-start", chat="<chat>"):
    """O `brza orchestration worker-start` da persona; no `hybrid` ele pega o chat já aberto."""
    agent, model, effort = settings(p)
    argv = ["brza", "orchestration", "worker-start", "--spec-file", prompt_path(reuniao, p, root)]
    if via == "hybrid":
        argv += ["--terminal", f"orca_session_id:{chat}", "--worktree", f"path:{checkout_abs(reuniao, root)}", "--json"]
        return argv
    argv += ["--agent", agent]
    argv += ["--model", model] if model else []
    argv += ["--effort", effort] if effort else []
    return argv + ["--worktree", f"path:{checkout_abs(reuniao, root)}", "--json"]


def dry_run(reuniao, p, root, out=print, via="agent-launch"):
    agent, model, effort = settings(p)
    path = prompt_path(reuniao, p, root)
    out(f"[dry-run] {p['nome']} ({agent}, modelo {model or '-'}, esforço {effort or '-'}, via {via})")
    if via in ("agent-launch", "hybrid"):
        out("  " + " ".join(shlex.quote(a) for a in session_argv(reuniao, p, root)))
        out("  brza agent launch --agent " + agent + " --surface chat --worktree path:<checkout> [--prompt ...]"
            + (" " + " ".join(agent_launch_extra(p)) if agent_launch_extra(p) else ""))
    if via == "worker-start":
        out("  aviso: a linha `open` não terá chat/claude_session/provider_session: `brza sessions send/list` e a "
            "medição não acharão a persona até a sonda P4a.0")
    if via in ("worker-start", "hybrid"):
        out("  " + " ".join(shlex.quote(a) for a in worker_start_argv(reuniao, p, root, via)))
        out(f"  recibo: {log_path(reuniao, p, root)}")
    out(f"  mapa: open model={model or '-'} effort={effort or '-'}"
        + (f" via={via} dispatch_id=<do recibo> orca_session_id=<do recibo>" if via != "agent-launch" else ""))
    if os.path.isfile(path):
        out(f"  prompt: {path} (existe)")
    else:
        out(f"  prompt: geraria {path}: {prompt_text(reuniao, p)}")


def lifecycle_argv(verbo, dispatch):
    return ["brza", "orchestration", verbo, "--dispatch", dispatch]


def find_key(obj, chain):
    """Primeiro valor escalar (str/int) sob a cadeia de chaves, em qualquer profundidade; None se não houver."""
    if isinstance(obj, dict):
        cur = obj
        for k in chain:
            cur = cur.get(k) if isinstance(cur, dict) else None
        if isinstance(cur, (str, int)) and not isinstance(cur, bool) and str(cur):
            return str(cur)
        for v in obj.values():
            r = find_key(v, chain)
            if r:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_key(v, chain)
            if r:
                return r
    return None


def extract_receipt(text):
    """(dispatch_id, orca_session_id) do recibo do `worker-start --json`, ou None onde não achar."""
    data = None
    try:
        data = json.loads(text)
    except ValueError:
        pass
    found = []
    for keys in (DISPATCH_KEYS, SESSION_KEYS):
        v = None
        for chain in keys:
            v = find_key(data, chain) if data is not None else None
            if v:
                break
        if not v and data is None:
            for chain in keys:
                mm = re.search(r"%s[\"']?\s*[:=]\s*[\"']?([\w.:-]+)" % re.escape(chain[0]), text)
                if mm:
                    v = mm.group(1)
                    break
        found.append(v)
    return tuple(found)


def run_cmd(argv):
    """(rc, stdout, stderr); `brza` ausente vira rc 127."""
    try:
        r = subprocess.run(argv, capture_output=True, text=True)
    except OSError as e:
        return 127, "", str(e)
    return r.returncode, r.stdout, r.stderr


def common_root(root):
    r = subprocess.run(["git", "-C", root, "rev-parse", "--git-common-dir"], capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        return os.path.abspath(root)
    return os.path.dirname(os.path.abspath(os.path.join(root, r.stdout.strip())))


def sessions_file(root, sessions=None):
    return sessions or os.path.join(common_root(root), ".sessions", "sessions.jsonl")


def read_map(path):
    rows = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    pass
    except OSError:
        pass
    return rows


def last_open(path, sessao):
    return next((r for r in reversed(read_map(path)) if r.get("event") == "open" and r.get("name") == sessao), None)


def record_open(path, explicit, **fields):
    """Grava a linha `open` no mapa: pelo `record` do brza-sessions quando carrega, senão direto no arquivo."""
    if not explicit:
        try:
            return load_sessions_module().record("open", **fields)
        except Exception:  # noqa: BLE001 - qualquer falha do módulo cai para a gravação direta
            pass
    os.makedirs(os.path.dirname(path), exist_ok=True)
    row = {"event": "open", "at": datetime.now().astimezone().isoformat(timespec="seconds"), **fields}
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_sessions_module():
    src = os.environ.get("BRZA_SESSIONS_BIN") or DEFAULT_BIN
    loader = importlib.machinery.SourceFileLoader("brza_sessions", src)
    spec = importlib.util.spec_from_loader("brza_sessions", loader)
    m = importlib.util.module_from_spec(spec)
    loader.exec_module(m)
    return m


def ensure_prompt(reuniao, p, root):
    path = prompt_path(reuniao, p, root)
    if not os.path.isfile(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(prompt_text(reuniao, p) + "\n")


def launch(reuniao, p, root):
    """A via `agent-launch`: abre a persona neste processo; devolve o código de saída do `brza sessions`."""
    ensure_prompt(reuniao, p, root)
    agent, model, effort = settings(p)
    extra = agent_launch_extra(p)
    m = load_sessions_module()
    orig_brza, orig_record = m.brza, m.record

    def brza(*args):
        args = list(args)
        if args[:2] == ["agent", "launch"]:
            args += extra
        return orig_brza(*args)

    def record(event, **fields):
        if event == "open":
            fields.update(model=model or "-", effort=effort or "-")
        return orig_record(event, **fields)

    m.brza, m.record = brza, record
    sys.argv = session_argv(reuniao, p, root)
    return m.main()


def start_worker(reuniao, p, root, via, sessions=None, chat=None, run_fn=run_cmd):
    """O `worker-start` da persona: grava o recibo bruto, lê o dispatch e a sessão e acrescenta o `open` ao mapa."""
    agent, model, effort = settings(p)
    argv = worker_start_argv(reuniao, p, root, via, chat or "<chat>")
    rc, out, err = run_fn(argv)
    log = log_path(reuniao, p, root)
    os.makedirs(os.path.dirname(log), exist_ok=True)
    with open(log, "w", encoding="utf-8") as f:
        f.write(f"$ {' '.join(shlex.quote(a) for a in argv)}\nrc={rc}\n--- stdout\n{out}\n--- stderr\n{err}\n")
    if rc != 0:
        print(f"{p['nome']}: worker-start falhou (rc {rc}); recibo em {log}", file=sys.stderr)
        return rc
    dispatch, sess = extract_receipt(out)
    if via == "hybrid" and not sess:
        sess = chat
    if not dispatch or not sess:
        print(f"{p['nome']}: recibo sem {'dispatch_id' if not dispatch else 'orca_session_id'}; "
              f"gravei null no mapa; veja {log}", file=sys.stderr)
    fields = dict(name=p["sessao"], via=via, dispatch_id=dispatch, orca_session_id=sess, model=model or "-",
                  effort=effort or "-", title=title_for(reuniao, p, agent, model, effort))
    if chat:
        fields["chat"] = chat
    path = sessions_file(root, sessions)
    record_open(path, bool(sessions), **fields)
    print(f"{p['nome']}: {via} dispatch_id={dispatch} orca_session_id={sess}")
    if not chat:
        print(AVISO_MAPA.format(nome=p["nome"]), file=sys.stderr)
    return 0


def launch_via(reuniao, p, root, via, sessions=None):
    if via == "agent-launch":
        return launch(reuniao, p, root)
    ensure_prompt(reuniao, p, root)
    if via == "worker-start":
        return start_worker(reuniao, p, root, via, sessions)
    rc = launch(reuniao, p, root)
    if rc:
        return rc
    row = last_open(sessions_file(root, sessions), p["sessao"]) or {}
    if not row.get("chat"):
        print(f"{p['nome']}: sem chat no mapa depois do agent launch; sem worker-start", file=sys.stderr)
        return 1
    return start_worker(reuniao, p, root, via, sessions, chat=row["chat"])


def dispatch_of(p, path):
    """O dispatch da persona: o `dispatch_id` do manifesto, se houver, senão o da última linha `open` do mapa."""
    return p.get("dispatch_id") or (last_open(path, p["sessao"]) or {}).get("dispatch_id")


def send_argv(dispatch, message):
    return ["brza", "orchestration", "send", "--to", f"dispatch:{dispatch}", "--subject", "rodada", "--body", message]


def send(reuniao, escolhidas, root, message, sessions=None, dry=False, run_fn=run_cmd):
    """`--send`: a mensagem de rodada a cada persona aberta como worker (`send --to dispatch:<id do mapa>`)."""
    path = sessions_file(root, sessions)
    rc = 0
    for p in escolhidas:
        dispatch = dispatch_of(p, path)
        if not dispatch:
            print(f"{p['nome']}: sem dispatch_id no mapa nem no manifesto ({path})", file=sys.stderr)
            rc = rc or 1
            continue
        argv = send_argv(dispatch, message)
        if dry:
            print(f"[dry-run] {p['nome']}: " + " ".join(shlex.quote(a) for a in argv))
            continue
        r, out, err = run_fn(argv)
        print(f"{p['nome']}: send rc={r} {(out or err).strip()}")
        rc = rc or r
    return rc


def lifecycle(reuniao, escolhidas, root, verbo, sessions=None, dry=False, run_fn=run_cmd):
    """`worker-release`, `worker-keep-open` ou `worker-stop` com o dispatch de cada persona (manifesto, senão mapa)."""
    path = sessions_file(root, sessions)
    rc = 0
    for p in escolhidas:
        dispatch = dispatch_of(p, path)
        if not dispatch:
            print(f"{p['nome']}: sem dispatch_id no mapa ({path})", file=sys.stderr)
            rc = rc or 1
            continue
        argv = lifecycle_argv(verbo, dispatch)
        if dry:
            print(f"[dry-run] {p['nome']}: " + " ".join(shlex.quote(a) for a in argv))
            continue
        r, out, err = run_fn(argv)
        print(f"{p['nome']}: {verbo} rc={r} {(out or err).strip()}")
        rc = rc or r
    return rc


def pick(reuniao, nomes):
    if not nomes or [q.lower() for q in nomes] == ["todas"]:
        return list(reuniao["personas"])
    chosen = []
    for q in nomes:
        achou = [p for p in reuniao["personas"]
                 if q.lower() in (p["nome"].lower(), (p.get("slug") or "").lower(), (p.get("sessao") or "").lower())]
        if not achou:
            raise SystemExit(f"persona desconhecida: {q}")
        chosen += achou
    return chosen


def raiz_padrao():
    """O topo do repositório git do cwd (`git rev-parse --show-toplevel`); sem git, o cwd."""
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return os.getcwd()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Abre as personas da reunião, com modelo, esforço e o ciclo de vida do Orca.")
    ap.add_argument("reuniao")
    ap.add_argument("personas", nargs="*", help="nome, slug ou sessão; `todas` ou nada = todas")
    ap.add_argument("--via", choices=VIAS, default="worker-start")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--release", action="store_true", help="worker-release (só worker settled; dispatch do mapa)")
    ap.add_argument("--keep-open", action="store_true", help="worker-keep-open das personas (dispatch do mapa)")
    ap.add_argument("--stop", action="store_true", help="worker-stop de quem não respondeu ao encerramento")
    ap.add_argument("--send", action="store_true", help="send --to dispatch:<id> --subject rodada --body <--message>")
    ap.add_argument("--message", help="o texto do --send")
    ap.add_argument("--sessions", help="arquivo do mapa (padrão: .sessions/sessions.jsonl da raiz comum do git)")
    ap.add_argument("--root", help="padrão: o topo do repositório git do cwd")
    a = ap.parse_args(argv)
    a.root = os.path.abspath(a.root) if a.root else raiz_padrao()
    path = a.reuniao if os.path.isabs(a.reuniao) or not os.path.isfile(os.path.join(a.root, a.reuniao)) \
        else os.path.join(a.root, a.reuniao)
    with open(path, encoding="utf-8") as f:
        reuniao = json.load(f)
    escolhidas = pick(reuniao, a.personas)
    if a.send:
        if not a.message:
            ap.error("--send pede --message")
        return send(reuniao, escolhidas, a.root, a.message, a.sessions, a.dry_run)
    if a.release or a.keep_open or a.stop:
        verbo = "worker-stop" if a.stop else "worker-keep-open" if a.keep_open else "worker-release"
        return lifecycle(reuniao, escolhidas, a.root, verbo, a.sessions, a.dry_run)
    if a.dry_run:
        for p in escolhidas:
            dry_run(reuniao, p, a.root, via=a.via)
        return 0
    if len(escolhidas) == 1:
        return launch_via(reuniao, escolhidas[0], a.root, a.via, a.sessions)
    extra = ["--via", a.via, "--root", a.root] + (["--sessions", a.sessions] if a.sessions else [])
    procs = [(p, subprocess.Popen([sys.executable, os.path.abspath(__file__), os.path.abspath(path), p["nome"], *extra],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)) for p in escolhidas]
    rc = 0
    for p, proc in procs:
        saida, _ = proc.communicate()
        print(f"--- {p['nome']}\n{saida.rstrip()}")
        rc = rc or proc.returncode
    return rc


if __name__ == "__main__":
    sys.exit(main())
