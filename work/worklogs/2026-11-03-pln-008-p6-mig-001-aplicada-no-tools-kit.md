---
scope:
  - workspace
refs:
  - MIG-001
  - PLN-002
  - PLN-003
  - PLN-008
  - PLN-009
  - REV-001
  - REV-005
---

# O PLN-008 P6: a MIG-001 aplicada no tools-kit, primeira passagem

A pedido da sessão `workspace-a6`, com a autorização de Anderson de 2026-11-03 ("sim", à pergunta "Quer que eu abra
essa sessão pelo `brza sessions` com o pedido da aplicação?"), esta sessão rodou o item 1 da "Aplicação" da
`MIG-001` no workstream `tools-kit`: a renomeação do REV-001. A `MIG-001`, a `REV-005` e o PLN-008 moram no
workstream `workspace` e não foram editados daqui; a consolidação é da `workspace-a6`.

## O que rodou e o que deu

1. `git status --short -- plans work wiki`: vazio, conferido de novo logo antes de aplicar, porque as sessões do
   PLN-009 e do PLN-003 também trabalham neste worktree.
2. Prévia, `python3 "$HOME/Projects/brza-workflow/scripts/migrate_pln008.py" --workstream tools-kit`: 0 criados,
   1 parecer renomeado, 5 notas com links reescritos, 29 worklogs atualizados — os mesmos números do ensaio.
3. Aplicação, o mesmo comando com `--apply`: saída 0.
   - `work/reviews/pln-002-os-comandos-brza.md` → [REV-001: a entrega do PLN-002, do P0 ao P9](../reviews/REV-001-pln-002-os-comandos-brza.md).
   - Links reescritos no `PLN-002-plan.md`, no `PLN-002-interview.md`, na issue do `brza test` e em dois worklogs de
     2026-10-29.
   - `refs:` gravado e `date:` retirado em 29 worklogs.
   - Commit `bf36704` (`docs(pln-008): migração MIG-001 em tools-kit`, 33 arquivos), com push na
     `workstream/tools-kit`.
   - Índice na `master`: `81620e3` (PLN-002, a issue do `brza test` e o REV-001) e `6e10fd0`, a reconstrução, com
     50 linhas acrescentadas.
4. `python3 .claude/skills/notes-checker/scripts/check_notes.py`: 73 arquivos, 0 links não resolvidos, 0 erros,
   0 avisos.

## Fora do mapa da MIG-001

Três pareceres do PLN-009 nasceram hoje em `work/reviews/` sem o número `REV-NNN`, depois do ensaio, e o script não os
renomeia: `pln-009-o-desenho-antes-da-execucao.md` (`3d94663`), `pln-009-a-revisao-dos-passos.md` (`8b622f8`) e
`pln-009-a-revisao-da-entrega.md` (`5ef53de`). O checador não os acusa. Ficaram como estão, e o achado foi à
`workspace-a6`, que decide se entram na MIG-001.

## Pendente

A segunda passagem no `tools-kit`, item 3 da "Aplicação", quando a `workspace-a6` pedir, depois que o `workspace`
aplicar.
