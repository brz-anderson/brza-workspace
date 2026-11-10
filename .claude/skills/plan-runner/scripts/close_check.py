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

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import plan_md  # noqa: E402
import plan_state  # noqa: E402

RE_LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
RE_DESTINO = re.compile(r"→\s*(.+?)\s*$")
RE_FECHO_JANELA = re.compile(r"\bmeta\b.*(cumpri|atingi|alcan[cç]ad)|(cumpri|atingi|alcan[cç]ad).*\bmeta\b", re.I)


def _git(raiz, *args):
    try:
        r = subprocess.run(["git", "-C", raiz] + list(args), capture_output=True, text=True, timeout=20)
        return r.returncode, r.stdout
    except (OSError, subprocess.SubprocessError):
        return 1, ""


def le_nota(raiz, caminho_abs):
    """Texto da nota: no disco, ou na branch de outro workstream (`git show workstream/x:caminho`)."""
    if os.path.isfile(caminho_abs):
        with open(caminho_abs, encoding="utf-8") as f:
            return f.read()
    try:
        rel = os.path.relpath(caminho_abs, raiz)
    except ValueError:
        return None
    if rel.startswith(".."):
        # nota de outro worktree irmão (`../../../workspace/work/...`): tenta o mesmo caminho relativo à raiz comum
        return None
    rc, refs = _git(raiz, "for-each-ref", "--format=%(refname:short)", "refs/heads/workstream/")
    if rc != 0:
        return None
    for ref in refs.split():
        rc, out = _git(raiz, "show", "%s:%s" % (ref, rel))
        if rc == 0:
            return out
    return None


def _status(texto):
    m = re.match(r"^---\n(.*?)\n---", texto, re.S)
    if not m:
        return None
    for ln in m.group(1).split("\n"):
        mm = re.match(r"^status:\s*(\S+)", ln)
        if mm:
            return mm.group(1).strip("\"'")
    return None


def item1(pl, est):
    falta = []
    for p in pl.passos():
        if p.estado == "feito":
            continue
        if p.estado == "descartado":
            marcas = [c for c in p.checks if c[1] == "-"]
            if not any(re.search(r"—\s*\S+\s+\S+\s+\S+|descart|motivo|porque|pois", c[2], re.I) for c in marcas):
                falta.append("%s: `[-]` sem motivo" % p.id)
        else:
            falta.append("%s: pendente" % p.id)
    for pr in est["problemas"]:
        if pr["codigo"] in ("checked-without-evidence", "checked-without-executed"):
            falta.append("%s: %s" % (pr["onde"], pr["msg"]))
    if not pl.passos():
        return ("falta", ["o plano não tem passos"])
    return ("falta", falta) if falta else ("ok", [])


def item2(pl):
    sec = pl.secao(r"^Revisões\b")
    if not sec:
        return ("ok", ["sem `## Revisões`: nenhum achado"])
    falta, vistos = [], 0
    for ln in sec.corpo:
        for rot, alvo in RE_LINK.findall(ln):
            if not re.match(r"REV-\d+", rot):
                continue
            alvo = alvo.split("#")[0]
            path = os.path.normpath(os.path.join(pl.dir, alvo))
            txt = le_nota(pl.raiz, path)
            if txt is None:
                falta.append("%s: a nota %s não existe" % (rot.split(":")[0], alvo))
                continue
            linhas = txt.split("\n")
            for i, l in enumerate(linhas):
                m = re.match(r"^#{2,4}\s+(A\d+)\b", l)
                if not m:
                    continue
                vistos += 1
                destino = None
                mh = re.search(r"→\s*(.+?)\s*$", l)
                if mh:
                    destino = mh.group(1)
                for l2 in ([] if destino else linhas[i + 1:i + 6]):
                    mm = RE_DESTINO.search(l2) if l2.lstrip().startswith(">") else None
                    if mm:
                        destino = mm.group(1)
                        break
                    if re.match(r"^#{1,4}\s", l2):
                        break
                tag = "%s/%s" % (rot.split(":")[0], m.group(1))
                if not destino or re.fullmatch(r"a definir\.?", destino.strip(), re.I):
                    falta.append("%s: sem destino (`a definir`)" % tag)
                    continue
                msg = _destino_existe(pl, path, destino)
                if msg:
                    falta.append("%s: %s" % (tag, msg))
    return ("falta", falta) if falta else ("ok", ["%d achado(s) com destino" % vistos])


def _destino_existe(pl, nota_path, destino):
    d = destino.strip().strip("`").strip()
    base = re.split(r"\s+[—-]\s+|[:;,]", d, maxsplit=1)[0].strip().lower()
    if base.startswith("corrigid") or base in ("descartado", "falso"):
        return None
    m = RE_LINK.search(d)
    if m:
        alvo = os.path.normpath(os.path.join(os.path.dirname(nota_path), m.group(2).split("#")[0]))
        return None if le_nota(pl.raiz, alvo) is not None else "o link %s não existe" % m.group(2)
    m = re.match(r"(issue|decisão|decisao)\s+`?([\w.-]+?)`?(?:\.md)?(?:\s|$)", d, re.I)
    if m:
        pasta = "issues" if m.group(1).lower() == "issue" else "decisions"
        alvo = os.path.join(pl.raiz, "work", pasta, m.group(2) + ".md")
        return None if le_nota(pl.raiz, alvo) is not None else "%s %s não existe" % (m.group(1), m.group(2))
    return "o destino `%s` não é nenhum dos conhecidos" % d


def item3(pl):
    sec = pl.secao(r"^Decisões\b")
    cobertos = set()
    for d in pl.desenhos():
        for r in d["origem_rs"]:
            cobertos.add(r)
    texto_dec = sec.texto() if sec else ""
    ja = set()
    for mm in plan_md.RE_R.finditer(texto_dec):
        ja.add("R%s" % mm.group(1) + (".%s" % mm.group(2) if mm.group(2) else ""))
    cand = []
    for r in pl.rodadas():
        for q in r.perguntas:
            if not q.decidida:
                continue
            if q.id in cobertos or ("R%d" % r.n) in cobertos or q.id in ja:
                continue
            cand.append("%s — %s" % (q.id, q.tema))
    if cand:
        return ("manual", cand)
    return ("ok", ["nenhuma rodada decidida sem D nem link em `## Decisões`"])


def item4(pl):
    sec = pl.secao(r"^Decisões\b")
    if not sec:
        return ("ok", ["sem `## Decisões`"])
    falta, n = [], 0
    for ln in sec.corpo:
        for rot, alvo in RE_LINK.findall(ln):
            if alvo.startswith("http"):
                continue
            n += 1
            path = os.path.normpath(os.path.join(pl.dir, alvo.split("#")[0]))
            txt = le_nota(pl.raiz, path)
            if txt is None:
                falta.append("%s: a nota não existe" % alvo)
                continue
            st = _status(txt)
            if st != "done":
                falta.append("%s: status %s, e deveria ser done" % (os.path.basename(alvo), st))
    return ("falta", falta) if falta else ("ok", ["%d decisão(ões) done" % n])


def item5(pl):
    if any(re.search(r"brza-studio@|brza-studio/", p.evidencia or "") for p in pl.passos()):
        return ("manual", ["há commit do brza-studio na evidência: o resumo vai no commit ou no PR, com o link do plano"])
    return ("n/a", ["sem commit do brza-studio na evidência"])


def item6(pl):
    sec = pl.secao(r"^Janela\b")
    if not sec:
        return ("n/a", ["o plano não tem `## Janela`"])
    for ln in sec.corpo:
        if RE_FECHO_JANELA.search(ln) and re.search(r"fecho|fechou|fechamento|cumpri|atingi|alcan", ln, re.I) \
                and not re.match(r"^\s*[-*]\s+\*\*(Janela e meta|Cortes previstos)", ln.strip()):
            return ("ok", [ln.strip()[:160]])
    return ("falta", ["a `## Janela` não tem a linha que diz se a meta foi cumprida"])


ITENS = [
    (1, "passo `[x]` com evidência ou `[-]` com motivo"),
    (2, "achado com destino que existe"),
    (3, "o durável na casa dona"),
    (4, "decisões `done`"),
    (5, "o resumo no commit ou PR"),
    (6, "a Janela fechada"),
]


def confere(plano):
    pl = plan_md.carrega(plano)
    est = plan_state.estado(pl)
    res = {1: item1(pl, est), 2: item2(pl), 3: item3(pl), 4: item4(pl), 5: item5(pl), 6: item6(pl)}
    itens = [{"item": n, "titulo": t, "resultado": res[n][0], "detalhe": res[n][1]} for n, t in ITENS]
    return {"plano": pl.id, "itens": itens, "limpo": not any(i["resultado"] == "falta" for i in itens)}


def tela(r):
    ls = ["%s — conferência do fechamento" % r["plano"]]
    for i in r["itens"]:
        ls.append("%d. %-6s %s" % (i["item"], i["resultado"], i["titulo"]))
        for d in i["detalhe"]:
            ls.append("     - %s" % d)
    ls.append("fechamento: %s" % ("pode seguir" if r["limpo"] else "trava, algum item falta"))
    return "\n".join(ls)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="close_check.py", description="a conferência do fechamento do plano")
    ap.add_argument("plano")
    ap.add_argument("--json", action="store_true")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        r = confere(a.plano)
    except plan_md.PlanoNaoEncontrado as e:
        print("erro: %s" % e, file=sys.stderr)
        return 2
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else tela(r))
    return 0 if r["limpo"] else 1


if __name__ == "__main__":
    sys.exit(main())
