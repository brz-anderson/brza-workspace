---
name: brza-studio-cli-help-testes
description: Mexer no texto impresso do help do CLI do brza-studio quebra testes além dos que o plano lista; como rodar o CLI local sem instalar
metadata:
  type: project
---

- Qualquer troca na **impressão** do `printHelp` (`src/cli/help.ts`) quebra os testes que passam por `main(['x','--help'])` ou `printHelp`: no P6 foram 11 testes em 5 arquivos além do `skills.test.ts` (`handlers/computer.test.ts`, `handlers/file.test.ts`, `handlers/terminal-set-pane-title.test.ts`, `index-automation-run-output.test.ts`, `index.test.ts`). O plano dizia "sem mudança". Rode `pnpm test src/cli` inteiro (213 arquivos, ~30 s) logo após mexer, não só os três do prompt.
- O `check:changed --base=master` (19 checks, ~35 s) roda esses testes e é o que acusa; na base `master` o `src/cli` está 100% verde.
- Rodar o CLI sem instalar o app: `pnpm build:cli` no worktree (emite `out/cli`, ignorado pelo git; o `install-dev-cli` tenta `ln` em `/usr/local/bin` e falha com permission denied, sem efeito) e depois `./config/scripts/orca-dev.mjs --help`.
- Regex `(^|\s)orca\s` por linha não pega o cabeçalho `orca` sozinho na linha; no teste use `(^|\s)orca(\s|$)`.
- `sed -i` com `${...}` ou `\n` falha neste ambiente; edite com python ou Edit.
