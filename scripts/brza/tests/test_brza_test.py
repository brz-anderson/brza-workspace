"""Testes do brza-test, num brza-studio de mentira: um clone de uma origin local, com o vitest, o install e o
check:changed trocados por falsos.

    python3 -m unittest discover -s scripts/brza/tests
"""
import contextlib
import io
import json
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

TEST = runpy.run_path(str(SCRIPTS / 'brza-test'))
# As funções leem os globais do módulo em que nasceram, não da cópia que o run_path devolve.
GLOBALS = TEST['main'].__globals__


def git(*args, cwd: Path):
    return subprocess.run(['git', '-C', str(cwd), '-c', 'user.name=t', '-c', 'user.email=t@t', *args],
                          check=True, capture_output=True, text=True).stdout.strip()


def write(root: Path, *paths: str):
    """Cria cada arquivo, ou o altera quando ele já existe."""
    for rel in paths:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(path.read_text() + '// mudou\n' if path.exists() else f'// {rel}\n')


class BrzaTestTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()
        origin, seed, self.studio = self.base / 'origin.git', self.base / 'seed', self.base / 'studio'
        subprocess.run(['git', 'init', '-q', '--bare', '-b', 'master', str(origin)], check=True)
        subprocess.run(['git', 'clone', '-q', str(origin), str(seed)], check=True, capture_output=True)
        write(seed, 'src/a.ts', 'src/a.test.ts', 'src/b.tsx', 'src/b.test.tsx', 'src/old.test.ts',
              'config/scripts/c.mjs', 'config/scripts/c.test.mjs', 'src/lonely.ts')
        git('add', '.', cwd=seed)
        git('commit', '-q', '-m', 'um', cwd=seed)
        git('push', '-q', 'origin', 'HEAD:master', cwd=seed)
        subprocess.run(['git', 'clone', '-q', str(origin), str(self.studio)], check=True)
        self.tree = self.studio / '.worktrees' / 'x'
        git('worktree', 'add', '-q', '-b', 'feat/x', str(self.tree), 'origin/master', cwd=self.studio)
        # a master anda depois que a branch saiu: o que muda só nela não conta como alterado
        write(seed, 'src/master-only.ts', 'src/master-only.test.ts')
        git('add', '.', cwd=seed)
        git('commit', '-q', '-m', 'dois', cwd=seed)
        git('push', '-q', 'origin', 'HEAD:master', cwd=seed)

        self.runs = []  # (raiz, arquivos) de cada vitest
        self.failing = {}  # raiz -> {arquivo: [testes que falham]}; '' é a falha do arquivo inteiro
        self.installed = []
        self.install_error = None
        for p in (patch.object(runtime, 'STUDIO', self.studio),
                  patch.object(runtime, 'install_offline', self.fake_install),
                  patch.dict(GLOBALS, {'run_vitest': self.fake_vitest})):
            p.start()
            self.addCleanup(p.stop)
        self.pnpm_args = self.base / 'pnpm-args'
        self.check_exit = 0
        self.fake_bin()

    def fake_bin(self):
        """Um pnpm no PATH que grava os argumentos e sai com o código do check_exit."""
        bin_dir = self.base / 'bin'
        bin_dir.mkdir(exist_ok=True)
        pnpm = bin_dir / 'pnpm'
        pnpm.write_text(f'#!/bin/sh\necho "$*" >> {self.pnpm_args}\necho "saída do check"\n'
                        f'exit $(cat {self.base / "check-exit"})\n')
        pnpm.chmod(0o755)
        p = patch.dict(os.environ, {'PATH': f'{bin_dir}:{os.environ["PATH"]}'})
        p.start()
        self.addCleanup(p.stop)

    def fake_install(self, path: Path):
        self.installed.append(path)
        if self.install_error:
            raise runtime.BrzaError(self.install_error)

    def fake_vitest(self, root: Path, files: list[str]) -> dict[str, list[str]]:
        root = Path(root).resolve()
        self.runs.append((root, list(files)))
        failing = self.failing.get('master' if root != self.tree.resolve() else 'tree', {})
        return {f: failing.get(f, []) for f in files}

    def run_test(self, *argv, cwd: Path | None = None) -> tuple[int, str]:
        (self.base / 'check-exit').write_text(str(self.check_exit))
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out), \
                contextlib.chdir(cwd or self.tree):
            try:
                code = GLOBALS['main'](list(argv))
            except SystemExit as e:
                code = e.code
        return code, out.getvalue()

    def worktrees(self) -> list[str]:
        return [line for line in git('worktree', 'list', '--porcelain', cwd=self.studio).splitlines()
                if line.startswith('worktree ')]

    # a lista dos testes

    def test_changed_tests_and_neighbours_against_the_merge_base(self):
        write(self.tree, 'src/a.ts', 'src/b.tsx', 'config/scripts/c.test.mjs', 'src/lonely.ts', 'README.md')
        write(self.tree, 'src/new.test.ts')  # não rastreado ainda
        tests, untested = GLOBALS['select_tests'](self.tree, GLOBALS['changed_files'](self.tree))
        self.assertEqual(tests, ['config/scripts/c.test.mjs', 'src/a.test.ts', 'src/b.test.tsx', 'src/new.test.ts'])
        self.assertEqual(untested, ['src/lonely.ts'])

    def test_committed_changes_count_and_deleted_tests_do_not(self):
        write(self.tree, 'src/a.ts')
        git('rm', '-q', 'src/old.test.ts', cwd=self.tree)
        git('commit', '-q', '-am', 'na branch', cwd=self.tree)
        tests, untested = GLOBALS['select_tests'](self.tree, GLOBALS['changed_files'](self.tree))
        self.assertEqual((tests, untested), (['src/a.test.ts'], []))

    def test_given_paths_replace_the_changed_list(self):
        write(self.tree, 'src/a.ts')
        code, out = self.run_test('--', 'src/b.test.tsx')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.runs, [(self.tree.resolve(), ['src/b.test.tsx'])])

    def test_worktree_argument_and_refusal_outside_the_studio(self):
        write(self.tree, 'src/a.ts')
        code, out = self.run_test(str(self.tree), cwd=self.base)
        self.assertEqual(code, 0, out)
        self.assertEqual(self.runs, [(self.tree.resolve(), ['src/a.test.ts'])])
        code, out = self.run_test(cwd=self.base)
        self.assertEqual(code, 2)
        self.assertIn('worktree do brza-studio', out)

    # o check:changed

    def test_check_changed_always_gets_the_origin_master_base(self):
        code, out = self.run_test()
        self.assertEqual(code, 0, out)
        self.assertEqual(self.pnpm_args.read_text().split(),
                         ['check:changed', '--base=origin/master', '--maxWorkers=2'])
        self.assertIn('nenhum teste alterado', out)
        self.assertEqual(self.runs, [])

    def test_red_check_changed_exits_1_with_its_output(self):
        self.check_exit = 1
        code, out = self.run_test()
        self.assertEqual(code, 1)
        self.assertIn('check:changed: vermelho', out)
        self.assertIn('saída do check', out)

    # os três grupos

    def test_three_groups_and_the_baseline_runs_only_the_failures(self):
        write(self.tree, 'src/a.ts', 'src/b.tsx', 'config/scripts/c.mjs', 'src/new.test.ts')
        self.failing = {
            'tree': {'src/a.test.ts': ['a › quebrou'], 'src/b.test.tsx': ['b › velho', 'b › novo'],
                     'src/new.test.ts': ['']},
            'master': {'src/b.test.tsx': ['b › velho']},
        }
        code, out = self.run_test()
        self.assertEqual(code, 1, out)
        tree_run, master_run = self.runs
        self.assertEqual(tree_run[1], ['config/scripts/c.test.mjs', 'src/a.test.ts', 'src/b.test.tsx',
                                       'src/new.test.ts'])
        # o arquivo que não existe na master não vai ao baseline: é falha nova de saída
        self.assertEqual(master_run[1], ['src/a.test.ts', 'src/b.test.tsx'])
        self.assertNotEqual(master_run[0], self.tree.resolve())
        report = out[out.index('passou'):]
        self.assertRegex(report, r'passou:.*\n.*config/scripts/c\.test\.mjs')
        self.assertRegex(report, r'falha nova:(.|\n)*src/a\.test\.ts › a › quebrou')
        self.assertRegex(report, r'falha nova:(.|\n)*src/b\.test\.tsx › b › novo')
        self.assertRegex(report, r'falha nova:(.|\n)*src/new\.test\.ts \(o arquivo\)')
        self.assertRegex(report, r'já falhava na master:(.|\n)*src/b\.test\.tsx › b › velho')
        self.assertNotRegex(report.split('já falhava na master:')[0], r'b › velho')
        self.assertEqual(self.installed, [master_run[0]])
        self.assertEqual(len(self.worktrees()), 2)  # o temporário saiu
        self.assertFalse(master_run[0].exists())

    def test_only_old_failures_exit_0(self):
        write(self.tree, 'src/b.tsx')
        self.failing = {'tree': {'src/b.test.tsx': ['b › velho']}, 'master': {'src/b.test.tsx': ['b › velho']}}
        code, out = self.run_test()
        self.assertEqual(code, 0, out)
        self.assertIn('já falhava na master', out)

    def test_no_baseline_reports_failures_without_the_master(self):
        write(self.tree, 'src/b.tsx')
        self.failing = {'tree': {'src/b.test.tsx': ['b › velho']}}
        code, out = self.run_test('--no-baseline')
        self.assertEqual(code, 1)
        self.assertEqual(len(self.runs), 1)
        self.assertIn('falha, sem baseline', out)

    def test_the_temporary_worktree_leaves_even_when_the_baseline_fails(self):
        write(self.tree, 'src/b.tsx')
        self.failing = {'tree': {'src/b.test.tsx': ['b › velho']}}
        self.install_error = 'o install offline falhou'
        code, out = self.run_test()
        self.assertEqual(code, 1)
        self.assertIn('baseline: falhou', out)
        self.assertIn('falha, sem baseline', out)
        temp = self.installed[0]
        self.assertFalse(temp.exists())
        self.assertEqual(len(self.worktrees()), 2)

    def test_the_temporary_worktree_leaves_even_when_tests_dirty_it(self):
        write(self.tree, 'src/b.tsx')
        self.failing = {'tree': {'src/b.test.tsx': ['b › velho']}}

        def dirty_vitest(root, files):
            (Path(root) / 'sujeira.txt').write_text('x')
            return self.fake_vitest(root, files)

        with patch.dict(GLOBALS, {'run_vitest': dirty_vitest}):
            code, out = self.run_test()
        self.assertEqual(code, 1, out)
        self.assertFalse(self.installed[0].exists())
        self.assertEqual(len(self.worktrees()), 2)

    # o relatório do vitest

    def test_report_parsing_keeps_test_and_file_failures(self):
        root = Path('/w')
        report = {'testResults': [
            {'name': '/w/src/a.test.ts', 'status': 'failed', 'assertionResults': [
                {'fullName': 'a quebrou', 'status': 'failed'}, {'fullName': 'a passa', 'status': 'passed'}]},
            {'name': '/w/src/b.test.ts', 'status': 'passed', 'assertionResults': [
                {'fullName': 'b passa', 'status': 'passed'}, {'fullName': 'b pula', 'status': 'skipped'}]},
            {'name': '/w/src/c.test.ts', 'status': 'failed', 'message': 'SyntaxError', 'assertionResults': []},
        ]}
        self.assertEqual(GLOBALS['parse_report'](report, root),
                         {'src/a.test.ts': ['a quebrou'], 'src/b.test.ts': [], 'src/c.test.ts': ['']})

    def test_vitest_command_writes_json_to_a_file(self):
        command = GLOBALS['vitest_command'](['src/a.test.ts'], Path('/tmp/r.json'))
        self.assertEqual(command, ['node', 'config/scripts/run-vitest.mjs', 'run', '--config', 'config/vitest.config.ts',
                                   '--reporter=json', '--outputFile=/tmp/r.json', 'src/a.test.ts'])

    def test_usage_errors_exit_2(self):
        for argv in (['a', 'b'], ['--wat']):
            with self.subTest(argv=argv):
                code, _ = self.run_test(*argv)
                self.assertEqual(code, 2)


if __name__ == '__main__':
    unittest.main()
