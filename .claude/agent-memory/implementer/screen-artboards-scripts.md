---
name: screen-artboards-scripts
description: scripts da skill screen-artboards (PLN-021 P7) — mapa, decisões não escritas, armadilhas do tokens.py e do PNG, comandos que validam
metadata:
  type: project
---

**Valida (2026-11-10):** `python3 -I -m unittest discover -s ".claude/skills/screen-artboards/scripts/tests"` (48 OK, brza shot trocado
por atribuição em `artboard.gera_png`). `tokens.py check brza-studio` contra o disco real; apague os `__pycache__`.

- O `main.css` do brza-studio tem `--destructive` num 2º bloco `:root,\n.native-chat-appearance[...]` (e no `.dark,`): o
  `bloco_css` varre os blocos de topo e junta os que têm o seletor numa lista por vírgula (o último vence). Só o `:root {` não basta.
- `var(--color-blue-N)` do Tailwind v4 vira hex por uma tabela em `tokens.TAILWIND`; cor nova do app que use outra escala não resolve e é descartada.
- `check`: hash mudou mas nenhum token mudou sai 0 (nota), não 4; o main.css muda toda semana.
- O artboard guarda a meta em `<meta name="sa-art">` (frame, larguras, esquemas, outer); `shot` e `promote` recortam a variante
  escondendo as outras `.sa-cell` por CSS, sem reconstruir. Largura do PNG = moldura externa + 2*12 (o iPhone é 415+24, não 393+24).
- `python3 -I` não põe a pasta do script no `sys.path`: `artboard.py` faz `sys.path.insert(0, AQUI)` antes de `import _kit, tokens`.
- `rm -rf $D/*.html` com variável é barrado pelo hook de segurança: use pasta de saída nova (`v2`, `v3`) em vez de apagar.
