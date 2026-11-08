---
name: brza-studio-mapa
description: Onde mora cada assunto no brza-studio (native chat, dashboard, crew, plugins, CLI de chats) e armadilhas de busca
metadata:
  type: reference
---

Mapa do `~/Projects/brza-studio` (fork do Orca) para levantamentos de UI/chat/plugins.

- **Origem da mensagem / cartão de agente**: `src/shared/agent-session/agent-session-message-source.ts`, `agent-message-presentation.ts`; renderer em `src/renderer/src/components/native-chat/NativeChatAgentMessageCard.tsx`. Origem nossa em `src/shared/native-chat/brza/`.
- **Visão de conjunto**: não existe "FleetView". É o Agent Dashboard (`components/dashboard/`, `src/shared/dashboard-snapshot.ts`) e a lista "activity threads" (`components/sidebar/SidebarAgentsList.tsx`, `components/activity/`).
- **Crew panel (equipe de orquestração)**: `components/orchestration-crew/`, modelo `src/shared/orchestration-crew.ts`; está desligado (`use-orchestration-panel-enabled.ts` devolve `false`).
- **Visuals**: skill em `resources/native-chat-visuals/skills/orca-chat-visuals/SKILL.md` (não em `skills/`), shell em `src/shared/native-chat/native-chat-visual-shell.ts`.
- **Plugins**: docs em `docs/reference/plugin-*.md` (geradas; manifest e host-api são as úteis); `contributes.sidebarCards` é reservado.
- **Orquestração**: guia em `skill-guides/orchestration.md` + `references/`; specs da CLI em `src/cli/specs/orchestration*.ts`. Gates só na CLI, sem UI.
- **CLI `chat list/read/send`**: só na branch `feat/pln-011-chat-cli` (worktree `.worktrees/pln-011-chat-cli`), não na `master`.

**Armadilhas**
- O `PLN-011-design.md` foi escrito antes do sync da 251: a Jump Palette já inclui chats na `master`; confira o código antes de repetir o design.
- `grep --include=*.ts` sem aspas falha no zsh; use `--include='*.ts'`.
- Não há `CLAUDE.md` no `brza-studio`; só `AGENTS.md` (curto, 66 linhas), que exige remoto + mobile em toda UI.
- As issues do playground sobre PRs/CI/cartões descrevem PRs do upstream, não o que o fork já tem.
