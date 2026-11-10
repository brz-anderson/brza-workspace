---
status: open
description: O brza note commit grava o custo e a sessão de quem commita em todo worklog do commit, também nos das personas de uma reunião, depois do marcador de fim de rodada.
scope:
  - brza-workflow
opened: 2026-11-09
priority: medium
tags:
  - tooling
---

# O brza note commit grava o custo da coordenação no worklog de cada persona

## O pedido

Registrado pela sessão da meeting-runner do `playground`, em 2026-11-09, por decisão de Anderson em rodada:
"tally tolera + issue ao tools-kit (Recomendado)". A rodada está no PLN-017 do `playground`, como Rodada 10.

## O que acontece

A coordenação de uma reunião multiagente commita os worklogs das personas junto com o dela, num `brza note commit`
só. Para cada worklog do commit, `prepare_worklog_measure` (`~/Projects/brza-workflow/bin/brza-note:860-873`) faz duas
coisas:

- **Acrescenta a sessão de quem commita** ao `sessions:` do frontmatter. Nas personas, essa é a sessão da coordenação, e
  não a delas.
- **Grava a seção `## Custo da tarefa` no fim do arquivo,** com a medida da tarefa da coordenação. Na reunião do `tev1`, os
  seis worklogs de persona ganharam a mesma linha: "US$ 2,48 … dividida com 6 outros worklogs do commit".

A seção cai **depois** do marcador `<!-- fim-rodada-N -->`, que a meeting-runner exige na última linha do arquivo. O
`tally.py` passou a ler as seis personas como "atrasado", e o painel da última rodada saiu "0 de 6" até a coordenação
regenerá-lo a partir de cópias cortadas no marcador. A meeting-runner agora tolera o bloco final `## Custo da tarefa`
(PLN-017/R10.4), mas o dado gravado continua errado.

## O que se espera

O custo e a sessão de quem commita vão só ao worklog da tarefa dessa sessão. Uma forma possível:

- **Só os worklogs da sessão:** gravar só no worklog cujo `sessions:` já traz a sessão, ou no que o comando recebeu
  primeiro.
- **Ou uma flag:** `--measure <worklog>` para escolher o worklog medido.

O worklog de persona fica como a persona o deixou.

## Como se confere

`brza note commit` com o worklog da coordenação e dois de persona: só o da coordenação ganha `sessions:` e `## Custo da
tarefa`; os de persona continuam terminando no marcador.
