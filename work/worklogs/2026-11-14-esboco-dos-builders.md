---
scope:
  - workspace
  - brza-workflow
tags:
  - planning
  - tooling
refs:
  - PLN-023
  - PLN-024
  - PLN-025
---

# O PLN-025 do esboço dos Builders foi aberto

Pedido de Anderson, em 2026-11-14: abrir só o plano do esboço dos Builders, sem executar passo.

## O que se fez

O `brza note plan-open esboco-dos-builders` no workstream `workspace` reservou o PLN-025. O plano está em [PLN-025: Cada execução de Builder deixa métrica, nota e persona calibrável](../../plans/PLN-025-esboco-dos-builders/PLN-025-plan.md), com `phase: interview` e `status: open`. A R1 está enviada e sem resposta. D1 a D4 estão como recomendação. P1 a P6 estão desmarcados.

O desenho reaproveita o hook em `measure.py`, a telemetria `route`, o `brza quota` e o resumo que já existe. A nota de feedback recomendada é um gênero `work/feedbacks/`. O catálogo recomendado é `.brza/personas.toml`, ao lado do manifesto do PLN-024. O gate do [PLN-023: O plano novo do playground mostra a pendência, o dono e quem pode executar](../../plans/PLN-023-gates-do-plano/PLN-023-plan.md) entra só como forma de "quem destrava". O exemplo da execução desta sessão, `grok-4.7` com esforço `high` depois da recusa de `claude-opus-5-5`, está no D2 do plano.

O `brza-workflow` não foi editado. A branch `builder/bob-the-builder` não foi tocada.

## O que ficou

A resposta da R1. Sem ela, nenhum P roda. Os números do ciclo (3, 2 e 5) ficam para uma R2, quando houver notas.
