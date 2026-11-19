---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-19
completed: 2026-11-19
tags:
  - tooling
refs:
  - issue:abas-de-navegador-sem-moldura-e-ergonomia-de-workspace
  - issue:alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas
  - issue:chaveamento-automatico-de-contas-claude-por-limite-de-uso-e-planos-observados
  - issue:comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-19)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-18T21:00:00Z` e `2026-11-19T03:15:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Atualização de 5 issues rastreadas em `work/issues/`:**
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionado o PR `#44430` (resolve Issue `#42512`), que contorna a falha de Secret Service / keyring temporariamente
     inacessível em ambientes Linux headless lendo diretamente o armazenamento de tokens baseado em arquivo do `agy`,
     eliminando o falso fallback que exibia o prompt de download desnecessário de 337 MB do runtime gerenciado.
   - [Chaveamento automático de contas Claude por limite de uso, planos observados e resgate de cota](../issues/chaveamento-automatico-de-contas-claude-por-limite-de-uso-e-planos-observados.md):
     adicionado o PR `#44431`, que reabre e restaura o painel do Claude com estado visível de erro/recuperação caso o reinício
     por troca de conta falhe, além de pular explicitamente a inicialização de teammates e subagentes associados para prevenir
     falhas em cascata em sessões quebradas.
   - [Abas de navegador sem moldura e ergonomia de workspace](../issues/abas-de-navegador-sem-moldura-e-ergonomia-de-workspace.md):
     adicionado o PR `#44428`, que centraliza a instalação de listeners de requisições web (`webRequest`) de sessões de navegador
     em um único proprietário gerenciado para evitar vazamentos de listeners e preserva os baselines de título e favicon de páginas
     durante os ciclos de descarte e hibernação de abas pelo Memory Saver.
   - [Comandos shell no chat, recibos de perguntas e foco espacial em terminais](../issues/comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais.md):
     adicionada a Issue `#44012` (resolvida no commit `1615e5c`), que trava os controles e opções do cartão de pergunta
     assíncrona (`ask_question`) imediatamente após a submissão inicial, impedindo cliques duplicados ou respostas concorrentes
     durante o aperto de mão da fila (*queue handshake*) do Codex.
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionado o PR `#42965`, que preserva o menu de contexto nativo do navegador/sistema operacional (ação "Copiar" / "Copy")
     ao selecionar trechos de texto em mensagens do chat na interface móvel web, corrigindo o bloqueio causado por manipuladores de toque.
