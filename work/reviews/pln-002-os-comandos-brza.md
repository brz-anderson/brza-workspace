---
status: done
scope:
  - workspace
opened: 2026-10-29
completed: 2026-10-29
tags:
  - tooling
---

# REV: a entrega do PLN-002, do P0 ao P9

O parecer da entrega do
[PLN-002: Os passos manuais que se repetem entre sessões viram comandos `brza`](../../plans/PLN-002-os-comandos-brza/PLN-002-plan.md),
na versão `brza-workspace@0eaf986` e `brza-studio@9a81e65c852`, numa revisão só depois do P9 (R11.2). O revisor foi um
subagente da camada alta, chamado pela sessão `pln-002-sessions-rename`, que não executou os passos; os destinos saíram
da R14 e da R15, com Anderson.

## Veredito

A Cobertura está cumprida: as 16 linhas têm teste ou caso manual. Os 11 commits citados existem, estão na `origin/master`
e trazem o que os passos dizem; as contagens de teste somam 151; os X1, X2 e X4 a X11 fazem o que dizem; o contrato do
runtime só cresceu; o `close` não usa `--resume`; o `--json` do `list` bate com o D7. Seis achados, quatro deles
corrigidos no P10.

## Achados

### A1 — O `brza test` roda no checkout principal do `brza-studio` e reconstrói o que está nele

> desvio · importante · → corrigido aqui, no P10 (R14.1)

**Evidência:** o `worktree_root` de `scripts/brza/brza-test:50-59` só confere o `--git-common-dir`; o de
`scripts/brza/brza-dev:56-57` recusa o principal pelo `.git`, que lá é diretório. Por `runpy`, o
`worktree_root(~/Projects/brza-studio)` do `brza-test` devolveu `/Users/andepb/Projects/brza-studio`, e o do `brza-dev`
recusou. O `PRELUDE` (`brza-test:36-37,106-109`) reconstrói os módulos nativos em `node_modules`. Fere a restrição "O
checkout principal do `brza-studio` não é tocado".

### A2 — O `--force` do `brza tree --rm` apaga em silêncio o worktree sujo e a branch não mergeada

> lacuna · importante · → corrigido aqui, no P10, com o `--empty` (R14.2, que reabriu a R1.4)

**Evidência:** em `scripts/brza/brza-tree:144-152`, as razões só são impressas sem `--force`; com ele, roda o
`git worktree remove --force` e o `git branch -D` sem dizer o que descartou, e o órfão sai pelo `shutil.rmtree`
(`:127-131`). O `--force` é rotina, porque o worktree de prova recém-criado cai no "sem commit próprio": as evidências
do P2 e do P3 usaram `--rm … --force`.

### A3 — O `brza note commit` põe num stash o trabalho sujo das outras sessões a cada push, mesmo sem nada a puxar

> bug · sugestão · → corrigido aqui, no P10 (R14.3)

**Evidência:** `scripts/brza/brza-note:111` roda `git pull -q --rebase --autostash` sempre. Num repositório temporário,
com um commit local e arquivos sujos, sem nada novo na origin: `Created autostash: cbdda79 / Current branch master is up
to date. / Applied autostash.` Entre o stash e a volta dele, o arquivo de outra sessão volta ao `HEAD`.

### A4 — O `brza app install` interrompido no meio da troca apaga o build novo e deixa o `/Applications` sem app

> bug · sugestão · → corrigido aqui, no P10 (R14.4)

**Evidência:** `scripts/brza/brza-app:138` só dá valor ao `keep` quando o `install()` retorna; uma exceção depois do
`shutil.rmtree(APP)` — `OSError` no `rmtree` parcial, Ctrl-C no `ditto` (`:106-108`) — deixa o `keep=False`, e o
`finally` (`:143-150`) remove o worktree com o app construído. O `except runtime.BrzaError` (`:140`) não pega o
`OSError`.

### A5 — O `brza test` sai 0 com testes alterados que o vitest da raiz não roda

> lacuna · sugestão · → issue [O brza test sai 0 com os testes de mobile/ e cloud/, que o vitest da raiz não roda](../issues/brza-test-sai-0-com-testes-fora-do-vitest-da-raiz.md) (R15.1)

**Evidência:** a `select_tests` (`scripts/brza/brza-test:71-83`) escolhe o vizinho `*.test.ts` de qualquer pasta; o
`UNIT_INCLUDE` (`brza-studio/config/scripts/ci-unit-files.mjs:7-13`) só cobre `src/`, `config/scripts/`, `tests/tools/`
e `tests/e2e/*.unit.test.ts`. Contados: 1102 arquivos de teste em `mobile/` e 261 em `cloud/`, com `vitest.config.ts`
próprio. Eles caem em "não rodou" (`brza-test:228`), que não entra na saída (`:234`).

### A6 — O X3 ficou sem destino

> lacuna · sugestão · → corrigido aqui, no P10 (R15.2)

**Evidência:** o `Retomar` do plano dizia "O X3 tem fonte […], sem passo para ela"; a fonte está em
`work/worklogs/2026-10-29-pln-002-p7-o-brza-sessions.md:49-51`, e não havia issue. Depois do P9, o nome da sessão sem
`--rename` só está no mapa, e o `brza-note:76` lê só o `CLAUDE_SESSION_NAME`.

## O que rodou e o que deu

- `env -u TERM_PROGRAM python3 -m unittest discover -s scripts/brza/tests` → `Ran 151 tests … OK`.
- `python3 -m unittest discover -s .claude/hooks/tests` → `Ran 25 tests … OK`.
- `git show --stat` nos 11 commits do workspace e `git -C ~/Projects/brza-studio merge-base --is-ancestor 9a81e65c852
  origin/master` → existem, com o noreply do `brz-anderson`, e estão na `origin/master`.
- `git diff 9daa020^ 88d8a3a --stat -- .claude/hooks/` → vazio, como o X11 diz.
- `git diff 9e95a2c^ HEAD -- scripts/brza/brza_runtime.py` → só a docstring removida.
- `scripts/brza/brza-sessions list --json`, só leitura → 14 chats em 1,0 s, com `source` `map` e `transcript`.
- `git check-ignore -v .sessions/sessions.jsonl` → `.gitignore:5`.
