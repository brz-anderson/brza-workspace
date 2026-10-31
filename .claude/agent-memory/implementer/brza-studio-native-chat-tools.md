---
name: brza-studio-native-chat-tools
description: Armadilhas e comandos ao mexer em src/shared/native-chat/tools/brza do brza-studio (resolvedor de categoria, ícone e título MCP)
metadata:
  type: project
---

- **Formatador é o `oxfmt`**, não o prettier: `npx oxfmt --write <arquivos>`. Rodar o prettier no repo
  reformata do jeito errado; rode o oxfmt por último, antes do `check:changed`.
- **Teste de `src/shared` vai em `.test.ts`** e roda com
  `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts <arquivos>`; `src/shared/native-chat`
  inteiro leva ~2 s (81 arquivos), bom para varrer regressão.
- **Todos os chamadores do resolvedor** (`brzaToolCategory`, `nativeChatToolIconName`, o chip, o título, o
  `NativeChatToolLine.tsx` e o `MobileNativeChatToolLine.tsx`) já passam `call.input`; mudar o que o resolvedor lê
  do input não pede mexer no desktop nem no mobile.
- **`mcpToolIdentity` troca `_` e `-` por espaço no `tool`** (`get_screenshot` vira `get screenshot`), mas deixa
  camelCase (`executeRead`) intacto; ao casar nome de ferramenta, considere as duas formas.
- **`pnpm tc` e `cd mobile && pnpm typecheck`** saem com 0 e quase sem saída útil; confira com `echo $?`.
- **Shell zsh:** `--include=*.tsx` sem aspas dá "no matches found"; ponha entre aspas simples.
- `check:changed --base=origin/master` leva de ~2 a ~10 min, conforme a máquina está disputada; rode em background e espere a notificação.
- **Worktree novo do `brza-studio` não traz o `mobile/node_modules`**: `cd mobile && pnpm install --offline --frozen-lockfile`
  (~8 s) antes de rodar o vitest do mobile (`cd mobile && npx vitest run <arquivos>`); sem isso vem `Cannot find package
  'react-test-renderer'`. Em zsh, `echo ====` dá "=== not found"; use `echo '----'`.
- **Mobile: helpers de teste vão em `mobile/src/test-support/`** (alias do expo-crypto, `findAllByHostType`, e o
  `lucide-react-native-mock.ts`, que responde a qualquer ícone PascalCase com o próprio nome). O `tests-typecheck-baseline.txt`
  está vazio: todo teste e helper novo precisa passar no `pnpm typecheck:tests`. O oxlint (anti-slop) barra `Reflect.get`.
- **Testes do mobile que simulam ícone**: `String(node.type) === 'Bot'`; o ícone simulado é string com o nome, não componente.
