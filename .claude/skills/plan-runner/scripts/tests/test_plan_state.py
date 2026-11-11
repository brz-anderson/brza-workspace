import io
import json
import os
import shutil
import unittest
from contextlib import redirect_stderr, redirect_stdout

import _paths  # noqa: F401
import plan_md
import plan_state
from mini import DESIGN, ROUND1, step, plan

EV = "`brza-workspace@a1b2c3d` · `python3 -m unittest` → 12 OK"


def code_list(overview, level=None):
    return sorted(p["code"] for p in overview["problems"] if level is None or p["level"] == level)


class Base(unittest.TestCase):
    def setUp(self):
        self.dirs = []

    def tearDown(self):
        for d in self.dirs:
            shutil.rmtree(d, ignore_errors=True)

    def build(self, *a, **k):
        root, path = _paths.plan_tmp(*a, **k)
        self.dirs.append(root)
        return root, path

    def state(self, *a, **k):
        root, path = self.build(*a, **k)
        return plan_state.state(path)

    def cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = plan_state.main(list(args) + ["--no-panel"])
        return rc, out.getvalue(), err.getvalue()


class RealPlans(Base):
    def test_pln021_open_clean(self):
        overview = plan_state.state("PLN-021", root=_paths.ROOT_DIR)
        self.assertEqual(overview["problems"], [])
        self.assertEqual(overview["next"], "P1")
        self.assertEqual(overview["hours"]["summed"]["estimate_h"], 41)
        self.assertTrue(overview["hours"]["matches"])
        self.assertEqual(overview["ids"]["P"][-1], "P10")
        self.assertEqual([p["state"] for p in overview["steps"]], ["pendente"] * 10)
        self.assertEqual(overview["steps"][1]["executes"], ["D6"])

    def test_pln017_closed_finds_the_evidence_and_the_hours(self):
        overview = plan_state.state("PLN-017", root=_paths.ROOT_DIR)
        errors = [(p["code"], p["where"]) for p in overview["problems"] if p["level"] == "erro"]
        self.assertIn(("checked-without-evidence", "P7"), errors)
        self.assertIn(("hours-mismatch", "frontmatter:executed_h"), errors)
        self.assertEqual(len(errors), 2)
        self.assertIsNone(overview["next"])
        self.assertFalse(overview["hours"]["matches"])
        self.assertEqual(overview["hours"]["frontmatter"]["executed_h"], 9.516)
        self.assertEqual(overview["hours"]["summed"]["estimate_h"], 34.75)
        self.assertTrue(all(p["state"] == "feito" for p in overview["steps"]))
        # a P7 é a única `[x]` sem evidência válida
        self.assertEqual([p["id"] for p in overview["steps"] if not p["evidence"]], ["P7"])

    def test_cli_exit_codes_in_real(self):
        pln21 = os.path.join(_paths.ROOT_DIR, "plans", "PLN-021-o-plano-coordenado-e-os-artboards", "PLN-021-plan.md")
        pln17 = os.path.join(_paths.ROOT_DIR, "plans", "PLN-017-a-reuniao-multiagente-como-fluxo-replicavel", "PLN-017-plan.md")
        self.assertEqual(self.cli(pln21)[0], 0)
        self.assertEqual(self.cli(pln17)[0], 1)
        rc, out, _ = self.cli(pln21, "--json")
        self.assertEqual(json.loads(out)["next"], "P1")
        rc, out, _ = self.cli(pln21, "--next")
        self.assertEqual((rc, out.split(" —")[0]), (0, "P1"))
        self.assertEqual(self.cli("PLN-999-que-nao-existe")[0], 2)
        self.assertEqual(self.cli()[0], 2)


class Codes(Base):
    def test_clean(self):
        overview = self.state(plan(step("P1", estimate="5") , ROUND1), design=DESIGN)
        self.assertEqual(overview["problems"], [])

    def test_checked_without_evidence_without_evidence(self):
        overview = self.state(plan(step(checks="- [x] **1. A**", exe="1 h", estimate="5"), ROUND1, rest="0", exe="1"), design=DESIGN)
        self.assertIn("checked-without-evidence", code_list(overview))

    def test_checked_without_evidence_evidence_empty_of_proof(self):
        overview = self.state(plan(step(checks="- [x] **1. A**", exe="1 h", estimate="5",
                                      evidence="feito, confia"), ROUND1, rest="0", exe="1"), design=DESIGN)
        self.assertIn("checked-without-evidence", code_list(overview))

    def test_evidence_with_commit_command_or_file_line_counts(self):
        for ev in ("`brza-workspace@bf06d0a`", "`pytest` → 3 OK", "`scripts/x.py:42` muda o que o D pede"):
            overview = self.state(plan(step(checks="- [x] **1. A**", exe="1 h", estimate="5", evidence=ev), ROUND1,
                                    rest="0", exe="1"), design=DESIGN)
            self.assertNotIn("checked-without-evidence", code_list(overview), ev)

    def test_id_with_underscore_is_not_commit(self):
        overview = self.state(plan(step(checks="- [x] **1. A**", exe="1 h", estimate="5", evidence="o run run_fe70b351bc36 rodou"),
                                ROUND1, rest="0", exe="1"), design=DESIGN)
        self.assertIn("checked-without-evidence", code_list(overview))

    def test_checked_without_executed(self):
        overview = self.state(plan(step(checks="- [x] **1. A**", exe="— h", estimate="5", evidence=EV), ROUND1, rest="0", exe="0"),
                          design=DESIGN)
        self.assertEqual(code_list(overview), ["checked-without-executed"])

    def test_executed_in_text_counts_as_filled(self):
        overview = self.state(plan(step(checks="- [x] **1. A**", exe="incluído nas 1,1 h agregadas", estimate="5", evidence=EV),
                                ROUND1, rest="0", exe="0"), design=DESIGN)
        self.assertNotIn("checked-without-executed", code_list(overview))

    def test_hours_mismatch(self):
        overview = self.state(plan(step(estimate="5"), ROUND1, estimate="9", exe="0", rest="5"), design=DESIGN)
        self.assertEqual(code_list(overview), ["hours-mismatch"])
        self.assertFalse(overview["hours"]["matches"])
        self.assertEqual(overview["hours"]["summed"], {"estimate_h": 5.0, "executed_h": 0.0, "remaining_h": 5.0})

    def test_discarded_exits_of_sums(self):
        steps = step("P1", estimate="2", exe="1 h", checks="- [x] **1. A**", evidence=EV) + \
            step("P2", executes="Executa D2", estimate="3", checks="- [-] **1. A** — descartado porque o D mudou") + \
            step("P3", executes="Executa D2", estimate="4")
        overview = self.state(plan(steps, ROUND1, estimate="6", exe="1", rest="4"), design=DESIGN)
        self.assertEqual(overview["problems"], [])
        self.assertEqual([p["state"] for p in overview["steps"]], ["feito", "descartado", "pendente"])
        self.assertEqual(overview["next"], "P3")

    def test_step_without_design(self):
        overview = self.state(plan(step("P1", executes="Executor: a sessão"), ROUND1), design=DESIGN)
        self.assertEqual(code_list(overview), ["step-without-design"])

    def test_step_without_design_exempt_round_review_closing_and_request(self):
        steps = step("P1", title="A rodada de decisão", executes="Executa a rodada", estimate="1") + \
            step("P2", title="O aceite", executes="Executa os `C`", estimate="1") + \
            step("P3", title="Passo a pedido", executes="Executa a pedido de Anderson", estimate="1") + \
            step("P4", title="O fechamento", executes="Executa o fechamento", estimate="1") + \
            step("P5", title="A revisão da entrega", executes="Executa a revisão", estimate="1")
        overview = self.state(plan(steps, ROUND1, estimate="5", rest="5"), design=DESIGN)
        self.assertEqual(overview["problems"], [])

    def test_without_design_not_requires_executes_d(self):
        overview = self.state(plan(step("P1", executes="Executor: a sessão"), ROUND1))
        self.assertEqual(overview["problems"], [])

    def test_step_cites_unknown_design(self):
        overview = self.state(plan(step("P1", executes="Executa D1, D9"), ROUND1), design=DESIGN)
        self.assertEqual(code_list(overview), ["step-cites-unknown-design"])

    def test_design_without_origin(self):
        d = DESIGN.replace("- **Origem:** R1.1\n", "")
        overview = self.state(plan(step("P1"), ROUND1), design=d)
        self.assertEqual(code_list(overview), ["design-without-origin"])
        self.assertEqual(overview["problems"][0]["where"], "D2")

    def test_origin_unknown_round(self):
        d = DESIGN.replace("R1.1, R1.2", "R1.1, R7.3")
        overview = self.state(plan(step("P1"), ROUND1), design=d)
        self.assertEqual(code_list(overview), ["origin-unknown-round"])
        self.assertIn("R7.3", overview["problems"][0]["msg"])

    def test_origin_only_with_round_without_question(self):
        d = DESIGN.replace("R1.1, R1.2", "R1")
        self.assertEqual(self.state(plan(step("P1"), ROUND1), design=d)["problems"], [])
        d = DESIGN.replace("R1.1, R1.2", "R5")
        self.assertEqual(code_list(self.state(plan(step("P1"), ROUND1), design=d)), ["origin-unknown-round"])

    def test_deviation_not_cited(self):
        deviations = "## Desvios\n\n- **X1 — O que mudou.** Por quê, e nada mais.\n"
        overview = self.state(plan(step("P1"), ROUND1, deviations=deviations), design=DESIGN)
        self.assertEqual(code_list(overview), ["deviation-not-cited"])
        self.assertEqual(overview["problems"][0]["level"], "aviso")

    def test_deviation_cited_by_step_or_naming_the_step(self):
        deviations = "## Desvios\n\n- **X1 — O que mudou.** Afeta P1.\n- **X2 — Outro.** Sem passo.\n"
        extra = step("P1") .replace("- [ ] **1. A**", "- [ ] **1. A** (o X2 entra aqui)")
        overview = self.state(plan(extra, ROUND1, deviations=deviations), design=DESIGN)
        self.assertEqual(overview["problems"], [])

    def test_duplicate_id(self):
        overview = self.state(plan(step("P1") + step("P1"), ROUND1, estimate="5", rest="5"), design=DESIGN)
        self.assertIn("duplicate-id", code_list(overview))
        d = DESIGN + "\n### D1 — Repetido\n\n- **Origem:** R1.1\n"
        overview = self.state(plan(step("P1"), ROUND1), design=d)
        self.assertEqual(code_list(overview), ["duplicate-id"])
        overview = self.state(plan(step("P1"), ROUND1 + "\n" + ROUND1), design=DESIGN)
        self.assertIn("duplicate-id", code_list(overview))

    def test_alternative_repeated_in_other_d_is_not_duplicate(self):
        d = DESIGN + "\n#### As alternativas\n\n##### A1 — Mais uma\n"
        overview = self.state(plan(step("P1"), ROUND1), design=d)
        self.assertEqual(overview["problems"], [])
        self.assertIn("D2/A1", overview["ids"]["A"])

    def test_next_respects_depends_on(self):
        steps = step("P1", estimate="1", executes="Executa D1") + \
            step("P2", estimate="1", executes="Executa D1 · depende de P3") + step("P3", estimate="1", executes="Executa D1")
        overview = self.state(plan(steps, ROUND1, estimate="3", rest="3"), design=DESIGN)
        self.assertEqual(overview["next"], "P1")


class Fix(Base):
    def test_fix_rewrites_only_the_three_hours(self):
        txt = plan(step(estimate="2,5") + step("P2", estimate="1,5"), ROUND1, estimate="9", exe="9", rest="9")
        root, path = self.build(txt, design=DESIGN)
        rc, out, err = self.cli(path, "--fix")
        self.assertEqual(rc, 0, out)
        with open(path, encoding="utf-8") as f:
            fresh = f.read()
        self.assertIn("estimate_h: 4\n", fresh)
        self.assertIn("executed_h: 0\n", fresh)
        self.assertIn("remaining_h: 4\n", fresh)
        lines_before = [l for l in txt.split("\n") if not l.startswith(("estimate_h", "executed_h", "remaining_h"))]
        lines_after = [l for l in fresh.split("\n") if not l.startswith(("estimate_h", "executed_h", "remaining_h"))]
        self.assertEqual(lines_before, lines_after)

    def test_fix_appends_a_key_missing(self):
        fm = "---\nstatus: open\nphase: design\nready: sim\n---\n"
        root, path = self.build(plan(step(estimate="2"), ROUND1, fm=fm), design=DESIGN)
        self.cli(path, "--fix")
        fmt = plan_md.load(path).fm
        self.assertEqual((fmt["estimate_h"], fmt["executed_h"], fmt["remaining_h"]), ("2", "0", "2"))
        self.assertEqual(plan_state.state(path)["problems"], [])

    def test_strict_and_warnings(self):
        deviations = "## Desvios\n\n- **X1 — O que mudou.** Nada.\n"
        root, path = self.build(plan(step("P1"), ROUND1, deviations=deviations), design=DESIGN)
        self.assertEqual(self.cli(path)[0], 0)
        self.assertEqual(self.cli(path, "--strict")[0], 1)

    def test_next_without_pending(self):
        steps = step("P1", exe="1 h", checks="- [x] **1. A**", evidence=EV)
        root, path = self.build(plan(steps, ROUND1, estimate="2.5", exe="1", rest="0"), design=DESIGN)
        rc, out, _ = self.cli(path, "--next")
        self.assertEqual((rc, out.strip()), (0, "nenhum"))


if __name__ == "__main__":
    unittest.main()
