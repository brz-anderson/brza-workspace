---
scope:
  - brza-workflow
tags:
  - tooling
refs:
  - PLN-003
  - PLN-009
  - PLN-013
  - issue:o-grok-fica-sem-medida-por-tarefa
---

# Abertura e entrevista do PLN-013, o Grok no `brza sessions` e no MCP

O pedido de Anderson, em 2026-11-03, na sessão `tools-kit-produtividade`: "precisamos urgentemente adicionar o `grok` no
fluxo do `brza sessions` e do `MCP`". Esta sessão rodou os Passos 0 a 2 da `plan-runner` e a entrevista.

## O que se fez

- **O destino.** O roteador multiruntime do `brza sessions` já era o PLN-003/P12, e o PLN-009 deixou os outros
  runtimes fora de escopo. Na R1.1, Anderson escolheu um plano novo, o
  [PLN-013: O Grok, o Codex e o Antigravity abrem pelo `brza sessions` e recebem tarefas do MCP](../../plans/PLN-013-grok-codex-e-agy-no-brza-sessions-e-no-mcp/PLN-013-plan.md),
  e o pedido de marcar o P12 como `[-]` foi ao `Retomar` do
  [PLN-003](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md).
- **O corte (R1.2 e R1.3).** Entram as quatro partes: abrir o Grok, `--rename` e `--wait` nele, o despacho pelo MCP e a
  conta e a cota. O Codex e o Antigravity entram juntos no MCP.
- **A medição (R1.4)** foi a uma issue irmã, [O Grok fica sem medida por tarefa](../issues/o-grok-fica-sem-medida-por-tarefa.md).
- **Os fatos novos.**
  - **A cota dos três runtimes já sai do app**, no formato das janelas do Claude: `orca account list --json` traz
    `rateLimits.grok`, `.codex` e `.antigravity`, com `session` e `weekly`.
  - **Só o Claude e o Codex têm lista de contas no app**: as chaves de topo são `claude`, `codex`, `opencode` e `devin`,
    e há `inactiveCodexAccounts`.
  - **O Grok está sem login:** `grokAuthConfigured: false`.

- **A R2.** Fica a cota dos três runtimes, com a troca de conta só no Codex. O `--rename` e o `--wait` valem no Grok, no
  Codex e no Antigravity. A entrega sai em três partes: E1, abrir e despachar; E2, a cota e a conta; E3, o `--rename` e
  o `--wait`. A soma vai a ~13 h.

- **O Terreno**, por um `collector`, só leitura:
  - o `worker-start` aceita os três runtimes;
  - o MCP conta todo pedido na conta Claude ativa, e a política dele põe `sonnet` e `opus` por cima do pedido;
  - a troca de conta do Codex é global, do app;
  - o `agentSession.history` dá um id de sessão nos quatro runtimes.
  
  Os fatos e as fontes estão no Desenho do PLN-013.
- **A R3.** O modelo e o esforço saem de uma tabela por runtime. A cota é por runtime, pelas janelas de topo. O Codex
  troca de conta pelo gate. Uma sonda vem antes da E3.

## Em aberto

- Os itens `D` das três entregas, com os valores da tabela de modelo por runtime como rodada.
- O `grok login`, que é de Anderson e é pré-requisito da sonda da E3 e de toda abertura real.
