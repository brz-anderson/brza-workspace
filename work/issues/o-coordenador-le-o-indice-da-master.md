---
status: open
scope:
  - workspace
opened: 2026-10-31
owner: Anderson
tags:
  - planning
---

# O coordenador se baseia no índice de notas da master

## O pedido

Na R4.3 do [PLN-006: O `brza init` monta a norma num workspace do zero](../../plans/PLN-006-o-brza-init-monta-a-norma-do-zero/PLN-006-plan.md),
Anderson trocou o contador "Último PLN usado" por "jsonl na master do *-workspace com titulo, descrição, status,
worktree/workstream e horário em que foi criado/alterado, assim o coordenador tem um indice pra se basear".

A R5 fechou o índice: planos, issues e decisões; uma linha por evento, só acrescentada, com `merge=union`; gravado pelo
`brza note`. A R5.4 deixou o coordenador fora do PLN-006, nesta issue.

## O que falta decidir

- **Quem é o coordenador**: uma sessão que abre e acompanha as sessões dos workstreams pelo `brza sessions`, um painel
  do BrzA Studio, ou outra coisa.
- **O que ele decide a partir do índice**: a ordem dos planos, a sessão a abrir, o bloqueio entre workstreams.
- **Se o índice basta**, ou se ele precisa de campo que o PLN-006 não grava — `blocks`, `priority`, `owner`.

O índice nasce no PLN-006; esta issue espera por ele.
