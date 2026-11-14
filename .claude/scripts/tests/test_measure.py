"""Testes do skillkit.measure: o custo do Claude pelas medições e o turno do Codex pelo rollout."""
import json
import os
import tempfile
import unittest
from datetime import timedelta

import _paths  # noqa: F401
from skillkit import measure

T0 = "2026-11-09T10:00:00-03:00"


def turn(sid, ts, cost_text, dur, ev="turn"):
    return {"event": ev, "session_id": sid, "timestamp": ts, "estimated_cost_usd": cost_text, "duration_s": dur}


class BasicCase(unittest.TestCase):
    def test_load_jsonl_ignores_line_bad_and_file_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "m.jsonl")
            with open(p, "w", encoding="utf-8") as f:
                f.write('{"a": 1}\n\nlixo\n[2]\n{"b": 2}\n')
            self.assertEqual(measure.load_jsonl(p), [{"a": 1}, {"b": 2}])
            self.assertEqual(measure.load_jsonl(os.path.join(tmp, "nada")), [])
            self.assertEqual(measure.load_jsonl(None), [])

    def test_parse_ts_accepts_z(self):
        self.assertEqual(measure.parse_ts("2026-11-09T13:00:00Z"), measure.parse_ts("2026-11-09T10:00:00-03:00"))

    def test_win_bounds_sum_60_s_at_the_end(self):
        a, b = measure.parse_ts(T0), measure.parse_ts("2026-11-09T10:05:00-03:00")
        self.assertEqual(measure.win_bounds(a, b), (a, b + timedelta(seconds=60)))
        self.assertIsNone(measure.win_bounds(None, b))
        self.assertIsNone(measure.win_bounds(a, None))


class SessionIds(unittest.TestCase):
    ROWS = [{"event": "open", "name": "a", "chat": "c", "agent": "claude"},
            {"event": "session", "name": "a", "chat": "c", "provider_session": "UUID"}]

    def test_claude_uses_the_id_of_provider(self):
        self.assertEqual(measure.session_ids(self.ROWS, "a"), ({"UUID"}, {"UUID"}))

    def test_codex_not_becomes_claude(self):
        rows = [dict(self.ROWS[0], agent="codex"), self.ROWS[1]]
        self.assertEqual(measure.session_ids(rows, "a"), (set(), {"UUID"}))

    def test_manifest_overwrites_and_missing_name_is_empty(self):
        self.assertEqual(measure.session_ids(self.ROWS, "a", {"claude_session": "F"}), ({"F"}, {"UUID"}))
        self.assertEqual(measure.session_ids(self.ROWS, "nada"), (set(), set()))


class Claude(unittest.TestCase):
    ROWS = [turn("S", "2026-11-09T10:01:00-03:00", 0.5, 30), turn("S", "2026-11-09T10:02:00-03:00", 0.25, 12.4, "subagent"),
            turn("S", "2026-11-09T11:00:00-03:00", 9, 99), turn("OUTRA", "2026-11-09T10:01:30-03:00", 7, 7),
            {"event": "skill", "session_id": "S", "timestamp": T0}]

    def test_sum_in_window(self):
        win = (measure.parse_ts(T0), measure.parse_ts("2026-11-09T10:30:00-03:00"))
        m = measure.measure_claude(self.ROWS, {"S"}, win)
        self.assertEqual((m["cost_usd"], m["latency_s"], m["events"]), (0.75, 42, 2))
        self.assertEqual(m["end"], measure.parse_ts("2026-11-09T10:02:00-03:00"))

    def test_without_window_sum_everything_and_without_end(self):
        m = measure.measure_claude(self.ROWS, {"S"}, None)
        self.assertEqual((m["events"], m["end"]), (3, None))

    def test_without_event_is_none(self):
        self.assertIsNone(measure.measure_claude(self.ROWS, {"X"}, None))
        self.assertIsNone(measure.measure_claude([{"event": "turn", "session_id": "S", "timestamp": "lixo"}], {"S"}, None))


class Codex(unittest.TestCase):
    def rollout(self, tmp, pid="PID"):
        d = os.path.join(tmp, "2026", "11", "09")
        os.makedirs(d)
        p = os.path.join(d, f"rollout-x-{pid}.jsonl")

        def ev(ts, kind, **kw):
            return {"type": "event_msg", "timestamp": ts, "payload": dict({"type": kind}, **kw)}

        def tok(i, c, o):
            return {"total_token_usage": {"input_tokens": i, "cached_input_tokens": c, "output_tokens": o}}
        rows = [ev("2026-11-09T10:00:00-03:00", "task_started", turn_id="t1"),
                ev("2026-11-09T10:00:10-03:00", "token_count", info=tok(100, 40, 10)),
                ev("2026-11-09T10:00:20-03:00", "task_complete", turn_id="t1"),
                ev("2026-11-09T10:10:00-03:00", "task_started", turn_id="t2"),
                ev("2026-11-09T10:10:30-03:00", "token_count", info=tok(250, 100, 30)),
                ev("2026-11-09T10:10:40-03:00", "token_count", info=None),
                ev("2026-11-09T10:10:50-03:00", "task_complete", turn_id="t2", error=None)]
        with open(p, "w", encoding="utf-8") as f:
            f.write("\n".join(json.dumps(r) for r in rows) + "\n")
        return p

    def test_turns_and_difference_of_tokens_of_last_turn_in_window(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self.rollout(tmp)
            self.assertEqual(len(measure.codex_turns(p)), 2)
            self.assertEqual(measure.find_rollout(tmp, ["PID"]), p)
            win = (measure.parse_ts("2026-11-09T10:09:00-03:00"), measure.parse_ts("2026-11-09T10:12:00-03:00"))
            m = measure.measure_codex(tmp, ["PID"], 2, win)
            self.assertEqual(m["latency_s"], 50)
            self.assertEqual(m["tokens"], {"input_tokens": 150, "cache": 60, "output_tokens": 20})
            self.assertFalse(m["failed"])

    def test_without_window_or_without_rollout_is_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.rollout(tmp)
            self.assertIsNone(measure.measure_codex(tmp, ["PID"], 2, None))
            self.assertIsNone(measure.measure_codex(tmp, ["OUTRO"], 2, (measure.parse_ts(T0), measure.parse_ts(T0))))
            self.assertIsNone(measure.measure_codex(os.path.join(tmp, "nada"), ["PID"], 2, None))
            self.assertIsNone(measure.measure_codex(None, ["PID"], 2, None))


if __name__ == "__main__":
    unittest.main()
