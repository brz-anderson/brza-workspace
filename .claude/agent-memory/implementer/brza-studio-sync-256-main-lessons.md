---
name: brza-studio-sync-256-main-lessons
description: Lições do grupo src/main do sync v1.4.256 — fork-only em caminho velho, resíduo de pick do upstream, worker de cópia do Claude, helpers de script, zsh sem word-split
metadata:
  type: feedback
---

- **Upstream reorganizou `src/main` em subpastas** (acp/{journal,session,timeline,turns,options}, wire/{host,operations,providers,acquisition,…}, rpc/methods/structured-sessions/*). Arquivo do fork que não existia na base **fica no caminho velho com import velho**, sem conflito: o `tsc` temporário (`config/tsconfig.<x>tmp.json` com `extends ./tsconfig.node.json`, `composite:false`, include `../src/main`, `shared`, `preload`, `types`; ~30 s) acha tudo. Mova com `git mv` para a pasta irmã e corrija import por script de "stem único" (refaça: ~40 linhas de python, sobre `git ls-files --cached --others` **deduplicado**, pois `UU` lista 3 estágios e vira "ambíguo").
- **Não rode o corretor de import nos `UD` de outro grupo** (excluir com `git status --porcelain | grep ^UD`).
- **Resíduo de pick do upstream**: o fork trouxe PRs (`(#NNNN)`) que na 256 estão movidos; os arquivos ficam duplicados no caminho velho (status vazio). `git rm` quando a 256 tem o equivalente (comparar com `diff` do basename).
- **Feature do fork em arquivo de tipo gigante do upstream** (adapter type, no `max-lines`): o fork já extraía para `native-chat/brza/` e `acp/brza/`; mantenha a montagem de 1-5 linhas e extraia o resto (ex.: `brza-opening-message.ts`) quando o oxlint barrar.
- **Cópia/rewind do Claude virou worker** (`materializeClaudeConversationTranscript`); teste que a usa precisa de `import './claude-conversation-worker.test-fixture'` na primeira linha, senão `ERR_MODULE_NOT_FOUND` no worker.
- **O Bifurcar do fork e o `fork-boundary` do upstream convivem**; é ponto de rodada, não decisão.
- **zsh não divide `$T` com vários arquivos**: use `xargs` ou `bash -c`; senão o vitest roda só o filtro vazio.
- **Resolução por hunk**: script que troca o N-ésimo bloco `<<<<<<< ours…>>>>>>> theirs` por um arquivo de texto é o jeito mais rápido; `git diff -U0 :1:f :2:f` mostra só o que o fork mudou, e um verificador de "linha `+` do fork presente no resolvido" pega linha perdida.
