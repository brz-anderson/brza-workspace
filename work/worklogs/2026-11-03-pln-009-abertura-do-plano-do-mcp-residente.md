---
scope:
  - workspace
  - brza-studio
refs:
  - PLN-003
  - PLN-009
---

# O PLN-009: abertura do plano do MCP residente

A pedido de Anderson ("crie um plano só pro `MCP`"), o componente MCP do PLN-003 foi destacado em um plano próprio, o
[PLN-009](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md).

## O que se fez

- **Reserva do plano:** número `PLN-009` reservado no índice da master pelo `brza note plan-open`.
- **Escopo e Desenho:** o plano concentra os itens D1 a D5 que cobrem o servidor HTTP residente em Python stdlib, a fila
  de prioridade SQLite com ordenação e os três tetos de concorrência, o protocolo MCP de despacho com gates de
  aprovação, a política declarativa com o modelo `tev1:4b` e fallback Haiku, e a telemetria de roteamento.
- **Passos:** estruturados em P1 a P5, com estimativa total de 22.5 h.

## Retomar

Apresentar o [PLN-009](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md) a Anderson para aprovação da
execução.
