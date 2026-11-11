#!/usr/bin/env python3
"""A conferência do fechamento do plano (PLN-021/D6): os seis itens de `references/close.md`.

Uso:
    python3 -I close_check.py PLN-NNN|caminho [--json]

| item | como confere                                                                     | resultado          |
| 1    | passo `[x]` com evidência ou `[-]` com motivo (pelo `plan_state`)                | ok / falta         |
| 2    | cada `### A<n>` dos `REV` de `## Revisões` tem `→ destino` ≠ `a definir` que existe | ok / falta         |
| 3    | os `R` decididos sem `D` nem link em `## Decisões`: candidatos, não veredito      | manual, com a lista |
| 4    | o `status` de cada nota de `## Decisões` é `done`                                | ok / falta         |
| 5    | o resumo no commit ou PR: sem commit do `brza-studio` na evidência, não se aplica | manual / n/a       |
| 6    | com `## Janela`, a linha que diz se a meta foi cumprida                          | ok / falta / n/a   |

Saída 0 só com tudo `ok` ou `n/a`, mais os `manual` listados; 1 com algum `falta`; 2 uso ou plano que não existe.
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plan_md  # noqa: E402
import plan_state  # noqa: E402

RE_LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
RE_TARGET = re.compile(r"→\s*(.+?)\s*$")
RE_CLOSE_WINDOW = re.compile(r"\bmeta\b.*(cumpri|atingi|alcan[cç]ad)|(cumpri|atingi|alcan[cç]ad).*\bmeta\b", re.I)


def _git(root, *args):
    try:
        r = subprocess.run(["git", "-C", root] + list(args), capture_output=True, text=True, timeout=20)
        return r.returncode, r.stdout
    except (OSError, subprocess.SubprocessError):
        return 1, ""


def read_note(root, path_abs):
    """Texto da nota: no disco, ou na branch de outro workstream (`git show workstream/x:caminho`)."""
    if os.path.isfile(path_abs):
        with open(path_abs, encoding="utf-8") as f:
            return f.read()
    try:
        rel = os.path.relpath(path_abs, root)
    except ValueError:
        return None
    if rel.startswith(".."):
        # nota de outro worktree irmão (`../../../workspace/work/...`): tenta o mesmo caminho relativo à raiz comum
        return None
    rc, refs = _git(root, "for-each-ref", "--format=%(refname:short)", "refs/heads/workstream/")
    if rc != 0:
        return None
    for ref in refs.split():
        rc, out = _git(root, "show", "%s:%s" % (ref, rel))
        if rc == 0:
            return out
    return None


def _status(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return None
    for ln in m.group(1).split("\n"):
        mm = re.match(r"^status:\s*(\S+)", ln)
        if mm:
            return mm.group(1).strip("\"'")
    return None


def item1(pl, overview):
    missing_ids = []
    for p in pl.steps():
        if p.state == "feito":
            continue
        if p.state == "descartado":
            mark_texts = [c for c in p.checks if c[1] == "-"]
            if not any(re.search(r"—\s*\S+\s+\S+\s+\S+|descart|motivo|porque|pois", c[2], re.I) for c in mark_texts):
                missing_ids.append("%s: `[-]` sem motivo" % p.id)
        else:
            missing_ids.append("%s: pendente" % p.id)
    for pr in overview["problems"]:
        if pr["code"] in ("checked-without-evidence", "checked-without-executed"):
            missing_ids.append("%s: %s" % (pr["where"], pr["msg"]))
    if not pl.steps():
        return ("falta", ["o plano não tem passos"])
    return ("falta", missing_ids) if missing_ids else ("ok", [])


def item2(pl):
    sec = pl.section(r"^Revisões\b")
    if not sec:
        return ("ok", ["sem `## Revisões`: nenhum achado"])
    missing_ids, seen = [], 0
    for ln in sec.body_text:
        for link_label, link_target in RE_LINK.findall(ln):
            if not re.match(r"REV-\d+", link_label):
                continue
            link_target = link_target.split("#")[0]
            path = os.path.normpath(os.path.join(pl.dir, link_target))
            txt = read_note(pl.root, path)
            if txt is None:
                missing_ids.append("%s: a nota %s não existe" % (link_label.split(":")[0], link_target))
                continue
            lines = txt.split("\n")
            for i, l in enumerate(lines):
                m = re.match(r"^#{2,4}\s+(A\d+)\b", l)
                if not m:
                    continue
                seen += 1
                target_path = None
                mh = re.search(r"→\s*(.+?)\s*$", l)
                if mh:
                    target_path = mh.group(1)
                for l2 in ([] if target_path else lines[i + 1:i + 6]):
                    mm = RE_TARGET.search(l2) if l2.lstrip().startswith(">") else None
                    if mm:
                        target_path = mm.group(1)
                        break
                    if re.match(r"^#{1,4}\s", l2):
                        break
                tag = "%s/%s" % (link_label.split(":")[0], m.group(1))
                if not target_path or re.fullmatch(r"a definir\.?", target_path.strip(), re.I):
                    missing_ids.append("%s: sem destino (`a definir`)" % tag)
                    continue
                msg = _target_exists(pl, path, target_path)
                if msg:
                    missing_ids.append("%s: %s" % (tag, msg))
    return ("falta", missing_ids) if missing_ids else ("ok", ["%d achado(s) com destino" % seen])


def _target_exists(pl, note_path, target_path):
    d = target_path.strip().strip("`").strip()
    base = re.split(r"\s+[—-]\s+|[:;,]", d, maxsplit=1)[0].strip().lower()
    if base.startswith("corrigid") or base in ("descartado", "falso"):
        return None
    m = RE_LINK.search(d)
    if m:
        link_target = os.path.normpath(os.path.join(os.path.dirname(note_path), m.group(2).split("#")[0]))
        return None if read_note(pl.root, link_target) is not None else "o link %s não existe" % m.group(2)
    m = re.match(r"(issue|decisão|decisao)\s+`?([\w.-]+?)`?(?:\.md)?(?:\s|$)", d, re.I)
    if m:
        folder = "issues" if m.group(1).lower() == "issue" else "decisions"
        link_target = os.path.join(pl.root, "work", folder, m.group(2) + ".md")
        return None if read_note(pl.root, link_target) is not None else "%s %s não existe" % (m.group(1), m.group(2))
    return "o destino `%s` não é nenhum dos conhecidos" % d


def item3(pl):
    sec = pl.section(r"^Decisões\b")
    covered = set()
    for d in pl.design_list():
        for r in d["origin_ids"]:
            covered.add(r)
    text_dec = sec.text() if sec else ""
    already_ = set()
    for mm in plan_md.RE_R.finditer(text_dec):
        already_.add("R%s" % mm.group(1) + (".%s" % mm.group(2) if mm.group(2) else ""))
    cand = []
    for r in pl.rounds():
        for q in r.questions:
            if not q.is_decided:
                continue
            if q.id in covered or ("R%d" % r.n) in covered or q.id in already_:
                continue
            cand.append("%s — %s" % (q.id, q.topic))
    if cand:
        return ("manual", cand)
    return ("ok", ["nenhuma rodada decidida sem D nem link em `## Decisões`"])


def item4(pl):
    sec = pl.section(r"^Decisões\b")
    if not sec:
        return ("ok", ["sem `## Decisões`"])
    missing_ids, n = [], 0
    for ln in sec.body_text:
        for link_label, link_target in RE_LINK.findall(ln):
            if link_target.startswith("http"):
                continue
            n += 1
            path = os.path.normpath(os.path.join(pl.dir, link_target.split("#")[0]))
            txt = read_note(pl.root, path)
            if txt is None:
                missing_ids.append("%s: a nota não existe" % link_target)
                continue
            st = _status(txt)
            if st != "done":
                missing_ids.append("%s: status %s, e deveria ser done" % (os.path.basename(link_target), st))
    return ("falta", missing_ids) if missing_ids else ("ok", ["%d decisão(ões) done" % n])


def item5(pl):
    if any(re.search(r"brza-studio@|brza-studio/", p.evidence or "") for p in pl.steps()):
        return ("manual", ["há commit do brza-studio na evidência: o resumo vai no commit ou no PR, com o link do plano"])
    return ("n/a", ["sem commit do brza-studio na evidência"])


def item6(pl):
    sec = pl.section(r"^Janela\b")
    if not sec:
        return ("n/a", ["o plano não tem `## Janela`"])
    for ln in sec.body_text:
        if RE_CLOSE_WINDOW.search(ln) and re.search(r"fecho|fechou|fechamento|cumpri|atingi|alcan", ln, re.I) \
                and not re.match(r"^\s*[-*]\s+\*\*(Janela e meta|Cortes previstos)", ln.strip()):
            return ("ok", [ln.strip()[:160]])
    return ("falta", ["a `## Janela` não tem a linha que diz se a meta foi cumprida"])


ITEM_LIST = [
    (1, "passo `[x]` com evidência ou `[-]` com motivo"),
    (2, "achado com destino que existe"),
    (3, "o durável na casa dona"),
    (4, "decisões `done`"),
    (5, "o resumo no commit ou PR"),
    (6, "a Janela fechada"),
]


def check(plan):
    pl = plan_md.load(plan)
    overview = plan_state.state(pl)
    res = {1: item1(pl, overview), 2: item2(pl), 3: item3(pl), 4: item4(pl), 5: item5(pl), 6: item6(pl)}
    item_list = [{"item": n, "title": t, "result": res[n][0], "detail": res[n][1]} for n, t in ITEM_LIST]
    return {"plan": pl.id, "items": item_list, "clean": not any(i["result"] == "falta" for i in item_list)}


def screen(r):
    ls = ["%s — conferência do fechamento" % r["plan"]]
    for i in r["items"]:
        ls.append("%d. %-6s %s" % (i["item"], i["result"], i["title"]))
        for d in i["detail"]:
            ls.append("     - %s" % d)
    ls.append("fechamento: %s" % ("pode seguir" if r["clean"] else "trava, algum item falta"))
    return "\n".join(ls)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="close_check.py", description="a conferência do fechamento do plano")
    ap.add_argument("plan")
    ap.add_argument("--json", action="store_true")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        r = check(a.plan)
    except plan_md.PlanNotFound as e:
        print("erro: %s" % e, file=sys.stderr)
        return 2
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else screen(r))
    return 0 if r["clean"] else 1


if __name__ == "__main__":
    sys.exit(main())
