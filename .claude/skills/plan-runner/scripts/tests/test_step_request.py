import io
import os
import shutil
import unittest
from contextlib import redirect_stderr, redirect_stdout

import _paths  # noqa: F401
import plan_md
import step_request
from mini import DESENHO, RODADA1, passo, plano


class Pedido(unittest.TestCase):
    def setUp(self):
        self.dirs = []

    def tearDown(self):
        for d in self.dirs:
            shutil.rmtree(d, ignore_errors=True)

    def monta(self, *a, **k):
        raiz, path = _paths.plano_tmp(*a, **k)
        self.dirs.append(raiz)
        return raiz, path

    def cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = step_request.main(list(args))
        return rc, out.getvalue(), err.getvalue()

    def test_pedido_do_p2_do_pln021(self):
        texto, info = step_request.monta(plan_md.carrega("PLN-021", raiz=_paths.RAIZ), "P2", hoje="2026-11-10")
        self.assertTrue(texto.startswith("Você executa o passo P2 do PLN-021 numa sessão aberta pela coordenação."))
        heads = [l for l in texto.split("\n") if l.startswith("## ")]
        ordem = ["## O passo", "## O que o Desenho fixou", "## O que as rodadas decidiram", "## Restrições e Regressão",
                 "## Onde trabalhar", "## Regras", "## O fim"]
        self.assertEqual(heads, ordem)
        self.assertIn("### P2 — Os quatro scripts de R2.2 e o `plan_md.py`", texto)
        self.assertIn("Estimado: 11.5 h", texto)
        self.assertIn("### D6 — Os quatro scripts de R2.2", texto)
        self.assertIn("#### `close_check.py`", texto)  # o D inteiro, até o fim
        self.assertNotIn("### D7", texto)
        self.assertIn("### R2.2 — Os scripts de apoio", texto)
        self.assertIn("- **Escolhida:** os quatro.", texto)
        self.assertIn("**O `plan-runner` muda só na branch `workstream/playground`**", texto)
        self.assertIn("**A `meeting-runner` faz o mesmo com o `skillkit`.**", texto)
        self.assertIn("(branch feat/pln-021-p2)", texto)
        self.assertTrue(info["worklog"].endswith("2026-11-10-pln-021-p2-os-quatro-scripts-de-r2-2-e-o-plan-md-py.md"), info["worklog"])
        self.assertEqual(step_request.slug("Uma frase bem comprida que passa do limite de caracteres permitido", 30), "uma-frase-bem-comprida-que")
        self.assertIn("pln-021-p2", info["checkout"])
        self.assertTrue(texto.rstrip().endswith("encerramento."))

    def test_o_protocolo_de_fim(self):
        texto, _ = step_request.monta(plan_md.carrega("PLN-021", raiz=_paths.RAIZ), "P2")
        self.assertIn("1. Preencha `## Evidência` no worklog", texto)
        self.assertIn("`commit: brza-studio@<sha7>` (ou `commit: aguarda confirmação`)", texto)
        self.assertIn("`<!-- fim-P2: feito -->` ou `<!-- fim-P2: parado -->`", texto)
        self.assertIn("Não envie `worker_done`", texto)
        self.assertIn("autoriza o commit na branch `feat/pln-021-p2`", texto)
        self.assertIn("Merge e push pedem confirmação", texto)

    def test_checkout_e_worklog_dados(self):
        texto, info = step_request.monta(plan_md.carrega("PLN-021", raiz=_paths.RAIZ), "P3",
                                         worklog="/w/x.md", checkout="/c/estudio", branch="feat/outro")
        self.assertIn("- checkout: /c/estudio (branch feat/outro)", texto)
        self.assertIn("- worklog: /w/x.md", texto)
        self.assertIn("`<!-- fim-P3: feito -->`", texto)

    def test_resposta_literal_e_sem_resposta(self):
        pl = plan_md.carrega("PLN-021", raiz=_paths.RAIZ)
        bloco = step_request._bloco_r(pl, "R2.1")
        self.assertIn("**Resposta literal:** \"pasta script/ em .claude/", bloco)
        bloco = step_request._bloco_r(pl, "R4.1")
        self.assertIn("sem resposta na rodada; vale a recomendada, a confirmar:", bloco)
        self.assertIn("o pedido do passo autoriza o commit na branch do passo", bloco)

    def test_recusa_passo_sem_d(self):
        raiz, path = self.monta(plano(passo("P1", executa="Executor: a sessão"), RODADA1), design=DESENHO)
        rc, out, err = self.cli(path, "P1", "--out", os.path.join(raiz, "p.md"))
        self.assertEqual(rc, 1)
        self.assertIn("não tem `Executa D…`", err)
        self.assertFalse(os.path.exists(os.path.join(raiz, "p.md")))

    def test_passo_sem_d_vale_sem_desenho(self):
        raiz, path = self.monta(plano(passo("P1", executa="Executor: a sessão"), RODADA1))
        rc, out, err = self.cli(path, "P1", "--out", os.path.join(raiz, "p.md"))
        self.assertEqual(rc, 0, err)

    def test_recusa_r_que_nao_existe(self):
        d = DESENHO.replace("R1.1, R1.2", "R1.1, R9.9")
        raiz, path = self.monta(plano(passo("P1"), RODADA1), design=d)
        rc, out, err = self.cli(path, "P1", "--out", os.path.join(raiz, "p.md"))
        self.assertEqual(rc, 1)
        self.assertIn("R9.9", err)

    def test_recusa_passo_e_d_inexistentes(self):
        raiz, path = self.monta(plano(passo("P1", executa="Executa D1, D8"), RODADA1), design=DESENHO)
        self.assertEqual(self.cli(path, "P1")[0], 1)
        self.assertEqual(self.cli(path, "P7")[0], 1)
        self.assertEqual(self.cli("PLN-999-nao-existe", "P1")[0], 2)
        self.assertEqual(self.cli(path)[0], 2)

    def test_saida_padrao_em_sessions_e_imprime_o_caminho(self):
        raiz, path = self.monta(plano(passo("P1"), RODADA1), design=DESENHO)
        rc, out, err = self.cli(path, "P1")
        self.assertEqual(rc, 0, err)
        esperado = os.path.join(raiz, ".sessions", "pln-900", "P1", "pedido.md")
        self.assertEqual(os.path.realpath(out.strip()), os.path.realpath(esperado))
        with open(esperado, encoding="utf-8") as f:
            self.assertIn("## O passo", f.read())

    def test_r_so_com_rodada_traz_todas_as_perguntas(self):
        d = DESENHO.replace("R1.1, R1.2", "R1")
        raiz, path = self.monta(plano(passo("P1"), RODADA1), design=d)
        texto, _ = step_request.monta(path, "P1")
        self.assertIn("### R1.1 — Destino", texto)
        self.assertIn("### R1.2 — O nome", texto)
        self.assertIn("**Resposta literal:** \"mantém o nome\"", texto)


if __name__ == "__main__":
    unittest.main()
