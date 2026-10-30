---
scope:
  - workspace
---

# As notas em workstreams, e a `master` só com a norma

O pedido de Anderson, em 2026-10-30, na sessão `brza-workspace-73`: "divida os planos e crie worktrees no workspace por
frente, deixe apenas a norma na master, plans/ wiki/ e work/ seguem a mesma regra, na master apenas a norma". A
decisão está em
[As notas moram em workstreams, e a `master` guarda só a norma](../decisions/as-notas-moram-em-workstreams-e-a-master-guarda-so-a-norma.md).

## O que se fez

- **As rodadas:** quatro sobre o lugar dos worktrees, o que é norma, o merge da `master`, o link entre branches, o
  `brza note` e a forma do corte. O termo foi de "frente" a `track` e de `track` a `workstream`; o modelo de uma
  branch por plano caiu quando Anderson disse que o workstream é a frente de trabalho, e as frentes ficaram `studio`,
  `tools-kit` e `workspace`.
- **O código, por um subagente Sonnet:** o `brza-note` ganhou a raiz pelo workstream, o `--workstream`, o
  `workstream <nome>` e o `sync`, e recusa a `master`; o `check_notes.py` procura nas branches `workstream/*` o alvo
  que falta na árvore. `python3 -m unittest discover -s scripts/brza/tests` → 187 OK;
  `python3 .claude/skills/notes-checker/tests/run.py` → saída 0.
- **A norma, em `786f5b1` na `master`:** o `AGENTS.md`, o `CLAUDE.md`, o `README.md`, o `plans/README.md`, o
  `work/README.md` e a `plan-runner`, no texto aprovado com "A.1".
- **O corte:** as três branches nasceram de `786f5b1`, cada uma sem as notas das outras (`d6c8991`, `d527d78`,
  `f7273e4`); a `master` perdeu as notas em `4f0838f`, que entrou nos workstreams por `git merge -s ours`, para que o
  `brza note sync` de depois não apague nada. O `studio` ficou com 26 notas, o `tools-kit` com 33 e o `workspace` com 4,
  mais esta e a decisão.
- **O checador em cada worktree:** 0 erros. No `studio`, dois links do PLN-001 para o workspace da Fixfy
  (`../../../fixfy/…`) só resolviam do checkout principal; viraram citação em crase, como manda o `work/README.md`
  (`191ad6e`).
- **O PLN-003:** uma linha no `Retomar`, porque o Desenho pode contar com as notas na `master` e com o `brza note` de
  antes.

## O que ficou

- **O `brza sessions --checkout .worktrees/<nome>`:** o `--dry-run` monta o comando, mas o chat aberto de verdade num
  worktree do workspace ainda não foi testado.
- **O `move_note.py`** reescreve só os links do workstream em que roda; o link de outro workstream para a nota movida
  fica quebrado até alguém o corrigir lá, e o checador daquele workstream o acusa.
- **A decisão de 2026-10-29** cita a seção "Uma frente, uma sessão…", que agora se chama "Um workstream, uma
  sessão…"; fica como foi escrita.
