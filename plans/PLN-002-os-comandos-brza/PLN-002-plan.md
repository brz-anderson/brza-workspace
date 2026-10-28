---
status: open
phase: interview
origin: issue
origin_ref: os-comandos-brza-que-viram-o-pln-002
ready: não — faltam as rodadas dos pontos de desenho da issue
scope:
  - workspace
  - brza-studio
opened: 2026-10-28
owner: Anderson
tags:
  - tooling
---

# PLN-002: Os passos manuais que se repetem entre sessões viram comandos `brza`

- **Retomar:** a entrevista está em curso, na sessão `pln-002-comandos-brza`. A R1, a R2 e a R3 fecharam, e as rodadas
  seguintes cobrem o `brza-install`, o `doctor`, o `note`, o nome do `tree`, o `sessions` e a
  ordem. O P0, o despacho, está feito em `brza-studio@9a81e65c852`.

## Pedido

- **Origem:** [Os comandos `brza` que viram o PLN-002](../../work/issues/os-comandos-brza-que-viram-o-pln-002.md), com
  o levantamento e as rodadas em
  [Os comandos brza que faltam, levantados nas notas e nos scripts](../../work/worklogs/2026-10-28-os-comandos-brza-que-faltam.md).

"Acione a plan-runner e escreva o PLN-002 a partir de work/issues/os-comandos-brza-que-viram-o-pln-002.md: um passo por
comando, com as rodadas dos pontos de desenho listados na issue." — Anderson, na sessão `pln-002-comandos-brza`, em
2026-10-28.

## Entrevista

### Rodada 1 — o `brza tree` (enviada 2026-10-28)

**Apresentado antes:**
- **O P0:** o despacho `brza X` → `brza-X` é feito pela `brza-cli-subcomandos`, fora desta sessão. O checkout principal
  do `brza-studio` está sujo e com a `master` local atrás da `origin/master` (`7e9e0d18948` contra `d7f4e5b5618`).
- **Os worktrees de hoje:** ficam todos em `.worktrees/`. As branches nasceram de `origin/master`, pelo reflog de
  `feat/pln-001-p48` e `feat/pln-001-p44-p47`.
- **O `brza-sessions --checkout`:** só abre o chat (`scripts/brza/brza-sessions:115,135`).
- **O conserto do node_modules:** foi `pnpm install --offline --frozen-lockfile` no próprio worktree, em menos de 1 s
  ([o worklog do ▶ e do ⤢](../../work/worklogs/2026-10-27-o-executar-e-o-expandir-do-orca-fixfy-no-chat.md), linhas
  48-52).
- **Os órfãos:**
  - o `conferencia-p52-p53` é worktree registrado, em detached HEAD;
  - o `chat-markdown-largura-e-links` é só um diretório com `.cache/`, sem registro.
- **A regra "na `origin/master`":** deixaria o `--rm` apagar as branches sem commit próprio, como `feat/pln-001-p44-p47`
  e `feat/pln-001-p48`.

Respondida em 2026-10-28, na sessão `pln-002-comandos-brza`.

1. **O `tree` abre também o chat?** Opções:
   - só cria o worktree, instala e imprime o caminho (recomendada). Custo: um segundo comando por quem abre a sessão. Se
     paga: agora, porque o `tree` não depende do app aberto nem da interface do `sessions`;
   - `--chat <nome>` opcional, que chama o `brza-sessions --checkout` no fim. Custo: o `tree` passa a depender do app e da
     interface do `sessions`, a combinar com a 2d. Se paga: depois que o `list/send/close` fechar;
   - sempre abre o chat. Custo: quem quer o worktree só para `dev`, `test` ou worker abre sessão à toa. Se paga: nunca, no
     uso levantado.

   **Decidido — `--chat <nome>` opcional.** O `tree` chama o `--checkout` que já existe, sem esperar o `list/send/close`.

2. **De que base sai a branch?** Opções:
   - `git fetch origin` e a branch de `origin/master`, com `--base <ref>` opcional (recomendada). Custo: um fetch pela
     chave `personal` por chamada. Se paga: agora, porque a `master` local está atrás;
   - `origin/master` sem fetch. Custo: pode sair de base velha sem avisar. Se paga: só offline;
   - o `HEAD` do checkout principal. Custo: herda o checkout sujo e atrasado. Se paga: nunca, para trabalho de plano.

   **Decidido — fetch e `origin/master`, com `--base <ref>`.**

3. **Como instala sem o node_modules por symlink?** Opções:
   - `pnpm install --offline --frozen-lockfile` dentro do worktree, com falha clara que diz o comando online
     (recomendada). Custo: menos de 1 s; falha quando há dependência nova. Se paga: agora;
   - offline e depois online, sozinho. Custo: rede e minutos no pior caso, sem aviso. Se paga: quando o offline falhar na
     prática, o que não se mediu;
   - não instalar. Custo: o `verifyDepsBeforeRun` já derrubou o checkout principal uma vez. Se paga: nunca.

   **Decidido — offline, com falha clara.**

4. **Qual a regra do `--rm`?** Opções:
   - remove se o `HEAD` é ancestral da `origin/master` e o worktree está limpo; pede `--force` à branch sem commit
     próprio; trata o diretório órfão sem registro (recomendada). Custo: umas 30 linhas a mais. Se paga: no primeiro
     `--rm`;
   - só a regra da issue. Custo: o diretório órfão fica sem proteção, e a branch vazia passa por mergeada. Se paga: nunca,
     porque a perda é irreversível;
   - o `brza worktree rm` do app. Custo: não se conferiu se ele remove do disco e do git. Se paga: se o app guardar estado
     fora do `git worktree list`, o que não se mediu.

   **Decidido — merge, limpo e órfãos.**

### Rodada 2 — o `brza dev` e o baseline do `brza test` (enviada 2026-10-28)

**Apresentado antes:**
- **O seed:** o `pnpm dev:seed-profile` falha quando o perfil já tem estado (`config/scripts/dev-profile-seed.mjs:126-128`).
- **Um build por worktree:** cada worktree tem perfil e portas próprios (`config/scripts/dev-instance-isolation.mjs:90-111`).
  O lock de instância única é por `userData`, então dois builds no mesmo worktree colidem.
- **O pid:** o runner grava o `runnerPid` em `out/dev-instance.json`, não o apaga ao sair, e escala de SIGTERM para
  SIGKILL em 5 s (`config/scripts/run-electron-vite-dev.mjs:593-645`). Os dois pids em disco são de processos mortos.
- **O baseline:** nenhuma nota registra como foi refeito.

Respondida em 2026-10-28, na sessão `pln-002-comandos-brza`.

1. **O `dev` semeia o perfil por padrão?** Opções:
   - só se o perfil do worktree está vazio, com `--no-seed` e `--reset` opcionais (recomendada). Custo: lê o perfil do
     `brza-dev` ou do app instalado na primeira subida. Se paga: agora, porque sem seed o build abre vazio e com a
     Interface de Chat desligada;
   - nunca semeia. Custo: toda conferência começa configurando o app à mão. Se paga: nunca;
   - sempre com `--reset`. Custo: perde o estado da conferência anterior. Se paga: nunca.

   **Decidido — só se o perfil está vazio.**

2. **Quantos builds por worktree, e de onde o `--stop` tira o pid?** Opções:
   - um por worktree, com o `runnerPid` de `out/dev-instance.json`, conferido vivo e como runner antes do SIGTERM
     (recomendada). Custo: umas 40 linhas. Se paga: agora;
   - vários por worktree. Custo: mexer no `dev-instance-isolation.mjs` do `brza-studio`. Se paga: nenhum caso levantado
     precisa;
   - pid próprio em `~/.local/state`. Custo: duplica o registro do runner. Se paga: nunca.

   **Decidido — um, pelo `dev-instance.json`.**

3. **A janela sobe visível ou em background?** Opções:
   - visível, com `--background` opcional, que põe `ORCA_BACKGROUND_LAUNCH=1` (recomendada). Custo: o agente que esquecer
     o flag rouba o foco. Se paga: agora, porque as conferências são com Anderson olhando;
   - background, com `--visible` opcional. Custo: na conferência, a janela não aparece sem o flag. Se paga: se a maioria
     das chamadas for de agente, o que não se mediu.

   **Decidido — visível, com `--background` opcional.**

4. **De onde o `test` tira o baseline da master?** Opções:
   - worktree temporário da `origin/master`, pelo código do `tree`, rodando só os arquivos que falharam, removido no fim
     (recomendada). Custo: segundos de criação e install, mais a corrida. Se paga: agora, porque não toca o checkout
     principal;
   - checkout principal com stash. Custo: mexe no que outras sessões usam. Se paga: nunca;
   - sem baseline. Custo: o julgamento volta à mão. Se paga: só se o baseline ficar caro, o que não se mediu.

   **Decidido — worktree temporário.**

### Rodada 3 — o `brza test`, o `brza app install` e o `brza_runtime.py` (enviada 2026-10-28)

**Apresentado antes:**
- **O `check:changed`:** sem `--base`, ele cai em `origin/main`, que não existe no `brza-studio`
  (`config/scripts/check-changed.mjs:48,64`).
- **O build:** o `build:mac` grava na versão o `HEAD` de onde roda (`config/scripts/build-mac-local.mjs:22-30`). O alvo
  padrão é `dir`.
- **O app aberto:** o chat roda dentro do `/Applications/BrzA Studio.app`, e o `claude-brza` e os `brza-*` chamam o CLI
  dele. Ninguém mediu o que o `ditto` faz com o app aberto.
- **O que o P0 deixa para o `app install`:**
  - a reinstalação, com a conferência do `brza sessions --help` no chat e no terminal;
  - a troca de `brza-install`/`brza-run` por `brza install`/`brza run` na ajuda dos scripts e no `CLAUDE.md`.
- **A duplicação:** o `canonicalize` e o `send_to_chat` estão iguais em `brza-run:109-133` e `brza-sessions:82-100`.

Respondida em 2026-10-28, na sessão `pln-002-comandos-brza`.

1. **O que o `test` roda?** Opções:
   - os testes dos caminhos alterados contra `origin/master` e o `check:changed --base=origin/master`, sempre com a base
     injetada (recomendada). Custo: o tempo do `check:changed`, que não se mediu. Se paga: agora, porque o `--base`
     esquecido já quebrou a corrida;
   - só o vitest por caminho. Custo: lint, tipos e ratchets voltam à mão. Se paga: só se o `check:changed` for lento demais.

   **Decidido — vitest e `check:changed`.**

2. **O `app install` pede confirmação antes de sobrescrever?** Opções:
   - pergunta antes do `ditto`, recusa com o app aberto (saída 2) sem `--yes` e só apaga `dist` com `--clean`
     (recomendada). Custo: um `--yes` a mais. Se paga: na primeira vez com sessões abertas;
   - sem confirmação. Custo: a sessão que roda o comando pode derrubar a si mesma e às outras. Se paga: nunca;
   - instala ao lado e troca no fim. Custo: mais 1,8 GB temporário. Se paga: se a falha no meio do `ditto` virar problema.

   **Decidido — confirma e recusa com o app aberto.**

3. **De que checkout o `app install` constrói?** Opções:
   - um worktree da `origin/master` pelo código do `tree`, com `--from <caminho>` e `--dmg` opcionais (recomendada).
     Custo: um worktree e um install a mais por build. Se paga: agora, porque o checkout principal está sujo;
   - sempre do checkout principal. Custo: constrói o que estiver lá. Se paga: nunca;
   - do diretório atual. Custo: o resultado depende de onde a sessão está. Se paga: para testar um worktree antes do
     merge, que o `--from` também cobre.

   **Decidido — worktree da `origin/master`.**

4. **O `canonicalize` e o `send_to_chat` vão para o `brza_runtime.py`?** Opções:
   - sim, e o runtime ganha a constante `STUDIO`, do checkout do `brza-studio`; o contrato só cresce (recomendada). Custo:
     ajustar os patches de `test_brza_sessions.py:62-76` e `test_brza_scripts.py:110-113`. Se paga: no primeiro
     `sessions send`;
   - não. Custo: três cópias do envio. Se paga: nunca;
   - módulo novo `brza_chat.py`. Custo: mais um arquivo. Se paga: se o runtime passar de ~200 linhas (tem 77).

   **Decidido — sim, com o `STUDIO`.**

## Worklogs

- 2026-10-28 — P0, o despacho, feito pela `brza-cli-subcomandos` em `brza-studio@9a81e65c852`. A reinstalação e a troca
  dos textos ficam para o `brza app install`.
  [O CLI brza despacha o subcomando desconhecido ao brza-X do PATH](../../work/worklogs/2026-10-28-o-cli-brza-despacha-ao-brza-x-do-path.md)
- 2026-10-28 — aberto; o Terreno foi levantado e a R1 fechou.
  [O PLN-002 escrito: os comandos brza, com as rodadas de desenho](../../work/worklogs/2026-10-28-pln-002-comandos-brza.md)
