---
name: anderson-criterios-continue-outra-conta
description: Critério de Anderson no "Continue in another account" com tarefa de fundo (2026-11-26) — o host completa a intenção sozinho, sem matar trabalho nem só avisar
metadata:
  type: feedback
---

Em 2026-11-26, no defeito do "Continue in another account" com tarefa de fundo retendo o agente na conta esgotada,
Anderson escolheu "Trocar e continuar quando a tarefa acabar — o botão troca a conta e o host continua sozinho depois
que a tarefa termina". Recusou: avisar e não continuar; mover o chat fixando-o; forçar a troca matando a tarefa.

**Why:** ele quer que o clique da pessoa vire o resultado pedido sem um segundo clique e sem perder o trabalho em
curso. Paga complexidade no host para isso, mas não aceita mudar o modo do chat (fixar) como efeito colateral.

**How to apply:** em fluxo que esbarra em trabalho em andamento, ofereça como opção forte o "adiar e completar
sozinho", com cancelamento explícito. "Avisar e parar" e "matar o trabalho" vão como alternativas de custo baixo,
não como recomendação. Não reabra as três recusadas sem fato novo. Ligado a [[anderson-criterios-pln-011]], que
prefere não mexer no wire do host e manter versões misturadas: o desenho seguinte (H1) usou método novo com
capacidade e fallback ao caminho antigo.
