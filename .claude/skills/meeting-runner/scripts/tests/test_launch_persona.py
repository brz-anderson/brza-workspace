"""Testes do launch_persona.py sobre o `brza sessions` v2: o manifesto vira argv, e a saída REAL do v2 (fixtures da sonda)
se lê sem relançar nada. Nenhum comando do brza roda: o corredor `sessions_fn`/`brza_fn` é falso."""
import contextlib
import io
import json
import os
import shlex
import shutil
import tempfile
import unittest

import _paths  # noqa: F401
from _paths import HERE, fixture, le

import launch_persona

with open(fixture("reuniao-mcp-remoto.json"), encoding="utf-8") as _f:
    REUNIAO = json.load(_f)

SEND_REAL = json.loads(le("v2", "logs", "pln017-smoke-send.log"))        # recibo pending real (um objeto)
CLOSE_REAL = json.loads(le("v2", "logs", "pln017-smoke-close.log"))      # closing real
SHOW_OK = json.loads(le("v2", "pure-claude-show.json"))                  # succeeded/settled, com {"ok","result"}
SHOW_LIBERADA = json.loads(le("v2", "pure-claude-after-deadline.json"))  # sem o envelope, released
SHOW_ATIVA = json.loads(le("v2", "pure-grok-show.json"))                 # ready/input_accepted


class Fake:
    """Corredor falso: devolve a próxima resposta da fila (ou a função) e guarda os argv recebidos."""

    def __init__(self, *respostas, padrao=(0, "", "")):
        self.respostas, self.padrao, self.chamadas = list(respostas), padrao, []

    def __call__(self, argv):
        self.chamadas.append(list(argv))
        r = self.respostas.pop(0) if self.respostas else self.padrao
        return r(argv) if callable(r) else r


def js(obj, rc=0):
    return (rc, json.dumps(obj), "")


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.manifesto = os.path.join(self.tmp, "reuniao.json")
        with open(self.manifesto, "w", encoding="utf-8") as f:
            json.dump(REUNIAO, f, ensure_ascii=False)
        os.makedirs(os.path.join(self.tmp, REUNIAO["dir"]))
        self.mapa = os.path.join(self.tmp, "sessions.jsonl")
        self.saida = []

    def roda(self, *args, sessions_fn=None, brza_fn=None, **kw):
        with contextlib.redirect_stderr(io.StringIO()) as err:
            rc = launch_persona.main([self.manifesto, *args, "--root", self.tmp, "--sessions", self.mapa],
                                     sessions_fn=sessions_fn, brza_fn=brza_fn, out=self.saida.append, **kw)
        self.stderr = err.getvalue()
        return rc, "\n".join(self.saida)

    def grava_mapa(self, *rows):
        with open(self.mapa, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")


class Molde(unittest.TestCase):
    def texto(self):
        return launch_persona.prompt_text(REUNIAO, REUNIAO["personas"][0])

    def test_sem_comando_de_orchestration_proprio_e_com_o_preambulo(self):
        t = self.texto()
        self.assertNotIn("brza orchestration", t)         # X19: o envio é do `brza sessions`
        for trecho in ("--task-id", "--dispatch-id", "preâmbulo", "worker_done", "date '+%H:%M'"):  # X9, X11
            self.assertIn(trecho, t)
        self.assertEqual(t.count("\n"), 0)                 # uma linha

    def test_slots_do_manifesto(self):
        t = self.texto()
        self.assertIn("Muralha, Arquiteta de Rede e Segurança", t)
        self.assertIn(".sessions/reuniao-mcp-remoto/rodada-1.md", t)
        self.assertIn("work/worklogs/2026-11-07-reuniao-mcp-remoto-muralha.md", t)
        self.assertIn(".sessions/reuniao-mcp-remoto/personas/muralha.md", t)
        self.assertIn("prazo até 22h15", t)

    def test_prompt_existente_nunca_e_sobrescrito(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        p = REUNIAO["personas"][0]
        caminho = launch_persona.prompt_path(REUNIAO, p, tmp)
        os.makedirs(os.path.dirname(caminho))
        with open(caminho, "w", encoding="utf-8") as f:
            f.write("meu prompt\n")
        launch_persona.ensure_prompt(REUNIAO, p, tmp)
        self.assertEqual(le_arquivo(caminho), "meu prompt\n")
        os.remove(caminho)
        launch_persona.ensure_prompt(REUNIAO, p, tmp)
        self.assertIn("Você é uma persona numa reunião multiagente", le_arquivo(caminho))


def le_arquivo(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


class Argv(Base):
    def argv_de(self, nome):
        p = launch_persona.pick(REUNIAO, [nome])[0]
        return launch_persona.open_argv(REUNIAO, p, self.tmp)

    def test_claude_com_modelo_e_esforco(self):
        a = self.argv_de("Muralha")
        co = a[a.index("--checkout") + 1]
        self.assertTrue(os.path.isabs(co) and co.endswith("/.worktrees/playground"), co)
        self.assertEqual(a, ["mcp-muralha", "--agent", "claude", "--checkout", co, "--prompt-file",
                             os.path.join(self.tmp, REUNIAO["dir"], "prompt-muralha.txt"), "--title",
                             "Reunião mcp-remoto: Muralha (opus-5.5 high)", "--wait", "--model", "opus-5.5",
                             "--effort", "high"])

    def test_codex_e_grok_repassam(self):
        self.assertEqual(self.argv_de("Régua")[-4:], ["--model", "gpt-6-astra", "--effort", "xhigh"])
        self.assertEqual(self.argv_de("Régua")[2], "codex")
        a = self.argv_de("Salto")
        self.assertIn("--model", a)
        self.assertEqual(a[a.index("--model") + 1], "grok-4.7-build-fast")
        self.assertEqual(a[a.index("--effort") + 1], "low")

    def test_antigravity_nunca_leva_modelo_nem_esforco(self):
        a = self.argv_de("Cartógrafo")
        self.assertNotIn("--model", a)
        self.assertNotIn("--effort", a)

    def test_modelo_nulo_ou_traco_nao_vira_flag_e_esforco_sem_modelo_nao_vai(self):
        p = dict(REUNIAO["personas"][0], modelo="-", esforco="high")
        a = launch_persona.open_argv(REUNIAO, p, self.tmp)
        self.assertNotIn("--model", a)
        self.assertNotIn("--effort", a)   # o v2 recusa --effort sem --model
        self.assertNotIn("--model", launch_persona.open_argv(REUNIAO, dict(p, modelo=None), self.tmp))

    def test_escolha_por_nome_slug_ou_sessao(self):
        for q in ("Muralha", "muralha", "mcp-muralha", "MURALHA"):
            self.assertEqual([p["nome"] for p in launch_persona.pick(REUNIAO, [q])], ["Muralha"])
        self.assertEqual(len(launch_persona.pick(REUNIAO, ["todas"])), 6)
        with self.assertRaises(SystemExit):
            launch_persona.pick(REUNIAO, ["ninguem"])

    def test_checkout_nao_dobra_o_caminho_dentro_de_um_worktree(self):
        raiz = os.path.abspath(os.path.join(HERE, *([".."] * 5)))
        r = launch_persona.checkout_abs({"checkout": ".worktrees/playground"}, raiz)
        self.assertTrue(r.endswith("/.worktrees/playground"), r)
        self.assertFalse(r.endswith(".worktrees/playground/.worktrees/playground"), r)
        self.assertEqual(launch_persona.checkout_abs({"checkout": "/x/y"}, "/tmp"), "/x/y")

    def test_raiz_padrao_e_o_mesmo_de_qualquer_diretorio(self):
        aqui = os.path.dirname(os.path.dirname(HERE))
        raiz = launch_persona.raiz_padrao()
        antes = os.getcwd()
        try:
            for d in (raiz, aqui, HERE):
                os.chdir(d)
                self.assertEqual(os.path.realpath(launch_persona.raiz_padrao()), os.path.realpath(raiz))
        finally:
            os.chdir(antes)


class DryRun(Base):
    def test_imprime_o_comando_do_sessions_sem_executar_nem_gravar_prompt(self):
        fake = Fake()
        rc, s = self.roda("Muralha", "--dry-run", sessions_fn=fake)
        self.assertEqual(rc, 0)
        self.assertEqual(fake.chamadas, [])
        self.assertIn("[dry-run] Muralha (claude, modelo opus-5.5, esforço high)", s)
        self.assertIn("brza sessions mcp-muralha --agent claude --checkout", s)
        self.assertIn("geraria", s)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, REUNIAO["dir"], "prompt-muralha.txt")))

    def test_todas_as_personas(self):
        rc, s = self.roda("--dry-run")
        self.assertEqual(s.count("[dry-run] "), 6)

    def test_via_antiga_sai_2_com_a_mensagem(self):
        for via in ("worker-start", "hybrid", "agent-launch"):
            fake = Fake()
            self.saida.clear()
            rc, _ = self.roda("--via", via, "--dry-run", sessions_fn=fake)
            self.assertEqual(rc, 2)
            self.assertIn("via removida: a abertura é a do brza sessions v2 (PLN-017 R6/P4a)", self.stderr)
            self.assertEqual(fake.chamadas, [])
        rc, _ = self.roda("--via", "sessions", "--dry-run")
        self.assertEqual(rc, 0)


OPEN_OK = (0, "open:     x  (chat, /w, c1)\n", "")


class Abrir(Base):
    def test_uma_de_cada_vez_na_ordem_do_manifesto_e_sem_orchestration(self):
        fake = Fake(padrao=OPEN_OK)
        self.roda(sessions_fn=fake)
        self.assertEqual([c[0] for c in fake.chamadas],
                         ["mcp-muralha", "mcp-regua", "mcp-atalho", "mcp-salto", "mcp-plantao", "mcp-cartografo"])
        for c in fake.chamadas:
            self.assertNotIn("orchestration", c)
            self.assertNotIn("worker-start", c)
        fonte = le_arquivo(launch_persona.__file__)
        for proibido in ("Popen", "threading", "multiprocessing", "worker_start_argv", "extract_receipt", "record_open",
                         "load_sessions_module"):
            self.assertNotIn(proibido, fonte, proibido)

    def test_prompt_gerado_antes_de_cada_abertura(self):
        fake = Fake(padrao=OPEN_OK)
        self.roda("Muralha", sessions_fn=fake)
        self.assertIn("Você é uma persona numa reunião multiagente", le_arquivo(
            os.path.join(self.tmp, REUNIAO["dir"], "prompt-muralha.txt")))

    def test_saida_real_do_v2_open_e_running(self):
        real_open = le("v2", "logs", "pln017-smoke-open.log")
        fake = Fake((0, real_open, ""), (0, "running:  mcp-regua\n", ""), padrao=OPEN_OK)
        rc, s = self.roda("Muralha", "Régua", sessions_fn=fake)
        self.assertEqual(rc, 0)
        self.assertIn("Muralha: aberta", s)
        self.assertIn("Régua: já aberta; não reabre", s)

    def test_nao_abriu_manda_conferir_o_pending_e_nao_relanca(self):
        msg = "CHECK:    mcp-muralha não abriu: boom; não relance: confira /x/.sessions/pending-abc.json\n"
        fake = Fake((1, msg, ""), padrao=OPEN_OK)
        rc, s = self.roda("Muralha", "Régua", sessions_fn=fake)
        self.assertEqual(rc, 1)
        self.assertIn("não relance antes de conferir o pending-*.json citado", s)
        self.assertEqual(len(fake.chamadas), 2)          # a outra persona segue; a Muralha NÃO é repetida
        self.assertEqual(sum(c[0] == "mcp-muralha" for c in fake.chamadas), 1)

    def test_sem_sessao_em_60_s_abriu_sem_id_e_o_lote_segue(self):
        msg = "CHECK:    mcp-muralha não deu a sessão em 60 s; confira a aba\n"
        fake = Fake((1, msg, ""), padrao=OPEN_OK)
        rc, s = self.roda("Muralha", "Régua", sessions_fn=fake)
        self.assertEqual(rc, 0)
        self.assertIn("abriu; não relance; o `wait` grava o id depois", s)
        self.assertEqual([c[0] for c in fake.chamadas], ["mcp-muralha", "mcp-regua"])

    def test_outro_rc_e_falha_sem_relancar(self):
        fake = Fake((127, "", "brza: não achado"), padrao=OPEN_OK)
        rc, s = self.roda("Muralha", sessions_fn=fake)
        self.assertEqual(rc, 1)
        self.assertIn("falha na abertura (rc 127); sem relançar", s)
        self.assertIn("brza: não achado", self.stderr)
        self.assertEqual(len(fake.chamadas), 1)

    def test_tabela_da_narracao_e_run_unico(self):
        self.grava_mapa(
            {"event": "open", "name": "mcp-muralha", "chat": "c1", "dispatch": "ctx_1", "run": "run_A",
             "agent": "claude", "model": "opus-5.5", "effort": "high"},
            {"event": "session", "name": "mcp-muralha", "chat": "c1", "provider_session": "uuid-m", "claude_session": "uuid-m"},
            {"event": "open", "name": "mcp-regua", "chat": "c2", "dispatch": "ctx_2", "run": "run_A", "agent": "codex",
             "model": "gpt-6-astra", "effort": "xhigh"})
        rc, s = self.roda("Muralha", "Régua", sessions_fn=Fake(padrao=OPEN_OK))
        self.assertEqual(rc, 0)
        self.assertIn("Persona · papel · runtime · modelo · esforço · Dispatch · Run · sessão do provedor", s)
        self.assertIn("Muralha · Arquiteta de Rede e Segurança · claude · opus-5.5 · high · ctx_1 · run_A · uuid-m", s)
        self.assertIn("Régua · Cético que mede · codex · gpt-6-astra · xhigh · ctx_2 · run_A · —", s)
        self.assertNotIn("Run múltiplo", s)

    def test_run_multiplo_avisa_e_sai_1_sem_relancar(self):
        self.grava_mapa({"event": "open", "name": "mcp-muralha", "chat": "c1", "dispatch": "ctx_1", "run": "run_A"},
                        {"event": "open", "name": "mcp-regua", "chat": "c2", "dispatch": "ctx_2", "run": "run_B"})
        fake = Fake(padrao=OPEN_OK)
        rc, s = self.roda("Muralha", "Régua", sessions_fn=fake)
        self.assertEqual(rc, 1)
        self.assertIn("⚠ Run múltiplo: Muralha=run_A, Régua=run_B", s)
        self.assertEqual(len(fake.chamadas), 2)


class Enviar(Base):
    def test_uma_chamada_para_todas_com_o_texto_e_json(self):
        fake = Fake(js({"results": [dict(SEND_REAL, name="mcp-muralha", status="accepted", operation="op1"),
                                    dict(SEND_REAL, name="mcp-regua", status="queued", operation="op2")]}))
        rc, s = self.roda("Muralha", "Régua", "--send", "--round", "2", sessions_fn=fake)
        self.assertEqual(rc, 0)
        self.assertEqual(fake.chamadas, [["send", "mcp-muralha", "mcp-regua", "--text",
                                          f"Faça a rodada 2: {REUNIAO['dir']}/rodada-2.md", "--json"]])
        self.assertIn("Muralha: accepted · op1", s)
        self.assertIn("Régua: queued · op2", s)

    def test_pending_real_do_v2_nunca_reenvia_e_diz_o_que_fazer(self):
        fake = Fake((75, json.dumps(dict(SEND_REAL, name="mcp-muralha")), ""))  # o recibo real, com o nome da persona
        rc, s = self.roda("mcp-muralha", "--send", "--message", "oi", sessions_fn=fake)
        op = SEND_REAL["operation"]
        self.assertEqual(fake.chamadas, [["send", "mcp-muralha", "--text", "oi", "--json"]])
        self.assertEqual(rc, 75)
        self.assertIn(f"Muralha: pending — não reenvie às cegas; espere com wait_round.py N, ou repita só esta persona "
                      f"com --operation {op} e o mesmo texto", s)

    def test_unknown_com_numero_da_rodada(self):
        fake = Fake((75, json.dumps({"results": [{"name": "mcp-regua", "status": "unknown", "operation": "opX"}]}), ""))
        rc, s = self.roda("Régua", "--send", "--round", "3", sessions_fn=fake)
        self.assertEqual(rc, 75)
        self.assertIn("Régua: unknown — não reenvie às cegas; espere com wait_round.py 3, ou repita só esta persona com "
                      "--operation opX e o mesmo texto", s)
        self.assertEqual(len(fake.chamadas), 1)   # o wrapper nunca reenvia sozinho

    def test_repetir_com_a_mesma_operation_passa_o_flag(self):
        fake = Fake(js({"name": "mcp-regua", "status": "accepted", "operation": "opX", "replayed": True}))
        rc, _ = self.roda("Régua", "--send", "--message", "mesmo texto", "--operation", "opX", sessions_fn=fake)
        self.assertEqual(rc, 0)
        self.assertEqual(fake.chamadas, [["send", "mcp-regua", "--text", "mesmo texto", "--json", "--operation", "opX"]])

    def test_operation_com_mais_de_uma_persona_e_erro_2_antes_de_chamar(self):
        fake = Fake()
        rc, s = self.roda("Muralha", "Régua", "--send", "--message", "x", "--operation", "o", sessions_fn=fake)
        self.assertEqual(rc, 2)
        self.assertEqual(fake.chamadas, [])

    def test_rejected_sai_1_com_o_motivo(self):
        fake = Fake(js({"name": "mcp-regua", "status": "rejected", "operation": "o", "refusal": "fence antigo"}, rc=0))
        rc, s = self.roda("Régua", "--send", "--message", "x", sessions_fn=fake)
        self.assertEqual(rc, 1)
        self.assertIn("fence antigo", s)

    def test_erro_do_v2_sai_1(self):
        fake = Fake(js({"error": "nenhum chat aberto se chama x"}, rc=1))
        rc, s = self.roda("Régua", "--send", "--message", "x", sessions_fn=fake)
        self.assertEqual(rc, 1)
        self.assertIn("erro do brza sessions send", s)

    def test_message_e_round_juntos_ou_nenhum_e_erro_de_uso(self):
        with self.assertRaises(SystemExit):
            self.roda("--send")
        with self.assertRaises(SystemExit):
            self.roda("--send", "--message", "x", "--round", "2")


class Fechar(Base):
    def test_cada_nome_vira_o_close_do_v2_um_por_chamada(self):
        casos = {"--close": [], "--release": [], "--stop": ["--force"], "--keep-open": ["--keep-open"]}
        for flag, extra in casos.items():
            fake = Fake(padrao=js({"name": "x", "status": "released", "closed": True}))
            self.roda("Muralha", "Régua", flag, sessions_fn=fake)
            self.assertEqual(fake.chamadas, [["close", "mcp-muralha", *extra, "--json"],
                                             ["close", "mcp-regua", *extra, "--json"]], flag)

    def test_closing_real_nao_e_fechada(self):
        fake = Fake(js(CLOSE_REAL))
        rc, s = self.roda("mcp-muralha", "--close", sessions_fn=fake)
        self.assertEqual(rc, 0)
        self.assertIn("pedido de encerramento enviado; NÃO está fechada; confira com --status", s)
        self.assertNotIn("fechada (", s)

    def test_released_e_already_released_fecham(self):
        for st in ("released", "already_released"):
            self.saida.clear()
            rc, s = self.roda("Muralha", "--close", sessions_fn=Fake(js({"name": "x", "status": st, "closed": True})))
            self.assertEqual(rc, 0)
            self.assertIn(f"fechada ({st})", s)

    def test_incerto_sai_75_e_nao_repete(self):
        for st in ("stop_unknown", "release_unknown", "release_pending"):
            self.saida.clear()
            fake = Fake(js({"name": "x", "status": st, "closed": False}, rc=75))
            rc, s = self.roda("Muralha", "--stop", sessions_fn=fake)
            self.assertEqual(rc, 75, st)
            self.assertIn(f"incerto ({st}): não está fechada; não repita; confira com --status", s)
            self.assertEqual(len(fake.chamadas), 1, st)

    def test_retained_e_outro_status_nao_fecham(self):
        rc, s = self.roda("Muralha", "--close", sessions_fn=Fake(js({"name": "x", "status": "retained", "closed": False}, rc=1)))
        self.assertEqual(rc, 1)
        self.assertIn("não fechada (retained)", s)

    def test_refused_sai_1_com_o_erro(self):
        fake = Fake(js({"name": "x", "status": "refused", "error": "identidade diferente da coordenação"}, rc=1))
        rc, s = self.roda("Muralha", "--close", sessions_fn=fake)
        self.assertEqual(rc, 1)
        self.assertIn("identidade diferente da coordenação", s)

    def test_keep_open_kept_open_e_sucesso_sem_dizer_fechada(self):
        rc, s = self.roda("Muralha", "--keep-open", sessions_fn=Fake(js({"name": "x", "status": "kept_open"})))
        self.assertEqual(rc, 0)
        self.assertIn("mantida aberta", s)

    def test_pior_vence_1_sobre_75(self):
        fake = Fake(js({"status": "stop_unknown"}, rc=75), js({"status": "retained"}, rc=1))
        rc, _ = self.roda("Muralha", "Régua", "--stop", sessions_fn=fake)
        self.assertEqual(rc, 1)


class Status(Base):
    def test_mostra_task_completed_auto_release_e_o_veredito(self):
        self.grava_mapa({"event": "open", "name": "mcp-muralha", "chat": "c1", "dispatch": "ctx_ab0fa42d1e9a", "run": "r"})
        fake = Fake(js(SHOW_OK))
        rc, s = self.roda("Muralha", "--status", brza_fn=fake)
        self.assertEqual(rc, 0)
        self.assertEqual(fake.chamadas, [["orchestration", "worker-show", "--dispatch", "ctx_ab0fa42d1e9a", "--full", "--json"]])
        self.assertIn("Muralha · succeeded/settled · completed · task_f82ca8f37528 · 2026-11-09T15:53:56.116Z · "
                      "2026-11-09T15:55:56Z · not_requested → encerrada e aceita", s)

    def test_sem_o_envelope_e_liberada(self):
        self.grava_mapa({"event": "open", "name": "mcp-muralha", "chat": "c1", "dispatch": "ctx_ab0fa42d1e9a", "run": "r"})
        rc, s = self.roda("Muralha", "--status", brza_fn=Fake(js(SHOW_LIBERADA)))
        self.assertIn("released → liberada", s)

    def test_ativa_e_falhou(self):
        self.grava_mapa({"event": "open", "name": "mcp-salto", "chat": "c1", "dispatch": "ctx_6bb3a52e3ab6", "run": "r"})
        rc, s = self.roda("Salto", "--status", brza_fn=Fake(js(SHOW_ATIVA)))
        self.assertIn("ready/input_accepted · dispatched · task_a398f6b57a89 · — · — · not_requested → ativa", s)
        falhou = json.loads(json.dumps(SHOW_ATIVA))
        falhou["result"]["worker"]["state"] = "abandoned"
        self.saida.clear()
        rc, s = self.roda("Salto", "--status", brza_fn=Fake(js(falhou)))
        self.assertIn("→ falhou", s)

    def test_retained_reason_aparece(self):
        show = json.loads(json.dumps(SHOW_ATIVA))
        show["result"]["terminalResource"].update(releaseState="retained", retainedReason="keep_open")
        v, c = launch_persona.veredito(show)
        self.assertEqual(v, "ativa")
        self.assertIn("retained (keep_open)", launch_persona.linha_status("X", c, v))

    def test_dispatch_do_manifesto_quando_o_mapa_nao_tem(self):
        p = dict(REUNIAO["personas"][0], dispatch_id="ctx_man")
        fake = Fake(js(SHOW_OK))
        launch_persona.consulta([p], {}, fake)
        self.assertEqual(fake.chamadas[0][3], "ctx_man")

    def test_wait_settled_ate_encerrar(self):
        self.grava_mapa({"event": "open", "name": "mcp-muralha", "chat": "c1", "dispatch": "ctx_1", "run": "r"})
        t = {"v": 0.0}

        def sleep(s):
            t["v"] += s
        fake = Fake(js(SHOW_ATIVA), js(SHOW_ATIVA), js(SHOW_OK))
        rc, s = self.roda("Muralha", "--status", "--wait-settled", "60", brza_fn=fake, clock=lambda: t["v"], sleep=sleep)
        self.assertEqual(rc, 0)
        self.assertEqual(len(fake.chamadas), 3)
        self.assertEqual(t["v"], 10.0)

    def test_wait_settled_vencido_75_com_o_diagnostico_do_worker_done(self):
        self.grava_mapa({"event": "open", "name": "mcp-salto", "chat": "c1", "dispatch": "ctx_6bb3a52e3ab6", "run": "r"})
        t = {"v": 0.0}

        def sleep(s):
            t["v"] += s
        rc, s = self.roda("Salto", "--status", "--wait-settled", "12", brza_fn=Fake(padrao=js(SHOW_ATIVA)),
                          clock=lambda: t["v"], sleep=sleep)
        self.assertEqual(rc, 75)
        self.assertIn("faltam Salto (ativa)", s)
        self.assertIn("--type worker_done --task-id task_a398f6b57a89 --dispatch-id ctx_6bb3a52e3ab6 --outcome succeeded", s)

    def test_wait_settled_para_cedo_com_rc_1_quando_alguma_falhou(self):
        self.grava_mapa({"event": "open", "name": "mcp-muralha", "chat": "c1", "dispatch": "ctx_1", "run": "r"},
                        {"event": "open", "name": "mcp-regua", "chat": "c2", "dispatch": "ctx_2", "run": "r"})
        falhou = json.loads(json.dumps(SHOW_ATIVA))
        falhou["result"]["worker"]["state"] = "failed"
        t = {"v": 0.0}

        def sleep(s):
            t["v"] += s
        rc, s = self.roda("Muralha", "Régua", "--status", "--wait-settled", "600", clock=lambda: t["v"], sleep=sleep,
                          brza_fn=Fake(js(SHOW_ATIVA), js(falhou)))
        self.assertEqual(rc, 1)
        self.assertIn("falhou: Régua; parei de esperar", s)
        self.assertEqual(t["v"], 0.0)

    def test_nao_chama_nada_alem_do_worker_show(self):
        self.grava_mapa({"event": "open", "name": "mcp-muralha", "chat": "c1", "dispatch": "ctx_1", "run": "r"})
        fake = Fake(js(SHOW_OK))
        self.roda("Muralha", "--status", brza_fn=fake, sessions_fn=Fake())
        for c in fake.chamadas:
            self.assertEqual(c[:2], ["orchestration", "worker-show"])


class SemTransporteDuplicado(unittest.TestCase):
    def test_o_script_nao_monta_nenhum_verbo_de_orchestration_que_age(self):
        fonte = le_arquivo(launch_persona.__file__)
        codigo = "\n".join(l for l in fonte.split("\n") if not l.lstrip().startswith(("#", '"""')))
        for verbo in ('"worker-start"', '"worker-release"', '"worker-stop"', '"worker-keep-open"', '"check"'):
            self.assertNotIn(f'"orchestration", {verbo}', codigo)
            self.assertNotIn(f"'orchestration', {verbo}", codigo)
        self.assertIn('"orchestration", "worker-show"', codigo)


class RevisaoStatus(Base):
    def show(self, **kw):
        s = json.loads(json.dumps(SHOW_OK))
        r = s["result"]
        r["worker"].update({k: v for k, v in kw.items() if k in ("state", "stage")})
        r["terminalResource"].update({k: v for k, v in kw.items() if k in ("releaseState", "retainedReason")})
        return s

    def test_encerrada_retida_nao_e_aceita_nem_ok_final(self):
        v, c = launch_persona.veredito(self.show(releaseState="retained", retainedReason="keep_open"))
        self.assertEqual(v, "encerrada, retida (keep_open): não fecha sozinha")
        self.assertNotIn(v, launch_persona.OK_FINAL)

    def test_wait_settled_nao_sai_0_por_retida_e_lista_no_fim(self):
        self.grava_mapa({"event": "open", "name": "mcp-muralha", "chat": "c1", "dispatch": "ctx_1", "run": "r"})
        t = {"v": 0.0}

        def sleep(s):
            t["v"] += s
        rc, s = self.roda("Muralha", "--status", "--wait-settled", "12", clock=lambda: t["v"], sleep=sleep,
                          brza_fn=Fake(padrao=js(self.show(releaseState="retained", retainedReason="keep_open"))))
        self.assertEqual(rc, 75)
        self.assertIn("prazo: faltam Muralha (encerrada, retida (keep_open): não fecha sozinha)", s)

    def test_liberada_vence_falhou(self):
        v, _ = launch_persona.veredito(self.show(state="stopped", releaseState="released"))
        self.assertEqual(v, "liberada")
        v, _ = launch_persona.veredito(self.show(state="stopped", releaseState="not_requested"))
        self.assertEqual(v, "falhou")

    def test_tabela_so_quando_o_veredito_muda_e_sem_dispatch_entra_no_fim(self):
        self.grava_mapa({"event": "open", "name": "mcp-muralha", "chat": "c1", "dispatch": "ctx_1", "run": "r"})
        t = {"v": 0.0}

        def sleep(s):
            t["v"] += s
        fake = Fake(js(SHOW_ATIVA), js(SHOW_ATIVA), js(SHOW_ATIVA), js(SHOW_OK))
        rc, s = self.roda("Muralha", "--status", "--wait-settled", "600", brza_fn=fake, clock=lambda: t["v"], sleep=sleep)
        self.assertEqual(rc, 0)
        self.assertEqual(len(fake.chamadas), 4)
        self.assertEqual(s.count("Muralha ·"), 2)          # a primeira volta e a da mudança; as repetidas não imprimem
        self.saida.clear()
        rc, s = self.roda("Muralha", "Régua", "--status", "--wait-settled", "6", brza_fn=Fake(padrao=js(SHOW_OK)),
                          clock=lambda: t["v"], sleep=sleep)
        self.assertEqual(rc, 75)
        self.assertIn("Régua (sem veredito: sem Dispatch no mapa nem no manifesto)", s)


class MoldePrazo(unittest.TestCase):
    def test_duracao_do_cabecalho_de_rodada_1_ou_ate_a_hora(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        p = REUNIAO["personas"][0]
        self.assertIn("prazo até 22h15;", launch_persona.prompt_text(REUNIAO, p, tmp))
        os.makedirs(os.path.join(tmp, REUNIAO["dir"]))
        with open(os.path.join(tmp, REUNIAO["dir"], "rodada-1.md"), "w", encoding="utf-8") as f:
            f.write("# Rodada 1 — opinião (duração: ~10 min)\n")
        t = launch_persona.prompt_text(REUNIAO, p, tmp)
        self.assertIn("prazo ~10 min;", t)
        self.assertNotIn("22h15", t)

    def test_pick_sem_caixa_usa_a_funcao_comum(self):
        self.assertEqual(launch_persona.pick(REUNIAO, ["MCP-REGUA"])[0]["nome"], "Régua")


class LiberadaFalhou(RevisaoStatus):
    def test_failed_liberado_continua_falha_e_stopped_liberado_e_liberada(self):
        v, _ = launch_persona.veredito(self.show(state="failed", releaseState="released"))
        self.assertEqual(v, "liberada (falhou)")
        self.assertNotIn(v, launch_persona.OK_FINAL)
        v, _ = launch_persona.veredito(self.show(state="stopped", releaseState="released"))
        self.assertEqual(v, "liberada")

    def test_wait_settled_sai_1_com_failed_liberado(self):
        self.grava_mapa({"event": "open", "name": "mcp-muralha", "chat": "c1", "dispatch": "ctx_1", "run": "r"})
        rc, s = self.roda("Muralha", "--status", "--wait-settled", "60", clock=lambda: 0.0, sleep=lambda s: None,
                          brza_fn=Fake(padrao=js(self.show(state="failed", releaseState="released"))))
        self.assertEqual(rc, 1)
        self.assertIn("falhou: Muralha; parei de esperar", s)


if __name__ == "__main__":
    unittest.main()
