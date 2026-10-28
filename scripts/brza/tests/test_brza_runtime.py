"""Testes do brza_runtime: o envio ao chat, o git e o worktree do brza-studio.

    python3 -m unittest discover -s scripts/brza/tests
"""
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))
import brza_runtime as runtime  # noqa: E402


def git(*args, cwd: Path):
    return subprocess.run(['git', '-C', str(cwd), '-c', 'user.name=t', '-c', 'user.email=t@t', *args],
                          check=True, capture_output=True, text=True).stdout.strip()


class SendTest(unittest.TestCase):
    def test_canonical_json_sorts_keys_and_keeps_accents(self):
        self.assertEqual(runtime.canonicalize({'b': [1, 'ã', {'d': 2, 'c': True}], 'a': None}),
                         '{"a":null,"b":[1,"ã",{"c":true,"d":2}]}')

    def test_send_mutation_matches_the_app_fingerprint(self):
        # a mesma impressão digital do teste do brza-run, conferida no node com o brza-studio
        text = 'Rodei pelo ▶:\n```bash\nls\t-la\n```\n\x01 ção 😀 \u2028 "aspas" \\ fim'
        params = runtime.send_mutation('claude_x', text, 1, 1792900000000, '0' * 32)
        self.assertEqual(params['envelope']['payloadFingerprint'],
                         '6c1f3d3de96998c2cb1c2ed99684ed68b1cdea5a8bc9bff9955819b4535bfb31')
        self.assertEqual(params['body']['blocks'], [{'type': 'text', 'text': text}])

    def test_send_to_chat_queues_after_the_last_fence(self):
        calls = []

        def rpc(method, params=None):
            calls.append((method, params))
            return {'page': {'fence': 7}} if method == 'agentSession.history' else {}

        with patch.object(runtime, 'rpc', rpc):
            runtime.send_to_chat('claude_1', 'faça a tarefa')
        self.assertEqual([m for m, _ in calls], ['agentSession.history', 'agentSession.send'])
        params = calls[1][1]
        payload = runtime.canonicalize({'method': 'agentSession.send', 'sessionId': 'claude_1',
                                        'fields': {'body': params['body'], 'delivery': 'queue-if-active'}})
        self.assertEqual(params['envelope']['expectedRuntimeFence'], 7)
        self.assertEqual(params['envelope']['payloadFingerprint'], hashlib.sha256(payload.encode()).hexdigest())
        self.assertRegex(params['envelope']['clientOperationId'], r'^\d{13}-[0-9a-f]{32}$')


class StudioTest(unittest.TestCase):
    def test_studio_comes_from_the_environment_or_the_projects_folder(self):
        self.assertEqual(runtime.STUDIO, Path(os.environ.get('BRZA_STUDIO')
                                              or Path.home() / 'Projects' / 'brza-studio'))


class WorktreeTest(unittest.TestCase):
    """Um brza-studio de mentira: um clone de uma origin local, na master."""

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
        p = patch.object(runtime, 'STUDIO', self.studio)
        p.start()
        self.addCleanup(p.stop)

    def test_git_returns_stdout_and_turns_failure_into_brza_error(self):
        self.assertEqual(runtime.git('rev-parse', '--abbrev-ref', 'HEAD').strip(), 'master')
        with self.assertRaisesRegex(runtime.BrzaError, 'nao-existe'):
            runtime.git('rev-parse', 'nao-existe')

    def test_worktree_add_fetches_and_branches_from_origin_master(self):
        path = runtime.worktree_add(self.base / 'studio' / '.worktrees' / 'x', branch='feat/x')
        self.assertEqual(git('rev-parse', '--abbrev-ref', 'HEAD', cwd=path), 'feat/x')
        self.assertEqual(git('rev-parse', 'HEAD', cwd=path), self.tip)

    def test_worktree_add_without_branch_is_detached(self):
        path = runtime.worktree_add(self.base / 'tmp-wt')
        self.assertEqual(git('rev-parse', '--abbrev-ref', 'HEAD', cwd=path), 'HEAD')
        self.assertEqual(git('rev-parse', 'HEAD', cwd=path), self.tip)

    def test_worktree_add_without_fetch_uses_what_is_known(self):
        path = runtime.worktree_add(self.base / 'tmp-wt', fetch=False)
        self.assertNotEqual(git('rev-parse', 'HEAD', cwd=path), self.tip)

    def test_worktree_remove_takes_the_clean_worktree_and_refuses_the_dirty(self):
        clean, dirty = runtime.worktree_add(self.base / 'limpo'), runtime.worktree_add(self.base / 'sujo')
        runtime.worktree_remove(clean)
        self.assertFalse(clean.exists())
        (dirty / 'novo.txt').write_text('x')
        with self.assertRaises(runtime.BrzaError):
            runtime.worktree_remove(dirty)
        self.assertTrue(dirty.exists())


class InstallOfflineTest(unittest.TestCase):
    """O pnpm trocado por um falso, que sai com o código gravado em `code` e anota os argumentos."""

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name)
        bin_dir = self.base / 'bin'
        bin_dir.mkdir()
        pnpm = bin_dir / 'pnpm'
        pnpm.write_text(f'#!/bin/sh\necho "$(pwd -P) $*" >> {self.base}/calls\necho falhou >&2\n'
                        f'exit $(cat {self.base}/code)\n')
        pnpm.chmod(0o755)
        p = patch.dict(os.environ, {'PATH': f'{bin_dir}:/usr/bin:/bin'})
        p.start()
        self.addCleanup(p.stop)
        self.tree = self.base / 'tree'
        self.tree.mkdir()

    def test_failure_names_the_online_command_and_success_passes(self):
        (self.base / 'code').write_text('1')
        with self.assertRaisesRegex(runtime.BrzaError, 'pnpm install --frozen-lockfile'):
            runtime.install_offline(self.tree)
        (self.base / 'code').write_text('0')
        runtime.install_offline(self.tree)
        calls = (self.base / 'calls').read_text().splitlines()
        self.assertEqual(calls, [f'{self.tree.resolve()} install --offline --frozen-lockfile'] * 2)


if __name__ == '__main__':
    unittest.main()
