---
name: reference-studio-fork-quality-audit-tricks
description: Atalhos e armadilhas para auditar o fork brza-studio contra o upstream v1.4.246 (testes, lint, catálogos de idioma, supressões) sem rodar a suíte inteira
metadata:
  type: reference
---

Levantamento de qualidade do fork (2026-11-02, HEAD 384d4b08fd6 × v1.4.246). O que poupa tempo na próxima vez:

- **Comparar por arquivo esconde falha por teste.** `test-final.failed` ⊂ `test-upstream.failed` dá "tudo igual", mas
  `packaged-cli-assets.test.ts` falha no fork num teste que passa na pura. Compare por `FAIL |proj| arquivo > teste` nos
  `.log` de `/private/tmp/brza-sync/` (script de parsing é curto: split em ` FAIL  |`).
- **Rodar teste exige `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts <arquivo>`**; o
  `npx vitest` cru dá "No test files found" (projetos `bun`/`node-runtime` só existem pelo run-vitest). `bun` não está instalado.
- **Árvore pura sem mexer no repo:** `git archive v1.4.246 | tar -x` + `cp -cR` do `node_modules` do worktree de sync.
  Os symlinks do pnpm são relativos e contam 4 níveis abaixo de `~`: o destino tem de ser `~/Projects/<a>/<b>/<raiz>`
  (o link curto do scratch quebra). Copiar também `src/packages/process-host/{dist,node_modules}`. `git init` + commit
  dentro dela para os scripts que usam `git ls-files`/`rev-parse`. Harness `cross-version-wire` não funciona nela (sem tag/história). Apague depois.
- **O worktree `sync-v1.4.246` fica atrás do HEAD da master** (a70f63b6a92 × 384d4b08fd6): arquivos novos da master não
  existem lá; para o HEAD, faça `git archive` do commit.
- **zsh:** `git show $r:path` com `$r` quebra (`:p` vira modificador); use `${r}:path`.
- **Catálogos desktop:** `src/renderer/src/i18n/locales/{en,de,es,fr,ja,ko,pt,ru,tr,zh,zh-Hant}.json`, JSON aninhado; chaves
  `_many` em pt/es/fr são plural válido, não órfã. `node config/scripts/verify-localization-catalogs.mjs` roda sem bun.
  A varredura de "Orca" tem de ser sem diferenciar caixa: o rebrand trocou só `\bOrca\b` e deixou `ORCA` em ko.json.
- **Supressões:** contar com `git grep -hoE` nas duas árvores e varrer `git diff -U0`; no fork a contagem é idêntica à pura.
- **Fonte velha:** a lista "3 passos de lint vermelhos" do worklog do sync é de a70f63b6a92; no HEAD só o
  `lint:ast-grep-gates` está vermelho (commit a3a89e3aaf5 corrigiu os outros dois).
