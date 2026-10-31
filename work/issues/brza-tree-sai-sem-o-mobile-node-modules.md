---
status: done
scope:
  - workspace
  - brza-studio
opened: 2026-10-31
completed: 2026-10-31
priority: medium
tags:
  - tooling
---

# O brza tree diz "install: ok" e o worktree sai sem o mobile/node_modules

**Resolvida em 2026-10-31** pelo `f87357d` da `master`, em
[O brza tree instala também o mobile/](../worklogs/2026-10-31-o-brza-tree-instala-o-mobile.md): o `brza tree` instala a
raiz e o `mobile/`, e imprime `install:  ok (offline: raiz, mobile)`.

## O pedido

A sessão do workstream `studio` repassou, em 2026-10-31, o que registrou em "Para o tools-kit" de
[O P68 e o P37 do PLN-001, o mock compartilhado do lucide e a ortografia conferida](../worklogs/2026-10-31-pln-001-p68-mock-do-lucide-e-p37-ortografia.md).
O `brza tree pln-001-p68` imprimiu `install: ok (offline)`, mas o worktree saiu sem o `mobile/node_modules`. O vitest do
mobile deu `Cannot find package 'react-test-renderer'`, e o `implementer` rodou
`pnpm install --offline --frozen-lockfile` no `mobile/` antes dos testes. O mesmo valeu para o `pln-001-p67`, onde só a
raiz foi usada.

A rodada desta sessão, no mesmo dia, respondeu:
- "Para onde vai o conserto?" — "Issue, executada já (Recomendado)", e não um P11 no PLN-002 fechado.
- "Qual escopo o install do brza tree deve cobrir?" — "Raiz e mobile/ (Recomendado)".

## A causa

O `pnpm-workspace.yaml` do `brza-studio` deixa o `mobile/` de fora de propósito ("Exclude mobile's independent
workspace/lockfile"), e o `mobile/` tem `pnpm-lock.yaml` próprio. O `install_offline`
(`scripts/brza/brza_runtime.py:129`) roda num diretório só, e o `brza-tree` o chamava só na raiz.

Medido num worktree temporário de `origin/master`:
- `mobile/`: o install offline passou em 8 s;
- `cloud/`: o install offline falhou, por falta dos metadados no store, e o checkout da raiz também não tem
  `cloud/node_modules`. Por isso o `cloud/` ficou de fora.

## O conserto

O `brza-tree` ganhou a constante `OWN_LOCKFILE = ('mobile',)` e instala cada pacote dela que tenha `pnpm-lock.yaml`,
depois da raiz. A falha num deles imprime o `CHECK:` com o diretório em que se roda o `pnpm install --frozen-lockfile`,
e sai com 1, como a da raiz. O `brza test` e o `brza app` seguem só na raiz: o primeiro roda o vitest da raiz, e o
segundo faz o build do desktop.
