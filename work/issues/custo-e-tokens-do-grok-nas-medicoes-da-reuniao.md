---
status: open
description: Integrar os tokens e o custo disponíveis no usage.json do Grok ao CLI e às medições da reunião, conferindo unidade e agregação antes de somar.
scope:
  - workspace
  - brza-workflow
opened: 2026-11-09
priority: low
tags:
  - tooling
---

# O custo e os tokens do Grok entram nas medições da reunião

Correção factual ao [PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md). O levantamento dizia que Grok não tinha tokens/custo em disco. O CLI e a skill ainda o mostram como `unmeasured`, mas os dados existem. Esta issue registra a integração futura, sem ampliar a execução atual das correções após P7.

## Evidência

Leitura em 2026-11-09 de `~/.grok/sessions/%2FUsers%2Fandepb%2FProjects%2Fbrza-workspace%2F.worktrees%2Fplayground/01a1c119-2faf-71f0-9d21-dfd87c062873/usage.json`: `session.inputTokens=2632760`, `outputTokens=24264`, `costUsdTicks=18738880000`; quatro `turns[]` somam os mesmos valores. A escala informada pelo levantamento recebido é 10^10 ticks/US$, o que dá US$ 1,873888 neste exemplo; a unidade no produtor ainda precisa de conferência.

O levantamento também informa que o pai já inclui o consumo dos subagentes. Essa agregação ainda precisa de validação antes da implementação, para não somar o mesmo consumo duas vezes. Antigravity não foi reconferido; a correção não se estende a ele nem recalcula retroativamente as reuniões de origem.

## Trabalho pendente

- No `tools-kit`, integrar a fonte a `brza sessions usage`, identificando a sessão exata pelo provedor e cwd.
- Na skill `meeting-runner`, integrar o resultado ao `tally.py` e ao painel, com janela por turno, dados ausentes explícitos e distinção de total de sessão.
- Conferir escala monetária e agregação pai/subagente; testar com fixtures fiéis ao formato observado, inclusive sessão ausente e atualização parcial.

Aceite: custo e tokens do Grok com fonte e janela explícitas; sem dupla contagem e sem transformar ausência de dados em zero. A promoção da skill ao `core/` continua condicionada a duas reuniões sem desvio.
