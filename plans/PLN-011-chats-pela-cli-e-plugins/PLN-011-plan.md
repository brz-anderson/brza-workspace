---
status: open
phase: interview
origin: issue
origin_ref: brza-chat-list-read-send-no-studio
description: O brza-studio ganha brza chat list/read/send com cursor, fila e recibos, a navegação de chats pela CLI, pela barra lateral e pela Jump Palette, a limpeza do journal fora do thread principal, o Native Chat na API de plugins e o account usage, em fases por prioridade.
ready: "não — falta o Desenho e os Passos da fase 1, e a entrevista das fases 2 a 5"
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

- **Retomar:** em 2026-11-03, a entrevista da fase 1 fechou na R6 (base, cursor, fila, recibo, retry, contrato e
  prova); o próximo passo é o Desenho da fase 1 (os itens `D` do contrato da CLI) e os Passos dela, e depois a
  entrevista da fase 2.

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
| 1 | `high` | Coordenação: `brza chat list/read/send` com cursor, fila e recibos, pelo porte do `#33115` estendido (R5.2); o `#37774` saiu da fase em R5.1 | [O `brza chat list/read/send` coordena chats abertos no BrzA Studio](../../work/issues/brza-chat-list-read-send-no-studio.md) |
| 2 | `medium` | Navegação: `brza chat focus`, a seleção da barra lateral e a Jump Palette | [O chat ativo se escolhe pela CLI e aparece na barra lateral e na Jump Palette](../../work/issues/chat-ativo-pela-cli-na-barra-lateral-e-na-jump-palette.md) |
| 3 | `medium` | Journal: a limpeza do SQLite fora do thread principal, depois da integração do `#37802` no upstream | [A limpeza do journal de chats sai do thread principal](../../work/issues/limpeza-do-journal-de-chats-fora-do-thread-principal.md) |
| 4 | `low` | Plugins: Native Chat em `agents.list` e `agent.status.changed`, e o caminho em `workspace.readContext` | [Os plugins enxergam as sessões de Native Chat](../../work/issues/native-chat-na-api-de-plugins.md) |
| 5 | `low` | `brza account usage` | [O `brza account usage` mostra o uso dos limites por conta](../../work/issues/brza-account-usage-na-cli.md) |

### Cobertura

Os critérios de aceite saem das rodadas de cada fase; os passos, do Desenho. Até lá, cada linha diz o que a fase prova.

| Origem | Critério de aceite | Passo | Teste (nível) |
| :----- | :----------------- | :---- | :------------ |
| Fase 1, R5.2 | `brza chat list` lista as sessões de Native Chat abertas com o id que `read` e `send` aceitam | a planejar | `chat.test.ts` (unidade) |
| Fase 1, R2.1, R6.3 | `brza chat read --cursor <epoch:sequence>` devolve só o que mudou depois do cursor, e o `--json` traz `itemId`, `revision`, `sequence`, `nextCursor` e `hasNewer` | a planejar | `chat.test.ts` (unidade); C1 (manual) |
| Fase 1, R5.3 | o cursor inválido sai com código não zero e `cursor_reset: <motivo>`, com a página `tail` e o `nextCursor` novos | a planejar | `chat.test.ts`, um caso por motivo (unidade) |
| Fase 1, R2.2, R5.4 | o `send` enfileirado diz a posição, o `nextQueuedMessageId` e `held_by: question\|working` | a planejar | `chat.test.ts` (unidade); C1 (manual) |
| Fase 1, R6.1 | o código de saída do `send` é 0 em `accepted` e `queued`, 1 em recusa e `rejected`, 3 em `pending` e `unknown` | a planejar | `chat.test.ts` (unidade) |
| Fase 1, R6.2 | `send --operation-id <id>` com o mesmo texto devolve o resultado gravado sem reenviar, e o `unknown` continua `unknown` | a planejar | `chat.test.ts` (unidade) |
| Fase 1, R6.3 | o `send` leva o `ORCA_AGENT_SESSION_ID` como origem do coordenador e o `expectedRuntimeFence` lido do histórico | a planejar | `chat.test.ts` e o teste do `client.ts` (unidade) |
| Fase 2 | `brza chat focus`, a barra lateral e a Jump Palette seguem o chat ativo | a planejar | a definir na rodada |
| Fase 3 | a limpeza do journal não roda no thread principal | a planejar | a definir na rodada |
| Fase 4 | um plugin vê as sessões de Native Chat em `agents.list` e `agent.status.changed` | a planejar | a definir na rodada |
| Fase 5 | `brza account usage` imprime o uso por conta | a planejar | a definir na rodada |

### Fora de escopo

- **O `brza sessions` do `brza-workflow` sobre a CLI nova** — os aliases, o retry e o resultado fiel do envio no
  wrapper. Vão ao plano do `tools-kit`, com `depends_on` neste, como decidido em R4.1.
- **O porte do `stablyai/orca#37774`** (o rascunho do chat de terminal limpo antes do envio). Chega no próximo sync do
  upstream; só se porta antes se o `brza chat send` passar a cobrir chat PTY, como decidido em R5.1.

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
   `#37774` antes do `send` **→ o `#37774` reaberto em R5.1**. `medium`: navegação (`focus`, barra lateral, Jump Palette) e o journal do `#37802`, que
   espera a integração no upstream. `low`: plugins e `account usage` (`#37467`).
4. **Issues.** **Decidido:** "No workstream da frente (Recomendado)". A sessão que abre o plano cria as issues dele.

### Rodada 5 — a base da fase 1 (enviada 2026-11-03)

> **Apresentado antes:** o Terreno da fase 1, levantado por um `collector` no `brza-studio@8f41dd56a33` e conferido
> nesta sessão. O `#37774` toca só `mobile/`, `src/renderer/src/components/native-chat/` e `src/shared/`, nenhum
> arquivo de `src/main`, e limpa o rascunho do chat de **terminal** antes de um envio do celular ou do desktop; o
> `brza chat send` fala com o host estruturado (`agentSession.send`). Portá-lo agora traz 6 conflitos de lógica e 4
> commits do upstream posteriores à `v1.4.246` (`#37212`, `#36493`, `#37334`, `#37565`). O `#33115` aplica limpo na
> `master` (`git apply --3way` num índice temporário: 11 arquivos, sem conflito), com `list` por `worktree.ps`, `read`
> por `tail`/`before`, `send` com `queue-if-active` e 10 testes, sem cursor, sem o estado da submissão e sem o motivo
> da fila. O host já tem o cursor `{epoch, sequence}` (`src/shared/agent-session-journal-identity.ts:5-8`) e cinco
> motivos de reset com a página `tail` pronta (`agent-session-journal-types.ts:477-483`,
> `agent-session-history-page.ts:87-104`). O motivo da retenção da fila (`prompt|working`) só existe no host
> (`structured-agent-session-queued-messages.ts:46-58`).

Respondida em 2026-11-03.

1. **O `#37774`, que a R4.3 punha antes do `send`.** Opções:
   - sai da fase 1 (recomendada) — custo: nenhum agora; o envio a chat PTY fica como está até o sync; se paga: já, a
     fase 1 começa sem 4 commits de pré-requisito e 6 conflitos;
   - porta antes, com os 4 prévios — custo: estimada uma sessão de código e risco de regressão no composer PTY, antes
     da coordenação; se paga: só se o `chat send` cobrir chat PTY na fase 1;
   - fica, mas no fim da fase 1 — custo: o mesmo, no fim da fase; se paga: se o Studio usar o envio do celular a chat
     PTY antes do sync.

   **Decidido — "Sai da fase 1 (Recomendado)"**: chega no próximo sync do upstream, e só se porta antes se o `chat send`
   passar a cobrir chat PTY. Reabre a parte do `#37774` da R4.3.

2. **A base do `list/read/send`.** Opções:
   - portar o `#33115` e estender (recomendada) — custo: estender o `chat read` e conviver com divergência no sync se
     o upstream fundir outra forma; se paga: na fase 1, poupa o parse do `worktree.ps`, o laço de reset e os testes;
   - escrever do zero — custo: estimado em cerca de 3 vezes o porte, sem os testes do upstream; se paga: nunca, hoje;
   - esperar o `#33115` fundir — custo: a prioridade `high` parada por tempo indefinido, com o PR aberto desde
     2026-10-24; se paga: nunca, para a coordenação de agora.

   **Decidido — "Portar o #33115 e estender (Recomendado)"**: o porte vai num commit separado, e o cursor, o recibo e o
   motivo da fila vêm depois.

3. **O cursor inválido.** Opções:
   - erro com a página `tail` (recomendada) — custo: um contrato de erro a documentar e testar; se paga: na fase 1, a
     sessão coordenadora nunca segue com estado misturado sem saber;
   - reabre sozinho, com aviso — custo: o script que não olha `reset: true` duplica ou pula itens; se paga: nunca, para
     a coordenação.

   **Decidido — "Erro com a página tail (Recomendado)"**: código de saída não zero e `cursor_reset: <motivo>`, com a
   página `tail` e o `nextCursor` novos no JSON.

4. **O motivo da fila.** Opções:
   - lê o histórico após enfileirar (recomendada) — custo: um RPC a mais por envio enfileirado, com o motivo deduzido no
     cliente; se paga: na fase 1, cumpre a R2.2 sem mudar o contrato do host;
   - o host passa a devolver o motivo — custo: muda o contrato do wire e conflita no sync; se paga: só quando um segundo
     cliente precisar do motivo.

   **Decidido — "Lê o histórico após enfileirar (Recomendado)"**: depois de `queued`, um `history tail`, e o JSON traz a
   posição, o `nextQueuedMessageId` e `held_by: question|working`.

### Rodada 6 — o contrato e a prova da fase 1 (enviada 2026-11-03)

> **Apresentado antes:** as inferências do código, com a fonte. O cursor como string opaca `epoch:sequence`, que mapeia
> 1:1 o `{epoch, sequence}` do host; o `--json` com `itemId`, `revision`, `sequence`, `nextCursor` e `hasNewer`, que
> o do `#33115` não traz; a origem do coordenador no `send` pelo `ORCA_AGENT_SESSION_ID`, como o wrapper já faz
> (`brza-workflow/bin/brza_runtime.py:95-97`), lida pelo host no `send`
> (`src/main/runtime/rpc/methods/structured-agent-session-send-compatibility.ts:10`) e ausente da CLI, que só a manda
> em `agent.launch` (`src/cli/runtime/client.ts:58,140`); e a divergência com o levantamento sobre o `fence`, que o
> host atual ignora, mas que a norma do `brza-studio` manda manter, pela compatibilidade entre versões misturadas
> (`AGENTS.md:61`).

Respondida em 2026-11-03.

1. **O código de saída do `send`.** Opções:
   - código por estado (recomendada) — custo: um contrato de códigos a documentar e testar na fase 1; se paga: no
     plano do `tools-kit`, quando o wrapper decide sem ler o JSON e o `sent: true` falso acaba;
   - sempre 0, estado só no JSON — custo: quem chama lê o JSON, e o `sent: true` falso se repete em quem esquecer; se
     paga: nunca, para a coordenação.

   **Decidido — "Código por estado (Recomendado)"**: 0 em `accepted` e `queued`; 1 em recusa e `rejected`; 3 em
   `pending` e `unknown`, entrega incerta que não se reenvia. O JSON traz sempre `delivery` e `submission.state`.

2. **O retry.** Opções:
   - `--operation-id` no `send` (recomendada) — custo: uma flag e o teste de replay na fase 1; se paga: no `tools-kit`,
     no primeiro timeout de envio, sem mensagem duplicada no chat;
   - sem retry na CLI — custo: o retry depois de um timeout duplica a mensagem, ou o wrapper mantém o socket cru; se
     paga: nunca, se o wrapper migrar para a CLI.

   **Decidido — "--operation-id no send (Recomendado)"**: o `send` imprime o `clientOperationId`, e o mesmo id com o
   mesmo texto devolve o resultado gravado, sem reenviar.

3. **O contrato inferido.** Opções:
   - confirma, lendo o `fence` (recomendada) — custo: um RPC por envio, desde a fase 1; se paga: no primeiro host
     remoto mais velho que ainda confere o `fence`;
   - confirma, sem ler o `fence` — custo: o host mais velho recusa o envio, e o código diverge do `#33115`; se paga: uma
     chamada a menos por envio, agora; com versões misturadas, nunca.

   **Decidido — "Confirma, lendo o fence (Recomendado)"**: cursor `epoch:sequence`, `--json` com os ids, origem do
   coordenador no `send` e o `expectedRuntimeFence` lido do histórico antes do envio.

4. **A prova da fase 1.** Opções:
   - unidade e um caso manual (recomendada) — custo: cerca de 30 min de Anderson no app ao fechar a fase; se paga: no
     fim da fase 1, porque a fila retida por pergunta só aparece com o agente real;
   - só unidade — custo: nenhum de Anderson; se paga: agora, mas a dedução do `held_by` só se confere no `tools-kit`.

   **Decidido — "Unidade + 1 caso manual (Recomendado)"**: `chat.test.ts` cobre cursor, reset, fila com `held_by`,
   códigos de saída, replay e origem; o C1 roda no app de dev com dois chats.

## Worklogs

- 2026-11-03 — abertura: as cinco issues das frentes, o PLN-011 com as fases e as R1 a R4 do `playground`; R5 e
  R6 fecham a entrevista da fase 1, e o `#37774` sai dela. Parou antes do Desenho da fase 1.
  [PLN-011: abertura do plano dos chats pela CLI e pelos plugins](../../work/worklogs/2026-11-03-pln-011-abertura-chats-pela-cli-e-plugins.md)

## Fechamento

- [ ] Todo passo `[x]` com evidência, ou `[-]` com motivo.
- [ ] Todo achado com destino que existe.
- [ ] Um resumo por commit ou PR do `brza-studio` da entrega, com o link do plano: os achados e o destino de cada um.
- [ ] O durável saiu para a casa dona e está em `## Decisões` e `## Documentação`.
- [ ] As decisões que o plano respondeu estão `done`, citando a rodada.
- [ ] As cinco issues das fases estão `done`, com `completed`.
- [ ] `status: done`, `phase: closed` e `completed` no frontmatter.
