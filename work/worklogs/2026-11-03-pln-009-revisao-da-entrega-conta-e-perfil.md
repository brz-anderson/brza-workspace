---
scope:
  - workspace
refs:
  - PLN-003
  - PLN-009
  - REV-016
---

# O PLN-009: a revisão da entrega e a correção da conta e do perfil

A pedido de Anderson, "Retomar PLN-009", foi retomada a revisão da entrega do
[PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md).

Um `reviewer` independente conferiu Pedido, Cobertura e testes: encontrou conta explícita que envelhecia na fila,
consulta de contas da produção para worker de perfil de desenvolvimento e omissão do C4 no fechamento.
Pela preferência registrada de corrigir aqui, um `implementer` corrigiu A1/A2, e o revisor aprovou o delta.
A3 foi corrigido no plano. Parecer:
[REV-016: a entrega do PLN-009 contra o Pedido e a Cobertura](../reviews/REV-016-pln-009-a-revisao-da-entrega.md).

O P7 fechou em `brza-workflow@354d004`: três regressões falharam antes; 63 testes pontuais passaram depois;
gate final MCP 349 OK (um pulado). Hooks 290 OK e CLI limpo 445 OK foram refeitos no código original da entrega.
O sandbox negava o `sysctl` de swap; a suíte MCP passou ao liberar a leitura. Checador de notas sem erros na retomada.

O plano permanece em revisão. C1 a C4 e a confirmação do merge continuam pendentes. O índice já contém
prioridades, mas não foi provado o C3 com `blocks` e `deadline`; o estado do PLN-003/P1 depende da sessão dona.

## Fora do workspace

- **O quê e onde:** correção de seis arquivos em `~/Projects/brza-workflow/.worktrees/pln-009-mcp`,
  commit `354d004` publicado na `feat/pln-009-mcp`. **Risco:** alteração dos tetos e da seleção de conta,
  coberta por regressões e revisão independente. **Estado:** publicada, sem merge.
  **Como desfazer:** reverter `354d004` na branch, preservando o histórico.
