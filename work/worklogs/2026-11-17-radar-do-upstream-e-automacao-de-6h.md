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
  - issue:chaveamento-automatico-de-contas-claude-por-limite-de-uso-e-planos-observados
  - issue:comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais
  - issue:fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks
  - issue:leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins
  - issue:modos-build-e-plan-e-ferramentas-de-artifacts-no-native-chat
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle
  - issue:retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot
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

### 3. Ciclo de 6h (12:00 BRT / 15:00 UTC em 2026-11-17)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-17T09:00:00Z` e `2026-11-17T15:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Atualização de 8 issues rastreadas em `work/issues/`:**
   - [Chaveamento automático de contas Claude por limite de uso e planos observados](../issues/chaveamento-automatico-de-contas-claude-por-limite-de-uso-e-planos-observados.md):
     adicionados o PR `#43578` (resolve Issue `#43579` — chaveamento automático de contas Claude ao atingir 95% do limite de uso da janela ativa),
     a Issue `#43594` (linhas detalhadas de cotas de 5h e semanal com contadores regressivos de reset no seletor de contas do Codex) e
     a Issue `#43375` (correção de persistência de credenciais ao alternar contas de provedor de IA).
   - [Modos Build e Plan e ferramentas de artifacts no Native Chat](../issues/modos-build-e-plan-e-ferramentas-de-artifacts-no-native-chat.md):
     adicionados o PR `#43606` (resolve Issue `#43603` — modo Plan nativo para agentes OpenCode no Native Chat) e
     a Issue `#43602` (ocultação de prosa emitida antes de `AskUserQuestion` enquanto o card de pergunta estiver pendente de resposta).
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados o PR `#43571` (fallback de esforço de raciocínio `xhigh`/`max` para `high` em modelos incompatíveis, extração limpa de mensagens de commit Git sem prefixo de hash e invalidação de catálogo) e
     o PR `#43564` (suporte a chat estruturado via CLI TRAE no Native Chat UI).
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados o PR `#43550` (aposentadoria paginada de Runs concluídas no banco de orquestração para evitar congelamentos na thread principal),
     a Issue `#43618` (tratamento de `worker_done` de workers conectados em servidores remotos rejeitados como dispatch desconhecido) e
     o PR `#43467` / PR `#43463` (resolve Issue `#43039` — reconciliação de reservas estruturadas na liberação de workers).
   - [Fontes web em plugins, isolamento de atalhos e resiliência de hooks](../issues/fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks.md):
     adicionados o PR `#43569` (resolve Issue `#42938` — pilha de fontes de fallback separadas por vírgula para Editor e Terminal),
     o PR `#43604` (suporte a configurações portáteis em `~/.orca/settings.json` para dotfiles) e
     a Issue `#43552` (suporte a layout ELK `layout: elk` em diagramas Mermaid na pré-visualização Markdown).
   - [Comandos shell no chat, recibos de perguntas e foco espacial em terminais](../issues/comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais.md):
     adicionados o PR `#43593` (escrita direta não bloqueante no descritor de PTY Unix para entrada de teclado imune a gargalos do pool de I/O workers) e
     o PR `#43574` (resolve Issue `#43573` — prevenção de auto-resume duplicado concorrente ao restaurar abas salvas se a conversa de agente já estiver ativa).
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados o PR `#43607` (resolve Issue `#43599` — presets rápidos de modelo, esforço de raciocínio e velocidade),
     o PR `#43600` (resolve Issue `#43595` — configuração `nativeChatSendKey` para envio com Shift+Enter),
     o PR `#43562` (listagem de painéis de agentes recém-iniciados no menu "Send notes to" via fallback de título de terminal),
     o PR `#43567` (sincronização do realce da view de Activity na barra lateral com o workspace e aba ativos),
     a Issue `#43610` (exibição de resumos de raciocínio intermediários do Claude entre chamadas de ferramentas),
     a Issue `#43549` (parse e estilização visual de tags `<advisory>` do harness OMP) e
     a Issue `#43597` (auto-hide da barra lateral com revelação por hover).
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionados o PR `#43587` (resolve Issue `#43539` — retenção de descritor aberto único por cursor no polling de transcripts Codex, eliminando `openSync` síncrono e travamentos de 5–9s no Windows),
     o PR `#43557` (renovação estrita de leases de chats ativos no startup sem regravar desnecessariamente todas as sessões salvas),
     o PR `#43563` (preenchimento incremental de baselines faltantes no upgrade com journal inalterado) e
     o PR `#43551` (resolve Issue `#43523` — contenção e recuperação de heap no scanner de sessões).

