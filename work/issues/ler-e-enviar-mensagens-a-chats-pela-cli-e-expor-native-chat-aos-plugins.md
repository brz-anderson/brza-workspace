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
