import json
import os

import _exec
import _paths  # noqa: F401
import plan_panel
import plan_state
import round_log
from mini import DESENHO, RODADA1, passo, plano


class Painel(_exec.Base):
    def setUp(self):
        super().setUp()
        plan_panel.publica_seguro = self.originais[(plan_panel, "publica_seguro")]   # aqui o painel é o de verdade
        self.raiz, self.path = self.monta()
        self.pub = os.path.join(self.raiz, "pub")
        self.vazio = os.path.join(self.raiz, "nada.jsonl")
        self.kw = dict(measurements=self.vazio, sessions=self.vazio, states={}, at="2026-11-10T12:00:00-03:00")

    def html(self, **extra):
        r = plan_panel.publica(self.path, publish_dir=self.pub, **{**self.kw, **extra})
        with open(r["html"], encoding="utf-8") as f:
            return r, f.read()

    def test_sem_medicao_nunca_zero(self):
        r, h = self.html()
        self.assertIn("sem medição", h)
        self.assertNotIn("US$ 0", h)
        self.assertRegex(r["linha"], r'^::orca-visual\{file="pln-900-painel-[0-9a-f]{4}\.html" title="PLN-900 — painel do plano"\}$')

    def test_um_arquivo_por_plano_e_dia(self):
        a, _ = self.html()
        b, _ = self.html()
        self.assertEqual(a["linha"], b["linha"])
        c, _ = self.html(at="2026-11-11T09:00:00-03:00")
        self.assertNotEqual(a["linha"], c["linha"])

    def test_cabecalho_e_aviso_de_soma(self):
        _, h = self.html()
        self.assertIn("fase execution", h)
        self.assertNotIn("⚠", h)
        with open(self.path, encoding="utf-8") as f:
            t = f.read()
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(t.replace("estimate_h: 5", "estimate_h: 9"))
        _, h = self.html()
        self.assertIn("⚠ soma dos passos", h)

    def test_estado_do_manifesto_idade_e_sessoes_vivas(self):
        co = self.checkout()[0]
        self.assertEqual(self.roda(executor_mod(), "open", self.path, "P1", "--checkout", co, "--no-panel"), 0)
        r, h = self.html(states={"pln900-p1": "working"}, at=executor_mod().iso(self.clock.t + 120))
        self.assertIn("pln900-p1", h)
        self.assertIn("working", h)
        self.assertIn("2 min", h)
        self.assertIn(">aberto<", h)

    def test_consultores_vivos_entram(self):
        d = os.path.join(self.raiz, ".sessions", "pln-900", "D1")
        os.makedirs(d)
        with open(os.path.join(d, "consultores.json"), "w") as f:
            json.dump({"decisao": "D1", "focos": {"equilibrio": {"sessao": "pln900-d1-equilibrio", "agent": "grok", "estado": "aberto"}}}, f)
        _, h = self.html(states={"pln900-d1-equilibrio": "done"})
        self.assertIn("pln900-d1-equilibrio (D1 · equilibrio)", h)
        self.assertIn("consultor · done", h)

    def test_ultima_rodada(self):
        _, h = self.html()
        self.assertIn("R1 — 2 perguntas, 2 decididas", h)

    def test_publica_seguro_nao_levanta(self):
        r = plan_panel.publica_seguro("PLN-999-nao-existe")
        self.assertTrue(r["aviso"].startswith("⚠ painel:"))
        self.assertIsNone(r["linha"])

    def test_png_com_falha_vira_aviso(self):
        original = plan_panel.gera_png
        plan_panel.gera_png = lambda *a, **k: "sem Chrome"
        try:
            r = plan_panel.publica_seguro(self.path, publish_dir=self.pub, png=True, **self.kw)
        finally:
            plan_panel.gera_png = original
        self.assertEqual(r["aviso"], "⚠ painel: sem Chrome")
        self.assertIsNone(r["png"])
        self.assertTrue(r["linha"])

    def cli(self, *args):
        import io
        from contextlib import redirect_stderr, redirect_stdout
        o, e = io.StringIO(), io.StringIO()
        with redirect_stdout(o), redirect_stderr(e):
            rc = plan_panel.main(list(args))
        return rc, o.getvalue(), e.getvalue()

    def test_cli_render_e_publish(self):
        out = os.path.join(self.raiz, "r.html")
        base = ["--measurements", self.vazio, "--sessions", self.vazio, "--list-json", self.vazio]
        self.assertEqual(self.cli("render", self.path, "--out", out, *base)[0], 0)
        self.assertTrue(os.path.isfile(out))
        rc, o, _ = self.cli("publish", self.path, "--publish-dir", self.pub, *base)
        self.assertEqual(rc, 0)
        self.assertIn("::orca-visual", o)
        self.assertEqual(self.cli("publish", "PLN-999-nao-existe")[0], 2)


def executor_mod():
    import executor
    return executor


import contextlib
import io


class Chamadores(_exec.Base):
    """round_log e plan_state --fix republicam o painel; --no-panel desliga; o aviso não muda o rc."""

    def setUp(self):
        super().setUp()
        self.raiz, self.path = self.monta(plano(passo("P1"), RODADA1, est="9"))
        ctx = contextlib.ExitStack()
        ctx.enter_context(contextlib.redirect_stdout(io.StringIO()))
        ctx.enter_context(contextlib.redirect_stderr(io.StringIO()))
        self.addCleanup(ctx.close)

    def test_plan_state_fix_publica_e_no_panel_desliga(self):
        plan_state.main([self.path, "--fix"])
        self.assertEqual(len(self.paineis), 1)
        plan_state.main([self.path, "--fix", "--no-panel"])
        self.assertEqual(len(self.paineis), 1)
        plan_state.main([self.path])                       # sem --fix não republica
        self.assertEqual(len(self.paineis), 1)

    def test_aviso_do_painel_nao_muda_o_rc(self):
        plan_panel.publica_seguro = lambda pl, **kw: {"linha": None, "png": None, "aviso": "⚠ painel: quebrou"}
        rc_com = plan_state.main([self.path, "--fix"])
        rc_sem = plan_state.main([self.path, "--fix", "--no-panel"])
        self.assertEqual(rc_com, rc_sem)

    def test_round_log_publica_depois_de_gravar(self):
        dados = {"titulo": "a", "enviada": "2026-11-10", "perguntas": [{"tema": "t", "opcoes": [{"rotulo": "x", "recomendada": True, "custo": "c", "se_paga": "agora"}, {"rotulo": "y", "custo": "c", "se_paga": "nunca"}], "resposta": {"escolhidas": [1]}}]}
        d = os.path.join(self.raiz, "rodada.json")
        with open(d, "w") as f:
            json.dump(dados, f)
        self.assertEqual(round_log.main([self.path, "--from", d, "--dry-run"]), 0)
        self.assertEqual(len(self.paineis), 0)
        self.assertEqual(round_log.main([self.path, "--from", d, "--no-panel"]), 0)
        self.assertEqual(len(self.paineis), 0)
        self.assertEqual(round_log.main([self.path, "--from", d]), 0, self.err)
        self.assertEqual(len(self.paineis), 1)


if __name__ == "__main__":
    import unittest
    unittest.main()
