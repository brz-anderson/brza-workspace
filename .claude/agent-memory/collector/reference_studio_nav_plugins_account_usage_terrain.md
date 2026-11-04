---
name: studio-nav-plugins-account-usage-terrain
description: Onde moram reveal/foco de chat, seleção da barra lateral, Jump Palette, API de plugins e account usage (#37467) no brza-studio; armadilhas do levantamento
metadata:
  type: reference
---

- Foco de aba: RPC `terminal.reveal` (`src/main/runtime/rpc/methods/terminal/terminal-lifecycle-methods.ts`) -> relay `src/main/window/terminal-pane-reveal-relay.ts` (traz a janela) -> renderer `lib/reveal-terminal-pane.ts`, só terminal. O análogo de chat é `components/dashboard/reveal-dashboard-agent.ts` + `lib/agent-session/structured-agent-session-tab-activation.ts`. `agentSession.reveal` existe (`structured-agent-session-reveal.ts`), é de mobile/histórico.
- Barra lateral de agentes: `useState selectedPaneKey` em `components/sidebar/SidebarAgentsList.tsx`; destaque do card em `sidebar/focused-agent-row-highlight.ts` (só terminal).
- Jump Palette: `lib/workspace-tab-palette-content-type.ts` + `-entry-builder.ts` + `-activation.ts`.
- Plugins: `src/main/plugins/workers/plugin-workspace-projection.ts`, `plugin-host-service-bindings.ts` (descarta `path` de propósito), schemas em `src/shared/plugins/{workers,events}`, doc `docs/reference/plugin-host-api.md`. Chat já publica status no hook server (`agent-hook-runtime-deps.ts:29`), então `agents.list` pode já listar chats.
- #33139/#37467 e #37801/#37807/#37615 de issues do upstream: `gh pr view` falha em issue; use `gh issue view`.
- zsh: `--include=*.ts` sem aspas dá "no matches found"; use aspas.
- Não use `git checkout-index --stage=all` no repo alvo: deixa `.merge_file_*` no cwd (limpei). Para ver conflito, leia `git diff` no índice temporário.
- Fork e upstream/main idênticos nos arquivos de nav/plugins em 2026-11-03: relatos do upstream conferem sem checar versão.
