---
name: brza-studio-sync-256-rebrand-lessons
description: Rebrand de código e catálogos no sync 256 - substituição só com aspas, gates de localização, chaves reusadas, listar todos os drifts
metadata:
  type: feedback
---

- **Troca de fallback inline só com a string entre aspas** (`'s'`, `"s"`, `` `s` ``): substring solta atinge guias gerados, texto de agente e comentários (strings curtas como "Orca CLI"). Fiz e desfiz uma vez (`git show HEAD:f > f`).
- **Listar todos os drifts do extraction**: o verificador mostra só 20; copiar o `verify-localization-extraction.mjs` para o mesmo diretório com `slice(0, 5000)`, rodar e apagar. Depois do en.json rebrandado, a diferença é só `Orca` na fonte.
- **Chave que o upstream tirou do catálogo mas um arquivo do fork usa** (`...QuickLaunchButton.465e432ef1`): restaure o valor de todos os idiomas a partir do blob da base (`git show <base>:locales/x.json`), não troque o texto.
- **Chaves órfãs**: apagar de todos os locales, rodar `pnpm -s sync:localization-runtime-catalog`; `verify:localization-catalogs` precisa de `bun` e acusa a mesma chave com textos diferentes entre arquivos (corrija o outro arquivo).
- **Varredura de código**: pegar linhas `+` do diff base..tag que ainda existem no HEAD; poupar orchestration, plugins, guias, `src/main/claude/` (tema), console.*, comentários, fixtures.
- zsh: `--include=*.ts` sem aspas falha; use `'*.ts'`.
