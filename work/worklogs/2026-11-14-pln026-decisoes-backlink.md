---
scope:
  - workspace
tags:
  - tooling
---

# O PLN-026 aponta as treze decisões da auditoria

O [PLN-026: brza sessions e meeting-runner funcionam na cloud](../../plans/PLN-026-sessoes-e-meeting-runner-na-cloud/PLN-026-plan.md) ganhou a seção `## Decisões`, com um link para cada nota `pln026-justificativa-*`. As notas do Bauble e as caixas do plano não foram editadas.

## Desvio

O commit `c21d29020faa800e9fea55ec650939c823ab07d5` saiu pelo conector do GitHub com o autor Anderson Pereira Brzezinski (`brz.anderson.pereira@gmail.com`), e não `Bob The Builder <bob@brza.dev>`, porque o computador do Bauble não tem credencial de push. É desvio de autoria conhecido. O histórico não foi reescrito.

## Checador

```bash
python3 .claude/skills/notes-checker/scripts/check_notes.py --detail
```

rc 0. 0 erros e 0 avisos `backlink-missing`. Os 13 das decisões sumiram. O mesmo run avisou `review-without-number` em `work/reviews/2026-11-14-REV-pln026-pr-a-r1.md` e `work/reviews/2026-11-14-REV-pln026-pr-b-r2.md`, pareceres que já estavam na branch.
