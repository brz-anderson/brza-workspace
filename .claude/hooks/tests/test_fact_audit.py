"""Testes do fact_audit.py, modo `stop`: a captura das marcas de confiança na devolução e nos arquivos do subagente.

Os transcripts são montados pelo próprio teste, em diretório temporário.

    python3 -m unittest discover -s .claude/hooks/tests
"""

import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))


def load_fact_audit(directory):
    os.environ["MEASURE_DIR"] = directory
    spec = importlib.util.spec_from_file_location("fact_audit", os.path.join(os.path.dirname(HERE), "fact_audit.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.measure.settle = lambda path, **_: None  # o transcript do teste não cresce
    return module


def assistant(*blocks):
    return json.dumps({"type": "assistant", "timestamp": "2026-10-31T00:00:00Z", "requestId": "r",
                       "message": {"role": "assistant", "content": list(blocks)}})


def text(value):
    return {"type": "text", "text": value}


def write_tool(path, content):
    return {"type": "tool_use", "id": "t", "name": "Write", "input": {"file_path": path, "content": content}}


def handback(message):
    return {"type": "tool_use", "id": "h", "name": "SubagentHandback", "input": {"message": message}}


REAL_TRANSCRIPT = ("/Users/andepb/.claude/projects/-Users-andepb-Projects-brza-workspace--worktrees-workspace/"
                   "746b7a51-6fa4-47d9-95ef-35afb7fcc654/subagents/agent-a4e396c649819d3fd.jsonl")


def user(value):
    return json.dumps({"type": "user", "message": {"role": "user", "content": value}})


class FactAuditTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(os.environ.pop, "MEASURE_DIR", None)
        self.addCleanup(os.environ.pop, "BRZA_FACT_AUDIT", None)
        os.environ.pop("BRZA_FACT_AUDIT", None)
        self.fa = load_fact_audit(self.tmp.name)
        self.transcript = os.path.join(self.tmp.name, "agent-a1.jsonl")
        self.payload = {"session_id": "s1", "cwd": self.tmp.name, "agent_id": "a1", "agent_type": "designer",
                        "agent_transcript_path": self.transcript}

    def append(self, *lines):
        with open(self.transcript, "a", encoding="utf-8") as f:
            f.write("".join(line + "\n" for line in lines))

    def run_hook(self, payload=None, mode="stop"):
        payload = self.payload if payload is None else payload
        with mock.patch.object(sys, "argv", ["fact_audit.py", mode]), \
                mock.patch.object(sys, "stdin", io.StringIO(json.dumps(payload))):
            with self.assertRaises(SystemExit) as raised:
                self.fa.main()
        self.assertEqual(raised.exception.code, 0)

    def logged(self):
        try:
            with open(self.fa.measure.LOG, encoding="utf-8") as f:
                return [json.loads(line) for line in f.read().splitlines()]
        except FileNotFoundError:
            return []

    def events(self, name):
        return [e for e in self.logged() if e["event"] == name]

    def test_marks_in_the_reply_and_in_a_write_become_facts_with_their_source(self):
        self.append(
            user("desenhe"),
            assistant(text("vou gravar"), write_tool("/x/rascunho.md",
                      "# Rascunho\n- o timeout é 30 [F1 · lido · 90]\n- vale `x` [F2 · doc · 75]\n")),
            assistant(text("Resumo\n  - o preço é 0,10 [F3 · rodado · 100]  \n- talvez [C1 · inferido · 40] sirva")))
        self.run_hook()
        facts = self.events("fact")
        self.assertEqual([(f["fact_id"], f["kind"], f["confidence"], f["source"]) for f in facts],
                         [("F1", "lido", 90, "/x/rascunho.md"), ("F2", "doc", 75, "/x/rascunho.md"),
                          ("F3", "rodado", 100, "reply"), ("C1", "inferido", 40, "reply")])
        self.assertEqual(facts[0]["text"], "- o timeout é 30 [F1 · lido · 90]")
        self.assertEqual(facts[2]["text"], "- o preço é 0,10 [F3 · rodado · 100]")  # sem espaços nas pontas
        first = facts[0]
        self.assertEqual((first["session_id"], first["agent_id"], first["agent_type"]), ("s1", "a1", "designer"))
        self.assertIn("timestamp", first)
        self.assertIn("workstream", first)
        self.assertIsInstance(first["confidence"], int)
        captures = self.events("fact_capture")
        self.assertEqual(len(captures), 1)
        c = captures[0]
        self.assertEqual((c["facts"], c["malformed"], c["segment"], c["agent_id"], c["agent_type"]),
                         (4, 0, "first", "a1", "designer"))
        self.assertFalse(c.get("unmarked"))

    def test_subagent_handback_is_the_reply(self):
        self.append(user("x"), assistant(handback("## Devolução\n- o timeout é 30 [F1 · lido · 90]\n- custo [C1 · inferido · 40]")))
        self.run_hook()
        self.assertEqual([(f["fact_id"], f["source"]) for f in self.events("fact")], [("F1", "reply"), ("C1", "reply")])
        self.assertFalse(self.events("fact_capture")[0].get("unmarked"))

    def test_handback_wins_over_an_earlier_text_in_the_segment(self):
        self.append(user("x"), assistant(text("rascunho [F1 · lido · 90]")),
                    assistant(handback("final [F2 · doc · 80]")))
        self.run_hook()
        self.assertEqual([f["fact_id"] for f in self.events("fact")], ["F2"])

    def test_last_handback_wins_and_a_later_text_does_not_replace_it(self):
        self.append(user("x"), assistant(handback("a [F1 · lido · 90]")), assistant(handback("b [F2 · lido · 90]")),
                    assistant(text("depois [F3 · lido · 90]")))
        self.run_hook()
        self.assertEqual([f["fact_id"] for f in self.events("fact")], ["F2"])

    def test_text_is_the_fallback_without_handback(self):
        self.append(user("x"), assistant(text("a [F1 · lido · 90]")), assistant(text("b [F2 · lido · 90]")))
        self.run_hook()
        self.assertEqual([f["fact_id"] for f in self.events("fact")], ["F2"])

    def test_handback_without_marks_is_unmarked(self):
        self.append(user("x"), assistant(handback("sem marca")))
        self.run_hook()
        self.assertTrue(self.events("fact_capture")[0]["unmarked"])

    def test_real_transcript_before_p2_is_unmarked(self):
        if not os.path.exists(REAL_TRANSCRIPT):
            self.skipTest("transcript real ausente")
        self.run_hook({**self.payload, "agent_transcript_path": REAL_TRANSCRIPT})
        self.assertEqual(self.events("fact"), [])
        capture = self.events("fact_capture")[0]
        self.assertIs(capture["unmarked"], True)
        self.assertEqual(capture["segment"], "first")

    def test_text_of_a_fact_stops_at_300_characters(self):
        self.append(user("x"), assistant(text("a" * 400 + " [F1 · lido · 90]")))
        self.run_hook()
        self.assertEqual(len(self.events("fact")[0]["text"]), 300)

    def test_only_the_last_text_message_of_the_segment_is_read(self):
        self.append(user("x"), assistant(text("rascunho [F1 · lido · 90]")),
                    assistant({"type": "tool_use", "id": "t2", "name": "Bash", "input": {"command": "ls"}}),
                    assistant(text("final [F2 · lido · 80]")),
                    assistant({"type": "tool_use", "id": "t3", "name": "Bash", "input": {"command": "ls"}}))
        self.run_hook()
        self.assertEqual([f["fact_id"] for f in self.events("fact")], ["F2"])

    def test_repeated_id_between_write_and_reply_is_one_fact(self):
        self.append(user("x"), assistant(write_tool("/x/a.md", "[F1 · lido · 90] no arquivo")),
                    assistant(text("de novo [F1 · lido · 60] e [F2 · doc · 70]")))
        self.run_hook()
        facts = self.events("fact")
        self.assertEqual([(f["fact_id"], f["source"], f["confidence"]) for f in facts],
                         [("F1", "/x/a.md", 90), ("F2", "reply", 70)])  # a primeira ocorrência fica
        self.assertEqual(self.events("fact_capture")[0]["facts"], 2)

    def test_resume_records_only_new_ids_and_marks_the_segment(self):
        self.append(user("x"), assistant(text("[F1 · lido · 90]")))
        self.run_hook()
        self.append(user("continue"), assistant(text("[F1 · lido · 90] e [F2 · rodado · 95]")))
        self.run_hook()
        self.assertEqual([f["fact_id"] for f in self.events("fact")], ["F1", "F2"])
        captures = self.events("fact_capture")
        self.assertEqual([(c["segment"], c["facts"]) for c in captures], [("first", 1), ("resume", 1)])
        self.assertFalse(captures[1].get("unmarked"))  # a devolução tinha marcas, só que já vistas

    def test_empty_segment_writes_nothing_and_does_not_advance(self):
        self.append(user("x"), assistant(text("[F1 · lido · 90]")))
        self.run_hook()
        before = len(self.logged())
        state = self.read_state()
        self.run_hook()  # nada novo no transcript
        self.assertEqual(len(self.logged()), before)
        self.assertEqual(self.read_state(), state)

    def read_state(self):
        with open(os.path.join(self.fa.measure.DIR, "fact-audit-state.json"), encoding="utf-8") as f:
            return json.load(f)

    def test_state_keeps_the_offset_and_the_seen_ids_by_transcript(self):
        self.append(user("x"), assistant(text("[F1 · lido · 90] [C2 · doc · 50]")))
        self.run_hook()
        entry = self.read_state()[self.transcript]
        self.assertEqual(entry["offset"], os.path.getsize(self.transcript))
        self.assertEqual(sorted(entry["seen"]), ["C2", "F1"])

    def test_other_agent_types_write_nothing(self):
        self.append(user("x"), assistant(text("[F1 · lido · 90]")))
        for kind in ("implementer", "reviewer", None):
            self.run_hook({**self.payload, "agent_type": kind})
        self.assertEqual(self.logged(), [])
        self.assertFalse(os.path.exists(os.path.join(self.fa.measure.DIR, "fact-audit-state.json")))

    def test_agent_type_falls_back_to_the_meta_file(self):
        self.append(user("x"), assistant(text("[F1 · lido · 90]")))
        with open(self.transcript.replace(".jsonl", ".meta.json"), "w", encoding="utf-8") as f:
            json.dump({"agentType": "collector"}, f)
        self.run_hook({k: v for k, v in self.payload.items() if k != "agent_type"})
        facts = self.events("fact")
        self.assertEqual([(f["fact_id"], f["agent_type"]) for f in facts], [("F1", "collector")])

    def test_collector_is_audited(self):
        self.append(user("x"), assistant(text("[C1 · lido · 90]")))
        self.run_hook({**self.payload, "agent_type": "collector"})
        self.assertEqual(self.events("fact")[0]["agent_type"], "collector")

    def test_env_flag_of_the_audit_itself_writes_nothing(self):
        self.append(user("x"), assistant(text("[F1 · lido · 90]")))
        os.environ["BRZA_FACT_AUDIT"] = "1"
        self.run_hook()
        self.assertEqual(self.logged(), [])

    def test_malformed_marks_are_counted(self):
        self.append(user("x"), assistant(text(
            "a [F4 · lido] b [F5 · visto · 90] c [F6 · lido · 120] d [F7 · lido · 90]")))
        self.run_hook()
        self.assertEqual([f["fact_id"] for f in self.events("fact")], ["F7"])
        c = self.events("fact_capture")[0]
        self.assertEqual((c["facts"], c["malformed"]), (1, 3))

    def test_confidence_bounds(self):
        self.append(user("x"), assistant(text("[F1 · lido · 0] [F2 · lido · 100] [F3 · lido · 101] [F4 · lido · 1000]")))
        self.run_hook()
        self.assertEqual([(f["fact_id"], f["confidence"]) for f in self.events("fact")], [("F1", 0), ("F2", 100)])
        self.assertEqual(self.events("fact_capture")[0]["malformed"], 2)

    def test_malformed_mark_in_a_write_is_counted_too(self):
        self.append(user("x"), assistant(write_tool("/x/a.md", "[F1 · lido]\n[F2 · lido · 90]")), assistant(text("ok")))
        self.run_hook()
        c = self.events("fact_capture")[0]
        self.assertEqual((c["facts"], c["malformed"]), (1, 1))

    def test_reply_without_marks_is_unmarked(self):
        self.append(user("x"), assistant(text("Nada marcado, e um [link](x) e [F] e [Fx]")))
        self.run_hook()
        self.assertEqual(self.events("fact"), [])
        c = self.events("fact_capture")[0]
        self.assertEqual((c["facts"], c["malformed"], c["unmarked"], c["segment"]), (0, 0, True, "first"))

    def test_forced_exception_becomes_hook_error_and_exits_zero(self):
        self.append(user("x"), assistant(text("[F1 · lido · 90]")))
        self.fa.measure.read_from = mock.Mock(side_effect=RuntimeError("boom"))
        self.run_hook()
        errors = self.events("hook_error")
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["mode"], "fact_audit:stop")
        self.assertIn("boom", errors[0]["error"])
        self.assertEqual(self.events("fact"), [])

    def test_invalid_payload_and_unknown_mode_become_hook_error(self):
        with mock.patch.object(sys, "argv", ["fact_audit.py", "stop"]), mock.patch.object(sys, "stdin", io.StringIO("{")):
            with self.assertRaises(SystemExit) as raised:
                self.fa.main()
        self.assertEqual(raised.exception.code, 0)
        self.run_hook(mode="nada")
        self.assertEqual([e["mode"] for e in self.events("hook_error")], ["fact_audit:stop", "fact_audit:nada"])

    def test_missing_transcript_writes_nothing(self):
        self.run_hook()
        self.assertEqual(self.logged(), [])


if __name__ == "__main__":
    unittest.main()
