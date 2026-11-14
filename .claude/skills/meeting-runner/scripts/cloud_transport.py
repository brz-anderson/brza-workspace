#!/usr/bin/env python3
"""Transporte cloud do meeting-runner.

O padrão continua o `brza sessions` do Studio, em `launch_persona.py`.
Este módulo só entra com `--transport cloud`. Cada persona abre com
`CloudRuntime.open` e recebe a rodada com `send`. O `agent -p` volta
síncrono. A ata da coordenação ganha o marcador `<!-- fim-rodada-N -->`.

O `cloud_runtime.py` é importado do checkout do `brza-workflow` na branch
`builder/pln-026-pr-b`, pelo caminho do repositório. Não há cópia na skill.
O `send` repete `persona` e `workspace`: sem memória do processo, o
`CloudRuntime` recusa o turno antes de chamar o `agent`. O home da persona
fica em `~/.local/share/brza/cloud-runtime/<persona>` e sobrevive ao `close`;
a chave não fica nesse diretório.
"""
import importlib.util
import json
import os
import sys
import time

TOKEN_FIELDS = ("input", "output", "cache_read", "cache_write", "reasoning")
MARKER_TEMPLATE = "<!-- fim-rodada-{n} -->"


class CloudTransportError(Exception):
    """Falha do transporte cloud. `returncode` sai diferente de 0."""

    def __init__(self, message, returncode=1):
        super().__init__(message)
        self.returncode = returncode


def choose_transport(name):
    """O Studio é o padrão. `cloud` só entra quando o nome é esse."""
    if name in (None, "", "studio"):
        return "studio"
    if name == "cloud":
        return "cloud"
    raise CloudTransportError(
        f"transporte {name}: use studio (padrão) ou cloud.", returncode=2)


def round_marker(n):
    """A linha exata que fecha a rodada na ata."""
    return MARKER_TEMPLATE.format(n=int(n))


def workspace_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))


def workflow_checkout(env=None):
    """O checkout do brza-workflow que tem `packages/client/cloud_runtime.py`."""
    env = os.environ if env is None else env
    candidates = []
    if env.get("BRZA_WORKFLOW"):
        candidates.append(env["BRZA_WORKFLOW"])
    candidates.append(os.path.join(os.path.dirname(workspace_root()), "brza-workflow"))
    for root in candidates:
        if os.path.isfile(os.path.join(root, "packages", "client", "cloud_runtime.py")):
            return root
    raise CloudTransportError(
        "runtime cloud: não achei packages/client/cloud_runtime.py. "
        "Faça checkout da branch builder/pln-026-pr-b no brza-workflow "
        "ao lado deste repositório, ou exporte BRZA_WORKFLOW com esse caminho. "
        "O arquivo não é copiado para a skill.")


def load_cloud_runtime(checkout):
    """Importa o módulo pelo caminho do checkout, sem copiar o arquivo."""
    path = os.path.join(checkout, "packages", "client", "cloud_runtime.py")
    spec = importlib.util.spec_from_file_location("brza_cloud_runtime", path)
    if spec is None or spec.loader is None:
        raise CloudTransportError(f"runtime cloud: não consegui importar {path}.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def persona_mode(persona):
    """`ask` no revisor; o resto abre como `agent`, e o CLI não recebe `--mode`."""
    return persona.get("modo") or "agent"


def refuse_if_undeclared(runtime, capability):
    """Sem chave ou sem `agent`, a mensagem nomeia a capacidade e o que falta."""
    runtime.require(capability)


def minutes_path(reuniao, root):
    ata = reuniao.get("ata")
    if not ata:
        raise CloudTransportError(
            "runtime cloud: o manifesto precisa do campo ata, o caminho da coordenação.")
    return ata if os.path.isabs(ata) else os.path.join(root, ata)


def cloud_workspace(reuniao):
    workspace = reuniao.get("workspace")
    if not workspace:
        raise CloudTransportError(
            "runtime cloud: o manifesto precisa de workspace, um diretório absoluto.")
    return workspace


def persona_model(persona, reuniao):
    model = persona.get("modelo") or reuniao.get("modelo")
    if not model or model == "-":
        raise CloudTransportError(
            f"runtime cloud: a persona {persona.get('nome') or '?'} precisa de modelo.")
    return model


def open_prompt(reuniao, persona):
    tema = reuniao.get("tema") or reuniao.get("id") or "reunião"
    return (
        f"Você é {persona['nome']}, {persona.get('papel') or 'persona'}, "
        f"numa reunião cujo tema é: {tema}. "
        "Não use ferramentas e não grave arquivo. Responda apenas: pronto."
    )


def round_text(reuniao, root, n):
    path = os.path.join(root, reuniao.get("dir", "."), f"rodada-{n}.md")
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as handle:
            return handle.read().strip()
    return (reuniao.get("tema") or "").strip()


def send_prompt(reuniao, persona, n, root, prior):
    heard = ""
    if prior:
        heard = "\n\nFalas anteriores desta rodada:\n\n" + "\n\n".join(prior)
    return (
        f"Você é {persona['nome']}, {persona.get('papel') or 'persona'}. "
        f"Rodada {n}. Responda em português do Brasil. "
        "Não use ferramentas e não grave arquivo.\n\n"
        f"{round_text(reuniao, root, n)}{heard}"
    )


def _tokens(turn):
    usage = turn.usage if isinstance(getattr(turn, "usage", None), dict) else {}
    return {field: usage.get(field, "ausente") for field in TOKEN_FIELDS}


def _cost(turn):
    measurement = getattr(turn, "measurement", None)
    if isinstance(measurement, dict) and "estimated_cost_usd" in measurement:
        return measurement["estimated_cost_usd"]
    return "ausente"


def _row(persona, turn_name, turn):
    return {
        "nome": persona["nome"],
        "turn": turn_name,
        "session_id": turn.session_id,
        "duration_ms": turn.duration_ms,
        "tokens": _tokens(turn),
        "result": turn.result or "",
        "cost": _cost(turn),
    }


def render_header(reuniao):
    title = reuniao.get("ata_titulo") or f"Reunião {reuniao.get('id') or 'cloud'}"
    lines = [
        "---",
        "scope:",
        "  - workspace",
        "tags:",
        "  - tooling",
        "---",
        "",
        f"# {title}",
        "",
    ]
    if reuniao.get("smoke"):
        lines.extend([
            "**SMOKE.** Esta reunião não conta para a promoção da meeting-runner.",
            "",
        ])
    note = reuniao.get("ata_nota")
    if note:
        lines.extend([note, ""])
    lines.extend(["## Pauta", "", reuniao.get("tema") or "", "", "## Personas", ""])
    lines.append("| Persona | papel | modelo | modo |")
    lines.append("| :------ | :---- | :----- | :--- |")
    for persona in reuniao.get("personas") or []:
        lines.append(
            f"| {persona['nome']} | {persona.get('papel') or '—'} | "
            f"{persona.get('modelo') or '—'} | {persona_mode(persona)} |")
    lines.append("")
    return "\n".join(lines)


def render_round(n, records, wall_ms):
    """A rodada e, na última linha, o marcador."""
    lines = [
        f"## Rodada {n}",
        "",
        f"Duração da rodada: {wall_ms} ms.",
        "",
        "| Persona | turno | session_id | duração_ms | input | output | cache_read | cache_write | reasoning | custo |",
        "| :------ | :---- | :--------- | ---------: | ----: | -----: | ---------: | ----------: | --------: | :---- |",
    ]
    for row in records:
        tokens = row["tokens"]
        lines.append(
            f"| {row['nome']} | {row['turn']} | `{row['session_id']}` | {row['duration_ms']} | "
            f"{tokens['input']} | {tokens['output']} | {tokens['cache_read']} | "
            f"{tokens['cache_write']} | {tokens['reasoning']} | {row['cost']} |")
    lines.extend(["", "## Falas", ""])
    for row in records:
        if row["turn"] != "send":
            continue
        lines.extend([f"### {row['nome']}", "", row["result"].rstrip(), ""])
    lines.extend([round_marker(n), ""])
    return "\n".join(lines)


def write_minutes(path, reuniao, n, records, wall_ms):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    block = render_round(n, records, wall_ms)
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as handle:
            existing = handle.read()
        sep = "" if existing.endswith("\n") else "\n"
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(sep + block)
        return
    with open(path, "w", encoding="utf-8") as handle:
        header = render_header(reuniao)
        if not header.endswith("\n\n"):
            header = header.rstrip("\n") + "\n\n"
        handle.write(header + block)


def make_runtime(env, log_path, timeout_s):
    module = load_cloud_runtime(workflow_checkout(env))
    return module.CloudRuntime(env=env, log_path=log_path, timeout_s=timeout_s)


def _runtime_failure(exc):
    return exc.__class__.__name__ in ("CapabilityError", "CloudTurnError", "CloudRuntimeError")


def run_round(reuniao, personas, root, n, dry=False, out=print, sessions_fn=None,
              env=None, log_path=None, timeout_s=None, runtime=None):
    """Abre cada persona e manda a rodada. `sessions_fn` é do Studio e não é chamado."""
    if dry:
        workspace = cloud_workspace(reuniao)
        for persona in personas:
            out(f"[dry-run] {persona['nome']} modo {persona_mode(persona)} "
                f"modelo {persona_model(persona, reuniao)} workspace {workspace}")
            out("  open: CloudRuntime.open")
            out(f"  send: CloudRuntime.send rodada {n}")
        out(f"[dry-run] ata: {minutes_path(reuniao, root)}")
        out(f"[dry-run] marcador: {round_marker(n)}")
        return 0
    own_runtime = runtime is None
    started = time.monotonic()
    try:
        workspace = cloud_workspace(reuniao)
        path = minutes_path(reuniao, root)
        os.makedirs(workspace, exist_ok=True)
        if runtime is None:
            timeout = reuniao.get("timeout_s", 240) if timeout_s is None else timeout_s
            if log_path is None:
                log_path = reuniao.get("log")
            runtime = make_runtime(env, log_path, timeout)
        refuse_if_undeclared(runtime, "open")
        refuse_if_undeclared(runtime, "send")
        records = []
        prior = []
        for persona in personas:
            mode = persona_mode(persona)
            model = persona_model(persona, reuniao)
            opened = runtime.open(
                persona["nome"], model, workspace, mode, open_prompt(reuniao, persona))
            records.append(_row(persona, "open", opened))
            # persona e workspace vão sempre: um send sem memória não herda o bucket.
            sent = runtime.send(
                opened.session_id, send_prompt(reuniao, persona, n, root, prior),
                persona=persona["nome"], model=model, workspace=workspace, mode=mode)
            records.append(_row(persona, "send", sent))
            prior.append(f"{persona['nome']}:\n{sent.result}")
            out(f"{persona['nome']}: {sent.session_id} · {sent.duration_ms} ms · custo {_cost(sent)}")
        wall_ms = int((time.monotonic() - started) * 1000)
        write_minutes(path, reuniao, n, records, wall_ms)
        out(f"ata: {path}")
        out(round_marker(n))
        return 0
    except CloudTransportError as exc:
        print(str(exc), file=sys.stderr)
        return exc.returncode
    except Exception as exc:
        if not _runtime_failure(exc):
            raise
        print(str(exc), file=sys.stderr)
        return getattr(exc, "returncode", 1)
    finally:
        if own_runtime and runtime is not None:
            runtime.close()


def run_cli(args, sessions_fn=None, out=print, env=None, log_path=None, timeout_s=None):
    verbs = [name for name in ("send", "close", "release", "stop", "keep_open", "status") if getattr(args, name)]
    if verbs:
        raise CloudTransportError(
            "--transport cloud usa --round N; os verbos do brza sessions ficam no transporte studio.",
            returncode=2)
    if not args.round:
        raise CloudTransportError("--transport cloud pede --round N.", returncode=2)
    root = os.path.abspath(args.root) if args.root else __import__("common").raiz_padrao()
    path = args.reuniao if os.path.isabs(args.reuniao) or not os.path.isfile(os.path.join(root, args.reuniao)) \
        else os.path.join(root, args.reuniao)
    with open(path, encoding="utf-8") as handle:
        reuniao = json.load(handle)
    try:
        import common
        personas = common.resolver_personas(reuniao, args.personas)
    except ValueError as exc:
        raise CloudTransportError(str(exc), returncode=2) from None
    return run_round(
        reuniao, personas, root, args.round, dry=args.dry_run, out=out,
        sessions_fn=sessions_fn, env=env, log_path=log_path, timeout_s=timeout_s)
