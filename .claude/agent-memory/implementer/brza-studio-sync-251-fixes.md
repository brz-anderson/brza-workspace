---
name: brza-studio-sync-251-fixes
description: Receitas dos consertos pós-merge do sync v1.4.251 (typecheck de testes do fork, remover feature do fork, padrão de setting)
metadata:
  type: project
---

- **Erro de import em teste esconde teste quebrado**: `describe`/tipo sem import faz o vitest ainda rodar, mas depois de consertar o tsc pode aparecer falha real (ex.: upstream passou a pôr sufixo de id `reviewer (child)` na linha de agente sem nome). Rode o vitest do arquivo depois de consertar o tipo.
- **Achar o lugar novo de um módulo movido**: `ls src/shared | grep nome` e `git grep -n "from '.*nome'" -- src | head -3` mostram o caminho novo (ex.: `shared/agent-launch/picker/`, `shared/agent-session/journal/`).
- **Remover feature do fork que o upstream substituiu**: `git rm` por caminho, `git show v1.4.251:<arq> > <arq>` para devolver o arquivo ao texto do upstream (sem `git checkout`), `pnpm -s run generate:rpc-params-catalog` regera o catálogo RPC, e `git grep -n usageLimitAutoResume tests mobile` acha fixtures e2e (`tests/e2e/cross-version-wire`).
- **Default de setting**: o store faz merge `{...defaults, ...salvo}`; mudar o padrão em `default-global-settings.ts` já vale para perfil sem a chave, sem migração. Teste no molde de `persistence-plugin-system-default-on.test.ts`.
- **macOS**: `sed -i 's/…/'` sem `''` falha ou deixa `arquivo-E`; use python para trocas.
- `pnpm -s typecheck` sai sem saída quando passa: confira o exit code (`>/tmp/x 2>&1; echo $?`; `PIPESTATUS` não vale no zsh).
- `structured-agent-session-queued-image-lifecycle.test.ts` falhou 2 casos no sync 251 sem relação com o que mexi; a linha de base não foi conferida.
