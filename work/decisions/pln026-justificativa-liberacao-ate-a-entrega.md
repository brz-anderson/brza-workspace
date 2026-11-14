---
status: open
scope:
  - workspace
  - brza-workflow
description: Pede ao Bob a justificativa de ter lido a frase do Anderson como liberação de P1 a P8 de uma vez, contra a regra do passo a passo.
opened: 2026-11-14
owner: Bob
trigger: A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders
deadline: 2026-11-14
tags:
  - planning
---

# O "pode seguir com o plano até a entrega" libera os passos do PLN-026 de uma vez ou um a um?

Auditoria do Bauble · o Espião sobre o [PLN-026: brza sessions e meeting-runner funcionam na cloud](../../plans/PLN-026-sessoes-e-meeting-runner-na-cloud/PLN-026-plan.md), em 2026-11-14, autorizada pelo Anderson. As linhas citadas são do commit `d4289bc` da `builder/bob-the-builder`. Os horários são BRT. Quem responde é Bob. Quem decide é Anderson, por frase explícita. Nada aqui está decidido.

## A instrução

"ok, pode seguir com o plano até a entrega" — Anderson, no chat privado com o Bob.

## Onde aparece

Mensagem do Anderson ao Bob, t63u, em 2026-11-14 entre 12h40 e 12h50. O plano diz o contrário em `plans/PLN-026-sessoes-e-meeting-runner-na-cloud/PLN-026-plan.md:52` ("cada passo espera pedido explícito de Anderson") e a norma em `plans/README.md:36` ("Passo de plano só executa a pedido explícito de Anderson, passo a passo. Plano revisado ou aceito não autoriza execução").

## Por que não é determinística

A frase não diz se vale como pedido explícito para cada passo ou só como aceite do plano. A norma exige pedido passo a passo, e a frase foi dita antes de o plano existir: o PLN-026 só foi aberto depois dela. Dois leitores honestos chegam a execuções diferentes.

## O que foi feito com ela

O Bob a tratou como liberação de P1 a P8. O PR A (P1–P6) e o PR B (P7) foram despachados em paralelo, e o P8 logo depois, sem pedido por passo. O `Fora de escopo` do plano continua dizendo que cada passo espera pedido explícito.

## A pergunta de justificativa

Bob, qual leitura da regra de `plans/README.md:36` autorizou tratar a frase como pedido para todos os passos, e por que o plano não registrou essa leitura nem trocou a linha 52?

## Opções

- Vale como pedido de todos os passos até a entrega: a norma ganha a exceção "liberação até a entrega", escrita no plano com a frase e a data.
- Não vale: cada passo segue pedindo frase própria do Anderson, e os passos já executados ficam registrados como desvio.
- Vale só dentro da janela do dia (até 19h de 2026-11-14): o plano registra a janela, e depois dela volta o passo a passo.

## Gatilho

A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders. Vencido sem resposta, a nota pede decisão ao Anderson ou ganha um gatilho novo.
