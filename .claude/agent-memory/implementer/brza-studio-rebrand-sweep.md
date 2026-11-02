---
name: brza-studio-rebrand-sweep
description: Como varrer "Orca" -> "BrzA Studio" depois de um merge do upstream no brza-studio, e as armadilhas que quebraram testes e geradores
metadata:
  type: project
---

- **Varrer só as linhas que o upstream adicionou** (`git diff -U0 <base> <tag>`, linhas `+` com `Orca` fora de
  comentário) e trocar por correspondência exata de linha no arquivo atual; tem ~900 linhas em ~420 arquivos por release.
  A troca cega por regex em tudo derruba coisa que parece prosa.
- **Revisar o que a troca automática estraga**: (1) `type Orca = {` / `orca: Orca` em teste (checar sintaxe com
  `oxc-parser` `parseSync` em todos os arquivos tocados; o `typescript` do node_modules não carrega por `require`);
  (2) string só com `'Orca'` em fixture (nome de processo `comm`, pasta do userData, UA) — reverter; (3) `Orca-Test-B`
  em allowlist de distro; (4) fixtures do preâmbulo (`You are working inside Orca`) em testes que checam ausência;
  (5) "an Orca" -> "a BrzA Studio".
- **Fontes de bundles/guias gerados ficam Orca**, senão o lint e testes de frescor falham:
  `node config/scripts/generate-plugin-authoring-skill-references.mjs --check`, `generate-bundled-skill-guides.mjs --check`
  e `config/scripts/build-plugin-declarative-runtime.test.mjs`. Afetam `src/cli/specs/plugin*.ts`,
  `src/shared/plugins/{events,images,contributions,manifest/plugin-manifest.ts,workers/plugin-host-api*,declarative}`.
  Procedimento: aplicar por arquivo e rodar o `--check` (0,4 s) para decidir manter ou reverter.
- **Rodar teste com `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts <arq>`**, não com o
  `node_modules/.bin/vitest` direto: o direto não põe `ORCA_BACKGROUND_LAUNCH=1` e dá dezenas de falhas falsas
  (browser-manager-*, claude-provider-session-rename).
- **Locale**: o `rebrand_locales.py` não pega substantivo composto alemão (`Orca-Server`, `Orca-Version`) nem
  partícula coreana/japonesa colada (`Orcaが`, `Orca를`), por causa do `(?![\w-])`; varrer depois com
  `(?<![A-Za-z0-9_./:-])Orca(?![A-Za-z0-9_-])` nos valores.
- **Goldens de snapshot** (`__goldens__/*.txt`) e fixtures JSON gravadas (`src/cli/runtime/fixtures/`) carregam texto
  da fonte: atualizar junto.
- **Max-lines do oxlint**: "BrzA Studio" é mais longo e o oxfmt quebra a linha; arquivo no limite de 300 estoura
  (`wsl-move-copy.ts`). Resolveu com `/* eslint-disable max-lines -- Why: ... */`.
- **Baseline que não é do rebrand**: `verify-localization-catalogs` (de.json, `en-runtime-required` com
  `resumeInNewChat.*`, `protected-copy-keys.json`), updater (url `stablyai` vs `brz-anderson`), `bun` ausente,
  `.cross-version-checkouts`, `packaged-cli-assets` (`/var` vs `/private/var`), path-budget do daemon (234 > 230:
  "BrzA Studio" é 7 chars maior que "Orca" na raiz do LOCALAPPDATA).
- Suíte inteira leva ~17 min; os testes criam `tests/e2e/.cross-version-checkouts` (ignorado pelo git).
