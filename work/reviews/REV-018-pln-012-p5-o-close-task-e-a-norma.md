---
status: done
description: As duas rodadas do agy e a final do reviewer sobre o close-task, a norma do worklog e o adaptador do PLN-012/P5
scope:
  - brza-workflow
opened: 2026-11-06
completed: 2026-11-06
tags:
  - tooling
---

# REV-018: A revisão do P5 do PLN-012, o close-task e a norma

O parecer da parte de código e norma do P5 do
[PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md),
na branch `feat/pln-012-p5` do `brza-workflow`, contra o D6, a norma do D3, a Cobertura e a Regressão do plano. Duas
rodadas do `agy` (`gemini-3.8-flash-high`, `--mode plan`) e uma final do subagente `reviewer` do Claude Code. Os achados
`corrigido aqui` foram a um subagente `implementer`. O worklog do passo é
[O P5 do PLN-012, o close-task e a norma](../worklogs/2026-11-06-pln-012-p5-o-close-task-e-a-norma.md).

| Rodada | Revisor | Diff | Veredito | Destino |
| :----- | :------ | :--- | :------- | :------ |
| 1 | `agy` | `591f0ed..332c6f9` | aprova com correções | A2 e A3 corrigidos em `19509c2`; A1 à sessão que conduz |
| 2 | `agy` | `591f0ed..19509c2` | aprova | A8–A11 falsos |
| final | `reviewer` | `591f0ed..19509c2` | aprova com correções | A12–A14 e a R-a corrigidos em `22805fb` |

## Os achados

### A1 — O comando do plano não roda a suíte do checador

> plano · importante · confiança 95 · → rodada (a sessão que conduz é dona do plano)

**Evidência:** `python3 -m unittest discover -s tests/notes-checker` → `Ran 0 tests`, `NO TESTS RAN`, saída 5. A pasta
só tem o `run.py`, e o `README.md:160` do `brza-workflow` dá a suíte como `python3 tests/notes-checker/run.py`. O comando
errado está no P5.3, na Evidência do P5 e na última linha da `## Regressão` do plano.

### A12 — O acréscimo ao worklog de hoje não dizia onde, e a `## Medida` é a última seção

> correção · importante · confiança 80 · → corrigido aqui, em `22805fb`

**Evidência:** `close-task/SKILL.md`, passo 3, mandava acrescentar "o que veio depois", e o bullet da `## Medida` diz que
o comando a reescreve a cada commit. No segundo commit do mesmo worklog, o texto acrescentado no fim fica dentro da
`## Medida` e se perde. Premissa: o P3 corta a seção até o próximo H2 ou o fim. Agora: "acima da `## Medida` quando ela
existe". Vai ao P3 como aviso: preservar o que vier depois da seção.

### A2 — O passo 6 dizia "achou duas", e o passo 2 "mais de uma"

> skill · sugestão · confiança 90 · → corrigido aqui, em `19509c2`

**Evidência:** `close-task/SKILL.md:36` e `:82` em `332c6f9`. Agora o passo 6 diz "mais de uma", e o 2 manda repetir
da mais antiga para a mais nova.

### A3 — A menção inline do `--until` omitia o `-m` obrigatório

> skill · sugestão · confiança 85 · → corrigido aqui, em `19509c2`

**Evidência:** `bin/brza-note`, o `-m` com `required=True`; `brza note commit x.md --until 12:00` → "the following
arguments are required: -m".

### A13 — A linha `turn` dizia "a CPU e o RSS do `claude`", e o `machine` traz os filhos

> norma · sugestão · confiança 85 · → corrigido aqui, em `22805fb`

**Evidência:** o D2 e o `measure.py` do P1 (`feat/pln-012-p1`) gravam `cpu_self_s` e `cpu_children_s`. Agora: "a CPU do
`claude` e dos comandos que ele rodou, com o RSS".

### A14 — A seção "Commit" da norma descrevia o `brza note commit` só pelo `refs:`

> norma · sugestão · confiança 85 · → corrigido aqui, em `22805fb`

**Evidência:** `core/work/README.md:193`. Agora aponta o `sessions:` e a `## Medida` à seção `work/worklogs/`, sem
repetir a regra.

### A15 — O `--until` mandava a hora do fim do último turno, que o aviso não mostra (a R-a do `reviewer`)

> skill · importante · confiança 85 · → corrigido aqui, em `22805fb`, como desvio do texto do D6

**Evidência:** o turno vai à tarefa pela hora em que começa, em `(marco anterior, marco]` (D1); o `--pending` do P2
imprime só o começo de cada turno, em `%H:%M`; o `HH:MM` vira `HH:MM:00`. O fim de um turno curto, cortado no minuto,
cai antes do começo dele, e o turno passa à tarefa seguinte. Agora: o `--until` leva a hora que a lista mostra para o
primeiro turno da tarefa seguinte, ou a hora ISO quando os dois começam no mesmo minuto.

### A4 — "O teste não é TDD"

> teste · importante · → falso

**Por que é falso:** o caso do checador já passava (F26), mas as asserções da norma no mesmo `check_pln012_p5` barram o
código de antes.

**Evidência:** o `run.py` de `19509c2` sobre o `git archive 591f0ed` sai 1, com 11 FALHA nas asserções da norma, da
skill e do adaptador.

### A5 — Os acréscimos ao texto do D6 divergem do Desenho

> skill · importante · → falso

**Por que é falso:** a linha "nada a fechar" e sem `CLAUDE_CODE_SESSION_ID`, e o bullet da `## Medida`, saem do D1 e do
D3.

**Evidência:** D1, "Sem `CLAUDE_CODE_SESSION_ID` … o worklog não ganha carimbo"; D3, a seção escrita pelo comando; D4,
"sem turno pendente, imprime 'nada a fechar'".

### A6 — Os campos novos do `turn` no `CLAUDE.md` são do P1

> norma · importante · → falso

**Por que é falso:** o `CLAUDE.md` do adaptador só se edita neste passo, e a tabela sem os campos do D2 ficaria atrás
do `--by-task` que ela descreve.

**Evidência:** `git diff --stat 591f0ed...feat/pln-012-p{1,2,4}` sobre os arquivos do P5 sai vazio.

### A7 — A suíte deveria virar `unittest`

> teste · importante · → falso

**Por que é falso:** o `run.py` é a convenção da pasta, e os casos de antes (`check_pln008_p1`, `check_pln008_p8`)
moram nele.

**Evidência:** `README.md:160` do `brza-workflow`.

### A8 — A regra de três ou mais tarefas diverge do D6

> norma · importante · → falso

**Por que é falso:** o D6 diz "mais de uma tarefa"; o exemplo de duas é ilustração.

**Evidência:** `PLN-012-design.md`, o bloco do D6.

### A9 — O comando com `--until` do passo 2 omite as notas e a memória

> norma · importante · → falso

**Por que é falso:** o passo 2 só corta a tarefa anterior; os caminhos da tarefa em curso ficam no passo 6.

**Evidência:** `close-task/SKILL.md`, passos 2 e 6.

### A10 — O caminho dos testes do hook diverge entre o `core/CLAUDE.md` e a cópia golden

> norma · importante · → falso

**Por que é falso:** a diferença é a entrada `tests-moved` da lista fechada do golden.

**Evidência:** `tests/hooks/golden_differences.py`; `python3 -m unittest tests/hooks/test_golden_render.py` → OK.

### A11 — A asserção do worklog antigo seria inoperante

> teste · sugestão · → falso

**Por que é falso:** ela isola o worklog sem `sessions:` no relatório do checador, que é o "e o antigo" da Regressão.

**Evidência:** `tests/notes-checker/run.py`, `check_pln012_p5`.

## O que rodou

- `python3 tests/notes-checker/run.py` → saída 0, os 14 casos do `check_pln012_p5` `ok`.
- `python3 -m unittest discover -s tests/hooks` → 291 testes, OK (com o golden e o `test_compact_guard`).
- `python3 -m unittest discover -s tests/cli` → 492 testes, OK; `-s tests/mcp` → 389 testes, OK.
- No `agy`, três erros do `test_brza_runtime` com `Operation not permitted` no socket: do sandbox dele, e não do código.
