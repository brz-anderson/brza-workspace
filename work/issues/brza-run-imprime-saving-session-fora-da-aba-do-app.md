---
status: open
scope:
  - workspace
opened: 2026-10-28
tags:
  - tooling
---

# O `brza-run` imprime o "Saving session..." do zsh quando roda fora da aba do app

Fora de uma aba do BrzA Studio, o `$SHELL -ic` do `brza-run` herda o ambiente do Terminal.app e, ao sair, imprime as
linhas do `zsh_sessions` do macOS, que entram na saída capturada. Na aba do app isso não acontece. Hoje o efeito
conhecido é só nos testes, que falham numa sessão de agente do app aberto pelo Terminal.app. Achado na sessão
`pln-002-p8`, em [O PLN-002/P8: o brza doctor](../worklogs/2026-10-28-pln-002-p8-o-brza-doctor.md), e conferido nesta
(`issue-brza-run-saving-session`), em 2026-10-28.

## O que se observou

- **O ambiente:** com o app aberto pelo Terminal.app, a sessão de agente herda `TERM_PROGRAM=Apple_Terminal` e um
  `TERM_SESSION_ID`.
- **O caminho:** o `brza-run` roda o comando com `pty.spawn([$SHELL, '-ic', command])` (`scripts/brza/brza-run:101`).
  O `/etc/zshrc:74` carrega o `/etc/zshrc_$TERM_PROGRAM`, e o `/etc/zshrc_Apple_Terminal:96` liga o salvamento de sessão
  quando há `TERM_SESSION_ID` e o `SHELL_SESSIONS_DISABLE` não é 1.
- **A saída:** ao sair, o zsh imprime, depois da saída do comando:
  ```
  Saving session...
  ...saving history...truncating history files...
  ...completed.
  Deleting expired sessions...none found.
  ```
- **Os testes:** o `test_chat_mode_runs_here_and_sends_the_blocks` e o `test_tab_mode_prints_blocks_and_closes_on_success`,
  do `BrzaRunTest` em `scripts/brza/tests/test_brza_scripts.py`, falham com essas linhas a mais. Passam com qualquer um
  destes: `env -u TERM_PROGRAM`, `env -u TERM_SESSION_ID` ou `SHELL_SESSIONS_DISABLE=1`.

## O ▶ não leva as linhas ao chat

O worklog do P8 supunha que o ▶ de um app aberto assim levaria as mesmas linhas ao chat. Não leva:
- **O app reescreve o ambiente da aba:** o `buildInheritedLocalPtyEnvironment` põe `TERM_PROGRAM: 'Orca'` por cima do
  herdado (`src/main/providers/local-pty-spawn-environment.ts:63` do `brza-studio`), e o daemon faz o mesmo
  (`src/main/daemon/pty-subprocess/spawn-environment.ts:180`). O `/etc/zshrc_Orca` não existe.
- **Conferido numa aba real:** `brza run -- 'printenv TERM_PROGRAM TERM_SESSION_ID; echo fim'`, desta sessão, abriu a
  aba e devolveu `Orca` e `fim`, sem `TERM_SESSION_ID` e sem as linhas.

O ▶ em si não foi clicado. Que a aba dele nasça pelo mesmo ambiente é inferência pelo código acima, não rastreada até o
handler do ▶.

## O que falta confirmar

- **Se o ▶ abre a aba pelo mesmo montador de ambiente** que o `brza terminal create`: um clique num bloco
  `printenv TERM_PROGRAM` com o app aberto pelo Terminal.app fecha a dúvida.
- **Se há outro caminho que roda o `run_here` fora da aba**, além dos testes. Pelo docstring do `brza-run`, os dois modos
  rodam o comando numa aba do app.

## O conserto provável

`SHELL_SESSIONS_DISABLE=1` no ambiente do `$SHELL -ic`, no `os.environ.update` do `run_here`
(`scripts/brza/brza-run:100`), ao lado do `PAGER` e do `GIT_PAGER`. Desliga só o salvamento de sessão, vale dentro e
fora da aba e não mexe no `TERM_PROGRAM`, de que outras ferramentas dependem — na aba, o `Orca`.

As alternativas, e por que ficam atrás:
- **Tirar o `TERM_PROGRAM` do ambiente do filho:** na aba, apagaria o `Orca`, que o app põe para as TUIs.
- **Corrigir só no teste**, no `quiet_terminal`: os testes passam, mas o `run_here` segue frágil fora da aba.
- **`SHELL_SESSIONS_DISABLE=1` no `~/.zshenv`:** muda fora do workspace e desliga a restauração de sessão do
  Terminal.app também nas janelas dele.

O conserto vem com o teste: os dois testes acima passando no ambiente herdado do Terminal.app, sem `env -u`.
