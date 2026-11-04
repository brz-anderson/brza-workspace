---
status: open
description: A API de plugins do brza-studio passa a incluir as sessões de Native Chat em agents.list e agent.status.changed, com superfície, sessionId e modelo, e o caminho do worktree em workspace.readContext.
scope:
  - brza-studio
priority: low
opened: 2026-11-03
tags:
  - chat
  - tooling
---

# Os plugins enxergam as sessões de Native Chat

Frente `low` da issue de origem
[Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md),
do `playground`. Conduzida pelo
[PLN-011: Os chats do BrzA Studio se coordenam pela CLI, aparecem na navegação e chegam aos plugins](../../plans/PLN-011-chats-pela-cli-e-plugins/PLN-011-plan.md),
na fase dela.

## O recorte

- **`agents.list`:** as sessões de Native Chat entram com um discriminador de superfície (`chat` ou `terminal`), o
  `sessionId` e o modelo em uso.
- **`agent.status.changed`:** emitido também para as sessões de Native Chat.
- **`workspace.readContext`:** com o caminho do worktree no disco, o que muda o contrato público.

## As fontes do upstream

- **[`stablyai/orca#37615`](https://github.com/stablyai/orca/issues/37615)** — na `1.4.246`, o host monta `agents.list`
  e emite `agent.status.changed` só a partir de `listWorktreeTerminals` e `listAgentStatuses`. Aberta, sem PR.

## O que o `brza-studio` já tem

Do levantamento da issue de origem, no `brza-studio@8f41dd56a33`:

- o hook server já ingere status estruturados (`src/main/agent-hooks/server/server-ingest-structured.ts:147-169`) e os
  põe no snapshot (`server-listeners.ts:216-217`);
- a projeção de `agents.list` admite linha sem terminal, mas omite identidade de sessão, superfície e modelo
  (`src/main/plugins/workers/plugin-workspace-projection.ts:74-93`);
- o contexto omite os caminhos de propósito (`plugin-workspace-projection.ts:45-60`): pôr o caminho em
  `workspace.readContext` é decisão de contrato, que vai à rodada da fase. A issue
  [O worker de plugin sem sandbox alcança o token do runtime](o-worker-de-plugin-sem-sandbox-alcanca-o-token-do-runtime.md)
  pesa nessa rodada.

## O que fecha

O Native Chat em `agents.list` e `agent.status.changed`, e a resposta da rodada sobre o caminho em
`workspace.readContext`. O como fica no PLN-011.
