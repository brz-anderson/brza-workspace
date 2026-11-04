---
status: open
description: O brza quota do MCP lê o uso por conta pelo account usage do app, quando o Studio portar o #37467.
scope:
  - brza-workflow
priority: low
opened: 2026-11-03
tags:
  - tooling
---

# O `brza quota` lê o uso por conta pelo `account usage` do app

Fase `low` do
[PLN-010: O `brza sessions` lê e envia pelo `brza chat` do Studio, com recibo fiel](../../plans/PLN-010-brza-sessions-sobre-o-brza-chat/PLN-010-plan.md),
escolhida por Anderson na R1.1, em 2026-11-03. Vem da frente `account usage` da issue
[Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md)
(`stablyai/orca#37467`).

## O que se quer

O MCP do
`PLN-009`
mostra o uso por conta pelo `brza quota` (`PLN-009-plan.md:65`), com fonte própria. Com o `account usage` do app, o
`brza quota` passa a ler a mesma fonte que o Studio mostra.

## Depende de

O porte do `#37467` no `brza-studio`, frente `low` do `PLN-011`, no workstream `studio`, que espera a integração no
upstream.
