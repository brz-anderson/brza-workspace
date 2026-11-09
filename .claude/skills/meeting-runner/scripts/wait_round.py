#!/usr/bin/env python3
r"""wait_round.py: espera as personas entregarem a rodada N e narra cada chegada, sobre o `brza sessions wait`.

Uso:
    wait_round.py <N> --reuniao reuniao.json [--root DIR] [--timeout SEG] [--source {sessions,marker}]
                  [--sessions ARQUIVO] [--once] [--personas NOME ...]
                  [--poll SEG] [--sessions-state "cmd" | --no-state | --list-json arquivo]     # estes dois, só no marker

`--source sessions` (padrão; `mailbox` é alias): a espera é do `brza sessions wait <sessoes…> --any --timeout <t> --json`
(PLN-017 R6/R7), que lê o Run do mapa com `--all` e `--peek --wait`, sem consumir a caixa da coordenação. O fim de rodada é
a mensagem `status` da persona com `round_id` e `dispatchId` do envio, que o v2 já converte em `done`. O worklog continua
sendo o registro: chegada pelo v2 sem o marcador `<!-- fim-rodada-N -->` na última linha sai como
`⚠ <nome> avisou o fim da rodada N mas o worklog não termina no marcador`. `--source marker` mantém o modo de arquivo
(só o marcador), para chat sem Dispatch.

O RELÓGIO é o do mapa: a rodada começa no `at` do `last_send` de cada sessão (para a R1, o `at` do `open`, cujo
`operation` é o `round_id` inicial), e não no início do script. O PRAZO: lê `(duração: ~M min)` da primeira linha de
`rodada-N.md`; sem `--timeout`, o limite é `max(M min + 120 s, 180 s)` contado do início da rodada (nunca encerra antes da
duração anunciada); sem duração anunciada, o de antes (180 s até a primeira chegada; depois 2 x a mediana das latências,
mínimo 180 s). `--timeout` explícito conta do início do script. Cada chamada do `wait` leva `min(180, o que falta)`; sem
chegada em 180 s, a linha de status se repete (a narração de 3 min). `--once`: uma chamada com `--timeout 0`.
`--personas` restringe a espera ao subconjunto da rodada. O `state` de quem falta (o campo `pending[].state` do v2) entra
na linha final; `--no-state` o tira.

Saída, uma linha por chegada:
    R2 · 2/3 — entregaram Prumo, Trava; faltam Relance (Antigravity, 5 min)

OS EVENTOS que o `wait` devolve (o Run INTEIRO, sem `createdAt`; os ids já narrados ficam em `<dir da reunião>/eventos-vistos.json`,
lido e gravado a cada invocação, e só o evento novo é classificado e narrado; dedupe pelo `id`): contam para a persona quando `from` é o `sender` do mapa ou o
`payload.dispatchId|dispatch_id` é o `dispatch` do mapa; evento de outro Dispatch do mesmo Run é ignorado.
`escalation` "Worker stopped without reporting" (ou `payload.stopReason == "finished"`) é ruído previsto do fim de turno
sem `worker_done`: não imprime por evento, e o fim leva UMA linha com a contagem. `question`, `blocked`,
`decision_gate` e outro `escalation` viram `⚠ <nome> enviou <tipo>: <assunto>`; `worker_done` de persona antes do
encerramento vira `⚠ <nome> enviou worker_done antes do encerramento`; `status` não imprime nada. Desfecho `failed`
(`✗ <nome> falhou (<latency_source>)`) e `blocked` (`⚠ <nome> está blocked: leia com brza sessions read <sessao> --last`)
contam como fim da persona e levam o rc a 1. Erro do v2 (`{"error": …}`, como "nenhum send registrado") imprime
`erro do brza sessions wait: …` e sai 1: não cai para o marcador em silêncio.

Termina com 0 (todas chegaram), 2 no limite (quem falta, com o `state` do v2) ou 1 (erro ou desfecho failed/blocked,
também quando o limite chega com uma delas já registrada).
Funções puras para teste: `scan`, `status_line`, `compute_timeout`, `calc_limite`, `classifica_evento`, `run` (que recebe
`wait_fn(sessoes, timeout_s) -> (rc, dict)`).
"""
import argparse
import json
import os
import re
import shlex
import statistics
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import common  # noqa: E402
import sessions_map  # noqa: E402

BRZA = os.environ.get("BRZA_BIN", "brza")
MARCADOR = re.compile(r"^<!-- fim-rodada-(\d+) -->$")
RUNTIME_NOME = {"claude": "Claude", "codex": "Codex", "grok": "Grok", "antigravity": "Antigravity"}
STATUS_A_CADA = 180
ATENCAO = {"question", "blocked", "decision_gate", "escalation"}
RUIDO_ASSUNTO = "worker stopped without reporting"


def last_marker(path):
    """N do marcador que é a última linha não vazia do arquivo; None se não for ou se o arquivo não existe."""
    try:
        with open(path, encoding="utf-8") as f:
            texto = common.corta_medida(f.read())  # a `## Medida` do `brza note commit` vem depois do marcador e não invalida
        linhas = [l.rstrip() for l in texto.split("\n") if l.strip()]  # marcador recuado não vale (o `tally.py` também recusa)
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


def calc_limite(duracao_min, latencias):
    """O limite (s) contado do início da rodada, sem `--timeout`: com duração anunciada, `max(duração + 120 s, 180 s)`;
    sem ela, `compute_timeout`."""
    if duracao_min:
        return max(duracao_min * 60 + 120.0, 180.0)
    return compute_timeout(latencias)


def fetch_states(reuniao, list_json=None, cmd=None):
    """{sessao: state} de `brza sessions list --json`; {} se o comando ou o JSON falhar (só o modo marker)."""
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
    nomes = {p.get("sessao") for p in reuniao["personas"]}
    out = {s.get("name"): s.get("state") for s in sess if s.get("name") in nomes}
    for p in reuniao["personas"]:  # sobrescrita do manifesto: a linha do list que traz a sessão da persona
        ids = {p.get("claude_session"), p.get("provider_session")} - {None, ""}
        for s in sess:
            if ids & {s.get("claude_session"), s.get("provider_session")}:
                out[p.get("sessao")] = s.get("state")
    return out


raiz_padrao = common.raiz_padrao


def wait_argv(sessoes, timeout_s):
    """O argv (sem o `brza sessions`) do `wait`: `wait <sessoes…> --any --timeout <t> --json`."""
    return ["wait", *sessoes, "--any", "--timeout", f"{max(0.0, timeout_s):g}", "--json"]


def wait_brza(sessoes, timeout_s):
    """O padrão do `wait_fn`: `brza sessions wait <sessoes…> --any --timeout <t> --json`; (rc, dict).
    `brza` ausente ou saída que não é JSON vira rc 127 e `{"error": …}`."""
    argv = [BRZA, "sessions", *wait_argv(sessoes, timeout_s)]
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout_s + 60)
    except (OSError, subprocess.SubprocessError) as e:
        return 127, {"error": str(e)}
    try:
        dado = json.loads(r.stdout)
    except ValueError:
        return r.returncode or 1, {"error": f"saída sem JSON (rc {r.returncode}): {(r.stderr or r.stdout).strip()[:200]}"}
    return r.returncode, dado if isinstance(dado, dict) else {"error": "JSON inesperado"}


def _dispatch_do_evento(ev):
    pl = ev.get("payload") if isinstance(ev.get("payload"), dict) else {}
    return pl.get("dispatchId") or pl.get("dispatch_id")


def dono_do_evento(ev, personas, entradas):
    """A persona dona do evento: `from` igual ao `sender` do mapa ou o dispatch do payload igual ao `dispatch` do mapa."""
    remetente = ev.get("from") or ev.get("from_handle")
    d = _dispatch_do_evento(ev)
    for p in personas:
        e = entradas.get(p.get("sessao")) or {}
        disp = sessions_map.dispatch_of(p, entradas)
        if (remetente and e.get("sender") and remetente == e["sender"]) or (d and disp and d == disp):
            return p
    return None


def classifica_evento(ev):
    """'ruido' | 'atencao' | 'worker_done' | 'status' | 'outro' para um evento do `wait`."""
    tipo = str(ev.get("type") or "").lower().replace("-", "_")
    pl = ev.get("payload") if isinstance(ev.get("payload"), dict) else {}
    if tipo == "escalation" and (str(ev.get("subject") or "").strip().lower() == RUIDO_ASSUNTO
                                 or pl.get("stopReason") == "finished"):
        return "ruido"
    if tipo in ATENCAO:
        return "atencao"
    if tipo == "worker_done":
        return "worker_done"
    if tipo == "status":
        return "status"
    return "outro"


def carrega_vistos(path):
    """Os ids de evento já narrados em invocações anteriores (`eventos-vistos.json`); vazio sem arquivo ou com JSON ruim."""
    if not path:
        return set()
    try:
        with open(path, encoding="utf-8") as f:
            dado = json.load(f)
    except (OSError, ValueError):
        return set()
    return {str(x) for x in dado} if isinstance(dado, list) else set()


def grava_vistos(path, vistos):
    """Grava os ids vistos de forma atômica (arquivo temporário e `os.replace`)."""
    if not path:
        return
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = f"{path}.{os.getpid()}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(sorted(vistos), f, ensure_ascii=False)
    os.replace(tmp, path)


def inicio_da_rodada(personas, entradas):
    """O `at` do `last_send` mais recente das personas (epoch), ou None sem nenhum; o relógio é o do mapa."""
    ts = [sessions_map.epoch(((entradas.get(p.get("sessao")) or {}).get("last_send") or {}).get("at")) for p in personas]
    ts = [t for t in ts if t is not None]
    return max(ts) if ts else None


def run(reuniao, n, root, *, timeout=None, poll=5.0, once=False, state_fn=None, clock=None, sleep=None,
        out=None, source="marker", wait_fn=None, entradas=None, personas=None, duracao=None, com_state=True,
        vistos_path=None):
    """O laço da espera. `clock` (epoch), `sleep`, `out` e `wait_fn` se injetam nos testes. Devolve 0, 2 ou 1.

    `source="marker"` (o padrão da biblioteca; o da linha de comando é `sessions`) é o modo de arquivo; `sessions` usa `wait_fn(sessoes, timeout_s) -> (rc, dict)` (padrão
    `wait_brza`). `personas` restringe a espera ao subconjunto; `duracao` é a duração anunciada, em minutos."""
    out = out or (lambda s: print(s, flush=True))
    clock, sleep = clock or time.time, sleep or time.sleep
    todas = [p for p in reuniao["personas"] if not personas or p["nome"] in personas or p.get("sessao") in personas]
    rsub = {**reuniao, "personas": todas}
    if source == "marker":
        return _run_marker(rsub, n, root, timeout, poll, once, state_fn, clock, sleep, out)
    wait_fn = wait_fn or wait_brza
    entradas = entradas if entradas is not None else {}
    t0 = clock()
    ini = inicio_da_rodada(todas, entradas)
    ini = ini if ini is not None else t0
    vistos = carrega_vistos(vistos_path)
    chegaram, latencias, ruido = [], [], 0
    falhou = False
    states = {}
    pessoas = {p["nome"]: p for p in todas}
    por_sessao = {p["sessao"]: p for p in todas}

    def fim(rc):
        if ruido:
            out(f'ruído previsto: {ruido} avisos "Worker stopped without reporting" '
                '(fim de turno sem worker_done entre rodadas); não responda')
        return rc

    while True:
        pendentes = [p for p in todas if p["nome"] not in chegaram]
        agora = clock()
        limite_abs = (t0 + timeout) if timeout is not None else (ini + calc_limite(duracao, latencias))
        espera = 0 if once else max(0.0, min(float(STATUS_A_CADA), limite_abs - agora))
        rc, dado = wait_fn([p["sessao"] for p in pendentes], espera)
        if "error" in dado and "done" not in dado:
            out(f"erro do brza sessions wait: {dado['error']}")
            return fim(1)
        agora = clock()
        nova, novos_vistos = False, False
        for ev in dado.get("events") or []:
            chave = ev.get("id") or json.dumps(ev, sort_keys=True, ensure_ascii=False)
            if chave in vistos:
                continue
            dono = dono_do_evento(ev, reuniao["personas"], entradas)
            if dono is not None and dono not in todas:
                continue   # persona da reunião FORA desta rodada: fica para a próxima invocação que a inclua
            vistos.add(chave)
            novos_vistos = True
            p = dono
            if p is None:
                continue
            classe = classifica_evento(ev)
            tipo = str(ev.get("type") or "").lower().replace("-", "_")
            if classe == "ruido":
                ruido += 1
            elif classe == "atencao":
                out(f"⚠ {p['nome']} enviou {tipo}: {ev.get('subject') or ''}")
            elif classe == "worker_done":
                out(f"⚠ {p['nome']} enviou worker_done antes do encerramento")
        if novos_vistos:
            grava_vistos(vistos_path, vistos)
            novos_vistos = False
        for row in dado.get("done") or []:
            p = por_sessao.get(row.get("name"))
            if p is None or p["nome"] in chegaram:
                continue
            desfecho = row.get("outcome")
            chegaram.append(p["nome"])
            if isinstance(row.get("latency_s"), (int, float)):
                latencias.append(float(row["latency_s"]))
            nova = True
            lat = f" ({p['nome']}: {int(round(row['latency_s']))} s)" if isinstance(row.get("latency_s"), (int, float)) else ""
            if desfecho == "failed":
                out(f"✗ {p['nome']} falhou ({row.get('latency_source') or '?'})")
                falhou = True
            elif desfecho == "blocked":
                out(f"⚠ {p['nome']} está blocked: leia com brza sessions read {p['sessao']} --last")
                falhou = True
            elif desfecho != "done":
                out(f"⚠ {p['nome']} terminou com {desfecho}: leia com brza sessions read {p['sessao']} --last")
                falhou = True
            else:
                m = last_marker(os.path.join(root, worklog_path(reuniao, p)))
                if (m or 0) < n:
                    out(f"⚠ {p['nome']} avisou o fim da rodada {n} mas o worklog não termina no marcador")
            out(status_line(n, rsub, chegaram, agora - ini) + lat)
        for q in dado.get("pending") or []:
            if q.get("name") in por_sessao:
                states[q["name"]] = q.get("state")
        if len(chegaram) == len(todas):
            return fim(1 if falhou else 0)
        limite_abs = (t0 + timeout) if timeout is not None else (ini + calc_limite(duracao, latencias))
        if once or agora >= limite_abs:
            out(status_line(n, rsub, chegaram, agora - ini, (states or None) if com_state else None))
            return fim(1 if falhou else 2)
        if not nova:
            out(status_line(n, rsub, chegaram, agora - ini))


def _run_marker(reuniao, n, root, timeout, poll, once, state_fn, clock, sleep, out):
    """O modo de arquivo: o marcador `<!-- fim-rodada-N -->` como última linha do worklog."""
    t0 = clock()
    chegaram, latencias, ultima_linha = [], [], t0
    while True:
        agora = clock()
        atual = scan(reuniao, n, root)
        for p in reuniao["personas"]:
            nome = p["nome"]
            if atual.get(nome) and nome not in chegaram:
                chegaram.append(nome)
                latencias.append(agora - t0)
                out(status_line(n, reuniao, chegaram, agora - t0))
                ultima_linha = agora
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
        sleep(poll)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Espera o fim da rodada pelo brza sessions wait (ou pelo marcador do worklog).")
    ap.add_argument("n", type=int)
    ap.add_argument("--reuniao", required=True)
    ap.add_argument("--root", help="padrão: o topo do repositório git do cwd")
    ap.add_argument("--timeout", type=float)
    ap.add_argument("--poll", type=float, help="segundos entre leituras do marcador (padrão 5; só no --source marker)")
    ap.add_argument("--source", choices=("sessions", "mailbox", "marker"), default="sessions",
                    help="`mailbox` é alias de `sessions`")
    ap.add_argument("--sessions", help="mapa de sessões (padrão: .sessions/sessions.jsonl da raiz comum do git)")
    ap.add_argument("--sessions-state", help="comando que imprime o JSON do `brza sessions list --json` (marker)")
    ap.add_argument("--no-state", action="store_true")
    ap.add_argument("--list-json", help="arquivo com o JSON do list (para teste)")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--personas", nargs="+", metavar="NOME", help="só estas personas (nome, slug ou sessão)")
    a = ap.parse_args(argv)
    a.root = os.path.abspath(a.root) if a.root else raiz_padrao()
    path = a.reuniao if os.path.isabs(a.reuniao) or not os.path.isfile(os.path.join(a.root, a.reuniao)) \
        else os.path.join(a.root, a.reuniao)
    with open(path, encoding="utf-8") as f:
        reuniao = json.load(f)
    if not any(os.path.isfile(os.path.join(a.root, worklog_path(reuniao, p))) for p in reuniao["personas"]):
        print(f"aviso: nenhum worklog existe ainda sob {a.root}; se a raiz está certa, as personas ainda não gravaram",
              file=sys.stderr)
    nomes = None
    if a.personas:
        try:
            nomes = {p["nome"] for p in common.resolver_personas(reuniao, a.personas)}
        except ValueError as e:
            print(str(e), file=sys.stderr)
            return 2
    source = "sessions" if a.source == "mailbox" else a.source
    state_fn = None if a.no_state or source == "sessions" else (lambda: fetch_states(reuniao, a.list_json, a.sessions_state))
    entradas = sessions_map.load_map(a.root, a.sessions) if source == "sessions" else {}
    _, _, duracao = common.cabecalho_rodada(os.path.join(a.root, reuniao.get("dir", "."), f"rodada-{a.n}.md"))
    return run(reuniao, a.n, a.root, timeout=a.timeout, poll=a.poll or 5.0, once=a.once, state_fn=state_fn,
               source=source, entradas=entradas, personas=nomes, duracao=duracao, com_state=not a.no_state,
               vistos_path=os.path.join(a.root, reuniao.get("dir", "."), "eventos-vistos.json"))


if __name__ == "__main__":
    sys.exit(main())
