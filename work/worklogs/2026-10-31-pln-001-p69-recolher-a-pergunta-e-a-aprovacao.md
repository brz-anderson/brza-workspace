---
scope:
  - brza-studio
date: 2026-10-31
tags:
  - chat
---

# O P69 do PLN-001, recolher a pergunta e a aprovação no chat estruturado

O pedido de Anderson, em 2026-10-31, na sessão `pln-001-pedido-34`: executar o P69 do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md),
o pedido 34, autorizado na R60.4. A evidência detalhada está no passo, no plano.

## O que se fez

Commit `brza-studio@a0eefa646e4`, pela sessão do `brza-studio` no worktree `.worktrees/pln-001-pedido-34`, com o push
direto na `master`.

- **Os testes primeiro.** Cinco testes novos ou ajustados falharam antes do código (5 failed, 98 passed, em 5
  arquivos). O do host, o `queue-if-active` atrás de pergunta pendente, passou já antes: ele fixa o que a R61 mediu, e o
  composer usável se apoia nisso.
- **O recolher.** O cartão de pergunta e o de aprovação do chat estruturado ganham a seta; recolhido, o cartão fica
  montado com `hidden` e `inert`, a `NativeChatPromptStrip` mostra o título, e o composer volta (R60.1, R60.2). O estado
  é por `itemId` e `revision`: prompt novo abre aberto. O cartão de aprovação mostra o X e a seta juntos.
- **O "Steer".** Com prompt pendente, o "Steer" do cartão da fila fica desabilitado e o Cmd+Enter com o composer vazio
  não o aciona, pelo `hasPendingPrompt` do hook da fila (R61.1).
- **O Esc e o foco (D52, "A conferir no passo").** Com o X e a seta, o Esc recolhe a aprovação, e o cancelar fica no
  X (X57). O foco vai ao composer ao recolher e volta ao cartão ao reabrir, como o D52 previa.
- **Onde ficou.** O cartão e a faixa saíram para o `NativeChatStructuredPromptCard.tsx`, porque a sessão passou do
  `max-lines`; o teste da sessão foi para um arquivo irmão, com os cartões reais (X58).
- **Os testes depois.** 112 arquivos, 1.138 passed; o `check:changed` ficou só com o vermelho de antes, o
  `external-subcommand.ts` nas fronteiras de import.

## O que ficou

O C22, num build, com Anderson, incluindo o segundo envio com o "enfileirar follow-ups" desligado (R61.2). O mobile segue
sem recolher no estruturado (R60.3).

## Fora do workspace

Nada.
