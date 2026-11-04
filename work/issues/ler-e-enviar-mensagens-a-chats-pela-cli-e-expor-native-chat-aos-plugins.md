---
status: open
description: As issues #33114 e #37615 do upstream propõem brza chat list/read/send na CLI e a inclusão de sessões de Native Chat em agents.list e agent.status.changed da API de plugins.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-03
tags:
  - chat
  - tooling
---

# Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins

Rastreado das issues abertas no upstream [`stablyai/orca#33114`](https://github.com/stablyai/orca/issues/33114),
[`stablyai/orca#37615`](https://github.com/stablyai/orca/issues/37615),
[`stablyai/orca#37801`](https://github.com/stablyai/orca/issues/37801) e
[`stablyai/orca#37807`](https://github.com/stablyai/orca/issues/37807), além dos PRs
[`stablyai/orca#37467`](https://github.com/stablyai/orca/pull/37467),
[`stablyai/orca#37774`](https://github.com/stablyai/orca/pull/37774) e
[`stablyai/orca#37802`](https://github.com/stablyai/orca/pull/37802).

## O problema

1. **Chats invisíveis para a CLI (`#33114`):** `brza terminal read/send` cobre apenas agentes em terminais PTY. Sessões
   abertas como Native Chat (o padrão de novas abas) aparecem em `worktree ps`, mas não podem ter o histórico lido nem
   receber mensagens pela linha de comando (`brza chat list`, `brza chat read`, `brza chat send`). Isso trava a
   coordenação entre sessões e a automação pelo `brza-workflow` fora da UI.
2. **Falta de comando CLI para focar/abrir chat específico e dessincronização da barra lateral (`#37801`):**
   ao alternar abas via runtime, atalho ou notificação, o painel de agentes na barra lateral esquerda não atualiza a
   seleção para refletir o chat ativo. Além disso, não há comando público como `brza chat focus <id>` (dependendo do
   RPC não documentado `terminal.reveal`), impedindo integrações externas (Stream Deck, scripts de automação).
3. **Ausência de Native Chats na Jump Palette (`#37807`):** abas de Native Chat (`contentType: 'agent-session'`) são
   omitidas da seção de sessões recentes e da busca por título no Jump Palette (`Ctrl+Shift+J` / `Cmd+P`), aparecendo apenas
   arquivos e terminais.
4. **Chats invisíveis para a API de plugins (`#37615`):** na `1.4.246`, o host monta `agents.list` e emite
   `agent.status.changed` apenas a partir de `listWorktreeTerminals` e `listAgentStatuses`, cobrindo somente painéis de
   terminal. Um plugin não enxerga abas de Native Chat, o modelo em uso, o `sessionId` nem o diretório de trabalho
   (`workspace.readContext` também omite o caminho no disco).
5. **Concorrência e travamento no journal de chats (`#37774`, `#37802`):** limpeza de histórico no SQLite do journal
   chegava a travar a interface por 5 a 10 segundos no thread principal, e envios para chats podiam descartar rascunhos
   abertos no terminal.

## O caminho técnico apontado no upstream

- **Na CLI e navegação (`#33114`, `#37801`, `#37807`):** expor comandos do grupo `chat` (`list`, `read`, `send`,
  `focus`), sincronizar bidirecionalmente a seleção da barra lateral com o chat ativo e incluir `agent-session` no
  filtro de abas do Jump Palette.
- **Na robustez do chat (`#37774`, `#37802`):** isolar rascunhos de terminal contra envios de chat e mover operações
  pesadas de SQLite do journal para background writer compartilhado.
- **Nos plugins (`#37615`):** incluir sessões de Native Chat em `agents.list` com discriminador de superfície (`chat` vs
  `terminal`), emitir `agent.status.changed` para elas e acrescentar o caminho do worktree em `workspace.readContext`.
- **Em `account usage` (`#37467`):** portar `src/cli/handlers/account-usage-command.ts` e `account-usage-format.ts`.

## O que fazer

Implementar `brza chat list/read/send/focus`, incluir Native Chat na Jump Palette e na seleção da barra lateral, e
expor Native Chat em `agents.list` no `brza-studio`, alinhando com as necessidades do `brza-workflow`.

## Aprofundamento verificado em 2026-11-03

As descrições acima registram os relatos do upstream; o checkout local do Studio `8f41dd56a33` e o workflow já cobrem parte delas:

- **Há implementação candidata:** o PR aberto [#33115](https://github.com/stablyai/orca/pull/33115), ausente do levantamento inicial, acrescenta `chat list/read/send` em 11 arquivos, reutilizando RPCs existentes. Não inclui `focus`, `wait`, `read --since` ou envio condicionado atomicamente à ociosidade. Seus recibos não comprovam conclusão da tarefa.
- **Envio por nome já existe:** `brza-workflow/packages/client/bin/brza-sessions:68` oferece `open/list/send/title/close`. Em `:283-287`, o envio imprime `sent: true`; `bin/brza_runtime.py:141-145` descarta o resultado da mutação. O RPC verifica apenas o sucesso externo (`:115-117`), embora a mutação possa retornar recusa interna. A lacuna é leitura e resultado fiel do envio, não ausência total de acesso a chats.
- **O wrapper tem limites próprios:** usa socket Unix local, não negocia a capability de fila e cria nova identidade de operação a cada envio. Já preserva a origem do coordenador por `orchestrationCompatibilityEvidence` (`bin/brza_runtime.py:84-145`). Uma substituição precisa preservar essa origem.
- **O backend de leitura já existe:** `src/main/runtime/rpc/methods/structured-agent-session.ts:195-225` expõe histórico e assinatura incremental com permissão `workspace`. A CLI pode reutilizá-los.
- **O protocolo evoluiu:** `src/shared/agent-session/lifecycle/agent-session-mutation-envelope.ts:66` documenta que o host atual ignora `expectedRuntimeFence` na admissão; hosts antigos ainda o verificam. A fila atual tem contrato `agent-session.queued-messages.v2` (`src/shared/rpc-contract/structured-agent-session-params.ts:113`). Portar o PR exige conferir a semântica atual, não prometer proteção universal por fence.
- **Plugins têm cobertura parcial:** o hook server já ingere status estruturados (`src/main/agent-hooks/server/server-ingest-structured.ts:147-169`) e os inclui no snapshot (`server-listeners.ts:216-217`). A projeção de `agents.list` admite linhas sem terminal, mas omite identidade de sessão, superfície e modelo (`src/main/plugins/workers/plugin-workspace-projection.ts:74-93`). O contexto omite caminhos deliberadamente (`:45-60`); ampliá-lo muda o contrato público.
- **Transporte e conclusão são distintos:** `src/main/runtime/orchestration/send-agent-turn.ts:143-164` distingue recusa, fila e submissão pendente. A reconciliação de `worker_done` continua exigindo tarefa, dispatch e autoridade (`lifecycle-reconciliation.ts:182-254`). Texto no histórico não substitui esse protocolo.

O aprofundamento é levantamento técnico. O recorte de implementação ainda depende de escolha; nenhum código foi alterado e nenhuma mensagem foi enviada a outra sessão.

## Foco escolhido para detalhamento em 2026-11-03

Anderson respondeu nesta sessão:

> Coordenação entre sessões (Recomendado). Custo: adaptar list/read/send à CLI e integrar nomes, recibos e retry ao wrapper existente. Se paga: ao encaminhar trabalho para chats já abertos e acompanhar suas respostas.

A resposta orienta a proposta técnica; não autoriza iniciar a implementação. O detalhamento cobre identificação da sessão existente, leitura, envio, recibos e retry. O levantamento de plugins permanece como referência para outra etapa.

### Restrições verificadas para o contrato

- `AgentSessionSendResult` distingue fila de submissão (`brza-studio/src/shared/agent-session/agent-session-wire.ts:317-332`). A submissão pode estar `pending`, `accepted`, `rejected` ou `unknown`; este último não significa envio nem falha confirmada (`src/shared/agent-session/journal/agent-session-journal-types.ts:396-411`).
- Os testes de envio documentam replay com a mesma operação sem novo disparo e preservação de `unknown` mesmo com `retryUnknown` (`src/main/native-chat/agent-session-wire/structured-agent-session-send.test.ts:176-227`). Um retry não pode prometer resolver uma entrega incerta.
- O cliente da CLI atual encaminha a origem do coordenador em orquestração e launch, mas não em `agentSession.send` (`src/cli/runtime/client.ts:134-142`). O wrapper já a encaminha; migrar o transporte exige manter essa informação.

**Próxima rodada:** definir o acompanhamento das respostas e a política de envio durante trabalho em andamento. O foco de coordenação já foi escolhido; esses comportamentos ainda não foram aprovados.

### Respostas da rodada de 2026-11-03

- **Acompanhamento:** Anderson escolheu leitura incremental por cursor, com tratamento de cursor inválido.
- **Envio durante atividade:** Anderson escolheu preservar `queue-if-active` e expor que a mensagem está enfileirada, inclusive quando uma pergunta pendente retém a fila.

Com essas respostas, a proposta da primeira versão fica delimitada a coordenação por cursor e fila existente, integrada aos aliases de `brza sessions`, com recibos e retry seguros. A implementação ainda não foi iniciada.

### Rodada de abertura do plano (2026-11-03)

Apresentado antes: o recorte já respondido (coordenação por cursor e fila, aliases de `brza sessions`, recibos e retry)
e as frentes fora dele (focus e barra lateral, Jump Palette, robustez do journal, plugins, `account usage`).

- **Destino** — opções: `PLN` em `plans/` (recomendado); seção num worklog. **Resposta:** "um plano pra cada
  `workstream` e elas se coordenam na execução".
- **Recorte** — opções: só a coordenação (recomendado); coordenação + `chat focus`; a issue inteira, por fases.
  **Resposta:** "A issue inteira, por fases".
- **Restante** — opções: fica na issue de origem (recomendado); vira issues próprias. **Resposta:** "issues próprias,
  repriorize individualmente".

As respostas em texto livre voltam em rodada de esclarecimento: que workstreams recebem plano e como as fases se
combinam com as issues próprias.

### Rodada de esclarecimento do plano (2026-11-03)

Apresentado antes: a leitura das respostas em texto livre — `studio` para o código do `brza-studio` e `tools-kit` para o
`brza sessions` (`README.md:12-14`), abertos por sessões novas, como manda o `AGENTS.md`; e o estado no upstream:
`#37774` integrado em 2026-11-03 18:28 UTC e ausente do checkout local `8f41dd56a33`, `#37802` e `#37467` abertos.

- **Workstreams:** "studio + tools-kit (Recomendado)". Um `PLN` no `studio` e outro no `tools-kit`, este com
  `depends_on` no do `studio`, cada um aberto por sessão nova no worktree dele.
- **Fases:** "Todas as frentes, por prioridade (Recomendado)". Cada frente vira issue com prioridade própria; os planos
  cobrem todas, em fases na ordem da prioridade, cada fase citando a issue dela.
- **Prioridades:** "Proposta abaixo (Recomendado)". `high`: coordenação (`list/read/send`) e o porte do `#37774` antes
  do `send`. `medium`: navegação (`focus`, barra lateral, Jump Palette) e o journal do `#37802`, que espera a integração
  no upstream. `low`: plugins e `account usage` (`#37467`).
- **Issues:** "No workstream da frente (Recomendado)". A sessão que abre cada plano cria as issues dele. Esta issue
  passa a `done`, com os links para as novas, quando elas existirem.
