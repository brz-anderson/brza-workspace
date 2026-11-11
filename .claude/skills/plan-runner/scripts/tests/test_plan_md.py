import os
import shutil
import unittest

import _paths  # noqa: F401
import plan_md
from mini import DESIGN, ROUND1, step, plan


class Hours(unittest.TestCase):
    def test_point_comma_approximate_and_empty(self):
        self.assertEqual(plan_md.parse_hours("11,5 h"), 11.5)
        self.assertEqual(plan_md.parse_hours("11.5 h"), 11.5)
        self.assertEqual(plan_md.parse_hours("~4 h (estimativa de relógio)"), 4.0)
        self.assertEqual(plan_md.parse_hours("0,174 h (janela)"), 0.174)
        self.assertIsNone(plan_md.parse_hours("— h"))
        self.assertIsNone(plan_md.parse_hours(""))
        self.assertIsNone(plan_md.parse_hours("incluído nas 1,109 h agregadas"))

    def test_format(self):
        self.assertEqual(plan_md.format_hours(41.0), "41")
        self.assertEqual(plan_md.format_hours(34.75), "34.75")
        self.assertEqual(plan_md.format_hours(9.5160000001), "9.516")


class RealPlans(unittest.TestCase):
    def test_resolve_pln_by_root_and_joins_the_design(self):
        pl = plan_md.load("PLN-021", root=_paths.ROOT_DIR)
        self.assertEqual(pl.id, "PLN-021")
        self.assertEqual([a.name for a in pl.files], ["PLN-021-plan.md", "PLN-021-design.md"])
        self.assertTrue(pl.is_split())
        self.assertEqual(pl.fm["phase"], "execution")
        self.assertEqual(pl.fm["scope"], ["workspace"])

    def test_ids_of_pln021(self):
        ids = plan_md.load("PLN-021", root=_paths.ROOT_DIR).ids()
        self.assertEqual(ids["P"], ["P%d" % i for i in range(1, 11)])
        self.assertEqual(ids["D"], ["D%d" % i for i in range(1, 8)])
        self.assertEqual(ids["X"], ["X1"])
        self.assertEqual(len(ids["R"]), 20)  # R1:4 R2:4 R3:3 R4:9
        self.assertIn("R4.9", ids["R"])
        self.assertIn("D3/A1", ids["A"])

    def test_steps_of_pln021(self):
        pl = plan_md.load("PLN-021", root=_paths.ROOT_DIR)
        p2 = pl.step("P2")
        self.assertEqual(p2.executes, ["D6"])
        self.assertEqual(p2.estimated_h, 11.5)
        self.assertIsNone(p2.executed_h)
        self.assertFalse(p2.executed_filled)
        self.assertEqual(p2.state, "pendente")
        self.assertEqual(pl.step("P3").depends, ["P1", "P2"])
        self.assertEqual(pl.step("P8").depends, ["P1", "P2", "P3", "P4", "P5", "P6", "P7"])

    def test_pln017_closed_with_evidence(self):
        pl = plan_md.load("PLN-017", root=_paths.ROOT_DIR)
        ids = [p.id for p in pl.steps()]
        self.assertEqual(ids, ["P1", "P2", "P3", "P4a", "P4b", "P5", "P6", "P7", "P8"])
        self.assertTrue(all(p.state == "feito" for p in pl.steps()))
        self.assertEqual(pl.step("P1").estimated_h, 10.5)
        self.assertEqual(pl.step("P1").executed_h, 4.0)
        self.assertIn("bf06d0a", pl.step("P1").evidence)
        self.assertIsNone(pl.step("P4a").executed_h)
        self.assertTrue(pl.step("P4a").executed_filled)
        self.assertEqual(len(pl.rounds()), 10)
        self.assertEqual(pl.round(8).questions[0].k, 1)  # a pergunta única de `**Pergunta:**`

    def test_questions_is_decided_literal_reopened(self):
        pl = plan_md.load("PLN-021", root=_paths.ROOT_DIR)
        q = pl.question_text("R1.2")
        self.assertTrue(q.is_decided)
        self.assertEqual(q.reopened, "R3.1")
        self.assertEqual([o["recommended"] for o in q.option_list()], [True, False, False])
        q = pl.question_text("R2.1")
        self.assertIn("pasta script/ em .claude/", q.answer)
        self.assertFalse(q.is_decided)
        self.assertTrue(pl.round(4).unanswered)


class MiniPlan(unittest.TestCase):
    def setUp(self):
        self.dirs = []

    def tearDown(self):
        for d in self.dirs:
            shutil.rmtree(d, ignore_errors=True)

    def build(self, *a, **k):
        root, path = _paths.plan_tmp(*a, **k)
        self.dirs.append(root)
        return root, path

    def test_answer_with_a_reading_counts_and_counterproposal_does_not(self):
        multiple = ROUND1 + """
3. **Escolhas menores** (seleção múltipla). Opções:
   - a (recomendada);
   - b.

   **Resposta:** "restante recomendado" Lida como: a e b.
"""
        root, path = self.build(plan(step(), multiple), design=DESIGN)
        pl = plan_md.load(path)
        self.assertTrue(pl.question_text("R1.2").is_decided)       # `Resposta:` com "lida como a primeira opção"
        self.assertTrue(pl.question_text("R1.3").is_decided)       # seleção múltipla em texto livre
        against = multiple.replace("lida como a primeira opção.", "Lida como contraproposta: foi à rodada 2.")
        root, path = self.build(plan(step(), against), design=DESIGN)
        self.assertFalse(plan_md.load(path).question_text("R1.2").is_decided)

    def test_heading_in_fence_does_not_count(self):
        root, path = self.build(plan(step(), ROUND1), design=DESIGN)
        pl = plan_md.load(path)
        self.assertEqual([d["id"] for d in pl.design_list()], ["D1", "D2"])
        self.assertFalse([s for s in pl.all_sections() if "isto não é heading" in s.title])

    def test_origin_and_alternatives(self):
        root, path = self.build(plan(step(), ROUND1), design=DESIGN)
        d = plan_md.load(path).design_text("D1")
        self.assertEqual(d["origin_ids"], ["R1.1", "R1.2"])
        self.assertEqual(d["alternatives"], ["A1", "A2"])

    def test_pln_without_root_climbs_until_plans(self):
        root, path = self.build(plan(step(), ROUND1))
        pl = plan_md.load("PLN-900", root=root)
        self.assertEqual(os.path.realpath(pl.path), os.path.realpath(path))
        with self.assertRaises(plan_md.PlanNotFound):
            plan_md.load("PLN-901", root=root)

    def test_hours_with_point_comma_and_empty(self):
        root, path = self.build(plan(step("P1", estimate="2,5") + step("P2", estimate="1.5", exe="— h")))
        ps = plan_md.load(path).steps()
        self.assertEqual([p.estimated_h for p in ps], [2.5, 1.5])
        self.assertEqual([p.executed_h for p in ps], [None, None])

    def test_interview_split(self):
        root, path = self.build(plan(step()).replace("## Entrevista\n", ""), interview="# PLN-900 — Entrevista\n\n" + ROUND1.replace("###", "##"))
        pl = plan_md.load(path)
        self.assertEqual([a.role for a in pl.files], ["plan", "interview"])
        self.assertEqual(pl.round_ids(), ["R1.1", "R1.2"])

    def test_questions_explicit(self):
        inter = ("# PLN-900 — Entrevista\n\n## Rodada 2 — o cliente (preparada 2026-11-09, não enviada)\n\n"
                 "**R2.1. Onde mora?**\n\n1. **Módulo (Recomendado).** Custo: um.\n2. **Só o verbo.** Custo: dois.\n\n"
                 "**R2.2. Quanto tempo?**\n\n1. **90 dias.** Custo: x.\n")
        root, path = self.build(plan(step()).replace("## Entrevista\n", ""), interview=inter)
        self.assertEqual(plan_md.load(path).round_ids(), ["R2.1", "R2.2"])


if __name__ == "__main__":
    unittest.main()
