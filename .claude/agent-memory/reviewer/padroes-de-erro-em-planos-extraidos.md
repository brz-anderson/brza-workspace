---
name: padroes-de-erro-em-planos-extraidos
description: Onde o defeito costuma se esconder num plano extraído de outro (PLN-009 de PLN-003) e no Desenho escrito por sessão de outro runtime — itens que caem entre os planos, limiares sem rodada, achados medidos não absorvidos
metadata:
  type: project
---

Padrões que apareceram na revisão do Desenho do PLN-009 (2026-11-03), extraído do PLN-003:

- **O que cai entre os dois planos.** Quando um plano novo "fica dono" dos passos de outro (P6–P9 → PLN-009), confira
  item a item da matriz (`M…`) e das rodadas que os passos que saem executavam (`Executa D5 (M8, M13, M14)`) contra o
  plano novo. No PLN-009 sumiram M6, M7, M13, M14 e R6.4; a issue de passagem também não os listava.
- **Limiar e porta sem rodada.** Números concretos (RAM > 4 GB, CPU > 90%, confiança 0,75, porta 4242, US$ 0,01)
  entram no Desenho com uma linha "Origem" que cita rodadas que não têm número. Conferir a rodada inteira, inclusive o
  texto da opção recomendada.
- **Achado medido que não chega ao Desenho.** Worklog e `[x]` dizendo "ajustes registrados nos D3–D7" sem o diff ter
  mudado os D. Conferir com `git diff`/`git show` do Desenho, não pelo que o worklog afirma.
- **Vocabulário de papel trocado.** `implementer` (subagente por papel do `AGENTS.md`) usado no lugar de `executor`
  (a sessão-worker da R5.2) no ramo do gate: papel desconhecido fica sem regra.
- **Afirmação sobre ferramenta do `brza-workflow`** ("o `brza install` liga o pacote novo") — conferir no código do
  `bin/brza-install`; ele só liga `bin/` e `packages/client/bin/`.

**Why:** foram os achados de maior gravidade, e todos se acham por comando em minutos.
**How to apply:** em revisão de plano extraído ou de Desenho vindo de outra sessão, rodar esses cinco cheques antes da
leitura fina. Ver também [[estado-muda-durante-a-revisao]] e [[achados-que-costumam-cair]].
