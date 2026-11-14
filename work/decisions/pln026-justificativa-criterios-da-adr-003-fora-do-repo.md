---
status: open
scope:
  - workspace
  - brza-workflow
description: Pede ao Linus o texto canônico dos critérios de aceite da ADR-003, que o plano manda seguir e que não está no repositório.
opened: 2026-11-14
owner: Linus
trigger: A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders
deadline: 2026-11-14
tags:
  - planning
---

# Onde o executor lê "os critérios de aceite que estão no fim" da ADR-003, se ela não tem arquivo?

Auditoria do Bauble · o Espião sobre o [PLN-026: brza sessions e meeting-runner funcionam na cloud](../../plans/PLN-026-sessoes-e-meeting-runner-na-cloud/PLN-026-plan.md), em 2026-11-14, autorizada pelo Anderson. As linhas citadas são do commit `d4289bc` da `builder/bob-the-builder`. Os horários são BRT. Quem responde é Linus. Quem decide é Anderson, por frase explícita. Nada aqui está decidido.

## A instrução

"Os passos do PLN-026 devem seguir essa ADR e os critérios de aceite que estão no fim dela." — repassada pelo Bob, citada no plano.

## Onde aparece

`PLN-026-plan.md:33` cita a frase. `PLN-026-plan.md:55` tira a ADR do repositório ("Artefato de arquiteto não entra em PR nem no repo"), e o Desenho guarda só um resumo (`PLN-026-plan.md:171-176`). A cobertura usa "ADR, aceite 2" a "ADR, aceite 5" (`PLN-026-plan.md:44-47`), sem o aceite 1.

## Por que não é determinística

O plano manda seguir um texto que o executor não pode ler. O resumo do Desenho não traz os critérios de aceite, e a cobertura começa no aceite 2. Duas sessões que leiam o plano não têm como chegar ao mesmo conjunto de critérios.

## O que foi feito com ela

Os PRs seguiram o resumo do Desenho e as mensagens repassadas pelo Bob. A emenda da ADR-003 foi combinada na sala para entrar por extenso na ata da reunião, mas ainda não está gravada.

## A pergunta de justificativa

Linus, quais são os critérios de aceite da ADR-003, por extenso, incluindo o aceite 1? Onde um executor sem acesso à sua memória os lê?

## Opções

- Os critérios entram por extenso no plano, na seção de cobertura, sem o arquivo da ADR.
- Os critérios entram na ata da reunião de fechamento, e o plano aponta para ela.
- A ADR volta ao repositório numa pasta própria, revertendo a R3.1, por decisão do Anderson.

## Gatilho

A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders. Vencido sem resposta, a nota pede decisão ao Anderson ou ganha um gatilho novo.
