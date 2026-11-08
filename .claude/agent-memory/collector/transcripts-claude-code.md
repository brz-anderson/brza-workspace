---
name: transcripts-claude-code
description: Onde ficam e como ler os transcripts JSONL das sessões do workstream playground; pegadinhas de timestamp e de mensagens injetadas
metadata:
  type: reference
---

- Transcripts: `~/.claude/projects/-Users-andepb-Projects-brza-workspace--worktrees-playground/<session>.jsonl`. Linha = JSON com `type`, `timestamp` (UTC, converter para BRT = -3h), `message.content`. Nem toda linha tem `timestamp` (use `.get`).
- Mensagens `type: user` que não são do Anderson: conteúdo de skill ("Base directory for this skill"), `[Image: …]` de leitura de PNG, `task-notification`, "Another Claude session sent a message" (hand-back de subagente). A de Anderson tem `promptSource`/`entrypoint: sdk-ts` e texto livre; o `AskUserQuestion` vem como `tool_use` e a resposta em `tool_result`.
- Uma sessão pode cruzar o dia: horários de 08/11 aparecem "menores" que os de 07/11; janele por data, não só HH:MM.
- Hipótese do pedido ("sessão fraca = longos silêncios") pode ser falsa: meça o intervalo antes de aceitar; no caso de 2026-11-07 o intervalo máximo foi ≤ 8 min nas duas, e a diferença estava no conteúdo dos blocos (persona como sujeito, síntese, painel visual).
- Scripts de extração reaproveitáveis ficam só no scratch da sessão; reescrever leva 5 min.
