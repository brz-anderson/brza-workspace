---
scope:
  - workspace
refs:
  - PLN-009
  - issue:o-start-e-o-stop-do-mcp-concorrentes
---

# O PLN-009: o C1 no launchd real e o stop que apaga o plist

A pedido de Anderson, "Executar C1", rodou o C1 do
[PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md)
no launchd real, com o `brza-workflow@354d004`.

**O roteiro passou:**
- `start` 0;
- `status` 0, e 3 antes e depois;
- `/health` 200 com o token e 401 sem ele, só em `127.0.0.1`;
- `stop` idempotente.

**Dois achados foram à R7:**
- **O plist no login:** o `stop` deixava o plist com `RunAtLoad`, e o próximo login subiria o serviço de novo.
- **A fila real:** a subida despachou ao Studio um pedido de teste de 04:55 que estava na fila real. O Studio o recusou
  com `session_caller_unknown`, sem efeito. A origem não foi achada: o único teste que usa a fila padrão grava em pasta
  temporária.

Anderson escolheu as duas recomendadas:
- o P8 faz o `stop` apagar o plist;
- a fila foi copiada para o scratch e zerada.

**O P8:**
- Um `implementer` escreveu 6 testes que falharam antes, e corrigiu.
- A r1 rodou em paralelo pelo `agy` (Flash) e pelo `reviewer` (Opus), com 10 achados. Cinco foram corrigidos aqui na
  r2, e a corrida entre `start` e `stop` virou a issue
  [O start e o stop do MCP concorrentes](../issues/o-start-e-o-stop-do-mcp-concorrentes.md).
- A r2 pelo `agy` não achou nada.
- Gate: MCP 358 OK (um pulado) e CLI limpo 445 OK. Commit `brza-workflow@007383a`, publicado na `feat/pln-009-mcp`.
- Parecer: na seção do P8 de
  [REV: a entrega do PLN-009 contra o Pedido e a Cobertura](../reviews/pln-009-a-revisao-da-entrega.md).

**O C1 refeito com o `007383a`** foi aprovado: o `stop` em 1 s, o plist apagado, o `status` 3 logo depois e a porta
livre.

**O que fica:**
- o C2, o C3 e o C4;
- a confirmação de Anderson para o merge;
- depois do merge, o `--relink` dos links do MCP a partir do checkout principal.

## Fora do workspace

- **Os links do MCP em `~/.local/bin`:**
  - **O quê e onde:** `brza-mcp` e `brza-quota`, apontando para
    `~/Projects/brza-workflow/.worktrees/pln-009-mcp/packages/mcp/bin/`, pelo `bin/brza-install --mcp` do worktree.
  - **Risco:** os links quebram quando o worktree sumir.
  - **Estado:** ficam.
  - **Como desfazer:** apagar os dois links, ou, depois do merge, rodar `brza install --mcp --relink` do checkout
    principal.
- **O LaunchAgent `com.brza.orchestrator`:**
  - **O quê e onde:** carregado e descarregado duas vezes (pid 77306 e pid 29443); plist em
    `~/Library/LaunchAgents/com.brza.orchestrator.plist`.
  - **Risco:** o plist da primeira rodada subiria o serviço no login.
  - **Estado:** descarregado, sem plist. O primeiro foi apagado à mão e o segundo pelo `stop` novo.
  - **Como desfazer:** nada a desfazer.
- **A fila do orquestrador:**
  - **O quê e onde:** `~/.brza/orchestrator.db`, com os pedidos de teste 1 (`gated`) e 2 (`failed`). Copiada para
    `orchestrator.db.c1-residuo` no scratch do chat e apagada. A subida do C1 refeito criou uma vazia.
  - **Risco:** a perda dos dois pedidos de teste.
  - **Estado:** a fila vazia.
  - **Como desfazer:** copiar a cópia de volta, com o serviço parado.
- **O Studio:** a subida do primeiro C1 chamou o `orca orchestration run-create` real para o pedido 2, recusado com
  `effectsApplied: false`.
- **O `brza-workflow`:** commit `007383a` na `feat/pln-009-mcp`, publicado, sem merge.
