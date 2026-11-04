---
name: anderson-criterios-pln-011
description: O que pesou nas escolhas de Anderson nas rodadas R1–R6 do PLN-011 e as recomendações que ele recusou (escopo, wire do host, versões misturadas)
metadata:
  type: feedback
---

Nas R4 a R6 do PLN-011 (2026-11-03), Anderson aceitou toda opção recomendada; o que as unia: não mudar o contrato do
wire do host (R5.4), manter a compatibilidade com host mais velho mesmo pagando um RPC a mais por envio (R6.3, pela
`AGENTS.md:61` do `brza-studio`), e porte do upstream em commit separado antes da extensão (R5.2).

As recusas vieram na R3: recomendei recorte só da coordenação, destino num plano só e o restante na issue de origem; ele
quis "a issue inteira, por fases", "um plano pra cada workstream" e "issues próprias, repriorize individualmente".

**Why:** ele prefere ver o escopo inteiro fatiado em fases com prioridade própria a cortar escopo; e paga custo agora
para não divergir do upstream nem quebrar versões misturadas.

**How to apply:** ao recomendar corte de escopo, ofereça a versão em fases com issue por frente como opção forte; ao
pesar mudança no host, prefira deduzir no cliente. Fato novo que contradiz premissa de rodada (como o `pending` comum
da CLI local no PLN-011, R8.1) vai como ponto de rodada com o fato, não como desvio silencioso.
