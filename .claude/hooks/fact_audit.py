#!/usr/bin/env python3
"""Hook da auditoria dos fatos do desenho (PLN-005): grava no log do `measure.py` a confiança que o `designer` e o
`collector` marcaram em cada fato.

Um modo por entrada de hook, no primeiro argumento:

- `stop` (SubagentStop, o mesmo payload do `measure.py subagent`): lê o trecho novo do transcript do subagente e tira as
  marcas `[F3 · lido · 90]` — tipo `F` (fato) ou `C` (custo), número, a evidência (`rodado`, `lido`, `doc`, `inferido`)
  e a confiança de 0 a 100 — da devolução (`source: reply`: o `input.message` do `SubagentHandback`, ou, sem ele, a
  última mensagem de texto do assistente) e do `content` de cada `Write`
  do trecho (`source`: o caminho gravado). Grava um evento `fact` por marca nova e um `fact_capture` por trecho, com o
  total, as marcas malformadas e `unmarked` quando a devolução veio sem nenhuma.

Só mede: nunca bloqueia, e toda exceção vira `hook_error` com saída 0. Sai sem gravar com `BRZA_FACT_AUDIT` no
ambiente — a sessão `claude -p` da própria auditoria — ou com `agent_type` fora de `designer` e `collector`. O estado
(onde parou a leitura de cada transcript e os ids já vistos) fica em .measurements/fact-audit-state.json, sob a trava do
`measure.py`, de onde vêm o `agent_transcript`, o `read_from`, o `write`, o `now` e o `workstream_of`.
"""

import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load_measure():
    spec = importlib.util.spec_from_file_location("measure", os.path.join(HERE, "measure.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


measure = load_measure()

AUDITED = ("designer", "collector")
MARK = re.compile(r"\[([FC])(\d+) · (rodado|lido|doc|inferido) · (\d{1,3})\]")
MARK_START = re.compile(r"\[[FC]\d")  # todo `[F3` ou `[C2` é tentativa de marca: a que MARK não casa é malformada
TEXT_LIMIT = 300
STATE_FILE = "fact-audit-state.json"


def agent_type_of(p, path):
    """O tipo do subagente pelo payload, ou pelo `agentType` do .meta.json ao lado do transcript."""
    if p.get("agent_type"):
        return p["agent_type"]
    try:
        with open(path.replace(".jsonl", ".meta.json"), encoding="utf-8") as f:
            return json.load(f).get("agentType")
    except (OSError, ValueError):
        return None


def blocks_of(line):
    """Os blocos de conteúdo de uma linha de assistente do transcript, ou []."""
    try:
        entry = json.loads(line)
    except ValueError:
        return []
    message = entry.get("message") if isinstance(entry, dict) else None
    if not isinstance(message, dict) or (entry.get("type") or message.get("role")) != "assistant":
        return []
    content = message.get("content")
    return [b for b in content if isinstance(b, dict)] if isinstance(content, list) else []


def sources_of(lines):
    """O texto a ler no trecho, na ordem: o `content` de cada `Write`, e a devolução, como `reply`: o `input.message` do
    último `tool_use` `SubagentHandback` — é assim que o subagente devolve —, ou, sem ele, a última mensagem do
    assistente que tenha bloco `text`. Devolve [(source, texto)]."""
    writes, reply, handback = [], None, None
    for line in lines:
        blocks = blocks_of(line)
        for b in blocks:
            if b.get("type") == "tool_use" and b.get("name") == "Write":
                tool = b.get("input") or {}
                if isinstance(tool.get("content"), str):
                    writes.append((tool.get("file_path"), tool["content"]))
            elif b.get("type") == "tool_use" and b.get("name") == "SubagentHandback":
                message = (b.get("input") or {}).get("message")
                if isinstance(message, str):
                    handback = message
        texts = [b["text"] for b in blocks if b.get("type") == "text" and isinstance(b.get("text"), str)]
        if texts:
            reply = "\n".join(texts)
    reply = handback if handback is not None else reply
    return writes + ([("reply", reply)] if reply is not None else [])


def line_of(text, pos):
    start = text.rfind("\n", 0, pos) + 1
    end = text.find("\n", pos)
    return text[start:end if end >= 0 else len(text)].strip()[:TEXT_LIMIT]


def marks_of(sources):
    """(marcas, malformadas): as marcas válidas na ordem das fontes, com a primeira ocorrência de cada id, e a contagem
    das ocorrências malformadas. Cada marca é (id, kind, confidence, texto, source); `found` conta as válidas antes de
    tirar as repetidas."""
    marks, ids, malformed, found = [], set(), 0, 0
    for source, text in sources:
        for start in MARK_START.finditer(text):
            m = MARK.match(text, start.start())
            if not m or int(m.group(4)) > 100:
                malformed += 1
                continue
            found += 1
            fact_id = m.group(1) + m.group(2)
            if fact_id not in ids:
                ids.add(fact_id)
                marks.append((fact_id, m.group(3), int(m.group(4)), line_of(text, m.start()), source))
    return marks, malformed, found


def stop(p):
    if os.environ.get("BRZA_FACT_AUDIT"):
        return
    path = measure.agent_transcript(p)
    if not path or not os.path.exists(path):
        return
    agent_type = agent_type_of(p, path)
    if agent_type not in AUDITED:
        return
    with measure.State(os.path.join(measure.DIR, STATE_FILE)) as state:
        entry = state.data.get(path) or {}
        offset, seen = entry.get("offset", 0), set(entry.get("seen", []))
        lines, end = measure.read_from(path, offset)
        if not lines:
            return  # trecho vazio: nada novo, e a leitura não avança
        marks, malformed, found = marks_of(sources_of(lines))
        marks = [m for m in marks if m[0] not in seen]  # o id já visto num trecho anterior não se grava de novo
        base = {"timestamp": measure.now(), "session_id": p.get("session_id"), "agent_id": p.get("agent_id"),
                "agent_type": agent_type, "workstream": measure.workstream_of(p.get("cwd"))}
        for fact_id, kind, confidence, text, source in marks:
            measure.write({"event": "fact", **base, "fact_id": fact_id, "kind": kind, "confidence": confidence,
                           "text": text, "source": source})
        capture = {"event": "fact_capture", **base, "facts": len(marks), "malformed": malformed,
                   "segment": "resume" if offset else "first"}
        if not found:
            capture["unmarked"] = True
        measure.write(capture)
        state.data[path] = {"offset": end, "seen": sorted(seen | {m[0] for m in marks})}
        state.save()


MODES = {"stop": stop}


def main():
    mode = (sys.argv[1:] or [None])[0]
    try:
        MODES[mode](json.load(sys.stdin))
    except Exception as error:  # o hook mede; nunca derruba a chamada medida
        try:
            measure.write({"event": "hook_error", "timestamp": measure.now(), "mode": f"fact_audit:{mode}",
                           "error": repr(error)})
        except Exception:
            pass
    sys.exit(0)


if __name__ == "__main__":
    main()
