---
name: brza-studio-ratchet-fix-lessons
description: Como consertar os ratchets de translate e do React Compiler e rodar o gate de qualidade no brza-studio sem origin/main
metadata:
  type: project
---

- **`i18n:reactive-translate` ignora `--help` e roda no repo todo**: qualquer argumento dispara a varredura inteira e reescreve
  arquivos fora do alvo (tocou `use-external-automation-actions.ts`). Rode com o caminho e confira `git status`; reverta o que não é seu.
  O codemod deixa `const t = useTranslate()` mal indentado (oxfmt resolve) e não pega hook com `useCallback`/`useMemo` (fica manual, com `t` nas deps).
- **React Compiler**: `try/finally` sai para função de módulo recebendo `args` (`inFlight`, `setX`). Passar `ref` como argumento a
  função em render ainda dá "Cannot access refs during render"; a saída foi `useState(fábrica de módulo)` que cria o objeto `{current}`.
  Escrita de ref em render vira `useLayoutEffect`; `useMemo` lendo ref vira snapshot em `useState` com "ajuste durante o render".
- **`check-changed-code-quality.mjs` sem `origin/main`**: `ORCA_CODE_QUALITY_BASE=<sha> node config/scripts/preflight/changed-checks/check-changed-code-quality.mjs`
  roda o gate de verdade (cast em teste exige `// oxlint-disable-next-line typescript/consistent-type-assertions -- SAFETY: …`).
- **zsh**: glob sem match aborta o comando todo; use `bash -c` com `find`. `--prune` do ratchet limpa também linhas de arquivos do upstream.
- **AppImage contract**: o 2º argumento de `verifyStaticAppImagePackage` é o enum Arch do electron-builder (1 x64, 3 arm64).
