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
  - issue:alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas
  - issue:cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat
  - issue:conectores-de-linhagem-na-sidebar-cores-de-grupos-e-isolamento-de-extensoes
  - issue:isolamento-de-artefatos-temporarios-de-chat-e-estudio-de-temas-via-cli
  - issue:plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados
  - issue:redesenho-de-cartoes-de-resposta-progresso-por-etapas-e-fila-de-mensagens
  - issue:retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot
  - issue:retomada-de-sessoes-gravadas-pela-cli-hosts-de-workspace-e-replay-de-terminal
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
