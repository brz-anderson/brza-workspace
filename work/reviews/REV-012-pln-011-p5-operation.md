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

# REV-012: P5 do PLN-011, replay com `--operation`

Revisão independente pelo Grok 4.7 do P5 do
[PLN-011: Os chats do BrzA Studio se coordenam pela CLI, aparecem na navegação e chegam aos plugins](../../plans/PLN-011-chats-pela-cli-e-plugins/PLN-011-plan.md),
commit `brza-studio@7ee6b1e5cc6f08301c58c144ba2f6426af565743`, sobre `0de38e7d082`, contra P5/1, D5/D6 e regressões.

## Veredito

Aprova. Nenhum achado com confiança >= 80. O host permanece a autoridade do ledger; o cliente valida o ID sem
normalização antes de consultar o host e preserva a mutação compartilhada, o fingerprint e os códigos do D4.

## Evidência

- `src/cli/handlers/chat.ts:168-172`: validação anterior a `getCliStatus` e RPC. ID ausente usa o gerador existente;
  vazio, sem valor ou malformado é recusado sem acesso ao host.
- `src/cli/brza/chat-operation-id.ts:3-12`: regex do gerador e casamento integral recusam inclusive newline final.
- `src/cli/handlers/chat-operation.test.ts:98-132`: mesmo ID e fingerprint com fence diferente, mesmo delivery e
  trimEnd, preservando espaços iniciais, nos hosts com e sem fila.
- `chat-operation.test.ts:135-220`: estados gravados do replay; uma mutação por invocação; recusa operationIdReused
  ao mudar texto/delivery; unknown/3 persistente nas duas invocações. Ledger, idade e deduplicação continuam no host.
- Spec, guia, referência e bundle documentam formato, replay, expiração e limite quando muda queued-messages.v2.

## O que rodou e o que deu

- Worker: antes, 12 testes do handler falharam e a suíte de parse não carregou sem o módulo; depois, 103 testes
  passaram em sete arquivos, incluindo P3/P4/R20. Os testes novos estão em arquivo vizinho para respeitar o limite de linhas.
- Worker: guias gerados e verificados, tc:cli, lint/formato e hooks aprovados;
  `pnpm check:changed --base=origin/master --maxWorkers=2 --force` → 22/22, 44,8 s.
- Grok refez `ORCA_BACKGROUND_LAUNCH=1 node config/scripts/run-vitest.mjs run --config config/vitest.config.ts src/cli/handlers/chat.test.ts src/cli/handlers/chat-send-observation.test.ts src/cli/handlers/chat-operation.test.ts src/cli/brza/chat-operation-id.test.ts src/cli/brza/chat-send-outcome.test.ts src/cli/brza/chat-queue-hold.test.ts src/cli/brza/chat-cursor.test.ts --maxWorkers=2` → 103 passed.
- Identidade: Anderson Pereira Brzezinski <brz.anderson.pereira@gmail.com>. Árvore limpa antes e depois da revisão;
  oito arquivos, +285/−3; sem push de código. Suíte completa reservada ao merge da fase.
