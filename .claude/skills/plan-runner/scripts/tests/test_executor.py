import json
import os
import re
import subprocess

import _exec
import _paths  # noqa: F401
import executor
import plan_md
from mini import DESIGN, ROUND1, step, plan


class Open(_exec.Base):
    def test_opens_writes_manifest_worklog_request_and_table(self):
        root, path = self.build()
        co, _ = self.checkout()
        rc = self.invoke(executor, "open", path, "P1", "--checkout", co)
        self.assertEqual(rc, 0, self.err)
        argv = next(a for k, a in self.calls if k == "sessions")
        self.assertEqual(argv[0], "pln900-p1")
        self.assertIn("--wait", argv)
        self.assertIn("--rename", argv)
        self.assertEqual(argv[argv.index("--title") + 1], "PLN-900 P1: Um passo")
        self.assertEqual(argv[argv.index("--model") + 1], executor.SONNET)
        self.assertEqual(argv[argv.index("--checkout") + 1], co)
        m = self.manifest_text(root)["steps"]["P1"]
        self.assertEqual((m["state"], m["marker"], m["agent"]), ("aberto", "fim-P1:", "claude"))
        self.assertEqual(m["events"][0]["state"], "aberto")
        wl = self.worklog(root)
        with open(wl, encoding="utf-8") as f:
            t = f.read()
        for section in ("## O que se fez", "## Desvios", "## Evidência", "# PLN-900 P1: Um passo"):
            self.assertIn(section, t)
        self.assertNotIn("<!-- fim-P1: feito -->\n", t.split("---")[-1].split("linha, e só")[-1])
        self.assertIsNone(executor.last_marker(wl, "P1"))
        self.assertTrue(os.path.isfile(os.path.join(root, m["request"])))
        self.assertIn("| P1 | pln900-p1 | claude | %s |" % executor.SONNET, self.out)
        self.assertIn("| Passo | Executor | Runtime | Modelo | Esforço | Checkout | Branch |", self.out)
        self.assertEqual(len(self.panels), 1)
        self.assertTrue(self.panels[0]["png"])

    def test_the_template_of_worklog_lacks_the_marker_literal(self):
        # o `--marker` do `brza` é um `re.search` no arquivo inteiro: a prosa do molde não pode casar com ele
        root, path = self.build()
        self.open_step(root, path)
        with open(self.worklog(root), encoding="utf-8") as f:
            t = f.read()
        self.assertIsNone(re.search(r"<!-- fim-P1:", t))
        self.assertIn("`fim-P1`", t)

    def test_tree_runs_brza_tree_and_infers_a_branch(self):
        root, path = self.build()
        co, _ = self.checkout()
        self.brza = lambda argv: (0, "worktree: %s\n" % os.path.join(os.path.dirname(co), os.path.basename(co)), "")
        rc = self.invoke(executor, "open", path, "P1", "--tree", os.path.basename(co), "--type", "fix", "--no-panel")
        self.assertEqual(rc, 0, self.err)
        self.assertIn(("brza", ["tree", os.path.basename(co), "--type", "fix"]), self.calls)
        self.assertEqual(self.manifest_text(root)["steps"]["P1"]["branch"], "fix/" + os.path.basename(co))

    def test_not_opened_not_writes_manifest(self):
        root, path = self.build()
        co, _ = self.checkout()
        self.sessions = lambda argv: (1, "", "CHECK: pln900-p1 não abriu: pending-x.json")
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 1)
        self.assertIn("pending-*.json", self.err)
        self.assertFalse(os.path.exists(os.path.join(root, ".sessions", "pln-900", "execucao.json")))
        self.assertEqual(len([1 for k, _ in self.calls if k == "sessions"]), 1)

    def test_without_id_opens_with_warning(self):
        root, path = self.build()
        co, _ = self.checkout()
        self.sessions = lambda argv: (1, "", "CHECK: pln900-p1 não deu a sessão em 60 s")
        rc = self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel")
        self.assertEqual(rc, 0)   # abriu sem o id do provedor: o `wait` o grava depois
        self.assertIn("sem o id do provedor", self.err)
        self.assertEqual(self.manifest_text(root)["steps"]["P1"]["state"], "aberto")

    def test_dry_run_not_writes(self):
        root, path = self.build()
        co, _ = self.checkout()
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--checkout", co, "--dry-run"), 0)
        self.assertIn("[dry-run] brza sessions pln900-p1", self.out)
        self.assertFalse(os.path.exists(os.path.join(root, ".sessions")))
        self.assertEqual(self.calls, [])

    def test_refuses_step_live_and_step_missing(self):
        root, path = self.build()
        co = self.open_step(root, path)
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 1)
        self.assertIn("já tem executor", self.err)
        self.assertEqual(self.invoke(executor, "open", path, "P9", "--checkout", co), 2)

    def test_reopen_stopped_ignores_the_marker_old(self):
        # A4: o `wait` seguinte esperava o executor novo, e voltava na hora com o `parado` do anterior
        root, path = self.build()
        co = self.open_step(root, path)
        self.closes_worklog(root, "- desvios: X? — muda o D", "parado")
        self.assertEqual(self.invoke(executor, "wait", path, "--no-panel"), 0)
        self.assertEqual(self.manifest_text(root)["steps"]["P1"]["state"], "parado")
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 0, self.err)
        self.assertIsNone(executor.last_marker(self.worklog(root), "P1"))
        with open(self.worklog(root), encoding="utf-8") as f:
            self.assertIn("X? — muda o D", f.read())      # o texto do executor anterior fica
        self.calls.clear()
        self.assertEqual(self.invoke(executor, "wait", path, "--timeout", "5", "--no-panel"), 75)
        self.assertTrue([x for x in self.calls if x[0] == "wait"])

    def test_reopen_with_a_session_live_refuses_and_not_deletes_the_marker(self):
        root, path = self.build()
        co = self.open_step(root, path)
        self.closes_worklog(root, "- desvios: X? — muda o D", "parado")
        self.invoke(executor, "wait", path, "--no-panel")
        self.sessions = lambda argv: (0, "running:  pln900-p1", "")
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 1)
        self.assertIn("brza sessions close pln900-p1", self.err)
        self.assertEqual(executor.last_marker(self.worklog(root), "P1"), "parado")
        self.assertEqual(self.manifest_text(root)["steps"]["P1"]["state"], "parado")

    def test_running_in_first_opening_sends_close_by_brza(self):
        # sem entrada no manifesto o `executor.py close` sairia rc 2: o comando certo é o do `brza`
        root, path = self.build()
        co, _ = self.checkout()
        self.sessions = lambda argv: (0, "running:  pln900-p1", "")
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 1)
        self.assertIn("brza sessions close pln900-p1", self.err)
        self.assertNotIn("executor.py close", self.err)

    def test_reopen_with_a_opening_that_failure_not_deletes_the_marker(self):
        root, path = self.build()
        co = self.open_step(root, path)
        self.closes_worklog(root, "- desvios: X? — muda o D", "parado")
        self.invoke(executor, "wait", path, "--no-panel")
        self.sessions = lambda argv: (1, "", "CHECK: pln900-p1 não abriu: pending-x.json")
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 1)
        self.assertEqual(executor.last_marker(self.worklog(root), "P1"), "parado")

    def test_reopen_done_or_with_evidence_recorded_is_refused_without_delete(self):
        root, path = self.build()
        co, sha = self.checkout()
        self.open_step(root, path, co)
        self.closes_worklog(root, "- commit: brza-studio@%s\n- arquivos: a.py\n- cobre: todos" % sha)
        self.assertEqual(self.invoke(executor, "wait", path, "--no-panel"), 0)
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 1)
        self.assertIn("não reabre", self.err)
        self.assertEqual(self.invoke(executor, "evidence", path, "P1", "--settle", "0", "--apply", "--no-panel"), 0, self.err)
        before = self.manifest_text(root)["steps"]["P1"]
        self.assertEqual(before["state"], "evidencia-gravada")
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 1)
        self.assertEqual(self.manifest_text(root)["steps"]["P1"], before)

    def test_checkout_missing(self):
        root, path = self.build()
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--checkout", "/nao/existe/x"), 1)

    def test_agent_codex_without_effort_opens_without_model(self):
        root, path = self.build()
        co, _ = self.checkout()
        self.invoke(executor, "open", path, "P1", "--checkout", co, "--agent", "codex", "--no-panel")
        argv = next(a for k, a in self.calls if k == "sessions")
        self.assertNotIn("--model", argv)
        self.assertNotIn("--effort", argv)
        self.assertEqual(argv[argv.index("--agent") + 1], "codex")

    def test_codex_with_effort_takes_the_model_default_because_the_brza_requires(self):
        # A1: `brza sessions --effort` sem `--model` sai com "CHECK: --effort exige --model"
        root, path = self.build()
        co, _ = self.checkout()
        self.invoke(executor, "open", path, "P1", "--checkout", co, "--agent", "codex", "--effort", "high", "--no-panel")
        argv = next(a for k, a in self.calls if k == "sessions")
        self.assertEqual(argv[argv.index("--model") + 1], executor.CODEX_MODEL)
        self.assertEqual(argv[argv.index("--effort") + 1], "high")
        self.assertEqual(self.manifest_text(root)["steps"]["P1"]["model"], executor.CODEX_MODEL)

    def test_runtime_without_model_default_not_passes_effort_and_warns(self):
        root, path = self.build()
        co, _ = self.checkout()
        self.invoke(executor, "open", path, "P1", "--checkout", co, "--agent", "grok", "--effort", "high", "--no-panel")
        argv = next(a for k, a in self.calls if k == "sessions")
        self.assertNotIn("--effort", argv)
        self.assertNotIn("--model", argv)
        self.assertIn("recusa --effort sem --model", self.err)

    def test_without_checkout_nor_tree_refuses_asking_checkout_explicit(self):
        # A5: o padrão seria o próprio brza-workspace, onde o pedido proíbe o commit
        root, path = self.build()
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--no-panel"), 2)
        self.assertIn("--checkout", self.err)
        self.assertEqual([k for k, _ in self.calls if k == "sessions"], [])
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--dry-run"), 2)

    def test_checkout_in_master_uses_a_branch_of_step_and_never_a_master(self):
        root, path = self.build()
        co, _ = self.checkout()
        subprocess.run(["git", "-C", co, "checkout", "-q", "-B", "master"], check=True)
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 0, self.err)
        self.assertEqual(self.manifest_text(root)["steps"]["P1"]["branch"], "feat/pln-900-p1")
        with open(os.path.join(root, self.manifest_text(root)["steps"]["P1"]["request"]), encoding="utf-8") as f:
            text = f.read()
        self.assertIn("autoriza o commit na branch `feat/pln-900-p1`", text)
        self.assertNotIn("branch `master`", text)
        root2, path2 = self.build()
        self.assertEqual(self.invoke(executor, "open", path2, "P1", "--checkout", co, "--branch", "main", "--no-panel"), 1)
        self.assertIn("master/main", self.err)

    def test_tree_checks_the_request_before_of_create_the_worktree(self):
        # A13: o passo executa um D que o Desenho não tem; o `brza tree` não pode ter rodado
        root, path = self.build(plan(step("P1", executes="Executa D9"), ROUND1), design=DESIGN)
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--tree", "pln-900-p1", "--no-panel"), 1)
        self.assertIn("D9", self.err)
        self.assertEqual([x for x in self.calls if x[0] == "brza"], [])


class OpenWindow(_exec.Base):
    """O `open` grava o `aberto` na hora do `open` do `sessions.jsonl`, e o `wait` grava o `feito` na hora do worklog."""

    def fake_brza_sessions(self, root, open_offset, marker_offset, write_open=True):
        """O `brza sessions … --wait` falso: grava a linha `open` e o marcador do executor durante a chamada."""
        def run(argv):
            t0 = self.clock.t
            if write_open:
                os.makedirs(os.path.join(root, ".sessions"), exist_ok=True)
                with open(os.path.join(root, ".sessions", "sessions.jsonl"), "a") as f:
                    f.write(json.dumps({"event": "open", "name": "pln900-p1", "at": executor.iso(t0 + open_offset)}) + "\n")
            wl = next(os.path.join(d, n) for d, _, ns in os.walk(os.path.join(root, "work")) for n in ns if n.endswith(".md"))
            with open(wl, "a", encoding="utf-8") as f:
                f.write("\n<!-- fim-P1: feito -->\n")
            os.utime(wl, (t0 + marker_offset, t0 + marker_offset))
            self.clock.t = t0 + 100      # o `--wait` só volta depois
            self.t0 = t0
            return (0, "open: x", "")
        return run

    def test_open_wait_measures_window_from_the_open_event_to_the_marker(self):
        root, path = self.build()
        co, _ = self.checkout()
        self.sessions = self.fake_brza_sessions(root, 1, 20)
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 0, self.err)
        ev = self.manifest_text(root)["steps"]["P1"]["events"]
        self.assertEqual(ev[0]["at"], executor.iso(self.t0 + 1))
        self.assertEqual(self.invoke(executor, "wait", path, "--no-panel"), 0, self.err)
        ev = self.manifest_text(root)["steps"]["P1"]["events"]
        self.assertEqual(ev[-1]["state"], "feito")
        self.assertEqual(ev[-1]["at"], executor.iso(self.t0 + 20))
        pl = executor.plan_md.load(path)
        a, b = executor._window(None, self.manifest_text(root)["steps"]["P1"], pl)
        self.assertEqual(round((executor.sessions_map.epoch(b) - executor.sessions_map.epoch(a)) / 3600, 3), 0.005)

    def test_open_without_event_in_the_map_uses_the_time_before_the_call(self):
        root, path = self.build()
        co, _ = self.checkout()
        self.sessions = self.fake_brza_sessions(root, 0, 20, write_open=False)
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 0, self.err)
        at = self.manifest_text(root)["steps"]["P1"]["events"][0]["at"]
        before = executor.sessions_map.epoch(at)
        self.assertLess(before, self.t0 + 2)     # a hora tomada antes da chamada, e não a da volta do `--wait` (t0 + 100)
        self.assertGreaterEqual(before, self.t0 - 5)

    def test_open_ignores_an_old_open_event_of_the_same_session(self):
        root, path = self.build()
        co, _ = self.checkout()
        os.makedirs(os.path.join(root, ".sessions"), exist_ok=True)
        with open(os.path.join(root, ".sessions", "sessions.jsonl"), "w") as f:
            f.write(json.dumps({"event": "open", "name": "pln900-p1", "at": executor.iso(self.clock.t - 7200)}) + "\n")
        self.sessions = self.fake_brza_sessions(root, 0, 20, write_open=False)
        self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel")
        at = executor.sessions_map.epoch(self.manifest_text(root)["steps"]["P1"]["events"][0]["at"])
        self.assertGreater(at, self.t0 - 60)

    def test_reopen_keeps_the_marker_that_the_new_executor_writes_inside_the_wait(self):
        root, path = self.build()
        co, _ = self.checkout()
        self.sessions = lambda argv: (self.append_marker(root, "parado"), (0, "open: x", ""))[1]
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 0, self.err)
        self.assertEqual(self.invoke(executor, "wait", path, "--no-panel"), 0, self.err)
        self.assertEqual(self.manifest_text(root)["steps"]["P1"]["state"], "parado")
        self.sessions = self.fake_brza_sessions(root, 1, 20)     # o executor novo fecha dentro do `--wait`
        self.assertEqual(self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel"), 0, self.err)
        wl = self.worklog(root)
        self.assertEqual(executor.last_marker(wl, "P1"), "feito")
        with open(wl, encoding="utf-8") as f:
            text = f.read()
        self.assertIn("<!-- reaberto: era fim-P1: parado -->", text)
        self.assertEqual(text.count("<!-- fim-P1: feito -->"), 1)
        self.assertEqual(self.invoke(executor, "wait", path, "--no-panel", "--timeout", "30"), 0, self.err)
        self.assertEqual(self.manifest_text(root)["steps"]["P1"]["state"], "feito")

    def append_marker(self, root, marker):
        wl = next(os.path.join(d, n) for d, _, ns in os.walk(os.path.join(root, "work")) for n in ns if n.endswith(".md"))
        with open(wl, "a", encoding="utf-8") as f:
            f.write("\n<!-- fim-P1: %s -->\n" % marker)

    def test_wait_done_row_with_the_marker_written_uses_the_mtime_of_the_worklog(self):
        root, path = self.build()
        self.open_step(root, path)
        wl = self.worklog(root)
        t = self.clock.t + 500

        def wait(name_list, tt, markers=(), any_=True):
            # o marcador chega durante o `wait_brza`: o 1º ponto do laço não o viu, e o `done` traz a sessão
            self.append_marker(root, "feito")
            os.utime(wl, (t, t))
            self.clock.t = t + 100
            return 0, {"done": [{"name": "pln900-p1", "outcome": "finished"}], "events": []}
        self.wait = wait
        self.assertEqual(self.invoke(executor, "wait", path, "--no-panel", "--timeout", "3000"), 0, self.err)
        ev = self.manifest_text(root)["steps"]["P1"]["events"][-1]
        self.assertEqual((ev["state"], ev["note"]), ("feito", "wait: finished"))
        self.assertEqual(ev["at"], executor.iso(t))

    def test_marker_before_the_open_or_in_the_future_falls_back_to_now(self):
        root, path = self.build()
        co, _ = self.checkout()
        self.sessions = self.fake_brza_sessions(root, 1, -3600)     # mtime anterior ao `aberto`
        self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel")
        self.invoke(executor, "wait", path, "--no-panel")
        ev = self.manifest_text(root)["steps"]["P1"]["events"]
        self.assertGreaterEqual(executor.sessions_map.epoch(ev[-1]["at"]), self.t0 + 100)

    def test_marker_mtime_after_now_falls_back_to_now(self):
        root, path = self.build()
        co, _ = self.checkout()
        self.sessions = self.fake_brza_sessions(root, 1, 20)
        self.invoke(executor, "open", path, "P1", "--checkout", co, "--no-panel")
        wl = self.worklog(root)
        future = self.clock.t + 10 ** 6
        os.utime(wl, (future, future))
        self.invoke(executor, "wait", path, "--no-panel")
        at = executor.sessions_map.epoch(self.manifest_text(root)["steps"]["P1"]["events"][-1]["at"])
        self.assertLess(at, future)
        self.assertLess(at, self.clock.t + 5)


class Wait(_exec.Base):
    def setUp(self):
        super().setUp()
        self.root, self.path = self.build()
        self.co = self.open_step(self.root, self.path)

    def state(self):
        return self.manifest_text(self.root)["steps"]["P1"]["state"]

    def test_marker_done_already_in_the_worklog(self):
        self.closes_worklog(self.root, "- arquivos: a.py")
        self.assertEqual(self.invoke(executor, "wait", self.path, "--timeout", "30", "--no-panel"), 0)
        self.assertRegex(self.out, r"P1 · feito em \d+ min")
        self.assertEqual(self.state(), "feito")

    def test_marker_stopped(self):
        self.closes_worklog(self.root, "- desvios: X? — muda o D", "parado")
        self.assertEqual(self.invoke(executor, "wait", self.path, "--no-panel"), 0)
        self.assertIn("P1 · parado", self.out)
        self.assertEqual(self.state(), "parado")

    def test_deadline_75_and_tick_with_age(self):
        rc = self.invoke(executor, "wait", self.path, "--timeout", "400", "--no-panel")
        self.assertEqual(rc, 75)
        self.assertRegex(self.out, r"P1 · em curso \d+ min \(último evento há \d+ min\)")
        self.assertIn("prazo:", self.out)
        self.assertEqual(self.state(), "em-curso")

    def test_ended_without_marker_is_not_end(self):
        n = []

        def wait_for(name_list, t, markers=(), any_=True):
            n.append(markers)
            return 0, {"done": [{"name": "pln900-p1", "outcome": "ended_without_marker"}], "pending": [], "timed_out": False, "events": []}
        self.wait = wait_for
        rc = self.invoke(executor, "wait", self.path, "--timeout", "60", "--no-panel")
        self.assertEqual(rc, 75)
        self.assertEqual(self.out.count("o turno acabou sem o marcador"), 1)
        self.assertGreater(len(n), 1)                       # a espera seguiu, e não girou para sempre
        self.assertEqual(len(n[0]), 1)
        self.assertTrue(n[0][0].endswith(":<!-- fim-P1:"))

    def test_done_with_marker_becomes_done(self):
        def wait_for(name_list, t, markers=(), any_=True):
            self.closes_worklog(self.root, "- arquivos: a.py")
            return 0, {"done": [{"name": "pln900-p1", "outcome": "done"}], "pending": [], "timed_out": False, "events": []}
        self.wait = wait_for
        self.assertEqual(self.invoke(executor, "wait", self.path, "--no-panel"), 0)
        self.assertEqual(self.state(), "feito")

    def test_blocked_3_and_failed_1(self):
        self.wait = lambda *a, **k: (0, {"done": [{"name": "pln900-p1", "outcome": "blocked"}], "pending": [], "timed_out": False, "events": []})
        self.assertEqual(self.invoke(executor, "wait", self.path, "--no-panel"), 3)
        self.assertIn("brza sessions read pln900-p1 --last", self.out)
        self.assertEqual(self.state(), "bloqueado")
        self.wait = lambda *a, **k: (1, {"done": [{"name": "pln900-p1", "outcome": "failed"}], "pending": [], "timed_out": False, "events": []})
        self.assertEqual(self.invoke(executor, "wait", self.path, "--no-panel"), 1)
        self.assertEqual(self.state(), "falhou")

    def test_noise_of_host_not_becomes_line(self):
        ev = [{"type": "escalation", "subject": "Worker stopped without reporting", "id": "1"},
              {"type": "question", "subject": "posso apagar?", "id": "2"}]
        self.wait = lambda *a, **k: (75, {"done": [], "pending": [], "timed_out": True, "events": ev})
        self.invoke(executor, "wait", self.path, "--timeout", "10", "--no-panel")
        self.assertNotIn("Worker stopped", self.out)
        self.assertIn("atenção · question — posso apagar?", self.out)

    def test_error_of_brza_and_step_without_executor(self):
        self.wait = lambda *a, **k: (127, {"error": "brza ausente"})
        self.assertEqual(self.invoke(executor, "wait", self.path, "--no-panel"), 1)
        self.assertEqual(self.invoke(executor, "wait", self.path, "P7"), 2)

    def test_missing_session_stops_with_a_clear_message_and_without_spin(self):
        # o `brza sessions wait` de uma sessão inexistente sai rc 1 com `error`; o laço girava sem pausa
        self.wait = lambda *a, **k: (1, {"error": "0 chats abertos se chamam pln900-p1: "})
        self.assertEqual(self.invoke(executor, "wait", self.path, "--timeout", "600", "--no-panel"), 1)
        self.assertEqual(len([x for x in self.calls if x[0] == "wait"]), 1)
        self.assertIn("pln900-p1", self.err)
        self.assertNotIn("pln900-p1,", self.err)
        self.assertIn("não existe", self.err)
        self.assertEqual(self.state(), "falhou")

    def test_only_a_session_lost_index_failure_and_a_other_continues_expected(self):
        m = self.manifest_text(self.root)
        m["steps"]["P2"] = dict(m["steps"]["P1"], session="pln900-p2", worklog=m["steps"]["P1"]["worklog"].replace("p1", "p2"))
        with open(os.path.join(self.root, ".sessions", "pln-900", "execucao.json"), "w") as f:
            json.dump(m, f)
        self.wait = lambda name_list, t, markers=(), any_=True: (
            (1, {"error": "0 chats abertos se chamam pln900-p2: "}) if "pln900-p2" in name_list else (75, {"done": [], "timed_out": True, "events": []}))
        self.assertEqual(self.invoke(executor, "wait", self.path, "P1", "P2", "--timeout", "5", "--no-panel"), 1)
        self.assertEqual(self.manifest_text(self.root)["steps"]["P2"]["state"], "falhou")
        self.assertEqual(self.state(), "em-curso")
        self.assertEqual(self.invoke(executor, "wait", self.path, "--timeout", "5", "--no-panel"), 75)   # o P1 segue esperável

    def test_duplicate_name_stops_and_does_not_say_it_does_not_exist(self):
        self.wait = lambda *a, **k: (1, {"error": "2 chats abertos se chamam pln900-p1: a, b"})
        self.assertEqual(self.invoke(executor, "wait", self.path, "--timeout", "600", "--no-panel"), 1)
        self.assertNotIn("não existe", self.err)
        self.assertIn("2 chats", self.err)

    def test_error_repeated_of_brza_pause_and_gives_up(self):
        self.wait = lambda *a, **k: (1, {"error": "saída sem JSON (rc 1): boom"})
        t0 = self.clock.t
        self.assertEqual(self.invoke(executor, "wait", self.path, "--timeout", "600", "--no-panel"), 1)
        n = len([x for x in self.calls if x[0] == "wait"])
        self.assertEqual(n, executor.MAX_WAIT_ERRORS)
        self.assertGreaterEqual(self.clock.t - t0, executor.WAIT_ERROR_PAUSE * (n - 1))
        self.assertIn("boom", self.err)

    def test_a_line_in_progress_exits_at_the_narration_interval_and_not_on_each_loop(self):
        # A15: com o turno acabado sem o marcador o `wait` volta na hora; a linha prometida é a cada ~3 min
        self.wait = lambda name_list, t, markers=(), any_=True: (
            0, {"done": [{"name": "pln900-p1", "outcome": "ended_without_marker"}], "pending": [], "timed_out": False, "events": []})
        self.assertEqual(self.invoke(executor, "wait", self.path, "--timeout", "600", "--no-panel"), 75)
        lines = [l for l in self.outputs if "em curso" in l]
        self.assertGreaterEqual(len(lines), 2)
        self.assertLessEqual(len(lines), 600 // executor.TICK + 1)

    def test_two_steps_not_pass_marker(self):
        root, path = self.root, self.path
        m = self.manifest_text(root)
        m["steps"]["P2"] = dict(m["steps"]["P1"], session="pln900-p2", worklog=m["steps"]["P1"]["worklog"].replace("p1", "p2"))
        with open(os.path.join(root, ".sessions", "pln-900", "execucao.json"), "w") as f:
            json.dump(m, f)
        seen = []
        self.wait = lambda name_list, t, markers=(), any_=True: (seen.append(markers), (75, {"done": [], "timed_out": True, "events": []}))[1]
        self.invoke(executor, "wait", path, "P1", "P2", "--timeout", "5", "--no-panel")
        self.assertEqual(seen[0], [])

    def test_panel_only_with_event(self):
        self.closes_worklog(self.root, "- arquivos: a.py")
        self.panels.clear()
        self.invoke(executor, "wait", self.path)
        self.assertEqual(len(self.panels), 1)


class SendRework(_exec.Base):
    def test_send_a_step_done_or_stopped_deletes_the_marker_and_the_wait_waits(self):
        # o caminho "não confere: volte ao executor pelo `send`"
        for marker in ("feito", "parado"):
            root, path = self.build()
            self.open_step(root, path)
            self.closes_worklog(root, "- arquivos: a.py", marker)
            self.assertEqual(self.invoke(executor, "wait", path, "--no-panel"), 0)
            self.assertEqual(self.invoke(executor, "send", path, "P1", "--text", "refaça"), 0, self.err)
            self.assertEqual(self.manifest_text(root)["steps"]["P1"]["state"], "em-curso")
            self.assertIsNone(executor.last_marker(self.worklog(root), "P1"))
            self.calls.clear()
            self.assertEqual(self.invoke(executor, "wait", path, "--timeout", "5", "--no-panel"), 75)
            self.assertTrue([x for x in self.calls if x[0] == "wait"])


class Evidence(_exec.Base):
    def setUp(self):
        super().setUp()
        self.root, self.path = self.build()
        self.co, self.sha = self.checkout()
        self.open_step(self.root, self.path, self.co)

    def closes(self, evidence=None, marker="feito"):
        evidence = evidence or ("- commit: brza-studio@%s\n- comando: `pytest -q` → 3 passed (≤ 2 min)\n- arquivos: a.py\n- cobre: todos\n- desvios: X? — nome trocado" % self.sha)
        self.closes_worklog(self.root, evidence, marker)

    def plan_text(self):
        with open(self.path, encoding="utf-8") as f:
            return f.read()

    def test_proposal_checks_and_not_writes(self):
        self.closes()
        before = self.plan_text()
        rc = self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--rerun")
        self.assertEqual(rc, 0, self.err)
        self.assertIn("confere: `git -C %s cat-file -e %s` → ok" % (self.co, self.sha), self.out)
        self.assertIn("confere: `pytest -q` → 3 passed", self.out)
        self.assertIn("**Evidência:** brza-studio@%s · `pytest -q` → 3 passed · arquivos: a.py" % self.sha, self.out)
        self.assertRegex(self.out, r"Executado: [\d.]+ h \(janela; sem medição dos turnos\)")
        self.assertIn("X? — nome trocado", self.out)
        self.assertEqual(self.plan_text(), before)
        self.assertEqual(self.manifest_text(self.root)["steps"]["P1"]["state"], "aberto")

    def test_a_proposal_not_runs_the_command_of_worklog(self):
        # A11: o worklog é entrada de outra sessão; o comando só roda com --apply ou --rerun, depois da leitura
        self.closes()
        called = []
        executor.run_shell = lambda cmd, cwd, timeout=120: (called.append(cmd), (0, "3 passed\n"))[1]
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0"), 0, self.err)
        self.assertEqual(called, [])
        self.assertIn("não rodei `pytest -q`", self.out)
        self.assertIn("a proposta não roda comando do worklog", self.out)
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--rerun"), 0, self.err)
        self.assertEqual(called, ["pytest -q"])
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 0, self.err)
        self.assertEqual(called, ["pytest -q", "pytest -q"])

    def test_command_that_is_not_simple_never_runs(self):
        self.closes("- commit: brza-studio@%s\n- comando: `pytest -q; rm -rf x` → ok (≤ 2 min)\n"
                   "- comando: `echo $(id) | cat` → ok (≤ 2 min)" % self.sha)
        called = []
        executor.run_shell = lambda cmd, cwd, timeout=120: (called.append(cmd), (0, ""))[1]
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--rerun"), 0, self.err)
        self.assertEqual(called, [])
        self.assertEqual(self.out.count("não é um comando que o argv reproduz"), 2)

    def test_hash_in_the_middle_of_a_word_is_not_a_comment_and_cd_expands_tilde(self):
        executor.run_shell = self.originals[(executor, "run_shell")]
        self.assertEqual(executor.parse_command("echo a#b")[2], [("echo", True), ("a#b", True)])
        self.assertEqual(executor.run_shell("echo a#b", self.co)[1].strip(), "a#b")
        rc, stdout = executor.run_shell("cd ~ && pwd", self.co)
        self.assertEqual(stdout.strip(), os.path.realpath(os.path.expanduser("~")))

    def test_covers_marks_only_the_substeps_declared(self):
        self.closes("- commit: brza-studio@%s\n- arquivos: a.py\n- cobre: 1" % self.sha)
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 0, self.err)
        self.assertEqual([c[1] for c in plan_md.load(self.path).step("P1").checks], ["x", " "])
        self.assertNotIn("sem `cobre:`", self.out + self.err)

    def test_covers_all_and_without_declaration_mark_all_and_a_second_warns(self):
        self.closes("- commit: brza-studio@%s\n- arquivos: a.py\n- cobre: todos" % self.sha)
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 0, self.err)
        self.assertEqual([c[1] for c in plan_md.load(self.path).step("P1").checks], ["x", "x"])
        self.assertNotIn("sem `cobre:`", self.out + self.err)

    def test_without_covers_refuses_the_apply_and_does_not_mark(self):
        self.closes("- commit: brza-studio@%s\n- arquivos: a.py" % self.sha)
        before = self.plan_text()
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 1, self.err)
        self.assertEqual(self.plan_text(), before)
        self.assertIn("sem `cobre:`", self.out + self.err)
        self.assertIn("não grava", self.out + self.err)
        self.assertIn("send", self.err)
        self.assertNotEqual(self.manifest_text(self.root)["steps"]["P1"]["state"], "evidencia-gravada")

    def test_proposal_without_covers_does_not_offer_the_apply(self):
        self.closes("- commit: brza-studio@%s\n- arquivos: a.py" % self.sha)
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0"), 0, self.err)
        self.assertIn("proposta: não grave", self.out)
        self.assertNotIn("para gravar no plano", self.out)

    def test_apply_without_covers_does_not_run_the_command(self):
        self.closes("- commit: brza-studio@%s\n- comando: `pytest -q` → 3 passed (≤ 2 min)\n- arquivos: a.py" % self.sha)
        called = []
        executor.run_shell = lambda cmd, cwd, timeout=120: (called.append(cmd), (0, "3 passed"))[1]
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 1, self.err)
        self.assertEqual(called, [])
        self.assertIn("não rodei `pytest -q`: sem `cobre:`", self.out)
        self.assertIn("volte ao executor pelo `send`", self.out)
        self.assertNotIn("a proposta não roda", self.out)
        self.assertNotIn("use `--rerun`", self.out)

    def test_apply_rerun_without_covers_does_not_run_and_does_not_ask_to_rerun(self):
        self.closes("- commit: brza-studio@%s\n- comando: `pytest -q` → 3 passed (≤ 2 min)\n- arquivos: a.py" % self.sha)
        called = []
        executor.run_shell = lambda cmd, cwd, timeout=120: (called.append(cmd), (0, "3 passed"))[1]
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--apply", "--rerun"), 1, self.err)
        self.assertEqual(called, [])
        self.assertIn("não rodei `pytest -q`: sem `cobre:`", self.out)
        self.assertIn("volte ao executor pelo `send`", self.out)
        self.assertNotIn("a proposta não roda", self.out)
        self.assertNotIn("use `--rerun`", self.out)
        self.assertEqual(self.plan_text().count("- [x]"), 0)

    def test_rerun_without_covers_still_runs_the_command(self):
        self.closes("- commit: brza-studio@%s\n- comando: `pytest -q` → 3 passed (≤ 2 min)\n- arquivos: a.py" % self.sha)
        called = []
        executor.run_shell = lambda cmd, cwd, timeout=120: (called.append(cmd), (0, "3 passed\n"))[1]
        before = self.plan_text()
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--rerun"), 0, self.err)
        self.assertEqual(called, ["pytest -q"])
        self.assertIn("confere: `pytest -q`", self.out)
        self.assertIn("proposta: não grave", self.out)
        self.assertEqual(self.plan_text(), before)

    def test_covers_partial_leaves_the_step_reopenable_by_send_and_by_open(self):
        self.closes("- commit: brza-studio@%s\n- arquivos: a.py\n- cobre: 1" % self.sha)
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 0, self.err)
        self.assertEqual(self.manifest_text(self.root)["steps"]["P1"]["state"], "evidencia-gravada")
        # o `send` do que falta: marcador novo e `em-curso`, e o `wait` espera de verdade
        self.assertEqual(self.invoke(executor, "send", self.path, "P1", "--text", "falta o 2"), 0, self.err)
        self.assertEqual(self.manifest_text(self.root)["steps"]["P1"]["state"], "em-curso")
        self.assertIsNone(executor.last_marker(self.worklog(self.root), "P1"))
        self.calls.clear()
        self.assertEqual(self.invoke(executor, "wait", self.path, "--timeout", "5", "--no-panel"), 75)
        self.assertTrue([x for x in self.calls if x[0] == "wait"])
        # o ciclo fecha: cobre o que falta e aplica de novo
        with open(self.worklog(self.root), encoding="utf-8") as f:
            text = f.read()
        with open(self.worklog(self.root), "w", encoding="utf-8") as f:
            f.write(text.replace("- cobre: 1", "- cobre: 1\n- cobre: 2") + "\n<!-- fim-P1: feito -->\n")
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 0, self.err)
        self.assertEqual([c[1] for c in plan_md.load(self.path).step("P1").checks], ["x", "x"])

    def test_open_reopens_the_step_partial_and_refuses_when_not_remains_pending(self):
        self.closes("- commit: brza-studio@%s\n- arquivos: a.py\n- cobre: 1" % self.sha)
        self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--apply")
        self.assertEqual(self.invoke(executor, "open", self.path, "P1", "--checkout", self.co, "--no-panel"), 0, self.err)
        self.assertIsNone(executor.last_marker(self.worklog(self.root), "P1"))

    def test_send_a_step_complete_with_evidence_recorded_not_reopens(self):
        self.closes()
        self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--apply")
        self.invoke(executor, "send", self.path, "P1", "--text", "x")
        self.assertEqual(self.manifest_text(self.root)["steps"]["P1"]["state"], "evidencia-gravada")

    def test_two_lines_covers_join_and_all_wins(self):
        self.closes("- commit: brza-studio@%s\n- arquivos: a.py\n- cobre: 1\n- cobre: 2" % self.sha)
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 0, self.err)
        self.assertEqual([c[1] for c in plan_md.load(self.path).step("P1").checks], ["x", "x"])
        self.assertEqual(executor.read_evidence("## Evidência\n- cobre: 1\n- cobre: todos\n")["covers"], "todos")
        self.assertEqual(executor.read_evidence("## Evidência\n- cobre: 1\n- cobre: 2, 1\n")["covers"], ["1", "2"])

    def test_covers_with_substep_that_not_exists_not_checks(self):
        self.closes("- commit: brza-studio@%s\n- arquivos: a.py\n- cobre: 1, 9" % self.sha)
        before = self.plan_text()
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 1)
        self.assertIn("9", self.err)
        self.assertEqual(self.plan_text(), before)

    def test_command_with_env_and_cd_in_front_and_rechecked(self):
        self.closes("- commit: brza-studio@%s\n- comando: `cd app && PYTHONDONTWRITEBYTECODE=1 python3 -I -m unittest` → 3 passed (≤ 2 min)" % self.sha)
        called = []
        executor.run_shell = lambda cmd, cwd, timeout=120: (called.append(cmd), (0, "3 passed\n"))[1]
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--rerun"), 0, self.err)
        self.assertEqual(len(called), 1)

    def test_run_shell_runs_without_shell_and_accepts_env_cd_glob_and_tilde(self):
        executor.run_shell = self.originals[(executor, "run_shell")]
        self.assertEqual(executor.parse_command("pytest -q 'a b'"), ({}, None, [("pytest", True), ("-q", True), ("a b", False)]))
        for bad in ("a; b", "a && b", "a | b", "a > f", "echo $(x)", "echo `x`", "a\nb", "", "a 'b", "A=1"):
            self.assertIsNone(executor.parse_command(bad), bad)
        rc, stdout = executor.run_shell("echo oi", self.co)
        self.assertEqual((rc, stdout.strip()), (0, "oi"))
        self.assertEqual(executor.run_shell("nao-existe-xyz", self.co)[0], 127)
        self.assertEqual(executor.run_shell("FOO=bar env", self.co)[1].count("FOO=bar"), 1)       # VAR= pelo env
        os.makedirs(os.path.join(self.co, "sub"))
        with open(os.path.join(self.co, "sub", "t1.py"), "w") as f:
            f.write("x")
        self.assertEqual(executor.run_shell("cd sub && pwd", self.co)[1].strip(), os.path.realpath(os.path.join(self.co, "sub")))  # cd pelo cwd
        self.assertEqual(executor.run_shell("ls sub/t*.py", self.co)[1].strip(), "sub/t1.py")     # glob
        self.assertEqual(executor.run_shell("echo 'sub/t*.py'", self.co)[1].strip(), "sub/t*.py")   # aspas: sem glob
        self.assertEqual(executor.run_shell("echo ~", self.co)[1].strip(), os.path.expanduser("~"))

    def test_commit_that_not_exists_not_checks(self):
        self.closes("- commit: brza-studio@deadbee1\n- arquivos: a.py")
        before = self.plan_text()
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 1)
        self.assertIn("NÃO confere", self.out)
        self.assertIn("o passo não fecha", self.err)
        self.assertEqual(self.plan_text(), before)

    def test_command_that_failure_not_checks(self):
        self.closes()
        executor.run_shell = lambda cmd, cwd, timeout=120: (1, "1 failed\n")
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--rerun"), 1)
        self.assertIn("NÃO confere: `pytest -q` → rc 1, 1 failed", self.out)

    def test_command_without_limit_of_time_not_runs(self):
        self.closes("- commit: brza-studio@%s\n- comando: `pytest` → 900 passed" % self.sha)
        called = []
        executor.run_shell = lambda cmd, cwd, timeout=120: (called.append(cmd), (0, ""))[1]
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0"), 0)
        self.assertEqual(called, [])
        self.assertIn("não rodei `pytest`", self.out)

    def test_without_marker_or_without_evidence(self):
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0"), 1)
        self.assertIn("não termina em", self.err)
        self.closes("nada aqui")
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0"), 1)
        self.assertIn("não traz `## Evidência` com itens", self.err)

    def test_stopped_not_applies(self):
        self.closes(marker="parado")
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0"), 0)
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--apply"), 1)
        self.assertIn("parado", self.err)

    def test_apply_writes_marks_sum_and_publish(self):
        self.closes()
        self.panels.clear()
        rc = self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--apply")
        self.assertEqual(rc, 0, self.err)
        pl = plan_md.load(self.path)
        p = pl.step("P1")
        self.assertEqual([c[1] for c in p.checks], ["x", "x"])
        self.assertIn("brza-studio@%s" % self.sha, p.evidence)
        self.assertTrue(p.executed_filled)
        self.assertIn("janela", p.executed_txt)
        self.assertAlmostEqual(float(pl.fm["executed_h"]), p.executed_h, 2)
        man = self.manifest_text(self.root)["steps"]["P1"]
        self.assertEqual(man["state"], "evidencia-gravada")
        self.assertEqual(man["evidence"]["deviations"], ["X? — nome trocado"])
        self.assertEqual(len(self.panels), 1)
        # roda de novo: troca a evidência, não duplica
        self.assertEqual(self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--apply", "--no-panel"), 0)
        self.assertEqual(self.plan_text().count("**Evidência:**"), 1)

    def test_apply_with_evidence_previous_replaces(self):
        self.closes()
        t = self.plan_text().replace("- [ ] **1. A**", "- [ ] **1. A**\n\n**Evidência:** velha · `x` → y\n", 1)
        with open(self.path, "w") as f:
            f.write(t)
        self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--apply", "--no-panel")
        self.assertNotIn("velha", self.plan_text())

    def test_grok_and_without_measurement(self):
        m = self.manifest_text(self.root)
        m["steps"]["P1"]["agent"] = "grok"
        with open(os.path.join(self.root, ".sessions", "pln-900", "execucao.json"), "w") as f:
            json.dump(m, f)
        self.closes()
        self.invoke(executor, "evidence", self.path, "P1", "--settle", "0")
        self.assertIn("Executado: sem medição", self.out)

    def test_claude_measured_by_window_and_by_turns(self):
        self.closes()
        m = self.manifest_text(self.root)
        ev = m["steps"]["P1"]["events"]
        ev[0]["at"] = "2026-11-10T10:00:00-03:00"
        ev.append({"at": "2026-11-10T10:36:00-03:00", "state": "feito", "note": "x"})
        with open(os.path.join(self.root, ".sessions", "pln-900", "execucao.json"), "w") as f:
            json.dump(m, f)
        mp = os.path.join(self.root, "meas.jsonl")
        sp = os.path.join(self.root, "sess.jsonl")
        with open(sp, "w") as f:
            f.write(json.dumps({"event": "open", "name": "pln900-p1", "chat": "c", "agent": "claude", "provider_session": "S1", "at": "2026-11-10T10:00:00-03:00"}) + "\n")
        with open(mp, "w") as f:
            for dur, cost_text, h in ((600, 1.5, "10:10:00"), (840, 1.6, "10:35:30")):
                f.write(json.dumps({"event": "turn", "session_id": "S1", "timestamp": "2026-11-10T%s-03:00" % h,
                                    "duration_s": dur, "estimated_cost_usd": cost_text}) + "\n")
        self.invoke(executor, "evidence", self.path, "P1", "--settle", "0", "--measurements", mp, "--sessions", sp)
        self.assertIn("Executado: 0.6 h (janela; 0.4 h de turnos; US$ 3.10)", self.out)

    def test_parser_of_evidence(self):
        ev = executor.read_evidence("# x\n\n## Evidência\n\n- commit: aguarda confirmação\n- comando: `a b` → ok\n- arquivos: x.py, y.py\n"
                                   "- desvios: nenhum\n\n<!-- fim-P1: feito -->\n\n## Custo da tarefa\n\nUS$ 1\n")
        self.assertTrue(ev["waiting"])
        self.assertEqual(ev["commits"], [])
        self.assertEqual(ev["commands"], [{"cmd": "a b", "result": "ok", "rerun": False}])
        self.assertEqual(ev["files"], ["x.py", "y.py"])
        self.assertIsNone(executor.read_evidence("# sem seção\n"))

    def test_marker_counts_with_the_attachment_of_brza_note(self):
        self.closes()
        with open(self.worklog(self.root), "a") as f:
            f.write("\n## Custo da tarefa\n\nUS$ 1,00\n")
        self.assertEqual(executor.last_marker(self.worklog(self.root), "P1"), "feito")


class CloseSend(_exec.Base):
    def setUp(self):
        super().setUp()
        self.root, self.path = self.build()
        self.open_step(self.root, self.path)

    def state(self):
        return self.manifest_text(self.root)["steps"]["P1"]["state"]

    def switches_lookup(self, f):
        self.lookup_orig = executor._lookup
        executor._lookup = f

    def test_closing_is_not_closed(self):
        self.sessions = lambda argv: (0, json.dumps({"status": "closing"}), "")
        self.assertEqual(self.invoke(executor, "close", self.path, "P1", "--no-panel"), 0)
        self.assertIn("NÃO está fechada", self.out)
        self.assertEqual(self.state(), "aberto")
        argv = [a for k, a in self.calls if k == "sessions"][-1]
        self.assertEqual(argv, ["close", "pln900-p1", "--json"])

    def test_acceptance_checks_and_closes(self):
        self.sessions = lambda argv: (0, json.dumps({"status": "closing"}), "")
        self.switches_lookup(lambda pl, name: ("encerrada e aceita", None))
        try:
            self.assertEqual(self.invoke(executor, "close", self.path, "P1", "--wait-settled", "30"), 0)
        finally:
            executor._lookup = self.lookup_orig
        self.assertIn("P1 · encerrada e aceita", self.out)
        self.assertEqual(self.state(), "fechado")
        self.assertTrue(self.panels[-1]["png"])

    def test_deadline_of_acceptance_75_and_uncertain_75(self):
        self.sessions = lambda argv: (0, json.dumps({"status": "closing"}), "")
        self.switches_lookup(lambda pl, name: ("ativa", None))
        try:
            self.assertEqual(self.invoke(executor, "close", self.path, "P1", "--wait-settled", "20", "--no-panel"), 75)
        finally:
            executor._lookup = self.lookup_orig
        self.sessions = lambda argv: (75, json.dumps({"status": "stop_unknown"}), "")
        self.assertEqual(self.invoke(executor, "close", self.path, "P1"), 75)

    def test_modes_of_close(self):
        self.sessions = lambda argv: (0, json.dumps({"status": "kept_open"}), "")
        self.invoke(executor, "close", self.path, "P1", "--keep-open")
        self.assertEqual([a for k, a in self.calls if k == "sessions"][-1], ["close", "pln900-p1", "--keep-open", "--json"])
        self.assertIn("mantida aberta", self.out)

    def test_verdict(self):
        v = executor.verdict({"worker": {"state": "succeeded", "stage": "settled"}, "dispatch": {"completedAt": "x"}})[0]
        self.assertEqual(v, "encerrada e aceita")
        self.assertEqual(executor.verdict({"result": {"worker": {"state": "running"}}})[0], "ativa")
        self.assertEqual(executor.verdict({"worker": {"state": "failed"}})[0], "falhou")

    def test_send_uses_one_call_and_reopens_the_state(self):
        self.sessions = lambda argv: (0, json.dumps({"receipts": [{"status": "delivered"}]}), "")
        self.assertEqual(self.invoke(executor, "send", self.path, "P1", "--text", "use X", "--operation", "op1"), 0)
        argv = [a for k, a in self.calls if k == "sessions"][-1]
        self.assertEqual(argv, ["send", "pln900-p1", "--text", "use X", "--json", "--operation", "op1"])
        self.assertEqual(self.state(), "em-curso")

    def test_send_uncertain_not_resends(self):
        self.sessions = lambda argv: (75, json.dumps({"receipts": [{"status": "pending"}]}), "")
        self.assertEqual(self.invoke(executor, "send", self.path, "P1", "--text", "x"), 75)
        self.assertIn("não reenvie", self.err)

    def test_status(self):
        self.assertEqual(self.invoke(executor, "status", self.path), 0)
        self.assertRegex(self.out, r"P1 · pln900-p1 · aberto · aberto há \d+ min")
        self.invoke(executor, "status", self.path, "--json")
        self.assertEqual(json.loads(self.out)["steps"][0]["session"], "pln900-p1")

    def test_status_without_manifest(self):
        root, path = self.build()
        self.invoke(executor, "status", path)
        self.assertIn("sem executor aberto", self.out)


if __name__ == "__main__":
    import unittest
    unittest.main()
