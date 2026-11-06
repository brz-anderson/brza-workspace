---
status: open
description: O aviso do `--pending` soma os turnos sem tarefa de toda sessão do workstream parada há mais de 2 h, sem teto de idade, e cresce até ser ignorado.
scope:
  - brza-workflow
opened: 2026-11-06
priority: low
---

# O aviso do --pending soma as sessões paradas de qualquer idade

## O pedido

Ponto deixado pela rodada final da revisão do P2 do
[PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md),
no [REV-020: O P2 do PLN-012, o --by-task e o --pending, revisado pelo agy e pelo Opus](../reviews/REV-020-pln-012-p2-by-task-e-pending.md).
Fica como issue, e não como conserto no passo, porque acrescenta um filtro que a R3.3 ("os 'sem tarefa' das outras
sessões do workstream paradas há mais de 2 h") e o D6 não têm.

## O que se sabe

- **O critério de hoje** (`summarize_measurements.py`, `pending()`, `brza-workflow@8442b35`): entra a outra sessão do
  mesmo workstream que tem turno depois do último marco dela e cujo último turno tem mais de 2 h (`STALE_S`). Não há
  limite de idade.
- **O efeito no log real:** com o deploy simulado em 2026-11-03 (os `task` montados à mão da sessão `08e6c812`), o
  aviso de uma sessão do `tools-kit` em 2026-11-06 já diz "35 turnos em 3 sessões paradas há mais de 2 h (US$ 41,79)".
  Toda sessão que fecha sem worklog fica no aviso para sempre.
- **O que o revisor recomendou:** limitar às sessões cujo último turno é posterior ao último marco desta sessão, ou dos
  últimos 7 dias. Custo: ~15 min e um teste. Se paga: na primeira semana depois do deploy.

## O que falta

A rodada com Anderson sobre o teto (nenhum, o último marco desta sessão ou N dias), depois da primeira semana do deploy,
com o número que o aviso der nela.
