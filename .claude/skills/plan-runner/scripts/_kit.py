"""Põe `.claude/scripts/` no sys.path (ou `SKILLKIT`, para rodar contra outra cópia). Importar antes de `skillkit`."""
import os
import sys

KIT = os.environ.get("SKILLKIT") or os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "..", "scripts"))
if KIT not in sys.path:
    sys.path.insert(0, KIT)
