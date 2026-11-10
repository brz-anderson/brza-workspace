"""Os corredores e o argv do `brza sessions` v2: abrir, enviar, esperar, fechar e listar, sem o manifesto de reunião.

Só biblioteca padrão. Extraído de `launch_persona.py` e `wait_round.py` da `meeting-runner` (PLN-021/D1).

Os corredores (`run_sessions`, `run_brza`, `wait_brza`) rodam por `subprocess`, sem shell, com `BRZA = $BRZA_BIN ou
"brza"`; os testes os trocam por atribuição no módulo de quem os chama. `brza` ausente vira rc 127.
"""
import json
import os
import re
import shlex
import subprocess

BRZA = os.environ.get("BRZA_BIN", "brza")
MODOS_FECHAR = {"close": [], "stop": ["--force"], "keep-open": ["--keep-open"]}


def _roda(argv):
    """(rc, stdout, stderr), sem shell; `brza` ausente vira rc 127."""
    try:
        r = subprocess.run(argv, capture_output=True, text=True)
    except OSError as e:
        return 127, "", str(e)
    return r.returncode, r.stdout, r.stderr


def run_sessions(argv):
    """O corredor do `brza sessions <argv>`."""
    return _roda([BRZA, "sessions", *argv])


def run_brza(argv):
    """O corredor do `brza <argv>` (por exemplo, a leitura `orchestration worker-show`)."""
    return _roda([BRZA, *argv])


def _json(texto):
    try:
        return json.loads(texto)
    except (ValueError, TypeError):
        return None


def open_argv(name, *, agent, checkout, prompt_file, title, model=None, effort=None, rename=False):
    """O argv (sem o `brza sessions`) que abre a sessão e espera o id: `--model` só com modelo (o Antigravity abre sem)."""
    argv = [name, "--agent", agent, "--checkout", checkout, "--prompt-file", prompt_file, "--title", title, "--wait"]
    if model:
        argv += ["--model", model]
    if effort:
        argv += ["--effort", effort]
    if rename:
        argv.append("--rename")
    return argv


def send_argv(names, text=None, file=None, operation=None):
    """O argv (sem o `brza sessions`) do `send`: UMA chamada para todas as sessões, com `--text` ou `--file`."""
    if (text is None) == (file is None):
        raise ValueError("send_argv pede text ou file, um dos dois")
    argv = ["send", *names]
    argv += ["--text", text] if text is not None else ["--file", file]
    argv.append("--json")
    return argv + (["--operation", operation] if operation else [])


def wait_argv(names, timeout_s, *, any_=True, markers=()):
    """O argv (sem o `brza sessions`) do `wait`: `wait <nomes…> [--any] [--marker M …] --timeout <t> --json`."""
    argv = ["wait", *names]
    if any_:
        argv.append("--any")
    for m in markers:
        argv += ["--marker", m]
    return argv + ["--timeout", f"{max(0.0, timeout_s):g}", "--json"]


def close_argv(name, modo="close"):
    """O argv (sem o `brza sessions`) do `close` de UMA sessão; `modo`: close | stop | keep-open."""
    return ["close", name, *MODOS_FECHAR[modo], "--json"]


def interpreta_abertura(rc, out, err):
    """'aberta' | 'ja' | 'nao-abriu' | 'sem-id' | 'falha', pela saída do `brza sessions <nome>` v2."""
    texto = f"{out or ''}\n{err or ''}"
    if rc == 0:
        return "ja" if re.search(r"^running:", texto, re.M) else "aberta"
    if re.search(r"CHECK:\s+\S+ não abriu:", texto):
        return "nao-abriu"
    if re.search(r"não deu a sessão em", texto):
        return "sem-id"
    return "falha"


def wait_brza(names, timeout_s, markers=(), *, any_=True):
    """`brza sessions wait …`: (rc, dict) com `done`, `pending`, `timed_out` e `events`. `brza` ausente ou saída que não é
    JSON vira rc 127 (ou o rc do `brza`) e `{"error": …}`."""
    argv = [BRZA, "sessions", *wait_argv(names, timeout_s, any_=any_, markers=markers)]
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout_s + 60)
    except (OSError, subprocess.SubprocessError) as e:
        return 127, {"error": str(e)}
    try:
        dado = json.loads(r.stdout)
    except ValueError:
        return r.returncode or 1, {"error": f"saída sem JSON (rc {r.returncode}): {(r.stderr or r.stdout).strip()[:200]}"}
    return r.returncode, dado if isinstance(dado, dict) else {"error": "JSON inesperado"}


def list_states(names, list_json=None, cmd=None, ids=None):
    """{nome: state} de `brza sessions list --json`, só das `names`; {} se o comando ou o JSON falhar. `list_json` lê um
    arquivo no lugar do comando; `cmd` troca o comando (string, sem shell); `ids` ({nome: {id, …}}) acha a sessão pela
    linha do `list` que traz o `claude_session` ou o `provider_session` dado, no lugar do nome."""
    try:
        if list_json:
            with open(list_json, encoding="utf-8") as f:
                data = json.load(f)
        else:
            r = subprocess.run(shlex.split(cmd or f"{BRZA} sessions list --json"), capture_output=True, text=True,
                               timeout=20)
            data = json.loads(r.stdout)
    except (OSError, ValueError, subprocess.SubprocessError):
        return {}
    sess = data.get("sessions", []) if isinstance(data, dict) else []
    nomes = set(names)
    out = {s.get("name"): s.get("state") for s in sess if s.get("name") in nomes}
    for nome, quais in (ids or {}).items():
        quais = set(quais) - {None, ""}
        for s in sess:
            if quais & {s.get("claude_session"), s.get("provider_session")}:
                out[nome] = s.get("state")
    return out
