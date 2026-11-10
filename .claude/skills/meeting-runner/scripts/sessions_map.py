"""O mapa de sessões do `brza sessions` v2: o código vive em `.claude/scripts/skillkit/sessions_map.py`; aqui ficam o
reexporte (para `import sessions_map` seguir valendo) e o `dispatch_of`, que lê o manifesto de reunião."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _kit  # noqa: E402,F401
from skillkit.sessions_map import (OPEN_FIELDS, common_root, epoch, fold_map, load_map, map_file,  # noqa: E402,F401
                                   read_rows)


def dispatch_of(persona, entradas):
    """O Dispatch da persona: o do mapa v2, senão o `dispatch_id` do manifesto, senão o da linha v1."""
    e = entradas.get(persona.get("sessao")) or {}
    if e.get("dispatch") and not e.get("legacy"):
        return e["dispatch"]
    return persona.get("dispatch_id") or e.get("dispatch")
