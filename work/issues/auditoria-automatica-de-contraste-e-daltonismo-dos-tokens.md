---
status: open
description: Um portão automático confere contraste WCAG, ΔE2000 entre sinais nas três deficiências de cor e as oito cenas do chat em cinza, a cada mudança de token.
scope:
  - brza-studio
opened: 2026-11-07
priority: high
tags:
  - design
---

# A auditoria automática de contraste e daltonismo dos tokens

Levantado na [Reunião Carvão em Brasa: a coordenação e a proposta de plano](../worklogs/2026-11-07-reuniao-carvao-em-brasa-coordenacao.md), como os portões 1 e 2 do plano proposto. Toda a reunião dependeu de contas refeitas à mão;
o Cinza deixou um script que mede 182 pares e 20 comparações de sinais
(`.sessions/reuniao-brasa/entregas/cinza-audit-tokens.py`, fora do git, no worktree do `playground`).

## O pedido

- **Portão 1:** a auditoria dos pares efetivos (com os fundos compostos: hover, transparências, caixa do código em
  linha, fundos do diff), nos dois temas: texto ≥ 4,5:1, ícone e indicador ≥ 3:1, e ΔE2000 ≥ 15 entre erro, aviso,
  ação e link em deuteranopia, protanopia e tritanopia — **como triagem**, não como garantia de percepção.
- **Portão 2:** as oito cenas do chat renderizadas com `grayscale(1)`, com critério verificável de forma e texto para
  cada par de estados (repouso e foco, CTA e erro, aviso e informação), mais revisão humana. Ideia do Cinza (piloto sem
  cor), levada a portão permanente pelo Tição.
- Promover o script do Cinza a teste do `brza-studio`, conferindo o APCA contra o pacote oficial.

## O que a reunião levantou

Cinco de seis a favor dos portões. Cinza votou contra a redação da v1 — "ΔE é triagem, não garantia" — e a redação foi
corrigida. Fogareiro deu 99 de confiança; Lenha pede medir o custo de manter o CI antes de prometê-lo "para sempre".

Fontes: [Reunião Carvão em Brasa: a participação de Cinza, o Cético Analítico](../worklogs/2026-11-07-reuniao-carvao-em-brasa-cinza.md), [Reunião Carvão em Brasa: a participação de Tição, o Guardião](../worklogs/2026-11-07-reuniao-carvao-em-brasa-ticao.md), [Reunião Carvão em Brasa: a participação de Lenha, a Engenheira Pragmática](../worklogs/2026-11-07-reuniao-carvao-em-brasa-lenha.md).
