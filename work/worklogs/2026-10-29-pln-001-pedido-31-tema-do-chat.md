---
scope:
  - brza-studio
date: 2026-10-29
tags:
  - chat
---

# O pedido 31 do PLN-001, o tema do chat no Markdown e no terminal

Anderson fez o pedido 31 do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md)
na sessão do `brza-workspace` que orquestrou o P54 ao P56: o fundo do visualizador de Markdown ficou escuro demais, e o
Markdown e o terminal devem seguir o tema e a tipografia do chat. Trocar o tema do chat troca os três; trocar o de um
dos outros troca só ele. Sem código nesta sessão.

## O que se fez

- **O levantamento.** Um subagente Sonnet leu o `brza-studio`, só leitura. O chat não tem tema próprio, e o "igualar ao
  terminal" leva a herança do terminal ao chat, ao contrário do pedido. Os fundos escuros hoje: o chat `#161616`, o
  olho `#0a0a0a`, o lápis `#1e1e1e`, o modo código `#191A1C` e o terminal `#282c34`. As fontes estão na R48 do plano.
- **As rodadas.** A R48 e a R49, pelo AskUserQuestion, com as respostas no plano.
  - O chat ganha um seletor de tema próprio, um par escuro e claro do catálogo do terminal. O padrão é o "Padrão do
    BrzA", que mantém o visual de hoje.
  - O Markdown e o terminal ganham cada um um interruptor "Seguir o chat". O Markdown desligado tem seletor próprio.
  - A tipografia do chat vale no olho e no lápis. O terminal e o modo código seguem só as cores e o fundo.
  - O "igualar ao terminal" sai, com migração.
- **O plano.** O pedido 31, a Cobertura, o D45 ao D47, o P58 ao P61 e o C15 ao C17. O estimado sobe 22,3 h, para
  146,8 h.
- **A execução.** Anderson pediu na mesma sessão: "e já execute os passos em paralelo". O P58 roda primeiro, porque
  os outros leem o resolvedor dele. Depois o P59 e o P60 rodam em paralelo, em worktrees do `brza-studio`. O P61 e os
  casos manuais ficam com Anderson.
