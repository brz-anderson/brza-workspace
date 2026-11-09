"""Põe no sys.path a pasta de scripts sob teste: `MR_SCRIPTS` (para rodar a mesma suíte contra o snapshot anterior) ou a
pasta `scripts/` desta skill. Importar este módulo antes dos scripts."""
import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
SCRIPTS = os.environ.get("MR_SCRIPTS") or os.path.dirname(HERE)
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)
FIXTURES = os.path.join(HERE, "fixtures")


def fixture(*partes):
    return os.path.join(FIXTURES, *partes)


def le(*partes):
    with open(fixture(*partes), encoding="utf-8") as f:
        return f.read()
