---
name: skill-evals-need-rules-the-repo-lacks
description: "No playground, o baseline sem skill lê os precedentes do repositório e empata; a expectativa de um eval só discrimina quando é de uma regra que o repositório ainda não tem"
metadata:
  node_type: memory
  type: project
  originSessionId: 4ff47083-be14-41f1-b06f-89dc276c02e7
  modified: 2026-11-09T22:46:05.673Z
---

Ao testar uma skill do playground com e sem ela (laço da `skill-creator`), o subagente sem skill acha no próprio repositório os briefings, worklogs e `.sessions/` das reuniões anteriores e reproduz a forma. Na iteração 1 da `meeting-runner` (2026-11-08) a skill empatou em 2 dos 3 casos (briefing 8/8 e síntese 9/9, com e sem); só discriminou onde a regra era nova (o `tally.py` com `--exclude-rater`, que explica o Fole 8,25).

**Why:** o repositório é o material de treino do baseline; um eval cuja resposta já está nos precedentes mede o repositório, não a skill. Descoberto ao ler o benchmark da iteração 1 (+0,11, com dois casos não discriminantes).

**How to apply:** escreva a expectativa de eval a partir da regra que a skill acrescenta e o repositório ainda não registra (na iteração 2: o sinal de fim por `brza orchestration send` com o `worker_done` só no encerramento; o `tally.py` como fonte). Reaproveite os baselines entre iterações enquanto o prompt não muda, para não pagar de novo. Confira o corretor por script: o meu primeiro tinha um `or True` que fazia a expectativa passar sempre. Ver [[skills-via-skill-creator]].

Na iteração 3/4 (2026-11-09, correções da P7), dois vazamentos novos: o enunciado que já nomeia o estado (`pending`, `stop_unknown`, "Worker stopped without reporting") deixa a linha de base acertar por raciocínio genérico (caso 4: 5/6 × 6/6); e a linha de base com a skill antiga usou um campo (`rodada_extra`) que só existia na skill viva do repositório, apesar da ordem de não lê-la (caso 6: 5/5 × 5/5). O que discriminou foi o mecanismo novo da skill (flags de subconjunto, molde com "Fatos lidos", ausência de comando de mailbox no briefing). Para a linha de base com a skill antiga, rode-a numa cópia do repositório sem a pasta viva da skill, ou aceite que ela mede o repositório.

No PLN-021 (2026-11-10), dois aprendizados novos. **Skill que abre sessão se testa com um `brza` falso no `PATH`** (`/private/tmp/pln021/evals/bin/brza`: registra cada chamada num log e devolve saída plausível, com o `shot` repassado ao verdadeiro), numa cópia do repositório em git novo; o log é o que o corretor lê, e nenhum chat de verdade abre. **A fixture não pode citar commit ou arquivo que não existam no repositório real:** a linha de base conferiu o `brza-studio` de verdade, viu que o commit do P1 do plano de mentira não existia e parou com razão, e o caso mediu a fixture, não a skill. De novo empatou o que o repositório ensina (o artboard de desktop pelas regras do `brza-client.md`, o diagnóstico de retomar pela invariante do `[x]`); discriminou o mecanismo novo (o executor e os consultores em sessão; a página web num artboard só).
