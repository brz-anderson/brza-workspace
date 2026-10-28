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

- **Retomar:** a entrevista está em curso, na sessão `pln-002-comandos-brza`. A R1, do `tree`, fechou, e as rodadas
  seguintes cobrem o `dev`, o `test`, o `app install`, o `brza_runtime.py`, o `brza-install`, o `doctor`, o `note` e a
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

## Worklogs

- 2026-10-28 — P0, o despacho, feito pela `brza-cli-subcomandos` em `brza-studio@9a81e65c852`. A reinstalação e a troca
  dos textos ficam para o `brza app install`.
  [O CLI brza despacha o subcomando desconhecido ao brza-X do PATH](../../work/worklogs/2026-10-28-o-cli-brza-despacha-ao-brza-x-do-path.md)
- 2026-10-28 — aberto; o Terreno foi levantado e a R1 fechou.
  [O PLN-002 escrito: os comandos brza, com as rodadas de desenho](../../work/worklogs/2026-10-28-pln-002-comandos-brza.md)
