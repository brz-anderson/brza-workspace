---
status: done
scope:
  - workspace
opened: 2026-10-31
decided: 2026-11-02
decided_by: Anderson
tags:
  - tooling
---

# O índice de notas mora na `master`, a única exceção à regra da norma

A `master` do workspace guarda a norma e, como única exceção, o índice `.brza/index.jsonl`: uma linha por
plano, issue ou decisão criada ou alterada, em qualquer workstream, para que quem coordena veja todas as frentes num
arquivo só. Só o `brza note` acrescenta — o `plan-open`, que reserva o número do plano, e o `commit`, quando o
frontmatter, o H1 ou o caminho da nota muda —, por commit sem checkout, e ninguém edita.

Decidido por Anderson em 2026-11-02, na R17.1 do PLN-006: "decidido, agora".

## De onde vem

Na R4.3 do [PLN-006: O `brza init` monta a norma num workspace do zero](../../plans/PLN-006-o-brza-init-monta-a-norma-do-zero/PLN-006-plan.md),
Anderson trocou o contador "Último PLN usado" por "jsonl na master do *-workspace com titulo, descrição, status,
worktree/workstream e horário em que foi criado/alterado, assim o coordenador tem um indice pra se basear". A R5 fechou
o índice — planos, issues e decisões; só acrescenta, com `merge=union`; gravado pelo `brza note` —, e a R8.4 mandou
registrar a exceção nesta nota.

## A relação com a decisão de 2026-10-30

[As notas moram em workstreams, e a `master` guarda só a norma](as-notas-moram-em-workstreams-e-a-master-guarda-so-a-norma.md)
recusou um passo de subida à `master` a cada fechamento. O índice é esse passo, aceito só para a linha do índice: a
nota continua morando no workstream, e a regra de antes segue valendo para ela. Por isso esta nota não a substitui, e
não há `superseded_by`.

## Onde já está escrita

O texto do `AGENTS.md`, do `work/README.md`, do `plans/README.md` e da `plan-runner` está no núcleo, em
`brz-anderson/brza-workflow@8b2a355`, e chega ao `brza-workspace` no P8.

## A alternativa recusada

Recusar o índice e voltar ao contador "Último PLN usado" na `master`: custava ~2 h para desfazer o P4 e a norma, e
deixava quem coordena sem uma visão das frentes num arquivo só.
