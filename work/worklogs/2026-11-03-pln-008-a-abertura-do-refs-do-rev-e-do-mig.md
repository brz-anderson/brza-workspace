---
scope:
  - workspace
refs:
  - PLN-008
---

# A abertura do PLN-008: o refs nos worklogs, o REV e o MIG

Anderson propôs IDs de plano, revisão e migração em `tags` nos worklogs. Três rodadas trocaram o `tags` por um `refs:`
preenchido pelo `brza note commit`, deram `REV-NNN` às revisões e `MIG-NNN` às migrações, e abriram o
[PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md),
parado antes do Desenho.

- **O MIG veio do modelo da Fixfy, com dois ajustes.** Lidos o `docs/migrations/README.md` do `flutter-template` e o
  `docs/migration/README.md` do `fixfy_flutter`: a migração é divergência entre o disco e a norma, e sai do diretório ao
  concluir. Aqui ela é issue `type: migration` e fica com `status: done`, porque o `refs:` confere a existência.
- **Dois `designer` em paralelo**, um defendendo o MIG como plano e outro atacando, a pedido de Anderson. A síntese mudou
  a recomendação: a definição do ataque, no lugar que a defesa apontou para a fila. Os dois gravaram o aprendizado em
  `.claude/agent-memory/designer/project_porte-da-fixfy-regua-sem-lastro.md`.
- **As skills entraram no pedido.** Depois da R3, Anderson pediu: "Temos também que criar/adaptar skills para a
  criação, revisão e execução dessas novas notas". É o item 4 do Pedido; criar ou adaptar vai ao Desenho.
- **O frontmatter para o coordenador entrou como item 5.** Anderson pediu um levantamento de "como o frontmatter das
  notas pode melhorar visando um nelhor desempenhi no fluxo do coordenador", com o `sessionId` e o runtime. Um
  `collector` varreu as 4 branches: nenhuma nota com `blocks` nem `deadline`, `priority` em 8 de 32 issues, e o índice
  sem esses campos. As R4 e R5 deixaram sessão, runtime, conta e modelo na medição (consertando o `workstream` nulo, a
  conta `home` e o `session` do índice), puseram aviso de `priority` no commit, os campos de pressão, o `owner` e as
  horas no índice, `estimate_h` opcional na issue, tiraram o `date` dos worklogs e deixaram o `depends_on` para depois
  do `refs:`.
- **A data no nome de issues e decisões ficou de fora (R6).** A chegada já está no índice e no `opened`, e o rename
  mexeria em 95 links e descolaria o id do nome. No lugar, um `brza note ls` que lista pelo índice.
- **O que é norma comum:** o `work/README.md`, o `plans/README.md`, o checador e o `brza-note` moram no
  `brza-workflow`; os passos do PLN-008 mexem lá e chegam aqui pelo `brza sync`.
