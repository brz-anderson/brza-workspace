#!/usr/bin/env python3
"""O estado do plano e a conferência dele (PLN-021/D6): onde o plano está, o próximo passo, as horas somadas contra o
frontmatter, os IDs, e os problemas que o `check_notes.py` não cobre.

Uso:
    python3 -I plan_state.py PLN-NNN|caminho [--json] [--next] [--fix] [--strict]

    --json     o estado inteiro em JSON: {plan, file, title, phase, status, ready, next, steps, hours, ids, problems}
    --next     imprime só o próximo passo (o primeiro pendente cujas dependências fecharam)
    --fix      reescreve só as três horas do frontmatter (estimate_h, executed_h, remaining_h) pela soma das linhas
               `Estimado`/`Executado`; o resto do arquivo não muda
    --strict   os avisos também dão saída 1

Códigos de problema (`level` `erro`, salvo o marcado): checked-without-evidence, checked-without-executed,
hours-mismatch, step-without-design, step-cites-unknown-design, design-without-origin, origin-unknown-round,
deviation-not-cited (aviso), duplicate-id, hours-unreadable (aviso).

Saída: 0 limpo, 1 com problema, 2 uso ou plano que não existe.

Outros scripts importam `state(plan)` (`plan` é `PLN-NNN`, um caminho ou um `plan_md.Plan`).
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plan_md  # noqa: E402

RE_COMMIT = re.compile(r"(?<!\w)(?=[0-9a-f]*\d)[0-9a-f]{7,40}(?!\w)")
RE_FILE_LINE = re.compile(r"[\w./-]+\.\w+:\d+")
EXEMPT_TITLE = re.compile(r"fechament|revis|rodada|aceite|a pedido", re.I)
EXEMPT_EXECUTES = re.compile(r"revis|fechament|rodada|a pedido|aceite|`C`|\bC\d", re.I)
TOL = 0.01


def evidence_validates(txt):
    """A evidência traz commit, comando com `→` ou `arquivo:linha` (D6)."""
    if not txt or not txt.strip():
        return False
    return bool(RE_COMMIT.search(txt) or "→" in txt or RE_FILE_LINE.search(txt))


def step_requires_design(plan, p):
    """O passo precisa de `Executa D…` quando o plano tem Desenho, salvo os de rodada, revisão, aceite, fechamento."""
    if not plan.has_design():
        return False
    if EXEMPT_TITLE.search(p.title):
        return False
    if p.executes_txt is not None and EXEMPT_EXECUTES.search(p.executes_txt):
        return False
    if p.executes_txt is None and not p.has_estimate:
        return False
    return not p.executes


def sums(plan):
    estimate = exe = rest = 0.0
    found = False
    for p in plan.steps():
        if p.state == "descartado":
            continue
        if p.estimated_h is not None:
            found = True
            estimate += p.estimated_h
            if p.state == "feito":
                if p.executed_h is not None:
                    exe += p.executed_h
            else:
                rest += p.estimated_h
        elif p.state == "feito" and p.executed_h is not None:
            exe += p.executed_h
    return {"estimate_h": round(estimate, 3), "executed_h": round(exe, 3), "remaining_h": round(rest, 3)}, found


def _fm_num(plan, key):
    v = plan.fm.get(key)
    if v in (None, "", []):
        return None
    try:
        return float(str(v).replace(",", "."))
    except ValueError:
        return "?"


def next_step(plan):
    steps = plan.steps()
    closed_states = {p.id for p in steps if p.state in ("feito", "descartado")}
    pending = [p for p in steps if p.state == "pendente"]
    for p in pending:
        if all(d in closed_states for d in p.depends):
            return p
    return pending[0] if pending else None


def problems(plan):
    output = []

    def add(code_text, where, msg, line=None, level="erro"):
        output.append({"code": code_text, "where": where, "msg": msg, "level": level, "line": line})

    # passos
    for p in plan.steps():
        marked = [c for c in p.checks if c[1].lower() == "x"]
        if marked:
            if not p.evidence:
                add("checked-without-evidence", p.id, "o passo tem `[x]` e nenhum `**Evidência:**`", p.where)
            elif not evidence_validates(p.evidence):
                add("checked-without-evidence", p.id,
                    "a `**Evidência:**` não traz commit, comando com `→` nem `arquivo:linha`", p.where)
        if p.state == "feito" and p.has_estimate and not p.executed_filled:
            add("checked-without-executed", p.id, "o passo está fechado e o `Executado` está vazio", p.where)
        if p.has_estimate and p.estimated_h is None and p.state != "descartado":
            add("hours-unreadable", p.id, "o `Estimado` não é um número de horas", p.where, "aviso")
        if step_requires_design(plan, p):
            add("step-without-design", p.id, "o passo não tem `Executa D…` e o plano tem Desenho", p.where)
        d_ids = {d["id"] for d in plan.design_list()}
        for d in p.executes:
            if d not in d_ids:
                add("step-cites-unknown-design", p.id, "o passo executa %s, que o Desenho não tem" % d, p.where)
    # o Desenho
    rounds = {r.n: r for r in plan.rounds()}
    questions = set(plan.round_ids())
    for d in plan.design_list():
        where = d["section"].where()
        if not d["origin_text"]:
            add("design-without-origin", d["id"], "o item não tem a linha `- **Origem:**`", where)
            continue
        for r in d["origin_ids"]:
            if "." in r:
                ok = r in questions
            else:
                ok = int(r[1:]) in rounds
            if not ok:
                add("origin-unknown-round", d["id"], "a Origem cita %s, que a Entrevista não tem" % r, where)
    # desvios
    cited = set()
    for p in plan.steps():
        cited.update(re.findall(r"\bX\d+\b", p.text))
    seen = set()
    for x in plan.deviations():
        if x["id"] in seen:
            continue
        seen.add(x["id"])
        if not x["steps"] and x["id"] not in cited:
            add("deviation-not-cited", x["id"], "nenhum passo cita o desvio, e ele não nomeia o passo que afeta",
                x["where"], "aviso")
    # IDs repetidos
    ids = plan.ids()
    for kind in ("P", "D", "X", "C", "A"):
        seen = set()
        for i in ids[kind]:
            if i in seen:
                add("duplicate-id", i, "o ID %s aparece mais de uma vez (%s)" % (i, kind))
            seen.add(i)
    ns = [r.n for r in plan.rounds()]
    for n in sorted({n for n in ns if ns.count(n) > 1}):
        add("duplicate-id", "Rodada %d" % n, "a Rodada %d aparece mais de uma vez" % n)
    # perguntas repetidas dentro da rodada
    for r in plan.rounds():
        ks = [q.k for q in r.questions]
        for k in sorted({k for k in ks if ks.count(k) > 1}):
            add("duplicate-id", "R%d.%d" % (r.n, k), "a pergunta R%d.%d aparece mais de uma vez" % (r.n, k))
    # horas
    total, found = sums(plan)
    fm = {k: _fm_num(plan, k) for k in ("estimate_h", "executed_h", "remaining_h")}
    if found or any(v is not None for v in fm.values()):
        for k in ("estimate_h", "executed_h", "remaining_h"):
            v = fm[k]
            if v == "?":
                add("hours-mismatch", "frontmatter:" + k, "o %s do frontmatter não é um número" % k)
            elif v is None:
                if found:
                    add("hours-mismatch", "frontmatter:" + k, "o frontmatter não tem %s e a soma dá %s" % (k, plan_md.format_hours(total[k])))
            elif abs(v - total[k]) > TOL:
                add("hours-mismatch", "frontmatter:" + k,
                    "%s no frontmatter é %s e a soma dos passos dá %s" % (k, plan_md.format_hours(v), plan_md.format_hours(total[k])))
    return output


def state(plan, root=None):
    """O estado do plano, como o `--json` imprime. `plan`: `PLN-NNN`, um caminho ou um `plan_md.Plan`."""
    pl = plan_md.load(plan, root)
    total, found = sums(pl)
    fm = {k: _fm_num(pl, k) for k in ("estimate_h", "executed_h", "remaining_h")}
    probs = problems(pl)
    check = not any(p["code"] == "hours-mismatch" for p in probs)
    following = next_step(pl)
    return {
        "plan": pl.id,
        "file": os.path.relpath(pl.path, pl.root) if pl.root and pl.path.startswith(pl.root) else pl.path,
        "title": pl.h1(),
        "phase": pl.fm.get("phase"),
        "status": pl.fm.get("status"),
        "ready": pl.fm.get("ready"),
        "next": following.id if following else None,
        "steps": [{
            "id": p.id, "title": p.title, "executes": p.executes, "executor": p.executor,
            "estimated_h": p.estimated_h, "executed_h": p.executed_h, "state": p.state,
            "evidence": bool(p.evidence and evidence_validates(p.evidence)),
        } for p in pl.steps()],
        "hours": {"frontmatter": {k: (None if v == "?" else v) for k, v in fm.items()}, "summed": total,
                  "matches": check},
        "ids": pl.ids(),
        "problems": [{"code": p["code"], "where": p["where"], "msg": p["msg"], "level": p["level"],
                       "line": p["line"]} for p in probs],
    }


def fix_hours(plan):
    """Reescreve as três horas do frontmatter pela soma dos passos. Devolve as chaves que mudaram."""
    pl = plan_md.load(plan)
    total, found = sums(pl)
    if not found:
        return []
    plan_file = pl.main_file
    if plan_file.fm_end < 0:
        return []
    lines = list(plan_file.lines)
    changed = []
    for k in ("estimate_h", "executed_h", "remaining_h"):
        fresh = "%s: %s" % (k, plan_md.format_hours(total[k]))
        idx = None
        for i in range(1, plan_file.fm_end):
            if re.match(r"^%s:" % k, lines[i]):
                idx = i
                break
        if idx is not None:
            if lines[idx].strip() != fresh:
                lines[idx] = fresh
                changed.append(k)
        else:
            # depois da última chave escalar de topo anterior; as três entram juntas, em ordem
            pos = plan_file.fm_end
            for i in range(1, plan_file.fm_end):
                if re.match(r"^(ready|estimate_h|executed_h):", lines[i]):
                    pos = i + 1
            lines.insert(pos, fresh)
            plan_file.fm_end += 1
            changed.append(k)
    if changed:
        with open(plan_file.path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    return changed


def screen(overview):
    ls = []
    ls.append("%s — %s" % (overview["plan"], overview["title"] or ""))
    ls.append("fase %s · status %s" % (overview["phase"], overview["status"]))
    if overview["ready"]:
        ls.append("ready: %s" % overview["ready"])
    ps = overview["steps"]
    done_states = sum(1 for p in ps if p["state"] == "feito")
    ls.append("passos: %d, %d feitos, %d pendentes, %d descartados" % (
        len(ps), done_states, sum(1 for p in ps if p["state"] == "pendente"), sum(1 for p in ps if p["state"] == "descartado")))
    h = overview["hours"]
    ls.append("horas: frontmatter %s · somado %s · %s" % (
        _fmt_h(h["frontmatter"]), _fmt_h(h["summed"]), "matches" if h["matches"] else "NÃO confere"))
    if overview["next"]:
        p = next(x for x in ps if x["id"] == overview["next"])
        ls.append("próximo: %s — %s" % (p["id"], p["title"]))
    else:
        ls.append("próximo: nenhum")
    if overview["problems"]:
        ls.append("problemas (%d):" % len(overview["problems"]))
        for p in overview["problems"]:
            ls.append("  [%s] %s %s: %s%s" % (p["level"], p["code"], p["where"], p["msg"],
                                              " (%s)" % p["line"] if p.get("line") else ""))
    else:
        ls.append("problemas: nenhum")
    return "\n".join(ls)


def _fmt_h(d):
    return "est %s / exec %s / rest %s" % tuple("—" if d[k] is None else plan_md.format_hours(d[k])
                                                  for k in ("estimate_h", "executed_h", "remaining_h"))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="plan_state.py", description="o estado do plano e a conferência dele")
    ap.add_argument("plan")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--next", action="store_true")
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--no-panel", action="store_true", help="com --fix, não republica o painel do plano")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        plan_md.load(a.plan)
    except plan_md.PlanNotFound as e:
        print("erro: %s" % e, file=sys.stderr)
        return 2
    if a.fix:
        changed = fix_hours(a.plan)
        print("--fix: %s" % (", ".join(changed) if changed else "as horas já conferiam"), file=sys.stderr)
        if not a.no_panel:
            import plan_panel
            r = plan_panel.publish_safe(a.plan)
            plan_panel.emit(r, out=lambda s: print(s, file=sys.stderr if a.json or a.next else sys.stdout))
    overview = state(a.plan)
    if a.next:
        pl = plan_md.load(a.plan)
        p = next_step(pl)
        print("%s — %s" % (p.id, p.title) if p else "nenhum")
        return 0
    if a.json:
        print(json.dumps(overview, ensure_ascii=False, indent=2))
    else:
        print(screen(overview))
    errors = [p for p in overview["problems"] if p["level"] == "erro"]
    warning_texts = [p for p in overview["problems"] if p["level"] == "aviso"]
    return 1 if errors or (a.strict and warning_texts) else 0


if __name__ == "__main__":
    sys.exit(main())
