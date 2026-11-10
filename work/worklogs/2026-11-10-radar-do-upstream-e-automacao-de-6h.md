---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-10
completed: 2026-11-10
tags:
  - tooling
refs:
  - issue:aprovacao-de-workers-no-chat-atualizacao-de-agentes-e-diretorio-de-mensagens
  - issue:autenticacao-mcp-no-chat-alerta-de-turnos-ativos-e-cache-de-orquestracao
  - issue:badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes
  - issue:bifurcacao-de-conversas-no-chat-ui-e-resiliencia-de-inicializacao-do-claude
  - issue:comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais
  - issue:historico-de-navegacao-no-editor-e-identificacao-de-workspaces-por-plugins
  - issue:ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins
  - issue:plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados
  - issue:workers-de-plugins-em-hosts-remotos-e-gerenciamento-cli-de-ssh
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-10)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-09T21:00:00Z` e `2026-11-10T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Badges de worktree para plugins, cadência de PR e redesenho de automações](../issues/badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes.md):
     rastreia o PR `#40557` (ponto de contribuição `contributes.worktreeBadges` nos manifestos de plugins, avaliando `when.pathExists`
     com `searchDepth: 0..3` e exibindo badges com menu de ações dedicado na sidebar),
     PR `#40541` / STA-8667 (cadência configurável de auto-refresh de PRs e CI checks em `Settings → Git & Source Control → PR Auto-Refresh`:
     Default 1-2min, Reduced 5-10min, Minimal 10-20min, Off),
     PR `#40507` (redesenho completo da visualização de detalhes de automações `AutomationDetailOverview`, com cabeçalho limpo,
     faixa de saúde com métricas/custos de tokens, prompt expansível com botão de cópia e ações destrutivas em menu dropdown "…"),
     PR `#40534` (eliminação da varredura global em rajada de issues vinculadas do GitHub ao restaurar o foco da janela, restringindo
     a cartões visíveis no viewport `visible-only` com janela de 5 min e liberando a fila da CLI),
     PR `#40539` / STA-2380 (verificação de comando desenhado `hasTerminalCommandPainted` após o marcador OSC 133;C no estado `tui-idle`
     para evitar injeções prematuras de tarefas em inicializações a frio do Claude Code no terminal) e
     PR `#40540` / issue `#40510` (persistência e restauração do modo tela cheia nativo após reinicialização do app).
3. **Atualização de 2 issues existentes em `work/issues/`:**
   - [Histórico de navegação no editor e identificação de workspaces por plugins](../issues/historico-de-navegacao-no-editor-e-identificacao-de-workspaces-por-plugins.md):
     adicionada a issue `#40492` (exposição do `id` unívoco e do caminho absoluto `path` do workspace no resultado de
     `workspace.readContext` e nos argumentos do evento `workspace.changed`, permitindo que linters, observadores e plugins
     amarrem com exatidão suas ferramentas ao diretório raiz correto).
   - [Bifurcação de conversas no Chat UI e resiliência de inicialização do Claude](../issues/bifurcacao-de-conversas-no-chat-ui-e-resiliencia-de-inicializacao-do-claude.md):
     adicionados o PR `#40548` (identidade de chat do Claude mantida estritamente nativa, isolando geração de títulos e processos de
     background sob identidades dedicadas de cliente e delimitando a fronteira de inicialização no SDK sem vazamento para overrides
     de conta), o PR `#40558` (preservação do estado de runtime e mapas de sessões de cada conta Claude durante refresh em background) e
     o PR `#38001` / issue `#37707` (fallback seguro para inicializar um novo chat limpo ao retomar conversas de CLI cujo transcript
     esteja ausente ou corrompido no disco, prevenindo abas travadas).

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-10)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-10T03:00:00Z` e `2026-11-10T09:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Autenticação MCP no chat, alerta de turnos ativos e cache de orquestração](../issues/autenticacao-mcp-no-chat-alerta-de-turnos-ativos-e-cache-de-orquestracao.md):
     rastreia o PR `#40616` / issue `#38962` (suporte a comandos comuns do Claude e autenticação interativa de MCP diretamente no Chat UI
     com `/mcp`, `/config` e `/permissions`, dispondo de barra compacta no desktop e drawer no mobile para login OAuth),
     PR `#40564` (indexação de despachos e cache com invalidação direcionada para fatos de orquestração e leitura direta de painéis, reduzindo
     de 102.610 para 8 statements SQL e de ~8,3s para 0,1ms em frotas de 1.000 worktrees),
     PR `#40550` / issue `#39852` e PR `#40527` (preservação de variáveis de ambiente de clipboard `ORCA_REMOTE_VIEWER_CLIPBOARD` em terminais
     remotos abertos sem comando inicial por visualizadores pareados),
     PR `#40612` / issue `#40607` (remoção do hook não suportado `PermissionRequest` no Factory Droid, eliminando advertências do `droid doctor`),
     issue `#40640` (alerta de confirmação contra fechamento de janela com agentes em turno ativo no Native Chat `mid-turn`) e
     issue `#40682` (diagnóstico arquitetural do bloqueio do event loop de 20–250s no macOS por re-renderização síncrona do journal).
3. **Atualização de 4 issues existentes em `work/issues/`:**
   - [Comandos shell no chat, recibos de perguntas e foco espacial em terminais](../issues/comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais.md):
     adicionado o PR `#40620` (execução inline nativa de comandos shell iniciados por `!` diretamente dentro do Chat UI com streaming em tempo
     real via pipes, botão Stop de cancelamento, ordenação estrita de stderr com cor, persistência de `cd` e cartão opcional "Add to chat"
     para injetar a saída como contexto do próximo prompt para o agente, além de virtualização com `content-visibility` para saídas de até 100k linhas).
   - [Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](../issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md):
     adicionada a issue `#40664` (demanda por equivalência completa de CLI para chats nativos: `orca chat list`, `orca chat read` e
     `orca chat send` por session ID, permitindo que automações externas e bots acionem e recebam respostas de agentes estruturados).
   - [Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados](../issues/plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados.md):
     adicionados o PR `#40597` / issue `#39620` (grupos nomeados e colapsáveis para worktrees fixados na seção Pinned com menus de contexto
     dedicados e qualificação por host), o PR `#40604` / issue `#40392` (ação "Move to top" no menu de opções do cabeçalho de projetos na sidebar) e
     o PR `#40603` / issue `#40397` (priorização da seção Workspaces à frente de Open Tabs na busca digitada da Jump Palette via Cmd+J).
   - [Workers de plugins em hosts remotos e gerenciamento CLI de SSH](../issues/workers-de-plugins-em-hosts-remotos-e-gerenciamento-cli-de-ssh.md):
     adicionado o PR `#40589` / issue `#38342` (execução de painéis de plugins da barra lateral direita no host pareado onde o workspace
     focado reside, usando RPC de streaming `plugins.panelSession` com validação de fingerprint de consentimento e nota visual informativa `Running on <host>`).

### 3. Ciclo de 6h (12:00 BRT / 15:00 UTC em 2026-11-10)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-10T09:00:00Z` e `2026-11-10T15:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Aprovação de workers no chat, atualização de agentes e diretório de mensagens](../issues/aprovacao-de-workers-no-chat-atualizacao-de-agentes-e-diretorio-de-mensagens.md):
     rastreia o PR `#40756` (cartões `NativeChatApprovalCard` no chat do coordenador com contagem regressiva, faixa "N approvals · Show" e botões
     Allow/Deny que respondem via `orchestration.approvalAnswer` gerando recibos transparentes),
     PR `#40760` / issue `#40714` (painel expansível "Chat history" no Chat UI com virtualização `VirtualizedList` para mais de 10k mensagens e atalhos completos de teclado),
     PR `#40679` / issue `#24958` (segmento na status bar informando CLIs de agentes desatualizadas com popover detalhado e atualização com 1 clique),
     PR `#40754` e PR `#40712` (resiliência contra exaustão de PIDs/processos em cgroups, contendo falha ao spawn individual e protegendo o daemon),
     PR `#40757` (exibição de credenciais herdadas e allowlist `passEnv` em scripts de receitas de ambiente) e
     PR `#40750` (rolagem suave e sem flicker no Claude Code em tela cheia).
3. **Atualização de 2 issues existentes em `work/issues/`:**
   - [Bifurcação de conversas no Chat UI e resiliência de inicialização do Claude](../issues/bifurcacao-de-conversas-no-chat-ui-e-resiliencia-de-inicializacao-do-claude.md):
     adicionado o PR `#40705` / issue `#40704` (bifurcação direta de chats para um novo worktree isolado com cópia nativa de conversação
     `destinationCwd` para Claude, Codex e ACP, além do modo "As a background subagent…" que reporta automaticamente via `orca orchestration send`).
   - [Histórico de navegação no editor e identificação de workspaces por plugins](../issues/historico-de-navegacao-no-editor-e-identificacao-de-workspaces-por-plugins.md):
     adicionado o PR `#40743` / issue `#40742` (extensão da API de plugins Host API 1.7 com `agents.list({ workspaceId? })` para listar agentes de qualquer
     workspace e `terminal.focus({ terminalId })` para trazer aba e painel de terminal para o primeiro plano via plugin).
