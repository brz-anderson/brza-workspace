---
status: open
description: O dispatch do MCP aceita um caller que não é sessão do Studio, abre o gate e pede a aprovação, e só falha depois dela, no run-create; ele deveria recusar antes do gate.
scope:
  - workspace
opened: 2026-11-03
priority: low
tags:
  - tooling
---

# O dispatch aceita chamador fora do Studio

No teste do MCP do [PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md),
em 2026-11-03, com o `brza-workflow@007383a`, Anderson chamou o `dispatch` de uma sessão do Claude Code aberta no
terminal, com o servidor ligado por `--mcp-config` e sem o header `X-Brza-Session`. O pedido 1 da fila
`~/.brza/orchestrator.db` fez este caminho:

1. Às 21:01:51, o `dispatch` entrou com o `caller` vindo do argumento (`tools-kit-mcp-teste`, o nome da sessão), porque
   o header faltava (`packages/mcp/brza_mcp/tools.py:176`). O papel era `collector`.
2. O gate abriu, porque `collector` não é `consultant`, e foi aprovado às 21:02:11.
3. O `orca orchestration run-create`, com `ORCA_AGENT_SESSION_ID=tools-kit-mcp-teste` (`cycle.py:115`), voltou
   `session_caller_unknown`: "No BrzA Studio agent session tools-kit-mcp-teste exists on this host. No effects were
   applied." O pedido ficou `failed`.

O erro é claro e não teve efeito, mas chega depois de quem pediu aprovar um gate que nunca poderia virar worker.

## O que falta

Recusar o `dispatch` antes do gate quando o chamador não é uma sessão do cliente. O caminho fica para quem corrigir:
exigir o `X-Brza-Session` no `dispatch`, ou conferir a sessão no Studio antes de abrir o gate.

O gatilho é o primeiro client fora do Studio que chame o `dispatch`, como a sessão do terminal deste teste.
