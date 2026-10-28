---
scope:
  - workspace
---

# O PLN-002/P1: o runtime comum e o brza-install --all

O pedido de Anderson, em 2026-10-28, na sessão `pln-002-p1`: "Execute o P1 do
plans/PLN-002-os-comandos-brza/PLN-002-plan.md pela plan-runner". O passo executa o D1 do
[PLN-002: Os passos manuais que se repetem entre sessões viram comandos `brza`](../../plans/PLN-002-os-comandos-brza/PLN-002-plan.md).

## O que se fez

**O runtime** (`scripts/brza/brza_runtime.py`) ganhou, sem mudar nenhum nome de antes:
- o `canonicalize`, o `send_mutation` e o `send_to_chat`, vindos do `brza-run` e do `brza-sessions`, que passam a
  importá-los e os mantêm no módulo. O `send_to_chat` do `brza-sessions` tinha a mutação embutida e agora usa a do
  runtime, a mesma do `brza-run`;
- o `STUDIO`, do `BRZA_STUDIO` ou de `~/Projects/brza-studio`;
- o `git`, o `worktree_add`, o `install_offline` e o `worktree_remove`, como o D1 os assina, com um desvio: o
  `git` recebe `cwd=None` e resolve o `STUDIO` na hora da chamada (`PLN-002/X1`).

**O `brza-install --all`** liga todo `brza-*` executável de `scripts/brza/`, inclusive ele mesmo; o `claude-brza` segue
só pelo `--chat-command`. O estado sem flag passa a listar o `claude-brza` e todo `brza-*`. A ajuda ganhou o `--all` e
continua com os nomes `brza-install`/`brza-run`: o `brza install` ainda responde `Unknown command: install` no app
instalado, e a troca dos textos é o P5.5.

**Os testes:** o `tests/test_brza_runtime.py` é novo, com 10 casos. O worktree é testado num clone de uma `origin`
local, com um commit que só chega pelo `fetch`, e o `pnpm` é trocado por um falso que sai 1 e depois 0. O `InstallTest`
ganhou o `--all` e o `--all --dry-run`. O teste de envio do `brza-sessions` passou a fazer o patch em
`brza_runtime.rpc`. `python3 -m unittest discover -s scripts/brza/tests` → 33 testes OK; eram 21 antes, e os 21 seguem
entre eles.

**O que se ligou:** `scripts/brza/brza-install --all` criou o link do `brza-install`; o `brza-install` mostra
`claude-brza`, `brza-install`, `brza-run` e `brza-sessions` como `ok`, e o override do chat no `claude-brza`.

## O que se aprendeu

- **O texto de prova da impressão digital carrega um ` ` cru** em `tests/test_brza_scripts.py`. Copiado à mão,
  ele some e a impressão muda; no teste novo ele vai como escape.

## O que ficou

- O P2, o `brza tree`, numa sessão `pln-002-p2`, que já importa o `worktree_add` e o `install_offline`.

## Fora do workspace

- **O quê e onde:** o link `~/.local/bin/brza-install` → `scripts/brza/brza-install` do checkout principal, criado pelo
  `scripts/brza/brza-install --all`.
- **O risco:** o comando passa a ser achado pelo PATH; o link quebra se o checkout principal sair do lugar.
- **Estado:** ativo.
- **Como desfazer:** `rm ~/.local/bin/brza-install`.
