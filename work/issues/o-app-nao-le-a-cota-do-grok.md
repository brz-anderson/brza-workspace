---
status: done
description: Com o login, o rateLimits.grok do app sai sem janela, e o MCP admite o worker Grok sem cota lida, só pelo teto de sessões.
scope:
  - brza-studio
  - brza-workflow
opened: 2026-11-03
completed: 2026-11-06
priority: medium
tags:
  - tooling
---

# O app não lê a cota do Grok

## O pedido

A R2.1 do
[PLN-013: O Grok, o Codex e o Antigravity abrem pelo `brza sessions` e recebem tarefas do MCP](../../plans/PLN-013-grok-codex-e-agy-no-brza-sessions-e-no-mcp/PLN-013-plan.md)
pediu a cota dos três runtimes no MCP. Para o Grok, o app não dá a cota. Na R4.2, Anderson escolheu deixá-lo em
`quota_unknown`, dentro do teto de sessões, com o `status` citando o erro, e abrir esta issue.

## O que se sabe

- **Com o login, a cota não vem.** `orca account list --json`, em 2026-11-03, dá `rateLimits.grokAuthConfigured: true`,
  mas `rateLimits.grok` traz `session: null`, `weekly: null`, `status: "unavailable"` e
  `error: "Grok did not report a usage percentage for this account"`.
- **O app tenta.** A leitura é do `brza-studio/src/main/rate-limits/grok-fetcher.ts`.

- **Em 2026-11-04 a cota veio.** O `brza quota`, no `brza-workflow@7c1684f`, mostra `[grok] … weekly usado 17%, reset
  2026-11-10 22:28`. A ausência de ontem pode ter sido só a falta de uso da conta logo depois do login. Ainda não se
  sabe se a janela `session` também vem.

## O que falta

1. Confirmar, por mais uns dias, se a leitura se mantém; se sim, fechar a issue. Se não, saber por que o Grok não reporta o percentual: o plano da conta, a API que o fetcher consulta, ou o fetcher.
2. Com a cota lida, o MCP passa a segurar o worker Grok pelas janelas de topo, como os outros (PLN-013/R3.2), sem
   mudança no desenho.

## Resolução (2026-11-06)

A leitura se manteve. O `account list --json` do BrzA Studio, com `refreshUsage: false`, devolveu o instantâneo que o
app já guardava (`updatedAt` 2026-11-06 18:10): `grokAuthConfigured: true`, `status: "ok"`, `error: null` e `weekly` a
38% (`windowMinutes` 10080, reset 2026-11-10 22:28). É a mesma janela do dia 04, quando o `brza quota` mostrou 17%.

A janela `session` não vem. O `billingUsageResult` de
`brza-studio/src/main/rate-limits/grok-fetcher.ts` grava `session: null`. O que o billing do Grok vira janela é o
`weekly` (`creditUsagePercent`) ou o `monthly` (`used` / `monthlyLimit`).

Com essa forma, o `parse` do `brza-workflow` (`accounts.py`, `_windows`) lê a janela `weekly`, e o `Limits._quota`
segura o worker quando ela passa do teto. Na forma lida hoje, 38% admite (`ok`); 95% segura em `account_quota`
(`janela weekly já em 95%, quota.hard_cap_percent = 90`). Sem mudança de código.
