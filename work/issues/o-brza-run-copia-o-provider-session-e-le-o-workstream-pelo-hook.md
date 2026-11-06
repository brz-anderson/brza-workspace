---
status: open
description: O `brza-run` copia o `provider_session` do `brza-sessions`, que já divergiu, e lê o workstream carregando o `measure.py` pelo `runpy`.
scope:
  - brza-workflow
opened: 2026-11-06
priority: low
tags:
  - tooling
---

# O brza-run copia o provider_session e lê o workstream pelo hook de medição

## O pedido

Os achados A4 e A5 da rodada final de
[REV-019: A revisão do P4 do PLN-012, o brza run que mede](../reviews/REV-019-pln-012-p4-o-brza-run-mede.md), iguais aos
A1 e A2 das rodadas do `agy`, ficaram para depois do
[PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md).
O P4 deixou os dois de lado para não mexer nos testes do `brza-sessions` e do `brza-note` nem no `measure.py`, que o P1
editava em paralelo.

## O que se sabe

- **A cópia do `provider_session`.** O `brza-workflow/packages/client/bin/brza-run` tem uma cópia de 5 linhas do
  `provider_session` do `packages/client/bin/brza-sessions:244-250`, e as duas já divergiram. A do `brza-run` aceita o
  `result` nulo do RPC (`(found or {})`) e pega mais exceções. A do `brza-sessions:250` levanta `AttributeError` com o
  `result` nulo, nos chamadores `:237` e `:302`, e esse defeito é anterior ao PLN-012.
- **O lugar certo é o `bin/brza_runtime.py`**, ao lado do `rpc` e do `send_to_chat`. O custo da mudança está nos
  testes, que trocam o `rpc` global do `brza-sessions` (`tests/cli/test_brza_sessions.py:67,152,261`) e injetam o
  `provider_session` (`tests/cli/test_brza_note.py:160-164`).
- **O workstream pelo hook.** O `workstream_of` do `brza-run` carrega o `core/.claude/hooks/measure.py` inteiro, pelo
  `runpy`, a cada linha `run`. Custa ~35 a 58 ms, e o `except Exception` devolve `None` sem aviso. A resolução do
  workstream (`resolve_workstream`) caberia no `core/.claude/hooks/brza_root.py`, que o hook e o CLI já importam.

## Como fecha

O `provider_session` mora no `brza_runtime` e o `brza-sessions` e o `brza-run` o usam, com o `result` nulo coberto. O
`resolve_workstream` mora no `brza_root`, e o `measure.py` e o `brza-run` o chamam sem o `runpy`.
