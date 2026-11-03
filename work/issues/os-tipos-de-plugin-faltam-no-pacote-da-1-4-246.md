---
status: open
description: O pacote da 1.4.246, no BrzA Studio e no Orca, não traz os .d.ts de resources/plugins/declarative, e o plugin create e o plugin types quebram com ENOENT; o plugin nasce sem tipos e o tsc não roda.
scope:
  - brza-studio
opened: 2026-11-03
tags:
  - tooling
---

# Os tipos de plugin faltam no pacote da 1.4.246

Achado no spike do C5 do [PLN-003](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md), em 2026-11-03.

## O que falhou

`brza plugin create spikes/c5-plugin --template worker-panel --json`, no BrzA Studio `1.4.246-alpha.1`, gravou o molde e
saiu com erro ao escrever os tipos:

```text
"code": "runtime_error",
"message": "ENOENT: no such file or directory, open '/Applications/BrzA Studio.app/Contents/Resources/app.asar.unpacked/resources/plugins/declarative/orca-components-layout.d.ts'"
```

O molde nasce com o `tsconfig.json` estendendo `./.orca/types/tsconfig.json`, que não existe. Sem ele, o
`npx tsc -p .` que a skill `orca-plugin-authoring` manda rodar não tem os tipos de `orca` e `orca/worker`. O `plugin dev
watch`, que segundo a skill também roda o `plugin types`, rodou no Orca em 2026-11-03 sem emitir erro e sem gravar
`.orca/types/`: a falha ali é silenciosa.

## A evidência

- **Os dois apps:** a pasta `Contents/Resources/app.asar.unpacked/resources/plugins/declarative/` tem só
  `orca-runtime.mjs`, `orca-test-hooks.mjs`, `orca-test-register.mjs` e `orca-testing.mjs`, no BrzA Studio e no Orca
  `1.4.246` (`ls`, 2026-11-03). Não é defeito só do fork.
- **No código, os arquivos existem:** `resources/plugins/declarative/orca-components*.d.ts` no `brza-studio`, e o
  `src/cli/plugin-authoring/plugin-type-files.ts:46` os lista entre os que o `plugin types` copia.
- **A `1.4.247` também não traz:** o Orca, atualizado em 2026-11-03, tem os mesmos quatro `.mjs` na pasta.
- **O transpile não depende deles:** o `plugin validate`, o `plugin check` e o `plugin test` passaram sem os tipos.

## O que fazer

Conferir se o empacotamento (`electron-builder`, `asarUnpack`) do upstream leva os `.d.ts`; a `1.4.247` não corrige. O
conserto vai ao fork e, como PR, ao upstream.
