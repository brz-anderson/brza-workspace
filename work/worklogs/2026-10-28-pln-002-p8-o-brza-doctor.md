---
scope:
  - workspace
---

# O PLN-002/P8: o brza doctor

O pedido de Anderson, em 2026-10-28, na sessão `pln-002-p8`: "Execute o P8 do
plans/PLN-002-os-comandos-brza/PLN-002-plan.md pela plan-runner: o brza doctor, pelo D8, do P8.1 ao P8.4, com o C4 com
Anderson". O passo executa o D8 do
[PLN-002: Os passos manuais que se repetem entre sessões viram comandos `brza`](../../plans/PLN-002-os-comandos-brza/PLN-002-plan.md).

## O que se fez

**O `scripts/brza/brza-doctor`** tem a forma do D8, sem mudar o runtime nem o `brza-install`, de quem importa o
`link_state`, o `commands` e o `override` pelo `runpy`:
- **ERRO:** a identidade, pelo `git var GIT_AUTHOR_IDENT` e `GIT_COMMITTER_IDENT` no brza-workspace; a medição, pelo
  `measure.py` no `.claude/settings.json` e pelo `BRZA_WORKSPACE` no ambiente; os links de todo `brza-*`; o
  `agentCmdOverrides.claude` igual ao `~/.local/bin/claude-brza`, com o link dele `ok`.
- **AVISO:** o app que não responde ao `rpc`, e o override fica sem conferir; o `pnpm` fora do PATH; o perfil
  `brza-dev` sem os arquivos de estado do `profileHasState`; o app instalado atrás da `origin/master`.
- Cada linha diz o que conferiu, e o erro e o aviso trazem uma linha `conserta:`. O `--json` devolve a lista. A saída
  é 1 com algum ERRO, e a conferência que quebra vira ERRO dela, sem derrubar as outras.

**As escolhas que o D8 não fixava:**
- **O app velho compara com a `origin/master` do último fetch**, sem `git fetch`: o doctor só lê. O commit sai do fim
  da versão (`…local.<ms>.<12 hex>`), e o aviso diz quantos commits atrás. O commit que o checkout não conhece também
  vira aviso.
- **O link do `claude-brza` entra na conferência do chat**, e não na dos links: o `--all` não o liga, e o override
  que aponta para um link ausente quebra o chat do mesmo jeito.
- **O conserto do perfil** é entrar na conta num dev build com `ORCA_DEV_PROFILE=shared pnpm dev`, porque o `brza dev`
  descarta o `ORCA_DEV_PROFILE` herdado (`brza-dev`, `INHERITED_ENV`).

**Os testes:** o `tests/test_brza_doctor.py` é novo, com 18 casos. Rodam num workspace temporário, com o ambiente, o
`rpc` e o `git var` trocados e um `brza-studio` com uma `origin/master` de verdade. Sem o script, falham no
`run_path`. `python3 -m unittest scripts/brza/tests/test_brza_doctor.py` → `Ran 18 tests … OK`.
`env -u TERM_PROGRAM python3 -m unittest discover -s scripts/brza/tests` → `Ran 129 tests … OK`; eram 111.

**A corrida real:**
- `scripts/brza/brza-doctor`, antes de ligar → saída 1, só com `ERRO  links: brza-doctor ausente` e o conserto
  `brza install --all`.
- `brza install --all --dry-run` mostrou que só o `brza-doctor` seria ligado; o `--all` o ligou.
- `brza doctor` no chat, pelo despacho do app → saída 0, tudo `ok`, com o app na `…9747ac2b68d1`, a `origin/master`.
- Num ambiente limpo (`env -i HOME PATH`) → saída 1, com `ERRO  medição: BRZA_WORKSPACE fora do ambiente` e o conserto.
  A identidade saiu `ok`, porque o git global já tem o noreply.
- O C4: a metade do terminal, rodada por Anderson num terminal fora do app, deu "Como o esperado".

O commit é `brza-workspace@cc19e75`.

## O que se aprendeu

- **Os dois testes de saída do `brza-run` falham quando o app foi aberto pelo Terminal.app.** O `TERM_PROGRAM=Apple_Terminal`
  herdado liga o `zsh_sessions` do macOS no `$SHELL -ic`, que imprime "Saving session..." ao sair. Com
  `env -u TERM_PROGRAM`, passam. O ▶ de um app aberto assim deve levar as mesmas linhas ao chat.
  - **Emenda em 2026-10-28:** a aba do app põe `TERM_PROGRAM=Orca` por cima do herdado, e o `brza run` numa aba real
    saiu sem as linhas. O ▶ não foi clicado: que ele também não as leve é inferência pelo código. O detalhe está em
    [O `brza-run` imprime o "Saving session..." do zsh quando roda fora da aba do app](../issues/brza-run-imprime-saving-session-fora-da-aba-do-app.md).
- **O X3 segue:** o esqueleto do `brza note new` saiu com `<a escrever>` no lugar do nome da sessão.

## O que ficou

- O P7 do PLN-002, que espera a 2d, e a revisão da entrega depois dele.
- O "Saving session..." do `brza-run` com o app aberto pelo Terminal.app, sem casa ainda.
  - **Emenda em 2026-10-28:** a casa é [O `brza-run` imprime o "Saving session..." do zsh quando roda fora da aba do app](../issues/brza-run-imprime-saving-session-fora-da-aba-do-app.md).

## Fora do workspace

- **O quê e onde:** o link `~/.local/bin/brza-doctor` → `scripts/brza/brza-doctor` do checkout principal, pelo
  `brza install --all`.
- **O risco:** o comando passa a ser achado pelo PATH; o link quebra se o checkout principal sair do lugar.
- **Estado:** ativo.
- **Como desfazer:** `rm ~/.local/bin/brza-doctor`.
