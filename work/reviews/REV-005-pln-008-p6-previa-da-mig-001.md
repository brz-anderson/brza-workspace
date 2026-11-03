---
status: done
description: Revisão prévia da MIG-001; A1 e A2 corrigidos na própria MIG, A3 falso.
scope:
  - workspace
  - brza-workflow
opened: 2026-11-03
completed: 2026-11-03
owner: Anderson
tags:
  - tooling
---

# REV-005: A revisão prévia da MIG-001 em P6 do PLN-008

Revisor independente: subagente reviewer desta sessão, em 2026-11-03. Esta é a revisão anterior à aplicação da
[MIG-001: Renumeração dos pareceres REV-001..REV-004 e backfill de refs nos worklogs](../issues/MIG-001-renumeracao-rev-e-refs-pln-008.md),
prevista em P6 do [PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md).
Não substitui P7. Os destinos saíram da rodada de 2026-11-03, em "Rodada dos destinos".

### A1 — O critério não comprova preservação de tags e dos demais campos

> lacuna · importante · confiança 99 · → corrigido aqui, com o bloco de preservação no critério da MIG-001

**Evidência:** no critério da MIG-001, a comparação do worklog com a própria normalização de refs/date aprova
um frontmatter do qual tags foi removido. A sonda do revisor ocorreu somente em memória, sobre o worklog
`2026-10-27-o-brza-workspace-nasce.md`. A fixture `brza-workflow/tests/cli/test_migrate_pln008.py:367` cobre
preservação em um worklog; falta prova sobre o acervo real. Não foi demonstrada perda pelo migrador.

**Recomendação:** comparar cada frontmatter com seu commit anterior à aplicação, excluindo apenas refs/date.
Os cinco HEADs foram capturados em `/tmp/pln008-p6-baseline.json`, sem alteração das notas históricas.

### A2 — Os passos não explicitam o comando de aplicação e a ordem das sessões donas

> lacuna · sugestão · confiança 97 · → corrigido aqui, com a seção "Aplicação" da MIG-001

**Evidência:** os quatro passos da MIG-001 enumeram conferências, sem invocar
`scripts/migrate_pln008.py --apply --workstream <dono>`. O script exige seleção explícita em
`brza-workflow/scripts/migrate_pln008.py:328` e restringe a aplicação às árvores selecionadas.

**Recomendação:** documentar comando por sessão, tools-kit antes de workspace, brand/studio em suas próprias sessões;
conferir nova passagem em tools-kit se referências ou links cruzados só materializarem depois de workspace.

### A3 — O cwd herdado faria o checador conferir a árvore errada

> bug · importante · confiança 99 · → falso

**Por que é falso:** cada `check_notes.py` resolve a raiz pela própria localização, e não pelo cwd.

**Evidência:** `.claude/skills/notes-checker/scripts/check_notes.py:79` resolve DEFAULT_ROOT por `__file__`.
O comando da MIG passa o script de cada árvore; `Path.cwd().parent.parent` é a raiz correta ao rodar no worktree
workspace indicado. Sessão principal refez a leitura da resolução da raiz.

No ensaio de 2026-11-03, cada chamada imprimiu a própria árvore como `raiz:`.

## Verificação

O revisor executou 10 testes focais de migração em 23,683 s, todos aprovados; confirmou as cinco reservas e a prévia.
A sessão principal executou a regressão: CLI 467 testes, hooks 288 e notes-checker 26 casos, todos aprovados.
O código do migrador não apresentou bloqueador de implementação nesta revisão. Relatório detalhado temporário: `/tmp/pln008-p6-mig-review.md`.

Depois da rodada, a sessão principal ensaiou a aplicação num clone isolado (`/private/tmp/pln008-sandbox`, com remoto
local e sem `BRZA_WORKSPACE`), na ordem da seção "Aplicação" da MIG-001. As seis passagens saíram com 0, e os três
blocos do critério passaram: o de preservação conferiu 107 notas, das quais 98 worklogs. Antes da aplicação, o bloco
falhou com `sem commit da MIG-001 em tools-kit`; um commit mutante que tirou `tags` de
`work/worklogs/2026-10-27-brza-studio-convive-com-o-orca.md` foi barrado com `frontmatter mudou além de refs/date`.

## Rodada dos destinos

Respondida por Anderson em 2026-11-03, na sessão `workspace`:

- **A1:** "Corrigir o critério antes de aplicar (Recomendado). Custo: acrescentar e conferir a comparação com os
  commits anteriores agora. Se paga: em P6, ao provar a preservação de tags e dos demais campos."
- **A2:** "Completar os passos agora (Recomendado). Custo: documentar comando e ordem antes da aplicação. Se paga: em
  P6, ao permitir execução e conferência por cada sessão dona."
- **A3:** "Registrar como falso (Recomendado). Custo: registrar a evidência já conferida. Se paga: agora, evitando
  reabrir a hipótese em P7."
