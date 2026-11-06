---
status: open
description: O `run_in_background` e o servidor MCP stdio só somam à CPU dos filhos do `claude` quando terminam, e caem no turno em que saem, ou em nenhum.
scope:
  - brza-workflow
opened: 2026-11-06
priority: low
tags:
  - tooling
---

# O processo em segundo plano entra na CPU só quando sai

## O pedido

Lacuna de medida que o [PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md) deixa,
aberta pela R1.3 ("sempre abra issue para lacunas deixadas") e pelo D7 do Desenho.

## O que se sabe

O `proc_pid_rusage` conta os filhos já colhidos. Um processo vivo não conta, e um que vive a sessão inteira não entra em turno nenhum.
