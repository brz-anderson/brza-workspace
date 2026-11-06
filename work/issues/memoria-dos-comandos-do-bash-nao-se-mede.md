---
status: open
description: O `proc_pid_rusage` do `claude` dá a CPU dos filhos que saíram, mas não o pico de memória deles; só o `brza run` mede a memória do comando.
scope:
  - brza-workflow
opened: 2026-11-06
priority: low
tags:
  - tooling
---

# A memória dos comandos rodados pelo Bash não se mede

## O pedido

Lacuna de medida que o [PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md) deixa,
aberta pela R1.3 ("sempre abra issue para lacunas deixadas") e pelo D7 do Desenho.

## O que se sabe

O teste ou o build rodado direto pelo `Bash` entra no `machine.cpu_children_s` do turno, sem o pico de memória. O `brza run` mede o pico pelo `getrusage(RUSAGE_CHILDREN)` (D5).
