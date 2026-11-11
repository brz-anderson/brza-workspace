"""A medição de uma sessão: o custo e a duração do Claude pelo `.measurements/measurements.jsonl`, o turno do Codex pelo
rollout em disco. Só biblioteca padrão. Extraído de `tally.py` da `meeting-runner` (PLN-021/D1).

`session_ids` só lê o mapa do `brza sessions` v2 (`sessions_map.fold_map`) e a sobrescrita explícita; nada aqui procura
transcript por texto, prompt ou nome.
"""
import glob
import json
import os
from datetime import datetime, timedelta

from . import sessions_map


def load_jsonl(path):
    rows = []
    if not path or not os.path.isfile(path):
        return rows
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if isinstance(d, dict):
                rows.append(d)
    return rows


def parse_ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def session_ids(sessions_rows, session, persona=None):
    """Os ids do mapa do `brza sessions` v2 para a `session` (`sessions_map.fold_map`: o `open` e o `session` do mesmo
    nome, também depois do `close`); `claude_session`/`provider_session` da persona no manifesto SOBRESCREVEM o mapa.
    Nada aqui procura transcript: o id vem do mapa ou da sobrescrita explícita."""
    e = sessions_map.fold_map(sessions_rows).get(session) or {}
    claude, provider = set(), set()
    if e.get("claude_session"):
        claude.add(e["claude_session"])
    if e.get("provider_session"):
        provider.add(e["provider_session"])
        if (e.get("agent") or "claude") == "claude" and not claude:
            claude.add(e["provider_session"])  # no Claude o id do provedor é a sessão do transcript
    persona = persona or {}
    if persona.get("claude_session"):
        claude = {persona["claude_session"]}
    if persona.get("provider_session"):
        provider = {persona["provider_session"]}
    return claude, provider


def win_bounds(opened, closed):
    return (opened, closed + timedelta(seconds=60)) if opened and closed else None


def measure_claude(rows, ids, win):
    """Soma custo e duração dos eventos turn/subagent das sessões `ids` na janela `win` (ou no total, sem janela)."""
    sel = []
    for r in rows:
        if r.get("event") not in ("turn", "subagent") or r.get("session_id") not in ids:
            continue
        try:
            ts = parse_ts(r["timestamp"])
        except (KeyError, ValueError):
            continue
        if win and not (win[0] <= ts <= win[1]):
            continue
        sel.append((ts, r))
    if not sel:
        return None
    return {"cost_usd": round(sum(r.get("estimated_cost_usd") or 0 for _, r in sel), 2),
            "latency_s": int(round(sum(r.get("duration_s") or 0 for _, r in sel))),
            "end": max(ts for ts, _ in sel) if win else None, "events": len(sel)}


def find_rollout(codex_dir, provider_ids):
    for pid in provider_ids:
        matches = glob.glob(os.path.join(codex_dir, "**", f"*-{pid}.jsonl"), recursive=True)
        if matches:
            return sorted(matches)[0]
    return None


def codex_turns(path):
    """Turnos do rollout: [{start, end, failed, snap}], `snap` = o total_token_usage ao fim do turno (info null ignorado)."""
    turns, open_states, cum = [], {}, None
    for d in load_jsonl(path):
        p = d.get("payload") or {}
        if d.get("type") != "event_msg" or "timestamp" not in d:
            continue
        t = p.get("type")
        if t == "task_started":
            open_states[p.get("turn_id")] = parse_ts(d["timestamp"])
        elif t == "token_count":
            info = p.get("info")
            if isinstance(info, dict) and isinstance(info.get("total_token_usage"), dict):
                cum = info["total_token_usage"]
        elif t == "task_complete" and p.get("turn_id") in open_states:
            turns.append({"start": open_states.pop(p["turn_id"]), "end": parse_ts(d["timestamp"]),
                          "failed": bool(p.get("error")), "snap": cum})
    return turns


def measure_codex(codex_dir, provider_ids, n, win):
    path = find_rollout(codex_dir, provider_ids) if codex_dir and os.path.isdir(codex_dir) else None
    if not path:
        return None
    turns = codex_turns(path)
    if win:
        idx = [i for i, t in enumerate(turns) if win[0] <= t["end"] <= win[1]]
        k = idx[-1] if idx else None
    else:
        k = None  # sem janela não há como saber quais turnos são da reunião: N-1 por posição erra com um turno a mais
    if k is None:
        return None
    t, prior_snap = turns[k], (turns[k - 1]["snap"] if k > 0 else {})
    tokens = None
    if t["snap"]:
        def delta(key):
            return int((t["snap"].get(key) or 0) - ((prior_snap or {}).get(key) or 0))
        tokens = {"input_tokens": delta("input_tokens"), "cache": delta("cached_input_tokens"), "output_tokens": delta("output_tokens")}
    return {"latency_s": int(round((t["end"] - t["start"]).total_seconds())), "tokens": tokens,
            "failed": t["failed"], "end": t["end"]}
