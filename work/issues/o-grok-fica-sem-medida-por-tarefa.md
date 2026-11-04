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

- **Ainda não pesa.** O Grok entrou em 2026-11-03 (o cask `grok-build` 1.0.70), sem login: `orca account list --json` →
  `rateLimits.grok.error` "Not signed in to Grok — run grok login".
- **Há por onde ler.** A CLI grava o estado em `~/.grok` (ou no `GROK_HOME` da conta, pelo `GROK_LAUNCH_SPEC` do app
  em `brza-studio/src/main/acp/acp-launch-specs.ts:163`), tem id de sessão (`grok -s`), e o modo sem interface sai em
  JSON (`--output-format`). O app lê a cota dele (`rateLimits.grok`, em janelas `session` e `weekly`).

## O que falta

1. Saber onde o Grok grava a sessão, os tokens e o modelo, e se há um id de sessão no ambiente, como o
   `CLAUDE_CODE_SESSION_ID`, para o `brza note commit` carimbar no worklog.
2. Decidir se vale medir, quando o Grok pesar no gasto.
