---
name: brza-studio-sync-263-main-lessons
description: Lições do grupo src/main do sync v1.4.263 — tsc em cópia sombra, journal SQL novo (write/readers), mutação de store para P36, testes que o upstream envelheceu
metadata:
  type: feedback
---
- **tsc com marcadores de outros grupos**: cópia sombra (rsync + `git show :3:` nos arquivos com marcador) e `config/tsconfig.<x>tmp.json`. **Nunca `--exclude mobile` sem barra**: some `src/main/runtime/rpc/mobile/`; use `--exclude /mobile`. Apague o tsconfig temporário no fim.
- **Script que reescreve import por stem único** só nos arquivos `M`/sem status; ele toca arquivos `UD` de outro grupo (restaure com `git show :2:f > f`). O upstream renomeou helpers de teste para `*.test-fixture` / `*.test-support`: tente esses sufixos.
- **Journal 263 é SQL e assíncrono**: `journal.write({kind:'item'|'context-clear',...}, () => ({receipt}))`; leituras por `journal.reads.*` (`itemBody`, `queuedMessages.list()` são Promise); testes usam `readTestHostJournal(host, id)` / `readTestJournalItems(journal)` (de `journal-observation.test-support`), `openTestAgentSessionDatabase(dir)` async e `closeTestJournalHostDatabase(dir)`; `host.captureAgentStartDestination` é Promise; `conversationCommandBlocked` é async e a mutação exige `readWork:` (via `readHostStructuredAgentSessionWork`).
- **Recibo do store de operação do fork (P36)**: `conversationReceipts.X` agora é `transactions.mutationReceipt({kind})`; o fork acrescenta o kind `account-switch` (`runtime/agent-session/brza/brza-account-switch-mutation.ts`) com 4 ramos em `agent-session-store-mutation.ts`. Teste unitário sem host: `journal.write(item)` + `store.commitOperationReceipt(store.conversationReceipts.accountSwitch(...))`.
- **Feature do fork que o upstream passou a fazer igual** (modo de permissão ao vivo do ACP): o teste do fork passa contra a implementação do upstream; fica ponto de rodada, não decisão.
- **Updater**: o upstream apagou `updater-test-harness`; o teste P76 foi reescrito com mocks inline sobre `updater-service` (`vi.resetModules` + `import('./updater-service')`).
- **Teste que mocka `shared/app-environment`** quebra em silêncio (path vira o real): o módulo está em `shared/app-lifecycle/app-environment`.
