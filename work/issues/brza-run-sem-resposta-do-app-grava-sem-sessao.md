---
status: open
description: Quando o app não responde, o `provider_session(chat)` falha, e a linha `run` sai sem sessão e cai em "sem tarefa".
scope:
  - brza-workflow
opened: 2026-11-06
priority: low
tags:
  - tooling
---

# O ▶ do brza run sem resposta do app grava o comando sem sessão

## O pedido

Lacuna de medida que o [PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md) deixa,
aberta pela R1.3 ("sempre abra issue para lacunas deixadas") e pelo D7 do Desenho.

## O que se sabe

O ▶ (`brza run --chat`) não roda no ambiente da sessão, e acha o id dela pelo app (D5).
