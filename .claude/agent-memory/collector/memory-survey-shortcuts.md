---
name: memory-survey-shortcuts
description: Atalhos para levantar memórias de outros workstreams sem checkout e conferir contra a norma da master (armadilhas do nome de arquivo, ordem de leitura)
metadata:
  type: reference
---

- Listar/ler memória de outra branch: `git ls-tree -r --name-only workstream/<ws> -- memory .claude/agent-memory` e `git show workstream/<ws>:<f>`; um laço que concatena tudo num arquivo do scratch (cabeçalho `######## ws:caminho`) e `Read` em blocos de ~400 linhas poupa 35 chamadas (126 KB).
- Copiar a norma da master para o scratch: nome com `tr / _` de `.claude/...` vira arquivo **oculto** (`.claude_agents_*.md`); `ls -A` e glob `.[a-z]*`. Em zsh, `echo =====X` falha ("not found"): use aspas.
- Norma de conduta que o grep acha: `conduct.md:48` ("Commite só com confirmação de Anderson") e `AGENTS.md:23` (edição em cerca diff) são as duas que colidem com memórias (2026-11-08).
- Hoje (2026-11-08) a master não tem `.claude/hooks/tests` nem `brza_runtime.py`; tudo foi ao `~/Projects/brza-workflow` (`tests/`, `core/.claude/hooks`, `bin/`). Memória que cita o caminho velho está obsoleta.
- Status de plano em outra branch: `git show workstream/<ws>:plans/<pasta>/<PLN>-plan.md | grep -m1 '^status:'`.
