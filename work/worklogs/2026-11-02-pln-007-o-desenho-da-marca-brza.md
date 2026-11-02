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

A R5: o tile na grade da Apple (T1); o `logo.svg` com o A1 colorido (G2) e o estado vazio com o S1 no degradê (V2), os
dois contra a recomendação; o logotipo dentro do app como texto vivo na Geist.

O `brza shot` quebrou no meio da R5: o merge do upstream v1.4.246 no `brza-studio` moveu o
`PANEL_DESIGN_TOKEN_ALLOWLIST` para `src/shared/plugins/frames/plugin-panel-design-tokens.ts`. Os PNGs da R5 já tinham
saído e foram copiados do scratch; o pedido do conserto foi a
[O brza shot quebra com os tokens do painel movidos no brza-studio](../issues/brza-shot-quebra-com-os-tokens-do-painel-movidos.md),
e o Desenho segue com uma cópia corrigida no scratch, conferida igual pixel a pixel.
