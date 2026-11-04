---
status: open
description: Com o login, o rateLimits.grok do app sai sem janela, e o MCP admite o worker Grok sem cota lida, só pelo teto de sessões.
scope:
  - brza-studio
  - brza-workflow
opened: 2026-11-03
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

## O que falta

1. Saber por que o Grok não reporta o percentual: o plano da conta, a API que o fetcher consulta, ou o fetcher.
2. Com a cota lida, o MCP passa a segurar o worker Grok pelas janelas de topo, como os outros (PLN-013/R3.2), sem
   mudança no desenho.
