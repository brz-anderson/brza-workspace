---
status: open
phase: interview
origin: issue
origin_ref: brza-chat-list-read-send-no-studio
description: O brza-studio ganha brza chat list/read/send com cursor, fila e recibos, a navegação de chats pela CLI, pela barra lateral e pela Jump Palette, a limpeza do journal fora do thread principal, o Native Chat na API de plugins e o account usage, em fases por prioridade.
ready: "não — a entrevista da fase 1 (coordenação) não fechou, e o Desenho e os Passos dependem dela"
priority: high
scope:
  - brza-studio
opened: 2026-11-03
owner: Anderson
tags:
  - chat
  - tooling
---

# PLN-011: Os chats do BrzA Studio se coordenam pela CLI, aparecem na navegação e chegam aos plugins

- **Retomar:** aberto em 2026-11-03, com as cinco issues das frentes e as rodadas do `playground` gravadas como R1 a R4;
  o próximo passo é a rodada R5, da fase 1 (coordenação), depois do levantamento do Terreno dela.

## Pedido

- **Origem:** [O `brza chat list/read/send` coordena chats abertos no BrzA Studio](../../work/issues/brza-chat-list-read-send-no-studio.md),
  com as outras frentes em
  [O chat ativo se escolhe pela CLI e aparece na barra lateral e na Jump Palette](../../work/issues/chat-ativo-pela-cli-na-barra-lateral-e-na-jump-palette.md),
  [A limpeza do journal de chats sai do thread principal](../../work/issues/limpeza-do-journal-de-chats-fora-do-thread-principal.md),
  [Os plugins enxergam as sessões de Native Chat](../../work/issues/native-chat-na-api-de-plugins.md) e
  [O `brza account usage` mostra o uso dos limites por conta](../../work/issues/brza-account-usage-na-cli.md); todas
  nascem da issue do `playground`
  [Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](../../work/issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md).

Pedido de 2026-11-03, da sessão "Plano: chat via CLI e plugins" do `playground`:

> abra o plano do workstream `studio` para a coordenação, a navegação e a exposição de chats pela CLI e aos plugins, a
> partir da issue de origem do `playground`.

E o pedido da issue de origem, em "O que fazer":

> Implementar `brza chat list/read/send/focus`, incluir Native Chat na Jump Palette e na seleção da barra lateral, e
> expor Native Chat em `agents.list` no `brza-studio`, alinhando com as necessidades do `brza-workflow`.

### Fases

Na ordem da prioridade, como decidido em R4.2 e R4.3; cada fase fecha a issue dela.

| Fase | Prioridade | Frente | Issue |
| :--- | :--------- | :----- | :---- |
| 1 | `high` | Coordenação: o porte do `#37774`, e então `brza chat list/read/send` com cursor, fila e recibos | [O `brza chat list/read/send` coordena chats abertos no BrzA Studio](../../work/issues/brza-chat-list-read-send-no-studio.md) |
| 2 | `medium` | Navegação: `brza chat focus`, a seleção da barra lateral e a Jump Palette | [O chat ativo se escolhe pela CLI e aparece na barra lateral e na Jump Palette](../../work/issues/chat-ativo-pela-cli-na-barra-lateral-e-na-jump-palette.md) |
| 3 | `medium` | Journal: a limpeza do SQLite fora do thread principal, depois da integração do `#37802` no upstream | [A limpeza do journal de chats sai do thread principal](../../work/issues/limpeza-do-journal-de-chats-fora-do-thread-principal.md) |
| 4 | `low` | Plugins: Native Chat em `agents.list` e `agent.status.changed`, e o caminho em `workspace.readContext` | [Os plugins enxergam as sessões de Native Chat](../../work/issues/native-chat-na-api-de-plugins.md) |
| 5 | `low` | `brza account usage` | [O `brza account usage` mostra o uso dos limites por conta](../../work/issues/brza-account-usage-na-cli.md) |

### Cobertura

Os critérios de aceite saem das rodadas de cada fase; os passos, do Desenho. Até lá, cada linha diz o que a fase prova.

| Origem | Critério de aceite | Passo | Teste (nível) |
| :----- | :----------------- | :---- | :------------ |
| Fase 1, R2.1 | `brza chat read` lê o histórico a partir de um cursor e trata o cursor inválido | a planejar | a definir na rodada |
| Fase 1, R2.2 | `brza chat send` preserva o `queue-if-active` e diz que a mensagem foi enfileirada, inclusive com pergunta pendente retendo a fila | a planejar | a definir na rodada |
| Fase 1, R4.3 | o `#37774` está no `brza-studio` antes do `send` | a planejar | a definir na rodada |
| Fase 2 | `brza chat focus`, a barra lateral e a Jump Palette seguem o chat ativo | a planejar | a definir na rodada |
| Fase 3 | a limpeza do journal não roda no thread principal | a planejar | a definir na rodada |
| Fase 4 | um plugin vê as sessões de Native Chat em `agents.list` e `agent.status.changed` | a planejar | a definir na rodada |
| Fase 5 | `brza account usage` imprime o uso por conta | a planejar | a definir na rodada |

### Fora de escopo

- **O `brza sessions` do `brza-workflow` sobre a CLI nova** — os aliases, o retry e o resultado fiel do envio no
  wrapper. Vão ao plano do `tools-kit`, com `depends_on` neste, como decidido em R4.1.

## Pré-requisitos

- **Fase 3:** o `stablyai/orca#37802` integrado no upstream (`gh api repos/stablyai/orca/pulls/37802 --jq .merged_at`
  diferente de `null`). Sem isso, a fase espera, como decidido em R4.3.

## Entrevista

As rodadas R1 a R4 foram respondidas por Anderson em 2026-11-03, na sessão "Plano: chat via CLI e plugins" do
`playground`, e estão gravadas na issue de origem com o que foi apresentado antes; entram aqui com a resposta literal,
sem perguntar de novo. As opções sem preço registrado na origem ficam sem preço aqui.

### Rodada 1 — o foco (enviada 2026-11-03, no `playground`)

> **Apresentado antes:** o aprofundamento verificado da issue de origem, no `brza-studio@8f41dd56a33` e no
> `brza-workflow`.

Respondida em 2026-11-03.

1. **Foco do detalhamento.** **Decidido:** "Coordenação entre sessões (Recomendado). Custo: adaptar list/read/send à
   CLI e integrar nomes, recibos e retry ao wrapper existente. Se paga: ao encaminhar trabalho para chats já abertos e
   acompanhar suas respostas."

### Rodada 2 — acompanhamento e envio (enviada 2026-11-03, no `playground`)

> **Apresentado antes:** as restrições do contrato — o `AgentSessionSendResult` que distingue fila de submissão, o
> `unknown` que não é envio nem falha, o replay que não resolve o `unknown`, e o cliente da CLI que não encaminha a
> origem do coordenador em `agentSession.send`.

Respondida em 2026-11-03.

1. **Acompanhamento.** **Decidido:** leitura incremental por cursor, com tratamento de cursor inválido.
2. **Envio durante atividade.** **Decidido:** preservar `queue-if-active` e expor que a mensagem está enfileirada,
   inclusive quando uma pergunta pendente retém a fila.

### Rodada 3 — abertura do plano (enviada 2026-11-03, no `playground`)

> **Apresentado antes:** o recorte já respondido (coordenação por cursor e fila, aliases de `brza sessions`, recibos e
> retry) e as frentes fora dele (focus e barra lateral, Jump Palette, robustez do journal, plugins, `account usage`).

Respondida em 2026-11-03.

1. **Destino.** Opções: `PLN` em `plans/` (recomendado); seção num worklog. **Resposta:** "um plano pra cada
   `workstream` e elas se coordenam na execução" — vai à R4.1.
2. **Recorte.** Opções: só a coordenação (recomendado); coordenação + `chat focus`; a issue inteira, por fases.
   **Resposta:** "A issue inteira, por fases".
3. **Restante.** Opções: fica na issue de origem (recomendado); vira issues próprias. **Resposta:** "issues próprias,
   repriorize individualmente" — vai à R4.2 e à R4.3.

### Rodada 4 — esclarecimento do plano (enviada 2026-11-03, no `playground`)

> **Apresentado antes:** a leitura das respostas em texto livre da R3 — `studio` para o código do `brza-studio` e
> `tools-kit` para o `brza sessions` — e o estado no upstream: `#37774` integrado em 2026-11-03 18:28 UTC e ausente do
> checkout local `8f41dd56a33`, `#37802` e `#37467` abertos.

Respondida em 2026-11-03.

1. **Workstreams.** **Decidido:** "studio + tools-kit (Recomendado)". Um `PLN` no `studio` e outro no `tools-kit`,
   este com `depends_on` no do `studio`, cada um aberto por sessão nova no worktree dele.
2. **Fases.** **Decidido:** "Todas as frentes, por prioridade (Recomendado)". Cada frente vira issue com prioridade
   própria; os planos cobrem todas, em fases na ordem da prioridade, cada fase citando a issue dela.
3. **Prioridades.** **Decidido:** "Proposta abaixo (Recomendado)". `high`: coordenação (`list/read/send`) e o porte do
   `#37774` antes do `send`. `medium`: navegação (`focus`, barra lateral, Jump Palette) e o journal do `#37802`, que
   espera a integração no upstream. `low`: plugins e `account usage` (`#37467`).
4. **Issues.** **Decidido:** "No workstream da frente (Recomendado)". A sessão que abre o plano cria as issues dele.

## Worklogs

- 2026-11-03 — abertura: as cinco issues das frentes, o PLN-011 com as fases e as R1 a R4 do `playground`.
  [PLN-011: abertura do plano dos chats pela CLI e pelos plugins](../../work/worklogs/2026-11-03-pln-011-abertura-chats-pela-cli-e-plugins.md)

## Fechamento

- [ ] Todo passo `[x]` com evidência, ou `[-]` com motivo.
- [ ] Todo achado com destino que existe.
- [ ] Um resumo por commit ou PR do `brza-studio` da entrega, com o link do plano: os achados e o destino de cada um.
- [ ] O durável saiu para a casa dona e está em `## Decisões` e `## Documentação`.
- [ ] As decisões que o plano respondeu estão `done`, citando a rodada.
- [ ] As cinco issues das fases estão `done`, com `completed`.
- [ ] `status: done`, `phase: closed` e `completed` no frontmatter.
