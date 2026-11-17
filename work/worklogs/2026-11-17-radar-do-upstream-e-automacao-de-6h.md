---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-17
completed: 2026-11-17
tags:
  - tooling
refs:
  - issue:alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas
  - issue:cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat
  - issue:comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais
  - issue:fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks
  - issue:leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle
  - issue:seletor-de-branches-na-status-bar-e-suporte-a-workspaces-em-pastas-multirrepositorio
  - issue:vazamento-de-memoria-gpu-webgl-no-terminal-e-performance-macos
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-17)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-16T21:00:00Z` e `2026-11-17T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Atualização de 5 issues rastreadas em `work/issues/`:**
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados o PR `#43385` (resolve Issue `#43366` — faixa contextual e link de navegação quando um agente de chat migra para outro worktree) e
     o PR `#43380` (restauração da entrega direta e síncrona de mensagens de outros agentes no chat nativo).
   - [Cartões de Pull Request, feedback de Steer e atalhos no Native Chat](../issues/cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat.md):
     adicionados o PR `#43392` (envio imediato de Steer com <kbd>Cmd/Ctrl+Enter</kbd> no chat nativo sem exibir estado espúrio de cartão enfileirado),
     o PR `#43345` (aviso compacto de cota e limite de uso de IA em linha única condensada no topo da conversa) e
     o PR `#43331` (indicação de pasta correta quando a conversa pertence a outro worktree, evitando falsos retries).
   - [Comandos shell no chat, recibos de perguntas e foco espacial em terminais](../issues/comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais.md):
     adicionados o PR `#43388` e o PR `#43393` (resolvem Issue `#43387` — execução em um clique no terminal e no mobile de linhas `! command` sugeridas por agentes).
   - [Fontes web em plugins, isolamento de atalhos e resiliência de hooks](../issues/fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks.md):
     adicionado o PR `#43389` (resolve Issue `#43379` — aplicação do ambiente de `agent.launch.before` de plugins com precedência sobre o ambiente de conta do host).
   - [Seletor de branches na status bar e suporte a workspaces em pastas multirrepositório](../issues/seletor-de-branches-na-status-bar-e-suporte-a-workspaces-em-pastas-multirrepositorio.md):
     adicionados o PR `#43351` (resolve Issue `#43373` — faixas alternadas por projeto e densidade vertical compacta na barra lateral de worktrees),
     o PR `#43319` (preservação do título da primeira tarefa resolvida na sidebar após renomeação de branch) e
     as Issues `#43384` e `#43383` (ações de criação direta de workspace e suspensão em lote de projeto no menu de contexto da sidebar).
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionado o PR `#43363` (consulta e listagem de modelos no agent picker do Antigravity a partir da conta configurada para a nova sessão de chat).

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-17)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-17T03:00:00Z` e `2026-11-17T09:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Atualização de 6 issues rastreadas em `work/issues/`:**
   - [Vazamento de memória GPU WebGL no terminal e performance no macOS](../issues/vazamento-de-memoria-gpu-webgl-no-terminal-e-performance-macos.md):
     adicionados o PR `#43465` e a Issue `#43464` (reconstrução dos renderizadores `WebglRenderer` e descarte de contexto de textura ao atingir páginas de 4096² no glyph atlas, eliminando acúmulo de até 6 GB de VRAM no processo `Orca Helper (GPU)` no macOS).
   - [Leitura antecipada e preservação de skills no arranque e nos plugins](../issues/leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins.md):
     adicionados o PR `#43436` (retenção estrita de escopos de skills ao selecioná-las pelo seletor `/` do Native Chat) e
     a Issue `#43418` (harmonização entre o registro bundled `computer-use` e o repositório comunitário `orca-computer-use` para viabilizar instalação via CLI).
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados o PR `#43521` (banner de worker temporário no topo de chat workers),
     o PR `#43425` (resolve Issue `#43424` — identificação visual com nome e ícone de plugins remetentes de mensagens no chat),
     o PR `#43474` (retenção de conversas aguardando confirmação humana na fila de reinício pendente sem auto-retomada indevida),
     o PR `#43456` (limitação de memória em filas de eventos de entrega e buffers de histórico atrasados),
     o PR `#43516` (montagem tardia/lazy de abas de chat ocultas para acelerar o carregamento de workspaces) e
     as Issues `#43462` (autocompletar com menções `@` para outros chats e terminais no composer) e
     `#43461` (citações como chips visuais clicáveis com salto de navegação para a posição de origem).
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionados o PR `#43498` (cards de worktrees agrupados por repositório, etapas distintas de confirmação e deleção e card de progresso em background no Workspace Cleanup),
     o PR `#43525` (resolve Issue `#43523` — liberação imediata de metadados retidos em streaming e controle de heap no scanner do AI Vault) e
     o PR `#43532` (resolve Issue `#43368` — remoção limpa de worktrees irmãos externos sem disparar verificações bloqueantes de reautorização).
   - [Comandos shell no chat, recibos de perguntas e foco espacial em terminais](../issues/comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais.md):
     adicionados o PR `#43431` (ação `Move Tab to Split` configurável e bindável em todas as direções cardeais),
     o PR `#43479` (interrupção forçada do processo PTY no encerramento de terminal via CLI quando a janela não confirmar) e
     o PR `#42651` (comando CLI para fechar diretamente abas de terminais já parados indicando seu ID).
   - [Seletor de branches na status bar e suporte a workspaces em pastas multirrepositório](../issues/seletor-de-branches-na-status-bar-e-suporte-a-workspaces-em-pastas-multirrepositorio.md):
     adicionados o PR `#43488` (resolve Issue `#43487` — identificação do nome do worktree corrente no cabeçalho do File Explorer),
     o PR `#43493` (suporte a movimentação e renomeação de projetos sob letras de drive mapeadas no WSL) e
     a Issue `#43443` (botões de ação rápida "New File" e "New Folder" na toolbar do File Explorer).
