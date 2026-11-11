"""Testes do skillkit.paths: a raiz do git, a raiz comum e o corte do anexo de medida."""
import os
import subprocess
import tempfile
import unittest

import _paths  # noqa: F401
from skillkit import paths


class Roots(unittest.TestCase):
    def test_default_root_is_the_git_top_of_the_cwd(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["git", "init", "-q", tmp], check=True)
            os.makedirs(os.path.join(tmp, "a", "b"))
            before = os.getcwd()
            os.chdir(os.path.join(tmp, "a", "b"))
            try:
                self.assertEqual(os.path.realpath(paths.default_root()), os.path.realpath(tmp))
            finally:
                os.chdir(before)

    def test_default_root_without_git_is_the_cwd(self):
        with tempfile.TemporaryDirectory() as tmp:
            before = os.getcwd()
            os.chdir(tmp)
            original = paths.subprocess.run
            paths.subprocess.run = lambda *a, **k: (_ for _ in ()).throw(FileNotFoundError("git"))
            try:
                self.assertEqual(os.path.realpath(paths.default_root()), os.path.realpath(tmp))
            finally:
                paths.subprocess.run = original
                os.chdir(before)

    def test_common_root_of_worktree_and_a_root_shared(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = os.path.join(tmp, "repo")
            subprocess.run(["git", "init", "-q", repo], check=True)
            subprocess.run(["git", "-C", repo, "-c", "user.email=a@b", "-c", "user.name=a", "commit", "-q",
                            "--allow-empty", "-m", "x"], check=True)
            wt = os.path.join(repo, ".worktrees", "w")
            subprocess.run(["git", "-C", repo, "worktree", "add", "-q", "-b", "w", wt], check=True)
            self.assertEqual(paths.common_root(wt), os.path.realpath(repo))
            self.assertEqual(paths.common_root(repo), os.path.realpath(repo))

    def test_common_root_outside_git_is_the_path_itself(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(paths.common_root(tmp), os.path.abspath(tmp))


class StripMeasurement(unittest.TestCase):
    BASE = "# w\n\ntexto\n\n<!-- fim-rodada-1 -->\n"

    def test_strips_the_attachment_after_of_marker(self):
        self.assertEqual(paths.strip_measurement(self.BASE + "\n## Medida\n\n| a |\n"), self.BASE + "")
        self.assertTrue(paths.strip_measurement(self.BASE + "\n## Custo da tarefa\n\nUS$ 1\n").rstrip().endswith("-->"))

    def test_without_attachment_the_text_stays(self):
        self.assertEqual(paths.strip_measurement(self.BASE), self.BASE)
        self.assertEqual(paths.strip_measurement(None), "")

    def test_section_of_level_two_after_of_attachment_leaves_the_text(self):
        t = self.BASE + "\n## Medida\n\nx\n\n## Outra\n"
        self.assertEqual(paths.strip_measurement(t), t)

    def test_marker_after_of_header_is_not_attachment(self):
        t = "# w\n\n## Medida\n\nx\n<!-- fim-rodada-2 -->\n"
        self.assertEqual(paths.strip_measurement(t), t)


if __name__ == "__main__":
    unittest.main()
