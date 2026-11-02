---
status: open
description: O test_brza_sessions do brza-workflow passa num ambiente limpo e falha dentro do chat do BrzA Studio, que vaza a BRZA_WORKSPACE e as ORCA_*.
scope:
  - workspace
opened: 2026-11-02
tags:
  - tooling
---

# Os testes do brza-workflow falham quando rodam dentro do chat do BrzA Studio

Achado em 2026-11-02, ao rodar a suíte para o `brza devices`, no
[O brza devices, que lista, cria e abre os simuladores e os emuladores](../worklogs/2026-11-02-o-brza-devices.md).

## O que se viu

O `tests/cli/test_brza_sessions.py` do `~/Projects/brza-workflow` passa num ambiente limpo e falha no do chat. Às
15h, com o `a313ec5` já na `master` de lá:

| Onde rodou | Resultado |
| :-- | :-- |
| No chat do BrzA Studio | `Ran 33 tests … FAILED (failures=4)` |
| No mesmo chat, com `env -i HOME=… PATH=…` | `OK` |

- **As 4 falhas:**
  - `test_a_relative_checkout_from_a_worktree_starts_at_the_workspace_root`;
  - `test_a_relative_checkout_from_a_code_worktree_outside_its_directory_starts_at_the_workspace_root`;
  - `test_a_relative_checkout_outside_the_workspace_starts_at_the_workspace_variable`;
  - `test_open_without_any_workspace_refuses_and_launches_nothing`.
- **Nas duas primeiras**, o `--worktree` sai com o
  `path:/Users/andepb/Projects/brza-workspace/.worktrees/tools-kit` da sessão, e não com o workspace temporário do
  teste. O ambiente do chat vence o do teste. A suspeita é a `BRZA_WORKSPACE`, que o `claude-brza` põe na sessão, ou uma
  das `ORCA_*`; isso não foi isolado.
- **A suíte inteira, no ambiente limpo:** `Ran 433 tests … OK`.

Uma rodada anterior, também no chat, deu ainda 15 erros e 1 falha no `test_brza_note_index.py`:
`ImportError: cannot import name 'NoWorkspace' from 'brza_runtime'`, vindo do `packages/client/bin/brza-sessions:59`. A
sessão do PLN-006 commitava o `a313ec5` (14:00) no mesmo checkout enquanto a suíte rodava. Depois do commit, o arquivo
passa no chat. Esses erros vieram da edição concorrente, e não do ambiente.

## O que falta

Fazer o `test_brza_sessions.py` ignorar o ambiente de quem o roda: limpar a `BRZA_*`, a `ORCA_*` e a
`CLAUDE_SESSION_NAME` no `setUp`, ou numa base comum dos testes do `tests/cli`. Até lá, a suíte que vale é a do
ambiente limpo:

```bash
env -i HOME="$HOME" PATH="$(dirname "$(command -v python3)"):/opt/homebrew/bin:/usr/bin:/bin" python3 -m unittest discover -s tests/cli
```
