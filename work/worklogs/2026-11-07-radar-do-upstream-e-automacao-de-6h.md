---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-07
completed: 2026-11-07
tags:
  - tooling
refs:
  - issue:bifurcacao-de-conversas-no-chat-ui-e-resiliencia-de-inicializacao-do-claude
  - issue:cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat
  - issue:fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks
  - issue:gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache
  - issue:historico-de-navegacao-no-editor-e-identificacao-de-workspaces-por-plugins
  - issue:melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:sincronizacao-de-temas-com-claude-code-titulos-localizados-e-sugestoes-no-chat
  - issue:subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent
  - issue:vazamento-de-memoria-gpu-webgl-no-terminal-e-performance-macos
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h e 12h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-07)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados mais de 50 novos PRs e issues criados ou
   atualizados entre `2026-11-06T21:00:00Z` e `2026-11-07T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl` para evitar duplicidade de assuntos já rastreados.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Histórico de navegação no editor e identificação de workspaces por plugins](../issues/historico-de-navegacao-no-editor-e-identificacao-de-workspaces-por-plugins.md):
     rastreia o PR `#39162` (`editor.navigateBack` / `editor.navigateForward` com atalhos `Cmd+[` / `Cmd+]` no macOS e `Alt+Left` / `Alt+Right`
     no Windows/Linux, pilha de histórico de posições de cursor e reabertura de abas fechadas por workspace), issue `#39177`
     (resolução inequívoca com `workspaceId` em `workspace.readContext` para plugins, prevenindo colisão em projetos múltiplos
     com mesmo `displayName` e branch `primary/main`), issue `#39176` (API `workspace.createFromRecipe` para criação programática
     de workspaces a partir de templates corporativos sem redigitação no chat) e issue `#39267` (acordar silencioso de workspaces
     em repouso sem disparar terminais/PTYs desnecessários na inspeção passiva de arquivos).
3. **Atualização de 3 issues existentes em `work/issues/`:**
   - [Bifurcação de conversas no Chat UI e resiliência de inicialização do Claude](../issues/bifurcacao-de-conversas-no-chat-ui-e-resiliencia-de-inicializacao-do-claude.md):
     adicionado o PR `#39168` (replicação fiel do registro de conversa serializado da UI do app ao acionar fork, preservando histórico
     visual, formatação, timestamps e recibos imutáveis de identidades nativas herdadas para não duplicar turnos futuros do modelo).
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     adicionado o PR `#39169` (continuação imediata de conversas em limite de uso de 5h ao trocar de conta no Claude switcher,
     conectando o evento `onSwitched` ao dispatch de `continueUsageLimit`).
   - [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md):
     adicionadas a issue `#39263` (subcomando `orca orchestration reply --decision user|technical` vinculando a classificação da
     resposta ao Run/Dispatch para auditoria de dúvidas de workers) e a issue `#39262` (mitigação de descarte silencioso de mensagens
     de correio com `accepted: true` em workers remotos).

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-07)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados mais de 60 novos PRs e issues criados ou
   atualizados entre `2026-11-07T03:00:00Z` e `2026-11-07T09:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Fontes web em plugins, isolamento de atalhos e resiliência de hooks](../issues/fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks.md):
     rastreia o PR `#39416` (campo `fonts` no manifesto de plugins para distribuição de tipografias WOFF2 no terminal, editor e UI,
     com sanitização, remensuração no Monaco/xterm e fallbacks exatos), PR `#39413` (rastreamento de `hydrationId` em formulários
     declarativos de plugins, garantindo que edições salvas antes de uma troca rápida de workspace sejam persistidas no workspace
     de origem), PR `#39407` (deadline centralizado de 2s para substituição de comandos nativos por plugins no processo principal,
     bloqueando execuções duplicadas via `commands.run`), PR `#39393` (aplicação estrita de negação *fail-closed* em ganchos com
     `onError: "deny"` quando o resultado for malformado), PR `#39348` (execução de atalhos globais de plugins em terminais ativos
     respeitando a política de teclado configurada) e PR `#39383` (cancelamento de inventários caros de terminais para eventos de status
     quando não houver painéis de plugins ouvintes).
3. **Atualização de 4 issues existentes em `work/issues/`:**
   - [Melhorias de Native Chat, ACP do Gemini CLI, abas e diff no upstream](../issues/melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream.md):
     adicionados o PR `#39398` e a issue `#39395` (detecção correta dos arquivos de credencial `acp_token.json` e `acp_business_token.json`
     do servidor gerenciado do Antigravity Chat, prevenindo que novas conversas migrem erroneamente para a conta host do `agy`).
   - [Cartões de Pull Request, feedback de Steer e atalhos no Native Chat](../issues/cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat.md):
     adicionados o PR `#39287` e issue `#39286` (preservação do cartão interativo de aprovação Allow/Deny quando a atualização de título
     do terminal do Claude sucede o gancho de permissão), PR `#39309` (preservação de referências `#N` como texto plano quando a mensagem
     cita repositórios externos) e PR `#39369` (esmaecimento sutil da message rail no Chat UI para leitura sem distrações).
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados o PR `#39276` e issue `#39275` (renderização completa de subagentes do OpenCode 2.x no Chat UI com cartão dedicado,
     acompanhamento de ciclo de vida e aninhamento das ferramentas do subagente sob o bloco).
   - [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md):
     adicionados o PR `#39283` (backoff exponencial de até 60s em relays de federação com falha em vez de polling contínuo a cada segundo,
     eliminando alto consumo de CPU e acessos a disco no macOS) e a issue `#39300` (observador para notificar o término de processos
     supervisionados do Codex cujo PTY permaneça aberto).

### 3. Ciclo de 6h (12:00 BRT / 15:00 UTC em 2026-11-07)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados mais de 50 novos PRs e issues criados ou
   atualizados entre `2026-11-07T09:00:00Z` e `2026-11-07T15:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Sincronização de temas com Claude Code, títulos localizados e sugestões no chat](../issues/sincronizacao-de-temas-com-claude-code-titulos-localizados-e-sugestoes-no-chat.md):
     rastreia o PR `#39447` (sincronização automática e dinâmica do tema do terminal do Orca com a interface do Claude Code,
     injetando temas customizados no `settings.json` com hot-reload e toggle dedicado em configurações), PR `#37107` / issue `#22316`
     (sugestões de prompt nativas do Claude Code no composer do Native Chat, renderizadas de forma transitória sem gravar no histórico e
     aceitas com <kbd>Tab</kbd> ou <kbd>Seta para a Direita</kbd>), PR `#39437` / issue `#39281` (suporte a títulos de workspace
     localizados desacoplados dos slugs ASCII dos branches Git) e PR `#37190` / issue `#36722` (reabertura de chats nativos órfãos após
     remoção e recadastro de pastas de projetos com restauração de rascunhos e transcripts).
3. **Atualização de 4 issues existentes em `work/issues/`:**
   - [Vazamento de memória GPU WebGL no terminal e performance no macOS](../issues/vazamento-de-memoria-gpu-webgl-no-terminal-e-performance-macos.md):
     adicionados o PR `#39465` e a issue `#39405` (cache do snapshot de layout de teclado no processo principal com invalidação via
     notificação TIS Carbon, estancando vazamento de portas Mach no WindowServer a cada foco de janela no macOS) e o PR `#39445`
     (execução direta do binário `ps` sem invocação de shell intermediário no Resource Manager).
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     adicionadas a issue `#39495` (proposta de motor de rotação automática de contas Claude por host quando o limite de 5h ou semanal
     esgotar, com limites discriminados por modelo e sincronização cross-device) e a issue `#39502` (configuração para desativar polling
     em background da cota OAuth à API da Anthropic).
   - [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md):
     adicionadas a issue `#39517` (papéis salvos de workers `--role <name>` para `orchestration worker-start` com pré-validação de
     combinações de modelo e esforço no catálogo do host) e a issue `#39499` (limpeza oportuna de linhas de agentes marcadas como "Done"
     na sidebar quando a pane já encerrou e retornou ao shell).
   - [Cartões de Pull Request, feedback de Steer e atalhos no Native Chat](../issues/cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat.md):
     adicionadas a issue `#39516` (isolamento de trocas de modelo/esforço mid-turn rotuladas como "Next turn: ..." para não distorcer o
     turno em andamento, e entrega prioritária imediata de respostas a perguntas sem retenção na fila) e a issue `#39520` (ação "Background"
     para comandos Bash e subagentes Claude longos diretamente na interface de chat).
