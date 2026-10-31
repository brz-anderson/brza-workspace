---
name: reference-brza-norma-acoplamento-atalhos
description: Onde moram os acoplamentos do brza-workspace (caminho/nome/pessoa) em scripts, hooks e ~/.zshrc, e os greps que poupam leitura num levantamento de genérico/local
metadata:
  type: reference
---

Confirmado em 2026-10-31 para o PLN-006 (confira que os caminhos ainda existem).

**Atalhos**
- `git ls-tree -r --name-only master` dá 61 arquivos de norma; a master **não versiona** `wiki/` nem as subpastas de `work/` (só os dois `README.md` e `plans/README.md`). O `.gitkeep` de `wiki/guides` só existe no worktree.
- Um grep único cobre quase tudo: `BrzA|brza-studio|brza-workspace|Anderson|brz-anderson|noreply|personal|~/Projects|Application Support|~/orca|Orca|Fixfy|tools-kit|2026-`; não inclua `workspace` solto (infla com falso positivo).
- Os acoplamentos de código se resumem a quatro focos: `scripts/brza/brza_runtime.py:19-24`, `claude-brza:40-71`, `.claude/hooks/measure.py:76-90,589-598` e as 10 linhas de hook do `settings.json` (`${BRZA_WORKSPACE:-$CLAUDE_PROJECT_DIR}`). `compact_guard.py` herda tudo do `measure` (`:34,72`).
- `brza-sessions:144-154` é o único script que já deduz a raiz do workspace pelo git common dir do cwd, em vez de constante.
- Tabela de "o que reconhece só os dois repositórios": `~/.zshrc:57-61,80` (`brza_where`, `for label in workspace studio`) e `claude-brza:61-71` (`repo_of`).
- Doc de memória do Claude Code (https://code.claude.com/docs/en/memory): `@import` em `CLAUDE.md` (4 saltos), `CLAUDE.local.md` gitignorado; `AGENTS.md` + `CLAUDE.md` juntos carrega só o `CLAUDE.md`. Salvo a página inteira no tool-results; use `grep -n` nele em vez de reler (53 KB).

**Fontes que envelhecem / armadilhas**
- O `README.md` do brza-workspace e o `~/.zshrc` estão alinhados (offset de 4 linhas); o do PLN-011 (Fixfy) não estava, ver [[reference-fixfy-pln-011-onde-mora]].
- `resume_guard.py` + `test_resume_guard.py` seguem versionados, mas fora do `settings.json` (órfãos): não conte como hook ativo.
- `~/.local/bin/brza-*` são symlinks para o checkout principal do brza-workspace (13 links); um workspace segundo compartilha esses scripts.
- Contagem de linhas do plano (~250 locais / ~40 arquivos) vem do plano; o grep acima dá números maiores se incluir testes.
