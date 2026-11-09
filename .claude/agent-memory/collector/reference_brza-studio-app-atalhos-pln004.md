---
name: reference-brza-studio-app-atalhos-pln004
description: Onde mora cada peça do brza-studio que o PLN-004 cruza (override, trust, hooks do Grok/Codex/agy, subagentes no chat) e os caminhos que mudaram depois de 2026-11-03
metadata:
  type: reference
---

Levantado em 2026-11-09 no `brza-studio` `8abbde720ce` (confira `git rev-parse` antes de reusar).

- **Spec ACP por agente:** `src/main/acp/acp-launch-specs.ts` (Grok :171-203, Antigravity `ignoreAgentCommandSetting` :296); override: `src/shared/agent-launch/startup/tui-agent-launch-command-override.ts` e `src/main/native-chat/structured-agent-command-resolution.ts`; Codex `[...prefixArgs, ...args, 'app-server']` em `src/main/codex/structured/launch/codex-structured-launch-resolution.ts:126`.
- **Trust:** `preflightTrust` mora em `src/shared/agent-launch/catalog/tui-agent-config.ts` (grok :284 sem ele); gravadores em `src/main/agent-launch/trust/`; só roda em terminal novo, não na ACP.
- **Hooks gerenciados pelo app:** `src/main/<agente>/hook-service.ts`, registro em `src/main/agent-hooks/managed-agent-hook-registry.ts`; gravam em `~/.grok/hooks/orca-status.json`, `~/.codex/hooks.json`, `~/.gemini/config/hooks.json` (global, gate `ORCA_PANE_KEY`, `agentStatusHooksEnabled` padrão true). O Grok mescla hooks global + projeto (`~/.grok/docs/user-guide/10-hooks.md:64-71`).
- **Atalho que poupou leitura:** `git log --since=<data> --format='%h %cs %s' master | grep -iE '...'` filtra bem, mas esconda `test: remove low-value` (centenas) com `grep -v`; 1249 commits em 10 dias, quase tudo refactor/teste. `git log -S` com `--diff-filter=A` acha quando um arquivo nasceu.
- **Caminhos velhos:** levantamento do Grok de 2026-11-03 e a issue do `studio` sobre Codex-subagente citam arquivos movidos (`codex-collab-agent-item-translation` agora em `codex/structured/items/`, `acp-session-runtime.ts:143` -> :163). Refactors "group … owners" (d5f2a17cd20, 8417fa890af) mudam pastas sem mudar comportamento.
- **Não existe no app:** persona, reunião multiagente (o que há é orquestração coordenador/worker), MCP próprio, `GROK_MEMORY`/`--trust` para o Grok.
- No zsh, `grep ... --include=*.ts` sem aspas falha ("no matches found"); use `--include='*.ts'`.
