---
status: open
scope:
  - workspace
  - brza-workflow
description: Pede ao Bob o critério de "entregável", porque o brief do P8 chama a reunião de real e de entregável e, no mesmo texto, de smoke que não conta.
opened: 2026-11-14
owner: Bob
trigger: A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders
deadline: 2026-11-14
tags:
  - planning
---

# Uma reunião SMOKE conta como o entregável das 19h do PLN-026?

Auditoria do Bauble · o Espião sobre o [PLN-026: brza sessions e meeting-runner funcionam na cloud](../../plans/PLN-026-sessoes-e-meeting-runner-na-cloud/PLN-026-plan.md), em 2026-11-14, autorizada pelo Anderson. As linhas citadas são do commit `d4289bc` da `builder/bob-the-builder`. Os horários são BRT. Quem responde é Bob. Quem decide é Anderson, por frase explícita. Nada aqui está decidido.

## A instrução

"se não tiver um entregavel até às 19h, pare e reporte o estado atual" — Anderson; e "fazer uma reunião real funcionar na cloud pelo meeting-runner, com ata. Este é o entregável do Anderson" — Bob, no brief do P8.

## Onde aparece

Mensagem do Anderson ao Bob, t63u, em 2026-11-14 entre 12h40 e 12h50, e o brief do P8 ao agente `bc-ae6dd743`, entre 14h00 e 14h17. A cobertura do plano pede "Uma reunião real pelo `meeting-runner` na cloud" (`PLN-026-plan.md:43`). As duas atas gravadas são marcadas SMOKE e "não contam para a promoção" (`PLN-026-plan.md:379`).

## Por que não é determinística

"Entregável" não tem critério: PR aberto, PR mergeado, reunião smoke ou reunião que conta. O mesmo brief chama a reunião de "real" e "entregável" e, quatro linhas abaixo, de smoke que "NÃO conta". O campo `ready` do plano diz que nenhuma caixa fecha antes do merge, e o merge depende do Anderson.

## O que foi feito com ela

O P8 rodou duas reuniões smoke, com ata, e o plano as registra como "implementado, aguardando merge". Não está escrito se isso satisfaz o entregável das 19h ou se o Bob deve parar e reportar o que faltou.

## A pergunta de justificativa

Bob, por qual critério a reunião smoke é o entregável das 19h, se ela não conta para a promoção e a cobertura do plano pede reunião real? E qual estado você vai reportar às 19h: entregue ou não entregue?

## Opções

- Entregável é a reunião smoke com ata e os PRs abertos com revisão aprovada; o merge fica com o Anderson.
- Entregável só com os PRs mergeados e uma reunião que conta para a promoção; às 19h o Bob reporta o que faltou.
- O Anderson fixa o critério na reunião de fechamento, e o plano o registra no `ready`.

## Gatilho

A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders. Vencido sem resposta, a nota pede decisão ao Anderson ou ganha um gatilho novo.
