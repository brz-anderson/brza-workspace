"""A reunião real do P7 (CI no chat) como fixture: manifesto, worklogs de trecho, síntese e estado da R3, em um root temporário."""
import json
import os
import shutil

from _paths import fixture


def monta_raiz(tmp, manifesto_puro=True):
    """Copia os arquivos de `fixtures/p7/` para `<tmp>` na forma do repositório e devolve (root, reuniao).

    `manifesto_puro` tira do manifesto as sobrescritas (`dispatch_id`, `claude_session`): o mapa decide."""
    d = os.path.join(tmp, ".sessions", "reuniao-ci-no-chat")
    os.makedirs(d, exist_ok=True)
    for nome in ("reuniao.json", "briefing.md", "sintese-3.json", "rodada-2.md", "rodada-3.md", "estado-r3.json",
                 "launch-prumo.log", "launch-trava.log", "launch-relance.log"):
        shutil.copy(fixture("p7", nome), os.path.join(d, nome))
    wl = os.path.join(tmp, "work", "worklogs")
    os.makedirs(wl, exist_ok=True)
    for slug in ("prumo", "trava", "relance"):
        shutil.copy(fixture("p7", "worklogs", f"{slug}.md"), os.path.join(wl, f"2026-11-09-reuniao-ci-no-chat-{slug}.md"))
    with open(os.path.join(d, "reuniao.json"), encoding="utf-8") as f:
        reuniao = json.load(f)
    if manifesto_puro:
        for p in reuniao["personas"]:
            for k in ("dispatch_id", "claude_session", "provider_session"):
                p.pop(k, None)
    return tmp, reuniao


def jsonl(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
