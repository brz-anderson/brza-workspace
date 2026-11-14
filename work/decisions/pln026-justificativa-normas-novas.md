---
status: open
scope:
  - workspace
  - brza-workflow
description: Pede ao Bob a lista das "normas novas" que o brief do PR A mandou rodar junto com o checador, sem nomeá-las.
opened: 2026-11-14
owner: Bob
trigger: A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders
deadline: 2026-11-14
tags:
  - planning
---

# Quais são as "normas novas" que o PR A devia rodar nas notas reais?

Auditoria do Bauble · o Espião sobre o [PLN-026: brza sessions e meeting-runner funcionam na cloud](../../plans/PLN-026-sessoes-e-meeting-runner-na-cloud/PLN-026-plan.md), em 2026-11-14, autorizada pelo Anderson. As linhas citadas são do commit `d4289bc` da `builder/bob-the-builder`. Os horários são BRT. Quem responde é Bob. Quem decide é Anderson, por frase explícita. Nada aqui está decidido.

## A instrução

"Rode o checador e as normas novas nas notas reais do brza-studio, brza-workspace e demais consumidores (`/agent/repos`) e compare com a master." — Bob, no brief do PR A.

## Onde aparece

Brief do Bob ao agente `bc-7d3d9ffc` (PR A, P1–P6), em 2026-11-14 entre 13h05 e 13h14.

## Por que não é determinística

O brief não diz quais normas são "novas", nem onde estão. O PR A não muda o checador. Sem a lista, o agente não tem como saber o que comparar, e qualquer saída serve de prova.

## O que foi feito com ela

O worklog do PR A rodou só o checador da master e o da branch, "o mesmo arquivo", e comparou a saída JSON nas notas reais ([O PR A do PLN-026 levou o degrau 1](../worklogs/2026-11-14-pln026-pr-a.md)). Nenhuma "norma nova" foi nomeada nem rodada.

## A pergunta de justificativa

Bob, quais eram as normas novas, em que arquivo estavam, e por que o relatório do PR A foi aceito sem elas?

## Opções

- Eram as regras do PR #1 do `brza-workflow` (PLN-025); o PR A devia rodar o checador daquela branch.
- Não havia normas novas; a frase sai dos próximos briefs.
- Normas novas são as do PLN-026 (porta, `ausente`, chave só no filho), e o PR A precisa de um teste que as cubra.

## Gatilho

A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders. Vencido sem resposta, a nota pede decisão ao Anderson ou ganha um gatilho novo.
