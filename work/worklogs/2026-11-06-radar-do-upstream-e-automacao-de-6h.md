---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-06
completed: 2026-11-06
tags:
  - tooling
refs:
  - issue:acoes-de-commit-no-git-graph-checkout-cherry-pick-e-revert
  - issue:adaptadores-acp-customizados-e-isolamento-de-permissoes-de-sessao
  - issue:cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat
  - issue:ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins
  - issue:melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados
  - issue:repositorios-vinculados-no-source-control-e-escopo-de-worktree-na-cli
  - issue:resultados-de-ci-no-chat-e-disparo-automatico-de-agentes-em-falhas-de-pr
  - issue:seletor-de-branches-na-status-bar-e-suporte-a-workspaces-em-pastas-multirrepositorio
  - issue:subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent
  - issue:vazamento-de-memoria-gpu-webgl-no-terminal-e-performance-macos
  - issue:workers-de-plugins-em-hosts-remotos-e-gerenciamento-cli-de-ssh
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-06)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados mais de 40 novos PRs e issues criados ou
   atualizados entre `2026-11-05T21:00:00Z` e `2026-11-06T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl` para evitar duplicidade de assuntos já rastreados.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Cartões de Pull Request, feedback de Steer e atalhos no Native Chat](../issues/cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat.md):
     rastreia o PR `#38750` (cartão visual compacto no chat ao criar PR com status, diff e link clicável), PR `#38749` (feedback dinâmico
     no botão de envio e tecla Cmd/Ctrl para chaveamento instantâneo entre Steer e Queue), PR `#38727` (eliminação do timeout rígido de 60s
     no handshake de inicialização de chats nativos para Claude, ACP e Pi), PR `#38724` (passagem de atalhos globais de teclado no editor de chat),
     PR `#38756` (toggle para ocultar o cartão sumário de arquivos alterados) e PR `#38660` (seletor rápido de modelo de chat com preservação de estado).
3. **Atualização de 5 issues existentes em `work/issues/`:**
   - [Melhorias de Native Chat, ACP do Gemini, CLI, abas e diff no upstream](../issues/melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream.md):
     adicionados o PR `#38737` e issue `#38606` (suporte a autenticação Gemini Enterprise no Antigravity Chat com project ID e location),
     PR `#38767` (limpeza de bookkeeping legado de ferramentas e mensagens ACP no ciclo de vida) e issue `#38663` (saída abrupta do ACP OpenCode).
   - [Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](../issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md):
     adicionados o PR `#38719` e issue `#38556` (subcomando `orca chat rename` na CLI e persistência de títulos manuais ao restaurar chats).
   - [Workers de plugins em hosts remotos e gerenciamento CLI de SSH](../issues/workers-de-plugins-em-hosts-remotos-e-gerenciamento-cli-de-ssh.md):
     adicionados o PR `#38774` (`orca host rm` implementado na CLI com desalocação completa de chaves e túneis), issue `#38673` (falha de permissão
     chmod em filesystems somente leitura no host remoto) e issue `#38669` / PR `#38782` (resolução correta de endpoints de host na criação de workspace via VM remota).
   - [Repositórios vinculados no Source Control e escopo de worktree na CLI](../issues/repositorios-vinculados-no-source-control-e-escopo-de-worktree-na-cli.md):
     adicionados o PR `#38744` (recusa preventiva de troca de branch com modificações sem commit, rebase ativo ou agentes trabalhando) e
     PR `#38773` (vida útil limitada para checkouts especulativos de worktrees órfãs).
   - [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md):
     adicionados a issue `#38720` (entrega de mensagens de orquestração em terminais OMP via protocolo/extensão dedicada em vez de digitação PTY crua),
     PR `#38713` (papéis de modelos, seletores dedicados e controle de reasoning effort em agentes OMP) e PR `#38768` (prevenção de suspensão
     de agentes enquanto o cliente emparelhado estiver ativo ou digitando).

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-06)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados mais de 50 novos PRs e issues criados ou
   atualizados entre `2026-11-06T03:00:00Z` e `2026-11-06T09:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Seletor de branches na status bar e suporte a workspaces em pastas multirrepositório](../issues/seletor-de-branches-na-status-bar-e-suporte-a-workspaces-em-pastas-multirrepositorio.md):
     rastreia o PR `#38869` (`BranchStatusSegment` no canto inferior da barra de status com popover pesquisável de branches e fetch silencioso),
     PR `#38836` (seletor interativo de branches no cabeçalho do Source Control `⎇ main ▾` para alternar, criar ou rastrear branches locais e remotos),
     PR `#38831` (seções colapsáveis por worktree no Source Control para pastas de projetos multirrepositório), PR `#38904` (aninhamento
     visual de worktrees filhos sob o folder workspace pai na sidebar e mobile), PR `#38875` (linhagem de pais persistente na criação e suporte cross-machine),
     além das issues `#38931` (overflow de sufixo numérico `-100` em worktrees) e `#38830` (ocultação indevida de workspaces ao remover `.git` aninhado).
3. **Atualização de 4 issues existentes em `work/issues/`:**
   - [Vazamento de memória GPU WebGL no terminal e performance no macOS](../issues/vazamento-de-memoria-gpu-webgl-no-terminal-e-performance-macos.md):
     adicionados o PR `#38861` e issue `#38860` (suspensão de renderização invisível xterm/WebGL sob coberturas de Native Chat, contenção
     de quadros sincronizados DEC `?2026` e teto para warm tab WebViews), PR `#38857` e issue `#38856` (recuperação automática de desync de versão
     do glyph-atlas WebGL ao reexibir abas), PR `#38858` (contenção de rajadas de redimensionamento e storm de sinais SIGWINCH) e PR `#38859`
     (propagações de esquemas de cores Light/Dark para consultas PTY `OSC 10/11` e WebViews).
   - [Cartões de Pull Request, feedback de Steer e atalhos no Native Chat](../issues/cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat.md):
     adicionados o PR `#38877` (envio imediato do primeiro cartão pausado pós-<kbd>Stop</kbd> via <kbd>Cmd/Ctrl</kbd>+<kbd>Enter</kbd> no composer vazio),
     PR `#38848` (roteamento para o último cartão enfileirado quando o composer estiver vazio), PR `#38892` (pré-visualização rica de cartões de PR
     para qualquer repositório no mesmo host autenticado), PR `#38879` (streaming incremental mantido ao citar tipos genéricos como `Vec<T>`),
     PR `#38883` (despacho isolado de eventos de status sem despertar chats de outras abas) e PR `#38895` (busca de transcrição O(1) por ID de sessão).
   - [Melhorias de Native Chat, ACP do Gemini, CLI, abas e diff no upstream](../issues/melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream.md):
     adicionados o PR `#38872` (suporte a formulários interativos e perguntas de múltipla escolha do OpenCode em cartões de chat), PR `#38815`
     (preservação de modelo salvo ao restaurar conversas ACP) e a issue `#38833` (proposta de migração do Antigravity Chat do runtime empacotado `.par`
     para o comando oficial `agy acp` nativo do host, unificando stores de conversas).
   - [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md):
     adicionados o PR `#38901` (falha imediata com `agent-sign-in-prompt` quando o worker Antigravity é chamado com CLI deslogada, evitando timeouts
     inúteis), PR `#38899` (verificação contínua e reparo de ganchos de status `~/.gemini/config/hooks.json`), issue `#38850` (travas FIFO determinísticas
     em SQLite `lock-acquire/release/list` com leases TTL e quadros de colaboração para DAGs multi-agente) e PR `#38814` (modularização de donos de caixas de correio).
   - [Adaptadores ACP customizados e isolamento de permissões de sessão](../issues/adaptadores-acp-customizados-e-isolamento-de-permissoes-de-sessao.md):
     adicionados o PR `#38826` (suporte a credenciais em chaveiro do SO / Windows Credential Manager para contas Codex), PR `#38807` e issue `#38806`
     (alinhamento do algoritmo de slug de confiança de workspace com o `cursor-agent`), issue `#38866` (respeito estrito às políticas de permissão do host
     remoto em handoffs de agentes) e issue `#38849` (conector de primeira classe e scanner no AI Vault para o agente ZeroClaw).

### 3. Ciclo de 6h (12:00 BRT / 15:00 UTC em 2026-11-06)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados mais de 50 novos PRs e issues criados ou
   atualizados entre `2026-11-06T09:00:00Z` e `2026-11-06T15:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Resultados de CI no chat e disparo automático de agentes em falhas de PR](../issues/resultados-de-ci-no-chat-e-disparo-automatico-de-agentes-em-falhas-de-pr.md):
     rastreia o PR `#39020` (linhas contextuais de status de CI no diário do chat que abriu ou enviou commits para o PR, com links diretos
     e supressão de estados cancelados transitórios) e o PR `#38950` ("Automatic follow-ups for failing checks", disparando autonomamente
     o fluxo "Fix with AI" no workspace do PR ao detectar checks quebrados, com prevenção estrita de loops, limite de 3 tentativas por commit
     e 6 execuções por PR/dia).
3. **Atualização de 4 issues existentes em `work/issues/`:**
   - [Melhorias de Native Chat, ACP do Gemini, CLI, abas e diff no upstream](../issues/melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream.md):
     adicionados o PR `#39006` (implementa a execução do Antigravity Chat diretamente via `agy acp` nativo do host para versões >= 1.5.0,
     unificando contas e histórico de sessões com o terminal e resolvendo a issue `#38833`), PR `#39012` (ação interativa "Sign in" em chats nativos
     para recuperação de autenticação em terminais de OpenCode, Pi e OMP) e PR `#38976` (retry resiliente em erros `-32603` de catálogo ACP).
   - [Seletor de branches na status bar e suporte a workspaces em pastas multirrepositório](../issues/seletor-de-branches-na-status-bar-e-suporte-a-workspaces-em-pastas-multirrepositorio.md):
     adicionados o PR `#39018` (subcomando `orca worktree set --parent-worktree folder:<id>` para anexar worktrees existentes a pastas multirrepositório
     e resolução de `--parent-worktree active`), PR `#39000` (resolução da issue `#38931` iniciando sufixo numérico de worktrees além do maior existente)
     e PR `#38955` (`orca repo delete-branch` com validação de commits integrados e cerca transacional).
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados o PR `#38995` e issue `#38994` (agrupamento de sessões floating e subagentes na sidebar com contadores ao vivo), PR `#38963`
     (ação "Background" para transferir ferramentas e subagentes Claude Bash longos para segundo plano, liberando o chat), PR `#38945`
     (isolamento do SQLite de busca do Session History em worker threads dedicadas para manter fluidez em históricos gigantes) e PR `#39013`
     / issue `#39010` (contabilização no Resource Usage de processos órfãos que desanexaram de seus terminais usando as tags `ORCA_WORKTREE_ID`).
   - [Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](../issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md):
     adicionada a issue `#38952` (subcomandos `orca chat list` para listar chats abertos por CLI e `orca session resume --session <id>` para
     retomar sessões salvas) e issue `#39043` (exposição de foco visual ativo da interface `focusedCard`/`focusedTerminal` na CLI para limpezas seguras).
   - [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md):
     adicionadas a issue `#39042` (prevenção de cancelamento espúrio de turnos em execução do OMP quando `orchestration send` pressiona Enter com steer
     enfileirado), issue `#38951` (bloqueio de injeção cega de avisos de ponteiro em buffers de digitação ativa) e issue `#39021` (inclusão de `statusMessage`
     explícita nos hooks do Codex).

### 4. Ciclo de 6h (18:00 BRT / 21:00 UTC em 2026-11-06)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados mais de 50 novos PRs e issues criados ou
   atualizados entre `2026-11-06T15:00:00Z` e `2026-11-06T21:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Ações de commit no Git Graph (checkout, cherry-pick e revert)](../issues/acoes-de-commit-no-git-graph-checkout-cherry-pick-e-revert.md):
     rastreia o PR `#39069` (menu de contexto e barra de confirmação inline no Git Graph para Check out commit desanexado seguro, Cherry-pick
     com abort automático se vazio e Revert com detecção de conflitos e `GIT_EDITOR=true`), PR `#39124` (catálogo completo de UI em Português do Brasil)
     e as issues `#39083` (filtro de worktrees por status de atividade) e `#39067` / PR `#39091` (tratamento de jobs GitLab com `allow_failure: true`).
3. **Atualização de 4 issues existentes em `work/issues/`:**
   - [Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados](../issues/plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados.md):
     adicionados o PR `#39100` (resolve a issue `#38617` expondo `createdAt` e `lastActivityAt` em `workspace.list` para a API de plugins),
     PR `#39080` (opção para ocultar pastas e grupos de projetos vazios na barra lateral), PR `#39081` (ícone colorido do Linear refletindo o estado da issue)
     e a issue `#39086` (correção do filtro Projects no Search palette que ocultava sessões em folder-workspaces).
   - [Cartões de Pull Request, feedback de Steer e atalhos no Native Chat](../issues/cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat.md):
     adicionados o PR `#39050` (redimensionamento proporcional automático de imagens coladas com alta resolução no chat/terminal em vez de erro
     fatal `Clipboard image is too large`), PR `#39141` (eliminação de cartões sintéticos redundantes "Ran /model" ao trocar de modelo pelo seletor visual)
     e a issue `#39060` (ajuste na espessura de renderização de fontes em negrito no Chat UI).
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados o PR `#39082` e issue `#39074` (pré-visualização sob demanda de transcrições de chat estruturado em modo read-only diretamente dentro do Agent Dashboard)
     e o PR `#39079` / issue `#39073` (notificações desktop opt-in exclusivamente para perguntas de agentes, silenciando aprovações e conclusões).
   - [Repositórios vinculados no Source Control e escopo de worktree na CLI](../issues/repositorios-vinculados-no-source-control-e-escopo-de-worktree-na-cli.md):
     adicionados o PR `#39096` e issue `#38940` (carregamento diferido do histórico zsh por worktree `HISTFILE` via `builtin fc -RI` na inicialização do terminal macOS),
     PR `#39089` (captura atômica de snapshots headless entre escritas PTY para eliminar sequências ANSI residuais) e o PR `#39087` (indicação de status
     "Waiting for user" na sidebar e mobile durante perguntas assíncronas no meio do turno do Codex).
