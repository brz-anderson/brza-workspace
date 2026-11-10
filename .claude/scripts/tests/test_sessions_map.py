"""Testes do skillkit.sessions_map: o mapa v2 dobrado por nome (formato na docstring do módulo)."""
import json
import os
import tempfile
import unittest

import _paths  # noqa: F401
from skillkit import sessions_map

CHAT = "chat-1"


def open_row(nome="a", **kw):
    return dict({"event": "open", "name": nome, "chat": CHAT, "at": "2026-11-09T10:00:00-03:00", "dispatch": "ctx_1",
                 "run": "run_1", "sender": "s1", "coordinator": "c1", "agent": "claude", "model": "opus",
                 "effort": "high", "operation": "op-1"}, **kw)


class Fold(unittest.TestCase):
    def test_open_inicia_a_entrada_e_e_o_last_send_da_rodada_1(self):
        e = sessions_map.fold_map([open_row()])["a"]
        self.assertEqual((e["dispatch"], e["run"], e["agent"], e["closed"]), ("ctx_1", "run_1", "claude", False))
        self.assertEqual(e["last_send"]["origem"], "open")
        self.assertEqual(e["last_send"]["round_id"], "op-1")

    def test_session_traz_o_id_do_provedor_depois(self):
        e = sessions_map.fold_map([open_row(), {"event": "session", "name": "a", "chat": CHAT,
                                                  "provider_session": "uuid-1"}])["a"]
        self.assertEqual(e["provider_session"], "uuid-1")

    def test_session_de_outro_chat_nao_vale(self):
        e = sessions_map.fold_map([open_row(), {"event": "session", "name": "a", "chat": "outro",
                                                  "provider_session": "uuid-x"}])["a"]
        self.assertIsNone(e["provider_session"])

    def test_send_turn_e_close(self):
        rows = [open_row(), {"event": "send", "name": "a", "chat": CHAT, "operation": "op-2", "at": "t2",
                             "receipt": {"status": "sent"}},
                {"event": "turn", "name": "a", "chat": CHAT, "operation": "op-2", "outcome": "done", "latency_s": 7},
                {"event": "close", "name": "a", "chat": CHAT, "at": "t3"}]
        e = sessions_map.fold_map(rows)["a"]
        self.assertEqual((e["last_send"]["operation"], e["last_send"]["status"]), ("op-2", "sent"))
        self.assertEqual(e["last_turn"]["latency_s"], 7)
        self.assertEqual((e["closed"], e["closed_at"]), (True, "t3"))

    def test_close_nao_apaga_os_ids(self):
        rows = [open_row(provider_session="p1"), {"event": "close", "name": "a", "chat": CHAT, "at": "t"}]
        self.assertEqual(sessions_map.fold_map(rows)["a"]["provider_session"], "p1")

    def test_linha_v1_so_vale_sem_linha_v2(self):
        v1 = {"event": "open", "name": "velha", "dispatch_id": "ctx_old", "model": "m"}
        e = sessions_map.fold_map([v1])["velha"]
        self.assertEqual((e["dispatch"], e["legacy"]), ("ctx_old", True))
        e = sessions_map.fold_map([v1, open_row("velha")])["velha"]
        self.assertEqual((e["dispatch"], e["legacy"]), ("ctx_1", False))

    def test_dispatch_of_nao_mora_no_kit(self):
        self.assertFalse(hasattr(sessions_map, "dispatch_of"))


class Arquivo(unittest.TestCase):
    def test_read_rows_ignora_linha_ruim_e_arquivo_ausente(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "m.jsonl")
            with open(p, "w", encoding="utf-8") as f:
                f.write(json.dumps(open_row()) + "\nlixo\n[1]\n")
            self.assertEqual(len(sessions_map.read_rows(p)), 1)
            self.assertEqual(sessions_map.read_rows(os.path.join(tmp, "nada")), [])

    def test_map_file_e_load_map(self):
        self.assertEqual(sessions_map.map_file("/x", "/y/m.jsonl"), "/y/m.jsonl")
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "m.jsonl")
            with open(p, "w", encoding="utf-8") as f:
                f.write(json.dumps(open_row()) + "\n")
            self.assertIn("a", sessions_map.load_map(tmp, p))

    def test_epoch(self):
        self.assertEqual(sessions_map.epoch("2026-11-09T13:00:00-03:00"), sessions_map.epoch("2026-11-09T16:00:00Z"))
        self.assertEqual(sessions_map.epoch(1700000000000), 1700000000.0)
        self.assertIsNone(sessions_map.epoch("lixo"))
        self.assertIsNone(sessions_map.epoch(None))

    def test_common_root_vem_do_paths(self):
        from skillkit import paths
        self.assertIs(sessions_map.common_root, paths.common_root)


if __name__ == "__main__":
    unittest.main()
