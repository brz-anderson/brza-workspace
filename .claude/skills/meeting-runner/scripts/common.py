"""Pedaços que os scripts da skill dividem: a raiz padrão e o cabeçalho de `rodada-N.md`.

Só biblioteca padrão; a raiz padrão e o `corta_medida` vêm do `skillkit`. O `panel.py`, o `wait_round.py` e o `launch_persona.py` importam daqui (fonte única do prazo e da
duração anunciada da rodada, para o painel e a espera nunca divergirem).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _kit  # noqa: E402,F401
from skillkit.paths import (  # noqa: E402,F401
    HEADING_H12_RE as TITULO_N12_RE,
    MEASUREMENT_RE as MEDIDA_RE,
    ROUND_END_RE as FIM_RODADA_RE,
    default_root as raiz_padrao,
    strip_measurement as corta_medida,
)

PRAZO_RE = re.compile(r'\(\s*prazo:\s*(\d{1,2})\s*[h:]\s*(\d{2})\s*\)')
DURACAO_RE = re.compile(r'\(\s*dura[çc][ãa]o:\s*~?\s*(\d+)\s*min(?:utos?)?\s*\)', re.IGNORECASE)
TITULO_RE = re.compile(r'^#\s*Rodada\s+\d+\s*[—–-]\s*(.*)$')


def cabecalho_rodada(path):
    """Primeira linha do rodada-N.md -> (titulo, prazo 'HH:MM', duracao_min). O título não leva o "(prazo…)" nem o
    "(duração…)"; `(prazo: 21h40)` vale como horário, `(duração: ~5 min)` vira minutos (o prazo é a abertura + eles)."""
    try:
        with open(path, encoding='utf-8') as f:
            linha = f.readline().strip()
    except OSError:
        return None, None, None
    m = TITULO_RE.match(linha)
    if not m:
        return None, None, None
    resto = m.group(1)
    prazo = duracao = None
    pm = PRAZO_RE.search(resto)
    if pm:
        prazo = f'{int(pm.group(1)):02d}:{pm.group(2)}'
        resto = (resto[:pm.start()] + resto[pm.end():]).strip()
    dm = DURACAO_RE.search(resto)
    if dm:
        duracao = int(dm.group(1))
        resto = (resto[:dm.start()] + resto[dm.end():]).strip()
    return resto.strip() or None, prazo, duracao


def resolver_personas(reuniao, nomes):
    """As personas do manifesto por nome, slug ou sessão (sem caixa); `todas` ou nada = todas. Nome que não existe
    levanta `ValueError("persona desconhecida: X")`: nenhuma flag trata o nome desconhecido em silêncio."""
    if not nomes or [q.lower() for q in nomes] == ["todas"]:
        return list(reuniao["personas"])
    chosen = []
    for q in nomes:
        achou = [p for p in reuniao["personas"]
                 if q.lower() in (p["nome"].lower(), (p.get("slug") or "").lower(), (p.get("sessao") or "").lower())]
        if not achou:
            raise ValueError(f"persona desconhecida: {q}")
        chosen += achou
    return chosen


def duracao_anunciada(path):
    """A duração anunciada (min) na primeira linha do `rodada-N.md`, ou None."""
    return cabecalho_rodada(path)[2]
