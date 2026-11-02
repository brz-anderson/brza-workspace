---
scope:
  - brza-studio
  - workspace
---

# PLN-007: o Desenho da marca BrzA

O Desenho do
[PLN-007: A marca BrzA tem símbolo, logotipo e derivadas a partir da chama do app](../../plans/PLN-007-a-identidade-visual-da-marca-brza/PLN-007-plan.md),
depois da entrevista fechada em 2026-10-31.

## O que se levantou

O `designer` rascunhou 8 itens `D` e 14 pontos para rodada, no scratch da sessão (`desenho-rascunho.md`), com sondas:
o `}` corrigido no traço mono, o CoreText do `swift` lendo a Geist woff2 com o peso — o `opentype.js` e o `hb-view` não
leem —, e a grade da Apple para o tile. A sessão conferiu por amostra quatro fatos: o app só leva o `.icns`, o
`#1447e6` dá 2,9:1 no escuro, o cabeçalho do painel do chat não tem título, e o "agente trabalhando" é o spinner do
`NativeChatTurnActivityLine`.

## O que se decidiu

A R4, toda na recomendada: a fonte da marca mora em `brza-studio/resources/brand/`; esta sessão do `brand` desenha o
símbolo e os lockups, e o `brza-studio` só copia o aprovado; o `.icns` sai do SVG pelo `rsvg-convert` e o `iconutil`,
sem o `actool`, o que tira o `icon.json` do caminho do ícone; a execução vai em seis passos e três branches.
