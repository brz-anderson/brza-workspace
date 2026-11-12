---
name: brza-studio-sync-256-fix-lessons
description: Consertos pós-merge v1.4.256 (typecheck/lint/ratchets): max-lines por tipo em brza/, ratchet de fs síncrono, rig de teste sem ready, check:changed sem origin/main
metadata:
  type: project
---

- **max-lines por 1 linha**: mover o campo do fork para um tipo em `brza/` e compor `Tipo = BrzaCampo & {...}` troca 2 linhas (import+campo) por 1 (import). Rebrand que quebra linha: encurtar a frase ("BrzA's ...") até caber em 1 linha.
- **`check:main-sync-fs-ratchet`**: linha nova no `config/main-sync-fs-baseline.txt` em ordem alfabética; só `ad-hoc-signed-build.ts` (arquivo do fork) foi para o baseline, o resto vira `fs/promises`. Decoder síncrono + escrita: fire-and-forget com `Map<path, Promise>` e `flush...()` exportado para o `afterEach` do teste.
- **Rig de teste do upstream 256** (`openHostRig`) não tem `ready`; use `rig.frame('session/new')` + `rig.settle()` depois do attach.
- **`check-changed-code-quality.mjs`** pede base: rode `node config/scripts/preflight/changed-checks/check-changed-code-quality.mjs v1.4.256` (sem `origin/main` o `pnpm lint` falha nele por ambiente).
- **Teste de shiki/oniguruma no node** quebra no wasm: `vi.mock('../textmate-token-provider')` com `loadEditorCore` e `core.getLanguage`.
- **Leitura de imagem no main**: todas as leituras (`fs:readFile`, chunk, runtime preview) passam por `resolveLocalFileRequestPath` em `ipc/filesystem/access/local-file-access-resolution.ts`; é o ponto mais estreito para gancho de leitura (1 await). Escrita assíncrona de decoder síncrono: `failedWrites` Set + `awaitToolImageWrite` que lança erro explícito.
- **`--x: initial` no happy-dom** fica literal dentro de `color-mix(var(--x, fb))`; num navegador cai no fallback. No fork, defina o token derivado (`--chat-link`) concreto inline em vez de depender do fallback.
- zsh: `files=($(...))` e `for f in $files` falham/são barrados; use python para edição em lote. `sed -i ''` com texto com `/` ou `→` quebrou; use python.
