---
status: open
description: O transcript não marca a pergunta de permissão, e a espera de Anderson para aprovar uma ferramenta cai no tempo do agente.
scope:
  - brza-workflow
opened: 2026-11-06
priority: low
tags:
  - tooling
---

# A espera de permissão de ferramenta conta como tempo do agente

## O pedido

Lacuna de medida que o [PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md) deixa,
aberta pela R1.3 ("sempre abra issue para lacunas deixadas") e pelo D7 do Desenho.

## O que se sabe

Os três tempos (D2) tiram do turno só a espera das rodadas (`AskUserQuestion`) e a do pedido interrompido. A espera de permissão fica dentro do `tool_use` da ferramenta, sem linha própria no transcript.
