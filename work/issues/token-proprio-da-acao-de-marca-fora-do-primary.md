---
status: open
description: A ação de marca ganha o token `--action-brand`, fora do `--primary` que a segunda camada de tema reescreve, com rótulo escuro e uma brasa por região.
scope:
  - brza-studio
opened: 2026-11-07
priority: high
tags:
  - design
---

# A ação de marca tem token próprio, fora do `--primary`

Levantado na [Reunião Carvão em Brasa: a coordenação e a proposta de plano](../worklogs/2026-11-07-reuniao-carvao-em-brasa-coordenacao.md). A Brasa Incandescente `#FF3D00` vira a cor da ação principal, mas não pode morar no
`--primary`: no ramo de catálogo, `src/renderer/src/lib/native-chat-theme-surface-style.ts:38-39` define
`--primary = var(--chat-foreground-strong)`, aplicado inline pela raiz do chat
(`NativeChatStructuredSession.tsx:276-277`). Pintar o `--primary` de laranja "incendeia o catálogo" (Faísca); mudar
só o CSS não vence a declaração inline (Lenha).

## O pedido

- Expor `--color-action-brand` e `--color-action-brand-foreground` no `@theme inline` de `main.css:99-103`, com
  `#FF3D00` e `#1A1B1E`, sob a flag `brand.brasa`.
- Variante `brand` em `ui/button.tsx`, sem trocar o `default`; Allow e Submit, que são `<button>` próprios, compartilham
  a receita.
- Usar só no Enviar com conteúdo, no Continue, no Allow e no Submit.
- **Uma brasa sólida por região** (cabeçalho, transcript, composer; o cartão de aprovação conta como região, pela
  Faísca), conferida renderizando as oito cenas — o lint confere o uso do token, não a cota.
- **Rótulo sempre `#1A1B1E`:** branco sobre a 07 dá 3,55:1. O APCA do rótulo dá Lc 40,9: peso ≥ 600 e conferência no
  render.
- Desligar a regra de `main.css:1199-1210`, que força o degradê e o branco no Enviar em foco.

## O que a reunião levantou

Seis de seis a favor (índice 76,6). Derruba a proposta mostrar que a segunda camada reescreve também o
`--action-brand`.

Fontes: [Reunião Carvão em Brasa: a participação de Faísca, a Provocadora](../worklogs/2026-11-07-reuniao-carvao-em-brasa-faisca.md), [Reunião Carvão em Brasa: a participação de Lenha, a Engenheira Pragmática](../worklogs/2026-11-07-reuniao-carvao-em-brasa-lenha.md), [Reunião Carvão em Brasa: a participação de Tição, o Guardião](../worklogs/2026-11-07-reuniao-carvao-em-brasa-ticao.md).
