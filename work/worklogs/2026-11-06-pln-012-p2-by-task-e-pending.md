---
scope:
  - brza-workflow
refs:
  - PLN-012
  - REV-018
  - REV-020
  - issue:o-pending-mostra-sessoes-paradas-sem-teto-de-idade
---

# O P2 do PLN-012, o --by-task e o --pending no resumo da medição

O pedido de Anderson, em 2026-11-06, na sessão "Plano: medir a produtividade por tarefa (tools-kit)", depois do aceite
do corte (R5.1): "inicie os passos em paralelo". Esta sessão, `pln012-p2`, executou o P2 do
[PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md),
que executa o D4, no worktree `brza-workflow/.worktrees/pln-012-p2`, branch `feat/pln-012-p2`.

## O que se fez

- **`summarize_measurements.py --by-task`:**
  - `task_segments(rows)` corta cada sessão em segmentos pelos eventos `task` (o marco é o `until` ou o `timestamp`);
  - `task_measure(rows)` dá os três tempos, o custo de turnos e subagentes, a CPU do `machine` e o `brza run`;
  - `aggregate_by_task(rows, since, workstream)` monta as três tabelas do D4 e o `--json`;
  - todas ficam no módulo, prontas para o `brza-note` usar por `runpy` no P3.
- **`--by-task --pending --session <id>`:** imprime o aviso do D6, os turnos depois do último marco da sessão e os sem
  tarefa das outras sessões do workstream paradas há mais de 2 h. Sai 0 sempre.
- **A linha antiga:** `waits_s` ausente é sem espera, e `machine` ausente é sem CPU (a CPU sai "—").
- **A fixture da sessão `08e6c812` de 2026-11-03**, tirada do `.measurements/measurements.jsonl` e dos commits de
  worklog do `workstream/tools-kit` (`74fbe0f` às 22:07:39 e `539b744` às 22:16:03, da abertura do PLN-012; `afaf8c0`
  às 22:32:31, da instalação do grok). Os 3 `task` foram montados à mão na forma do D1. O teste confere o que o P2 pede:
  - a abertura com agente 452 s, Anderson 625 s e pausa 0;
  - o T2 com o grok;
  - a ociosa de 13,8 min (828 s, mais 1 s antes do trecho sem tarefa);
  - o T3 a T5 sem tarefa, com os 2 subagentes.
  - O `--pending` dessa sessão reproduz o exemplo do D6: "3 turnos desde 22:32 (corrido 10 min, US$ 0,65…)".
- **A revisão:** três rodadas do `agy` e a final do Opus, com os consertos do `implementer`, no
  [REV-020: O P2 do PLN-012, o --by-task e o --pending, revisado pelo agy e pelo Opus](../reviews/REV-020-pln-012-p2-by-task-e-pending.md).
  O ponto que não coube no passo foi para a issue
  [O aviso do --pending soma as sessões paradas de qualquer idade](../issues/o-pending-mostra-sessoes-paradas-sem-teto-de-idade.md).

**Evidência:**
- `brza-workflow@a4e98bf` (os 5 commits `01ea058`, `0f5fbde`, `89726f3`, `8442b35`, `a4e98bf`, no
  `origin/feat/pln-012-p2`).
- `python3 -m unittest discover -s tests/hooks -p test_summarize_measurements.py` → 79 testes, OK; o mesmo no
  `/usr/bin/python3` 3.9.6 → 79, OK.
- `python3 -m unittest discover -s tests/hooks` → 322 testes, OK.
- **A Regressão:** o `summarize_measurements.py` de `591f0ed` e o de `a4e98bf`, sobre uma cópia do log de hoje, sem
  flag, com `--by-workstream`, `--facts`, `--json` e `--denials` → as cinco saídas iguais (`cmp`).

**Executado:** 1,3 h (de 18:22 a 19:40).

### Os desvios

- **X2, o segmento passou a `[marco k−1, marco k)`.** O D1 dizia `(marco k−1, marco k]`. A sessão que conduz pediu a
  troca por correio depois do REV-018/A15 do P5: o `--until` leva a hora do começo do primeiro turno da tarefa
  seguinte, e esse turno tem de ir à seguinte. O D1 já traz o X2 (`tools-kit@fbda802`). O revisor final achou o mesmo
  (A1). Teste: o turno que começa exatamente no `until`, em ISO e em `HH:MM:00`, vai à tarefa seguinte.
- **O comando de teste do plano não roda.** `python3 -m unittest tests/hooks/test_summarize_measurements.py` falha no
  `import repo_fixture`, que mora na pasta. A evidência usa
  `python3 -m unittest discover -s tests/hooks -p test_summarize_measurements.py`.
- **O `--pending` não segue à risca o formato do D6.**
  - A hora de cada turno é `HH:MM`, mas sai em ISO completa quando o turno começou noutro dia ou no mesmo minuto de
    outro, porque é ela que o `--until` recebe (REV-020, A2 e N1).
  - O custo traz os subagentes ("US$ 0,65 dos turnos e US$ 4,05 de 2 subagentes").
  - Aceita `--workstream` como o workstream das outras sessões, para a sessão que ainda não tem turno fechado
    (REV-020, A4).
  - Sem `--session`, ou com ela vazia, imprime "nada a fechar" e sai 0.
- **O que o D4 não fixava, decidido no código e mantido pelas quatro revisões:**
  - O corte do R4.1 é pela linha que *termina* antes do primeiro `task`: o turno que contém o primeiro commit entra.
  - A tabela 2 é por evento `task`, com os dois motivos do D4. O worklog com outro commit medido segue na tabela 1.
  - A ociosa soma também o intervalo antes do trecho sem tarefa.
  - Na divisão por n, os tempos, o custo e a CPU entram com 1/n, e as contagens e os picos entram inteiros; a tarefa
    leva "÷n" no nome.
  - O `--since` e o `--workstream` filtram a saída, e não a leitura, para os marcos de antes da data não sumirem.
  - A sessão só de `task`, sem linha medida, fica fora da tabela 3.

## O que ficou

- **Para o P3:** o revisor final recomenda que a `## Medida` saia do `aggregate_by_task(rows)["tasks"]`, filtrado pelo
  worklog, e não de uma soma remontada de `task_measure`, para bater com a tabela com a divisão por n. E o corte do
  R4.1 vale para o `task` que o P3 acrescentar antes de gravá-lo: no primeiro commit depois do deploy, entram só as
  linhas que terminam depois dele.
- **Para o P5:** o bloco do `close-task` não passa o `--workstream` ao `--pending`. A sessão cujo único turno está em
  curso fica sem a linha das outras sessões paradas (REV-020, A4).
- **A memória do `reviewer`** em `.claude/agent-memory/reviewer/` mudou nas revisões do P1, do P2, do P4 e do P5, nos
  mesmos arquivos. Não foi a este commit; fica para a sessão que conduz juntar.
