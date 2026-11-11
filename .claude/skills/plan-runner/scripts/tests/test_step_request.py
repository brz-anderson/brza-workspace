import io
import os
import shutil
import subprocess
import unittest
from contextlib import redirect_stderr, redirect_stdout

import _paths  # noqa: F401
import plan_md
import step_request
from mini import DESIGN, ROUND1, step, plan


class RequestText(unittest.TestCase):
    def setUp(self):
        self.dirs = []

    def tearDown(self):
        for d in self.dirs:
            shutil.rmtree(d, ignore_errors=True)

    def build(self, *a, **k):
        root, path = _paths.plan_tmp(*a, **k)
        self.dirs.append(root)
        return root, path

    def cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = step_request.main(list(args))
        return rc, out.getvalue(), err.getvalue()

    def test_request_of_p2_of_pln021(self):
        text, info = step_request.build(plan_md.load("PLN-021", root=_paths.ROOT_DIR), "P2", on_date="2026-11-10")
        self.assertTrue(text.startswith("Você executa o passo P2 do PLN-021 numa sessão aberta pela coordenação."))
        heads = [l for l in text.split("\n") if l.startswith("## ")]
        order = ["## O passo", "## O que o Desenho fixou", "## O que as rodadas decidiram", "## Restrições e Regressão",
                 "## Onde trabalhar", "## Regras", "## O fim"]
        self.assertEqual(heads, order)
        self.assertIn("### P2 — Os quatro scripts de R2.2 e o `plan_md.py`", text)
        self.assertIn("Estimado: 11.5 h", text)
        self.assertIn("### D6 — Os quatro scripts de R2.2", text)
        self.assertIn("#### `close_check.py`", text)  # o D inteiro, até o fim
        self.assertNotIn("### D7", text)
        self.assertIn("### R2.2 — Os scripts de apoio", text)
        self.assertIn("- **Escolhida:** os quatro.", text)
        self.assertIn("**O `plan-runner` muda só na branch `workstream/playground`**", text)
        self.assertIn("**A `meeting-runner` faz o mesmo com o `skillkit`.**", text)
        self.assertIn("(branch feat/pln-021-p2)", text)
        self.assertTrue(info["worklog"].endswith("2026-11-10-pln-021-p2-os-quatro-scripts-de-r2-2-e-o-plan-md-py.md"), info["worklog"])
        self.assertEqual(step_request.slug("Uma frase bem comprida que passa do limite de caracteres permitido", 30), "uma-frase-bem-comprida-que")
        self.assertIn("pln-021-p2", info["checkout"])
        self.assertTrue(text.rstrip().endswith("encerramento."))

    def test_the_protocol_of_end(self):
        text, _ = step_request.build(plan_md.load("PLN-021", root=_paths.ROOT_DIR), "P2")
        self.assertIn("1. Preencha `## Evidência` no worklog", text)
        self.assertIn("`commit: brza-studio@<sha7>` (ou `commit: aguarda confirmação`)", text)
        self.assertIn("`<!-- fim-P2: feito -->` ou `<!-- fim-P2: parado -->`", text)
        self.assertIn("Não envie `worker_done`", text)
        self.assertIn("escreva a forma simples", text)
        self.assertIn("`cobre: <n>, <n>`", text)
        self.assertIn("autoriza o commit na branch `feat/pln-021-p2`", text)
        self.assertIn("Merge e push pedem confirmação", text)

    def test_checkout_and_worklog_data(self):
        text, info = step_request.build(plan_md.load("PLN-021", root=_paths.ROOT_DIR), "P3",
                                         worklog="/w/x.md", checkout="/c/estudio", branch="feat/outro")
        self.assertIn("- checkout: /c/estudio (branch feat/outro)", text)
        self.assertIn("- worklog: /w/x.md", text)
        self.assertIn("`<!-- fim-P3: feito -->`", text)

    def test_the_commit_is_only_in_the_checkout_and_the_request_does_not_contradict(self):
        root, path = self.build(plan(step("P1"), ROUND1), design=DESIGN)
        text, _ = step_request.build(path, "P1", checkout="/c/estudio", branch="feat/x")
        self.assertIn("não commite nada no brza-workspace", text)
        self.assertIn("autoriza o commit na branch `feat/x` do checkout `/c/estudio`", text)
        # o checkout é o do próprio workspace: nenhuma branch é autorizada, e o pedido diz isso
        text, _ = step_request.build(path, "P1", checkout=root, branch="feat/x")
        self.assertNotIn("autoriza o commit", text)
        self.assertIn("não commite em lugar nenhum", text)
        self.assertIn("commit: aguarda confirmação", text)

    def test_other_checkout_of_same_repository_also_not_authorizes_commit(self):
        root, path = self.build(plan(step("P1"), ROUND1), design=DESIGN)
        git = ["git", "-C", root, "-c", "user.name=t", "-c", "user.email=t@t"]
        subprocess.run(git + ["init", "-q"], check=True)
        subprocess.run(git + ["add", "-A"], check=True)
        subprocess.run(git + ["commit", "-qm", "c"], check=True)
        other = root + "-wt"
        self.dirs.append(other)
        subprocess.run(git + ["worktree", "add", "-q", "-b", "outra", other], check=True)
        sub = os.path.join(root, "plans")
        for co in (other, sub):
            text, _ = step_request.build(path, "P1", checkout=co, branch="feat/x")
            self.assertNotIn("autoriza o commit", text, co)
            self.assertIn("não commite em lugar nenhum", text, co)

    def test_a_branch_authorized_never_and_master_nor_main(self):
        root, path = self.build(plan(step("P1"), ROUND1), design=DESIGN)
        for b in ("master", "main"):
            with self.assertRaises(step_request.Refusal) as cm:
                step_request.build(path, "P1", checkout="/c/estudio", branch=b)
            self.assertIn("master/main", str(cm.exception))
        rc, _, err = self.cli(path, "P1", "--checkout", "/c/estudio", "--branch", "master")
        self.assertEqual(rc, 1)
        self.assertIn("master/main", err)

    def test_answer_literal_and_without_answer(self):
        pl = plan_md.load("PLN-021", root=_paths.ROOT_DIR)
        block = step_request._block_r(pl, "R2.1")
        self.assertIn("**Resposta literal:** \"pasta script/ em .claude/", block)
        block = step_request._block_r(pl, "R4.1")
        self.assertIn("sem resposta na rodada; vale a recomendada, a confirmar:", block)
        self.assertIn("o pedido do passo autoriza o commit na branch do passo", block)

    def test_refuses_step_without_d(self):
        root, path = self.build(plan(step("P1", executes="Executor: a sessão"), ROUND1), design=DESIGN)
        rc, out, err = self.cli(path, "P1", "--out", os.path.join(root, "p.md"))
        self.assertEqual(rc, 1)
        self.assertIn("não tem `Executa D…`", err)
        self.assertFalse(os.path.exists(os.path.join(root, "p.md")))

    def test_step_without_d_counts_without_design(self):
        root, path = self.build(plan(step("P1", executes="Executor: a sessão"), ROUND1))
        rc, out, err = self.cli(path, "P1", "--out", os.path.join(root, "p.md"))
        self.assertEqual(rc, 0, err)

    def test_refuses_r_that_not_exists(self):
        d = DESIGN.replace("R1.1, R1.2", "R1.1, R9.9")
        root, path = self.build(plan(step("P1"), ROUND1), design=d)
        rc, out, err = self.cli(path, "P1", "--out", os.path.join(root, "p.md"))
        self.assertEqual(rc, 1)
        self.assertIn("R9.9", err)

    def test_refuses_step_and_d_missing(self):
        root, path = self.build(plan(step("P1", executes="Executa D1, D8"), ROUND1), design=DESIGN)
        self.assertEqual(self.cli(path, "P1")[0], 1)
        self.assertEqual(self.cli(path, "P7")[0], 1)
        self.assertEqual(self.cli("PLN-999-nao-existe", "P1")[0], 2)
        self.assertEqual(self.cli(path)[0], 2)

    def test_output_default_in_sessions_and_prints_the_path(self):
        root, path = self.build(plan(step("P1"), ROUND1), design=DESIGN)
        rc, out, err = self.cli(path, "P1")
        self.assertEqual(rc, 0, err)
        expected = os.path.join(root, ".sessions", "pln-900", "P1", "pedido.md")
        self.assertEqual(os.path.realpath(out.strip()), os.path.realpath(expected))
        with open(expected, encoding="utf-8") as f:
            self.assertIn("## O passo", f.read())

    def test_r_only_with_round_brings_all_the_questions(self):
        d = DESIGN.replace("R1.1, R1.2", "R1")
        root, path = self.build(plan(step("P1"), ROUND1), design=d)
        text, _ = step_request.build(path, "P1")
        self.assertIn("### R1.1 — Destino", text)
        self.assertIn("### R1.2 — O nome", text)
        self.assertIn("**Resposta literal:** \"mantém o nome\"", text)


if __name__ == "__main__":
    unittest.main()
