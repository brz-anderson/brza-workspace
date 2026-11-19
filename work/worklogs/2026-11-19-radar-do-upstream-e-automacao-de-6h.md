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
  - issue:protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle
  - issue:retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot
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

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-19)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e commits criados ou
   atualizados entre `2026-11-19T03:00:00Z` e `2026-11-19T09:15:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Atualização de 5 issues rastreadas em `work/issues/`:**
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados o PR `#44475` (resposta a pedidos de permissão de subagentes auxiliares/helpers de workers diretamente pela interface
     do coordenador com hold de 2 minutos antes de delegar ao terminal) e o PR `#44327` (execução assíncrona dos checkpoints do WAL
     do `orchestration.db` fora da thread principal para eliminar stalls de 500 ms no Electron).
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados o PR `#44559` (resolve Issue `#39556`, repassa `--effort` na família de modelo no lançamento do Antigravity),
     o PR `#44517` (refs Issue `#44489`, mapeia avisos 401 de streaming para falha formal do turno com `outcome: failure`),
     o PR `#44497` (resolve Issue `#44496`, permite remover contas Antigravity não autenticadas no `agy` em Settings para destravar novos chats) e
     o PR `#44484` (resolve Issue `#44483`, fallback para `summary.WorkspaceURIs` para mapear conversas Antigravity no escopo Workspace de `/resume`).
   - [Chaveamento automático de contas Claude por limite de uso, planos observados e resgate de cota](../issues/chaveamento-automatico-de-contas-claude-por-limite-de-uso-e-planos-observados.md):
     adicionado o PR `#43822` (varredura e liberação de locks obsoletos do Codex via helper sob `.coordination.lock` exclusivo para permitir compartilhamento de histórico de contas).
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionados o PR `#44477` (resolve Issue `#37707`, ignora pastas de projeto ilegíveis no resume de chat em vez de abortar com `transcriptUnreadable`),
     o PR `#44445` (preserva a mensagem digitada durante a criação de worktrees quando o agente falha no arranque) e
     o PR `#44275` (conversão linear $O(N)$ do histórico legado de chat eliminando rescans por mensagem).
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados o PR `#44413` (mensagens entre agentes tornam-se linhas compactas de status com o estado gravado do despacho do worker),
     o PR `#44508` (estabilização da faixa de agentes contra cintilações e reflows durante atualizações de sessão) e
     o PR `#44203` (streaming de saídas extensas de ferramentas na exportação de contexto do chat para evitar estouro de heap).
