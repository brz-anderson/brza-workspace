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
não reproduz: NÃO é segurança, a proteção é a coordenação ler a proposta antes do `--rerun` ou do `--apply`. Com `--apply`, grava a `**Evidência:**` no `### Pn` do plano, marca `[x]`, roda o `plan_state.py --fix` e publica o
painel. Só se aplica depois de a coordenação ler a proposta (regra da SKILL.md). Saída 1 se algo não confere.

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

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import _kit  # noqa: E402,F401
import plan_md  # noqa: E402
import plan_panel  # noqa: E402
import plan_state  # noqa: E402
import step_request  # noqa: E402
from skillkit import measure, sessions_map  # noqa: E402
from skillkit.paths import common_root, corta_medida  # noqa: E402
from skillkit.sessions_cli import (close_argv, interpreta_abertura, open_argv, run_brza, run_sessions, send_argv,  # noqa: E402
                                   wait_brza, list_states)

SONNET = "claude-sonnet-5-5"
CODEX_MODEL = "gpt-6.1-sol"   # o `brza sessions` exige --model com --effort; o modelo do ~/.codex/config.toml e do smoke do PLN-017
VIVOS = ("aberto", "em-curso", "bloqueado")
BATIDA = 180          # a cada ~3 min sem evento o `wait` repete a linha com a idade
MAX_WAIT_ERRORS = 5   # erros seguidos do `brza sessions wait` até desistir
WAIT_ERROR_PAUSE = 5  # segundos de pausa entre eles
RE_NO_SESSION = re.compile(r"\b(\d+) chats? abertos? se chamam ([^\s:]+)", re.I)
FALHOU = ("failed", "stopped", "abandoned")
OK_FINAL = ("encerrada e aceita", "liberada")
INCERTOS = ("stop_unknown", "release_unknown", "release_pending")
RUIDO = "worker stopped without reporting"
ATENCAO = {"question", "blocked", "decision_gate", "escalation"}
RE_MARCADOR = r"^<!-- fim-%s: (feito|parado) -->$"


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
                achados = sorted(glob.glob(w, root_dir=workdir))
                argv.extend(achados or [w])
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
        self.hoje = lambda: datetime.date.fromtimestamp(self.clock()).isoformat()


# ---------------------------------------------------------------- o manifesto

def sessao_nome(plan_id, pid):
    n = re.search(r"\d+", plan_id).group(0)
    return "pln%s-%s" % (n, pid.lower())


def le_manifesto(pl):
    m = plan_panel.le_json(plan_panel.manifesto_path(pl.raiz, pl.id))
    m.setdefault("plano", pl.id)
    m.setdefault("passos", {})
    return m


def salva_manifesto(pl, m):
    m["plano"] = pl.id
    m["plano_path"] = os.path.relpath(pl.path, pl.raiz)
    path = plan_panel.manifesto_path(pl.raiz, pl.id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = "%s.%d.tmp" % (path, os.getpid())
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def evento(c, e, estado, nota):
    e["estado"] = estado
    e.setdefault("eventos", []).append({"at": iso(c.clock()), "estado": estado, "nota": nota})


def minutos(c, e, desde=None):
    """Minutos desde `desde` (ISO) ou desde a abertura."""
    ev = e.get("eventos") or []
    t0 = sessions_map.epoch(desde or (ev[0].get("at") if ev else None))
    return None if t0 is None else max(0, int((c.clock() - t0) // 60))


def _painel(pl, c, a, png=False):
    if getattr(a, "no_panel", False):
        return
    plan_panel.emite(plan_panel.publica_seguro(pl, png=True if png else None), c.out, c.err)


def ultimo_marcador(path, pid):
    """'feito' | 'parado' | None: o marcador do passo é a última linha não vazia do worklog (sem o anexo `## Medida`)."""
    try:
        with open(path, encoding="utf-8") as f:
            texto = corta_medida(f.read())
    except OSError:
        return None
    linhas = [l.rstrip() for l in texto.split("\n") if l.strip()]
    m = re.match(RE_MARCADOR % re.escape(pid), linhas[-1]) if linhas else None
    return m.group(1) if m else None


def has_pending_checks(pl, pid):
    """True se o `### Pn` ainda tem subpasso `[ ]`."""
    p = pl.passo(pid)
    return p is not None and any(marca == " " for _, marca, _ in p.checks)


def neutraliza_marcador(path, pid):
    """Troca o último `<!-- fim-Pn: feito|parado -->` do worklog por um comentário que o `wait` não lê; o texto fica."""
    try:
        with open(path, encoding="utf-8") as f:
            linhas = f.read().split("\n")
    except OSError:
        return False
    for i in range(len(linhas) - 1, -1, -1):
        m = re.match(RE_MARCADOR % re.escape(pid), linhas[i].rstrip())
        if m:
            linhas[i] = "<!-- reaberto: era fim-%s: %s -->" % (pid, m.group(1))
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(linhas))
            return True
    return False


def _abs(pl, caminho):
    return caminho if os.path.isabs(caminho) else os.path.join(pl.raiz, caminho)


# ---------------------------------------------------------------- open

MOLDE_WORKLOG = """---
scope:
{scope}
tags:
{tags}
---

# {pln} {pid}: {titulo}

Worklog do executor do passo {pid} do {pln}, criado pela coordenação em {hoje}. O executor preenche as seções abaixo; a
coordenação o confere e o commita com o plano. O marcador de fim é o comentário HTML `fim-{pid}` com `feito` ou `parado`
(o pedido dá a forma exata), última linha do arquivo, e só entra quando o passo termina.

## O que se fez

## Desvios

## Evidência
"""


def _lista_yaml(v, padrao):
    itens = v if isinstance(v, list) and v else [padrao]
    return "\n".join("  - %s" % x for x in itens)


def cria_worklog(pl, p, path, hoje):
    if os.path.exists(path):
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    txt = MOLDE_WORKLOG.format(scope=_lista_yaml(pl.fm.get("scope"), "workspace"), tags=_lista_yaml(pl.fm.get("tags"), "tooling"),
                               pln=pl.id, pid=p.id, titulo=p.titulo, hoje=hoje)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    return True


def effective_model_effort(agent, model, effort):
    """(model, effort, aviso): o `brza sessions` recusa `--effort` sem `--model`. O Codex ganha o `CODEX_MODEL`; o runtime sem
    modelo padrão conhecido perde o esforço, com o aviso."""
    if model or not effort:
        return model, effort, None
    if agent == "codex":
        return CODEX_MODEL, effort, None
    return None, None, "o `brza sessions` recusa --effort sem --model e não há modelo padrão para %s: abro sem --effort" % agent


def _caminho_da_arvore(saida, nome):
    for tok in re.findall(r"(/\S+)", saida or ""):
        if os.path.basename(tok.rstrip("/")) == nome:
            return tok.rstrip("/")
    return None


def _branch_atual(raiz):
    rc, so, _ = run_git(["-C", raiz, "branch", "--show-current"])
    return so.strip() if rc == 0 and so.strip() else "workstream"


def cmd_open(a, c):
    try:
        pl = plan_md.carrega(a.plano)
    except plan_md.PlanoNaoEncontrado as e:
        c.err("erro: %s" % e)
        return 2
    p = pl.passo(a.passo)
    if p is None:
        c.err("erro: o plano %s não tem o passo %s" % (pl.id, a.passo))
        return 2
    pid, base = p.id, "%s-%s" % (pl.id.lower(), p.id.lower())
    m = le_manifesto(pl)
    ant = m["passos"].get(pid) or {}
    if ant.get("estado") in VIVOS and not a.dry_run:
        c.err("o passo %s já tem executor %s (%s): use `wait` ou `status`; `open` só reabre passo parado, falhado ou "
              "fechado sem evidência" % (pid, ant.get("sessao"), ant.get("estado")))
        return 1
    if (ant.get("estado") == "feito" or ant.get("estado") == "evidencia-gravada" or ant.get("evidencia")) and not a.dry_run:
        if ant.get("estado") == "feito" or not has_pending_checks(pl, pid):
            c.err("o passo %s está %s e a evidência dele já foi lida: `open` não reabre (só passo parado, falhado, fechado ou com "
                  "subpasso `[ ]` pendente); a evidência fica como está" % (pid, ant.get("estado")))
            return 1
    agent = a.agent or "claude"
    model = a.model or (SONNET if agent == "claude" else None)
    model, effort, aviso = effective_model_effort(agent, model, a.effort)
    if aviso:
        c.err("⚠ " + aviso)
    hoje = c.hoje()
    worklog = os.path.join(pl.raiz, "work", "worklogs", "%s-%s-%s.md" % (hoje, base, step_request.slug(p.titulo)))
    # o checkout: `brza tree` ou o dado; sem nenhum dos dois, recusa (o padrão seria o próprio brza-workspace)
    if not a.tree and not a.checkout:
        c.err("passe --checkout <worktree> ou --tree <nome>: sem eles o executor trabalharia no brza-workspace, onde o "
              "pedido proíbe o commit")
        return 2
    if a.tree:
        tipo = a.type or "feat"
        branch = "%s/%s" % (tipo, a.tree)
        padrao = os.path.join(os.path.dirname(step_request._repo_principal(pl.raiz)), "brza-studio", ".worktrees", a.tree)
        try:   # A13: confere o pedido antes de criar o worktree
            step_request.monta(pl, pid, worklog, padrao, branch, hoje)
        except step_request.Recusa as e:
            c.err("recusado: %s" % e)
            return 1
        argv_tree = ["tree", a.tree, "--type", tipo]
        if a.dry_run:
            c.out("[dry-run] brza " + shlex.join(argv_tree))
            checkout = padrao
        else:
            rc, so, se = run_brza(argv_tree)
            if rc != 0:
                c.err("o `brza tree` falhou (rc %s): %s" % (rc, (se or so or "").strip()[:300]))
                return 1
            checkout = _caminho_da_arvore(so, a.tree) or padrao
    else:
        checkout = os.path.abspath(a.checkout)
        branch = a.branch or _branch_atual(checkout)
        if branch in ("master", "main") and not a.branch:
            branch = "feat/%s" % base   # nunca a branch principal: a do passo
    if not a.dry_run and not os.path.isdir(checkout):
        c.err("o checkout %s não existe; passe --checkout ou --tree" % checkout)
        return 1
    pedido = os.path.join(plan_panel.pasta_sessoes(pl.raiz, pl.id), pid, "pedido.md")
    try:
        texto, info = step_request.monta(pl, pid, worklog, checkout, branch, hoje)
    except step_request.Recusa as e:
        c.err("recusado: %s" % e)
        return 1
    nome = sessao_nome(pl.id, pid)
    titulo = "%s %s: %s" % (pl.id, pid, p.titulo.replace("`", ""))
    argv = open_argv(nome, agent=agent, checkout=checkout, prompt_file=pedido, title=titulo, model=model, effort=effort,
                     rename=True)
    if a.dry_run:
        c.out("[dry-run] pedido: %s" % pedido)
        c.out("[dry-run] worklog: %s" % worklog)
        c.out("[dry-run] brza sessions " + shlex.join(argv))
        return 0
    os.makedirs(os.path.dirname(pedido), exist_ok=True)
    with open(pedido, "w", encoding="utf-8") as f:
        f.write(texto)
    novo = cria_worklog(pl, p, worklog, hoje)
    rc, so, se = run_sessions(argv)
    res = interpreta_abertura(rc, so, se)
    if res == "nao-abriu":
        c.err("%s não abriu: leia o `pending-*.json` que o `brza sessions` cita antes de relançar; não relanço.\n%s"
              % (nome, ((se or "") + (so or "")).strip()[:400]))
        return 1
    if res == "falha":
        c.err("`brza sessions %s` falhou (rc %s): %s" % (nome, rc, ((se or "") + (so or "")).strip()[:400]))
        return 1
    if res == "ja":
        c.err("%s já está aberta (`running:`) e o pedido novo não chegou a ela: feche com `brza sessions close %s` e rode `open` "
              "de novo; o marcador do worklog ficou como estava" % (nome, nome))
        return 1
    if res == "sem-id":
        c.err("⚠ %s abriu sem o id do provedor; o `wait` o grava depois. Não relance." % nome)
    if not novo:
        neutraliza_marcador(worklog, pid)   # só com a sessão nova aberta: o marcador do executor anterior não vale para ela
    e = {"sessao": nome, "agent": agent, "model": model, "effort": effort, "checkout": checkout, "branch": branch,
         "pedido": os.path.relpath(pedido, pl.raiz), "worklog": os.path.relpath(worklog, pl.raiz),
         "marcador": "fim-%s:" % pid, "estado": "aberto", "eventos": [], "evidencia": None, "medicao": None}
    evento(c, e, "aberto", "open: %s%s" % (nome, "" if novo else " (worklog já existia)"))
    m["passos"][pid] = e
    salva_manifesto(pl, m)
    c.out("| Passo | Executor | Runtime | Modelo | Esforço | Checkout | Branch |")
    c.out("| :-- | :-- | :-- | :-- | :-- | :-- | :-- |")
    c.out("| %s | %s | %s | %s | %s | %s | %s |" % (pid, nome, agent, model or "padrão do runtime", effort or "padrão", checkout, branch))
    c.out("pedido: %s" % pedido)
    c.out("worklog: %s" % worklog)
    _painel(pl, c, a, png=True)
    return 0


# ---------------------------------------------------------------- send

def cmd_send(a, c):
    try:
        pl = plan_md.carrega(a.plano)
    except plan_md.PlanoNaoEncontrado as e:
        c.err("erro: %s" % e)
        return 2
    m = le_manifesto(pl)
    pid = a.passo.upper() if re.match(r"^p\d", a.passo) else a.passo
    e = m["passos"].get(pid)
    if not e:
        c.err("erro: o passo %s não tem executor aberto em %s" % (a.passo, plan_panel.manifesto_path(pl.raiz, pl.id)))
        return 2
    try:
        argv = send_argv([e["sessao"]], text=a.text, file=a.file, operation=a.operation)
    except ValueError as ex:
        c.err("erro: %s" % ex)
        return 2
    rc, so, se = run_sessions(argv)
    try:
        d = json.loads(so)
    except ValueError:
        d = None
    rec = (d or {}).get("receipts") if isinstance(d, dict) else None
    st = (rec[0].get("status") if rec else None) if isinstance(rec, list) and rec else None
    if rc == 75 or st in ("pending", "unknown"):
        c.err("%s: envio incerto (%s): não reenvie às cegas; confira com `status` e `brza sessions read %s --last`"
              % (e["sessao"], st or "rc 75", e["sessao"]))
        return 75
    if rc != 0:
        c.err("`brza sessions send` falhou (rc %s): %s" % (rc, (se or so or "").strip()[:300]))
        return 1
    c.out("%s · enviado a %s (%s)" % (pid, e["sessao"], st or "ok"))
    partial = e.get("estado") == "evidencia-gravada" and has_pending_checks(pl, pid)   # cobre parcial: falta subpasso
    if e.get("estado") in ("feito", "parado") or partial:
        neutraliza_marcador(_abs(pl, e["worklog"]), pid)   # o retrabalho pede um marcador novo, e o `wait` não pode devolver o velho
    novo = "em-curso" if e.get("estado") in ("bloqueado", "parado", "aberto", "feito") or partial else e.get("estado")
    evento(c, e, novo, "send: %s" % (a.operation or "sem operation"))
    salva_manifesto(pl, m)
    return 0


# ---------------------------------------------------------------- wait

def wait_error_verdict(rc, erro, streak, nomes):
    """(ação, mensagem, nome) para o `error` do `brza sessions wait`. Ação: `missing` (o `brza` diz "0 chats abertos se chamam
    <nome>" para um dos `nomes`: só essa sessão se perdeu, e quem chama a marca `falhou` e segue com as outras), `stop` (nome
    duplicado, rc fora de 0/1/75 ou `MAX_WAIT_ERRORS` erros seguidos) ou `retry` (pausa `WAIT_ERROR_PAUSE`)."""
    m = RE_NO_SESSION.search(erro)
    if m and m.group(2) in nomes:
        if int(m.group(1)) == 0:
            return "missing", "a sessão %s não existe mais no `brza sessions` (fechada à mão?); confira `brza sessions list` e "\
                              "reabra com `open`" % m.group(2), m.group(2)
        return "stop", "o nome %s está em %s chats abertos: o `brza sessions` não sabe qual esperar; feche o que sobra" % (
            m.group(2), m.group(1)), m.group(2)
    if rc not in (0, 1, 75):
        return "stop", "o `brza sessions wait` falhou (rc %s): %s" % (rc, erro), None
    if streak >= MAX_WAIT_ERRORS:
        return "stop", "o `brza sessions wait` falhou %d vezes seguidas (rc %s): %s" % (streak, rc, erro), None
    return "retry", "⚠ o `brza sessions wait` falhou (rc %s, %d/%d): %s; espero %d s" % (
        rc, streak, MAX_WAIT_ERRORS, erro, WAIT_ERROR_PAUSE), None


def _linha_evento(pid, estado, c, e):
    mi = minutos(c, e)
    quando = " em %d min" % mi if mi is not None else ""
    if estado == "feito":
        return "%s · feito%s" % (pid, quando)
    if estado == "parado":
        return "%s · parado%s — o executor achou desvio que muda o D: leia o X no worklog %s" % (pid, quando, e.get("worklog"))
    if estado == "bloqueado":
        return "%s · bloqueado%s — o chat espera resposta: `brza sessions read %s --last`" % (pid, quando, e["sessao"])
    return "%s · falhou%s — a sessão %s falhou; confira com `brza sessions read %s --last`" % (pid, quando, e["sessao"], e["sessao"])


def cmd_wait(a, c):
    try:
        pl = plan_md.carrega(a.plano)
    except plan_md.PlanoNaoEncontrado as e:
        c.err("erro: %s" % e)
        return 2
    m = le_manifesto(pl)
    pids = [x.upper() for x in a.passos] if a.passos else [k for k, v in m["passos"].items() if v.get("estado") in VIVOS]
    falta = [x for x in pids if x not in m["passos"]]
    if falta or not pids:
        c.err("erro: %s" % ("sem executor aberto para %s" % ", ".join(falta) if falta else "nenhum executor vivo em %s"
                            % plan_panel.manifesto_path(pl.raiz, pl.id)))
        return 2
    t0 = c.clock()
    fim = t0 + a.timeout
    resultado = {}
    avisado = set()
    vistos = set()
    erros = 0
    ultima_batida = t0
    for pid in pids:
        e = m["passos"][pid]
        if e.get("estado") == "aberto":
            evento(c, e, "em-curso", "wait")
    salva_manifesto(pl, m)
    while True:
        for pid in pids:
            e = m["passos"][pid]
            mk = ultimo_marcador(_abs(pl, e["worklog"]), pid)
            if mk and pid not in resultado:
                resultado[pid] = mk
                evento(c, e, mk, "marcador no worklog")
                c.out(_linha_evento(pid, mk, c, e))
        if resultado:
            break
        restante = fim - c.clock()
        if restante <= 0:
            break
        trecho = min(restante, BATIDA)
        nomes = {m["passos"][p]["sessao"]: p for p in pids}
        marcadores = []
        if len(pids) == 1:   # o `--marker` do brza vale para todas as sessões: com duas, o script confere sozinho
            marcadores = ["%s:<!-- %s" % (_abs(pl, m["passos"][pids[0]]["worklog"]), m["passos"][pids[0]]["marcador"])]
        ini = c.clock()
        rc, dado = wait_brza(list(nomes), trecho, markers=marcadores)
        if dado.get("error"):
            erros += 1
            action, msg, perdida = wait_error_verdict(rc, dado["error"], erros, list(nomes))
            c.err(msg)
            if action == "stop":
                return 1
            if action == "missing":
                perdido = nomes[perdida]
                resultado[perdido] = "falhou"
                evento(c, m["passos"][perdido], "falhou", "wait: sessão inexistente")
                c.out(_linha_evento(perdido, "falhou", c, m["passos"][perdido]))
                break
            c.sleep(WAIT_ERROR_PAUSE)
            continue
        erros = 0
        sem_fim = False
        for ev in dado.get("events") or []:
            tipo = str(ev.get("type") or "").lower().replace("-", "_")
            pl_ev = ev.get("payload") if isinstance(ev.get("payload"), dict) else {}
            if tipo == "escalation" and (str(ev.get("subject") or "").strip().lower() == RUIDO or pl_ev.get("stopReason") == "finished"):
                continue
            if tipo in ATENCAO and (ev.get("id") or json.dumps(ev, sort_keys=True)) not in vistos:
                vistos.add(ev.get("id") or json.dumps(ev, sort_keys=True))
                c.out("atenção · %s%s" % (tipo, (" — " + str(ev.get("subject"))) if ev.get("subject") else ""))
        for row in dado.get("done") or []:
            pid = nomes.get(row.get("name"))
            if pid is None or pid in resultado:
                continue
            e = m["passos"][pid]
            saida = row.get("outcome")
            mk = ultimo_marcador(_abs(pl, e["worklog"]), pid)
            if saida == "failed":
                resultado[pid] = "falhou"
            elif saida == "blocked":
                resultado[pid] = "bloqueado"
            elif mk:
                resultado[pid] = mk
            else:
                sem_fim = True
                if pid not in avisado:
                    avisado.add(pid)
                    c.out("%s · o turno acabou sem o marcador `<!-- fim-%s: … -->` como última linha; a espera segue" % (pid, pid))
                continue
            evento(c, e, resultado[pid], "wait: %s" % saida)
            c.out(_linha_evento(pid, resultado[pid], c, e))
        if resultado:
            break
        if sem_fim:
            c.sleep(min(5, max(0, fim - c.clock())))   # o `wait` volta na hora com o turno já terminado: não gira
        elif c.clock() - ini < trecho and (dado.get("timed_out") or rc == 75):
            c.sleep(max(0, trecho - (c.clock() - ini)))
        if c.clock() < fim and not resultado and c.clock() - ultima_batida >= BATIDA:
            ultima_batida = c.clock()
            c.out(" · ".join("%s · em curso %s min (último evento há %s min)" % (
                p, minutos(c, m["passos"][p]) or 0, minutos(c, m["passos"][p], m["passos"][p]["eventos"][-1]["at"]) or 0)
                for p in pids))
    salva_manifesto(pl, m)
    if resultado:
        _painel(pl, c, a)
    if not resultado:
        c.out("prazo: %s sem marcador em %d s; `status` e decida, sem envio novo às cegas" % (", ".join(pids), a.timeout))
        return 75
    estados = set(resultado.values())
    if "falhou" in estados:
        return 1
    if "bloqueado" in estados:
        return 3
    return 0


# ---------------------------------------------------------------- evidence

RE_ITEM = re.compile(r"^\s*(?:[-*]\s+)?(commit|comando|arquivos|desvios|cobre)\s*:\s*(.*)$", re.I)
RE_COMMIT = re.compile(r"(?:([\w.-]+)@)?\b([0-9a-f]{7,40})\b")
RE_COMANDO = re.compile(r"^`(.+?)`\s*(?:→|->)\s*(.*?)\s*(\(\s*≤\s*2\s*min\s*\))?\s*$")


def le_evidencia(texto):
    """A seção `## Evidência` do worklog: {commits, comandos, arquivos, desvios, aguarda}. None sem a seção."""
    linhas = corta_medida(texto).split("\n")
    ini = next((i for i, l in enumerate(linhas) if re.match(r"^##\s+Evidência\s*$", l)), None)
    if ini is None:
        return None
    ev = {"commits": [], "comandos": [], "arquivos": [], "desvios": [], "aguarda": False, "bruta": [], "cobre": None}
    dentro = False
    for l in linhas[ini + 1:]:
        if re.match(r"^#{1,2}\s", l) or re.match(r"^<!-- fim-", l.strip()):
            break
        if l.strip().startswith("```"):
            dentro = not dentro
            continue
        if dentro:
            continue
        mi = RE_ITEM.match(l)
        if not mi:
            continue
        tipo, valor = mi.group(1).lower(), mi.group(2).strip()
        ev["bruta"].append(l.strip())
        if tipo == "commit":
            if re.search(r"aguarda", valor, re.I):
                ev["aguarda"] = True
            for repo, sha in RE_COMMIT.findall(valor):
                if re.search(r"\d", sha):
                    ev["commits"].append((repo or None, sha))
        elif tipo == "comando":
            mc = RE_COMANDO.match(valor.replace("\\`", "`"))
            if mc:
                ev["comandos"].append({"cmd": mc.group(1), "resultado": mc.group(2), "rerun": bool(mc.group(3))})
        elif tipo == "cobre":   # `cobre: todos` ou `cobre: 1, 3`: os subpassos que a evidência cobre
            if re.match(r"^todos\b", valor, re.I) or ev["cobre"] == "todos":
                ev["cobre"] = "todos"   # `todos` vence; várias linhas `cobre:` se juntam
            else:
                novos = [x.strip().strip("`*") for x in valor.split(",") if x.strip()]
                ev["cobre"] = (ev["cobre"] or []) + [x for x in novos if x not in (ev["cobre"] or [])]
        elif tipo == "arquivos":
            ev["arquivos"] = [x.strip().strip("`") for x in valor.split(",") if x.strip()]
        else:
            ev["desvios"].append(valor)
    return ev


def confere(ev, checkout, raiz, c, rerun=False):
    """Roda as conferências: [(ok, linha)]. `ok` None é "não conferido" (informativo). O comando do worklog só roda com
    `rerun` (o `--apply` ou o `--rerun`) e se for simples: o worklog é entrada de outra sessão."""
    res = []
    for repo, sha in ev["commits"]:
        base = raiz if repo == "brza-workspace" else checkout
        rc, _, se = run_git(["-C", base, "cat-file", "-e", sha])
        cmd = "git -C %s cat-file -e %s" % (base, sha)
        res.append((rc == 0, ("confere: `%s` → ok" % cmd) if rc == 0 else "NÃO confere: `%s` → rc %s %s" % (cmd, rc, (se or "").strip()[:120])))
    for k in ev["comandos"]:
        if not k["rerun"]:
            res.append((None, "não rodei `%s` (sem `(≤ 2 min)`): vale a palavra do executor: %s" % (k["cmd"], k["resultado"])))
            continue
        if not rerun:
            res.append((None, "não rodei `%s`: a proposta não roda comando do worklog (use `--rerun` ou `--apply` depois de ler): "
                              "vale a palavra do executor: %s" % (k["cmd"], k["resultado"])))
            continue
        if parse_command(k["cmd"]) is None:
            res.append((None, "não rodei `%s`: não é um comando que o argv reproduz (só `VAR=v` e `cd X &&` na frente; sem `;`, `|`, `>`, `$`, crase); vale a palavra do "
                              "executor: %s" % (k["cmd"], k["resultado"])))
            continue
        rc, so = run_shell(k["cmd"], checkout)
        cauda = [l for l in so.strip().split("\n") if l.strip()]
        fim = cauda[-1].strip()[:140] if cauda else "sem saída"
        res.append((rc == 0, ("confere: `%s` → %s (disse: %s)" % (k["cmd"], fim, k["resultado"])) if rc == 0
                    else "NÃO confere: `%s` → rc %s, %s (disse: %s)" % (k["cmd"], rc, fim, k["resultado"])))
    ausentes = [f for f in ev["arquivos"] if not os.path.exists(os.path.join(checkout, f)) and not os.path.exists(os.path.join(raiz, f))]
    if ev["arquivos"]:
        res.append((None, "arquivos: %d citados%s" % (len(ev["arquivos"]), ("; não achei no disco: " + ", ".join(ausentes)) if ausentes else ", todos no disco")))
    return res


def linha_evidencia(ev):
    partes = []
    for repo, sha in ev["commits"]:
        partes.append("%s@%s" % (repo or "brza-studio", sha[:7]))
    if ev["aguarda"] and not ev["commits"]:
        partes.append("commit aguarda confirmação")
    for k in ev["comandos"]:
        partes.append("`%s` → %s" % (k["cmd"], k["resultado"]))
    if ev["arquivos"]:
        partes.append("arquivos: " + ", ".join(ev["arquivos"]))
    return "**Evidência:** " + " · ".join(partes)


def _janela(c, e, pl):
    """(aberto_iso, fim_iso, fim_epoch): da abertura ao marcador (o evento `feito`/`parado`, ou o mtime do worklog)."""
    ev = e.get("eventos") or []
    aberto = ev[0].get("at") if ev else None
    fim = next((x.get("at") for x in reversed(ev) if x.get("estado") in ("feito", "parado")), None)
    if fim is None:
        try:
            fim = iso(os.path.getmtime(_abs(pl, e["worklog"])))
        except OSError:
            fim = None
    return aberto, fim


def mede(c, pl, e, settle, measurements=None, sessions=None):
    """{texto, custo_usd, janela_h, turnos_h}: o `Executado` proposto. Grok e Antigravity: `sem medição`."""
    agent = e.get("agent") or "claude"
    if agent not in ("claude", "codex"):
        return {"texto": "sem medição", "custo_usd": None, "janela_h": None, "turnos_h": None}
    aberto, fim = _janela(c, e, pl)
    ea, ef = sessions_map.epoch(aberto), sessions_map.epoch(fim)
    if ea is None or ef is None or ef < ea:
        return {"texto": "sem medição", "custo_usd": None, "janela_h": None, "turnos_h": None}
    janela_h = round((ef - ea) / 3600, 3)
    srows = measure.load_jsonl(sessions or sessions_map.map_file(pl.raiz))
    claude_ids, provider_ids = measure.session_ids(srows, e["sessao"])
    d0, d1 = (datetime.datetime.fromtimestamp(x).astimezone() for x in (ea, ef))
    win = measure.win_bounds(d0, d1)
    out = {"custo_usd": None, "janela_h": janela_h, "turnos_h": None}
    if agent == "claude":
        mpath = measurements or plan_panel._achar(pl.raiz, ".measurements/measurements.jsonl")
        limite = c.clock() + settle
        while True:
            r = measure.measure_claude(measure.load_jsonl(mpath), claude_ids, win) if claude_ids else None
            if r or not claude_ids or not os.path.isfile(mpath) or c.clock() >= limite:
                break
            c.sleep(5)
        if r:
            out["custo_usd"], out["turnos_h"] = r["custo_usd"], round(r["latencia_s"] / 3600, 3)
            out["texto"] = "%s h (janela; %s h de turnos; US$ %.2f)" % (plan_md.fmt_horas(janela_h), plan_md.fmt_horas(out["turnos_h"]), r["custo_usd"])
        else:
            out["texto"] = "%s h (janela; sem medição dos turnos)" % plan_md.fmt_horas(janela_h)
    else:
        r = measure.measure_codex(os.path.expanduser("~/.codex/sessions"), provider_ids, 1, win)
        if r:
            out["turnos_h"] = round(r["latencia_s"] / 3600, 3)
            out["texto"] = "%s h (janela; %s h do último turno Codex; sem custo medido)" % (plan_md.fmt_horas(janela_h), plan_md.fmt_horas(out["turnos_h"]))
        else:
            out["texto"] = "%s h (janela; sem medição dos turnos)" % plan_md.fmt_horas(janela_h)
    return out


def check_number(texto):
    """O número do subpasso (`**3. Texto**` → `3`, `**4a. …**` → `4a`); None se o texto não começa por número."""
    m = re.match(r"^[\s*`]*(\d+[a-z]?)\s*[.)]", texto)
    return m.group(1).lower() if m else None


def unknown_covered(p, cobre):
    """Os números de `cobre:` que o passo não tem."""
    if not isinstance(cobre, list):
        return []
    tem = {check_number(texto) for _, _, texto in p.checks}
    return [x for x in cobre if x.lower() not in tem]


def aplica_no_plano(pl, pid, linha, executado, cobre=None):
    """Grava no `### Pn`: o `Executado`, o `[x]` nos subpassos pendentes e a `**Evidência:**`. Devolve os subpassos marcados.
    `cobre` é a lista de números que a evidência declara; None ou `"todos"` marca todos os pendentes."""
    p = pl.passo(pid)
    arq = p.arquivo
    linhas = list(arq.linhas)
    if p.linha_horas is not None and executado:
        l = linhas[p.linha_horas]
        mm = re.match(r"^(Estimado:\s*.*?)\s*·\s*Executado:.*$", l)
        linhas[p.linha_horas] = ("%s · Executado: %s" % (mm.group(1), executado)) if mm else "%s · Executado: %s" % (l.rstrip(), executado)
    marcados = []
    for i, marca, texto in p.checks:
        if marca == " " and (not isinstance(cobre, list) or (check_number(texto) or "") in [x.lower() for x in cobre]):
            linhas[i] = linhas[i].replace("[ ]", "[x]", 1)
            marcados.append(re.sub(r"\*\*", "", texto).split("—")[0].strip())
    if p.evidencia_ini is not None:
        j = p.evidencia_ini + 1
        while j < p.secao.fim and linhas[j].strip():
            j += 1
        linhas[p.evidencia_ini:j] = [linha]
    else:
        fim = p.secao.fim
        while fim > p.secao.ini + 1 and not linhas[fim - 1].strip():
            fim -= 1
        linhas[fim:fim] = ["", linha]
    with open(arq.path, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    return marcados


def cmd_evidence(a, c):
    try:
        pl = plan_md.carrega(a.plano)
    except plan_md.PlanoNaoEncontrado as e:
        c.err("erro: %s" % e)
        return 2
    m = le_manifesto(pl)
    pid = a.passo.upper()
    e = m["passos"].get(pid)
    if not e:
        c.err("erro: o passo %s não tem executor aberto" % a.passo)
        return 2
    wl = _abs(pl, e["worklog"])
    try:
        with open(wl, encoding="utf-8") as f:
            texto = f.read()
    except OSError as ex:
        c.err("erro: não li o worklog %s: %s" % (wl, ex))
        return 1
    mk = ultimo_marcador(wl, pid)
    if mk is None:
        c.err("o worklog %s não termina em `<!-- fim-%s: feito|parado -->`: o executor não fechou; não há evidência para ler" % (wl, pid))
        return 1
    ev = le_evidencia(texto)
    if ev is None or not (ev["commits"] or ev["comandos"] or ev["arquivos"] or ev["aguarda"]):
        c.err("o worklog %s não traz `## Evidência` com itens (`commit:`, `comando:`, `arquivos:`): volte ao executor pelo `send`" % wl)
        return 1
    res = confere(ev, e["checkout"], pl.raiz, c, rerun=bool(a.apply or getattr(a, "rerun", False)))
    for _, linha in res:
        c.out(linha)
    ruins = [l for ok, l in res if ok is False]
    linha = linha_evidencia(ev)
    medicao = mede(c, pl, e, a.settle, getattr(a, "measurements", None), getattr(a, "sessions", None))
    c.out(linha)
    c.out("Executado: %s" % medicao["texto"])
    c.out("desvios (lidos do worklog, não gravados): %s" % ("; ".join(ev["desvios"]) if ev["desvios"] else "o executor não declarou"))
    if ev["aguarda"] and not ev["commits"]:
        c.out("⚠ o executor deixou `commit: aguarda confirmação`: não há commit para conferir")
    if not plan_state.evidencia_valida(linha):
        c.err("a evidência não traz commit, comando com `→` nem `arquivo:linha`: não vale")
        ruins.append("evidência sem prova")
    faltam = unknown_covered(pl.passo(pid), ev.get("cobre"))
    if faltam:
        c.err("`cobre:` cita o subpasso %s, que o passo %s não tem" % (", ".join(faltam), pid))
        ruins.append("cobre com subpasso inexistente")
    if ev.get("cobre") is None:
        c.out("⚠ o worklog não traz `cobre:`: sem `cobre:`, o `--apply` marca todos os subpassos pendentes")
    else:
        c.out("cobre: %s" % (ev["cobre"] if ev["cobre"] == "todos" else ", ".join(ev["cobre"])))
    if ruins:
        c.err("não confere (%d): volte ao executor pelo `send`; o passo não fecha" % len(ruins))
        return 1
    if not a.apply:
        c.out("proposta: leia e rode `evidence %s %s --apply` para gravar no plano" % (pl.id, pid))
        return 0
    if mk != "feito":
        c.err("o marcador é `parado`: o executor achou desvio que muda o D; leve o X à rodada, não grave o passo como feito")
        return 1
    executado = medicao["texto"]
    marcados = aplica_no_plano(pl, pid, linha, executado, ev.get("cobre"))
    mudou = plan_state.fix_horas(pl.path)
    e["evidencia"] = {"linha": linha, "executado": executado, "desvios": ev["desvios"], "gravada_em": iso(c.clock()),
                      "conferencias": [l for _, l in res]}
    e["medicao"] = {"custo_usd": medicao["custo_usd"], "janela_h": medicao["janela_h"], "turnos_h": medicao["turnos_h"]}
    evento(c, e, "evidencia-gravada", "evidence --apply")
    salva_manifesto(pl, m)
    c.out("gravado em %s: `### %s`, %d subpasso(s) marcados, Executado: %s" % (os.path.relpath(pl.path, pl.raiz), pid, len(marcados), executado))
    c.out("--fix: %s" % (", ".join(mudou) if mudou else "as horas já conferiam"))
    prob = [p for p in plan_state.estado(pl.path)["problemas"] if p["nivel"] == "erro"]
    for p in prob:
        c.err("plan_state: %s %s: %s" % (p["codigo"], p["onde"], p["msg"]))
    _painel(pl, c, a)
    return 0


# ---------------------------------------------------------------- close

def veredito(show):
    """(veredito, campos) do JSON do `worker-show --full`, com ou sem o envelope `{"ok", "result"}`."""
    r = show.get("result") if isinstance(show.get("result"), dict) else show
    d, w, tr = r.get("dispatch") or {}, r.get("worker") or {}, r.get("terminalResource") or {}
    cc = {"state": w.get("state"), "stage": w.get("stage"), "completedAt": d.get("completedAt"),
          "releaseState": tr.get("releaseState"), "retainedReason": tr.get("retainedReason")}
    if cc["releaseState"] == "released":
        v = "liberada (falhou)" if cc["state"] == "failed" else "liberada"
    elif cc["state"] in FALHOU:
        v = "falhou"
    elif cc["state"] == "succeeded" and cc["stage"] == "settled" and cc["releaseState"] == "retained":
        v = "encerrada, retida (%s): não fecha sozinha" % (cc["retainedReason"] or "motivo não informado")
    elif cc["state"] == "succeeded" and cc["stage"] == "settled" and cc["completedAt"]:
        v = "encerrada e aceita"
    else:
        v = "ativa"
    return v, cc


def _consulta(pl, nome):
    ent = sessions_map.load_map(pl.raiz).get(nome) or {}
    d = ent.get("dispatch")
    if not d:
        return None, "sem Dispatch no mapa: nada a conferir"
    rc, so, se = run_brza(["orchestration", "worker-show", "--dispatch", d, "--full", "--json"])
    try:
        show = json.loads(so)
    except ValueError:
        show = None
    if rc != 0 or not isinstance(show, dict):
        return None, "worker-show falhou (rc %s): %s" % (rc, (se or so or "").strip()[:200])
    return veredito(show)[0], None


def cmd_close(a, c):
    try:
        pl = plan_md.carrega(a.plano)
    except plan_md.PlanoNaoEncontrado as e:
        c.err("erro: %s" % e)
        return 2
    m = le_manifesto(pl)
    pid = a.passo.upper()
    e = m["passos"].get(pid)
    if not e:
        c.err("erro: o passo %s não tem executor aberto" % a.passo)
        return 2
    nome = e["sessao"]
    modo = "keep-open" if a.keep_open else "stop" if a.stop else "close"
    rc, so, se = run_sessions(close_argv(nome, modo))
    try:
        d = json.loads(so)
    except ValueError:
        d = None
    if isinstance(d, dict) and isinstance(d.get("results"), list) and d["results"]:
        d = d["results"][0]
    if not isinstance(d, dict):
        c.err("%s: sem JSON do close (rc %s): %s; não repita; confira com `status`" % (nome, rc, (se or so or "").strip()[:300]))
        return rc or 1
    st = d.get("status")
    if st in INCERTOS:
        c.err("%s: incerto (%s): não está fechada; não repita" % (nome, st))
        return 75
    if st == "refused" or "error" in d:
        c.err("%s: recusado: %s" % (nome, d.get("error") or d))
        return 1
    if st == "kept_open":
        c.out("%s · mantida aberta (kept_open); não fecha sozinha" % pid)
        return 0
    if st == "closing":
        c.out("%s · pedido de encerramento enviado; NÃO está fechada (closing)" % pid)
    if a.wait_settled:
        fim = c.clock() + a.wait_settled
    else:
        fim = None
    v = None
    while True:
        v, motivo = _consulta(pl, nome)
        if v in OK_FINAL or v in ("falhou", "liberada (falhou)"):
            break
        if fim is None or c.clock() >= fim:
            break
        c.sleep(5)
    if v in OK_FINAL:
        if e.get("estado") != "evidencia-gravada":
            c.err("⚠ %s fechada sem a evidência aplicada ao plano (estado %s)" % (pid, e.get("estado")))
        evento(c, e, "fechado", "close: %s" % v)
        salva_manifesto(pl, m)
        c.out("%s · encerrada e aceita" % pid if v == "encerrada e aceita" else "%s · %s" % (pid, v))
        _painel(pl, c, a, png=True)
        return 0
    if v in ("falhou", "liberada (falhou)"):
        c.err("%s · a sessão falhou (%s)" % (pid, v))
        return 1
    c.out("%s · %s" % (pid, ("não encerrada: " + v) if v else motivo))
    return 75 if fim is not None else 0


# ---------------------------------------------------------------- status

def cmd_status(a, c):
    try:
        pl = plan_md.carrega(a.plano)
    except plan_md.PlanoNaoEncontrado as e:
        c.err("erro: %s" % e)
        return 2
    m = le_manifesto(pl)
    if not m["passos"]:
        c.out("%s · sem executor aberto" % pl.id)
        return 0
    estados = list_states([e["sessao"] for e in m["passos"].values()])
    linhas = []
    for pid, e in m["passos"].items():
        ev = e.get("eventos") or []
        linhas.append({"passo": pid, "sessao": e["sessao"], "estado": e.get("estado"), "agent": e.get("agent"),
                       "aberto_ha_min": minutos(c, e), "ultimo_evento_ha_min": minutos(c, e, ev[-1]["at"]) if ev else None,
                       "ultimo_evento": ev[-1] if ev else None, "sessao_state": estados.get(e["sessao"]),
                       "worklog": e.get("worklog"), "evidencia": bool(e.get("evidencia"))})
    if a.json:
        c.out(json.dumps({"plano": pl.id, "passos": linhas}, ensure_ascii=False, indent=2))
        return 0
    for l in linhas:
        c.out("%s · %s · %s · aberto há %s min · último evento há %s min · sessão: %s%s" % (
            l["passo"], l["sessao"], l["estado"], l["aberto_ha_min"], l["ultimo_evento_ha_min"],
            l["sessao_state"] or "?", " · evidência gravada" if l["evidencia"] else ""))
    return 0


# ---------------------------------------------------------------- CLI

def main(argv=None, *, out=None, err=None, clock=None, sleep=None):
    ap = argparse.ArgumentParser(prog="executor.py", description="as sessões executoras dos passos do plano")
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("open")
    o.add_argument("plano")
    o.add_argument("passo")
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
    s.add_argument("plano")
    s.add_argument("passo")
    gs = s.add_mutually_exclusive_group(required=True)
    gs.add_argument("--text")
    gs.add_argument("--file")
    s.add_argument("--operation")
    w = sub.add_parser("wait")
    w.add_argument("plano")
    w.add_argument("passos", nargs="*")
    w.add_argument("--timeout", type=float, default=1800)
    w.add_argument("--no-panel", action="store_true")
    ev = sub.add_parser("evidence")
    ev.add_argument("plano")
    ev.add_argument("passo")
    ev.add_argument("--apply", action="store_true")
    ev.add_argument("--rerun", action="store_true", help="roda os comandos `(≤ 2 min)` do worklog, só os simples, sem gravar")
    ev.add_argument("--settle", type=float, default=60)
    ev.add_argument("--no-panel", action="store_true")
    ev.add_argument("--measurements")
    ev.add_argument("--sessions")
    cl = sub.add_parser("close")
    cl.add_argument("plano")
    cl.add_argument("passo")
    gc = cl.add_mutually_exclusive_group()
    gc.add_argument("--keep-open", action="store_true")
    gc.add_argument("--stop", action="store_true")
    cl.add_argument("--wait-settled", type=float, default=0, metavar="SEG")
    cl.add_argument("--no-panel", action="store_true")
    st = sub.add_parser("status")
    st.add_argument("plano")
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
