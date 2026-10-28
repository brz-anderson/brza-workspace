---
scope:
  - workspace
  - brza-studio
---

# O PLN-002 escrito: os comandos brza, com as rodadas de desenho

O pedido de Anderson, em 2026-10-28, na sessão `pln-002-comandos-brza`: "Acione a plan-runner e escreva o PLN-002 a
partir de work/issues/os-comandos-brza-que-viram-o-pln-002.md: um passo por comando, com as rodadas dos pontos de
desenho listados na issue."

## O que se fez

- **O plano:** o [PLN-002: Os passos manuais que se repetem entre sessões viram comandos `brza`](../../plans/PLN-002-os-comandos-brza/PLN-002-plan.md),
  dividido em plano, entrevista e desenho. Foi aceito na R7.4 e está em `execution`, com o P1 a P8 e 18 h estimadas.
- **O Terreno:** levantado por um subagente Sonnet, só lendo os dois repositórios. Os fatos estão no "Apresentado antes"
  de cada rodada e no Terreno do desenho.
- **As rodadas:** sete, todas fechadas nesta sessão.
  - R1, o `tree`. A única resposta fora da recomendação foi o `--chat <nome>` opcional.
  - R2, o `dev` e o baseline.
  - R3, o `test`, o `app install` e o runtime.
  - R4, o `brza-install`, o `doctor`, o `note` e a ordem.
  - R5, o nome do `tree`, o `sessions` e o executor.
  - R6, onde mora o código do worktree.
  - R7, os pontos sem lastro do rascunho e o corte.
- **O P0:** o despacho foi feito pela `brza-cli-subcomandos` em `brza-studio@9a81e65c852`, combinado pelo correio. A
  reinstalação e a troca dos textos passaram ao P5, por resposta de Anderson a ela.

## O que se aprendeu

- **A `master` local do `brza-studio` fica atrás da `origin/master`, e o checkout principal fica sujo** com o trabalho
  de outras sessões. Por isso nenhum comando do PLN-002 parte dele.
- **O `chat-markdown-largura-e-links` não é worktree registrado:** é só um diretório com `.cache/`. O
  `git worktree prune` não o pega.
- **Ninguém mediu o que o `ditto` faz sobre o app aberto.** O C2 roda com o app fechado.

## O que ficou

- **O P1 ao P8:** cada passo abre numa sessão `pln-002-pN` do `brza-workspace`, a pedido de Anderson. O próximo é o P1.
- **A combinação com a `brza-workspace-2d`:** é o primeiro subpasso do P7, e Anderson reabre a sessão.
