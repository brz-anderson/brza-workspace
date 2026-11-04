---
name: pln-013-terreno-atalhos
description: Onde moram brza sessions, MCP, validação do worker-start e estado dos runtimes (grok/codex/agy) e que atalhos de leitura funcionaram
metadata:
  type: reference
---

- **brza sessions:** `brza-workflow/packages/client/bin/brza-sessions` (~425 linhas); testes `tests/cli/test_brza_sessions.py`.
- **MCP:** `brza-workflow/packages/mcp/brza_mcp/{tools,accounts,cycle,limits,policy}.py`; testes `tests/mcp/` (358 OK; `unittest discover -s tests/mcp`).
  Fixture real do `account list`: `tests/mcp/fixtures/orca-account-list.json`.
- **Validação do worker-start --agent:** `brza-studio/src/main/runtime/rpc/methods/orchestration/worker/worker-start-validation.ts` (isTuiAgent + `disabledTuiAgents`); modo chat/terminal em `src/main/agent-launch/agent-launch-mode.ts`; ACP em `src/main/acp/acp-launch-specs.ts`.
- **Atalho que poupou leitura:** chamar o app por `brza_runtime.rpc` em Python (`session.tabs.listAll`, `agentSession.history`, `settings.getAgentLaunch`) dá a forma REAL; o `orca account list --json` idem. O JSON real contradiz a doc (tab usa `agent`, não `agentSessionAgent`).
- **Fonte velha:** README do `~/.grok` não lista `/rename`; o `strings` do binário sim. `which codex/agy` pode dar função de shell: use `readlink -f /opt/homebrew/bin/codex` e `~/.local/bin/agy`.
- **Rodar `tests/cli` dentro de um worktree com BRZA_WORKSPACE herdado** faz 4 testes de `test_brza_sessions` falharem por ambiente; `discover -s tests/cli` passa de 120 s (mande para background).
- zsh: `grep --include=*.ts` sem aspas dá "no matches found"; use `--include='*.ts'`.
