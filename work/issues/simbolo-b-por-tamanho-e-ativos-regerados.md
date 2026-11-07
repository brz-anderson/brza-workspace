---
status: open
description: O símbolo vira a B (núcleo incandescente) com regra por tamanho — halo só no grande, chapado no pequeno, tray template — e os ativos saem regerados do gerador.
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
| 128–1024 px (ícone do app, Dock) | B radial: 07 → 06 → 05 | 06 a 30%, só aqui |
| 33–64 px | B radial | sem halo |
| 17–32 px | chapada na 07 | sem halo |
| 16 px, favicon | chapada na 07, tile 01 liso | nada |
| Tray | template preto | nada |

- Lockups: "Brz" vai a `#E8E2DC` e a filha a `#A8A29E` no escuro; o "A" leva o linear 07 → 06 → 05.
- Ordem: as cores no `brza-brand-build.mjs` → os 23 SVG → `pnpm build:icons` (o tray deve sair idêntico) → o
  `--brand-gradient` em `main.css`.
- Os nomes `orca-*` ficam, porque o seletor de ícone do upstream os importa.

## O que a reunião levantou

- Fole e Faísca votaram pela C (a única que "conta o nome"): Fole com a C a partir de 64 px e o núcleo da B abaixo; a
  Faísca com a C a partir de 48 px e um glifo "D", uma fresta só, no miúdo. **Anderson decide** se a C entra como braço
  do teste de 5 s.
- Ninguém testou a 13, 16 e 32 px reais, a 1× e 2×: é o que confirma ou derruba a regra de 17–32 px.

Fontes: [Reunião Carvão em Brasa: a participação de Tição, o Guardião](../worklogs/2026-11-07-reuniao-carvao-em-brasa-ticao.md), [Reunião Carvão em Brasa: a participação de Fole, a Estrategista de Marca](../worklogs/2026-11-07-reuniao-carvao-em-brasa-fole.md), [Reunião Carvão em Brasa: a participação de Faísca, a Provocadora](../worklogs/2026-11-07-reuniao-carvao-em-brasa-faisca.md).
