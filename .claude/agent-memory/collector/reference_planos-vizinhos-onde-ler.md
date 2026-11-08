---
name: planos-vizinhos-onde-ler
description: Onde moram os planos do fluxo de sessões/MCP/medição e os atalhos para lê-los sem checkout
metadata:
  type: reference
---

- Planos de runtime/MCP/medição moram em `workstream/tools-kit` (PLN-009, 010, 012, 013, 015); PLN-004 e 005 em `workstream/workspace`. Lê-se com `git show workstream/<ws>:plans/PLN-NNN-.../PLN-NNN-plan.md`. Planos grandes (009: 748 linhas, 005: 819) — leia o frontmatter, `Retomar`, `Cobertura`, `Passos` (grep `^- \[|Evidência`) e `Pendências conhecidas`; as rodadas ficam no próprio plano (009, 012) ou em `-interview.md` (004, 013).
- Frontmatter+H1 de muitas issues: loop `git grep -il` + `git show | grep -m1 '^status:'`.
- Código do `brza sessions`: `~/Projects/brza-workflow/packages/client/bin/brza-sessions` (VERBS, sem `read`, sem `--model/--effort` em 2026-11-08). MCP: `packages/mcp/brza_mcp/{policy,cycle,tools}.py`; a tabela modelo/esforço por runtime é `DEFAULTS` em `policy.py`.
- Branches do brza-workflow quase todas já mescladas (`git branch --merged master`); a única só em branch em 2026-11-08 era `feat/pln-012-medida-por-tarefa`. Os worktrees dos planos ficam em `~/Projects/brza-workflow/.worktrees/`.
- O scratch `/private/tmp/pln004/` (Desenho v3 do PLN-004) não vai ao git e pode ter sumido.
- `Retomar` dos planos está desatualizado vs `Pendências` às vezes (ex.: PLN-013 lista issues já fechadas); confirme com `status:` da issue.
