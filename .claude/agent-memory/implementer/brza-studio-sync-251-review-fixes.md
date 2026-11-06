---
name: brza-studio-sync-251-review-fixes
description: Receitas dos consertos pós-revisão do sync v1.4.251 (build, hashes gravados, bundles versionados, max-lines por helper)
metadata:
  type: project
---

- **Entrada de build movida pelo upstream**: confira `CLI_MAIN_ENTRY_NAMES` (`config/build-plugins/plain-node-entry-guard.ts`) e o `asarUnpack` do `electron-builder.config.cjs` contra `src/main/<nome>.ts`; `pnpm build:electron-vite` valida em segundos (a saída `out/` é ignorada). O teste que guarda isso mora em `config/scripts/build/brza/` (o vitest só inclui `config/scripts/**`, não `config/build-plugins/`).
- **Hash gravado de leitor lançado** (`*released-reader-record*.json`): o rebrand de frase de runtime muda o hash. Não troque os hashes; mapeie a frase de marca de volta no `normalize` do fixture. Ache a diferença exata rodando o teste no `.worktrees/base-v1.4.251` e no sync com um dump JSON temporário em `verify()` e comparando em Python (restaure o fixture e apague os dumps).
- **Bundle versionado alimentado por fonte** (`resources/plugins/declarative/*.mjs`): trocar texto de fonte exige `node config/scripts/plugin-build/declarative-runtime/build-plugin-declarative-runtime.mjs` (sem `--check`) e conferir os diffs por tokens; o teste de frescor é `build-plugin-declarative-runtime.test.mjs`.
- **Arquivo no limite do max-lines**: constante sozinha ainda estoura por 1 linha (import conta). Leve o bloco inteiro (checagem + mensagem) a um helper em `brza/`; para vários textos use um objeto único para um import só.
- **Teste que procura classe no `p`**: o upstream trocou texto puro por `NativeChatMarkdown`; a classe vai na `div.native-chat-markdown` e o `p` herda. Antes de "restaurar" estilo, dump do `innerHTML` (console.log some no vitest; grave em `/tmp`).
- **Vitest com lista em variável no zsh**: `${=B}`; sem isso roda 3 arquivos e parece verde.
- `ast-grep-gates` do lint tem 2 achados que vieram do merge (`integration-credentials-location.test.ts`, `brza-message-list.turn-indicator.test.tsx`) além dos da base; `process-host-dev-rebuild.test.ts` falha também na 251 pura.
