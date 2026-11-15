---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-15
completed: 2026-11-15
tags:
  - tooling
refs:
  - issue:agente-kiro-no-native-chat-janela-flutuante-e-enderecamento-de-workspaces
  - issue:alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas
  - issue:aprovacao-de-planos-abc-feedback-de-revisao-inline-e-resiliencia-de-composer-no-chat
  - issue:avaliacao-comparativa-de-agentes-via-cli-e-revisao-de-diff-com-ia-no-source-control
  - issue:cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat
  - issue:conectores-de-linhagem-na-sidebar-cores-de-grupos-e-isolamento-de-extensoes
  - issue:consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks
  - issue:cursor-no-chat-via-acp-previa-de-links-de-imagem-bifurcacao-resiliente-e-leitura-por-voz
  - issue:integracao-nativa-do-devin-no-chat-respostas-a-mensagens-especificas-e-abertura-de-arquivos-alterados
  - issue:isolamento-de-artefatos-temporarios-de-chat-e-estudio-de-temas-via-cli
  - issue:plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados
  - issue:projecoes-sqlite-de-native-chat-submenu-de-agentes-e-links-no-terminal
  - issue:redesenho-de-cartoes-de-resposta-progresso-por-etapas-e-fila-de-mensagens
  - issue:retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot
  - issue:retomada-de-sessoes-gravadas-pela-cli-hosts-de-workspace-e-replay-de-terminal
  - issue:servidor-mcp-stdio-na-cli-e-otimizacoes-de-captura-no-computer-use
  - issue:worktrees-com-clones-copy-on-write-prompt-inicial-de-workspace-e-ack-seletivo-de-inbox
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-15)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-14T21:00:00Z` e `2026-11-15T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Redesenho de cartões de resposta, progresso por etapas e fila de mensagens](../issues/redesenho-de-cartoes-de-resposta-progresso-por-etapas-e-fila-de-mensagens.md):
     rastreia o PR `#42515` (redesenho completo do *Answer card* com ladrilhos preenchidos, barra de progresso segmentada, botões de avanço e submissão, fila de mensagens acoplada atrás do composer com ações de repetição/limpeza e dock adaptativo para painéis curtos),
     o PR `#42520` (steers no Claude movendo subagentes e comandos de primeiro plano para segundo plano e enviando com prioridade `now` para resposta imediata sem bloqueio),
     o PR `#42524` (exibição de detalhes e logs de diagnóstico sob o botão "Details" quando o chat do Claude falha ao inicializar),
     o PR `#42496` (recolhimento/dobra correto de turnos concluídos cujos registros em cache ainda não foram carregados),
     e os PRs `#42529`, `#42546` e `#42550` (otimizações de streaming com reutilização estável de identidades de painéis, isolamento de assinaturas da sidebar e loteamento de status).
3. **Atualização de 6 issues existentes em `work/issues/`:**
   - [Retomada de sessões gravadas pela CLI, hosts de workspace e replay de terminal](../issues/retomada-de-sessoes-gravadas-pela-cli-hosts-de-workspace-e-replay-de-terminal.md):
     adicionados o PR `#42555` (resolve Issue `#42553` — flag `focused` em `orca terminal list --json` e novo comando `orca terminal watch-focus` via long-poll RPC para acompanhar o painel focado em tempo real),
     o PR `#42580` (resolve Issue `#35719` — remoção profunda de abas salvas, layouts, scrollback e placeholders de workspaces excluídos, reduzindo em até 65% o tamanho do arquivo de sessão),
     e o PR `#42504` (leitura delimitada de stdin no statusline do Claude no Windows para evitar processos órfãos).
   - [Cartões de Pull Request, feedback de Steer e atalhos no Native Chat](../issues/cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat.md):
     adicionados o PR `#42579` (resolve Issue `#42059` — abertura confiável de links no terminal via middle-click sem acionar colagem acidental de texto selecionado no macOS e Linux),
     e o PR `#42544` (ação rápida de um clique para adotar <kbd>⌘K</kbd> / <kbd>Ctrl+K</kbd> para busca global nos perfis existentes).
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados o PR `#42506` (seletor dinâmico de conta para Claude ou Codex no lançamento de chats e terminais),
     a Issue `#42512` (eliminação de falso fallback para o runtime gerenciado de 337 MB no Antigravity Chat por marcador temporário de timeout do chaveiro),
     e a Issue `#42589` (prevenção de crash e perda irrecuperável de sessão ao alternar de terminal para chat estruturado).
   - [Isolamento de artefatos temporários de chat e estúdio de temas via CLI](../issues/isolamento-de-artefatos-temporarios-de-chat-e-estudio-de-temas-via-cli.md):
     adicionados o PR `#42563` (comando `orca theme publish` para empacotar e publicar temas no GitHub com validação de contraste e confirmação `--yes`),
     e o PR `#42536` (preservação de contraste e legibilidade para seleções de texto no editor de código quando a aba perde o foco).
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionado o PR `#42535` (resolve Issue `#42148` — validação rigorosa e rejeição de corpos vazios ou apenas espaços em branco em mensagens `worker_done`, mantendo a tarefa aberta para evitar perda de relatórios).
   - [Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados](../issues/plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados.md):
     adicionados o PR `#42558` (relacionado a `#41707` e `#28300` — suporte a ícones SVG personalizados delimitados e servidos com segurança para painéis de plugins na activity-bar/sidebar),
     e a Issue `#42575` (propagação da família tipográfica do Studio para frames de plugins via variável CSS `--orca-font-family`).
   - [Conectores de linhagem na sidebar, cores de grupos de projeto e isolamento de extensões em perfis](../issues/conectores-de-linhagem-na-sidebar-cores-de-grupos-e-isolamento-de-extensoes.md):
     adicionado o PR `#42574` (resolve Issue `#42556` — início do cronômetro de expiração de cache de prompt do Claude na sidebar restrito aos momentos posteriores ao envio real de requisições de IA).

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-15)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-15T03:00:00Z` e `2026-11-15T09:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Integração nativa do Devin no chat, respostas a mensagens específicas e abertura de arquivos alterados](../issues/integracao-nativa-do-devin-no-chat-respostas-a-mensagens-especificas-e-abertura-de-arquivos-alterados.md):
     rastreia o PR `#42598` (resolve Issue `#30791` — integração do Devin como agente estruturado ACP com migração *in-place* de sessões de terminal, mapeamento de `run_subagent` no roster e geração de títulos e texto *one-shot* via `devin --print`),
     o PR `#42650` (resposta direta com citação a mensagens específicas com faixa "Replying to …", citação de até 500 caracteres, salto de rolagem e botão dedicado de rewind),
     e o PR `#42647` (abertura direta de arquivos HTML no navegador integrado com auto-refresh e visualização direta de Markdown a partir de cartões de resumo do chat e visualizadores de diffs do Source Control).
3. **Atualização de 5 issues existentes em `work/issues/`:**
   - [Cursor no Chat via ACP, prévia de links de imagem, bifurcação resiliente e leitura por voz](../issues/cursor-no-chat-via-acp-previa-de-links-de-imagem-bifurcacao-resiliente-e-leitura-por-voz.md):
     adicionados o PR `#42654` (resolve Issue `#42653` — síntese e leitura de respostas em voz alta no cliente mobile usando a voz nativa do smartphone),
     o PR `#42646` (resolve Issue `#42645` — visualização em tela cheia de blocos de código com rotulagem automática de cercas sem linguagem no mobile),
     o PR `#42639` (resolve Issue `#42631` — Context Sheet unificado no mobile para câmera direta, fotos recentes e arquivos do workspace),
     o PR `#42590` (rastreamento e reabertura correta de conversas do OpenCode após movimentação de pastas de projetos),
     e a Issue `#42602` (prevenção de seletor TUI indevido em `/models` do OpenCode no app móvel).
   - [Retomada de sessões gravadas pela CLI, hosts de workspace e replay de terminal](../issues/retomada-de-sessoes-gravadas-pela-cli-hosts-de-workspace-e-replay-de-terminal.md):
     adicionados o PR `#42651` (resolve Issue `#40329` — novo comando `orca terminal close --tab-id <tabId>` para fechamento programático seguro de abas de terminais já inativos/mortos com proteção `terminal_tab_live`),
     o PR `#42614` (resolve Issue `#30621` — compartilhamento unificado do histórico do Codex em `~/.codex` entre todas as contas via links/junctions sem duplicação de dados),
     e a Issue `#42619` (mitigação de travamentos de sincronização e telas congeladas em hosts de terminal legados).
   - [Isolamento de artefatos temporários de chat e estúdio de temas via CLI](../issues/isolamento-de-artefatos-temporarios-de-chat-e-estudio-de-temas-via-cli.md):
     adicionados o PR `#42612` (motor determinístico e unificado de contraste de cores com sonda pura de luminância e tabela de conformidade WCAG integradas na CLI e UI),
     e o PR `#42623` (ferramenta `orca theme specimen` para inspeção comparativa de componentes em modos claro e escuro simultaneamente com alertas de coerência e contraste).
   - [Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados](../issues/plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados.md):
     adicionados o PR `#42658` (resolve Issue `#42657` — preservação da extensão correta registrada por plugins no primeiro salvamento "Save as" de arquivos gerados),
     a Issue `#42632` (persistência e execução contínua de painéis de plugins em background na sidebar ao alternar de aba),
     e o PR `#42638` (relacionado a `#42637` — estabilização de subpastas `source.path` combinadas com workers assíncronos em plugins).
   - [Consumo de recursos em agentes: reaper de LSP e overhead de hooks](../issues/consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks.md):
     adicionados o PR `#42660` (resolve Issue `#19116` — suspensão de loops de renderização e descarregamento de memória GPU para abas não observadas no `orca serve`),
     o PR `#42655` (dreno imediato de entrada e saída rápida de hooks executados fora do contexto de automação do Orca),
     e a Issue `#42601` (desativação limpa e tratamento de hooks órfãos de python3 após remoção do aplicativo).

### 3. Ciclo de 6h (12:00 BRT / 15:00 UTC em 2026-11-15)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-15T09:00:00Z` e `2026-11-15T15:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Aprovação de planos A/B/C, feedback de revisão inline e resiliência de composer no Native Chat](../issues/aprovacao-de-planos-abc-feedback-de-revisao-inline-e-resiliencia-de-composer-no-chat.md):
     rastreia o PR `#42740` (resolve Issue `#42736` — aprovação de planos com opções estruturadas A/B/C: `allowAcceptEdits`, `allow`, `deny`, atalhos `1`/`2`/`3`, caixa inline "Other" para revisão via <kbd>⌘Enter</kbd> / <kbd>Ctrl+Enter</kbd> e recibos `<opção> · <feedback>`),
     o PR `#42695` (preservação do rascunho de mensagem e estado do composer em reconexões e troca de abas),
     o PR `#42710` (pausa automática de chats ocultos em segundo plano para aceleração de troca de abas),
     o PR `#42704` (resolve Issue `#42701` — retentativa automática com backoff em erros transitórios `-32603` de RPC em `session/load` e `session/resume`),
     o PR `#42705` (resolve Issue `#42703` — logs de recusa de parada de chat em repouso de workspace),
     a Issue `#42706` (enfileiramento resiliente de inserção imediata/Steer sem bloqueio de navegação),
     e a Issue `#42720` (reabertura de abas de chat fechadas via <kbd>⌘Shift+T</kbd> / <kbd>Ctrl+Shift+T</kbd>).
3. **Atualização de 4 issues existentes em `work/issues/`:**
   - [Agente Kiro no Native Chat, janela flutuante e endereçamento de workspaces](../issues/agente-kiro-no-native-chat-janela-flutuante-e-enderecamento-de-workspaces.md):
     adicionados o PR `#42739` (janelas satélite de workspace multijanela sob a flag `experimentalWorkspacePopout`, sobrevida de PTY na janela principal entre popout/dock, guarda STRIDE no IPC e recuperação multi-monitor),
     a Issue `#42721` (ação para redefinir a geometria e tamanho do Floating Workspace para o layout padrão),
     e os PRs `#42741` e `#42737` (preservação de titularidade de escopo de workspace em abas de navegador sidecar Electron e no `orcad`).
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados o PR `#42747` (resolve Issue `#42732` — flag `--run` na CLI `orca orchestration inbox` para filtrar por Run ativo),
     o PR `#42708` (contabilização atômica de prompt aprovado durante execução da ferramenta vinculada),
     o PR `#42707` (paginação de leituras de workers de chat e projeção estável de frota),
     a Issue `#42731` (descarte de alarmes falsos para recusas de `decision_gate` por não-atribuídos),
     a Issue `#42719` (terminais coordenadores ocultos para execuções de orquestração),
     e as Issues `#42733` e `#42734` (redução de 70% no payload JSON de `worktree ps/list` e inclusão de worktree/título em recibos de `worker-start`).
   - [Projeções SQLite de Native Chat, submenu de agentes e links no terminal](../issues/projecoes-sqlite-de-native-chat-submenu-de-agentes-e-links-no-terminal.md):
     adicionados o PR `#42738` (resolve Issue `#42730` — ação direta "Resume session…" no painel de configuração do menu `+` de novos agentes com pré-filtragem da sessão e retomada com ▶),
     e a Issue `#42673` (suporte à importação e retomada de sessões do DSH Harness `.dsh`).
   - [Worktrees com clones Copy-on-Write, prompt inicial de workspace e ack seletivo de inbox](../issues/worktrees-com-clones-copy-on-write-prompt-inicial-de-workspace-e-ack-seletivo-de-inbox.md):
     adicionados o PR `#42709` (bloqueio de criação de workspace tentando mesclar branch base já ativo em outro checkout),
     o PR `#42689` (resolve Issue `#42684` — arquivos de texto sem título com escopo de projeto fora da árvore git),
     a Issue `#42681` (configuração para ocultar a estrela de worktree primário e indentação visual profunda),
     e a Issue `#42718` (correção de escopo de servidor em abas criadas com `--worktree`).
   - [Consumo de recursos em agentes: reaper de LSP e overhead de hooks](../issues/consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks.md):
     adicionados o PR `#42686` (descarte automático de abas ociosas de navegador no `orca serve` com restauração transparente sob demanda),
     o PR `#42743` (formato seguro de exec hook para caminhos com espaços no Windows),
     o PR `#42725` (resolve Issue `#42724` — contenção visual de grandes custos nos tiles de Stats & Usage),
     e a Issue `#42675` (eliminação da espera de 2.1s de SIGKILL no fechamento de terminais zsh interativos).

### 4. Ciclo de 6h (18:00 BRT / 21:00 UTC em 2026-11-15)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-15T15:00:00Z` e `2026-11-15T21:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 2 novas issues priorizadas em `work/issues/`:**
   - `priority: high` — [Avaliação comparativa de agentes via CLI, revisão de diff com IA e notas de worktree](../issues/avaliacao-comparativa-de-agentes-via-cli-e-revisao-de-diff-com-ia-no-source-control.md):
     rastreia o PR `#42804` (resolve Issue `#42794` — criação e avaliação competitiva best-of-N com `orca worktree create --agents <lista>` e juiz automático com `orca worktree compare`),
     o PR `#42811` (resolve Issue `#42800` — ação "Review changes with AI" no menu `⋯` do Source Control gerando notas inline no diff com severidades `[critical]`, `[major]`, `[minor]`),
     e o PR `#42796` (resolve Issue `#11777` — grupo de comandos `orca worktree notes list|add|clear` para anotações programáticas em linhas de diff via CLI).
   - `priority: high` — [Servidor MCP stdio na CLI, otimizações de captura no Computer Use e automação de documentação](../issues/servidor-mcp-stdio-na-cli-e-otimizacoes-de-captura-no-computer-use.md):
     rastreia o PR `#42808` (resolve Issue `#13079` — servidor MCP stdio nativo via subcomando `orca mcp` expondo 11 ferramentas essenciais de worktrees, terminais e repositórios para agentes externos),
     o PR `#42801` (flags `--format`, `--quality`, `--max-width` e `--max-height` em `orca computer screenshot`, reduzindo payloads de visão em até 85%),
     e o PR `#42809` (resolve Issue `#42799` — template de automação interna `docs-weekly-audit` para refresh semanal de documentação contra mudanças na CLI).
3. **Atualização de 4 issues existentes em `work/issues/`:**
   - [Consumo de recursos em agentes: reaper de LSP e overhead de hooks](../issues/consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks.md):
     adicionados o PR `#42760` (substituição de supervisores Electron por workers nativos leves no Native Chat, economizando ~7 GB de RAM em 150 chats),
     e o PR `#42807` (limpeza de runtimes gerenciados obsoletos no boot do daemon e compressão gzip streaming de caches de telemetria do Codex/OpenCode/Muse).
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionada a Issue `#42759` (investigação do bug de omissão de modelos não-Gemini no seletor do Antigravity Chat por filtro estrito de `clientInfo` no `agy_acp_server.par`, propondo declaração alinhada à CLI `agy acp`).
   - [Aprovação de planos A/B/C, feedback de revisão inline e resiliência de composer no Native Chat](../issues/aprovacao-de-planos-abc-feedback-de-revisao-inline-e-resiliencia-de-composer-no-chat.md):
     adicionados o PR `#42789` (envio correto de resposta `skip` ao pular etapas em cartões de perguntas interativas),
     o PR `#42784` (identificação dinâmica do modelo Claude a partir da resposta mais recente no cabeçalho fixo),
     o PR `#42783` (tolerância e compatibilidade retroativa de esquemas JSONL contra downgrade de versão),
     o PR `#42776` (enfileiramento estrito de intenções de Steer atrás de inserções ativas),
     e o PR `#42775` (suporte a comandos slash e restauração confiável de modo de chat/terminal para OpenCode).
   - [Retomada de sessões gravadas pela CLI, hosts de workspace e replay de terminal](../issues/retomada-de-sessoes-gravadas-pela-cli-hosts-de-workspace-e-replay-de-terminal.md):
     adicionados os PRs `#42806` e `#42770` (foco imediato e ativação de digitação direta no terminal ativo ao selecionar workspace na barra lateral),
     o PR `#42791` (serialização JSON compacta em uma linha sem campos nulos nas listagens de terminal e worktree da CLI),
     a Issue `#42769` (correção no envio automático de comando de resume para abas acordadas de sleep do Claude Code),
     e a Issue `#42761` (tratamento de rascunhos sujos de editor em conexões SSH remotas impedindo o encerramento do host).
