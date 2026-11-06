---
scope:
  - brza-workflow
refs:
  - PLN-012
  - REV-017
  - REV-018
  - REV-019
  - REV-020
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

- **Anderson pediu**: "assim que todos os passos retornarem, feche as sessões e limpe as branches que você abriu". Uma
  espera (`Monitor`) acompanhou o commit dos worklogs: P4 em `4a49d9c`, P1 em `2a28d32` e P2 em `9da2957`. Os três também
  avisaram por correio, porque esta sessão estava num turno.
- **P1, P2 e P4 juntados na integração** (`2602b6d`, `9e82bb1`, `5ecddfe`). O conjunto falhou 43 vezes no
  `test_brza_init`: o P1 e o P2 escreveram "Anderson" no `measure.py` e no resumo, e o `brza init` recusa nome de
  workspace no `core/`. Consertado em `0a6f181` (X6). Depois disso, as três suítes verdes, sem a `BRZA_WORKSPACE`:
  `tests/hooks` → 348 OK, `tests/cli` → 506 OK, `tests/notes-checker/run.py` → saída 0.
- **A `BRZA_WORKSPACE` desta sessão quebra 20 testes de `tests/cli`**, os que descobrem o workspace; sem ela, passam. As
  sessões abertas no `brza-workflow` não a têm, e por isso não viram.
- **O plano ficou com P1, P2 e P4 `[x]`**, com o `Executado` (1,1 h, 1,3 h e 1,1 h), os desvios X3 a X6, os pareceres
  REV-017, REV-019 e REV-020 e as duas issues dos passos. O P1.4 foi ao P6; o P5.6 (o `--workstream` no `--pending`)
  vai junto do P3.
- **As sessões `pln012-p1`, `-p2`, `-p4` e `-p5` já estavam fechadas** no app: o `brza sessions close` deu
  `tab_not_found`, e elas não aparecem no `brza sessions list`.
- **Limpeza no `brza-workflow`:** os worktrees `.worktrees/pln-012-p1`, `-p2`, `-p4`, `-p5` e `.worktrees/pln-012`
  removidos, e as branches `feat/pln-012-p1`, `-p2`, `-p4` e `-p5` apagadas no local e no `origin`, depois de conferido
  que cada uma está na integração. A `feat/pln-012-medida-por-tarefa` fica, com o trabalho dos passos, até o merge na
  `master`.
- **A memória do `reviewer`**, que os passos deixaram suja, foi junto deste commit.

## O que ficou

- O P3, com o P5.6, num worktree saído da integração; depois o merge na `master` do `brza-workflow` (P5.4) e o P6.
