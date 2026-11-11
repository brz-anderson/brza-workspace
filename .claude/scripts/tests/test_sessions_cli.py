"""Testes do skillkit.sessions_cli: o argv do `brza sessions` v2 e os corredores (com `subprocess.run` trocado)."""
import json
import subprocess
import unittest

import _paths  # noqa: F401
from skillkit import sessions_cli


class ResultCase:
    def __init__(self, rc=0, out="", err=""):
        self.returncode, self.stdout, self.stderr = rc, out, err


class Argv(unittest.TestCase):
    def test_open_argv(self):
        a = sessions_cli.open_argv("p1", agent="claude", checkout=".worktrees/x", prompt_file="/p.txt", title="T",
                                   model="opus", effort="high")
        self.assertEqual(a, ["p1", "--agent", "claude", "--checkout", ".worktrees/x", "--prompt-file", "/p.txt",
                             "--title", "T", "--wait", "--model", "opus", "--effort", "high"])

    def test_open_argv_without_model_and_with_rename(self):
        a = sessions_cli.open_argv("p1", agent="antigravity", checkout="c", prompt_file="/p", title="T", rename=True)
        self.assertNotIn("--model", a)
        self.assertNotIn("--effort", a)
        self.assertEqual(a[-1], "--rename")

    def test_send_argv(self):
        self.assertEqual(sessions_cli.send_argv(["a", "b"], text="oi"), ["send", "a", "b", "--text", "oi", "--json"])
        self.assertEqual(sessions_cli.send_argv(["a"], file="/f.md", operation="op"),
                         ["send", "a", "--file", "/f.md", "--json", "--operation", "op"])

    def test_send_argv_asks_text_or_file(self):
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


class InterpretOpen(unittest.TestCase):
    def test_opening(self):
        f = sessions_cli.interpret_open
        self.assertEqual(f(0, "opened: a\n", ""), "aberta")
        self.assertEqual(f(0, "running: a\n", ""), "ja")
        self.assertEqual(f(1, "", "CHECK: a não abriu: x"), "nao-abriu")
        self.assertEqual(f(1, "", "não deu a sessão em 60s"), "sem-id")
        self.assertEqual(f(2, "", "outro"), "falha")


class Runners(unittest.TestCase):
    def setUp(self):
        self.run = subprocess.run
        self.seen = []

    def tearDown(self):
        subprocess.run = self.run

    def switches(self, result_text):
        def fake(argv, **kw):
            self.seen.append(argv)
            if isinstance(result_text, Exception):
                raise result_text
            return result_text
        subprocess.run = fake

    def test_run_sessions_and_run_brza(self):
        self.switches(ResultCase(0, "ok", ""))
        self.assertEqual(sessions_cli.run_sessions(["list"]), (0, "ok", ""))
        self.assertEqual(sessions_cli.run_brza(["orchestration", "worker-show"]), (0, "ok", ""))
        self.assertEqual(self.seen, [[sessions_cli.BRZA, "sessions", "list"],
                                      [sessions_cli.BRZA, "orchestration", "worker-show"]])

    def test_without_brza_becomes_127(self):
        self.switches(FileNotFoundError("brza"))
        rc, out, err = sessions_cli.run_sessions(["list"])
        self.assertEqual((rc, out), (127, ""))
        self.assertIn("brza", err)

    def test_wait_brza_returns_the_json(self):
        self.switches(ResultCase(0, json.dumps({"done": ["a"], "pending": [], "events": []})))
        rc, d = sessions_cli.wait_brza(["a"], 60, markers=("w:x",))
        self.assertEqual((rc, d["done"]), (0, ["a"]))
        self.assertEqual(self.seen[0][2:], ["wait", "a", "--any", "--marker", "w:x", "--timeout", "60", "--json"])

    def test_wait_brza_without_binary_without_json_and_json_strange(self):
        self.switches(FileNotFoundError("brza"))
        self.assertEqual(sessions_cli.wait_brza(["a"], 1)[0], 127)
        self.switches(ResultCase(1, "CHECK: x", ""))
        rc, d = sessions_cli.wait_brza(["a"], 1)
        self.assertEqual(rc, 1)
        self.assertIn("saída sem JSON", d["error"])
        self.switches(ResultCase(0, "[1]"))
        self.assertEqual(sessions_cli.wait_brza(["a"], 1), (0, {"error": "JSON inesperado"}))

    def test_list_states_of_file(self):
        import os
        import tempfile
        list_packs = {"sessions": [{"name": "a", "state": "working"}, {"name": "z", "state": "idle"},
                              {"name": "x", "state": "done", "provider_session": "P"}]}
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "l.json")
            with open(p, "w", encoding="utf-8") as f:
                json.dump(list_packs, f)
            self.assertEqual(sessions_cli.list_states(["a", "b"], list_json=p), {"a": "working"})
            self.assertEqual(sessions_cli.list_states(["a", "b"], list_json=p, ids={"b": {"P", None}}),
                             {"a": "working", "b": "done"})
            self.assertEqual(sessions_cli.list_states(["a"], list_json=os.path.join(tmp, "nada")), {})

    def test_list_states_by_command(self):
        self.switches(ResultCase(0, json.dumps({"sessions": [{"name": "a", "state": "idle"}]})))
        self.assertEqual(sessions_cli.list_states(["a"]), {"a": "idle"})
        self.assertEqual(self.seen[0], [sessions_cli.BRZA, "sessions", "list", "--json"])
        self.switches(ResultCase(0, "não é json"))
        self.assertEqual(sessions_cli.list_states(["a"]), {})


if __name__ == "__main__":
    unittest.main()
