---
status: open
description: As linhas queued, running e finished do status do MCP não trazem o runtime, o modelo nem o esforço do pedido, e com três runtimes não se sabe qual worker é de qual.
scope:
  - brza-workflow
opened: 2026-11-04
priority: medium
tags:
  - tooling
---

# O `status` do MCP não diz o runtime do pedido

## O pedido

Achado na execução do
[PLN-013: O Grok, o Codex e o Antigravity abrem pelo `brza sessions` e recebem tarefas do MCP](../../plans/PLN-013-grok-codex-e-agy-no-brza-sessions-e-no-mcp/PLN-013-plan.md),
no P4. Anderson pediu, na R5: "não pare o plano ao encontrar problemas ou desvios no meio do caminho, registre em issue
e no worklog e siga".

## O que se sabe

- **O `dispatch` devolve o modelo e o esforço**, e a fila os grava: os pedidos 11, 12 e 13, a `codex`, `grok` e `agy`,
  voltaram com `gpt-6.1-sol`/`low`, `grok-4.7`/`low` e `gemini-4-argon-low`/`null`, em 2026-11-04, no `brza-workflow@975fe88`.
- **O `status` não os mostra.** A linha `running` do pedido 11 traz só `id`, `task`, `role`, `account`, `ref` e
  `caller`; sem `runtime`, `model` e `effort`, os três workers parecem iguais.

## O que falta

1. O `status` passa a trazer `runtime`, `model` e `effort` em cada linha, com um teste no `test_mcp_dispatch.py`.
