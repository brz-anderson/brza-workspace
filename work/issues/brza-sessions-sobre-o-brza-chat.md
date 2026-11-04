---
status: open
description: O brza sessions passa a ser alias do brza chat do Studio, com leitura por cursor, recibo fiel do envio, retry seguro e a origem do coordenador preservada.
scope:
  - brza-workflow
priority: high
opened: 2026-11-03
tags:
  - chat
  - tooling
---

# O `brza sessions` lê e envia pelo `brza chat` do Studio, com recibo fiel

Frente do `brza-workflow` da issue
[Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md),
do workstream `playground`. Lá estão o levantamento verificado e as rodadas de 2026-11-03; aqui fica só o que é do
`brza sessions`. O `brza chat list/read/send` em si é do `brza-studio`, no `PLN-011`, do workstream `studio`.

## O que falta hoje

Conferido no `brza-workflow@7a18392`:

- **O envio promete o que não sabe.** `packages/client/bin/brza-sessions:283-287` imprime `sent: true` depois do
  `send_to_chat`, e `bin/brza_runtime.py:141-145` descarta o resultado do `agentSession.send`. O `rpc` só confere o
  `ok` externo (`bin/brza_runtime.py:115-117`): a recusa interna, a fila e a submissão `pending` ou `unknown` saem
  todas como `sent: true`.
- **Não há leitura.** Os verbos são `open/list/send/title/close` (`brza-sessions:68`); a sessão que coordena não lê a
  resposta do chat de destino.
- **Cada envio é uma operação nova.** O `clientOperationId` nasce do relógio e de um `uuid4` a cada chamada
  (`brza_runtime.py:135` e `:145`), e por isso repetir o comando não é retry: é um segundo envio.
- **A origem do coordenador já vai.** O `rpc` acrescenta `orchestrationCompatibilityEvidence` com o
  `ORCA_AGENT_SESSION_ID` no `agentSession.send` (`brza_runtime.py:95-97`); sem ela, o Studio mostra a mensagem como
  a da pessoa.

## O que se quer

Decidido em 2026-11-03, na sessão "Plano: chat via CLI e plugins" do `playground`:

- **Aliases.** `brza sessions` sobre o `brza chat` do Studio: a resolução por nome do mapa de sessões continua aqui, e
  a leitura e o envio passam ao comando do Studio.
- **Leitura por cursor**, incremental, com tratamento de cursor inválido.
- **Recibo fiel do envio:** o que o Studio devolveu — enfileirada, inclusive quando uma pergunta pendente retém a fila;
  submetida e `accepted`, `rejected`, `pending` ou `unknown` —, preservando o `queue-if-active`.
- **Retry seguro:** repetir com a mesma operação não dispara de novo, e o retry não promete resolver um `unknown`.
- **A origem do coordenador preservada**, o `orchestrationCompatibilityEvidence`, quando o transporte passar ao
  comando do Studio.

## Depende de

O `brza chat list/read/send` no `brza-studio`, do `PLN-011`, no workstream `studio`
(`plans/PLN-011-chats-pela-cli-e-plugins/`). O contrato dele — o cursor, a forma do recibo, a operação reusável — é decisão daquele plano; o daqui o consome.
