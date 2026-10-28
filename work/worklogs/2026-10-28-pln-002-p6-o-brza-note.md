---
scope:
  - workspace
---

# O PLN-002/P6: o brza note

O pedido de Anderson, em 2026-10-28, na sessão `pln-002-p6`: "Execute o P6 do plans/PLN-002-os-comandos-brza/PLN-002-plan.md
pela plan-runner. O P3 ao P6 correm em paralelo, em sessões separadas, no mesmo checkout do brza-workspace: mexa só nos
arquivos do seu passo, e grave o plano só no fechamento, em uma edição seguida de git pull --rebase e commit imediato,
para não levar a edição de outra sessão no mesmo arquivo." O passo executa o D6 do
[PLN-002: Os passos manuais que se repetem entre sessões viram comandos `brza`](../../plans/PLN-002-os-comandos-brza/PLN-002-plan.md).

## O que se fez

**O `scripts/brza/brza-note`** tem as três formas do D6, sobre o `git` e o `WORKSPACE` do runtime, sem mudar o runtime:
- `brza-note new worklog <assunto>` cria `work/worklogs/AAAA-MM-DD-<assunto>.md` com o esqueleto do D6 e imprime o
  caminho; `new issue <assunto>` cria `work/issues/<assunto>.md` com `status: open`, o `scope`, o `opened` de hoje e o
  `priority` só quando dado, o H1 e o `## O pedido`. Os dois recusam a nota que existe (saída 1);
- `brza-note commit <caminho>… -m <mensagem>` roda o `check_notes.py` e para no erro dele, faz o `git add` e o commit só
  dos caminhos dados, e então o `git pull --rebase --autostash` e o push; `--no-push` para no commit.

**As escolhas que o D6 não fixava:**
- **O commit leva os caminhos** (`git commit -- <caminhos>`), e não o índice inteiro, e o pull usa `--autostash`. As
  sessões do P3 ao P6 dividem o mesmo checkout, e o índice e o arquivo sujo de uma estão no caminho da outra. É o X2 do
  plano.
- **O caminho relativo** parte do diretório atual quando ele está no workspace, e da raiz do workspace quando não está,
  como numa sessão do `brza-studio`. O que cai fora do workspace é uso errado (saída 2).
- **O assunto** é kebab-case sem a data; `Com Espaço` e `2026-10-28-x` são uso errado. O `--priority` vale só na issue.
- **Nada a commitar** nos caminhos dados sai com 1, sem commit vazio.

**Os testes:** o `tests/test_brza_note.py` é novo, com 14 casos, num clone de uma `origin` local, com um `check_notes.py`
falso que sai com o código pedido e o `today` fixo. O commit é provado com outro arquivo sujo ao lado e outro no índice,
e o pull com um push de outro clone antes. `python3 -m unittest scripts/brza/tests/test_brza_note.py` → 14 OK.
`python3 -m unittest discover -s scripts/brza/tests` → 111 OK, contando os testes do P3, do P4 e do P5 que as sessões
deles escreviam no mesmo checkout; numa corrida do meio, o `test_brza_test.py` do P4 falhou por estar sendo escrito.

**O primeiro uso real:**
- este worklog saiu do `brza-note new worklog pln-002-p6-o-brza-note` (saída 0), e a segunda chamada recusou (saída 1);
- o `feat(brza): brza note (PLN-002/P6)` saiu do `brza-note commit scripts/brza/brza-note
  scripts/brza/tests/test_brza_note.py -m …`, pelo link: o checador deu 0 erros, o commit levou só os dois caminhos, com
  o `brza-app`, o `brza-dev` e o `brza-test` das outras sessões sujos ao lado, e o push foi à `origin`;
- o fechamento — este worklog e o plano — também saiu do `brza-note commit`.

**O que se ligou:** só o `brza-note`, pela `link_command` do `brza-install`, e não pelo `--all`: o `--all` ligaria também
o `brza-app`, o `brza-dev` e o `brza-test`, ainda em escrita nas outras sessões. O `brza-install` mostra o `brza-note`
como `ok`, e os três como `ausente`.

O commit é `brza-workspace@bafce7e`.

## O que se aprendeu

- **O `$CLAUDE_SESSION_NAME` não existe no ambiente desta sessão**, aberta pelo app e renomeada com `/rename`. O esqueleto
  do D6 cai então no `<a escrever>`, e o nome se escreve à mão. É o X3 do plano.

## O que ficou

- **O nome da sessão no esqueleto.** Falta achar de onde o lê-lo: o `claude --name` e o chat do app não foram conferidos.
  Vai ao `Retomar` do plano.
- **O link dos outros scripts** vem do `brza-install --all` de cada sessão, ou do último passo.

## Fora do workspace

- **O quê e onde:** o link `~/.local/bin/brza-note` → `scripts/brza/brza-note` do checkout principal, criado pela
  `link_command` do `brza-install`.
- **O risco:** o comando passa a ser achado pelo PATH; o link quebra se o checkout principal sair do lugar.
- **Estado:** ativo.
- **Como desfazer:** `rm ~/.local/bin/brza-note`.
