---
scope:
  - workspace
  - brza-studio
refs:
  - PLN-003
  - PLN-007
  - issue:o-design-md-do-brza-vem-do-pln-003
---

# O PLN-003: o painel de componentes

Depois de [O PLN-003: o spike do C5 nos dois apps](2026-11-03-pln-003-o-spike-do-c5-nos-dois-apps.md), a sessão
levou a Anderson a decisão que o spike destravou: o caminho do painel, que a R4.2 tinha fechado como "HTML regenerado".

## As rodadas

Gravadas na [Entrevista](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-interview.md), respondidas em
2026-11-03 nesta sessão:
- **R10.1**, o painel: **"Componentes (TSX) + worker (Recomendado)"**. Reabre a R4.2.
- **R10.2**, o `DESIGN.md` da R6.2: em texto livre, **"vai para o `workstream/brand`"**. Reabre a R6.2.
- **R10.3**, os botões: **"O botão chama o MCP residente"**, fora da recomendada (o worker rodar o `brza` direto). Os
  botões só existem na fase 2, com o B6; até lá, o painel só mostra.
- **R11.1**, a entrega ao `brand`: **"Issue no brand, gravada daqui (Recomendado)"**.

## O que se fez

- **O [Desenho](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-design.md):**
  - **Premissas:** R1.2, R10.1 e R10.3 no lugar do "em revisão"; R7.2, R10.2 e R11.1 no lugar da R6.2.
  - **B3:** no Orca, cadastra o repositório do workspace (item 2 do C5).
  - **B7:** passa a ser o painel de componentes com worker, com os botões pelo MCP. Sai o `brza panel render`. As
    6–10 h não foram refeitas.
  - **M17:** sem o "em revisão".
  - **Seção de arquitetura:** chama-se agora "ARCHITECTURE.md — proposta (R7.2)", e o `DESIGN.md` aponta para o
    `brand`.
  - **Terreno:** o "Não testado" virou ponteiro ao C5.
- **No workstream `brand`:** a issue
  [O DESIGN.md do BrzA vem do PLN-003](../issues/o-design-md-do-brza-vem-do-pln-003.md), pelo `brza note commit
  --workstream brand` (`b5ba181`). O worktree estava limpo. O PLN-007 não foi tocado e é citado sem link.
- **O `Retomar` do [PLN-003](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md):** o próximo passo são os
  itens `D`.

## Retomar

Escrever os itens `D` a partir da matriz, com os riscos da fase 0 como hipóteses (R7.3), e os Passos. Fica no
`Retomar` do PLN-003.
