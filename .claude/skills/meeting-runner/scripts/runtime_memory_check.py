#!/usr/bin/env python3
"""runtime_memory_check.py: lista a memória de runtime gravada fora do repositório depois de um instante.

Uso:
    runtime_memory_check.py <início ISO ou HH:MM[:SS]> [--root DIR]

As personas de outros runtimes gravam auto-memória fora do repositório e fora de `memory/`, mesmo com o briefing
mandando escrever só no worklog (F24 do levantamento do PLN-017). Este script lista os arquivos criados ou
modificados depois do início, no formato pronto para a seção `## Fora do workspace` do worklog:

    caminho · mtime · tamanho

Onde procura (o `~` é o `HOME` do ambiente; o que não existe é ignorado em silêncio):
  - `~/.grok/memory-v2/`                 (Grok: MEMORY.md, topics/, índices sqlite)
  - `~/.codex/memories/`                 (Codex)
  - `~/.gemini/GEMINI.md`, `~/.gemini/antigravity/brain/` e `~/.gemini/antigravity/knowledge/`
                                         (Antigravity: só o que é memória e notas; os logs, as conversas e o cache ficam de fora)
  - `~/.claude/projects/*/memory/`       (Claude: sai com a marca `aviso`, não é erro; a memória do workstream mora no repositório)
`--root` exclui o que estiver dentro do repositório. Sai sempre com 0; sem nada, imprime "nenhum".
"""
import argparse
import glob
import os
import sys
from datetime import date, datetime, time, timedelta


def parse_start(s):
    """'2026-11-07T21:19' / '2026-11-07 21:19:25' (ISO) ou 'HH:MM[:SS]' (hoje, no fuso local) -> datetime local."""
    s = s.strip()
    if len(s) <= 8 and s.count(":") >= 1 and "-" not in s:
        h, m, *sec = [int(x) for x in s.split(":")]
        d = datetime.combine(date.today(), time(h, m, sec[0] if sec else 0)).astimezone()
        # HH:MM no futuro é de ontem (a reunião atravessou a meia-noite)
        return d - timedelta(days=1) if d > datetime.now().astimezone() else d
    d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    return d if d.tzinfo else d.astimezone()


def locations(home):
    """[(rótulo, [caminhos])]: arquivos soltos ou diretórios, os que não existem ficam de fora na varredura."""
    j = lambda *p: os.path.join(home, *p)
    return [
        ("grok", [j(".grok", "memory-v2")]),
        ("codex", [j(".codex", "memories")]),
        ("gemini", [j(".gemini", "GEMINI.md"), j(".gemini", "antigravity", "brain"),
                    j(".gemini", "antigravity", "knowledge")]),
        ("claude", sorted(glob.glob(j(".claude", "projects", "*", "memory")))),
    ]


def files_in(path):
    if os.path.isfile(path):
        yield path
    elif os.path.isdir(path):
        for dirpath, _, names in os.walk(path):
            for n in names:
                yield os.path.join(dirpath, n)


def find_changed(start, home, root=None):
    """[(caminho, mtime, tamanho, rótulo)] dos arquivos com mtime >= início, do mais antigo ao mais novo."""
    root = os.path.realpath(root) if root else None
    achados = []
    for rotulo, paths in locations(home):
        for base in paths:
            for f in files_in(base):
                try:
                    st = os.stat(f)
                except OSError:
                    continue
                if root and os.path.realpath(f).startswith(root + os.sep):
                    continue
                mtime = datetime.fromtimestamp(st.st_mtime).astimezone()
                if mtime >= start:
                    achados.append((f, mtime, st.st_size, rotulo))
    return sorted(achados, key=lambda x: x[1])


def format_line(path, mtime, size, rotulo, home):
    shown = "~" + path[len(home):] if path.startswith(home + os.sep) else path
    linha = f"{shown} · {mtime.strftime('%Y-%m-%d %H:%M:%S')} · {size} B"
    return linha + (" · aviso: memória do Claude fora do repositório" if rotulo == "claude" else "")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Lista a memória de runtime criada ou alterada depois de um instante.")
    ap.add_argument("inicio")
    ap.add_argument("--root")
    a = ap.parse_args(argv)
    home = os.path.expanduser("~")
    achados = find_changed(parse_start(a.inicio), home, a.root)
    if not achados:
        print("nenhum")
        return 0
    for f, mtime, size, rotulo in achados:
        print(format_line(f, mtime, size, rotulo, home))
    return 0


if __name__ == "__main__":
    sys.exit(main())
