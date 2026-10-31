---
scope:
  - brza-studio
date: 2026-10-31
tags:
  - chat
  - design
---

# O P70 do PLN-001, a faixa recolhida com ícone e ação

O pedido da sessão do workstream `workspace`, no chat do BrzA Studio, em 2026-10-31: implementar a issue
[A faixa recolhida da pergunta e da aprovação com ícone e ação](../issues/a-faixa-recolhida-com-icone-e-acao.md), a
alternativa C que Anderson escolheu na rodada de teste dos artboards ("C e já coloque na fila pra implementar"; depois,
"siga"). Entrou no
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md)
como o pedido 35, com o D53, o P70 e o C23.

## O que se fez

Commit `brza-studio@4eaac80df53`, nesta sessão, no worktree `.worktrees/pln-001-pedido-35`, com o push direto na `master`.

- **Os testes primeiro.** O teste do recolher do chat estruturado passou a conferir o tipo da faixa, o ícone e o botão
  "Answer" ou "Review"; o do chat do terminal, o mesmo botão. Antes do código: 4 failed, 7 passed.
- **A faixa.** A `NativeChatPromptStrip` recebe o `kind`: a borda esquerda de 3 px e o ícone do tipo, `CircleHelp` ou
  `Shield`, em `--primary`; à direita, o botão "Responder" ou "Revisar" com a seta, que reabre o cartão. A seta do
  cartão aberto não mudou. As chaves `components.native-chat.prompt.answer` e `.review` entraram nos sete locales.
- **O chat do terminal muda junto (X59).** A faixa é a mesma nos dois chats, e o do terminal já sabia o tipo.
- **O `check:changed` pediu dois ajustes.** O botão ficou no `ghost`, sem cor própria, pela regra `shadcn(no-restyle)`;
  e a espera de 100 ms do teste do P69 virou `vi.waitFor` no foco do composer, pelo `flaky-test-pattern-ratchet` (X60).
- **Os testes depois.** 33 arquivos, 269 passed; o `check:changed` ficou só com o vermelho de antes, os 2 casos do
  `open-uncommitted-entry.test.ts`.

## A cor

O `--primary` do tema padrão é neutro, e a barra e o ícone saem pretos no claro e brancos no escuro, como no PNG da
issue. Implementado assim, como o pedido mandou. Ver no app pede um build com um prompt pendente; a conferência é o
C23, no build do C22, e, se a falta de cor incomodar, a escolha do token vai a Anderson como rodada.

## O que ficou

O C23, no build do C22, com Anderson.

## Fora do workspace

Nada.
