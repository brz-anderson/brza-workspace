---
scope:
  - workspace
---

# O PLN-002/P4: o brza test

O pedido de Anderson, em 2026-10-28, na sessão `pln-002-p4`: "Execute o P4 do
plans/PLN-002-os-comandos-brza/PLN-002-plan.md pela plan-runner. O P3 ao P6 correm em paralelo, em sessões separadas, no
mesmo checkout do brza-workspace: mexa só nos arquivos do seu passo". O passo executa o D4 do
[PLN-002: Os passos manuais que se repetem entre sessões viram comandos `brza`](../../plans/PLN-002-os-comandos-brza/PLN-002-plan.md).

## O que se fez

**O `scripts/brza/brza-test`** tem a forma do D4, sobre o `git`, o `worktree_add`, o `install_offline` e o
`worktree_remove` do runtime, sem mudar o runtime:
- acha a raiz do worktree pelo argumento ou pelo diretório atual e recusa, com saída 2, o que não tem o `.git` comum do
  `brza-studio`;
- faz o `git fetch origin`, que vira uma linha `CHECK` quando falha;
- escolhe os testes pelo D4: o alterado contra o merge-base com a `origin/master`, commitado ou não, e o não rastreado,
  sem os apagados. O `-- <caminhos>` troca essa lista;
- roda o vitest como o `pnpm test` (X5) e lê o relatório JSON dele;
- com falha, cria um worktree temporário detached da `origin/master` fora do `brza-studio`, instala offline e roda só
  os arquivos que falharam e existem lá. Remove o worktree num `finally`, com `--force` se os testes o sujaram;
- roda o `pnpm check:changed --base=origin/master --maxWorkers=2` e imprime o relatório.

**As escolhas que o D4 não fixava:**
- **O teste vizinho** é o `*.test.ts`, `*.test.tsx` ou `*.test.mjs` de mesmo nome, as extensões do `UNIT_INCLUDE`
  (`config/scripts/ci-unit-files.mjs:7-14`). Arquivo que não é código (`.md`, `.json`) não entra nem como "sem teste".
- **A comparação com a master é teste a teste**, e não arquivo a arquivo (X6). O arquivo que não carrega conta como uma
  falha "(o arquivo)", e o que não existe na master é falha nova sem ir ao baseline.
- **O baseline que falha**, no install ou no vitest, põe as falhas no grupo "falha, sem baseline", que sai com 1, como
  o `--no-baseline`.

**Os testes:** o `tests/test_brza_test.py` é novo, com 14 casos. Rodam num clone de uma `origin` local em que a master
anda depois da branch. O vitest e o install são trocados por falsos, e um `pnpm` falso no PATH grava os argumentos do
`check:changed`. Os testes de hoje mais o novo
(`python3 -m unittest test_brza_runtime test_brza_scripts test_brza_sessions test_brza_tree test_brza_test`, em
`scripts/brza/tests`) → `Ran 61 tests … OK`; eram 47. O `discover` inteiro tinha, na hora, uma falha no
`test_brza_note.py` do P6, então em curso na outra sessão.

**A corrida real**, num worktree do `brza tree pln-002-p4-prova`, com um comentário no
`config/scripts/vitest-changed-precheck.mjs`:
- **Verde no vitest:** 1 arquivo em 1,6 s, no grupo "passou". O `check:changed` levou 20,3 s e saiu vermelho só pelo
  import boundaries do `src/cli/external-subcommand.ts`, a pendência conhecida do plano. Total: 24,7 s.
- **Com um caso que falha no `.test.mjs`:** "falha nova: … › prova do brza test falha só na branch". O baseline levou
  36,0 s (worktree, install offline, build dos pacotes e vitest), o `check:changed` levou 18,5 s, e o total foi 58,4 s.
  Depois, o `git worktree list` não tinha nenhum `brza-test-`, e o `$TMPDIR` também não.
- `brza-tree --rm pln-002-p4-prova --force` removeu o worktree e a branch.

**O que se ligou:** o `~/.local/bin/brza-test` já apontava para o script quando a sessão chamou a `link_command` do
`brza-install`. O `--all` de outra sessão o criou. Esta sessão não rodou o `--all`, para não ligar os scripts em curso
do P5. O `brza-install` mostra o link `ok`.

O commit é `brza-workspace@51eef6e`.

## O que se aprendeu

- **O `brza test` sai com 1 em todo worktree até a pendência do import boundaries fechar**, porque o
  `check:changed` acusa o `external-subcommand.ts` da master.
- **O `check:changed` já roda os testes afetados**: na corrida com falha, ele acusou "unit tests" junto. O vitest do
  `brza test` repete esses arquivos, mas só ele dá o relatório por teste que o baseline compara.
- **O `git pull --rebase` sem argumentos falhou** com "Cannot rebase onto multiple branches", com as sessões paralelas
  fazendo fetch no mesmo checkout. O `git pull --rebase origin master` passou.

## O que ficou

- O P5, o P7 e o P8 do PLN-002.

## Fora do workspace

- **O quê e onde:** o link `~/.local/bin/brza-test` → `scripts/brza/brza-test` do checkout principal, criado pelo
  `brza-install --all` de outra sessão do PLN-002 e conferido aqui.
- **O risco:** o comando passa a ser achado pelo PATH; o link quebra se o checkout principal sair do lugar.
- **Estado:** ativo.
- **Como desfazer:** `rm ~/.local/bin/brza-test`.
