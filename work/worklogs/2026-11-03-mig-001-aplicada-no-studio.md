---
scope:
  - workspace
tags:
  - tooling
refs:
  - MIG-001
  - PLN-008
---

# A MIG-001 aplicada no workstream `studio`

Item 4 da aplicação da [MIG-001: Renumeração dos pareceres REV-001..REV-004 e backfill de refs nos worklogs](../../../workspace/work/issues/MIG-001-renumeracao-rev-e-refs-pln-008.md),
na P6 do PLN-008, pedido pela sessão `workspace-a6` com a autorização de Anderson de 2026-11-03 ("sim", à pergunta
"Abro as três sessões com o mesmo roteiro do `tools-kit`?"). Rodou na sessão `studio-mig001`, depois de `tools-kit`
(`bf36704`) e `workspace` (`361d0d4`).

## O que rodou

1. `git status --short -- plans work wiki`: vazio.
2. Prévia, `python3 "$HOME/Projects/brza-workflow/scripts/migrate_pln008.py" --workstream studio`: saída 0,
   `0 criado(s), 0 parecer(es) renomeado(s), 0 nota(s) com links reescritos, 43 worklog(s) atualizado(s)`, igual ao
   ensaio. Dos 44 worklogs da pasta, um já estava na forma final. Três avisos `unknown-ref-mention` em
   `2026-10-28-pln-001-no-molde-do-workspace-de-origem.md`: menções históricas a planos do workspace de origem, que o D3
   só avisa.
3. `--apply --workstream studio`: saída 0, mesmas contagens. Commit `d5abc5e`
   (`docs(pln-008): migração MIG-001 em studio`), 43 arquivos, com push na `workstream/studio`. Índice da `master`: em
   dia, nada a acrescentar.
4. `python3 .claude/skills/notes-checker/scripts/check_notes.py`: 63 arquivos, 0 links não resolvidos, **0 erros** e 8
   avisos — 3 `backlink-missing`, 2 `tag-out-of-vocabulary` e os 3 `unknown-ref-mention` acima. Os mesmos avisos já
   existiam em `24e303e`, o pai do commit da migração, além de 39 `date-on-worklog`, que a migração eliminou.

## Pendente

A consolidação da MIG-001 e do PLN-008 é da sessão `workspace-a6`, avisada por correio. Faltam `brand` e `playground`.
