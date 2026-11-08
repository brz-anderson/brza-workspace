---
status: open
description: Se a medição do correio remoto mostrar perda com o Mac suspenso, entra um relay ou fila só de saída entre a Cloud e o Mac.
scope:
  - brza-workflow
opened: 2026-11-07
priority: low
trigger: A fase 1 do correio remoto medir perda de mensagem com o Mac suspenso.
tags:
  - infra
---

# A fila de saída, se o Mac dormindo perder correio

Levantado na [Reunião MCP remoto: a coordenação e a proposta de arquitetura](../worklogs/2026-11-07-reuniao-mcp-remoto-coordenacao.md). O Plantão (a voz do usuário) defendeu a fila desde a rodada 1: com o túnel, o Mac dormindo vira erro na
Cloud, e a pessoa reenvia à mão.

## A condição

A fase 1 do [O correio remoto por MCP para sessões fora do Mac](correio-remoto-por-mcp-para-sessoes-fora-do-mac.md) suspende o Mac 10 min
com 20 mensagens e conta perda e duplicata. Se houver perda, um relay só de saída (o Mac disca, a Cloud deposita)
entra antes da fase 2.
