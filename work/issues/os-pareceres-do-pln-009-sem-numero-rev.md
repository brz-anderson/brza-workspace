---
status: open
description: Os três pareceres do PLN-009 em work/reviews/ nasceram sem o número REV-NNN; a sessão dona do plano reserva cada número com o brza note review-open e os renomeia com o move_note.py.
scope:
  - workspace
opened: 2026-11-03
owner: Anderson
priority: low
tags:
  - planning
---

# Os pareceres do PLN-009 sem número REV

Os pareceres do [PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md)
moram em `work/reviews/` com H1 `# REV: …` e sem o número `REV-NNN` que a norma de `work/reviews/` pede:

| Parecer | Criado em |
| :------ | :-------- |
| [REV: o Desenho do PLN-009 antes da execução](../reviews/pln-009-o-desenho-antes-da-execucao.md) | `3d94663` |
| [REV: os passos P1 a P6 do PLN-009, revisados pelo agy e pelo Opus](../reviews/pln-009-a-revisao-dos-passos.md) | `8b622f8` |
| [REV: a entrega do PLN-009 contra o Pedido e a Cobertura](../reviews/pln-009-a-revisao-da-entrega.md) | `5ef53de`, às 18:59 de 2026-11-03, depois de a norma do REV chegar no merge `5dcc2b3` |

A origem é a MIG-001 do workstream `workspace`,
`workspace:work/issues/MIG-001-renumeracao-rev-e-refs-pln-008.md`: o script dela não renomeia os três, porque nasceram
depois do ensaio, e o checador não os acusa. Na rodada da sessão `workspace-a6`, em 2026-11-03, Anderson escolheu
"Issue no tools-kit (Recomendado)": a sessão dona do PLN-009 numera os três, sem reabrir o D4 nem mexer no script do
PLN-008.

## O que falta

A sessão que conduzir o PLN-009, para cada parecer:

1. Reserva o número com `brza note review-open`. Os números saem do índice da `master` na hora; não se supõe a faixa.
2. Renomeia com `python3 .claude/skills/notes-checker/scripts/move_note.py <origem> work/reviews/REV-NNN-<assunto>.md --title "REV-NNN: …"`,
   que reescreve o H1 e os links Markdown relativos nos dois sentidos.
3. Roda o checador, `python3 .claude/skills/notes-checker/scripts/check_notes.py`, e grava pelo `brza note commit`.

Os worklogs que citam os nomes antigos em crase ficam como estão: são o registro do dia.

O gatilho é o fechamento do PLN-009, como a escolha de Anderson previu.
