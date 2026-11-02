---
name: worklog-sem-pedir-autorizacao
description: "Registrar toda tarefa concluída no worklog do dia e commitar pelo brza note commit, sem perguntar a Anderson"
metadata:
  node_type: memory
  type: feedback
  originSessionId: d743a78d-03b5-4f6b-a92a-91aa4894ebaf
  modified: 2026-11-02T23:15:54.751Z
---

Ao concluir uma tarefa, grave o worklog do dia e commite pelo `brza note commit`, sem oferecer nem pedir autorização.

**Why:** em 2026-11-02, depois do revert dos ícones de skill e de MCP, terminei oferecendo o registro no worklog, e Anderson respondeu "registre" e em seguida "sempre registre as tarefas no worklog, sem precisar pedir minha autorização". A pergunta era atrito: a norma do `AGENTS.md` já manda fechar a tarefa num worklog na hora.

**How to apply:** feito o trabalho, inclusive o do `brza-studio`, escreva o worklog (`work/worklogs/AAAA-MM-DD-assunto.md`), rode o `check_notes.py` e o `brza note commit`, e mostre o arquivo na resposta. Não pergunte "quer que eu registre?". Isto vale só para o worklog: commit e push do código no `brza-studio` seguem pedindo a ordem de Anderson. Veja [[upstream-sync-procedure]] para o outro fluxo do `brza-studio`.
