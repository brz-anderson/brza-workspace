---
name: brza-studio-css-tests
description: Como testar CSS do renderer do brza-studio (cascata no happy-dom) e travas do check:changed para testes novos
metadata:
  type: project
---

- **happy-dom resolve a cascata real, com especificidade**: injete o `.css` num `<style>` e leia `getComputedStyle`.
  Reproduz bug de seletor que perde para outro. Não tem layout, então posição se testa pelas margens/propriedades.
- **`import.meta.url` quebra no `// @vitest-environment happy-dom`** (`URL must be a non-empty "file:" path`): leia o
  CSS por caminho relativo à raiz do repo (`readFileSync('src/renderer/src/assets/x.css')`).
- **`check:changed` barra `as` em teste novo** (`consistent-type-assertions`): use um helper
  `querySelector<HTMLElement>` que lança se nulo. `as const` passa.
- **Pedido de CSS do Markdown**: `markdown-preview.css` (tema `.markdown-dark/.markdown-light .markdown-body`) e o editor
  rico (`rich-markdown-editor.css`) são folhas separadas; o rico já tem `pre code` com especificidade maior.
