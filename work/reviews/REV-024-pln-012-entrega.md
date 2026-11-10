---
status: done
description: Revisão da entrega inteira do PLN-012 contra o Pedido, a Cobertura e a Regressão, em duas rodadas, com os quatro achados corrigidos no P8.
scope:
  - brza-workflow
opened: 2026-11-09
completed: 2026-11-09
tags:
  - tooling
---

# REV-024: A revisão da entrega do PLN-012, a medida por tarefa

Revisão da entrega do
[PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md)
inteira, de P1 a P7, contra o `## Pedido`, a Cobertura, a `## Regressão` e o Desenho (D1–D7). Os passos já tinham as
revisões deles: REV-017 a REV-021 e as três rodadas do P7, descritas no próprio passo.

**Quem revisou:** o subagente `reviewer` interno, que não executou nenhum passo, em duas rodadas. O `agy` da memória
do workstream ficou de fora porque a aprovação automática o barrou nesta data, como registra o REV-021. Os destinos
seguem o recomendado, pela mesma memória.

**O alvo:**
- na primeira rodada, `brza-workflow@7afed94`;
- na segunda, o P8 sem commit sobre ele, entregue em `b2b497d`.

## Achados

### A1 — O `close-task` só citava a `## Custo da tarefa`, e o texto acrescentado abaixo da `## Medida` se perdia

> lacuna · importante · confiança 85 · → corrigido aqui

**Evidência:** o `close-task` (`core/.claude/skills/close-task/SKILL.md:49`) mandava acrescentar ao worklog "acima da
`## Custo da tarefa`". O `without_cost_section` (`bin/brza-note:834-853`) corta no primeiro dos dois títulos. Uma sonda
com `## Medida` e uma seção depois devolveu só o texto de cima. O `git grep -l '^## Medida'` nas `workstream/*` achou
8 worklogs de 2026-11-09. Corrigido no P8: a skill cita os dois títulos (`brza-workflow@829527c`).

### A2 — O evento `task` gravava o pid do `brza-note`, e não o do `claude`, como o D1

> desvio · sugestão · confiança 88 · → corrigido aqui

**Evidência:** o `bin/brza-note:723` gravava `os.getpid()`. No log real, os `task` da sessão `c3083ec5` saíram com
pid 38305 e 14317, e os `turn` com `machine.pid` 32494. Corrigido no P8 com o `claude_pid()` do `measure.py`. O teste
`test_the_task_event_carries_the_pid_of_the_session_claude` falha no `7afed94`.

### A3 — A CPU da seção saía em segundos com decimais, contra a regra de números do D3

> desvio · sugestão · confiança 82 · → corrigido aqui

**Evidência:** o `bin/brza-note:812-815` formatava a CPU com `f'{v:.2f}'` e " s". O worklog do P6.2 saiu com "CPU
27,94 s do `claude` e 1089,43 s dos comandos" e, na mesma linha, a CPU do `brza run` pelo `human_duration`. Corrigido
no P8: a CPU passa pelo `human_duration`. O teste `test_the_cpu_follows_the_number_rule_of_the_section` espera "CPU
28 s do `claude` e 18 min dos comandos". O exemplo do D3 foi alinhado.

### A4 — O texto do plano e do Desenho tinha três restos

> lacuna · sugestão · confiança 95 · → corrigido aqui

**Evidência:**
- o cabeçalho da Cobertura estava duplicado (`PLN-012-plan.md:37-38`);
- as linhas da R3.1 e da R3.2 diziam `## Medida`;
- o D7 (`PLN-012-design.md:383`) apontava uma "lista final abaixo" que não existe.

Corrigidos no plano e no Desenho.

### A5 — O `CLAUDE.md` sincronizado não tinha `task`, `run` nem `--by-task`

> lacuna · importante · confiança 90 · → falso

**Por que é falso:** o contexto de arranque da sessão trazia a versão antiga do arquivo, e o disco tem a nova.

**Evidência:** o `grep -n` no `CLAUDE.md` do `tools-kit` acha as linhas 90, 91, 93, 105 e 107, e o `diff` contra o
`core/` mostra só a troca dos `{{…}}`.

### A6 — O commit com 4 worklogs dava a cada um o total, em vez de dividir

> bug · importante · confiança 90 · → falso

**Por que é falso:** só a coluna de turnos não divide, como o D4 manda.

**Evidência:** os 19 turnos do segmento das `reuniao-ci-*` do `playground` somam US$ 16,00, e cada tarefa tem
`cost_turns` 4,00 e `shared_with` 3.

### A7 — A suíte ainda escrevia no log real depois do P7

> bug · importante · confiança 95 · → falso

**Por que é falso:** o isolamento do `NoteFixture` e do teste do `--chat` cobre todo caminho que grava no log.

**Evidência:** antes e depois das suítes `tests/cli`, `tests/hooks` e `tests/notes-checker`, o log real teve 0
linhas `task` e 0 `run` com `cwd` no temp ou no `brza-workflow`.

## O que se conferiu sem achado

- Cada critério da Cobertura tem o teste do nível dito, e as 12 issues de `## Pendências conhecidas` existem, `open`.
- Os 15 commits citados estão na `master` do `brza-workflow`.
- O `--by-task --json` da tarefa do P6.2 bate com o P6.3.
- `executed_h` e `estimate_h` batem com a soma dos passos.
- A Regressão vale:
  - `tests/cli`: 592 testes, só as 4 falhas de linha de base de `test_brza_sessions`;
  - `tests/hooks`: 348 OK;
  - `tests/notes-checker`: saída 0;
  - o resumo padrão, o `--by-workstream`, o `--facts`, o `--denials` e o `--json` dão `diff` vazio entre a `master`
    de antes do plano (`d1fa1d7`) e a de agora, sobre uma cópia do log.
- Na segunda rodada, o `claude_pid()` fora de sessão devolve `(None, None)` sem travar o commit
  (`measure.py:603-617`, `ps` com `timeout=2`). A CPU sai "0 s" só abaixo de 0,5 s.
