---
name: estado-muda-durante-a-revisao
description: Neste workspace outras sessões editam e commitam o mesmo worktree durante a revisão; reconferir git log/diff antes de devolver, porque achados viram falsos e linhas mudam
metadata:
  type: feedback
---

Antes de gravar o parecer e de devolver, rode `git log --oneline -5` e `git status --short` no worktree alvo de novo e
compare com o começo da revisão.

**Why:** na revisão do PLN-009 (2026-11-03), a sessão principal gravou a Entrevista R1 no plano revisado e outra sessão
(Antigravity, P0) commitou o Desenho do PLN-003 (`ecd380e`) no meio do trabalho. Um achado de confiança 95 ("o `[x]`
do P0 tem evidência falsa") virou falso, e as linhas citadas do Desenho deslocaram ~15.
**How to apply:** cite as linhas do estado final; o achado que caiu por mudança no meio vai como `→ falso (no estado
atual)`, com o commit que o derrubou. Relacionado: [[padroes-de-erro-em-planos-extraidos]].
