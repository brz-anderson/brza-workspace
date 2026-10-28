#!/usr/bin/env python3
"""Resume o log de medição do workspace brza, `.measurements/measurements.jsonl`, escrito pelo hook `measure.py` (um
evento por linha) e pela trava `resume_guard.py` (a linha `guard`).

Agrega o subagente por agente, modelo e esforço, e por versão do plugin; o turno da sessão principal por modelo e
esforço, e pelas skills que entraram nele; os comandos digitados; as falhas por tipo de erro; o MCP por servidor; e as
decisões da trava de retomada. As negações de hook saem com o motivo.

  python3 scripts/summarize_measurements.py                      lê o .measurements/ da $BRZA_WORKSPACE, ou de ..
  python3 scripts/summarize_measurements.py --dir <diretório>    outro diretório com o log
  python3 scripts/summarize_measurements.py --since 2026-10-10   só os eventos a partir da data (AAAA-MM-DD)
  python3 scripts/summarize_measurements.py --denials            lista cada negação, com o agente, a data e o motivo
  python3 scripts/summarize_measurements.py --json               a mesma agregação em JSON

Log que não existe é pulado; linha que não é JSON é contada e ignorada. Só biblioteca padrão, Python 3.9.
"""

import argparse
import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# A raiz vem da BRZA_WORKSPACE, que a função do shell passa: rodado de um worktree, o `..` cairia em `.worktrees/`.
# Sem a variável, vale o diretório acima de scripts/.
WORKSPACE = os.environ.get("BRZA_WORKSPACE") or os.path.join(HERE, "..")
DEFAULT_DIR = os.path.normpath(os.path.join(WORKSPACE, ".measurements"))
LOG = "measurements.jsonl"
UNKNOWN = "—"


def read_log(path, since):
    """As linhas do log a partir da data, e quantas não eram JSON. Log ausente devolve nada, sem erro."""
    rows, bad = [], 0
    if not os.path.isfile(path):
        return rows, bad, False
    with open(path, encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except ValueError:
                bad += 1
                continue
            if since and str(row.get("timestamp", ""))[:10] < since:
                continue
            rows.append(row)
    return rows, bad, True


def short_name(value):
    return str(value or "?").rpartition(":")[2]


def label(value):
    return UNKNOWN if value in (None, "") else str(value)


def reason_key(reason):
    """A parte do motivo que identifica a regra, sem o alvo: tira o prefixo do hook e o que vem entre crases."""
    text = re.sub(r"^PreToolUse:\w+ hook error:\s*", "", str(reason))
    text = re.sub(r"`[^`]*`", "`…`", text)
    return " ".join(text.split())[:110]


def new_cost_bucket():
    return {"n": 0, "cost": 0.0, "no_cost": 0, "duration_s": 0.0, "api_calls": 0, "denials": 0, "resumes": 0}


def add_cost(bucket, row):
    bucket["n"] += 1
    cost = row.get("estimated_cost_usd")
    if cost is None:
        bucket["no_cost"] += 1
    else:
        bucket["cost"] += float(cost)
    bucket["duration_s"] += float(row.get("duration_s") or 0)
    bucket["api_calls"] += int(row.get("api_calls") or 0)
    bucket["denials"] += int(row.get("denials") or 0)
    if row.get("segment") == "resume":
        bucket["resumes"] += 1


def aggregate(measurements):
    agents = collections.defaultdict(new_cost_bucket)  # (agente, modelo, esforço)
    models = collections.defaultdict(new_cost_bucket)
    versions = collections.defaultdict(lambda: {"subagents": 0, "cost": 0.0, "skills": 0, "commands": 0})
    turns = collections.defaultdict(new_cost_bucket)  # (modelo, esforço)
    turns_by_skill = collections.defaultdict(new_cost_bucket)
    skills = collections.Counter()
    commands = collections.Counter()  # (comando, origem)
    failures = collections.Counter()
    mcp = collections.defaultdict(lambda: {"n": 0, "failed": 0, "duration_ms": 0})
    guard = collections.defaultdict(lambda: {"n": 0, "cost": 0.0, "no_cost": 0, "context": 0, "idle_min": 0})
    reasons = collections.Counter()
    denials = []
    hook_errors = 0

    for row in measurements:
        event = row.get("event")
        if event == "subagent":
            agent = short_name(row.get("agent_type"))
            add_cost(agents[(agent, label(row.get("model")), label(row.get("effort")))], row)
            add_cost(models[label(row.get("model"))], row)
            if row.get("plugin_version") and row.get("agent_type"):
                version = versions[f"{row['agent_type'].partition(':')[0]} {row['plugin_version']}"]
                version["subagents"] += 1
                version["cost"] += float(row.get("estimated_cost_usd") or 0)
            for reason in row.get("denial_reasons") or []:
                reasons[reason_key(reason)] += 1
                denials.append((str(row.get("timestamp", ""))[:16], agent, str(reason)))
        elif event == "turn":
            add_cost(turns[(label(row.get("model")), label(row.get("effort")))], row)
            for name in sorted(set(row.get("skills") or [])):
                add_cost(turns_by_skill[short_name(name)], row)
        elif event == "skill":
            skills[short_name(row.get("skill"))] += 1
            if row.get("plugin_version"):
                versions[f"{str(row.get('skill')).partition(':')[0]} {row['plugin_version']}"]["skills"] += 1
        elif event == "command":
            commands[(str(row.get("command") or "?"), label(row.get("source")))] += 1
            if row.get("plugin_version"):
                versions[f"{str(row.get('command')).partition(':')[0]} {row['plugin_version']}"]["commands"] += 1
        elif event == "failure":
            failures[(label(row.get("error")), short_name(row.get("agent_type")) if row.get("agent_type") else "principal")] += 1
        elif event == "mcp":
            server = mcp[label(row.get("server"))]
            server["n"] += 1
            server["failed"] += 1 if row.get("failed") else 0
            server["duration_ms"] += int(row.get("duration_ms") or 0)
        elif event == "guard":
            bucket = guard[label(row.get("decision"))]
            bucket["n"] += 1
            bucket["context"] += int(row.get("max_context") or 0)
            bucket["idle_min"] += int(row.get("idle_min") or 0)
            if row.get("estimated_cost_usd") is not None:  # só a linha `blocked` traz o custo
                bucket["cost"] += float(row["estimated_cost_usd"])
            elif row.get("decision") == "blocked":
                bucket["no_cost"] += 1
        elif event == "hook_error":
            hook_errors += 1

    return {
        "agents": agents, "models": models, "versions": versions, "turns": turns, "turns_by_skill": turns_by_skill,
        "skills": skills, "commands": commands, "failures": failures, "mcp": mcp, "guard": guard, "reasons": reasons,
        "denials": denials, "hook_errors": hook_errors,
    }


def usd(value):
    """Duas casas, como o Claude grava; quatro abaixo de um centavo."""
    return f"{value:.4f}" if 0 < abs(value) < 0.01 else f"{value:.2f}"


def money(bucket):
    text = usd(bucket["cost"])
    return text + (f" (+{bucket['no_cost']} s/ custo)" if bucket["no_cost"] else "")


def mean(bucket):
    return usd(bucket["cost"] / max(bucket["n"] - bucket["no_cost"], 1))


def kilo(n):
    return f"{n / 1000:.0f}k" if n >= 1000 else str(n)


def print_table(title, headers, aligns, rows):
    if not rows:
        return
    print(title)
    widths = [max(len(str(r[i])) for r in [headers] + rows) for i in range(len(headers))]

    def fmt(row):
        return "  ".join(str(c).ljust(w) if a == "<" else str(c).rjust(w) for c, w, a in zip(row, widths, aligns))

    print(fmt(headers))
    print("  ".join("-" * w for w in widths))
    for r in rows:
        print(fmt(r))
    print()


def print_report(agg, show_denials):
    by_cost = lambda items: sorted(items, key=lambda kv: -kv[1]["cost"])  # noqa: E731
    print_table("Subagentes, por agente, modelo e esforço",
                ("agente", "modelo", "esforço", "n", "US$ total", "US$ média", "min", "api", "neg", "retom."),
                ("<", "<", "<", ">", ">", ">", ">", ">", ">", ">"),
                [(a, m, e, b["n"], money(b), mean(b), f"{b['duration_s'] / 60:.1f}", b["api_calls"], b["denials"],
                  b["resumes"] or "") for (a, m, e), b in by_cost(agg["agents"].items())])
    print_table("Subagentes, por modelo", ("modelo", "n", "US$ total", "US$ média", "min", "api"),
                ("<", ">", ">", ">", ">", ">"),
                [(m, b["n"], money(b), mean(b), f"{b['duration_s'] / 60:.1f}", b["api_calls"])
                 for m, b in by_cost(agg["models"].items())])
    print_table("Por versão do plugin", ("plugin e versão", "subagentes", "US$ subagentes", "skills", "comandos"),
                ("<", ">", ">", ">", ">"),
                [(k, v["subagents"], usd(v["cost"]), v["skills"], v["commands"])
                 for k, v in sorted(agg["versions"].items())])
    print_table("Turnos da sessão principal, por modelo e esforço",
                ("modelo", "esforço", "turnos", "US$ total", "US$ média", "min", "api", "retom."),
                ("<", "<", ">", ">", ">", ">", ">", ">"),
                [(m, e, b["n"], money(b), mean(b), f"{b['duration_s'] / 60:.1f}", b["api_calls"], b["resumes"] or "")
                 for (m, e), b in by_cost(agg["turns"].items())])
    print_table("Turnos com skill — o turno inteiro, que pode ter mais de uma skill",
                ("skill", "turnos", "US$ total", "US$ média", "min"), ("<", ">", ">", ">", ">"),
                [(s, b["n"], money(b), mean(b), f"{b['duration_s'] / 60:.1f}")
                 for s, b in by_cost(agg["turns_by_skill"].items())])
    print_table("Skills (evento skill, o começo da janela)", ("skill", "n"), ("<", ">"), agg["skills"].most_common())
    print_table("Comandos digitados", ("comando", "origem", "n"), ("<", "<", ">"),
                [(c, s, n) for (c, s), n in agg["commands"].most_common()])
    print_table("Falhas, por tipo de erro", ("erro", "onde", "n"), ("<", "<", ">"),
                [(e, w, n) for (e, w), n in agg["failures"].most_common()])
    print_table("MCP, por servidor", ("servidor", "chamadas", "falhas", "ms médio"), ("<", ">", ">", ">"),
                [(s, b["n"], b["failed"], round(b["duration_ms"] / max(b["n"], 1)))
                 for s, b in sorted(agg["mcp"].items(), key=lambda kv: -kv[1]["n"])])
    print_table("Trava de retomada, por decisão (US$ é a regravação estimada na decisão)",
                ("decisão", "n", "parada média (min)", "contexto médio", "US$ total"), ("<", ">", ">", ">", ">"),
                [(d, b["n"], round(b["idle_min"] / b["n"]), kilo(round(b["context"] / b["n"])), money(b))
                 for d, b in sorted(agg["guard"].items())])
    print_table("Negações de hook, por motivo", ("n", "motivo (sem o alvo)"), (">", "<"),
                [(n, r) for r, n in agg["reasons"].most_common()])
    if show_denials and agg["denials"]:
        print("Cada negação")
        for when, agent, reason in agg["denials"]:
            print(f"- {when} {agent}: {reason}")
        print()
    if agg["hook_errors"]:
        print(f"Erros do próprio hook de medição: {agg['hook_errors']}")


def to_json(agg):
    def bucket_rows(mapping, keys):
        return [{**dict(zip(keys, k if isinstance(k, tuple) else (k,))), **v} for k, v in mapping.items()]

    return {
        "agents": bucket_rows(agg["agents"], ("agent", "model", "effort")),
        "models": bucket_rows(agg["models"], ("model",)),
        "plugin_versions": bucket_rows(agg["versions"], ("plugin_version",)),
        "turns": bucket_rows(agg["turns"], ("model", "effort")),
        "turns_by_skill": bucket_rows(agg["turns_by_skill"], ("skill",)),
        "skills": dict(agg["skills"]),
        "commands": [{"command": c, "source": s, "n": n} for (c, s), n in agg["commands"].items()],
        "failures": [{"error": e, "where": w, "n": n} for (e, w), n in agg["failures"].items()],
        "mcp": bucket_rows(agg["mcp"], ("server",)),
        "guard": bucket_rows(agg["guard"], ("decision",)),
        "denial_reasons": dict(agg["reasons"]),
        "hook_errors": agg["hook_errors"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dir", default=DEFAULT_DIR, help="diretório com o log")
    parser.add_argument("--since", default="", help="data mínima, AAAA-MM-DD")
    parser.add_argument("--denials", action="store_true", help="lista cada negação com o motivo inteiro")
    parser.add_argument("--json", action="store_true", help="imprime a agregação em JSON")
    args = parser.parse_args()

    rows, bad, exists = read_log(os.path.join(args.dir, LOG), args.since)
    if not exists:
        print(f"nenhum log em {args.dir}: {LOG}", file=sys.stderr)
        return 2

    agg = aggregate(rows)
    if args.json:
        print(json.dumps(to_json(agg), ensure_ascii=False, indent=2))
        return 0
    print(f"{args.dir}: {LOG} {len(rows)}" + (f" (+{bad} ilegível)" if bad else "")
          + (f", desde {args.since}" if args.since else ""))
    print()
    print_report(agg, args.denials)
    return 0


if __name__ == "__main__":
    sys.exit(main())
