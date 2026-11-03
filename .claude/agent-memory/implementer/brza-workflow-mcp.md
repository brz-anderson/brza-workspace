---
name: brza-workflow-mcp
description: Armadilhas de teste e ambiente ao implementar no brza-workflow (packages/mcp, tests/cli) no PLN-009
metadata:
  type: project
---

- `tests/cli` do brza-workflow leva ~150 s (passa do timeout de 120 s do Bash): rode em segundo plano com saída para arquivo e espere com `until grep -qE "^(OK|FAILED)" arq; do sleep 3; done` no Bash com `timeout` alto.
- Em 2026-11-03 o HEAD limpo da `feat/pln-009-mcp` já tem 20 falhas em `test_brza_note` (19) e `test_brza_sessions.CommandTest` (4 de mesma origem); verifique com `git archive HEAD | tar -x -C <tmp>` antes de culpar a mudança.
- Em shell não interativo `kill %1` / `wait %1` não acham o job: guarde o `$!` e use `kill -TERM $PID`.
- `ThreadingHTTPServer`: `shutdown()` espera o `poll_interval` (0.5 s); nos testes use `serve_forever(poll_interval=0.05)`, senão a suíte triplica. Do signal handler, `shutdown` tem de ir numa thread.
**How to apply:** ao acrescentar ferramentas (P3), use `brza_mcp.registry.REGISTRY.register(...)`, sem mexer em `server.py`.
