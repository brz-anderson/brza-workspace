---
status: done
scope:
  - workspace
  - brza-studio
opened: 2026-10-30
decided: 2026-10-30
decided_by: Anderson
tags:
  - tooling
---

# Cada workstream aprende na memória dele, com subagentes por papel e métricas por workstream

**A sessão e os subagentes por papel (`collector`, `implementer`, `reviewer`, `designer`) gravam a memória na branch
do workstream; o que vale para todos sobe à norma; a medição leva o workstream, a memória e as rodadas, e o resumo
sai por workstream e por dia.**

Decidido por Anderson em 2026-10-30, na sessão `brza-workspace-73`: o pedido "todo agente deve ter memória própria,
assim podemos acompanhar o "aprendizado" em cada frente de trabalho e ter métricas pra poder melhorar o fluxo cada vez
mais"; as rodadas "Sessão e subagentes por papel", "No git, na branch do workstream (Recomendado)", "Viram norma e
saem da memória (Recomendado)", as quatro métricas, os quatro papéis, "Inglês (Recomendado)", "memory/ na raiz
(Recomendado)", "Sonnet (Recomendado)", "No workstream do plano (Recomendado)", "Para o memory/ do workstream studio
(Recomendado)", "Levar pelo --agents no claude-brza", "Com o worklog que fecha a tarefa (Recomendado)", "Symlink para
o workstream (Recomendado)"; e, sobre o texto, "A.1 e F.1".

## Fundamento

- O runtime dá uma memória só por repositório, para todos os worktrees; o `autoMemoryDirectory` por worktree e o
  `memory: project` dos subagentes separam a memória por workstream sem código no runtime.
- **Recusados:** a memória fora do git, que não guarda histórico; a cópia das memórias gerais a cada workstream, que
  diverge; o commit automático por turno, que suja o log; o Haiku no `collector`, sem medição que o sustente; a
  memória dos agentes commitada no `brza-studio`, que mistura a frente ao código.

## Onde mais está

- **A norma:** o `AGENTS.md`, "Cada workstream aprende na memória dele", e o `CLAUDE.md`, "A memória vai ao
  workstream" e a tabela da medição, em `77f018c` na `master`.
- **Os agentes:** `.claude/agents/`, no mesmo commit.
- **O `brza-studio`:** a linha `/.claude/agent-memory` no `.gitignore`, em `3e36a6945f2`.
- **O registro:** [A memória por workstream, os subagentes por papel e as métricas](../worklogs/2026-10-30-a-memoria-por-workstream-os-subagentes-por-papel-e-as-metricas.md).
