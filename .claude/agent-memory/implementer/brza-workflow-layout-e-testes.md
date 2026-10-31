---
name: brza-workflow-layout-e-testes
description: Como as suítes rodam no repositório brza-workflow (PLN-006): comandos, layout dos testes, o que depende de P2/P3/P7, armadilhas de Python e de cópia
metadata:
  type: project
---

- Repositório `/Users/andepb/Projects/brza-workflow` (PLN-006, nasceu no P1 de `brza-workspace@d85c783`). Gate, da raiz dele, com
  `PYTHONDONTWRITEBYTECODE=1` (o repositório não tem `.gitignore` próprio; sem a variável sobra `__pycache__`):
  `python3 -m unittest discover -s tests/hooks`, `-s tests/cli` e `python3 tests/notes-checker/run.py`.
- Testes em `tests/{cli,hooks,notes-checker}/`; cada arquivo acha o código por `ROOT`/`BIN`/`CLIENT` ou `HOOKS` calculados do
  `__file__`. O CLI (`bin/`, `packages/client/bin/`) usa `str | None`: **exige Python >= 3.10** (no 3.9 do sistema a coleta
  dá 6 erros de import); os hooks e o `notes-checker` sobem no 3.9.
- Cópia da fonte: `git archive <sha> <caminhos> | tar -x -C $(mktemp -d)`. Não use `rm -rf dir/*` depois de `cd`: o guard do
  Claude barra o glob relativo; use `mktemp -d` e apague o caminho exato.
- `sed` do macOS não tem `\(a\|b\)`: edite com `python3` e `assert t.count(a) == 1`.
- Os scripts do `packages/client/bin` importam `brza_runtime` do `bin/` por `parents[3] / 'bin'` (ou `parents[2]` no
  `brza-doctor`, que usa `HERE`); o `brza-note` roda o `brza-sessions` do cliente por `HERE.parent / 'packages/client/bin'`.
- Skips marcados com o passo que os resolve: `SettingsTest` do `test_fact_audit` (P3, lê o `settings.json`) e
  `test_the_installer_picks_it_up_as_a_command` (P7, o `brza-install` lista `WORKSPACE/scripts/brza`).
