---
name: licao-artboard-sobre-o-componente
description: Artboard de rodada deve partir do componente real do brza-studio; o do M5 do PLN-007 desenhou um título que o cabeçalho do chat não tem
metadata:
  type: feedback
---

Antes de desenhar o artboard de uma mudança de UI, abra o componente e o CSS que ela altera e desenhe o "hoje" a partir
deles.

**Why:** no PLN-007 (R2.6, 2026-10-31) o artboard do M5 pôs a chama "antes do título" do cabeçalho do painel do chat,
mas a `pane-title-bar` do chat é `data-chromeless`, transparente e só com as ações à direita — não há título. O
Desenho (2026-11-02) teve de redesenhar o M5 e levar a diferença à rodada. O mesmo artboard do E2 pintou o botão de
enviar no degradê sem que a rodada perguntasse, e o fio de 1,5 px contrariava o comentário "constant container border"
do composer.

**How to apply:** o "Hoje" de cada artboard cita o `arquivo:linha` do componente; tudo o que o artboard muda além da
pergunta (cor de botão, largura de borda) vira opção da rodada, e não detalhe embutido na imagem.
