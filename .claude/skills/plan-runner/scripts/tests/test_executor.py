import json
import os
import re

import _exec
import _paths  # noqa: F401
import executor
import plan_md


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

    def test_checkout_inexistente(self):
        raiz, path = self.monta()
        self.assertEqual(self.roda(executor, "open", path, "P1", "--checkout", "/nao/existe/x"), 1)

    def test_agent_codex_sem_modelo_padrao(self):
        raiz, path = self.monta()
        co, _ = self.checkout()
        self.roda(executor, "open", path, "P1", "--checkout", co, "--agent", "codex", "--effort", "high", "--no-panel")
        argv = next(a for k, a in self.chamadas if k == "sessions")
        self.assertNotIn("--model", argv)
        self.assertEqual(argv[argv.index("--agent") + 1], "codex")


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
        rc = self.roda(executor, "evidence", self.path, "P1", "--settle", "0")
        self.assertEqual(rc, 0, self.err)
        self.assertIn("confere: `git -C %s cat-file -e %s` → ok" % (self.co, self.sha), self.out)
        self.assertIn("confere: `pytest -q` → 3 passed", self.out)
        self.assertIn("**Evidência:** brza-studio@%s · `pytest -q` → 3 passed · arquivos: a.py" % self.sha, self.out)
        self.assertRegex(self.out, r"Executado: [\d.]+ h \(janela; sem medição dos turnos\)")
        self.assertIn("X? — nome trocado", self.out)
        self.assertEqual(self.plano_texto(), antes)
        self.assertEqual(self.manifesto(self.raiz)["passos"]["P1"]["estado"], "aberto")

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
        self.assertEqual(self.roda(executor, "evidence", self.path, "P1", "--settle", "0"), 1)
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
