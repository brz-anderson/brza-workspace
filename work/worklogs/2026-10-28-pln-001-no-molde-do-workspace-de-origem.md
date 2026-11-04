---
scope:
  - workspace
tags:
  - tooling
refs:
  - PLN-001
  - issue:pln-001-passos-e-desvios-no-molde-depois-da-run
---

# O PLN-001 conferido contra a norma de planos do workspace de origem e levado ao molde

Anderson pediu, numa sessão do `brza-workspace`, para conferir se o frontmatter e as seções do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md)
seguem a norma nova de planos do workspace de origem (o `plans/README.md`, o molde da `plan-runner` e o checador), trazer
a norma de lá se a daqui estivesse atrás, mostrar as divergências antes de escrever e combinar a escrita com a sessão
`pln-001-p44-p50`, que coordena a Run `run_de875fc52a75`.

## A norma daqui não está atrás

- **O brza-workspace nasceu depois do último commit de norma do workspace de origem**: o `0bc2c77`, de 2026-10-27 às
  23:49, contra o `3b6ecdb` do checador, às 18:53, e o `084fa47` da `plan-runner`, às 18:52, que o molde e o
  `conduct.md` daqui já trazem (o worklog gravado antes da linha do `## Worklogs`). O checkout local do plugin de lá
  está 17 commits atrás da origin; a comparação foi contra a `origin/master`.
- **As diferenças são adaptação**: sem card, sprint, `ticket`, skills donas, agentes do plugin nem o cofre de lá.
- **O checador do workspace de origem tem regras que não vieram**: `legacy-header-field`, `legacy-log-section`,
  `legacy-review-section`, `decided-by-field` e `repo-field`. Rodado com `--root .` aqui, deu 0 erro. Na rodada,
  Anderson escolheu "Não trazer (Recomendado)".

## O PLN-001

Os dois checadores davam 0 erro no PLN-001, e o frontmatter seguia o molde. As divergências eram de seção, e as rodadas
de 2026-10-28 fecharam assim:

- **O `Retomar`, de ~33 linhas:** "A coordenadora, ao fechar a Run (Recomendado)". A `pln-001-p44-p50` concordou, pela
  orquestração (`msg_9f6cc3585095`, em resposta ao `msg_086642c5bb73`), e também pelo correio.
- **As seções com gatilho:** "## Casos manuais", "## Restrições" e "## Regressão", as três.
- **O formato herdado do plano de lá:** "Levar tudo ao molde". A coordenadora respondeu "depois-da-run" para os Passos,
  os Desvios, a Entrevista e o frontmatter, onde ela grava a evidência de cada `worker_done`.
- **Os pontos dos rascunhos:** "D40: fechar o Em aberto (Recomendado)", sem as A1 a A3 no D35; os Contextos "Aceitar
  como estão (Recomendado)"; os testes que faltam, "Marcar e levar à issue (Recomendado)"; e, dos itens discutíveis da
  Regressão, o aviso de limite com ressalva e o merge pelo `--numstat`.

O que foi gravado:

- **No plano:** a crase na Origem da Cobertura; a `## Restrições`, com o operacional do `Retomar`; a `## Regressão`,
  com 13 itens; o `## Decisões`, com link e rodada (R10 e R14 do plano de origem); as `## Pendências conhecidas`; os 13
  casos da `## Casos manuais`; e o `## Fechamento` do molde.
- **No desenho:** a seção "O que este desenho assume" (os D1 a D35 remetidos ao plano de origem, e as decisões das R29
  a R44), e os 23 itens `D` com Origem, Contexto e `#### Como fica`. O D40 fecha com a resposta do P52.

O levantamento da Regressão e o rascunho do desenho foram feitos por subagentes Sonnet. A Regressão rodou 25 arquivos de
teste do `brza-studio`, com 359 testes passando, sem alterar o repositório.

## O que ficou aberto

- [Os Passos e os Desvios do PLN-001 no molde, depois da Run do P44 ao P50](../issues/pln-001-passos-e-desvios-no-molde-depois-da-run.md):
  os Passos sem fases, os Desvios em até duas linhas e os três testes "a escrever" da Regressão, numa sessão nova
  depois do último commit da Run.
- O `Retomar` numa linha fica com a `pln-001-p44-p50`, ao fechar a Run.
