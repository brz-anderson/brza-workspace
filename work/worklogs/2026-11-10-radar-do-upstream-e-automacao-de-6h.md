---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-10
completed: 2026-11-10
tags:
  - tooling
refs:
  - issue:badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes
  - issue:bifurcacao-de-conversas-no-chat-ui-e-resiliencia-de-inicializacao-do-claude
  - issue:historico-de-navegacao-no-editor-e-identificacao-de-workspaces-por-plugins
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-10)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-09T21:00:00Z` e `2026-11-10T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Badges de worktree para plugins, cadência de PR e redesenho de automações](../issues/badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes.md):
     rastreia o PR `#40557` (ponto de contribuição `contributes.worktreeBadges` nos manifestos de plugins, avaliando `when.pathExists`
     com `searchDepth: 0..3` e exibindo badges com menu de ações dedicado na sidebar),
     PR `#40541` / STA-8667 (cadência configurável de auto-refresh de PRs e CI checks em `Settings → Git & Source Control → PR Auto-Refresh`:
     Default 1-2min, Reduced 5-10min, Minimal 10-20min, Off),
     PR `#40507` (redesenho completo da visualização de detalhes de automações `AutomationDetailOverview`, com cabeçalho limpo,
     faixa de saúde com métricas/custos de tokens, prompt expansível com botão de cópia e ações destrutivas em menu dropdown "…"),
     PR `#40534` (eliminação da varredura global em rajada de issues vinculadas do GitHub ao restaurar o foco da janela, restringindo
     a cartões visíveis no viewport `visible-only` com janela de 5 min e liberando a fila da CLI),
     PR `#40539` / STA-2380 (verificação de comando desenhado `hasTerminalCommandPainted` após o marcador OSC 133;C no estado `tui-idle`
     para evitar injeções prematuras de tarefas em inicializações a frio do Claude Code no terminal) e
     PR `#40540` / issue `#40510` (persistência e restauração do modo tela cheia nativo após reinicialização do app).
3. **Atualização de 2 issues existentes em `work/issues/`:**
   - [Histórico de navegação no editor e identificação de workspaces por plugins](../issues/historico-de-navegacao-no-editor-e-identificacao-de-workspaces-por-plugins.md):
     adicionada a issue `#40492` (exposição do `id` unívoco e do caminho absoluto `path` do workspace no resultado de
     `workspace.readContext` e nos argumentos do evento `workspace.changed`, permitindo que linters, observadores e plugins
     amarrem com exatidão suas ferramentas ao diretório raiz correto).
   - [Bifurcação de conversas no Chat UI e resiliência de inicialização do Claude](../issues/bifurcacao-de-conversas-no-chat-ui-e-resiliencia-de-inicializacao-do-claude.md):
     adicionados o PR `#40548` (identidade de chat do Claude mantida estritamente nativa, isolando geração de títulos e processos de
     background sob identidades dedicadas de cliente e delimitando a fronteira de inicialização no SDK sem vazamento para overrides
     de conta), o PR `#40558` (preservação do estado de runtime e mapas de sessões de cada conta Claude durante refresh em background) e
     o PR `#38001` / issue `#37707` (fallback seguro para inicializar um novo chat limpo ao retomar conversas de CLI cujo transcript
     esteja ausente ou corrompido no disco, prevenindo abas travadas).
