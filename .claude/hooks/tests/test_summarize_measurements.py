"""Testes do `scripts/summarize_measurements.py --by-workstream`, sobre um log montado pelo teste em diretório temporário.

    python3 -m unittest discover -s .claude/hooks/tests
"""

import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "..", "..", "scripts", "summarize_measurements.py")


def load():
    spec = importlib.util.spec_from_file_location("summarize", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def turn(day, workstream, cost, rounds=None, **extra):
    row = {"event": "turn", "timestamp": f"{day}T10:00:00-03:00", "estimated_cost_usd": cost, "api_calls": 1,
           "rounds": rounds}
    if workstream:
        row["workstream"] = workstream
    return {**row, **extra}


def mem(day, hour, workstream, owner, action, file, kind):
    return {"event": "memory", "timestamp": f"{day}T{hour}:00:00-03:00", "workstream": workstream, "owner": owner,
            "action": action, "file": file, "type": kind}


ROUNDS = {"questions": 4, "recommended": 2, "other_option": 1, "free_text": 1}

ROWS = [
    turn("2026-10-28", "studio", 1.0, ROUNDS),
    turn("2026-10-28", "studio", 3.0, {"questions": 0, "recommended": 0, "other_option": 0, "free_text": 0}),
    turn("2026-10-29", "studio", 2.0),
    turn("2026-10-28", None, 0.5),  # a linha antiga, sem workstream
    {"event": "subagent", "timestamp": "2026-10-28T11:00:00-03:00", "workstream": "studio", "agent_type": "collector",
     "estimated_cost_usd": 0.4},
    {"event": "subagent", "timestamp": "2026-10-28T11:30:00-03:00", "workstream": "studio", "agent_type": "collector",
     "estimated_cost_usd": 0.6},
    {"event": "subagent", "timestamp": "2026-10-28T12:00:00-03:00", "workstream": "studio", "agent_type": "fixfy:reviewer",
     "estimated_cost_usd": 2.0},
    mem("2026-10-28", "09", "studio", "session", "created", "memory/a.md", "feedback"),
    mem("2026-10-28", "09", "studio", "session", "created", "memory/b.md", "user"),
    mem("2026-10-28", "09", "studio", "session", "updated", "memory/MEMORY.md", "index"),  # o índice não conta
    mem("2026-10-28", "10", "studio", "reviewer", "created", ".claude/agent-memory/reviewer/c.md", "project"),
    mem("2026-10-29", "09", "studio", "session", "updated", "memory/a.md", "feedback"),
    mem("2026-10-29", "10", "studio", "session", "deleted", "memory/b.md", "user"),
    mem("2026-10-29", "11", "tools-kit", "session", "created", "memory/z.md", "reference"),
    {"event": "skill", "timestamp": "2026-10-28T11:00:00-03:00", "skill": "x"},  # ignorada
]


class ByWorkstreamTest(unittest.TestCase):
    def setUp(self):
        self.summarize = load()
        self.days = self.summarize.aggregate_by_workstream(ROWS)

    def test_turns_cost_and_mean_per_workstream_and_day(self):
        day = self.days[("studio", "2026-10-28")]
        self.assertEqual((day["turns"]["n"], day["turns"]["cost"]), (2, 4.0))
        self.assertEqual(self.summarize.mean(day["turns"]), "2.00")
        self.assertEqual(self.days[("studio", "2026-10-29")]["turns"]["n"], 1)

    def test_old_line_without_workstream_goes_to_its_bucket(self):
        self.assertEqual(self.days[("(sem workstream)", "2026-10-28")]["turns"]["n"], 1)

    def test_subagent_cost_by_agent_type(self):
        agents = self.days[("studio", "2026-10-28")]["subagents"]
        self.assertEqual((agents["collector"]["n"], round(agents["collector"]["cost"], 2)), (2, 1.0))
        self.assertEqual(agents["reviewer"]["cost"], 2.0)  # o prefixo do plugin sai

    def test_memory_by_owner_with_feedback_apart_and_index_out(self):
        memory = self.days[("studio", "2026-10-28")]["memory"]
        self.assertEqual(memory[("session", True)], {"created": 1, "updated": 0, "deleted": 0})
        self.assertEqual(memory[("session", False)], {"created": 1, "updated": 0, "deleted": 0})  # o índice ficou de fora
        self.assertEqual(memory[("reviewer", False)]["created"], 1)
        later = self.days[("studio", "2026-10-29")]["memory"]
        self.assertEqual(later[("session", True)]["updated"], 1)
        self.assertEqual(later[("session", False)]["deleted"], 1)

    def test_live_memories_at_the_end_of_the_day_are_cumulative_by_events(self):
        self.assertEqual(self.days[("studio", "2026-10-28")]["live"], 3)  # a, b e c
        self.assertEqual(self.days[("studio", "2026-10-29")]["live"], 2)  # b saiu
        self.assertEqual(self.days[("tools-kit", "2026-10-29")]["live"], 1)

    def test_live_carries_over_a_day_without_memory_events(self):
        days = self.summarize.aggregate_by_workstream(ROWS + [turn("2026-10-30", "studio", 1.0)])
        self.assertEqual(days[("studio", "2026-10-30")]["live"], 2)

    def test_rounds_sum_and_percentages(self):
        rounds = self.days[("studio", "2026-10-28")]["rounds"]
        self.assertEqual(rounds, ROUNDS)
        self.assertEqual([self.summarize.pct(rounds[k], rounds["questions"]) for k in
                          ("recommended", "other_option", "free_text")], ["50%", "25%", "25%"])
        self.assertEqual(self.summarize.pct(0, 0), "")

    def test_command_line_prints_the_tables_and_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "measurements.jsonl"), "w", encoding="utf-8") as f:
                f.write("\n".join(json.dumps(r) for r in ROWS) + "\nnão é json\n")
            out = io.StringIO()
            with mock.patch.object(sys, "argv", ["summarize", "--dir", tmp, "--by-workstream"]), \
                    contextlib.redirect_stdout(out):
                self.assertEqual(self.summarize.main(), 0)
            text = out.getvalue()
            for expected in ("studio", "(sem workstream)", "2026-10-28", "collector", "feedback", "50%", "ilegível"):
                self.assertIn(expected, text)
            out = io.StringIO()
            with mock.patch.object(sys, "argv", ["summarize", "--dir", tmp, "--by-workstream", "--json"]), \
                    contextlib.redirect_stdout(out):
                self.summarize.main()
            data = json.loads(out.getvalue())
            self.assertIn(("studio", "2026-10-28"), {(d["workstream"], d["day"]) for d in data})

    def test_default_report_is_unchanged_by_the_new_fields(self):
        agg = self.summarize.aggregate(ROWS)
        self.assertEqual(sum(b["n"] for b in agg["turns"].values()), 4)


if __name__ == "__main__":
    unittest.main()
