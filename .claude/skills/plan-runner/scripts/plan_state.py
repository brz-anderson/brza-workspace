#!/usr/bin/env python3
"""O estado do plano e a conferência dele (PLN-021/D6): onde o plano está, o próximo passo, as horas somadas contra o
frontmatter, os IDs, e os problemas que o `check_notes.py` não cobre.

Uso:
    python3 -I plan_state.py PLN-NNN|caminho [--json] [--next] [--fix] [--strict]

    --json     o estado inteiro em JSON: {plano, phase, status, ready, proximo, passos, horas, ids, problemas}
    --next     imprime só o próximo passo (o primeiro pendente cujas dependências fecharam)
    --fix      reescreve só as três horas do frontmatter (estimate_h, executed_h, remaining_h) pela soma das linhas
               `Estimado`/`Executado`; o resto do arquivo não muda
    --strict   os avisos também dão saída 1

Códigos de problema (`nivel` erro, salvo o marcado): checked-without-evidence, checked-without-executed,
hours-mismatch, step-without-design, step-cites-unknown-design, design-without-origin, origin-unknown-round,
deviation-not-cited (aviso), duplicate-id, hours-unreadable (aviso).

Saída: 0 limpo, 1 com problema, 2 uso ou plano que não existe.

Outros scripts importam `estado(plano)` (`plano` é `PLN-NNN`, um caminho ou um `plan_md.Plano`).
"""
import argparse
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import plan_md  # noqa: E402

RE_COMMIT = re.compile(r"(?<!\w)(?=[0-9a-f]*\d)[0-9a-f]{7,40}(?!\w)")
RE_ARQ_LINHA = re.compile(r"[\w./-]+\.\w+:\d+")
EXEMPTO_TITULO = re.compile(r"fechament|revis|rodada|aceite|a pedido", re.I)
EXEMPTO_EXECUTA = re.compile(r"revis|fechament|rodada|a pedido|aceite|`C`|\bC\d", re.I)
TOL = 0.01


def evidencia_valida(txt):
    """A evidência traz commit, comando com `→` ou `arquivo:linha` (D6)."""
    if not txt or not txt.strip():
        return False
    return bool(RE_COMMIT.search(txt) or "→" in txt or RE_ARQ_LINHA.search(txt))


def passo_exige_design(plano, p):
    """O passo precisa de `Executa D…` quando o plano tem Desenho, salvo os de rodada, revisão, aceite, fechamento."""
    if not plano.tem_desenho():
        return False
    if EXEMPTO_TITULO.search(p.titulo):
        return False
    if p.executa_txt is not None and EXEMPTO_EXECUTA.search(p.executa_txt):
        return False
    if p.executa_txt is None and not p.tem_estimado:
        return False
    return not p.executa


def somas(plano):
    est = exe = rest = 0.0
    achou = False
    for p in plano.passos():
        if p.estado == "descartado":
            continue
        if p.estimado_h is not None:
            achou = True
            est += p.estimado_h
            if p.estado == "feito":
                if p.executado_h is not None:
                    exe += p.executado_h
            else:
                rest += p.estimado_h
        elif p.estado == "feito" and p.executado_h is not None:
            exe += p.executado_h
    return {"estimate_h": round(est, 3), "executed_h": round(exe, 3), "remaining_h": round(rest, 3)}, achou


def _fm_num(plano, chave):
    v = plano.fm.get(chave)
    if v in (None, "", []):
        return None
    try:
        return float(str(v).replace(",", "."))
    except ValueError:
        return "?"


def proximo(plano):
    passos = plano.passos()
    fechados = {p.id for p in passos if p.estado in ("feito", "descartado")}
    pend = [p for p in passos if p.estado == "pendente"]
    for p in pend:
        if all(d in fechados for d in p.depende):
            return p
    return pend[0] if pend else None


def problemas(plano):
    saida = []

    def add(codigo, onde, msg, linha=None, nivel="erro"):
        saida.append({"codigo": codigo, "onde": onde, "msg": msg, "nivel": nivel, "linha": linha})

    # passos
    for p in plano.passos():
        marcados = [c for c in p.checks if c[1].lower() == "x"]
        if marcados:
            if not p.evidencia:
                add("checked-without-evidence", p.id, "o passo tem `[x]` e nenhum `**Evidência:**`", p.onde)
            elif not evidencia_valida(p.evidencia):
                add("checked-without-evidence", p.id,
                    "a `**Evidência:**` não traz commit, comando com `→` nem `arquivo:linha`", p.onde)
        if p.estado == "feito" and p.tem_estimado and not p.executado_preenchido:
            add("checked-without-executed", p.id, "o passo está fechado e o `Executado` está vazio", p.onde)
        if p.tem_estimado and p.estimado_h is None and p.estado != "descartado":
            add("hours-unreadable", p.id, "o `Estimado` não é um número de horas", p.onde, "aviso")
        if passo_exige_design(plano, p):
            add("step-without-design", p.id, "o passo não tem `Executa D…` e o plano tem Desenho", p.onde)
        d_ids = {d["id"] for d in plano.desenhos()}
        for d in p.executa:
            if d not in d_ids:
                add("step-cites-unknown-design", p.id, "o passo executa %s, que o Desenho não tem" % d, p.onde)
    # o Desenho
    rodadas = {r.n: r for r in plano.rodadas()}
    perguntas = set(plano.ids_r())
    for d in plano.desenhos():
        onde = d["secao"].onde()
        if not d["origem_txt"]:
            add("design-without-origin", d["id"], "o item não tem a linha `- **Origem:**`", onde)
            continue
        for r in d["origem_rs"]:
            if "." in r:
                ok = r in perguntas
            else:
                ok = int(r[1:]) in rodadas
            if not ok:
                add("origin-unknown-round", d["id"], "a Origem cita %s, que a Entrevista não tem" % r, onde)
    # desvios
    citados = set()
    for p in plano.passos():
        citados.update(re.findall(r"\bX\d+\b", p.texto))
    vistos = set()
    for x in plano.desvios():
        if x["id"] in vistos:
            continue
        vistos.add(x["id"])
        if not x["passos"] and x["id"] not in citados:
            add("deviation-not-cited", x["id"], "nenhum passo cita o desvio, e ele não nomeia o passo que afeta",
                x["onde"], "aviso")
    # IDs repetidos
    ids = plano.ids()
    for tipo in ("P", "D", "X", "C", "A"):
        vistos = set()
        for i in ids[tipo]:
            if i in vistos:
                add("duplicate-id", i, "o ID %s aparece mais de uma vez (%s)" % (i, tipo))
            vistos.add(i)
    ns = [r.n for r in plano.rodadas()]
    for n in sorted({n for n in ns if ns.count(n) > 1}):
        add("duplicate-id", "Rodada %d" % n, "a Rodada %d aparece mais de uma vez" % n)
    # perguntas repetidas dentro da rodada
    for r in plano.rodadas():
        ks = [q.k for q in r.perguntas]
        for k in sorted({k for k in ks if ks.count(k) > 1}):
            add("duplicate-id", "R%d.%d" % (r.n, k), "a pergunta R%d.%d aparece mais de uma vez" % (r.n, k))
    # horas
    soma, achou = somas(plano)
    fm = {k: _fm_num(plano, k) for k in ("estimate_h", "executed_h", "remaining_h")}
    if achou or any(v is not None for v in fm.values()):
        for k in ("estimate_h", "executed_h", "remaining_h"):
            v = fm[k]
            if v == "?":
                add("hours-mismatch", "frontmatter:" + k, "o %s do frontmatter não é um número" % k)
            elif v is None:
                if achou:
                    add("hours-mismatch", "frontmatter:" + k, "o frontmatter não tem %s e a soma dá %s" % (k, plan_md.fmt_horas(soma[k])))
            elif abs(v - soma[k]) > TOL:
                add("hours-mismatch", "frontmatter:" + k,
                    "%s no frontmatter é %s e a soma dos passos dá %s" % (k, plan_md.fmt_horas(v), plan_md.fmt_horas(soma[k])))
    return saida


def estado(plano, raiz=None):
    """O estado do plano, como o `--json` imprime. `plano`: `PLN-NNN`, um caminho ou um `plan_md.Plano`."""
    pl = plan_md.carrega(plano, raiz)
    soma, achou = somas(pl)
    fm = {k: _fm_num(pl, k) for k in ("estimate_h", "executed_h", "remaining_h")}
    probs = problemas(pl)
    confere = not any(p["codigo"] == "hours-mismatch" for p in probs)
    prox = proximo(pl)
    return {
        "plano": pl.id,
        "arquivo": os.path.relpath(pl.path, pl.raiz) if pl.raiz and pl.path.startswith(pl.raiz) else pl.path,
        "titulo": pl.h1(),
        "phase": pl.fm.get("phase"),
        "status": pl.fm.get("status"),
        "ready": pl.fm.get("ready"),
        "proximo": prox.id if prox else None,
        "passos": [{
            "id": p.id, "titulo": p.titulo, "executa": p.executa, "executor": p.executor,
            "estimado_h": p.estimado_h, "executado_h": p.executado_h, "estado": p.estado,
            "evidencia": bool(p.evidencia and evidencia_valida(p.evidencia)),
        } for p in pl.passos()],
        "horas": {"frontmatter": {k: (None if v == "?" else v) for k, v in fm.items()}, "somado": soma,
                  "confere": confere},
        "ids": pl.ids(),
        "problemas": [{"codigo": p["codigo"], "onde": p["onde"], "msg": p["msg"], "nivel": p["nivel"],
                       "linha": p["linha"]} for p in probs],
    }


def fix_horas(plano):
    """Reescreve as três horas do frontmatter pela soma dos passos. Devolve as chaves que mudaram."""
    pl = plan_md.carrega(plano)
    soma, achou = somas(pl)
    if not achou:
        return []
    arq = pl.principal
    if arq.fm_fim < 0:
        return []
    linhas = list(arq.linhas)
    mudou = []
    for k in ("estimate_h", "executed_h", "remaining_h"):
        novo = "%s: %s" % (k, plan_md.fmt_horas(soma[k]))
        idx = None
        for i in range(1, arq.fm_fim):
            if re.match(r"^%s:" % k, linhas[i]):
                idx = i
                break
        if idx is not None:
            if linhas[idx].strip() != novo:
                linhas[idx] = novo
                mudou.append(k)
        else:
            # depois da última chave escalar de topo anterior; as três entram juntas, em ordem
            pos = arq.fm_fim
            for i in range(1, arq.fm_fim):
                if re.match(r"^(ready|estimate_h|executed_h):", linhas[i]):
                    pos = i + 1
            linhas.insert(pos, novo)
            arq.fm_fim += 1
            mudou.append(k)
    if mudou:
        with open(arq.path, "w", encoding="utf-8") as f:
            f.write("\n".join(linhas))
    return mudou


def tela(est):
    ls = []
    ls.append("%s — %s" % (est["plano"], est["titulo"] or ""))
    ls.append("fase %s · status %s" % (est["phase"], est["status"]))
    if est["ready"]:
        ls.append("ready: %s" % est["ready"])
    ps = est["passos"]
    feitos = sum(1 for p in ps if p["estado"] == "feito")
    ls.append("passos: %d, %d feitos, %d pendentes, %d descartados" % (
        len(ps), feitos, sum(1 for p in ps if p["estado"] == "pendente"), sum(1 for p in ps if p["estado"] == "descartado")))
    h = est["horas"]
    ls.append("horas: frontmatter %s · somado %s · %s" % (
        _fmt_h(h["frontmatter"]), _fmt_h(h["somado"]), "confere" if h["confere"] else "NÃO confere"))
    if est["proximo"]:
        p = next(x for x in ps if x["id"] == est["proximo"])
        ls.append("próximo: %s — %s" % (p["id"], p["titulo"]))
    else:
        ls.append("próximo: nenhum")
    if est["problemas"]:
        ls.append("problemas (%d):" % len(est["problemas"]))
        for p in est["problemas"]:
            ls.append("  [%s] %s %s: %s%s" % (p["nivel"], p["codigo"], p["onde"], p["msg"],
                                              " (%s)" % p["linha"] if p.get("linha") else ""))
    else:
        ls.append("problemas: nenhum")
    return "\n".join(ls)


def _fmt_h(d):
    return "est %s / exec %s / rest %s" % tuple("—" if d[k] is None else plan_md.fmt_horas(d[k])
                                                  for k in ("estimate_h", "executed_h", "remaining_h"))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="plan_state.py", description="o estado do plano e a conferência dele")
    ap.add_argument("plano")
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
        plan_md.carrega(a.plano)
    except plan_md.PlanoNaoEncontrado as e:
        print("erro: %s" % e, file=sys.stderr)
        return 2
    if a.fix:
        mudou = fix_horas(a.plano)
        print("--fix: %s" % (", ".join(mudou) if mudou else "as horas já conferiam"), file=sys.stderr)
        if not a.no_panel:
            import plan_panel
            r = plan_panel.publica_seguro(a.plano)
            plan_panel.emite(r, out=lambda s: print(s, file=sys.stderr if a.json or a.next else sys.stdout))
    est = estado(a.plano)
    if a.next:
        pl = plan_md.carrega(a.plano)
        p = proximo(pl)
        print("%s — %s" % (p.id, p.titulo) if p else "nenhum")
        return 0
    if a.json:
        print(json.dumps(est, ensure_ascii=False, indent=2))
    else:
        print(tela(est))
    erros = [p for p in est["problemas"] if p["nivel"] == "erro"]
    avisos = [p for p in est["problemas"] if p["nivel"] == "aviso"]
    return 1 if erros or (a.strict and avisos) else 0


if __name__ == "__main__":
    sys.exit(main())
