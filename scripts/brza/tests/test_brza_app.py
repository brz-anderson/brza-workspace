"""Testes do brza-app, num brza-studio de mentira: um clone de uma origin local, com o install, o build, a pergunta e os
processos do app trocados por falsos, e um /Applications temporário. O ditto é o de verdade.

    python3 -m unittest discover -s scripts/brza/tests
"""
import contextlib
import io
import os
import plistlib
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

APP_SCRIPT = runpy.run_path(str(SCRIPTS / 'brza-app'))
# As funções leem os globais do módulo em que nasceram, não da cópia que o run_path devolve.
GLOBALS = APP_SCRIPT['main'].__globals__


def git(*args, cwd: Path):
    return subprocess.run(['git', '-C', str(cwd), '-c', 'user.name=t', '-c', 'user.email=t@t', *args],
                          check=True, capture_output=True, text=True).stdout.strip()


def make_app(path: Path, version: str, extra: str | None = None):
    (path / 'Contents').mkdir(parents=True)
    with open(path / 'Contents' / 'Info.plist', 'wb') as f:
        plistlib.dump({'CFBundleShortVersionString': version}, f)
    if extra:
        (path / 'Contents' / extra).write_text(extra)


class AppInstallTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()
        origin, seed, self.studio = self.base / 'origin.git', self.base / 'seed', self.base / 'studio'
        subprocess.run(['git', 'init', '-q', '--bare', '-b', 'master', str(origin)], check=True)
        subprocess.run(['git', 'clone', '-q', str(origin), str(seed)], check=True, capture_output=True)
        git('commit', '-q', '--allow-empty', '-m', 'um', cwd=seed)
        git('push', '-q', 'origin', 'HEAD:master', cwd=seed)
        subprocess.run(['git', 'clone', '-q', str(origin), str(self.studio)], check=True)
        # um commit que só chega ao studio pelo fetch
        git('commit', '-q', '--allow-empty', '-m', 'dois', cwd=seed)
        git('push', '-q', 'origin', 'HEAD:master', cwd=seed)
        self.tip = git('rev-parse', 'HEAD', cwd=seed)

        self.app = self.base / 'Applications' / 'BrzA Studio.app'
        make_app(self.app, '1.0.0-velho', extra='so-no-velho')
        self.downloads = self.base / 'Downloads'
        self.downloads.mkdir()
        self.tmp = self.base / 'tmp'
        self.tmp.mkdir()

        self.events = []
        self.pids, self.pids_after_build = [], None
        self.build_ok, self.answer = True, True
        self.install_error = None
        self.built_in = []
        for p in (patch.object(runtime, 'STUDIO', self.studio),
                  patch.object(runtime, 'install_offline', self.fake_install),
                  patch.object(tempfile, 'tempdir', str(self.tmp)),
                  patch.dict(GLOBALS, {'APP': self.app, 'DOWNLOADS': self.downloads, 'app_pids': self.fake_pids,
                                       'build': self.fake_build, 'ask': self.fake_ask,
                                       'ditto': self.spy_ditto(GLOBALS['ditto'])})):
            p.start()
            self.addCleanup(p.stop)

    def fake_install(self, path: Path):
        self.events.append('install')
        if self.install_error:
            raise runtime.BrzaError(self.install_error)

    def fake_pids(self):
        return self.pids

    def fake_build(self, src: Path, dmg: bool) -> bool:
        self.events.append(f'build dmg={dmg}')
        self.built_in.append((src, git('rev-parse', 'HEAD', cwd=src)))
        if self.pids_after_build is not None:
            self.pids = self.pids_after_build
        if not self.build_ok:
            return False
        make_app(GLOBALS['built_app'](src), '2.0.0-novo')
        if dmg:
            (src / 'dist' / 'brza-studio-macos-arm64.dmg').write_text('dmg')
        return True

    def fake_ask(self, question: str) -> bool:
        self.events.append('ask')
        self.question = question
        return self.answer

    def spy_ditto(self, real):
        def ditto(source, target):
            self.events.append('ditto')
            return real(source, target)
        return ditto

    def run_app(self, *argv) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            try:
                code = GLOBALS['main'](['install', *argv])
            except SystemExit as e:
                code = e.code
        return code, out.getvalue()

    def installed_version(self) -> str:
        return GLOBALS['version'](self.app)

    def worktrees(self) -> list[str]:
        return [line for line in git('worktree', 'list', '--porcelain', cwd=self.studio).splitlines()
                if line.startswith('worktree ')]

    def assert_temp_gone(self):
        self.assertEqual(len(self.worktrees()), 1, self.worktrees())
        self.assertEqual(list(self.tmp.iterdir()), [])

    # o caminho feliz

    def test_builds_fetched_origin_master_in_temp_worktree_asks_and_replaces_app(self):
        code, out = self.run_app()
        self.assertEqual(code, 0, out)
        src, head = self.built_in[0]
        self.assertEqual(head, self.tip)
        self.assertTrue(src.is_relative_to(self.tmp))
        self.assertEqual(self.events, ['install', 'build dmg=False', 'ask', 'ditto'])
        self.assertIn('2.0.0-novo', self.question)
        self.assertIn('1.0.0-velho', self.question)
        self.assertEqual(self.installed_version(), '2.0.0-novo')
        # apaga antes de copiar: o arquivo que só o velho tinha não sobra
        self.assertFalse((self.app / 'Contents' / 'so-no-velho').exists())
        self.assert_temp_gone()

    def test_no_answer_keeps_installed_app(self):
        self.answer = False
        code, out = self.run_app()
        self.assertEqual(code, 1, out)
        self.assertNotIn('ditto', self.events)
        self.assertEqual(self.installed_version(), '1.0.0-velho')
        self.assert_temp_gone()

    def test_installs_when_nothing_is_installed(self):
        subprocess.run(['rm', '-rf', str(self.app)], check=True)
        code, out = self.run_app()
        self.assertEqual(code, 0, out)
        self.assertIn('nenhuma', self.question)
        self.assertEqual(self.installed_version(), '2.0.0-novo')

    # o app aberto

    def test_refuses_open_app_without_yes_before_building(self):
        self.pids = [4242]
        code, out = self.run_app()
        self.assertEqual(code, 2, out)
        self.assertIn('4242', out)
        self.assertEqual(self.events, [])
        self.assertEqual(self.installed_version(), '1.0.0-velho')
        self.assert_temp_gone()

    def test_refuses_app_opened_during_build(self):
        self.pids_after_build = [4242]
        code, out = self.run_app()
        self.assertEqual(code, 2, out)
        self.assertNotIn('ditto', self.events)
        self.assertEqual(self.installed_version(), '1.0.0-velho')
        self.assert_temp_gone()

    def test_yes_installs_over_open_app_without_asking(self):
        self.pids = [4242]
        code, out = self.run_app('--yes')
        self.assertEqual(code, 0, out)
        self.assertNotIn('ask', self.events)
        self.assertEqual(self.installed_version(), '2.0.0-novo')

    def test_app_pids_leaves_out_this_process_and_its_parents(self):
        def fake_run(cmd, **kwargs):
            self.assertEqual(cmd[:2], ['pgrep', '-f'])
            self.assertEqual(cmd[2], f'{self.app}/Contents/')
            return subprocess.CompletedProcess(cmd, 0, stdout='42\n77\n', stderr='')
        with patch.dict(GLOBALS, {'app_pids': APP_SCRIPT['app_pids'], 'ancestors': lambda: {os.getpid(), 42}}), \
                patch('subprocess.run', fake_run):
            self.assertEqual(GLOBALS['app_pids'](), [77])

    def test_ancestors_has_this_process_and_its_parent(self):
        mine = APP_SCRIPT['ancestors']()
        self.assertIn(os.getpid(), mine)
        self.assertIn(os.getppid(), mine)

    # as falhas

    def test_failed_build_removes_temp_worktree_and_keeps_app(self):
        self.build_ok = False
        code, out = self.run_app()
        self.assertEqual(code, 1, out)
        self.assertNotIn('ask', self.events)
        self.assertEqual(self.installed_version(), '1.0.0-velho')
        self.assert_temp_gone()

    def test_failed_offline_install_removes_temp_worktree(self):
        self.install_error = 'o install offline falhou'
        code, out = self.run_app()
        self.assertEqual(code, 1, out)
        self.assertIn('o install offline falhou', out)
        self.assertEqual(self.built_in, [])
        self.assert_temp_gone()

    def test_failed_ditto_keeps_temp_worktree_and_prints_the_ditto(self):
        with patch.dict(GLOBALS, {'ditto': lambda source, target: False}):
            code, out = self.run_app()
        self.assertEqual(code, 1, out)
        src = self.built_in[0][0]
        self.assertIn(f"ditto '{GLOBALS['built_app'](src)}' '{self.app}'", out)
        self.assertTrue(GLOBALS['built_app'](src).is_dir())
        self.assertEqual(len(self.worktrees()), 2)

    def test_interrupted_swap_keeps_the_new_build_and_prints_the_ditto(self):
        for error in (OSError('rmtree parcial'), KeyboardInterrupt()):
            with self.subTest(error=type(error).__name__):
                self.built_in.clear()

                def broken(source, target, error=error):
                    raise error

                with patch.dict(GLOBALS, {'ditto': broken}):
                    code, out = self.run_app()
                self.assertEqual(code, 1, out)
                src = self.built_in[0][0]
                self.assertTrue(GLOBALS['built_app'](src).is_dir())
                self.assertIn(f"ditto '{GLOBALS['built_app'](src)}' '{self.app}'", out)
                self.assertNotIn('Traceback', out)

    # --from, --clean e --dmg

    def test_from_builds_in_checkout_without_worktree_and_keeps_dist(self):
        checkout = self.base / 'checkout'
        checkout.mkdir()
        (checkout / 'package.json').write_text('{}')
        with patch.dict(GLOBALS, {'build': self.build_without_git(checkout)}):
            code, out = self.run_app('--from', str(checkout), '--yes')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.events, ['build', 'ditto'])
        self.assertTrue((checkout / 'dist').is_dir())
        self.assertEqual(len(self.worktrees()), 1)

    def test_clean_removes_dist_of_from(self):
        checkout = self.base / 'checkout'
        checkout.mkdir()
        (checkout / 'package.json').write_text('{}')
        with patch.dict(GLOBALS, {'build': self.build_without_git(checkout)}):
            code, out = self.run_app('--from', str(checkout), '--yes', '--clean')
        self.assertEqual(code, 0, out)
        self.assertFalse((checkout / 'dist').exists())
        self.assertEqual(self.installed_version(), '2.0.0-novo')

    def build_without_git(self, checkout: Path):
        def build(src, dmg):
            self.events.append('build')
            self.assertEqual(src, checkout.resolve())
            make_app(GLOBALS['built_app'](src), '2.0.0-novo')
            return True
        return build

    def test_from_must_be_a_checkout(self):
        code, out = self.run_app('--from', str(self.base / 'nada'))
        self.assertEqual(code, 2, out)
        self.assertEqual(self.events, [])

    def test_dmg_builds_with_dmg_and_copies_it_to_downloads(self):
        code, out = self.run_app('--dmg', '--yes')
        self.assertEqual(code, 0, out)
        self.assertIn('build dmg=True', self.events)
        self.assertEqual((self.downloads / 'brza-studio-macos-arm64.dmg').read_text(), 'dmg')
        self.assert_temp_gone()


if __name__ == '__main__':
    unittest.main()
