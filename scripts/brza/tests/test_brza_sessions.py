"""Testes do brza-sessions.

    python3 -m unittest discover -s scripts/brza/tests
"""
import hashlib
import json
import os
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SESSIONS = runpy.run_path(str(Path(__file__).parent.parent / 'brza-sessions'))
# As funções leem os globais do módulo em que nasceram, não da cópia que o run_path devolve.
GLOBALS = SESSIONS['main'].__globals__


class RunningTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.sessions = Path(temp.name) / 'sessions'
        self.sessions.mkdir()
        self.dirs = patch.dict(GLOBALS, {'config_dirs': lambda: [Path(temp.name)]})
        self.dirs.start()
        self.addCleanup(self.dirs.stop)

    def write(self, name: str, pid: int):
        (self.sessions / f'{pid}.json').write_text(json.dumps({'pid': pid, 'name': name}))

    def test_a_live_session_with_the_name_is_running(self):
        self.write('pln-001-p44-p50', os.getpid())
        self.assertTrue(SESSIONS['running']('pln-001-p44-p50'))
        self.assertFalse(SESSIONS['running']('outra'))

    def test_a_dead_session_is_not_running(self):
        self.write('pln-001-p44-p50', 2 ** 22 + 1)
        self.assertFalse(SESSIONS['running']('pln-001-p44-p50'))


class ChatBlockerTest(unittest.TestCase):
    def blocker(self, checkout: Path, override):
        settings = {'settings': {'agentCmdOverrides': {'claude': override} if override else {}}}
        with patch.dict(GLOBALS, {'rpc': lambda method, params=None: settings}):
            return SESSIONS['chat_blocker'](checkout)

    def test_the_workspace_reads_its_own_settings(self):
        workspace = GLOBALS['WORKSPACE']
        self.assertIsNone(self.blocker(workspace, None))
        self.assertIsNone(self.blocker(workspace / 'plans', None))

    def test_another_checkout_needs_the_wrapper(self):
        studio = Path('/x/brza-studio')
        self.assertIn('vazio', self.blocker(studio, None))
        self.assertIn('não o claude-brza', self.blocker(studio, '/usr/local/bin/claude'))
        self.assertIsNone(self.blocker(studio, '/Users/x/.local/bin/claude-brza'))


class SendTest(unittest.TestCase):
    def test_canonical_json_sorts_keys_and_keeps_accents(self):
        self.assertEqual(SESSIONS['canonicalize']({'b': [1, 'ã'], 'a': None}), '{"a":null,"b":[1,"ã"]}')

    def test_the_message_is_queued_with_the_app_fingerprint(self):
        calls = []

        def rpc(method, params=None):
            calls.append((method, params))
            return {'page': {'fence': 7}} if method == 'agentSession.history' else {}

        with patch.object(sys.modules['brza_runtime'], 'rpc', rpc):
            SESSIONS['send_to_chat']('claude_1', 'faça a tarefa')
        method, params = calls[-1]
        fields = {'body': {'kind': 'message', 'role': 'user', 'blocks': [{'type': 'text', 'text': 'faça a tarefa'}]},
                  'delivery': 'queue-if-active'}
        payload = SESSIONS['canonicalize']({'method': 'agentSession.send', 'sessionId': 'claude_1', 'fields': fields})
        self.assertEqual(method, 'agentSession.send')
        self.assertEqual({k: params[k] for k in fields}, fields)
        self.assertEqual(params['envelope']['expectedRuntimeFence'], 7)
        self.assertEqual(params['envelope']['payloadFingerprint'], hashlib.sha256(payload.encode()).hexdigest())
        self.assertRegex(params['envelope']['clientOperationId'], r'^\d{13}-[0-9a-f]{32}$')


if __name__ == '__main__':
    unittest.main()
