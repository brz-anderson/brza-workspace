---
status: open
description: O texto ganha rampa própria em cinza quente (origens `#E8E2DC` e `#C4BEB9`), separada da rampa de superfície, porque a Cinza Carbono dá 1,8:1 como texto.
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
| Texto primário | origem `#E8E2DC` → efetivo `#BBB6B2` | `#1A1B1E` | 6,00 / 12,88 |
| Texto secundário e placeholder | origem `#C4BEB9` → efetivo `#A7A29F` | `#5C5650` / `#625C56` (a medir com o mix) | 4,77 no hover / 4,93 |
| Desabilitado (isento) | `#7A746F` | `#9C938B` | — |
| Divisória decorativa / funcional | `#454446` / `#8E8C90` | `#D9D1C9` / `#82776D` | funcional 3,62 / 3,27 |
| Código em linha | `#FFB088` | `#1A1B1E` | 6,79 / 12,88 |

- **O par medido não é o par renderizado** (revisor independente): o placeholder do composer usa `text-chat-foreground-faint` (`NativeChatComposerField.tsx:383`), que mistura a origem a 83% com o canvas (`main.css:330,358,684-688`). O `#99938E` da v1 reprovava no hover; o `#A8A29E` da v2 virava `#908B88` (3,58:1 no hover); a origem `#C4BEB9` rende `#A7A29F` (4,77). O secundário passa pela mesma `text-chat-foreground-faint` (48 arquivos), e por isso fica na mesma origem. O texto do corpo segue o controle de contraste do usuário (`native-chat-theme.ts:64-69,137-146`, 56% a 100%): no mínimo, o `#E8E2DC` rende 4,01 no 02 — o portão mede no padrão e registra o mínimo.
- **O código em linha sai da 07:** a 07 dá 4,1:1 dentro da caixa; `#FFB088`, o "rescaldo", fica a ΔE 23 da 07. Tição
  prefere o neutro; a caixa real decide.
- Nomes: primitivos `--brz-cinza-1..4` (Fole), semânticos em inglês, como o código do app.

## O que a reunião levantou

Cinco de seis a favor (Lenha preferia `#BCBCBC` neutro, pela margem). Risco: o APCA do secundário (Lc 45,7) pede o render real em Geist 14 px.

Fontes: [Reunião Carvão em Brasa: a participação de Fole, a Estrategista de Marca](../worklogs/2026-11-07-reuniao-carvao-em-brasa-fole.md), [Reunião Carvão em Brasa: a participação de Cinza, o Cético Analítico](../worklogs/2026-11-07-reuniao-carvao-em-brasa-cinza.md), [Reunião Carvão em Brasa: a participação de Tição, o Guardião](../worklogs/2026-11-07-reuniao-carvao-em-brasa-ticao.md).
