---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-11
completed: 2026-11-11
tags:
  - tooling
refs:
  - issue:alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas
  - issue:autenticacao-mcp-no-chat-alerta-de-turnos-ativos-e-cache-de-orquestracao
  - issue:notificacao-de-perda-de-workers-desengasgo-de-correio-e-tipo-notice
  - issue:seguranca-de-hooks-em-worktrees-e-integridade-de-setup-em-automacoes
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-11)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-10T21:00:00Z` e `2026-11-11T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Notificação de perda de workers, desengasgo de correio e tipo notice](../issues/notificacao-de-perda-de-workers-desengasgo-de-correio-e-tipo-notice.md):
     rastreia o PR `#40983` (alerta unificado `lost` ao coordenador quando workers falham no startup, sofrem fechamento de painel, queda de PTY ou encerramento inesperado, prevenindo esperas infinitas),
     PR `#40972` (introdução do tipo de mensagem `notice` para despachos interagentes com `--to`, eliminando interrupções espúrias e comandos reply desnecessários),
     PR `#40977` / issue `#40968` (desengasgo de filas de relay ao responder a `send --type question` de workers remotos em servidores pareados),
     PR `#40967` e PR `#40963` (recuperação de workers de chat e reabertura de terminais interrompidos com o restart da aplicação),
     PR `#40949` (encerramento limpo de sessões e relato de pareamento desfeito ao remover servidores remotos) e
     PR `#40962` / issue `#40956` (substituição de subshell intermediário por `exec` no profile do Claude, evitando falhas `agent_not_in_foreground` sob bash).
3. **Atualização de 3 issues existentes em `work/issues/`:**
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados o PR `#40986` / issue `#40984` (descoberta e exibição de skills instaladas do Antigravity no menu slash `/` do Native Chat),
     o PR `#40980` / issue `#40979` (descoberta dinâmica de modelos recém-lançados via CLI host `agy` para o picker de novos chats),
     o PR `#40867` / issue `#40865` (injeção automática de regras de usuário e workspace `AGENTS.md` e `GEMINI.md` no prompt ACP via `_meta.antigravity.systemPrompt.append`) e
     o PR `#40912` (composer e escolha de modelos desbloqueados no primeiro chat de novos worktrees).
   - [Autenticação MCP no chat, alerta de turnos ativos e cache de orquestração](../issues/autenticacao-mcp-no-chat-alerta-de-turnos-ativos-e-cache-de-orquestracao.md):
     adicionados o PR `#40953` / issue `#40640` (diálogo de aviso antes de fechar janela com agentes em turno ativo no Native Chat `mid-turn`) e
     o PR `#40923` / issue `#40607` (remoção definitiva de hook incompatível no Factory Droid).
   - [Segurança de hooks em worktrees e integridade de setup em automações](../issues/seguranca-de-hooks-em-worktrees-e-integridade-de-setup-em-automacoes.md):
     adicionados o PR `#40978` / issue `#40974` (comando `/hooks` para revisão e homologação criptográfica de hooks do Codex diretamente no chat) e
     o PR `#40976` (cartão unificado e condensado para hooks de worktree nas configurações).
