---
name: skill-evals-need-rules-the-repo-lacks
description: "No playground, o baseline sem skill lê os precedentes do repositório e empata; a expectativa de um eval só discrimina quando é de uma regra que o repositório ainda não tem"
metadata:
  node_type: memory
  type: project
  originSessionId: 4ff47083-be14-41f1-b06f-89dc276c02e7
  modified: 2026-11-09T07:29:42.255Z
---

Ao testar uma skill do playground com e sem ela (laço da `skill-creator`), o subagente sem skill acha no próprio repositório os briefings, worklogs e `.sessions/` das reuniões anteriores e reproduz a forma. Na iteração 1 da `meeting-runner` (2026-11-08) a skill empatou em 2 dos 3 casos (briefing 8/8 e síntese 9/9, com e sem); só discriminou onde a regra era nova (o `tally.py` com `--exclude-rater`, que explica o Fole 8,25).

**Why:** o repositório é o material de treino do baseline; um eval cuja resposta já está nos precedentes mede o repositório, não a skill. Descoberto ao ler o benchmark da iteração 1 (+0,11, com dois casos não discriminantes).

**How to apply:** escreva a expectativa de eval a partir da regra que a skill acrescenta e o repositório ainda não registra (na iteração 2: o sinal de fim por `brza orchestration send` com o `worker_done` só no encerramento; o `tally.py` como fonte). Reaproveite os baselines entre iterações enquanto o prompt não muda, para não pagar de novo. Confira o corretor por script: o meu primeiro tinha um `or True` que fazia a expectativa passar sempre. Ver [[skills-via-skill-creator]].
