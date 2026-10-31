---
status: open
scope:
  - workspace
opened: 2026-10-31
owner: Anderson
trigger: Anderson confirma ou recusa o texto, por frase explícita, antes do P8 do PLN-006 levar o índice à master.
tags:
  - tooling
---

# O índice de notas mora na `master`, a única exceção à regra da norma

**Proposta.** A `master` do workspace guarda a norma e, como única exceção, o índice `.brza/index.jsonl`: uma linha por
plano, issue ou decisão criada ou alterada, em qualquer workstream, para que quem coordena veja todas as frentes num
arquivo só. Só o `brza note` acrescenta — o `plan-open`, que reserva o número do plano, e o `commit`, quando o
frontmatter, o H1 ou o caminho da nota muda —, por commit sem checkout, e ninguém edita.

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

## O que falta

A confirmação de Anderson. A regra do PLN-006 ("escolha sempre o recomendado") escolhe a opção de rodada, mas não é a
frase explícita que transforma esta proposta em decisão.
