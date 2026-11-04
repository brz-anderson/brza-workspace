---
scope:
  - brza-workflow
tags:
  - tooling
refs:
  - PLN-003
  - PLN-009
  - PLN-010
  - PLN-011
  - PLN-013
  - REV-010
  - issue:o-app-nao-le-a-cota-do-grok
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

- **A revisão do rascunho por duas sessões Grok.** A pedido de Anderson, uma sessão Grok revisou o Desenho. A que ele
  indicou, a `grok_18ca2288…`, estava presa numa aprovação do P3 do PLN-011, e a sessão abriu a
  `pln-013-grok-revisor` pelo `brza sessions --agent grok`, a primeira abertura real do Grok. O pedido que ficou na
  fila da antiga rodou mesmo assim, e o parecer dela sobrescreveu o da nova no scratch, porque o aviso de desconsiderar
  entrou na fila atrás dele. Os dois pareceres foram ao
  [REV-010: O Desenho do PLN-013, revisado pela sessão Grok](../reviews/REV-010-pln-013-o-desenho-pelo-grok.md), com 16
  achados, um deles falso. O `send_to_chat` não deu recibo do envio: é a lacuna do
  [PLN-010](../../plans/PLN-010-brza-sessions-sobre-o-brza-chat/PLN-010-plan.md).
- **A R4** fechou a tabela de modelo e esforço por runtime, a cota do Grok em `quota_unknown`, o `provider_session` nos
  quatro e as convergências. A issue [O app não lê a cota do Grok](../issues/o-app-nao-le-a-cota-do-grok.md) nasceu dela.
- **O Desenho e os Passos.** O `designer` reescreveu os itens D1 a D7 com a R4 e os achados, e derivou 11 passos em três
  entregas: E1 6,5 h, E2 4,5 h e E3 5 h, 16 h ao todo. O plano foi dividido em `-interview` e `-design`.

## Em aberto

- A R5, o aceite do corte em passos.
- O pedido de marcar o PLN-003/P12 como `[-]` segue no `Retomar` do PLN-003.
