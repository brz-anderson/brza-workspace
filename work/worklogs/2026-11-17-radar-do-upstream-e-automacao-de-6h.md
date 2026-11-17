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
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:seletor-de-branches-na-status-bar-e-suporte-a-workspaces-em-pastas-multirrepositorio
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
