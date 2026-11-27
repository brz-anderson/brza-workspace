---
status: open
description: Depois de trocar de conta pelo seletor global, num chat com tarefa em segundo plano devendo acordar o lead, o auto-continue do upstream manda a continuação ao agente retido na conta esgotada.
scope:
  - brza-studio
opened: 2026-11-26
priority: medium
trigger: o sync em que o upstream corrigir, ou o caso doer no uso
tags:
  - chat
  - upstream
---

# O auto-continue entrega a continuação ao agente retido na conta esgotada

## O pedido

O P6 do [PLN-026: O Continuar em outra conta espera a tarefa em segundo plano e continua na conta
nova](../../plans/PLN-026-continuar-em-outra-conta-depois-da-tarefa/PLN-026-plan.md) (D6) provou a hipótese F14 do
desenho. Na R5.3, Anderson decidiu "Issue com teste e reportar (Recomendado)": o fork não corrige o upstream.

## O que se sabe

- **O cenário:** chat Claude que segue a seleção, turno cortado pelo limite de uso, tarefa em segundo plano terminada que
  ainda deve acordar o lead, conta trocada pelo **seletor global** (não pelo "Continue in another account"), auto-continue
  ligado.
- **O agente fica na conta esgotada de propósito** (#45478, `4639b50da92`): `structured-agent-session-outgrown-child.ts:140-144`
  no `releaseIdleChatsOnOtherAccount`, e `:175-179` no envio, pelo `owesWakeUp`.
- **A varredura do auto-continue atribui a conta pela seleção:** `recovery/structured-agent-session-usage-limit-account-hold.ts:95-99`
  (`launchAccountHome` → `movedTo` = B), e o `movedSince` antecipa o reset para o instante da troca (`:194-196`); a
  continuação fica pronta ~15 s depois (`:255`).
- **Nada olha o agente retido:** `recovery/structured-agent-session-usage-limit-disposition.ts:25-40`
  (`usageLimitCutContinuable`); a admissão só confere fences (`agent-session-journal/journal-sql-send-admission.ts:114-121`).
- **Resultado:** a continuação é entregue ao processo na conta A, que bate no limite de novo.
- **Provado no rig:** `src/main/native-chat/agent-session-wire/host/testing/structured-agent-session-usage-limit-account-switch.brza.test.ts:26`,
  `it.fails`, `brza-studio@c3289c12c9a` (branch `test/pln-026-p6-auto-continue`). Sem o `it.fails`:
  `expected { handed: 1, agent: 'kept on A' } to not deeply equal …`. Controles: sem a troca, nada sai antes do reset; sem o
  acordar devido, o agente é trocado e nada vai a A.

## Como reproduzir

- **No rig:** `node_modules/.bin/vitest run --config config/vitest.config.ts --maxWorkers=2 src/main/native-chat/agent-session-wire/host/testing/structured-agent-session-usage-limit-account-switch.brza.test.ts`
  → "1 expected fail"; trocar `it.fails` por `it` mostra a falha.
- **No app:** auto-continue ligado; chat que segue a seleção na conta A; pedir uma tarefa em segundo plano curta; esgotar A;
  deixar a tarefa terminar; trocar para B no seletor global; ~15 s depois a continuação automática vai ao processo em A.

## O que fazer

1. Reportar ao upstream, a pedido de Anderson, com o teste. O rascunho em inglês está abaixo.
2. Quando o upstream corrigir, virar o `it.fails` em `it` no sync.
3. Se o upstream não corrigir e o caso doer: barrar no `eligible` com um predicado do fork (~2 linhas em
   `structured-agent-session-usage-limit-continue.ts`, a opção 2 da R5.3 do PLN-026), ou o H2 do desenho.

### Rascunho do relato ao upstream

> **Usage-limit auto-continue sends to the agent kept on the exhausted account after a global account switch**
>
> After a Claude chat's turn ends on a usage limit while a background task still owes the lead a wake-up, switching
> accounts from the global picker deliberately keeps the agent on the old account (the retention guard from #45478,
> `structured-agent-session-outgrown-child.ts`, via `owesWakeUp`). The usage-limit sweep, however, attributes the chat's
> account from the current selection (`UsageLimitAccountHolds.attribute` → `launchAccountHome`), treats the switch as
> fresh room (`movedSince` pulls `resetsAt` to the switch time), and ~15 s later sends the automatic continue.
> `usageLimitCutContinuable` never looks at the kept agent, and on send the outgrown-child check keeps it again because
> of the owed wake-up — so the continue is handed to the process still on the exhausted account and hits the limit again.
>
> Repro (host rig, `createQueuedMessageTestRig`): Claude chat on account A, turn ends with `usageLimitReached` (reset 1 h
> out), a `done` child task settled after that turn, selection moved to B and `releaseIdleChatsOnOtherAccount` run (agent
> kept), auto-continue enabled, two sweep ticks at +30 s and +50 s. Result: one host continue submission handed over
> while `child.accountHome` is still A. Without the switch nothing is sent before the reset; without the owed wake-up the
> agent is replaced and nothing reaches A.
>
> Expected: the sweep either waits until the kept agent is released (its wake-up turn done) or continues on the newly
> selected account — never hands the continue to the agent on the exhausted account.
