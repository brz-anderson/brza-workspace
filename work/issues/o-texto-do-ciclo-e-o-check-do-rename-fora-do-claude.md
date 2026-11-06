---
status: done
description: O docstring do cycle.py ainda diz que o worker é sempre Claude, e o CHECK do --rename do Grok e do Antigravity diz que o nome ficou na aba mesmo quando o --title a manteve.
scope:
  - brza-workflow
opened: 2026-11-04
completed: 2026-11-06
priority: low
tags:
  - tooling
---

# O texto do ciclo e o `CHECK` do `--rename` fora do Claude

## O pedido

Os dois achados da revisão final do
[PLN-013: O Grok, o Codex e o Antigravity abrem pelo `brza sessions` e recebem tarefas do MCP](../../plans/PLN-013-grok-codex-e-agy-no-brza-sessions-e-no-mcp/PLN-013-plan.md),
com destino `issue`, no
[REV-013: A entrega do PLN-013, revisada pelo Grok a cada passo e no fim](../reviews/REV-013-pln-013-a-entrega-pelo-grok.md).

## O que se sabe

- **O docstring do ciclo.** O `brza-workflow/packages/mcp/brza_mcp/cycle.py:4` diz `worker-start --task --agent claude`.
  A abertura usa o agente do runtime, em `cycle.py:152`.
- **O `CHECK` do Grok e do Antigravity.** O `packages/client/bin/brza-sessions:436-439` mantém o `--title` fora do
  Codex, e o `:473-474` sempre diz "o nome ficou na aba e no mapa". Com o `--title` diferente, a aba fica com o título,
  e não com o nome (`tests/cli/test_brza_sessions.py:650-655`).

## O que falta

1. Trocar o docstring do `cycle.py:4`.
2. O `CHECK` diz "o nome ficou no mapa" quando o `--title` manteve a aba, ou o `--rename` põe o nome na aba fora do
   Claude também, a decidir.

## Resolução (2026-11-06)

O docstring do `cycle.py` passou a `worker-start --task --agent <agente do runtime>`.

A aba ficou como o P10/A1 já testava: o `--title` vale no Grok e no Antigravity. O `CHECK` é que passou a dizer a verdade. Sem `--title`, ou com ele igual ao nome, a linha segue "o nome ficou na aba e no mapa". Com `--title` diferente, diz `a aba ficou com o título "…"; o nome ficou no mapa`. O teste `test_rename_preserves_title_flag_on_claude_and_others` confere essa frase, e `test_rename_without_a_reader_gives_tab_and_map_and_a_check_line` segue com a frase de quando o nome é o título. `python3 -m unittest test_brza_sessions` → 47 OK. Commit local `brza-workflow@d1fa1d7`, ainda sem push.
