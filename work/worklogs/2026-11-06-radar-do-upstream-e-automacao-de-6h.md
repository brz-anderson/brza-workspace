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
  - issue:cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat
  - issue:ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins
  - issue:melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream
  - issue:repositorios-vinculados-no-source-control-e-escopo-de-worktree-na-cli
  - issue:subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent
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
