"""Testes do binário unificador brza e do despacho nos dois clients (B1 / PLN-003)."""
import contextlib
import io
import os
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
CLI_PATH = SCRIPTS / 'brza'


CLI_SCRIPT = runpy.run_path(str(CLI_PATH)) if CLI_PATH.exists() else None
GLOBALS = CLI_SCRIPT['main'].__globals__ if CLI_SCRIPT else {}


class BrzaCliTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.bin_dir = self.base / 'bin'
        self.bin_dir.mkdir()

    def run_cli(self, *argv, env: dict | None = None) -> tuple[int, str, str]:
        if not CLI_PATH.exists():
            self.fail(f'{CLI_PATH} não existe')
        out, err = io.StringIO(), io.StringIO()
        merged_env = {**os.environ, **(env or {})}
        with patch.dict(os.environ, merged_env, clear=True), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = GLOBALS['main'](list(argv))
            except SystemExit as e:
                code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
        return code, out.getvalue(), err.getvalue()

    def test_detect_client_from_brza_client_env(self):
        detect = GLOBALS['detect_client']
        self.assertEqual(detect({'BRZA_CLIENT': 'orca'}), 'orca')
        self.assertEqual(detect({'BRZA_CLIENT': 'studio'}), 'studio')
        self.assertEqual(detect({'BRZA_CLIENT': 'brza-studio'}), 'studio')

    def test_detect_client_from_inherited_app_env(self):
        detect = GLOBALS['detect_client']
        self.assertEqual(detect({'ORCA_USER_DATA_PATH': '/tmp/orca'}), 'orca')
        self.assertEqual(detect({'ORCA_VERSION': '1.4.246'}), 'orca')
        self.assertEqual(detect({'ORCA_AGENT_SESSION_ID': 's123'}), 'orca')
        self.assertEqual(detect({'BRZA_STUDIO_USER_DATA_PATH': '/tmp/studio'}), 'studio')
        self.assertEqual(detect({'BRZA_STUDIO_VERSION': '1.4.246-alpha.1'}), 'studio')

    def test_detect_client_from_running_process(self):
        detect = GLOBALS['detect_client']

        def fake_is_running(app_name: str) -> bool:
            return app_name == 'Orca'

        with patch.dict(GLOBALS, {'is_app_running': fake_is_running}):
            self.assertEqual(detect({}), 'orca')

        def fake_is_studio(app_name: str) -> bool:
            return app_name == 'BrzA Studio'

        with patch.dict(GLOBALS, {'is_app_running': fake_is_studio}):
            self.assertEqual(detect({}), 'studio')

    def test_detect_client_default_fallback(self):
        detect = GLOBALS['detect_client']
        with patch.dict(GLOBALS, {'is_app_running': lambda name: False}):
            self.assertEqual(detect({}), 'studio')

    def test_version_and_help(self):
        code, out, _ = self.run_cli('--version')
        self.assertEqual(code, 0)
        self.assertIn('brza', out.lower())

        code, out, _ = self.run_cli('--help')
        self.assertEqual(code, 0)
        self.assertIn('Uso:', out)
        self.assertIn('tree', out)
        self.assertIn('note', out)

        code, _, _ = self.run_cli()
        self.assertEqual(code, 2)

    def test_dispatch_to_existing_subcommand_executable(self):
        # Cria um script falso brza-custom no PATH
        custom = self.bin_dir / 'brza-custom'
        custom.write_text('#!/bin/sh\necho "custom called: $*"\nexit 0\n')
        custom.chmod(0o755)

        code, out, _ = self.run_cli('custom', 'arg1', 'arg2', env={'PATH': f'{self.bin_dir}:{os.environ["PATH"]}'})
        self.assertEqual(code, 0)
        self.assertIn('custom called: arg1 arg2', out)

    def test_dispatch_fallback_to_orca_client(self):
        fake_orca = self.bin_dir / 'orca'
        fake_orca.write_text('#!/bin/sh\necho "orca CLI dispatched: $*"\nexit 0\n')
        fake_orca.chmod(0o755)

        env = {
            'BRZA_CLIENT': 'orca',
            'PATH': f'{self.bin_dir}:{os.environ["PATH"]}',
        }
        code, out, _ = self.run_cli('plugin', 'list', env=env)
        self.assertEqual(code, 0)
        self.assertIn('orca CLI dispatched: plugin list', out)

    def test_dispatch_fallback_to_studio_client(self):
        fake_studio_bin = self.bin_dir / 'studio-brza'
        fake_studio_bin.write_text('#!/bin/sh\necho "studio CLI dispatched: $*"\nexit 0\n')
        fake_studio_bin.chmod(0o755)

        with patch.dict(GLOBALS, {'STUDIO_APP_BIN': fake_studio_bin}):
            env = {'BRZA_CLIENT': 'studio'}
            code, out, _ = self.run_cli('plugin', 'list', env=env)
            self.assertEqual(code, 0)
            self.assertIn('studio CLI dispatched: plugin list', out)

    def test_dispatch_unknown_command_missing_client_cli(self):
        with patch.dict(GLOBALS, {'STUDIO_APP_BIN': Path('/nonexistent/bin/brza')}):
            env = {
                'BRZA_CLIENT': 'studio',
                'PATH': '/bin:/usr/bin',
            }
            code, out, err = self.run_cli('inexistente', env=env)
            self.assertEqual(code, 1)
            self.assertIn('falhou:', out + err)
