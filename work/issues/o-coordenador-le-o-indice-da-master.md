---
status: done
scope:
  - workspace
opened: 2026-10-31
completed: 2026-11-03
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

## Desfecho (2026-11-03)

Anderson pediu, na sessão do `workspace`: o coordenador/orquestrador "prioriza a fila considerando a prioridade do
pedido - issue high, bloqueia avanço de plano, prazo de entrega curto e etc -, o limite de workers em paralelo é geral
do workspace somado, o cálculo também leva em consideração ritmo das contas e o recurso disponível na máquina pra
limitar workers". A rodada que seguiu respondeu:

- **"A mesma peça (Recomendado)":** o coordenador é o orquestrador do PLN-003, o MCP da fila, da conta e do runtime.
  Esta issue fecha aqui e segue no [PLN-003: O workflow do workspace roda igual no BrzA Studio e no Orca, por plugins e pelo `brza`](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md),
  no workstream `tools-kit`.
- **"A ordem da norma (Recomendado)":** a fila ordena por `deadline` próximo, depois `blocks`, depois `priority`
  (`high`, `medium`, `low`), depois a chegada; `blocks` vence `priority` quando discordam. Por isso o índice da `master`
  passa a gravar `priority`, `blocks` e `deadline` — a resposta ao terceiro ponto acima.
- **"Soma às camadas (Recomendado)":** o teto geral de workers do workspace soma-se ao limite por conta e runtime da R7.1
  do PLN-003 e ao da máquina; o menor manda.
- **"Projeção e memória (Recomendado)":** o ritmo é a variação do `usedPercent` projetada até o `resetsAt`, e a conta
  que chega a 90% antes do reset não recebe worker novo; a máquina limita pela memória livre e pelo swap, com a CPU como
  segundo sinal.
