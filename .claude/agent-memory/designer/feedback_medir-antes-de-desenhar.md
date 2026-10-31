---
name: feedback-medir-antes-de-desenhar
description: Anderson aceita pagar sonda antes do Desenho para trocar hipótese por fato; a sonda sem turno de modelo é o primeiro recurso do designer
metadata:
  type: feedback
---

Fato que pesa numa bifurcação se mede antes de virar opção: Anderson escolheu "sondar antes" nas duas vezes em que a
opção apareceu (PLN-004, R2.3 e R4.2, 2026-10-30), com o critério "no Desenho, com fato no lugar de hipótese".

**Why:** a sonda desmentiu duas hipóteses do desenho da Fixfy (o `.git` do worktree no sandbox do Codex, o commit do
`agy`), e um `D` escrito sobre hipótese teria de ser reescrito.

**How to apply:** antes de pôr uma alternativa na rodada, procure a sonda de custo zero — `codex debug prompt-input` com
`CODEX_HOME` temporário, `codex sandbox -- <cmd>` — e rode-a no scratch; o que pede turno de modelo ou aprovação de
Anderson vira ponto "quando rodam as sondas", com a R4.2 como precedente. Fato não sondado fica marcado "a conferir" no
próprio item. Ver também [[feedback-mecanismo-nativo-do-runtime]].
