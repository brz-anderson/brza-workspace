"""Testes do brza-sessions.

    python3 -m unittest discover -s scripts/brza/tests
"""
import hashlib
import io
import json
import os
import runpy
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
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



WORKTREE = '15bf3484::/Users/x/brza-workspace'


def tab(chat: str, title: str, state: str | None = 'done') -> dict:
    return {'type': 'agent-session', 'id': f'agent-session:{chat}', 'title': title, 'sessionId': chat,
            **({'chatStatus': {'state': state}} if state else {})}


class FakeApp:
    """O runtime do app: as abas do listAll, o providerSession de cada chat e as chamadas recebidas."""

    def __init__(self, tabs: list[dict], providers: dict[str, str]):
        self.tabs, self.providers, self.calls = tabs, providers, []

    def rpc(self, method, params=None):
        self.calls.append((method, params))
        if method == 'session.tabs.listAll':
            return {'snapshots': [{'worktree': WORKTREE, 'tabs': [*self.tabs, {'type': 'terminal', 'id': 't1'}]}]}
        if method == 'agentSession.history':
            chat = params['sessionId']
            provider = {'providerSession': {'key': 'session_id', 'id': self.providers[chat]}} \
                if chat in self.providers else {}
            return {'page': {'fence': 3}, **provider}
        return {'ok': True, 'closed': True}

    def methods(self) -> list[str]:
        return [method for method, _ in self.calls]


class CommandTest(unittest.TestCase):
    """O list, o send e o close sobre um app falso e transcripts num config temporário."""

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.config = Path(temp.name)
        self.app = FakeApp([tab('claude_a', 'PLN-002 P7: renomear chat', 'working'), tab('claude_b', 'Config'),
                            tab('claude_c', 'Sem nome', None)],
                           {'claude_a': 'uuid-a', 'claude_b': 'uuid-b', 'claude_c': 'uuid-c'})
        self.transcript('uuid-a', 'primeiro', 'pln-002-p7')
        self.transcript('uuid-b', 'pln-003')
        self.transcript('uuid-c')
        self.guards: dict[str, dict] = {}
        self.held: list[tuple[str, str]] = []
        patcher = patch.dict(GLOBALS, {'config_dirs': lambda: [self.config], 'rpc': self.app.rpc,
                                       'pending_guard': lambda sid: self.guards.get(sid),
                                       'hold_guard': lambda sid, text: self.held.append((sid, text))})
        patcher.start()
        self.addCleanup(patcher.stop)
        sent = patch.object(sys.modules['brza_runtime'], 'rpc', self.app.rpc)
        sent.start()
        self.addCleanup(sent.stop)

    def transcript(self, claude_id: str, *names: str):
        folder = self.config / 'projects' / '-Users-x-brza-workspace'
        folder.mkdir(parents=True, exist_ok=True)
        lines = [{'type': 'user', 'message': {'content': 'custom-title no texto não conta'}}]
        lines += [{'type': 'custom-title', 'customTitle': name, 'sessionId': claude_id} for name in names]
        (folder / f'{claude_id}.jsonl').write_text(''.join(json.dumps(line) + '\n' for line in lines))

    def run_main(self, *argv) -> tuple[int, str]:
        out = io.StringIO()
        with patch.object(sys, 'argv', ['brza-sessions', *argv]), redirect_stdout(out):
            code = SESSIONS['main']()
        return code, out.getvalue()

    def test_list_names_each_chat_by_the_last_rename_in_its_transcript(self):
        code, out = self.run_main('list', '--json')
        self.assertEqual(code, 0)
        sessions = json.loads(out)['sessions']
        self.assertEqual([s['name'] for s in sessions], ['pln-002-p7', 'pln-003', None])
        self.assertEqual(sessions[0], {'name': 'pln-002-p7', 'title': 'PLN-002 P7: renomear chat', 'chat': 'claude_a',
                                       'claude_session': 'uuid-a', 'worktree': '/Users/x/brza-workspace',
                                       'state': 'working', 'guard': None})
        self.assertIsNone(sessions[2]['state'])

    def test_list_carries_the_guard_of_an_idle_large_session(self):
        self.guards['uuid-b'] = {'idle_min': 90, 'ttl_min': 60, 'context': 200_000, 'cost_usd': 3.75}
        code, out = self.run_main('list')
        self.assertEqual(code, 0)
        self.assertIn('pln-003', out)
        self.assertIn('parada há 90 min, e o cache dura 60 min: o próximo pedido regrava 200.000 tokens, cerca de '
                      'US$ 3,75', out)
        self.assertIn('-', out.splitlines()[-1])  # o chat sem nome

    def test_a_chat_without_provider_session_is_listed_without_name(self):
        del self.app.providers['claude_c']
        sessions = json.loads(self.run_main('list', '--json')[1])['sessions']
        self.assertEqual((sessions[2]['name'], sessions[2]['claude_session']), (None, None))

    def test_send_queues_the_text_to_the_chat_found_by_name(self):
        code, out = self.run_main('send', 'pln-003', 'faça o P1', '--json')
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {'sent': True, 'name': 'pln-003', 'chat': 'claude_b'})
        method, params = self.app.calls[-1]
        self.assertEqual(method, 'agentSession.send')
        self.assertEqual(params['envelope']['sessionId'], 'claude_b')
        self.assertEqual(params['body']['blocks'][0]['text'], 'faça o P1')
        self.assertEqual(self.held, [])

    def test_send_refuses_the_session_the_guard_would_block(self):
        guard = {'idle_min': 90, 'ttl_min': 60, 'context': 200_000, 'cost_usd': 3.75}
        self.guards['uuid-b'] = guard
        code, out = self.run_main('send', 'pln-003', 'faça o P1', '--json')
        self.assertEqual(code, 3)
        self.assertEqual(json.loads(out), {'sent': False, 'name': 'pln-003', 'chat': 'claude_b', 'guard': guard})
        self.assertNotIn('agentSession.send', self.app.methods())
        code, out = self.run_main('send', 'pln-003', 'faça o P1')
        self.assertEqual(code, 3)
        self.assertIn('--wake', out)

    def test_send_wake_holds_the_passage_and_sends_once(self):
        self.guards['uuid-b'] = {'idle_min': 90, 'ttl_min': 60, 'context': 200_000, 'cost_usd': None}
        code, _ = self.run_main('send', 'pln-003', 'faça o P1', '--wake')
        self.assertEqual(code, 0)
        self.assertEqual(self.held, [('uuid-b', 'faça o P1')])
        self.assertEqual(self.app.methods().count('agentSession.send'), 1)

    def test_close_calls_both_rpcs_with_the_user_reason_and_never_resumes(self):
        code, out = self.run_main('close', 'pln-003', '--json')
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {'closed': True, 'name': 'pln-003', 'chat': 'claude_b'})
        calls = [(m, p) for m, p in self.app.calls if m in ('agentSession.close', 'session.tabs.close')]
        self.assertEqual(calls, [('agentSession.close', {'sessionId': 'claude_b'}),
                                 ('session.tabs.close', {'worktree': 'path:/Users/x/brza-workspace',
                                                         'tabId': 'agent-session:claude_b', 'reason': 'user'})])
        self.assertFalse(any('resume' in m.lower() or 'restart' in m.lower() for m in self.app.methods()))

    def test_close_refuses_a_working_chat_without_force(self):
        code, out = self.run_main('close', 'pln-002-p7', '--json')
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out), {'closed': False, 'name': 'pln-002-p7', 'chat': 'claude_a',
                                           'state': 'working'})
        self.assertNotIn('agentSession.close', self.app.methods())
        code, _ = self.run_main('close', 'pln-002-p7', '--force')
        self.assertEqual(code, 0)
        self.assertIn('session.tabs.close', self.app.methods())

    def test_an_absent_name_exits_one_with_the_error(self):
        for argv in (('send', 'nenhuma', 'x'), ('close', 'nenhuma')):
            code, out = self.run_main(*argv, '--json')
            self.assertEqual(code, 1)
            self.assertIn('nenhuma', json.loads(out)['error'])
        self.assertNotIn('agentSession.send', self.app.methods())

    def test_a_repeated_name_exits_one_and_lists_the_chats(self):
        self.transcript('uuid-c', 'pln-003')
        code, out = self.run_main('close', 'pln-003')
        self.assertEqual(code, 1)
        self.assertIn('claude_b', out)
        self.assertIn('claude_c', out)
        self.assertNotIn('agentSession.close', self.app.methods())

    def test_an_app_that_does_not_answer_exits_one(self):
        def down(method, params=None):
            raise GLOBALS['BrzaError']('session.tabs.listAll: o runtime não respondeu')

        with patch.dict(GLOBALS, {'rpc': down}):
            code, out = self.run_main('list', '--json')
        self.assertEqual(code, 1)
        self.assertIn('não respondeu', json.loads(out)['error'])

    def test_open_stays_the_default_and_takes_the_explicit_verb(self):
        for argv in (('c3-prova', '--dry-run'), ('open', 'c3-prova', '--dry-run')):
            code, out = self.run_main(*argv)
            self.assertEqual(code, 0)
            self.assertIn('abriria:  c3-prova', out)


if __name__ == '__main__':
    unittest.main()
