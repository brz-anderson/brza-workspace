---
status: open
description: Um em cada cinco runs agendados do CI do fork falha e ninguém vê, porque o fluxo é push direto sem PR e nenhum chat ou painel mostra o CI de schedule.
scope:
  - brza-studio
opened: 2026-11-09
priority: low
tags:
  - tooling
---

# O CI agendado do `brza-studio` falha sem ninguém ver

Levantado na reunião de verificação do [PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md) (P7), sobre [Resultados de CI no chat e disparo automático de agentes em falhas de PR](resultados-de-ci-no-chat-e-disparo-automatico-de-agentes-em-falhas-de-pr.md). O revisor independente achou e a coordenação mediu. Anderson decidiu registrá-la como issue `low` ao `studio` em 2026-11-09 ("2, 3 e 4 decididos", ao item 4.1 da rodada de decisões). Não é pedido de execução.

## O que se mediu

`gh run list -R brz-anderson/brza-studio --limit 100`, em 2026-11-09: 100 runs de 2026-11-05 a 2026-11-09, **20 com `failure`**, todos de evento `schedule` ou `workflow_run`. Nenhum é de `push` ou `pull_request`.

| Workflow | Falhas | Última |
| :------- | -----: | :----- |
| Computer-use e2e | 4 | 2026-11-09 |
| E2E | 4 | 2026-11-08 |
| Headless Node server | 4 | 2026-11-08 |
| Scheduled x86 unit compatibility | 3 | 2026-11-09 |
| Computer-use macOS native | 2 | 2026-11-09 |
| Packaged browser compatibility | 1 | 2026-11-09 |
| Performance contracts | 1 | 2026-11-09 |
| Warm shared CI caches | 1 | 2026-11-06 |

## Por que ninguém vê

- **O fluxo é push direto, sem PR** (`AGENTS.md`: "O push vai direto, sem PR"), e `gh pr list --state all` dá 0 PRs no `brza-studio`.
- **O push na `master` não gera run:** os workflows de `push` do fork filtram `branches: [main]`, e a branch padrão é `master` (revisor da reunião, `git show HEAD:.github/workflows/*`).
- **As linhas de CI do `#39020`** que chegam pelo próximo merge de tag só aparecem no chat que abriu ou empurrou um PR. Elas não cobrem o CI agendado.

## O que fazer

1. Separar o vermelho real (regressão do fork) do vermelho herdado do upstream ou de ambiente (runner, cache, macOS), workflow por workflow.
2. Escolher onde o vermelho agendado aparece: um aviso do radar, uma linha no checklist do sync de tag ou o painel Checks do Studio.
3. Desligar ou reagendar o workflow que só falha por ambiente e não tem dono.
