---
status: open
description: Um proxy remoto no brza-mcp, diante de túnel nomeado com Access, que tira o chamador do token, filtra o status, limita o dispatch a consultor com teto e deixa a aprovação de gate e o config só no Mac, para expor o brza-orchestrator a outras máquinas e sessões Cloud.
scope:
  - brza-workflow
opened: 2026-11-07
priority: medium
estimate_h: 10
tags:
  - tooling
  - auth
---

# O proxy remoto de autorização no brza-mcp

Levantado na [Reunião MCP remoto: a coordenação e a proposta de arquitetura](../worklogs/2026-11-07-reuniao-mcp-remoto-coordenacao.md). É a fase 0 da proposta v3, que a reunião recomendou e que espera o aceite de Anderson.

## Por quê

O `brza-orchestrator` (`packages/mcp/`) já é MCP Streamable HTTP com Bearer em `127.0.0.1:4242`, e a reunião o expôs
por túnel e o consumiu do Claude Code. Mas expor a porta crua é inaceitável:

- o chamador vem do cabeçalho `X-Brza-Session` (`brza_mcp/server.py:111`, `tools.py:234-236`);
- o gate se aprova "pelo mesmo chamador" (`tools.py:5-7,365-366`);
- o worker nasce com `ORCA_AGENT_SESSION_ID = caller` (`cycle.py:111-116`).

Quem tem o Bearer forja o chamador, aprova o próprio gate e abre workers que gastam conta e se reportam a uma sessão do
Mac como coordenador. Pelo túnel, um `X-Brza-Session` forjado gravou um pedido com o chamador forjado (M13, medido
com `BRZA_HOME` isolado).

## O pedido

`brza mcp serve --remote` (outra porta, em `127.0.0.1`):

- **Chamador:** um token por cliente remoto, mapeado a `remote:<cliente>`; o `X-Brza-Session` e o `X-Brza-Client`
  de fora são apagados.
- **`status`:** só os pedidos do próprio chamador.
- **`dispatch`:** só `consultant` sem `account`, com teto remoto.
- **Gate e política:** o `approved` remoto é recusado (aprova-se no Mac); o `config` também.
- **Worker:** o `cycle.py` recusa `remote:` como sessão local; o coordenador do worker remoto é uma sessão-caixa.

## O domínio

O túnel nomeado com Access pede um domínio na Cloudflare, e a rodada da reunião deixou "túnel e domínio só depois"
(D1). **O domínio existe desde 2026-11-11: `brza.dev`**, com os nameservers na Cloudflare (`piper` e
`sergi.ns.cloudflare.com`, pelo `dig NS brza.dev`). O host do túnel será um subdomínio dele, ainda sem nome. A ordem do
D1 não muda: o proxy vem antes do túnel.

## Pronto quando

Os testes negativos em `tests/mcp/` passam: o cabeçalho de fora é ignorado; o `approved` remoto, o `config` e o
`dispatch` acima do teto são recusados; o `status` é filtrado; o `remote:` não vira sessão local.
