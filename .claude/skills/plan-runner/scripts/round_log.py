#!/usr/bin/env python3
"""Grava a rodada na Entrevista do plano (PLN-021/D6).

Uso:
    python3 -I round_log.py PLN-NNN --next
    python3 -I round_log.py PLN-NNN --from rodada.json [--dry-run]

`--next` imprime o número da próxima rodada: o maior `### Rodada N` + 1.

`--from` lê o JSON da rodada e acrescenta `### Rodada N — <título> (enviada <data>)` ao fim da `## Entrevista` do
`-plan.md` — ou ao fim do `-interview.md`, quando o plano é dividido e ele existe —, com o "Apresentado antes", as
perguntas e as opções no formato do molde (rótulo, `(recomendada)`, `custo`, `se paga`) e, por pergunta:
  - `chosen` sem `literal`: `**Decidido — <rótulos>.**`;
  - `literal`: `**Resposta:** "…"`, com a leitura (`answer.reading`, ou `Lida como: <rótulos>` quando há `chosen`);
  - `reopens: "R1.2"`: acrescenta `**→ reaberta em R<N>.<k>**` à linha antiga (a `Decidido`/`Resposta` da R1.2, ou a
    última linha dela).
`--dry-run` imprime o bloco e o destino, sem gravar nada. Imprime o caminho gravado.

rodada.json (as chaves são estas; o Markdown gravado no plano continua em pt-BR):
    {"title": "...", "sent_on": "AAAA-MM-DD", "presented_before": "...",
     "answered": {"data": "AAAA-MM-DD", "session": "..."} | null,
     "questions": [{"topic": "...", "multiple": false,
                    "options": [{"label": "...", "recommended": true, "cost": "...", "pays_when": "..."}],
                    "answer": {"chosen": [0], "literal": null, "reading": null} | null, "reopens": null | "R1.2"}]}

`literal` fica como está. Saída 0; 1 com JSON fora da forma ou `reopens` que não existe; 2 uso ou plano que não existe.
"""
import argparse
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plan_md  # noqa: E402


class InvalidShape(Exception):
    def __init__(self, errors):
        super().__init__("; ".join(errors))
        self.errors = errors


def validates(payload, plan):
    errors = []
    if not isinstance(payload, dict):
        raise InvalidShape(["o JSON da rodada precisa ser um objeto"])
    if not isinstance(payload.get("title"), str) or not payload["title"].strip():
        errors.append("title: texto obrigatório")
    for key in ("sent_on", "presented_before"):
        if payload.get(key) is not None and not isinstance(payload[key], str):
            errors.append("%s: texto" % key)
    if payload.get("sent_on") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", payload["sent_on"]):
        errors.append("sent_on: AAAA-MM-DD")
    resp = payload.get("answered")
    if resp is not None:
        if not isinstance(resp, dict) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(resp.get("data", ""))):
            errors.append("answered: {data: AAAA-MM-DD, session: texto} ou null")
        elif resp.get("session") is not None and not isinstance(resp["session"], str):
            errors.append("answered.session: texto")
    ps = payload.get("questions")
    if not isinstance(ps, list) or not ps:
        errors.append("questions: lista com ao menos uma pergunta")
        ps = []
    for k, q in enumerate(ps, 1):
        pre = "questions[%d]" % (k - 1)
        if not isinstance(q, dict):
            errors.append("%s: objeto" % pre)
            continue
        if not isinstance(q.get("topic"), str) or not q["topic"].strip():
            errors.append("%s.topic: texto obrigatório" % pre)
        options = q.get("options")
        if not isinstance(options, list) or not options:
            errors.append("%s.options: lista com ao menos uma opção" % pre)
            options = []
        for j, o in enumerate(options):
            if not isinstance(o, dict) or not isinstance(o.get("label"), str) or not o["label"].strip():
                errors.append("%s.options[%d].label: texto obrigatório" % (pre, j))
                continue
            for c in ("cost", "pays_when"):
                if o.get(c) is not None and not isinstance(o[c], str):
                    errors.append("%s.options[%d].%s: texto" % (pre, j, c))
        r = q.get("answer")
        if r is not None:
            if not isinstance(r, dict):
                errors.append("%s.answer: objeto ou null" % pre)
            else:
                chosen_idxs = r.get("chosen")
                if chosen_idxs is not None:
                    if not isinstance(chosen_idxs, list) or not all(isinstance(i, int) and not isinstance(i, bool) for i in chosen_idxs):
                        errors.append("%s.answer.chosen: lista de índices" % pre)
                    elif any(i < 0 or i >= len(options) for i in chosen_idxs):
                        errors.append("%s.answer.chosen: índice fora das opções" % pre)
                    elif len(chosen_idxs) > 1 and not q.get("multiple"):
                        errors.append("%s.answer.chosen: mais de uma, e a pergunta não é `multiple`" % pre)
                if r.get("literal") is not None and not isinstance(r["literal"], str):
                    errors.append("%s.answer.literal: texto ou null" % pre)
        reopens = q.get("reopens")
        if reopens is not None:
            if not isinstance(reopens, str) or not re.fullmatch(r"R\d+\.\d+", reopens):
                errors.append("%s.reopens: `R<n>.<k>` ou null" % pre)
            elif plan.question_text(reopens) is None:
                errors.append("%s.reopens: %s não existe na Entrevista" % (pre, reopens))
    if errors:
        raise InvalidShape(errors)


def next_number(plan):
    return max([r.n for r in plan.rounds()] or [0]) + 1


def _labels(q, idxs):
    return "; ".join(q["options"][i]["label"].rstrip(".") for i in idxs)


def _session(txt):
    """`a sessão do workstream playground` -> `na sessão do workstream playground`; outro texto fica como veio."""
    t = txt.strip()
    t = re.sub(r"^(?:a\s+)?(sessão\b)", r"na \1", t)
    return t


def block(payload, n, level=3):
    """O Markdown da rodada `n`, com o heading de `level`."""
    sent_on = payload.get("sent_on") or datetime.date.today().isoformat()
    L = ["%s Rodada %d — %s (enviada %s)" % ("#" * level, n, payload["title"].strip(), sent_on), ""]
    if payload.get("presented_before"):
        ap = payload["presented_before"].strip().split("\n")
        L.append("> **Apresentado antes:** " + ap[0])
        L.extend("> " + x if x.strip() else ">" for x in ap[1:])
        L.append("")
    resp = payload.get("answered")
    if resp:
        L.append("Respondida em %s%s." % (resp["data"], (", " + _session(resp["session"])) if resp.get("session") else ""))
    else:
        L.append("Sem resposta.")
    L.append("")
    for k, q in enumerate(payload["questions"], 1):
        if q.get("multiple"):
            L.append("%d. **%s** (seleção múltipla). Opções:" % (k, q["topic"].strip().rstrip(".")))
        else:
            L.append("%d. **%s.** Opções:" % (k, q["topic"].strip().rstrip(".")))
        options = q["options"]
        for j, o in enumerate(options):
            pieces = o["label"].strip().rstrip(".;")
            if o.get("recommended"):
                pieces += " (recomendada)"
            extra = []
            if o.get("cost"):
                extra.append("custo: %s" % o["cost"].strip().rstrip(".;"))
            if o.get("pays_when"):
                extra.append("se paga: %s" % o["pays_when"].strip().rstrip(".;"))
            line = "   - " + pieces + (" — " + "; ".join(extra) if extra else "")
            line += "." if j == len(options) - 1 else ";"
            L.append(line)
        r = q.get("answer") or {}
        chosen_idxs = r.get("chosen") or []
        lit = r.get("literal")
        if lit:
            L.append("")
            reading_text = r.get("reading")
            if not reading_text and chosen_idxs:
                reading_text = "Lida como: %s." % _labels(q, chosen_idxs)
            L.append('   **Resposta:** "%s"%s' % (lit.strip(), (" " + reading_text.strip()) if reading_text else ""))
        elif chosen_idxs:
            L.append("")
            L.append("   **Decidido — %s.**" % _labels(q, chosen_idxs))
        L.append("")
    while L and not L[-1].strip():
        L.pop()
    return "\n".join(L) + "\n"


def _target(plan):
    """(arquivo, índice de inserção, nível dos headings): o fim da `## Entrevista`, ou o fim do `-interview.md`."""
    inter = next((a for a in plan.files if a.role == "interview"), None)
    level = 3
    if inter is not None:
        rs = [r for r in plan.rounds() if r.file is inter]
        if rs:
            level = rs[-1].level
        else:
            level = 2
        end = len(inter.lines)
        while end > 0 and not inter.lines[end - 1].strip():
            end -= 1
        return inter, end, level
    sec = plan.section(r"^Entrevista\b")
    if sec is None:
        raise InvalidShape(["o plano não tem `## Entrevista` nem `-interview.md`; abra a seção antes"])
    rs = [r for r in plan.rounds() if r.file is plan.main_file]
    if rs:
        level = rs[-1].level
    end = sec.end
    while end > sec.start + 1 and not plan.main_file.lines[end - 1].strip():
        end -= 1
    return plan.main_file, end, level


def _line_old(q):
    """Índice da linha da pergunta `q` que recebe `→ reaberta em`: a `Decidido`/`Resposta`, ou a última não vazia."""
    for i in (q.index_decided_line(), q.answer_index()):
        if i is not None:
            return i
    last_line = q.end - 1
    while last_line > q.start and not q.file.lines[last_line].strip():
        last_line -= 1
    return last_line


def applies(plan, payload, dry_run=False):
    """Devolve `{n, file, block, reopened}`; grava, salvo `dry_run`."""
    validates(payload, plan)
    n = next_number(plan)
    plan_file, pos, level = _target(plan)
    text = block(payload, n, level)
    reopened = []
    edits = {}  # arquivo -> {indice: texto}
    for k, q in enumerate(payload["questions"], 1):
        reopens = q.get("reopens")
        if reopens:
            prior = plan.question_text(reopens)
            i = _line_old(prior)
            fresh = "R%d.%d" % (n, k)
            edits.setdefault(prior.file, {})[i] = "**→ reaberta em %s**" % fresh
            reopened.append((reopens, fresh))
    if dry_run:
        return {"n": n, "file": plan_file.path, "block": text, "reopened": reopened}
    # monta as linhas novas de cada arquivo
    saved_paths = set(edits) | {plan_file}
    for a in saved_paths:
        lines = list(a.lines)
        for i, mark_text in sorted(edits.get(a, {}).items()):
            lines[i] = lines[i].rstrip() + " " + mark_text
        if a is plan_file:
            lines[pos:pos] = [""] + text.rstrip("\n").split("\n")
            if lines[-1] != "":
                lines.append("")
        with open(a.path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    return {"n": n, "file": plan_file.path, "block": text, "reopened": reopened}


def main(argv=None):
    ap = argparse.ArgumentParser(prog="round_log.py", description="grava a rodada na Entrevista do plano")
    ap.add_argument("plan")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--next", action="store_true")
    g.add_argument("--from", dest="origin")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-panel", action="store_true", help="não republica o painel do plano")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        pl = plan_md.load(a.plan)
    except plan_md.PlanNotFound as e:
        print("erro: %s" % e, file=sys.stderr)
        return 2
    if a.next:
        print(next_number(pl))
        return 0
    try:
        with open(a.origin, encoding="utf-8") as f:
            payload = json.load(f)
    except (OSError, ValueError) as e:
        print("erro: não li %s: %s" % (a.origin, e), file=sys.stderr)
        return 1
    try:
        res = applies(pl, payload, dry_run=a.dry_run)
    except InvalidShape as e:
        for x in e.errors:
            print("forma: %s" % x, file=sys.stderr)
        return 1
    if a.dry_run:
        print("# dry-run: Rodada %d, %s" % (res["n"], res["file"]))
        print(res["block"], end="")
        for old, new in res["reopened"]:
            print("# marcaria %s com `→ reaberta em %s`" % (old, new))
    else:
        print(res["file"])
        if not a.no_panel:
            import plan_panel
            plan_panel.emit(plan_panel.publish_safe(pl.path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
