---
scope:
  - workspace
---

# O PLN-002/P10: as correções da revisão

O pedido, em 2026-10-29, na sessão `pln-002-sessions-rename`: "sim", de Anderson, à pergunta "O P10 espera a sua
autorização. Posso executar nesta sessão?". O passo corrige o A1 ao A4 e o A6 da
[REV: a entrega do PLN-002, do P0 ao P9](../reviews/pln-002-os-comandos-brza.md), com os destinos da R14 e da R15 do
[PLN-002: Os passos manuais que se repetem entre sessões viram comandos `brza`](../../plans/PLN-002-os-comandos-brza/PLN-002-plan.md).

## O que se fez

Em `brza-workspace@82ff848`, com um caso que falhou antes para cada achado:
- **A1:** o `brza-test` recusa o checkout principal com saída 2, antes do `PRELUDE`, como o `brza-dev`.
- **A2:** o `brza-tree --rm` pede `--empty` para a branch sem commit próprio; o `--force` fica para o sujo, o não
  mergeado e o órfão, e imprime `descartado:` com cada razão. Um não cobre o outro.
- **A3:** o `brza-note commit` faz `git fetch` e só roda o `pull --rebase --autostash` quando a `origin` andou.
- **A4:** o `brza-app install` marca o worktree para ficar antes de apagar o app antigo; o `OSError` e o Ctrl-C na troca
  imprimem o `ditto` a repetir, sem traceback.
- **A6:** o esqueleto do `brza-note new worklog` leva o nome da sessão pelo `ORCA_AGENT_SESSION_ID`: o do mapa e, sem
  entrada, o `/rename`, com as funções do `brza-sessions`.

A suíte foi de 151 a 158 testes, todos `OK`.

## O que se aprendeu

- **O A3 apareceu antes do conserto.** No commit da revisão (`f77e28c`), o `git pull --rebase` desta sessão recusou
  pelos arquivos sujos da sessão do PLN-001; o `fetch` mostrou a `origin` parada, e o push foi direto, sem stash.

## O que ficou

- **O Fechamento do PLN-002.**
