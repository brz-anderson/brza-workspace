"""Testes do wait_round.py, com worklogs temporários e relógio falso."""
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import wait_round  # noqa: E402

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


SLUG = {"x-lenha": "lenha", "x-faisca": "faisca", "x-ticao": "ticao"}


def msg(subject, de="x-lenha", tipo="status", **extra):
    """Mensagem de uma persona: o remetente se reconhece pelo token `persona:<slug>` no corpo."""
    return {"id": f"{subject}-{de}-{tipo}", "type": tipo, "from": de, "subject": subject,
            "body": f"persona:{SLUG[de]}", **extra}


class Mailbox(Base):
    """`check_fn` falso; cada chamada avança o relógio falso em `poll` e entrega a próxima leva de registros."""

    def roda(self, levas, n=2, poll=10.0, timeout=None, dispatches=None, **kw):
        t = {"v": 0.0}
        levas = list(levas)
        saidas = []

        def check_fn(ms):
            t["v"] += ms / 1000
            leva = levas.pop(0) if levas else []
            return leva() if callable(leva) else leva

        def sleep(s):
            t["v"] += s
        rc = wait_round.run(REUNIAO, n, self.tmp, poll=poll, timeout=timeout, clock=lambda: t["v"], sleep=sleep,
                            out=saidas.append, source="mailbox", check_fn=check_fn, dispatches=dispatches, **kw)
        return rc, saidas

    def test_extracao_de_tres_formatos(self):
        a = {"messages": [{"subject": "fim-rodada-2", "from": "x"}]}
        b = [{"id": 1, "subject": "s"}, {"batch": {"items": [{"subject": "t"}]}}]
        c = {"result": {"data": {"unread": [{"subject": "u", "payload": {"subject": "interno"}}]}}}
        self.assertEqual([m["subject"] for m in wait_round.extract_messages(a)], ["fim-rodada-2"])
        self.assertEqual([m["subject"] for m in wait_round.extract_messages(b)], ["s", "t"])
        self.assertEqual([m["subject"] for m in wait_round.extract_messages(c)], ["u"])
        self.assertEqual(wait_round.extract_messages({"ok": True}), [])

    def test_atribuicao_so_por_dispatch_ou_token_exato(self):
        d = {"x-lenha": "disp-77"}
        f = lambda rec, dm=d: (wait_round.attribute(REUNIAO, rec, dm) or {}).get("nome")
        self.assertEqual(f({"subject": "fim-rodada-2", "from": "dispatch:disp-77"}), "Lenha")
        self.assertEqual(f({"subject": "fim-rodada-2", "payload": {"dispatch_id": "disp-77"}}), "Lenha")
        self.assertEqual(f({"subject": "fim-rodada-2", "body": "persona:ticao"}), "Tição")
        self.assertEqual(f({"subject": "persona:faisca fim"}), "Faísca")
        # nome, sessão e slug em texto livre NÃO atribuem (C1: "concordo com a Faísca" não é da Faísca)
        for corpo in ("sou a ticao", "TIÇÃO", "Lenha: fechei; concordo com a Faísca na rede", "x-faisca", "ticao"):
            self.assertIsNone(f({"subject": "fim-rodada-2", "body": corpo}), corpo)
        self.assertIsNone(f({"subject": "fim-rodada-2", "from": "x-faisca"}))   # a sessão não vale
        self.assertIsNone(f({"subject": "fim-rodada-2", "from": "disp-9"}))      # dispatch que não é de ninguém
        # o token é palavra inteira e o slug é case-sensitive
        for corpo in ("persona:Ticao", "persona:ticaox", "xpersona:ticao", "persona:ticao-2"):
            self.assertIsNone(f({"subject": "s", "body": corpo}), corpo)
        # dispatch igual vence o token de outra persona
        self.assertEqual(f({"subject": "s", "from": "dispatch:disp-77", "body": "persona:faisca"}), "Lenha")
        # o `dispatch_id` do manifesto sobrescreve o do mapa
        r2 = {"personas": [dict(REUNIAO["personas"][0], dispatch_id="man-1")] + REUNIAO["personas"][1:]}
        self.assertEqual((wait_round.attribute(r2, {"subject": "s", "from": "dispatch:man-1"}, d) or {}).get("nome"),
                         "Lenha")
        self.assertIsNone(wait_round.attribute(r2, {"subject": "s", "from": "dispatch:disp-77"}, d))

    def test_mensagem_sem_atribuicao_e_listada_e_nao_conta(self):
        rec = {"id": "z", "subject": "fim-rodada-2", "body": "Lenha: fechei, concordo com a Faísca"}
        rc, saidas = self.roda([[rec]], timeout=20)
        self.assertEqual(rc, 2)
        self.assertEqual(saidas[0], "mensagem sem remetente reconhecido: fim-rodada-2")
        self.assertFalse(any("(pela mensagem)" in s for s in saidas))
        self.assertTrue(saidas[-1].startswith("R2 · 0/3"))

    def test_delivery_id_do_lote_nao_e_id_de_mensagem(self):
        a = {"delivery_id": "d1", "subject": "fim-rodada-2", "body": "persona:lenha"}
        b = {"delivery_id": "d1", "subject": "fim-rodada-2", "body": "persona:faisca"}
        rc, saidas = self.roda([[a, b]], timeout=20)
        self.assertEqual(sum("(pela mensagem)" in s for s in saidas), 2)

    def test_caixa_vazia_avisa_uma_vez(self):
        rc, saidas = self.roda([], timeout=100, poll=10.0)
        avisos = [s for s in saidas if "caixa vazia: confira se a coordenação tem um Run ligado" in s]
        self.assertEqual(len(avisos), 1)

    def test_caixa_vazia_nao_avisa_se_chegou_mensagem(self):
        rc, saidas = self.roda([[msg("fim-rodada-1", tipo="question")]], timeout=100, poll=10.0)
        self.assertFalse(any("caixa vazia" in s for s in saidas))

    def test_marcador_recuado_nao_vale(self):
        with open(os.path.join(self.tmp, "wl/lenha.md"), "w", encoding="utf-8") as f:
            f.write("### Rodada 2: x\n\n  <!-- fim-rodada-2 -->\n")
        self.assertIsNone(wait_round.last_marker(os.path.join(self.tmp, "wl/lenha.md")))
        self.assertFalse(wait_round.scan(REUNIAO, 2, self.tmp)["Lenha"])

    def test_mensagem_com_marcador_chega_pela_mensagem(self):
        self.escreve("lenha", 2)
        rc, saidas = self.roda([[msg("fim-rodada-2")]] + [[msg("fim-rodada-3", "x-faisca"), msg("fim-rodada-2", "x-ticao")]])
        self.assertEqual(rc, 0)
        self.assertTrue(saidas[0].startswith("R2 · 1/3 — entregaram Lenha"))
        self.assertTrue(saidas[0].endswith("(pela mensagem)"))
        self.assertFalse(any("⚠" in s for s in saidas[:1]))

    def test_mensagem_sem_marcador_gera_aviso(self):
        rc, saidas = self.roda([[msg("fim-rodada-2")]] + [[]] * 40, timeout=60)
        self.assertEqual(rc, 2)
        self.assertEqual(saidas[1], "⚠ Lenha avisou fim-rodada-2 mas o worklog não termina no marcador")

    def test_marcador_sem_mensagem_diz_pelo_marcador(self):
        self.escreve("ticao", 2)
        rc, saidas = self.roda([[]], timeout=20)
        self.assertEqual(rc, 2)
        self.assertTrue(saidas[0].endswith("(pelo marcador)"))
        self.assertIn("entregaram Tição", saidas[0])

    def test_rodada_menor_nao_vale_e_maior_vale(self):
        rc, saidas = self.roda([[msg("fim-rodada-1")], [msg("fim-rodada-3", "x-faisca")]], timeout=30)
        self.assertEqual(rc, 2)
        self.assertEqual([s for s in saidas if "entregaram" in s and "pela mensagem" in s].__len__(), 1)
        self.assertIn("entregaram Faísca", saidas[0])

    def test_worker_done_e_bloqueio_nao_contam(self):
        rc, saidas = self.roda([[msg("fim-rodada-2", tipo="worker_done"), msg("dúvida", tipo="question"),
                                 msg("travei", tipo="blocked")]], timeout=20)
        self.assertEqual(rc, 2)
        self.assertEqual(saidas[0], "Lenha enviou worker_done: fim-rodada-2")
        self.assertEqual(saidas[1], "Lenha enviou question: dúvida")
        self.assertEqual(saidas[2], "Lenha enviou blocked: travei")
        self.assertFalse(any("(pela mensagem)" in s for s in saidas))

    def test_peek_repetido_nao_duplica(self):
        # `question` não passa pelo "já chegou": sem o `vistos` a linha sairia três vezes
        m = msg("dúvida", tipo="question")
        rc, saidas = self.roda([[m], [m], [m]], timeout=30)
        self.assertEqual(sum(s == "Lenha enviou question: dúvida" for s in saidas), 1)
        sem_id = {"subject": "dúvida 2", "type": "question", "body": "persona:lenha"}  # sem id: o hash da mensagem
        rc, saidas = self.roda([[sem_id], [dict(sem_id)], [dict(sem_id)]], timeout=30)
        self.assertEqual(sum(s == "Lenha enviou question: dúvida 2" for s in saidas), 1)

    def test_brza_ausente_cai_para_marker(self):
        def falha(ms):
            raise wait_round.CheckIndisponivel("brza não achado")
        self.escreve("lenha", 2)
        saidas, t = [], {"v": 0.0}

        def sleep(s):
            t["v"] += s
            if t["v"] >= 20:
                self.escreve("faisca", 2)
                self.escreve("ticao", 2)
        rc = wait_round.run(REUNIAO, 2, self.tmp, poll=10, clock=lambda: t["v"], sleep=sleep, out=saidas.append,
                            source="mailbox", check_fn=falha)
        self.assertEqual(rc, 0)
        self.assertTrue(saidas[0].startswith("aviso: brza orchestration check indisponível"))
        self.assertEqual(sum(s.startswith("aviso:") for s in saidas), 1)
        self.assertIn("todos entregaram", saidas[-1])

    def test_check_brza_real_sem_binario(self):
        with self.assertRaises(wait_round.CheckIndisponivel):
            wait_round.check_brza(1000, brza="comando-que-nao-existe-xyz")

    def test_timeout_mostra_quem_falta(self):
        rc, saidas = self.roda([], timeout=40)
        self.assertEqual(rc, 2)
        self.assertEqual(len(saidas), 1)
        self.assertTrue(saidas[0].startswith("R2 · 0/3 — faltam Lenha (Codex"))

    def test_mapa_de_dispatch_pega_a_ultima_linha_open(self):
        mapa = os.path.join(self.tmp, "m.jsonl")
        with open(mapa, "w") as f:
            for r in ({"event": "open", "name": "x-lenha", "dispatch_id": "a"},
                      {"event": "close", "name": "x-lenha"},
                      {"event": "open", "name": "x-lenha", "dispatch_id": "b"},
                      {"event": "open", "name": "x-faisca", "dispatch_id": None}):
                f.write(json.dumps(r) + "\n")
            f.write("lixo\n")
        self.assertEqual(wait_round.dispatch_map(mapa), {"x-lenha": "b"})
        self.assertEqual(wait_round.dispatch_map(os.path.join(self.tmp, "nao-existe")), {})


if __name__ == "__main__":
    unittest.main()
