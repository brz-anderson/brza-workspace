---
status: open
description: O /rename mandado pelo chat do app chega ao Antigravity como texto e não grava nome; o chat roda em mode_id yolo e o agente executou comandos sozinho na sonda.
scope:
  - brza-studio
  - brza-workflow
opened: 2026-11-04
priority: medium
tags:
  - tooling
---

# O `/rename` pelo chat não chega ao Antigravity

## O pedido

É a sonda negativa do P8 do
[PLN-013: O Grok, o Codex e o Antigravity abrem pelo `brza sessions` e recebem tarefas do MCP](../../plans/PLN-013-grok-codex-e-agy-no-brza-sessions-e-no-mcp/PLN-013-plan.md),
pela R4.4/P6.

## O que se sabe

- **O texto vai ao modelo.** `brza sessions send pln-013-sonda8-agy "/rename pln-013-sonda8-agy-nome"`, em
  2026-11-04: o chat `antigravity_9ecfd00f…` tratou o texto como tarefa e passou a investigar, rodando `sqlite3` nos
  bancos do app (`agent-session-journal.db`, `conversations/86b3cf9a….db`) e `brza sessions list`.
- **Nenhum nome em disco.** O `.meta` da conversa `86b3cf9a-e424-4585-880e-d229d531b06e` só traz `cwd` e `mode_id`.
- **O chat roda em `mode_id: "yolo"`**, que aprova tudo sem perguntar. Foi por isso que o agente rodou comandos sem
  aprovação durante a sonda. Isso pesa mais do que o nome.
- **O `close` falhou na aba:** `brza sessions close pln-013-sonda8-agy` → `session.tabs.close: tab_not_found`, depois do
  `agentSession.close`.

## O que falta

1. Decidir se o chat do Antigravity aberto pelo `brza sessions` deve rodar em `yolo`. É do `brza-studio` e de Anderson.
2. Achar onde o Antigravity guarda o título da conversa, se guardar, para a linha `antigravity` do `NAMED`
   (PLN-013/D7).
3. Saber por que o `session.tabs.close` não achou a aba.
