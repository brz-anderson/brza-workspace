---
status: open
description: O PR #38719 e as issues #33114, #37615 e #38556 trazem o comando orca chat rename na CLI, leitura e envio a sessões de Native Chat e integração com a API de plugins.
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

Rastreado do PR aberto no upstream [`stablyai/orca#38719`](https://github.com/stablyai/orca/pull/38719) (Issue [`#38556`](https://github.com/stablyai/orca/issues/38556)),
além das issues [`stablyai/orca#33114`](https://github.com/stablyai/orca/issues/33114),
[`stablyai/orca#37615`](https://github.com/stablyai/orca/issues/37615),
[`stablyai/orca#37801`](https://github.com/stablyai/orca/issues/37801) e
[`stablyai/orca#37807`](https://github.com/stablyai/orca/issues/37807), e dos PRs
[`stablyai/orca#37467`](https://github.com/stablyai/orca/pull/37467),
[`stablyai/orca#37774`](https://github.com/stablyai/orca/pull/37774) e
[`stablyai/orca#37802`](https://github.com/stablyai/orca/pull/37802).

## O problema

1. **Incapacidade de renomear abas de chat nativo pela CLI (`#38719`, `#38556`):**
   Enquanto terminais PTY podiam ter seus títulos ajustados via comandos de terminal ou scripts, abas de Native Chat
   só podiam ser renomeadas manualmente pelo mouse. Ao retomar uma sessão do Claude (`orca session resume --chat`),
   o título customizado anterior era perdido e não havia como scripts de automação ou agentes coordenadores definirem
   o nome descritivo da aba (`orca chat rename`).
2. **Chats invisíveis para a CLI (`#33114`):** `brza terminal read/send` cobre apenas agentes em terminais PTY. Sessões
   abertas como Native Chat (o padrão de novas abas) aparecem em `worktree ps`, mas não podem ter o histórico lido nem
   receber mensagens pela linha de comando (`brza chat list`, `brza chat read`, `brza chat send`). Isso trava a
   coordenação entre sessões e a automação pelo `brza-workflow` fora da UI.
3. **Falta de comando CLI para focar/abrir chat específico e dessincronização da barra lateral (`#37801`):**
   ao alternar abas via runtime, atalho ou notificação, o painel de agentes na barra lateral esquerda não atualiza a
   seleção para refletir o chat ativo. Além disso, não há comando público como `brza chat focus <id>` (dependendo do
   RPC não documentado `terminal.reveal`), impedindo integrações externas (Stream Deck, scripts de automação).
4. **Ausência de Native Chats na Jump Palette (`#37807`):** abas de Native Chat (`contentType: 'agent-session'`) são
   omitidas da seção de sessões recentes e da busca por título no Jump Palette (`Ctrl+Shift+J` / `Cmd+P`), aparecendo apenas
   arquivos e terminais.
5. **Chats invisíveis para a API de plugins (`#37615`):** na `1.4.246`, o host monta `agents.list` e emite
   `agent.status.changed` apenas a partir de `listWorktreeTerminals` e `listAgentStatuses`, cobrindo somente painéis de
   terminal. Um plugin não enxerga abas de Native Chat, o modelo em uso, o `sessionId` nem o diretório de trabalho
   (`workspace.readContext` também omite o caminho no disco).
6. **Concorrência e travamento no journal de chats (`#37774`, `#37802`):** limpeza de histórico no SQLite do journal
   chegava a travar a interface por 5 a 10 segundos no thread principal, e envios para chats podiam descartar rascunhos
   abertos no terminal.

## O caminho técnico apontado no upstream

- **Subcomando `orca chat rename` na CLI (`#38719`, resolve `#38556`):**
  - Implementa `orca chat rename --name <novo-nome>` (renomeando o chat da sessão atual) e
    `orca chat rename --session <sessionId> --name <novo-nome>` para chamadas externas de scripts ou coordenadores;
  - Preserva a sincronia do título na barra de abas e nos registros persistentes do app.
- **Na CLI e navegação (`#33114`, `#37801`, `#37807`):** expor comandos do grupo `chat` (`list`, `read`, `send`,
  `focus`), sincronizar bidirecionalmente a seleção da barra lateral com o chat ativo e incluir `agent-session` no
  filtro de abas do Jump Palette.
- **Na robustez do chat (`#37774`, `#37802`):** isolar rascunhos de terminal contra envios de chat e mover operações
  pesadas de SQLite do journal para background writer compartilhado.
- **Nos plugins (`#37615`):** incluir sessões de Native Chat em `agents.list` com discriminador de superfície (`chat` vs
  `terminal`), emitir `agent.status.changed` para elas e acrescentar o caminho do worktree em `workspace.readContext`.
- **Em `account usage` (`#37467`):** portar `src/cli/handlers/account-usage-command.ts` e `account-usage-format.ts`.

## O que fazer

- Implementar `brza chat rename` (`#38719`) na CLI do `brza`, permitindo que agentes nomeiem automaticamente suas conversas.
- Implementar `brza chat list/read/send/focus`, incluir Native Chat na Jump Palette e na seleção da barra lateral, e
  expor Native Chat em `agents.list` no `brza-studio`, alinhando com as necessidades do `brza-workflow`.
