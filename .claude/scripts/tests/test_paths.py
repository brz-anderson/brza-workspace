"""Testes do skillkit.paths: a raiz do git, a raiz comum e o corte do anexo de medida."""
import os
import subprocess
import tempfile
import unittest

import _paths  # noqa: F401
from skillkit import paths


class Raizes(unittest.TestCase):
    def test_raiz_padrao_e_o_topo_do_git_do_cwd(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["git", "init", "-q", tmp], check=True)
            os.makedirs(os.path.join(tmp, "a", "b"))
            antes = os.getcwd()
            os.chdir(os.path.join(tmp, "a", "b"))
            try:
                self.assertEqual(os.path.realpath(paths.raiz_padrao()), os.path.realpath(tmp))
            finally:
                os.chdir(antes)

    def test_raiz_padrao_sem_git_e_o_cwd(self):
        with tempfile.TemporaryDirectory() as tmp:
            antes = os.getcwd()
            os.chdir(tmp)
            original = paths.subprocess.run
            paths.subprocess.run = lambda *a, **k: (_ for _ in ()).throw(FileNotFoundError("git"))
            try:
                self.assertEqual(os.path.realpath(paths.raiz_padrao()), os.path.realpath(tmp))
            finally:
                paths.subprocess.run = original
                os.chdir(antes)

    def test_common_root_do_worktree_e_a_raiz_comum(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = os.path.join(tmp, "repo")
            subprocess.run(["git", "init", "-q", repo], check=True)
            subprocess.run(["git", "-C", repo, "-c", "user.email=a@b", "-c", "user.name=a", "commit", "-q",
                            "--allow-empty", "-m", "x"], check=True)
            wt = os.path.join(repo, ".worktrees", "w")
            subprocess.run(["git", "-C", repo, "worktree", "add", "-q", "-b", "w", wt], check=True)
            self.assertEqual(paths.common_root(wt), os.path.realpath(repo))
            self.assertEqual(paths.common_root(repo), os.path.realpath(repo))

    def test_common_root_fora_do_git_e_o_proprio_caminho(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(paths.common_root(tmp), os.path.abspath(tmp))


class CortaMedida(unittest.TestCase):
    BASE = "# w\n\ntexto\n\n<!-- fim-rodada-1 -->\n"

    def test_corta_o_anexo_depois_do_marcador(self):
        self.assertEqual(paths.corta_medida(self.BASE + "\n## Medida\n\n| a |\n"), self.BASE + "")
        self.assertTrue(paths.corta_medida(self.BASE + "\n## Custo da tarefa\n\nUS$ 1\n").rstrip().endswith("-->"))

    def test_sem_anexo_o_texto_fica(self):
        self.assertEqual(paths.corta_medida(self.BASE), self.BASE)
        self.assertEqual(paths.corta_medida(None), "")

    def test_secao_de_nivel_dois_depois_do_anexo_deixa_o_texto(self):
        t = self.BASE + "\n## Medida\n\nx\n\n## Outra\n"
        self.assertEqual(paths.corta_medida(t), t)

    def test_marcador_depois_do_cabecalho_nao_e_anexo(self):
        t = "# w\n\n## Medida\n\nx\n<!-- fim-rodada-2 -->\n"
        self.assertEqual(paths.corta_medida(t), t)


if __name__ == "__main__":
    unittest.main()
