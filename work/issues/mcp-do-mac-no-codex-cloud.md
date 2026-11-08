---
status: open
type: unknown
description: O Codex Cloud desliga a internet do agente por padrão e só expõe segredos no setup; falta saber se ele usa MCP remoto e como alcançaria o correio do Mac.
scope:
  - brza-workflow
opened: 2026-11-07
priority: low
tags:
  - tooling
---

# O MCP do Mac no Codex Cloud

Levantado na [Reunião MCP remoto: a coordenação e a proposta de arquitetura](../worklogs/2026-11-07-reuniao-mcp-remoto-coordenacao.md). A reunião deixou o Codex Cloud de fora da primeira fase.

## A pergunta

O Codex Cloud aceita servidor MCP remoto (streamable HTTP) durante a fase do agente? Com a internet limitada por
domínio, o host do túnel pode entrar, e o token, que hoje só existe no setup, chega ao agente de algum jeito seguro?

## O que se sabe

- A doc (marcada como legado) diz: internet do agente desligada por padrão, com opção limitada ou irrestrita; segredos
  só no setup, removidos antes do agente; MCP local "pode não estar disponível" na nuvem.
- O Codex **CLI** consome o MCP remoto (medido na reunião), mas o `codex exec` barra a ferramenta sem
  `tools.<t>.approval_mode="approve"`.
- Alternativa de contorno sem rede: o git como barramento (a ideia F do Salto), com latência de minutos.
