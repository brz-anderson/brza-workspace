---
name: artboard-fica-na-raiz-do-scratch
description: "o ::orca-visual só renderiza o .html que está na raiz do ORCA_CHAT_SCRATCH_DIR; com subpasta no file=\"\", a caixa fica vazia"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 0d0d8b73-a12f-4555-ae6c-11ff5e785f90
  modified: 2026-11-02T20:09:36.622Z
---

O `::orca-visual{file="…"}` só carrega artboard que está **na raiz** do `ORCA_CHAT_SCRATCH_DIR`. Com subpasta
(`file="pln-007/brand/p2-lockups.html"`) não renderizou; copiado para a raiz, com 355 KB e imagens embutidas, carregou.

**Why:** no PLN-007, o artboard do P2 estava em `pln-007/brand/`, junto dos SVG gerados, e a rodada saiu sem a imagem.
Anderson avisou "não renderizou", e a rodada ficou parada até a cópia. O peso não era a causa, ao contrário dos L1–L3,
que passavam de 600 KB (ver [[artboard-le-o-componente-antes]] para a outra lição de artboard).

**How to apply:** ao gerar o artboard numa subpasta do scratch, copie o `.html` para a raiz antes de escrever a linha
`::orca-visual`, e use só o nome do arquivo em `file=`. O PNG de conferência pelo `brza shot` pode ficar onde estiver.
