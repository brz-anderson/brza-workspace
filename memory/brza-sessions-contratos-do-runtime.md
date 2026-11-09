---
name: brza-sessions-contratos-do-runtime
description: Contratos sondados no Studio para workers, mailbox, operações e encerramento do brza sessions
metadata:
  type: reference
---

Na execução do PLN-017 em 2026-11-09, a sonda real do Studio confirmou:

- `message` não é tipo de mailbox; usar `status`. O payload da rodada precisa conter `round_id` e `dispatchId`.
  `--payload` não combina com `--task-id`/`--dispatch-id`; os identificadores vão juntos no JSON.
- `check --types` só filtra o despertar de `--wait`, não o lote entregue. Observador usa `--peek --wait`, sem `ack`;
  `--all` recupera mensagens já entregues ao chat. Validar remetente, Run, Dispatch e rodada; preservar os outros eventos.
- O worker puro retorna handle `structworker_<UUID>`, diferente do chat. O `worker-show --full` dá o chat em
  `terminalResource.endpointIncarnation`, `structured:<UUID>`. O agente deve vir do mapa/aba, não do prefixo desse UUID.
- A híbrida `agent launch --surface chat` + `worker-start --terminal` recebe a faixa, mas fica como
  `external_terminal`, com `autoReleaseAt: null`. O worker puro arma o prazo de cerca de dois minutos após `worker_done`.
- `worker-release` só aceita settled; `retained` não é fechado. A R7 escolheu pedido de `worker_done` no `close`
  normal e parada guardada no `--force`, com prova de `stopped` e settlement. `stop_unknown` não autoriza retry cego.
- O replay do mesmo envio foi aceito após o fence mudar, com `replayed: true`. O formato de operação emitido pelo host
  é timestamp mais entropia; um prefixo arbitrário `sonda-...` foi recusado. Não redefinir o instante do envio no replay.

Evidência e contexto:
[O `brza sessions` recebe as primitivas da reunião e o PLN-010 registra a transição pelo `rpc`](../work/worklogs/2026-11-09-pln-017-sessions-e-excecao-ao-pln-010.md).
