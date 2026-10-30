"""Testes do resume_guard.py: a trava de retomada de cache.

Tudo roda num diretório temporário pelo MEASURE_DIR, com o log de medição escrito pelo teste e o relógio por parâmetro.

    python3 -m unittest discover -s .claude/hooks/tests
"""

import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
NOW = datetime.fromisoformat("2026-10-23T15:00:00+00:00")


def load_guard(directory):
    os.environ["MEASURE_DIR"] = directory
    hooks = os.path.dirname(HERE)
    for name in ("measure", "resume_guard"):  # o measure.py é lido de novo para pegar o MEASURE_DIR do teste
        spec = importlib.util.spec_from_file_location(name, os.path.join(hooks, f"{name}.py"))
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def turn(minutes_ago, context=200_000, session="s1", model="claude-opus-5-5", write_5m=1000, write_1h=0, **extra):
    stamp = (NOW - timedelta(minutes=minutes_ago)).astimezone().isoformat(timespec="seconds")
    return dict({"event": "turn", "timestamp": stamp, "session_id": session, "model": model, "max_context": context,
                 "tokens": {"cache_write_5m": write_5m, "cache_write_1h": write_1h}}, **extra)


class GuardTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.guard = load_guard(self.tmp.name)
        self.env = mock.patch.dict(os.environ)
        self.env.start()
        os.environ.pop("CLAUDE_CODE_PROMPT_CACHE_TTL", None)

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()
        os.environ.pop("MEASURE_DIR", None)
        sys.modules.pop("measure", None)
        sys.modules.pop("resume_guard", None)

    def log(self, *rows):
        for row in rows:
            self.guard.measure.write(row)

    def logged(self, event="guard"):
        with open(self.guard.measure.LOG, encoding="utf-8") as f:
            return [r for r in map(json.loads, f) if r["event"] == event]

    def ask(self, prompt="segue", session="s1", at=NOW):
        return self.guard.guard({"session_id": session, "prompt": prompt, "cwd": "/w"}, clock=lambda: at.timestamp())

    def test_idle_large_session_is_blocked_with_the_rewrite_cost(self):
        self.log(turn(30))
        out = self.ask()
        self.assertEqual(out["decision"], "block")
        self.assertIn("parada há 30 min, e o cache dura 5 min", out["reason"])
        self.assertIn("200.000 tokens", out["reason"])
        self.assertIn("US$ 1,00 no claude-opus-5-5", out["reason"])  # 200 mil × US$ 5 por milhão
        self.assertIn("claude --name <nome>", out["reason"])
        (row,) = self.logged()
        self.assertEqual((row["kind"], row["decision"], row["idle_min"], row["ttl_min"], row["max_context"]),
                         ("resume", "blocked", 30, 5, 200_000))

    def test_same_prompt_within_two_minutes_is_released_once(self):
        self.log(turn(30))
        self.assertIsNotNone(self.ask("  segue  "))
        self.assertIsNone(self.ask("segue", at=NOW + timedelta(seconds=90)))
        self.assertEqual([r["decision"] for r in self.logged()], ["blocked", "released"])
        with open(self.guard.STATE, encoding="utf-8") as f:
            self.assertEqual(json.load(f), {})

    def test_pending_tells_what_the_next_prompt_would_meet_without_writing(self):
        self.log(turn(30), turn(30, context=1000, session="s2"))
        self.assertEqual(self.guard.pending("s1", NOW.timestamp()),
                         {"idle_min": 30, "ttl_min": 5, "context": 200_000, "model": "claude-opus-5-5"})
        self.assertIsNone(self.guard.pending("s2", NOW.timestamp()))
        self.assertIsNone(self.guard.pending("s3", NOW.timestamp()))
        self.assertEqual(self.logged(), [])

    def test_a_held_prompt_passes_at_the_first_try(self):
        self.log(turn(30))
        self.guard.hold("s1", " segue ", NOW.timestamp())
        self.assertIsNone(self.ask("segue", at=NOW + timedelta(seconds=5)))
        self.assertIsNotNone(self.ask("outro", at=NOW + timedelta(seconds=10)))
        self.assertEqual([r["decision"] for r in self.logged()], ["released", "blocked"])

    def test_state_keeps_the_hash_and_never_the_prompt(self):
        self.log(turn(30))
        self.ask("texto secreto")
        with open(self.guard.STATE, encoding="utf-8") as f:
            raw = f.read()
        self.assertNotIn("secreto", raw)
        self.assertEqual(json.loads(raw)["resume:s1"]["hash"], self.guard.fnv1a64("texto secreto"))

    def test_fnv1a_64_matches_the_reference_vectors(self):
        self.assertEqual(self.guard.fnv1a64(""), "cbf29ce484222325")
        self.assertEqual(self.guard.fnv1a64("a"), "af63dc4c8601ec8c")

    def test_resend_after_the_window_or_another_prompt_is_blocked_again(self):
        self.log(turn(30))
        self.ask("segue")
        self.assertIsNotNone(self.ask("segue", at=NOW + timedelta(seconds=150)))
        self.assertIsNotNone(self.ask("outro", at=NOW + timedelta(seconds=160)))

    def test_each_save_drops_the_entries_past_the_window(self):
        self.log(turn(30, session="old"), turn(30, session="s1"))
        self.ask(session="old")
        self.ask(session="s1", at=NOW + timedelta(seconds=200))
        with open(self.guard.STATE, encoding="utf-8") as f:
            self.assertEqual(list(json.load(f)), ["resume:s1"])

    def test_small_context_or_short_idle_passes_without_a_line(self):
        self.log(turn(30, context=149_999, session="small"), turn(4, session="recent"))
        self.assertIsNone(self.ask(session="small"))
        self.assertIsNone(self.ask(session="recent"))
        self.assertEqual(self.logged(), [])

    def test_mailbox_prompt_passes_and_is_logged_as_skipped(self):
        self.log(turn(30))
        self.assertIsNone(self.ask('<cross-session-message from="x">oi</cross-session-message>'))
        (row,) = self.logged()
        self.assertEqual(row["decision"], "skipped")

    def test_never_blocks_without_session_turn_or_context(self):
        self.log(turn(30, session="other"), turn(30, session="nocontext", context=0))
        self.assertIsNone(self.guard.guard({"prompt": "x"}))
        self.assertIsNone(self.ask(session="unknown"))
        self.assertIsNone(self.ask(session="nocontext"))

    def test_uses_the_last_turn_of_the_session(self):
        self.log(turn(30), turn(30, session="s2"))
        self.assertIsNotNone(self.ask())
        self.log(turn(1))
        self.assertIsNone(self.ask("outro"))

    def test_ttl_comes_from_the_one_hour_cache_write(self):
        self.log(turn(30, write_5m=0, write_1h=500))
        self.assertIsNone(self.ask())
        self.log(turn(61, write_5m=0, write_1h=500, session="s2"))
        out = self.ask(session="s2")
        self.assertIn("o cache dura 60 min", out["reason"])
        self.assertIn("US$ 1,60", out["reason"])  # 200 mil × US$ 8 por milhão

    def test_turn_without_writes_falls_back_to_the_previous_turn(self):
        self.log(turn(50, write_5m=0, write_1h=500), turn(30, write_5m=0, write_1h=0))
        self.assertIsNone(self.ask())  # 30 min parada, TTL de 60 do turno anterior

    def test_no_turn_with_writes_means_five_minutes(self):
        self.log(turn(30, write_5m=0, write_1h=0))
        self.assertIsNotNone(self.ask())

    def test_environment_ttl_wins_over_the_turn(self):
        self.log(turn(30, write_5m=1000, write_1h=0))
        os.environ["CLAUDE_CODE_PROMPT_CACHE_TTL"] = "1h"
        self.assertIsNone(self.ask())
        os.environ["CLAUDE_CODE_PROMPT_CACHE_TTL"] = "5m"
        self.log(turn(30, write_5m=0, write_1h=500, session="s2"))
        self.assertIsNotNone(self.ask(session="s2"))

    def test_unpriced_model_blocks_without_the_cost(self):
        self.log(turn(30, model="claude-x-9"))
        out = self.ask()
        self.assertNotIn("US$", out["reason"])
        self.assertIsNone(self.logged()[0]["estimated_cost_usd"])

    def test_reads_the_log_backwards_across_blocks(self):
        self.log(turn(30), *[turn(1, session=f"x{i}") for i in range(200)])
        rows = list(self.guard.session_turns("s1", block=64))
        self.assertEqual(len(rows), 1)

    def test_main_prints_the_block_and_exits_zero_and_survives_errors(self):
        self.log(turn(30))
        clock = mock.patch.object(self.guard.time, "time", return_value=NOW.timestamp())
        out = io.StringIO()
        with clock, mock.patch.object(sys, "stdin", io.StringIO(json.dumps({"session_id": "s1", "prompt": "x"}))), \
                mock.patch.object(sys, "stdout", out), self.assertRaises(SystemExit) as code:
            self.guard.main()
        self.assertEqual(code.exception.code, 0)
        self.assertEqual(json.loads(out.getvalue())["decision"], "block")
        out = io.StringIO()
        with mock.patch.object(sys, "stdin", io.StringIO("não é json")), mock.patch.object(sys, "stdout", out), \
                self.assertRaises(SystemExit) as code:
            self.guard.main()
        self.assertEqual((code.exception.code, out.getvalue()), (0, ""))
        self.assertEqual(self.logged("hook_error")[0]["mode"], "resume_guard")


if __name__ == "__main__":
    unittest.main()
