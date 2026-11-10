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
from mini import DESENHO, RODADA1, passo, plano


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
        self.saidas, self.erros = [], []
        self.clock = FakeClock()
        self.chamadas = []     # (corredor, argv)
        self.sessions = lambda argv: (0, "open: x", "")
        self.brza = lambda argv: (0, "", "")
        self.wait = lambda nomes, t, markers=(), any_=True: (75, {"done": [], "pending": list(nomes), "timed_out": True, "events": []})
        self.originais = {}
        for mod, nome in ((executor, "run_sessions"), (executor, "run_brza"), (executor, "wait_brza"), (executor, "run_shell"),
                          (consult, "run_sessions"), (consult, "run_brza"), (consult, "wait_brza"), (plan_panel, "publica_seguro"),
                          (executor, "list_states")):
            self.originais[(mod, nome)] = getattr(mod, nome)
        executor.run_sessions = consult.run_sessions = lambda argv: (self.chamadas.append(("sessions", argv)), self.sessions(argv))[1]
        executor.run_brza = consult.run_brza = lambda argv: (self.chamadas.append(("brza", argv)), self.brza(argv))[1]
        executor.wait_brza = consult.wait_brza = lambda *a, **k: (self.chamadas.append(("wait", a)), self.wait(*a, **k))[1]
        executor.list_states = lambda nomes, **k: {}
        self.paineis = []
        plan_panel.publica_seguro = lambda pl, **kw: (self.paineis.append(kw), {"linha": "::orca-visual{file=\"p.html\"}", "png": None, "aviso": None})[1]
        executor.run_shell = lambda cmd, cwd, timeout=120: (0, "3 passed\n")

    def tearDown(self):
        for (mod, nome), f in self.originais.items():
            setattr(mod, nome, f)
        for d in self.dirs:
            shutil.rmtree(d, ignore_errors=True)

    def monta(self, plan=None, design=DESENHO, interview=None):
        raiz, path = _paths.plano_tmp(plan or plano(passo("P1", titulo="Um passo", checks="- [ ] **1. A**\n- [ ] **2. B**"), RODADA1),
                                      design=design)
        self.dirs.append(raiz)
        return raiz, path

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

    def roda(self, mod, *args):
        self.saidas.clear()
        self.erros.clear()
        rc = mod.main(list(args), out=self.saidas.append, err=self.erros.append, clock=self.clock, sleep=self.clock.sleep)
        return rc

    @property
    def out(self):
        return "\n".join(self.saidas)

    @property
    def err(self):
        return "\n".join(self.erros)

    def manifesto(self, raiz):
        with open(plan_panel.manifesto_path(raiz, "PLN-900"), encoding="utf-8") as f:
            return json.load(f)

    def abre(self, raiz, path, co=None):
        co = co or self.checkout()[0]
        rc = self.roda(executor, "open", path, "P1", "--checkout", co, "--no-panel")
        self.assertEqual(rc, 0, self.err)
        return co

    def worklog(self, raiz):
        return os.path.join(raiz, self.manifesto(raiz)["passos"]["P1"]["worklog"])

    def fecha_worklog(self, raiz, evid, marcador="feito"):
        p = self.worklog(raiz)
        with open(p, encoding="utf-8") as f:
            t = f.read()
        t = t.replace("## Evidência\n", "## Evidência\n\n" + evid + "\n")
        t += "\n<!-- fim-P1: %s -->\n" % marcador
        with open(p, "w", encoding="utf-8") as f:
            f.write(t)
