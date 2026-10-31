---
name: feedback-mecanismo-nativo-do-runtime
description: Anderson recusa a recomendação que resolve por texto ou por chamada o que o runtime tem mecanismo nativo para resolver (skills, tools do agente); e quer a procedência gravada
metadata:
  type: feedback
---

Quando um runtime tem lugar nativo para a coisa, Anderson escolhe o lugar nativo, mesmo mais caro, e recusa a
recomendação que contorna com uma linha de texto ou com a flag da chamada.

**Why:** no PLN-004 (2026-10-30) ele recusou duas recomendações minhas nessa linha — R2.2: "uma linha no adaptador manda
ler `.claude/skills/<nome>/SKILL.md`" perdeu para "espelhar em `.agents/skills/`"; R3.2: "restringir pela chamada e
pelo texto, sem `tools` no `agy`" perdeu para "traduzir `tools` no `agy`". Na R3.1 ele acrescentou, por conta própria,
que a memória gravada fora do Claude registre o runtime que a gravou: procedência visível no git e na medição.

**How to apply:** ao recomendar, prefira a definição nativa do runtime (diretório de skills, frontmatter do agente,
campo de configuração) e ponha o contorno textual como alternativa, não como recomendada. Quando o desenho cruza
runtimes, ofereça registrar quem gravou. Ver também [[feedback-medir-antes-de-desenhar]].
