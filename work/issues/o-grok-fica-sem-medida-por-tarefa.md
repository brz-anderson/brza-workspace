---
status: open
description: As sessões do Grok não passam pelo hook de medição, e as tarefas delas ficam sem tempo, custo e máquina no PLN-012.
scope:
  - brza-workflow
opened: 2026-11-03
priority: low
tags:
  - tooling
---

# O Grok fica sem medida por tarefa

## O pedido

O [PLN-013: O Grok, o Codex e o Antigravity abrem pelo `brza sessions` e recebem tarefas do MCP](../../plans/PLN-013-grok-codex-e-agy-no-brza-sessions-e-no-mcp/PLN-013-plan.md)
põe o Grok no fluxo, e o PLN-012 mede só as sessões do Claude Code, pelo `measure.py`. Na R1.4 do PLN-013, Anderson
escolheu uma issue irmã de [Codex e Antigravity ficam sem medida por tarefa](codex-e-antigravity-sem-medida-por-tarefa.md),
pela regra da R1.3 do PLN-012: "sempre abra issue para lacunas deixadas".

## O que se sabe

- **O [PLN-018](../../plans/PLN-018-o-grok-e-o-codex-na-medicao/PLN-018-plan.md) mede o turno e o carimbo.** A R1.1
  decidiu a entrega. O plano está em desenho, sem passos. O escritor ainda não entrou no `brza-workflow`.
- **Onde o Grok grava o turno.** Sonda de 2026-11-09: `usage.json` da sessão, com `turns[].turnNumber` e o
  `costUsdTicks` daquele turno. O objeto `session` acumula e não se soma. O shell de ferramenta tem `GROK_SESSION_ID`
  e não tem `CLAUDE_CODE_SESSION_ID`.
- **O "sem login" de 2026-11-03 não descreve o disco de hoje.** Um `grok agent stdio` completou um turno.

## O que falta

1. A linha e o carimbo, no PLN-018. O corte dos passos espera decisão.
