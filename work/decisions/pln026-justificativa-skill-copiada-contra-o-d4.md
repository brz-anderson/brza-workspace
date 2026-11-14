---
status: open
scope:
  - workspace
  - brza-workflow
description: Pede ao Bob a justificativa da ordem do P8 que contrariou o D4 do plano sem rodada nem emenda.
opened: 2026-11-14
owner: Bob
trigger: A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders
deadline: 2026-11-14
tags:
  - planning
---

# Por que o brief do P8 mandou copiar a meeting-runner para a branch, se o D4 pedia worktree só de leitura?

Auditoria do Bauble · o Espião sobre o [PLN-026: brza sessions e meeting-runner funcionam na cloud](../../plans/PLN-026-sessoes-e-meeting-runner-na-cloud/PLN-026-plan.md), em 2026-11-14, autorizada pelo Anderson. As linhas citadas são do commit `d4289bc` da `builder/bob-the-builder`. Os horários são BRT. Quem responde é Bob. Quem decide é Anderson, por frase explícita. Nada aqui está decidido.

## A instrução

"Traga a skill `meeting-runner` de `origin/workstream/playground` para a branch `builder/bob-the-builder`, com `git checkout origin/workstream/playground -- .claude/skills/meeting-runner`." — Bob, no brief do P8.

## Onde aparece

Brief do Bob ao agente `bc-ae6dd743` (P8), em 2026-11-14 entre 14h00 e 14h17. O D4 diz "abre um worktree só de leitura de `origin/workstream/playground` em `03c9579d`" (`PLN-026-plan.md:264`). O desvio está em X6 de [O P8 do PLN-026 roda a reunião smoke na cloud](../worklogs/2026-11-14-pln026-p8.md).

## Por que não é determinística

Plano e brief dão duas ordens incompatíveis para o mesmo passo, e o brief não diz que substitui o D4. O agente que lê o plano, como o brief manda, não sabe qual seguir.

## O que foi feito com ela

O agente seguiu o brief: a skill e o `skillkit` entraram na branch (`61658f0`, `fd476c8`) e o desvio virou X6 e X7. A revisão xhigh `bc-b5fd74c7` aceitou X6 e X7 na branch do Bob, mas disse que o trecho do Desenho ficou velho.

## A pergunta de justificativa

Bob, por que o D4 não foi emendado nem levado à sala antes de o brief mandar o contrário? E o Desenho vai ser corrigido?

## Opções

- Emendar o D4 com data, dizendo que a skill mora na branch do Bob até a promoção.
- Voltar ao worktree só de leitura e apagar a cópia da branch.
- Manter a cópia e abrir rodada no plano para a promoção da skill ao `core/`.

## Gatilho

A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders. Vencido sem resposta, a nota pede decisão ao Anderson ou ganha um gatilho novo.
