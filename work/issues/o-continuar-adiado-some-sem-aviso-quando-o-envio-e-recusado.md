---
status: open
description: O Continuar adiado do PLN-026 encerra o pedido e tira a linha antes do envio; uma recusa do envio por outro motivo que não continuationSuperseded só vai ao log.
scope:
  - brza-studio
opened: 2026-11-27
priority: low
trigger: o primeiro caso real de pedido que some sem continuar, ou um cenário no rig que leve a essa recusa
tags:
  - chat
---

# O Continuar adiado some sem aviso quando o envio é recusado

## O pedido

A revisão do P5 do [PLN-026: O Continuar em outra conta espera a tarefa em segundo plano e continua na conta
nova](../../plans/PLN-026-continuar-em-outra-conta-depois-da-tarefa/PLN-026-plan.md) (achado B5, parecer de 2026-11-27)
mandou a issue: não há cenário conhecido no rig que leve à recusa.

## O que se sabe

- **O disparo encerra o pedido antes do envio:** o `end()` apaga a linha de espera e o status
  (`src/main/native-chat/agent-session-wire/brza/brza-deferred-usage-limit-continue.ts:177-187`, `:213-222`, em
  `brza-studio@92a028ccb58`).
- **A recusa só vai ao log:** `brza-continue-after-work-send.ts:46-52`. O `continuationSuperseded` está certo como fim calado
  (outra continuação já segue); qualquer outra recusa deixa o chat na conta esgotada sem aviso, que é o sintoma do pedido
  original do PLN-026.
- **A causa mais provável seria um fence velho.** O X13 cobriu o caso sem corte, não este.

## O que fazer

1. Achar um cenário que leve à recusa (fence velho, chat que fechou entre a decisão e o envio) e escrever o teste.
2. Se a recusa for real: em toda recusa que não seja `continuationSuperseded`, encerrar com `expired` e um motivo, como no
   fim do prazo, para a linha avisar.
