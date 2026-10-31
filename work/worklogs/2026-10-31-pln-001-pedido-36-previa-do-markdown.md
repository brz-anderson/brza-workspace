---
scope:
  - brza-studio
date: 2026-10-31
tags:
  - chat
---

# O pedido 36 do PLN-001, a prévia do Markdown e o expandir em todo bloco

Anderson fez dois pedidos na sessão `compact-guard`, do workstream `workspace`, e eles chegaram a esta sessão porque são
do app. O primeiro trata da tela cheia que o expandir de um bloco ` ```markdown ` abre: "deveria estar renderizado no
modo pré-visualização igual ao do editor". O segundo: "os de diff de código não está aparecendo o botão de expandir". Os
dois entraram no
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md)
como o pedido 36, com a R62, o D54, o P71 e o C24, sem código.

## A causa

O expandir não pertence ao bloco: é uma camada única, delegada pelo DOM, que só aparece quando o bloco rola
(`BrzaExpandLayer.tsx:11-26`, `brza-studio@046474ba49c`). O diff da linha de ferramenta nunca rola, porque tem
`overflow-hidden` (`NativeChatDiffView.tsx:9`). A cerca curta, de `diff` ou de `markdown`, também não rola. A tela
cheia clona o elemento e mostra o `innerText`, sem olhar a linguagem.

## As rodadas

- **R62.** O expandir aparece em todo bloco, role ou não. A cerca `markdown` ou `md` abre na prévia do olho do editor
  (`MarkdownPreviewBody`, com o tema do P60), com o `<>` para ver o cru. O frontmatter vai à caixa "Front Matter", e os
  links e as imagens relativos ficam sem ação. O P71 roda agora, num worktree.

## Próximo

O P71, na sessão `pln-001-pedido-36`, no worktree `.worktrees/pln-001-pedido-36` do `brza-studio`. Depois, o C24, no
build do C22, com Anderson.
