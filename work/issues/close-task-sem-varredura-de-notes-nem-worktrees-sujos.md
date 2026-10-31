---
status: open
scope:
  - workspace
opened: 2026-10-31
trigger: O work/notes/ de algum workstream deixa de estar vazio, ou um worktree fica com mudança sem commit de um dia para o outro.
tags:
  - tooling
---

# O close-task não varre o work/notes/ do dia nem relata os worktrees sujos

Na triagem do porte das skills da Fixfy, em 2026-10-31, o `end-day-runner` de lá ficou fora porque o `close-task`
daqui cobre o principal: worklog, pendente, memória e commit (`.claude/skills/close-task/SKILL.md`). Sobram dois furos
que a de lá cobria, e Anderson escolheu registrá-los aqui, sem mexer no `close-task` agora:

- **A releitura do `work/notes/`.** O `work/README.md` diz que "a releitura é no encerramento do dia", e nenhuma skill
  a faz. O `close-task` é por tarefa, e não por dia.
- **Os outros worktrees com mudança sem commit.** O `end-day-runner` da Fixfy relata os worktrees sujos
  (`~/Projects/fixfy/fixfy-plugin/skills/end-day-runner/SKILL.md:99-103`); aqui há um por workstream, e o `close-task`
  só olha o do cwd.

Juntar o fim do dia ao `close-task` mudaria o que a trava do `/compact` espera (`CLAUDE.md`, "A trava de fechamento
antes do `/compact`"). Por isso a saída, quando o gatilho disparar, é rodada: um passo no `close-task`, uma skill de
fim de dia ou um verbo do `brza note`. A triagem está em
[O porte das skills da Fixfy para o workspace](../worklogs/2026-10-31-o-porte-das-skills-da-fixfy.md).
