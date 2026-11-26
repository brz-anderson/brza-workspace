---
name: brza-studio-sync-278-ud-lessons
description: UD do sync v1.4.278 — upstream cortou a suíte e os fixtures, diff contra a tag anterior, restaurar .brza.test sem harness apagado
metadata:
  type: feedback
---

- **Diff do fork contra a tag do sync anterior, não contra a base:** `git diff v1.4.263 HEAD -- <arq>` mostra só o que o fork acrescentou; contra `c0eb69f752b` vem misturado com a 263 (antigravity e mailbox saíram "com delta" e não tinham nenhum).
- **O upstream apaga o teste E o fixture/mock dele** (`#46786` "cut the suite"): restaurar o teste do HEAD como `.brza.test.ts` costuma falhar por import de fixture sumido. Rode um scan de imports relativos (`python3` de 8 linhas) antes de rodar; fixture dá para restaurar como `<nome>.brza.test-fixture.ts`, harness de wasm (`oniguruma-test-harness`) não: tire o mock e os casos que dependem de realce.
- **Teste novo bloqueado por UU de outro grupo** (marcador em `NativeChatCodeBlock.tsx`, `native-chat-types.ts`): rode de novo no fim; o outro grupo costuma resolver enquanto você trabalha.
- **zsh não divide `$N` com lista de caminhos:** grave a lista em arquivo e use `while read f`.
- **CLI com texto ao usuário movida para arquivo novo** (`connectors/connector.ts` -> `bots/bot-reply.ts`): o arquivo novo vem sem rebrand; as strings visíveis ("Orca Cloud", "an Orca agent pane") precisam ser trocadas à mão.
