import json
import os

import _exec
import _paths  # noqa: F401
import consult
import executor
from mini import DESIGN, ROUND1, step, plan

END_TEXT = "<!-- fim-D1: %s -->"
QUOTA_REAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "quota-real.json")   # a saída do `brza quota --json`


def quota_json(quota):
    """O `brza quota --json` real (fixture) com a janela de cada runtime trocada: `session`, ou `weekly` quando é a única."""
    with open(QUOTA_REAL, encoding="utf-8") as f:
        d = json.load(f)
    for account in d["accounts"]:
        if account["active"] and account["runtime"] in quota:
            name_list = {w["name"]: w for w in account["windows"]}
            name_list.get("session", name_list.get("weekly"))["used"] = quota[account["runtime"]]
    return json.dumps(d)


class Consultants(_exec.Base):
    def setUp(self):
        super().setUp()
        self.root, self.path = self.build()
        self.brief = os.path.join(self.root, "brief.md")
        with open(self.brief, "w", encoding="utf-8") as f:
            f.write("# Brief\n\nTerreno: x.\nCasos: um, dois.\n")
        self.quota = {"claude": 20, "codex": 30, "grok": 10}
        self.brza = lambda argv: (0, quota_json(self.quota), "")

    def open_step(self, *extra):
        return self.invoke(consult, "open", self.path, "D1", "--brief", self.brief, "--no-panel", *extra)

    def man(self):
        with open(os.path.join(self.root, ".sessions", "pln-900", "D1", "consultants.json"), encoding="utf-8") as f:
            return json.load(f)

    def writes(self, focus, body_text, marker=True):
        p = os.path.join(self.root, ".sessions", "pln-900", "D1", focus + ".md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(body_text + ("\n" + END_TEXT % focus + "\n" if marker else ""))

    def test_roster_default_opens_three_in_runtimes_different(self):
        self.assertEqual(self.open_step(), 0, self.err)
        opened = [a for k, a in self.calls if k == "sessions"]
        self.assertEqual([a[a.index("--agent") + 1] for a in opened], ["claude", "codex", "grok"])
        self.assertEqual(opened[0][opened[0].index("--model") + 1], "claude-opus-5-5")
        self.assertEqual(opened[0][opened[0].index("--effort") + 1], "high")
        self.assertEqual(opened[0][0], "pln900-d1-arquitetura-limpa")
        self.assertEqual(opened[1][opened[1].index("--model") + 1], executor.CODEX_MODEL)   # A1: --effort exige --model
        self.assertEqual(opened[1][opened[1].index("--effort") + 1], "xhigh")
        for a in opened:
            self.assertEqual("--effort" in a, "--model" in a, a)
        self.assertEqual(opened[0][opened[0].index("--checkout") + 1], self.root)
        self.assertIn("| arquitetura-limpa | pln900-d1-arquitetura-limpa | Claude |", self.out)
        self.assertEqual(sorted(self.man()["focuses"]), ["arquitetura-limpa", "equilibrio", "mudanca-minima"])

    def test_prompt_starts_by_consultant_and_sends_write_only_the_file(self):
        self.open_step()
        with open(os.path.join(self.root, ".sessions", "pln-900", "D1", "prompt-mudanca-minima.md"), encoding="utf-8") as f:
            t = f.read()
        self.assertTrue(t.startswith("Você é consultor do Desenho de D1 do PLN-900"))
        self.assertIn("Terreno: x.", t)
        self.assertIn("Grave SÓ o arquivo", t)
        self.assertIn("<!-- fim-D1: mudanca-minima -->", t)
        self.assertIn("Não envie `worker_done`", t)

    def test_quota_above_of_55_switches_by_fallback(self):
        self.quota["codex"] = 56
        self.open_step()
        opened = [a for k, a in self.calls if k == "sessions"]
        self.assertEqual(opened[1][opened[1].index("--agent") + 1], "claude")
        self.assertEqual(opened[1][opened[1].index("--model") + 1], "claude-sonnet-5-5")
        self.assertIn("cota: codex cortado: codex a 56%", self.out)
        self.assertEqual(self.man()["focuses"]["mudanca-minima"]["agent"], "claude")

    def test_quotas_read_a_shape_real_of_brza_quota(self):
        # A2: `accounts[].windows[]`, a conta ativa de cada runtime; o Grok só tem `weekly`
        with open(QUOTA_REAL, encoding="utf-8") as f:
            real = f.read()
        self.brza = lambda argv: (0, real, "")
        self.assertEqual(consult.quotas(), {"claude": 30, "codex": 0, "grok": 22, "antigravity": 3})

    def test_quota_of_claude_by_shape_real_strips_and_not_warns(self):
        self.quota["claude"] = 80
        self.open_step()
        opened = [a for k, a in self.calls if k == "sessions"]
        self.assertEqual(opened[0][opened[0].index("--agent") + 1], "grok")       # o fallback da arquitetura-limpa
        self.assertNotIn("não li o `brza quota --json`", self.err)

    def test_roster_with_effort_without_model_in_a_runtime_without_default_loses_the_effort(self):
        r = os.path.join(self.root, "r.json")
        with open(r, "w") as f:
            json.dump({"consultants": [{"focus": "a", "agent": "grok", "effort": "high"}, {"focus": "b", "agent": "codex", "effort": "high"}]}, f)
        self.open_step("--roster", r)
        opened = [a for k, a in self.calls if k == "sessions"]
        self.assertNotIn("--effort", opened[0])
        self.assertEqual(opened[1][opened[1].index("--model") + 1], executor.CODEX_MODEL)
        self.assertIn("recusa --effort sem --model", self.err)

    def test_quota_equal_a_55_enters(self):
        self.quota["claude"] = 55
        self.open_step()
        self.assertEqual([a[a.index("--agent") + 1] for k, a in self.calls if k == "sessions"][0], "claude")

    def test_without_quota_warns_and_not_strips(self):
        self.brza = lambda argv: (1, "", "falhou")
        self.assertEqual(self.open_step(), 0)
        self.assertIn("não li o `brza quota --json`", self.err)

    def test_roster_own(self):
        r = os.path.join(self.root, "r.json")
        with open(r, "w") as f:
            json.dump({"consultants": [{"focus": "a", "agent": "grok"}, {"focus": "b", "agent": "grok"}]}, f)
        self.open_step("--roster", r)
        self.assertEqual(sorted(self.man()["focuses"]), ["a", "b"])
        with open(r, "w") as f:
            f.write("[]")
        self.assertEqual(self.open_step("--roster", r), 2)

    def test_dry_run_not_opens(self):
        self.assertEqual(self.open_step("--dry-run"), 0)
        self.assertEqual([k for k, _ in self.calls if k == "sessions"], [])
        self.assertIn("[dry-run] brza sessions pln900-d1-arquitetura-limpa", self.out)
        self.assertFalse(os.path.exists(os.path.join(self.root, ".sessions")))

    def test_not_opened_stops_the_batch(self):
        self.sessions = lambda argv: (1, "", "CHECK: x não abriu: pending-1.json")
        self.assertEqual(self.open_step(), 1)
        self.assertEqual(len([1 for k, _ in self.calls if k == "sessions"]), 1)

    def test_decision_missing_and_brief_missing(self):
        self.assertEqual(self.invoke(consult, "open", self.path, "D9", "--brief", self.brief), 2)
        self.assertEqual(self.invoke(consult, "open", self.path, "D1", "--brief", "/nao/existe.md"), 2)

    def test_wait_narrates_each_arrival_and_reaches_zero(self):
        self.open_step()
        self.writes("arquitetura-limpa", "Tese: a.")
        self.writes("mudanca-minima", "Tese: b.")
        self.writes("equilibrio", "Tese: c.")
        self.assertEqual(self.invoke(consult, "wait", self.path, "D1"), 0)
        self.assertEqual(self.out.count("entregou"), 3)
        self.assertIn("D1 · 3/3 — entregaram", self.out)

    def test_wait_deadline_75_listing_who_missing_ids(self):
        self.open_step()
        self.writes("equilibrio", "Tese: c.")
        self.assertEqual(self.invoke(consult, "wait", self.path, "D1", "--timeout", "20"), 75)
        self.assertIn("prazo: faltam arquitetura-limpa, mudanca-minima", self.out)

    def test_wait_file_without_marker_not_counts_and_failure_of_session(self):
        self.open_step()
        self.writes("equilibrio", "Tese: c.", marker=False)
        self.wait = lambda name_list, t, markers=(), any_=True: (0, {"done": [{"name": "pln900-d1-equilibrio", "outcome": "done"}], "timed_out": False, "events": []})
        self.assertEqual(self.invoke(consult, "wait", self.path, "D1", "--timeout", "30"), 75)
        self.assertIn("o turno acabou sem o marcador", self.out)
        self.wait = lambda name_list, t, markers=(), any_=True: (1, {"done": [{"name": "pln900-d1-equilibrio", "outcome": "failed"}], "timed_out": False, "events": []})
        self.assertEqual(self.invoke(consult, "wait", self.path, "D1", "--timeout", "30"), 1)

    def test_wait_session_lost_index_marks_only_that_focus_and_continues_with_the_others(self):
        self.open_step()
        self.wait = lambda name_list, t, markers=(), any_=True: (
            (1, {"error": "0 chats abertos se chamam pln900-d1-equilibrio: "}) if "pln900-d1-equilibrio" in name_list
            else (75, {"done": [], "timed_out": True, "events": []}))
        self.assertEqual(self.invoke(consult, "wait", self.path, "D1", "--timeout", "60"), 1)
        self.assertEqual(self.man()["focuses"]["equilibrio"]["state"], "falhou")
        self.assertEqual(self.man()["focuses"]["mudanca-minima"]["state"], "aberto")
        self.assertIn("a espera segue com as outras", self.out)
        # as outras ainda esperam depois do erro (mais de uma chamada)
        self.assertGreater(len([x for x in self.calls if x[0] == "wait"]), 1)

    def test_wait_error_repeated_pause_and_gives_up(self):
        self.open_step()
        self.wait = lambda *a, **k: (1, {"error": "saída sem JSON (rc 1): boom"})
        self.assertEqual(self.invoke(consult, "wait", self.path, "D1", "--timeout", "600"), 1)
        self.assertEqual(len([x for x in self.calls if x[0] == "wait"]), executor.MAX_WAIT_ERRORS)

    def test_wait_a_line_in_progress_exits_on_each_tick_and_not_on_each_loop(self):
        # A15: o turno acaba sem o marcador, o `wait` volta na hora
        self.open_step()
        self.wait = lambda name_list, t, markers=(), any_=True: (0, {"done": [{"name": "pln900-d1-equilibrio", "outcome": "done"}], "timed_out": False, "events": []})
        self.assertEqual(self.invoke(consult, "wait", self.path, "D1", "--timeout", "600"), 75)
        lines = [l for l in self.outputs if "em curso" in l]
        self.assertGreaterEqual(len(lines), 2)
        self.assertLessEqual(len(lines), 600 // consult.TICK + 1)

    def test_table_side_by_side_with_the_three_files(self):
        self.open_step()
        self.writes("arquitetura-limpa", "Tese: JSON.\n\n- **Caso 1:** Custo: 3 h · Se paga: já · Reabre: o schema\n- **Caso 2:** Custo: 1 h · Se paga: com anexo · Reabre: nada\n\nRisco: ninguém abre JSON.")
        self.writes("mudanca-minima", "Tese: Markdown.\n\n**Custo:** 1 h\n**Se paga:** agora\n**Reabre:** o importador\nRisco: sem metadado\n  que continua aqui.")
        self.writes("equilibrio", "Tese: YAML.\nCusto: 2 h · Se paga: já · Reabre: pouco\nRisco: formato novo")
        pub = os.path.join(self.root, "pub")
        self.assertEqual(self.invoke(consult, "table", self.path, "D1", "--publish-dir", pub), 0, self.err)
        lines = self.outputs[0].split("\n")
        self.assertEqual(lines[0], "| | arquitetura-limpa (Claude) | mudanca-minima (Codex) | equilibrio (Grok) |")
        self.assertIn("| **Custo** | 3 h / 1 h | 1 h | 2 h |", lines)
        self.assertIn("| **Se paga** | já / com anexo | agora | já |", lines)
        self.assertIn("| **Reabre** | o schema / nada | o importador | pouco |", lines)
        self.assertIn("| **Risco** | ninguém abre JSON. | sem metadado que continua aqui. | formato novo |", lines)
        self.assertRegex(self.outputs[-1], r'^::orca-visual\{file="pln-900-d1-[0-9a-f]{4}\.html" title="PLN-900 D1')
        name = self.outputs[-1].split('"')[1]
        with open(os.path.join(pub, name), encoding="utf-8") as f:
            self.assertIn("arquitetura-limpa", f.read())

    def test_table_with_focus_that_not_delivered(self):
        self.open_step()
        self.writes("equilibrio", "Tese: YAML.\nCusto: 2 h")
        self.invoke(consult, "table", self.path, "D1", "--publish-dir", os.path.join(self.root, "pub"))
        self.assertIn("(não entregou)", self.out)
        self.assertIn("sem arquivo com o marcador", self.err)
        self.assertIn("o arquivo não traz `Se paga:`", self.err)

    def test_close_one_by_one(self):
        self.open_step()
        self.sessions = lambda argv: (0, json.dumps({"status": "released"}), "")
        self.assertEqual(self.invoke(consult, "close", self.path, "D1"), 0)
        self.assertEqual({v["state"] for v in self.man()["focuses"].values()}, {"fechado"})
        closures = [a for k, a in self.calls if k == "sessions" and a[0] == "close"]
        self.assertEqual(len(closures), 3)
        self.sessions = lambda argv: (0, json.dumps({"status": "closing"}), "")
        self.assertIn("NÃO está fechada", (self.invoke(consult, "close", self.path, "D1"), self.out)[1])

    def test_pipe_in_cell_not_breaks_a_table(self):
        self.assertEqual(consult.escape_cell("a | b\nc"), "a \\| b c")


if __name__ == "__main__":
    import unittest
    unittest.main()
