#!/usr/bin/env python3
"""Transporte cloud do meeting-runner.

O padrão continua o `brza sessions` do Studio, em `launch_persona.py`.
Este módulo só entra com `--transport cloud`. Cada persona abre com
`CloudRuntime.open` e recebe a rodada com `send`. O `agent -p` volta
síncrono. A ata da coordenação ganha o marcador `<!-- fim-rodada-N -->`.

O `cloud_runtime.py` é importado de `BRZA_WORKFLOW_DIR`, pelo caminho
`packages/client/bin/cloud_runtime.py`, junto com a porta `agent_runtime`. Não há
cópia na skill e o texto não fixa branch. `open` recebe o spec e `send` recebe
`session_id` e o prompt. O `close` apaga o home da persona.
"""
import importlib.util
import json
import os
import subprocess
import sys
import time
import unicodedata

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


def workflow_checkout(env=None):
    """O checkout do brza-workflow. Só `BRZA_WORKFLOW_DIR` aponta o caminho."""
    env = os.environ if env is None else env
    root = (env.get("BRZA_WORKFLOW_DIR") or "").strip()
    if not root:
        raise CloudTransportError(
            "runtime cloud: defina BRZA_WORKFLOW_DIR com o caminho do checkout do "
            "brza-workflow que contém packages/client/bin/cloud_runtime.py. "
            "O arquivo não é copiado para a skill.")
    if not os.path.isdir(root):
        raise CloudTransportError(
            f"runtime cloud: BRZA_WORKFLOW_DIR={root} não é um diretório. "
            "Aponte para o checkout do brza-workflow.")
    if not os.path.isfile(os.path.join(root, "packages", "client", "bin", "cloud_runtime.py")):
        raise CloudTransportError(
            f"runtime cloud: {root} não contém packages/client/bin/cloud_runtime.py. "
            "Aponte BRZA_WORKFLOW_DIR para o checkout do workflow.")
    return root


def _exec_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise CloudTransportError(f"runtime cloud: não consegui importar {path}.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_cloud_runtime(checkout):
    """Importa a porta e o módulo pelo caminho do checkout, sem copiar o arquivo."""
    bindir = os.path.join(checkout, "packages", "client", "bin")
    runtime_bin = os.path.join(checkout, "bin")
    port_path = os.path.join(bindir, "agent_runtime.py")
    path = os.path.join(bindir, "cloud_runtime.py")
    runtime_path = os.path.join(runtime_bin, "brza_runtime.py")
    if not os.path.isfile(port_path):
        raise CloudTransportError(
            "runtime cloud: não achei a porta agent_runtime em "
            f"{port_path}. BRZA_WORKFLOW_DIR precisa do checkout com "
            "packages/client/bin/agent_runtime.py.")
    if not os.path.isfile(path):
        raise CloudTransportError(
            f"runtime cloud: não achei {path}. BRZA_WORKFLOW_DIR precisa do checkout "
            "com packages/client/bin/cloud_runtime.py.")
    if not os.path.isfile(runtime_path):
        raise CloudTransportError(
            f"runtime cloud: não achei {runtime_path}. A porta agent_runtime importa esse módulo. "
            "BRZA_WORKFLOW_DIR precisa do checkout completo do brza-workflow.")
    for directory in (runtime_bin, bindir):
        if directory not in sys.path:
            sys.path.insert(0, directory)
    port = _exec_module("agent_runtime", port_path)
    if "open" not in getattr(port, "CAPABILITIES", ()):
        raise CloudTransportError(
            "runtime cloud: a porta agent_runtime não declara a capacidade open. "
            f"O checkout é {checkout}.")
    module = _exec_module("cloud_runtime", path)
    runtime_cls = getattr(module, "CloudRuntime", None)
    if runtime_cls is None or not callable(getattr(runtime_cls, "open", None)):
        raise CloudTransportError(
            "runtime cloud: packages/client/bin/cloud_runtime.py não expõe a capacidade open. "
            f"O checkout é {checkout}.")
    return module


def workflow_sha(checkout):
    """O SHA do checkout enquanto o módulo não está na master do workflow."""
    try:
        sha = subprocess.check_output(
            ["git", "-C", checkout, "rev-parse", "HEAD"],
            text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    on_master = subprocess.call(
        ["git", "-C", checkout, "cat-file", "-e", "origin/master:packages/client/bin/cloud_runtime.py"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
    if on_master:
        return None
    return sha or None


def _fold(text):
    normalized = unicodedata.normalize("NFKD", text or "")
    return "".join(ch for ch in normalized if not unicodedata.combining(ch)).casefold()


def persona_mode(persona):
    """`ask` quando o manifesto diz; o resto abre como `agent`, e o CLI não recebe `--mode`."""
    return persona.get("modo") or "agent"


def role_is_critic(persona):
    """O papel decide. O nome da persona não entra."""
    words = _fold(persona.get("papel")).replace("/", " ").replace("-", " ").split()
    return any(word.strip(".,;:()[]") in {"critica", "critico", "revisor", "revisora"}
               or word.startswith("critic") or word.startswith("revisor") for word in words)


def require_critic_mode(persona):
    """Papel de crítica sem `modo: ask` para antes do `agent`."""
    if not role_is_critic(persona):
        return
    if _fold(persona.get("modo")) == "ask":
        return
    nome = persona.get("nome") or "?"
    raise CloudTransportError(
        f"runtime cloud: a persona {nome} tem papel de crítica e precisa de modo ask. "
        "O agent não foi chamado.",
        returncode=1)


def refuse_if_undeclared(runtime, capability):
    """Sem chave ou sem `agent`, a mensagem nomeia a capacidade e o que falta."""
    if capability in runtime.capabilities():
        return
    hinted = getattr(runtime, "_require_turn", None)
    if hinted is not None:
        hinted(capability)
        return
    module = sys.modules.get(runtime.__class__.__module__)
    require = getattr(module, "require_capability", None) if module else None
    if require is None:
        runtime.require(capability)
        return
    require(runtime, capability)


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


def render_header(reuniao, workflow_sha=None):
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
            "**SMOKE.** Esta reunião não conta para a promoção da meeting-runner. "
            "As duas posições ficam registradas. O modelo padrão não muda por causa dela.",
            "",
        ])
    if workflow_sha:
        lines.extend([
            f"CloudRuntime: `{workflow_sha}` em `packages/client/bin/cloud_runtime.py`, "
            "ainda fora da master do brza-workflow.",
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


def render_round(n, records, wall_ms, failure=None):
    """A rodada. O marcador só entra quando a rodada termina sem falha."""
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
    speeches = [row for row in records if row["turn"] == "send"]
    if speeches:
        lines.extend(["", "## Falas", ""])
        for row in speeches:
            lines.extend([f"### {row['nome']}", "", row["result"].rstrip(), ""])
    if failure:
        nome, message = failure
        lines.extend(["", "## Erro", "", f"A persona {nome} falhou: {message}", ""])
        return "\n".join(lines)
    lines.extend(["", round_marker(n), ""])
    return "\n".join(lines)


def write_minutes(path, reuniao, n, records, wall_ms, failure=None, workflow_sha=None):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    block = render_round(n, records, wall_ms, failure=failure)
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as handle:
            existing = handle.read()
        sep = "" if existing.endswith("\n") else "\n"
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(sep + block)
        return
    with open(path, "w", encoding="utf-8") as handle:
        header = render_header(reuniao, workflow_sha=workflow_sha)
        if not header.endswith("\n\n"):
            header = header.rstrip("\n") + "\n\n"
        handle.write(header + block)


def make_runtime(env, log_path, timeout_s):
    checkout = workflow_checkout(env)
    module = load_cloud_runtime(checkout)
    runtime = module.CloudRuntime(env=env, log_path=log_path, timeout_s=timeout_s)
    return runtime, workflow_sha(checkout)


def _runtime_failure(exc):
    return exc.__class__.__name__ in (
        "CapabilityError", "CloudTurnError", "CloudRuntimeError", "MissingCapability", "BrzaError")


def _fail_mid_round(path, reuniao, n, records, started, persona, exc, workflow_sha=None):
    """Grava as falas já feitas e o erro. A rodada incompleta não leva o marcador."""
    wall_ms = int((time.monotonic() - started) * 1000)
    nome = persona.get("nome") or "?"
    write_minutes(path, reuniao, n, records, wall_ms, failure=(nome, str(exc)),
                  workflow_sha=workflow_sha)
    print(f"{nome}: {exc}", file=sys.stderr)
    code = getattr(exc, "returncode", 1)
    return code if code else 1


def run_round(reuniao, personas, root, n, dry=False, out=print, sessions_fn=None,
              env=None, log_path=None, timeout_s=None, runtime=None):
    """Abre cada persona e manda a rodada. `sessions_fn` é do Studio e não é chamado."""
    try:
        for persona in personas:
            require_critic_mode(persona)
    except CloudTransportError as exc:
        print(str(exc), file=sys.stderr)
        return exc.returncode if exc.returncode else 1
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
    runtime_ready = False
    try:
        workspace = cloud_workspace(reuniao)
        path = minutes_path(reuniao, root)
        os.makedirs(workspace, exist_ok=True)
        used_sha = None
        if runtime is None:
            timeout = reuniao.get("timeout_s", 240) if timeout_s is None else timeout_s
            if log_path is None:
                log_path = reuniao.get("log")
            runtime, used_sha = make_runtime(env, log_path, timeout)
        runtime_ready = True
        refuse_if_undeclared(runtime, "open")
        refuse_if_undeclared(runtime, "send")
        records = []
        prior = []
        for persona in personas:
            try:
                mode = persona_mode(persona)
                model = persona_model(persona, reuniao)
                opened = runtime.open({
                    "persona": persona["nome"],
                    "model": model,
                    "workspace": workspace,
                    "mode": mode,
                    "prompt": open_prompt(reuniao, persona),
                })
                records.append(_row(persona, "open", opened))
                sent = runtime.send(
                    opened.session_id, send_prompt(reuniao, persona, n, root, prior))
                records.append(_row(persona, "send", sent))
                prior.append(f"{persona['nome']}:\n{sent.result}")
                out(f"{persona['nome']}: {sent.session_id} · {sent.duration_ms} ms · custo {_cost(sent)}")
            except CloudTransportError as exc:
                return _fail_mid_round(
                    path, reuniao, n, records, started, persona, exc, workflow_sha=used_sha)
            except Exception as exc:
                if not _runtime_failure(exc):
                    raise
                return _fail_mid_round(
                    path, reuniao, n, records, started, persona, exc, workflow_sha=used_sha)
        wall_ms = int((time.monotonic() - started) * 1000)
        write_minutes(path, reuniao, n, records, wall_ms, workflow_sha=used_sha)
        out(f"ata: {path}")
        out(round_marker(n))
        return 0
    except CloudTransportError as exc:
        print(str(exc), file=sys.stderr)
        return exc.returncode if exc.returncode else 1
    except Exception as exc:
        if not _runtime_failure(exc):
            raise
        print(str(exc), file=sys.stderr)
        code = getattr(exc, "returncode", 1)
        return code if code else 1
    finally:
        if own_runtime and runtime_ready and runtime is not None:
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
