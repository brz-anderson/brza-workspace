---
status: open
description: Sem a função `claude` do shell nem o `claude-brza`, o hook de medição não roda, e a tarefa dessa sessão aparece "não medida" no `--by-task`.
scope:
  - brza-workflow
opened: 2026-11-06
priority: low
tags:
  - tooling
---

# A sessão aberta sem a função do shell fica sem medida por tarefa

## O pedido

Lacuna de medida que o [PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md) deixa,
aberta pela R1.3 ("sempre abra issue para lacunas deixadas") e pelo D7 do Desenho.

## O que se sabe

A sessão aberta numa IDE, ou no app com o `agentCmdOverrides.claude` vazio, não carrega o `settings.json` do workspace, e o `measure.py` não grava turno. O `brza note commit` ainda grava o evento `task`, e a tarefa entra na tabela de não medidas.
