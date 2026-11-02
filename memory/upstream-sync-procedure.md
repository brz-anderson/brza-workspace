---
name: upstream-sync-procedure
description: "Como conduzir um sync do stablyai/orca no brza-studio — rebrand por script, linha de base na tag pura, pre-commit no merge, suítes sem concorrência"
metadata:
  node_type: memory
  type: project
  originSessionId: 7884383f-7a82-4f9c-a066-e1d749d6c2a6
  modified: 2026-11-02T18:07:10.020Z
---

O sync da v1.4.246 (2026-11-02) teve 404 arquivos em conflito, e o que funcionou fica aqui. O registro inteiro está no
worklog `2026-11-02-sync-da-v1-4-246-do-upstream.md`.

- **O rebrand é a maior parte dos conflitos.** Classifique cada trecho diff3: se a base e o nosso lado diferem só no
  vocabulário do rebrand, a resolução é o lado deles com a mesma troca. Os idiomas vão por merge de três vias, chave a
  chave.
- **Linha de base na tag pura.** Rode o lint e a suíte num worktree `--detach` da tag do upstream e compare arquivo a
  arquivo. Na v1.4.246, já falhavam 39 arquivos de teste e 3 ou 4 passos de lint.
- **O pre-commit morre no commit do merge.** O lint-staged em 18 mil arquivos é morto. Commite o merge com
  `--no-verify` e as correções em commit próprio, com o hook.
- **Uma suíte de cada vez.** A suíte inteira leva cerca de 16 min neste Mac. Rodada junto com outra suíte ou com agentes
  testando, ela dá centenas de `disk I/O error` do SQLite que não são do código.
- **Cada grupo de conflito vai a um `implementer`, com um brief comum** que traz as decisões das rodadas e as features a
  preservar. Depois, um `reviewer` faz a revisão adversária.

**Why:** cada sync fica maior sem isso; a linha de base separa o que é do merge do que já vem quebrado do upstream.

**How to apply:** no próximo sync, comece pela classificação dos conflitos e pela linha de base. Leve também a
conferência de identidade de [[brza-orca-coexistence]].
