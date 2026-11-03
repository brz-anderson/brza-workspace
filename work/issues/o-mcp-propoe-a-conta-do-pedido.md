---
status: open
description: O MCP do PLN-009 tem o choose_account e não o chama; falta decidir se ele propõe a conta do pedido sem conta, passando pelo gate da troca de conta, ou se fica na conta ativa.
scope:
  - workspace
opened: 2026-11-03
priority: low
tags:
  - tooling
---

# O MCP propõe a conta do pedido

Na revisão do P4 do [PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md),
em 2026-11-03, o Opus achou que o `choose_account` do `resolver.py` não tem chamador (O-A8 do P4): a regra de conta da
medição do M11 existe, e nada a usa. Pela PLN-009/R4.3, o que cabia no passo foi corrigido ali — a regra passou a usar o
mesmo cálculo do `Limits` —, e o pedido sem `account` conta como a conta ativa.

## O que falta decidir

Se o MCP propõe a conta do pedido que chega sem uma, escolhendo a menos cheia pelo `choose_account`. Trocar a conta passa
pelo gate da PLN-003/R5.2, então a proposta vira um gate a cada pedido que não cair na ativa. As saídas óbvias:

- o MCP propõe e a sessão principal aprova, como em qualquer troca de conta;
- o MCP propõe só quando a ativa está segurada pela cota, e o resto fica na ativa;
- o MCP nunca propõe, e o `choose_account` sai do código.

O gatilho é o primeiro choque de cota entre as duas contas Claude, que a R7.1 do PLN-003 dá como o momento em que o
semáforo por conta se paga.
