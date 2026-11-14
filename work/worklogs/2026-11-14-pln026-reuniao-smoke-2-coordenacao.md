---
scope:
  - workspace
tags:
  - tooling
---

# A segunda reunião smoke do PLN-026 não conta para a promoção

**SMOKE.** Esta reunião não conta para a promoção da meeting-runner. As duas posições ficam registradas. O modelo padrão não muda por causa dela.

CloudRuntime: `e07fd479fef2b5cc7e3656ca0e2cb6a05ec9274b` em `packages/client/bin/cloud_runtime.py`, ainda fora da master do brza-workflow.

Segunda prova do P8 do [PLN-026: brza sessions e meeting-runner funcionam na cloud](../../plans/PLN-026-sessoes-e-meeting-runner-na-cloud/PLN-026-plan.md), depois da revisão xhigh. R2.2: smoke, 2 personas, 1 rodada. Não conta para a promoção da meeting-runner.

## Pauta

Devemos manter `grok-4.7-low` como modelo padrão das personas de reunião smoke?

## Personas

| Persona | papel | modelo | modo |
| :------ | :---- | :----- | :--- |
| Arquiteto | propõe | grok-4.7-low | agent |
| Revisor | critica | grok-4.7-low | ask |

## Rodada 1

Duração da rodada: 68809 ms.

| Persona | turno | session_id | duração_ms | input | output | cache_read | cache_write | reasoning | custo |
| :------ | :---- | :--------- | ---------: | ----: | -----: | ---------: | ----------: | --------: | :---- |
| Arquiteto | open | `211351c1-238c-4c23-846a-3bddb1d42bcd` | 2790 | 12993 | 80 | 5504 | 0 | 78 | ausente |
| Arquiteto | send | `211351c1-238c-4c23-846a-3bddb1d42bcd` | 5484 | 293 | 248 | 18432 | 0 | 123 | ausente |
| Revisor | open | `5cc0b286-8663-4800-b2ef-e11586f7fd6b` | 2688 | 12664 | 77 | 6144 | 0 | 75 | ausente |
| Revisor | send | `5cc0b286-8663-4800-b2ef-e11586f7fd6b` | 8894 | 18080 | 405 | 1152 | 0 | 280 | ausente |

## Falas

### Arquiteto

Para reuniões smoke, o critério é custo, latência e formato estável, não profundidade de raciocínio. `grok-4.7-low` cobre o que a pauta pede: posição curta, em português, com fechamento binário. Trocar o padrão agora mistura qualidade de modelo com o sinal que o smoke deve medir — se a persona cumpre o protocolo. Modelos mais capazes ficam para a pauta real, quando houver divergência ou decisão de produto. Manter o low como padrão preserva o teste barato e repetível.

Posição: manter

### Revisor

O critério de custo e latência está certo, mas o low não entrega o formato estável que o smoke precisa medir. Em pauta curta ele escapa do português, estoura o limite de palavras ou omite o fechamento binário. Aí a falha não distingue persona de modelo: o teste acusa o protocolo quando o defeito é capacidade. Manter o low como padrão torna o sinal barato e também ruidoso. Um modelo um degrau acima, ainda barato, segura o contrato da rodada e deixa a profundidade para a pauta real.

Posição: trocar


<!-- fim-rodada-1 -->
