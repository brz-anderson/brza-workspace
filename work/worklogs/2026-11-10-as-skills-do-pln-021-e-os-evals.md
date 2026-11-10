---
scope:
  - workspace
tags:
  - tooling
  - planning
refs:
  - PLN-017
  - PLN-021
sessions:
  - 31cf964e-5b71-41bf-b845-36e86d01f0d7
---

# As skills do PLN-021 escritas e os evals da iteração 1

O [PLN-021: O plano roda por uma sessão coordenadora, com scripts de apoio e artboards de tela](../../plans/PLN-021-o-plano-coordenado-e-os-artboards/PLN-021-plan.md)
saiu da entrevista e foi à execução. Anderson pediu, em 2026-11-09: "registres as opções em Desenho e as rodadas em
Entrevista, retomaremos o plano amanhã, siga direto para escrever as skills", e depois "em seguida, já roda os evals".

## O que se fez

### O Desenho e a rodada 4

- **O Desenho** do `designer` foi a `PLN-021-design.md` como estava, com D1 a D7, os evals e as escolhas sem lastro.
- **A rodada 4** foi à Entrevista sem resposta, com oito pontos e seis escolhas menores. A execução seguiu as
  recomendadas, que ficam a confirmar e não são decisão.

### Os passos, por `implementer` (X1: não por sessão aberta pelo `brza sessions`)

- **P1:** o `.claude/scripts/skillkit/` (mapa de sessões, verbos do `brza sessions`, medição, visual com PNG pelo
  `brza shot`). A `meeting-runner` passou a importar dele sem mudar um teste: 55 testes do kit e 323 da `meeting-runner`.
- **P2:** o `plan_md.py` e os quatro scripts da R2.2, com 84 testes. Rodados nos planos reais, acharam no PLN-017 o P7
  sem evidência que se refaça e o `executed_h` que não bate. Não mexi no PLN-017; o achado fica para a R4.
- **P3 a P5:** o `executor.py`, o `plan_panel.py` e o `consult.py`. A suíte foi a 151 testes. A prova de ponta a ponta
  rodou com um `brza` falso, que registra as chamadas sem abrir sessão (`/private/tmp/pln021/evals/bin/brza`).
- **P7:** os scripts da `screen-artboards`, com 48 testes, cinco molduras, o pacote `brza-studio` extraído do código
  (188 tokens) e o `neutral`. Li 14 PNGs.

### A escrita, pela coordenação, com a `skill-creator`

- **O `plan-runner` (P6):** a `SKILL.md` foi reescrita como sessão coordenadora, com a tabela "Preciso de… / Leia /
  rode", quem é quem e duas invariantes novas. Vieram cinco references novas (`design`, `consultants`, `step-request`,
  `review`, `narration`), e três foram reescritas (`open-and-plan`, `conduct`, `close`), além do molde.
- **A `screen-artboards` (P7):** a `SKILL.md` e quatro references (`frames`, `tokens`, `chat-rules`, `design-round`).

### Os evals

- **Onde rodaram:** cópias isoladas do repositório, num git novo, sem o PLN-021, com o plano de mentira PLN-901 e o
  `brza` falso.
- **`plan-runner`, versão nova contra a antiga:** 17/17 × 9/17, delta +0,44.
  - Executar o passo por sessão: 7/7 × 2/7.
  - Consultores em sessão na decisão cara: 5/5 × 3/5.
  - Retomar: 5/5 × 4/5. Empata no diagnóstico e só difere no uso do script.
- **`screen-artboards`, com e sem a skill:** 13/13 × 12/13, delta +0,08.
  - O caso de desktop empata em 7/7: a linha de base achou as regras do chat no repositório.
  - O caso de mobile e web só separa as duas na página web num artboard só, que é a regra da R4.5, ainda a confirmar.
- **O que os evals corrigiram na skill:**
  - o `$A`/`$S` como abreviação falha no zsh;
  - o `tokens.py list <projeto>` não existe;
  - o fragmento responsivo do `browser` precisa de `@container`, porque `@media` lê o viewport do chat;
  - telas distintas saem sem letra.
- **Os visualizadores:** `/private/tmp/pln021/plan-runner-review.html` e `/private/tmp/pln021/screen-artboards-review.html`.

## O que ficou aberto

- **O código não foi commitado:** `.claude/scripts/`, as duas skills e a migração da `meeting-runner`. Fica para Anderson.
- **A R4 inteira e os desvios X2 a X5**, que estão no plano.
- **A fixture do PLN-901 cita um commit (`4c1d9e2`) e um arquivo que não existem no `brza-studio` real.** A versão antiga
  do eval do executor parou nisso, e não por falta de regra. A iteração 2 precisa de uma fixture que não aponte para o
  repositório real, ou de um commit verdadeiro.

## Para a norma

- **O `brza` falso para eval de skill que abre sessão** serve a qualquer skill do `core/`. Ele mora no scratch e
  é candidato a `tests/` do `brza-workflow` quando a `plan-runner` for promovida.

## Custo da tarefa

Corrido 44 min — agente 18 min, quem pediu 26 min, pausa 0 s · US$ 15,03 (turnos 9,14, subagentes 5,89) · CPU 2 min do `claude` e 6 min dos comandos, RSS até 623 MB · 15 turnos, 1 sessão · até 00:22 de 2026-11-10, pelo `brza note commit`
