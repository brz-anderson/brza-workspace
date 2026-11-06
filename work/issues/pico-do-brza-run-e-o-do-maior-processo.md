---
status: open
description: O `ru_maxrss` do `getrusage(RUSAGE_CHILDREN)` é o pico do maior processo, e oito workers de 400 MB aparecem como 400 MB.
scope:
  - brza-workflow
opened: 2026-11-06
priority: low
tags:
  - tooling
---

# O pico do brza run é o do maior processo, não o da árvore

## O pedido

Lacuna de medida que o [PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md) deixa,
aberta pela R1.3 ("sempre abra issue para lacunas deixadas") e pelo D7 do Desenho.

## O que se sabe

O `brza run` mede o pico pela rusage dos filhos (D5), que não soma processos simultâneos.
