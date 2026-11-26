---
name: brza-studio-sync-278-shared-cli-lessons
description: Sync v1.4.278 em shared/cli/config/mobile e locale - HEAD==tag anterior, bloco vazio do theirs, rebrand de locale com Hangul, verify:localization-catalogs
metadata:
  type: project
---

- **`git diff <tag-anterior> HEAD --stat -- arq`**: vazio = o fork não mexeu, pegue `git show <tag-nova>:arq`; sem isso se perde tempo lendo blocos enormes (e2e.yml tinha 266 linhas de bloco).
- **Bloco com `theirs` vazio** (upstream tirou a função do arquivo): ache o arquivo novo (`structured-agent-session-item-blocks.ts`) e porte para lá as linhas do fork que estavam na função; depois apague o import que ficou sem uso no arquivo antigo.
- **README do fork** é próprio (pt-BR, 44 linhas): em conflito, `ours` nos dois blocos.
- **Rebrand de locale com `rebrand_locales.py`**: o `WORD` dele (`(?![\w-])`) não casa `Orca가` (Hangul é `\w`) e deixa `Orca-Version` (de) com espaço errado. Use `(?<![A-Za-z0-9_./:-])Orca(?![A-Za-z0-9_])` e, em alemão, `Orca-` -> `BrzA-Studio-` antes. Script reutilizável: `/private/tmp/brza-sync-263/g278/g3/loc.py` (lê `locale-conflicts.md`, valida que o disco == "deles", `apply` grava).
- **Disco do locale depois do merge_locales = valor cru do "deles"**, não o do fork, apesar do texto do pedido; confira com um assert antes de gravar.
- **`verify:localization-catalogs` falha no meio do sync** por fonte do renderer sem rebrand (chave reusada com texto diferente) e `en-runtime-required.json` defasado; não é culpa dos JSON de idioma. `sync:localization-runtime-catalog` no fim.
- **Chamador novo de função do upstream**: parâmetro opcional no fim (`from?`) mantém os chamadores do upstream compilando; passe o valor só onde o fork precisa.
