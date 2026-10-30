---
scope:
  - brza-studio
date: 2026-10-29
tags:
  - chat
---

# O P60 do PLN-001, o Markdown segue o chat

Anderson autorizou o P58, e depois o P59 e o P60 em paralelo, do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md)
na sessão do `brza-workspace` que gravou o pedido 31, em 2026-10-29: "e já execute os passos em paralelo". O P60 rodou
na sessão `pln-001-p60`, no worktree `.worktrees/pln-001-p60` do `brza-studio`, na branch `feat/pln-001-p60`, com
rebase e push direto na `master`, sem PR. A evidência detalhada está no passo, no plano.

## O P60 — o visualizador de Markdown segue o chat

Commit `brza-studio@a44e84add32`.

- **O campo.** O `markdownTheme` das configurações globais guarda o `followChat`, ligado por padrão, e o par de temas
  próprio, na forma do chat. A ausência segue o chat, e o padrão não é gravado.
- **O tema.** O `resolveMarkdownTheme` lê o resolvedor do P58 sem mudar o contrato dele: o tema do chat com o
  interruptor ligado, e o par próprio, no contraste 100, com ele desligado.
- **O olho e o lápis.** Levam na raiz o canvas do tema, e, com tema do catálogo, o remapeamento das variáveis do app
  que o chat já fazia. Seguindo o chat, levam também a fonte e o tamanho do texto do chat, com o zoom do editor por
  cima, e a fonte de código do chat no código.
- **O modo código.** Leva a fonte de código do chat. O fundo vem por variável CSS no contêiner, porque o tema do
  Monaco é global, e só quando o esquema do tema é o do app (R53.1).
- **A tela.** O `MarkdownThemeSetting`, ao lado da fonte do editor, com o interruptor e o `ChatThemePairPicker` do
  P58, inerte enquanto segue o chat.
- **Os testes.** O da função `markdownSurfaceTheme` (4 casos) falhou antes, pelo módulo ausente. O da tela tem 1 caso.
  Os 61 arquivos das áreas tocadas deram 509 passed; depois do rebase sobre o P62, com os de i18n, 70 arquivos deram
  555 passed.

## A rodada

- **R53.1** — no modo código, com o esquema do tema oposto ao do app, o Monaco fica como hoje. Anderson escolheu "Fica
  como hoje (Recomendado)", contra trocar o tema global e gerar CSS de tokens por instância. O D47 foi reescrito no
  lugar.

## Desvios

- **X38** — o modo código segue o chat só no esquema do app.
- **X39** — a sintaxe clara é o `vs`, que o app já usa, e não o light-plus, e o Monaco não ganha tema derivado.
- **X40** — o remapeamento de cores do chat e a normalização do par viraram funções compartilhadas, e o
  `settings-update.ts` não passa das 300 linhas.

## O check

O `pnpm check:changed --base=origin/master --maxWorkers=2` deu 24 de 27, em 1047 s. A primeira rodada foi interrompida
pelo reinício do app. Ela apontou o `anti-slop(no-object-parameters)` no parâmetro `value: object`, corrigido antes do
commit. Os três vermelhos são os do P58, já na `master` sem esta mudança: o `updater-enabled.test.ts:20`, o
`external-subcommand.ts` e os 2 casos de `open-uncommitted-entry.test.ts`.

## O que fica

O worktree e a branch saíram depois do push. O C17 e o P61 ficam com Anderson, no build do pedido 31, depois do P59.
