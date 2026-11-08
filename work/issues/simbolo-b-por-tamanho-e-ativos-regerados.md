---
status: open
description: O símbolo vira a B (núcleo incandescente) com núcleo de rescaldo `#FFB088` e sem halo abaixo de 128 px, porque a B chapada na 07 perde para a de hoje a 16 px, e os ativos saem regerados do gerador.
scope:
  - brza-studio
opened: 2026-11-07
priority: medium
tags:
  - design
---

# O símbolo B por tamanho e os ativos regerados

Levantado na [Reunião Carvão em Brasa: a coordenação e a proposta de plano](../worklogs/2026-11-07-reuniao-carvao-em-brasa-coordenacao.md). Dos três tratamentos (A brasa acesa, B núcleo incandescente, C carvão em brasa), a sala
votou a B por 4 a 2 (índice 55,0): é a que muda a cor sem mexer na silhueta nem no tile que liga as quatro filhas. Em
16 px, os três viram a mesma mancha.

## O pedido

A especificação do Tição, lida em `resources/brand/README.md`, `resources/icon-source/generate.sh:33-53` e
`src/main/tray/system-tray.ts:1-93`:

| Tamanho | Chama | Halo |
| :------ | :---- | :--- |
| 128–1024 px (ícone do app, Dock) | B com o rescaldo largo: `#FFB088` → `#FF6A33` → 07 → 06 | 06 a 30%, só aqui |
| 33–127 px | B com o rescaldo largo | sem halo |
| 17–32 px | B com o rescaldo largo (a chapada na 07 reprovou) | sem halo |
| 16 px, favicon | B com o rescaldo largo, tile 01 liso | nada |
| Tray | template preto | nada |

- Lockups: "Brz" vai a `#E8E2DC` e a filha a `#A8A29E` no escuro; o "A" leva o linear 07 → 06 → 05.
- Ordem: as cores no `brza-brand-build.mjs` → os 23 SVG → `pnpm build:icons` (o tray deve sair idêntico) → o
  `--brand-gradient` em `main.css`.
- Os nomes `orca-*` ficam, porque o seletor de ícone do upstream os importa.

## O símbolo em tamanho real (rodadas 6 e 6b)

A coordenação renderizou o símbolo de hoje, A, B, C e duas variantes da B a 13–64 px, no Dock escuro e no papel claro
(Chrome headless, não o `iconutil`). As seis personas viram as folhas:

- **A de hoje lê melhor a 16 e a 32 px**, por unanimidade, e a C é a pior. A chama de hoje tem o topo `#ffaa44` a
  6,01:1 do tile; a brasa tem a 07 a 3,88:1.
- **Pico de luminância no Dock escuro** (Faísca mediu, a coordenação conferiu) — 16 px: hoje 142, B chapada 97, B com
  rescaldo largo 142, B com topo claro 125; 32 px: 166, 98, 161, 170; 64 px: 177, 98, 171, 189.
- **O voto empatou:** rescaldo largo (Fole, Faísca) contra topo claro (Tição, Lenha, Fogareiro); Cinza dividiu por
  tamanho. A coordenação recomenda o rescaldo largo, pelo pior caso. As variantes estão em
  `.sessions/reuniao-brasa/entregas/simbolo/` (`BR2-sem-halo.svg`, `BT-sem-halo.svg`), no worktree do `playground`.
- **Regra de saída** (Tição, Lenha), com o critério da contraprova do Tição: se, no `iconutil`, o pico de luminância
  da B ajustada ficar abaixo de 95% do de hoje a 16 ou 32 px, ou se menos de 4 de 5 a acharem entre seis chamas na
  fase 0, o símbolo de hoje fica inteiro, em todos os tamanhos, e a brasa muda só a interface.
- **A contraprova** (seis sessões novas, em outros modelos) leu a medida e votou seis de seis pelo rescaldo largo.

## A borda corta no Dock

Anderson viu, no Dock, a borda do símbolo cortada. A causa está no gerador: o traço da borda tem 24 de largura, centrado
na aresta do tile (`x=100 y=100 width=824 rx=185`), e o `clipPath` do tile usa essa mesma aresta, então a metade de fora
do traço (12 de 1024) é cortada. A correção é o traço inteiro dentro do tile: `x=112 y=112 width=800 rx=173`, mesma
largura de 24. Vale para o `brza-symbol.svg`, o `brza-app-icon.svg` e as variantes; a borda fica com o dobro da
espessura visível de hoje, e a largura se ajusta no render nativo (`iconutil`). O comparativo está em
`.sessions/reuniao-brasa/entregas/simbolo/` (`*-borda-inteira.svg`), no worktree do `playground`. A correção entra no
`config/scripts/brza-brand-build.mjs`, na fase 4, e não se edita o SVG à mão.

## O que a reunião levantou

- Fole e Faísca votaram pela C (a única que "conta o nome"): Fole com a C a partir de 64 px e o núcleo da B abaixo; a
  Faísca com a C a partir de 48 px e um glifo "D", uma fresta só, no miúdo. **Anderson decide** se a C entra como braço
  do teste de 5 s.
- Falta o render nativo (`iconutil`) a 13, 16 e 32 px, a 1× e 2×, e o tray real.

Fontes: [Reunião Carvão em Brasa: a participação de Tição, o Guardião](../worklogs/2026-11-07-reuniao-carvao-em-brasa-ticao.md), [Reunião Carvão em Brasa: a participação de Fole, a Estrategista de Marca](../worklogs/2026-11-07-reuniao-carvao-em-brasa-fole.md), [Reunião Carvão em Brasa: a participação de Faísca, a Provocadora](../worklogs/2026-11-07-reuniao-carvao-em-brasa-faisca.md).
