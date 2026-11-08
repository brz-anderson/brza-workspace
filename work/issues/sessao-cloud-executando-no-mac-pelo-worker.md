---
status: open
type: unknown
description: Medir o worker My Machines do Cursor e o ambiente self-hosted do Claude, em que o agente Cloud executa as ferramentas no Mac e usa o correio local sem túnel.
scope:
  - workspace
opened: 2026-11-07
priority: medium
tags:
  - tooling
  - infra
---

# A sessão Cloud executando no Mac pelo worker

Levantado na [Reunião MCP remoto: a coordenação e a proposta de arquitetura](../worklogs/2026-11-07-reuniao-mcp-remoto-coordenacao.md). É o modo 1 da proposta (G), que a coordenação achou no `--help` durante a reunião.

## A pergunta

- `cursor-agent worker` sem `--pool`: "a personal My Machines worker (no Enterprise plan needed)" que executa as
  ferramentas do Cloud Agent neste Mac, só por conexão de saída. O agente enxerga o `brza`, as sessões e os MCPs
  locais? O que o celular mostra quando o worker morre?
- `claude --environment <ccpool_…>`: o que é preciso para registrar o Mac como ambiente self-hosted?

## O risco

O agente Cloud ganha o poder de uma sessão local: quem controla a conta do Cursor ou do claude.ai controla o Mac.
Registrar o worker muda estado fora do workspace e vai ao worklog do dia.
