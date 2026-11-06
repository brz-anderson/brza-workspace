---
status: open
description: O `move_note.py` troca o caminho do worklog, e o `--by-task` passa a ver duas tarefas.
scope:
  - brza-workflow
opened: 2026-11-06
priority: low
tags:
  - tooling
---

# O worklog renomeado muda a chave da tarefa

## O pedido

Lacuna de medida que o [PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md) deixa,
aberta pela R1.3 ("sempre abra issue para lacunas deixadas") e pelo D7 do Desenho.

## O que se sabe

A tarefa é o caminho do worklog nos eventos `task`. O rename depois de um commit deixa os eventos antigos no caminho velho.
