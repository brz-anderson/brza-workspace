---
status: done
description: O plano novo do playground nasce com a pendência e o dono na tarefa, e com quem executa na tabela do open.
scope:
  - workspace
opened: 2026-11-10
decided: 2026-11-10
decided_by: Anderson
owner: Anderson
tags:
  - planning
---

# O plano novo do playground mostra a pendência na tarefa

Decidido por Anderson em 2026-11-10, com a palavra "gravar", na opção 1 da rodada em que a proposta v3 estava inteira na mensagem.

O plano novo deste workstream nasce com `## Passos` no lugar, a fase numa linha (`Espera:` com a fase que bloqueia e a pessoa que destrava) e a tarefa em `### Pn —`. `Autorizado:` pode conviver com `Pendente:`. `Pronto:` só entra quando não há `Pendente:`. O corpo da tarefa só tem o papel em `executor:`. Sessão, runtime, modelo e esforço ficam na tabela que o `open` imprime e em `.sessions/pln-nnn/execucao.json`.

Recusado: o corte na fase como gate (P2), que tira o dono da tarefa. Recusado também gravar a norma comum ou o código do parser nesta decisão: `plans/README.md` está no `.brza/core.lock`, e alteração fora deste workstream só sai com pedido explícito.

O link entre notas, fechado na mesma sessão antes da sala: definição no próprio arquivo, rótulo igual ao H1, chave igual ao id que já existe. Link externo continua inline.

Registrada no [PLN-023: O plano novo do playground mostra a pendência, o dono e quem pode executar](../../plans/PLN-023-gates-do-plano/PLN-023-plan.md).
