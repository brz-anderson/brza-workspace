---
scope:
  - workspace
  - brza-studio
---

# O brza tree instala também o mobile/

O pedido veio da sessão do workstream `studio`, em 2026-10-31. Ela foi aberta por Anderson ("abra a sessão do
`tools-kit`") e registrou o caso em "Para o tools-kit" de
[O P68 e o P37 do PLN-001, o mock compartilhado do lucide e a ortografia conferida](2026-10-31-pln-001-p68-mock-do-lucide-e-p37-ortografia.md).
O `brza tree pln-001-p68` imprimiu `install: ok (offline)`, e o worktree saiu sem o `mobile/node_modules`. O diagnóstico
e o conserto estão em
[O brza tree diz "install: ok" e o worktree sai sem o mobile/node_modules](../issues/brza-tree-sai-sem-o-mobile-node-modules.md).

## O que se leu antes

- **Bloqueios em vigor:** nenhum, em nenhum workstream.
- **O PLN-002:** fechado em 2026-10-29. O `Retomar` diz "fechado", e a pendência dele é a issue do A5.
- **As issues abertas do `tools-kit`:** nenhuma trata deste caso. A do A5,
  [O brza test sai 0 com os testes de mobile/ e cloud/, que o vitest da raiz não roda](../issues/brza-test-sai-0-com-testes-fora-do-vitest-da-raiz.md),
  tinha como gatilho "a primeira sessão que mexer em `mobile/` ou `cloud/`", e o P68 é essa sessão.

## O que Anderson respondeu

- **Para onde vai o conserto:** "Issue, executada já (Recomendado)", e não um P11 no PLN-002 fechado.
- **O escopo do install:** "Raiz e mobile/ (Recomendado)". As outras opções eram todo lockfile próprio, com o `cloud/`,
  e uma flag `--mobile`.
- **A issue do A5:** "Registrar o gatilho (Recomendado)". A rodada das opções dela fica para depois.

## O que se fez

- **A medição, antes da rodada,** num worktree detached de `origin/master` fora do `brza-studio`, removido em seguida:
  - `mobile/`: o install offline passou em 8 s;
  - `cloud/`: o install offline falhou, por falta dos metadados no store.
- **`f87357d` na `master`:** `fix(brza): o brza tree instala também o mobile/, que tem lockfile próprio`.
  - O `brza-tree` ganhou o `OWN_LOCKFILE = ('mobile',)` e instala depois da raiz cada pacote dele que tenha
    `pnpm-lock.yaml`.
  - A linha passa a ser `install:  ok (offline: raiz, mobile)`, e a falha num pacote nomeia o diretório onde rodar o
    `pnpm install --frozen-lockfile`.
  - O `test_brza_tree.py` ganhou 3 casos. O `python3 -m unittest discover -s scripts/brza/tests` deu
    `Ran 232 tests … OK`.
- **A conferência de ponta a ponta:**
  - O `scripts/brza/brza-tree conferencia-mobile-nm --type chore` no `brza-studio` real imprimiu
    `install:  ok (offline: raiz, mobile)`, com o `mobile/node_modules/react-test-renderer` presente.
  - O `--rm conferencia-mobile-nm --empty` removeu o worktree e a branch.
- **O `brza note sync`** levou a `master` ao `studio`, ao `tools-kit` e ao `workspace`.
- **As issues:** uma nova, já `done`, e a linha do gatilho na issue do A5.

## O que ficou aberto

A rodada da issue do A5: o `brza test` ainda sai 0 com o teste do `mobile/`. Isso está na própria issue.
