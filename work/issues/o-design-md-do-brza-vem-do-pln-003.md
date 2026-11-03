---
status: open
description: O DESIGN.md, o design system que a R6.2 do PLN-003 dava ao painel do plugin do Orca, saiu do PLN-003 e veio ao brand, por decisão de Anderson na R10.2; o painel de componentes usa o tema do app.
scope:
  - workspace
  - brza-studio
opened: 2026-11-03
tags:
  - design
---

# O DESIGN.md do BrzA vem do PLN-003

Pedido gravado pela sessão do `tools-kit` em 2026-11-03, na forma que Anderson escolheu na R11.1 do
[PLN-003](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md): "Issue no brand, gravada daqui
(Recomendado)".

## De onde vem

- **A R6.2 do PLN-003** (2026-10-29) decidiu que o `DESIGN.md` é "o design system do painel, no formato do Stitch", o
  formato de design system para agentes de UI do Google Stitch. O painel era HTML regenerado (R4.2).
- **O spike do C5** (2026-11-03) mediu os dois caminhos de painel no BrzA Studio e no Orca. O painel de componentes
  (`ui: "components"`) herda o tema, o teclado e o catálogo do app. O HTML precisa de tema próprio: no spike, saiu
  ilegível no tema escuro. A R10.1 escolheu o de componentes.
- **A R10.2**, sobre o que vira o `DESIGN.md`, foi respondida em texto livre: **"vai para o `workstream/brand`"**. A
  R11.1 escolheu esta issue como a entrega.

## O que se pede ao `brand`

Decidir se o `DESIGN.md` nasce aqui, junto da identidade do `PLN-007`, e o que ele cobre: o app, o painel do plugin, ou
os dois. O PLN-003 não espera por ele. O painel de componentes já segue o tema do app, e o que mudar
no tema chega ao painel sem trabalho do PLN-003.

O registro está no PLN-003, do workstream `tools-kit`: R6.2, R10.2 e R11.1 na Entrevista, e o C5 no Desenho.
