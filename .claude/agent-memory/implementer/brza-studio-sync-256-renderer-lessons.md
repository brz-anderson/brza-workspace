---
name: brza-studio-sync-256-renderer-lessons
description: Receita do sync v1.4.256 para o grupo renderer — resolver trechos de rebrand por script, typecheck com cópia sombra, testes do fork que o upstream envelhece
metadata:
  type: feedback
---

- **Trecho "manual" que na verdade é rebrand + reflow:** compare `ours` com `base` removendo espaço e vírgula (`[\s,]`) depois de aplicar o rebrand na base; igual -> resolução = `theirs` com o mesmo rebrand (regex `(?<![\w./:-])Orca(?![\w-])`, "an Orca", `github.com/stablyai/orca`). Cobre ~70% dos hunks; o resto é feature do fork. Se `ours` só difere de `theirs` por `translate(` vs `t(`, vale o mesmo.
- **Arquivo em que o fork só enxertou poucas linhas e o upstream reestruturou** (`GeneralEditorSettingsSection`, `TerminalThemeSections`, `CliSection`, `use-monaco-theme`): pegue `git show :3:<arq>`, aplique o rebrand e reenxerte as linhas do fork (`git diff base ours` filtrando Orca/BrzA). O diff3 desses hunks vem desalinhado.
- **AA (add/add) em arquivo que o fork trouxe do 251:** `:3:` com rebrand; confira com `diff :2: rb(:3:)`.
- **Typecheck com marcadores em outros grupos:** o `tsc` 7 (nativo) não tem API JS e não faz semântico com TS1185 no programa. Faça cópia sombra (`cp -R src config resources`, `ln -s node_modules`), troque cada arquivo com marcador por `git show :3:` (ou `:2:`), rode `tsc --noEmit -p config/tsconfig.web.json --composite false` lá e filtre pelos seus caminhos. Copie as edições para lá antes de repetir.
- **Arquivos do fork sem conflito que quebram por movimento do upstream** (import de `use-system-prefers-dark`, `plugin-themes`, `islands-dark-theme` relativo): ninguém é dono; o grupo de tema/renderer corrige.
- **Testes do fork que chamam o componente como função com `react` mockado:** `useTranslate` passou a chamar `useContext`; mocke `@/i18n/use-translate` devolvendo `translate`. Hook que lê `window.api.ui` (`use-window-active`) precisa de mock no teste do `use-document-appearance`.
- **Vitest direto:** `node_modules/.bin/vitest run --config config/vitest.config.ts` roda; `config/scripts/run-vitest.mjs` não existe na 256. Passar diretório grande passa de 120 s: filtre por arquivo ou rode em segundo plano.
- Mapa que o upstream trouxe: `@/store/plugin-themes` -> `@/store/plugins/appearance/plugin-themes`; `@/store/code-editor-theme` -> `@/store/appearance/code-editor-theme`; `terminal-pane/use-system-prefers-dark` -> `@/hooks/theme/use-system-prefers-dark`; `contrastRatio/over` -> `shared/color/rgba-contrast`.
