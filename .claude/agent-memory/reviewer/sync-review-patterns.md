---
name: sync-review-patterns
description: Onde os erros se escondem na revisão de merge do upstream (stablyai/orca) no brza-studio, e o método que achou cada um
metadata:
  type: project
---

Padrões que se repetiram na revisão do merge da v1.4.246 (2026-11-02):

- **Cópia paralela de constante de identidade.** O valor mora no `src/shared/brand-identity.ts` e também,
  à mão, no `config/nsis/orca-installer-hooks.nsh` (raiz do `%LOCALAPPDATA%`, filtro do PowerShell, `RMDir`).
  A varredura troca uma cópia e esquece a outra. Confira toda ocorrência literal do valor antigo, não só o
  consumidor do import.
- **Slug de repositório na resolução de conflito.** `stablyai/orca` virou `brz-anderson/orca` (repo que não
  existe) no `orca-star.ts`. Confira com `gh api repos/<slug>`; o fork é `brz-anderson/brza-studio`.
- **Pino por chat (P36) contra a seleção global.** O código do upstream lê a conta global em lugares que o
  pino não alcança: o login da linha de falha (`native-chat-claude-sign-in.ts`), o `canSwitchAccount` da
  recuperação e o seletor do limite (`NativeChatUsageLimitActions`). Procure `activeClaudeManagedAccountId` e
  `router.accountSelectionHomes` em caminho de chat que pode estar fixado.

- **Feature nova do upstream que cria chat a partir de outro** (o fork por mensagem da v1.4.246): o chat
  novo nasce sem `accountSwitch`, segue a seleção global e perde o pino do P36. Confira todo
  `resumeFrom`/adoção: o registro adotado não leva `resumeCursor`, e o lançamento em outra conta cai em
  sessão nova vazia, sem erro. Um teste temporário com o fixture do
  `claude-structured-launch-account-routing.test.ts` prova em 1 s.
- **Estado compartilhado em `~/.orca` × Keychain renomeado.** Os `.enc` de integração (Jira, Linear,
  Bitbucket, chaves de API) são selados pelo `safeStorage`; com `BrzA Studio Safe Storage`, o BrzA não lê
  o que o Orca selou, e reconectar sobrescreve o do Orca. Confira `ls ~/.orca` e as datas `cdat` dos itens
  (`security find-generic-password -s ...` sem `-w`).

- **Caminho de arquivo em config que o typecheck não vê** (sync da 251, 2026-11-06). O upstream
  reorganiza pastas a cada versão; o conserto do fork que mora em config não acompanha e nada
  reclama: `CLI_MAIN_ENTRY_NAMES` (`config/build-plugins/plain-node-entry-guard.ts`), que vira
  `input` do Rollup via `src/main/<nome>.ts`; o `asarUnpack` do electron-builder; os scripts próprios
  em `config/scripts/*.mjs` (`build-win-local`). Typecheck, lint e vitest passam e o `pnpm build`
  quebra. Rode um script que confira cada nome contra o `git ls-tree HEAD` e cada import relativo
  dos `.mjs/.cjs` de config, HEAD contra a tag pura.
- **O upstream apaga o teste-inventário que guardava um conserto do fork** ("remove low-value
  tests"): a linha do fork vai junto e o conserto fica sem guarda. Ao ver um conserto antigo do
  fork em arquivo de config, procure o teste dele no HEAD.

**Método que rendeu:** listar as linhas que o fork somou (`git diff -U0 <base do último sync> <master do
fork> -- src`) e que não existem em lugar nenhum da árvore atual. Quase tudo é refatoração ou texto
reescrito; o resto aponta o que caiu. Depois, `git diff v1.4.246 -- <arquivo>` nas junções.

**Cuidados:**
- Outra sessão edita o worktree do sync durante a revisão. Antes de reportar, releia o índice
  (`git show :<caminho>`) e o `git status`; um achado (overrides de cor sobre o tema do chat, D46) caiu
  porque foi corrigido no meio da revisão.
- No zsh, `git show "$r:config/..."` vira `$r:c` (modificador); use `"${r}:caminho"`.
- `src/main/claude/claude-provider-session-rename.test.ts` falha (spyOn em ESM) e é idêntico ao upstream:
  não é achado do fork.
- Rode vitest com `--config config/vitest.config.ts`; sem ela, falhas espúrias de PATH.

Related: [[reviewer-confidence-calibration]]
