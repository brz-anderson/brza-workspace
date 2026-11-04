---
name: brza-mcp-coordena-de-um-chat-do-studio
description: "O dispatch do brza-mcp só vale de um chat do Studio, por HTTP com os headers dele; sessão com --mcp-config fora do Studio cai em session_caller_unknown"
metadata:
  node_type: memory
  type: project
  originSessionId: 78a88a8b-66f4-4180-b2a6-8e7eaf456197
  modified: 2026-11-04T01:04:56.916Z
---

O `dispatch` do `brza-mcp` (PLN-009, `tools-kit`) abre o worker pelo `orchestration` do Studio com o
`ORCA_AGENT_SESSION_ID` de quem chamou. Uma sessão de terminal com `--mcp-config` não tem esse id e cai em
`session_caller_unknown`. O `brza sessions` abre chat do Studio, mas não aceita `--mcp-config`. O caminho que funciona
é um chat do Studio chamando o `/mcp` por `curl`, com Bearer de `~/.brza/runtime/mcp.token`, `X-Brza-Session:
$ORCA_AGENT_SESSION_ID` e `X-Brza-Client: $ORCA_USER_DATA_PATH`. Conferido em 2026-11-03 com `initialize` e `status`.

**Why:** a R7.3 do PLN-011 escolheu reabrir com `--mcp-config` e teve de ser refeita na R12, depois do plano gravado.

**How to apply:** ao planejar coordenação pelo `brza-mcp`, ofereça o chat do Studio por HTTP como caminho, até o
`.mcp.json` do PLN-003/P4 existir. Ligado a [[brza-orca-coexistence]].
