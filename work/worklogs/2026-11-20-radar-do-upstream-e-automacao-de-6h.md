---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-20
completed: 2026-11-20
tags:
  - tooling
refs:
  - issue:abas-de-navegador-sem-moldura-e-ergonomia-de-workspace
  - issue:alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas
  - issue:comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais
  - issue:protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle
  - issue:retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-20)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e commits criados ou atualizados entre `2026-11-19T21:00:00Z` e `2026-11-20T03:15:00Z`, comparando com as notas em `work/issues/` e o índice `.brza/index.jsonl`.
2. **Atualização de 4 issues rastreadas em `work/issues/`:**
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados os PRs `#44660` (resolve `#44585`), mantendo o stdout do hook `PreToolUse` vazio para permitir que a política embutida do revisor do `agy` decida a execução de ferramentas sem auto-recusa indevida em `agy -p`; `#44534`, que injeta explicitamente `AGY_CLI_DISABLE_AUTO_UPDATE=true` nas especificações de lançamento do host ACP e no probe `agy models`, além de purgar chaves em caixa alternada no Windows para prevenir corridas de background updater; e `#44538`, que inclui `%LOCALAPPDATA%\agy\bin` na descoberta de executáveis da CLI Antigravity no Windows quando omitido do PATH do Electron.
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionado o PR `#44919`, que roteia pedidos e streams de aprovação de permissão de workers (*worker approval prompts*) em chats de coordenador em servidores pareados e clientes remotos através do host proprietário da sessão de chat, além de permitir encerramento limpo por dispositivos conectados e recusar códigos de celular no comando `environment add`.
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionados os PRs `#44745` (resolve `#44715`), que trata worktrees vinculados a um workspace de pasta com múltiplos repositórios (`folder workspace`) como um único grupo unificado no cleanup para impedir que um repositório seja excluído enquanto outro ainda estiver em uso; e `#44905`, que protege pastas de importação do Codex no WSL por resolução estática de caminhos com lease de 1 segundo sem forçar a inicialização de distribuições WSL paradas durante varreduras de histórico.
   - [Comandos shell no chat, recibos de perguntas e foco espacial em terminais](../issues/comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais.md):
     adicionados os PRs `#44460` (refs `#31281`), que retém o nome renomeado de abas de terminal após o fechamento e o reaplica ao retomar sessões a partir do Session History / AI Vault; `#44916`, que unifica o envio de arquivos arrastados ou colados em chats de terminal em servidores pareados para `.orca/drops` via `stageClientFilesForAgent`; e `#44673`, que lista servidores MCP configurados antes do início do chat Codex com o status "not started" sem disparar polling de backoff nem cold-starts no `codex app-server`.

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-20)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e commits criados ou atualizados entre `2026-11-20T03:00:00Z` e `2026-11-20T09:15:00Z`, comparando com as notas em `work/issues/` e o índice `.brza/index.jsonl`.
2. **Atualização de 5 issues rastreadas em `work/issues/`:**
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados os PRs `#44965`, que detecta automaticamente Gemini API Key e gcloud ADC no host oferecendo troca em um clique na barra de login e diante de erros 401/403/cota; `#45254`, que exibe no rodapé do chat qual binário e versão do `agy` está sustentando a sessão; `#45117`, que roda bots e agentes gerenciados Antigravity no `agy` autenticado do host em vez de falhar no runtime empacotado; e `#45244`, que ignora glifos de Gemini enterrados em títulos de shell no status do agente.
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados os PRs `#45194`, permitindo anexar e enviar arquivos em comunicações por correio sobre itens gerenciados localmente ou em hosts remotos; `#44472`, que grava duravelmente o Dispatch no ato da escrita de mensagens de workers para manter identificação clara ("Tarefa · Agente [Servidor]") mesmo após fechamento da aba; `#45290`, que suspende a subscrição `orchestration.crewSubscribe` em chats nativos durante repouso do painel de tripulação, eliminando congelamentos de até 32s; e `#45330`, que otimiza consultas de coordenadores legados filtrando `dispatch_contexts` por tarefa.
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionados os PRs `#44979`, que preserva o branch Git e push-target em falhas parciais de exclusão de worktree apagando o link `.git` por último para viabilizar retentativa segura posterior; `#45053`, que suprime a criação de shells ociosos intermediários redundantes no provisionamento de worktrees de agentes; e `#44781`, que restringe reloads de layout apenas aos workspaces reportados por mutações persistidas.
   - [Comandos shell no chat, recibos de perguntas e foco espacial em terminais](../issues/comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais.md):
     adicionados os PRs `#45100`, roteando a colagem (Cmd+V) para o campo de resposta da pergunta interativa ativa no chat em vez de no composer oculto; `#45101`, liberando atalhos de alternância de workspace (`Mod+Shift+Up/Down`) através do composer de chat; `#45006`, que retém o botão "Approve once" em recusas de ferramentas do Codex de até 256 KB; `#45064`, repintando o cursor em pending-wrap no replay de snapshots de terminal; e `#45110`, neutralizando caudas parciais de sequências de escape superiores a 4096 caracteres em cortes de stream e snapshots.
   - [Abas de navegador sem moldura e ergonomia de workspace](../issues/abas-de-navegador-sem-moldura-e-ergonomia-de-workspace.md):
     adicionados os PRs `#44742`, introduzindo watchdog de carregamento estagnado no navegador embutido com diagnóstico visual e registro em trace de performance; e `#44598`, incorporando notificações de desempenho que sugerem proativamente ativar o Memory Saver quando abas inativas acumularem memória RAM em excesso em segundo plano.
