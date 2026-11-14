---
status: open
scope:
  - workspace
  - brza-workflow
description: Pede ao Bob o critério de "siga o código seguro e registre o desvio", que deixou ao agente a escolha entre plano e código.
opened: 2026-11-14
owner: Bob
trigger: A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders
deadline: 2026-11-14
tags:
  - planning
---

# O que é "o código seguro" quando o plano conflita com o código?

Auditoria do Bauble · o Espião sobre o [PLN-026: brza sessions e meeting-runner funcionam na cloud](../../plans/PLN-026-sessoes-e-meeting-runner-na-cloud/PLN-026-plan.md), em 2026-11-14, autorizada pelo Anderson. As linhas citadas são do commit `d4289bc` da `builder/bob-the-builder`. Os horários são BRT. Quem responde é Bob. Quem decide é Anderson, por frase explícita. Nada aqui está decidido.

## A instrução

"Se algo no plano conflitar com o código, siga o código seguro e registre o desvio." — Bob, no brief do PR A.

## Onde aparece

Brief do Bob ao agente `bc-7d3d9ffc` (PR A, P1–P6), em 2026-11-14 entre 13h05 e 13h14.

## Por que não é determinística

"Código seguro" não tem definição: pode ser o código que já existe, o que não quebra o Studio, o que não vaza a chave, ou o mais conservador. A frase também troca a fonte da verdade, do plano para o julgamento do agente, sem dizer quem revisa a troca.

## O que foi feito com ela

O PR A registrou desvios em [O PR A do PLN-026 levou o degrau 1](../worklogs/2026-11-14-pln026-pr-a.md), entre eles seguir o `117cb8d` e não o `52184ee` no `read`. Nenhum desvio diz qual sentido de "seguro" foi usado.

## A pergunta de justificativa

Bob, qual era o critério de "código seguro" que o agente devia aplicar, e quem aprova o desvio antes de ele virar código no PR?

## Opções

- Seguro é o que mantém o comportamento do Studio e não expõe a chave; qualquer outro conflito para o passo e vai à sala.
- Em conflito, o plano vence sempre; o agente para e pergunta.
- O agente escolhe e registra, e a revisão xhigh aprova ou reverte o desvio.

## Gatilho

A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders. Vencido sem resposta, a nota pede decisão ao Anderson ou ganha um gatilho novo.
