---
name: where-things-live
description: Onde mora cada assunto de brza sessions/MCP/orquestrador/medição e as buscas que poupam leitura
metadata:
  type: reference
---

- `brza sessions` = `~/Projects/brza-workflow/packages/client/bin/brza-sessions` (~500 linhas, ler inteiro); o runtime/RPC em `bin/brza_runtime.py` (`rpc`, `send_to_chat`).
- MCP = `packages/mcp/brza_mcp/`: `tools.py` (dispatch/status/config, gates), `policy.py` (papéis, DEFAULTS), `cycle.py` (abre worker via `brza orchestration run-create/task-create/worker-start`), `telemetry.py` (só linhas `route`).
- `brza agent launch` e `orchestration *` são do app: ver pelo `--help` (`/Applications/BrzA Studio.app/Contents/Resources/bin/brza`, roda sem efeito); fonte em `~/Projects/brza-studio/src/cli/specs/agent-launch.ts`. RPCs `agentSession.*` estão em `brza-studio/src/main` e `src/shared/rpc-contract`; quase nenhum tem verbo no CLI.
- `brza-workflow` master NÃO tem `plans/` nem `work/`; os planos (PLN-009/010/012/013) moram em `workstream/tools-kit`, lidos com `git show workstream/tools-kit:plans/...`.
- `brza-shot` mora em `brza-workspace/scripts/brza/brza-shot`, não no brza-workflow.
- Hook de medição: `brza-workflow/core/.claude/hooks/measure.py` (só Claude; grep de codex/grok/antigravity = 0).
- Mapa de sessões: `brza-workspace/.sessions/sessions.jsonl`.
- Armadilha: no shell zsh, `grep --include=*.ts` sem aspas dá "no matches found"; usar aspas ou `-l` sem include.
- Fonte velha: a memória de `memory/` do worktree é só de feedback de reunião; nada de código.
