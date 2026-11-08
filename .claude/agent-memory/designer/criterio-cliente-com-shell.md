---
name: criterio-cliente-com-shell
description: Critério que pesou na escolha de Anderson sobre onde moram as primitivas de sessão (CLI antes do MCP), e o que isso implica ao desenhar
metadata:
  type: project
---

Em 2026-11-08 (playground, reunião multiagente), Anderson escolheu a recomendada "brza sessions primeiro": o CLI ganha
os verbos, e o MCP só os embrulha depois, para quem chama sem shell (Cloud).

**Why:** o critério que venceu foi a independência de client. Claude, Codex, Grok e Antigravity chamam shell; o MCP
exige um client HTTP com Bearer e um ciclo que hoje só entende worker de uma tarefa.

**How to apply:** desenhe a primitiva primeiro como verbo de CLI com `--json` estável, que vira o contrato do embrulho
MCP. Do MCP, anote só o que ele reaproveitaria. Proposta que começa pelo MCP precisa de um fato novo, como um client sem
shell que passou a pesar.

Pendente (preencher quando a rodada responder): a resposta às quatro perguntas do D2 do CLI, que são o recibo pelo
`rpc` contra a R1.4 do PLN-010, o `read` fora, o `wait` por estado e o `usage` do Codex, e que estimativa errou. Ver
[[base-de-estimativa-brza-sessions]].
