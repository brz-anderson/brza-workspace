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
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:seguranca-de-hooks-em-worktrees-e-integridade-de-setup-em-automacoes
  - issue:seletor-de-branches-na-status-bar-e-suporte-a-workspaces-em-pastas-multirrepositorio
  - issue:subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent
  - issue:titulos-de-janela-para-time-trackers-ajuste-de-visualizadores-e-resiliencia-de-saida
  - issue:validacao-de-conclusao-em-automacoes-cli-de-extensoes-e-destravamento-de-rate-limit
---

# Radar de issues e PRs do upstream e automação de 6h (00h BRT)

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
