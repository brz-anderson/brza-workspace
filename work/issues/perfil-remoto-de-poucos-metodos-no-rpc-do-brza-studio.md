---
status: open
description: Um nível de permissão no RPC do runtime do BrzA Studio, abaixo do workspace, com uma allowlist de poucos métodos, para que o pareamento remoto sirva a sessões Cloud sem dar o desktop inteiro.
scope:
  - brza-studio
opened: 2026-11-07
priority: low
tags:
  - auth
  - infra
---

# O perfil remoto de poucos métodos no RPC do BrzA Studio

Levantado na [Reunião MCP remoto: a coordenação e a proposta de arquitetura](../worklogs/2026-11-07-reuniao-mcp-remoto-coordenacao.md), como a ideia mais ousada da Muralha (a arquiteta de segurança) na rodada 1.

## O pedido

O BrzA Studio já tem runtime remoto (`brza serve`, `brza environment add` com pareamento `orca://pair`, chave de
dispositivo Ed25519 e E2EE), mas o cliente pareado fala o RPC inteiro. Um perfil "remoto" com só
`agentSession.send` (rótulo forçado de origem não confiável) e a leitura do histórico das sessões permitidas faria o
pareamento servir à Cloud sem o servidor de correio à parte.

## O risco

Mexe no núcleo do controle de acesso do app: um método marcado errado abre o Mac inteiro.
