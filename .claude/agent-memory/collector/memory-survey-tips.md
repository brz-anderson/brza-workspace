---
name: memory-survey-tips
description: Atalhos e armadilhas para levantar memórias de outros workstreams por git show e conferir se subiram à norma (2026-11-08)
metadata:
  type: reference
---

- Dump de todas as memórias de um ws: `for f in $(git ls-tree -r --name-only workstream/<ws> -- memory .claude/agent-memory); do echo "##### $f"; git show workstream/<ws>:$f; done > dump.txt`, depois Read em fatias de ~330 linhas (84 KB para studio+brand). Norma da master: mesmo laço com `git show master:<arq>` num arquivo só e `grep -ciE` por palavra-chave.
- O `AGENTS.md` do `~/Projects/brza-studio` é o do upstream (autores Neil/Brennan): editar gera conflito no sync; a norma do fork ainda não tem lugar lá.
- Caminhos do brza-studio mudam a cada sync (v1.4.251): `run-vitest.mjs` hoje em `config/scripts/test-runtime/execution-policy/`, `ci-unit-files.mjs` em `config/scripts/ci/unit-selection/dependency-graph/`, `MarkdownPreviewBody` em `editor/markdown-preview/render-tree/`, `orca-dev.mjs` sumiu. Memórias de studio/brand citam os velhos: use `git ls-files | grep` antes de afirmar.
- `.claude/agents/implementer.md` da master manda "suíte inteira do que tocou"; memória do studio manda o contrário em sessões paralelas.
