#!/usr/bin/env python3
"""check_briefing.py: confere o briefing da reunião antes de abrir as personas (X8).

Uso:
    check_briefing.py <briefing.md>

Na seção `## O que existe hoje`, todo item de lista com algarismo precisa da marca `conferido`, seguida de um comando em
crase e de `→` com o resultado, na forma do molde:

    - ‹fato› — conferido às HH:MM: `comando` → resultado

O fato com número que a coordenação só leu (e não rodou) é o que as personas herdam como verdade: o `1.352` do P7 era a base
empilhada de um PR, e três personas o repetiram. Item sem algarismo não precisa da marca. Lista os itens sem a marca
(`linha N: …`) e sai 1; sai 0 quando todos têm; sai 2 sem a seção (ou sem o arquivo).
"""
import re
import sys

SECAO = re.compile(r"^##\s+O que existe hoje\b")
OUTRA_SECAO = re.compile(r"^##\s")
ITEM = re.compile(r"^(\s*)(?:[-*+]|\d+[.)])\s+(.*)$")
# número de fato: algarismos soltos ("163", "1.352"); não vale id/linha/rótulo (`R6`, `PLN-017`, `#39020`, `arq.py:120`,
# data)
NUMERO = re.compile(r"(?<![\w#.:/~-])\d+(?:[.,]\d+)*(?![\w-])|(?<=~)\d+(?:[.,]\d+)*(?![\w-])")
# entre crases, só sai o que é código: comando, caminho, id, hash ou ref. O resto (`1.352 commits`, `US$ 0,25`,
# `+19.165/−6.137`, `1352 de 2000`) é fato como fora das crases e passa pelo NUMERO (A1 da conferência de d12ed91).
COMANDOS = {"brza", "orca", "git", "gh", "grep", "rg", "ls", "wc", "find", "cat", "sed", "awk", "jq", "python3", "python",
            "node", "npm", "pnpm", "curl", "du", "head", "tail", "date", "sqlite3", "claude", "codex", "grok", "agy"}
SINAL_DE_COMANDO = re.compile(r"\s--?\w|\||\$\(|\s[<>]|\s=|=\S")
CAMINHO = re.compile(r"^[~.]?/|^\.{1,2}[\w-]|[\w-]/[\w.-]|\.\w{1,5}(?::\d+)?$|:\d+(?:-\d+)?$")
REF = re.compile(r"^#\d+$|^[A-Za-z][\w.-]*\d[\w.:-]*$|^\d*[a-f]\w*$")  # #39020, PLN-017, R6, ctx_…, v1.4.255, hash


def eh_codigo(conteudo):
    """O conteúdo da crase é comando, caminho, id, hash ou ref (e não um fato com número)?"""
    c = conteudo.strip()
    if not re.search(r"[A-Za-z]", c):
        return c.startswith("#")                     # só número e símbolo: fato; `#39020` é ref
    primeiro = c.split()[0]
    if primeiro in COMANDOS or SINAL_DE_COMANDO.search(c):
        return True
    if " " not in c and (CAMINHO.search(c) or REF.match(c)):
        return True
    return False
MARCA = re.compile(r"conferido\b.*?`[^`]+`.*?→\s*\S", re.S)


def itens_da_secao(texto):
    """[(linha, texto do item)] da seção `## O que existe hoje`, com as linhas de continuação juntas; None sem a seção."""
    linhas = texto.split("\n")
    ini = next((i for i, l in enumerate(linhas) if SECAO.match(l)), None)
    if ini is None:
        return None
    itens, atual = [], None
    for i in range(ini + 1, len(linhas)):
        l = linhas[i]
        if OUTRA_SECAO.match(l):
            break
        m = ITEM.match(l)
        if m and not (atual and l.startswith(" ") and len(m.group(1)) > atual[2]):
            atual = [i + 1, m.group(2), len(m.group(1))]
            itens.append(atual)
        elif atual is not None and l.strip() and l.startswith(" "):
            atual[1] += " " + l.strip()
        elif not l.strip():
            atual = None
    return [(n, t) for n, t, _ in itens]


def numeros(texto):
    """Os números de fato do item, sem o que está entre crases; a detecção e a exibição usam ESTA função."""
    return NUMERO.findall(re.sub(r"`([^`]*)`", lambda m: "" if eh_codigo(m.group(1)) else m.group(1), texto))


def sem_marca(texto):
    """Os itens com algarismo e sem a marca `conferido … `comando` → resultado`."""
    itens = itens_da_secao(texto)
    if itens is None:
        return None
    return [(n, t) for n, t in itens if numeros(t) and not MARCA.search(t)]


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("uso: check_briefing.py <briefing.md>", file=sys.stderr)
        return 2
    try:
        with open(argv[0], encoding="utf-8") as f:
            texto = f.read()
    except OSError as e:
        print(f"check_briefing: {e}", file=sys.stderr)
        return 2
    faltam = sem_marca(texto)
    if faltam is None:
        print("check_briefing: o briefing não tem a seção `## O que existe hoje`", file=sys.stderr)
        return 2
    for n, t in faltam:
        resumo = " ".join(t.split())
        achados = list(dict.fromkeys(numeros(t)))[:6]
        print(f"linha {n}: {resumo[:90]}{'…' if len(resumo) > 90 else ''} [números: {', '.join(achados)}] — "
              "falta `conferido às HH:MM: `comando` → resultado`")
    if faltam:
        print(f"{len(faltam)} item(ns) com número sem a marca de conferência")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
