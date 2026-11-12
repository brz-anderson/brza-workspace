---
name: brza-studio-sync-256-fork-fix-lessons
description: Remover feature do fork duplicada do upstream (Bifurcar) e portar o pino de conta ao Fork do upstream - restaurar da tag, onde o pino mora
metadata:
  type: project
---

- Para remover feature do fork que o upstream passou a ter, restaure os arquivos compartilhados da tag com `git show v<tag>:<caminho> > <caminho>` (ex.: `claude-rewind-fork.ts`, `claude-rewind-transcript.ts` voltam ao upstream puro) e `git rm` os exclusivos; depois `git grep` de cada símbolo.
- O contexto `NativeChatForkContext` do fork e o do upstream tinham o mesmo nome em módulos diferentes; ao tirar o do fork, a prop `messageId` de `NativeChatAgentControls` e do `NativeChatAssistantMessageRow` ficou sem uso e também saiu.
- Pino de conta no Fork do upstream: `prepareStructuredAgentSessionFork` (`acquisition/structured-agent-session-fork.ts`) monta o `AttachParams`; `accountSwitch` (accountId+account) do `record` de origem passa por `brza/brza-fork-account-pin.ts`. `reserveRequestFor` já grava no record filho; o launch lê `record.accountSwitch` em `session-tabs/structured-session-account-home.ts`. Fork não precisa do divider (o histórico copiado já o traz). Nada muda no renderer.
- Teste do fork: `forkTestSource(rig, 'claude')` devolve `record` mutável; `test.prepare()` devolve os params.
- `pnpm typecheck` leva ~10 s aqui (tsrs) e serve como validação final.
- Falhas de linha de base fora do escopo neste sync: `claude-provider-session-rename.test.ts`, `wsl-host-deployment-store.test.ts`, `structured-agent-session-precommit-refusal.test.ts` (rebrand).
