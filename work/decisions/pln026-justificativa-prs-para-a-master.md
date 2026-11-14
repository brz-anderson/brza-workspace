---
status: open
scope:
  - workspace
  - brza-workflow
description: Pede ao Bob a justificativa de ter previsto um PR da branch de notas para a master do workspace, lendo "PRs pra master" sem dizer os repositórios.
opened: 2026-11-14
owner: Bob
trigger: A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders
deadline: 2026-11-14
tags:
  - planning
---

# "O PR ou os PRs pra master" vale para quais repositórios?

Auditoria do Bauble · o Espião sobre o [PLN-026: brza sessions e meeting-runner funcionam na cloud](../../plans/PLN-026-sessoes-e-meeting-runner-na-cloud/PLN-026-plan.md), em 2026-11-14, autorizada pelo Anderson. As linhas citadas são do commit `d4289bc` da `builder/bob-the-builder`. Os horários são BRT. Quem responde é Bob. Quem decide é Anderson, por frase explícita. Nada aqui está decidido.

## A instrução

"siga até a entrega, que é o PR ou os PRs pra master" — Anderson, no chat privado com o Bob.

## Onde aparece

Mensagem do Anderson ao Bob, t63u, em 2026-11-14 entre 12h40 e 12h50. O brief do P8 do Bob ao agente `bc-ae6dd743`, entre 14h00 e 14h17, diz "O Bob abre o PR do workspace depois da revisão". A norma diz o contrário em `PLN-026-plan.md:66` ("A master deste repositório não recebe a nota") e no `work/README.md`, seção Commit (as notas não moram na `master`).

## Por que não é determinística

A frase não nomeia os repositórios. Com três repos na frente (`brza-workflow`, `brza-workspace`, `brza-studio`), "os PRs pra master" cabe tanto no código do `brza-workflow` quanto na branch de notas do workspace, que a norma proíbe na master.

## O que foi feito com ela

O brief do P8 previu o PR do workspace para a master. A revisão xhigh `bc-b5fd74c7` reprovou esse PR no achado 1, bloqueante: são 96 arquivos novos de nota e skill que a norma deixa fora da master. O PR não foi aberto.

## A pergunta de justificativa

Bob, qual norma autorizava o PR do `brza-workspace` para a master que o brief do P8 anunciou, e por que a frase não foi levada à sala para fixar os repositórios antes do despacho?

## Opções

- Só o `brza-workflow` recebe PR para a master; o workspace fica na `builder/bob-the-builder`.
- O workspace também recebe PR, só da parte que é skill (`.claude/`), depois da promoção que o `SKILL.md` exige.
- O Anderson nomeia, a cada entrega, os repositórios que recebem PR.

## Gatilho

A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders. Vencido sem resposta, a nota pede decisão ao Anderson ou ganha um gatilho novo.
