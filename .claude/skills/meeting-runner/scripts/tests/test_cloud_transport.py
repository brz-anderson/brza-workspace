"""Transporte cloud com um `agent` falso. O `brza sessions` do Studio não é chamado.

    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest scripts.tests.test_cloud_transport
"""
import contextlib
import io
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import _paths  # noqa: F401

import cloud_transport
import launch_persona

SECRET = "brza-test-key-not-real"
WORKFLOW = os.environ.get("BRZA_WORKFLOW_DIR", "/agent/repos/brza-workflow")

FAKE = r'''#!/usr/bin/env python3
import json, os, sys, time
from pathlib import Path
key = os.environ.get("CURSOR_API_KEY") or ""
expected = os.environ.get("BRZA_FAKE_EXPECT") or ""
capture = Path(os.environ["BRZA_FAKE_CAPTURE"])
argv = sys.argv
record = {
    "argv": argv,
    "key_matches": bool(key) and key == expected,
    "cursor_key_set": bool(key),
    "brza_absent": "BRZA_CURSOR_API_KEY" not in os.environ,
}
with capture.open("a", encoding="utf-8") as handle:
    handle.write(json.dumps(record, ensure_ascii=False) + "\n")
home = Path(os.environ["HOME"])
cursor = home / ".config" / "cursor"
cursor.mkdir(parents=True, exist_ok=True)
(cursor / "auth.json").write_text(json.dumps({"apiKey": key}))
prompt = argv[-1] if argv else ""
fail_on = os.environ.get("BRZA_FAKE_FAIL_PERSONA") or ""
behavior = os.environ.get("BRZA_FAKE_BEHAVIOR") or "ok"
applies = (not fail_on) or (fail_on in prompt)
if applies and behavior == "timeout":
    time.sleep(30)
if "--resume" in argv:
    session = argv[argv.index("--resume") + 1]
    if os.environ.get("BRZA_FAKE_MISMATCH") == "1":
        session = session + "-other"
    result = "Posição: manter o grok-4.7-low nesta smoke."
    duration = 55
else:
    counter = capture.parent / "sessions"
    n = int(counter.read_text()) if counter.exists() else 0
    counter.write_text(str(n + 1))
    session = f"sess-{n}"
    result = "pronto"
    duration = 40
is_error = bool(applies and behavior == "error")
print(json.dumps({
    "type": "result",
    "is_error": is_error,
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
            "BRZA_FAKE_EXPECT": SECRET,
            "BRZA_WORKFLOW_DIR": WORKFLOW,
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
        checkout = cloud_transport.workflow_checkout(self.env())
        module = cloud_transport.load_cloud_runtime(checkout)
        self.assertEqual(
            Path(module.__file__).resolve(),
            (Path(checkout) / "packages" / "client" / "bin" / "cloud_runtime.py").resolve())
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
        self.assertTrue(all(call["key_matches"] and call["cursor_key_set"] and call["brza_absent"] for call in calls))
        self.assertNotIn("CURSOR_API_KEY", self.env())
        text = self.ata.read_text()
        lines = text.splitlines()
        self.assertEqual(lines[-1], "<!-- fim-rodada-1 -->")
        self.assertIn(
            "**SMOKE.** Esta reunião não conta para a promoção da meeting-runner. "
            "As duas posições ficam registradas. O modelo padrão não muda por causa dela.",
            text)
        self.assertIn("`sess-0`", text)
        self.assertIn("`sess-1`", text)
        def turn_id(nome, turn):
            row = next(line for line in lines if line.startswith(f"| {nome} | {turn} |"))
            return row.split("`")[1]

        for nome in ("Arquiteto", "Revisor"):
            self.assertEqual(turn_id(nome, "open"), turn_id(nome, "send"))
        self.assertNotEqual(turn_id("Arquiteto", "open"), turn_id("Revisor", "open"))
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
            self.assertFalse(home.exists(), home)
        sha = subprocess.check_output(
            ["git", "-C", WORKFLOW, "rev-parse", "HEAD"], text=True).strip()
        self.assertIn(sha, text)
        module = cloud_transport.load_cloud_runtime(WORKFLOW)
        cold = module.CloudRuntime(env=self.env(), log_path=str(self.log), timeout_s=5)
        try:
            with self.assertRaises(module.CloudTurnError) as caught:
                cold.send("sess-0", "de novo")
        finally:
            cold.close()
        self.assertIn("session_id", str(caught.exception))
        self.assertEqual(len(self.calls()), 4)

    def test_missing_workflow_dir_names_the_variable_and_no_branch(self):
        env = self.env()
        env.pop("BRZA_WORKFLOW_DIR")
        with self.assertRaises(cloud_transport.CloudTransportError) as caught:
            cloud_transport.workflow_checkout(env)
        message = str(caught.exception)
        self.assertIn("BRZA_WORKFLOW_DIR", message)
        self.assertNotIn("builder/", message)

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
        self.assertIn(
            "As duas posições ficam registradas. O modelo padrão não muda por causa dela.",
            self.ata.read_text())

    def _personas(self, rows):
        reuniao = dict(self.reuniao)
        reuniao["personas"] = rows
        return reuniao

    def test_mid_round_is_error_omits_the_marker_and_returns_nonzero(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = cloud_transport.run_round(
                self.reuniao, self.reuniao["personas"], str(self.tmp), 1,
                env=self.env(BRZA_FAKE_BEHAVIOR="error", BRZA_FAKE_FAIL_PERSONA="Revisor"),
                log_path=str(self.log), timeout_s=5, out=lambda _line: None)
        self.assertNotEqual(rc, 0)
        text = self.ata.read_text()
        self.assertNotIn("<!-- fim-rodada-", text)
        self.assertNotIn(cloud_transport.round_marker(1), text)
        self.assertIn("Posição: manter o grok-4.7-low nesta smoke.", text)
        self.assertIn("A persona Revisor falhou:", text)
        self.assertIn("is_error", text)
        self.assertIn("Revisor", err.getvalue())
        self.assertEqual(len(self.calls()), 3)

    def test_mid_round_timeout_omits_the_marker_and_names_the_persona(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = cloud_transport.run_round(
                self.reuniao, self.reuniao["personas"], str(self.tmp), 1,
                env=self.env(BRZA_FAKE_BEHAVIOR="timeout", BRZA_FAKE_FAIL_PERSONA="Revisor"),
                log_path=str(self.log), timeout_s=1, out=lambda _line: None)
        self.assertNotEqual(rc, 0)
        text = self.ata.read_text()
        self.assertNotIn("<!-- fim-rodada-", text)
        self.assertIn("Posição: manter o grok-4.7-low nesta smoke.", text)
        self.assertIn("A persona Revisor falhou:", text)
        self.assertIn("timeout", text)
        stderr = err.getvalue()
        self.assertIn("Revisor", stderr)
        self.assertIn("timeout", stderr)

    def test_critic_role_without_ask_fails_before_the_agent(self):
        cases = (
            ("Fiscal", "crítica", None),
            ("Ana", "revisor", "agent"),
        )
        for nome, papel, modo in cases:
            with self.subTest(nome=nome, papel=papel, modo=modo):
                self.capture.unlink(missing_ok=True)
                self.ata.unlink(missing_ok=True)
                persona = {"nome": nome, "slug": nome.lower(), "papel": papel, "modelo": "grok-4.7-low"}
                if modo:
                    persona["modo"] = modo
                err = io.StringIO()
                with contextlib.redirect_stderr(err):
                    rc = cloud_transport.run_round(
                        self._personas([persona]), [persona], str(self.tmp), 1,
                        env=self.env(), log_path=str(self.log), timeout_s=5)
                self.assertNotEqual(rc, 0)
                self.assertIn(nome, err.getvalue())
                self.assertIn("ask", err.getvalue())
                self.assertFalse(self.capture.exists())
                self.assertFalse(self.ata.exists())

    def test_reviewer_name_with_proposer_role_still_calls_the_agent(self):
        persona = {"nome": "Revisor", "slug": "revisor", "papel": "propõe", "modelo": "grok-4.7-low"}
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = cloud_transport.run_round(
                self._personas([persona]), [persona], str(self.tmp), 1,
                env=self.env(), log_path=str(self.log), timeout_s=5, out=lambda _line: None)
        self.assertEqual(rc, 0, err.getvalue())
        self.assertEqual(len(self.calls()), 2)
        self.assertEqual(self.ata.read_text().splitlines()[-1], "<!-- fim-rodada-1 -->")

    def test_missing_workflow_dir_names_the_variable(self):
        env = self.env()
        env.pop("BRZA_WORKFLOW_DIR", None)
        env["BRZA_WORKFLOW"] = WORKFLOW
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = cloud_transport.run_round(
                self.reuniao, self.reuniao["personas"], str(self.tmp), 1,
                env=env, log_path=str(self.log), timeout_s=5)
        self.assertNotEqual(rc, 0)
        message = err.getvalue()
        self.assertIn("BRZA_WORKFLOW_DIR", message)
        self.assertIn("packages/client/bin/cloud_runtime.py", message)
        self.assertFalse(self.capture.exists())
        self.assertFalse(self.ata.exists())

    def test_runtime_without_open_fails_before_the_agent(self):
        root = self.tmp / "wf"
        bindir = root / "packages" / "client" / "bin"
        bindir.mkdir(parents=True)
        (root / "bin").mkdir()
        (root / "bin" / "brza_runtime.py").write_text(
            "class BrzaError(Exception):\n    pass\n", encoding="utf-8")
        (bindir / "agent_runtime.py").write_text(
            "CAPABILITIES = ('list', 'read', 'usage', 'open', 'send')\n", encoding="utf-8")
        (bindir / "cloud_runtime.py").write_text(
            "class CloudRuntime:\n"
            "    def __init__(self, env=None, log_path=None, timeout_s=180, keep_home=False):\n"
            "        pass\n"
            "    def close(self):\n"
            "        pass\n",
            encoding="utf-8")
        saved = {name: sys.modules.get(name) for name in ("agent_runtime", "brza_runtime", "cloud_runtime")}
        err = io.StringIO()
        try:
            with contextlib.redirect_stderr(err):
                rc = cloud_transport.run_round(
                    self.reuniao, self.reuniao["personas"], str(self.tmp), 1,
                    env=self.env(BRZA_WORKFLOW_DIR=str(root)), log_path=str(self.log), timeout_s=5)
        finally:
            for name, module in saved.items():
                if module is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = module
        self.assertNotEqual(rc, 0)
        self.assertIn("open", err.getvalue())
        self.assertFalse(self.capture.exists())

    def _restore_modules(self, saved):
        for name, module in saved.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module

    def test_port_without_open_fails_before_the_agent(self):
        root = self.tmp / "wf-port"
        bindir = root / "packages" / "client" / "bin"
        bindir.mkdir(parents=True)
        (root / "bin").mkdir()
        (root / "bin" / "brza_runtime.py").write_text(
            "class BrzaError(Exception):\n    pass\n", encoding="utf-8")
        (bindir / "agent_runtime.py").write_text(
            "CAPABILITIES = ('list', 'read', 'usage', 'send')\n", encoding="utf-8")
        (bindir / "cloud_runtime.py").write_text(
            "import os\n"
            "from pathlib import Path\n"
            "class CloudRuntime:\n"
            "    def __init__(self, env=None, log_path=None, timeout_s=180, keep_home=False):\n"
            "        pass\n"
            "    def capabilities(self):\n"
            "        return ('open', 'send')\n"
            "    def open(self, spec):\n"
            "        Path(os.environ['BRZA_FAKE_CAPTURE']).write_text('called\\n', encoding='utf-8')\n"
            "        raise AssertionError('open')\n"
            "    def close(self):\n"
            "        pass\n",
            encoding="utf-8")
        saved = {name: sys.modules.get(name) for name in ("agent_runtime", "brza_runtime", "cloud_runtime")}
        err = io.StringIO()
        try:
            with contextlib.redirect_stderr(err):
                rc = cloud_transport.run_round(
                    self.reuniao, self.reuniao["personas"], str(self.tmp), 1,
                    env=self.env(BRZA_WORKFLOW_DIR=str(root)), log_path=str(self.log), timeout_s=5)
        finally:
            self._restore_modules(saved)
        self.assertNotEqual(rc, 0)
        message = err.getvalue()
        self.assertIn("open", message)
        self.assertIn("porta", message)
        self.assertFalse(self.capture.exists())
        self.assertFalse(self.ata.exists())

    def test_send_session_id_must_match_the_open(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = cloud_transport.run_round(
                self.reuniao, self.reuniao["personas"], str(self.tmp), 1,
                env=self.env(BRZA_FAKE_MISMATCH="1"), log_path=str(self.log), timeout_s=5,
                out=lambda _line: None)
        self.assertNotEqual(rc, 0)
        text = self.ata.read_text()
        self.assertNotIn("<!-- fim-rodada-", text)
        stderr = err.getvalue()
        self.assertIn("Arquiteto", stderr)
        self.assertIn("session_id", stderr)
        self.assertEqual(len(self.calls()), 2)

    def _git(self, repo, *args):
        subprocess.run(
            ["git", "-C", str(repo), "-c", "user.name=Bob The Builder",
             "-c", "user.email=bob@brza.dev", *args],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _stub_sources(self):
        runtime = (
            "class Turn:\n"
            "    def __init__(self, session_id, result):\n"
            "        self.session_id = session_id\n"
            "        self.duration_ms = 1\n"
            "        self.result = result\n"
            "        self.usage = {}\n"
            "        self.measurement = {}\n"
            "class CloudRuntime:\n"
            "    def __init__(self, env=None, log_path=None, timeout_s=180, keep_home=False):\n"
            "        self.n = 0\n"
            "    def capabilities(self):\n"
            "        return ('open', 'send')\n"
            "    def open(self, spec):\n"
            "        self.n += 1\n"
            "        return Turn(f'stub-{self.n}', 'pronto')\n"
            "    def send(self, session_id, prompt):\n"
            "        return Turn(session_id, 'Posição: manter')\n"
            "    def close(self):\n"
            "        return None\n"
        )
        return {
            "bin/brza_runtime.py": "class BrzaError(Exception):\n    pass\n",
            "packages/client/bin/agent_runtime.py": "CAPABILITIES = ('list', 'read', 'usage', 'open', 'send')\n",
            "packages/client/bin/cloud_runtime.py": runtime,
        }

    def _commit_stub(self, repo, names):
        sources = self._stub_sources()
        for name in names:
            path = repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(sources[name], encoding="utf-8")
        self._git(repo, "add", ".")
        self._git(repo, "commit", "-m", "stub")

    def test_sha_is_recorded_only_when_the_module_is_absent_from_origin_master(self):
        cases = (("on", True), ("off", False))
        for label, on_master in cases:
            with self.subTest(on_master=on_master):
                self.capture.unlink(missing_ok=True)
                self.ata.unlink(missing_ok=True)
                repo = self.tmp / f"wf-sha-{label}"
                repo.mkdir()
                self._git(repo, "init")
                base = ("bin/brza_runtime.py", "packages/client/bin/agent_runtime.py")
                self._commit_stub(repo, base)
                self._git(repo, "update-ref", "refs/remotes/origin/master", "HEAD")
                if not on_master:
                    self._commit_stub(repo, base + ("packages/client/bin/cloud_runtime.py",))
                else:
                    self._commit_stub(repo, ("packages/client/bin/cloud_runtime.py",))
                    self._git(repo, "update-ref", "refs/remotes/origin/master", "HEAD")
                saved = {name: sys.modules.get(name) for name in ("agent_runtime", "brza_runtime", "cloud_runtime")}
                err = io.StringIO()
                try:
                    with contextlib.redirect_stderr(err):
                        rc = cloud_transport.run_round(
                            self.reuniao, self.reuniao["personas"], str(self.tmp), 1,
                            env=self.env(BRZA_WORKFLOW_DIR=str(repo)),
                            log_path=str(self.log), timeout_s=5, out=lambda _line: None)
                finally:
                    self._restore_modules(saved)
                self.assertEqual(rc, 0, err.getvalue())
                text = self.ata.read_text()
                sha = subprocess.check_output(
                    ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
                if on_master:
                    self.assertNotIn("CloudRuntime:", text)
                    self.assertNotIn(sha, text)
                else:
                    self.assertIn(f"CloudRuntime: `{sha}`", text)
                self.assertFalse(self.capture.exists())


if __name__ == "__main__":
    unittest.main()
