---
name: brza-studio-sync-263-renderer-lessons
description: Receita do sync v1.4.263 para conflitos UU do renderer — merge de 3 vias com base na tag anterior, feature do fork que o upstream moveu para contexto, imports quebrados em arquivos só do fork
metadata:
  type: feedback
---

- **Base melhor que a do merge:** o diff3 do git (base = `f8ffde…`) vem desalinhado. Use `git merge-file -p --diff3 ours.ts base.ts theirs.ts` com base = `git show v1.4.256:<caminho antigo>` (rebrand aplicado), ours = `:2:`, theirs = `:3:` com rebrand. Caminho antigo: `git diff -M -l30000 --name-status v1.4.256 v1.4.263 | awk '$1~/^R/{print $3"\t"$2}'`. 15 de 36 arquivos saíram sem conflito, o resto só nos pontos de enxerto do fork.
- **Fork enxertou em função que o upstream extraiu:** `git log --no-merges base..HEAD -- <arq>` vem vazio se o arquivo mudou de pasta; ache o commit por `git log -S'<símbolo>'`. Exemplos: `useTerminalAppTheme` foi para `use-app-theme-paint.ts`; blocos do preview de Markdown foram para `useMarkdownPreviewAnnotations()` (contexto) — porte o campo novo no retorno do hook e no consumidor.
- **Arquivos só do fork quebram por import** (nenhum grupo é dono): script de `/private/tmp/brza-sync-263/fix-imports-g3.py` (por stem único) resolve a maioria; ambíguos manuais: `@/lib/utils`→`@/lib/class-names`, `shared/constants`→`shared/orca-profiles/constants`, `@/lib/app-font-family`→`@/app-shell/appearance/app-font-family`. Reverta correção que mexa em comentário de arquivo do upstream; renomeado pelo git (`R`) com conteúdo do fork TEM import velho de verdade.
- **Teste do fork que o upstream envelhece:** `resetSystemPrefersDarkSubscriptionForTests` e `getBuiltinTheme` (use `getTheme` de `terminal-themes-data`) sumiram.
- **Não rode `oxfmt` em lista derivada de `git diff --name-only`:** ela traz arquivos de outros agentes. Monte a lista dos seus.
- **oxlint silencioso = limpo** (exit 0, sem saída). tsc: cópia sombra com `rsync -a --delete src/` + `git show :3:` nos arquivos com marcador de outros grupos; ~25 s.
