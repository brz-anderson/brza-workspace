---
name: brza-studio-sync-263-ud-lessons
description: UD do sync v1.4.263 — teste do fork vira .brza.test.ts restaurando o HEAD, imports velhos em movidos auto-mesclados, rename do upstream em cadeia, base != tag anterior
metadata:
  type: feedback
---

- **Receita rápida de teste do fork apagado pelo upstream:** `git show HEAD:<antigo> > <dir do código novo>/<nome>.brza.test.ts`, remapear os imports (script de 60 linhas: resolve cada `./`, `../`, `@/` pelo mapa de renames de `git log --name-status -M -l5000 base..tag`) e rodar. Se falhar, o motivo costuma ser (a) caso do upstream que mudou de comportamento (apague o caso, deixe só o do fork), (b) `vi.mock('@/hooks/…')` com caminho velho, (c) padrão novo do upstream (`DEFAULT_NATIVE_CHAT_FONT_SIZE` 14 -> 13).
- **Arquivo movido e auto-mesclado ("R" limpo) pode trazer o import do fork em profundidade velha**: o git aplica a linha do fork sem recalcular o relativo. Vale para `brand-identity`, imports novos do fork em `native-chat-appearance-settings.ts` e re-exports. Um scan de imports relativos que não resolvem acha todos; vitest acusa só o primeiro.
- **zsh não divide `$var` em `for p in "a b"`:** use `while read o n; do … done < arquivo`.
- **`git status --short -- <arq>` de arquivo UD pode virar `M ` se outra sessão o re-adicionar**; confira antes do `git rm`.
- **Mudança do recibo de sessão (`accountSwitch`) não cabe como linha de montagem**: o upstream trocou os recibos por `mutationReceipt({kind})` e o journal por SQLite com comandos no escritor. Ponto para rodada, não decida.
