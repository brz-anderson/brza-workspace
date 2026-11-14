---
status: open
scope:
  - workspace
  - brza-workflow
description: Pede ao Bob e ao Linus que fixem uma regra só para o primeiro turno e para o status do session_id, hoje contraditórios no plano.
opened: 2026-11-14
owner: Bob e Linus
trigger: A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders
deadline: 2026-11-14
tags:
  - planning
---

# O primeiro turno do `open` leva `--resume <chatId>` ou não?

Auditoria do Bauble · o Espião sobre o [PLN-026: brza sessions e meeting-runner funcionam na cloud](../../plans/PLN-026-sessoes-e-meeting-runner-na-cloud/PLN-026-plan.md), em 2026-11-14, autorizada pelo Anderson. As linhas citadas são do commit `d4289bc` da `builder/bob-the-builder`. Os horários são BRT. Quem responde é Bob e Linus. Quem decide é Anderson, por frase explícita. Nada aqui está decidido.

## A instrução

"`CloudRuntime.open` é um `agent -p` por persona, com `--resume <chatId>`, sem `--force`." (Desenho) e "O primeiro turno não leva `--resume` nem chama `create-chat`. O id é o `session_id` do JSON desse turno." (D1).

## Onde aparece

`PLN-026-plan.md:114` e `:176` dizem que o `open` leva `--resume <chatId>`; `PLN-026-plan.md:228` diz que o primeiro turno não leva. Na sala, na reunião das 15h, o Linus chamou o `session_id` de "mecanismo" e o Bob, de "hipótese" (registro do Bauble).

## Por que não é determinística

O mesmo plano dá as duas regras, e o resumo da ADR, que é a regra de referência, está do lado errado. Um executor que leia só o Desenho põe `--resume` no primeiro turno, sem id para dar a ele. O status do `session_id` também não está fixado: "mecanismo" é decisão, "hipótese" pede prova.

## O que foi feito com ela

O código do PR #2 segue o D1 (primeiro turno sem `--resume`, teste `test_open_argv_is_agent_p_without_force`). A prova do `--resume` com o `session_id` está em [O P7 do PLN-026 abre e retoma o turno na cloud](../worklogs/2026-11-14-pln026-pr-b.md), seção da rodada 1. A linha 176 e a Rodada 1, item 5, não foram corrigidas.

## A pergunta de justificativa

Bob, por que a linha 176 do Desenho não foi corrigida junto com o D1? Linus, o `session_id` do JSON é o mecanismo da ADR ou uma hipótese que ainda pede o teste de contrato?

## Opções

- O Desenho e a Rodada 1 ganham emenda datada: primeiro turno sem `--resume`, id do `session_id`; e o `session_id` passa a mecanismo, com o teste de contrato como prova.
- O `session_id` fica hipótese até o teste de contrato rodar no CI, e o plano diz isso no Desenho.
- O `create-chat` volta como caminho principal se o teste de contrato falhar, e o `session_id` fica de reserva.

## Gatilho

A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders. Vencido sem resposta, a nota pede decisão ao Anderson ou ganha um gatilho novo.
