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
- **O [PLN-018](../../plans/PLN-018-o-grok-e-o-codex-na-medicao/PLN-018-plan.md) leva a linha do Codex.** O formato está
  no Desenho. A instalação do hook muda o hash de confiança e espera decisão lá. Esta issue não abre outro plano para
  o Codex.
- **A sonda do Antigravity, em 2026-11-09.** Na CLI, 135 de 143 `transcript.jsonl` têm `input_tokens`,
  `output_tokens` e `cache_read_tokens`, e a linha não tem `model` nem custo. No chat ACP, 0 de 17 `transcript.jsonl`
  têm token, model ou custo. `acp_token.json` é credencial. O IDE não tem transcrição. O escritor não entrou no
  PLN-018.

## O que falta

1. O escritor do Antigravity. A CLI tem token e não tem custo nem model no turno; o chat ACP não tem os três na
   transcrição. A rodada que o traria não foi feita.
2. O Codex, no que o PLN-018 ainda não entrega: a instalação do hook.
