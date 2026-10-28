"""Testes do brza-dev, num brza-studio de mentira: um repositório com um worktree ligado, o HOME num diretório
temporário, e o pnpm e o ps trocados por falsos.

    python3 -m unittest discover -s scripts/brza/tests
"""
import contextlib
import hashlib
import io
import json
import os
import runpy
import signal
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS))
import brza_runtime as runtime  # noqa: E402

DEV = runpy.run_path(str(SCRIPTS / 'brza-dev'))
# As funções leem os globais do módulo em que nasceram, não da cópia que o run_path devolve.
GLOBALS = DEV['main'].__globals__
RUNNER = 'node /x/.worktrees/w/config/scripts/run-electron-vite-dev.mjs'


def git(*args, cwd: Path):
    subprocess.run(['git', '-C', str(cwd), '-c', 'user.name=t', '-c', 'user.email=t@t', *args],
                   check=True, capture_output=True)


class FakeProcess:
    """O pnpm dev de mentira: o returncode é None enquanto ele "vive"."""

    def __init__(self, returncode=None):
        self.returncode = returncode

    def poll(self):
        return self.returncode


class DevTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()
        self.studio, self.home = self.base / 'studio', self.base / 'home'
        self.home.mkdir()
        self.studio.mkdir()
        git('init', '-q', '-b', 'master', cwd=self.studio)
        git('commit', '-q', '--allow-empty', '-m', 'um', cwd=self.studio)
        self.tree = self.studio / '.worktrees' / 'w'
        git('worktree', 'add', '-q', '--detach', str(self.tree), cwd=self.studio)
        (self.tree / 'node_modules').mkdir()

        self.processes = {}      # pid → comando, o que o ps falso enxerga
        self.launched = []       # (raiz, env, log) de cada pnpm dev
        self.killed = []         # (pid, sinal)
        self.announce_pid = 4242  # o runnerPid que o pnpm dev falso anuncia
        self.process = FakeProcess()
        env = {k: v for k, v in os.environ.items()
               if not k.startswith(('ORCA_DEV_', 'ORCA_BACKGROUND'))}
        env['HOME'] = str(self.home)
        for p in (patch.object(runtime, 'STUDIO', self.studio),
                  patch.dict(os.environ, env, clear=True),
                  patch.dict(GLOBALS, {'process_command': self.processes.get, 'launch': self.fake_launch,
                                       'signal_runner': self.fake_kill, 'POLL': 0, 'START_TIMEOUT': 0.2,
                                       'STOP_TIMEOUT': 0.2})):
            p.start()
            self.addCleanup(p.stop)

    def fake_launch(self, root: Path, env: dict, log: Path):
        self.launched.append((root, env, log))
        if self.announce_pid is not None:
            self.write_record(self.announce_pid)
            self.processes[self.announce_pid] = RUNNER
        return self.process

    def fake_kill(self, pid: int, sig: int):
        self.killed.append((pid, sig))
        self.processes.pop(pid, None)

    def write_record(self, pid: int):
        out = self.tree / 'out'
        out.mkdir(exist_ok=True)
        (out / 'dev-instance.json').write_text(json.dumps({
            'userData': str(self.profile()), 'profile': 'worktree', 'rendererPort': 15210,
            'rendererUrl': 'http://localhost:15210', 'cdpPort': 9340, 'cdpUrl': 'http://127.0.0.1:9340',
            'repoRoot': str(self.tree), 'runnerPid': pid}))

    def profile(self) -> Path:
        name = hashlib.sha1(str(self.tree).encode()).hexdigest()[:10]
        return self.home / 'Library' / 'Application Support' / 'brza-dev-wt' / name

    def seed_profile(self):
        self.profile().mkdir(parents=True)
        (self.profile() / 'orca-profile-index.json').write_text('{}')

    def run_dev(self, *argv) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            try:
                code = GLOBALS['main'](list(argv))
            except SystemExit as e:
                code = e.code
        return code, out.getvalue()

    # subir

    def test_seeds_only_the_empty_profile(self):
        code, out = self.run_dev(str(self.tree))
        self.assertEqual(code, 0, out)
        (root, env, log), = self.launched
        self.assertEqual(root, self.tree)
        self.assertEqual(env.get('ORCA_DEV_SEED_PROFILE'), '1')
        self.assertEqual(log, self.tree / 'out' / 'brza-dev.log')
        self.assertIn('4242', out)
        self.assertIn('http://localhost:15210', out)

    def test_profile_with_state_is_not_seeded(self):
        self.seed_profile()
        code, out = self.run_dev(str(self.tree))
        self.assertEqual(code, 0, out)
        self.assertNotIn('ORCA_DEV_SEED_PROFILE', self.launched[0][1])

    def test_no_seed_skips_the_seed(self):
        code, out = self.run_dev(str(self.tree), '--no-seed')
        self.assertEqual(code, 0, out)
        self.assertNotIn('ORCA_DEV_SEED_PROFILE', self.launched[0][1])

    def test_reset_removes_the_profile_and_seeds_again(self):
        self.seed_profile()
        code, out = self.run_dev(str(self.tree), '--reset')
        self.assertEqual(code, 0, out)
        self.assertFalse(self.profile().exists())
        self.assertEqual(self.launched[0][1].get('ORCA_DEV_SEED_PROFILE'), '1')

    def test_visible_by_default_and_background_sets_the_flag(self):
        self.run_dev(str(self.tree))
        self.assertNotIn('ORCA_BACKGROUND_LAUNCH', self.launched[0][1])
        self.processes.clear()
        code, out = self.run_dev(str(self.tree), '--background')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.launched[1][1].get('ORCA_BACKGROUND_LAUNCH'), '1')

    def test_inherited_dev_instance_env_is_dropped(self):
        with patch.dict(os.environ, {'ORCA_DEV_USER_DATA_PATH': '/outro', 'ORCA_DEV_INSTANCE_KEY': '/outro',
                                     'ORCA_DEV_REPO_ROOT': '/outro', 'ORCA_BACKGROUND_LAUNCH': '1'}):
            self.run_dev(str(self.tree))
        env = self.launched[0][1]
        for key in ('ORCA_DEV_USER_DATA_PATH', 'ORCA_DEV_INSTANCE_KEY', 'ORCA_DEV_REPO_ROOT',
                    'ORCA_BACKGROUND_LAUNCH'):
            self.assertNotIn(key, env)

    def test_defaults_to_the_worktree_of_the_current_directory(self):
        (self.tree / 'src').mkdir()
        cwd = os.getcwd()
        os.chdir(self.tree / 'src')
        self.addCleanup(os.chdir, cwd)
        code, out = self.run_dev()
        self.assertEqual(code, 0, out)
        self.assertEqual(self.launched[0][0], self.tree)

    def test_refuses_with_a_live_build(self):
        self.write_record(77)
        self.processes[77] = RUNNER
        code, out = self.run_dev(str(self.tree))
        self.assertEqual(code, 1)
        self.assertEqual(self.launched, [])
        self.assertIn('77', out)

    def test_stale_record_does_not_block(self):
        self.write_record(77)  # o runner que saiu deixa o registro, e o pid 77 não vive
        code, out = self.run_dev(str(self.tree))
        self.assertEqual(code, 0, out)
        self.assertEqual(len(self.launched), 1)

    def test_refuses_the_main_checkout_and_other_repos(self):
        code, out = self.run_dev(str(self.studio))
        self.assertEqual(code, 1)
        self.assertIn('checkout principal', out)
        other = self.base / 'outro'
        other.mkdir()
        git('init', '-q', cwd=other)
        code, out = self.run_dev(str(other))
        self.assertEqual(code, 1)
        self.assertIn('não é um worktree do brza-studio', out)
        self.assertEqual(self.launched, [])

    def test_refuses_without_node_modules(self):
        (self.tree / 'node_modules').rmdir()
        code, out = self.run_dev(str(self.tree))
        self.assertEqual(code, 1)
        self.assertIn('pnpm install', out)
        self.assertEqual(self.launched, [])

    def test_build_that_dies_before_announcing_fails_with_the_log(self):
        self.announce_pid = None
        self.process = FakeProcess(returncode=1)
        (self.tree / 'out').mkdir()
        (self.tree / 'out' / 'brza-dev.log').write_text('linha um\nerro: o build quebrou\n')
        code, out = self.run_dev(str(self.tree))
        self.assertEqual(code, 1)
        self.assertIn('o build quebrou', out)

    def test_slow_build_returns_with_the_log_path(self):
        self.announce_pid = None
        code, out = self.run_dev(str(self.tree))
        self.assertEqual(code, 0, out)
        self.assertIn('brza-dev.log', out)

    # parar

    def test_stop_terminates_the_live_runner(self):
        self.write_record(77)
        self.processes[77] = RUNNER
        code, out = self.run_dev('--stop', str(self.tree))
        self.assertEqual(code, 0, out)
        self.assertEqual(self.killed, [(77, signal.SIGTERM)])

    def test_stop_with_a_dead_pid_says_there_is_no_build(self):
        self.write_record(77)
        code, out = self.run_dev('--stop', str(self.tree))
        self.assertEqual(code, 0, out)
        self.assertEqual(self.killed, [])
        self.assertIn('não há build', out)

    def test_stop_never_kills_a_pid_of_another_process(self):
        self.write_record(77)
        self.processes[77] = '/usr/bin/vim notas.md'
        code, out = self.run_dev('--stop', str(self.tree))
        self.assertEqual(code, 0, out)
        self.assertEqual(self.killed, [])
        self.assertIn('não há build', out)

    def test_stop_without_a_record_says_there_is_no_build(self):
        code, out = self.run_dev('--stop', str(self.tree))
        self.assertEqual(code, 0, out)
        self.assertIn('não há build', out)

    def test_stop_fails_when_the_runner_outlives_the_wait(self):
        self.write_record(77)
        self.processes[77] = RUNNER
        GLOBALS_KILL = lambda pid, sig: self.killed.append((pid, sig))  # noqa: E731 — o runner não sai
        with patch.dict(GLOBALS, {'signal_runner': GLOBALS_KILL}):
            code, out = self.run_dev('--stop', str(self.tree))
        self.assertEqual(code, 1)
        self.assertIn('77', out)

    # estado

    def test_status_shows_the_live_build(self):
        self.write_record(77)
        self.processes[77] = RUNNER
        code, out = self.run_dev('--status', str(self.tree))
        self.assertEqual(code, 0, out)
        for part in ('77', 'http://localhost:15210', 'http://127.0.0.1:9340', str(self.profile())):
            self.assertIn(part, out)

    def test_status_says_stopped(self):
        self.write_record(77)
        code, out = self.run_dev('--status', str(self.tree))
        self.assertEqual(code, 0, out)
        self.assertIn('parado', out)

    # uso

    def test_stop_and_status_take_no_start_flags(self):
        code, _ = self.run_dev('--stop', '--status')
        self.assertEqual(code, 2)
        code, _ = self.run_dev('--stop', '--reset')
        self.assertEqual(code, 2)


if __name__ == '__main__':
    unittest.main()
