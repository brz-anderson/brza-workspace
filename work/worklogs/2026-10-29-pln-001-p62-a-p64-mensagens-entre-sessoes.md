---
scope:
  - brza-studio
date: 2026-10-29
tags:
  - chat
---

# O P62 ao P64 do PLN-001, as mensagens entre sessões no chat

Anderson autorizou o P62, o P63 e o P64 do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md)
na sessão do `brza-workspace` que gravou o pedido 32, ao escolher "Agora, em paralelo" (R51.2). O P65 e os casos
manuais ficaram fora. Os passos rodam na sessão `pln-001-pedido-32`, no worktree `.worktrees/pln-001-pedido-32` do
`brza-studio`, com um push na `master` por passo, sem PR. A evidência detalhada está em cada passo do plano.

## O P62 — o leitor do BrzA

Commit `brza-studio@21f9cfe90bb`.

- **O envelope real.** Nos transcripts locais, 286 mensagens de outra sessão vêm no
  `<cross-session-message from="uds:…" from-name="…">`, com o `origin` (`kind: 'peer'`, `name`, `body`) na linha; a
  devolução de subagente vem no `<agent-message from="<tarefa>">`, com o `origin.handback`. O leitor lê o `origin`
  primeiro e os dois envelopes depois (X34). A sessão `pln-002-sessions-rename` mediu o mesmo no PLN-002/P9.1.
- **O remetente.** Um `AgentMessageSource` do upstream, com o tipo no endereço — `claude-peer:` ou
  `claude-hand-back:` —, sem mudar o contrato (X35). O nome do remetente fica como texto até o P64 (X37).
- **Onde liga.** O decoder do transcript, a importação para o journal, que perdia o `from` (X36), e o eco ao vivo no
  `journalClaudeMessage`, que descartava todo texto de usuário. Se o CLI ecoa o turno do correio ao vivo, só o C18
  mostra.
- **Os testes.** Dois arquivos do BrzA, com 6 casos; antes do leitor, 3 falharam pela asserção. Depois do rebase,
  16 arquivos → 101 passed.

## O check

O `pnpm check:changed --base=origin/master --maxWorkers=2` do P62 rodou a suíte inteira, em 1514 s, e deu 22 de 26. O
format saiu no `oxfmt`. Os outros vermelhos já estão na `master`: o typecheck no `updater-enabled.test.ts:20`, do
`8e708f9790d`; o import boundaries, na issue das Pendências; e 5 testes em 3 arquivos, que falham igual num worktree
da `origin/master` em `9c7fcdebbb0`.

## O que fica

- O P63 e o P64, nesta sessão.
- O C18, com Anderson, no build depois do P64.
