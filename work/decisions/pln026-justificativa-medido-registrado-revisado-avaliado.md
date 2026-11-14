---
status: open
scope:
  - workspace
  - brza-workflow
description: Pede ao Bob a métrica que ele adotou para "tudo deve ser devidamente medido, registrado, revisado e avaliado", que saiu sem critério.
opened: 2026-11-14
owner: Bob
trigger: A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders
deadline: 2026-11-14
tags:
  - planning
---

# O que conta como "medido, registrado, revisado e avaliado" no PLN-026?

Auditoria do Bauble · o Espião sobre o [PLN-026: brza sessions e meeting-runner funcionam na cloud](../../plans/PLN-026-sessoes-e-meeting-runner-na-cloud/PLN-026-plan.md), em 2026-11-14, autorizada pelo Anderson. As linhas citadas são do commit `d4289bc` da `builder/bob-the-builder`. Os horários são BRT. Quem responde é Bob. Quem decide é Anderson, por frase explícita. Nada aqui está decidido.

## A instrução

"tudo deve ser devidamente medido, registrado, revisado e avaliado" — Anderson, no chat privado com o Bob.

## Onde aparece

Mensagem do Anderson ao Bob, t63u, em 2026-11-14 entre 12h40 e 12h50. No plano, `executed_h` ficou 0 até a revisão xhigh (X5 em [O P7 do PLN-026 abre e retoma o turno na cloud](../worklogs/2026-11-14-pln026-pr-b.md)) e hoje é 1,7 pelo relógio entre dois commits (`PLN-026-plan.md:8` e `:23`). Os passos seguem com `Executado: — h`, contra `plans/README.md:23`.

## Por que não é determinística

Os quatro verbos não dizem o quê, com que métrica nem por quem. "Medido" pode ser horas, tokens, custo ou mutação. "Revisado" pode ser uma revisão xhigh no relatório do agente ou uma nota REV no repo. "Avaliado" não tem dono nem escala.

## O que foi feito com ela

Até a rodada 1 da revisão xhigh, não havia horas apontadas (X5) e as revisões ficavam só nos relatórios dos agentes. Depois, `executed_h` passou a ser o relógio entre `52184ee` e `e07fd47`, e duas revisões viraram nota em `work/reviews/`. Os custos ficaram `ausente`.

## A pergunta de justificativa

Bob, que métrica você adotou para cada um dos quatro verbos, onde ela está escrita, e por que as primeiras revisões não viraram nota REV na hora?

## Opções

- Medido é horas por passo e tokens por turno; registrado é worklog; revisado é nota REV por revisão; avaliado é o parecer da reunião de fechamento.
- Usar a medição do PLN-025 (`--by-execution`) como única fonte, com `ausente` onde não houver número.
- Deixar a métrica para o Anderson fixar, e registrar até lá que o PLN-026 não tem métrica de aceite para esses verbos.

## Gatilho

A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders. Vencido sem resposta, a nota pede decisão ao Anderson ou ganha um gatilho novo.
