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

## O P63 — o cartão do upstream

Commit `brza-studio@9564eff9368`, com `git cherry-pick -x 7321b066e83`.

- **A sondagem.** Antes do cherry-pick, um worktree descartável mediu 6 conflitos e o que faltava ao cartão: o
  `native-chat-prose`, que aqui mora em outro caminho (X50), e o harness de tooltip dos testes, 7 linhas (X49). Não foi
  preciso trazer módulo além disso, e a parada com Anderson não se aplicou.
- **A fila.** O upstream mudou a fila de mensagens para o `shared/`; a do BrzA ficou, com o `displayText` do commit
  portado no desktop e no mobile (X51). Os testes da edição da fila nova ficaram de fora (X52).
- **O cartão e o Claude Code.** O título diz "Hand-back from" para a devolução; o rótulo saiu da linha do remetente
  para o título do cartão, como no upstream (X54). O nome do remetente do Claude Code segue sem botão até o P64. O
  mobile ganhou o "Hand-back from", e o `pt.json` as 5 chaves do cartão (X55).
- **Os testes.** O caso de escala do cartão conta duas enumerações, e não três, sem a "aquisição de autoridade
  visível" do store do upstream (X53). Depois do rebase: `pnpm tc` → exit 0; 156 arquivos → 1263 passed.

## O P64 — o clique no remetente

Commit `brza-studio@ba4102b5c95`.

- **A busca.** Entre as abas de chat abertas, a única cujo rótulo próprio ou título do host é o nome do remetente; o
  clique a revela pelo mesmo caminho que abre um chat pelo histórico. Sem aba, ou com duas, o nome fica texto (X56).
- **O nome que o app guarda.** O título da aba é o que o `brza sessions --title` dá pelo `agentSession.rename`; o
  `/rename` do Claude Code fica só no transcript, e o nome automático `brza-workspace-<hex>` não casa.
- **Os testes.** O clique foca a aba da sessão; o nome sem aba fica sem botão. Antes do componente, o primeiro caso
  falhou; depois, 15 arquivos → 52 passed.

## O check

O `pnpm check:changed --base=origin/master --maxWorkers=2` do P62 rodou a suíte inteira, em 1514 s, e deu 22 de 26. O
format saiu no `oxfmt`. Os outros vermelhos já estão na `master`: o typecheck no `updater-enabled.test.ts:20`, do
`8e708f9790d`; o import boundaries, na issue das Pendências; e 5 testes em 3 arquivos, que falham igual num worktree
da `origin/master` em `9c7fcdebbb0`.

O do P63 deu 23 de 26, em 1851 s: o typecheck do mesmo teste, já corrigido na `master` em `586f4f69eb7`, o import
boundaries e os 2 casos do `open-uncommitted-entry.test.ts`, todos preexistentes. No mobile, o "words a host-restart
returned card" espera "Orca restarted" e falha igual sem o P63.

O do P64 deu 20 de 21, em 108 s; o vermelho é o import boundaries.

## O que fica

- O P65, com Anderson: o C18 ao C20 num build. O C18 mostra também se o CLI ecoa ao vivo o turno do correio.
- O worktree `.worktrees/pln-001-pedido-32` e a branch `feat/pln-001-pedido-32` saíram do `brza-studio`.
