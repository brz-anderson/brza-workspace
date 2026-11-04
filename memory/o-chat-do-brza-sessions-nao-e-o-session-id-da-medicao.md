---
name: o-chat-do-brza-sessions-nao-e-o-session-id-da-medicao
description: "Para achar as linhas de uma sessão em .measurements, use o claude_session do `brza sessions list --json`, não o id do chat"
metadata:
  node_type: memory
  type: reference
  originSessionId: c98dbd4e-654b-4ee4-aa54-4969d868c402
  modified: 2026-11-04T02:09:15.115Z
---

O id `claude_<uuid>` que o `brza sessions list` mostra é o do chat do app, e não casa com o `session_id` do
`.measurements/measurements.jsonl`: trocar `_` por `-` não funciona. A ponte é o campo `claude_session` do `brza
sessions list --json`. Sessões com cwd fora do `brza-workspace` (no `brza-workflow` ou no `brza-studio`) podem não ter
linha nenhuma, se subiram sem o `--settings` do workspace; Antigravity e Codex nunca têm.

**Why:** a aferição das horas do PLN-008 (2026-11-03) perdeu uma rodada com o mapa errado.

**How to apply:** ao medir uma sessão por título, mapeie pelo `claude_session` e diga "sem medição" com o porquê para o
que não tiver linha.
