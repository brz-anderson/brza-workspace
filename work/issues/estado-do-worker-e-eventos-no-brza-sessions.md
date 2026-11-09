---
status: open
description: Corrigir a leitura do estado efetivo do worker no brza sessions e preservar a data dos eventos de mailbox.
scope:
  - brza-workflow
opened: 2026-11-09
priority: medium
tags:
  - tooling
---

# O brza sessions distingue o estado do worker do estado do Dispatch

Pendência ao `tools-kit`, extraída do [PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md).

**Evidência:** `brza-workflow/packages/client/bin/brza-sessions:564`, em `db6bd28`, prefere `dispatch.status` a `worker.state`. A coordenação carregou a função real e a fixture `meeting-runner/scripts/tests/fixtures/v2/pure-claude-after-deadline.json`: `dispatch.status=completed`, `worker.state=succeeded`, resultado `worker_state=completed`. A inspeção do worker não reconhece settlement; o `close` pode pedir encerramento de novo e o `wait` não concluir pelo `worker_done`.

Corrigir com regressões usando o JSON real, incluindo falha, parada incerta e liberação retida. Conferir também a preservação de `createdAt` nos eventos de `wait`, hoje ausente conforme a revisão da skill. Preservar a R7 e a leitura da mailbox sem consumo.

Contorno atual: a skill confere `worker.state` diretamente no `--status`; seu `--wait-settled` é o gate pelo código de saída. Não anunciar o defeito do CLI como resolvido nem repetir `close --force` após incerteza.
