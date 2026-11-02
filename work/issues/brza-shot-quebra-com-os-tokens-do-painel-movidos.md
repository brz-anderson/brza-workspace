---
status: done
description: O brza shot procura os tokens do painel no caminho antigo, que o merge do upstream v1.4.246 moveu, e não gera mais o PNG.
scope:
  - workspace
opened: 2026-11-02
completed: 2026-11-02
tags:
  - tooling
---

# O brza shot quebra com os tokens do painel movidos no brza-studio

O `brza shot` lê dois arquivos do `brza-studio` por caminho fixo, em `scripts/brza/brza-shot:46-47`: o
`native-chat-visual-shell.ts` e o `src/shared/plugins/plugin-panel-shell.ts`, de onde tira o
`PANEL_DESIGN_TOKEN_ALLOWLIST` (`:178`). O merge do upstream v1.4.246 no `brza-studio` (`edc0373fcde`, "plugins: Plugin
Alpha", e o `a70f63b6a92` que fechou o sync) moveu o arquivo, e hoje a lista mora em
`src/shared/plugins/frames/plugin-panel-design-tokens.ts:5`, que o `native-chat-visual-shell.ts:1` importa.

Desde então, todo `brza shot` sai com "não li o shell dos visuais no brza-studio ([Errno 2] No such file or directory:
'…/src/shared/plugins/plugin-panel-shell.ts')" e não grava o PNG.

Achado em 2026-11-02, na sessão do `brand`, no Desenho do
[PLN-007: A marca BrzA tem símbolo, logotipo e derivadas a partir da chama do app](../../plans/PLN-007-a-identidade-visual-da-marca-brza/PLN-007-plan.md).
Uma cópia no scratch com `PANEL_SHELL = 'src/shared/plugins/frames/plugin-panel-design-tokens.ts'` gera o PNG igual,
pixel a pixel, ao de antes da quebra (`magick compare -metric AE` → `0`).

**O conserto** é trocar o caminho do `PANEL_SHELL` e, para a próxima mudança do upstream, achar o arquivo pelo import
do `native-chat-visual-shell.ts` em vez do caminho fixo. Mora no `scripts/brza/` da `master` ou no `brza-workflow`,
conforme o PLN-006 deixou o `brza shot`; não é do `brand`.

**Resolvida em 2026-11-02**, pela sessão `brza-shot-fix`, aberta a pedido de Anderson no worktree do `tools-kit`, na
conta `admin@fixfy.com.br`: `8d554e7` na `master` ("brza shot: acha a lista de tokens pelo import do shell dos
visuais"), que acha o arquivo da lista pelo import do `native-chat-visual-shell.ts`, com o teste novo que falhava antes
e os 98 `unittest` de `scripts/brza/tests/` passando, segundo o relato de Anderson. A sessão do `brand` conferiu o
commit na `origin/master` e rodou o `brza shot` oficial num artboard da R6 do PLN-007: o PNG saiu igual, pixel a pixel,
ao da cópia corrigida (`magick compare -metric AE` → `0`).
