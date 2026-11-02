---
name: brza-studio-armadilhas-de-checagem
description: Armadilhas do pnpm check:changed no brza-studio que só aparecem com arquivo novo, texto de marca ou JSX removido (i18n, path-literal, ico)
metadata:
  type: project
---

Ao mexer em UI do `brza-studio` (worktree em `.worktrees/<branch>`, `pnpm install --frozen-lockfile` leva ~3 s):

- **Texto literal em JSX novo falha em "localization coverage".** Nome de marca ("BrzA") vai ao
  `config/localization-coverage-allowlist.json` com `reason`, uma entrada por `(filePath, kind, text, dynamic)`: o template
  literal e a string simples do mesmo `aria-label` são duas entradas (`dynamic` true e false), cada uma `count: 1`.
  Confira antes com `node config/scripts/audit-localization-coverage.mjs --json` e `--check`.
- **Remover um `translate('auto...<hash>')` deixa chave órfã** e falha "localization catalogs" e "extraction": apague a
  linha do hash nos 11 `src/renderer/src/i18n/locales/*.json` (uma linha cada, vírgula final) e rode
  `pnpm sync:localization-runtime-catalog`.
- **Arquivo novo ainda não commitado falha o `path-literal-ratchet`** se algum JSON/config o cita por caminho (a allowlist
  acima cita). Resolva com `git add -N <arquivos novos>`; o ratchet lê `git ls-files`.
- **`pnpm check:changed` sem `origin/main`:** `--base=master --maxWorkers=2`; o `unit tests` leva ~7 min com 58 arquivos
  mudados. `oxfmt --write` nos arquivos tocados antes (o `className` que encolhe vira uma linha).
- **`magick compare -metric AE` imprime `0 (0)`**, não `0`: compare o primeiro campo (`cut -d' ' -f1`).
- **O `.ico` do `trim-windows-icon-source.mjs` tem 6 quadros** (`ICO_FRAME_SIZES`, sem o 24); o que estava commitado tinha 7,
  de um pipeline antigo. A especificação do PLN-007 P4 manda "7"; não bate.
- **Comentários e mensagens do `brza-studio` são em inglês**, mesmo em script vindo de fonte em português.
