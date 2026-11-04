---
status: open
description: A sessão aberta pelo brza sessions no brza-studio commitou sem os GIT_AUTHOR_* do settings.json, com o e-mail do .git/config local.
scope:
  - brza-workflow
  - brza-studio
opened: 2026-11-03
owner: Anderson
tags:
  - tooling
---

# A sessão no brza-studio não recebe a identidade do workspace

Origem: o D11 do P8 do [PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md).
Anderson escolheu "Issue e config agora (Recomendado)" na rodada do Fechamento, em 2026-11-03.

## O problema

O `CLAUDE.md` diz que o `env` do `.claude/settings.json` define `GIT_AUTHOR_*` e `GIT_COMMITTER_*` com o Gmail do
`brz-anderson`, e que isso vale para os commits do `brza-studio`. A sessão `d11-brza-studio`, aberta pelo `brza sessions`
com `--checkout ~/Projects/brza-studio`, não tinha essas variáveis no ambiente, só `GIT_EDITOR=true`. O commit `a6ef12c`
saiu com o `user.email` do `.git/config` local, `240569289+brz-anderson@users.noreply.github.com`. Anderson refez o
commit à mão (`1ef93b3`).

A mesma causa provável aparece na medição: as sessões `pln008-p8`, `d11-brza-workflow` e `d11-brza-studio`, com cwd
no `brza-workflow` e no `brza-studio`, não deixaram nenhuma linha em `.measurements/measurements.jsonl`. Sem o
`--settings` do workspace, elas também não tiveram os hooks. O levantamento das horas do PLN-008 achou isso
(`/private/tmp/pln008-p7/horas.md`, F8).

## O que já foi feito

- Em 2026-11-03, o `user.email` local do `brza-studio` passou a ser `brz.anderson.pereira@gmail.com`. Isso vale para os
  worktrees de lá.

## O que falta decidir

- Por que o `claude-brza` não passou o `--settings` do workspace a essa sessão: o checkout absoluto, o `git
  --git-common-dir` ou o caminho pelo `brza sessions`.
- Se o `brza doctor` deve conferir o `git var GIT_AUTHOR_IDENT` nas sessões de código.
