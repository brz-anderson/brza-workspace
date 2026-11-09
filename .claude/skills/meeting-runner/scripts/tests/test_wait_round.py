"""Testes do wait_round.py, com worklogs temporários e relógio falso."""
import json
import os
import shutil
import tempfile
from pathlib import Path
import unittest

import _paths  # noqa: F401
from _paths import HERE, le

import wait_round

try:
    import sessions_map
except ImportError:  # snapshot anterior ao v2: cada teste falha por si
    sessions_map = None

REUNIAO = {"id": "t", "worklog": "wl/{slug}.md", "personas": [
    {"nome": "Lenha", "slug": "lenha", "sessao": "x-lenha", "runtime": "codex"},
    {"nome": "Faísca", "slug": "faisca", "sessao": "x-faisca", "runtime": "grok"},
    {"nome": "Tição", "slug": "ticao", "sessao": "x-ticao", "runtime": "claude"},
]}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        os.makedirs(os.path.join(self.tmp, "wl"))

    def escreve(self, slug, n=None, depois="", corpo="### Rodada 2: x\n\ntexto\n"):
        with open(os.path.join(self.tmp, f"wl/{slug}.md"), "w", encoding="utf-8") as f:
            f.write(corpo + (f"\n<!-- fim-rodada-{n} -->\n" if n else "") + depois)


class Scan(Base):
    def test_ultima_linha_exata(self):
        self.escreve("lenha", 2)
        self.escreve("faisca", 2, depois="\n## O que ficou\n\nNada.\n")  # marcador no meio: não vale
        self.escreve("ticao", 1)  # marcador da rodada anterior: não vale
        self.assertEqual(wait_round.scan(REUNIAO, 2, self.tmp), {"Lenha": True, "Faísca": False, "Tição": False})

    def test_sem_worklog_e_marcador_de_rodada_adiante(self):
        self.escreve("ticao", 3)  # já passou da rodada pedida
        self.assertEqual(wait_round.scan(REUNIAO, 2, self.tmp), {"Lenha": False, "Faísca": False, "Tição": True})

    def test_marcador_recuado_nao_vale(self):
        with open(os.path.join(self.tmp, "wl/lenha.md"), "w", encoding="utf-8") as f:
            f.write("### Rodada 2: x\n\ntexto\n\n  <!-- fim-rodada-2 -->\n")
        self.assertFalse(wait_round.scan(REUNIAO, 2, self.tmp)["Lenha"])

    def test_fim_real_do_worklog_commitado_com_a_secao_medida(self):
        """O `brza note commit` acrescenta `## Medida` depois do marcador; o fim real do worklog da Trava ainda vale."""
        with open(os.path.join(self.tmp, "wl/lenha.md"), "w", encoding="utf-8") as f:
            f.write(le("p7", "worklogs", "trava-commitado.md").replace("fim-rodada-3", "fim-rodada-2"))
        self.assertTrue(wait_round.scan(REUNIAO, 2, self.tmp)["Lenha"])

    def test_outra_secao_depois_do_marcador_continua_invalidando(self):
        for extra in ("## O que ficou\n\nNada.\n", "## Medida\n\nx\n\n## O que ficou\n\nNada.\n"):
            with open(os.path.join(self.tmp, "wl/lenha.md"), "w", encoding="utf-8") as f:
                f.write("### Rodada 2: x\n\ntexto\n\n<!-- fim-rodada-2 -->\n\n" + extra)
            self.assertFalse(wait_round.scan(REUNIAO, 2, self.tmp)["Lenha"], extra)

    def test_linhas_em_branco_no_fim(self):
        self.escreve("lenha", 2, depois="\n\n   \n")
        self.assertTrue(wait_round.scan(REUNIAO, 2, self.tmp)["Lenha"])


class StatusLine(unittest.TestCase):
    def test_forma_do_pedido(self):
        r = {"personas": [{"nome": n, "runtime": rt} for n, rt in
                          [("Lenha", "codex"), ("Cinza", "codex"), ("Tição", "claude"), ("Fole", "claude"),
                           ("Faísca", "grok"), ("Fogareiro", "antigravity")]]}
        self.assertEqual(wait_round.status_line(2, r, ["Lenha", "Cinza", "Tição", "Fole"], 300),
                         "R2 · 4/6 — entregaram Lenha, Cinza, Tição, Fole; "
                         "faltam Faísca (Grok, 5 min) e Fogareiro (Antigravity, 5 min)")

    def test_ninguem_e_todos_e_state(self):
        r = {"personas": [{"nome": "A", "runtime": "claude", "sessao": "s-a"}, {"nome": "B", "runtime": "codex",
                                                                                "sessao": "s-b"}]}
        self.assertEqual(wait_round.status_line(1, r, [], 30), "R1 · 0/2 — faltam A (Claude) e B (Codex)")
        self.assertEqual(wait_round.status_line(1, r, ["B", "A"], 30), "R1 · 2/2 — todos entregaram: B, A")
        self.assertEqual(wait_round.status_line(1, r, ["A"], 90, {"s-b": "working"}),
                         "R1 · 1/2 — entregaram A; faltam B (Codex, 1 min, state working)")

    def test_timeout_calculado(self):
        self.assertEqual(wait_round.compute_timeout([]), 180.0)
        self.assertEqual(wait_round.compute_timeout([30, 50]), 180.0)   # 2 x 40 = 80, abaixo do piso
        self.assertEqual(wait_round.compute_timeout([100, 200, 400]), 400.0)


class Laco(Base):
    """Relógio falso: cada `sleep(poll)` avança o tempo e pode gravar um marcador."""

    def monta(self, agenda, poll=10.0):
        t = {"v": 0.0}
        saidas = []

        def clock():
            return t["v"]

        def sleep(s):
            t["v"] += s
            for quando, slug in list(agenda):
                if t["v"] >= quando:
                    self.escreve(slug, 2)
                    agenda.remove((quando, slug))
        return clock, sleep, saidas.append, saidas

    def test_uma_linha_por_chegada_e_sai_0(self):
        self.escreve("lenha", 2)  # já entregou antes de a espera começar
        clock, sleep, out, saidas = self.monta([(20, "ticao"), (50, "faisca")])
        rc = wait_round.run(REUNIAO, 2, self.tmp, poll=10, clock=clock, sleep=sleep, out=out)
        self.assertEqual(rc, 0)
        self.assertEqual(len(saidas), 3)
        self.assertTrue(saidas[0].startswith("R2 · 1/3 — entregaram Lenha; faltam Faísca"))
        self.assertTrue(saidas[1].startswith("R2 · 2/3 — entregaram Lenha, Tição; faltam Faísca (Grok)"))
        self.assertTrue(saidas[2].startswith("R2 · 3/3 — todos entregaram: Lenha, Tição, Faísca"))

    def test_timeout_automatico_mostra_o_state(self):
        clock, sleep, out, saidas = self.monta([])
        rc = wait_round.run(REUNIAO, 2, self.tmp, poll=30, clock=clock, sleep=sleep, out=out,
                            state_fn=lambda: {"x-lenha": "working", "x-faisca": "idle"})
        self.assertEqual(rc, 2)
        # 180 s sem chegada: o teto automático vence no mesmo instante do primeiro status; só a linha final sai
        self.assertEqual(len(saidas), 1)
        self.assertEqual(saidas[0], "R2 · 0/3 — faltam Lenha (Codex, 3 min, state working), "
                                    "Faísca (Grok, 3 min, state idle) e Tição (Claude, 3 min, state ?)")

    def test_status_periodico_com_timeout_longo(self):
        clock, sleep, out, saidas = self.monta([])
        rc = wait_round.run(REUNIAO, 2, self.tmp, timeout=400, poll=60, clock=clock, sleep=sleep, out=out)
        self.assertEqual(rc, 2)
        self.assertEqual(len(saidas), 3)  # aos 180 s, aos 360 s e a final aos 420 s
        self.assertIn("faltam Lenha (Codex, 3 min)", saidas[0])

    def test_once(self):
        self.escreve("lenha", 2)
        saidas = []
        rc = wait_round.run(REUNIAO, 2, self.tmp, once=True, out=saidas.append)
        self.assertEqual(rc, 2)
        self.assertEqual(len(saidas), 2)  # a chegada e o status

    def test_fetch_states_acha_a_persona_pela_sessao_do_manifesto(self):
        r = {"personas": [dict(REUNIAO["personas"][0], sessao="so-worker", claude_session="c-1")]}
        arq = os.path.join(self.tmp, "list.json")
        with open(arq, "w") as f:
            json.dump({"sessions": [{"name": "outro-nome", "claude_session": "c-1", "state": "working"}]}, f)
        self.assertEqual(wait_round.fetch_states(r, list_json=arq), {"so-worker": "working"})

    def test_raiz_padrao_e_o_topo_do_git(self):
        antes = os.getcwd()
        try:
            os.chdir(HERE)
            self.assertEqual(os.path.realpath(wait_round.raiz_padrao()),
                             os.path.realpath(os.path.join(HERE, *([".."] * 5))))
        finally:
            os.chdir(antes)

    def test_fetch_states_tolera_brza_ausente_e_le_arquivo(self):
        self.assertEqual(wait_round.fetch_states(REUNIAO, cmd="comando-que-nao-existe-xyz --json"), {})
        arq = os.path.join(self.tmp, "list.json")
        with open(arq, "w") as f:
            json.dump({"sessions": [{"name": "x-lenha", "state": "working"}, {"name": "outro", "state": "idle"}]}, f)
        self.assertEqual(wait_round.fetch_states(REUNIAO, list_json=arq), {"x-lenha": "working"})
        with open(arq, "w") as f:
            f.write("não é json")
        self.assertEqual(wait_round.fetch_states(REUNIAO, list_json=arq), {})





# ---------------------------------------------------------------- o modo `sessions` (o padrão da linha de comando)

BASE = 1794240000.0  # um instante qualquer, em epoch; o relógio dos testes e o `at` do mapa partem dele


def iso(delta=0):
    from datetime import datetime, timezone
    return datetime.fromtimestamp(BASE + delta, timezone.utc).isoformat(timespec="milliseconds")


PS = {"personas": [
    {"nome": "Prumo", "slug": "prumo", "sessao": "ci-prumo", "runtime": "claude"},
    {"nome": "Trava", "slug": "trava", "sessao": "ci-trava", "runtime": "grok"},
    {"nome": "Relance", "slug": "relance", "sessao": "ci-relance", "runtime": "antigravity"}],
    "worklog": "wl/{slug}.md", "dir": "dir"}
IDS = {"ci-prumo": ("ctx_p", "sw_p"), "ci-trava": ("ctx_t", "sw_t"), "ci-relance": ("ctx_r", "sw_r")}


def mapa(envio=0, operation="op-r2", so=None):
    rows = []
    for sessao, (d, snd) in IDS.items():
        if so and sessao not in so:
            continue
        rows.append({"event": "open", "at": iso(envio - 3600), "name": sessao, "chat": "c-" + sessao, "dispatch": d,
                     "run": "run_1", "sender": snd, "coordinator": "orca_session_id:x", "operation": "op-r1",
                     "round_id": "op-r1"})
        rows.append({"event": "send", "at": iso(envio), "name": sessao, "chat": "c-" + sessao, "operation": operation,
                     "round_id": operation, "receipt": {"status": "accepted"}})
    return sessions_map.fold_map(rows)


def done(sessao, latencia=40.0, outcome="done", fonte="mailbox"):
    return {"name": sessao, "agent": "claude", "outcome": outcome, "latency_s": latencia, "latency_source": fonte}


def evento(tipo, sessao, assunto="x", id=None, payload=None, **extra):
    d, snd = IDS[sessao]
    return {"id": id or f"{tipo}-{sessao}-{assunto}", "type": tipo, "from": snd, "subject": assunto,
            "payload": payload if payload is not None else {"dispatchId": d}, **extra}


class Sessions(Base):
    """`wait_fn` falso: cada chamada avança o relógio falso pelo `timeout` pedido e devolve o próximo resultado."""

    def roda(self, respostas, n=2, entradas=None, personas=None, timeout=None, duracao=None, once=False, inicio=0.0):
        t = {"v": BASE + inicio}
        respostas = list(respostas)
        self.chamadas, saidas = [], []

        def wait_fn(sessoes, timeout_s):
            self.chamadas.append((list(sessoes), timeout_s))
            r = respostas.pop(0) if respostas else (75, {"done": [], "pending": [], "timed_out": True, "events": []})
            r = r() if callable(r) else r
            # o v2 volta na hora quando há `done` (`--any`) e só gasta o timeout inteiro quando nada chega
            t["v"] += 5.0 if r[1].get("done") else timeout_s
            return r
        rc = wait_round.run(PS, n, self.tmp, source="sessions", wait_fn=wait_fn, clock=lambda: t["v"],
                            sleep=lambda s: None, out=saidas.append, entradas=entradas if entradas is not None else mapa(),
                            personas=personas, timeout=timeout, duracao=duracao, once=once)
        return rc, saidas

    def marcador(self, slug, n=2):
        self.escreve(slug, n)

    def test_chegada_pelo_v2_com_latencia_e_o_marcador_confere(self):
        self.marcador("prumo")
        self.marcador("trava")
        self.marcador("relance")
        rc, s = self.roda([(0, {"done": [done("ci-prumo", 40)], "pending": [], "timed_out": False, "events": []}),
                           (0, {"done": [done("ci-trava", 70), done("ci-relance", 80)], "pending": [], "events": []})])
        self.assertEqual(rc, 0)
        self.assertEqual(s[0], "R2 · 1/3 — entregaram Prumo; faltam Trava (Grok) e Relance (Antigravity) (Prumo: 40 s)")
        self.assertTrue(s[1].startswith("R2 · 2/3 — entregaram Prumo, Trava;"))
        self.assertTrue(s[-1].startswith("R2 · 3/3 — todos entregaram: Prumo, Trava, Relance"))
        self.assertEqual(self.chamadas[0][0], ["ci-prumo", "ci-trava", "ci-relance"])
        self.assertEqual(self.chamadas[1][0], ["ci-trava", "ci-relance"])      # só quem falta
        self.assertFalse(any("⚠" in l for l in s))

    def test_chegada_sem_marcador_no_worklog_avisa(self):
        self.escreve("prumo", None)  # worklog sem o marcador final
        rc, s = self.roda([(0, {"done": [done("ci-prumo")], "events": []})], personas=["Prumo"])
        self.assertEqual(rc, 0)
        self.assertIn("⚠ Prumo avisou o fim da rodada 2 mas o worklog não termina no marcador", s)

    def test_o_relogio_da_rodada_e_o_do_mapa(self):
        # o `send` foi 10 min antes de o script começar: a linha já diz 10 min de espera
        rc, s = self.roda([], entradas=mapa(envio=-600), duracao=30, once=True, inicio=0)
        self.assertEqual(rc, 2)
        self.assertIn("faltam Prumo (Claude, 10 min)", s[-1])

    def test_inicio_da_rodada_e_o_at_do_ultimo_send_e_na_r1_o_do_open(self):
        e = mapa(envio=100)
        self.assertEqual(wait_round.inicio_da_rodada(PS["personas"], e), BASE + 100)
        so_open = sessions_map.fold_map([{"event": "open", "at": iso(7), "name": "ci-prumo", "chat": "c",
                                          "operation": "op-r1"}])
        self.assertEqual(wait_round.inicio_da_rodada(PS["personas"][:1], so_open), BASE + 7)
        self.assertIsNone(wait_round.inicio_da_rodada(PS["personas"], {}))

    # X6: o prazo vem da duração anunciada
    def test_calc_limite(self):
        self.assertEqual(wait_round.calc_limite(10, []), 720.0)       # 10 min + 120 s
        self.assertEqual(wait_round.calc_limite(1, [999]), 180.0)     # o piso de 180 s
        self.assertEqual(wait_round.calc_limite(None, []), 180.0)
        self.assertEqual(wait_round.calc_limite(None, [100, 200, 400]), 400.0)

    def test_nunca_encerra_antes_da_duracao_anunciada(self):
        rc, s = self.roda([], duracao=10)
        self.assertEqual(rc, 2)
        # 4 chamadas de 180 s: 720 s = 10 min + 120 s, e nenhuma saída antes de 600 s
        self.assertEqual([t for _, t in self.chamadas], [180.0, 180.0, 180.0, 180.0])
        # sem chegada por 180 s, a linha de status se repete (a narração de 3 min)
        self.assertEqual(sum(l.startswith("R2 · 0/3") for l in s), 4)

    def test_sem_duracao_o_limite_e_o_de_antes(self):
        rc, s = self.roda([])
        self.assertEqual(rc, 2)
        self.assertEqual(len(self.chamadas), 1)

    def test_sem_duracao_depois_da_primeira_chegada_vale_2x_a_mediana(self):
        rc, s = self.roda([(0, {"done": [done("ci-prumo", 300)], "events": []})])
        # limite: 2 x 300 = 600 s do início; a 1ª chamada devolve a chegada aos 5 s e faltam 595 s
        self.assertEqual(rc, 2)
        self.assertEqual([t for _, t in self.chamadas], [180.0, 180.0, 180.0, 180.0, 55.0])

    def test_timeout_explicito_conta_do_inicio_do_script(self):
        rc, s = self.roda([], timeout=400, entradas=mapa(envio=-5000))
        self.assertEqual(rc, 2)
        self.assertEqual([t for _, t in self.chamadas], [180.0, 180.0, 40.0])

    def test_once_e_uma_chamada_com_timeout_0(self):
        rc, s = self.roda([], once=True)
        self.assertEqual(rc, 2)
        self.assertEqual(self.chamadas, [(["ci-prumo", "ci-trava", "ci-relance"], 0)])

    # X3: os eventos
    def test_evento_de_outro_dispatch_do_mesmo_run_e_ignorado(self):
        estranho = {"id": "e1", "type": "question", "from": "sw_OUTRO", "subject": "dúvida", "payload": {"dispatchId": "ctx_z"}}
        rc, s = self.roda([(0, {"done": [done("ci-prumo")], "events": [estranho]})], personas=["Prumo"])
        self.assertFalse(any("dúvida" in l for l in s))

    def test_ruido_previsto_conta_uma_linha_no_fim(self):
        r = lambda i: evento("escalation", "ci-prumo", "Worker stopped without reporting", id=i,
                             payload={"dispatchId": "ctx_p", "stopReason": "finished"})
        rc, s = self.roda([(0, {"done": [], "events": [r("a"), r("b")]}),
                           (0, {"done": [done("ci-prumo")], "events": [r("a"), r("b"), r("c")]})], personas=["Prumo"],
                          timeout=1000)
        self.assertEqual(rc, 0)
        ruido = [l for l in s if l.startswith("ruído previsto")]
        self.assertEqual(ruido, ['ruído previsto: 3 avisos "Worker stopped without reporting" '
                                 '(fim de turno sem worker_done entre rodadas); não responda'])
        self.assertEqual(s[-1], ruido[0])
        self.assertFalse(any("Worker stopped" in l and l.startswith("⚠") for l in s))

    def test_atencao_real_e_worker_done_antes_do_encerramento(self):
        evs = [evento("question", "ci-trava", "posso usar X?"), evento("decision_gate", "ci-trava", "G"),
               evento("blocked", "ci-prumo", "preso"), evento("escalation", "ci-relance", "falhei"),
               evento("worker_done", "ci-relance", "pronto"), evento("status", "ci-prumo", "brza-sessions-round",
                                                                    payload={"round_id": "op-r2", "dispatchId": "ctx_p"})]
        rc, s = self.roda([(0, {"done": [], "events": evs})], once=True)
        self.assertIn("⚠ Trava enviou question: posso usar X?", s)
        self.assertIn("⚠ Trava enviou decision_gate: G", s)
        self.assertIn("⚠ Prumo enviou blocked: preso", s)
        self.assertIn("⚠ Relance enviou escalation: falhei", s)
        self.assertIn("⚠ Relance enviou worker_done antes do encerramento", s)
        self.assertFalse(any("brza-sessions-round" in l for l in s))   # o `status` não imprime nada

    def test_remetente_do_mapa_basta_sem_dispatch_no_payload(self):
        ev = evento("question", "ci-trava", "sem payload", payload={})
        rc, s = self.roda([(0, {"done": [], "events": [ev]})], once=True)
        self.assertIn("⚠ Trava enviou question: sem payload", s)

    def test_dedupe_por_id_entre_chamadas(self):
        ev = evento("question", "ci-trava", "uma vez", id="m1")
        rc, s = self.roda([(75, {"done": [], "events": [ev]}), (75, {"done": [], "events": [ev]})], timeout=400)
        self.assertEqual(sum("uma vez" in l for l in s), 1)

    # os desfechos
    def test_failed_e_blocked_contam_como_fim_e_levam_o_rc_a_1(self):
        for personas, resp, esperado in (
                (["Trava"], done("ci-trava", 30, "failed", "dispatch"), "✗ Trava falhou (dispatch)"),
                (["Trava"], done("ci-trava", 30, "blocked", "poll"),
                 "⚠ Trava está blocked: leia com brza sessions read ci-trava --last")):
            rc, s = self.roda([(1, {"done": [resp], "events": []})], personas=personas)
            self.assertEqual(rc, 1)
            self.assertIn(esperado, s)
            self.assertTrue(s[-1].startswith("R2 · 1/1 — todos entregaram: Trava"))

    def test_failed_de_uma_e_chegada_de_outra_termina_1(self):
        rc, s = self.roda([(1, {"done": [done("ci-prumo", 10, "failed")], "events": []}),
                           (0, {"done": [done("ci-trava", 50)], "events": []})], personas=["Prumo", "Trava"])
        self.assertEqual(rc, 1)

    # os erros do v2 não caem para o marcador em silêncio
    def test_erro_do_v2_imprime_e_sai_1(self):
        self.marcador("prumo")     # o marcador existe, mas NÃO vale: o erro não vira "chegou pelo marcador"
        rc, s = self.roda([(1, {"error": "ci-prumo: nenhum send registrado para esperar; envie a rodada primeiro"})],
                          personas=["Prumo"])
        self.assertEqual(rc, 1)
        self.assertEqual(s, ["erro do brza sessions wait: ci-prumo: nenhum send registrado para esperar; "
                             "envie a rodada primeiro"])

    # X18
    def test_personas_restringe_a_espera_ao_subconjunto(self):
        rc, s = self.roda([(0, {"done": [done("ci-trava"), done("ci-relance")], "events": []})],
                          personas=["Trava", "Relance"])
        self.assertEqual(rc, 0)
        self.assertEqual(self.chamadas[0][0], ["ci-trava", "ci-relance"])
        self.assertTrue(s[-1].startswith("R2 · 2/2 — todos entregaram: Trava, Relance"))
        self.assertNotIn("Prumo", "\n".join(s))

    def test_a_linha_de_status_final_leva_o_state_do_v2(self):
        rc, s = self.roda([(75, {"done": [], "timed_out": True, "events": [],
                                 "pending": [{"name": "ci-prumo", "state": "working", "elapsed_s": 5}]})], once=True)
        self.assertIn("Prumo (Claude, state working)", s[-1])

    def test_o_fim_do_log_real_do_v2(self):
        """O JSON real do `brza sessions wait --json`: escalation e worker_done de OUTRO Dispatch do mesmo Run."""
        real = json.loads(le("v2", "logs", "pln017-smoke-initial-wait.log"))
        rows = sessions_map.read_rows(os.path.join(os.path.dirname(HERE), "tests", "fixtures", "v2", "smoke-sessions.jsonl"))
        ent = sessions_map.fold_map(rows)
        reuniao = {"personas": [{"nome": "Inicial", "slug": "inicial", "sessao": "pln017-smoke-inicial", "runtime": "codex"}],
                   "worklog": "wl/{slug}.md"}
        self.escreve("inicial", 1)
        saidas = []
        abre = sessions_map.epoch("2026-11-09T13:20:08.695-03:00")
        rc = wait_round.run(reuniao, 1, self.tmp, source="sessions", wait_fn=lambda s, t: (0, real),
                            clock=lambda: abre + 31, sleep=lambda s: None, out=saidas.append, entradas=ent)
        self.assertEqual(rc, 0)
        self.assertEqual(saidas[0], "R1 · 1/1 — todos entregaram: Inicial (Inicial: 31 s)")
        self.assertEqual(saidas[1:], ['ruído previsto: 1 avisos "Worker stopped without reporting" '
                                      '(fim de turno sem worker_done entre rodadas); não responda'])

    def test_classifica_evento(self):
        c = wait_round.classifica_evento
        self.assertEqual(c({"type": "escalation", "subject": "Worker stopped without reporting"}), "ruido")
        self.assertEqual(c({"type": "escalation", "subject": "x", "payload": {"stopReason": "finished"}}), "ruido")
        self.assertEqual(c({"type": "escalation", "subject": "limite de cota"}), "atencao")
        self.assertEqual(c({"type": "decision_gate"}), "atencao")
        self.assertEqual(c({"type": "worker-done"}), "worker_done")
        self.assertEqual(c({"type": "status"}), "status")


class CorredorEMain(Base):
    def test_wait_brza_monta_o_argv_do_brza_sessions_wait(self):
        import subprocess
        visto = {}

        class R:
            returncode, stdout, stderr = 0, json.dumps({"done": [], "events": []}), ""

        def fake(argv, **kw):
            visto["argv"] = argv
            return R
        original = subprocess.run
        subprocess.run = fake
        try:
            rc, d = wait_round.wait_brza(["a", "b"], 180)
        finally:
            subprocess.run = original
        self.assertEqual(visto["argv"], [wait_round.BRZA, "sessions", "wait", "a", "b", "--any", "--timeout", "180", "--json"])
        self.assertEqual((rc, d), (0, {"done": [], "events": []}))

    def test_wait_brza_sem_binario_ou_sem_json_vira_erro(self):
        import subprocess
        original = subprocess.run

        def sem(argv, **kw):
            raise FileNotFoundError("brza")
        subprocess.run = sem
        try:
            rc, d = wait_round.wait_brza(["a"], 1)
        finally:
            subprocess.run = original
        self.assertEqual(rc, 127)
        self.assertIn("error", d)

        class R:
            returncode, stdout, stderr = 1, "CHECK: x", ""
        subprocess.run = lambda argv, **kw: R
        try:
            rc, d = wait_round.wait_brza(["a"], 1)
        finally:
            subprocess.run = original
        self.assertEqual(rc, 1)
        self.assertIn("saída sem JSON", d["error"])

    def manifesto(self):
        d = {"id": "t", "dir": "dir", "worklog": "wl/{slug}.md", "personas": PS["personas"]}
        os.makedirs(os.path.join(self.tmp, "dir"), exist_ok=True)
        with open(os.path.join(self.tmp, "reuniao.json"), "w", encoding="utf-8") as f:
            json.dump(d, f)
        with open(os.path.join(self.tmp, "dir", "rodada-2.md"), "w", encoding="utf-8") as f:
            f.write("# Rodada 2 — debate (duração: ~1 min)\n")
        rows = []
        for sessao, (disp, snd) in IDS.items():
            rows.append({"event": "open", "at": iso(-9), "name": sessao, "chat": "c", "dispatch": disp, "sender": snd,
                         "run": "r", "operation": "o1"})
            rows.append({"event": "send", "at": iso(-5), "name": sessao, "chat": "c", "operation": "o2"})
        with open(os.path.join(self.tmp, "m.jsonl"), "w", encoding="utf-8") as f:
            f.write("\n".join(json.dumps(r) for r in rows) + "\n")

    def test_main_mailbox_e_alias_de_sessions_e_le_o_mapa_e_a_duracao(self):
        self.manifesto()
        visto = []
        original, relogio = wait_round.wait_brza, wait_round.time.time
        agora = [BASE]

        def falso(sessoes, t):
            visto.append((list(sessoes), t))
            agora[0] += t                      # o relógio anda o que o `wait` esperou
            return 75, {"done": [], "events": []}
        wait_round.wait_brza = falso
        wait_round.time.time = lambda: agora[0]
        try:
            import contextlib, io
            for fonte in ("mailbox", "sessions"):
                visto.clear()
                agora[0] = BASE
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    rc = wait_round.main(["2", "--reuniao", "reuniao.json", "--root", self.tmp, "--sessions",
                                          os.path.join(self.tmp, "m.jsonl"), "--source", fonte, "--personas", "trava"])
                self.assertEqual(rc, 2)
                self.assertEqual(visto[0][0], ["ci-trava"])
                self.assertEqual(visto[0][1], 175.0)   # duração ~1 min: limite 180 s; o envio foi 5 s antes
        finally:
            wait_round.wait_brza, wait_round.time.time = original, relogio

    def test_main_marker_nao_usa_o_v2(self):
        self.manifesto()
        for slug in ("prumo", "trava", "relance"):
            self.escreve(slug, 2)
        import contextlib, io
        original = wait_round.wait_brza
        wait_round.wait_brza = lambda s, t: self.fail("o marker não chama o brza sessions wait")
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                rc = wait_round.main(["2", "--reuniao", "reuniao.json", "--root", self.tmp, "--source", "marker", "--once"])
        finally:
            wait_round.wait_brza = original
        self.assertEqual(rc, 0)

    def test_o_script_nao_chama_mais_o_orchestration_check(self):
        with open(wait_round.__file__, encoding="utf-8") as f:
            fonte = f.read()
        for morto in ("check_brza", "extract_messages", "def attribute", "CAIXA_VAZIA_APOS", "caixa vazia"):
            self.assertNotIn(morto, fonte)
        self.assertNotIn('"orchestration"', fonte)       # nenhum argv `brza orchestration …` neste script
        self.assertFalse(hasattr(wait_round, "check_brza") or hasattr(wait_round, "attribute"))


class EventosVistos(Base):
    """O `wait` devolve o Run inteiro; os ids já narrados persistem entre as invocações (item 1 da revisão)."""

    def roda(self, vistos, n):
        self.escreve("a", n)
        reuniao = {"personas": [{"nome": "A", "slug": "a", "sessao": "x-a", "runtime": "claude"}], "worklog": "wl/{slug}.md"}
        entradas = {"x-a": {"sender": "sw_a", "dispatch": "ctx_a", "last_send": {"at": "2026-11-09T18:37:00-03:00"}}}
        pl = {"dispatchId": "ctx_a", "stopReason": "finished"}
        eventos = [{"id": "q1", "type": "question", "from": "sw_a", "subject": "dúvida da R1", "payload": {"dispatchId": "ctx_a"}},
                   {"id": "s1", "type": "escalation", "from": "sw_a", "subject": "Worker stopped without reporting", "payload": pl},
                   {"id": f"s-r{n}", "type": "escalation", "from": "sw_a", "subject": "Worker stopped without reporting", "payload": pl}]
        saidas = []
        rc = wait_round.run(reuniao, n, self.tmp, source="sessions", entradas=entradas, vistos_path=vistos,
                            wait_fn=lambda s, t: (0, {"done": [{"name": "x-a", "outcome": "done", "latency_s": 30}],
                                                       "events": eventos}),
                            clock=lambda: 1794260000.0, sleep=lambda s: None, out=saidas.append)
        return rc, saidas

    def test_segunda_invocacao_so_narra_o_evento_novo(self):
        vistos = os.path.join(self.tmp, "d", "eventos-vistos.json")
        rc, s1 = self.roda(vistos, 3)
        self.assertTrue(any("dúvida da R1" in l for l in s1))
        self.assertTrue(any(l.startswith("ruído previsto: 2 avisos") for l in s1))
        rc, s2 = self.roda(vistos, 4)
        self.assertFalse(any("dúvida" in l for l in s2), s2)
        self.assertEqual([l for l in s2 if l.startswith("ruído")],
                         ['ruído previsto: 1 avisos "Worker stopped without reporting" '
                          '(fim de turno sem worker_done entre rodadas); não responda'])
        self.assertEqual(sorted(json.loads(Path(vistos).read_text(encoding="utf-8"))), ["q1", "s-r3", "s-r4", "s1"])
        self.assertEqual(os.listdir(os.path.dirname(vistos)), ["eventos-vistos.json"])   # escrita atômica: sem .tmp

    def test_sem_arquivo_ou_com_json_ruim_comeca_vazio(self):
        self.assertEqual(wait_round.carrega_vistos(os.path.join(self.tmp, "nao-existe")), set())
        ruim = os.path.join(self.tmp, "ruim.json")
        Path(ruim).write_text("{lixo")
        self.assertEqual(wait_round.carrega_vistos(ruim), set())

    def test_main_grava_na_pasta_da_reuniao(self):
        import contextlib, io
        os.makedirs(os.path.join(self.tmp, "dir"))
        reuniao = {"id": "t", "dir": "dir", "worklog": "wl/{slug}.md",
                   "personas": [{"nome": "A", "slug": "a", "sessao": "x-a", "runtime": "claude"}]}
        Path(self.tmp, "reuniao.json").write_text(json.dumps(reuniao))
        self.escreve("a", 3)
        mapa = os.path.join(self.tmp, "m.jsonl")
        Path(mapa).write_text(json.dumps({"event": "open", "at": "2026-11-09T18:37:00-03:00", "name": "x-a", "chat": "c",
                                          "dispatch": "ctx_a", "sender": "sw_a", "operation": "o"}) + "\n")
        original = wait_round.wait_brza
        wait_round.wait_brza = lambda s, t: (0, {"done": [{"name": "x-a", "outcome": "done", "latency_s": 3}],
                                                  "events": [{"id": "q9", "type": "question", "from": "sw_a",
                                                              "subject": "x", "payload": {}}]})
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                wait_round.main(["3", "--reuniao", "reuniao.json", "--root", self.tmp, "--sessions", mapa])
        finally:
            wait_round.wait_brza = original
        self.assertEqual(json.loads(Path(self.tmp, "dir", "eventos-vistos.json").read_text()), ["q9"])


class EventoDePersonaForaDaRodada(Base):
    def test_o_evento_de_quem_esta_fora_fica_para_a_proxima_invocacao_que_a_inclua(self):
        vistos = os.path.join(self.tmp, "eventos-vistos.json")
        reuniao = {"personas": [{"nome": "A", "slug": "a", "sessao": "x-a", "runtime": "claude"},
                                {"nome": "B", "slug": "b", "sessao": "x-b", "runtime": "grok"}], "worklog": "wl/{slug}.md"}
        entradas = {s: {"sender": "sw_" + s[-1], "dispatch": "ctx_" + s[-1], "last_send": {"at": "2026-11-09T18:37:00-03:00"}}
                    for s in ("x-a", "x-b")}
        ev = [{"id": "qB", "type": "question", "from": "sw_b", "subject": "pergunta de B", "payload": {"dispatchId": "ctx_b"}},
              {"id": "estranho", "type": "question", "from": "sw_z", "subject": "de ninguém", "payload": {}}]

        def roda(n, personas, done):
            saidas = []
            wait_round.run(reuniao, n, self.tmp, source="sessions", entradas=entradas, vistos_path=vistos,
                           personas=personas, clock=lambda: 1794260000.0, sleep=lambda s: None, out=saidas.append,
                           wait_fn=lambda ss, t: (0, {"done": [{"name": x, "outcome": "done", "latency_s": 3}
                                                               for x in done if x in ss], "events": ev}))
            return saidas
        self.escreve("a", 4)
        self.escreve("b", 5)
        s4 = roda(4, {"A"}, ["x-a"])                     # rodada só da A: a pergunta da B NÃO é narrada nem gravada
        self.assertFalse(any("pergunta de B" in l for l in s4))
        self.assertEqual(json.loads(Path(vistos).read_text()), ["estranho"])   # quem não é persona se grava
        self.escreve("a", 5)
        s5 = roda(5, None, ["x-a", "x-b"])               # a sala inteira: agora ela sai, uma vez
        self.assertEqual(sum("pergunta de B" in l for l in s5), 1)
        self.assertEqual(sorted(json.loads(Path(vistos).read_text())), ["estranho", "qB"])


if __name__ == "__main__":
    unittest.main()
