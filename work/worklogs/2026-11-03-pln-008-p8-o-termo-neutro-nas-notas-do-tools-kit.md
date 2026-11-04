---
scope:
  - workspace
refs:
  - PLN-001
  - PLN-002
  - PLN-003
  - PLN-008
  - PLN-009
  - issue:scripts-da-fixfy-fora-do-port-para-o-brza
  - issue:skills-de-documento-da-fixfy-num-plugin
---

# O PLN-008 P8: o termo neutro nas notas do tools-kit

A pedido da sessão `workspace-a6`, com a autorização de Anderson de 2026-11-03 ("sim", à pergunta "Posso abrir as
sessões?" do D11), esta sessão tirou das notas do `tools-kit` as citações ao workspace de origem, trocadas por "outro
workspace" ou "o workspace de origem", sem nome nem ID da nota de lá (R15.1, R15.2, R16.1, R16.3). Ficaram, pela R17.1,
as duas identidades `issue:<slug>` antigas no `refs`. O PLN-008 e o D11 moram no workstream `workspace` e não foram
editados daqui.

## O que se fez

1. `git status --short`: vazio. A sessão do PLN-003 que trabalha neste worktree não tinha arquivo sujo, e o status
   seguiu só com os meus caminhos até o commit.
2. Três notas renomeadas pelo `move_note.py`, conforme o mapa da `workspace-a6`, com o H1 neutro:
   - [Os scripts de orquestração do workspace de origem que ficaram fora do port para o BrzA](../issues/scripts-do-workspace-de-origem-fora-do-port-para-o-brza.md);
   - [As skills de documento do workspace de origem num possível plugin do BrzA](../issues/skills-de-documento-do-workspace-de-origem-num-plugin.md);
   - [Os scripts do Orca do workspace de origem adaptados ao BrzA Studio](2026-10-28-scripts-do-orca-de-origem-adaptados-ao-brza.md).
3. O texto de 13 notas trocado frase a frase: os planos PLN-002 e PLN-003, as issues, o parecer do desenho do PLN-009 e
   os worklogs. Caminho de lá virou "o `scripts/…` do workspace de origem"; o e-mail das contas do app virou "a conta
   `admin@` (ou `anderson@`) do workspace de origem"; a decisão de lá citada no PLN-003 e o worktree com o ID de um
   plano de lá viraram descrição pelo assunto; nas citações de Anderson, o nome saiu entre colchetes.
4. Commit `9a40746`, 16 arquivos, com o `2026-10-31-o-brza-tree-instala-o-mobile.md`, que perdeu o PLN-001 do `refs`
   pelo extrator novo. Índice na `master`: as duas issues `changed`, com o caminho novo e o ID antigo.
5. Commit `ffc0cf7`: o `refs` de dois worklogs voltou à identidade antiga das issues.

## O que se aprendeu

- **Renomear issue e recalcular o `refs` no mesmo commit troca a identidade.** No `9a40746`, o `brza note commit`
  gravou no `refs` o slug novo das duas issues, porque o índice ainda não tinha o caminho novo e o `git log --follow`
  ainda não via o rename; o checador aceitou o slug novo pelo mesmo motivo. Depois do commit, o índice passou a mapear o
  caminho novo para o ID antigo, e o checador acusou `ref-not-found`. A linha do `refs` se corrige à mão e se recomita.
  O defeito é do `brza-workflow` e foi à `workspace-a6`.

## O que ficou

- **Dois links para notas de outros workstreams ficam para a segunda passagem**, porque o destino novo ainda não existe
  na branch dona (`git ls-tree` na `origin`):
  - no `PLN-002-interview.md`, o link para o worklog do ▶ e do ⤢, no `studio`;
  - na issue das skills de documento, o link para o worklog do porte das skills, no `workspace`, com o rótulo antigo.
- **O `git grep -il` final** acha só esses dois links e as duas identidades antigas no `refs` dos worklogs.
- **O checador:** 0 erros, 0 links não resolvidos, 3 avisos `review-without-number`, os pareceres do PLN-009 sem número
  que já vinham de antes.
