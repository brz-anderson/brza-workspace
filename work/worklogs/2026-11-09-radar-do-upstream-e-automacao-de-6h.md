---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-09
completed: 2026-11-09
tags:
  - tooling
refs:
  - issue:alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas
  - issue:cofre-de-chaves-de-api-esforco-no-antigravity-e-resiliencia-de-automacoes
  - issue:comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais
  - issue:historico-de-navegacao-no-editor-e-identificacao-de-workspaces-por-plugins
  - issue:leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins
  - issue:plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados
  - issue:preservar-o-dono-do-painel-do-antigravity-em-subagentes-aninhados
  - issue:scripts-de-setup-em-pastas-landing-vazia-e-remote-control-no-claude
  - issue:seletor-de-branches-na-status-bar-e-suporte-a-workspaces-em-pastas-multirrepositorio
  - issue:validacao-de-conclusao-em-automacoes-cli-de-extensoes-e-destravamento-de-rate-limit
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-09)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-08T21:00:00Z` e `2026-11-09T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Scripts de setup em pastas, landing vazia e Remote Control no Claude](../issues/scripts-de-setup-em-pastas-landing-vazia-e-remote-control-no-claude.md):
     rastreia o PR `#40034` (execução de scripts de setup e archive em folder projects via capability `worktree.folder-setup.v1`,
     permitindo orquestrar criação de worktrees filhos em multirrepositórios),
     PR `#40024` / issue `#39267` (configuração `When a workspace has no tabs: Show empty workspace`, exibindo landing surface
     com atalhos em vez de abrir PTYs compulsórios ao ativar workspaces adormecidos),
     PR `#40020` / issue `#37502` (conexão automática de sessões de Native Chat ao Remote Control do Claude Code quando
     `remoteControlAtStartup` está ativo, sincronizando status online com app mobile e claude.ai/code),
     PR `#40017` / issue `#39942` (guarda em `agentSession.createSupport` que recusa a transição "Continue in Chat UI" antes de
     confirmar a escrita do transcript em disco pelo Claude CLI, evitando `transcriptNotFound` e perda de terminal),
     PR `#39992` (fixação Always on top e atalho global para evocar janelas flutuantes de chat/terminal a partir de qualquer app) e
     PR `#39958` (preservação de vínculo entre tarefas em segundo plano do Claude e seus subagentes pais após reinicialização do app).
3. **Atualização de 2 issues existentes em `work/issues/`:**
   - [Seletor de branches na status bar e suporte a workspaces em pastas multirrepositório](../issues/seletor-de-branches-na-status-bar-e-suporte-a-workspaces-em-pastas-multirrepositorio.md):
     adicionados o PR `#39999` (visualização de Source Control de pastas multirrepositório no aplicativo móvel) e o
     PR `#39977` (ação "Rename project" no menu de opções do cabeçalho de projetos na barra lateral).
   - [Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados](../issues/plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados.md):
     adicionados o PR `#40004` (suporte a menus nativos nos popouts da barra de trilho e nova configuração de estilo visual
     `sidebarStyle`) e o PR `#40023` (opção para transformar seções de host remoto em agrupamento explícito "Group by: Host").

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-09)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-09T03:00:00Z` e `2026-11-09T09:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     rastreia o PR `#40201` / issue `#40192` (alternância bidirecional entre terminal TUI e Native Chat para o agente Antigravity
     `agy` via `⌘⇧J` / menu de contexto no desktop e mobile, com decodificador para `transcript_full.jsonl`, suporte a `ask_question`,
     `ask_permission`, diffs e catálogo `agy models`),
     PR `#40228` (card inline `AgentSignInCard` e túnel de callback `network.authCallbackTunnel` para autorizar Claude e Codex
     em hosts remotos/SSH com 1 clique no navegador local sem transitar tokens),
     PR `#40229` / issue `#40227` (configurações estilo VS Code de dimensionamento de abas `tabSizing: auto | fit | shrink | fixed`,
     `tabSizingMinWidth` e `tabSizingMaxWidth` de 60px a 800px via variáveis CSS),
     PR `#40208` (instalação guiada e sign-in de agentes ausentes diretamente a partir do Native Chat),
     PR `#40175` / issues `#38971`, `#39454` (catálogo dinâmico de modelos da conta conectada no host para menus de configurações e lançamento),
     PR `#40171` (otimização de memória liberando payloads de helpers concluídos e eliminando varreduras de histórico em sessões longas) e
     PR `#40183` / issue `#15317` (reconciliação atômica de tarefas pendentes do Claude via transcript para destravar painéis presos em "Working").
3. **Atualização de 2 issues existentes em `work/issues/`:**
   - [Preservar o dono do painel do Antigravity em subagentes aninhados](../issues/preservar-o-dono-do-painel-do-antigravity-em-subagentes-aninhados.md):
     adicionado o PR `#40153` (endereça issue `#40100`), corrigindo a captura de PID de hooks do Antigravity ao desembrulhar
     o processo envoltório `sh -c` efêmero no Linux e macOS, impedindo o sumiço e recriação espúria da linha do agente na barra lateral.
   - [Leitura antecipada e preservação de skills no arranque e nos plugins](../issues/leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins.md):
     adicionado o PR `#40214` (resolve issue `#40181`), corrigindo o algoritmo de classificação de bundled skills para ignorar
     arquivos sidecar como `agents/openai.yaml` ou scripts locais, evitando falsa classificação como `edited` e destravar auto-updates.

### 3. Ciclo de 6h (12:00 BRT / 15:00 UTC em 2026-11-09)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-09T09:00:00Z` e `2026-11-09T15:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Cofre de chaves de API, esforço no Antigravity e resiliência de automações](../issues/cofre-de-chaves-de-api-esforco-no-antigravity-e-resiliencia-de-automacoes.md):
     rastreia o PR `#40303` (cofre local de chaves de API com injeção per-processo em agentes locais, SSH e pareados via
     capability `agent-session.key-env.v1`, sem persistir credenciais em disco remoto nem em perfis de shell),
     PR `#40308` / issue `#39556` (seleção de esforço no Antigravity CLI via ID do modelo em vez de flag `--effort` conflitante,
     prevenindo regressão silenciosa para o modelo padrão),
     PR `#40311` / issue `#39905` (flag `--on-no-reusable-session skip` em automações coordenadas, registrando `skipped_unavailable`
     em vez de abrir sessões concorrentes duplicadas),
     PR `#40331` (escopamento de parking de terminais e output watchers por workspace, mantendo integridade de títulos e sino em splits secundários),
     PR `#40298` / issue `#40165` (renomeação de servidores Orca remotos salvos nas configurações) e
     PR `#40295` / issue `#40204` (ignorar `AppData`, staging de instaladores e arquivos `.asar` em observadores de filesystem).
3. **Atualização de 1 issue existente em `work/issues/`:**
   - [Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados](../issues/plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados.md):
     adicionados o PR `#40334` / issue `#40333` (fixação de projetos, grupos e subgrupos via `isPinned` mantendo ancoragem no topo
     em ordenação manual e recent, e ordenação manual intercalada entre subgrupos e projetos dentro de grupos) e
     PR `#40323` / issue `#40322` (criação direta de grupos e subgrupos na sidebar via `NewProjectGroupButton`, menu hierárquico `Move to group`
     e drag-and-drop de reparenting transversal com cálculo geométrico de drop lines).

### 4. Ciclo de 6h (18:00 BRT / 21:00 UTC em 2026-11-09)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-09T15:00:00Z` e `2026-11-09T21:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Comandos shell no chat, recibos de perguntas e foco espacial em terminais](../issues/comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais.md):
     rastreia o PR `#40432` / issue `#32165` (execução direta de comandos shell iniciados por `!` no composer do Native Chat
     em aba de terminal dedicada do workspace, sem enviar prompts à LLM nem vazar saídas/tokens no transcript),
     PR `#40424` (recibos expansíveis de perguntas interativas `ask_question`, exibindo todas as alternativas ofertadas com
     marcação da resposta escolhida via disclosure inline),
     PR `#40420` / issue `#40408` (atalho configurável `workspace.sleep` em Settings → Shortcuts para suspender workspaces
     ativos ou cartões sob o cursor sem depender do menu de contexto),
     PR `#40404` (foco direcional espacial entre divisões de terminal `terminal.focusPaneLeft/Right/Up/Down` via `Cmd+Option+Setas`),
     PR `#40412` / issue `#39864` (retenção de auto-continue em Native Chat até que a conta recupere cota em janelas de 5h, semanal e mensal),
     PR `#40405` / issue `#40402` (propagação imediata de troca de modelo em sessões estruturadas ociosas do Claude via `canSetOptionWhileIdle`) e
     PR `#40398` / issue `#12572` (upload transparente de arquivos arrastados para sessões de chat em servidores pareados via `fs:uploadPathsToRuntimeTempFiles`).
3. **Atualização de 2 issues existentes em `work/issues/`:**
   - [Histórico de navegação no editor e identificação de workspaces por plugins](../issues/historico-de-navegacao-no-editor-e-identificacao-de-workspaces-por-plugins.md):
     adicionados o PR `#40345` / issue `#40343` (novo hook de worker `editor.inlineCompletion` permitindo que plugins forneçam
     sugestões inline em texto fantasma cinza aceitas via `Tab` no editor Monaco).
   - [Validação de conclusão em automações, CLI de extensões e destravamento de rate limit](../issues/validacao-de-conclusao-em-automacoes-cli-de-extensoes-e-destravamento-de-rate-limit.md):
     adicionados o PR `#40411` / issue `#40401` (correção em `orca agent hooks status` para checar conectividade real do runtime,
     reportar `appliedBy: runtime` e apontar o caminho SQLite `profile-state.db`).

