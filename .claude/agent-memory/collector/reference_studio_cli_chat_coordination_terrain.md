---
name: studio-cli-chat-coordination-terrain
description: Onde moram cursor do histórico, fila, lista de chats e o PR #33115 (orca chat list/read/send) no brza-studio; truques de simulação sem tocar a árvore
metadata:
  type: reference
---

- Cursor `{epoch,sequence}` e resets: `src/main/native-chat/agent-session-journal/journal-cursor.ts`, `.../agent-session-wire/agent-session-history-page.ts`; tipos em `src/shared/agent-session/agent-session-wire.ts:75`.
- Resultado do send não diz o motivo da retenção da fila; o motivo (`prompt`) só existe em `structuredQueueHold` (host) — o cliente vê `queuedMessages`/`nextQueuedMessageId` na página/frames.
- `src/cli` não tem nenhum chamador de `agentSession.*` na master; `worktree.ps` lista chats com paneKey `structured-agent-session-<id>`.
- Simular PR sem worktree: `GIT_INDEX_FILE=/private/tmp/x/idx git read-tree master && git apply --cached --3way pr.diff` (não toca índice real). Sem `--3way` falha por drift de texto.
- Simular cherry-pick: `git merge-tree --write-tree --name-only --merge-base <sha>^1 master <sha>`; `git show <tree>:arq` lê os marcadores.
- `gh pr view --json body` de PR do Kelvin devolve corpo enorme: use `--jq` cortando.
- `git merge-tree master upstream/main` completo: 256 conflitos (2026-11-03), a maioria rebrand.
- Specs da CLI mantêm "orca ..." nas usage (rebrand não toca), então o porte do #33115 não exige rebrand dos nomes.
