"""Testes do subcomando brza-jira e da integração com a Atlassian CLI (acli jira)."""
import contextlib
import io
import os
import runpy
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
JIRA_SCRIPT_PATH = SCRIPTS / 'brza-jira'
CLI_SCRIPT_PATH = SCRIPTS / 'brza'

JIRA_SCRIPT = runpy.run_path(str(JIRA_SCRIPT_PATH)) if JIRA_SCRIPT_PATH.exists() else None
JIRA_GLOBALS = JIRA_SCRIPT['main'].__globals__ if JIRA_SCRIPT else {}

CLI_SCRIPT = runpy.run_path(str(CLI_SCRIPT_PATH)) if CLI_SCRIPT_PATH.exists() else None
CLI_GLOBALS = CLI_SCRIPT['main'].__globals__ if CLI_SCRIPT else {}


class BrzaJiraTest(unittest.TestCase):
    def run_jira(self, *argv) -> tuple[int, str, str]:
        if not JIRA_SCRIPT_PATH.exists():
            self.fail(f'{JIRA_SCRIPT_PATH} não existe')
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = JIRA_GLOBALS['main'](list(argv))
            except SystemExit as e:
                code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
        return code, out.getvalue(), err.getvalue()

    def test_help_and_version(self):
        code, out, _ = self.run_jira('--help')
        self.assertEqual(code, 0)
        self.assertIn('brza jira', out)
        self.assertIn('my-work', out)

        code, out, _ = self.run_jira('-h')
        self.assertEqual(code, 0)
        self.assertIn('brza jira', out)

        code, out, _ = self.run_jira()
        self.assertEqual(code, 0)
        self.assertIn('brza jira', out)

        code, out, _ = self.run_jira('--version')
        self.assertEqual(code, 0)
        self.assertIn('brza jira', out)

    def test_missing_acli_binary(self):
        with patch.dict(JIRA_GLOBALS, {'find_acli_binary': lambda: None}):
            code, out, err = self.run_jira('my-work')
            self.assertEqual(code, 1)
            self.assertIn('Atlassian CLI', err)
            self.assertIn('brew tap atlassian/homebrew-acli', err)
            self.assertIn('brew install acli', err)

    def test_build_acli_args_my_work(self):
        build = JIRA_GLOBALS['build_acli_args']

        args = build(['my-work'])
        self.assertEqual(args, ['workitem', 'search', '--jql', 'assignee = currentUser() AND statusCategory != Done'])

        args = build(['mine', '--limit', '10', '--json'])
        self.assertEqual(args, ['workitem', 'search', '--jql', 'assignee = currentUser() AND statusCategory != Done',
                                '--limit', '10', '--json'])

        # Se o usuário já passou --jql, não duplica
        args = build(['my-work', '--jql', 'project = TEST'])
        self.assertEqual(args, ['workitem', 'search', '--jql', 'project = TEST'])

    def test_build_acli_args_view(self):
        build = JIRA_GLOBALS['build_acli_args']

        args = build(['view', 'FIX-113'])
        self.assertEqual(args, ['workitem', 'view', 'FIX-113'])

        args = build(['view', 'FIX-113', '--web'])
        self.assertEqual(args, ['workitem', 'view', 'FIX-113', '--web'])

        with self.assertRaises(ValueError):
            build(['view'])

    def test_build_acli_args_search(self):
        build = JIRA_GLOBALS['build_acli_args']

        args = build(['search', 'project = FIX AND status = Done'])
        self.assertEqual(args, ['workitem', 'search', '--jql', 'project = FIX AND status = Done'])

        args = build(['search', 'project = FIX', '--limit', '5'])
        self.assertEqual(args, ['workitem', 'search', '--jql', 'project = FIX', '--limit', '5'])

        args = build(['search', '--filter', '1001'])
        self.assertEqual(args, ['workitem', 'search', '--filter', '1001'])

        with self.assertRaises(ValueError):
            build(['search'])

    def test_build_acli_args_done_and_start(self):
        build = JIRA_GLOBALS['build_acli_args']

        args = build(['done', 'FIX-113'])
        self.assertEqual(args, ['workitem', 'transition', '--key', 'FIX-113', '--status', 'Done', '--yes'])

        args = build(['start', 'FIX-113'])
        self.assertEqual(args, ['workitem', 'transition', '--key', 'FIX-113', '--status', 'In Progress', '--yes'])

        args = build(['in-progress', 'FIX-113'])
        self.assertEqual(args, ['workitem', 'transition', '--key', 'FIX-113', '--status', 'In Progress', '--yes'])

        with self.assertRaises(ValueError):
            build(['done'])

        with self.assertRaises(ValueError):
            build(['start'])

    def test_build_acli_args_transition(self):
        build = JIRA_GLOBALS['build_acli_args']

        args = build(['transition', 'FIX-113', 'Pendente'])
        self.assertEqual(args, ['workitem', 'transition', '--key', 'FIX-113', '--status', 'Pendente', '--yes'])

        with self.assertRaises(ValueError):
            build(['transition', 'FIX-113'])

    def test_build_acli_args_create(self):
        build = JIRA_GLOBALS['build_acli_args']

        args = build(['create', '-s', 'Nova Tarefa', '-p', 'FIX', '-t', 'Task'])
        self.assertEqual(args, ['workitem', 'create', '-s', 'Nova Tarefa', '-p', 'FIX', '-t', 'Task'])

    def test_build_acli_args_passthrough(self):
        build = JIRA_GLOBALS['build_acli_args']

        args = build(['board', 'list'])
        self.assertEqual(args, ['board', 'list'])

        args = build(['sprint', 'list', '--board-id', '1'])
        self.assertEqual(args, ['sprint', 'list', '--board-id', '1'])

        args = build(['auth', 'status'])
        self.assertEqual(args, ['auth', 'status'])

    def test_run_acli_invocation(self):
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        fake_acli = Path('/fake/bin/acli')

        with patch.dict(JIRA_GLOBALS, {'find_acli_binary': lambda: fake_acli}), \
             patch.object(JIRA_GLOBALS['subprocess'], 'run', return_value=mock_proc) as mock_run:
            code, _, _ = self.run_jira('view', 'FIX-113')
            self.assertEqual(code, 0)
            mock_run.assert_called_once()
            called_cmd = mock_run.call_args[0][0]
            self.assertEqual(called_cmd, [str(fake_acli), 'jira', 'workitem', 'view', 'FIX-113'])

    def test_brza_dispatcher_calls_jira(self):
        # Testa a integração com o despachante principal brza
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = CLI_GLOBALS['main'](['jira', '--version'])
        self.assertEqual(code, 0)
        self.assertIn('brza jira', out.getvalue())


if __name__ == '__main__':
    unittest.main()
