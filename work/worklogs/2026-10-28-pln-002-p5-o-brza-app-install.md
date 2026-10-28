---
scope:
  - workspace
---

# O PLN-002/P5: o brza app install

O pedido de Anderson, em 2026-10-28, na sessão `pln-002-p5`: "Execute o P5 do plans/PLN-002-os-comandos-brza/PLN-002-plan.md
pela plan-runner". O passo executa o D5 do
[PLN-002: Os passos manuais que se repetem entre sessões viram comandos `brza`](../../plans/PLN-002-os-comandos-brza/PLN-002-plan.md).
Parou no primeiro ponto de commit, a pedido de Anderson, para o reinício do app: "avise as sessões pra pararem no
primeiro ponto de commit e registrarem no plano, vamos reiniciar".

## O que se fez

**O `scripts/brza/brza-app`** tem o `install` do D5:
- sem `--from`, faz o `fetch`, cria um worktree detached da `origin/master` num diretório temporário do sistema, fora de
  `.worktrees/`, instala offline e roda o `pnpm build:mac [--dmg]`. Com `--from`, roda o build no checkout dado;
- confere o app aberto antes do build e de novo antes de instalar. Sem `--yes`, recusa com saída 2, e pergunta antes
  de substituir, com a versão nova e a instalada;
- apaga o `/Applications/BrzA Studio.app` antigo e copia o novo com `ditto`; o `--dmg` copia o `.dmg` para
  `~/Downloads`; o `--clean` apaga o `dist` do `--from`;
- o worktree temporário sai no fim com `git worktree remove --force`, também quando o build ou o install falham. Só o
  `ditto` que falha o deixa, e imprime o `ditto` a repetir.

**A rodada da sessão** (R8 do plano): o `.dmg` vai para `~/Downloads`, e a substituição apaga o app antigo antes do
`ditto`, porque o `ditto` por cima mescla e deixa no pacote o que saiu da versão nova.

**O app aberto se acha pelo `pgrep -f '/Applications/BrzA Studio.app/Contents/'`**, menos este processo e os pais dele:
o `brza app install` digitado no app chega ao script por um processo do próprio app.

**Os testes:** o `tests/test_brza_app.py` é novo, com 15 casos, num clone de uma `origin` local, com o install, o
build, a pergunta e os processos do app trocados por falsos, e o `ditto` de verdade num `/Applications` temporário.
Duas mutações conferiram que eles pegam o defeito: sem o `rmtree` antes do `ditto`, e sem a recusa com o app aberto,
cada uma quebra um teste. `python3 -m unittest discover -s scripts/brza/tests` → `Ran 111 tests … OK`, com o P3, o P4
e o P6 já commitados.

**A recusa real:** `scripts/brza/brza-app install`, de dentro do chat, → `recusado: o BrzA Studio.app está aberto (pid
…)`, saída 2, sem build.

O commit é `brza-workspace@1339793`.

## O que se aprendeu

- **Os processos do app incluem os supervisores dos chats**, que rodam o executável do app como node. Fechar a janela
  não basta para o `install` sem `--yes`: o app tem de sair inteiro.
- **O `git pull --rebase` bateu com o commit do P4 no mesmo checkout**, no mesmo instante, e abortou sugerindo
  `git reset --hard`, que apagaria o que as outras sessões não tinham commitado. O estado estava certo; bastou repetir.

## O que ficou

- O P5.4, o C2: Anderson fecha o app, roda `brza-app install` num terminal fora dele e confere o `brza sessions --help`
  no chat e no terminal.
- O P5.5, a troca dos textos: `brza-install`/`brza-run` por `brza install`/`brza run` na ajuda dos scripts e no
  `CLAUDE.md:33`, depois do C2.

## Fora do workspace

- **O quê e onde:** o link `~/.local/bin/brza-app` → `scripts/brza/brza-app` do checkout principal, criado pelo
  `link_command` do `brza-install`. Não usei o `--all`, para não ligar os scripts ainda não commitados dos outros passos.
- **O risco:** o comando passa a ser achado pelo PATH; o link quebra se o checkout principal sair do lugar.
- **Estado:** ativo.
- **Como desfazer:** `rm ~/.local/bin/brza-app`.
