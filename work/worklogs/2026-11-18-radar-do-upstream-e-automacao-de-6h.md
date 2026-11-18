---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-18
completed: 2026-11-18
tags:
  - tooling
refs:
  - issue:alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas
  - issue:comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais
  - issue:fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks
  - issue:modos-build-e-plan-e-ferramentas-de-artifacts-no-native-chat
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle
  - issue:retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot
  - issue:seletor-de-branches-na-status-bar-e-suporte-a-workspaces-em-pastas-multirrepositorio
  - issue:vazamento-de-memoria-gpu-webgl-no-terminal-e-performance-macos
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-18)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-18T03:00:00Z` e `2026-11-18T09:15:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Atualização de 9 issues rastreadas em `work/issues/`:**
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionado o PR `#43939` (suporte a autenticação de chat do Antigravity via Gemini API key e Google Agent Platform ADC sem exigir login OAuth no navegador).
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados o PR `#43953` (liberação imediata de terminal de worker na finalização via `settleWorkerStop`),
     a Issue `#43957` (exposição do `providerSessionId` no envelope de sessões de chat e subagentes),
     a Issue `#43925` (terminal substituto condicional para comandos Run),
     a Issue `#43875` (preservação de receitas de inicialização na retomada de workers),
     a Issue `#43874` (deep links com protocolo `orca://` para chats e mensagens) e
     a Issue `#43869` (correção de rejeição de `worker_done` vindo de host WSL).
   - [Comandos shell no chat, recibos de perguntas e foco espacial em terminais](../issues/comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais.md):
     adicionados o PR `#43896` (retenção de entrada em fila de terminal até prontidão do agente),
     o PR `#43889` (reconstrução de tela de terminal oculto a partir do daemon após descarte de saída) e
     o PR `#43901` (polling adaptativo de 15s para painéis inativos de agentes).
   - [Modos Build e Plan e ferramentas de artifacts no Native Chat](../issues/modos-build-e-plan-e-ferramentas-de-artifacts-no-native-chat.md):
     adicionado o PR `#43891` (execução assíncrona de `fsync` para registros de artifacts fora da thread principal).
   - [Fontes web em plugins, isolamento de atalhos e resiliência de hooks](../issues/fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks.md):
     adicionados o PR `#43916` (suporte a layout Mermaid ELK via `@mermaid-js/layout-elk`, resolvendo Issue `#43552`),
     o PR `#43877` (normalização de chaves de confiança para hooks do Codex no Windows) e
     o PR `#43876` (aviso explícito ao substituir symlinks durante registro de CLI).
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados o PR `#43908` (desacoplamento de filas de escrita de journal multi-chat evitando travamentos de 30-60s no status "Sending...", resolvendo Issue `#43988`),
     o PR `#43954` (limpeza de resumos de status de conversas fechadas),
     a Issue `#43983` (contagem de sessões de chat no Resource Manager) e
     a Issue `#44003` (persistência de descarte de linhas de atividades com falha).
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionado o PR `#43918` (retomada automática de chats e turnos interrompidos por crash ou reinício do runtime).
   - [Vazamento de memória GPU WebGL no terminal e performance no macOS](../issues/vazamento-de-memoria-gpu-webgl-no-terminal-e-performance-macos.md):
     adicionados o PR `#43898` (camada antecipada de diagnósticos de stalls de 8s a 45s com captura de perfil JS no watchdog) e
     o PR `#43880` (execução de animações de rotação apenas na main thread e enquanto visíveis para prevenir 100% de CPU no classificador de quadros do Chromium).
   - [Seletor de branches na status bar e suporte a workspaces em pastas multirrepositório](../issues/seletor-de-branches-na-status-bar-e-suporte-a-workspaces-em-pastas-multirrepositorio.md):
     adicionados o PR `#43927` (ação rápida "New File..." diretamente no menu `+` da barra de abas) e
     a Issue `#43928` (configuração para ocultar workspaces concluídos no status Done da barra lateral mantendo visibilidade no Workspace Board).
