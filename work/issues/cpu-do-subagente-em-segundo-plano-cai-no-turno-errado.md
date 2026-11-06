---
status: open
description: O custo do subagente em segundo plano vai ao turno em que ele começou, e a CPU dele vai ao delta do turno em que termina.
scope:
  - brza-workflow
opened: 2026-11-06
priority: low
tags:
  - tooling
---

# A CPU do subagente em segundo plano cai no turno em que ele termina

## O pedido

Lacuna de medida que o [PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md) deixa,
aberta pela R1.3 ("sempre abra issue para lacunas deixadas") e pelo D7 do Desenho.

## O que se sabe

O subagente roda no processo da sessão (F4), e a CPU entra no `machine` do turno que lê o `proc_pid_rusage` depois dele. Custo e CPU podem cair em tarefas diferentes.
