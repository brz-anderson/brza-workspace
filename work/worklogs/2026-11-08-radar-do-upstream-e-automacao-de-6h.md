---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-08
completed: 2026-11-08
tags:
  - tooling
refs:
  - issue:agente-kiro-no-native-chat-janela-flutuante-e-enderecamento-de-workspaces
  - issue:melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:seguranca-de-hooks-em-worktrees-e-integridade-de-setup-em-automacoes
  - issue:seletor-de-branches-na-status-bar-e-suporte-a-workspaces-em-pastas-multirrepositorio
  - issue:subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent
  - issue:titulos-de-janela-para-time-trackers-ajuste-de-visualizadores-e-resiliencia-de-saida
  - issue:validacao-de-conclusao-em-automacoes-cli-de-extensoes-e-destravamento-de-rate-limit
---

# Radar de issues e PRs do upstream e automação de 6h (00h e 06h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-08)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues criados ou
   atualizados entre `2026-11-07T21:00:00Z` e `2026-11-08T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Títulos de janela para time trackers, ajuste de visualizadores e resiliência de saída](../issues/titulos-de-janela-para-time-trackers-ajuste-de-visualizadores-e-resiliencia-de-saida.md):
     rastreia o PR `#39590` / issue `#34835` (templates customizáveis de título de janela com variáveis de repositório, worktree,
     issue key de Linear/Jira/GitHub e aba ativa para integração transparente com time trackers como Timeular/Toggl),
     PR `#39635` / issue `#39634` (ajuste dinâmico Fit-to-Width para visualizadores de PDF e páginas HTML em splits, recalculando sob
     redimensionamento e pausas no zoom) e PR `#39597` / issue `#39596` (cancelamento atômico de prompts de encerramento via IPC
     `window:close-cancelled`, desarmando a flag `isQuitting` no processo principal e evitando travamento de saída em branco).
3. **Atualização de 5 issues existentes em `work/issues/`:**
   - [Seletor de branches na status bar e suporte a workspaces em pastas multirrepositório](../issues/seletor-de-branches-na-status-bar-e-suporte-a-workspaces-em-pastas-multirrepositorio.md):
     adicionado o PR `#39637` (resolução unificada de seletores `path:` e `name:` para folder workspaces via capability
     `workspace-selector.folder-match.v1` e diferenciação de workspaces de mesmo ID em múltiplos hosts no `worktree ps`).
   - [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md):
     adicionados o PR `#39599` / issue `#39598` (variáveis de ambiente `ORCA_WORKER_AUTO_RELEASE` e `ORCA_WORKER_AUTO_RELEASE_GRACE_SECONDS`
     para desligar ou estender o tempo de carência de auto-release de workers em servidores `orca serve`) e a issue `#39631`
     (correção de falha espúria `run_home_unreachable` em `orchestration reply` para mensagens de status).
   - [Segurança de hooks em worktrees e integridade de setup em automações](../issues/seguranca-de-hooks-em-worktrees-e-integridade-de-setup-em-automacoes.md):
     adicionados o PR `#39229` / issue `#39617` (opção opt-in por agente sob Full access para dispensar o hook `PermissionRequest` do Orca,
     permitindo que o Claude Code 2.1.319+ execute sem emitir advertências ou travar em recusas embutidas) e a issue `#39609`
     (mitigação de relançamento de `claude --resume` no worktree errado após atualização decorrente de colisão de `ptyId`s numéricos legados).
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados o PR `#39606` / issue `#37379` (supressão de marcações de texto de harness do Claude como `<local-command-caveat>` nos
     títulos de abas após comandos `/clear`) e a issue `#39619` (isolamento de sessões irmãs do OpenCode no mesmo serviço compartilhado
     para que abas ociosas não fiquem presas exibindo o spinner de trabalho).
   - [Validação de conclusão em automações, CLI de extensões e destravamento de rate limit](../issues/validacao-de-conclusao-em-automacoes-cli-de-extensoes-e-destravamento-de-rate-limit.md):
     incorporado o PR `#39613` (atendendo à issue `#39578`), adicionando os comandos `orca extension list` e `orca extension reload` na CLI.

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-08)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues criados ou
   atualizados entre `2026-11-08T03:00:00Z` e `2026-11-08T09:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Agente Kiro no Native Chat, janela flutuante e endereçamento de workspaces](../issues/agente-kiro-no-native-chat-janela-flutuante-e-enderecamento-de-workspaces.md):
     rastreia o PR `#39769` (resolve Issue `#30095`, integrando Kiro como agente nativo de chat sobre ACP com seletor de modelos, 6 níveis de reasoning effort e aprovações interativas),
     o PR `#39733` (unificação da regra de enclosing workspace via `resolveEnclosingWorkspace`, suporte a `--environment local` e `--parent-environment`, saída copiável `address:` em `ps`/`show` e recusa de `worktree rm --worktree current|active`),
     o PR `#39722` (atendendo à Issue `#22167`, permitindo abrir o terminal ativo de Floating Workspaces em janela Electron destacada),
     o PR `#39692` (abertura rápida do seletor de branches ao clicar no nome do branch exibido sob o composer de chat) e
     o PR `#39741` (resolve Issue `#39728`, corrigindo pareamento mobile quando o servidor `orca serve` usa bind fixado em interface de rede/Tailscale).
3. **Atualização de 4 issues existentes em `work/issues/`:**
   - [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md):
     adicionadas a Issue `#39807` (sobrecarga crítica em `worker-list` onde a ausência de expurgo faz leituras levarem até 35 minutos) e
     a Issue `#39694` (rejeição espúria `worker_identity_changed` ao emitir `worker_done` em workers auto-liberados e reabertos).
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionado o PR `#39649` (resolve Issue `#39619`, contendo o broadcast de sequências de escape OSC 7501 do OpenCode em modo de serviço compartilhado para não marcar abas ociosas com status `working`).
   - [Melhorias de Native Chat, ACP do Gemini CLI, abas e diff no upstream](../issues/melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream.md):
     adicionada a Issue `#39742` (notificação falsa "The native Antigravity account changed" disparada após cada worker run do `agy` por comparação de hash em tokens atualizados).
   - [Segurança de hooks em worktrees e integridade de setup em automações](../issues/seguranca-de-hooks-em-worktrees-e-integridade-de-setup-em-automacoes.md):
     adicionadas a Issue `#39771` (perda de status de agente na UI quando `claude` no PATH é symlink para wrapper launcher),
     a Issue `#39714` (falha no SessionStart hook por erro de permissão no `printf`) e
     a Issue `#39736` (exceção `FileNotFoundError` no hook do Hermes após remoção de `cwd` em tarefas Kanban).
