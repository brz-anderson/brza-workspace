---
status: open
description: Um brza mcp start e um brza mcp stop concorrentes podem deixar o agente de pé sem plist, ou apagar o plist entre o write_plist e o bootstrap; o launchd.py não tem trava entre processos.
scope:
  - workspace
opened: 2026-11-03
priority: low
tags:
  - tooling
---

# O start e o stop do MCP concorrentes

Na revisão do P8 do [PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md),
em 2026-11-03, o `agy` (Flash, achado 5) e o `reviewer` (Opus, A3) acharam a mesma corrida. O P8 fez o `stop` apagar o
plist depois do `bootout`, para o login não subir de novo o serviço parado. Sem trava entre processos no
`packages/mcp/brza_mcp/launchd.py`, um `start` que roda junto com o `stop` cai em uma de duas sequências:

- **O `start` grava o plist e o `stop` o apaga antes do `bootstrap`.** O `start` falha com erro explícito, sem estado
  escondido.
- **O `stop` faz o `bootout` e o `start` consegue o `bootstrap` na nova tentativa.**
  - O `stop` apaga o plist e espera o agente do `start` até estourar o prazo, com uma mensagem que aponta a causa
    errada.
  - O agente fica de pé sem plist e não volta no login.
  - O `active_port` perde o recurso de ler a porta no plist (`paths.py:140`).

Antes do P8, a segunda sequência deixava um estado coerente: o agente de pé, com o plist.

## O que falta

Uma trava de arquivo, `fcntl.flock` em `~/.brza/runtime/`, em volta do `start` e do `stop`. Ela fica fora do P8 porque
pede testes de concorrência entre processos, cerca de 1 h, e hoje só um humano roda os dois verbos.

O gatilho é a primeira automação que chame `brza mcp start` ou `stop` sozinha, como um hook ou o `brza doctor` que
religa o serviço.
