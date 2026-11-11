import io
import json
import os
import shutil
import unittest
from contextlib import redirect_stderr, redirect_stdout

import _paths  # noqa: F401
import close_check
from mini import DESIGN, ROUND1, step, plan

EV = "`brza-workspace@a1b2c3d` · `python3 -m unittest` → 12 OK"
DONE_STATE = step("P1", estimate="5", exe="1 h", checks="- [x] **1. A**", evidence=EV)
FM_CLOSED = "---\nstatus: done\nphase: closed\nready: sim\nestimate_h: 5\nexecuted_h: 1\nremaining_h: 0\n---\n"


def note(status="done", h1="# Uma nota"):
    return "---\nstatus: %s\n---\n\n%s\n" % (status, h1)


def reviewed(*findings, name="REV-900"):
    t = "---\nstatus: done\n---\n\n# %s: o parecer\n\n" % name
    for a in findings:
        t += a + "\n\n"
    return t


class Base(unittest.TestCase):
    def setUp(self):
        self.dirs = []

    def tearDown(self):
        for d in self.dirs:
            shutil.rmtree(d, ignore_errors=True)

    def check(self, text, **k):
        root, path = _paths.plan_tmp(text, **k)
        self.dirs.append(root)
        return close_check.check(path), path

    def res(self, r):
        return {i["item"]: i["result"] for i in r["items"]}

    def cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = close_check.main(list(args))
        return rc, out.getvalue(), err.getvalue()


class Items(Base):
    def test_plan_closed_clean(self):
        r, _ = self.check(plan(DONE_STATE, ROUND1, fm=FM_CLOSED), design=DESIGN)
        # R1.1 e R1.2 estão na Origem de algum D: nada a levar à casa dona
        self.assertEqual(self.res(r), {1: "ok", 2: "ok", 3: "ok", 4: "ok", 5: "n/a", 6: "n/a"})
        self.assertTrue(r["clean"])

    def test_item1_step_pending_and_without_evidence(self):
        r, _ = self.check(plan(step("P1") + step("P2", checks="- [x] **1. A**", exe="1 h", estimate="5"), ROUND1,
                                  estimate="10", exe="1", rest="5"), design=DESIGN)
        self.assertEqual(self.res(r)[1], "falta")
        det = " ".join(r["items"][0]["detail"])
        self.assertIn("P1: pendente", det)
        self.assertIn("P2", det)
        self.assertFalse(r["clean"])

    def test_item1_discarded_requires_reason(self):
        absent = step("P1", checks="- [-] **1. A**")
        present = step("P1", checks="- [-] **1. A** — descartado porque o D1 mudou na R3")
        self.assertEqual(self.res(self.check(plan(absent, ROUND1, estimate="5", rest="0"), design=DESIGN)[0])[1], "falta")
        self.assertEqual(self.res(self.check(plan(present, ROUND1, estimate="5", rest="0"), design=DESIGN)[0])[1], "ok")

    def test_item1_without_steps(self):
        r, _ = self.check(plan("", ROUND1, fm=FM_CLOSED))
        self.assertEqual(self.res(r)[1], "falta")

    def test_item2_targets(self):
        review = reviewed(
            "### A1 — Corrige o que quebra\n\n> bug · importante · confiança 90 · → corrigido aqui\n\n**Evidência:** `a.py:1`",
            "### A2 — Vai a issue que existe\n\n> bug · sugestão · confiança 90 · → issue a-issue-boa\n\n**Evidência:** `a.py:2`",
            "### A3 — Falso\n\n> bug · importante · confiança 95 · → falso\n\n**Por que é falso:** x.",
            "### A4 — Título → descartado, por custo\n\n**Evidência:** `a.py:4`")
        rev = "\n## Revisões\n\n- [REV-900: o parecer](../../work/reviews/REV-900-p.md) — 2026-11-10, 4 achados.\n"
        extra = {"work/reviews/REV-900-p.md": review, "work/issues/a-issue-boa.md": note("open")}
        r, _ = self.check(plan(DONE_STATE, ROUND1, fm=FM_CLOSED, extra=rev), design=DESIGN, extra=extra)
        self.assertEqual(self.res(r)[2], "ok", r["items"][1])

    def test_item2_a_define_and_target_that_not_exists(self):
        review = reviewed(
            "### A1 — Sem destino\n\n> bug · importante · confiança 90 · → a definir\n\n**Evidência:** `a.py:1`",
            "### A2 — Issue fantasma\n\n> bug · sugestão · confiança 90 · → issue nao-existe\n\n**Evidência:** `a.py:2`",
            "### A3 — Sem a linha\n\n**Evidência:** `a.py:3`")
        rev = "\n## Revisões\n\n- [REV-900: o parecer](../../work/reviews/REV-900-p.md) — 2026-11-10.\n"
        r, _ = self.check(plan(DONE_STATE, ROUND1, fm=FM_CLOSED, extra=rev), design=DESIGN,
                            extra={"work/reviews/REV-900-p.md": review})
        self.assertEqual(self.res(r)[2], "falta")
        det = r["items"][1]["detail"]
        self.assertEqual(len(det), 3)
        self.assertTrue(any("A1" in d and "a definir" in d for d in det))
        self.assertTrue(any("A2" in d and "nao-existe" in d for d in det))
        self.assertTrue(any("A3" in d for d in det))

    def test_item2_review_that_not_exists(self):
        rev = "\n## Revisões\n\n- [REV-900: o parecer](../../work/reviews/REV-900-p.md) — 2026-11-10.\n"
        r, _ = self.check(plan(DONE_STATE, ROUND1, fm=FM_CLOSED, extra=rev), design=DESIGN)
        self.assertEqual(self.res(r)[2], "falta")

    def test_item3_is_decided_without_d_nor_link_and_manual(self):
        # a R1.1 foi decidida e nenhum D a cita; a R1.2 é resposta literal, e o D a cita
        d = DESIGN.replace("R1.1, R1.2", "R1.2").replace("- **Origem:** R1.1\n", "- **Origem:** R1.2\n")
        r, _ = self.check(plan(DONE_STATE, ROUND1, fm=FM_CLOSED), design=d)
        self.assertEqual(self.res(r)[3], "manual")
        self.assertEqual([c.split(" —")[0] for c in r["items"][2]["detail"]], ["R1.1"])

    def test_item3_counts_a_free_text_answer_read_as_an_option(self):
        # A10: a R1.2 foi respondida por `Resposta:` com a leitura; sem D nem link, também vai ao Retomar
        d = DESIGN.replace("R1.1, R1.2", "R1.1")
        r, _ = self.check(plan(DONE_STATE, ROUND1, fm=FM_CLOSED), design=d)
        self.assertEqual([c.split(" —")[0] for c in r["items"][2]["detail"]], ["R1.2"])

    def test_item3_counterproposal_does_not_count(self):
        round_text = ROUND1.replace('lida como a primeira opção.', 'Lida como contraproposta: foi à rodada 2.')
        d = DESIGN.replace("R1.1, R1.2", "R1.1")
        r, _ = self.check(plan(DONE_STATE, round_text, fm=FM_CLOSED), design=d)
        self.assertEqual(self.res(r)[3], "ok")

    def test_item3_link_in_decisions_covers(self):
        d = DESIGN.replace("R1.1, R1.2", "R1.2").replace("- **Origem:** R1.1\n", "- **Origem:** R1.2\n")
        dec = "\n## Decisões\n\n- [Uma nota](../../work/decisions/uma.md) — R1.1, `done`.\n"
        r, _ = self.check(plan(DONE_STATE, ROUND1, fm=FM_CLOSED, extra=dec), design=d,
                            extra={"work/decisions/uma.md": note("done")})
        self.assertEqual(self.res(r)[3], "ok")

    def test_item4_decisions_done(self):
        dec = "\n## Decisões\n\n- [A boa](../../work/decisions/a.md) — R1.1, `done`.\n- [A aberta](../../work/decisions/b.md) — R1.2.\n"
        extra = {"work/decisions/a.md": note("done"), "work/decisions/b.md": note("proposed")}
        r, _ = self.check(plan(DONE_STATE, ROUND1, fm=FM_CLOSED, extra=dec), design=DESIGN, extra=extra)
        self.assertEqual(self.res(r)[4], "falta")
        self.assertEqual(len(r["items"][3]["detail"]), 1)
        self.assertIn("b.md", r["items"][3]["detail"][0])
        dec2 = "\n## Decisões\n\n- [A boa](../../work/decisions/a.md) — R1.1, `done`.\n- [Fantasma](../../work/decisions/z.md).\n"
        r, _ = self.check(plan(DONE_STATE, ROUND1, fm=FM_CLOSED, extra=dec2), design=DESIGN, extra=extra)
        self.assertEqual(self.res(r)[4], "falta")

    def test_item5_commit_of_studio_and_manual(self):
        ev = "`brza-studio@a1b2c3d` · `pnpm test` → 12 OK"
        p = step("P1", estimate="5", exe="1 h", checks="- [x] **1. A**", evidence=ev)
        r, _ = self.check(plan(p, ROUND1, fm=FM_CLOSED), design=DESIGN)
        self.assertEqual(self.res(r)[5], "manual")
        r, _ = self.check(plan(DONE_STATE, ROUND1, fm=FM_CLOSED), design=DESIGN)
        self.assertEqual(self.res(r)[5], "n/a")

    def test_item6_window(self):
        absent = "\n## Janela\n\n- **Janela e meta:** de 2026-11-09 a 2026-11-12; o painel publica sozinho.\n- **Cortes previstos:** o P9.\n"
        present = absent + "- **Fecho:** a meta foi cumprida em 2026-11-11; `executed_h` 1 contra `estimate_h` 5.\n"
        r, _ = self.check(plan(DONE_STATE, ROUND1, fm=FM_CLOSED, extra=absent), design=DESIGN)
        self.assertEqual(self.res(r)[6], "falta")
        r, _ = self.check(plan(DONE_STATE, ROUND1, fm=FM_CLOSED, extra=present), design=DESIGN)
        self.assertEqual(self.res(r)[6], "ok")
        not_ = absent + "A meta não foi cumprida: o P9 ficou de fora.\n"
        r, _ = self.check(plan(DONE_STATE, ROUND1, fm=FM_CLOSED, extra=not_), design=DESIGN)
        self.assertEqual(self.res(r)[6], "ok")


class Cli(Base):
    def test_exit_0_with_manual_and_1_with_missing_ids(self):
        root, path = _paths.plan_tmp(plan(DONE_STATE, ROUND1, fm=FM_CLOSED), design=DESIGN)
        self.dirs.append(root)
        rc, out, _ = self.cli(path)
        self.assertEqual(rc, 0)
        self.assertIn("fechamento: pode seguir", out)
        root, path = _paths.plan_tmp(plan(step("P1"), ROUND1), design=DESIGN)
        self.dirs.append(root)
        rc, out, _ = self.cli(path, "--json")
        self.assertEqual(rc, 1)
        self.assertFalse(json.loads(out)["clean"])

    def test_pln021_real_open_blocks(self):
        rc, out, _ = self.cli(os.path.join(_paths.ROOT_DIR, "plans", "PLN-021-o-plano-coordenado-e-os-artboards", "PLN-021-plan.md"))
        self.assertEqual(rc, 1)
        self.assertIn("P1: pendente", out)

    def test_pln017_real(self):
        rc, out, _ = self.cli(os.path.join(_paths.ROOT_DIR, "plans", "PLN-017-a-reuniao-multiagente-como-fluxo-replicavel", "PLN-017-plan.md"), "--json")
        r = json.loads(out)
        self.assertEqual(rc, 1)
        res = {i["item"]: i["result"] for i in r["items"]}
        self.assertEqual(res[1], "falta")  # a evidência da P7 não traz commit, `→` nem arquivo:linha
        self.assertEqual(res[4], "ok")
        self.assertEqual(res[5], "n/a")
        self.assertEqual(res[6], "n/a")

    def test_usage(self):
        self.assertEqual(self.cli()[0], 2)
        self.assertEqual(self.cli("PLN-999-nao-existe")[0], 2)


if __name__ == "__main__":
    unittest.main()
