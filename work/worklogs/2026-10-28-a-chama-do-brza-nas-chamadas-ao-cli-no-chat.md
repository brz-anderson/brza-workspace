---
scope:
  - brza-studio
date: 2026-10-28
tags:
  - chat
  - design
---

# A chama do BrzA, monocromática, nas chamadas ao CLI no chat

Anderson pediu um ícone monocromático só com a chama e os detalhes dela, tirado do launcher do `.app`, para marcar no
chat as chamadas ao `brza` feitas no terminal. O ícone foi criado e ligado ao chat no commit `7e9e0d18948` da `master`
do `brza-studio`, sobre `fbff699fa58`.

## O que Anderson respondeu

- **Ligar ao chat:** "ligar já". A outra opção era deixar só o arquivo e ligar depois.
- **Versão simplificada para 14 e 16 px:** não respondeu. Ficou a recomendada, uma versão só, com todos os detalhes.
- **Fechamento:** "Commit e push já", sem conferir antes no dev build.

## O que se fez

- **O ícone (`resources/brza-flame-mono.svg`).** O launcher não tem fonte vetorial: o `resources/logo.svg` só embute
  um PNG, e o `resources/icon-source/` ainda é o desenho do Orca. Por isso a chama foi vetorizada do
  `resources/build/icon.png`, de 1024 px, em quatro passos:
  - separar os pixels laranja do fundo;
  - tirar as partículas soltas em volta da chama;
  - passar pelo potrace;
  - normalizar para um `viewBox` de 24×24.

  Ficaram a chama, o circuito, os nós em anel, o `>_` e o `{}`. O resultado é um único `path` com `currentColor` e
  `evenodd`, com 7,3 KB. Em 14 px, o `>_`, o `{}` e os anéis viram textura, mas a silhueta e o tronco do circuito
  continuam legíveis.
- **A ligação ao chat.** A ligação entrou como a categoria `brzaCli` do módulo BrzA de categorias, em
  `src/shared/native-chat/tools/brza/brza-tool-categories.ts`, criado no P43 do PLN-001. Ela usa o logo `brza-logo`,
  desenhado pelo `BrzaFlameLogo.tsx` no desktop. No mobile, a marca cai no `Flame` do lucide, como os outros logos de
  marca pela R29.4.
  - **Só o glifo muda.** A linha e a corrida seguem sendo comando no texto e no i18n.
  - **O globo continua no navegador:** o comando de navegador, como `brza snapshot`, segue com o globo do upstream.
  - **A corrida inteira ganha a chama** só quando todos os comandos dela chamam o CLI.
- **O parser do CLI** (`src/shared/orca-browser-cli-commands.ts`) passou a aceitar `brza` além de `orca`, `orca-dev` e
  `orca-ide`, e ganhou o `runsOrcaCliCommand`. A detecção do navegador usa a mesma varredura, e por isso `brza snapshot`
  agora também é lido como navegador.
- **Testes.** Passaram 453 arquivos com 5120 testes de `native-chat` e do parser, e um teste garante que o traçado do
  componente é o mesmo do SVG em `resources/`. O `tc` e o typecheck do mobile passaram. O `pnpm run lint` falha em
  duas etapas, `audit:anti-slop` e `lint:ast-grep-gates`, mas só em arquivos que esta tarefa não tocou: os watchers de
  filesystem, `claude-message-fork.test.ts` e `native-chat-markdown-prompt.ts`.

## O que se aprendeu

- **A primeira versão ficou fora do módulo BrzA.** Ela foi escrita direto no `native-chat-tool-icon.ts` e conflitou
  no rebase com o P43, que chegou à `origin` durante a tarefa. Foi refeita dentro do módulo. Depois disso, o rebase
  conflitou de novo com o `fbff699fa58`, que registrou Skill, Firebase e Context7 na mesma lista, e as duas listas
  foram juntadas. Categoria nova de ferramenta mora em `tools/brza/`, e não em arquivo do upstream.
- **O comando é `brza`, mas os terminais do app põem o `orca` no PATH** (`src/shared/brand-identity.ts`). Os dois
  nomes contam como chamada ao CLI.

## O que ficou aberto

- **Conferir no dev build** uma linha de chat com `brza …`, para ver o alinhamento no slot real. Por enquanto só a
  prévia renderizada foi vista.
- **Para o P44 a P47 do PLN-001:** a `brzaCli` já é uma categoria de comando. A pendência "o comando que casa com mais
  de uma categoria" passa a incluir ela, como em `brza … && git commit`. Hoje vale a primeira da lista que casar.

## Fora do workspace

- **`/private/tmp/brza-icon/`**:
  - **O quê e onde:** um venv com `pillow`, `numpy`, `scipy` e `potracer`, e os scripts `scripts/mask.py` e
    `scripts/trace.py`, que refazem a vetorização a partir do `icon.png`.
  - **O risco:** nenhum, porque é diretório temporário.
  - **Estado:** ativo até o sistema limpar o `/private/tmp`.
  - **Como desfazer:** `rm -rf /private/tmp/brza-icon`.
- **`brza-flame-mono-a41c.html`**:
  - **O quê e onde:** a prévia do ícone no scratch deste chat, em
    `~/Library/Application Support/brza-studio/chat-scratch/76a22f374cd971e03654434b1f71b8ad/`.
  - **O risco:** nenhum.
  - **Estado:** fica enquanto o chat existir.
  - **Como desfazer:** apagar o arquivo.
