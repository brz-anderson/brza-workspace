---
status: open
description: O "Entrar" do chat fixado pelo P36 faz login na conta global, e a conta fixada removida deixa o chat quebrado sem caminho ao seletor.
scope:
  - brza-studio
opened: 2026-11-02
tags:
  - chat
  - auth
---

# O chat fixado numa conta pelo P36 entra na conta global

Achado da revisão adversária do merge da v1.4.246 do upstream, em 2026-11-02. O defeito já existia na `master` do
`brza-studio` antes do merge, em `abc5e78c243`. Anderson respondeu "Issue, fora do sync (Recomendado)", na rodada da
sessão do merge no mesmo dia. O sync está em
[O sync da v1.4.246 do upstream, que tirou o chat do experimental](../worklogs/2026-11-02-sync-da-v1-4-246-do-upstream.md).

## O defeito

**O chat trocado de conta pelo seletor do P36 fica fixado nela** (`record.accountSwitch`).

**Quando a conta fixada perde a sessão ou é removida**, a falha chega ao chat como `notSignedIn` ou
`claudeAccountFolderMissing`. O botão "Entrar" da falha faz login na conta **global**, e não na conta fixada:
- O `useNativeChatClaudeSignIn` usa `activeClaudeManagedAccountIdsByRuntime.host ?? activeClaudeManagedAccountId`
  (`src/renderer/src/components/native-chat/native-chat-claude-sign-in.ts:37-43`).
- O login dá certo, o botão some e o chat continua quebrado.
- O texto do `claudeAccountFolderMissing` manda "choose another account" (`en-runtime-required.json:1557`), mas nada
  na falha leva ao seletor do chat.
- Nenhum caminho limpa o pino quando a conta é removida. O `pinnedClaudeAccountHome` lança `claudeProfileMissing()` a
  cada lançamento.

## O que resolve

- **O "Entrar" do chat fixado** faz login na conta do pino.
- **A falha de conta removida** oferece o seletor do chat, ou limpa o pino e volta à conta global, com o divisor
  "Conta trocada".
- **Um teste para cada caminho.**
