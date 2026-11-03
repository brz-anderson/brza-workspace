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

Rastreado das issues abertas no upstream [`stablyai/orca#33114`](https://github.com/stablyai/orca/issues/33114) e
[`stablyai/orca#37615`](https://github.com/stablyai/orca/issues/37615), além do PR
[`stablyai/orca#37467`](https://github.com/stablyai/orca/pull/37467).

## O problema

1. **Chats invisíveis para a CLI (`#33114`):** `brza terminal read/send` cobre apenas agentes em terminais PTY. Sessões
   abertas como Native Chat (o padrão de novas abas) aparecem em `worktree ps`, mas não podem ter o histórico lido nem
   receber mensagens pela linha de comando (`brza chat list`, `brza chat read`, `brza chat send`). Isso trava a
   coordenação entre sessões e a automação pelo `brza-workflow` fora da UI.
2. **Chats invisíveis para a API de plugins (`#37615`):** na `1.4.246`, o host monta `agents.list` e emite
   `agent.status.changed` apenas a partir de `listWorktreeTerminals` e `listAgentStatuses`, cobrindo somente painéis de
   terminal. Um plugin não enxerga abas de Native Chat, o modelo em uso, o `sessionId` nem o diretório de trabalho
   (`workspace.readContext` também omite o caminho no disco).
3. **Consumo de cota na CLI (`#37467`):** falta o subcomando `account usage` no CLI para inspecionar os limites de uso
   por conta sem abrir a janela desktop.

## O caminho técnico apontado no upstream

- **Na CLI (`#33114`):** os métodos RPC `agentSession.history` e `agentSession.send` (com entrega `queue-if-active` via
  `structuredAgentSessionMessageSendMutation`) já existem no runtime com permissão `workspace` para o cliente mobile;
  falta apenas expor o grupo `chat` (`list`, `read`, `send`) em `src/cli/handlers/` e `src/cli/specs/`.
- **Nos plugins (`#37615`):** incluir sessões de Native Chat em `agents.list` com discriminador de superfície (`chat` vs
  `terminal`), emitir `agent.status.changed` para elas e acrescentar o caminho do worktree em `workspace.readContext`.
- **Em `account usage` (`#37467`):** portar `src/cli/handlers/account-usage-command.ts` e `account-usage-format.ts`.

## O que fazer

Avaliar a implementação de `brza chat list/read/send` e a exposição de Native Chat em `agents.list` no `brza-studio`
(ou a incorporação dos PRs correspondentes do upstream assim que abrirem), alinhando com o `brza-workflow`.
