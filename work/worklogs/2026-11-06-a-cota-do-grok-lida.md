---
scope:
  - brza-studio
  - brza-workflow
tags:
  - tooling
refs:
  - PLN-013
  - issue:o-app-nao-le-a-cota-do-grok
---

# A cota do Grok lida pelo app

O pedido de Anderson, em 2026-11-06, ao retomar o
[PLN-013: O Grok, o Codex e o Antigravity abrem pelo `brza sessions` e recebem tarefas do MCP](../../plans/PLN-013-grok-codex-e-agy-no-brza-sessions-e-no-mcp/PLN-013-plan.md):
seguir a issue [O app não lê a cota do Grok](../issues/o-app-nao-le-a-cota-do-grok.md).

## O que se fez

- **A leitura de hoje.** O `account list --json` do BrzA Studio (`refreshUsage: false`) devolveu o instantâneo do app
  (`updatedAt` 2026-11-06 18:10): `grokAuthConfigured: true`, `status: "ok"`, `error: null`, `weekly` a 38% com reset
  2026-11-10 22:28. É a mesma janela de 2026-11-04, quando o `brza quota` mostrou 17%.
- **A janela `session`.** Não faz parte da leitura. O `billingUsageResult` em
  `brza-studio/src/main/rate-limits/grok-fetcher.ts` grava `session: null`. O billing vira `weekly` ou `monthly`.
- **O MCP.** O `parse` (`accounts.py`) coloca o `weekly` no uso da conta `systemDefault`. O `Limits._quota` admite 38%
  (`ok`) e segura 95% em `account_quota` (`janela weekly já em 95%, quota.hard_cap_percent = 90`). Sem mudança de
  código, como a issue pedia (PLN-013/R3.2).
- **A issue fechou** em 2026-11-06, com `completed`.

## Em aberto

- As outras pendências do PLN-013: o `status` sem runtime, o `/rename` do Grok e do Antigravity, e o texto do ciclo.
