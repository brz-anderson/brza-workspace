---
name: coordinator-cost-dominates
description: Ao estimar o custo de um passo de reunião multiagente (contraprova, rodada extra), some o turno da coordenação, que pesa mais que as personas
metadata:
  type: feedback
---

Em reunião multiagente com personas, o custo de um passo extra não é o das sessões das personas: a coordenação que o
conduz pesa mais. Em 2026-11-07, a coordenação foi 57–62% do custo Claude; a contraprova da Carvão custou ~US$ 3,5 nas
personas e ~US$ 6,3 no turno da coordenação que a conduziu (~US$ 9,8 no total).

**Why:** o levantamento anterior ao desenho da skill de reunião (2026-11-08) estimou a contraprova em US$ 3,5, só pelas
personas; a conferência do turno `resume` da coordenação mostrou quase o triplo.

**How to apply:** ao pôr `Custo:` em opção que acrescenta passo a uma reunião, procure o turno da coordenação na mesma
janela no `measurements.jsonl` e some. Premissa a conferir quando houver medição por passo.
