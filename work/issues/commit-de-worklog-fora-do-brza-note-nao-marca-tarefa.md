---
status: open
description: O `git commit` direto e a migração não gravam o evento `task`, e os turnos ficam para o marco seguinte da sessão.
scope:
  - brza-workflow
opened: 2026-11-06
priority: low
tags:
  - tooling
---

# O commit de worklog fora do brza note commit não marca tarefa

## O pedido

Lacuna de medida que o [PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md) deixa,
aberta pela R1.3 ("sempre abra issue para lacunas deixadas") e pelo D7 do Desenho.

## O que se sabe

O marco da tarefa (D1) só nasce no `brza note commit`. O commit por outro caminho não carimba `sessions:` nem grava o evento.
