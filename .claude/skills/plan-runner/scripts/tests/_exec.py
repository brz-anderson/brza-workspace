"""Base dos testes de executor, consult e painel: plano em tmp, git de teste, corredores trocados por atribuição."""
import json
import os
import shutil
import subprocess
import tempfile
import unittest

import _paths  # noqa: F401
import consult
import executor
import plan_panel
from mini import DESIGN, ROUND1, step
from mini import plan as make_plan


class FakeClock:
    """Relógio falso: `sleep` o avança, e cada leitura também (1 s), para laço nenhum girar para sempre."""

    def __init__(self, t=1762740000.0):
        self.t = t

    def __call__(self):
        self.t += 1
        return self.t

    def sleep(self, s):
        self.t += max(s, 1)


class Base(unittest.TestCase):
    def setUp(self):
        self.dirs = []
        self.outputs, self.errors = [], []
        self.clock = FakeClock()
        self.calls = []     # (corredor, argv)
        self.sessions = lambda argv: (0, "open: x", "")
        self.brza = lambda argv: (0, "", "")
        self.wait = lambda name_list, t, markers=(), any_=True: (75, {"done": [], "pending": list(name_list), "timed_out": True, "events": []})
        self.originals = {}
        for mod, name in ((executor, "run_sessions"), (executor, "run_brza"), (executor, "wait_brza"), (executor, "run_shell"),
                          (consult, "run_sessions"), (consult, "run_brza"), (consult, "wait_brza"), (plan_panel, "publish_safe"),
                          (executor, "list_states")):
            self.originals[(mod, name)] = getattr(mod, name)
        executor.run_sessions = consult.run_sessions = lambda argv: (self.calls.append(("sessions", argv)), self.sessions(argv))[1]
        executor.run_brza = consult.run_brza = lambda argv: (self.calls.append(("brza", argv)), self.brza(argv))[1]
        executor.wait_brza = consult.wait_brza = lambda *a, **k: (self.calls.append(("wait", a)), self.wait(*a, **k))[1]
        executor.list_states = lambda name_list, **k: {}
        self.panels = []
        plan_panel.publish_safe = lambda pl, **kw: (self.panels.append(kw), {"line": "::orca-visual{file=\"p.html\"}", "png": None, "warning": None})[1]
        executor.run_shell = lambda cmd, cwd, timeout=120: (0, "3 passed\n")

    def tearDown(self):
        for (mod, name), f in self.originals.items():
            setattr(mod, name, f)
        for d in self.dirs:
            shutil.rmtree(d, ignore_errors=True)

    def build(self, plan=None, design=DESIGN, interview=None):
        root, path = _paths.plan_tmp(plan or make_plan(step("P1", title="Um passo", checks="- [ ] **1. A**\n- [ ] **2. B**"), ROUND1),
                                      design=design)
        self.dirs.append(root)
        return root, path

    def checkout(self):
        d = tempfile.mkdtemp(prefix="pr-co-")
        self.dirs.append(d)
        subprocess.run(["git", "-C", d, "init", "-q"], check=True)
        with open(os.path.join(d, "a.py"), "w") as f:
            f.write("x\n")
        subprocess.run(["git", "-C", d, "add", "-A"], check=True)
        subprocess.run(["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "c"], check=True)
        sha = subprocess.run(["git", "-C", d, "rev-parse", "--short=7", "HEAD"], capture_output=True, text=True).stdout.strip()
        return d, sha

    def invoke(self, mod, *args):
        self.outputs.clear()
        self.errors.clear()
        rc = mod.main(list(args), out=self.outputs.append, err=self.errors.append, clock=self.clock, sleep=self.clock.sleep)
        return rc

    @property
    def out(self):
        return "\n".join(self.outputs)

    @property
    def err(self):
        return "\n".join(self.errors)

    def manifest_text(self, root):
        with open(plan_panel.manifest_path(root, "PLN-900"), encoding="utf-8") as f:
            return json.load(f)

    def open_step(self, root, path, co=None):
        co = co or self.checkout()[0]
        rc = self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel")
        self.assertEqual(rc, 0, self.err)
        return co

    def worklog(self, root):
        return os.path.join(root, self.manifest_text(root)["steps"]["P1"]["worklog"])

    def closes_worklog(self, root, evidence, marker="feito"):
        p = self.worklog(root)
        with open(p, encoding="utf-8") as f:
            t = f.read()
        t = t.replace("## Evidência\n", "## Evidência\n\n" + evidence + "\n")
        t += "\n<!-- fim-P1: %s -->\n" % marker
        with open(p, "w", encoding="utf-8") as f:
            f.write(t)
