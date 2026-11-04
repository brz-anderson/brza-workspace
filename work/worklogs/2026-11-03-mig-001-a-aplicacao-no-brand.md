---
scope:
  - workspace
refs:
  - MIG-001
  - PLN-008
---

# MIG-001: a aplicação no `brand`

O pedido da sessão `workspace-a6`, em 2026-11-03: o item 4 da aplicação da
[MIG-001: Renumeração dos pareceres REV-001..REV-004 e backfill de refs nos worklogs](../issues/MIG-001-renumeracao-rev-e-refs-pln-008.md)
no workstream `brand`, parte do
[PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md)
(P6). A autorização é de Anderson, de 2026-11-03: "sim", à pergunta "Abro as três sessões com o mesmo roteiro do
`tools-kit`?". `tools-kit` (`bf36704`) e `workspace` (`361d0d4`) já tinham aplicado. A MIG-001 e o PLN-008 moram no
`workspace`, e a consolidação é da sessão `workspace-a6`; daqui não foram editados.

## O que se fez

1. **Árvore limpa:** `git status --short -- plans work wiki` saiu vazio.
2. **Prévia**, igual ao ensaio:

   ```bash
   python3 "$HOME/Projects/brza-workflow/scripts/migrate_pln008.py" --workstream brand
   ```

   `0 criado(s), 0 parecer(es) renomeado(s), 0 nota(s) com links reescritos, 4 worklog(s) atualizado(s)`, saída 0. Os
   quatro: `2026-10-31-pln-007-a-abertura-da-marca-brza.md`, `2026-11-02-os-plugins-da-orca-1-4-246-e-os-planos.md`,
   `2026-11-02-pln-007-o-desenho-da-marca-brza.md` e `2026-11-02-pln-007-os-tokens-da-marca.md`. O worklog
   `2026-11-03-pln-007-o-brza-dark-theme.md`, posterior ao ensaio, não entrou: já nasceu com `refs:`.
3. **Aplicação:**

   ```bash
   python3 "$HOME/Projects/brza-workflow/scripts/migrate_pln008.py" --apply --workstream brand
   ```

   Saída 0, com as mesmas contagens. Commit `0e80b71` (`docs(pln-008): migração MIG-001 em brand`), só os quatro
   worklogs, 16 linhas acrescentadas, com push na `origin/workstream/brand`. O índice saiu "bootstrap em dia" e "em
   dia, nada a acrescentar": nenhum commit na `master`.
4. **Checador:** `python3 .claude/skills/notes-checker/scripts/check_notes.py` com 63 arquivos, 0 links não
   resolvidos, 0 erros e 0 avisos, também no que o próprio script rodou depois do commit.

## Pendente

Nada no `brand`. Faltam `studio` e `playground`, em sessões próprias, e o critério de conclusão, que a sessão
`workspace-a6` roda no worktree `workspace`.
