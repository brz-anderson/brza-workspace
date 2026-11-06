---
scope:
  - brza-workflow
refs:
  - PLN-012
---

# Os passos do PLN-012 em paralelo

O pedido de Anderson, em 2026-11-06, na sessão `tools-kit-produtividade`: "inicie os passos em paralelo".

## O que se fez

- **O que pode ir junto:** P1, P2, P4 e P5 mexem em arquivos diferentes, e o P2 e o P5 se escrevem contra o contrato
  do Desenho. O P3 espera o P1 e o P2, e o P6 fica por último. O desvio é o X1 do
  [PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md).
- **No `brza-workflow`:** a branch de integração `feat/pln-012-medida-por-tarefa`, saída da `origin/master` e com push,
  e um worktree por passo em `.worktrees/pln-012-p1`, `-p2`, `-p4` e `-p5`, nas branches `feat/pln-012-<pN>`.
- **Quatro sessões abertas pelo `brza sessions`, com `--rename`:** `pln012-p1`, `pln012-p2`, `pln012-p4` e
  `pln012-p5`. Cada pedido leva o passo, o D, o contrato dos outros passos, o laço de revisão pelo `agy` com a rodada
  final pelo `reviewer` e o aviso por correio ao fechar. Os pedidos estão no scratch do chat, em `pedidos/`.
- **O P5.5 está feito:** as 10 issues de lacuna do D7, listadas em `## Pendências conhecidas` do plano.

## O que ficou

- Juntar cada passo na branch de integração quando a sessão dele avisar, e marcar o `[x]` com a evidência.
- O P3, depois do P1 e do P2; o P6 por último.
