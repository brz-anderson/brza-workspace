---
scope:
  - workspace
tags:
  - tooling
refs:
  - MIG-001
  - PLN-008
  - REV-001
  - REV-004
---

# Aplicação da MIG-001 no playground

Item 4 da seção "Aplicação" da [MIG-001: Renumeração dos pareceres REV-001..REV-004 e backfill de refs nos worklogs](../issues/MIG-001-renumeracao-rev-e-refs-pln-008.md),
em P6 do PLN-008, a pedido da sessão `workspace-a6`, com a autorização de Anderson de 2026-11-03 ("sim", à pergunta
"Abro as três sessões com o mesmo roteiro do `tools-kit`?"). Rodou na sessão `playground-mig001`, depois do
`tools-kit` (`bf36704`) e do `workspace` (`361d0d4`).

## O que foi feito

1. **Notas limpas:** `git status --short -- plans work wiki` vazio, com a branch em `82c440b`.
2. **Prévia**, `python3 "$HOME/Projects/brza-workflow/scripts/migrate_pln008.py" --workstream playground`, com saída 0:
   `0 criado(s), 0 parecer(es) renomeado(s), 0 nota(s) com links reescritos, 0 worklog(s) atualizado(s)`. Igual ao
   ensaio, que dizia que o `playground` não muda.
3. **Aplicação**, o mesmo comando com `--apply`, com saída 0: `[APLICADO]` com os mesmos zeros e `índice: bootstrap em
   dia`. Sem mudança, o script não gerou commit da migração nem da reconstrução do índice: a branch seguiu em
   `82c440b`, igual a `origin/workstream/playground`.
4. **Checador**, `python3 .claude/skills/notes-checker/scripts/check_notes.py`, com saída 0: 22 arquivos, 0 links não
   resolvidos, 0 erros e 0 avisos.

## O que ficou aberto

Nada neste workstream. A consolidação da MIG-001 e do PLN-008 é da sessão `workspace-a6`, avisada por correio.
