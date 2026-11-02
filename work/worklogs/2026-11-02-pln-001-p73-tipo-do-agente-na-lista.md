---
scope:
  - brza-studio
date: 2026-11-02
tags:
  - chat
---

# O P73 do PLN-001, o tipo do agente na lista de agentes do chat

O pedido 38, de Anderson: a linha de cada agente na lista "AGENTES" da faixa do chat, `Revisar features do fork
pós-sync · Bash`, passa a mostrar o nome do agente chamado, `Revisar features do fork pós-sync · reviewer · Bash`. A
sessão `pln-001-pedido-38` executou o P73 do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md),
com a R64.1 (só a faixa do chat) e o D56.

## O que a leitura do D56 confirmou

O `agentType` chega à linha do subagente do Claude: o `claude-child-work-decoder.ts:75` grava o `subagent_type` em `name`
e em `agentType`, e o `rowFromView` o repassa ao `AgentChildRowModel.agentType`. Nada do D56 caiu; não houve pergunta
a Anderson.

## O que mudou, em `brza-studio@563705a7aaf`

- O `AgentChildRowContent` ganhou o parâmetro opcional `agentTypeBeforeTool`, que só a
  `NativeChatBackgroundTasksStatus` passa. O `agentChildRowTypeBeforeTool`, no `agent-child-row-text.ts`, decide o tipo:
  só quando o detalhe é a ferramenta, e nunca `default`, `unknown`, em branco ou igual ao nome da linha.
- O `agentChildRowLeadTrail` compartilhado, a barra lateral e o celular ficaram como estavam.
- Sete `it` (nove casos) novos no `NativeChatBackgroundTasksStatus.test.tsx`; o `agent-child-row-parity.test.tsx` passou a esperar,
  na faixa, o tipo antes da ferramenta, e a barra lateral igual à de antes.
- `pnpm check:changed --base=origin/master`: 24 de 24 verdes. Push direto na `master` (`384d4b08fd6..563705a7aaf`), sem
  mexer na tag nem no app instalado.

## Desvios

- **X65.** A faixa mostra o `agentType` cru, e não o `formatAgentTypeLabel`, que capitaliza os nomes de CLI.
- **X66.** O teste de paridade afirmava faixa igual à barra lateral nas linhas com ferramenta, que é o que o R64.1
  muda; ele agora afirma a diferença nas 4 linhas.

## Próximo

O C26, de Anderson, num build novo: disparar um subagente com `subagent_type` (um `reviewer`) e olhar a lista "AGENTES"
enquanto ele roda. Não rodei o app, e o C26 segue em aberto.
