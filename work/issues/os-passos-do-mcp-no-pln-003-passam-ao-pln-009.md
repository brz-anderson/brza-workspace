---
status: open
description: Os P6 a P9 do PLN-003 repetem os P1 a P5 do PLN-009; a sessão do PLN-003 os marca como passados ao PLN-009, liga o P10 a ele e reabre a R5.3 para o código do MCP no brza-workflow.
scope:
  - workspace
opened: 2026-11-03
priority: high
tags:
  - planning
---

# Os passos do MCP no PLN-003 passam ao PLN-009

Ao retomar o [PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md),
em 2026-11-03, a sessão do `tools-kit` achou o mesmo trabalho em dois planos: os P6 a P9 do
[PLN-003: O workflow do workspace roda igual no BrzA Studio e no Orca, por plugins e pelo `brza`](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md)
(o servidor, a fila e os tetos, a política e os gates, o desempatador) e os P1 a P5 do PLN-009. O PLN-003 não aponta
para o PLN-009.

A PLN-009/R1, respondida em 2026-11-03 na sessão do `tools-kit`, fechou dois pontos:

- **R1.1, "brza-workflow (Recomendado)":** o código do MCP mora em `~/Projects/brza-workflow/packages/mcp/`, e não no
  repositório `brz-anderson/brza` da PLN-003/R5.3, que não existe; isso reabre a R5.3 para o código do MCP.
- **R1.2, "PLN-009 (Recomendado)":** o PLN-009 é o dono do trabalho do MCP.

## O pedido à sessão do PLN-003

Esta sessão não editou o PLN-003, que estava em edição pela sessão do P0 no mesmo worktree. Cabe à sessão que conduz o
PLN-003:

1. marcar os P6, P7, P8 e P9 como `[-]`, com "→ PLN-009" e o link, e tirar as horas deles do `remaining_h`;
2. apontar as linhas da Cobertura do `Pedido 4` e do `Pedido 5` que citam P6 e P7 para o PLN-009;
3. registrar no P10 (os botões pelo MCP, R10.3) a dependência do PLN-009/P3;
4. gravar na Entrevista a R5.3 com "→ reaberta em PLN-009/R1.1" para o código do MCP, e conferir se o P3 (o repositório
   público) segue valendo para o resto — a CLI e os plugins;
5. marcar no Desenho do PLN-003 que o M6, o M7, o M13, o M14 e a R6.4 passaram ao PLN-009 (PLN-009/R2.1, D6 e P5),
   e que o D4 a D6 de lá são substituídos pelo D1 a D6 do PLN-009;
6. no PLN-003/P4, montar o `.mcp.json` do plugin com `"type": "http"`, a URL do `brza mcp url` e
   `"Authorization": "Bearer ${BRZA_MCP_TOKEN}"` (PLN-009/D1; a porta é a chave `[mcp] port` do `brza.toml`, R2.2), e
   os headers `"X-Brza-Session": "${ORCA_AGENT_SESSION_ID}"` e `"X-Brza-Client": "${ORCA_USER_DATA_PATH}"` (PLN-009/D3,
   R4.3), de que o MCP tira a sessão chamadora e o client.

Os ajustes do P0 que tocam o MCP já estão no Desenho do PLN-009, desde a reescrita da R2 (2026-11-03).
