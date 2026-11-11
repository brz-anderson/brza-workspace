import io
import json
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

import _paths  # noqa: F401
import plan_md
import plan_state
import round_log
from mini import DESIGN, ROUND1, step, plan

PLN21 = os.path.join("plans", "PLN-021-o-plano-coordenado-e-os-artboards", "PLN-021-plan.md")


def round(**k):
    d = {
        "title": "o P2 volta com desvios", "sent_on": "2026-11-10",
        "presented_before": "O implementer devolveu o P2.\nTrês desvios.",
        "answered": {"data": "2026-11-10", "session": "a sessão do workstream playground"},
        "questions": [{
            "topic": "O commit do executor", "multiple": False,
            "options": [
                {"label": "o pedido autoriza o commit na branch do passo", "recommended": True,
                 "cost": "muda a regra de hoje", "pays_when": "em todo passo"},
                {"label": "o executor para antes do commit", "cost": "uma rodada por passo", "pays_when": "agora"},
            ],
            "answer": {"chosen": [0], "literal": None}, "reopens": None,
        }],
    }
    d.update(k)
    return d


class Base(unittest.TestCase):
    def setUp(self):
        self.dirs = []

    def tearDown(self):
        for d in self.dirs:
            shutil.rmtree(d, ignore_errors=True)

    def copy(self):
        r = _paths.copy_root()
        self.dirs.append(os.path.dirname(r))
        return r, os.path.join(r, PLN21)

    def build(self, *a, **k):
        root, path = _paths.plan_tmp(*a, **k)
        self.dirs.append(root)
        return root, path

    def json(self, payload):
        d = tempfile.mkdtemp(prefix="rl-")
        self.dirs.append(d)
        p = os.path.join(d, "rodada.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)
        return p

    def cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = round_log.main(list(args) + ["--no-panel"])
        return rc, out.getvalue(), err.getvalue()

    def read_text(self, path):
        with open(path, encoding="utf-8") as f:
            return f.read()


class NextRound(Base):
    def test_next(self):
        root, path = self.copy()
        rc, out, _ = self.cli(path, "--next")
        self.assertEqual((rc, out.strip()), (0, "5"))

    def test_next_without_round(self):
        root, path = self.build(plan(step(), ""))
        self.assertEqual(self.cli(path, "--next")[1].strip(), "1")


class WritesRound(Base):
    def test_is_decided_appends_at_the_end_of_interview(self):
        root, path = self.copy()
        before = self.read_text(path)
        rc, out, err = self.cli(path, "--from", self.json(round()))
        self.assertEqual(rc, 0, err)
        self.assertEqual(os.path.realpath(out.strip()), os.path.realpath(path))
        fresh = self.read_text(path)
        self.assertIn("### Rodada 5 — o P2 volta com desvios (enviada 2026-11-10)", fresh)
        self.assertIn("> **Apresentado antes:** O implementer devolveu o P2.\n> Três desvios.", fresh)
        self.assertIn("Respondida em 2026-11-10, na sessão do workstream playground.", fresh)
        self.assertIn("1. **O commit do executor.** Opções:", fresh)
        self.assertIn("   - o pedido autoriza o commit na branch do passo (recomendada) — custo: muda a regra de hoje; "
                      "se paga: em todo passo;", fresh)
        self.assertIn("   - o executor para antes do commit — custo: uma rodada por passo; se paga: agora.", fresh)
        self.assertIn("   **Decidido — o pedido autoriza o commit na branch do passo.**", fresh)
        # a rodada entra antes de `## Passos`, e o resto do arquivo não muda
        self.assertLess(fresh.index("### Rodada 5"), fresh.index("\n## Passos\n"))
        self.assertGreater(fresh.index("### Rodada 5"), fresh.index("### Rodada 4"))
        added_lines = [l for l in fresh.split("\n") if l not in before.split("\n")]
        self.assertTrue(all(l.strip() == "" or "Rodada 5" in l or l.startswith(("> ", "Respondida", "1. ", "   ")) for l in added_lines))
        # relê como rodada decidida
        pl = plan_md.load(path)
        q = pl.question_text("R5.1")
        self.assertTrue(q.is_decided)
        self.assertEqual(q.topic, "O commit do executor")
        self.assertEqual([o["recommended"] for o in q.option_list()], [True, False])
        self.assertEqual(plan_state.state(path)["problems"], [])

    def test_literal_goes_as_answer_with_a_reading(self):
        root, path = self.copy()
        d = round()
        d["questions"][0]["answer"] = {"chosen": None, "literal": "para antes do commit, sempre"}
        self.cli(path, "--from", self.json(d))
        q = plan_md.load(path).question_text("R5.1")
        self.assertFalse(q.is_decided)
        self.assertIn('**Resposta:** "para antes do commit, sempre"', q.answer)

    def test_literal_with_chosen_is_read_as(self):
        root, path = self.copy()
        d = round()
        d["questions"][0]["answer"] = {"chosen": [1], "literal": "a segunda"}
        self.cli(path, "--from", self.json(d))
        q = plan_md.load(path).question_text("R5.1")
        self.assertIn('"a segunda" Lida como: o executor para antes do commit.', q.answer)
        self.assertIsNone(q.decided_line)

    def test_without_answer(self):
        root, path = self.copy()
        d = round(answered=None)
        d["questions"][0]["answer"] = None
        self.cli(path, "--from", self.json(d))
        pl = plan_md.load(path)
        self.assertTrue(pl.round(5).unanswered)
        self.assertFalse(pl.question_text("R5.1").is_decided)

    def test_multiple(self):
        root, path = self.copy()
        d = round()
        d["questions"][0]["multiple"] = True
        d["questions"][0]["answer"] = {"chosen": [0, 1], "literal": None}
        self.cli(path, "--from", self.json(d))
        fresh = self.read_text(path)
        self.assertIn("1. **O commit do executor** (seleção múltipla). Opções:", fresh)
        self.assertIn("**Decidido — o pedido autoriza o commit na branch do passo; o executor para antes do commit.**", fresh)

    def test_reopens_marks_a_line_old(self):
        root, path = self.copy()
        d = round()
        d["questions"][0]["reopens"] = "R1.2"
        rc, out, err = self.cli(path, "--from", self.json(d))
        self.assertEqual(rc, 0, err)
        pl = plan_md.load(path)
        self.assertEqual(pl.question_text("R1.2").reopened, "R3.1")  # a R1.2 já estava reaberta em R3.1: a marca nova vai junto
        self.assertIn("**→ reaberta em R5.1**", pl.question_text("R1.2").block)
        lines = [l for l in self.read_text(path).split("\n") if "reaberta em R5.1" in l]
        self.assertEqual(len(lines), 1)
        self.assertTrue(lines[0].lstrip().startswith("**Decidido — protótipo no playground.**"))

    def test_reopens_without_line_decided_line_goes_in_last_line(self):
        root, path = self.copy()
        d = round()
        d["questions"][0]["reopens"] = "R4.1"  # a R4.1 não tem Decidido
        self.cli(path, "--from", self.json(d))
        q = plan_md.load(path).question_text("R4.1")
        self.assertIn("reaberta em R5.1", q.block)
        self.assertEqual(q.reopened, "R5.1")
        self.assertEqual(plan_md.load(path).question_text("R4.2").reopened, None)

    def test_dry_run_not_writes(self):
        root, path = self.copy()
        before = self.read_text(path)
        d = round()
        d["questions"][0]["reopens"] = "R1.2"
        rc, out, err = self.cli(path, "--from", self.json(d), "--dry-run")
        self.assertEqual(rc, 0, err)
        self.assertEqual(self.read_text(path), before)
        self.assertIn("# dry-run: Rodada 5", out)
        self.assertIn("### Rodada 5 — o P2 volta com desvios", out)
        self.assertIn("# marcaria R1.2 com `→ reaberta em R5.1`", out)

    def test_two_consecutive_records_number_up_to_6(self):
        root, path = self.copy()
        self.cli(path, "--from", self.json(round()))
        self.cli(path, "--from", self.json(round(title="a segunda")))
        pl = plan_md.load(path)
        self.assertEqual([r.n for r in pl.rounds()], [1, 2, 3, 4, 5, 6])
        self.assertEqual(plan_state.state(path)["problems"], [])

    def test_plan_split_writes_in_the_interview(self):
        inter = "# PLN-900 — Entrevista\n\n" + ROUND1.replace("###", "##") + "\n"
        root, path = self.build(plan(step()).replace("## Entrevista\n", ""), interview=inter)
        folder = os.path.dirname(path)
        before_plan = self.read_text(path)
        d = round(title="a nova")
        d["questions"][0]["reopens"] = "R1.1"
        rc, out, err = self.cli(path, "--from", self.json(d))
        self.assertEqual(rc, 0, err)
        self.assertEqual(self.read_text(path), before_plan)
        interview_path = os.path.join(folder, "PLN-900-interview.md")
        self.assertEqual(os.path.realpath(out.strip()), os.path.realpath(interview_path))
        fresh = self.read_text(interview_path)
        self.assertIn("## Rodada 2 — a nova (enviada 2026-11-10)", fresh)
        self.assertTrue(fresh.endswith("\n"))
        pl = plan_md.load(path)
        self.assertEqual(pl.question_text("R1.1").reopened, "R2.1")

    def test_sent_on_missing_becomes_on_date(self):
        root, path = self.copy()
        d = round()
        d.pop("sent_on")
        self.cli(path, "--from", self.json(d))
        import datetime
        self.assertIn("(enviada %s)" % datetime.date.today().isoformat(), self.read_text(path))


class Shape(Base):
    def cases(self):
        base = round()
        without_title = dict(base, title="")
        without_questions = dict(base, questions=[])
        empty_options = json.loads(json.dumps(base))
        empty_options["questions"][0]["options"] = []
        idx = json.loads(json.dumps(base))
        idx["questions"][0]["answer"] = {"chosen": [5], "literal": None}
        multi = json.loads(json.dumps(base))
        multi["questions"][0]["answer"] = {"chosen": [0, 1], "literal": None}
        reopens = json.loads(json.dumps(base))
        reopens["questions"][0]["reopens"] = "R9.9"
        reopens_bad = json.loads(json.dumps(base))
        reopens_bad["questions"][0]["reopens"] = "a R1"
        data = dict(base, sent_on="ontem")
        resp = dict(base, answered={"data": "x"})
        return {"title": without_title, "questions": without_questions, "options": empty_options, "índice": idx, "multiple": multi,
                "reabre inexistente": reopens, "reabre fora da forma": reopens_bad, "data": data, "answered": resp,
                "não é objeto": ["x"]}

    def test_json_outside_of_shape_exits_1_and_not_writes(self):
        root, path = self.copy()
        before = self.read_text(path)
        for name, payload in self.cases().items():
            rc, out, err = self.cli(path, "--from", self.json(payload))
            self.assertEqual(rc, 1, name)
            self.assertTrue(err.strip(), name)
            self.assertEqual(self.read_text(path), before, name)

    def test_json_unreadable_and_file_missing(self):
        root, path = self.copy()
        d = tempfile.mkdtemp(prefix="rl-")
        self.dirs.append(d)
        bad = os.path.join(d, "ruim.json")
        with open(bad, "w") as f:
            f.write("{nao e json")
        self.assertEqual(self.cli(path, "--from", bad)[0], 1)
        self.assertEqual(self.cli(path, "--from", os.path.join(d, "nao-existe.json"))[0], 1)

    def test_usage(self):
        self.assertEqual(self.cli()[0], 2)
        self.assertEqual(self.cli("PLN-999-que-nao-existe", "--next")[0], 2)

    def test_plan_without_interview_refuses(self):
        root, path = self.build(plan(step()).replace("## Entrevista\n", ""))
        rc, out, err = self.cli(path, "--from", self.json(round()))
        self.assertEqual(rc, 1)
        self.assertIn("Entrevista", err)


if __name__ == "__main__":
    unittest.main()
