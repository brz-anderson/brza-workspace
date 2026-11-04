---
scope:
  - workspace
  - brza-studio
  - brza-workflow
tags:
  - planning
refs:
  - PLN-014
---

# Refinamento do radar do playground até a entrevista

## O que foi feito

Pedido de Anderson, nesta sessão: refinar as issues deste workstream, com coleta, auditoria, hipóteses, e só então abrir o plano, o terreno, a medição e as opções, deixando a entrevista por último.

1. **Coleta.** Três collectors. Há 15 issues `open` em `work/issues/`, não 14: 9 `high`, 4 `medium`, 2 `low`. Os 121 números citados existem em `stablyai/orca`. O agregado está em `/private/tmp/refino-playground/01-inventario.md`, `02-sobreposicao.md` e `03-medicoes.md`.
2. **Auditoria.** A classe "6 parciais, 8 ausentes" não se susteve. Ficou 0 cobertas, 4 parciais, 10 ausentes, 1 não verificada. Dos 12 `closed` no endpoint de issues, 8 PRs estão `MERGED`, 2 PRs fechados sem merge e 2 issues fechadas. O merge `14819eb8c043` do `#37774` não é ancestral do `brza-studio` `8f41dd56a336`. US$ 3,77 é o `playground` em 2026-11-03, não esta sessão. Pareceres em `04-auditoria-sobreposicao.md` e `05-auditoria-medicoes.md`.
3. **Hipóteses.** Três designers. A mínima recomenda não abrir plano e cumprir o `done` da issue de chats. A arquitetura recomenda uma decisão de despacho, sem porte. O equilíbrio recomenda um plano só da issue de hooks. Rascunhos em `06-hipoteses-minima.md`, `07-hipoteses-arquitetura.md` e `08-hipoteses-equilibrio.md`.
4. **Plano.** `brza note plan-open` reservou o PLN-014. O arquivo é [PLN-014: O refinamento do radar do playground chega à entrevista com as opções medidas](../../plans/PLN-014-refinamento-do-radar-do-playground/PLN-014-plan.md), `phase: interview`. O pedido desta sessão já tinha escolhido PLN em vez de worklog; a pergunta do plano não foi escolhida.
5. **Terreno e medição.** O padrão de setup é `run-by-default` (`src/shared/constants.ts:127`). `runApprovedSetup` não tem linha (`git grep` exit 1). A automação `f75b8281-8ae3-4558-afe4-7ab5bbc35601` está ligada e manda criar ou atualizar as issues; não diz que preserva emenda. Sete notas citam um dos doze números fechados. Agregado em `09-terreno.md`. O prompt foi relido em `profiles/local-default/profile-state.db`, só leitura.

## O que não foi decidido

A R1 está na mensagem desta sessão e ainda não tem resposta. Nenhuma issue mudou de `status`. Nenhum porte começou. A nota de Native Chat continua sem classe.

## Fora do workspace

Nada. A leitura do `profile-state.db` não alterou o arquivo.
