---
status: open
description: O brza-mcp não tem como cancelar um pedido que espera na fila; no PLN-011, o pedido retido pela cota teve de sair por um UPDATE direto no SQLite.
scope:
  - workspace
opened: 2026-11-03
priority: low
tags:
  - tooling
---

# O `brza-mcp` não cancela um pedido que espera na fila

## O pedido

Da sessão coordenadora do PLN-011 (`studio`), "pln-011-coord", em 2026-11-03, para o
[PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md),
pelas Restrições do PLN-011: o defeito do orquestrador vai ao PLN-009, numa issue daqui.

## O que aconteceu

- O pedido 7 (`PLN-011/P3`, `implementer`) entrou na fila com o gate aprovado e ficou retido por `account_quota`. A
  janela de sessão da conta projetava 171% e depois 210% no reset, com `quota.hard_cap_percent = 90`.
- Anderson passou os passos de código a Codex e as revisões a Antigravity (PLN-011/R18.1). O `dispatch` só aceita
  `runtime: claude` (`packages/mcp/brza_mcp/tools.py:192-193`), e por isso o P3 abriu pelo `orchestration worker-start`
  do Studio, fora do `brza-mcp`.
- O pedido 7 tinha de sair da fila, ou abriria um worker Claude duplicado quando a janela virasse. As ferramentas são
  `dispatch`, `status` e `config`, e o `PLN-009-plan.md:207` diz "sem ferramenta `cancel`". O estado `cancelled` existe
  (`queue.py:20`), mas nada chega a ele. A coordenadora cancelou o pedido com
  `UPDATE requests SET state='cancelled' … WHERE id=7 AND state='queued'` em `~/.brza/orchestrator.db`, e o `status`
  deixou de listá-lo.

## O que fazer

Decidir no PLN-009 se o primeiro uso real justifica uma ferramenta `cancel`, só para o chamador que abriu o pedido e só
em `queued` ou `gated`. O Codex e o Antigravity no `dispatch` já são do PLN-013.
