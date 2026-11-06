---
scope:
  - workspace
refs:
  - PLN-003
  - PLN-009
  - REV-014
  - REV-015
  - REV-016
  - issue:o-mcp-nao-cancela-pedido-na-fila
  - issue:os-pareceres-do-pln-009-sem-numero-rev
  - issue:os-passos-do-mcp-no-pln-003-passam-ao-pln-009
---

# O PLN-009: os pareceres numerados, a decisão do código do MCP e o fechamento

Pedido de Anderson: "Retomar PLN-009". O plano é o
[PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md),
em `phase: review`, com P1 a P8 `[x]` e os casos C1 a C4 aprovados.

## O que o `Retomar` dizia que faltava, conferido no disco

- **A R5.3 no PLN-003 já estava feita:** `PLN-003-interview.md:260` traz "→ reaberta em PLN-009/R1.1", e os P6 a P9 de
  lá estão `[-] → PLN-009`. A issue [Os passos do MCP no PLN-003 passam ao PLN-009](../issues/os-passos-do-mcp-no-pln-003-passam-ao-pln-009.md)
  já estava `done`.
- **O plist já estava corrigido:** `~/Library/LaunchAgents/com.brza.orchestrator.plist` aponta o checkout principal,
  `~/Projects/brza-workflow/packages/mcp/bin/brza-mcp`. O `brza mcp status` respondeu "carregado: sim", pid 18765.
- **Os três pareceres continuavam sem número REV.**

## Os pareceres numerados

Anderson escolheu "Numerar e conferir (Recomendado)". O `brza note review-open` reservou os números na ordem em que os
pareceres nasceram, e o `move_note.py` renomeou cada um, reescrevendo o H1 e os links:

- [REV-014: o Desenho do PLN-009 antes da execução](../reviews/REV-014-pln-009-o-desenho-antes-da-execucao.md);
- [REV-015: os passos P1 a P6 do PLN-009, revisados pelo agy e pelo Opus](../reviews/REV-015-pln-009-a-revisao-dos-passos.md);
- [REV-016: a entrega do PLN-009 contra o Pedido e a Cobertura](../reviews/REV-016-pln-009-a-revisao-da-entrega.md).

Os três ganharam a `description`, e a issue [Os pareceres do PLN-009 sem número REV](../issues/os-pareceres-do-pln-009-sem-numero-rev.md)
foi a `done`. O plano ganhou a seção `## Documentação` e, nas Pendências, a issue
[O `brza-mcp` não cancela um pedido que espera na fila](../issues/o-mcp-nao-cancela-pedido-na-fila.md), que o checador
acusava como `backlink-missing`. Commit `8ae71fa`.

## A conferência de fechamento e a decisão

A conferência (`close.md`) deu tudo limpo, menos a R1.1, que decide algo além do plano. Anderson escolheu "Gravar a
nota" e "Fechar agora (Recomendado)". Enquanto eu escrevia o rascunho, achei um fato novo: o `brz-anderson/brza` passou
a existir em 2026-11-04, criado pelo PLN-003/P3, só com a CLI. Isso confirma a divisão da R5.3. Sobre o texto, com ele
inteiro na mensagem, Anderson respondeu: "pode gravar".

- A decisão: [O código do MCP mora no `brza-workflow`, em `packages/mcp/`](../decisions/o-codigo-do-mcp-mora-no-brza-workflow.md).
- O plano foi a `status: done` e `phase: closed`, com `completed: 2026-11-06` e o `remaining_h` corrigido de 2.0 para
  0, porque nenhum passo estava aberto.

## O que ficou aberto

As seis issues de `## Pendências conhecidas` do plano seguem `open`, cada uma com o próprio gatilho.
