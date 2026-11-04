---
status: open
description: O brza-studio ganha brza chat focus, a seleção da barra lateral que acompanha o chat ativo e os Native Chats nas recentes e na busca da Jump Palette.
scope:
  - brza-studio
priority: medium
opened: 2026-11-03
tags:
  - chat
  - tooling
---

# O chat ativo se escolhe pela CLI e aparece na barra lateral e na Jump Palette

Frente `medium` da issue de origem
[Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md),
do `playground`. Conduzida pelo
[PLN-011: Os chats do BrzA Studio se coordenam pela CLI, aparecem na navegação e chegam aos plugins](../../plans/PLN-011-chats-pela-cli-e-plugins/PLN-011-plan.md),
na fase dela, depois da coordenação de
[O `brza chat list/read/send` coordena chats abertos no BrzA Studio](brza-chat-list-read-send-no-studio.md), de quem
herda o id de chat.

## O recorte

- **`brza chat focus <id>`:** abre e foca um chat pela CLI, sem depender do RPC não documentado `terminal.reveal`.
- **A barra lateral:** o painel de agentes atualiza a seleção quando o chat ativo muda por runtime, atalho ou
  notificação.
- **A Jump Palette:** as abas `contentType: 'agent-session'` entram nas sessões recentes e na busca por título
  (`Ctrl+Shift+J` / `Cmd+P`), ao lado de arquivos e terminais.

## As fontes do upstream

- **[`stablyai/orca#37801`](https://github.com/stablyai/orca/issues/37801)** — a seleção da barra lateral que segue o
  chat ativo e o comando público para abrir um chat. Aberta, sem PR.
- **[`stablyai/orca#37807`](https://github.com/stablyai/orca/issues/37807)** — a Jump Palette exclui os Native Chats
  das recentes e da busca. Aberta, sem PR.

Os relatos são do upstream e ainda não foram conferidos no `brza-studio`: o levantamento do código vem antes do Desenho
desta fase.

## O que fecha

O `brza chat focus`, a barra lateral e a Jump Palette no `brza-studio`, com testes e a conferência no app. O como fica
no PLN-011.
