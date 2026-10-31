---
name: o-log-de-medicao-como-dado
description: Onde ficam o log de medição, o estado dos hooks e os transcripts que servem de evidência numa revisão do workspace
metadata:
  type: reference
---

- **O log:** `~/Projects/brza-workspace/.measurements/measurements.jsonl` (o da `master`, pela `BRZA_WORKSPACE`); o
  `.measurements/` de um worktree pode existir e ser velho, de sessão sem a variável.
- **O estado do `fact_audit.py`:** `.measurements/fact-audit-state.json` (offset e ids vistos por transcript); o arquivo
  da rodada em `.measurements/fact-audit/` some ao fim.
- **Transcript de subagente:** `~/.claude/projects/<cwd com - no lugar de />/<session>/subagents/agent-<id>.jsonl`.
- **Sessão `claude -p` da auditoria:** `~/.claude/projects/<cwd do subagente>/<session>.jsonl`; achar por
  `grep -l "auditor dos fatos"`. O `turn` dela no log leva `fact_audit: true` e o `session_id`.
- **Os testes não sujam o log real** (usam `MEASURE_DIR`): `wc -l` antes e depois confirma.
