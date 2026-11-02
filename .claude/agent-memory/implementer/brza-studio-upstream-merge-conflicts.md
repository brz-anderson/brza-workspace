---
name: brza-studio-upstream-merge-conflicts
description: Como resolver conflito de merge do upstream (stablyai/orca) no brza-studio com vários agentes no mesmo worktree — git add, imports movidos, max-lines, catálogo RPC, linhas do fork perdidas
metadata:
  type: feedback
---

Consolidado das quatro notas dos resolvedores do sync da v1.4.246 (2026-11-02), que caíram no scratch da sessão.

- **`git add` só por caminho exato.**
  - `git add src/main` marca como resolvido o `UU` de outro grupo que ainda tem marcador.
  - Desfaça com `git update-index --unresolve <arq>`.
  - Confira com `git grep --cached -lE '^<<<<<<< ours$'`.
- **Imports do arquivo movido.** O git não reescreve import quando o upstream move arquivo, por exemplo `shared/*` para
  `shared/native-chat/`, `shared/agent-session/{journal,view,lifecycle}` ou `main/claude/structured/journal/`.
  - Afeta o arquivo do fork que foi movido e o arquivo `brza/` que o importa.
  - O `tsc` mostra `TS2307`. Conserte pelo caminho novo.
- **Linha do fork perdida sem conflito.** O auto-merge pode devolver a versão do upstream fora do conflito. Foi o caso do
  "Hand-back from" no `NativeChatAgentMessageCard.tsx`. Depois de resolver, faça `git diff <commit do fork>` das
  features da área e confira que as linhas existem.
- **`max-lines`.**
  - O limite é 300 `.ts`, 400 `.tsx` e 800 teste, sem contar linha em branco nem comentário.
  - O arquivo do upstream muitas vezes já está no limite. A parte do fork sai para `brza/` ou para um vizinho, e fica uma
    linha de montagem no arquivo do upstream.
  - O `check-max-lines-ratchet` barra o `eslint-disable max-lines` novo: divida o arquivo.
- **Catálogo RPC.** Resolva o marcador com a união dos dois lados, depois rode `pnpm generate:rpc-params-catalog` e
  `pnpm verify:rpc-params-catalog`.
- **Teste do upstream apagado.** O upstream apaga teste "de baixo valor". Aceite, mas porte o caso que só existe pelo
  fork (identidade, porta, `brza`) para um teste em `brza/`.
- **Cópia nova da identidade do Orca.** Use as constantes do `src/shared/brand-identity.ts`. Exemplo: a
  `orca-protocol-registration.ts` da v1.4.246 registrava o `orca://` no Windows.
- **Comandos.**
  - Teste: `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts <arqs>`. Sem o `--config`, o alias
    `@/` não resolve.
  - `oxlint` e `oxfmt` estão em `node_modules/.bin`; passe a lista por `xargs`.
  - No macOS, `sed -i ''`.
  - O mobile não tem dependências instaladas e não roda aqui.
- **Testes do fork que o upstream envelhece.**
  - O `render` sai do `native-chat-tooltip-test-harness`.
  - O `setRendererUiLanguage` sumiu: use `i18n.changeLanguage(await loadRendererUiLanguage(x))`.
  - O `steerNewest` virou `steerHead`.
  - O hook que assina `s.settings` inteiro quebra "isolates mounted chats from unrelated settings": use `useShallow`.

Relacionadas: [[brza-studio-sync-test-failures]], [[brza-studio-lint-gates-after-sync]], [[brza-studio-rebrand-sweep]].
