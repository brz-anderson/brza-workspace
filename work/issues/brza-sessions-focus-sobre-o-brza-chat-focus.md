---
status: open
description: O brza sessions ganha o focus, que traz à frente o chat aberto pelo nome, sobre o brza chat focus do Studio.
scope:
  - brza-workflow
priority: medium
opened: 2026-11-03
tags:
  - chat
  - tooling
---

# O `brza sessions focus` traz à frente o chat pelo nome

Fase `medium` do
[PLN-010: O `brza sessions` lê e envia pelo `brza chat` do Studio, com recibo fiel](../../plans/PLN-010-brza-sessions-sobre-o-brza-chat/PLN-010-plan.md),
escolhida por Anderson na R1.1, em 2026-11-03. Vem da frente de navegação da issue
[Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md)
(`stablyai/orca#37801`).

## O que se quer

`brza sessions focus <nome>` resolve o nome pelo mapa de sessões e chama o `brza chat focus <chat>` do Studio, como os
outros aliases do PLN-010. Hoje os verbos são `open/list/send/title/close` (`brza-workflow`,
`packages/client/bin/brza-sessions:68`), e não há como trazer à frente um chat pelo nome.

## Depende de

O `brza chat focus` no `brza-studio`, da frente de navegação do `PLN-011`, no workstream `studio`.
