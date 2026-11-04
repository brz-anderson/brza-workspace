---
scope:
  - brza-studio
tags:
  - chat
  - planning
refs:
  - PLN-011
  - issue:brza-account-usage-na-cli
  - issue:brza-chat-list-read-send-no-studio
  - issue:chat-ativo-pela-cli-na-barra-lateral-e-na-jump-palette
  - issue:ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins
  - issue:limpeza-do-journal-de-chats-fora-do-thread-principal
  - issue:native-chat-na-api-de-plugins
---

# PLN-011: abertura do plano dos chats pela CLI e pelos plugins

Pedido da sessão "Plano: chat via CLI e plugins" do `playground`, em 2026-11-03: criar neste workstream as issues das
frentes da issue
[Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](../issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md),
abrir o plano e seguir para a entrevista. Nenhum código.

## O que se fez

- **Upstream conferido** pelo `gh api`, hoje: `#33114`, `#33115`, `#37615`, `#37801`, `#37807`, `#37467` e `#37802`
  abertos; `#37774` integrado em 2026-11-03 18:28 UTC (`14819eb8c04`). Os arquivos que `#37774`, `#33115` e `#37467`
  modificam existem todos no `brza-studio@8f41dd56a33` (42, 7 e 8 arquivos).
- **Cinco issues**, uma por frente, com `priority`, o recorte, as fontes do upstream e o link para a de origem:
  - [O `brza chat list/read/send` coordena chats abertos no BrzA Studio](../issues/brza-chat-list-read-send-no-studio.md) — `high`;
  - [O chat ativo se escolhe pela CLI e aparece na barra lateral e na Jump Palette](../issues/chat-ativo-pela-cli-na-barra-lateral-e-na-jump-palette.md) — `medium`;
  - [A limpeza do journal de chats sai do thread principal](../issues/limpeza-do-journal-de-chats-fora-do-thread-principal.md) — `medium`;
  - [Os plugins enxergam as sessões de Native Chat](../issues/native-chat-na-api-de-plugins.md) — `low`;
  - [O `brza account usage` mostra o uso dos limites por conta](../issues/brza-account-usage-na-cli.md) — `low`.
- **O plano**, pelo `brza note plan-open`:
  [PLN-011: Os chats do BrzA Studio se coordenam pela CLI, aparecem na navegação e chegam aos plugins](../../plans/PLN-011-chats-pela-cli-e-plugins/PLN-011-plan.md),
  `phase: interview`, com as cinco fases na ordem da prioridade e as rodadas do `playground` gravadas como R1 a R4.

## O que ficou aberto

- A rodada R5, da fase 1, depois do levantamento do Terreno dela.
- A issue de origem passa a `done` pelo `playground`, que lê estas pelo git.
