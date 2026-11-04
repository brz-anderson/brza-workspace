---
status: open
phase: interview
origin: issue
origin_ref: brza-sessions-sobre-o-brza-chat
description: O brza sessions passa a ser alias do brza chat do Studio, com leitura por cursor, recibo fiel do envio, retry seguro e a origem do coordenador preservada
ready: "não — faltam a Rodada 1 e o contrato do brza chat do PLN-011, no studio; isso trava o Desenho"
scope:
  - brza-workflow
opened: 2026-11-03
owner: Anderson
priority: high
tags:
  - chat
  - tooling
---

# PLN-010: O `brza sessions` lê e envia pelo `brza chat` do Studio, com recibo fiel

- **Retomar:** aberto em 2026-11-03, com a issue e as rodadas do `playground` transcritas na R0. Próximo: a Rodada 1 —
  as fases deste plano, os chamadores do recibo, onde mora o cursor e o caminho sem o `brza chat`. Falta o
  `depends_on: [PLN-011]`, que o checador recusa até o `studio` commitar o plano reservado.

## Pedido

- **Origem:** [O `brza sessions` lê e envia pelo `brza chat` do Studio, com recibo fiel](../../work/issues/brza-sessions-sobre-o-brza-chat.md),
  frente do `brza-workflow` da issue
  [Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](../../work/issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md),
  do workstream `playground`, pelo pedido da sessão "Plano: chat via CLI e plugins" de 2026-11-03.

"os aliases de `brza sessions` sobre o `brza chat` do Studio, a leitura por cursor, o recibo fiel do envio (hoje o
`sent: true` de `brza-sessions:283-287` e o resultado descartado em `brza_runtime.py:141-145`), o retry seguro sem
prometer resolver `unknown`, e a origem do coordenador preservada (`orchestrationCompatibilityEvidence`)." — o pedido de
abertura, de 2026-11-03.

1. Os aliases de `brza sessions` sobre o `brza chat` do Studio.
2. A leitura incremental por cursor, com tratamento de cursor inválido.
3. O recibo fiel do envio, preservando o `queue-if-active` e expondo a fila, também quando uma pergunta pendente a
   retém.
4. O retry seguro, sem prometer resolver o `unknown`.
5. A origem do coordenador preservada (`orchestrationCompatibilityEvidence`).

### Cobertura

Rascunho da abertura; o critério de aceite de cada linha é proposta até a rodada que o confirma.

| Origem     | Critério de aceite                                                                                                     | Passo | Teste (nível)                         |
| :--------- | :--------------------------------------------------------------------------------------------------------------------- | :---- | :------------------------------------ |
| `Pedido 1` | `brza sessions list/read/send <nome>` resolve o nome pelo mapa e chama o `brza chat` do Studio com o id do chat         | —     | `test_brza_sessions` (unidade)        |
| `Pedido 2` | `read` devolve só o que veio depois do cursor e o cursor seguinte; cursor inválido sai com erro próprio, sem reler tudo | —     | `test_brza_sessions` (unidade)        |
| `Pedido 3` | `send` imprime o recibo que o Studio devolveu — enfileirada ou submetida, com `accepted`, `rejected`, `pending` ou `unknown` —, nunca `sent: true` por conta própria | — | `test_brza_sessions` (unidade); envio a chat ocupado (manual) |
| `Pedido 4` | repetir o envio com a mesma operação não dispara de novo, e o `unknown` sai como `unknown`                            | —     | `test_brza_sessions` (unidade)        |
| `Pedido 5` | o envio feito de dentro de um chat chega ao destino como tarefa do coordenador, não como a mensagem da pessoa          | —     | `test_brza_sessions` (unidade); conferência no app (manual) |

### Fora de escopo

- **O `brza chat list/read/send` no `brza-studio`**, o contrato dele e o porte do `#37774`. Do `PLN-011`, no workstream
  `studio`.
- **A navegação (`focus`, barra lateral, Jump Palette), o journal do `#37802`, os plugins e o `account usage`
  (`#37467`)** no `brza-studio`. Do mesmo `PLN-011`, por prioridade; o que deles couber ao `brza-workflow` é a
  R1.1.

## Pré-requisitos

- **O `brza chat` do Studio, com a forma que o `PLN-011` decidir.** Assinatura a conferir no build:
  `brza chat list --json`, `brza chat read <chat> --since <cursor> --json` com o cursor seguinte na saída, e
  `brza chat send <chat> <texto> --json` com o recibo do `AgentSessionSendResult` e a operação que se repete. Falta:
  o Desenho daqui para nos itens que dependem dele, e o `ready` fica `não`.
- **O envio leva a origem do coordenador.** O `brza chat send` aceita o chat de origem (o `ORCA_AGENT_SESSION_ID`), ou o
  item do Pedido 5 fica no `rpc` do `brza_runtime`. É ponto a pedir ao `PLN-011`, não decisão daqui.

## Entrevista

### Rodada 0 — o que o `playground` já decidiu (respondida em 2026-11-03)

Respondida na sessão "Plano: chat via CLI e plugins" do `playground`, e transcrita do pedido de abertura e da
[issue de origem](../../work/issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md), sem
perguntar de novo. As opções que perderam estão lá.

1. **Foco.** **Decidido:** "Coordenação entre sessões (Recomendado)".
2. **Acompanhamento.** **Decidido:** leitura incremental por cursor, com tratamento de cursor inválido.
3. **Envio durante atividade.** **Decidido:** preservar `queue-if-active` e expor que a mensagem está enfileirada,
   inclusive quando uma pergunta pendente retém a fila.
4. **Workstreams.** **Decidido:** "studio + tools-kit (Recomendado)" — um `PLN` no `studio`, o `brza chat` no
   `brza-studio`, e este no `tools-kit`, com `depends_on` no do `studio`, o `PLN-011`.
5. **Fases.** **Decidido:** "Todas as frentes, por prioridade (Recomendado)".
6. **Prioridades.** **Decidido:** "Proposta abaixo (Recomendado)" — a coordenação (`list/read/send`) é `high`.
7. **Issues.** **Decidido:** "No workstream da frente (Recomendado)" — a sessão que abre o plano cria as issues dele.

## Worklogs

- 2026-11-03 — abertura: a issue da frente, o `PLN-010` e a R0 transcrita. Parou na Rodada 1.
  [O PLN-010: a abertura do `brza sessions` sobre o `brza chat`](../../work/worklogs/2026-11-03-pln-010-abertura-do-brza-sessions-sobre-o-brza-chat.md)
