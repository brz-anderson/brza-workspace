---
status: done
description: Revisão independente da entrega do PLN-008 (P7), com oito achados, quatro falsos e o P8 de correção.
scope:
  - workspace
  - brza-workflow
opened: 2026-11-03
completed: 2026-11-03
owner: Anderson
tags:
  - tooling
---

# REV-006: A entrega do PLN-008 contra o Pedido e a Cobertura

Revisor independente: subagente `reviewer` da sessão `workspace-a6`, em 2026-11-03, sem as conclusões de quem
conduziu. Ele conferiu o entregue em `brza-workflow` (`b7fb3d2`, `b7e8727`, `3fc3935`, `a168f73`, `a666e78`) e no
acervo das cinco árvores contra o `## Pedido` e a Cobertura do
[PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md).
A sessão principal refez a evidência de A1, A2, A3 e A6 antes da rodada. Os destinos são de Anderson, na Rodada 14.

### A1 — O checador não avisa parecer novo sem `REV-NNN`, que some do índice e do `refs`

> lacuna · importante · confiança 95 · → corrigido aqui, no P8, como aviso

**Evidência:** a norma pede `REV-NNN-<assunto>.md` (`brza-workflow/core/work/README.md:159,326`); o checador só
reconhece `REV_NOTE_RE` (`check_notes.py:72`) e não acusa o nome fora da forma. Sonda em
`/private/tmp/pln008-p7-sonda/s1`: parecer `work/reviews/pln-001-sem-numero.md`, MIG sem `type` e issue `type: migration`
sem número dão 0 avisos. Três pareceres do PLN-009 no `tools-kit` nasceram assim, um depois da norma (`5ef53de`); o
índice da master não tem linha para eles, e o worklog que os linka fica sem a referência. Cobertura `Pedido 2`; D7.

### A2 — A norma aceita `REV-NNN` e `decision:` em `depends_on`, e o checador barra os dois

> bug · importante · confiança 97 · → corrigido aqui, no P8, voltando a norma ao D2

**Evidência:** `core/work/README.md:226` e `plan-template.md:24` listam `REV-NNN` e `decision:<slug>`;
`check_notes.py:350-368` só põe PLN, MIG e `issue:` em `dep_targets`. Sonda `s1`: `depends_on: [decision:minha-decisao,
REV-001]`, com as duas notas `done`, dá `depends-on-not-found` duas vezes. O D2 só previu PLN, MIG e issue. Cobertura
`R7.2`.

### A3 — Do P2 até `7a18392`, `blocks` em lista não chegava ao índice

> bug · sugestão · confiança 96 · → descartado: `7a18392`, do PLN-003/P1, já corrigiu, e nenhuma nota usa `blocks`

**Evidência:** `a666e78:bin/brza-note:946-947` punha `blocks` entre os campos escalares; a sonda de `note_state`
devolve a lista em `7a18392` e a perde em `a666e78`. `git grep '^blocks:'` nas cinco branches não acha nada. Cobertura
`R4.3`; D9.

### A4 — ID no texto de um link entra no `refs`, e o intervalo marca só as pontas

> lacuna · sugestão · confiança 97 · → corrigido aqui, no P8, tirando o texto do link da extração (D3 reaberto)

**Evidência:** `bin/brza-note:588` e `check_notes.py:420` tiram o href e mantêm o texto do link na varredura.
`brand/work/worklogs/2026-11-03-mig-001-a-aplicacao-no-brand.md:4-8,14` ganha REV-001 e REV-004 pelo título da MIG-001;
o mesmo em `studio`, `playground` e um worklog do `tools-kit` (PLN-001): 4 de 121 worklogs. Há 7 intervalos em 6
worklogs, todos marcando só as pontas. O D3 e a R10.1 contam "links" sem tratar o texto deles. Cobertura `R10`;
`Pedido 1`.

### A5 — Há duas cópias do extrator do D3 sem teste de paridade

> lacuna · sugestão · confiança 90 · → issue [O extrator do refs tem duas cópias sem teste de paridade](../issues/o-extrator-do-refs-tem-duas-copias-sem-teste-de-paridade.md)

**Evidência:** `bin/brza-note:180-187,536-596` e `check_notes.py:72-79,417-460`. Hoje concordam em 121 de 121
worklogs, mas o checador não compara o `refs` gravado com o calculado. D3; D8.

### A6 — Duas issues resolvidas do PLN-008 continuam `open`

> lacuna · sugestão · confiança 92 · → corrigido aqui, no fechamento

**Evidência:** `work/issues/bloqueio-de-p6-e-p7-sem-entrega-e-sync-do-core.md:2` e
`work/issues/falso-negativo-em-test-brza-note-por-caminho-com-brza-studio.md:2` com `status: open`; o P6 fechou e a
correção da segunda está em `b7fb3d2` (`tests/cli/test_brza_note.py:811-831`). Fechamento.

### A7 — O núcleo guarda o mapa e a flag de uma migração única deste workspace

> lacuna · sugestão · confiança 85 · → issue [O núcleo guarda o bootstrap da migração do PLN-008](../issues/o-nucleo-guarda-o-bootstrap-da-migracao-do-pln-008.md)

**Evidência:** `bin/brza-note:131-178` (`PLN008_BOOTSTRAP`, com os workstreams daqui) e `:1410`
(`--bootstrap-pln008`), sem uso depois da MIG-001 `done`. Premissa: o `brza-workflow` serve outros workspaces pelo
`brza init`. D7.

### A8 — P1–P4 saíram com o e-mail da Fixfy, e `7a18392` repete

> desvio · sugestão · confiança 99 · → descartado: já registrado nos worklogs de P5 e P6, e a Restrição proíbe reescrever histórico

**Evidência:** `git log --format='%h %ae'` dá `anderson@fixfy.com.br` em `b7fb3d2`, `b7e8727`, `3fc3935`, `a168f73`,
`9f51cda` e `7a18392`; `git config --show-origin user.email` aponta o `~/.gitconfig`, herdado pela sessão sem o `env`.

### A9 — A suíte CLI falha em 20 testes

> bug · importante · confiança 97 · → falso

**Por que é falso:** as falhas vêm da `BRZA_WORKSPACE` herdada, que dispara a recusa `foreign_cwd`.

**Evidência:** com a variável, 468 testes e 20 falhas ("a BRZA_WORKSPACE aponta o workspace…"); com
`env -u BRZA_WORKSPACE -u BRZA_STUDIO -u BRZA_WORKFLOW`, 468 OK em 177,9 s.

### A10 — Os commits de outras tarefas quebram o que o PLN-008 entregou

> bug · importante · confiança 95 · → falso

**Por que é falso:** `f0f1171`, `9f51cda` e `c527e42` não tocam o entregue; `7a18392` altera, mas para cumprir o D9
(A3).

**Evidência:** `f0f1171` mantém `session_map`, `provider_session` e `chat_name`
(`packages/client/bin/brza-sessions:83,204,215`); `c527e42` só troca texto e golden, com os 288 testes de hooks
passando; `9f51cda` só mexe em teste.

### A11 — O `refs` gravado no acervo diverge do extrator

> bug · importante · confiança 98 · → falso

**Por que é falso:** o gravado é igual ao calculado em 121 de 121 worklogs.

**Evidência:** o bloco 2 do critério da MIG-001, rodado de novo pelo revisor, sai com 0.

### A12 — O índice ficou incompleto ou com estado velho depois da MIG-001

> bug · importante · confiança 95 · → falso, exceto os três pareceres da A1

**Por que é falso:** o `status` em disco das cinco árvores bate com `origin/master:.brza/index.jsonl`.

**Evidência:** a comparação não achou status divergente; só faltam os três `pln-009-*` da A1.

## Cobertura

Cumpre: Pedido 1 (os três critérios), Pedido 3, Pedido 4 (os dois), R4.2, R4.3 (desde `7a18392`), R5.2, R5.3, R6.1,
R9.1, R9.2, R10 (com a lacuna da A4), R11.2, R12 e a emenda da R12. Cumpre parcialmente: Pedido 2 (A1), R7.2 (A2) e
R4.1, cuja sonda atual não cobre worktree de código em branch de plano, caso que segue só em fixture. Nada deixa de
cumprir. Relatório detalhado temporário: `/private/tmp/pln008-p7/revisao.md`.

## Verificação

Rodado pelo revisor, em `brza-workflow@7a18392`, com `TMPDIR=/tmp PYTHONDONTWRITEBYTECODE=1`: `tests/cli` com 468 OK
em 177,9 s, sem a `BRZA_WORKSPACE`; `tests/hooks` com 288 OK em 18,4 s; `tests/notes-checker/run.py` com 26 casos;
`scripts/brza/tests` do workspace com 98 OK em 22,9 s; checador nas cinco árvores com 0 erros; os três blocos do
critério da MIG-001 com saída 0. Nenhum `--apply`, commit, push, rebuild ou reserva.

## Rodada dos destinos

Rodada 14 do PLN-008, respondida por Anderson em 2026-11-03, na sessão `workspace-a6`:

- **A1:** "Aviso, passo novo P8 (Recomendado)".
- **A2:** "Norma volta ao D2 (Recomendado)".
- **A4:** "Tirar o texto do link".
- **A3, A5, A6, A7, A8:** "A5, A7: issues no workspace", "A6: fechar 2 issues", "A3, A8: descartados".
