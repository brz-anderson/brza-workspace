---
name: commit-ao-fechar-todo-passo
description: "Sempre realizar o commit imediatamente ao fechar todo passo de um plano, sem parar para pedir confirmação antes de commitar"
metadata:
  node_type: memory
  type: feedback
  originSessionId: e3c4daa9-33f1-4165-8fb4-b97c3459f025
  modified: 2026-11-03T06:15:35.000Z
---

Ao fechar qualquer passo de um plano (com os critérios atendidos, os testes verdes e a evidência registrada no plano), o `commit` deve ser realizado diretamente como parte do fechamento do passo, sem parar para pedir confirmação prévia antes de commitar.

**Why:** Anderson instruiu em 2026-11-03, ao fechar o P0 do PLN-003: "sempre, ao fechar todo passo, deve ser realizado o `commit`". O pedido explícito de executar o passo já inclui o commit de fechamento dele.

**How to apply:**
- Ao concluir um passo (código e/ou notas em `plans/` e `work/`), rode os testes/checadores cabíveis (`check_notes.py` e suíte do passo) e faça o `commit` imediatamente, registrando o hash na evidência e na resposta.
- Selecione no `git add` apenas os arquivos pertencentes ao passo para não misturar arquivos em edição por outra sessão concorrente no mesmo worktree.
