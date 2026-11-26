---
name: brza-studio-sync-278-main-lessons
description: Lições do grupo src/main do sync v1.4.278 — pick do upstream vira theirs inteiro, P75 reaplicado sobre loja assíncrona, glob vazio no zsh roda a suíte toda, testes do fork que a 278 envelheceu
metadata:
  type: feedback
---
- **Arquivo cujo "ours" só tem picks `(#NNNN)` do upstream**: pegue `git show :3:f` inteiro (4 arquivos do antigravity). Confira com `git log c0eb..HEAD -- <dir>`.
- **P75 sobre loja que o upstream tornou assíncrona** (`inCredentialFileOrder`): resolva `theirs` em cada bloco e reaplique por sed: apagar `import { homedir }`, `ensureOrcaDir`->`ensureCredentialsDir`, `getOrcaDir()`->`getIntegrationCredentialsDir()`, remover a função `getOrcaDir`. Arquivos novos do upstream que importam `ensureOrcaDir` (linear-login-store) e lojas novas seladas em `~/.orca` (google-credential-store, bot-tool-credentials) também entram. Teste `integration-credentials-location.test.ts` precisa de `await` em tudo.
- **Esquema `orca://` fixo em arquivo novo** (deep-link-state.drainArguments): trocar por `BRAND_PROTOCOL_SCHEME` ao entregar a link a outra instância.
- **NUNCA `ls a b c 2>/dev/null` dentro de `$( )` no zsh**: um glob sem match aborta, a lista fica vazia e `vitest run` sem filtro roda a suíte inteira. Use `bash -c 'T=$(find ... -name "*.test.ts"); vitest run ... $T'` e confira `echo $T | wc -w` antes.
- **updater-setup.ts no limite de 300**: o import do `UpdateInstallTrigger` do upstream estoura em 1; extraia bloco para o módulo vizinho (`pinWindowsUpdateInstallDirectory`), pois oxfmt não deixa colapsar o import em uma linha.
- **Testes do fork que a 278 envelheceu**: `updater-test-main-window` apagado (inline no teste); `hasAgyCredential` virou `agyCredentialPresence` (`'present'`); upstream carimba `typedBy` (`agent`/`host`/`device`) em envio de pessoa; no P72 não carimbar.
