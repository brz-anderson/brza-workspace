---
scope:
  - brza-studio
  - brza-workflow
tags:
  - chat
refs:
  - PLN-001
---

# O P72 do PLN-001, o prompt do `brza sessions` como cartão "Tarefa do coordenador"

O pedido 37, de Anderson: as mensagens que o `brza sessions` manda ao criar sessões aparecem como o cartão "Tarefa do
coordenador", e não como mensagem do usuário. A sessão `pln-001-pedido-37` executou o P72 do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md),
com a R63 e o D55.

## O que a leitura do D55 confirmou, e o que não

Confirmou: o cartão sai do `task` com ids sintéticos; o provedor Claude só lê o `from` no `mail-notice`, então o texto
chega igual; o `/rename x` do launch é só comando do catálogo e fica sem `from`; a fila guarda o `from`; o cartão dobra
em 3 linhas pela altura renderizada.

**Não se sustentou:** "sem mudança no `brza-workflow`". O `brza sessions send` e o prompt do `--rename` saem pelo
`send_to_chat`, que chama o socket por um `rpc()` em Python sem identidade de chat, e o `orca` CLI só leva o chat no
`agent.launch`. O servidor não tinha como saber o remetente. Parei e perguntei a Anderson, que escolheu mexer no
`brza-workflow`.

## O que mudou

- **`brza-studio@9a8631369ac`:** o `chat-task-source.ts` monta o `from` (os três ids iguais ao id da operação); o
  `caller-chat-sender.ts` acha o chat chamador (só `orca` CLI local com `agentSessionId`); o `launchPromptCreateInputs`
  leva o `from`, exceto para prompt que é só comando do catálogo; o `firstMessage` ganhou o `from`, só do host, gravado
  como mensagem de agente (o schema do wire segue `strict`); o `agentSession.send` põe o `from` no corpo quando o
  chamador é outro chat. O cartão "Entregue a um agente" usa o mesmo helper. Testes novos: 6 no
  `structured-agent-session-chat-task-send.test.ts` e 4 no `agent-launch-handoff-card.test.ts`.
- **`brza-workflow@d48ee31`:** o `rpc()` do `brza_runtime.py` manda o `ORCA_AGENT_SESSION_ID` no
  `orchestrationCompatibilityEvidence` do `agentSession.send`. 3 testes novos no `test_brza_runtime.py`.
- Os gates: os testes por caminho e os vizinhos, `pnpm tc:node` e `pnpm check:changed --base=origin/master` (24 de 25
  verdes; o grupo "unit tests" falhou em 3 arquivos de `cross-version-wire`, que falham igual na `master`, sem a
  mudança). Suíte inteira: roda no merge, pela coordenação.

## Desvios

- **X74.** O `brza-workflow` mudou, contra o D55, por escolha de Anderson depois da pergunta acima.
- **X75.** O `from` marca a mensagem como de agente para além do cartão: a primeira mensagem do chat aberto por um
  agente deixa de oferecer o rewind, não responde pergunta pendente (`native-chat-ask.ts:149`) e, se um Stop a tirar
  antes de chegar, não volta como rascunho da pessoa (`agent-session-stopped-history.ts:44`). O D55 supunha que só o
  `mail-notice` era lido; o resto lê a presença do `from`. É o mesmo que já vale para as tarefas do Dispatch.
- **X76.** O coordenador do launch entra pela `AgentLaunchSurfaceFactory` (`promptCoordinator`), e não pela execução: o
  `agent-launch.ts` já estava no limite de 300 linhas do lint.
- **X77.** Preexistentes, sem relação e sem conserto aqui: 20 falhas em `tests/cli` do `brza-workflow` (`test_brza_note`
  e `test_brza_sessions`), as mesmas na `master`; 3 falhas em `tests/e2e/cross-version-wire` do `brza-studio`.

## Próximo

O C25, de Anderson, num build novo, com o `brza-workflow` instalado onde o chat o roda: `brza sessions <nome> --prompt`,
com `--rename`, e o `brza sessions send`; e, num terminal fora de chat, o mesmo, que deve seguir como balão. Não rodei o
app, e o C25 segue em aberto.
