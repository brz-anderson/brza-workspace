---
scope:
  - brza-studio
tags:
  - chat
refs:
  - PLN-001
---

# O P79 do PLN-001, o Continuar em outra conta de volta e o Retomar automaticamente por padrão

O pedido 41, de Anderson: "o botão `Transferir para outro agente` do `upstream` só transfere entre `runtimes`, retorne o
botão que criamos, ao lado do `Retomar automaticamente` e deixe o `Retomar automaticamente` marcado por padrão". A
sessão `pln-001-pedido-41` executou o P79 pelo D62, no worktree `~/Projects/brza-studio/.worktrees/pln-001-pedido-41`,
branch `feat/pln-001-pedido-41`. O passo reabre o P40 e a R1 do worklog do sync da v1.4.246 ("Fica o do upstream").

## A leitura do D62

A leitura de `brza-studio@9a8631369ac` se sustentou no código. Os quatro pontos "A conferir no passo":

- **Onde o agendamento roda:** o `useNativeChatUsageLimitAutoResume` roda no `NativeChatStructuredSession`
  (`NativeChatInterruptedContinue.tsx:91`), só com o chat aberto. O host não tem um evento de "bateu o limite": o corte
  sai do journal a cada leitura (`latestNativeChatUsageLimitCut`). Daria para ligá-lo no `onJournalActivity` das
  mensagens na fila, por ~4 h.
- **O Cancelar:** o `cancel` só apaga a entrada do arquivo da agenda, e o `list` não diz que um corte foi cancelado. Uma
  linha remontada agendaria de novo.
- **Dois menus de conta:** a linha do upstream (`NativeChatUsageLimitActions`) já mostra embaixo o seletor (o global, ou o
  `BrzaPinnedAccountSwitch` no chat fixado). Na v1.4.242, o P40 não tinha esse seletor ao lado.
- **O que o botão de 2026-10-28 usava:** o `NativeChatAccountSwitchView` do `useNativeChatAccountSwitch`, que segue igual,
  e o `continueUsageLimit`. O `switchTo` é a troca por chat (`agentSession.switchAccount`). Para o chat sem pino, a troca
  global é a do `ClaudeSwitcherForOwner`: o `agentSession.options` e depois o `selectClaudeProviderAccount`.

Os dois primeiros mudavam o custo ou o comportamento, e foram a Anderson na R68.

## A rodada

- **R68.1:** "No app, marca no host". O agendamento sai do app, só com o chat aberto, e o host guarda o corte cancelado.
- **R68.2:** "Esconder o do upstream". O seletor da linha some quando o botão aparece, e o Hand Off fica.

## O que mudou

`brza-studio@4bbaecabf18`, na `master`:

- **O botão volta:** `brza/BrzaContinueInOtherAccount.tsx`, do `15b028ba23f`, ao lado do "Retomar automaticamente" na
  `NativeChatNoticeRow`. A troca vem do novo `brza/use-brza-continue-in-other-account.ts`: a do chat no fixado, a global
  no sem pino. Depois da troca, o botão cancela a retomada agendada e envia o Continue. O `NativeChatUsageLimitActions`
  esconde o seletor quando o botão aparece, e o `BrzaPinnedAccountSwitch.tsx` saiu.
- **O Retomar por padrão:** o hook pede ao host o agendamento com `automatic: true`, uma vez por corte, quando o `list`
  não traz nada. O host grava, um por chat e no máximo 500, o corte cancelado ou já enviado (`declined`, no mesmo
  arquivo da agenda), e recusa o automático dele. O clique no botão ainda agenda.
- **Compatibilidade:** a capability `agent-session.usage-limit-auto-resume-automatic.v1`. Com host antigo, fica só o
  botão. Um host antigo lê só o `entries` do arquivo. O mobile não tem o Retomar, e segue sem ele.
- **Textos:** a chave `continueInOtherAccount.continue` nos sete catálogos que têm o `usageLimitAutoResume`.

## Desvios

- **X81 — O Retomar por padrão pediu protocolo novo no host.** O D62 previa a mudança só no renderer. O Cancelar que
  dura depois de remontar a linha não cabe sem o host (R68.1): entraram o `automatic` no agendamento, a marca
  `declined` no arquivo e uma capability.
- **X82 — O seletor do chat fixado saiu junto com o do upstream.** Pela R68.2, o seletor da linha some. O
  `BrzaPinnedAccountSwitch` (a R4 do sync, "Seletor do chat") ocupava o mesmo lugar, e o botão já usa a troca por chat no
  chat fixado. O teste dele virou o da linha nova.
- **X83 — O `check:changed` ficou vermelho nos unit tests, por dois pontos preexistentes.** O `src/main/runtime/rpc/methods/usage-credentials.test.ts` falha sozinho (8 de 13): ainda espera as chaves em `~/.orca`, que o P75 (`f7490afab9e`) levou a `~/.brza` sem atualizá-lo. Os dois `tests/e2e/cross-version-wire/*.unit.test.ts` não acham arquivos na cópia em cache da v1.4.246 deste worktree (`tests/e2e/.cross-version-checkouts/`). O P79 não toca nenhum dos dois.

## O que rodou

- Antes do código, falharam 10 testes novos: 4 do host, 1 do hook, 2 do botão e 3 da linha.
- Depois, `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts --maxWorkers=2`, por caminho: o teste
  do host deu 13 passed; os 8 do renderer deram 85 passed (o hook, o botão, a linha nova,
  `NativeChatUsageLimitActions.test.tsx`, `.scaling.test.tsx`, `NativeChatNoticeRow.test.tsx`, `.auto-resume.test.tsx` e
  `NativeChatInterruptedContinue.test.tsx`). Repetidos depois do rebase.
- `pnpm tc:web` e `pnpm tc:node`: sem erro. `pnpm check:code-quality:changed origin/master`: passou, depois de tirar duas
  asserções `as` dos `vi.hoisted`.
- `pnpm check:changed --base=origin/master --maxWorkers=2`: 29 de 30; o vermelho é o de unit tests (1344 s), em dois pontos preexistentes, fora do que o P79 toca (X83). Depois do rebase sobre a `d501bb230ff`, os 9 arquivos por caminho → 98 passed, e o `tc:web` sem erro.
- Suíte inteira: roda depois do push, pela coordenação.

## O que ficou aberto

- **O C32**, de Anderson, num build novo: o build instalado não tem este commit.

## Fora do workspace

- O `brza-studio` ganhou o commit `4bbaecabf18` na `master`, com push direto para `brz-anderson/brza-studio`.
- O worktree `~/Projects/brza-studio/.worktrees/pln-001-pedido-41` e a branch `feat/pln-001-pedido-41` ficaram.
