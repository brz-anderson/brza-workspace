---
scope:
  - workspace
  - brza-studio
refs:
  - PLN-003
---

# O PLN-003: a medição das hipóteses da fase 0 (P0)

Executado o passo **P0** do [PLN-003](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md) (R7.3) na sessão
`antigravity_462439a0_03c3_483b_a0db_e72f48caf392` ("PLN-003 P0: Medição da fase 0"), validando empiricamente as seis
hipóteses técnicas da fase 0 (**H1 a H6**) contra o Claude Code `2.1.317`, o `@anthropic-ai/claude-agent-sdk` `0.3.284`
embutido nos dois apps (`BrzA Studio.app` e `Orca.app`), o daemon `orca-runtime` do BrzA Studio e um servidor MCP HTTP/SSE
protótipo em Python `3.15` stdlib.

Todas as seis hipóteses (**H1 a H6**) foram **confirmadas**, com ajustes técnicos registrados diretamente nos itens
`D3`, `D4`, `D5`, `D6` e `D7` do [Desenho](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-design.md).

## O que rodou e o que deu

### 1. H1 — Expansão de `${ORCA_AGENT_SESSION_ID}` no `.mcp.json` (sobre D3 e D4 — M12)

- **Sonda:** plugin temporário em `scratch/probe-plugin/` com `.mcp.json` apontando para o servidor MCP local em
  `http://127.0.0.1:14242/mcp`, cabeçalho `"X-Brza-Session": "${ORCA_AGENT_SESSION_ID}"` e `"Authorization": "Bearer ${BRZA_MCP_TOKEN}"`.
- **No CLI (`claude -p --plugin-dir`):** com `ORCA_AGENT_SESSION_ID=orca_session_probe_h1_ok`, o servidor recebeu 6
  requisições HTTP (`POST /mcp` `server/discover`, `POST /mcp` `initialize`, `POST /mcp` `notifications/initialized`,
  `GET /mcp` SSE, `POST /mcp` `tools/list`, `POST /mcp` `tools/call`) — todas com `"x-brza-session": "orca_session_probe_h1_ok"`
  e `"authorization": "Bearer secret_token_123"`. A ferramenta `echo_caller` devolveu o identificador ao modelo (`exit=0`).
- **No SDK dos apps (`@anthropic-ai/claude-agent-sdk@0.3.284`):** chamado via `query({ options: { plugins: [{ type: 'local', path }] } })`
  com `ORCA_AGENT_SESSION_ID=sdk_chat_session_999`, expandiu `"x-brza-session": "sdk_chat_session_999"` em todas as
  requisições e executou `mcp__plugin_brza-probe_brza-orchestrator__echo_caller` com sucesso.
- **Achado crítico para D3:** omitir `"type": "http"` (ou `"type": "sse"`) no `.mcp.json` faz o Claude Code tratar a
  entrada como `stdio` e ignorar a URL (`0` requisições HTTP). O campo `"type": "http"` foi tornado obrigatório em `D3`.

### 2. H2 — `claude -p` com `CLAUDE_CONFIG_DIR` em background sem TTY (sobre D4 e D6 — M6, M11)

- **Sonda:** subprocesso Python isolado com `start_new_session=True` (`setsid()`, sem TTY controlador), `stdin=DEVNULL`,
  `cwd=/tmp` e ambiente mínimo de `launchd` (`HOME`, `USER`, `LOGNAME`, `PATH=/usr/bin:/bin:/usr/sbin:/sbin:/Users/andepb/.local/bin`),
  invocando `claude -p --model haiku --effort low --output-format json --json-schema ... --max-budget-usd 0.01 --no-session-persistence`.
- **Contas gerenciadas (`CLAUDE_CONFIG_DIR` explícito):**
  - `dot-claude-adm` (`~/.claude-adm`): `exit=0`, `4,58 s`, `structured_output={"choice":"A"}`, custo `US$ 0,00376`.
  - `studio-admin` (`~/Library/Application Support/brza-studio/claude-profiles/8eee0e1b-f5d7-40ba-8337-8cae0df3a062/home`, a conta `admin@` do workspace de origem): `exit=0`, `3,29 s`, `structured_output={"choice":"A"}`, custo `US$ 0,00393`.
  - `studio-anderson` (`~/Library/Application Support/brza-studio/claude-profiles/c2e4f85c-388a-4603-8edc-a0844496c902/home`, a conta `anderson@` do workspace de origem): `exit=0`, `4,28 s`, `structured_output={"choice":"A"}`, custo `US$ 0,00162`.
- **Achado crítico para D6 (conta `systemDefault`):** passar `CLAUDE_CONFIG_DIR=/Users/andepb/.claude` explicitamente
  faz o Claude Code calcular um sufixo de hash no serviço do Keychain (`Claude Code-credentials-<hash>`) em vez da chave
  padrão `"Claude Code-credentials"`, falhando com `OAuth session expired and could not be refreshed` (`exit=1`). Omitindo
  `CLAUDE_CONFIG_DIR` para a conta `systemDefault` (como faz `claude-profile-router.ts:155-161` no `brza-studio`), a chamada
  passa (`exit=0`, `result="OK"`). `D4` e `D6` foram atualizados com essa regra e com o `PATH` do `launchd`.

### 3. H3 — `agentSession.switchAccount` em sessão de chat (sobre D6 e D7 — M6)

- **Suíte de testes do `brza-studio`:** `vitest run src/main/claude/claude-account-switch.test.ts src/main/native-chat/agent-session-wire/structured-agent-session-account-switch.test.ts` → **6 arquivos / 15 testes verdes (`3,42 s`)**.
- **Sonda ao vivo no socket RPC (`orca-runtime.json`):**
  - Criada sessão temporária `claude_d8fa320f_4040_42bc_83e1_9ab32e8eddd4` (`fence: 1`, `sequence: 1`).
  - `agentSession.switchAccount` para `8eee0e1b-f5d7-40ba-8337-8cae0df3a062` (a conta `admin@` do workspace de origem) → `ok: true`, `sequence: 2`.
  - `agentSession.switchAccount` para `c2e4f85c-388a-4603-8edc-a0844496c902` (a conta `anderson@` do workspace de origem) → `ok: true`, `fence: 2`, `sequence: 3`.
  - `copyClaudeTranscriptsToAccount` (`src/main/claude/claude-account-switch-transcript.ts:20-58`) copia atomicamente o `.jsonl` e a pasta de subagentes para `projects/` da conta destino antes do próximo turno `--resume`.
  - Em sessão **em turno ativo (`in-run`)**, o runtime recusa com `agent_session_operation_invalid` (`details: {"reason": "turnActive"}`, `"Wait for the current turn to finish before using this command"`).
- **Achados críticos para D6 e D7:** `agentSession.switchAccount` é método RPC do socket local (`orca-runtime.json`, com `MutationEnvelope`), não subcomando da CLI, e só opera em sessão em repouso (`at-rest`).

### 4. H4 — `orca orchestration` fora do shell e vínculo com a sessão chamadora (sobre D5 — M13)

- **Sem `ORCA_AGENT_SESSION_ID` no `env`:** `run-list` funciona (`exit=0`), mas `run-create` a partir de `/tmp` falha com
  `no_active_sender_terminal` (quando não há terminal único) ou vincula a Run a um terminal aberto ao acaso (`run_a244fac8b97f`),
  e tentar operar na Run de um chat recebe `consumer_fenced`. Declarar `--from orca_session_id:<id>` sem a variável no `env`
  é bloqueado por `orchestration-party.ts:99` (`session_caller_chat_not_declarable`).
- **Com `ORCA_AGENT_SESSION_ID=<valor de X-Brza-Session>` injetado pelo MCP no subprocesso** (e `ORCA_USER_DATA_PATH` do
  client ativo), mesmo de `cwd=/tmp` e sem `ORCA_TERMINAL_HANDLE`, `ORCA_PANE_KEY` nem `ORCA_AGENT_SESSION_SPAWN_TOKEN`:
  - `brza orchestration run-create` → `exit=0`, `runId: "run_185d85625d65"`.
  - `brza orchestration task-create --run run_185d85625d65 --task-title "Probe H4 task" --spec "Spec H4"` → `exit=0`, `taskId: "task_677fb72d6e08"`.
  - `brza orchestration task-update --id task_677fb72d6e08 --status completed` → `exit=0`.
- **Achado crítico para D5:** o daemon MCP repassa `ORCA_AGENT_SESSION_ID` (recebido no header `X-Brza-Session` validado em H1) e `ORCA_USER_DATA_PATH` no `env` de cada chamada a `orca orchestration`.

### 5. H5 — Servidor MCP HTTP/SSE só com Python 3 stdlib (sobre D4 — B6)

- **Sonda:** `scratch/mcp_stdlib_server.py` (~160 linhas, usando apenas `http.server.ThreadingHTTPServer`, `BaseHTTPRequestHandler`,
  `json`, `queue`, `threading`, `urllib.parse` e `uuid`), implementando **Streamable HTTP** (`POST /mcp` + `GET /mcp` SSE) e
  **SSE legado** (`GET /sse` + `POST /messages`).
- **Resultado:** handshake completo, `tools/list` e `tools/call` executados com `exit=0` tanto pelo `claude -p` (`2.1.317`)
  quanto pelo `@anthropic-ai/claude-agent-sdk` (`0.3.284`).
- **Achado crítico para D4:** o uso de `ThreadingHTTPServer` com `protocol_version = "HTTP/1.1"` e `Content-Length` explícito
  é obrigatório porque o Claude Code mantém um `GET /mcp` (SSE) aberto em paralelo aos `POST /mcp` de `tools/list` e `tools/call`.

### 6. H6 — `workflows/*.js` pelo SDK nos dois apps (sobre D3 — B9)

- **Sonda:** ambos os apps (`BrzA Studio.app` e `Orca.app`) usam `@anthropic-ai/claude-agent-sdk@0.3.284` apontando para
  `~/.local/bin/claude` (`2.1.317`). Testado `workflows/review.js` no plugin `brza-probe` via `query()` do SDK com ambiente
  padrão (sem `CLAUDE_CODE_WORKFLOWS=1`).
- **Resultado:** `SYSTEM: init` expôs a ferramenta `Workflow` e o skill `brza-probe:review`; o modelo invocou
  `Workflow {"name": "brza-probe:review"}`, disparou `task_started` (`task_type: "local_workflow"`), executou o subagente
  definido em `await agent(...)` em `2,3 s` e retornou `WORKFLOW_STAGE_OK`.
- **Achado crítico para D3 (P11):** o validador AST (Acorn) do Claude Code exige:
  1. `export const meta = { name, description, whenToUse, phases }` literal no topo;
  2. nenhum outro `export` no arquivo (proibido `export default`; o resultado sai por `return` no nível superior do script);
  3. `phase("<título>")` como instrução simples (sem callback) e `await agent("<prompt>", { label, model, tools, schema })`
     com o prompt como 1º argumento posicional.

## Retomar

O P0 está concluído e os itens `D3` a `D7` do Desenho estão atualizados. O próximo passo do
[PLN-003](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md) é o **P1** (o índice da `master` com
`priority`, `blocks` e `deadline` no `scripts/brza/brza-note`), seguido do **P2** (a CLI `brza` unificada).

## Fora do workspace

- **O quê e onde:** sessão de chat temporária `claude_d8fa320f_4040_42bc_83e1_9ab32e8eddd4` ("Probe H3 switchAccount"),
  criada via RPC no BrzA Studio para testar `agentSession.switchAccount`. **Risco:** nenhum. **Estado:** fechada via
  `agentSession.close` (`status: closed`). **Como desfazer:** já desfeito.
- **O quê e onde:** duas Runs de teste (`run_a244fac8b97f` e `run_185d85625d65`) e a task `task_677fb72d6e08` ("Probe H4 task")
  no SQLite de orquestração do BrzA Studio (`~/Library/Application Support/brza-studio/orchestration/`). **Risco:** nenhum;
  a task `task_677fb72d6e08` foi marcada como `completed` e não há workers ativos. **Estado:** encerrada (`completed`).
  **Como desfazer:** já encerrada; os registros históricos não afetam novas Runs.
- **O quê e onde:** servidor MCP de teste em `127.0.0.1:14242` e arquivos temporários de sessão do SDK em
  `~/.claude/projects/-Users-andepb-Library-Application-Support-brza-studio-antigravity-chat-antigravity-acp-brain-e3c4daa9-33f1-4165-8fb4-b97c3459f025-scratch/`.
  **Risco:** nenhum. **Estado:** processo encerrado e diretório de transcripts temporários removido; os scripts de sonda
  permanecem apenas no diretório `scratch/` da conversa. **Como desfazer:** já desfeito.
