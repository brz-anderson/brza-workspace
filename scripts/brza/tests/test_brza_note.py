"""Testes do brza-note, num brza-workspace de mentira: um clone de uma origin local, com um checador falso.

    python3 -m unittest discover -s scripts/brza/tests
"""
import contextlib
import datetime
import io
import os
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS))
import brza_runtime as runtime  # noqa: E402

NOTE = runpy.run_path(str(SCRIPTS / 'brza-note'))
# As funções leem os globais do módulo em que nasceram, não da cópia que o run_path devolve.
GLOBALS = NOTE['main'].__globals__
TODAY = datetime.date(2026, 10, 28)


def git(*args, cwd: Path):
    return subprocess.run(['git', '-C', str(cwd), *args], check=True, capture_output=True, text=True).stdout.strip()


class NoteTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()
        self.origin, self.other, self.ws = self.base / 'origin.git', self.base / 'other', self.base / 'ws'
        subprocess.run(['git', 'init', '-q', '--bare', '-b', 'master', str(self.origin)], check=True)
        subprocess.run(['git', 'clone', '-q', str(self.origin), str(self.ws)], check=True, capture_output=True)
        git('config', 'user.name', 't', cwd=self.ws)
        git('config', 'user.email', 't@t', cwd=self.ws)
        (self.ws / 'work' / 'worklogs').mkdir(parents=True)
        (self.ws / 'work' / 'issues').mkdir(parents=True)
        (self.ws / 'README.md').write_text('um\n')
        self.checker_exit(0)
        git('add', '.', cwd=self.ws)
        git('commit', '-q', '-m', 'um', cwd=self.ws)
        git('push', '-q', 'origin', 'HEAD:master', cwd=self.ws)
        git('branch', '-q', '--set-upstream-to=origin/master', cwd=self.ws)
        for p in (patch.object(runtime, 'WORKSPACE', self.ws),
                  patch.dict(GLOBALS, {'today': lambda: TODAY})):
            p.start()
            self.addCleanup(p.stop)

    def checker_exit(self, code: int):
        """Troca o check_notes.py do workspace de mentira por um que imprime e sai com `code`."""
        checker = self.ws / '.claude' / 'skills' / 'notes-checker' / 'scripts' / 'check_notes.py'
        checker.parent.mkdir(parents=True, exist_ok=True)
        checker.write_text(f'import sys\nprint("checador: saída {code}")\nsys.exit({code})\n')

    def run_note(self, *argv, env: dict | None = None, cwd: Path | None = None) -> tuple[int, str]:
        """Roda o main; sem `cwd`, de fora do workspace de mentira, onde o caminho relativo parte da raiz dele."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out), \
                patch.dict('os.environ', env or {}), contextlib.chdir(cwd or self.base):
            try:
                code = GLOBALS['main'](list(argv))
            except SystemExit as e:
                code = e.code
        return code, out.getvalue()

    def origin_log(self) -> list[str]:
        return git('log', '--format=%s', 'master', cwd=self.origin).splitlines()

    def committed_files(self, ref: str = 'HEAD') -> list[str]:
        return git('show', '--name-only', '--format=', ref, cwd=self.ws).splitlines()

    # new

    def test_new_worklog_writes_the_skeleton_and_prints_the_path(self):
        code, out = self.run_note('new', 'worklog', 'o-brza-note', env={'CLAUDE_SESSION_NAME': 'pln-002-p6'})
        self.assertEqual(code, 0, out)
        path = self.ws / 'work' / 'worklogs' / '2026-10-28-o-brza-note.md'
        self.assertEqual(out.strip().splitlines()[-1], str(path))
        text = path.read_text()
        self.assertTrue(text.startswith('---\nscope:\n  - workspace\n---\n\n# '))
        self.assertIn('O pedido de Anderson, em 2026-10-28, na sessão `pln-002-p6`: "', text)
        for section in ('## O que se fez', '## O que ficou', '## Fora do workspace'):
            self.assertIn(f'\n{section}\n', text)

    def test_new_worklog_without_session_name_leaves_it_to_write(self):
        with patch.dict('os.environ'):
            os.environ.pop('CLAUDE_SESSION_NAME', None)
            code, out = self.run_note('new', 'worklog', 'sem-nome')
        self.assertEqual(code, 0, out)
        text = (self.ws / 'work' / 'worklogs' / '2026-10-28-sem-nome.md').read_text()
        self.assertIn('na sessão `<a escrever>`', text)

    def test_new_issue_has_open_status_today_scope_and_priority(self):
        code, out = self.run_note('new', 'issue', 'algo-quebrado', '--scope', 'workspace,brza-studio',
                                  '--priority', 'high')
        self.assertEqual(code, 0, out)
        text = (self.ws / 'work' / 'issues' / 'algo-quebrado.md').read_text()
        self.assertTrue(text.startswith('---\nstatus: open\nscope:\n  - workspace\n  - brza-studio\n'
                                        'opened: 2026-10-28\npriority: high\n---\n\n# '), text)
        self.assertIn('\n## O pedido\n', text)

    def test_new_issue_without_priority_omits_the_field(self):
        code, out = self.run_note('new', 'issue', 'sem-prioridade')
        self.assertEqual(code, 0, out)
        self.assertNotIn('priority', (self.ws / 'work' / 'issues' / 'sem-prioridade.md').read_text())

    def test_new_refuses_an_existing_note_and_keeps_it(self):
        path = self.ws / 'work' / 'issues' / 'ja-existe.md'
        path.write_text('meu texto\n')
        code, out = self.run_note('new', 'issue', 'ja-existe')
        self.assertEqual(code, 1, out)
        self.assertIn('já existe', out)
        self.assertEqual(path.read_text(), 'meu texto\n')

    def test_new_refuses_a_subject_out_of_kebab_case(self):
        code, _ = self.run_note('new', 'worklog', 'Com Espaço')
        self.assertEqual(code, 2)
        code, _ = self.run_note('new', 'issue', '2026-10-28-com-data')
        self.assertEqual(code, 2)

    # commit

    def write(self, rel: str, text: str = 'texto\n') -> Path:
        path = self.ws / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def test_commit_stops_on_checker_error_and_commits_nothing(self):
        self.write('work/issues/a.md')
        self.checker_exit(1)
        head = git('rev-parse', 'HEAD', cwd=self.ws)
        code, out = self.run_note('commit', 'work/issues/a.md', '-m', 'docs: a')
        self.assertEqual(code, 1, out)
        self.assertIn('checador: saída 1', out)
        self.assertEqual(git('rev-parse', 'HEAD', cwd=self.ws), head)
        self.assertEqual(git('diff', '--cached', '--name-only', cwd=self.ws), '')

    def test_commit_takes_only_the_given_paths_even_with_something_else_staged(self):
        self.write('work/issues/a.md')
        self.write('README.md', 'sujo ao lado\n')
        self.write('work/issues/de-outra-sessao.md')
        git('add', 'work/issues/de-outra-sessao.md', cwd=self.ws)
        code, out = self.run_note('commit', 'work/issues/a.md', '-m', 'docs: a', '--no-push')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.committed_files(), ['work/issues/a.md'])
        self.assertEqual(git('log', '-1', '--format=%s', cwd=self.ws), 'docs: a')
        self.assertEqual(git('diff', '--name-only', cwd=self.ws), 'README.md')
        self.assertEqual(git('diff', '--cached', '--name-only', cwd=self.ws), 'work/issues/de-outra-sessao.md')

    def test_commit_path_is_relative_to_the_current_directory_inside_the_workspace(self):
        self.write('work/issues/a.md')
        code, out = self.run_note('commit', 'a.md', '-m', 'docs: a', '--no-push', cwd=self.ws / 'work' / 'issues')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.committed_files(), ['work/issues/a.md'])

    def test_commit_path_is_relative_to_the_workspace_root_from_outside(self):
        self.write('work/issues/a.md')
        code, out = self.run_note('commit', 'work/issues/a.md', '-m', 'docs: a', '--no-push', cwd=self.base)
        self.assertEqual(code, 0, out)
        self.assertEqual(self.committed_files(), ['work/issues/a.md'])

    def test_commit_refuses_a_path_outside_the_workspace(self):
        outside = self.base / 'fora.md'
        outside.write_text('x\n')
        code, out = self.run_note('commit', str(outside), '-m', 'docs: fora')
        self.assertEqual(code, 2, out)
        code, out = self.run_note('commit', '../fora.md', '-m', 'docs: fora', cwd=self.ws)
        self.assertEqual(code, 2, out)

    def test_commit_pulls_with_rebase_over_a_push_from_elsewhere_and_pushes(self):
        subprocess.run(['git', 'clone', '-q', str(self.origin), str(self.other)], check=True, capture_output=True)
        (self.other / 'work').mkdir(exist_ok=True)
        (self.other / 'work' / 'outra.md').write_text('de outra sessão\n')
        git('add', '.', cwd=self.other)
        git('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-q', '-m', 'docs: outra', cwd=self.other)
        git('push', '-q', 'origin', 'HEAD:master', cwd=self.other)
        self.write('work/issues/a.md')
        self.write('README.md', 'sujo ao lado\n')
        code, out = self.run_note('commit', 'work/issues/a.md', '-m', 'docs: a')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.origin_log()[:2], ['docs: a', 'docs: outra'])
        self.assertEqual((self.ws / 'README.md').read_text(), 'sujo ao lado\n')

    def test_commit_no_push_stops_at_the_commit(self):
        self.write('work/issues/a.md')
        code, out = self.run_note('commit', 'work/issues/a.md', '-m', 'docs: a', '--no-push')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.origin_log(), ['um'])
        self.assertEqual(git('log', '-1', '--format=%s', cwd=self.ws), 'docs: a')

    def test_commit_with_nothing_changed_in_the_paths_fails(self):
        code, out = self.run_note('commit', 'README.md', '-m', 'docs: nada', '--no-push')
        self.assertEqual(code, 1, out)
        self.assertEqual(git('log', '-1', '--format=%s', cwd=self.ws), 'um')


if __name__ == '__main__':
    unittest.main()
