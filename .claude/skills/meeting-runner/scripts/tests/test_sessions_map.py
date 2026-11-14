"""Testes do sessions_map.py: o mapa do `brza sessions` v2 dobrado por nome, com o mapa REAL da sonda como fixture."""
import json
import os
import unittest

import _paths  # noqa: F401
from _paths import fixture

try:
    import sessions_map
except ImportError:  # snapshot anterior ao v2: cada teste falha por si
    sessions_map = None


def linhas(*rows):
    return list(rows)


class Real(unittest.TestCase):
    def setUp(self):
        self.rows = sessions_map.read_rows(fixture("v2", "smoke-sessions.jsonl"))
        self.e = sessions_map.fold_map(self.rows)

    def test_open_session_send_turn_do_mapa_real(self):
        e = self.e["pln017-smoke"]
        self.assertEqual((e["dispatch"], e["run"], e["agent"]), ("ctx_559e9e198a7e", "run_7ec4f06af9d7", "codex"))
        self.assertEqual(e["sender"], "structworker_3638f9ef-3b18-4459-a21f-cd000de3451b")
        self.assertEqual(e["coordinator"], "orca_session_id:9e9e3082-55be-4d10-b0a4-8796db1798a7")
        self.assertEqual(e["provider_session"], "01a1c117-511e-7c20-bb9f-31d820660b33")  # do `session`, depois do open
        self.assertIsNone(e["claude_session"])
        self.assertEqual(e["last_send"]["status"], "pending")
        self.assertEqual(e["last_send"]["round_id"], "1794240948436-4c48e69720b745198ffffda8a61a1832")
        self.assertEqual(e["last_turn"]["latency_s"], 32.063)
        self.assertEqual(e["opened"], "2026-11-09T13:14:54.497-03:00")

    def test_um_run_so_para_as_duas_sessoes(self):
        self.assertEqual({v["run"] for v in self.e.values()}, {"run_7ec4f06af9d7"})

    def test_o_open_e_o_last_send_da_rodada_1(self):
        e = self.e["pln017-smoke-inicial"]
        self.assertEqual(e["last_send"]["origem"], "open")
        self.assertEqual(e["last_send"]["round_id"], "1794241207153-8e351738a38e46ce8d32b62e6e427adc")
        self.assertEqual(e["last_send"]["at"], "2026-11-09T13:20:08.695-03:00")


class Dobra(unittest.TestCase):
    def test_close_marca_sem_apagar_os_ids(self):
        e = sessions_map.fold_map(linhas(
            {"event": "open", "at": "2026-11-09T10:00:00-03:00", "name": "a", "chat": "c1", "dispatch": "d1", "run": "r",
             "agent": "claude", "claude_session": None},
            {"event": "session", "at": "t", "name": "a", "chat": "c1", "provider_session": "uuid", "claude_session": "uuid"},
            {"event": "close", "at": "2026-11-09T11:00:00-03:00", "name": "a", "chat": "c1"}))["a"]
        self.assertTrue(e["closed"])
        self.assertEqual((e["claude_session"], e["provider_session"], e["dispatch"]), ("uuid", "uuid", "d1"))
        self.assertEqual(e["closed_at"], "2026-11-09T11:00:00-03:00")

    def test_open_novo_substitui_a_entrada_do_nome(self):
        e = sessions_map.fold_map(linhas(
            {"event": "open", "name": "a", "chat": "c1", "dispatch": "d1"},
            {"event": "close", "name": "a", "chat": "c1"},
            {"event": "open", "name": "a", "chat": "c2", "dispatch": "d2"}))["a"]
        self.assertEqual((e["chat"], e["dispatch"], e["closed"]), ("c2", "d2", False))

    def test_session_de_outro_chat_nao_vale(self):
        e = sessions_map.fold_map(linhas(
            {"event": "open", "name": "a", "chat": "c2", "dispatch": "d2"},
            {"event": "session", "name": "a", "chat": "c1", "provider_session": "velho"}))["a"]
        self.assertIsNone(e["provider_session"])

    def test_linha_v1_so_vale_sem_linha_v2(self):
        v1 = {"event": "open", "name": "a", "dispatch_id": "legado", "via": "worker-start"}
        so_v1 = sessions_map.fold_map(linhas(v1))["a"]
        self.assertEqual((so_v1["dispatch"], so_v1["legacy"]), ("legado", True))
        com_v2 = sessions_map.fold_map(linhas(v1, {"event": "open", "name": "a", "chat": "c", "dispatch": "novo"}))["a"]
        self.assertEqual((com_v2["dispatch"], com_v2["legacy"]), ("novo", False))

    def test_dispatch_of_prefere_o_mapa_v2_depois_o_manifesto_depois_o_legado(self):
        ent = sessions_map.fold_map(linhas({"event": "open", "name": "a", "chat": "c", "dispatch": "v2"},
                                           {"event": "open", "name": "b", "dispatch_id": "v1"}))
        f = sessions_map.dispatch_of
        self.assertEqual(f({"sessao": "a", "dispatch_id": "man"}, ent), "v2")
        self.assertEqual(f({"sessao": "b", "dispatch_id": "man"}, ent), "man")
        self.assertEqual(f({"sessao": "b"}, ent), "v1")
        self.assertIsNone(f({"sessao": "c"}, ent))

    def test_fixture_antiga_sem_chat_nos_session_continua_valendo(self):
        e = sessions_map.fold_map(sessions_map.read_rows(fixture("sessions-mini.jsonl")))
        self.assertEqual(e["mcp-muralha"]["claude_session"], "claude-aaa")
        self.assertEqual(e["mcp-regua"]["provider_session"], "prov-regua")

    def test_epoch_e_map_file(self):
        self.assertEqual(sessions_map.epoch("2026-11-09T13:00:00-03:00"), sessions_map.epoch("2026-11-09T16:00:00Z"))
        self.assertIsNone(sessions_map.epoch("lixo"))
        self.assertEqual(sessions_map.map_file("/x", "/y/m.jsonl"), "/y/m.jsonl")


if __name__ == "__main__":
    unittest.main()
