---
status: open
description: Os passos P6 e P7 do PLN-008 dependem estritamente da entrega das ferramentas e normas no brza-workflow e sincronização com o core antes da migração do acervo.
scope:
  - workspace
  - brza-workflow
opened: 2026-11-03
owner: Anderson
tags:
  - tooling
---

# Bloqueio de P6 e P7 sem a entrega publicada de P1 a P5 e sincronização do core

## O contexto

O [PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md)
divide o trabalho em 7 passos sequenciais com dependências estritas:
- P1 a P5 implementam no `brza-workflow` o extrator de referências, o validador de `depends_on`, os comandos `review-open` e `migration-open`,
  a nova listagem `ls`, as skills e o script `scripts/migrate_pln008.py`.
- P6 aplica a migração MIG-001 nos workstreams (`workspace` e `tools-kit`), renomeia as revisões para REV-001 a REV-004 e recalcula o `refs:`.
- P7 realiza a revisão independente e fecha o plano.

## O problema e o desvio

Ao solicitar a execução até o final do plano na sessão atual:
1. **Dependência de ferramentas inexistentes:** `bin/brza-note` e `check_notes.py` no workspace ainda não possuem
   as implementações de D1 a D10. Aplicar alterações manuais no acervo sem o script de migração e sem o suporte formal
   no checador geraria divergências normativas imediatas (ex: `check_notes.py` não reconheceria `issue:<slug>` em refs
   ou falharia ao conferir dependências).
2. **Integridade do `core.lock`:** arquivos de norma (`core/`) não devem ser alterados diretamente no worktree
   de notas; a alteração direta quebraria os hashes do manifesto e violaria a restrição expressa do plano:
   *"Norma comum, CLI, scripts e testes mudam no `brza-workflow`; chegam ao workspace pelo sync, sem editar cópias do core."*
3. **Respeito à integridade do relatório:** afirmar a conclusão de P6 e P7 sem a execução efetiva de P1 a P5 violaria
   as diretrizes de integridade e verificação factual.

## O que falta decidir

- Concluir a implementação e testes de P1 a P5 no repositório `brza-workflow`.
- Publicar a branch e rodar `brza sync` no `brza-workspace`.
- Executar P6 nos workstreams correspondentes e conduzir a revisão independente em P7.
