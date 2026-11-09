---
name: reference-brza-workflow-estado-pln004-atalhos
description: Atalhos para cruzar o Desenho do PLN-004 com o brza-workflow vigente (sessions, MCP, measure, summarize, testes); o que envelhece e as armadilhas dos testes
metadata:
  type: reference
---

Confirmado em 2026-11-09 contra `db6bd28` (BW = `~/Projects/brza-workflow`). Complementa [[reference-brza-workflow-depois-da-migracao]].

- **Grep de ausência resolve a metade da tabela D × estado:** `grep -rniE 'codex|grok|antigravity|\bagy\b|brzAgents|\.agents|\.grok|\.codex|GROK_HOOK_EVENT|120000|symlink'` no BW, fora de `tests/**/fixtures`, só acha o que o PLN-013 e o PLN-017 puseram (`packages/mcp/brza_mcp/{runtimes,policy,accounts,limits,tools}.py`, `packages/client/bin/brza-sessions`, `bin/brza-note:253`). `packages/runtimes/`, wrappers, `.brzAgents` e link no sync: 0.
- **Quem entregou o quê:** `3d3d2bb` e `db6bd28` (09/11) são os verbos v2 do `brza sessions` do PLN-017/P4a-P4b, mas a mensagem não cita o plano; a ponte está no plano do PLN-017 em `workstream/playground` (linhas 54 e 159) e nos commits `ff8def8`/`e8f775f` de lá. PLN-013 = `6eda393`…`591f0ed` (04/11); PLN-012 = P1-P5 (06/11) e P3 `4119ec1` (09/11).
- **O `brza sessions` já não usa `agent launch --surface`:** abre por `orchestration worker-start --agent` e só aceita `mode == structured`; sem `--surface`. Citação de `:409-456` do v3 é velha. `chat_blocker` só vale para Claude e devolve `None` dentro do workspace.
- **`measure.py` ganhou 179 linhas (PLN-012):** os números do v3 (`:93`, `:734`, `:619`, `:676`) viraram `:97`, `:913`, `:798`, `:855`. `brza-sync`, `brza-install`, `claude-brza`, `core/AGENTS.md`, `fact_audit.py`, `compact_guard.py` não mudaram desde `d1fa1d7`: as citações deles seguem certas.
- **`summarize_measurements.py` tem 3 caminhos que somam `subagent`** (`aggregate`, `aggregate_by_workstream`, `task_measure`), todos por `estimated_cost_usd`; qualquer `in_parent`/runtime entra nos três. A medida por tarefa liga a sessão pelo `CLAUDE_CODE_SESSION_ID` (`bin/brza-note:719`): runtime sem esse id fica "sem sessão".
- **Testes:** `python3 -m unittest discover -s tests -t .` NÃO roda (tests/ não é pacote); use as 3 suítes do `README.md:182-196` (`tests/cli` leva ~4 min, as outras ~20 s). Com `BRZA_WORKSPACE` herdado o `tests/cli` dá 22 falhas; com `env -u BRZA_WORKSPACE` sobram 2, que vêm do `CLAUDE_CODE_SESSION_ID` da sessão (worklog ganha `sessions:`). Use `-u CLAUDE_CODE_SESSION_ID` também.
- `sed -i` falhou no sandbox ("-I or -i may not be used with stdin"): edite arquivo do scratch com `python3 -I`.
- `brza orchestration worker-start --help` roda sem estado e foi aceito (`/Applications/BrzA Studio.app/.../bin/brza`).
- Fontes de estado de outras branches: `git show workstream/<b>:<caminho> | grep -m1 '^status:'`; PLN-009 e PLN-013 `done`, PLN-010 `open`, PLN-012 `in_progress` (tools-kit), PLN-017 `in_progress` (playground).
