---
status: done
description: Revisão interna do carimbo, marco, corte e medida no commit dos worklogs, com o aviso por workstream.
scope:
  - brza-workflow
opened: 2026-11-09
completed: 2026-11-09
tags:
  - tooling
---

# REV-021: O P3 e o ajuste do P5.6 do PLN-012

Revisão independente pelo subagente `reviewer` do
[PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md),
contra D1, D3, P3, P5.6 e a regressão. Alvo final: `brza-workflow@4119ec1`, sobre `0a6f181`.

A aprovação automática bloqueou a chamada ao `agy` por possível envio de código privado a serviço externo. Anderson
respondeu em 2026-11-09, nesta sessão: "Usar somente um subagente interno nesta execução". A exceção vale para esta
execução; a preferência durável da memória não foi alterada.

## Achados

### A1 — O commit de uma pasta reabria worklogs intactos

> bug · importante · confiança 100 · → corrigido aqui

**Evidência:** uma sonda com worklog novo e antigo intacto reproduziu a alteração do antigo e a divisão indevida da
tarefa. `bin/brza-note:862` agora filtra os worklogs modificados ou novos antes de gerar metadados. A regressão
`test_directory_commit_does_not_reopen_or_rewrite_unchanged_worklog` falhou antes e passou depois da correção.

### A2 — O evento guardava o SHA anterior ao rebase

> bug · importante · confiança 100 · → corrigido aqui

**Evidência:** uma sonda com remoto adiantado reproduziu `event.commit != HEAD` depois do push.
`bin/brza-note:904` agora registra o SHA depois da sincronização e antes do push. Falha de fetch conserva o marco do
commit local. As regressões `test_task_hash_matches_rebased_commit_before_push` e
`test_failed_fetch_keeps_event_for_successful_local_commit`
passaram na conferência independente.

## Hipóteses conferidas

- A prévia avançaria o estado do hook: falsa; os testes de offset e CPU mantêm `state.json` intacto.
- A divisão divergiria do resumo: falsa; `bin/brza-note:839` usa `aggregate_by_task`, com teste de divisão.
- A exceção golden aceitaria mudanças arbitrárias: falsa; `tests/hooks/golden_differences.py:285` exige a troca
  textual exata do comando, mantendo a comparação integral.

## Verificação e parecer

- Conferência independente de `TaskCommitTest`: 20 testes OK; os dois casos adicionais do implementer, corte local
  `HH:MM` e falha de push, compõem a classe final com 22 testes OK.
- `python3 -m unittest discover -s tests/hooks -p test_golden_render.py`: 17 testes OK.
- `git diff --check`: limpo.

**Aprovado após as duas correções, sem achados impeditivos restantes.** O P6 não foi executado; as suítes completas
de integração ficam registradas no worklog da entrega.
