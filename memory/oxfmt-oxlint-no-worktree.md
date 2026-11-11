---
name: oxfmt-oxlint-no-worktree
description: "no worktree do brza-studio, oxfmt/oxlint com vários caminhos juntos não acham os arquivos; rode um por um"
metadata:
  node_type: memory
  type: project
  originSessionId: 85ae8eba-93c8-42f2-9ae8-ee460db37dfc
  modified: 2026-11-03T00:35:17.637Z
---

Em `~/Projects/brza-studio/.worktrees/*`, `pnpm exec oxfmt --check a b c` só achou o CSS, e `oxlint a b c` disse "No files found" (2026-11-02, P80). Arquivo por arquivo, com `--ignore-path=/dev/null`, o `oxfmt` funciona. Suspeita não confirmada: o `.worktrees/` no `.git/info/exclude`.

**Why:** um lint "limpo" sem saída pode não ter lido nada.
**How to apply:** formate arquivo por arquivo e conte como lint válido o `lint-staged` do commit (oxlint, ast-grep, react-doctor) e o `pnpm check:changed`. A suíte completa só roda na CI (norma em `.claude/rules/workspace.md`).
