---
scope:
  - workspace
refs:
  - PLN-003
  - PLN-004
  - PLN-008
  - PLN-009
---

# O PLN-003 P1: o índice da master com priority, blocks e deadline

Na sessão `tools-kit` de 2026-11-03, em continuidade ao [PLN-003: O workflow do workspace roda igual no BrzA Studio e no Orca, por plugins e pelo `brza`](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md),
esta sessão executou o passo **P1** (D2/M24): a extração e persistência das propriedades de ordenação da fila do
orquestrador (`priority`, `blocks` e `deadline`) no índice unificado da master (`.brza/index.jsonl`).

## Contexto e TDD

O passo P2 do PLN-008 havia introduzido a extração de campos D9 para o índice. No entanto, o campo `blocks`, essencial
para a ordenação da fila (R9.2 / PLN-009/P2: `deadline` > `blocks` > `priority` > chegada), era extraído apenas como
escalar estrito (`isinstance(val, str)`). Ao declarar listas YAML (`blocks:\n  - PLN-004`) ou listas inline (`blocks: [PLN-004]`),
o campo era descartado silenciosamente.

1. **Teste que falha:**
   Adicionado o teste `test_pln003_p1_master_index_ordering_properties_for_plans_and_notes` na classe `Pln008P2IndexAndLsTest`
   de `tests/cli/test_brza_note_index.py` em `brza-workflow`. O teste falhou como esperado com `KeyError: 'blocks'`.

2. **Implementação:**
   Atualizada a função `note_state` em `bin/brza-note` para extrair `blocks` tanto quando fornecido em string escalar
   quanto em lista de strings (`list[str]`), limpando espaços em branco e preservando a integridade para serialização JSON
   no `.brza/index.jsonl`. Os campos `priority` e `deadline` continuam validados e comparados em `INDEX_COMPARED`.

3. **Validação:**
   A suíte de testes de `test_brza_note*.py` rodou com 131 testes passando (0 erros, 0 falhas):
   ```
   Ran 131 tests in 81.931s
   OK
   ```

4. **Publicação:**
   Commit `7a18392` (`feat(note): extrai priority, blocks e deadline para o índice da master (PLN-003/P1)`) na branch
   `master` de `brza-workflow`, sincronizado com a origin.
