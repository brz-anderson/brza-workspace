---
status: open
description: Os plugins do brza-workflow passam a ver as sessões de Native Chat no agents.list, quando o Studio as expuser.
scope:
  - brza-workflow
priority: low
opened: 2026-11-03
tags:
  - chat
  - tooling
---

# Os plugins do workflow veem o Native Chat no `agents.list`

Fase `low` do
[PLN-010: O `brza sessions` lê e envia pelo `brza chat` do Studio, com recibo fiel](../../plans/PLN-010-brza-sessions-sobre-o-brza-chat/PLN-010-plan.md),
escolhida por Anderson na R1.1, em 2026-11-03. Vem da frente de plugins da issue
[Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md)
(`stablyai/orca#37615`).

## O que se quer

Os plugins do workflow, do
o `PLN-003`,
leem o `agents.list` para escolher onde o worker roda (`PLN-003-interview.md:387-388`) e hoje só enxergam terminais.
Com o Native Chat no `agents.list`, com a superfície, o `sessionId` e o modelo, eles passam a enxergar os chats.

## Depende de

A frente de plugins do `PLN-011`, no workstream `studio`: o Native Chat em `agents.list` e `agent.status.changed`.
