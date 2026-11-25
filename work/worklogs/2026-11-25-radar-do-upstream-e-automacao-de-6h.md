---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-25
completed: 2026-11-25
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

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-25)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):**
   - Buscados novos PRs, issues e commits criados ou atualizados entre `2026-11-24T21:00:00Z` e `2026-11-25T03:00:00Z` (range upstream `d7bd9c630bd..4843fe1b3de`, total de 85 commits incorporados no upstream e PRs/issues em aberto correspondentes).
   - Cruzamento e deduplicação com as issues existentes em `work/issues/` e o índice `.brza/index.jsonl`.

2. **Atualização das 10 issues temáticas rastreadas em `work/issues/` com preenchimento de prioridade (`priority: high`):**
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     - Incorporados os PRs `#48581` (bandeja de workers compacta em chip recolhível no composer), `#48564` e `#48598` (espaçamento e alinhamento visual da queued row de mensagens pendentes), `#48472` (chips de prompts sugeridos contextuais para o Codex no Native Chat), `#48666` e `#48528` (tratamento robusto de colagem direta de imagens da área de transferência no composer) e `#48609` (restauração determinística de foco no chat principal ao fechar sheet de subagente, resolvendo Issue `#48602`).
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     - Incorporados os PRs `#48562` (chat workers adormecem o workspace em vez de fechar a aba de chat), `#48202` (sincronização de arranque de workers estruturados sob wait-for-setup), `#48518` (descarte imediato de subagentes cancelados ou interrompidos pelo Codex), `#42264` (liberação incondicional de workers em `worker-release` com terminal PTY encerrado) e `#48427` (ação de Clear para limpar falhas de workers assentados no dock do Home Chat, resolvendo Issues `#48594`, `#48593`, `#48592`, `#48614`).
   - [Consumo de recursos em agentes, reaper de LSP e overhead de hooks](../issues/consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks.md):
     - Incorporados os PRs `#45956` (desalocação de buffers PTY e layouts de workspaces estacionados ou minimizados), `#48577` (fila estrita FIFO de execuções para `check:changed` entre worktrees), `#48486` (isolamento da home do servidor Codex impedindo varredura de `~/.codex`), `#48600` (substituição de spawn tradicional por `posix_spawn` nativo em subprocessos) e Issue `#48656` (amortecimento dinâmico em sondagens contínuas de telemetria).
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     - Incorporados os PRs `#48611` (links curtos seguros para autenticação OAuth do Claude em hosts remotos), `#48448` (tratamento ordenado de recusa prematura com retenção em buffer antes de `onRefusal`), `#48570` (token check explícito em erros HTTP 401 durante wake de agentes evitando falsos bloqueios de cota) e `#48246` (compartilhamento e colaboração de agentes e bots entre contas Orca distintas).
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     - Incorporados os PRs `#48451` (invalidação de cache e recarregamento de imagens locais ao focar a janela via refocus), `#48524` (recuperação e diagnóstico claro em falhas de migração na interface web pareada), `#48530` (limpeza atômica do selo Needs you ao responder perguntas e exibição de títulos descritivos em itens), `#48526` (preservação e recuperação de rascunhos em respostas de itens recusadas) e Issue `#48588` (coleta e expurgo programado de worktrees temporários órfãos de automações interrompidas).
   - [Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados](../issues/plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados.md):
     - Incorporados os PRs `#48607`, `#48572` e `#48565` (repo badges de 16px integrados diretamente na linha de título com cores de alto contraste), `#48489` (títulos legíveis de sessão com chip contextual de modelo), `#48561` (fixação da aba Home do bot permanentemente à esquerda na barra de abas), `#48554` (remoção da borda âmbar fixa na visualização de Activity) e Issues `#48625`, `#48651` (persistência estável da ordenação customizada de workspaces e boards no layout store).
   - [Badges de worktree para plugins, cadência de PR e redesenho de automações](../issues/badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes.md):
     - Incorporados os PRs `#47907` (retentativa de turnos vazios do Slack antes de falhar a entrega), `#47901` (aviso claro e explícito no Slack quando turnos do bot concluem sem prosa final), `#46794` (timer de disparo único de alta precisão com `--once --by`), `#48487` (exibição destacada do propósito e escopo do bot na tela pós-criação), `#47381` (sincronização de mascote e paleta visual do bot com o avatar do Slack), `#48496` (supressão transparente de tokens `NO_REPLY` em chats de grupo) e `#48477`, `#47789`, `#48621`, Issue `#48615` (propagação de cabeçalhos MCP estruturados no relay e follow-ups ancorados na mesma thread).
   - [Leitura antecipada e preservação de skills no arranque e nos plugins](../issues/leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins.md):
     - Incorporados os PRs `#48578` (verificação local prévia de skills antes de lookups remotos de release na rede), `#48610` (card compacto de atualização de CLI no rodapé inferior), `#48659` e `#48658` (provedor e gestão de servidores MCP por plugins via manifesto e CLI), `#48616` (recusa estrita de symlinks cross-device inseguros em pacotes de skills) e Issues `#48635`, `#48617` (resolução determinística de namespaces e isolamento de ferramentas MCP).
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     - Incorporados os PRs `#48305` e `#48304` (execução de todo chat no Antigravity sob o Native Chat com sign-in in-app integrado e listagem dinâmica de modelos via ACP), `#48525` (suporte a cliques e eventos de ponteiro em cross-site frames para captchas em páginas Server), `#48490` (navegação transparente no navegador embutido via túnel SSH para portas loopback remotas), `#48467` (destaque visual e confirmação de destino para downloads no setup do Google Connector), `#48556` (probes de release resilientes sob proxies corporativos com autenticação), `#48517` (expurgo imediato de update groups ao remover hosts) e Issues `#48657`, `#48645` (reconciliação atômica de geometria e buffers entre TUI e Native Chat).
   - [Progresso de revisão no diff, backend de métricas e abertura de pastas](../issues/progresso-de-revisao-no-diff-backend-de-metricas-e-abertura-de-pastas.md):
     - Incorporados os PRs `#48553` (poda de trabalho redundante de histórico no scope-menu de diff review, STA-17982..17986), `#48558` (suporte a PowerShell e encadeamento seguro de comandos em Look around no Windows), `#48520` (suporte a `--focus text` e reporte explícito de motivo formal de recusa de ferramentas), `#48587` (atribuição de mensagens de turnos em passagem única no SQLite, STA-18015), `#48493` (transporte de diagnósticos de chats que falharam no arranque de volta ao conector de origem), `#48663` (ação de executar scripts a partir do menu de contexto do File Explorer, resolvendo Issue `#48661`) e `#48650` (controles de zoom e pan no Workspace Board, resolvendo Issue `#48647`).

3. **Validação e auditoria das notas:**
   - Executado `python3 .claude/skills/notes-checker/scripts/check_notes.py --detail`, confirmando zero erros de sintaxe, frontmatter ou referências quebradas.
