---
status: open
description: O texto ganha rampa própria em cinza quente (`#E8E2DC`, `#A8A29E`), separada da rampa de superfície, porque a Cinza Carbono dá 1,8:1 como texto.
scope:
  - brza-studio
opened: 2026-11-07
priority: high
tags:
  - design
---

# A rampa de texto quente, separada da rampa de superfície

Levantado na [Reunião Carvão em Brasa: a coordenação e a proposta de plano](../worklogs/2026-11-07-reuniao-carvao-em-brasa-coordenacao.md). A paleta de sete etapas não tem tom de texto: a 03 `#454446` dá 1,78:1 sobre o 01, e o
protótipo saiu da paleta para `#BCBCBC`. A sala decidiu manter o fundo `#1A1B1E` e pôr o calor do carvão no texto.

## O pedido

| Papel | Escuro | Claro | Pior contraste (E / C) |
| :---- | :----- | :---- | :--------------------- |
| Texto primário | `#E8E2DC` | `#1A1B1E` | 9,39 / 12,88 |
| Texto secundário e placeholder | `#A8A29E` | `#5C5650` / `#625C56` | 4,79 / 4,93 |
| Desabilitado (isento) | `#7A746F` | `#9C938B` | — |
| Divisória decorativa / funcional | `#454446` / `#8E8C90` | `#D9D1C9` / `#82776D` | funcional 3,62 / 3,27 |
| Código em linha | `#FFB088` | `#1A1B1E` | 6,79 / 12,88 |

- **O placeholder de `#99938E`, da v1, reprovou** no hover da superfície elevada (3,98:1) e foi para `#A8A29E`.
- **O código em linha sai da 07:** a 07 dá 4,1:1 dentro da caixa; `#FFB088`, o "rescaldo", fica a ΔE 23 da 07. Tição
  prefere o neutro; a caixa real decide.
- Nomes: primitivos `--brz-cinza-1..4` (Fole), semânticos em inglês, como o código do app.

## O que a reunião levantou

Cinco de seis a favor (Lenha preferia `#BCBCBC` neutro, pela margem). Risco: placeholder igual ao secundário encolhe
a hierarquia; o APCA do secundário (Lc 45,7) pede o render real em Geist 14 px.

Fontes: [Reunião Carvão em Brasa: a participação de Fole, a Estrategista de Marca](../worklogs/2026-11-07-reuniao-carvao-em-brasa-fole.md), [Reunião Carvão em Brasa: a participação de Cinza, o Cético Analítico](../worklogs/2026-11-07-reuniao-carvao-em-brasa-cinza.md), [Reunião Carvão em Brasa: a participação de Tição, o Guardião](../worklogs/2026-11-07-reuniao-carvao-em-brasa-ticao.md).
