import json
import os

import _exec
import _paths  # noqa: F401
import plan_panel
import plan_state
import round_log
from mini import DESIGN, ROUND1, step, plan


class PanelCase(_exec.Base):
    def setUp(self):
        super().setUp()
        plan_panel.publish_safe = self.originals[(plan_panel, "publish_safe")]   # aqui o painel é o de verdade
        self.root, self.path = self.build()
        self.pub = os.path.join(self.root, "pub")
        self.empty_value = os.path.join(self.root, "nada.jsonl")
        self.kw = dict(measurements=self.empty_value, sessions=self.empty_value, states={}, at="2026-11-10T12:00:00-03:00")

    def html(self, **extra):
        r = plan_panel.publish(self.path, publish_dir=self.pub, **{**self.kw, **extra})
        with open(r["html"], encoding="utf-8") as f:
            return r, f.read()

    def test_without_measurement_never_zero(self):
        r, h = self.html()
        self.assertIn("sem medição", h)
        self.assertNotIn("US$ 0", h)
        self.assertRegex(r["line"], r'^::orca-visual\{file="pln-900-painel-[0-9a-f]{4}\.html" title="PLN-900 — painel do plano"\}$')

    def test_one_file_by_plan_and_day(self):
        a, _ = self.html()
        b, _ = self.html()
        self.assertEqual(a["line"], b["line"])
        c, _ = self.html(at="2026-11-11T09:00:00-03:00")
        self.assertNotEqual(a["line"], c["line"])

    def test_header_and_warning_of_sum(self):
        _, h = self.html()
        self.assertIn("fase execution", h)
        self.assertNotIn("⚠", h)
        with open(self.path, encoding="utf-8") as f:
            t = f.read()
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(t.replace("estimate_h: 5", "estimate_h: 9"))
        _, h = self.html()
        self.assertIn("⚠ soma dos passos", h)

    def test_state_of_manifest_age_and_sessions_live(self):
        co = self.checkout()[0]
        self.assertEqual(self.invoke(executor_mod(), "open", self.path, "P1", "--checkout", co, "--no-panel"), 0)
        r, h = self.html(states={"pln900-p1": "working"}, at=executor_mod().iso(self.clock.t + 120))
        self.assertIn("pln900-p1", h)
        self.assertIn("working", h)
        self.assertIn("2 min", h)
        self.assertIn(">aberto<", h)

    def test_consultants_live_enter(self):
        d = os.path.join(self.root, ".sessions", "pln-900", "D1")
        os.makedirs(d)
        with open(os.path.join(d, "consultants.json"), "w") as f:
            json.dump({"decision": "D1", "focuses": {"equilibrio": {"session": "pln900-d1-equilibrio", "agent": "grok", "state": "aberto"}}}, f)
        _, h = self.html(states={"pln900-d1-equilibrio": "done"})
        self.assertIn("pln900-d1-equilibrio (D1 · equilibrio)", h)
        self.assertIn("consultor · done", h)

    def test_last_round(self):
        _, h = self.html()
        self.assertIn("R1 — 2 perguntas, 2 decididas", h)

    def test_publish_safe_not_raises(self):
        r = plan_panel.publish_safe("PLN-999-nao-existe")
        self.assertTrue(r["warning"].startswith("⚠ painel:"))
        self.assertIsNone(r["line"])

    def test_png_with_failure_becomes_warning(self):
        original = plan_panel.render_png
        plan_panel.render_png = lambda *a, **k: "sem Chrome"
        try:
            r = plan_panel.publish_safe(self.path, publish_dir=self.pub, png=True, **self.kw)
        finally:
            plan_panel.render_png = original
        self.assertEqual(r["warning"], "⚠ painel: sem Chrome")
        self.assertIsNone(r["png"])
        self.assertTrue(r["line"])

    def cli(self, *args):
        import io
        from contextlib import redirect_stderr, redirect_stdout
        o, e = io.StringIO(), io.StringIO()
        with redirect_stdout(o), redirect_stderr(e):
            rc = plan_panel.main(list(args))
        return rc, o.getvalue(), e.getvalue()

    def test_cli_render_and_publish(self):
        out = os.path.join(self.root, "r.html")
        base = ["--measurements", self.empty_value, "--sessions", self.empty_value, "--list-json", self.empty_value]
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


class Callers(_exec.Base):
    """round_log e plan_state --fix republicam o painel; --no-panel desliga; o aviso não muda o rc."""

    def setUp(self):
        super().setUp()
        self.root, self.path = self.build(plan(step("P1"), ROUND1, estimate="9"))
        ctx = contextlib.ExitStack()
        ctx.enter_context(contextlib.redirect_stdout(io.StringIO()))
        ctx.enter_context(contextlib.redirect_stderr(io.StringIO()))
        self.addCleanup(ctx.close)

    def test_plan_state_fix_publish_and_no_panel_turns_off(self):
        plan_state.main([self.path, "--fix"])
        self.assertEqual(len(self.panels), 1)
        plan_state.main([self.path, "--fix", "--no-panel"])
        self.assertEqual(len(self.panels), 1)
        plan_state.main([self.path])                       # sem --fix não republica
        self.assertEqual(len(self.panels), 1)

    def test_warning_of_panel_not_changes_the_rc(self):
        plan_panel.publish_safe = lambda pl, **kw: {"line": None, "png": None, "warning": "⚠ painel: quebrou"}
        rc_with = plan_state.main([self.path, "--fix"])
        rc_without = plan_state.main([self.path, "--fix", "--no-panel"])
        self.assertEqual(rc_with, rc_without)

    def test_round_log_publish_after_of_write(self):
        payload = {"title": "a", "sent_on": "2026-11-10", "questions": [{"topic": "t", "options": [{"label": "x", "recommended": True, "cost": "c", "pays_when": "agora"}, {"label": "y", "cost": "c", "pays_when": "nunca"}], "answer": {"chosen": [1]}}]}
        d = os.path.join(self.root, "rodada.json")
        with open(d, "w") as f:
            json.dump(payload, f)
        self.assertEqual(round_log.main([self.path, "--from", d, "--dry-run"]), 0)
        self.assertEqual(len(self.panels), 0)
        self.assertEqual(round_log.main([self.path, "--from", d, "--no-panel"]), 0)
        self.assertEqual(len(self.panels), 0)
        self.assertEqual(round_log.main([self.path, "--from", d]), 0, self.err)
        self.assertEqual(len(self.panels), 1)


if __name__ == "__main__":
    import unittest
    unittest.main()
