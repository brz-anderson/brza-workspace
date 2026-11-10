"""Testes do skillkit.sessions_cli: o argv do `brza sessions` v2 e os corredores (com `subprocess.run` trocado)."""
import json
import subprocess
import unittest

import _paths  # noqa: F401
from skillkit import sessions_cli


class Resultado:
    def __init__(self, rc=0, out="", err=""):
        self.returncode, self.stdout, self.stderr = rc, out, err


class Argv(unittest.TestCase):
    def test_open_argv(self):
        a = sessions_cli.open_argv("p1", agent="claude", checkout=".worktrees/x", prompt_file="/p.txt", title="T",
                                   model="opus", effort="high")
        self.assertEqual(a, ["p1", "--agent", "claude", "--checkout", ".worktrees/x", "--prompt-file", "/p.txt",
                             "--title", "T", "--wait", "--model", "opus", "--effort", "high"])

    def test_open_argv_sem_modelo_e_com_rename(self):
        a = sessions_cli.open_argv("p1", agent="antigravity", checkout="c", prompt_file="/p", title="T", rename=True)
        self.assertNotIn("--model", a)
        self.assertNotIn("--effort", a)
        self.assertEqual(a[-1], "--rename")

    def test_send_argv(self):
        self.assertEqual(sessions_cli.send_argv(["a", "b"], text="oi"), ["send", "a", "b", "--text", "oi", "--json"])
        self.assertEqual(sessions_cli.send_argv(["a"], file="/f.md", operation="op"),
                         ["send", "a", "--file", "/f.md", "--json", "--operation", "op"])

    def test_send_argv_pede_text_ou_file(self):
        with self.assertRaises(ValueError):
            sessions_cli.send_argv(["a"])
        with self.assertRaises(ValueError):
            sessions_cli.send_argv(["a"], text="x", file="y")

    def test_wait_argv(self):
        self.assertEqual(sessions_cli.wait_argv(["a", "b"], 180), ["wait", "a", "b", "--any", "--timeout", "180", "--json"])
        self.assertEqual(sessions_cli.wait_argv(["a"], -5, any_=False, markers=("w.md:fim", "x:y")),
                         ["wait", "a", "--marker", "w.md:fim", "--marker", "x:y", "--timeout", "0", "--json"])

    def test_close_argv(self):
        self.assertEqual(sessions_cli.close_argv("a"), ["close", "a", "--json"])
        self.assertEqual(sessions_cli.close_argv("a", "stop"), ["close", "a", "--force", "--json"])
        self.assertEqual(sessions_cli.close_argv("a", "keep-open"), ["close", "a", "--keep-open", "--json"])


class Interpreta(unittest.TestCase):
    def test_abertura(self):
        f = sessions_cli.interpreta_abertura
        self.assertEqual(f(0, "opened: a\n", ""), "aberta")
        self.assertEqual(f(0, "running: a\n", ""), "ja")
        self.assertEqual(f(1, "", "CHECK: a não abriu: x"), "nao-abriu")
        self.assertEqual(f(1, "", "não deu a sessão em 60s"), "sem-id")
        self.assertEqual(f(2, "", "outro"), "falha")


class Corredores(unittest.TestCase):
    def setUp(self):
        self.run = subprocess.run
        self.visto = []

    def tearDown(self):
        subprocess.run = self.run

    def troca(self, resultado):
        def fake(argv, **kw):
            self.visto.append(argv)
            if isinstance(resultado, Exception):
                raise resultado
            return resultado
        subprocess.run = fake

    def test_run_sessions_e_run_brza(self):
        self.troca(Resultado(0, "ok", ""))
        self.assertEqual(sessions_cli.run_sessions(["list"]), (0, "ok", ""))
        self.assertEqual(sessions_cli.run_brza(["orchestration", "worker-show"]), (0, "ok", ""))
        self.assertEqual(self.visto, [[sessions_cli.BRZA, "sessions", "list"],
                                      [sessions_cli.BRZA, "orchestration", "worker-show"]])

    def test_sem_brza_vira_127(self):
        self.troca(FileNotFoundError("brza"))
        rc, out, err = sessions_cli.run_sessions(["list"])
        self.assertEqual((rc, out), (127, ""))
        self.assertIn("brza", err)

    def test_wait_brza_devolve_o_json(self):
        self.troca(Resultado(0, json.dumps({"done": ["a"], "pending": [], "events": []})))
        rc, d = sessions_cli.wait_brza(["a"], 60, markers=("w:x",))
        self.assertEqual((rc, d["done"]), (0, ["a"]))
        self.assertEqual(self.visto[0][2:], ["wait", "a", "--any", "--marker", "w:x", "--timeout", "60", "--json"])

    def test_wait_brza_sem_binario_sem_json_e_json_estranho(self):
        self.troca(FileNotFoundError("brza"))
        self.assertEqual(sessions_cli.wait_brza(["a"], 1)[0], 127)
        self.troca(Resultado(1, "CHECK: x", ""))
        rc, d = sessions_cli.wait_brza(["a"], 1)
        self.assertEqual(rc, 1)
        self.assertIn("saída sem JSON", d["error"])
        self.troca(Resultado(0, "[1]"))
        self.assertEqual(sessions_cli.wait_brza(["a"], 1), (0, {"error": "JSON inesperado"}))

    def test_list_states_de_arquivo(self):
        import os
        import tempfile
        lista = {"sessions": [{"name": "a", "state": "working"}, {"name": "z", "state": "idle"},
                              {"name": "x", "state": "done", "provider_session": "P"}]}
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "l.json")
            with open(p, "w", encoding="utf-8") as f:
                json.dump(lista, f)
            self.assertEqual(sessions_cli.list_states(["a", "b"], list_json=p), {"a": "working"})
            self.assertEqual(sessions_cli.list_states(["a", "b"], list_json=p, ids={"b": {"P", None}}),
                             {"a": "working", "b": "done"})
            self.assertEqual(sessions_cli.list_states(["a"], list_json=os.path.join(tmp, "nada")), {})

    def test_list_states_pelo_comando(self):
        self.troca(Resultado(0, json.dumps({"sessions": [{"name": "a", "state": "idle"}]})))
        self.assertEqual(sessions_cli.list_states(["a"]), {"a": "idle"})
        self.assertEqual(self.visto[0], [sessions_cli.BRZA, "sessions", "list", "--json"])
        self.troca(Resultado(0, "não é json"))
        self.assertEqual(sessions_cli.list_states(["a"]), {})


if __name__ == "__main__":
    unittest.main()
