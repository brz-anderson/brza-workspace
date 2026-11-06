---
status: done
description: As três rodadas do agy e a final do reviewer do Claude Code sobre o --by-task e o --pending do PLN-012/P2, com os achados e o destino de cada um
scope:
  - brza-workflow
opened: 2026-11-06
completed: 2026-11-06
tags:
  - tooling
---

# REV-020: O P2 do PLN-012, o --by-task e o --pending, revisado pelo agy e pelo Opus

O parecer do P2 do
[PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md).
O alvo foi o `core/scripts/summarize_measurements.py` e o `tests/hooks/test_summarize_measurements.py` do
`brza-workflow`, na branch `feat/pln-012-p2`. A régua foi o D4 do Desenho, com o D1 (o marco e a janela), o D2 (as
contas) e o D6 (o aviso), o P2, a Cobertura e a Regressão do plano.

Pelas memórias `cada-passo-revisado-pelo-agy` e `commit-ao-fechar-todo-passo`:
- três rodadas do `agy -p --model gemini-3.8-flash-high --mode plan`, com o corpo do `reviewer.md` no prompt; a cota
  respondeu nas três;
- a rodada final pelo `reviewer` do Claude Code, em Opus. O papel não está registrado na sessão do `brza-workflow`, e
  por isso ele rodou como `general-purpose` com o corpo do papel;
- os consertos pelo `implementer`, também como `general-purpose`, em Sonnet, com o corpo do papel.

Os pareceres completos ficaram no scratch (`/tmp/pln012-p2/agy-r1.md` a `agy-r3.md`); aqui vão os achados e os
destinos.

## As rodadas

| Rodada | Diff | Achados | Destino |
| :----- | :--- | :------ | :------ |
| agy 1 | `591f0ed..01ea058` | A1 a sessão parada sumia do `--pending` quando o trecho sem tarefa não tinha `workstream`; A2 o custo dos subagentes sem `US$`; A3 o teste de regressão sem o `--facts` | corrigido em `0f5fbde` |
| agy 2 | `591f0ed..0f5fbde` | A1 a tabela de sessões não usava o `session_workstream`, e o `--workstream` a descartava; A2 o `task` antigo vencia o turno recente no `session_workstream` | corrigido em `89726f3`, com o `until` impossível ("25:00") que derrubava o resumo, achado pela sessão |
| agy 3 | `591f0ed..89726f3` | nenhum; 3 hipóteses caídas (separador decimal, `run` sem sessão, sessão só com turno sem workstream) | — |
| Opus, final | `591f0ed..89726f3` | A1 a fronteira `(k−1, k]` contra o X2, sem teste; A2 o `--pending` só em `HH:MM`, sem a hora com segundos que o close-task pede; A3 o teste do subagente no turno passava sem a regra; A4 a sessão sem turno fechado perdia o workstream; A5 `--session ""` saía 2; A6 duas escolhas sem teste (custo dos subagentes das sessões paradas, contagens inteiras na divisão) | corrigido em `8442b35` |
| Opus, conferência | `89726f3..8442b35` | os 6 fechados; N1 o turno de outro dia saía em `HH:MM`, que o `--until` lê como de hoje | corrigido em `a4e98bf` |

## As escolhas do executor, atacadas nas quatro rodadas

As seis escolhas que o código fez sem rodada saíram mantidas por todos os revisores:
1. o corte do R4.1 pela linha que termina antes do primeiro `task`;
2. o "não medida" por evento `task`;
3. a ociosa com o intervalo antes do trecho sem tarefa;
4. na divisão por n, os tempos, o custo e a CPU com 1/n, e as contagens e os picos inteiros;
5. o `--since` e o `--workstream` filtram a saída;
6. o `--pending` com o custo dos subagentes.

## Os pontos da rodada final

### P1 — O aviso soma as sessões paradas de qualquer idade

> ponto · confiança 90 · → issue [O aviso do --pending soma as sessões paradas de qualquer idade](../issues/o-pending-mostra-sessoes-paradas-sem-teto-de-idade.md)

**Evidência:** no log real, com o deploy simulado em 2026-11-03, o aviso de 2026-11-06 já soma 35 turnos em 3 sessões
(US$ 41,79). Vai a issue porque o teto acrescenta um filtro que a R3.3 não tem.

### P2 — A data na lista que atravessa a meia-noite

> ponto · confiança 90 · → corrigido aqui, em `8442b35` e `a4e98bf`

**Evidência:** 11 de 164 sessões reais têm turnos em mais de um dia. A primeira forma (`dd/mm HH:MM`) caiu na
conferência (N1), porque o `--until` não a aceita. Ficou a hora ISO para todo turno que não é de hoje.

### A4 — O close-task ainda não passa o `--workstream`

> uso · confiança 90 · → a sessão que conduz, para o P5

**Evidência:** a sessão cujo único turno está em curso não tem linha no log. O `--pending` só acha o workstream dela
pelo `--workstream`, que o P2 passou a aceitar. O bloco do `close-task`
(`feat/pln-012-medida-por-tarefa:core/.claude/skills/close-task/SKILL.md:32`) não o passa.

## Hipóteses que caíram

- **O rollover do `--until HH:MM` depois da meia-noite** → falso: o D1 restringe o `HH:MM` a hoje, e o P3 recusa fora
  da janela.
- **A tarefa chaveada só pelo caminho funde worklogs de workstreams diferentes** → falso: 0 nomes repetidos nos 165
  worklogs de todas as `workstream/*`.
- **O resumo sem `--by-task` muda com `task` e `run` no log** → falso: a saída do CLI sai igual nas três visões, e
  sobre uma cópia do log real antes e depois.
- **Fica lento no log real** → falso: 3.864 linhas, `aggregate_by_task` em 4 ms.
- **Não roda no Python 3.9** → falso: 79 testes OK no `/usr/bin/python3` 3.9.6.

## A mutação

O revisor final rodou 15 mutantes do código (`/tmp/pln012-p2/opus/mutate2.py`). Depois dos consertos, 14 morrem. Só
sobrevive o `sem_max_last_end`, que não muda o resultado em sessão sem turnos sobrepostos.
