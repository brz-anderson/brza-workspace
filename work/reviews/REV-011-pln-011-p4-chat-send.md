---
status: done
scope:
  - brza-studio
opened: 2026-11-04
completed: 2026-11-04
tags:
  - chat
  - tooling
---

# REV-011: P4 do PLN-011, estados e fila do `chat send`

Revisão independente pelo Grok 4.7 do P4 do
[PLN-011: Os chats do BrzA Studio se coordenam pela CLI, aparecem na navegação e chegam aos plugins](../../plans/PLN-011-chats-pela-cli-e-plugins/PLN-011-plan.md),
contra P4/1, D4/D6, Cobertura e Regressão. Base `brza-studio@a7099022850`; entrega inicial `55225f8cb878`, cobertura
complementar `ed5bf0283e1`, correção dos achados `a243520d41f` e complemento R20 `0de38e7d082`.

## Veredito

Aprova. Os dois achados estão corrigidos e confirmados pelo revisor. A lacuna das releituras do histórico foi
resolvida pela R20, implementada e revisada. Nenhum achado novo com confiança >= 80 na revisão final.

### A1 — A linha humana do timeout divergia do D4

> desvio · sugestão · confiança 92 · → corrigido aqui

**Evidência:** em `src/cli/handlers/chat.ts:220-224` da entrega inicial, a linha humana não incluía sessão e texto no
comando de retry fixado pelo D4. Corrigido em `brza-studio@a243520d41f`, com `quoteStartupArg`. O Grok confirmou a
frase inteira em teste com apóstrofo, substituição de comando e crase, sem executar o comando gerado.

### A2 — O fallback sem `actionablePromptIds` não tinha teste

> lacuna · sugestão · confiança 86 · → corrigido aqui

**Evidência:** `src/cli/brza/chat-queue-hold.ts:13-22` da entrega inicial implementava o fallback nos itens
`approval`/`question`, mas os testes não o exercitavam. Corrigido em `brza-studio@a243520d41f`; o Grok confirmou que
esses itens pendentes vencem `working` quando o campo falta e que uma lista vazia continua autoritativa.

## Lacuna de contrato resolvida pela R20

O revisor apontou que uma falha de transporte nas releituras após o envio escapava como erro comum, sem recibo.
A R20 foi respondida pelo agy às cegas e acordada com a coordenadora; D4/D6 foram complementados (X5).

**Evidência final:** `observePendingChatSend`, em `src/cli/brza/chat-send-observation.ts:19-63`, fixa um único prazo de
30 s, passa o tempo restante como `timeoutMs` e mantém os polls somente diante de falhas comprovadas de transporte.
Não há novo `agentSession.send`. No teto, preserva `submitted/pending`, saída 3 e `operation`; o último erro ainda não
recuperado vai para `reason`. O Grok conferiu os timers dos transportes local e remoto, inclusive `timeoutMs: 0`.

No tail adicional de queued (`src/cli/handlers/chat.ts:232-266`), transporte indisponível mantém recibo, posição e
código de saída, acrescenta `queueMetadataUnavailable: true` e omite os campos não observados. Recibo retirado em
replay continua rejected/1. A leitura não se repete. `TypeError`, `invalid_runtime_response` e `RuntimeRpcFailureError`
são relançados; a classe de transporte foi conferida nas fontes do cliente pelo revisor.

## O que rodou e o que deu

- Complemento de cobertura: 1 falha e 43 passes antes da correção da pausa; depois, 60 testes do alvo e 62 de terminal.
- A1/A2: 3 falhas e 49 passes antes; 66 testes do alvo depois, refeitos pelo Grok.
- R20: 7 falhas e 48 passes antes; depois, 79 testes em cinco arquivos do alvo e 62 de regressão terminal.
- Worker: `pnpm verify:bundled-skill-guides`, `pnpm tc:cli`, lint, hooks e
  `pnpm check:changed --base=origin/master --maxWorkers=2 --force` → 22/22 passaram.
- Grok: `ORCA_BACKGROUND_LAUNCH=1 node config/scripts/run-vitest.mjs run --config config/vitest.config.ts src/cli/handlers/chat.test.ts src/cli/handlers/chat-send-observation.test.ts src/cli/brza/chat-send-outcome.test.ts src/cli/brza/chat-queue-hold.test.ts src/cli/brza/chat-cursor.test.ts --maxWorkers=2` → 79 passed; oxlint → 0 erros.
- Identidade dos commits: Anderson Pereira Brzezinski <brz.anderson.pereira@gmail.com>. Worktree limpo antes e depois;
  `cli-exit-code.ts` fora do diff. Suíte completa reservada ao merge da fase.
