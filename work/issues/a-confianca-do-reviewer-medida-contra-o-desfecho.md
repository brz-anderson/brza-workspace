---
status: open
scope:
  - workspace
opened: 2026-10-31
trigger: O --facts passa de 100 fatos com desfecho, ou de duas semanas de medição, sem que a confiança do reviewer seja medida.
tags:
  - tooling
---

# A confiança dos achados do reviewer se mede contra o desfecho deles

O `reviewer` dá a cada achado uma confiança de 0 a 100, com corte em 80 (`.claude/agents/reviewer.md`), e o destino de
cada achado sai de uma rodada com Anderson. Ninguém compara as duas coisas: um achado de 90 que a rodada derruba como
`→ falso` não volta como dado para a régua.

O [PLN-005: A confiança dos fatos do desenho se mede contra o que se sustentou](../../plans/PLN-005-a-confianca-dos-fatos-do-desenho/PLN-005-plan.md)
deixou o `reviewer` fora de escopo para medir primeiro o `designer` e o `collector`, com a marca nos papéis, o
`fact_audit.py`, o `scripts/fact_outcome.py` e o `summarize_measurements.py --facts`. Quando o gatilho disparar, a
pergunta da rodada é se o achado entra no mesmo mecanismo — uma marca no achado e o destino da rodada como desfecho —
ou se o parecer de `work/reviews/` já basta como fonte, lido por um script.
