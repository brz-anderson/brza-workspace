---
status: open
description: Os PRs #41216, #40953, #40616, #40564, #40550, #40923 trazem guarda de cartões MCP, alerta de janela ocupada, auth MCP e cache.
scope:
  - brza-studio
  - brza-workflow
  - workspace
priority: high
opened: 2026-11-10
tags:
  - chat
  - tooling
  - infra
---

# Autenticação MCP no chat, alerta de turnos ativos e cache de orquestração

Rastreado dos PRs abertos no upstream [`stablyai/orca#41216`](https://github.com/stablyai/orca/pull/41216),
[`stablyai/orca#40953`](https://github.com/stablyai/orca/pull/40953) (resolve Issue [`#40640`](https://github.com/stablyai/orca/issues/40640)),
[`stablyai/orca#40616`](https://github.com/stablyai/orca/pull/40616) (resolve Issue [`#38962`](https://github.com/stablyai/orca/issues/38962), relacionado a [`#39920`](https://github.com/stablyai/orca/issues/39920) e [`#38190`](https://github.com/stablyai/orca/issues/38190)),
[`stablyai/orca#40564`](https://github.com/stablyai/orca/pull/40564),
[`stablyai/orca#40550`](https://github.com/stablyai/orca/pull/40550) (resolve Issue [`#39852`](https://github.com/stablyai/orca/issues/39852) e PR [`#40527`](https://github.com/stablyai/orca/pull/40527)),
[`stablyai/orca#40923`](https://github.com/stablyai/orca/pull/40923) / [`stablyai/orca#40612`](https://github.com/stablyai/orca/pull/40612) (resolve Issue [`#40607`](https://github.com/stablyai/orca/issues/40607)) e da issue
[`stablyai/orca#40682`](https://github.com/stablyai/orca/issues/40682).

## O problema

1. **Inexistência de interação com comandos Claude e sign-in de servidores MCP no Native Chat (`#40616`, `#38962`):**
   No terminal CLI do Claude, o comando `/mcp` abre menus interativos de autenticação OAuth e alternância de servidores.
   No Native Chat estruturado do Orca/Studio, o comando `/mcp` emitia apenas um resumo plano somente-leitura, sem permitir
   seleção de servidores, entrada em fluxos de consentimento OAuth ou configuração interativa de permissões (`/permissions`, `/config`).
2. **Degradação massiva por consultas síncronas de orquestração e títulos em frotas de worktrees (`#40564`):**
   Após o primeiro despacho de orquestração, cada sincronização de janela executava leituras síncronas no SQLite para inspecionar
   o estado de despacho de todos os terminais, inclusive terminais inativos. Leitura de atenção no chat e geração de títulos de abas
   reconstruíam todos os contextos de orquestração para avaliar um único painel, atingindo mais de 100.000 declarações SQL e ~8,3s
   por leitura em frotas grandes de worktrees.
3. **Fechamento silencioso de janelas com agentes trabalhando no meio de um turno (`#40640`):**
   A rotina de proteção contra fechamento acidental de janela (`assessWindowCloseRunningWork`) inspecionava apenas processos PTY
   em abas de terminal (`state.tabsByWorktree`). Como abas de Native Chat (`contentType: 'agent-session'`) não utilizam PTYs
   locais e residem em `unifiedTabsByWorktree`, fechar a janela do aplicativo enquanto um agente estava respondendo (`mid-turn`)
   fechava a janela imediatamente sem exibir diálogo de confirmação, abortando tarefas em execução.
4. **Travamento de 20 a 250 segundos no event loop do processo principal por projeção do journal (`#40682`):**
   Em ambientes com múltiplos chats nativos simultâneos e extensos (44k a 60k itens), cada commit de journal disparava uma
   re-renderização síncrona completa do chat na thread principal via `renderJournalStatus` / `renderJournalItems(state)` e
   leitura total com descarte de cache por sequência, consumindo cerca de 40ms de CPU por evento a cada 100k itens e
   congelando a interface do app no macOS.
5. **Perda de variáveis de ambiente de clipboard em terminais remotos sem comando inicial (`#40550`, `#39852`):**
   A ponte IPC de criação de terminais só enfileirava o startup com variáveis de ambiente quando um comando explícito era
   fornecido. Ao abrir um terminal remoto via botão `+` em visualizador pareado, a variável `ORCA_REMOTE_VIEWER_CLIPBOARD`
   era descartada, impedindo a sincronização de área de transferência.
6. **Alerta espúrio do Factory Droid por hook `PermissionRequest` não suportado (`#40612`, `#40607`):**
   O instalador registrava o hook `PermissionRequest` em `~/.factory/settings.json`, evento não suportado pelo Droid que
   fazia o `droid doctor` acusar advertência de integridade de forma contínua.

## O que o upstream implementa e corrige

- **Interface interativa para MCP e comandos Claude no Chat UI (`#40616`):**
  - Implementa barra de ferramentas compacta de linha única no desktop com suporte completo a teclado (setas, Enter, Escape, Back, Done) e drawer nativo no mobile para seleção de servidores MCP e login OAuth;
  - Roteia `/config` e `/permissions` para folhas de opções integradas, preservando rascunhos e anexos digitados pelo usuário;
  - Encaminha requisições ao host da sessão sem exigir abandono do Chat UI para o terminal.
- **Cache indexado de fatos de orquestração e leitura direta de painéis (`#40564`):**
  - Indexa despachos elegíveis com invalidação direcionada em mutações do banco de dados, reduzindo consultas de atenção de ~8.300ms (102.610 SQL statements) para 0,1ms (8 statements) em frotas com 1.000 worktrees;
  - Leitores de atenção e geradores de títulos passam a solicitar diretamente o painel alvo em vez de reconstruir o grafo completo.
- **Alerta de confirmação ao fechar janela com chat nativo ativo (`#40640`):**
  - Estende `assessWindowCloseRunningWork` para consultar sessões `agent-session` em `unifiedTabsByWorktree` via sonda com deadline de 2,5s;
  - Exibe diálogo modal "An agent is still working in a chat. Close the window anyway?" caso haja agente em turno ativo.
- **Diagnóstico arquitetural e caminho de mitigação para projeção de journal (`#40682`):**
  - Mapeia o gargalo de `statusRead()` e `agentSession.history` síncronos na thread principal, apontando a necessidade de renderização incremental por item e fatiamento antes da projeção de cauda.
- **Envio garantido de variáveis de clipboard em terminais remotos sem comando (`#40550`):**
  - Enfileira startup exclusivo de variáveis de ambiente mesmo sem comando inicial, mantendo `ORCA_REMOTE_VIEWER_CLIPBOARD` ativo.
- **Remoção de hook incompatível do Droid (`#40612`):**
  - Remove o registro de `PermissionRequest` do instalador Droid, preservando esperas de aprovação nos eventos suportados `PreToolUse` e `Notification`.
- **Validação de consentimento e cartões para múltiplos servidores MCP (`#41216`):**
  - Implementa a guarda de segurança `requireStartupDialog` no envio de respostas de cartões interativos para a PTY do Claude: relê a tela headless imediatamente antes de enviar sequências de setas/Enter e recusa o envio se o destaque na tela tiver mudado ou se a tela repintou, impedindo aprovações acidentais em opções divergentes;
  - Adiciona suporte nativo a cartões para o diálogo multi-servidor `.mcp.json` do Claude 2.1.322 ("N new MCP servers found") com ações "Enable selected" e "Reject all";
  - Substitui o payload JSON bruto no pill do dashboard de agentes por um resumo legível com o título ou questão da espera interativa (`interactivePromptLabel`).

## O que fazer no BrzA Studio

1. Adotar a guarda de consentimento `requireStartupDialog` e o suporte a cartões de múltiplos servidores MCP (`#41216`).
2. Incorporar a barra de ferramentas de controle de MCP e comandos Claude (`#40616`) no composer do Native Chat.
3. Adotar a indexação e cache de fatos de orquestração (`#40564`) para eliminar gargalos de SQLite no Studio.
4. Adotar o diálogo de proteção de fechamento de janela com chats em andamento (`#40640`).
5. Considerar a refatoração incremental de projeção de histórico do chat nativo (`#40682`) para prevenir travamentos com chats longos.
6. Garantir o repasse de ambiente de clipboard em terminais remotos (`#40550`).
7. Atualizar os hooks do Droid eliminando `PermissionRequest` (`#40612`).
