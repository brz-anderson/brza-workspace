"""Transporte cloud com um `agent` falso. O `brza sessions` do Studio não é chamado.

    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest scripts.tests.test_cloud_transport
"""
import contextlib
import io
import json
import os
import stat
import tempfile
import unittest
from pathlib import Path

import _paths  # noqa: F401

import cloud_transport
import launch_persona

SECRET = "brza-test-key-not-real"
WORKFLOW = str(Path(cloud_transport.workspace_root()).parent / "brza-workflow")

FAKE = r'''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
key = os.environ.get("CURSOR_API_KEY") or ""
brza = os.environ.get("BRZA_CURSOR_API_KEY") or ""
capture = Path(os.environ["BRZA_FAKE_CAPTURE"])
argv = sys.argv
record = {
    "argv": argv,
    "key_matches": bool(key) and key == brza,
    "cursor_key_set": bool(key),
}
with capture.open("a", encoding="utf-8") as handle:
    handle.write(json.dumps(record, ensure_ascii=False) + "\n")
home = Path(os.environ["HOME"])
cursor = home / ".config" / "cursor"
cursor.mkdir(parents=True, exist_ok=True)
(cursor / "auth.json").write_text(json.dumps({"apiKey": key}))
if "--resume" in argv:
    session = argv[argv.index("--resume") + 1]
    result = "Posição: manter o grok-4.7-low nesta smoke."
    duration = 55
else:
    counter = capture.parent / "sessions"
    n = int(counter.read_text()) if counter.exists() else 0
    counter.write_text(str(n + 1))
    session = f"sess-{n}"
    result = "pronto"
    duration = 40
print(json.dumps({
    "type": "result",
    "is_error": False,
    "duration_ms": duration,
    "result": result,
    "session_id": session,
    "usage": {
        "inputTokens": 10,
        "outputTokens": 4,
        "cacheReadTokens": 1,
        "cacheWriteTokens": 0,
        "reasoningTokens": 2,
    },
}))
'''


def files_with(root, secret):
    found = []
    if not root or not Path(root).exists():
        return found
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if not os.path.islink(os.path.join(dirpath, name))]
        for name in filenames:
            path = Path(dirpath) / name
            try:
                blob = path.read_bytes()
            except OSError:
                continue
            if secret.encode() in blob:
                found.append(str(path))
    return found


class CloudTransportTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="brza-meeting-cloud-"))
        self.addCleanup(lambda: __import__("shutil").rmtree(self.tmp, ignore_errors=True))
        bindir = self.tmp / "bin"
        bindir.mkdir()
        agent = bindir / "agent"
        agent.write_text(FAKE)
        agent.chmod(agent.stat().st_mode | stat.S_IEXEC)
        (self.tmp / "home").mkdir()
        (self.tmp / "workspace").mkdir()
        self.capture = self.tmp / "capture.jsonl"
        self.log = self.tmp / "measurements.jsonl"
        self.ata = self.tmp / "ata.md"
        self.manifest = self.tmp / "reuniao.json"
        self.reuniao = {
            "id": "reuniao-smoke",
            "tema": "Devemos manter grok-4.7-low?",
            "smoke": True,
            "ata_titulo": "A reunião smoke do PLN-026 não conta para a promoção",
            "ata": str(self.ata),
            "workspace": str(self.tmp / "workspace"),
            "dir": ".",
            "personas": [
                {"nome": "Arquiteto", "slug": "arquiteto", "papel": "propõe",
                 "modelo": "grok-4.7-low", "modo": "agent"},
                {"nome": "Revisor", "slug": "revisor", "papel": "critica",
                 "modelo": "grok-4.7-low", "modo": "ask"},
            ],
        }
        self.manifest.write_text(json.dumps(self.reuniao), encoding="utf-8")

    def env(self, **extra):
        base = {
            "PATH": str(self.tmp / "bin") + os.pathsep + "/usr/bin:/bin",
            "HOME": str(self.tmp / "home"),
            "BRZA_FAKE_CAPTURE": str(self.capture),
            "BRZA_CURSOR_API_KEY": SECRET,
            "BRZA_WORKFLOW": WORKFLOW,
        }
        base.update(extra)
        base.pop("CURSOR_API_KEY", None)
        return base

    def calls(self):
        return [json.loads(line) for line in self.capture.read_text().splitlines() if line.strip()]

    def flags(self, call):
        argv = call["argv"]
        self.assertEqual(os.path.basename(argv[0]), "agent")
        return argv[1:]

    def test_choose_transport_defaults_to_studio(self):
        self.assertEqual(cloud_transport.choose_transport(None), "studio")
        self.assertEqual(cloud_transport.choose_transport(""), "studio")
        self.assertEqual(cloud_transport.choose_transport("studio"), "studio")
        self.assertEqual(cloud_transport.choose_transport("cloud"), "cloud")
        with self.assertRaises(cloud_transport.CloudTransportError):
            cloud_transport.choose_transport("worker-start")

    def test_round_marker_is_the_exact_line(self):
        self.assertEqual(cloud_transport.round_marker(1), "<!-- fim-rodada-1 -->")

    def test_cloud_runtime_is_imported_from_the_workflow_checkout(self):
        module = cloud_transport.load_cloud_runtime(cloud_transport.workflow_checkout(self.env()))
        self.assertTrue(str(module.__file__).endswith("packages/client/cloud_runtime.py"))
        self.assertIn("brza-workflow", str(module.__file__))
        skill_copy = Path(cloud_transport.__file__).with_name("cloud_runtime.py")
        self.assertFalse(skill_copy.exists())

    def test_round_opens_then_sends_and_writes_the_marker(self):
        called = []

        def sessions_fn(argv):
            called.append(argv)
            raise AssertionError("studio transport called")

        rc = cloud_transport.run_round(
            self.reuniao, self.reuniao["personas"], str(self.tmp), 1,
            sessions_fn=sessions_fn, env=self.env(), log_path=str(self.log), timeout_s=5,
            out=lambda _line: None)
        self.assertEqual(rc, 0)
        self.assertEqual(called, [])
        calls = self.calls()
        self.assertEqual(len(calls), 4)
        architect_open, architect_send, reviewer_open, reviewer_send = [self.flags(c) for c in calls]
        self.assertNotIn("--resume", architect_open)
        self.assertNotIn("--mode", architect_open)
        self.assertIn("--resume", architect_send)
        self.assertEqual(reviewer_open[reviewer_open.index("--mode") + 1], "ask")
        self.assertEqual(reviewer_send[reviewer_send.index("--mode") + 1], "ask")
        self.assertIn("--resume", reviewer_send)
        self.assertNotIn("--api-key", architect_open + reviewer_send)
        self.assertNotIn("--force", architect_open)
        self.assertTrue(all(call["key_matches"] for call in calls))
        self.assertNotIn("CURSOR_API_KEY", self.env())
        text = self.ata.read_text()
        lines = text.splitlines()
        self.assertEqual(lines[-1], "<!-- fim-rodada-1 -->")
        self.assertIn("**SMOKE.**", text)
        self.assertIn("`sess-0`", text)
        self.assertIn("`sess-1`", text)
        self.assertIn("ausente", text)
        self.assertIn("Posição: manter o grok-4.7-low nesta smoke.", text)
        self.assertIn("Posição: manter o grok-4.7-low nesta smoke.", reviewer_send[-1])
        self.assertEqual(files_with(self.tmp / "home", SECRET), [])
        self.assertNotIn(SECRET.encode(), self.ata.read_bytes())
        self.assertNotIn(SECRET.encode(), self.log.read_bytes())
        self.assertNotIn(SECRET.encode(), self.capture.read_bytes())
        self.assertEqual(
            architect_send[architect_send.index("--workspace") + 1], str(self.tmp / "workspace"))
        for nome in ("Arquiteto", "Revisor"):
            home = self.tmp / "home" / ".local" / "share" / "brza" / "cloud-runtime" / nome
            self.assertTrue(home.is_dir(), home)
            self.assertEqual(files_with(home, SECRET), [])
        module = cloud_transport.load_cloud_runtime(WORKFLOW)
        cold = module.CloudRuntime(env=self.env(), log_path=str(self.log), timeout_s=5)
        try:
            with self.assertRaises(module.CloudTurnError) as caught:
                cold.send("sess-0", "de novo")
        finally:
            cold.close()
        message = str(caught.exception)
        self.assertIn("persona", message)
        self.assertIn("workspace", message)
        self.assertEqual(len(self.calls()), 4)

    def test_missing_key_fails_with_an_actionable_message(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = cloud_transport.run_round(
                self.reuniao, self.reuniao["personas"], str(self.tmp), 1,
                env=self.env(BRZA_CURSOR_API_KEY=""), log_path=str(self.log), timeout_s=5)
        self.assertEqual(rc, 1)
        message = err.getvalue()
        self.assertIn("cloud", message)
        self.assertIn("open", message)
        self.assertIn("BRZA_CURSOR_API_KEY", message)
        self.assertFalse(self.capture.exists())
        self.assertFalse(self.ata.exists())

    def test_missing_agent_names_the_install_command(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = cloud_transport.run_round(
                self.reuniao, self.reuniao["personas"], str(self.tmp), 1,
                env=self.env(PATH="/usr/bin:/bin"), log_path=str(self.log), timeout_s=5)
        self.assertEqual(rc, 1)
        message = err.getvalue()
        self.assertIn("cloud", message)
        self.assertIn("curl https://cursor.com/install -fsS | bash", message)
        self.assertFalse(self.ata.exists())

    def test_studio_dry_run_still_prints_brza_sessions(self):
        fixture = Path(_paths.fixture("reuniao-mcp-remoto.json"))
        lines = []
        rc = launch_persona.main(
            [str(fixture), "--dry-run", "--root", str(self.tmp)], out=lines.append)
        self.assertEqual(rc, 0)
        text = "\n".join(lines)
        self.assertIn("brza sessions", text)
        self.assertNotIn("CloudRuntime", text)
        self.assertNotIn("agent -p", text)

    def test_cloud_cli_does_not_call_studio(self):
        def sessions_fn(argv):
            raise AssertionError(argv)

        lines = []
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = launch_persona.main(
                [str(self.manifest), "--transport", "cloud", "--round", "1", "--root", str(self.tmp)],
                sessions_fn=sessions_fn, out=lines.append, env=self.env(),
                log_path=str(self.log), timeout_s=5)
        self.assertEqual(rc, 0, err.getvalue())
        self.assertTrue(self.ata.is_file())
        self.assertEqual(self.ata.read_text().splitlines()[-1], "<!-- fim-rodada-1 -->")


if __name__ == "__main__":
    unittest.main()
