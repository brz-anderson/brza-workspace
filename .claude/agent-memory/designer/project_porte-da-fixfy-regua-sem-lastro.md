---
name: project-porte-da-fixfy-regua-sem-lastro
description: Ao portar régua ou gênero da Fixfy/flutter-template, conferir se a regra cabe na norma daqui (ex.: a migração de lá se apaga ao concluir); e o custo de referência de uma revisão Opus (US$ 2,27)
metadata:
  type: project
---

Regra de revisão da Fixfy que a norma daqui não escreve vira achado sem régua, e pode bater contra uma escolha da norma:
o "estado presente" da `doc-governance.md` não existe aqui, e o `CLAUDE.md` e o `AGENTS.md` guardam medição datada e a
trava que saiu de propósito (conferido em 2026-10-31, defesa da ordem de revisão do `review-writer`).

**Why:** o reviewer cobra "achado sem régua nomeada é opinião"; portar a régua sem a regra gera achado falso em série.

**How to apply:** em todo porte de régua da Fixfy, faça o grep da regra na norma daqui antes de pô-la no texto; a que
falta vira ponto de rodada, não linha do rascunho. Para estimar custo de revisão, a única medida até 2026-10-31: a
revisão da entrega do PLN-002 (Opus, `general-purpose`) custou US$ 2,27, 457 s, contexto máximo de 147 mil tokens;
três revisores em paralelo eu estimei em ~3×, a conferir. Ver também [[feedback-medir-antes-de-desenhar]].

O mesmo vale para o porte de gênero de nota (o MIG-NNN, defesa e ataque de 2026-11-03): o `docs/migrations/` da Fixfy
e do template é fila de dívida disco-contra-norma e apaga o arquivo ao concluir; aqui o item fica onde nasceu
(`work/README.md`, linha do `archive/`), o `refs:` decidido confere existência, e a fila já é `work/issues/`. A triagem
de 2026-10-31 já pôs a `migration-writer` como "não serve aqui". Prefixo novo ao lado do `PLN` não custa só norma: o
`PLN` está fixo em regex no `brza-note`, no `brza_runtime.py` e no `measure.py` do `brza-workflow` (24 arquivos fora dos
testes). Antes de portar um gênero, confira o "nada se apaga" e o "único molde é o do plano" do `work/README.md`, e veja
se a parte "fila" não é issue. Desfecho da rodada: a registrar quando Anderson responder.
