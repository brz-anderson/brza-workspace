---
status: open
description: Sem o resolver.tev1_min_confidence calibrado, todo desempate do MCP vai ao Haiku (~3,5 s e até US$ 0,01); calibrado com casos reais, o tev1 carregado resolve em ~15 ms.
scope:
  - workspace
opened: 2026-11-03
priority: low
tags:
  - tooling
---

# O limiar do tev1 sem calibração

No C2 do [PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md),
em 2026-11-03, o `Resolver` real (`brza-workflow@007383a`) desempatou duas tarefas com o Ollama e o Haiku de verdade:

- **Sem limiar**, o padrão da R2.2, todo desempate foi ao Haiku: 3,2 s a 3,7 s de Haiku, mais o `tev1`, que levou
  1,6 s a frio e 7 ms a 145 ms carregado.
- **Com o limiar 0,5**, só de teste, a tarefa de desenho ficou no `tev1` (confiança 0,55), em 15 ms. A de contagem, com
  confiança 0,41, foi ao Haiku.
- **O `keep_alive` é de 1 min**: pedidos espaçados encontram o modelo frio.

Anderson aprovou o C2 com esta issue: "Aprovado + issue do limiar".

## O que falta

Calibrar o `resolver.tev1_min_confidence` com casos reais: as escolhas do `tev1` e do Haiku nos pedidos que passarem
pelo MCP, e os casos de `tests/mcp/fixtures/m11_cases.json`. Depois, gravar o limiar no `brza.toml`, e talvez revisar o
`resolver.tev1_keep_alive`.

O gatilho é o volume de `dispatch` fazer pesar os ~3,5 s do Haiku em cada desempate. Hoje é um pedido por vez.
