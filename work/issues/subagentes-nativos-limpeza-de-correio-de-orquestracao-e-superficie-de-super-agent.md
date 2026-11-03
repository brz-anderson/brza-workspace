---
status: open
description: Os PRs #37574, #33403 e #21333 e as issues #37407 e #37637 do upstream refinam o roteamento para subagentes nativos, o correio entre workers e a supervisão externa de workflows.
scope:
  - brza-studio
  - brza-workflow
priority: medium
opened: 2026-11-03
tags:
  - chat
  - tooling
---

# Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent

Rastreado dos PRs abertos no upstream [`stablyai/orca#37574`](https://github.com/stablyai/orca/pull/37574),
[`stablyai/orca#33403`](https://github.com/stablyai/orca/pull/33403),
[`stablyai/orca#21333`](https://github.com/stablyai/orca/pull/21333) e
[`stablyai/orca#11279`](https://github.com/stablyai/orca/pull/11279), além das issues
[`stablyai/orca#37407`](https://github.com/stablyai/orca/issues/37407),
[`stablyai/orca#37637`](https://github.com/stablyai/orca/issues/37637) e
[`stablyai/orca#19388`](https://github.com/stablyai/orca/issues/19388).

## Os pontos do upstream

1. **Preferência por subagentes nativos nomeados (`#37574`):** remove da skill `orchestration` (`skills/orchestration/SKILL.md`
   e `skill-guides/orchestration.md`) a regra que transformava toda requisição de revisão em um worker externo do app,
   preferindo os subagentes nativos nomeados do runtime quando disponíveis.
2. **Correio de orquestração recolhido e sem atropelar digitação (`#33403`, `#37637`, `#11279`):**
   - `#33403` recolhe envelopes internos de correio de orquestração e mantém a trilha do chat voltada para a conversa
     humana;
   - `#37637` pede que o assunto e o corpo enviados por um worker apareçam diretamente no Native Chat do coordenador;
   - `#11279` adia a injeção `push-on-idle` enquanto o usuário está digitando no composer (evitando o bug da `#14832`).
3. **Nome do worktree no preâmbulo de despacho (`#21333`) e GC de workers encerrados (`#19388`):** identifica o worktree
   do worker no preâmbulo e aponta a falta de coleta automática para workers em `terminalState=reclaimable`.
4. **Superfície estável para super-agent (`#37407`):** propõe contratos estáveis para que um supervisor externo observe,
   direcione e feche o ciclo de execução de agentes sem depender de scraping de terminal.

## O que fazer

- Conferir o impacto de `#37574` e `#11279` na convivência entre a skill `orchestration` embutida no `brza-studio` e os
  subagentes por papel (`collector`, `implementer`, `reviewer`, `designer`) do `brza-workflow`.
- Usar os requisitos das issues `#37407` e `#37637` como insumo para a evolução da coordenação entre workstreams no
  `brza-workflow`.
