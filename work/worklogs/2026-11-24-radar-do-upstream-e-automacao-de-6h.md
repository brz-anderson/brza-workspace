---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-24
completed: 2026-11-24
tags:
  - tooling
refs:
  - issue:alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas
  - issue:badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes
  - issue:consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks
  - issue:gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache
  - issue:leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados
  - issue:progresso-de-revisao-no-diff-backend-de-metricas-e-abertura-de-pastas
  - issue:protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle
  - issue:retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-24)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):**
   - Buscados novos PRs, issues e commits criados ou atualizados entre `2026-11-23T21:00:00Z` e `2026-11-24T03:00:00Z` (range upstream `dbb1cf1bc41..644d6778e61`, total de 82 commits incorporados no upstream e PRs/issues em aberto correspondentes).
   - Cruzamento e deduplicação estrita com as issues existentes em `work/issues/` e o índice `.brza/index.jsonl`.

2. **Atualização das 10 issues temáticas rastreadas em `work/issues/` com preenchimento de prioridade (`priority: high`):**
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     - Incorporados os PRs `#47980` (card flutuante de worker como pílula acima da caixa de mensagem), `#47949` (Add to chat em chips compactos), `#47929` (exibição de novos chats Claude e Codex na sidebar antes do primeiro envio), `#47878` (janela de journal com leitura apenas dos sends necessários), `#47959` (remoção da step bar e contagem em setas), `#47941` (manutenção do estado Needs you quando worker inicia com questão aberta), `#47934` (cancelamento instantâneo de itens de agentes sem diálogo de motivo), `#47815` (preload de histórico de sessão e busca `/resume` imediata) e `#47931` (filtro e contagem de itens por autor no Native Chat).
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     - Incorporados os PRs `#47947` (diagnóstico informativo quando worker fica silencioso), `#47887` (persistência de mudanças de turnos em 1s contra falhas de idle mail), `#47877` (cessação de envio de mensagens no shell após saída do OpenCode), `#47554` (execução do SQL da work store no worker do banco de bots), `#47548` (registro de workers sob a conversa de origem), `#47818` (distinção entre In progress e Waiting para workers próprios), `#47973` (preservação de contexto de handoff e limite de fan-out), `#47914` (distribuição equilibrada de turnos entre bots com fila única) e `#47953` (paginação retrógrada com `--cursor` em `orca agent read`).
   - [Consumo de recursos em agentes, reaper de LSP e overhead de hooks](../issues/consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks.md):
     - Incorporados os PRs `#47943` (delegação da varredura de portas locais no Linux com `ls -ln /proc/*/fd` fora do processo principal do Electron), `#47580` (boot sob demanda de workers de journal SQLite), `#47578` (inicialização lazy do backend de usage), `#47835` e `#47911` (supressão de lookups de workers vinculados para itens limitados por cota de uso e cache de workers assentados), `#44265` (reativação de watch de raízes locais após o resfriamento do fusível de crash), `#47821` e `#47900` (serialização de `check:changed` entre worktrees e reuso de grafo de importação), `#47836` e `#47853` (instalação de hooks gerenciados no local lido pelo Droid e isolamento de Task workers).
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     - Incorporados os PRs `#47858` (cessação de releituras redundantes de transcripts na alternância de worktrees), `#47834` (botão direto de Sign-in no cartão de conta Claude pendente), `#47804` (atualização dos planos Anthropic para Max e Ultra), `#47983` (leitura de histórico inicial do Claude em background worker), `#47948` (proteção de esperas de cota de bots contra mutações concorrentes), `#47910` (modelos de backup para failover automático de cotas de bots), `#47954` (multi-account orchestration com pools de contas, cotas configuráveis e roteamento por repositório e agente, refs `#47020`, `#45090`, `#44117`) e `#47933` (reversão de ocultação de uso na barra de status com chat em foco).
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     - Incorporados os PRs `#47952` (expurgo de pastas temporárias residuais de git deixadas por plugins), `#47657` (garantia de execução da conferência de histórico antigo de chat em todos os arranques sem deleções prematuras), `#47981` (espera de ociosidade `away` para aplicação de atualizações automáticas) e `#47906` (encerramento automático de conversas de automação concluídas após tempo ocioso).
   - [Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados](../issues/plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados.md):
     - Incorporados os PRs `#47915` (compactação do App Rail com botões de 28px e ícones de 16px), `#47884` (avatares recortados com dicas de status e destaque "Needs you" em bots colapsados, refs `#47693`), `#47935` (ação de delete na barra lateral atuando no workspace aberto quando não houver item selecionado), `#47922` (abertura de caminhos absolutos no worktree correspondente), `#47902` (disposição de bots fixados em duas colunas paralelas), `#47968` (manutenção de status fresco de PR de workspaces) e `#47871` (aumento de contraste entre aba ativa e abas inativas).
   - [Badges de worktree para plugins, cadência de PR e redesenho de automações](../issues/badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes.md):
     - Incorporados os PRs `#47879` (disparo de regras `from=me` para pull requests abertos sob a conta do dono), `#47865` (truncamento de rótulos longos de resultado de automação), `#47876` (precisão em horários de verão DST e validação rigorosa de `--timezone`), `#47855` (preservação de execuções abertas de automação durante o encerramento do app para reavaliação no startup), `#47938` (conclusão de automações retidas em sign-in como `skip` sem travar a fila) e `#47897` (reconciliação e despacho ordenado de ocorrências agendadas perdidas entre reinicializações, refs `#47888`).
   - [Leitura antecipada e preservação de skills no arranque e nos plugins](../issues/leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins.md):
     - Incorporados os PRs `#47895` (vinculação estrita do cache de listagem e prévia de skills no diálogo Share às pastas e build que os produziram), `#47979` (subida do resolvedor de pacotes até a raiz real ultrapassando marcadores `package.json` aninhados) e `#47797` (especificação de comandos de CLI e skills para work items do Azure Boards).
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     - Incorporados os PRs `#47955` (limpeza de cookies por perfil em qualquer host nas preferências, incluindo SSH), `#47970` (busca textual em perfis de Import Cookies), `#47827` (impressão em PDF de páginas streamed salva diretamente no Desktop), `#47577` (proteção de arquivos de sessão ilegíveis contra exclusão acidental na limpeza de cookies), `#47863` (retomada imediata do controle humano de páginas compartilhadas ao detectar input no viewer), `#47833` (resolução relativa de caminhos de arquivo em `orca exec`), `#47832` (respostas segmentadas acima de 4 MB em conexões pareadas para screenshots completos), `#47861`, `#47905`, `#47823`, `#47820`, `#47814`, `#47790` (redesenho dos cards Connect Google, setup de novas aplicações e desacoplamento de notificações no chat), `#47994` (port-forwarding de portas de servidores pareados para o navegador padrão), `#47957` (migração de abas de navegador entre computador e servidor pareado), `#47965` (diagnóstico explícito em falhas de abertura de link) e `#47944` (eliminação de recarga dupla em abas abertas por agentes/CLI).
   - [Progresso de revisão no diff, backend de métricas e abertura de pastas](../issues/progresso-de-revisao-no-diff-backend-de-metricas-e-abertura-de-pastas.md):
     - Incorporados os PRs `#47531` (prevenção de encerramento precoce de processos de terminal por marcas OSC emitidas pelo próprio agente), `#47932` (início imediato de seleção no primeiro clique do mouse em células de código de notebooks) e `#47870` (especificação de busca contínua transversal Cmd/Ctrl+F percorrendo todos os arquivos no diff combinado "View all changes").

3. **Validação e auditoria das notas:**
   - Executado `python3 .claude/skills/notes-checker/scripts/check_notes.py --detail`, confirmando zero erros de sintaxe, frontmatter ou referências quebradas.
