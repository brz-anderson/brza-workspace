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
