#!/usr/bin/env python3
"""launch_persona.py: o manifesto da reunião vira argv do `brza sessions` v2 (abrir, enviar, fechar, conferir).

Uso:
    launch_persona.py <reuniao.json> [persona ...] [--dry-run] [--root DIR] [--sessions ARQUIVO]          # abre
    launch_persona.py <reuniao.json> [persona ...|todas] --send (--message T | --round N) [--operation OP]
    launch_persona.py <reuniao.json> [persona ...] --close | --release | --stop | --keep-open
    launch_persona.py <reuniao.json> [persona ...] --status [--wait-settled SEG]

`--root` padrão: o topo do repositório git do cwd (`git rev-parse --show-toplevel`; sem git, o cwd); o manifesto relativo
resolve contra ele. Rodar da raiz do worktree, da pasta da reunião ou da pasta da skill dá o mesmo resultado.

O transporte é do `brza sessions` v2 (PLN-017 R6/P4a): a persona é um worker do Orca aberto por `worker-start` DENTRO do
`brza sessions <nome>`, que grava Nome, Dispatch, Run, remetente, coordenação, modelo, esforço e o id do provedor no mapa
(`.sessions/sessions.jsonl`). Este script NÃO chama `brza orchestration worker-start|send|check|worker-release|worker-stop|
worker-keep-open`; a única chamada direta ao `brza orchestration` é a LEITURA `worker-show --dispatch <id> --full` do
`--status`. O `--via` antigo saiu: aceita só `sessions` (o padrão).

ABRIR: uma persona de cada vez, na ordem do manifesto, NUNCA em paralelo (a primeira abertura cria o Run, e as outras
entram nele). Por persona: `brza sessions <sessao> --agent <runtime> --checkout <abs> --prompt-file <prompt> --title <t>
--wait` mais `--model` e `--effort` quando valem (Antigravity nunca leva modelo nem esforço; o esforço só vai com
modelo). A saída do v2 se lê assim: `open:` abriu; `running:` já estava aberto (não reabre); `CHECK: <nome> não abriu`
(rc 1): não abriu, e não se relança antes de conferir o `pending-*.json` citado; `CHECK: <nome> não deu a sessão em 60 s`
(rc 1): ABRIU sem o id do provedor, não relance, o `wait` grava o id depois, e o lote segue; outro rc ≠ 0: falha da
persona, sem relançar. Depois, imprime a tabela da narração (`Persona · papel · runtime · modelo · esforço · Dispatch ·
Run · sessão do provedor`, do mapa) e, se as abertas estão em mais de um Run, `⚠ Run múltiplo` e rc 1.

ENVIAR (`--send`): UMA chamada `brza sessions send <sessoes…> --text <T> --json` (`--round N` gera `Faça a rodada N:
<dir>/rodada-N.md`; `--operation` só com uma persona). `pending` e `unknown` (rc 75) NUNCA se reenviam às cegas (R2.1):
espere com `wait_round.py N`, ou repita só a persona com a MESMA `--operation` e o MESMO texto. O script nunca reenvia.

FECHAR: um nome por chamada, `--json`: `--close`/`--release` = `close`; `--stop` = `close --force` (parada guardada, R7);
`--keep-open` = `close --keep-open`. `closing` NÃO é fechada; `stop_unknown`/`release_unknown`/`release_pending` são
incertos (rc 75, não se repete); `retained` ou outro não é fechada (rc 1); só `released`/`already_released` fecham.

CONFERIR (`--status`, só leitura): `brza orchestration worker-show --dispatch <id> --full --json` por persona e o veredito
(`encerrada e aceita`, `liberada`, `ativa`, `falhou`); `--wait-settled SEG` repete a cada 5 s até todas encerradas ou
liberadas (rc 0), alguma `falhou` (rc 1, para na hora e a lista) ou o prazo (rc 75, com o `worker_done` que o preâmbulo da persona deveria ter mandado, só como diagnóstico).

Corredores injetáveis (testes): `run_sessions(argv) -> (rc, stdout, stderr)` e `run_brza(argv)`, ambos por `subprocess`
sem shell, com `BRZA = $BRZA_BIN ou "brza"`.

`--dry-run` imprime os comandos exatos, sem executar nada nem gravar o prompt.
"""
import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import common  # noqa: E402
import sessions_map  # noqa: E402

BRZA = os.environ.get("BRZA_BIN", "brza")
MOLDE = ("Você é uma persona numa reunião multiagente: {nome}, {papel}. Tema: {tema}. Leia o briefing ({briefing}) e a "
         "sua persona ({persona_md}) e faça a rodada 1 conforme {dir}/rodada-1.md; o seu worklog é {worklog}; prazo "
         "{prazo}; responda em português do Brasil. Ao fechar cada rodada, grave a seção e o marcador no worklog e "
         "envie só o status do protocolo que a coordenação anexa a cada pedido (round_id e dispatchId no payload); "
         "não responda por mensagem, não envie outro aviso. O worker_done é só do encerramento, quando a coordenação "
         "pedir: use exatamente o comando worker_done do seu preâmbulo do Orca, com o --task-id e o --dispatch-id "
         "dele, uma vez. Hora no worklog só a de `date '+%H:%M'`, rodado na hora.")
VIA_REMOVIDA = "via removida: a abertura é a do brza sessions v2 (PLN-017 R6/P4a)"
VIAS_REMOVIDAS = ("worker-start", "hybrid", "agent-launch")
FALHOU = ("failed", "stopped", "abandoned")
OK_FINAL = ("encerrada e aceita", "liberada")
INCERTOS = ("stop_unknown", "release_unknown", "release_pending")
PENDENTES = ("pending", "unknown")


# ---------------------------------------------------------------- o manifesto

def dash(v):
    return None if v in (None, "", "-") else v


def settings(p):
    """(agent, model, effort) que valem na abertura; model/effort None quando não vão ao `brza sessions`."""
    agent = (p.get("runtime") or "claude").lower()
    if agent == "antigravity":
        return agent, None, None
    model = dash(p.get("modelo"))
    return agent, model, (dash(p.get("esforco")) if model else None)


def slug_de(p):
    return p.get("slug") or p["nome"].lower()


def prompt_path(reuniao, p, root):
    return os.path.join(root, reuniao.get("dir", "."), p.get("prompt") or f"prompt-{slug_de(p)}.txt")


def prazo_do_molde(reuniao, root=None):
    """`~M min` da primeira linha de `rodada-1.md` quando existe; senão `até <fim>` (a hora do manifesto)."""
    if root:
        dur = common.duracao_anunciada(os.path.join(root, reuniao.get("dir", "."), "rodada-1.md"))
        if dur:
            return f"~{dur} min"
    return f"até {reuniao.get('fim') or 'o combinado'}"


def prompt_text(reuniao, p, root=None):
    slug = slug_de(p)
    d = reuniao.get("dir", ".")
    return MOLDE.format(
        nome=p["nome"], papel=p.get("papel") or "persona", tema=reuniao.get("tema") or reuniao.get("id"),
        briefing=os.path.join(d, reuniao.get("briefing") or "briefing.md"),
        persona_md=os.path.join(d, "personas", f"{slug}.md"), dir=d,
        worklog=reuniao["worklog"].format(slug=slug, nome=p["nome"], sessao=p.get("sessao", "")),
        prazo=prazo_do_molde(reuniao, root))


def title_for(reuniao, p, agent, model, effort):
    rotulo = " ".join(x for x in (model, effort) if x) or agent
    nome_reuniao = (reuniao.get("id") or "").removeprefix("reuniao-")
    return p.get("title") or f"Reunião {nome_reuniao}: {p['nome']} ({rotulo})"


def checkout_abs(reuniao, root):
    """O `checkout` do manifesto é relativo à RAIZ COMUM do repositório (como no `brza sessions --checkout`), não ao
    worktree em que o script roda: `.worktrees/playground` junto do worktree dobraria o caminho."""
    co = reuniao.get("checkout") or "."
    return co if os.path.isabs(co) else os.path.abspath(os.path.join(sessions_map.common_root(root), co))


def ensure_prompt(reuniao, p, root):
    """Grava o molde só quando `prompt-<slug>.txt` não existe: o arquivo existente nunca é sobrescrito."""
    path = prompt_path(reuniao, p, root)
    if not os.path.isfile(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(prompt_text(reuniao, p, root) + "\n")


def open_argv(reuniao, p, root):
    """O argv (sem o `brza sessions`) que abre a persona."""
    agent, model, effort = settings(p)
    argv = [p["sessao"], "--agent", agent, "--checkout", checkout_abs(reuniao, root),
            "--prompt-file", prompt_path(reuniao, p, root), "--title", title_for(reuniao, p, agent, model, effort),
            "--wait"]
    return argv + (["--model", model] if model else []) + (["--effort", effort] if effort else [])


def send_argv(sessoes, texto, operation=None):
    """O argv (sem o `brza sessions`) do `send`: UMA chamada para todas as sessões."""
    return ["send", *sessoes, "--text", texto, "--json"] + (["--operation", operation] if operation else [])


def close_argv(sessao, modo="close"):
    """O argv (sem o `brza sessions`) do `close` de UMA sessão; `modo`: close | stop | keep-open."""
    return ["close", sessao, *{"close": [], "stop": ["--force"], "keep-open": ["--keep-open"]}[modo], "--json"]


def pick(reuniao, nomes):
    try:
        return common.resolver_personas(reuniao, nomes)
    except ValueError as e:
        raise SystemExit(str(e)) from None


raiz_padrao = common.raiz_padrao


# ---------------------------------------------------------------- os corredores

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
    """O corredor do `brza <argv>` (só a leitura `orchestration worker-show` do `--status`)."""
    return _roda([BRZA, *argv])


def _cmd(argv):
    return "brza " + " ".join(shlex.quote(a) for a in argv)


def _json(texto):
    try:
        return json.loads(texto)
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------- abrir

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


def tabela(reuniao, escolhidas, entradas, out=print):
    """A tabela da narração, uma linha por persona, e o conjunto de Runs das abertas."""
    out("Persona · papel · runtime · modelo · esforço · Dispatch · Run · sessão do provedor")
    runs = {}
    for p in escolhidas:
        e = entradas.get(p["sessao"]) or {}
        agent, model, effort = settings(p)
        prov = e.get("provider_session") or e.get("claude_session") or "—"
        out(" · ".join([p["nome"], p.get("papel") or "—", e.get("agent") or agent, e.get("model") or model or "—",
                        e.get("effort") or effort or "—", sessions_map.dispatch_of(p, entradas) or "—",
                        e.get("run") or "—", prov]))
        if e.get("run"):
            runs[p["nome"]] = e["run"]
    return runs


def abrir(reuniao, escolhidas, root, sessions=None, dry=False, sessions_fn=None, out=print, err=None):
    """Abre as personas UMA DE CADA VEZ e imprime a tabela; rc 0 se todas abertas, 1 se alguma falhou ou há Run múltiplo."""
    sessions_fn = sessions_fn or run_sessions
    err = err or (lambda s: print(s, file=sys.stderr))
    rc = 0
    for p in escolhidas:
        argv = open_argv(reuniao, p, root)
        if dry:
            agent, model, effort = settings(p)
            path = prompt_path(reuniao, p, root)
            out(f"[dry-run] {p['nome']} ({agent}, modelo {model or '-'}, esforço {effort or '-'})")
            out("  " + _cmd(["sessions", *argv]))
            out(f"  prompt: {path} (existe)" if os.path.isfile(path) else f"  prompt: geraria {path}: {prompt_text(reuniao, p, root)}")
            continue
        ensure_prompt(reuniao, p, root)
        r, so, se = sessions_fn(argv)
        quadro = interpreta_abertura(r, so, se)
        for linha in (so or "").splitlines():
            out(f"{p['nome']}: {linha}")
        for linha in (se or "").splitlines():
            err(f"{p['nome']}: {linha}")
        if quadro == "aberta":
            out(f"{p['nome']}: aberta")
        elif quadro == "ja":
            out(f"{p['nome']}: já aberta; não reabre")
        elif quadro == "sem-id":
            out(f"{p['nome']}: abriu; não relance; o `wait` grava o id depois")
        elif quadro == "nao-abriu":
            out(f"{p['nome']}: não abriu; não relance antes de conferir o pending-*.json citado")
            rc = 1
        else:
            out(f"{p['nome']}: falha na abertura (rc {r}); sem relançar")
            rc = 1
    if dry:
        return 0
    entradas = sessions_map.load_map(root, sessions)
    runs = tabela(reuniao, escolhidas, entradas, out)
    if len(set(runs.values())) > 1:
        out("⚠ Run múltiplo: " + ", ".join(f"{n}={r}" for n, r in runs.items())
            + "; as personas devem dividir um Run só; não relance nada, confira o mapa")
        rc = 1
    return rc


# ---------------------------------------------------------------- enviar

def round_message(reuniao, n):
    return f"Faça a rodada {n}: {reuniao.get('dir', '.')}/rodada-{n}.md"


def enviar(reuniao, escolhidas, root, texto, operation=None, n=None, dry=False, sessions_fn=None, out=print):
    """UMA chamada de `brza sessions send` para todas; `pending`/`unknown` nunca se reenviam às cegas (R2.1)."""
    sessions_fn = sessions_fn or run_sessions
    if operation and len(escolhidas) != 1:
        out("--operation vale para uma persona só: nomeie uma (repita só a que ficou pending/unknown)")
        return 2
    argv = send_argv([p["sessao"] for p in escolhidas], texto, operation)
    if dry:
        out("[dry-run] " + _cmd(["sessions", *argv]))
        return 0
    rc, so, se = sessions_fn(argv)
    dado = _json(so)
    if not isinstance(dado, dict):
        out(f"erro do brza sessions send (rc {rc}): {(se or so or '').strip()[:300]}")
        return rc or 1
    if "error" in dado and "results" not in dado and "status" not in dado:
        out(f"erro do brza sessions send: {dado['error']}")
        return rc or 1
    linhas = dado["results"] if isinstance(dado.get("results"), list) else [dado]
    por_sessao = {p["sessao"]: p["nome"] for p in escolhidas}
    quando = f"wait_round.py {n}" if n else "wait_round.py N"
    ruim = False
    for r in linhas:
        nome = por_sessao.get(r.get("name"), r.get("name"))
        status, op = r.get("status"), r.get("operation")
        out(f"{nome}: {status} · {op}")
        if status in PENDENTES:
            out(f"{nome}: {status} — não reenvie às cegas; espere com {quando}, ou repita só esta persona com "
                f"--operation {op} e o mesmo texto")
        elif status == "rejected":
            out(f"{nome}: rejected — {r.get('refusal') or r.get('error') or 'sem motivo no recibo'}")
            ruim = True
    return 1 if ruim and rc == 0 else rc


# ---------------------------------------------------------------- fechar

def fechar(escolhidas, modo, root, sessions=None, dry=False, sessions_fn=None, out=print):
    """`close` do v2, um nome por chamada, sem repetir sozinho. `modo`: close | stop | keep-open."""
    sessions_fn = sessions_fn or run_sessions
    codigos = []
    for p in escolhidas:
        argv = close_argv(p["sessao"], modo)
        if dry:
            out(f"[dry-run] {p['nome']}: " + _cmd(["sessions", *argv]))
            continue
        rc, so, se = sessions_fn(argv)
        d = _json(so)
        if isinstance(d, dict) and isinstance(d.get("results"), list) and d["results"]:
            d = d["results"][0]
        if not isinstance(d, dict):
            out(f"{p['nome']}: sem JSON do close (rc {rc}): {(se or so or '').strip()[:300]}; "
                "não repita; confira com --status")
            codigos.append(rc or 1)
            continue
        status = d.get("status")
        if status == "closing":
            out(f"{p['nome']}: pedido de encerramento enviado; NÃO está fechada; confira com --status")
            codigos.append(0)
        elif status in ("released", "already_released") or (status is None and d.get("closed") is True):
            out(f"{p['nome']}: fechada ({status or 'closed'})")
            codigos.append(0)
        elif status == "kept_open":
            out(f"{p['nome']}: mantida aberta (kept_open); NÃO fecha sozinha")
            codigos.append(0)
        elif status in INCERTOS:
            out(f"{p['nome']}: incerto ({status}): não está fechada; não repita; confira com --status")
            codigos.append(75)
        elif status == "refused" or "error" in d:
            out(f"{p['nome']}: recusado: {d.get('error') or d}")
            codigos.append(1)
        else:
            out(f"{p['nome']}: não fechada ({status or d.get('state') or 'sem status'})")
            codigos.append(1)
    return 1 if 1 in codigos else 75 if 75 in codigos else 0


# ---------------------------------------------------------------- conferir

def veredito(show):
    """(veredito, campos) do JSON do `worker-show --full`, com ou sem o envelope `{"ok", "result"}`."""
    r = show.get("result") if isinstance(show.get("result"), dict) else show
    d, w, tr = r.get("dispatch") or {}, r.get("worker") or {}, r.get("terminalResource") or {}
    c = {"state": w.get("state"), "stage": w.get("stage"), "dispatch_status": d.get("status"),
         "taskId": d.get("taskId") or d.get("task_id") or (r.get("projection") or {}).get("taskId"),
         "completedAt": d.get("completedAt"), "autoReleaseAt": r.get("autoReleaseAt"),
         "releaseState": tr.get("releaseState"), "retainedReason": tr.get("retainedReason")}
    if c["releaseState"] == "released":
        # o host libera sozinho succeeded e failed: o `failed` liberado continua falha; `stopped` + liberado depois do
        # --stop é "liberada"
        v = "liberada (falhou)" if c["state"] == "failed" else "liberada"
    elif c["state"] in FALHOU:
        v = "falhou"
    elif c["state"] == "succeeded" and c["stage"] == "settled" and c["releaseState"] == "retained":
        v = f"encerrada, retida ({c['retainedReason'] or 'motivo não informado'}): não fecha sozinha"
    elif c["state"] == "succeeded" and c["stage"] == "settled" and c["completedAt"]:
        v = "encerrada e aceita"
    else:
        v = "ativa"
    return v, c


def linha_status(nome, c, v):
    ret = f" ({c['retainedReason']})" if c.get("retainedReason") else ""
    return (f"{nome} · {c['state'] or '?'}/{c['stage'] or '?'} · {c['dispatch_status'] or '?'} · {c['taskId'] or '?'} · "
            f"{c['completedAt'] or '—'} · {c['autoReleaseAt'] or '—'} · {c['releaseState'] or '?'}{ret} → {v}")


def consulta(escolhidas, entradas, brza_fn):
    """([(persona, veredito, campos, dispatch)], [(persona, linha)], [(persona, motivo)] de quem ficou sem veredito)."""
    achados, linhas, sem = [], [], []
    for p in escolhidas:
        d = sessions_map.dispatch_of(p, entradas)
        if not d:
            sem.append((p, "sem Dispatch no mapa nem no manifesto"))
            continue
        r, so, se = brza_fn(["orchestration", "worker-show", "--dispatch", d, "--full", "--json"])
        show = _json(so)
        if not isinstance(show, dict) or r != 0:
            sem.append((p, f"worker-show falhou (rc {r}): {(se or so or '').strip()[:300]}"))
            continue
        v, c = veredito(show)
        achados.append((p, v, c, d))
        linhas.append((p["nome"], linha_status(p["nome"], c, v)))
    return achados, linhas, sem


def status(escolhidas, root, sessions=None, espera=0, brza_fn=None, out=print, clock=time.time, sleep=time.sleep):
    """`--status`: só leitura. Com `espera` (s), repete a cada 5 s até todas encerradas ou liberadas (rc 0), alguma
    `falhou` (rc 1) ou o prazo (rc 75). A tabela sai na primeira volta e depois só quando algum veredito muda."""
    brza_fn = brza_fn or run_brza
    entradas = sessions_map.load_map(root, sessions)
    fim = clock() + espera
    antes = None
    while True:
        achados, linhas, sem = consulta(escolhidas, entradas, brza_fn)
        atual = {p["nome"]: v for p, v, _, _ in achados}
        if antes is None or atual != antes:
            for _, l in linhas:
                out(l)
            for p, motivo in sem:
                if antes is None:
                    out(f"{p['nome']}: {motivo}; nada a conferir")
        antes = atual
        if not espera:
            return 1 if sem else 0
        if not sem and all(v in OK_FINAL for _, v, _, _ in achados):
            return 0
        falhas = [p for p, v, _, _ in achados if v in ("falhou", "liberada (falhou)")]
        if falhas:
            out("falhou: " + ", ".join(p["nome"] for p in falhas) + "; parei de esperar")
            return 1
        if clock() >= fim:
            break
        sleep(5)
    faltam = [(p, v, c, d) for p, v, c, d in achados if v not in OK_FINAL]
    out("prazo: faltam " + ", ".join([f"{p['nome']} ({v})" for p, v, _, _ in faltam]
                                     + [f"{p['nome']} (sem veredito: {m})" for p, m in sem]))
    for p, v, c, d in faltam:
        out(f"  diagnóstico (o script não envia): o preâmbulo de {p['nome']} deveria ter usado "
            f"`orchestration send --type worker_done --task-id {c['taskId'] or '<taskId>'} --dispatch-id {d} "
            f"--outcome succeeded …`")
    return 75


# ---------------------------------------------------------------- CLI

def main(argv=None, *, sessions_fn=None, brza_fn=None, out=print, clock=time.time, sleep=time.sleep):
    ap = argparse.ArgumentParser(description="Abre, envia, fecha e confere as personas da reunião pelo brza sessions v2.")
    ap.add_argument("reuniao")
    ap.add_argument("personas", nargs="*", help="nome, slug ou sessão; `todas` ou nada = todas")
    ap.add_argument("--via", default="sessions", help="só `sessions` (as vias antigas saíram)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--close", action="store_true", help="brza sessions close (pede worker_done; closing NÃO é fechada)")
    ap.add_argument("--release", action="store_true", help="alias de --close")
    ap.add_argument("--stop", action="store_true", help="brza sessions close --force (parada guardada)")
    ap.add_argument("--keep-open", action="store_true", help="brza sessions close --keep-open")
    ap.add_argument("--send", action="store_true", help="brza sessions send, uma chamada para as personas")
    ap.add_argument("--message", help="o texto do --send")
    ap.add_argument("--round", type=int, help="o --send da rodada N: `Faça a rodada N: <dir>/rodada-N.md`")
    ap.add_argument("--operation", help="repete um send pending/unknown (uma persona, mesmo texto)")
    ap.add_argument("--status", action="store_true", help="worker-show de cada persona e o veredito (só leitura)")
    ap.add_argument("--wait-settled", type=float, metavar="SEG", help="com --status: espera as encerradas, até SEG")
    ap.add_argument("--sessions", help="arquivo do mapa (padrão: .sessions/sessions.jsonl da raiz comum do git)")
    ap.add_argument("--root", help="padrão: o topo do repositório git do cwd")
    a = ap.parse_args(argv)
    if a.via != "sessions":
        if a.via in VIAS_REMOVIDAS:
            print(VIA_REMOVIDA, file=sys.stderr)
            return 2
        ap.error(f"--via {a.via}: só `sessions`")
    a.root = os.path.abspath(a.root) if a.root else raiz_padrao()
    path = a.reuniao if os.path.isabs(a.reuniao) or not os.path.isfile(os.path.join(a.root, a.reuniao)) \
        else os.path.join(a.root, a.reuniao)
    with open(path, encoding="utf-8") as f:
        reuniao = json.load(f)
    escolhidas = pick(reuniao, a.personas)
    if a.send:
        if a.message and a.round:
            ap.error("--send pede --message OU --round, não os dois")
        if not (a.message or a.round):
            ap.error("--send pede --message ou --round")
        texto = a.message or round_message(reuniao, a.round)
        return enviar(reuniao, escolhidas, a.root, texto, a.operation, a.round, a.dry_run, sessions_fn, out)
    ciclo = [m for m, ligado in (("close", a.close or a.release), ("stop", a.stop), ("keep-open", a.keep_open)) if ligado]
    if len(ciclo) > 1:
        ap.error("--close/--release, --stop e --keep-open se excluem")
    if ciclo:
        return fechar(escolhidas, ciclo[0], a.root, a.sessions, a.dry_run, sessions_fn, out)
    if a.status:
        return status(escolhidas, a.root, a.sessions, a.wait_settled or 0, brza_fn, out, clock, sleep)
    return abrir(reuniao, escolhidas, a.root, a.sessions, a.dry_run, sessions_fn, out)


if __name__ == "__main__":
    sys.exit(main())
