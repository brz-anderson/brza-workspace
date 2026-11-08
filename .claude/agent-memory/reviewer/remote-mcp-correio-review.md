---
name: remote-mcp-correio-review
description: Onde erram as propostas de correio/MCP remoto do brza (sessão Cloud ↔ Mac): a autoria da mensagem no app, o [medido] confundido e a volta que não acorda ninguém
metadata:
  type: project
---

Na revisão da proposta de MCP e correio remotos (reunião mcp-remoto, 2026-11-07, `playground`), o erro mais grave
estava no **modelo de autoridade do app**, que a sala tratou como binário mas é pior que isso:

- **Sem a `orchestrationCompatibilityEvidence`, a mensagem chega como a da pessoa** (Anderson), e não "rebaixada".
  O comentário do `rpc` no `brza_runtime.py` e o `caller-chat-sender.ts` do `brza-studio` ("windows, phones and
  remote CLIs act for a person") dizem isso. As relações são só `worker | coordinator | none`. "Dado rotulado, sem
  autoridade" exige mudança no app, e não cabe numa fase de 4–8 h.
- **Todo processo lançado por uma sessão do chat herda `ORCA_AGENT_SESSION_ID`**, e o seu `send` sai como tarefa de
  coordenador daquela sessão. Isso vale para o servidor da prova também.
- **Um [medido] que compara dois runtimes pode estar confundido**: entre a corrida do Codex e a do Claude, o código
  da prova mudou (o corte de 4000 virou 12000). Confira o mtime do script contra o horário de cada linha do log.
- **"Volta por poll"** não serve à conversa: o agente Cloud que fechou o turno não lê a caixa. E o
  `brza sessions send` só resolve os chats abertos no Mac (`find`), então o Mac não tem verbo para responder ao remoto.

**Why:** a proposta media o transporte (túnel, latência, 401) e deu como certo o que chega no destino.
**How to apply:** em proposta de mensagem entre sessões, leia primeiro como o app atribui o remetente. Depois
confira se o critério de "consumido/recibo" tem observável hoje: o `send_to_chat` descarta o resultado, e o
`clientOperationId` é novo a cada chamada, então não deduplica um retry.

**Na v2.1, a correção de um achado abriu uma contradição.** O "leia por um subagente sem ferramentas" conflita com
"consumido = o `mail_read`", que é uma ferramenta. E o observável foi definido só para o lado do Mac, sem o do
`--cloud`. Ao conferir uma correção, confira também se ela vale nos dois sentidos e se alguma fase de fato a
entrega.

**No `brza-orchestrator` (`packages/mcp`), o chamador vale mais do que parece.** Ele é também o
`ORCA_AGENT_SESSION_ID` do worker, em `cycle.py` (`env_for`): forjar o chamador escolhe qual chat do Mac vira
coordenador do worker. O gate só se aprova pelo mesmo chamador, e a decisão de Anderson é norma, não código. Por
fim, `role: consultant` sem `account` entra na fila sem gate. Proposta de "gate só no Mac" esbarra nessas três.

**A versão anunciada pode não estar no disco.** Na v3, a coordenação mandou revisar, e o arquivo ainda era a v2.1.
Confira o H1 e o mtime antes de revisar, e diga o que de fato revisou.

**O que costuma cair:** "o túnel da prova ficou exposto". Os PIDs já estavam mortos e o `tunnel.log` dizia
"Tunnel server stopped". Confira com `ps` antes de dar confiança.

Ver também [[meeting-plan-review-patterns]].
