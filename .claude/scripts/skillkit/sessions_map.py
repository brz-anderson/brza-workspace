"""O mapa de sessões do `brza sessions` v2 (`.sessions/sessions.jsonl`), lido em UM lugar.

Quem abre, espera ou mede sessão usa `fold_map`: a identidade (Dispatch, Run, remetente, coordenação, id do provedor)
vem só daqui ou de uma sobrescrita explícita; nenhum script procura transcript por texto, prompt ou nome. O
`dispatch_of`, que lê o manifesto de reunião, fica na `meeting-runner`.

Formato (linhas JSON, uma por evento, gravadas pelo v2):
    open     {at, name, chat, dispatch, run, sender, coordinator, agent, model, effort, operation, round_id,
              claude_session, provider_session, checkout, title}
    session  {at, name, chat, provider_session[, claude_session]}      # o id do provedor depois do `--wait`
    send     {at, name, chat, operation, round_id, receipt{status, ...}}
    turn     {at, name, chat, operation, outcome, latency_s, latency_source, ended_at}
    close    {at, name, chat}                                         # só quando o worker foi liberado
Linha v1 (`open` sem `chat`, com `dispatch_id`) só vale como Dispatch legado quando o nome não tem linha v2.
"""
import json
import os
from datetime import datetime

from .paths import common_root  # noqa: F401  (reexportado: é daqui que os scripts o importam)


def map_file(root, sessions=None):
    """`--sessions` ou `<raiz comum do git>/.sessions/sessions.jsonl`."""
    return sessions or os.path.join(common_root(root), ".sessions", "sessions.jsonl")


def read_rows(path):
    rows = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if isinstance(row, dict):
                    rows.append(row)
    except OSError:
        pass
    return rows


def epoch(value):
    """Segundos desde a época de um ISO 8601 (ou número em s/ms); None se não houver."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value / 1000 if value > 100000000000 else float(value)
    if not value or not isinstance(value, str):
        return None
    try:
        d = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return (d if d.tzinfo else d.astimezone()).timestamp()


OPEN_FIELDS = ("dispatch", "run", "sender", "coordinator", "agent", "model", "effort", "claude_session",
               "provider_session", "chat", "checkout", "title")


def _novo(row):
    e = {"name": row.get("name"), "opened": row.get("at"), "closed": False, "closed_at": None, "legacy": False,
         "last_send": None, "last_turn": None}
    e.update({k: row.get(k) for k in OPEN_FIELDS})
    return e


def fold_map(rows):
    """{nome: entrada}: dobra as linhas do mapa por NOME.

    `open` (com `chat`) inicia/substitui a entrada; `session` atualiza `claude_session`/`provider_session` do mesmo
    chat (sem `chat` na linha, vale para o nome); `send` guarda `last_send`, `turn` guarda `last_turn`; `close` marca
    `closed` sem apagar os ids (a medição precisa deles depois do auto-release). O `open` também é o `last_send` da
    rodada 1 (`origem: "open"`), como no v2. Linha v1 entra como `dispatch` legado só quando o nome não tem linha v2."""
    entradas, legado = {}, {}
    for row in rows:
        nome, ev = row.get("name"), row.get("event")
        if not nome or not ev:
            continue
        if ev == "open":
            if not row.get("chat"):
                if row.get("dispatch_id"):
                    legado[nome] = row
                continue
            e = entradas[nome] = _novo(row)
            if row.get("operation") or row.get("round_id"):
                e["last_send"] = {"operation": row.get("operation"), "round_id": row.get("round_id") or row.get("operation"),
                                  "at": row.get("at"), "status": None, "origem": "open"}
            continue
        e = entradas.get(nome)
        if ev == "session":
            if e is None:  # `session` sem `open` antes: o id vale para o nome
                e = entradas[nome] = _novo(row)
                e["opened"] = None
            elif row.get("chat") and e.get("chat") and row["chat"] != e["chat"]:
                continue
            if row.get("provider_session"):
                e["provider_session"] = row["provider_session"]
            if row.get("claude_session"):
                e["claude_session"] = row["claude_session"]
            continue
        if e is None or (row.get("chat") and e.get("chat") and row["chat"] != e["chat"]):
            continue
        if ev == "send":
            rc = row.get("receipt") or {}
            e["last_send"] = {"operation": row.get("operation"), "round_id": row.get("round_id") or row.get("operation"),
                              "at": row.get("at"), "status": rc.get("status"), "origem": "send"}
        elif ev == "turn":
            e["last_turn"] = {k: row.get(k) for k in ("operation", "outcome", "latency_s", "latency_source", "ended_at", "at")}
        elif ev == "close":
            e["closed"], e["closed_at"] = True, row.get("at")
        elif ev == "model":
            for k in ("model", "effort"):
                if k in row:
                    e[k] = row[k]
    for nome, row in legado.items():
        if nome not in entradas:
            e = _novo(row)
            e.update(dispatch=row.get("dispatch_id"), legacy=True, model=row.get("model"), effort=row.get("effort"))
            entradas[nome] = e
    return entradas


def load_map(root, sessions=None):
    return fold_map(read_rows(map_file(root, sessions)))
