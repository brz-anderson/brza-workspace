---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-13
completed: 2026-11-13
tags:
  - tooling
refs:
  - issue:cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat
  - issue:controle-de-agentes-e-chats-pela-cli-por-id-de-sessao-e-rotulagem-de-contas
  - issue:historico-de-navegacao-no-editor-e-identificacao-de-workspaces-por-plugins
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:preservar-o-dono-do-painel-do-antigravity-em-subagentes-aninhados
  - issue:protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle
  - issue:retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot
  - issue:seguranca-de-hooks-em-worktrees-e-integridade-de-setup-em-automacoes
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-13)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-12T21:00:00Z` e `2026-11-13T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     rastreia o PR `#41757` (resolve Issue `#41756` — limpeza periódica com timer do banco `orchestration.db` expurgando Runs concluídos e itens relay expirados/unacked após período de retenção configurável para evitar crescimento descontrolado),
     PR `#41746` (despertar automático de coordenadores em sleep mode quando há mensagens ou resultados de workers pendentes em mailboxes de run/task),
     PR `#41702` (notificação proativa ao coordenador quando um worker fica silencioso no meio do turno por tempo excessivo, sem interromper prematuramente a tarefa),
     PR `#41729` (resolve Issue `#41726` — novo comando CLI `orca text generate` e método RPC para respostas rápidas de modelos sem ferramentas nem provisionamento de worktree) e
     PR `#41754` (resolve Issue `#40838` — suporte a envio de texto para terminais via stdin com `--text -` ou via arquivo com `--text-file <path>`).
3. **Atualização de 4 issues existentes em `work/issues/`:**
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionado o PR `#41766` (exibição de modelo, nível de esforço, ferramenta corrente em execução e resumo do resultado final para cada subagente na lista do Native Chat e Mobile, com hover card detalhado e campos opcionais no schema de journal).
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionados o PR `#41765` (varredura offline 4x mais rápida de cleanup de workspaces bloqueando downloads de rede do Git em clones parciais e acelerando busca de squashes com `--name-only`) e
     o PR `#41760` (execução automática de regras de cleanup de workspace em background por host via `WorkspaceCleanupRunner`, com revalidação estrita de evidências antes da exclusão).
   - [Cartões de Pull Request, feedback de Steer e atalhos no Native Chat](../issues/cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat.md):
     adicionados o PR `#41770` (configuração em *Settings → Chat → Behavior* para alternar o envio de mensagens entre Enter e Cmd/Ctrl+Enter, prevenindo envios prematuros em redação multilinha e digitação IME) e
     o PR `#41762` (alimentação da barra de uso do Claude com eventos `rate_limit_event` das mensagens de chat em tempo real, contornando falhas no endpoint `/api/oauth/usage`).
   - [Histórico de navegação no editor e identificação de workspaces por plugins](../issues/historico-de-navegacao-no-editor-e-identificacao-de-workspaces-por-plugins.md):
     adicionados o PR `#41768` (ordenação opcional de abas por mais recentemente usadas - MRU, promovendo abas ativas para a frente na digitação ou seleção por teclado) e
     o PR `#41767` (abertura direta de links Markdown visuais no navegador interno, suporte a clique médio para navegador externo e menu contextual de edição/cópia no hover).

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-13)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-13T03:00:00Z` e `2026-11-13T09:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Controle de agentes e chats pela CLI por ID de sessão e rotulagem de contas](../issues/controle-de-agentes-e-chats-pela-cli-por-id-de-sessao-e-rotulagem-de-contas.md):
     rastreia o PR `#41850` (subcomandos `orca chat send` e `orca chat close` para continuar chats existentes sem abrir novas abas e fechar abas programaticamente com histórico preservado),
     PR `#41815` (comandos unificados `orca agent list`, `show` e `read` por `orcaSessionId` conectando chats nativos e agentes de terminal com paginação e leitura sem acordar o processo) e
     PR `#41824` (resolve Issue `#21182` — ação Rename para contas salvas de Claude e Codex, exibição `Nome (email)` na interface, na status bar e seleção na CLI).
3. **Atualização de 4 issues existentes em `work/issues/`:**
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionados o PR `#41858` / STA-15099 (recuperação durável de exclusões de workspaces e checkpoints de estado em servidores pareados e headless),
     o PR `#41835` / STA-15114 (cancelamento imediato de varreduras locais de arquivos ignorados com `AbortController` ao fechar prévias de deleção) e
     o PR `#41833` (backend de arquivamento `worktree.archive` e restauração `worktree.restore` para liberar espaço em disco mantendo branch, metadados e histórico).
   - [Cartões de Pull Request, feedback de Steer e atalhos no Native Chat](../issues/cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat.md):
     adicionados o PR `#41800` / Issue `#41781` (navegação contínua entre todas as imagens da conversa no visualizador ampliado com setas e atalhos de teclado) e
     o PR `#41776` / Issue `#41353` (inclusão de perguntas assíncronas pendentes na projeção de atenção da sessão para evitar perda de foco de input).
   - [Histórico de navegação no editor e identificação de workspaces por plugins](../issues/historico-de-navegacao-no-editor-e-identificacao-de-workspaces-por-plugins.md):
     adicionados o PR `#41786` / Issue `#41783` (configuração opcional de clique simples ou duplo para abertura de arquivos no file explorer) e
     o PR `#41828` / Issue `#41827` (normalização Unicode NFC na busca de caminhos do Quick Open e do seletor `@` para suporte a acentos e coreano).
   - [Segurança de hooks em worktrees e integridade de setup em automações](../issues/seguranca-de-hooks-em-worktrees-e-integridade-de-setup-em-automacoes.md):
     adicionado o PR `#41823` (aprovação de comandos de setup pré-criação inspecionando o manifesto da branch base de origem, eliminando alertas falsos de divergência de comandos).
   - [Preservar o dono do painel do Antigravity em subagentes aninhados](../issues/preservar-o-dono-do-painel-do-antigravity-em-subagentes-aninhados.md):
     adicionado o PR `#41806` / Issue `#41857` (ignorar hooks de agentes filhos para proteger a sessão líder do painel contra falsos status `done` e notificações indevidas).

