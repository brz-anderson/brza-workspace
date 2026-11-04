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

## A entrevista da fase 1

- **Terreno** levantado por um `collector` no `brza-studio@8f41dd56a33`, com o agregado no scratch da sessão. O achado
  que mudou o plano: o `#37774` toca só `mobile/`, `src/renderer/src/components/native-chat/` e `src/shared/`, e limpa
  o rascunho do chat de terminal; o `brza chat send` fala com o host estruturado e não passa por ele. Conferido nesta
  sessão pelo `gh api`. Também conferido aqui: o host lê a origem do coordenador no `agentSession.send`
  (`structured-agent-session-send-compatibility.ts:10`), e a CLI só a manda em `agent.launch` (`src/cli/runtime/client.ts:58`).
- **R5**, as quatro na recomendada: o `#37774` sai da fase 1 e chega no sync, reabrindo essa parte da R4.3; a base é o
  porte do `#33115` estendido; cursor inválido sai com erro e a página `tail`; o motivo da fila vem de um `history tail`
  depois de enfileirar.
- **R6**, as quatro na recomendada: código de saída por estado (0, 1, 3), `--operation-id` para o retry, o contrato
  inferido lendo o `fence` e a prova por unidade mais o caso C1 no app.
- A issue da fase 1 deixou de pedir o porte do `#37774`.

## O que ficou aberto

- O Desenho e os Passos da fase 1, e então a entrevista da fase 2.
- A issue de origem passa a `done` pelo `playground`, que lê estas pelo git.
