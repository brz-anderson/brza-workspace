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
  - issue:leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins
  - issue:plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados
  - issue:preservar-o-dono-do-painel-do-antigravity-em-subagentes-aninhados
  - issue:scripts-de-setup-em-pastas-landing-vazia-e-remote-control-no-claude
  - issue:seletor-de-branches-na-status-bar-e-suporte-a-workspaces-em-pastas-multirrepositorio
---

# Radar de issues e PRs do upstream e automação de 6h (00h e 06h BRT)

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

