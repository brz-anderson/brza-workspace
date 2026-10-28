---
scope:
  - brza-studio
---

# O modo de permissão do chat do Antigravity se aplica ao servidor vivo

O pedido de Anderson, em 2026-10-28: "o modo de permissão não está funcionando no chat com o agy, corrija com urgencia".
Na rodada, o sintoma escolhido foi "Full access ainda pede" e "Trocar o modo não pega".

## A causa

No chat `antigravity_99120b11_…` ("Executar o P2 do brza tree (PLN-002)"), o registro ficou com `permissionMode:
full-access`. Mesmo assim, o servidor pediu aprovação de cada comando e do `edit_file`, todos no mesmo processo (fence 4).
- O modo só chegava ao servidor no arranque, pelo `session/set_config_option` do handshake
  (`src/main/acp/acp-structured-handshake.ts:131`). A troca no seletor só gravava o registro.
- A troca valeria quando o processo fosse substituído no envio seguinte (`structured-agent-session-outgrown-child.ts`).
  Só que o segundo envio chegou com o primeiro turno ainda aberto, e a substituição é pulada enquanto o filho tem
  trabalho em curso. O servidor ficou em `default`.

O servidor `agy_acp_server.par` 1.3.0, testado direto com uma cópia da conta em diretório temporário:
- em `yolo`, o comando e a edição rodam sem pedir permissão;
- trocado para `yolo` **no meio do turno**, os comandos seguintes já não pedem.

## O que se fez

O commit `e2c71f9f5fe` na `master` do `brza-studio`, com push (era o `4bed5665efd` local, rebaseado por outra sessão no
mesmo checkout):
- **A troca de modo vai ao processo vivo.** O `recordStructuredAgentSessionOptionIntent` grava o registro e chama o
  novo `applyPermissionMode` do adapter, que manda o `session/set_config_option` com o valor mapeado (`default`,
  `auto_edit`, `yolo`). Se a escrita falhar, o erro é engolido e a troca fica para o próximo arranque.
- **A substituição segue o modo que o servidor informa.** O ACP passa a implementar o
  `permissionModeRequiresAcquisition`: substitui só quando o modo informado difere do pedido. Sem modo informado, vale a
  comparação antiga com o modo de arranque, para não reiniciar a cada envio.
- O código novo fica em `src/main/acp/acp-live-permission-mode.ts`, porque o adapter passaria do `max-lines`.
- O teste `switches the live server to the chat permission mode picked mid-chat, without a restart`, em
  `acp-structured-antigravity.test.ts`, substitui o que fixava o reinício no próximo envio.

**O que rodou:**
- `typecheck:node` limpo;
- `oxlint` e `oxfmt` limpos, também no hook do commit;
- `vitest` em `src/main/acp` e `src/main/native-chat/agent-session-wire`: 2682 passam e 9 falham, em 7 arquivos. As
  mesmas 7 falhas aparecem na `master` sem a mudança, com `git stash`.

## Retomar

- O build do app com a correção, para conferir no chat real: pôr Full access durante um turno e ver os comandos seguintes
  rodarem sem pedir.
- Falta teste da troca durante um turno aberto, o caso exato do sintoma. Hoje o teste cobre a troca entre envios, no
  mesmo processo.
- O pedido de aprovação que já está pendente na hora da troca continua esperando resposta. A troca vale só para os
  pedidos seguintes.
