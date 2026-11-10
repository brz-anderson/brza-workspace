---
name: estimativa-de-norma-pelo-sync
description: Antes de pôr "~1 h, uma linha de norma" numa opção que distribui algo pelo brza sync ou grava pelo brza doctor, confira se o comando leva aquele tipo de artefato ou escreve
metadata:
  type: feedback
---

Na R3 do PLN-020 (2026-11-09), o symlink `.agents/skills` no `core/` (R3.1) e a identidade no `.git/config` pelo
`brza doctor` (R3.3) foram apresentados a Anderson a ~1 h cada. Lido o código no desenho, os dois viraram ~2 h: o
`brza sync` não levava symlink (gravava arquivo com o texto do alvo e quebrava no sync seguinte) e o `brza doctor` só
lia, sem nenhuma conferência que escrevesse.

**Why:** o custo foi estimado pela norma ("uma linha"), sem abrir o comando que a entrega.

**How to apply:** opção que diz "o `brza sync` leva X" ou "o `brza doctor` faz Y" leva no `Custo:` a conferência de que o
comando já suporta aquilo; sem ela, rode uma sonda curta (o `SyncTest` herdado no scratch roda em ~2 s) ou marque a
estimativa abaixo de 80. Ainda não sei o que Anderson escolheu nos pontos 1–5 de D1/D2: registre aqui o critério quando
a rodada responder. Ver [[base-de-estimativa-brza-sessions]].
