---
status: open
description: As sessões do Codex e do Antigravity não passam pelo hook de medição, e as tarefas delas ficam sem tempo, custo e máquina no PLN-012.
scope:
  - brza-workflow
opened: 2026-11-03
priority: low
tags:
  - tooling
---

# Codex e Antigravity ficam sem medida por tarefa

## O pedido

O [PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md)
mede só as sessões do Claude Code, pelo `measure.py`. Na R1.3, Anderson escolheu deixar a lacuna à vista — a tarefa sem
turno medido aparece como "não medida" — e "sempre abra issue para lacunas deixadas". Esta é a lacuna do Codex e do
Antigravity.

## O que se sabe

- **Pesam pouco hoje.** No mapa do `brza sessions` (`.sessions/sessions.jsonl`), desde 2026-10-29: 1 abertura do
  Codex e 1 do Antigravity, contra 42 do Claude. A sessão aberta direto no app ou no terminal não entra no mapa.
- **Há worklog sem turno medido.** 3 dos 6 worklogs do `playground` de 2026-11-03 não têm turno medido, provavelmente
  de outro runtime (levantado pela sessão do `playground`).
- **Medir pede outro formato e outra tabela de preço**, lidos dos logs de cada runtime: custo estimado de 6 h ou mais
  na R1.3.

## O que falta

1. Saber onde o Codex e o `agy` gravam a sessão, os tokens e o modelo, e se há um id de sessão no ambiente, como o
   `CLAUDE_CODE_SESSION_ID`, para o `brza note commit` carimbar no worklog.
2. Decidir se vale medir, quando esses runtimes pesarem no gasto.
