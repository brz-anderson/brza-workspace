#!/usr/bin/env python3
"""O executor do passo (PLN-021/D3): abre a sessão executora pelo `brza sessions`, espera o marcador, lê e confere a
evidência, leva-a ao plano e fecha. A coordenação não digita comando de sessão.

Uso:
    executor.py open     PLN-NNN Pn [--agent claude|codex|grok|antigravity] [--model M] [--effort E]
                                    (--checkout CAMINHO | --tree NOME [--type feat|fix|docs|chore]) [--branch B] [--no-panel] [--dry-run]
    executor.py send     PLN-NNN Pn (--text T | --file F) [--operation OP]
    executor.py wait     PLN-NNN [Pn …] [--timeout SEG] [--no-panel]
    executor.py evidence PLN-NNN Pn [--apply | --rerun] [--settle 60] [--no-panel]
    executor.py close    PLN-NNN Pn [--keep-open | --stop] [--wait-settled SEG] [--no-panel]
    executor.py status   PLN-NNN [--json]

O manifesto é `.sessions/pln-nnn/execucao.json` (na raiz do worktree do plano): por passo, a sessão, o runtime, o
checkout, a branch, o pedido, o worklog, o marcador, o estado (`aberto` → `em-curso` → `feito` | `parado` | `bloqueado` |
`falhou` → `evidencia-gravada` → `fechado`), os eventos, a evidência e a medição. O mapa de identidade (Dispatch, Run, id do
provedor) continua só no `.sessions/sessions.jsonl` da raiz comum.

`open` gera o pedido pelo `step_request.py`, cria o worklog do executor (seções `## O que se fez`, `## Desvios`,
`## Evidência`, sem marcador), abre a sessão (`--wait`) e imprime a tabela da abertura e a linha `::orca-visual` do painel.
O padrão é Claude Sonnet (a camada da implementação). "Não abriu" não se relança antes do `pending-*.json` que o `brza
sessions` cita; `running:` não reabre.

`wait` espera pelo marcador `<!-- fim-Pn: feito|parado -->` como ÚLTIMA linha do worklog. `ended_without_marker` não é fim: a
linha diz "o turno acabou sem o marcador" e a espera segue até o prazo. Saída: 0 com algum `feito` ou `parado`, 3 com
`bloqueado` (o chat pede resposta: `brza sessions read <sessão> --last`), 1 com falha, 75 no prazo.

`evidence` lê a `## Evidência` do worklog, confere cada commit (`git cat-file -e`) e roda de novo o comando marcado
`(≤ 2 min)`, e mede o `Executado` (janela da abertura ao marcador; Claude também pelos turnos do hook). Sem `--apply`, só
propõe, e a proposta NÃO roda o comando do worklog (entrada de outra sessão): `--rerun` o roda sem gravar, e o
`--apply` o roda e grava, por argv e sem shell (aceita `VAR=v` e `cd X &&` na frente, glob e `~`). O filtro só tira o que o argv
não reproduz: NÃO é segurança, a proteção é a coordenação ler a proposta antes do `--rerun` ou do `--apply`. Com `--apply`, grava a `**Evidência:**` no `### Pn` do plano, marca `[x]` só nos subpassos da linha `cobre:` (`todos` marca todos), roda o `plan_state.py --fix` e publica o
painel. Sem `cobre:`, o `--apply` não roda o comando, não grava e manda completar pelo `send`. Só se aplica depois de a coordenação ler a proposta (regra da SKILL.md). Saída 1 se algo não confere.

`close` pede o encerramento e confere o aceite (`closing` não é fechado; `--wait-settled SEG` repete a cada 5 s).

Saída: 0 ok, 1 falha, 2 uso ou plano/passo que não existe, 3 bloqueado (`wait`), 75 prazo ou estado incerto.
"""
import argparse
import datetime
import glob
import json
import os
import re
import shlex
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _kit  # noqa: E402,F401
import plan_md  # noqa: E402
import plan_panel  # noqa: E402
import plan_state  # noqa: E402
import step_request  # noqa: E402
from skillkit import measure, sessions_map  # noqa: E402
from skillkit.paths import common_root, strip_measurement  # noqa: E402
from skillkit.sessions_cli import (close_argv, interpret_open, open_argv, run_brza, run_sessions, send_argv,  # noqa: E402
                                   wait_brza, list_states)

SONNET = "claude-sonnet-5-5"
CODEX_MODEL = "gpt-6.1-sol"   # o `brza sessions` exige --model com --effort; o modelo do ~/.codex/config.toml e do smoke do PLN-017
LIVE_FLAGS = ("aberto", "em-curso", "bloqueado")
TICK = 180          # a cada ~3 min sem evento o `wait` repete a linha com a idade
MAX_WAIT_ERRORS = 5   # erros seguidos do `brza sessions wait` até desistir
WAIT_ERROR_PAUSE = 5  # segundos de pausa entre eles
RE_NO_SESSION = re.compile(r"\b(\d+) chats? abertos? se chamam ([^\s:]+)", re.I)
FAILED = ("failed", "stopped", "abandoned")
OK_FINAL = ("encerrada e aceita", "liberada")
UNCERTAIN = ("stop_unknown", "release_unknown", "release_pending")
NOISE = "worker stopped without reporting"
ATTENTION = {"question", "blocked", "decision_gate", "escalation"}
RE_MARKER = r"^<!-- fim-%s: (feito|parado) -->$"


# ---------------------------------------------------------------- relógio, saída e corredores (os testes trocam)

def iso(epoch):
    return datetime.datetime.fromtimestamp(epoch).astimezone().isoformat(timespec="seconds")


def run_git(argv):
    try:
        r = subprocess.run(["git", *argv], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError) as e:
        return 127, "", str(e)
    return r.returncode, r.stdout, r.stderr


RE_SHELL = re.compile(r"[;&|<>`$(){}\\\n\r]")


RE_CD = re.compile(r"^\s*cd\s+(\S+)\s*&&\s*(.+)$", re.S)
RE_ENV = re.compile(r"^([A-Za-z_]\w*)=(.*)$", re.S)


def parse_command(cmd):
    """(env, cwd, words) de um comando que o argv reproduz: `VAR=v` na frente (vai ao env), um `cd X &&` na frente (vai ao
    cwd), palavras e aspas. Glob e `~` sem aspas se expandem na hora de rodar. None se tiver qualquer outro operador de shell.
    Isto só tira o que o argv não reproduz: NÃO é segurança, a proteção é a leitura da proposta."""
    if not cmd:
        return None
    cwd = None
    m = RE_CD.match(cmd)
    if m:
        cwd, cmd = m.group(1).strip("'\""), m.group(2)
        if RE_SHELL.search(cwd):
            return None
    if RE_SHELL.search(cmd):
        return None
    lex = shlex.shlex(cmd, posix=False)
    lex.whitespace_split = True
    lex.commenters = ""   # `#` no meio da palavra não é comentário
    try:
        raw = list(lex)
    except ValueError:
        return None
    words = []
    for w in raw:
        if "'" in w or '"' in w:
            try:
                words.append((shlex.split(w)[0] if shlex.split(w) else "", False))
            except ValueError:
                return None
        else:
            words.append((w, True))
    env = {}
    while words and RE_ENV.match(words[0][0]):
        k, v = RE_ENV.match(words.pop(0)[0]).groups()
        env[k] = v
    return (env, cwd, words) if words else None


def run_shell(cmd, cwd, timeout=120):
    """(rc, saída) de um comando rodado de novo na conferência, por argv e sem shell; estourar o tempo vale rc 124."""
    parsed = parse_command(cmd)
    if parsed is None:
        return 2, "não é um comando que o argv reproduz: %s" % cmd
    env, sub, words = parsed
    workdir = os.path.abspath(os.path.join(cwd, os.path.expanduser(sub))) if sub else cwd
    argv = []
    for w, expand in words:
        if expand:
            w = os.path.expanduser(w)
            if re.search(r"[*?\[]", w):
                findings = sorted(glob.glob(w, root_dir=workdir))
                argv.extend(findings or [w])
                continue
        argv.append(w)
    try:
        r = subprocess.run(argv, cwd=workdir, env={**os.environ, **env}, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, "tempo esgotado (%d s)" % timeout
    except OSError as e:
        return 127, str(e)
    return r.returncode, (r.stdout + r.stderr)


class Ctx:
    """O que os testes trocam: saída, relógio e corredores."""

    def __init__(self, out=None, err=None, clock=None, sleep=None):
        self.out = out or (lambda s: print(s, flush=True))
        self.err = err or (lambda s: print(s, file=sys.stderr, flush=True))
        self.clock = clock or time.time
        self.sleep = sleep or time.sleep
        self.on_date = lambda: datetime.date.fromtimestamp(self.clock()).isoformat()


# ---------------------------------------------------------------- o manifesto

def session_name(plan_id, pid):
    n = re.search(r"\d+", plan_id).group(0)
    return "pln%s-%s" % (n, pid.lower())


def read_manifest(pl):
    m = plan_panel.read_json(plan_panel.manifest_path(pl.root, pl.id))
    m.setdefault("plan", pl.id)
    m.setdefault("steps", {})
    return m


def write_manifest(pl, m):
    m["plan"] = pl.id
    m["plan_path"] = os.path.relpath(pl.path, pl.root)
    path = plan_panel.manifest_path(pl.root, pl.id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = "%s.%d.tmp" % (path, os.getpid())
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def append_event(c, e, state, note):
    e["state"] = state
    e.setdefault("events", []).append({"at": iso(c.clock()), "state": state, "note": note})


def minutes(c, e, since=None):
    """Minutos desde `since` (ISO) ou desde a abertura."""
    ev = e.get("events") or []
    t0 = sessions_map.epoch(since or (ev[0].get("at") if ev else None))
    return None if t0 is None else max(0, int((c.clock() - t0) // 60))


def _panel(pl, c, a, png=False):
    if getattr(a, "no_panel", False):
        return
    plan_panel.emit(plan_panel.publish_safe(pl, png=True if png else None), c.out, c.err)


def last_marker(path, pid):
    """'feito' | 'parado' | None: o marcador do passo é a última linha não vazia do worklog (sem o anexo `## Medida`)."""
    try:
        with open(path, encoding="utf-8") as f:
            text = strip_measurement(f.read())
    except OSError:
        return None
    lines = [l.rstrip() for l in text.split("\n") if l.strip()]
    m = re.match(RE_MARKER % re.escape(pid), lines[-1]) if lines else None
    return m.group(1) if m else None


def has_pending_checks(pl, pid):
    """True se o `### Pn` ainda tem subpasso `[ ]`."""
    p = pl.step(pid)
    return p is not None and any(mark_text == " " for _, mark_text, _ in p.checks)


def neutralize_marker(path, pid):
    """Troca o último `<!-- fim-Pn: feito|parado -->` do worklog por um comentário que o `wait` não lê; o texto fica."""
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().split("\n")
    except OSError:
        return False
    for i in range(len(lines) - 1, -1, -1):
        m = re.match(RE_MARKER % re.escape(pid), lines[i].rstrip())
        if m:
            lines[i] = "<!-- reaberto: era fim-%s: %s -->" % (pid, m.group(1))
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            return True
    return False


def _abs(pl, path):
    return path if os.path.isabs(path) else os.path.join(pl.root, path)


# ---------------------------------------------------------------- open

WORKLOG_TEMPLATE = """---
scope:
{scope}
tags:
{tags}
---

# {pln} {pid}: {title}

Worklog do executor do passo {pid} do {pln}, criado pela coordenação em {on_date}. O executor preenche as seções abaixo; a
coordenação o confere e o commita com o plano. O marcador de fim é o comentário HTML `fim-{pid}` com `feito` ou `parado`
(o pedido dá a forma exata), última linha do arquivo, e só entra quando o passo termina.

## O que se fez

## Desvios

## Evidência
"""


def _yaml_list(v, default_value):
    item_list = v if isinstance(v, list) and v else [default_value]
    return "\n".join("  - %s" % x for x in item_list)


def create_worklog(pl, p, path, on_date):
    if os.path.exists(path):
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    txt = WORKLOG_TEMPLATE.format(scope=_yaml_list(pl.fm.get("scope"), "workspace"), tags=_yaml_list(pl.fm.get("tags"), "tooling"),
                               pln=pl.id, pid=p.id, title=p.title, on_date=on_date)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    return True


def effective_model_effort(agent, model, effort):
    """(model, effort, warning): o `brza sessions` recusa `--effort` sem `--model`. O Codex ganha o `CODEX_MODEL`; o runtime sem
    modelo padrão conhecido perde o esforço, com o aviso."""
    if model or not effort:
        return model, effort, None
    if agent == "codex":
        return CODEX_MODEL, effort, None
    return None, None, "o `brza sessions` recusa --effort sem --model e não há modelo padrão para %s: abro sem --effort" % agent


def _tree_path(output, name):
    for tok in re.findall(r"(/\S+)", output or ""):
        if os.path.basename(tok.rstrip("/")) == name:
            return tok.rstrip("/")
    return None


def _current_branch(root):
    rc, stdout, _ = run_git(["-C", root, "branch", "--show-current"])
    return stdout.strip() if rc == 0 and stdout.strip() else "workstream"


def cmd_open(a, c):
    try:
        pl = plan_md.load(a.plan)
    except plan_md.PlanNotFound as e:
        c.err("erro: %s" % e)
        return 2
    p = pl.step(a.step)
    if p is None:
        c.err("erro: o plano %s não tem o passo %s" % (pl.id, a.step))
        return 2
    pid, base = p.id, "%s-%s" % (pl.id.lower(), p.id.lower())
    m = read_manifest(pl)
    prior = m["steps"].get(pid) or {}
    if prior.get("state") in LIVE_FLAGS and not a.dry_run:
        c.err("o passo %s já tem executor %s (%s): use `wait` ou `status`; `open` só reabre passo parado, falhado ou "
              "fechado sem evidência" % (pid, prior.get("session"), prior.get("state")))
        return 1
    if (prior.get("state") == "feito" or prior.get("state") == "evidencia-gravada" or prior.get("evidence")) and not a.dry_run:
        if prior.get("state") == "feito" or not has_pending_checks(pl, pid):
            c.err("o passo %s está %s e a evidência dele já foi lida: `open` não reabre (só passo parado, falhado, fechado ou com "
                  "subpasso `[ ]` pendente); a evidência fica como está" % (pid, prior.get("state")))
            return 1
    agent = a.agent or "claude"
    model = a.model or (SONNET if agent == "claude" else None)
    model, effort, warning_text = effective_model_effort(agent, model, a.effort)
    if warning_text:
        c.err("⚠ " + warning_text)
    on_date = c.on_date()
    worklog = os.path.join(pl.root, "work", "worklogs", "%s-%s-%s.md" % (on_date, base, step_request.slug(p.title)))
    # o checkout: `brza tree` ou o dado; sem nenhum dos dois, recusa (o padrão seria o próprio brza-workspace)
    if not a.tree and not a.checkout:
        c.err("passe --checkout <worktree> ou --tree <nome>: sem eles o executor trabalharia no brza-workspace, onde o "
              "pedido proíbe o commit")
        return 2
    if a.tree:
        kind = a.type or "feat"
        branch = "%s/%s" % (kind, a.tree)
        default_value = os.path.join(os.path.dirname(step_request._repo_main(pl.root)), "brza-studio", ".worktrees", a.tree)
        try:   # A13: confere o pedido antes de criar o worktree
            step_request.build(pl, pid, worklog, default_value, branch, on_date)
        except step_request.Refusal as e:
            c.err("recusado: %s" % e)
            return 1
        argv_tree = ["tree", a.tree, "--type", kind]
        if a.dry_run:
            c.out("[dry-run] brza " + shlex.join(argv_tree))
            checkout = default_value
        else:
            rc, stdout, se = run_brza(argv_tree)
            if rc != 0:
                c.err("o `brza tree` falhou (rc %s): %s" % (rc, (se or stdout or "").strip()[:300]))
                return 1
            checkout = _tree_path(stdout, a.tree) or default_value
    else:
        checkout = os.path.abspath(a.checkout)
        branch = a.branch or _current_branch(checkout)
        if branch in ("master", "main") and not a.branch:
            branch = "feat/%s" % base   # nunca a branch principal: a do passo
    if not a.dry_run and not os.path.isdir(checkout):
        c.err("o checkout %s não existe; passe --checkout ou --tree" % checkout)
        return 1
    request = os.path.join(plan_panel.folder_sessions(pl.root, pl.id), pid, "pedido.md")
    try:
        text, info = step_request.build(pl, pid, worklog, checkout, branch, on_date)
    except step_request.Refusal as e:
        c.err("recusado: %s" % e)
        return 1
    name = session_name(pl.id, pid)
    title = "%s %s: %s" % (pl.id, pid, p.title.replace("`", ""))
    argv = open_argv(name, agent=agent, checkout=checkout, prompt_file=request, title=title, model=model, effort=effort,
                     rename=True)
    if a.dry_run:
        c.out("[dry-run] pedido: %s" % request)
        c.out("[dry-run] worklog: %s" % worklog)
        c.out("[dry-run] brza sessions " + shlex.join(argv))
        return 0
    os.makedirs(os.path.dirname(request), exist_ok=True)
    with open(request, "w", encoding="utf-8") as f:
        f.write(text)
    fresh = create_worklog(pl, p, worklog, on_date)
    rc, stdout, se = run_sessions(argv)
    res = interpret_open(rc, stdout, se)
    if res == "nao-abriu":
        c.err("%s não abriu: leia o `pending-*.json` que o `brza sessions` cita antes de relançar; não relanço.\n%s"
              % (name, ((se or "") + (stdout or "")).strip()[:400]))
        return 1
    if res == "falha":
        c.err("`brza sessions %s` falhou (rc %s): %s" % (name, rc, ((se or "") + (stdout or "")).strip()[:400]))
        return 1
    if res == "ja":
        c.err("%s já está aberta (`running:`) e o pedido novo não chegou a ela: feche com `brza sessions close %s` e rode `open` "
              "de novo; o marcador do worklog ficou como estava" % (name, name))
        return 1
    if res == "sem-id":
        c.err("⚠ %s abriu sem o id do provedor; o `wait` o grava depois. Não relance." % name)
    if not fresh:
        neutralize_marker(worklog, pid)   # só com a sessão nova aberta: o marcador do executor anterior não vale para ela
    e = {"session": name, "agent": agent, "model": model, "effort": effort, "checkout": checkout, "branch": branch,
         "request": os.path.relpath(request, pl.root), "worklog": os.path.relpath(worklog, pl.root),
         "marker": "fim-%s:" % pid, "state": "aberto", "events": [], "evidence": None, "measurement": None}
    append_event(c, e, "aberto", "open: %s%s" % (name, "" if fresh else " (worklog já existia)"))
    m["steps"][pid] = e
    write_manifest(pl, m)
    c.out("| Passo | Executor | Runtime | Modelo | Esforço | Checkout | Branch |")
    c.out("| :-- | :-- | :-- | :-- | :-- | :-- | :-- |")
    c.out("| %s | %s | %s | %s | %s | %s | %s |" % (pid, name, agent, model or "padrão do runtime", effort or "padrão", checkout, branch))
    c.out("pedido: %s" % request)
    c.out("worklog: %s" % worklog)
    _panel(pl, c, a, png=True)
    return 0


# ---------------------------------------------------------------- send

def cmd_send(a, c):
    try:
        pl = plan_md.load(a.plan)
    except plan_md.PlanNotFound as e:
        c.err("erro: %s" % e)
        return 2
    m = read_manifest(pl)
    pid = a.step.upper() if re.match(r"^p\d", a.step) else a.step
    e = m["steps"].get(pid)
    if not e:
        c.err("erro: o passo %s não tem executor aberto em %s" % (a.step, plan_panel.manifest_path(pl.root, pl.id)))
        return 2
    try:
        argv = send_argv([e["session"]], text=a.text, file=a.file, operation=a.operation)
    except ValueError as ex:
        c.err("erro: %s" % ex)
        return 2
    rc, stdout, se = run_sessions(argv)
    try:
        d = json.loads(stdout)
    except ValueError:
        d = None
    rec = (d or {}).get("receipts") if isinstance(d, dict) else None
    st = (rec[0].get("status") if rec else None) if isinstance(rec, list) and rec else None
    if rc == 75 or st in ("pending", "unknown"):
        c.err("%s: envio incerto (%s): não reenvie às cegas; confira com `status` e `brza sessions read %s --last`"
              % (e["session"], st or "rc 75", e["session"]))
        return 75
    if rc != 0:
        c.err("`brza sessions send` falhou (rc %s): %s" % (rc, (se or stdout or "").strip()[:300]))
        return 1
    c.out("%s · enviado a %s (%s)" % (pid, e["session"], st or "ok"))
    partial = e.get("state") == "evidencia-gravada" and has_pending_checks(pl, pid)   # cobre parcial: falta subpasso
    if e.get("state") in ("feito", "parado") or partial:
        neutralize_marker(_abs(pl, e["worklog"]), pid)   # o retrabalho pede um marcador novo, e o `wait` não pode devolver o velho
    fresh = "em-curso" if e.get("state") in ("bloqueado", "parado", "aberto", "feito") or partial else e.get("state")
    append_event(c, e, fresh, "send: %s" % (a.operation or "sem operation"))
    write_manifest(pl, m)
    return 0


# ---------------------------------------------------------------- wait

def wait_error_verdict(rc, error, streak, name_list):
    """(ação, mensagem, nome) para o `error` do `brza sessions wait`. Ação: `missing` (o `brza` diz "0 chats abertos se chamam
    <nome>" para um dos `name_list`: só essa sessão se perdeu, e quem chama a marca `falhou` e segue com as outras), `stop` (nome
    duplicado, rc fora de 0/1/75 ou `MAX_WAIT_ERRORS` erros seguidos) ou `retry` (pausa `WAIT_ERROR_PAUSE`)."""
    m = RE_NO_SESSION.search(error)
    if m and m.group(2) in name_list:
        if int(m.group(1)) == 0:
            return "missing", "a sessão %s não existe mais no `brza sessions` (fechada à mão?); confira `brza sessions list` e "\
                              "reabra com `open`" % m.group(2), m.group(2)
        return "stop", "o nome %s está em %s chats abertos: o `brza sessions` não sabe qual esperar; feche o que sobra" % (
            m.group(2), m.group(1)), m.group(2)
    if rc not in (0, 1, 75):
        return "stop", "o `brza sessions wait` falhou (rc %s): %s" % (rc, error), None
    if streak >= MAX_WAIT_ERRORS:
        return "stop", "o `brza sessions wait` falhou %d vezes seguidas (rc %s): %s" % (streak, rc, error), None
    return "retry", "⚠ o `brza sessions wait` falhou (rc %s, %d/%d): %s; espero %d s" % (
        rc, streak, MAX_WAIT_ERRORS, error, WAIT_ERROR_PAUSE), None


def _event_line(pid, state, c, e):
    mi = minutes(c, e)
    when = " em %d min" % mi if mi is not None else ""
    if state == "feito":
        return "%s · feito%s" % (pid, when)
    if state == "parado":
        return "%s · parado%s — o executor achou desvio que muda o D: leia o X no worklog %s" % (pid, when, e.get("worklog"))
    if state == "bloqueado":
        return "%s · bloqueado%s — o chat espera resposta: `brza sessions read %s --last`" % (pid, when, e["session"])
    return "%s · falhou%s — a sessão %s falhou; confira com `brza sessions read %s --last`" % (pid, when, e["session"], e["session"])


def cmd_wait(a, c):
    try:
        pl = plan_md.load(a.plan)
    except plan_md.PlanNotFound as e:
        c.err("erro: %s" % e)
        return 2
    m = read_manifest(pl)
    pids = [x.upper() for x in a.steps] if a.steps else [k for k, v in m["steps"].items() if v.get("state") in LIVE_FLAGS]
    missing_ids = [x for x in pids if x not in m["steps"]]
    if missing_ids or not pids:
        c.err("erro: %s" % ("sem executor aberto para %s" % ", ".join(missing_ids) if missing_ids else "nenhum executor vivo em %s"
                            % plan_panel.manifest_path(pl.root, pl.id)))
        return 2
    t0 = c.clock()
    end = t0 + a.timeout
    result_text = {}
    warned = set()
    seen = set()
    errors = 0
    last_tick = t0
    for pid in pids:
        e = m["steps"][pid]
        if e.get("state") == "aberto":
            append_event(c, e, "em-curso", "wait")
    write_manifest(pl, m)
    while True:
        for pid in pids:
            e = m["steps"][pid]
            mk = last_marker(_abs(pl, e["worklog"]), pid)
            if mk and pid not in result_text:
                result_text[pid] = mk
                append_event(c, e, mk, "marcador no worklog")
                c.out(_event_line(pid, mk, c, e))
        if result_text:
            break
        remainder = end - c.clock()
        if remainder <= 0:
            break
        snippet = min(remainder, TICK)
        name_list = {m["steps"][p]["session"]: p for p in pids}
        markers = []
        if len(pids) == 1:   # o `--marker` do brza vale para todas as sessões: com duas, o script confere sozinho
            markers = ["%s:<!-- %s" % (_abs(pl, m["steps"][pids[0]]["worklog"]), m["steps"][pids[0]]["marker"])]
        start = c.clock()
        rc, payload = wait_brza(list(name_list), snippet, markers=markers)
        if payload.get("error"):
            errors += 1
            action, msg, lost_index = wait_error_verdict(rc, payload["error"], errors, list(name_list))
            c.err(msg)
            if action == "stop":
                return 1
            if action == "missing":
                lost_name = name_list[lost_index]
                result_text[lost_name] = "falhou"
                append_event(c, m["steps"][lost_name], "falhou", "wait: sessão inexistente")
                c.out(_event_line(lost_name, "falhou", c, m["steps"][lost_name]))
                break
            c.sleep(WAIT_ERROR_PAUSE)
            continue
        errors = 0
        without_marker = False
        for ev in payload.get("events") or []:
            kind = str(ev.get("type") or "").lower().replace("-", "_")
            pl_ev = ev.get("payload") if isinstance(ev.get("payload"), dict) else {}
            if kind == "escalation" and (str(ev.get("subject") or "").strip().lower() == NOISE or pl_ev.get("stopReason") == "finished"):
                continue
            if kind in ATTENTION and (ev.get("id") or json.dumps(ev, sort_keys=True)) not in seen:
                seen.add(ev.get("id") or json.dumps(ev, sort_keys=True))
                c.out("atenção · %s%s" % (kind, (" — " + str(ev.get("subject"))) if ev.get("subject") else ""))
        for row in payload.get("done") or []:
            pid = name_list.get(row.get("name"))
            if pid is None or pid in result_text:
                continue
            e = m["steps"][pid]
            output = row.get("outcome")
            mk = last_marker(_abs(pl, e["worklog"]), pid)
            if output == "failed":
                result_text[pid] = "falhou"
            elif output == "blocked":
                result_text[pid] = "bloqueado"
            elif mk:
                result_text[pid] = mk
            else:
                without_marker = True
                if pid not in warned:
                    warned.add(pid)
                    c.out("%s · o turno acabou sem o marcador `<!-- fim-%s: … -->` como última linha; a espera segue" % (pid, pid))
                continue
            append_event(c, e, result_text[pid], "wait: %s" % output)
            c.out(_event_line(pid, result_text[pid], c, e))
        if result_text:
            break
        if without_marker:
            c.sleep(min(5, max(0, end - c.clock())))   # o `wait` volta na hora com o turno já terminado: não gira
        elif c.clock() - start < snippet and (payload.get("timed_out") or rc == 75):
            c.sleep(max(0, snippet - (c.clock() - start)))
        if c.clock() < end and not result_text and c.clock() - last_tick >= TICK:
            last_tick = c.clock()
            c.out(" · ".join("%s · em curso %s min (último evento há %s min)" % (
                p, minutes(c, m["steps"][p]) or 0, minutes(c, m["steps"][p], m["steps"][p]["events"][-1]["at"]) or 0)
                for p in pids))
    write_manifest(pl, m)
    if result_text:
        _panel(pl, c, a)
    if not result_text:
        c.out("prazo: %s sem marcador em %d s; `status` e decida, sem envio novo às cegas" % (", ".join(pids), a.timeout))
        return 75
    state_values = set(result_text.values())
    if "falhou" in state_values:
        return 1
    if "bloqueado" in state_values:
        return 3
    return 0


# ---------------------------------------------------------------- evidence

RE_ITEM = re.compile(r"^\s*(?:[-*]\s+)?(commit|comando|arquivos|desvios|cobre)\s*:\s*(.*)$", re.I)
RE_COMMIT = re.compile(r"(?:([\w.-]+)@)?\b([0-9a-f]{7,40})\b")
RE_COMMAND = re.compile(r"^`(.+?)`\s*(?:→|->)\s*(.*?)\s*(\(\s*≤\s*2\s*min\s*\))?\s*$")


def read_evidence(text):
    """A seção `## Evidência` do worklog: {commits, commands, files, deviations, waiting, raw, covers}. None sem a seção."""
    lines = strip_measurement(text).split("\n")
    start = next((i for i, l in enumerate(lines) if re.match(r"^##\s+Evidência\s*$", l)), None)
    if start is None:
        return None
    ev = {"commits": [], "commands": [], "files": [], "deviations": [], "waiting": False, "raw": [], "covers": None}
    inside = False
    for l in lines[start + 1:]:
        if re.match(r"^#{1,2}\s", l) or re.match(r"^<!-- fim-", l.strip()):
            break
        if l.strip().startswith("```"):
            inside = not inside
            continue
        if inside:
            continue
        mi = RE_ITEM.match(l)
        if not mi:
            continue
        kind, value = mi.group(1).lower(), mi.group(2).strip()
        ev["raw"].append(l.strip())
        if kind == "commit":
            if re.search(r"aguarda", value, re.I):
                ev["waiting"] = True
            for repo, sha in RE_COMMIT.findall(value):
                if re.search(r"\d", sha):
                    ev["commits"].append((repo or None, sha))
        elif kind == "comando":
            mc = RE_COMMAND.match(value.replace("\\`", "`"))
            if mc:
                ev["commands"].append({"cmd": mc.group(1), "result": mc.group(2), "rerun": bool(mc.group(3))})
        elif kind == "cobre":   # `cobre: todos` ou `cobre: 1, 3`: os subpassos que a evidência cobre
            if re.match(r"^todos\b", value, re.I) or ev["covers"] == "todos":
                ev["covers"] = "todos"   # `todos` vence; várias linhas `cobre:` se juntam
            else:
                added = [x.strip().strip("`*") for x in value.split(",") if x.strip()]
                ev["covers"] = (ev["covers"] or []) + [x for x in added if x not in (ev["covers"] or [])]
        elif kind == "arquivos":
            ev["files"] = [x.strip().strip("`") for x in value.split(",") if x.strip()]
        else:
            ev["deviations"].append(value)
    return ev


def check(ev, checkout, root, c, rerun=False, skip_reason=None):
    """Roda as conferências: [(ok, linha)]. `ok` None é "não conferido" (informativo). O comando do worklog só roda com
    `rerun` (o `--apply` ou o `--rerun`) e se for simples: o worklog é entrada de outra sessão. `skip_reason`
    `missing-covers` é a recusa do `--apply` sem `cobre:`: a linha manda voltar pelo `send`, e não repetir o `--apply`."""
    res = []
    for repo, sha in ev["commits"]:
        base = root if repo == "brza-workspace" else checkout
        rc, _, se = run_git(["-C", base, "cat-file", "-e", sha])
        cmd = "git -C %s cat-file -e %s" % (base, sha)
        res.append((rc == 0, ("confere: `%s` → ok" % cmd) if rc == 0 else "NÃO confere: `%s` → rc %s %s" % (cmd, rc, (se or "").strip()[:120])))
    for k in ev["commands"]:
        if not k["rerun"]:
            res.append((None, "não rodei `%s` (sem `(≤ 2 min)`): vale a palavra do executor: %s" % (k["cmd"], k["result"])))
            continue
        if not rerun:
            if skip_reason == "missing-covers":
                res.append((None, "não rodei `%s`: sem `cobre:`, o `--apply` não roda o comando (volte ao executor pelo `send` e peça a linha `cobre:`): "
                                  "vale a palavra do executor: %s" % (k["cmd"], k["result"])))
            else:
                res.append((None, "não rodei `%s`: a proposta não roda comando do worklog (use `--rerun` ou `--apply` depois de ler): "
                                  "vale a palavra do executor: %s" % (k["cmd"], k["result"])))
            continue
        if parse_command(k["cmd"]) is None:
            res.append((None, "não rodei `%s`: não é um comando que o argv reproduz (só `VAR=v` e `cd X &&` na frente; sem `;`, `|`, `>`, `$`, crase); vale a palavra do "
                              "executor: %s" % (k["cmd"], k["result"])))
            continue
        rc, stdout = run_shell(k["cmd"], checkout)
        tail = [l for l in stdout.strip().split("\n") if l.strip()]
        end = tail[-1].strip()[:140] if tail else "sem saída"
        res.append((rc == 0, ("confere: `%s` → %s (disse: %s)" % (k["cmd"], end, k["result"])) if rc == 0
                    else "NÃO confere: `%s` → rc %s, %s (disse: %s)" % (k["cmd"], rc, end, k["result"])))
    missing_files = [f for f in ev["files"] if not os.path.exists(os.path.join(checkout, f)) and not os.path.exists(os.path.join(root, f))]
    if ev["files"]:
        res.append((None, "arquivos: %d citados%s" % (len(ev["files"]), ("; não achei no disco: " + ", ".join(missing_files)) if missing_files else ", todos no disco")))
    return res


def line_evidence(ev):
    pieces = []
    for repo, sha in ev["commits"]:
        pieces.append("%s@%s" % (repo or "brza-studio", sha[:7]))
    if ev["waiting"] and not ev["commits"]:
        pieces.append("commit aguarda confirmação")
    for k in ev["commands"]:
        pieces.append("`%s` → %s" % (k["cmd"], k["result"]))
    if ev["files"]:
        pieces.append("arquivos: " + ", ".join(ev["files"]))
    return "**Evidência:** " + " · ".join(pieces)


def _window(c, e, pl):
    """(opened_at, end): da abertura ao marcador (o evento `feito`/`parado`, ou o mtime do worklog)."""
    ev = e.get("events") or []
    opened_at = ev[0].get("at") if ev else None
    end = next((x.get("at") for x in reversed(ev) if x.get("state") in ("feito", "parado")), None)
    if end is None:
        try:
            end = iso(os.path.getmtime(_abs(pl, e["worklog"])))
        except OSError:
            end = None
    return opened_at, end


def measures(c, pl, e, settle, measurements=None, sessions=None):
    """{text, cost_usd, window_h, turns_h}: o `Executado` proposto. Grok e Antigravity: `sem medição`."""
    agent = e.get("agent") or "claude"
    if agent not in ("claude", "codex"):
        return {"text": "sem medição", "cost_usd": None, "window_h": None, "turns_h": None}
    opened_at, end = _window(c, e, pl)
    opened_epoch, ended_epoch = sessions_map.epoch(opened_at), sessions_map.epoch(end)
    if opened_epoch is None or ended_epoch is None or ended_epoch < opened_epoch:
        return {"text": "sem medição", "cost_usd": None, "window_h": None, "turns_h": None}
    window_h = round((ended_epoch - opened_epoch) / 3600, 3)
    srows = measure.load_jsonl(sessions or sessions_map.map_file(pl.root))
    claude_ids, provider_ids = measure.session_ids(srows, e["session"])
    d0, d1 = (datetime.datetime.fromtimestamp(x).astimezone() for x in (opened_epoch, ended_epoch))
    win = measure.win_bounds(d0, d1)
    out = {"cost_usd": None, "window_h": window_h, "turns_h": None}
    if agent == "claude":
        mpath = measurements or plan_panel._find(pl.root, ".measurements/measurements.jsonl")
        limit = c.clock() + settle
        while True:
            r = measure.measure_claude(measure.load_jsonl(mpath), claude_ids, win) if claude_ids else None
            if r or not claude_ids or not os.path.isfile(mpath) or c.clock() >= limit:
                break
            c.sleep(5)
        if r:
            out["cost_usd"], out["turns_h"] = r["cost_usd"], round(r["latency_s"] / 3600, 3)
            out["text"] = "%s h (janela; %s h de turnos; US$ %.2f)" % (plan_md.format_hours(window_h), plan_md.format_hours(out["turns_h"]), r["cost_usd"])
        else:
            out["text"] = "%s h (janela; sem medição dos turnos)" % plan_md.format_hours(window_h)
    else:
        r = measure.measure_codex(os.path.expanduser("~/.codex/sessions"), provider_ids, 1, win)
        if r:
            out["turns_h"] = round(r["latency_s"] / 3600, 3)
            out["text"] = "%s h (janela; %s h do último turno Codex; sem custo medido)" % (plan_md.format_hours(window_h), plan_md.format_hours(out["turns_h"]))
        else:
            out["text"] = "%s h (janela; sem medição dos turnos)" % plan_md.format_hours(window_h)
    return out


def check_number(text):
    """O número do subpasso (`**3. Texto**` → `3`, `**4a. …**` → `4a`); None se o texto não começa por número."""
    m = re.match(r"^[\s*`]*(\d+[a-z]?)\s*[.)]", text)
    return m.group(1).lower() if m else None


def unknown_covered(p, covers):
    """Os números de `cobre:` que o passo não tem."""
    if not isinstance(covers, list):
        return []
    known = {check_number(text) for _, _, text in p.checks}
    return [x for x in covers if x.lower() not in known]


def apply_to_plan(pl, pid, line, executed_text, covers=None):
    """Grava no `### Pn`: o `Executado`, o `[x]` nos subpassos pendentes e a `**Evidência:**`. Devolve os subpassos marcados.
    `covers` é a lista de números que a evidência declara; `"todos"` marca todos os pendentes. None não marca nenhum:
    o `--apply` recusa antes de chegar aqui."""
    p = pl.step(pid)
    plan_file = p.file
    lines = list(plan_file.lines)
    if p.line_hours is not None and executed_text:
        l = lines[p.line_hours]
        mm = re.match(r"^(Estimado:\s*.*?)\s*·\s*Executado:.*$", l)
        lines[p.line_hours] = ("%s · Executado: %s" % (mm.group(1), executed_text)) if mm else "%s · Executado: %s" % (l.rstrip(), executed_text)
    marked = []
    for i, mark_text, text in p.checks:
        covered = covers == "todos" or (isinstance(covers, list) and (check_number(text) or "") in [x.lower() for x in covers])
        if mark_text == " " and covered:
            lines[i] = lines[i].replace("[ ]", "[x]", 1)
            marked.append(re.sub(r"\*\*", "", text).split("—")[0].strip())
    if p.evidence_at is not None:
        j = p.evidence_at + 1
        while j < p.section.end and lines[j].strip():
            j += 1
        lines[p.evidence_at:j] = [line]
    else:
        end = p.section.end
        while end > p.section.start + 1 and not lines[end - 1].strip():
            end -= 1
        lines[end:end] = ["", line]
    with open(plan_file.path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return marked


def cmd_evidence(a, c):
    try:
        pl = plan_md.load(a.plan)
    except plan_md.PlanNotFound as e:
        c.err("erro: %s" % e)
        return 2
    m = read_manifest(pl)
    pid = a.step.upper()
    e = m["steps"].get(pid)
    if not e:
        c.err("erro: o passo %s não tem executor aberto" % a.step)
        return 2
    wl = _abs(pl, e["worklog"])
    try:
        with open(wl, encoding="utf-8") as f:
            text = f.read()
    except OSError as ex:
        c.err("erro: não li o worklog %s: %s" % (wl, ex))
        return 1
    mk = last_marker(wl, pid)
    if mk is None:
        c.err("o worklog %s não termina em `<!-- fim-%s: feito|parado -->`: o executor não fechou; não há evidência para ler" % (wl, pid))
        return 1
    ev = read_evidence(text)
    if ev is None or not (ev["commits"] or ev["commands"] or ev["files"] or ev["waiting"]):
        c.err("o worklog %s não traz `## Evidência` com itens (`commit:`, `comando:`, `arquivos:`): volte ao executor pelo `send`" % wl)
        return 1
    # Sem `cobre:`, o `--apply` recusa mais abaixo e não grava. Não roda o comando nessa ida.
    refuse_missing_covers = bool(a.apply and ev.get("covers") is None)
    res = check(ev, e["checkout"], pl.root, c,
                rerun=bool((a.apply or getattr(a, "rerun", False)) and not refuse_missing_covers),
                skip_reason="missing-covers" if refuse_missing_covers else None)
    for _, line in res:
        c.out(line)
    bad = [l for ok, l in res if ok is False]
    line = line_evidence(ev)
    measured = measures(c, pl, e, a.settle, getattr(a, "measurements", None), getattr(a, "sessions", None))
    c.out(line)
    c.out("Executado: %s" % measured["text"])
    c.out("desvios (lidos do worklog, não gravados): %s" % ("; ".join(ev["deviations"]) if ev["deviations"] else "o executor não declarou"))
    if ev["waiting"] and not ev["commits"]:
        c.out("⚠ o executor deixou `commit: aguarda confirmação`: não há commit para conferir")
    if not plan_state.evidence_validates(line):
        c.err("a evidência não traz commit, comando com `→` nem `arquivo:linha`: não vale")
        bad.append("evidência sem prova")
    still_missing = unknown_covered(pl.step(pid), ev.get("covers"))
    if still_missing:
        c.err("`cobre:` cita o subpasso %s, que o passo %s não tem" % (", ".join(still_missing), pid))
        bad.append("cobre com subpasso inexistente")
    if ev.get("covers") is None:
        c.out("⚠ o worklog não traz `cobre:`; o `--apply` não grava. Volte ao executor pelo `send` e peça a linha `cobre:`.")
    else:
        c.out("cobre: %s" % (ev["covers"] if ev["covers"] == "todos" else ", ".join(ev["covers"])))
    if bad:
        c.err("não confere (%d): volte ao executor pelo `send`; o passo não fecha" % len(bad))
        return 1
    if not a.apply:
        if ev.get("covers") is None:
            c.out("proposta: não grave. Volte ao executor pelo `send` e peça a linha `cobre:`.")
        else:
            c.out("proposta: leia e rode `evidence %s %s --apply` para gravar no plano" % (pl.id, pid))
        return 0
    if mk != "feito":
        c.err("o marcador é `parado`: o executor achou desvio que muda o D; leve o X à rodada, não grave o passo como feito")
        return 1
    if ev.get("covers") is None:
        c.err("sem `cobre:`, o `--apply` não grava. Volte ao executor pelo `send` e peça a linha `cobre:`.")
        return 1
    executed_text = measured["text"]
    marked = apply_to_plan(pl, pid, line, executed_text, ev.get("covers"))
    changed = plan_state.fix_hours(pl.path)
    e["evidence"] = {"line": line, "executed": executed_text, "deviations": ev["deviations"], "recorded_at": iso(c.clock()),
                      "checks": [l for _, l in res]}
    e["measurement"] = {"cost_usd": measured["cost_usd"], "window_h": measured["window_h"], "turns_h": measured["turns_h"]}
    append_event(c, e, "evidencia-gravada", "evidence --apply")
    write_manifest(pl, m)
    c.out("gravado em %s: `### %s`, %d subpasso(s) marcados, Executado: %s" % (os.path.relpath(pl.path, pl.root), pid, len(marked), executed_text))
    c.out("--fix: %s" % (", ".join(changed) if changed else "as horas já conferiam"))
    prob = [p for p in plan_state.state(pl.path)["problems"] if p["level"] == "erro"]
    for p in prob:
        c.err("plan_state: %s %s: %s" % (p["code"], p["where"], p["msg"]))
    _panel(pl, c, a)
    return 0


# ---------------------------------------------------------------- close

def verdict(show):
    """(veredito, campos) do JSON do `worker-show --full`, com ou sem o envelope `{"ok", "result"}`."""
    r = show.get("result") if isinstance(show.get("result"), dict) else show
    d, w, tr = r.get("dispatch") or {}, r.get("worker") or {}, r.get("terminalResource") or {}
    cc = {"state": w.get("state"), "stage": w.get("stage"), "completedAt": d.get("completedAt"),
          "releaseState": tr.get("releaseState"), "retainedReason": tr.get("retainedReason")}
    if cc["releaseState"] == "released":
        v = "liberada (falhou)" if cc["state"] == "failed" else "liberada"
    elif cc["state"] in FAILED:
        v = "falhou"
    elif cc["state"] == "succeeded" and cc["stage"] == "settled" and cc["releaseState"] == "retained":
        v = "encerrada, retida (%s): não fecha sozinha" % (cc["retainedReason"] or "motivo não informado")
    elif cc["state"] == "succeeded" and cc["stage"] == "settled" and cc["completedAt"]:
        v = "encerrada e aceita"
    else:
        v = "ativa"
    return v, cc


def _lookup(pl, name):
    entry = sessions_map.load_map(pl.root).get(name) or {}
    d = entry.get("dispatch")
    if not d:
        return None, "sem Dispatch no mapa: nada a conferir"
    rc, stdout, se = run_brza(["orchestration", "worker-show", "--dispatch", d, "--full", "--json"])
    try:
        show = json.loads(stdout)
    except ValueError:
        show = None
    if rc != 0 or not isinstance(show, dict):
        return None, "worker-show falhou (rc %s): %s" % (rc, (se or stdout or "").strip()[:200])
    return verdict(show)[0], None


def cmd_close(a, c):
    try:
        pl = plan_md.load(a.plan)
    except plan_md.PlanNotFound as e:
        c.err("erro: %s" % e)
        return 2
    m = read_manifest(pl)
    pid = a.step.upper()
    e = m["steps"].get(pid)
    if not e:
        c.err("erro: o passo %s não tem executor aberto" % a.step)
        return 2
    name = e["session"]
    mode = "keep-open" if a.keep_open else "stop" if a.stop else "close"
    rc, stdout, se = run_sessions(close_argv(name, mode))
    try:
        d = json.loads(stdout)
    except ValueError:
        d = None
    if isinstance(d, dict) and isinstance(d.get("results"), list) and d["results"]:
        d = d["results"][0]
    if not isinstance(d, dict):
        c.err("%s: sem JSON do close (rc %s): %s; não repita; confira com `status`" % (name, rc, (se or stdout or "").strip()[:300]))
        return rc or 1
    st = d.get("status")
    if st in UNCERTAIN:
        c.err("%s: incerto (%s): não está fechada; não repita" % (name, st))
        return 75
    if st == "refused" or "error" in d:
        c.err("%s: recusado: %s" % (name, d.get("error") or d))
        return 1
    if st == "kept_open":
        c.out("%s · mantida aberta (kept_open); não fecha sozinha" % pid)
        return 0
    if st == "closing":
        c.out("%s · pedido de encerramento enviado; NÃO está fechada (closing)" % pid)
    if a.wait_settled:
        end = c.clock() + a.wait_settled
    else:
        end = None
    v = None
    while True:
        v, reason = _lookup(pl, name)
        if v in OK_FINAL or v in ("falhou", "liberada (falhou)"):
            break
        if end is None or c.clock() >= end:
            break
        c.sleep(5)
    if v in OK_FINAL:
        if e.get("state") != "evidencia-gravada":
            c.err("⚠ %s fechada sem a evidência aplicada ao plano (estado %s)" % (pid, e.get("state")))
        append_event(c, e, "fechado", "close: %s" % v)
        write_manifest(pl, m)
        c.out("%s · encerrada e aceita" % pid if v == "encerrada e aceita" else "%s · %s" % (pid, v))
        _panel(pl, c, a, png=True)
        return 0
    if v in ("falhou", "liberada (falhou)"):
        c.err("%s · a sessão falhou (%s)" % (pid, v))
        return 1
    c.out("%s · %s" % (pid, ("não encerrada: " + v) if v else reason))
    return 75 if end is not None else 0


# ---------------------------------------------------------------- status

def cmd_status(a, c):
    try:
        pl = plan_md.load(a.plan)
    except plan_md.PlanNotFound as e:
        c.err("erro: %s" % e)
        return 2
    m = read_manifest(pl)
    if not m["steps"]:
        c.out("%s · sem executor aberto" % pl.id)
        return 0
    state_values = list_states([e["session"] for e in m["steps"].values()])
    lines = []
    for pid, e in m["steps"].items():
        ev = e.get("events") or []
        lines.append({"step": pid, "session": e["session"], "state": e.get("state"), "agent": e.get("agent"),
                       "open_for_min": minutes(c, e), "last_event_for_min": minutes(c, e, ev[-1]["at"]) if ev else None,
                       "last_event": ev[-1] if ev else None, "session_state": state_values.get(e["session"]),
                       "worklog": e.get("worklog"), "evidence": bool(e.get("evidence"))})
    if a.json:
        c.out(json.dumps({"plan": pl.id, "steps": lines}, ensure_ascii=False, indent=2))
        return 0
    for l in lines:
        c.out("%s · %s · %s · aberto há %s min · último evento há %s min · sessão: %s%s" % (
            l["step"], l["session"], l["state"], l["open_for_min"], l["last_event_for_min"],
            l["session_state"] or "?", " · evidência gravada" if l["evidence"] else ""))
    return 0


# ---------------------------------------------------------------- CLI

def main(argv=None, *, out=None, err=None, clock=None, sleep=None):
    ap = argparse.ArgumentParser(prog="executor.py", description="as sessões executoras dos passos do plano")
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("open")
    o.add_argument("plan")
    o.add_argument("step")
    o.add_argument("--agent", choices=("claude", "codex", "grok", "antigravity"))
    o.add_argument("--model")
    o.add_argument("--effort")
    g = o.add_mutually_exclusive_group()
    g.add_argument("--checkout")
    g.add_argument("--tree")
    o.add_argument("--type", choices=("feat", "fix", "docs", "chore"))
    o.add_argument("--branch", help="a branch do checkout dado (o `--tree` deduz <tipo>/<nome>)")
    o.add_argument("--no-panel", action="store_true")
    o.add_argument("--dry-run", action="store_true")
    s = sub.add_parser("send")
    s.add_argument("plan")
    s.add_argument("step")
    gs = s.add_mutually_exclusive_group(required=True)
    gs.add_argument("--text")
    gs.add_argument("--file")
    s.add_argument("--operation")
    w = sub.add_parser("wait")
    w.add_argument("plan")
    w.add_argument("steps", nargs="*")
    w.add_argument("--timeout", type=float, default=1800)
    w.add_argument("--no-panel", action="store_true")
    ev = sub.add_parser("evidence")
    ev.add_argument("plan")
    ev.add_argument("step")
    ev.add_argument("--apply", action="store_true")
    ev.add_argument("--rerun", action="store_true", help="roda os comandos `(≤ 2 min)` do worklog, só os simples, sem gravar")
    ev.add_argument("--settle", type=float, default=60)
    ev.add_argument("--no-panel", action="store_true")
    ev.add_argument("--measurements")
    ev.add_argument("--sessions")
    cl = sub.add_parser("close")
    cl.add_argument("plan")
    cl.add_argument("step")
    gc = cl.add_mutually_exclusive_group()
    gc.add_argument("--keep-open", action="store_true")
    gc.add_argument("--stop", action="store_true")
    cl.add_argument("--wait-settled", type=float, default=0, metavar="SEG")
    cl.add_argument("--no-panel", action="store_true")
    st = sub.add_parser("status")
    st.add_argument("plan")
    st.add_argument("--json", action="store_true")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    c = Ctx(out, err, clock, sleep)
    return {"open": cmd_open, "send": cmd_send, "wait": cmd_wait, "evidence": cmd_evidence, "close": cmd_close,
            "status": cmd_status}[a.cmd](a, c)


if __name__ == "__main__":
    sys.exit(main())
