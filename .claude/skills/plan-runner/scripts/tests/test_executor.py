import json
import os
import re
import subprocess

import _exec
import _paths  # noqa: F401
import executor
import plan_md
from mini import DESENHO, RODADA1, passo, plano


class Open(_exec.Base):
    def test_abre_grava_manifesto_worklog_pedido_e_tabela(self):
        raiz, path = self.monta()
        co, _ = self.checkout()
        rc = self.roda(executor, "open", path, "P1", "--checkout", co)
        self.assertEqual(rc, 0, self.err)
        argv = next(a for k, a in self.chamadas if k == "sessions")
        self.assertEqual(argv[0], "pln900-p1")
        self.assertIn("--wait", argv)
        self.assertIn("--rename", argv)
        self.assertEqual(argv[argv.index("--title") + 1], "PLN-900 P1: Um passo")
        self.assertEqual(argv[argv.index("--model") + 1], executor.SONNET)
        self.assertEqual(argv[argv.index("--checkout") + 1], co)
        m = self.manifesto(raiz)["passos"]["P1"]
        self.assertEqual((m["estado"], m["marcador"], m["agent"]), ("aberto", "fim-P1:", "claude"))
        self.assertEqual(m["eventos"][0]["estado"], "aberto")
        wl = self.worklog(raiz)
        with open(wl, encoding="utf-8") as f:
            t = f.read()
        for secao in ("## O que se fez", "## Desvios", "## Evidência", "# PLN-900 P1: Um passo"):
            self.assertIn(secao, t)
        self.assertNotIn("<!-- fim-P1: feito -->\n", t.split("---")[-1].split("linha, e só")[-1])
        self.assertIsNone(executor.ultimo_marcador(wl, "P1"))
        self.assertTrue(os.path.isfile(os.path.join(raiz, m["pedido"])))
        self.assertIn("| P1 | pln900-p1 | claude | %s |" % executor.SONNET, self.out)
        self.assertIn("| Passo | Executor | Runtime | Modelo | Esforço | Checkout | Branch |", self.out)
        self.assertEqual(len(self.paineis), 1)
        self.assertTrue(self.paineis[0]["png"])

    def test_o_molde_do_worklog_nao_tem_o_marcador_literal(self):
        # o `--marker` do `brza` é um `re.search` no arquivo inteiro: a prosa do molde não pode casar com ele
        raiz, path = self.monta()
        self.abre(raiz, path)
        with open(self.worklog(raiz), encoding="utf-8") as f:
            t = f.read()
        self.assertIsNone(re.search(r"<!-- fim-P1:", t))
        self.assertIn("`fim-P1`", t)

    def test_tree_roda_brza_tree_e_deduz_a_branch(self):
        raiz, path = self.monta()
        co, _ = self.checkout()
        self.brza = lambda argv: (0, "worktree: %s\n" % os.path.join(os.path.dirname(co), os.path.basename(co)), "")
        rc = self.roda(executor, "open", path, "P1", "--tree", os.path.basename(co), "--type", "fix", "--no-panel")
        self.assertEqual(rc, 0, self.err)
        self.assertIn(("brza", ["tree", os.path.basename(co), "--type", "fix"]), self.chamadas)
        self.assertEqual(self.manifesto(raiz)["passos"]["P1"]["branch"], "fix/" + os.path.basename(co))

    def test_nao_abriu_nao_grava_manifesto(self):
        raiz, path = self.monta()
        co, _ = self.checkout()
        self.sessions = lambda argv: (1, "", "CHECK: pln900-p1 não abriu: pending-x.json")
        self.assertEqual(self.roda(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 1)
        self.assertIn("pending-*.json", self.err)
        self.assertFalse(os.path.exists(os.path.join(raiz, ".sessions", "pln-900", "execucao.json")))
        self.assertEqual(len([1 for k, _ in self.chamadas if k == "sessions"]), 1)

    def test_sem_id_abre_com_aviso(self):
        raiz, path = self.monta()
        co, _ = self.checkout()
        self.sessions = lambda argv: (1, "", "CHECK: pln900-p1 não deu a sessão em 60 s")
        rc = self.roda(executor, "open", path, "P1", "--checkout", co, "--no-panel")
        self.assertEqual(rc, 0)   # abriu sem o id do provedor: o `wait` o grava depois
        self.assertIn("sem o id do provedor", self.err)
        self.assertEqual(self.manifesto(raiz)["passos"]["P1"]["estado"], "aberto")

    def test_dry_run_nao_grava(self):
        raiz, path = self.monta()
        co, _ = self.checkout()
        self.assertEqual(self.roda(executor, "open", path, "P1", "--checkout", co, "--dry-run"), 0)
        self.assertIn("[dry-run] brza sessions pln900-p1", self.out)
        self.assertFalse(os.path.exists(os.path.join(raiz, ".sessions")))
        self.assertEqual(self.chamadas, [])

    def test_recusa_passo_vivo_e_passo_inexistente(self):
        raiz, path = self.monta()
        co = self.abre(raiz, path)
        self.assertEqual(self.roda(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 1)
        self.assertIn("já tem executor", self.err)
        self.assertEqual(self.roda(executor, "open", path, "P9", "--checkout", co), 2)

    def test_reabrir_parado_ignora_o_marcador_velho(self):
        # A4: o `wait` seguinte esperava o executor novo, e voltava na hora com o `parado` do anterior
        raiz, path = self.monta()
        co = self.abre(raiz, path)
        self.fecha_worklog(raiz, "- desvios: X? — muda o D", "parado")
        self.assertEqual(self.roda(executor, "wait", path, "--no-panel"), 0)
        self.assertEqual(self.manifesto(raiz)["passos"]["P1"]["estado"], "parado")
        self.assertEqual(self.roda(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 0, self.err)
        self.assertIsNone(executor.ultimo_marcador(self.worklog(raiz), "P1"))
        with open(self.worklog(raiz), encoding="utf-8") as f:
            self.assertIn("X? — muda o D", f.read())      # o texto do executor anterior fica
        self.chamadas.clear()
        self.assertEqual(self.roda(executor, "wait", path, "--timeout", "5", "--no-panel"), 75)
        self.assertTrue([x for x in self.chamadas if x[0] == "wait"])

    def test_reabrir_com_a_sessao_viva_recusa_e_nao_apaga_o_marcador(self):
        raiz, path = self.monta()
        co = self.abre(raiz, path)
        self.fecha_worklog(raiz, "- desvios: X? — muda o D", "parado")
        self.roda(executor, "wait", path, "--no-panel")
        self.sessions = lambda argv: (0, "running:  pln900-p1", "")
        self.assertEqual(self.roda(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 1)
        self.assertIn("brza sessions close pln900-p1", self.err)
        self.assertEqual(executor.ultimo_marcador(self.worklog(raiz), "P1"), "parado")
        self.assertEqual(self.manifesto(raiz)["passos"]["P1"]["estado"], "parado")

    def test_running_na_primeira_abertura_manda_fechar_pelo_brza(self):
        # sem entrada no manifesto o `executor.py close` sairia rc 2: o comando certo é o do `brza`
        raiz, path = self.monta()
        co, _ = self.checkout()
        self.sessions = lambda argv: (0, "running:  pln900-p1", "")
        self.assertEqual(self.roda(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 1)
        self.assertIn("brza sessions close pln900-p1", self.err)
        self.assertNotIn("executor.py close", self.err)

    def test_reabrir_com_a_abertura_que_falha_nao_apaga_o_marcador(self):
        raiz, path = self.monta()
        co = self.abre(raiz, path)
        self.fecha_worklog(raiz, "- desvios: X? — muda o D", "parado")
        self.roda(executor, "wait", path, "--no-panel")
        self.sessions = lambda argv: (1, "", "CHECK: pln900-p1 não abriu: pending-x.json")
        self.assertEqual(self.roda(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 1)
        self.assertEqual(executor.ultimo_marcador(self.worklog(raiz), "P1"), "parado")

    def test_reabrir_feito_ou_com_evidencia_gravada_e_recusado_sem_apagar(self):
        raiz, path = self.monta()
        co, sha = self.checkout()
        self.abre(raiz, path, co)
        self.fecha_worklog(raiz, "- commit: brza-studio@%s\n- arquivos: a.py" % sha)
        self.assertEqual(self.roda(executor, "wait", path, "--no-panel"), 0)
        self.assertEqual(self.roda(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 1)
        self.assertIn("não reabre", self.err)
        self.assertEqual(self.roda(executor, "evidence", path, "P1", "--settle", "0", "--apply", "--no-panel"), 0, self.err)
        antes = self.manifesto(raiz)["passos"]["P1"]
        self.assertEqual(antes["estado"], "evidencia-gravada")
        self.assertEqual(self.roda(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 1)
        self.assertEqual(self.manifesto(raiz)["passos"]["P1"], antes)

    def test_checkout_inexistente(self):
        raiz, path = self.monta()
        self.assertEqual(self.roda(executor, "open", path, "P1", "--checkout", "/nao/existe/x"), 1)

    def test_agent_codex_sem_esforco_abre_sem_modelo(self):
        raiz, path = self.monta()
        co, _ = self.checkout()
        self.roda(executor, "open", path, "P1", "--checkout", co, "--agent", "codex", "--no-panel")
        argv = next(a for k, a in self.chamadas if k == "sessions")
        self.assertNotIn("--model", argv)
        self.assertNotIn("--effort", argv)
        self.assertEqual(argv[argv.index("--agent") + 1], "codex")

    def test_codex_com_esforco_leva_o_modelo_padrao_porque_o_brza_exige(self):
        # A1: `brza sessions --effort` sem `--model` sai com "CHECK: --effort exige --model"
        raiz, path = self.monta()
        co, _ = self.checkout()
        self.roda(executor, "open", path, "P1", "--checkout", co, "--agent", "codex", "--effort", "high", "--no-panel")
        argv = next(a for k, a in self.chamadas if k == "sessions")
        self.assertEqual(argv[argv.index("--model") + 1], executor.CODEX_MODEL)
        self.assertEqual(argv[argv.index("--effort") + 1], "high")
        self.assertEqual(self.manifesto(raiz)["passos"]["P1"]["model"], executor.CODEX_MODEL)

    def test_runtime_sem_modelo_padrao_nao_passa_esforco_e_avisa(self):
        raiz, path = self.monta()
        co, _ = self.checkout()
        self.roda(executor, "open", path, "P1", "--checkout", co, "--agent", "grok", "--effort", "high", "--no-panel")
        argv = next(a for k, a in self.chamadas if k == "sessions")
        self.assertNotIn("--effort", argv)
        self.assertNotIn("--model", argv)
        self.assertIn("recusa --effort sem --model", self.err)

    def test_sem_checkout_nem_tree_recusa_pedindo_checkout_explicito(self):
        # A5: o padrão seria o próprio brza-workspace, onde o pedido proíbe o commit
        raiz, path = self.monta()
        self.assertEqual(self.roda(executor, "open", path, "P1", "--no-panel"), 2)
        self.assertIn("--checkout", self.err)
        self.assertEqual([k for k, _ in self.chamadas if k == "sessions"], [])
        self.assertEqual(self.roda(executor, "open", path, "P1", "--dry-run"), 2)

    def test_checkout_na_master_usa_a_branch_do_passo_e_nunca_a_master(self):
        raiz, path = self.monta()
        co, _ = self.checkout()
        subprocess.run(["git", "-C", co, "checkout", "-q", "-B", "master"], check=True)
        self.assertEqual(self.roda(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 0, self.err)
        self.assertEqual(self.manifesto(raiz)["passos"]["P1"]["branch"], "feat/pln-900-p1")
        with open(os.path.join(raiz, self.manifesto(raiz)["passos"]["P1"]["pedido"]), encoding="utf-8") as f:
            texto = f.read()
        self.assertIn("autoriza o commit na branch `feat/pln-900-p1`", texto)
        self.assertNotIn("branch `master`", texto)
        raiz2, path2 = self.monta()
        self.assertEqual(self.roda(executor, "open", path2, "P1", "--checkout", co, "--branch", "main", "--no-panel"), 1)
        self.assertIn("master/main", self.err)

    def test_tree_confere_o_pedido_antes_de_criar_o_worktree(self):
        # A13: o passo executa um D que o Desenho não tem; o `brza tree` não pode ter rodado
        raiz, path = self.monta(plano(passo("P1", executa="Executa D9"), RODADA1), design=DESENHO)
        self.assertEqual(self.roda(executor, "open", path, "P1", "--tree", "pln-900-p1", "--no-panel"), 1)
        self.assertIn("D9", self.err)
        self.assertEqual([x for x in self.chamadas if x[0] == "brza"], [])


class Wait(_exec.Base):
    def setUp(self):
        super().setUp()
        self.raiz, self.path = self.monta()
        self.co = self.abre(self.raiz, self.path)

    def estado(self):
        return self.manifesto(self.raiz)["passos"]["P1"]["estado"]

    def test_marcador_feito_ja_no_worklog(self):
        self.fecha_worklog(self.raiz, "- arquivos: a.py")
        self.assertEqual(self.roda(executor, "wait", self.path, "--timeout", "30", "--no-panel"), 0)
        self.assertRegex(self.out, r"P1 · feito em \d+ min")
        self.assertEqual(self.estado(), "feito")

    def test_marcador_parado(self):
        self.fecha_worklog(self.raiz, "- desvios: X? — muda o D", "parado")
        self.assertEqual(self.roda(executor, "wait", self.path, "--no-panel"), 0)
        self.assertIn("P1 · parado", self.out)
        self.assertEqual(self.estado(), "parado")

    def test_prazo_75_e_batida_com_idade(self):
        rc = self.roda(executor, "wait", self.path, "--timeout", "400", "--no-panel")
        self.assertEqual(rc, 75)
        self.assertRegex(self.out, r"P1 · em curso \d+ min \(último evento há \d+ min\)")
        self.assertIn("prazo:", self.out)
        self.assertEqual(self.estado(), "em-curso")

    def test_ended_without_marker_nao_e_fim(self):
        n = []

        def espera(nomes, t, markers=(), any_=True):
            n.append(markers)
            return 0, {"done": [{"name": "pln900-p1", "outcome": "ended_without_marker"}], "pending": [], "timed_out": False, "events": []}
        self.wait = espera
        rc = self.roda(executor, "wait", self.path, "--timeout", "60", "--no-panel")
        self.assertEqual(rc, 75)
        self.assertEqual(self.out.count("o turno acabou sem o marcador"), 1)
        self.assertGreater(len(n), 1)                       # a espera seguiu, e não girou para sempre
        self.assertEqual(len(n[0]), 1)
        self.assertTrue(n[0][0].endswith(":<!-- fim-P1:"))

    def test_done_com_marcador_vira_feito(self):
        def espera(nomes, t, markers=(), any_=True):
            self.fecha_worklog(self.raiz, "- arquivos: a.py")
            return 0, {"done": [{"name": "pln900-p1", "outcome": "done"}], "pending": [], "timed_out": False, "events": []}
        self.wait = espera
        self.assertEqual(self.roda(executor, "wait", self.path, "--no-panel"), 0)
        self.assertEqual(self.estado(), "feito")

    def test_bloqueado_3_e_falhou_1(self):
        self.wait = lambda *a, **k: (0, {"done": [{"name": "pln900-p1", "outcome": "blocked"}], "pending": [], "timed_out": False, "events": []})
        self.assertEqual(self.roda(executor, "wait", self.path, "--no-panel"), 3)
        self.assertIn("brza sessions read pln900-p1 --last", self.out)
        self.assertEqual(self.estado(), "bloqueado")
        self.wait = lambda *a, **k: (1, {"done": [{"name": "pln900-p1", "outcome": "failed"}], "pending": [], "timed_out": False, "events": []})
        self.assertEqual(self.roda(executor, "wait", self.path, "--no-panel"), 1)
        self.assertEqual(self.estado(), "falhou")

    def test_ruido_do_host_nao_vira_linha(self):
        ev = [{"type": "escalation", "subject": "Worker stopped without reporting", "id": "1"},
              {"type": "question", "subject": "posso apagar?", "id": "2"}]
        self.wait = lambda *a, **k: (75, {"done": [], "pending": [], "timed_out": True, "events": ev})
        self.roda(executor, "wait", self.path, "--timeout", "10", "--no-panel")
        self.assertNotIn("Worker stopped", self.out)
        self.assertIn("atenção · question — posso apagar?", self.out)

    def test_erro_do_brza_e_passo_sem_executor(self):
        self.wait = lambda *a, **k: (127, {"error": "brza ausente"})
        self.assertEqual(self.roda(executor, "wait", self.path, "--no-panel"), 1)
        self.assertEqual(self.roda(executor, "wait", self.path, "P7"), 2)

    def test_sessao_que_nao_existe_para_com_mensagem_clara_e_sem_girar(self):
        # o `brza sessions wait` de uma sessão inexistente sai rc 1 com `error`; o laço girava sem pausa
        self.wait = lambda *a, **k: (1, {"error": "0 chats abertos se chamam pln900-p1: "})
        self.assertEqual(self.roda(executor, "wait", self.path, "--timeout", "600", "--no-panel"), 1)
        self.assertEqual(len([x for x in self.chamadas if x[0] == "wait"]), 1)
        self.assertIn("pln900-p1", self.err)
        self.assertNotIn("pln900-p1,", self.err)
        self.assertIn("não existe", self.err)
        self.assertEqual(self.estado(), "falhou")

    def test_so_a_sessao_perdida_falha_e_a_outra_segue_esperavel(self):
        m = self.manifesto(self.raiz)
        m["passos"]["P2"] = dict(m["passos"]["P1"], sessao="pln900-p2", worklog=m["passos"]["P1"]["worklog"].replace("p1", "p2"))
        with open(os.path.join(self.raiz, ".sessions", "pln-900", "execucao.json"), "w") as f:
            json.dump(m, f)
        self.wait = lambda nomes, t, markers=(), any_=True: (
            (1, {"error": "0 chats abertos se chamam pln900-p2: "}) if "pln900-p2" in nomes else (75, {"done": [], "timed_out": True, "events": []}))
        self.assertEqual(self.roda(executor, "wait", self.path, "P1", "P2", "--timeout", "5", "--no-panel"), 1)
        self.assertEqual(self.manifesto(self.raiz)["passos"]["P2"]["estado"], "falhou")
        self.assertEqual(self.estado(), "em-curso")
        self.assertEqual(self.roda(executor, "wait", self.path, "--timeout", "5", "--no-panel"), 75)   # o P1 segue esperável

    def test_nome_duplicado_para_e_nao_diz_que_nao_existe(self):
        self.wait = lambda *a, **k: (1, {"error": "2 chats abertos se chamam pln900-p1: a, b"})
        self.assertEqual(self.roda(executor, "wait", self.path, "--timeout", "600", "--no-panel"), 1)
        self.assertNotIn("não existe", self.err)
        self.assertIn("2 chats", self.err)

    def test_erro_repetido_do_brza_pausa_e_desiste(self):
        self.wait = lambda *a, **k: (1, {"error": "saída sem JSON (rc 1): boom"})
        t0 = self.clock.t
        self.assertEqual(self.roda(executor, "wait", self.path, "--timeout", "600", "--no-panel"), 1)
        n = len([x for x in self.chamadas if x[0] == "wait"])
        self.assertEqual(n, executor.MAX_WAIT_ERRORS)
        self.assertGreaterEqual(self.clock.t - t0, executor.WAIT_ERROR_PAUSE * (n - 1))
        self.assertIn("boom", self.err)

    def test_a_linha_em_curso_sai_no_intervalo_da_narracao_e_nao_a_cada_volta(self):
        # A15: com o turno acabado sem o marcador o `wait` volta na hora; a linha prometida é a cada ~3 min
        self.wait = lambda nomes, t, markers=(), any_=True: (
            0, {"done": [{"name": "pln900-p1", "outcome": "ended_without_marker"}], "pending": [], "timed_out": False, "events": []})
        self.assertEqual(self.roda(executor, "wait", self.path, "--timeout", "600", "--no-panel"), 75)
        linhas = [l for l in self.saidas if "em curso" in l]
        self.assertGreaterEqual(len(linhas), 2)
        self.assertLessEqual(len(linhas), 600 // executor.BATIDA + 1)

    def test_dois_passos_nao_passam_marker(self):
        raiz, path = self.raiz, self.path
        m = self.manifesto(raiz)
        m["passos"]["P2"] = dict(m["passos"]["P1"], sessao="pln900-p2", worklog=m["passos"]["P1"]["worklog"].replace("p1", "p2"))
        with open(os.path.join(raiz, ".sessions", "pln-900", "execucao.json"), "w") as f:
            json.dump(m, f)
        vistos = []
        self.wait = lambda nomes, t, markers=(), any_=True: (vistos.append(markers), (75, {"done": [], "timed_out": True, "events": []}))[1]
        self.roda(executor, "wait", path, "P1", "P2", "--timeout", "5", "--no-panel")
        self.assertEqual(vistos[0], [])

    def test_painel_so_com_evento(self):
        self.fecha_worklog(self.raiz, "- arquivos: a.py")
        self.paineis.clear()
        self.roda(executor, "wait", self.path)
        self.assertEqual(len(self.paineis), 1)


class SendRework(_exec.Base):
    def test_send_a_passo_feito_ou_parado_apaga_o_marcador_e_o_wait_espera(self):
        # o caminho "não confere: volte ao executor pelo `send`"
        for marcador in ("feito", "parado"):
            raiz, path = self.monta()
            self.abre(raiz, path)
            self.fecha_worklog(raiz, "- arquivos: a.py", marcador)
            self.assertEqual(self.roda(executor, "wait", path, "--no-panel"), 0)
            self.assertEqual(self.roda(executor, "send", path, "P1", "--text", "refaça"), 0, self.err)
            self.assertEqual(self.manifesto(raiz)["passos"]["P1"]["estado"], "em-curso")
            self.assertIsNone(executor.ultimo_marcador(self.worklog(raiz), "P1"))
            self.chamadas.clear()
            self.assertEqual(self.roda(executor, "wait", path, "--timeout", "5", "--no-panel"), 75)
            self.assertTrue([x for x in self.chamadas if x[0] == "wait"])


class Evidence(_exec.Base):
    def setUp(self):
        super().setUp()
        self.raiz, self.path = self.monta()
        self.co, self.sha = self.checkout()
        self.abre(self.raiz, self.path, self.co)

    def fecha(self, evid=None, marcador="feito"):
        evid = evid or ("- commit: brza-studio@%s\n- comando: `pytest -q` → 3 passed (≤ 2 min)\n- arquivos: a.py\n- desvios: X? — nome trocado" % self.sha)
        self.fecha_worklog(self.raiz, evid, marcador)

    def plano_texto(self):
        with open(self.path, encoding="utf-8") as f:
            return f.read()

    def test_proposta_confere_e_nao_grava(self):
        self.fecha()
        antes = self.plano_texto()
        rc = self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--rerun")
        self.assertEqual(rc, 0, self.err)
        self.assertIn("confere: `git -C %s cat-file -e %s` → ok" % (self.co, self.sha), self.out)
        self.assertIn("confere: `pytest -q` → 3 passed", self.out)
        self.assertIn("**Evidência:** brza-studio@%s · `pytest -q` → 3 passed · arquivos: a.py" % self.sha, self.out)
        self.assertRegex(self.out, r"Executado: [\d.]+ h \(janela; sem medição dos turnos\)")
        self.assertIn("X? — nome trocado", self.out)
        self.assertEqual(self.plano_texto(), antes)
        self.assertEqual(self.manifesto(self.raiz)["passos"]["P1"]["estado"], "aberto")

    def test_a_proposta_nao_roda_o_comando_do_worklog(self):
        # A11: o worklog é entrada de outra sessão; o comando só roda com --apply ou --rerun, depois da leitura
        self.fecha()
        chamado = []
        executor.run_shell = lambda cmd, cwd, timeout=120: (chamado.append(cmd), (0, "3 passed\n"))[1]
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0"), 0, self.err)
        self.assertEqual(chamado, [])
        self.assertIn("não rodei `pytest -q`", self.out)
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--rerun"), 0, self.err)
        self.assertEqual(chamado, ["pytest -q"])
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 0, self.err)
        self.assertEqual(chamado, ["pytest -q", "pytest -q"])

    def test_comando_que_nao_e_simples_nunca_roda(self):
        self.fecha("- commit: brza-studio@%s\n- comando: `pytest -q; rm -rf x` → ok (≤ 2 min)\n"
                   "- comando: `echo $(id) | cat` → ok (≤ 2 min)" % self.sha)
        chamado = []
        executor.run_shell = lambda cmd, cwd, timeout=120: (chamado.append(cmd), (0, ""))[1]
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--rerun"), 0, self.err)
        self.assertEqual(chamado, [])
        self.assertEqual(self.out.count("não é um comando que o argv reproduz"), 2)

    def test_hash_no_meio_da_palavra_nao_e_comentario_e_cd_expande_til(self):
        executor.run_shell = self.originais[(executor, "run_shell")]
        self.assertEqual(executor.parse_command("echo a#b")[2], [("echo", True), ("a#b", True)])
        self.assertEqual(executor.run_shell("echo a#b", self.co)[1].strip(), "a#b")
        rc, so = executor.run_shell("cd ~ && pwd", self.co)
        self.assertEqual(so.strip(), os.path.realpath(os.path.expanduser("~")))

    def test_cobre_marca_so_os_subpassos_declarados(self):
        self.fecha("- commit: brza-studio@%s\n- arquivos: a.py\n- cobre: 1" % self.sha)
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 0, self.err)
        self.assertEqual([c[1] for c in plan_md.carrega(self.path).passo("P1").checks], ["x", " "])
        self.assertNotIn("sem `cobre:`", self.out + self.err)

    def test_cobre_todos_e_sem_declaracao_marcam_todos_e_a_segunda_avisa(self):
        self.fecha("- commit: brza-studio@%s\n- arquivos: a.py\n- cobre: todos" % self.sha)
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 0, self.err)
        self.assertEqual([c[1] for c in plan_md.carrega(self.path).passo("P1").checks], ["x", "x"])
        self.assertNotIn("sem `cobre:`", self.out + self.err)

    def test_sem_cobre_marca_todos_e_avisa(self):
        self.fecha("- commit: brza-studio@%s\n- arquivos: a.py" % self.sha)
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 0, self.err)
        self.assertEqual([c[1] for c in plan_md.carrega(self.path).passo("P1").checks], ["x", "x"])
        self.assertIn("sem `cobre:`", self.out + self.err)

    def test_cobre_parcial_deixa_o_passo_reabrivel_pelo_send_e_pelo_open(self):
        self.fecha("- commit: brza-studio@%s\n- arquivos: a.py\n- cobre: 1" % self.sha)
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 0, self.err)
        self.assertEqual(self.manifesto(self.raiz)["passos"]["P1"]["estado"], "evidencia-gravada")
        # o `send` do que falta: marcador novo e `em-curso`, e o `wait` espera de verdade
        self.assertEqual(self.roda(executor, "send", self.path, "P1", "--text", "falta o 2"), 0, self.err)
        self.assertEqual(self.manifesto(self.raiz)["passos"]["P1"]["estado"], "em-curso")
        self.assertIsNone(executor.ultimo_marcador(self.worklog(self.raiz), "P1"))
        self.chamadas.clear()
        self.assertEqual(self.roda(executor, "wait", self.path, "--timeout", "5", "--no-panel"), 75)
        self.assertTrue([x for x in self.chamadas if x[0] == "wait"])
        # o ciclo fecha: cobre o que falta e aplica de novo
        with open(self.worklog(self.raiz), encoding="utf-8") as f:
            texto = f.read()
        with open(self.worklog(self.raiz), "w", encoding="utf-8") as f:
            f.write(texto.replace("- cobre: 1", "- cobre: 1\n- cobre: 2") + "\n<!-- fim-P1: feito -->\n")
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 0, self.err)
        self.assertEqual([c[1] for c in plan_md.carrega(self.path).passo("P1").checks], ["x", "x"])

    def test_open_reabre_o_passo_parcial_e_recusa_quando_nao_sobra_pendente(self):
        self.fecha("- commit: brza-studio@%s\n- arquivos: a.py\n- cobre: 1" % self.sha)
        self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--apply")
        self.assertEqual(self.roda(executor, "open", self.path, "P1", "--checkout", self.co, "--no-panel"), 0, self.err)
        self.assertIsNone(executor.ultimo_marcador(self.worklog(self.raiz), "P1"))

    def test_send_a_passo_completo_com_evidencia_gravada_nao_reabre(self):
        self.fecha()
        self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--apply")
        self.roda(executor, "send", self.path, "P1", "--text", "x")
        self.assertEqual(self.manifesto(self.raiz)["passos"]["P1"]["estado"], "evidencia-gravada")

    def test_duas_linhas_cobre_se_juntam_e_todos_vence(self):
        self.fecha("- commit: brza-studio@%s\n- arquivos: a.py\n- cobre: 1\n- cobre: 2" % self.sha)
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 0, self.err)
        self.assertEqual([c[1] for c in plan_md.carrega(self.path).passo("P1").checks], ["x", "x"])
        self.assertEqual(executor.le_evidencia("## Evidência\n- cobre: 1\n- cobre: todos\n")["cobre"], "todos")
        self.assertEqual(executor.le_evidencia("## Evidência\n- cobre: 1\n- cobre: 2, 1\n")["cobre"], ["1", "2"])

    def test_cobre_com_subpasso_que_nao_existe_nao_confere(self):
        self.fecha("- commit: brza-studio@%s\n- arquivos: a.py\n- cobre: 1, 9" % self.sha)
        antes = self.plano_texto()
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 1)
        self.assertIn("9", self.err)
        self.assertEqual(self.plano_texto(), antes)

    def test_comando_com_env_e_cd_na_frente_e_reconferido(self):
        self.fecha("- commit: brza-studio@%s\n- comando: `cd app && PYTHONDONTWRITEBYTECODE=1 python3 -I -m unittest` → 3 passed (≤ 2 min)" % self.sha)
        chamado = []
        executor.run_shell = lambda cmd, cwd, timeout=120: (chamado.append(cmd), (0, "3 passed\n"))[1]
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--rerun"), 0, self.err)
        self.assertEqual(len(chamado), 1)

    def test_run_shell_roda_sem_shell_e_aceita_env_cd_glob_e_til(self):
        executor.run_shell = self.originais[(executor, "run_shell")]
        self.assertEqual(executor.parse_command("pytest -q 'a b'"), ({}, None, [("pytest", True), ("-q", True), ("a b", False)]))
        for ruim in ("a; b", "a && b", "a | b", "a > f", "echo $(x)", "echo `x`", "a\nb", "", "a 'b", "A=1"):
            self.assertIsNone(executor.parse_command(ruim), ruim)
        rc, so = executor.run_shell("echo oi", self.co)
        self.assertEqual((rc, so.strip()), (0, "oi"))
        self.assertEqual(executor.run_shell("nao-existe-xyz", self.co)[0], 127)
        self.assertEqual(executor.run_shell("FOO=bar env", self.co)[1].count("FOO=bar"), 1)       # VAR= pelo env
        os.makedirs(os.path.join(self.co, "sub"))
        with open(os.path.join(self.co, "sub", "t1.py"), "w") as f:
            f.write("x")
        self.assertEqual(executor.run_shell("cd sub && pwd", self.co)[1].strip(), os.path.realpath(os.path.join(self.co, "sub")))  # cd pelo cwd
        self.assertEqual(executor.run_shell("ls sub/t*.py", self.co)[1].strip(), "sub/t1.py")     # glob
        self.assertEqual(executor.run_shell("echo 'sub/t*.py'", self.co)[1].strip(), "sub/t*.py")   # aspas: sem glob
        self.assertEqual(executor.run_shell("echo ~", self.co)[1].strip(), os.path.expanduser("~"))

    def test_commit_que_nao_existe_nao_confere(self):
        self.fecha("- commit: brza-studio@deadbee1\n- arquivos: a.py")
        antes = self.plano_texto()
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 1)
        self.assertIn("NÃO confere", self.out)
        self.assertIn("o passo não fecha", self.err)
        self.assertEqual(self.plano_texto(), antes)

    def test_comando_que_falha_nao_confere(self):
        self.fecha()
        executor.run_shell = lambda cmd, cwd, timeout=120: (1, "1 failed\n")
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--rerun"), 1)
        self.assertIn("NÃO confere: `pytest -q` → rc 1, 1 failed", self.out)

    def test_comando_sem_limite_de_tempo_nao_roda(self):
        self.fecha("- commit: brza-studio@%s\n- comando: `pytest` → 900 passed" % self.sha)
        chamado = []
        executor.run_shell = lambda cmd, cwd, timeout=120: (chamado.append(cmd), (0, ""))[1]
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0"), 0)
        self.assertEqual(chamado, [])
        self.assertIn("não rodei `pytest`", self.out)

    def test_sem_marcador_ou_sem_evidencia(self):
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0"), 1)
        self.assertIn("não termina em", self.err)
        self.fecha("nada aqui")
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0"), 1)
        self.assertIn("não traz `## Evidência` com itens", self.err)

    def test_parado_nao_aplica(self):
        self.fecha(marcador="parado")
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0"), 0)
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 1)
        self.assertIn("parado", self.err)

    def test_apply_grava_marca_soma_e_publica(self):
        self.fecha()
        self.paineis.clear()
        rc = self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--apply")
        self.assertEqual(rc, 0, self.err)
        pl = plan_md.carrega(self.path)
        p = pl.passo("P1")
        self.assertEqual([c[1] for c in p.checks], ["x", "x"])
        self.assertIn("brza-studio@%s" % self.sha, p.evidencia)
        self.assertTrue(p.executado_preenchido)
        self.assertIn("janela", p.executado_txt)
        self.assertAlmostEqual(float(pl.fm["executed_h"]), p.executado_h, 2)
        man = self.manifesto(self.raiz)["passos"]["P1"]
        self.assertEqual(man["estado"], "evidencia-gravada")
        self.assertEqual(man["evidencia"]["desvios"], ["X? — nome trocado"])
        self.assertEqual(len(self.paineis), 1)
        # roda de novo: troca a evidência, não duplica
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--apply", "--no-panel"), 0)
        self.assertEqual(self.plano_texto().count("**Evidência:**"), 1)

    def test_apply_com_evidencia_anterior_substitui(self):
        self.fecha()
        t = self.plano_texto().replace("- [ ] **1. A**", "- [ ] **1. A**\n\n**Evidência:** velha · `x` → y\n", 1)
        with open(self.path, "w") as f:
            f.write(t)
        self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--apply", "--no-panel")
        self.assertNotIn("velha", self.plano_texto())

    def test_grok_e_sem_medicao(self):
        m = self.manifesto(self.raiz)
        m["passos"]["P1"]["agent"] = "grok"
        with open(os.path.join(self.raiz, ".sessions", "pln-900", "execucao.json"), "w") as f:
            json.dump(m, f)
        self.fecha()
        self.roda(executor, "evidence", self.path, "P1", "--settle", "0")
        self.assertIn("Executado: sem medição", self.out)

    def test_claude_medido_pela_janela_e_pelos_turnos(self):
        self.fecha()
        m = self.manifesto(self.raiz)
        ev = m["passos"]["P1"]["eventos"]
        ev[0]["at"] = "2026-11-10T10:00:00-03:00"
        ev.append({"at": "2026-11-10T10:36:00-03:00", "estado": "feito", "nota": "x"})
        with open(os.path.join(self.raiz, ".sessions", "pln-900", "execucao.json"), "w") as f:
            json.dump(m, f)
        mp = os.path.join(self.raiz, "meas.jsonl")
        sp = os.path.join(self.raiz, "sess.jsonl")
        with open(sp, "w") as f:
            f.write(json.dumps({"event": "open", "name": "pln900-p1", "chat": "c", "agent": "claude", "provider_session": "S1", "at": "2026-11-10T10:00:00-03:00"}) + "\n")
        with open(mp, "w") as f:
            for dur, custo, h in ((600, 1.5, "10:10:00"), (840, 1.6, "10:35:30")):
                f.write(json.dumps({"event": "turn", "session_id": "S1", "timestamp": "2026-11-10T%s-03:00" % h,
                                    "duration_s": dur, "estimated_cost_usd": custo}) + "\n")
        self.roda(executor, "evidence", self.path, "P1", "--settle", "0", "--measurements", mp, "--sessions", sp)
        self.assertIn("Executado: 0.6 h (janela; 0.4 h de turnos; US$ 3.10)", self.out)

    def test_parser_da_evidencia(self):
        ev = executor.le_evidencia("# x\n\n## Evidência\n\n- commit: aguarda confirmação\n- comando: `a b` → ok\n- arquivos: x.py, y.py\n"
                                   "- desvios: nenhum\n\n<!-- fim-P1: feito -->\n\n## Custo da tarefa\n\nUS$ 1\n")
        self.assertTrue(ev["aguarda"])
        self.assertEqual(ev["commits"], [])
        self.assertEqual(ev["comandos"], [{"cmd": "a b", "resultado": "ok", "rerun": False}])
        self.assertEqual(ev["arquivos"], ["x.py", "y.py"])
        self.assertIsNone(executor.le_evidencia("# sem seção\n"))

    def test_marcador_vale_com_o_anexo_do_brza_note(self):
        self.fecha()
        with open(self.worklog(self.raiz), "a") as f:
            f.write("\n## Custo da tarefa\n\nUS$ 1,00\n")
        self.assertEqual(executor.ultimo_marcador(self.worklog(self.raiz), "P1"), "feito")


class CloseSend(_exec.Base):
    def setUp(self):
        super().setUp()
        self.raiz, self.path = self.monta()
        self.abre(self.raiz, self.path)

    def estado(self):
        return self.manifesto(self.raiz)["passos"]["P1"]["estado"]

    def troca_consulta(self, f):
        self.consulta_orig = executor._consulta
        executor._consulta = f

    def test_closing_nao_e_fechada(self):
        self.sessions = lambda argv: (0, json.dumps({"status": "closing"}), "")
        self.assertEqual(self.roda(executor, "close", self.path, "P1", "--no-panel"), 0)
        self.assertIn("NÃO está fechada", self.out)
        self.assertEqual(self.estado(), "aberto")
        argv = [a for k, a in self.chamadas if k == "sessions"][-1]
        self.assertEqual(argv, ["close", "pln900-p1", "--json"])

    def test_aceite_confere_e_fecha(self):
        self.sessions = lambda argv: (0, json.dumps({"status": "closing"}), "")
        self.troca_consulta(lambda pl, nome: ("encerrada e aceita", None))
        try:
            self.assertEqual(self.roda(executor, "close", self.path, "P1", "--wait-settled", "30"), 0)
        finally:
            executor._consulta = self.consulta_orig
        self.assertIn("P1 · encerrada e aceita", self.out)
        self.assertEqual(self.estado(), "fechado")
        self.assertTrue(self.paineis[-1]["png"])

    def test_prazo_do_aceite_75_e_incerto_75(self):
        self.sessions = lambda argv: (0, json.dumps({"status": "closing"}), "")
        self.troca_consulta(lambda pl, nome: ("ativa", None))
        try:
            self.assertEqual(self.roda(executor, "close", self.path, "P1", "--wait-settled", "20", "--no-panel"), 75)
        finally:
            executor._consulta = self.consulta_orig
        self.sessions = lambda argv: (75, json.dumps({"status": "stop_unknown"}), "")
        self.assertEqual(self.roda(executor, "close", self.path, "P1"), 75)

    def test_modos_de_fechar(self):
        self.sessions = lambda argv: (0, json.dumps({"status": "kept_open"}), "")
        self.roda(executor, "close", self.path, "P1", "--keep-open")
        self.assertEqual([a for k, a in self.chamadas if k == "sessions"][-1], ["close", "pln900-p1", "--keep-open", "--json"])
        self.assertIn("mantida aberta", self.out)

    def test_veredito(self):
        v = executor.veredito({"worker": {"state": "succeeded", "stage": "settled"}, "dispatch": {"completedAt": "x"}})[0]
        self.assertEqual(v, "encerrada e aceita")
        self.assertEqual(executor.veredito({"result": {"worker": {"state": "running"}}})[0], "ativa")
        self.assertEqual(executor.veredito({"worker": {"state": "failed"}})[0], "falhou")

    def test_send_usa_uma_chamada_e_reabre_o_estado(self):
        self.sessions = lambda argv: (0, json.dumps({"receipts": [{"status": "delivered"}]}), "")
        self.assertEqual(self.roda(executor, "send", self.path, "P1", "--text", "use X", "--operation", "op1"), 0)
        argv = [a for k, a in self.chamadas if k == "sessions"][-1]
        self.assertEqual(argv, ["send", "pln900-p1", "--text", "use X", "--json", "--operation", "op1"])
        self.assertEqual(self.estado(), "em-curso")

    def test_send_incerto_nao_reenvia(self):
        self.sessions = lambda argv: (75, json.dumps({"receipts": [{"status": "pending"}]}), "")
        self.assertEqual(self.roda(executor, "send", self.path, "P1", "--text", "x"), 75)
        self.assertIn("não reenvie", self.err)

    def test_status(self):
        self.assertEqual(self.roda(executor, "status", self.path), 0)
        self.assertRegex(self.out, r"P1 · pln900-p1 · aberto · aberto há \d+ min")
        self.roda(executor, "status", self.path, "--json")
        self.assertEqual(json.loads(self.out)["passos"][0]["sessao"], "pln900-p1")

    def test_status_sem_manifesto(self):
        raiz, path = self.monta()
        self.roda(executor, "status", path)
        self.assertIn("sem executor aberto", self.out)


if __name__ == "__main__":
    import unittest
    unittest.main()
