"""Testes do check_briefing.py (X8): número no briefing precisa de `conferido às HH:MM: `comando` → resultado`."""
import contextlib
import io
import os
import shutil
import tempfile
import unittest

import _paths  # noqa: F401
from _paths import fixture

import check_briefing


def roda(texto):
    tmp = tempfile.mkdtemp()
    try:
        path = os.path.join(tmp, "briefing.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(texto)
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = check_briefing.main([path])
        return rc, out.getvalue(), err.getvalue()
    finally:
        shutil.rmtree(tmp, True)


SECAO = "# B\n\n## O que existe hoje\n\n{itens}\n\n## As alternativas\n\n- A com 3 itens sem marca\n"


class Briefing(unittest.TestCase):
    def test_o_briefing_real_do_p7_sai_1_apontando_o_item_do_1352(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = check_briefing.main([fixture("p7", "briefing.md")])
        self.assertEqual(rc, 1)
        linha = next(l for l in out.getvalue().splitlines() if "1.352" in l)
        self.assertTrue(linha.startswith("linha 22:"), linha)
        self.assertIn("conferido", linha)

    def test_item_com_a_marca_completa_passa(self):
        item = ("- `#38950` foi fechado sem merge, com 163 arquivos — conferido às 14:02: "
                "`gh pr view 38950 -R stablyai/orca --json changedFiles` → 163")
        self.assertEqual(roda(SECAO.format(itens=item))[0], 0)

    def test_item_sem_numero_nao_precisa(self):
        self.assertEqual(roda(SECAO.format(itens="- O botão existe no fork `CheckRunDetailsPanel.tsx`."))[0], 0)

    def test_marca_incompleta_nao_vale(self):
        for item in ("- 3 PRs — conferido às 14:02", "- 3 PRs — conferido às 14:02: `gh pr list`",
                     "- 3 PRs — `gh pr list` → 3", "- 3 PRs — conferido às 14:02: gh pr list → 3"):
            rc, out, _ = roda(SECAO.format(itens=item))
            self.assertEqual(rc, 1, item)
            self.assertIn("linha 5:", out)

    def test_item_em_varias_linhas_e_lista_numerada(self):
        item = "1. O PR tem 5 arquivos\n   — conferido às 14:02: `gh pr view` → 5 arquivos"
        self.assertEqual(roda(SECAO.format(itens=item))[0], 0)

    def test_so_a_secao_conta(self):
        rc, out, _ = roda(SECAO.format(itens="- sem número"))
        self.assertEqual(rc, 0)   # o "3 itens sem marca" fora da seção não conta

    def test_sem_a_secao_sai_2(self):
        rc, out, err = roda("# B\n\n## Outra\n\n- 3 coisas\n")
        self.assertEqual(rc, 2)
        self.assertIn("O que existe hoje", err)

    def test_sem_arquivo_e_uso_errado_saem_2(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(check_briefing.main(["/nao/existe.md"]), 2)
            self.assertEqual(check_briefing.main([]), 2)


class IdsELinhas(unittest.TestCase):
    def test_molde_b_com_arquivo_linha_e_r6_passa(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = check_briefing.main([fixture("review", "b.md")])
        self.assertEqual(rc, 0, out.getvalue())

    def test_id_linha_rotulo_e_crases_nao_sao_numero_de_fato(self):
        for item in ("- Está em `arquivo.py:120`.", "- Foi o R6 do PLN-017.", "- Veja arquivo.py:120.", "- O `#39020` e `abc123` ali.",
                     "- Em 2026-11-08 houve isso."):
            self.assertEqual(roda(SECAO.format(itens=item))[0], 0, item)

    def test_numero_de_fato_sem_crases_continua_exigindo_a_marca(self):
        for item in ("- 1.352 arquivos", "- 3 PRs abertos", "- cerca de ~2 min"):
            self.assertEqual(roda(SECAO.format(itens=item))[0], 1, item)

    def test_a_exibicao_usa_a_mesma_regex(self):
        rc, out, _ = roda(SECAO.format(itens="- Foram 1.352 arquivos em `a.py:9`."))
        self.assertIn("[números: 1.352]", out)


class NumeroEntreCrases(unittest.TestCase):
    def test_numero_ou_medida_entre_crases_exige_a_marca(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = check_briefing.main([fixture("review", "b2.md")])
        self.assertEqual(rc, 1)
        self.assertIn("linha 5:", out.getvalue())          # "`1.352` arquivos"
        self.assertIn("[números: 1.352]", out.getvalue())

    def test_caminho_id_hash_e_comando_entre_crases_continuam_ignorados(self):
        for item in ("- Em `.claude/hooks/measure.py:120`.", "- O `fd334f1e99a3` e `#39020`.", "- Rode `gh pr list -n 5`.",
                     "- `arquivo.py` e `R6`."):
            self.assertEqual(roda(SECAO.format(itens=item))[0], 0, item)
        self.assertEqual(roda(SECAO.format(itens="- Levou `12 min`."))[0], 1)


if __name__ == "__main__":
    unittest.main()
