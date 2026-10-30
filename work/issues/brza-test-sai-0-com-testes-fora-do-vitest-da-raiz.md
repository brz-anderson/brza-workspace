---
status: open
scope:
  - workspace
opened: 2026-10-29
priority: low
tags:
  - tooling
---

# O brza test sai 0 com os testes de mobile/ e cloud/, que o vitest da raiz não roda

## O pedido

O A5 da [REV: a entrega do PLN-002, do P0 ao P9](../reviews/pln-002-os-comandos-brza.md), mandado a issue na R15.1 do
[PLN-002: Os passos manuais que se repetem entre sessões viram comandos `brza`](../../plans/PLN-002-os-comandos-brza/PLN-002-plan.md):
"Issue, com as opções", de Anderson, em 2026-10-29.

O `scripts/brza/brza-test` escolhe o teste vizinho de qualquer pasta (`:71-83`), mas o vitest da raiz só inclui
`src/`, `config/scripts/`, `tests/tools/` e `tests/e2e/*.unit.test.ts`
(`brza-studio/config/scripts/ci-unit-files.mjs:7-13`). O teste de `mobile/` (1102 arquivos) ou de `cloud/` (261), com
`vitest.config.ts` próprio, cai em "não rodou" (`brza-test:228`), fora da saída (`:234`), e o comando sai 0. Com o
relatório vazio, o `if results else []` da `:228` esconde até o "não rodou".

## As opções, para a rodada

1. Sair 1 e listar como "fora do config" o que não rodou. Custo: 0,4 h e a troca do contrato do D4. Se paga: no
   primeiro `brza test` de uma mudança em `mobile/` ou `cloud/`.
2. Rodar cada arquivo pelo `vitest.config.ts` do pacote dele. Custo: ~1 h, e o preparo de cada pacote no worktree
   temporário do baseline. Se paga: quando `mobile/` ou `cloud/` virarem frente de trabalho.
3. Só avisar numa linha `CHECK:`, saindo 0. Custo: 0,2 h. Se paga: só se quem chama ler a saída.

**Gatilho:** a primeira sessão que mexer em `mobile/` ou `cloud/`.
