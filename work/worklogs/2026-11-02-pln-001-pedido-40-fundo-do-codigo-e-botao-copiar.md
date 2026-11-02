---
scope:
  - brza-studio
date: 2026-11-02
tags:
  - chat
---

# O P78 do PLN-001, o fundo do texto no bloco de código e o botão de copiar do visualizador de Markdown

O pedido 40, de Anderson, com a imagem do README no modo olho e o recorte do botão de copiar: "corrija o [recorte] e deixe
os blocos de código sem o fundo cinza atrás". Esta sessão leu o CSS do `brza-studio`, fez a rodada R66, abriu o pedido no
plano (R66, D61, P78, C31) e delegou a escrita a um `implementer`, num worktree. O commit e o push vieram depois do "faça
isso" de Anderson.

## A rodada

Respondida em 2026-11-02, por Anderson nesta sessão (`studio`), pelo AskUserQuestion:

- **R66.1, o que está errado no botão:** "O ícone aparece fora do hover". É leitura minha, a confirmar no C31, que o
  defeito é a posição: o CSS só mostra o botão no hover do `.code-block-wrapper`, e o que está fora do lugar é o botão.
- **R66.2, o que fica no bloco:** em texto livre, "eu quiz dizer o fundo da escrita, como se estivesse grifado, o bloco se
  mantém igual". O `pre` não muda; o fundo a tirar é o do texto dentro dele.
- **R66.3, onde:** "resposta anterior". Também leitura minha: o olho, que é o da imagem; o lápis só se o defeito existir
  lá, e não existe.

O pedido entrou como 40 porque outra sessão já tinha usado o 39 (R65, D57 a D60, P74 a P77) no mesmo dia.

## A causa e a correção

Duas causas, as duas no `markdown-preview.css`, lidas e confirmadas pelo `implementer` com teste que falhava antes:

- **O texto "grifado":** `.markdown-dark .markdown-body code` e `.markdown-light .markdown-body code` (0,2,1) vencem o
  `.markdown-body pre code { background: none }` (0,1,2), e o `code` dentro do `pre` fica com o fundo de código inline. A
  correção é `background: none` em `.markdown-dark .markdown-body pre code, .markdown-light .markdown-body pre code`.
- **O botão sobre a borda:** o grid do bloco anotado deixa a margem de `1em` do `pre` dentro do `.code-block-wrapper`, e o
  botão (`top: 8px`) cai 8 px acima do bloco. A margem passa ao wrapper e o `pre` fica com 0; o wrapper do diagrama fica
  de fora.

O editor rico não tem o defeito (`rich-markdown-editor.css:999` vence o `:930`) e não foi tocado.

## O que fechou

O P78 em `brza-studio@2738100d3f5`, na `master`, com o teste novo `markdown-preview-code-block.test.ts` (10 testes, 4 deles
falhavam sem a correção). Os testes do que foi tocado e o `pnpm check:changed --base=origin/master` passaram (24 de 24),
e o teste novo e o do wrapper mermaid passaram de novo sobre a base rebaseada (12). O worktree
`.worktrees/pln-001-pedido-40` e a branch `fix/pln-001-pedido-40` ficaram no `brza-studio`.

## O que ficou aberto

- **O C31**, num build, com Anderson: a posição do botão e o fundo do texto, nos dois temas. O happy-dom não tem layout, e
  a posição só se provou pelas margens.
- **A R66.1 e a R66.3** seguem como leitura da sessão até o C31. Se o botão aparecer sem o mouse em cima, a causa é outra
  e volta à rodada.
- O build instalado, o `v1.4.246-alpha.1`, não tem este commit.
- **A memória do `implementer`** (`brza-studio-css-tests.md`) trata de teste de CSS no `brza-studio`; vale só para este
  workstream, não é candidata à norma.

## Fora do workspace

- O `brza-studio` ganhou o commit `2738100d3f5` na `master`, com push para `brz-anderson/brza-studio`.
- O worktree `~/Projects/brza-studio/.worktrees/pln-001-pedido-40` foi criado e nele rodou o `pnpm install --offline`, e a
  branch `fix/pln-001-pedido-40` foi criada, depois de um `git worktree move` e um `git branch -m` a partir do nome
  `pedido-39`.
