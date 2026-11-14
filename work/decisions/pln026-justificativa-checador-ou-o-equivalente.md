---
status: open
scope:
  - workspace
  - brza-workflow
description: Pede ao Bob qual comando valia como "o equivalente" do checador no P8, já que o `brza note` recusa a branch builder/.
opened: 2026-11-14
owner: Bob
trigger: A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders
deadline: 2026-11-14
tags:
  - planning
---

# O que é "o equivalente" do `brza note check` na branch do Bob?

Auditoria do Bauble · o Espião sobre o [PLN-026: brza sessions e meeting-runner funcionam na cloud](../../plans/PLN-026-sessoes-e-meeting-runner-na-cloud/PLN-026-plan.md), em 2026-11-14, autorizada pelo Anderson. As linhas citadas são do commit `d4289bc` da `builder/bob-the-builder`. Os horários são BRT. Quem responde é Bob. Quem decide é Anderson, por frase explícita. Nada aqui está decidido.

## A instrução

"Rode o checador de notas (`brza note check` ou o equivalente) e deixe 0 erros." — Bob, no brief do P8.

## Onde aparece

Brief do Bob ao agente `bc-ae6dd743` (P8), em 2026-11-14 entre 14h00 e 14h17. O plano registra que o `brza note` recusa `builder/*` (`PLN-026-plan.md:66`), e o PR A repete que o `brza note commit` recusa a branch ([O PR A do PLN-026 levou o degrau 1](../worklogs/2026-11-14-pln026-pr-a.md)).

## Por que não é determinística

"O equivalente" não nomeia comando, versão nem checkout. Há pelo menos duas cópias do checador (a da master do `brza-workflow` e a de cada branch de PR), e o resultado depende de qual se roda. Sem o comando, "0 erros" não é reproduzível.

## O que foi feito com ela

Os worklogs citam "o checador" sem caminho nem SHA na maioria das vezes. Nenhum fixa qual cópia vale para a branch do Bob.

## A pergunta de justificativa

Bob, qual comando e qual SHA do checador valem para a `builder/bob-the-builder`, e por que o brief não os fixou?

## Opções

- `python3 core/.claude/skills/notes-checker/scripts/check_notes.py --root <worktree>` da master do `brza-workflow`, com o SHA citado na evidência.
- O checador da branch do PR em revisão, quando o PR mexe nele.
- Esperar o `brza note builder` do PLN-024 e, até lá, a primeira opção.

## Gatilho

A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders. Vencido sem resposta, a nota pede decisão ao Anderson ou ganha um gatilho novo.
