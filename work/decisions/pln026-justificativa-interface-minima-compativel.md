---
status: open
scope:
  - workspace
  - brza-workflow
description: Pede ao Bob e ao Linus a justificativa do brief do P7, que pediu uma interface compatível sem assinatura e gerou dois cloud_runtime.
opened: 2026-11-14
owner: Bob e Linus
trigger: A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders
deadline: 2026-11-14
tags:
  - planning
---

# Que assinatura a "interface mínima compatível com a porta" do P7 devia ter?

Auditoria do Bauble · o Espião sobre o [PLN-026: brza sessions e meeting-runner funcionam na cloud](../../plans/PLN-026-sessoes-e-meeting-runner-na-cloud/PLN-026-plan.md), em 2026-11-14, autorizada pelo Anderson. As linhas citadas são do commit `d4289bc` da `builder/bob-the-builder`. Os horários são BRT. Quem responde é Bob e Linus. Quem decide é Anderson, por frase explícita. Nada aqui está decidido.

## A instrução

"Ponha o código do `open`/`send` num módulo isolado, com uma interface mínima compatível com a porta descrita acima, para facilitar o rebase quando o PR A entrar." e "`open(persona, model, workspace, mode)` faz o primeiro turno e devolve o `session_id`. `send(session, prompt)` faz `--resume`." — Bob, no brief do P7.

## Onde aparece

Brief do Bob ao agente `bc-584c3f02` (P7, PR B), em 2026-11-14 entre 13h26 e 13h40. O desvio X4 de [O P7 do PLN-026 abre e retoma o turno na cloud](../worklogs/2026-11-14-pln026-pr-b.md) registra que `open` e `send` devolvem `Turn`, e não a string do id.

## Por que não é determinística

"Compatível com a porta descrita acima" não aponta assinatura: a porta descrita no brief só lista nomes de capacidade. O mesmo brief dá uma assinatura (`open(persona, model, workspace, mode)` devolve o id) que não era a da porta do PR A. O módulo isolado não tinha caminho nem nome fixado.

## O que foi feito com ela

O PR #2 criou `packages/client/cloud_runtime.py` e o PR #3 criou `packages/client/bin/cloud_runtime.py`: duas portas. A sala fixou depois a assinatura canônica (`open(spec) -> Turn`, `send(session_id, prompt) -> Turn`, módulo do PR #3), e o rebase `e07fd47` tirou a cópia. O retrabalho foi a rodada 1 inteira da revisão xhigh.

## A pergunta de justificativa

Bob, por que o brief do P7 não fixou caminho e assinatura antes do despacho, se o PR A já estava definindo a porta? Linus, a assinatura canônica estava escrita em algum lugar acessível ao agente às 13h26?

## Opções

- Todo brief que cria interface paralela fixa caminho, nome e assinatura, copiados do contrato do arquiteto.
- Não se despacha o segundo PR antes de a porta do primeiro estar no origin.
- A emenda da ADR-003 vira o contrato de referência, citado por seção nos briefs.

## Gatilho

A resposta na reunião de fechamento do PLN-026, em 2026-11-14 às 19h30 (BRT), na sala BrzA Cloud Builders. Vencido sem resposta, a nota pede decisão ao Anderson ou ganha um gatilho novo.
