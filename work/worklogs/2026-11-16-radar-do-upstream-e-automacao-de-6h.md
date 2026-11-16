---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-16
completed: 2026-11-16
tags:
  - tooling
refs:
  - issue:alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas
  - issue:aprovacao-de-planos-abc-feedback-de-revisao-inline-e-resiliencia-de-composer-no-chat
  - issue:card-unificado-de-agentes-com-abas-superiores-atalhos-e-barreira-de-setup
  - issue:cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat
  - issue:chaveamento-automatico-de-contas-claude-por-limite-de-uso-e-planos-observados
  - issue:consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks
  - issue:execucao-em-lote-no-computer-use-e-protecao-de-digitacao-segura
  - issue:git-blame-na-linha-do-cursor-e-rebase-pelo-source-control
  - issue:historico-de-navegacao-no-editor-e-identificacao-de-workspaces-por-plugins
  - issue:ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins
  - issue:protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle
  - issue:retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot
  - issue:seletor-de-branches-na-status-bar-e-suporte-a-workspaces-em-pastas-multirrepositorio
  - issue:servidor-mcp-stdio-na-cli-e-otimizacoes-de-captura-no-computer-use
  - issue:workers-de-plugins-em-hosts-remotos-e-gerenciamento-cli-de-ssh
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-16)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-15T21:00:00Z` e `2026-11-16T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 2 novas issues priorizadas em `work/issues/`:**
   - `priority: high` — [Execução em lote de ações no Computer Use, proteção de digitação segura e otimizações de acessibilidade](../issues/execucao-em-lote-no-computer-use-e-protecao-de-digitacao-segura.md):
     rastreia o PR `#42859` (resolve Issue `#42850` — execução em lote de até 50 ações sequenciais com `orca computer batch` mantendo diff baseline e economizando turnos),
     o PR `#42861` (resolve Issue `#42849` — bloqueio de injeção de teclas automatizadas se o operador estiver digitando ativamente ou sobre campos seguros de senha `NSSecureTextField`),
     o PR `#42855` (resolve Issue `#42848` — truncamento de nós fora da tela em listas e textos longos de snapshots de acessibilidade no macOS),
     o PR `#42842` (resolve Issue `#42843` — desativação de screenshots padrão após micro-ações de GUI, exigindo flag explícita `--screenshot`),
     os PRs `#42863` e `#42826` (resolvem Issues `#42846` e `#42825` — substituição de polling fixo de 200ms por subscrição direta a notificações de acessibilidade `AXUIElementRegisterForNotification`),
     o PR `#42816` (resolve Issue `#42815` — extração consolidada de atributos AX em chamada única via `AXUIElementCopyMultipleAttributeValues`),
     e os PRs `#42853` e `#42814` (resolvem Issues `#42841` e `#42813` — guias enxutos para orientar modelos ao caminho de menor custo de tokens em Computer Use).
   - `priority: high` — [Chaveamento automático de contas Claude por limite de uso, planos observados e resgate de cota](../issues/chaveamento-automatico-de-contas-claude-por-limite-de-uso-e-planos-observados.md):
     rastreia o PR `#42856` (chaveamento automático e transparente de conta do Claude ao atingir 100% da cota, selecionando a conta salva com reset mais próximo e reiniciando tarefas sem perda de contexto),
     o PR `#42917` (exibição da categoria de plano Free/Pro/Team/Enterprise em contas salvas de Claude e Codex),
     e o PR `#42891` (resolve Issue `#42887` — resgate de resets de cota do Claude diretamente pelo menu de contas do app).
3. **Atualização de 6 issues existentes em `work/issues/`:**
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados o PR `#42839` (resolve STA-15101 — expurgo de cópias resolvidas de chat de workers convertendo-as em referências leves, `auto_vacuum = INCREMENTAL` e ação 'Reclaim space' em *Settings › Agent orchestration*)
     e a Issue `#42852` (roteamento para o host criador original de ordens de Stop/Close em workers federados iniciados remotamente).
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados o PR `#42847` (resolve Issue `#40321` — suporte a Antigravity Native Chat no Windows conectando diretamente ao host `agy acp`)
     e o PR `#42896` (correção na deleção de tokens de autenticação garantindo que falhas em contas Gemini Enterprise apaguem `acp_business_token.json` e isolamento da variável `ELECTRON_RUN_AS_NODE=1`).
   - [Aprovação de planos A/B/C, feedback de revisão inline e resiliência de composer no Native Chat](../issues/aprovacao-de-planos-abc-feedback-de-revisao-inline-e-resiliencia-de-composer-no-chat.md):
     adicionados o PR `#42907` (Issues `#22316` e `#42609` — renderização de sugestão do próximo prompt do Claude como ghost text no composer vazio, aceita com <kbd>Tab</kbd> ou <kbd>→</kbd>)
     e o PR `#42895` (suporte completo ao Hermes Agent no Native Chat via servidor ACP com cartões de aprovação de edições e comandos).
   - [Workers de plugins em hosts remotos e gerenciamento CLI de SSH](../issues/workers-de-plugins-em-hosts-remotos-e-gerenciamento-cli-de-ssh.md):
     adicionado o PR `#42898` (resolve Issue `#37826` — comando `orca host add` na CLI para cadastro explícito e persistente de alvos SSH com retorno de seletor `--host ssh:<id>`).
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionados o PR `#42877` (exclusão segura e opt-in de histórico, rollouts do Codex e transcrições de agentes ao deletar workspaces)
     e o PR `#42905` / Issue `#42909` (reorganização visual de regras em seções manuais e automáticas e declaração de pastas regeneráveis em `orca.yaml`).
   - [Consumo de recursos em agentes: reaper de LSP e overhead de hooks](../issues/consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks.md):
     adicionados o PR `#42889` (resolve Issue `#42601` — remoção profunda e atômica de hooks, scripts, binários da PATH e serviços em background via `orca uninstall` e *Settings › Advanced*)
     e o PR `#42890` (política de aprovação única *Always trust* para comandos de setup em `orca.yaml` por repositório).
   - [Servidor MCP stdio na CLI, métricas com orca stats usage e automação de documentação](../issues/servidor-mcp-stdio-na-cli-e-otimizacoes-de-captura-no-computer-use.md):
     adicionado o PR `#42812` (resolve Issue `#41618` — subcomando `orca stats usage` e RPC `stats.usage` para consumo direto e conciso de métricas agregadas de tokens e custos estimados por modelo e projeto).

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-16)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados PRs e issues abertos criados ou atualizados entre `2026-11-16T03:00:00Z` e `2026-11-16T09:00:00Z`, comparando com as notas existentes em `work/issues/` e o índice `.brza/index.jsonl`.
2. **Criação de nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Git Blame inline na linha do cursor, rebase pelo Source Control e suporte a submódulos](../issues/git-blame-na-linha-do-cursor-e-rebase-pelo-source-control.md):
     rastreia o PR `#42982` (`feat(editor): git blame for the cursor line` — exibe autor, tempo relativo e mensagem de commit na linha ativa sob o cursor no editor com atualização assíncrona),
     o PR `#42949` (`feat(source-control): rebase from the base-branch row` — ação assistida de rebase direto na linha da branch base no painel Source Control),
     o PR `#42997` (`feat(plugins): let workspace.create set the branch name` — permissão para que plugins e rotinas de orquestração especifiquem `branchName` na criação de workspaces),
     e a Issue `#42924` (demanda e arquitetura para suporte nativo de primeira classe a submódulos Git nos workspaces gerenciados).
3. **Atualização de 5 issues rastreadas em `work/issues/`:**
   - [Aprovação de planos A/B/C, feedback de revisão inline e resiliência de composer no Native Chat](../issues/aprovacao-de-planos-abc-feedback-de-revisao-inline-e-resiliencia-de-composer-no-chat.md):
     adicionados o PR `#42975` (permite selecionar o modelo a ser utilizado no próximo turno enquanto o agente ainda está processando o turno atual),
     o PR `#42981` (`fix(acp): keep saved chats retryable after temporary restore failures` — mantém chats salvos passíveis de retry após falhas transitórias de conexão ACP),
     o PR `#43020` (`fix(native-chat): resend a subscriber's snapshot when its capture was abandoned` — retransmissão de snapshots para subscritores de chat quando capturas prévias foram abandonadas),
     o PR `#43007` (`fix(native-chat): an upgrade no longer reopens closed chats or copies unchanged ones` — protege contra reabertura acidental de abas encerradas em atualizações do app),
     e o PR `#42942` (espaçamento vertical padronizado sobre a action row de resposta).
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados o PR `#42933` (`feat(antigravity): support Orchestrator mode and native auto/plan execution modes` — suporte ao Antigravity atuar no papel de Orchestrator e alternar entre modos de execução nativos `plan` e `auto`)
     e o PR `#42940` (padronização de IDs de novos agentes como UUIDs puros).
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionado o PR `#43016` (`fix(orchestration): keep a refused escalation or decision_gate out of the recipient's mailbox` — isolamento de solicitações de escalation ou decision_gate recusadas fora da caixa postal do destinatário original).
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionados o PR `#42959` (configuração dedicada para exclusão de chats do Claude Code vinculados a workspaces removidos),
     o PR `#43000` (exclusão de histórico do Codex junto ao workspace),
     o PR `#43015` (exclusão de conversas do Orca Chat com histórico ao remover workspace),
     e o PR `#42943` (`fix(workspaces): reopen unsaved editor drafts for workspaces that vanished while closed` — preservação e reabertura de buffers não salvos de workspaces que desapareceram externamente com o app fechado).
   - [Workers de plugins em hosts remotos e gerenciamento CLI de SSH](../issues/workers-de-plugins-em-hosts-remotos-e-gerenciamento-cli-de-ssh.md):
     adicionado o PR `#42984` (`feat(ssh): let the host move Orca's server and data out of the login home` — suporte para realocação de dados e servidor do daemon para fora do `$HOME` do usuário SSH via config/ambiente).
   - [Consumo de recursos em agentes: reaper de LSP e overhead de hooks](../issues/consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks.md):
     adicionados o PR `#42964` (resolve Issue `#42921` — elevação do heap do scanner de sessões do AI Vault para 768 MB configuráveis para estancar crashes de OOM),
     o PR `#43004` (cache de nomes de terminal no macOS reduzindo varreduras caras na tabela de processos),
     e o PR `#42935` (aprovação única e durável de setup hooks de `orca.yaml` no cliente móvel).

### 3. Ciclo de 6h (12:00 BRT / 15:00 UTC em 2026-11-16)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-16T09:00:00Z` e `2026-11-16T15:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Card unificado de agentes com abas superiores, atalhos de teclado e barreira de setup](../issues/card-unificado-de-agentes-com-abas-superiores-atalhos-e-barreira-de-setup.md):
     rastreia o PR `#43082` (`feat(agent): one agent picker card with agent tabs on top` — unifica os dropdowns de seleção de agente em um único card com abas de ícones no topo, busca global, escolha de modelo, esforço de raciocínio e toggle segmentado Chat vs CLI),
     o PR `#37434` (resolve Issue `#37433`, `#43071` — navegação 100% por teclado no painel Agents / AI Vault com atalhos configuráveis de foco, alternância de escopo Workspace/Project/All e retorno ao terminal via Esc),
     o PR `#43153` (STA-15243, STA-13006 — barreira de Setup obrigatório antes da inicialização de agentes e entrega de rascunhos vinculados de issues),
     o PR `#40407` (suporte nativo ao agente MiniMax Code com modelos de chat),
     o PR `#39855` (abertura de links do terminal em Floating Workspaces) e
     a Issue `#43126` (sinal de draft pronto em workers Muse no Windows).
3. **Atualização de 6 issues existentes em `work/issues/`:**
   - [Chaveamento automático de contas Claude por limite de uso, planos observados e resgate de cota](../issues/chaveamento-automatico-de-contas-claude-por-limite-de-uso-e-planos-observados.md):
     adicionados o PR `#43135` (resolve Issue `#9496` — fixação de worktree a uma conta específica de Claude ou Codex, evitando contaminação de cotas entre repositórios distintos),
     o PR `#43145` (retenção de novas mensagens de chat até que a conta alternada esteja pronta para execução),
     o PR `#43105` (configuração para migrar automaticamente todas as sessões em execução na troca de conta),
     o PR `#43087` (atribuição correta de métricas de telemetria e planos pela conta real da leitura e não pela linha focada na UI),
     o PR `#43118` (preservação do histórico de conversas pertencentes a contas removidas do Claude),
     o PR `#37943` (reinício transparente de sessões na nova conta) e
     o PR `#37998` (fluxo de sign-in limpo na troca de conta do Antigravity Chat).
   - [Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](../issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md):
     adicionados o PR `#43057` e a Issue `#43055` (`feat(cli): let agents list and read native chat sessions` — comandos na CLI para agentes listarem sessões e lerem transcrições completas do chat nativo de forma programática).
   - [Histórico de navegação no editor e identificação de workspaces por plugins](../issues/historico-de-navegacao-no-editor-e-identificacao-de-workspaces-por-plugins.md):
     adicionados o PR `#43132` (resolve Issue `#43130` — abertura direta de arquivos importados via <kbd>⌘Click</kbd> / <kbd>Ctrl+Click</kbd> no caminho do import),
     o PR `#41132` (indicadores visuais de modificação Git no gutter do editor Monaco),
     os PRs `#43111` e `#43103` (resolvem Issue `#43100` — realce de palavras-chave de controle de fluxo idêntico aos temas do VS Code),
     o PR `#43094` (contador de palavras em tempo real na barra de status para documento inteiro e seleções ativas),
     o PR `#43144` (resolve Issue `#43143` — preservação de scroll, zoom e viewport em custom editors de plugins na alternância de abas) e
     o PR `#43137` (resolve Issue `#43136` — método `raiseWindow` na API de plugins para trazer o app para frente).
   - [Seletor de branches na status bar e suporte a workspaces em pastas multirrepositório](../issues/seletor-de-branches-na-status-bar-e-suporte-a-workspaces-em-pastas-multirrepositorio.md):
     adicionados o PR `#43157` (resolve Issue `#43156` — sugestão automática de checkouts Git existentes ao definir a localização de um projeto no host),
     o PR `#43121` e o PR `#33600` (exibição de folder workspaces pinados no topo da sidebar e filtragem estrita por projeto selecionado) e
     o PR `#43113` (recolhimento e ocultação de projetos movidos no WSL).
   - [Cartões de Pull Request, feedback de Steer e atalhos no Native Chat](../issues/cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat.md):
     adicionados o PR `#43119` (resolve Issue `#43114` — exibição explícita de aprovadores e revisores pendentes no painel de Checks de PRs),
     o PR `#43124` (resolve Issue `#43122` — resumo retrátil "N files changed" para listas longas de arquivos modificados por turno),
     o PR `#43060` (resolve Issue `#43059` — menção de agentes arrastando o card da barra lateral para dentro do composer),
     o PR `#43141` (isolamento entre envios de chat e a linha de entrada do terminal para evitar comandos misturados) e
     o PR `#43093` (despacho de correio de agentes como ponteiro leve e autorização direta de ações negadas).
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados o PR `#43049` (suporte a flags remotas e execução headless em SSH/WSL para Antigravity),
     o PR `#43101` (medição de uso real e estimativas de custos de API do Antigravity no AI Vault) e
     as Issues `#43154` e `#43155` (correção da perda de modelo em follow-up e retomada de conversas `agy --conversation <id>`).
   - [Consumo de recursos em agentes: reaper de LSP e overhead de hooks](../issues/consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks.md):
     adicionados o PR `#43081` (Issue `#43095` — supressão de scripts de hooks fora de painéis Orca, cortando processos repetidos de `ps`),
     o PR `#43106` (resolve Issue `#43104` — resumo de uso de contexto eliminando rajadas de chamadas `count_tokens`),
     o PR `#43090` (resolve Issue `#40261` — reaper periódico de PTYs desacoplados de agentes no daemon),
     o PR `#43142` (eliminação de rebuilds a cada 20s na lista de títulos do AI Vault),
     o PR `#43164` (isolamento de leituras de fingerprint Git fora da libuv pool principal) e
     o PR `#43129` (resolve Issue `#40636` — suspensão de sondagens de PATH no Windows para agentes desabilitados).
