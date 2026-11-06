---
scope:
  - brza-workflow
tags:
  - tooling
refs:
  - PLN-013
  - issue:o-rename-pelo-chat-nao-chega-ao-antigravity
  - issue:o-rename-pelo-chat-nao-chega-ao-grok
  - issue:o-status-do-mcp-nao-diz-o-runtime-do-pedido
  - issue:o-texto-do-ciclo-e-o-check-do-rename-fora-do-claude
---

# O status e o CHECK das pendências do PLN-013

O pedido de Anderson, em 2026-11-06, depois de fechar a cota do Grok: "siga com as próximas", as pendências do
[PLN-013: O Grok, o Codex e o Antigravity abrem pelo `brza sessions` e recebem tarefas do MCP](../../plans/PLN-013-grok-codex-e-agy-no-brza-sessions-e-no-mcp/PLN-013-plan.md).

## O que se fez

- **O `status`.** O `brief` passou a incluir `runtime`, `model` e `effort`. O
  `test_status_lines_carry_runtime_model_and_effort` cobre `running`, `queued` e `finished`.
  `python3 -m unittest test_mcp_dispatch` → 32 OK. A issue
  [O `status` do MCP não diz o runtime do pedido](../issues/o-status-do-mcp-nao-diz-o-runtime-do-pedido.md) fechou.
- **O texto do ciclo e o `CHECK`.** O docstring do `cycle.py` deixou de fixar `--agent claude`. Com `--title`
  diferente do nome, o Grok e o Antigravity avisam que a aba ficou com o título e o nome ficou no mapa. A aba em si
  segue o P10/A1. `python3 -m unittest test_brza_sessions` → 47 OK. A issue
  [O texto do ciclo e o `CHECK` do `--rename` fora do Claude](../issues/o-texto-do-ciclo-e-o-check-do-rename-fora-do-claude.md)
  fechou.

## Em aberto

- [O `/rename` pelo chat não chega ao Grok](../issues/o-rename-pelo-chat-nao-chega-ao-grok.md). O `renameProviderSession`
  existe no Codex e no Pi; o adaptador do Grok não o implementa.
- [O `/rename` pelo chat não chega ao Antigravity](../issues/o-rename-pelo-chat-nao-chega-ao-antigravity.md). O item do
  `yolo` é decisão de Anderson.

## Fora do workspace

- **O quê e onde:** dois commits no `master` de `~/Projects/brza-workflow`, `190cf58` (o `status`) e `d1fa1d7`
  (o docstring e o `CHECK`). **Risco:** nenhum além do código publicado. **Estado:** no `origin/master` desde
  2026-11-06 (`591f0ed..d1fa1d7`). **Como desfazer:** `git revert d1fa1d7` e `git revert 190cf58` nesse checkout.
- **O quê e onde:** o serviço `com.brza.orchestrator` parado e subido de novo, a pedido de Anderson. O plist segue
  `~/Library/LaunchAgents/com.brza.orchestrator.plist`, com o `brza-mcp` do checkout principal. O pid passou de 71714
  para 18765. **Risco:** os três pedidos da sonda do P4 (11 Codex, 12 Grok, 13 Antigravity) continuam `running` na
  fila. **Estado:** de pé; o `/health` responde, e o `status` ao vivo já traz `runtime`, `model` e `effort`.
  **Como desfazer:** `brza mcp stop`.
