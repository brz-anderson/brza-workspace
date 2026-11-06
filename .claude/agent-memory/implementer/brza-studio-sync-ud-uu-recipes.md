---
name: brza-studio-sync-ud-uu-recipes
description: Receita para UD/UU de teste no sync do upstream (v1.4.251) — achar o destino do arquivo movido, reaplicar o rebrand por bloco exato, armadilhas do git rm --cached
metadata:
  type: feedback
---

- **UD = movido OU apagado.** Siga o destino: `git log --diff-filter=D --format=%h -1 v1.4.251 -- <arq>` e `git show -M -l5000 --name-status --format= <commit>` (awk em `R`); repita se o destino foi apagado depois. O `git diff -M` base..tag inteiro não acha renomeação (8 mil), use por commit.
- **UU sem diff base..HEAD no mesmo caminho** = o git detectou renomeação; o caminho antigo vem de `awk $3==f` no `git diff --name-status -M -l20000 base tag`.
- **Reaplicar rebrand**: `git merge-file` (diff3) cria conflito onde o upstream apagou testes. Melhor: pegar `git show v1.4.251:<novo>` e trocar, por bloco contíguo exato dos `-` do `git diff -U0 base HEAD -- <velho>`, pelos `+`; bloco sem match = o upstream já apagou/mudou (ok). Script feito em /tmp, refaça (30 linhas de python).
- **Depois de mover**: o arquivo antigo fica no disco como untracked (`rm`); `git add` no novo.
- Feature do fork num teste apagado pelo upstream: porte um caso mínimo para `brza/` ou `<nome>.brza.test.ts` vizinho; teste do fork de build (`config/scripts`) restaure inteiro no caminho novo.
- Falha de import em teste do seu grupo costuma ser arquivo de outro grupo ainda quebrado (`../editor/raw-markdown-html`, `terminal-chat-theme.ts` com imports de `shared/` movidos): reporte, não conserte.
