---
scope:
  - workspace
---

# O PLN-002/P2: o brza tree

O pedido de Anderson, em 2026-10-28, na sessão `pln-002-p2`: "Execute o P2 (o brza tree) do
plans/PLN-002-os-comandos-brza/PLN-002-plan.md". O passo executa o D2 do
[PLN-002: Os passos manuais que se repetem entre sessões viram comandos `brza`](../../plans/PLN-002-os-comandos-brza/PLN-002-plan.md).

## O que se fez

**O `scripts/brza/brza-tree`** tem as três formas do D2, sobre o `git`, o `worktree_add` e o `install_offline` do
runtime, sem mudar o runtime:
- `brza-tree <nome>` faz o `git fetch origin`, cria `.worktrees/<nome>` na `<tipo>/<nome>` (padrão `feat`) da
  `origin/master` ou do `--base`, instala offline e imprime o caminho na última linha; `--chat <sessão>` chama o
  `brza-sessions <sessão> --checkout <caminho>`;
- `brza-tree --rm <nome>` faz o fetch e recusa o sujo, o `HEAD` fora da `origin/master` e a branch sem commit próprio,
  cada motivo numa linha; com `--force`, remove o worktree e apaga a branch com `-D`. O órfão é listado e só sai com
  `--force`;
- `brza-tree --list` mostra a branch, os commits à frente da `origin/master` e o limpo ou sujo; o fetch que falha vira
  uma linha `CHECK` e a lista sai assim mesmo.

**As escolhas que o D2 não fixava:**
- **O install offline que falha sai com 1**, depois de imprimir o caminho e o comando online, e não abre o chat do
  `--chat`.
- **"Sem commit próprio" se lê pelo reflog da branch.** Ela nasce com `branch: Created from …` e ganha uma linha por
  commit, rebase ou merge. Reflog vazio ou expirado conta como sem commit próprio, o lado que pede `--force`.
- **O worktree detached** sai sem `--force` quando está limpo e o `HEAD` está na `origin/master`, porque não há branch
  a perder.
- **O nome** aceita minúsculas, dígitos, ponto, hífen e sublinhado; o resto é uso errado (saída 2).

**Os testes:** o `tests/test_brza_tree.py` é novo, com 14 casos, num clone de uma `origin` local com um commit que só
chega pelo fetch, e com o `install_offline` trocado por um falso. `python3 -m unittest discover -s scripts/brza/tests`
→ 47 testes OK; eram 33.

**A corrida real**, pelo caminho inteiro, porque o link ainda não existia:
- `scripts/brza/brza-tree pln-002-p2-prova` → saída 0 em 10 s, na `feat/pln-002-p2-prova` em `fc7f07a8a1e`, a
  `origin/master`, com o `node_modules` como diretório real;
- o `--rm` sem `--force` recusou pela branch sem commit próprio, e o `--rm` no `chat-markdown-largura-e-links` o
  listou como órfão com `.cache/` e recusou; os dois saíram com 1;
- `--rm pln-002-p2-prova --force` removeu o worktree e a branch.

**O que se ligou:** `brza-install --all` ligou o `brza-tree`, e o `brza-install` mostra todo link `ok`.

O commit é `brza-workspace@2ac6638`.

## O que se aprendeu

- **O estado dos worktrees muda entre duas leituras.** O `pln-001-p48` estava detached no começo da sessão e na
  `feat/pln-001-p48` no `--list`, porque outra sessão o trocou no meio. O `--rm` lê o `git worktree list` na hora, e não
  guarda nada.

## O que ficou

- O P3 ao P6, em paralelo, cada um numa sessão `pln-002-pN`. O worktree de código de cada um sai do `brza-tree <nome>`.
- Os dois órfãos de hoje seguem em disco: quem remove é Anderson (Fora de escopo do PLN-002).

## Fora do workspace

- **O quê e onde:** o link `~/.local/bin/brza-tree` → `scripts/brza/brza-tree` do checkout principal, criado pelo
  `brza-install --all`.
- **O risco:** o comando passa a ser achado pelo PATH; o link quebra se o checkout principal sair do lugar.
- **Estado:** ativo.
- **Como desfazer:** `rm ~/.local/bin/brza-tree`.
