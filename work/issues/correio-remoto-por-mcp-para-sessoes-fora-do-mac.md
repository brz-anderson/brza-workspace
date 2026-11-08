---
status: open
description: A volta da conversa entre as sessões remotas e as do Mac — o resultado do worker remoto e o correio, pela caixa e pelo claude --cloud — com recibo e sem a mensagem remota virar turno da pessoa.
scope:
  - brza-workflow
  - workspace
opened: 2026-11-07
priority: medium
estimate_h: 24
tags:
  - tooling
  - infra
---

# O correio remoto por MCP para sessões fora do Mac

Levantado na [Reunião MCP remoto: a coordenação e a proposta de arquitetura](../worklogs/2026-11-07-reuniao-mcp-remoto-coordenacao.md). Nasceu como o modo 2 da v2.1; depois da correção de Anderson (o tema é o MCP do `brza-workflow`), é a **fase 3 da v3**: o `brza-orchestrator` não é canal de conversa (o `status` devolve o estado, não o texto do worker), e a resposta volta por aqui. Depende de [O proxy remoto de autorização no brza-mcp](proxy-remoto-de-autorizacao-no-brza-mcp.md).

## O pedido

Um servidor `brza-correio` — MCP streamable HTTP, só em `127.0.0.1` — com `mail_send` (grava na caixa do
destinatário e devolve um `id`), `mail_status` (recibo), `mail_inbox`/`mail_read` e `sessions_list` com
`total` e corte declarado. Exposto por Cloudflare Tunnel nomeado + Access com service token, e um token por cliente
vinculado no servidor ao remetente e aos destinos.

## O que a reunião já mediu

- O transporte funciona: Codex CLI e Claude Code consumiram um MCP de prova pelo túnel, com 401 sem token e ~125 ms de
  ida e volta; o `mail_send` entregou correio a uma sessão do Mac.
- A sessão Claude Code Cloud com a rede padrão **não alcança** o túnel (`403 connect_rejected`); precisa de rede
  Custom ou de um "network secret" para o host (a doc diz que o host com secret fica alcançável em Trusted; não medido).
- **A mensagem remota não pode ir pelo `agentSession.send`:** sem a `orchestrationCompatibilityEvidence`, o app a
  mostra como a da pessoa (`brza-workflow/bin/brza_runtime.py:87-88,96-97`); com ela, como tarefa do coordenador. Vai
  à caixa, e o chat recebe só um aviso fixo, sem o texto do remetente.
- Com Bearer válido, a prova aceitou um `X-Brza-Session` forjado: a identidade tem de vir do token, no servidor.

## Pronto quando

20/20 IDs consumidos nos dois sentidos, zero duplicata no replay, nenhum byte do remetente remoto como turno da pessoa,
e o Mac suspenso 10 min com 20 mensagens: perda e duplicata contadas.
