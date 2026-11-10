---
status: open
description: O PR #38719 e as issues #40664, #38952, #39043, #33114, #37615 trazem orca chat list, read, send e rename, retomada por ID e orquestração.
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
além das issues [`stablyai/orca#40664`](https://github.com/stablyai/orca/issues/40664),
[`stablyai/orca#38952`](https://github.com/stablyai/orca/issues/38952),
[`stablyai/orca#39043`](https://github.com/stablyai/orca/issues/39043),
[`stablyai/orca#33114`](https://github.com/stablyai/orca/issues/33114),
[`stablyai/orca#37615`](https://github.com/stablyai/orca/issues/37615),
[`stablyai/orca#37801`](https://github.com/stablyai/orca/issues/37801) e
[`stablyai/orca#37807`](https://github.com/stablyai/orca/issues/37807), e dos PRs
[`stablyai/orca#37467`](https://github.com/stablyai/orca/pull/37467),
[`stablyai/orca#37774`](https://github.com/stablyai/orca/pull/37774) e
[`stablyai/orca#37802`](https://github.com/stablyai/orca/pull/37802).

## O problema

1. **Invisibilidade e falta de retomada de chats pela CLI (`#38952`):**
   Enquanto `orca terminal list` expõe apenas abas de terminal PTY, sessões abertas como Native Chat ficam invisíveis para
   scripts automatizados. Além disso, embora `orca search` e o Session History encontrem transcrições antigas, não há
   nenhum comando de linha de comando para retomar uma sessão específica pelo seu ID (`orca session resume --session <id>`),
   forçando o uso manual do mouse na interface gráfica.
2. **Incapacidade da CLI de reportar foco da interface (`#39043`):**
   Automações que encerram ou liberam painéis de agentes não conseguem saber se o usuário está com o foco visual voltado
   para aquele cartão ou terminal no momento. O comando `orca worktree show --worktree active` resolve apenas a pasta de
   trabalho da chamada, e nenhum campo JSON reporta qual terminal tem o foco real da UI, arriscando fechar abas que o operador está lendo.
3. **Incapacidade de renomear abas de chat nativo pela CLI (`#38719`, `#38556`):**
   Abas de Native Chat só podiam ser renomeadas manualmente pelo mouse. Ao retomar uma sessão do Claude, o título
   customizado anterior era perdido e não havia como scripts de automação definirem o nome descritivo da aba (`orca chat rename`).
4. **Chats invisíveis para a CLI e bots de orquestração externa (`#40664`, `#33114`):**
   Comandos `orca terminal read` e `orca orchestration send` funcionam exclusivamente com abas de terminal PTY. Ao mover
   sessões para abas de chat estruturado (`agent-session`), automações e bots externos não conseguem encontrar nem interagir
   com as conversas (`orca terminal list` omite chats). Além disso, quando um chat nativo tenta responder a um despachante
   de orquestração chamador, a chamada falha com o erro "terminal is closed".
5. **Falta de comando CLI para focar/abrir chat específico e dessincronização da barra lateral (`#37801`):**
   Ao alternar abas via runtime, atalho ou notificação, o painel de agentes na barra lateral esquerda não atualiza a
   seleção para refletir o chat ativo.
6. **Ausência de Native Chats na Jump Palette (`#37807`):** abas de Native Chat são omitidas da busca por título no Jump Palette.
7. **Chats invisíveis para a API de plugins (`#37615`):** na `1.4.246`, o host emite status apenas a partir de terminais PTY.
8. **Concorrência e travamento no journal de chats (`#37774`, `#37802`):** limpeza de histórico no SQLite do journal travava a UI.

## O caminho técnico apontado no upstream

- **Listagem, leitura e envio de mensagens para chats na CLI (`#40664`, `#38952`, `#33114`):**
  - Implementa comandos equivalentes aos de terminal: `orca chat list` (com `sessionId`, `worktree`, `agent`, `status`), `orca chat read --session <id>` e `orca chat send --session <id> <mensagem>`;
  - Permite que respostas emitidas pelo chat via orquestração alcancem o processo chamador externo;
  - Implementa `orca session resume --session <id> [--as chat|terminal] [--worktree <selector>]` permitindo retomar programaticamente qualquer sessão catalogada pelo ID.
- **Relatório de foco da UI na CLI (`#39043`):**
  - Expõe campos `focusedCard` e `focusedTerminal` em `worktree show --json` e `terminal list --json`, permitindo que rotinas de limpeza decidam com segurança se uma aba pode ser liberada.
- **Subcomando `orca chat rename` na CLI (`#38719`, resolve `#38556`):**
  - Implementa `orca chat rename --name <novo-nome>` e `orca chat rename --session <sessionId> --name <novo-nome>`;
  - Preserva a sincronia do título na barra de abas e nos registros persistentes do app.
- **Na CLI e navegação (`#33114`, `#37801`, `#37807`):** expor comandos do grupo `chat` (`list`, `read`, `send`, `focus`),
  sincronizar bidirecionalmente a seleção da barra lateral com o chat ativo e incluir `agent-session` no Jump Palette.
- **Na robustez do chat (`#37774`, `#37802`):** isolar rascunhos de terminal contra envios de chat e otimizar queries SQLite.

## O que fazer

- Adotar `orca chat list`, `orca chat read` e `orca chat send` (`#40664`, `#38952`, `#33114`) no `brza-workflow` e `brza-cli` para orquestração headless e bidirecional de chats nativos.
- Adotar `orca session resume` (`#38952`) para retomada automatizada de sessões por ID.
- Incorporar os campos de reporte de foco da UI (`#39043`) para evitar fechamento acidental de telas ativas do usuário.
- Portar o comando `orca chat rename` (`#38719`) e a exposição de Native Chats para plugins (`#37615`).
