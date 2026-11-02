---
name: artboard-le-o-componente-antes
description: "Antes de desenhar um artboard sobre um componente do brza-studio, ler as classes dele — forma, tamanho, o que existe — e não desenhar de memória."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 0d0d8b73-a12f-4555-ae6c-11ff5e785f90
  modified: 2026-11-02T18:19:29.044Z
---

O artboard de um componente do app copia o componente real: forma, tamanho e o que ele mostra saem das classes no
código, lidas antes de desenhar.

**Why:** em 2026-11-02, no PLN-007, Anderson pediu "refaça o artboard do 6.2 com o botão redondo" — o botão de enviar
do app já é `size-8 rounded-full` (`NativeChatComposerActions.tsx:145`), e os artboards da R2.5 e da R6 o tinham
desenhado quadrado e de 24 px. O mesmo erro saiu no M5 da R2.6, que desenhou um título que o cabeçalho do painel não
tem. A escolha feita sobre um artboard infiel aprova o que o app não é.

**How to apply:** antes de montar o `.html`, `grep` das classes do componente (`rounded-*`, `size-*`, o que renderiza) e
uma linha no artboard citando o `arquivo:linha`. O que o artboard muda de propósito vai dito no texto da opção. Ver
também [[pln-007-marca-brza]].
