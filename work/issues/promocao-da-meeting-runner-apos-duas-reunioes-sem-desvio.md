---
status: open
description: Promover a meeting-runner ao core somente depois de duas reuniões sem desvio e tratar as pendências da revisão final.
scope:
  - workspace
  - brza-workflow
opened: 2026-11-09
priority: low
tags:
  - tooling
---

# A meeting-runner chega ao core depois de duas reuniões sem desvio

Destino de P8.2 do [PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md), ao workstream `workspace`. A skill permanece no `playground` até cumprir R2.1: duas reuniões sem desvio. **Contagem atual: zero.** P7 teve 19 desvios e usou scripts v1; os 300 testes da versão v2 não substituem reuniões reais. Não promover nesta execução.

## Antes da promoção

- Rodar e registrar duas reuniões reais pela integração v2, com painel e encerramento. Registrar desvios; não contar smoke como reunião.
- Tratar a issue [O brza sessions distingue o estado do worker do estado do Dispatch](estado-do-worker-e-eventos-no-brza-sessions.md) antes de depender desses ramos do CLI sem o contorno.
- Definir e implementar a reabertura por `fallback`: hoje não há caminho no script, e o mesmo nome com aba aberta volta `running:`. Não improvisar outra abertura com identidade incerta.
- Corrigir o cartão da coordenação sem dados: `tally.py:783` produz um dict com `None`; `panel.py:239,300-302` mostra `US$ 0 … até —`, contrariando `synthesis.md:81-82`. Ausência deve ficar explícita, sem virar zero.
- Afinar `check_briefing.py:27-30`: ainda ignora fatos como `codex 1.352 M tokens`, `média = 84` e `1.5GB` entre crases; acusa comandos legítimos como `sleep 5`. A conferência humana dos números continua necessária.
- Isolar a linha de base das avaliações do repositório novo e usar casos discriminantes. Os resultados 97%×73% e 100%×84% não demonstram ganho causal: houve vazamento, e o caso 6 não discrimina.

Evidência: [REV-023: A revisão final da meeting-runner v2 e os limites antes da promoção](../reviews/REV-023-pln-017-meeting-runner-v2-final.md). O custo/tokens do Grok tem destino próprio em [O custo e os tokens do Grok entram nas medições da reunião](custo-e-tokens-do-grok-nas-medicoes-da-reuniao.md).

Depois do critério cumprido, promover ao `core/` do `brza-workflow` por sessão do workstream dono, preservando R7, R8 e R9. A promoção não nasce do fechamento do PLN-017.
