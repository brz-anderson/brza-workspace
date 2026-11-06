---
status: open
description: O `/clear` troca o `session_id` do hook, e não se sabe se o `CLAUDE_CODE_SESSION_ID` do Bash acompanha.
scope:
  - brza-workflow
opened: 2026-11-06
priority: low
tags:
  - tooling
---

# O /clear pode partir a tarefa em duas sessões

## O pedido

Lacuna de medida que o [PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md) deixa,
aberta pela R1.3 ("sempre abra issue para lacunas deixadas") e pelo D7 do Desenho.

## O que se sabe

Se os dois divergem, o carimbo do worklog aponta uma sessão e os turnos estão noutra, e a tarefa sai partida ou "não medida". O Desenho marcou o ponto como inferido, com confiança 40 (F20).
