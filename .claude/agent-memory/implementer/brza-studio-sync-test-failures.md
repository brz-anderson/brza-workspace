---
name: brza-studio-sync-test-failures
description: Como triar teste que falha só no merge do upstream do brza-studio (linha de base, tipos de causa e o que já se achou na v1.4.246)
metadata:
  type: project
---

- **Linha de base primeiro**: `git worktree add --detach .worktrees/fork-pre-sync <master>` +
  `pnpm install --frozen-lockfile` (o `--offline` falhou por falta de metadados; sem ele leva ~7 s). Rode os testes lá.
  Na v1.4.246, 3 dos 4 grupos já falhavam na master (updater, verify-dev-channel); só o tema do terminal era do merge.
- **Teste do upstream com URL/repo do Orca** (`stablyai/orca`, `orca-hourly`): o fork usa `brz-anderson/brza-studio` e
  `brza-studio-*`; troque a URL no teste. Atenção às asserções `not.toContainEqual`, que passam vazias com a URL velha.
  `config/scripts/verify-dev-channel-packaging.mjs` (roda no workflow win-build) também carregava `orca-*`: o
  verificador e o teste mudam juntos.
- **Merge perdeu o `terminalColorOverrides` no terminal que segue o chat** (D46: overrides valem por cima): o upstream
  moveu os overrides para `resolveTerminalPalette` (por slot, `terminalColorOverridesLight`), e o ramo do chat em
  `src/shared/terminal-chat-theme.ts` ficou sem eles. Slot = o do modo do app (`theme`), não o `scheme` do chat.
  Quem escreve teste do merge afirmando "deixa os overrides de fora" está racionalizando a perda.
- `pnpm tc` leva ~6 s com cache; o grupo `src/renderer/src/{components,lib,runtime,app-shell}` + `src/main/ipc/pty` leva
  >2 min: rode em background.
