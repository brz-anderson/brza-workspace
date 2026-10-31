---
name: project-porte-da-projeto-externo-regua-sem-lastro
description: Ao portar régua de revisão da projeto-externo, conferir se a regra está escrita na norma daqui; e o custo de referência de uma revisão Opus de entrega (US$ 2,27)
metadata:
  type: project
---

Regra de revisão da projeto-externo que a norma daqui não escreve vira achado sem régua, e pode bater contra uma escolha da norma:
o "estado presente" da `doc-governance.md` não existe aqui, e o `CLAUDE.md` e o `AGENTS.md` guardam medição datada e a
trava que saiu de propósito (conferido em 2026-10-31, defesa da ordem de revisão do `review-writer`).

**Why:** o reviewer cobra "achado sem régua nomeada é opinião"; portar a régua sem a regra gera achado falso em série.

**How to apply:** em todo porte de régua da projeto-externo, faça o grep da regra na norma daqui antes de pô-la no texto; a que
falta vira ponto de rodada, não linha do rascunho. Para estimar custo de revisão, a única medida até 2026-10-31: a
revisão da entrega do PLN-002 (Opus, `general-purpose`) custou US$ 2,27, 457 s, contexto máximo de 147 mil tokens;
três revisores em paralelo eu estimei em ~3×, a conferir. Ver também [[feedback-medir-antes-de-desenhar]].
