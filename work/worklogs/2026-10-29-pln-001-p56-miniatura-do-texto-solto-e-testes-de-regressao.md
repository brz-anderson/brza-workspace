---
scope:
  - brza-studio
date: 2026-10-29
tags:
  - chat
---

# O P56 do PLN-001 e os testes de regressão do P26.4, do P43.4 e do P44.4

Anderson autorizou o P56, o P26.4, o P43.4 e o P44.4 do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md)
na sessão do `brza-workspace` de 2026-10-29, ao escolher "P56 e os testes pendentes" numa rodada de opções. O P57 e os
casos manuais ficaram fora. Os passos rodaram na sessão `pln-001-p56`, aberta no `brza-studio`, direto na `master`, com
push e sem PR, como o pedido mandou. A evidência detalhada está em cada passo do plano.

## O P56 — a miniatura do caminho ou da URL de imagem solto no texto

Commit `brza-studio@fc43b03b9ef`.

- **O plugin.** O `remarkBrzaImageMentions` (`src/renderer/src/components/native-chat/brza/brza-image-mention-markdown.ts`)
  acha o link cujo alvo é imagem: o caminho em código inline que existe, o `[x](a.png)` e a URL http(s). Depois do bloco
  que o nomeia, entra um nó que o `BrzaImageMention.tsx` desenha com o `NativeChatMarkdownImage`. O link fica.
- **A ordem dos plugins**, que o passo pedia conferir: o de links de arquivo roda antes dos da extensão, e o do BrzA vê o
  link que ele cria no código inline, só para o caminho que existe.
- **Uma vez por mensagem.** A resposta que veio em streaming fica cortada em blocos, cada um com o seu parse. O plugin
  guarda a primeira menção de cada imagem num mapa da mensagem, e o `![]()` da mesma imagem conta como menção.
- **Só com a mensagem terminada, e só se abre.** O plugin só entra sem `streaming`. A miniatura fica montada e invisível
  até a imagem carregar, para a carga perto da tela seguir disparando; a falha não mostra nada.
- **Os testes.** O do plugin, com 4 casos, falhou antes pelo módulo ausente. O caso novo em
  `NativeChatMarkdown.image-preview.test.tsx` falhou pela asserção: os links existiam, sem miniatura. Depois, os dois
  arquivos → 39 passed, e o `pnpm tc:web` → exit 0.

No caminho, a primeira versão desenhava duas miniaturas para o mesmo caminho citado duas vezes no parágrafo. O link que
o plugin de links cria não tem `position`, e as duas menções empatavam. A menção passou a se identificar pela ordem no
bloco.

## Os testes de regressão

Cada um passou com o código de hoje, sem mexer no código:

- **P26.4**, `brza-studio@8e708f9790d` — `src/main/updater/updater-enabled.test.ts`: o `isUpdaterEnabled()` dá
  verdadeiro com `1.4.242` empacotado e falso com `1.4.242-local.1.abc` → 2 passed.
- **P43.4**, `brza-studio@2e263df152f` — `mobile/.../brza/brza-mobile-tool-glyphs.test.ts`: git → `GitBranch`, GitHub
  → `GitPullRequest` e Jira → `SquareKanban` (X10) → 1 passed.
- **P44.4**, `brza-studio@8850460267c` — um caso em `src/shared/native-chat/tools/brza/brza-tool-line-title.test.ts`, e
  não no teste do upstream: o comando sem categoria do BrzA fica com o verbo, o alvo e o título do upstream → 6 passed.

A `## Regressão` do plano perdeu as três marcas de "teste a escrever".

## Desvios

- **X29** — a miniatura entra depois do bloco que nomeia a imagem: no título e na tabela, depois deles; no item de lista
  e na citação, dentro deles.
- **X30** — o `![]()` que vem depois do link não apaga a miniatura da primeira menção, e a imagem aparece duas vezes.
- **X31** — a miniatura tem 96 px de altura, como a da linha da ferramenta, e fica invisível até carregar.

## O check

O `pnpm check:changed --base=origin/master --maxWorkers=2` do P56 deu 20 de 21, em 107 s. O vermelho é o import
boundaries, pelo `external-subcommand.ts`, preexistente e na issue de mesmo assunto. Os testes unitários passaram. Os
três testes de regressão rodaram cada um pelo seu comando, com o lint e o format do hook de commit.

## O que fica

- O C12, a conferência no BrzA Studio de uma resposta com um print por caminho em código inline e outra com uma URL de
  imagem. Fica com Anderson, no build único dos casos manuais, junto do C1 ao C7, do C10, do C11 e do C14.
- O P57, a conferência das quatro partes da prévia, com Anderson.
- O X10 segue a conferir com Anderson: o teste do P43.4 prende a escolha de hoje.
- O mobile não ganha a miniatura do texto solto, como no P55.
