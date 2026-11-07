---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-07
completed: 2026-11-07
tags:
  - tooling
refs:
  - issue:bifurcacao-de-conversas-no-chat-ui-e-resiliencia-de-inicializacao-do-claude
  - issue:gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache
  - issue:historico-de-navegacao-no-editor-e-identificacao-de-workspaces-por-plugins
  - issue:subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent
---

# Radar de issues e PRs do upstream e automação de 6h (ciclo 00h BRT / 03h UTC)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-07)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados mais de 50 novos PRs e issues criados ou
   atualizados entre `2026-11-06T21:00:00Z` e `2026-11-07T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl` para evitar duplicidade de assuntos já rastreados.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Histórico de navegação no editor e identificação de workspaces por plugins](../issues/historico-de-navegacao-no-editor-e-identificacao-de-workspaces-por-plugins.md):
     rastreia o PR `#39162` (`editor.navigateBack` / `editor.navigateForward` com atalhos `Cmd+[` / `Cmd+]` no macOS e `Alt+Left` / `Alt+Right`
     no Windows/Linux, pilha de histórico de posições de cursor e reabertura de abas fechadas por workspace), issue `#39177`
     (resolução inequívoca com `workspaceId` em `workspace.readContext` para plugins, prevenindo colisão em projetos múltiplos
     com mesmo `displayName` e branch `primary/main`), issue `#39176` (API `workspace.createFromRecipe` para criação programática
     de workspaces a partir de templates corporativos sem redigitação no chat) e issue `#39267` (acordar silencioso de workspaces
     em repouso sem disparar terminais/PTYs desnecessários na inspeção passiva de arquivos).
3. **Atualização de 3 issues existentes em `work/issues/`:**
   - [Bifurcação de conversas no Chat UI e resiliência de inicialização do Claude](../issues/bifurcacao-de-conversas-no-chat-ui-e-resiliencia-de-inicializacao-do-claude.md):
     adicionado o PR `#39168` (replicação fiel do registro de conversa serializado da UI do app ao acionar fork, preservando histórico
     visual, formatação, timestamps e recibos imutáveis de identidades nativas herdadas para não duplicar turnos futuros do modelo).
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     adicionado o PR `#39169` (continuação imediata de conversas em limite de uso de 5h ao trocar de conta no Claude switcher,
     conectando o evento `onSwitched` ao dispatch de `continueUsageLimit`).
   - [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md):
     adicionadas a issue `#39263` (subcomando `orca orchestration reply --decision user|technical` vinculando a classificação da
     resposta ao Run/Dispatch para auditoria de dúvidas de workers) e a issue `#39262` (mitigação de descarte silencioso de mensagens
     de correio com `accepted: true` em workers remotos).
