---
scope:
  - brza-studio
date: 2026-10-28
tags:
  - chat
---

# O P55 do PLN-001, a miniatura na linha da ferramenta

Anderson autorizou o P55 do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md)
na sessão do `brza-workspace` de 2026-10-28 ("siga com o P55"), só ele: o P56 e o P57 ficaram fora. O passo rodou na
sessão `pln-001-p55`, aberta no `brza-studio`, direto na `master`, com push e sem PR, como o pedido mandou. Commit
`brza-studio@eca0bf772ba`. A evidência detalhada está no P55 do plano.

## O que se fez

- **O componente.** O `BrzaToolImageStrip` (`src/renderer/src/components/native-chat/brza/BrzaToolImageStrip.tsx`) mostra
  até quatro miniaturas de 96 px de altura, com a largura pela proporção, e um "+N" no lugar da quinta. O clique no "+N"
  abre a linha, e então a faixa mostra todas, com quebra.
- **A montagem.** Uma linha em `NativeChatToolLine.tsx`, abaixo do botão da linha e fora do `NativeChatExpandable`, com
  o `body?.images`. O `body` é o resultado tanto na linha da chamada quanto na do resultado solto.
- **A leitura e o clique.** Cada miniatura é o `NativeChatMarkdownImage`, sem cópia: o `ExpandableMarkdownImage` com o
  `PanZoomImageDialog`, o `useLocalImageSrc` com o acesso `chat-image` e a carga perto da tela. O caminho absoluto do
  temp que o P54 grava resolve fora do worktree, e o `chat-image` o autoriza pelo tipo do arquivo.
- **O teste.** `BrzaToolImageStrip.test.tsx`, com 3 casos: duas imagens na linha fechada, abaixo do título; seis, com
  quatro e o "+2", que abre a linha com as seis; sem `images`, nada muda. Antes do componente, os dois com imagens
  falharam pela asserção.
- **A conferência visual.** Numa fixture temporária, fora do commit (`pnpm fixtures:shot`), nos temas claro e escuro: a
  primeira versão encolhia as miniaturas com tarja, quando não cabiam lado a lado; a faixa passou a quebrar (X27).

## Desvios

- **X26** — o "+N" abre a linha, e as imagens todas aparecem na própria faixa, acima do corpo, e não dentro dele.
- **X27** — a faixa quebra também fechada: num painel estreito, o "+N" passa à segunda linha, em vez de cortado.
- **X28** — a mesma imagem duas vezes no resultado aparece uma vez: a `key` é o `path` ou a `url`, pela regra do
  react-doctor contra o índice.

## O check

O `pnpm check:changed --base=origin/master --maxWorkers=2` deu 19 de 21. Os dois vermelhos são preexistentes:

- o import boundaries, pelo `external-subcommand.ts`, na issue de mesmo assunto;
- 2 testes do `open-uncommitted-entry.test.ts`, que falham igual na `master` limpa (`44ed13bfec9`, com o P55 no
  `stash`).

A primeira corrida pegou a `key` por índice e o format da linha de montagem, corrigidos antes do commit. Cada corrida
leva cerca de 8 minutos com dois workers.

## O que fica

- O C11, a conferência no BrzA Studio com um `Read` de PNG, um `get_screenshot` do Figma e um print do browser. Fica com
  Anderson, no build único dos casos manuais.
- O P56 (a miniatura do texto solto), que espera a autorização de Anderson, e depois o P57.
