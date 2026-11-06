---
scope:
  - brza-workflow
refs:
  - PLN-012
  - REV-018
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

- **O aviso do P5 foi para a sessão errada.** Anderson perguntou: "o `P5` terminou e não retornou pra vc, pq?". O P5
  mandou o correio às 19:12:37, e o processo desta sessão só subiu às 19:13:50, no turno seguinte de Anderson
  (`ps -o lstart` do `claude`): o app encerra o processo da sessão parada, e ela some do `ListAgents`. Sem o nome
  exato na lista, o P5 mandou o aviso a `tools-kit`, outra sessão, que o leu e editou o PLN-012 em `0b65202`, de novo
  com o e-mail `noreply` do GitHub. As edições conferem com o REV-018: o comando de teste do checador, a
  `## Revisões` e a linha do worklog.
- **O P1, o P2 e o P4 foram avisados** por correio para não mandar o aviso a outra sessão: o worklog de cada um é a
  devolução.
- **O P5 foi juntado na integração** (`feat/pln-012-medida-por-tarefa@cbbe0bd`), com `python3 tests/notes-checker/run.py`
  → saída 0; falta o merge na `master` do `brza-workflow`, no fim.
- **X2:** o `--until` do P5 leva o começo do primeiro turno da tarefa seguinte (REV-018, A15), e por isso o segmento
  passou a `[marco anterior, marco)` no D1. O P2 foi avisado por correio.

## O que ficou

- Juntar cada passo na branch de integração quando a sessão dele avisar, e marcar o `[x]` com a evidência.
- O P3, depois do P1 e do P2; o P6 por último.
