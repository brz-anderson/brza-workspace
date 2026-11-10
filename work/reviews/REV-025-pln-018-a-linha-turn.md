---
status: done
description: Revisão da entrega do PLN-018, a linha turn do Grok e do Codex, contra o Pedido e a Cobertura, sem achado.
scope:
  - brza-workflow
opened: 2026-11-09
completed: 2026-11-09
tags:
  - tooling
---

# REV-025: A revisão da entrega do PLN-018, a linha turn

Revisão da entrega do
[PLN-018: O turno do Grok e do Codex entra no log, e a tarefa carimba o id dessa sessão](../../plans/PLN-018-o-grok-e-o-codex-na-medicao/PLN-018-plan.md),
de P1 a P4, contra o `## Pedido`, a Cobertura, a `## Regressão` e o Desenho (D1–D3).

**Quem revisou:** o subagente `reviewer`, que não executou o escritor. Devolveu sem achado. Esta sessão refez a
conferência no disco e a suíte abaixo, e gravou o parecer.

**O alvo:** `brza-workflow@5098439`.

## Achados

Nenhum.

## O que se conferiu sem achado

- O diff `7afed94..5098439` tem sete arquivos: `core/.claude/hooks/runtime_turn.py`, `tests/hooks/test_runtime_turn.py`,
  `bin/brza-note`, `packages/client/bin/brza-sessions`, `tests/cli/test_brza_note.py`, `tests/cli/test_brza_sessions.py`
  e `README.md`. Não há `.grok/hooks` nem `.codex/hooks.json`.
- O blob de `core/.claude/settings.hooks.json` é `8e6e579` no `5098439` e no pai `7afed94`.
- A linha do Grok sai de `read_grok_usage` (`runtime_turn.py:41-58`): `input` é `inputTokens` menos
  `cachedReadTokens`, e `estimated_cost_usd` é `costUsdTicks / 1e10`, sem arredondar. O objeto `session` não entra.
  Sem `session_id` no payload, sem arquivo, ou com `sessionId` diferente, nada é gravado (`runtime_turn.py:150-166`).
  `SubagentStop` e um `transcript_path` com o componente `subagents` também não gravam (`runtime_turn.py:99-103` e
  `159-160`).
- A linha do Codex usa o delta `usage` (`runtime_turn.py:198-216` e `233-234`). O custo é null. `guardian_review`
  não grava (`runtime_turn.py:191-195` e `226-227`). Sem `transcript_path` ou sem `session_id`, nada é gravado
  (`runtime_turn.py:218-222`).
- O carimbo lê `GROK_SESSION_ID` só na ausência de `CLAUDE_CODE_SESSION_ID` (`bin/brza-note:722-723`). O `--until`
  continua a exigir a sessão Claude (`bin/brza-note:730`).
- O `usage` do Grok chama `read_grok_usage` (`packages/client/bin/brza-sessions:818-841` e `898-899`). Sem id, sem
  script ou sem arquivo, sai `unmeasured`. O Antigravity permanece no ramo `unmeasured` (`brza-sessions:900-901`).
  O `usage` do Codex continua no último total do rollout (`brza-sessions:844-873`).
- O `README.md` do `brza-workflow` diz que o Grok lê o `usage.json` quando o arquivo existe (`README.md:152-154`).
- Nesta gravação, no checkout do `brza-workflow`:

  `python3 -m unittest tests.hooks.test_runtime_turn tests.cli.test_brza_note.TaskCommitTest tests.cli.test_brza_note.NoteEnvironmentIsolationTest` e os quatro `test_usage_grok_*` mais `test_usage_codex_ignores_info_null_and_returns_last_totals` → 51 passed.

## Onde o commit está

`5098439` está na `master` local, com pai `7afed94`. O `origin/master` está em `b2b497d` (o P8 do PLN-012), também
filho de `7afed94`. Os dois commits alteram `bin/brza-note` e `tests/cli/test_brza_note.py`. O push não foi feito.
Isso não é achado da linha: é o estado da publicação, e trava o fechamento do plano.
