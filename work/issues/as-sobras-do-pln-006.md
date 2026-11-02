---
status: open
description: Seis sobras do PLN-006 que as rodadas deixaram para depois, do nome fixo do código ao plano longo demais.
scope:
  - workspace
opened: 2026-11-02
owner: Anderson
tags:
  - tooling
---

# As sobras do PLN-006 no brza-workflow e no plano

## O pedido

O [PLN-006: O `brza init` monta a norma num workspace do zero](../../plans/PLN-006-o-brza-init-monta-a-norma-do-zero/PLN-006-plan.md)
fechou com estas pendências, cada uma deixada para depois por uma rodada decidida pela regra de Anderson, "escolha
sempre o recomendado":

- **O nome fixo do código.** O `brza_runtime` ainda cai no `~/Projects/brza-studio` quando a `STUDIO` não vem do
  registro nem do manifesto, porque o `runtime.git` e o `brza-doctor` não aceitam o código ausente. Vem da devolução
  do conserto da segunda revisão, ponto 2.
- **O app no pacote do cliente.** A seção do scratch e dos artboards em `packages/client/core/.claude/rules/brza-client.md`
  usa `~/Library/Application Support/{{code.name}}/`, e erra quando o nome do código difere do nome do app. O conserto
  é uma tabela `[app]` no manifesto. Vem do conserto da primeira revisão, ponto 2.
- **O parágrafo do scratch do chat no `core/CLAUDE.md`**, o do "hash de 32 caracteres", ainda é texto do app no
  núcleo. Vem do conserto da primeira revisão, ponto 3.
- **O `--rebuild` e o rename com `--no-push`** dão um `created` duplicado no índice, e a nota movida sem mudança de
  conteúdo mantém o workstream antigo, porque o `workstream` não entra na comparação. Vem do conserto da primeira
  revisão, pontos 4 e 7.
- **O `ref` do lock** pode ficar velho até o próximo arquivo mudado, porque o sync só regrava o lock com arquivo mudado
  (A4 da segunda revisão).
- **O `PLN-006-plan.md` passou de 900 linhas**, e a norma manda levar a Entrevista ao `PLN-006-interview.md` acima de
  ~400. A mudança só move texto e ficou para depois do fechamento.

## O que falta decidir

Qual delas vale um conserto, e quando. Nenhuma trava o uso de hoje, que é um workspace só, com o código no mesmo nome
do app.
