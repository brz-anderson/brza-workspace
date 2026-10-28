---
scope:
  - brza-studio
date: 2026-10-28
tags:
  - chat
  - design
---

# O pedido 30, a prévia de imagem no chat, desenhado

Anderson pediu para retomar o
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md)
e conduzir o pedido 30 ("seria mto bom se conseguicemos adicionar image preview no chat"), com as quatro partes da R34.2,
em entrevista e desenho, sem executar código. Saíram as rodadas R36, R39 e R42, o D42 ao D44 e o P54 ao P57.

## O que o levantamento achou

Levantado em `brza-studio@7e9e0d18948`, por um subagente Sonnet e conferido em disco:

- **Três das quatro partes já existem no upstream:**
  - o `![]()` da mensagem já vira imagem, por URL ou caminho local (`NativeChatMarkdownImage.tsx`);
  - o anexo enviado já aparece em miniatura (`NativeChatUserMessageRow.tsx:138-164`);
  - ampliar ao clicar já existe (`MarkdownImageLightbox.tsx` e `PanZoomImageDialog.tsx`).
- **A lacuna é a imagem de ferramenta.** Os dois decoders descartam o bloco `image` do `tool_result`: o ao vivo
  (`claude-structured-item-translation.ts:127-143`) e o do histórico (`transcript-record-blocks.ts:8-34`).
- **O caminho ou a URL de imagem solto no texto** vira link, mas não vira imagem.

## O que Anderson respondeu

- **R36:**
  - o motivo foi a imagem de ferramenta, e as outras três partes viram conferência;
  - a imagem é extraída para arquivo;
  - a miniatura aparece com a linha fechada;
  - só o desktop, por agora.
- **R39:**
  - o arquivo fica no temp, como o colar;
  - o texto solto ganha miniatura abaixo do parágrafo;
  - a URL remota carrega sozinha;
  - a linha mostra até 4 imagens, com "+N".
- **R42:**
  - o "+N" abre a linha;
  - a miniatura do texto entra ao terminar a mensagem;
  - o corte do P54 ao P57 foi aceito;
  - os passos rodam depois do P44 ao P50.

Todas as respostas foram a opção recomendada.

## O que se fez

- **Nenhum código.** Saíram só as rodadas, o D42 ao D44 no Desenho e o P54 ao P57 no F7, com a Cobertura.
- **As horas.** O plano soma 7,8 h a `estimate_h` e a `remaining_h`.
- **O P50.2.** A miniatura do `get_screenshot` do Figma fica com o P55 (PLN-001/R38.4). A sessão `pln-001-p44-p50`
  grava o `[-]` dele.
- **A numeração com a sessão paralela.** A `pln-001-p44-p50` edita o mesmo checkout e gravou a R37 e a R38 antes de mim.
  A minha rodada foi renumerada para R39. As duas sessões combinaram por correio:
  - a R40 e a R41 ficam com a `pln-001-p44-p50`;
  - o D42 ao D44 e o P54 ao P57 ficam com o pedido 30;
  - cada sessão commita só o seu trecho, com o índice montado a partir do HEAD.

## Pendente

O P54 ao P57, no `Retomar` do plano, depois do P44 ao P50 (R42.4).
