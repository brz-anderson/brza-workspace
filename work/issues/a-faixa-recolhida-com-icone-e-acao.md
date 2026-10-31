---
status: open
scope:
  - brza-studio
opened: 2026-10-31
tags:
  - chat
  - design
---

# A faixa recolhida da pergunta e da aprovação com ícone e ação

Anderson escolheu, em 2026-10-31, na rodada de teste dos artboards do chat (sessão do workstream `workspace`), a
alternativa **C — Ícone e ação** para a faixa recolhida do chat estruturado, e pediu: "C e já coloque na fila pra
implementar". A rodada está em
[Os artboards na rodada de desenho de interface](../worklogs/2026-10-31-artboards-na-rodada-de-desenho.md),
na seção "O teste no chat".

## O que existe

A faixa é o `NativeChatPromptStrip` (`src/renderer/src/components/native-chat/NativeChatPromptCollapse.tsx:50-70`,
criada no `a0eefa646e4`): o título truncado da primeira pergunta ou da aprovação e o `NativeChatPromptCollapseToggle`
com a seta para cima, sem rótulo. Quem monta a faixa é o `NativeChatStructuredPromptCard`
(`NativeChatStructuredPromptCard.tsx`), que já sabe o tipo pelo `prompt.body.kind`.

## O que muda

- **À esquerda, a barra de 3 px** na cor `--primary` e o ícone do tipo, também em `--primary`: `CircleHelp` para a
  pergunta e `Shield` para a aprovação, do `lucide-react`.
- **À direita, um botão com texto e a seta**: "Responder" na pergunta, "Revisar" na aprovação, com `translate` e as
  chaves novas em `components.native-chat.prompt.*`. O botão abre o cartão, como a seta faz hoje.
- **O título** continua truncado e ocupa o que sobra.
- **O toggle compartilhado não muda**: o `NativeChatPromptCollapseToggle` também é a seta do cartão aberto. Por isso a
  faixa ganha o próprio botão, ou o toggle ganha uma variante com rótulo, e a seta do cartão aberto fica como está.
- **O `NativeChatPromptStrip` recebe o tipo**, `kind: 'question' | 'approval'`, além do `title`.

## A conferir na implementação

- **O `--primary` do tema padrão é neutro** (`#171717` no claro e `#e5e5e5` no escuro, em `main.css:214` e `:326`).
  Por isso a barra e o ícone saem pretos ou brancos, e não coloridos. O PNG do teste mostra isso. Se a faixa precisar de
  cor, a escolha do token vira pergunta antes de implementar.
- **O título perde uns 110 px** para o ícone e o botão. Na largura do chat, 46rem, ainda cabe bem mais que no artboard
  do teste, que punha os dois casos lado a lado.
- **Os testes** do `NativeChatStructuredSession.prompt-collapse.test.tsx` passam a conferir o rótulo do botão e o ícone
  de cada tipo.
