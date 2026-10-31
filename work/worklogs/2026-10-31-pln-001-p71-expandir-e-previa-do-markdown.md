---
scope:
  - brza-studio
date: 2026-10-31
tags:
  - chat
  - design
---

# O P71 do PLN-001, o expandir em todo bloco e a prévia do Markdown

O pedido de Anderson, em 2026-10-31, na sessão `pln-001-pedido-36`: executar o P71 do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md),
o pedido 36, autorizado na R62.4 ("Agora, num worktree (Recomendado)"), pelo D54 e pela R62.1 a R62.3 ("Olho e <>",
"Em todo bloco", "Caixa e relativos inertes").

## O que se fez

Commit `brza-studio@abc5e78c243`, nesta sessão, no worktree `.worktrees/pln-001-pedido-36`, com o push direto na
`master`.

- **Os testes primeiro.** O `BrzaExpandLayer.test.tsx` passou a pedir o botão na cerca curta e nos dois diffs, a cerca
  `markdown` e a `md` na prévia com o "Front Matter" à parte, o `<>` com o cru e a quebra, o link relativo sem
  navegar, o copiar com o cru nos dois modos e a outra linguagem sem o seletor. Antes do código: 10 failed.
- **O expandir em todo bloco.** O `brzaExpandTarget` não exige mais que o bloco role, e o `brzaBlockScrolls` saiu.
- **A prévia.** O `brza-markdown-fence.ts` lê a linguagem do bloco; a tela cheia monta o `EditorViewToggle` do editor e
  o `BrzaMarkdownExpandPreview`, com o `MarkdownPreviewBody` do olho e o tema do `useMarkdownSurfaceTheme`. A caixa
  "Front Matter" saiu do `MarkdownPreviewSurface.tsx` para um componente que os dois usam (X63).
- **Os pontos a conferir do D54.** Uma fixture local, fora do commit, mostrou o botão sobre a primeira linha da cerca
  sem linguagem; sem cabeçalho, ele passou à borda de cima do bloco, sem cobrir texto (X61). O frontmatter sai do
  corpo e entra na caixa; o link relativo não navega. No happy-dom, o `innerText` juntava a primeira quebra da cerca, e
  a cerca Markdown passou ao `textContent` sem a quebra final, o mesmo do copiar do bloco (X62).
- **Os testes depois.** 37 arquivos, 245 passed; o `check:changed` com 21 de 21 verdes.

## O link `file:`

O D54 diz que o link absoluto segue como no olho do editor. Na prévia, só o `http(s)` abre; o `file:` absoluto e a
imagem `file:` ficam sem ação, porque abri-los pede o roteamento pelo worktree que a R62.3 deixou de fora (X64). Se o
`file:` precisar abrir, vai a Anderson como rodada.

## O que ficou

O C24, no build do C22, com Anderson.

## Fora do workspace

Nada.
