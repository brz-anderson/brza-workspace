---
status: open
description: Usar o tev1:4b local como classificador barato nos scripts da meeting-runner — gatilho da rodada extra, reserva do classify_vote e estado da persona —, depois de calibrá-lo com os pares reais das três reuniões.
scope:
  - workspace
  - brza-workflow
opened: 2026-11-09
tags:
  - tooling
---

# O `tev1` local classifica nos scripts da meeting-runner, depois de calibrado com as três reuniões

Proposta registrada por pedido de Anderson na sessão do `tools-kit`, em 2026-11-09. Pergunta: "o `tev1` rodando no
`Ollama` pode ser útil no fluxo que foi montado no `PLN-017`?". Resposta na rodada: "Issue no playground (Recomendado)".
Sem pedido de execução: a issue registra a proposta e o teste.

Origem: [PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md),
nas [Pendências conhecidas](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md#pendências-conhecidas).
Toca a promoção em [A meeting-runner chega ao core depois de duas reuniões sem desvio](promocao-da-meeting-runner-apos-duas-reunioes-sem-desvio.md):
o que entrar nos scripts antes dela conta nas duas reuniões sem desvio.

## O que é o `tev1`

O `tev1:4b` é um Qwen 3.5 de 4,2B ajustado para escolher uma opção numa lista fechada, com `num_ctx` 2048 e
`temperature` 0 (`ollama show tev1:4b`). Só responde pelo `/v1/systemone` do Ollama; o `/api/generate` devolve "does
not support generate". **Entra como classificador, nunca como persona, síntese ou revisor.**

O formato da chamada e a cadeia `tev1` → Haiku → tabela já existem em
`~/Projects/brza-workflow/packages/mcp/brza_mcp/resolver.py` (PLN-009/P4, `8801c77`), para reaproveitar. O
`resolver.tev1_min_confidence` está sem valor de propósito (R2.2 do PLN-009): sem limiar, tudo vai ao Haiku.

## Onde cabe, em ordem de valor

1. **O gatilho da rodada extra (R8/R9 do PLN-017).** Um script cruza cada fato novo (M#) com cada voto da rodada e
   grava os pares suspeitos no `estado-rN.json`, para que a coordenação não dependa de lembrar — o X10 da P7, em que o
   M6 (0 PRs) contradizia os votos de Trava e Relance. Quem participa continua com a coordenação (R9). O `tev1` não
   decide sozinho que não há gatilho: a dúvida sobe ao Haiku ou à coordenação.
2. **A reserva do `classify_vote`** (`.claude/skills/meeting-runner/scripts/tally.py:226`). O voto em texto livre, que
   hoje sai `None`, passa ao `tev1`, com um aviso no estado.
3. **O estado da persona no painel:** recusa, sem cota, erro ou respondeu, a partir da última resposta truncada para
   caber em 2048 tokens. Liga-se a
   [O brza sessions distingue o estado do worker do estado do Dispatch](estado-do-worker-e-eventos-no-brza-sessions.md).

## O teste de 2026-11-09

Quatro casos sintéticos no formato da P7, pergunta `gatilho` com `sim`/`nao`. O script ficou em
`/private/tmp/tev1_probe.py`, fora do git.

| Caso | Esperado | `tev1` | Probabilidade da escolhida | `confidence` | Tempo |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Trava × M6 (0 PRs) | sim | sim | 0,72 | 0,15 | 1,5 s (frio) |
| Prumo × M6 | não | não | 0,91 | 0,57 | ~100 ms |
| Relance × custo do runner | sim | sim | 0,86 | 0,42 | ~100 ms |
| Régua × fato sem relação | não | não | 0,97 | 0,80 | ~100 ms |

Acertou 4 de 4, sem custo e com saída determinística: o mesmo resultado nas duas rodadas. **A fraqueza está no "sim"**,
que é o caso caro: as duas menores `confidence` são os dois gatilhos verdadeiros. Quatro casos sintéticos não calibram
nada.

## Primeiro passo: calibrar antes de qualquer código

Montar os pares reais de voto × fato das três reuniões, das fixtures em
`.claude/skills/meeting-runner/scripts/tests/fixtures/` (`reuniao-carvao.json`, `reuniao-mcp-remoto.json` e `p7/`),
com o esperado de cada par marcado à mão. Medir, por limiar de `confidence`, o acerto e o **falso negativo** — o
gatilho perdido —, que é o erro que importa. Só com essa tabela se decide se o item 1 entra, com que limiar e onde a
dúvida sobe ao Haiku; os itens 2 e 3 esperam o mesmo resultado.
