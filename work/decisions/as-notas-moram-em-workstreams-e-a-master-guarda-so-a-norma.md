---
status: done
scope:
  - workspace
opened: 2026-10-30
decided: 2026-10-30
decided_by: Anderson
tags:
  - tooling
---

# As notas moram em workstreams, e a `master` guarda só a norma

**Cada frente de trabalho é uma branch `workstream/<nome>`, com worktree em `.worktrees/<nome>` e os planos e as notas
dela; a `master` guarda só a norma, que chega aos workstreams pelo `git merge`.** Os de agora são o `studio`, o
`tools-kit` e o `workspace`; plano novo nasce no workstream da sessão que o abre; o link para outro workstream continua
relativo, e o checador o procura nas branches; o `brza note` grava no workstream do worktree, ou no que tem o plano da
branch `<tipo>/pln-NNN-<slug>` do `brza-studio`, ou no do `--workstream`, e recusa a `master`.

Decidido por Anderson em 2026-10-30, na sessão `brza-workspace-73`: o pedido "divida os planos e crie worktrees no
workspace por frente, deixe apenas a norma na master, plans/ wiki/ e work/ seguem a mesma regra, na master apenas a
norma"; "`workstream` fica melhor que `track`"; "os workstrems são `frentes de trabalho`, então o certo seria
`workstream/sprint-3` ou `workstrem/brza-studio`"; "studio / workspace / tools-kit"; as rodadas ".worktrees/<frente>
dentro", "Regras + ferramental", "git merge master na frente", "Relativo, e o checador olha as branches", "Procura o
plano nas branches", "No da sessão que o abre", "Cortar agora e avisar por correio", todas "(Recomendado)"; e, sobre
o texto, "A.1" ("Pode aplicar como está (Recomendado)"), com "B.1", "D.1" e "E.1" para o código e a classificação.

## Fundamento

- **Recusados:** uma branch por plano, porque o workstream é a frente e não o plano; o worktree fora do repositório,
  porque a função `claude` e o `claude-brza` teriam de aprender o caminho novo; as decisões na `master`, porque
  pediriam um passo de subida a cada fechamento; o `rebase`, que reescreve a branch já enviada; a URL do GitHub no
  link, que o `move_note` não reescreve.

## Onde mais está

- **A norma:** o `AGENTS.md`, "Cada workstream mora numa branch…" e "Um workstream, uma sessão…"; o
  `plans/README.md`; o `work/README.md`, "Commit"; a `plan-runner`.
- **O código:** o `brza-note` (`workstream`, `sync`, a raiz pelo workstream) e o `check_notes.py` (o link entre
  branches), em `786f5b1` na `master`.
- **O registro:** [As notas em workstreams, e a `master` só com a norma](../worklogs/2026-10-30-as-notas-em-workstreams-e-a-master-so-com-a-norma.md).
