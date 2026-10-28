"""Testes do claude-brza, do brza-run e do brza-install. Os do brza-run vêm dos do orca-run da Fixfy.

    python3 -m unittest discover -s scripts/brza/tests
"""
import contextlib
import io
import os
import runpy
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).parent
SCRIPTS = HERE.parent
WRAPPER = runpy.run_path(str(SCRIPTS / 'claude-brza'))
RUN = runpy.run_path(str(SCRIPTS / 'brza-run'))
INSTALL = runpy.run_path(str(SCRIPTS / 'brza-install'))


def git(*args):
    subprocess.run(['git', *args], check=True, capture_output=True)


class WrapperTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()
        self.workspace, self.studio = self.base / 'brza-workspace', self.base / 'brza-studio'
        for repo in (self.workspace, self.studio):
            repo.mkdir()
            git('-C', str(repo), 'init', '-q')
            git('-C', str(repo), '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-q', '--allow-empty', '-m', 'x')
        self.env = {'PATH': '/bin', 'BRZA_WORKSPACE': str(self.workspace), 'BRZA_STUDIO': str(self.studio)}

    def test_checkouts_and_app_worktrees_are_brza(self):
        outside = self.base / 'orca' / 'workspaces' / 'brza-studio' / 'feat'
        outside.parent.mkdir(parents=True)
        git('-C', str(self.studio), 'worktree', 'add', '-q', str(outside))
        for path in (self.workspace, self.studio / 'src', Path(str(self.studio).upper()), outside):
            self.assertTrue(WRAPPER['is_brza'](path, self.env), path)

    def test_other_repos_and_root_are_not_brza(self):
        other = self.base / 'fixfy'
        other.mkdir()
        git('-C', str(other), 'init', '-q')
        for path in (other, Path('/'), Path(str(self.studio) + '-outro')):
            self.assertFalse(WRAPPER['is_brza'](path, self.env), path)

    def test_command_adds_settings_only_inside_brza(self):
        args, out = WRAPPER['command']('/x/claude', ['-p', 'oi'], Path('/'), self.env)
        self.assertEqual((args, out), (['/x/claude', '-p', 'oi'], self.env))
        args, out = WRAPPER['command']('/x/claude', ['--input-format', 'stream-json'], self.studio, self.env)
        self.assertEqual(args, ['/x/claude', '--settings', str(self.workspace / '.claude' / 'settings.json'),
                                '--input-format', 'stream-json'])
        self.assertEqual(out['BRZA_WORKSPACE'], str(self.workspace))
        self.assertNotIn('GH_CONFIG_DIR', out)

    def test_wrapper_skips_itself_in_path(self):
        mine, real = self.base / 'mine', self.base / 'real'
        mine.mkdir()
        real.mkdir()
        (mine / 'claude').symlink_to(SCRIPTS / 'claude-brza')
        (real / 'claude').write_text('#!/bin/sh\n')
        (real / 'claude').chmod(0o755)
        with patch.dict(os.environ, {'PATH': f'{mine}:{real}'}):
            self.assertEqual(WRAPPER['real_claude'](), str(real / 'claude'))


@contextlib.contextmanager
def quiet_terminal(temp):
    """O zsh sem o ~/.zshrc de quem roda o teste, e a cópia da saída que o pty escreve direto no fd 1 calada."""
    saved, devnull = os.dup(1), os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, 1)
    try:
        with patch.dict(os.environ, {'ORCA_CHAT_SCRATCH_DIR': temp, 'SHELL': '/bin/zsh', 'ZDOTDIR': temp}):
            yield
    finally:
        os.dup2(saved, 1)
        os.close(saved)
        os.close(devnull)


class BrzaRunTest(unittest.TestCase):
    def test_clean_strips_color_and_rewritten_lines(self):
        raw = b'\x1b[32mok\x1b[0m\r\n10%\r50%\r100%\r\n\x1b]0;titulo\x07\x1b>\x1b(Bfim\r\n'
        self.assertEqual(RUN['clean'](raw), 'ok\n100%\nfim\n')

    def test_tail_keeps_last_lines_within_the_byte_cap(self):
        text = '\n'.join(f'linha {i}' for i in range(500)) + '\n'
        shown, cut = RUN['tail'](text)
        self.assertEqual((shown.split('\n')[0], shown.split('\n')[-1], cut), ('linha 300', 'linha 499', 300))
        shown, cut = RUN['tail']('\n'.join(['x' * 1000] * 50))
        self.assertLessEqual(len(shown.encode()), RUN['TAIL_BYTES'])
        self.assertEqual(cut, 50 - len(shown.split('\n')))
        self.assertEqual(RUN['tail']('  \n'), ('', 0))

    def test_fence_outgrows_backticks_in_the_output(self):
        self.assertEqual(RUN['fenced']('a ```b``` ````c', 'bash'), '`````bash\na ```b``` ````c\n`````')

    def test_report_points_to_the_full_output_only_when_cut(self):
        log = Path('/tmp/r/output.log')
        self.assertEqual(RUN['report']('ls', 0, '', log), '```bash\nls\n```\n```\n(sem saída)\n```\nSaiu com 0.')
        long = RUN['report']('make', 2, '\n'.join(map(str, range(201))), log)
        self.assertTrue(long.endswith('Saiu com 2. Cortei as 1 linhas antes destas; '
                                      'a saída inteira está em `/tmp/r/output.log`.'))

    def test_send_mutation_matches_the_app_fingerprint(self):
        # impressão digital conferida com o structuredAgentSessionPayloadFingerprint do brza-studio no node
        text = 'Rodei pelo ▶:\n```bash\nls\t-la\n```\n\x01 ção 😀   "aspas" \\ fim'
        params = RUN['send_mutation']('claude_x', text, 1, 1792900000000, '0' * 32)
        self.assertEqual(params['envelope'], {
            'sessionId': 'claude_x', 'clientOperationId': '1792900000000-' + '0' * 32, 'expectedRuntimeFence': 1,
            'payloadFingerprint': '6c1f3d3de96998c2cb1c2ed99684ed68b1cdea5a8bc9bff9955819b4535bfb31'})
        self.assertEqual(params['delivery'], 'queue-if-active')

    def test_chat_mode_runs_here_and_sends_the_blocks(self):
        calls = []

        def rpc(method, params):
            calls.append((method, params))
            return {'page': {'fence': 7}} if method == 'agentSession.history' else {}

        with tempfile.TemporaryDirectory() as temp, quiet_terminal(temp), \
                patch.object(RUN['runtime'], 'rpc', rpc), contextlib.redirect_stdout(io.StringIO()):
            code = RUN['run_in_chat']("printf 'um\\ndois\\n'; exit 3", 'claude_x')
        self.assertEqual(code, 3)
        method, params = calls[1]
        self.assertEqual((method, params['envelope']['expectedRuntimeFence']), ('agentSession.send', 7))
        self.assertEqual(params['body']['blocks'][0]['text'],
                         "Rodei pelo ▶:\n\n```bash\nprintf 'um\\ndois\\n'; exit 3\n```\n```\num\ndois\n```\nSaiu com 3.")

    def tab_run(self, command):
        calls = []

        def brza(*args):
            calls.append(args)
            if args[:2] == ('terminal', 'create'):
                # a aba do app digita o --command num shell: aqui ele roda na hora
                subprocess.run(['/bin/sh', '-c', args[args.index('--command') + 1]], capture_output=True)
            return {'terminal': {'handle': 'term-1'}} if args[1] == 'create' else {'terminals': []}

        out = io.StringIO()
        with tempfile.TemporaryDirectory() as temp, quiet_terminal(temp), \
                patch.object(RUN['runtime'], 'brza', brza), contextlib.redirect_stdout(out):
            code = RUN['run_in_tab'](command, HERE, poll=0)
        return code, calls, out.getvalue()

    def test_tab_mode_prints_blocks_and_closes_on_success(self):
        code, calls, out = self.tab_run(['echo', "'a b'", '&&', 'pwd'])
        self.assertEqual(code, 0)
        self.assertEqual(out, f"```bash\necho 'a b' && pwd\n```\n```\na b\n{HERE}\n```\nSaiu com 0.\n")
        create = calls[0]
        top = subprocess.run(['git', '-C', str(HERE), 'rev-parse', '--show-toplevel'],
                             capture_output=True, text=True).stdout.strip()
        self.assertEqual(create[create.index('--worktree') + 1], f'path:{top}')
        self.assertEqual(calls[-1], ('terminal', 'close', '--terminal', 'term-1'))

    def test_tab_mode_keeps_the_tab_on_failure(self):
        code, calls, out = self.tab_run(['exit 4'])
        self.assertEqual(code, 4)
        self.assertTrue(out.endswith('Saiu com 4.\n'))
        self.assertNotIn('close', [c[1] for c in calls])


class InstallTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        base = Path(temp.name)
        self.bin, self.workspace = base / 'bin', base / 'ws'
        (self.workspace / 'scripts' / 'brza').mkdir(parents=True)
        for name in ('claude-brza', 'brza-run'):
            (self.workspace / 'scripts' / 'brza' / name).write_text('#!/bin/sh\n')
        runtime = INSTALL['runtime']
        for attr, value in (('LOCAL_BIN', self.bin), ('WORKSPACE', self.workspace)):
            p = patch.object(runtime, attr, value)
            p.start()
            self.addCleanup(p.stop)

    def test_link_is_created_once_and_foreign_link_is_refused(self):
        with contextlib.redirect_stdout(io.StringIO()):
            INSTALL['link_command']('brza-run', False)
            self.assertEqual(INSTALL['link_state']('brza-run'), 'ok')
            INSTALL['link_command']('brza-run', False)
        (self.bin / 'claude-brza').symlink_to('/outro')
        with self.assertRaises(SystemExit), contextlib.redirect_stdout(io.StringIO()):
            INSTALL['link_command']('claude-brza', False)

    def test_dry_run_changes_nothing(self):
        calls = []
        with patch.object(INSTALL['runtime'], 'rpc', lambda *a: calls.append(a)), \
                contextlib.redirect_stdout(io.StringIO()):
            INSTALL['install_chat_command'](True)
        self.assertEqual((INSTALL['link_state']('claude-brza'), calls), ('ausente', []))

    def test_chat_command_points_the_override_to_the_link(self):
        calls = []
        with patch.object(INSTALL['runtime'], 'rpc', lambda *a: calls.append(a)), \
                contextlib.redirect_stdout(io.StringIO()):
            INSTALL['install_chat_command'](False)
        self.assertEqual(calls, [('settings.mutateAgentLaunch',
                                  {'type': 'command', 'agent': 'claude', 'value': str(self.bin / 'claude-brza')})])
        self.assertEqual(INSTALL['link_state']('claude-brza'), 'ok')


if __name__ == '__main__':
    unittest.main()
