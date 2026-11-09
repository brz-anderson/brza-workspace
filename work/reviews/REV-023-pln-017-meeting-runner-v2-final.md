---
status: done
description: Conferência independente de d12ed91 e db619ac com 300 testes, A1-A4 resolvidos e resíduos com destino explícito.
scope:
  - workspace
opened: 2026-11-09
completed: 2026-11-09
tags:
  - tooling
---

# REV-023: A revisão final da meeting-runner v2 e os limites antes da promoção

Revisor independente Claude `reviewer`, com `skill-creator`; Dispatches `ctx_9c4702bb2c23` e `ctx_94cc8fa2b15b`. Alvos: `d12ed91` e correção `db619ac`. Régua: D1 e R7/R8/R9 do [PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md).

## Achados resolvidos

- A1: o verificador ignorava números acompanhados de unidade, moeda, razão e diff entre crases. Corrigido em `db619ac`, confirmado com sondas próprias do revisor e comparação dentro/fora de crase.
- A2: `--status` sem espera sai 0 mesmo com `failed`. Documentado como consulta; `--wait-settled` continua gate. Evidência: `launch_persona.py:426`, `SKILL.md:208-211`, `closing.md:57-58`.
- A3: títulos sugeriam subconjunto fixo. Corrigidos conforme R9: participantes escolhidos com motivo, sem composição fixa. Evidência: `SKILL.md:124-125`, `round-request.md:180`.
- A4: custo de Codex/Claude fora da rodada aparecia nos rótulos. Corrigido e conferido no painel e tally com subconjunto e sala inteira.

## Resíduos com destino

### R1 — Heurística de código ainda ignora alguns fatos e acusa alguns comandos

> bug · sugestão · confiança 95 · → issue promoção-da-meeting-runner-apos-duas-reunioes-sem-desvio

**Evidência:** `check_briefing.py:27-30`; entre crases passam `codex 1.352 M tokens`, `claude 3 sessões`, `média = 84`, `latência < 5 s`, `1.5GB`; fora são acusados. Comandos como `sleep 5` dão falso positivo seguro. A conferência humana permanece exigida.

### R2 — Cartão atribui zero à coordenação sem medição

> bug · sugestão · confiança 95 · → issue promoção-da-meeting-runner-apos-duas-reunioes-sem-desvio

**Evidência:** `tally.py:783`, `panel.py:239,300-302`, contra `synthesis.md:81-82`; `custos_coordenacao` com valores `None` gera `US$ 0 … até —`. Reproduzido no painel da R3 de P7.

Destinos: [A meeting-runner chega ao core depois de duas reuniões sem desvio](../issues/promocao-da-meeting-runner-apos-duas-reunioes-sem-desvio.md) e, para o defeito externo, [O brza sessions distingue o estado do worker do estado do Dispatch](../issues/estado-do-worker-e-eventos-no-brza-sessions.md).

## Verificação e limites

O revisor refez 300 testes: OK; sondas de briefing com 11/9 itens acusados, 32 fatos comparados dentro/fora de crase e 28 trechos de código, além de painel por PNG a 736 px. Confirmou preservação de eventos fora do subconjunto, falha após auto-release e R8/R9. Resíduos não bloqueiam P8, conforme conclusão independente.

Sem reunião real pelos verbos v2 e sem promoção. Avaliações com vazamento da linha de base não provam ganho causal. Relatórios integrais preservados no scratch do reviewer, sessão `ce34545d-b2d8-433c-baf1-bdf361ad2b39`: `relatorio-conferencia-final-d12ed91.md` e `relatorio-reconferencia-db619ac.md`.
