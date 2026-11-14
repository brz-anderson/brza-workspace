---
scope:
  - workspace
tags:
  - tooling
---

# A reunião smoke do PLN-026 não conta para a promoção

**SMOKE.** Esta reunião não conta para a promoção da meeting-runner. As duas posições ficam registradas. O modelo padrão não muda por causa dela.

Prova do P8 do [PLN-026: brza sessions e meeting-runner funcionam na cloud](../../plans/PLN-026-sessoes-e-meeting-runner-na-cloud/PLN-026-plan.md). R2.2: smoke, 2 personas, 1 rodada. Não conta para a promoção da meeting-runner.

## Pauta

Devemos manter `grok-4.7-low` como modelo padrão das personas de reunião smoke?

## Personas

| Persona | papel | modelo | modo |
| :------ | :---- | :----- | :--- |
| Arquiteto | propõe | grok-4.7-low | agent |
| Revisor | critica | grok-4.7-low | ask |

## Rodada 1

Duração da rodada: 82640 ms.

| Persona | turno | session_id | duração_ms | input | output | cache_read | cache_write | reasoning | custo |
| :------ | :---- | :--------- | ---------: | ----: | -----: | ---------: | ----------: | --------: | :---- |
| Arquiteto | open | `03906c4f-fb04-4cc4-b8a1-f00a329c8f44` | 2318 | 12993 | 75 | 5504 | 0 | 73 | ausente |
| Arquiteto | send | `03906c4f-fb04-4cc4-b8a1-f00a329c8f44` | 4445 | 288 | 236 | 18432 | 0 | 143 | ausente |
| Revisor | open | `de2b0a59-022f-409d-a39e-c8f27175bc72` | 2592 | 18808 | 78 | 0 | 0 | 76 | ausente |
| Revisor | send | `de2b0a59-022f-409d-a39e-c8f27175bc72` | 11223 | 513 | 553 | 18688 | 0 | 401 | ausente |

## Falas

### Arquiteto

Manter `grok-4.7-low` como padrão das personas de reunião smoke. O objetivo desse rito é exercitar pauta, turno e formato, não a qualidade máxima de raciocínio. Um modelo low reduz latência e custo, deixa o smoke repetível e evita que a reunião vire benchmark de modelo. Quem precisar de mais profundidade troca o modelo naquela rodada, sem alterar o padrão.

Posição: manter

### Revisor

O smoke não mede só pauta e turno: ele mede se a persona cumpre o contrato da fala — limite de palavras, idioma, fechamento com `Posição:` e uma crítica que não ecoa o turno anterior. `grok-4.7-low` barateia a rodada e mascara falha de instrução; um passe verde vira falso positivo do rito que vai para o modelo real. Repetibilidade também piora quando o low oscila no formato. Profundidade extra continua opcional, mas o padrão do smoke deve ser o mesmo modelo das personas em reunião de verdade. Trocar o default alinha o sinal do smoke com o que o rito de fato protege.

Posição: trocar

<!-- fim-rodada-1 -->
