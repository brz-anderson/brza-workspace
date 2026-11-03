---
scope:
  - workspace
  - tools-kit
---

# A fila do coordenador vai ao PLN-003

## O que se fez

- **O spike do C5 foi à sessão `tools-kit`.** A pedido de Anderson, esta sessão mandou à `tools-kit` duas mensagens:
  "retome o PLN-003 pelo Retomar", e depois "rode o spike do C5 até o final, se conseguir", abrindo uma issue para cada
  problema e seguindo em frente.
- **O coordenador virou o orquestrador do PLN-003.** Anderson pediu que o coordenador/orquestrador "prioriza a fila
  considerando a prioridade do pedido - issue high, bloqueia avanço de plano, prazo de entrega curto e etc -, o limite
  de workers em paralelo é geral do workspace somado, o cálculo também leva em consideração ritmo das contas e o recurso
  disponível na máquina pra limitar workers". O que já havia: a R7.1 do PLN-003 ("por conta e por runtime", pelo
  `usedPercent`), o M8 sem ordem de prioridade (`PLN-003-design.md:193`), e as notas com `priority`, `blocks` e
  `deadline` (`work/README.md`, "As propriedades") que o índice da `master` não grava.

## A rodada (2026-11-03)

- Coordenador e orquestrador: **"A mesma peça (Recomendado)"**.
- A ordem da fila: **"A ordem da norma (Recomendado)"** — `deadline`, `blocks`, `priority`, chegada.
- O teto geral: **"Soma às camadas (Recomendado)"** — o teto do workspace, o da conta e runtime (R7.1) e o da máquina;
  o menor manda.
- O ritmo e a máquina: **"Projeção e memória (Recomendado)"** — o `usedPercent` projetado até o `resetsAt`, e a memória
  livre e o swap, com a CPU como segundo sinal.

A issue [O coordenador se baseia no índice de notas da master](../issues/o-coordenador-le-o-indice-da-master.md) fechou
com o desfecho, e o registro no PLN-003 foi pedido à sessão `tools-kit`, para depois do spike.
