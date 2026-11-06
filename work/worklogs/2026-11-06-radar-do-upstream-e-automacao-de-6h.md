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
  - issue:adaptadores-acp-customizados-e-isolamento-de-permissoes-de-sessao
  - issue:cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat
  - issue:ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins
  - issue:melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream
  - issue:repositorios-vinculados-no-source-control-e-escopo-de-worktree-na-cli
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
