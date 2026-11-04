---
status: open
description: O /rename mandado pelo chat do app chega ao Grok como texto, e o nome da sessão não fica no runtime; o brza sessions --rename dá só a aba e o mapa.
scope:
  - brza-studio
  - brza-workflow
opened: 2026-11-04
priority: low
tags:
  - tooling
---

# O `/rename` pelo chat não chega ao Grok

## O pedido

É a sonda negativa do P8 do
[PLN-013: O Grok, o Codex e o Antigravity abrem pelo `brza sessions` e recebem tarefas do MCP](../../plans/PLN-013-grok-codex-e-agy-no-brza-sessions-e-no-mcp/PLN-013-plan.md),
pela R4.4/P6: "a issue só abre depois da sonda negativa".

## O que se sabe

- **O texto vai ao modelo.** `brza sessions send pln-013-sonda8-grok "/rename pln-013-sonda8-grok-nome"`, em 2026-11-04:
  o chat `grok_2e0d3ce3…` respondeu "O `/rename` chegou como texto neste chat. O runtime não executou o comando".
- **O disco confirma.** Em `~/.grok/sessions/<tools-kit>/01a1a534-c741-7cf2-a8ce-2b616f7dd735/summary.json`, o
  `generated_title` virou o auto-título "Chat /rename probe left Grok title unchanged", sem `title_is_manual`.
- **O método existe no agente.** O binário 1.0.70 tem `x.ai/session/rename`, e o app não o chama
  ([REV-010: O Desenho do PLN-013, revisado pela sessão Grok](../reviews/REV-010-pln-013-o-desenho-pelo-grok.md), A2).
- **O cwd da sessão é o do worktree**, e não o do scratch do app, ao contrário do que o REV-010/A1 supunha.

## O que falta

1. Fazer o app chamar o `x.ai/session/rename` no `agentSession.rename` do Grok, ou expandir o `/rename` no ACP, no
   `brza-studio`. Com isso, a linha `grok` do `NAMED` (PLN-013/D7) volta a valer.
