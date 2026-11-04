---
status: open
description: O brza-studio ganha brza chat list/read/send, com leitura por cursor, a fila do queue-if-active à vista e recibos fiéis, depois do porte do #37774, para que uma sessão encaminhe trabalho a um chat aberto e acompanhe a resposta.
scope:
  - brza-studio
priority: high
opened: 2026-11-03
tags:
  - chat
  - tooling
---

# O `brza chat list/read/send` coordena chats abertos no BrzA Studio

Frente `high` da issue de origem
[Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md),
do `playground`. Conduzida pelo
[PLN-011: Os chats do BrzA Studio se coordenam pela CLI, aparecem na navegação e chegam aos plugins](../../plans/PLN-011-chats-pela-cli-e-plugins/PLN-011-plan.md),
na fase dela. O `brza sessions` do `brza-workflow`, que consome esta CLI, tem plano próprio no `tools-kit`, dependente
deste.

## O recorte

- **`brza chat list`:** as sessões de Native Chat abertas, com o id que `read` e `send` aceitam.
- **`brza chat read`:** o histórico de um chat, com **leitura incremental por cursor** e tratamento de cursor inválido.
- **`brza chat send`:** o envio a um chat aberto, **preservando o `queue-if-active`** e dizendo no resultado que a
  mensagem foi enfileirada, inclusive quando uma pergunta pendente retém a fila; o recibo distingue recusa, fila e
  submissão `pending`, `accepted`, `rejected` ou `unknown`, e o retry não promete resolver o `unknown`.
- **Antes do `send`:** o porte do `#37774`, que isola os rascunhos do terminal dos envios de chat.

As três primeiras saíram das rodadas de 2026-11-03 na sessão "Plano: chat via CLI e plugins" do `playground`, citadas na
issue de origem: foco "Coordenação entre sessões (Recomendado)", acompanhamento por cursor e envio que preserva o
`queue-if-active`.

## As fontes do upstream

- **[`stablyai/orca#33114`](https://github.com/stablyai/orca/issues/33114)** — o pedido de `chat list/read/send`,
  aberto no upstream em 2026-10-24.
- **[`stablyai/orca#33115`](https://github.com/stablyai/orca/pull/33115)** — o PR aberto que implementa os três
  comandos: 11 arquivos, +761/−4, todos os 7 modificados presentes no `brza-studio@8f41dd56a33`. Não traz `focus`,
  `wait`, `read --since` nem envio condicionado à ociosidade, e os recibos dele não comprovam conclusão da tarefa.
- **[`stablyai/orca#37774`](https://github.com/stablyai/orca/pull/37774)** — "fix(chat): isolate sends from terminal
  drafts", integrado em 2026-11-03 18:28 UTC (`14819eb8c04`): 44 arquivos, +2266/−627, os 42 modificados presentes no
  `brza-studio@8f41dd56a33`, que ainda não o tem.

## O que o `brza-studio` já tem

O levantamento da issue de origem, no `brza-studio@8f41dd56a33`, com `arquivo:linha`, vale aqui e não se repete; os
pontos que pesam no recorte:

- o histórico e a assinatura incremental já existem no RPC, com permissão `workspace`
  (`src/main/runtime/rpc/methods/structured-agent-session.ts:195-225`);
- o resultado do envio distingue fila de submissão (`src/shared/agent-session/agent-session-wire.ts:317-332`), e o
  `unknown` não é envio nem falha confirmada (`src/shared/agent-session/journal/agent-session-journal-types.ts:396-411`);
- a fila tem o contrato `agent-session.queued-messages.v2`
  (`src/shared/rpc-contract/structured-agent-session-params.ts:113`), e o host atual ignora `expectedRuntimeFence` na
  admissão (`src/shared/agent-session/lifecycle/agent-session-mutation-envelope.ts:66`);
- o cliente da CLI não encaminha a origem do coordenador em `agentSession.send` (`src/cli/runtime/client.ts:134-142`),
  e o wrapper `brza sessions` a encaminha; a CLI nova precisa preservá-la.

## O que fecha

O `brza chat list/read/send` no `brza-studio`, com testes, e o `#37774` portado antes do `send`. O como fica no
PLN-011.
