---
scope:
  - tools-kit
  - brza-workflow
tags:
  - chat
  - tooling
refs:
  - PLN-010
  - PLN-011
  - issue:brza-sessions-focus-sobre-o-brza-chat-focus
  - issue:brza-sessions-sobre-o-brza-chat
  - issue:ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins
  - issue:o-brza-quota-le-o-account-usage-do-app
  - issue:os-plugins-do-workflow-veem-o-native-chat
---

# O PLN-010: a abertura do `brza sessions` sobre o `brza chat`

Pedido da sessão "Plano: chat via CLI e plugins" do `playground`, em 2026-11-03: abrir no `tools-kit` o plano da frente
do `brza-workflow` da issue
[Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](../issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md),
e seguir para a entrevista. Nenhum código.

## O que se fez

- **A issue da frente:**
  [O `brza sessions` lê e envia pelo `brza chat` do Studio, com recibo fiel](../issues/brza-sessions-sobre-o-brza-chat.md),
  `priority: high`, com as linhas do `brza-workflow@7a18392` conferidas: o `sent: true` em `brza-sessions:283-287`, o
  resultado descartado em `brza_runtime.py:141-145`, o `ok` externo em `:115-117` e a origem em `:95-97`.
- **O plano:** [PLN-010: O `brza sessions` lê e envia pelo `brza chat` do Studio, com recibo fiel](../../plans/PLN-010-brza-sessions-sobre-o-brza-chat/PLN-010-plan.md),
  reservado pelo `brza note plan-open`, em `phase: interview`, com as respostas do `playground` na R0.
- **O `depends_on` ficou de fora.** O `PLN-011`, do `studio` (slug `chats-pela-cli-e-plugins`), foi reservado às
  21:19 no índice da `origin/master`, mas o arquivo ainda não estava em nenhuma branch, e o `brza note commit` recusou
  (`depends-on-not-found`). A dependência fica nos Pré-requisitos e no `Retomar` até ele aparecer.

- **A Rodada 1**, respondida nesta sessão: as fases 2 a 4 (`focus`, Native Chat nos plugins, `account usage` no MCP),
  os três chamadores do `send_to_chat` no recibo, o cursor com quem chama e a falha sem o `brza chat`. As fases
  ganharam issue cada uma (R0.7):
  [O `brza sessions focus` traz à frente o chat pelo nome](../issues/brza-sessions-focus-sobre-o-brza-chat-focus.md),
  [Os plugins do workflow veem o Native Chat no `agents.list`](../issues/os-plugins-do-workflow-veem-o-native-chat.md) e
  [O `brza quota` lê o uso por conta pelo `account usage` do app](../issues/o-brza-quota-le-o-account-usage-do-app.md).

## O que ficou aberto

- A Rodada 2, e o `depends_on: [PLN-011]` quando o `studio` commitar o plano.
