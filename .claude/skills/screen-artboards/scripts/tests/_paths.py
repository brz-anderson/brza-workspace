"""Põe `scripts/` da skill no sys.path (e o skillkit, pelo `_kit`). Importar antes dos módulos da skill."""
import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
SCRIPTS = os.path.dirname(HERE)
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)
import _kit  # noqa: E402,F401
