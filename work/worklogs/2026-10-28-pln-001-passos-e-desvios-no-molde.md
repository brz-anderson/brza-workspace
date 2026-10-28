---
scope:
  - workspace
date: 2026-10-28
tags:
  - tooling
---

# Os Passos e os Desvios do PLN-001 levados ao molde, depois da Run do P44 ao P50

Anderson pediu, na sessão `pln-001-molde`, para trabalhar a issue
[Os Passos e os Desvios do PLN-001 no molde, depois da Run do P44 ao P50](../issues/pln-001-passos-e-desvios-no-molde-depois-da-run.md),
porque a Run `run_de875fc52a75` tinha fechado no `b102c91` com os Desvios do X1 ao X20. O plano é o
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md).

## A rodada

- **As horas:** "Recalcular pelas linhas (Recomendado)". O frontmatter vinha de somas encadeadas e não batia com as
  linhas: o `executed_h` ficava 0,8 h abaixo, e o `remaining_h` tinha 0,6 h sem origem no `git log`.
- **Os três testes a escrever:** "0,3 h cada no Estimado (Recomendado)", com o P42 como régua.
- **As rodadas gravadas dentro dos passos:** "Para a Entrevista, como R45 a R47 (Recomendado)".

## O que mudou no plano

- **Os Passos sem fases.** Os `### F1` a `### F7` saíram, e cada `#### P<n>` virou `### P<n>`. O que o F7 dizia — o
  executor, a conferência no BrzA Studio e a ordem de execução — foi para a introdução dos Passos, que também deixou de
  ser citação. Cada passo do chat ganhou o `executor` na linha do `Executa` (sessão do `brza-studio` ou worker do Orca,
  com a rodada que o escolheu) e o `Estimado` em parágrafo próprio.
- **As rodadas na Entrevista.** A R45 é o sync da v1.4.242 (P1, P40 e P41), a R46 é a sessão `pln-001-retomar` (R46.1
  a R46.6, com a resposta do import boundaries e a dos casos num build só), e a R47 são as respostas do P52. As R46 e R47
  gravam só a opção escolhida, porque o plano não guardou as outras. Cada passo cita a rodada numa linha.
- **Os Desvios em até duas linhas**, do X1 ao X22, cada um com o passo que afeta. A evidência do X8 (o run
  `40432265386`, o DMG de 250705822 bytes e o sha256) foi ao P1. Os desvios propostos no P53.4 e no P40 viraram o X21
  (o push com o import boundaries vermelho, pela R46.6) e o X22 (o tom `faint` sem medição, para o C10).
- **Os três testes** viraram o P26.4, o P43.4 e o P44.4, a pedir à sessão do `brza-studio`. A `## Regressão` aponta o
  subpasso de cada um, e a marca "teste a escrever" sai quando o teste entra.
- **O frontmatter:** `estimate_h` 124.5, `executed_h` 15.25 (o P53 com 1,1 h, contando o 0,5 h do P53.4) e
  `remaining_h` 11.7 (o P27, o P37 e o P54 ao P57, mais o 0,9 h dos testes); o `ready` sem o P53.4 e o P40.

O checador saiu com 0 erro.

## Fora da tarefa

No meio da sessão, Anderson pediu para parar um script que pedia a permissão de acessibilidade. Era um laço de outra
sessão de chat do BrzA Studio (o `zsh` 84442, filho do `claude` 39378), que rodava `brza computer permissions --json`
até 120 vezes. O classificador de permissões barrou o `kill`, por ser processo de outra sessão, e o comando ficou com
Anderson.

## Aberto

O P54 ao P57 do pedido 30 e os testes do P26.4, do P43.4 e do P44.4, numa sessão do `brza-studio`; os casos manuais
com Anderson.
