#!/usr/bin/env python3
"""Trava de retomada de cache: barra o prompt que acorda uma sessão grande parada além do TTL do cache.

Ligado no UserPromptSubmit. Lê a última linha `event: turn` da sessão em .measurements/measurements.jsonl, gravada
pelo measure.py no Stop: se a sessão ficou parada mais que o TTL do cache e o contexto do último turno passa de
150 mil tokens, o próximo pedido regrava o contexto inteiro. A trava barra com a conta da regravação e a orientação de
abrir sessão nova; o mesmo prompt reenviado em até 2 min passa.

O TTL vem de CLAUDE_CODE_PROMPT_CACHE_TTL (`1h` ou `5m`); sem ela, da escrita de cache do último turno que escreveu:
`cache_write_1h` é 60 min, `cache_write_5m` é 5 min, e sem turno que tenha escrito, 5 min.

Nunca barra sem `session_id`, sem turno da sessão, sem `max_context`, em prompt de correio entre sessões nem em
qualquer exceção. O estado da passagem guarda o hash FNV-1a do prompt, nunca o texto, em .measurements/guard.json.
"""

import json
import os
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import measure  # noqa: E402 — PRICES, o log e a raiz do workspace brza vêm de lá, sem duplicar a tabela

THRESHOLD = 150_000
WINDOW_S = 120  # o reenvio do mesmo prompt dentro dela passa
STATE = os.path.join(measure.DIR, "guard.json")
LOCK = os.path.join(measure.DIR, "guard.lock")
MAILBOX = "<cross-session-message"


def fnv1a64(text):
    h = 0xcbf29ce484222325
    for byte in text.encode("utf-8"):
        h = ((h ^ byte) * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
    return f"{h:016x}"


def session_turns(session_id, block=1 << 16):
    """As linhas `turn` da sessão, da mais recente para a mais antiga, lendo o log de trás para frente: o log só cresce,
    e o último turno está quase sempre no fim."""
    try:
        f = open(measure.LOG, "rb")
    except OSError:
        return
    with f:
        f.seek(0, os.SEEK_END)
        pos, rest = f.tell(), b""
        while pos > 0:
            step = min(block, pos)
            pos -= step
            f.seek(pos)
            chunk = f.read(step) + rest
            lines = chunk.split(b"\n")
            rest = lines.pop(0)  # pode estar pela metade: junta com o bloco anterior
            for raw in reversed(lines):
                row = parse(raw, session_id)
                if row:
                    yield row
        row = parse(rest, session_id)
        if row:
            yield row


def parse(raw, session_id):
    if session_id.encode() not in raw or b'"turn"' not in raw:
        return None
    try:
        row = json.loads(raw)
    except ValueError:
        return None
    if row.get("event") != "turn" or row.get("session_id") != session_id:
        return None
    return row


def ttl_minutes(turns):
    """O TTL do cache em minutos, e o primeiro turno lido (o último da sessão), ou None sem turno."""
    env = (os.environ.get("CLAUDE_CODE_PROMPT_CACHE_TTL") or "").strip().lower()
    last, ttl = None, None
    if env in ("1h", "60m"):
        ttl = 60
    elif env == "5m":
        ttl = 5
    for row in turns:
        last = last or row
        if ttl:
            break
        tokens = row.get("tokens") or {}
        if tokens.get("cache_write_1h"):
            ttl = 60
        elif tokens.get("cache_write_5m"):
            ttl = 5
    return ttl or 5, last


class State(measure.State):
    """O estado da passagem, sob a mesma trava do measure.py, em arquivo próprio."""

    def __enter__(self):
        os.makedirs(measure.DIR, exist_ok=True)
        self.lock = open(LOCK, "w")
        if measure.fcntl:
            measure.fcntl.flock(self.lock, measure.fcntl.LOCK_EX)
        try:
            with open(STATE, encoding="utf-8") as f:
                self.data = json.load(f)
        except (OSError, ValueError):
            self.data = {}
        return self

    def save(self, now):
        self.data = {k: v for k, v in self.data.items() if v.get("at", 0) >= now - WINDOW_S}
        with open(STATE + ".tmp", "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=1)
        os.replace(STATE + ".tmp", STATE)


def rewrite_cost(model, context, ttl):
    """US$ de regravar o contexto inteiro na escrita de cache do TTL, pela tabela do measure.py, ou None."""
    price = measure.price_of(model)
    if not price:
        return None
    field = "cache_write_1h" if ttl == 60 else "cache_write_5m"
    return measure.request_cost(price, {"cache_write": context, field: context})


def number(n):
    return f"{n:,}".replace(",", ".")


def message(idle, ttl, context, model, cost):
    price = f", cerca de US$ {cost:.2f}".replace(".", ",") + f" no {model}" if cost is not None else ""
    return (f"Sessão parada há {idle} min, e o cache dura {ttl} min: o próximo pedido regrava o contexto de "
            f"{number(context)} tokens inteiro{price}.\n"
            "Para economizar, abra sessão nova — /exit e claude --name <nome> — e retome pelo Retomar do plano "
            "em plans/ ou pela issue em work/issues/.\nPara continuar aqui mesmo, reenvie o mesmo prompt em até 2 min.")


def pending(session_id, now):
    """O que a trava diria do próximo prompt da sessão: None quando ele passa; senão os minutos parada, o TTL, o
    contexto e o modelo do último turno. O `brza sessions send` pergunta por aqui antes de mandar."""
    ttl, last = ttl_minutes(session_turns(session_id))
    if not last or not last.get("max_context") or not last.get("timestamp"):
        return None
    idle = (now - datetime.fromisoformat(last["timestamp"]).timestamp()) / 60
    context = last["max_context"]
    if idle <= ttl or context < THRESHOLD:
        return None
    return {"idle_min": round(idle), "ttl_min": ttl, "context": context, "model": last.get("model")}


def hold(session_id, prompt, now):
    """Grava a passagem do prompt como se ele tivesse sido barrado agora: o mesmo prompt em até 2 min passa."""
    with State() as state:
        state.data[f"resume:{session_id}"] = {"hash": fnv1a64(prompt.strip()), "at": now}
        state.save(now)


def guard(p, clock=None):
    session_id = p.get("session_id")
    if not session_id:
        return None
    now = (clock or time.time)()
    found = pending(session_id, now)
    if not found:
        return None
    idle, ttl, context, model = found["idle_min"], found["ttl_min"], found["context"], found["model"]
    prompt = (p.get("prompt") or "").strip()
    row = {"event": "guard", "timestamp": measure.now(), "session_id": session_id,
           "bridge_session_id": measure.bridge_session(), "cwd": p.get("cwd"), "kind": "resume",
           "idle_min": idle, "ttl_min": ttl, "max_context": context}
    if prompt.startswith(MAILBOX):
        measure.write(dict(row, decision="skipped"))
        return None
    key, digest = f"resume:{session_id}", fnv1a64(prompt)
    with State() as state:
        held = state.data.get(key)
        if held and held.get("hash") == digest and now - held.get("at", 0) <= WINDOW_S:
            del state.data[key]
            state.save(now)
            measure.write(dict(row, decision="released"))
            return None
        state.data[key] = {"hash": digest, "at": now}
        state.save(now)
    cost = rewrite_cost(model, context, ttl)
    measure.write(dict(row, decision="blocked", estimated_cost_usd=round(cost, 2) if cost is not None else None))
    return {"decision": "block", "reason": message(idle, ttl, context, model, cost)}


def main():
    try:
        out = guard(json.load(sys.stdin))
        if out:
            print(json.dumps(out, ensure_ascii=False))
    except Exception as error:  # a trava nunca barra por falha própria
        try:
            measure.write({"event": "hook_error", "timestamp": measure.now(), "mode": "resume_guard",
                           "error": repr(error)})
        except Exception:
            pass
    sys.exit(0)


if __name__ == "__main__":
    main()
