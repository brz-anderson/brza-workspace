---
scope:
  - workspace
  - tools-kit
refs:
  - PLN-003
  - issue:o-coordenador-le-o-indice-da-master
---

# O PLN-003: a fila do orquestrador

Pedido de Anderson, passado pela sessão `bb0fd632` do `workspace` em 2026-11-03: registrar no PLN-003 a rodada
respondida lá e ajustar o Desenho na R7.1, no M8, no M17 e no índice. Os registros de lá estão no `workstream/workspace`,
commit `19a9dda`:
- [O coordenador se baseia no índice de notas da master](../issues/o-coordenador-le-o-indice-da-master.md), que fechou;
- [A fila do coordenador vai ao PLN-003](2026-11-03-a-fila-do-coordenador-vai-ao-pln-003.md).

O spike do C5 estava parado na aprovação e continua assim
([O PLN-003: o spike do C5 parou na aprovação](2026-11-03-pln-003-o-spike-do-c5-parou-na-aprovacao.md)).

## O que se fez

- **A Rodada 9** foi gravada na
  [Entrevista](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-interview.md), com o pedido e as quatro respostas
  literais. As opções que perderam não vieram no pedido e não foram transcritas.
- **O [Desenho](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-design.md)**:
  - **Premissas:** a R9.1–R9.4 entra ao lado da R7.1, que fica.
  - **M8:** a fila ordena por `deadline`, `blocks`, `priority` e chegada, a partir do índice. Worker novo só abre sob o
    menor de três tetos: o do workspace, o da conta e runtime (com o ritmo projetado até o `resetsAt` e o corte a 90%)
    e o da máquina. As 4–6 h não foram refeitas.
  - **M17:** o painel mostra o motivo de cada posição e o teto que segura cada pedido parado.
  - **M24, item novo:** o índice da `master` grava `priority`, `blocks` e `deadline`, ~1 h no `brza note`, na fase 1,
    antes do M8.
  - **Regra × mecanismo:** a ordem da fila, que mora no `work/README.md` e o mcp impõe.
- **O [PLN-003](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md)**: o pedido 5, com a citação literal
  e duas linhas de Cobertura em rascunho; um item no `Retomar`; e a linha deste worklog.

## A decisão de Anderson

Respondida em 2026-11-03, na sessão `bb0fd632` do `workspace`:
- **"A mesma peça (Recomendado)"**;
- **"A ordem da norma (Recomendado)"**;
- **"Soma às camadas (Recomendado)"**;
- **"Projeção e memória (Recomendado)"**.

O texto de cada uma está na R9 da Entrevista. É registro de rodada no Desenho, sem item `D`: o plano segue no desenho.

## Retomar

O spike do C5, depois da aprovação de Anderson nos dois apps; depois, os itens `D`. Fica no `Retomar` do PLN-003.
