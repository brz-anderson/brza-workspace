---
scope:
  - brza-studio
tags:
  - chat
refs:
  - PLN-001
---

# O PLN-001 e o merge da v1.4.246 do upstream

Anderson pediu que esta sessão, que conduz o
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md),
trabalhe com a sessão `studio-75`. A `studio-75` faz o merge da `v1.4.246` do upstream no worktree
`.worktrees/sync-v1.4.246` do `brza-studio`, a partir de `abc5e78c243`, que já tem o P71.

## O acordo, pelo correio

- **A `master` do `brza-studio` fica congelada para o PLN-001** até o merge chegar a ela.
- **Os passos a preservar nos conflitos:** o P58 ao P60, o P62 ao P64, o P66, o P69, o P70 e o P71. A escolha forçada
  entre o upstream e um deles vai a Anderson como rodada, na sessão do merge.
- **Só esta sessão grava no PLN-001.** A sessão do merge manda o commit, a rodada com as respostas literais, os desvios e
  os testes, e fica com o worklog do sync.
- **Um build só:** o do merge, para os casos manuais e o P57, o P61 e o P65.

## A rodada de lá que toca o plano

Respondida por Anderson em 2026-11-02, na sessão do merge:
- **O alvo:** "Tag v1.4.246 (Recomendado)".
- **O rebrand dos textos novos:** "Tudo agora".
- **O P40 contra o #31241:** "Fica o do upstream (Recomendado)".
- **O P36 contra o #30955:** "Mantém o P36 (Recomendado)".

O P40 e o C14 viram `[-]` quando o merge chegar à `master`.

## Próximo

A devolução da `studio-75`, com o merge na `master`. Depois, o passo do sync no PLN-001 e o build dos casos manuais, com
Anderson.
