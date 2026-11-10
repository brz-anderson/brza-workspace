"""Põe `.claude/scripts/` no sys.path: `SKILLKIT` (para rodar a mesma suíte contra outra cópia) ou a pasta `scripts/` daqui.
Importar este módulo antes de `skillkit`."""
import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
SKILLKIT = os.environ.get("SKILLKIT") or os.path.dirname(HERE)
if SKILLKIT not in sys.path:
    sys.path.insert(0, SKILLKIT)
