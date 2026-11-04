---
status: open
description: Renomear uma issue e recalcular o refs no mesmo brza note commit grava o slug novo no refs, e não a identidade preservada.
scope:
  - brza-workflow
opened: 2026-11-03
owner: Anderson
tags:
  - tooling
---

# O refs grava o slug novo quando o commit renomeia a issue

Origem: o P8 do [PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md),
achado pela sessão `d11-tools-kit` em 2026-11-03. Anderson escolheu "Issue no workspace (Recomendado)" na Rodada 18.

## O problema

A identidade de uma issue é o slug da criação, que o rename não muda (`check_notes.py:269`, `issue_id_for_path`; o
contrato do P1 do PLN-008). Quando o mesmo `brza note commit` renomeia a issue e recalcula o `refs` de um worklog que a
cita, o índice ainda não tem o caminho novo, e o `git log --follow` ainda não vê o rename. O extrator então grava o
slug novo no `refs`, e o checador o aceita pelo mesmo motivo. Depois do commit, o checador acusa `ref-not-found`, e a
linha precisa ser corrigida à mão.

Reprodução no `tools-kit`: o `9a40746` renomeou as duas issues e gravou os slugs novos no `refs` de dois worklogs; o
`ffc0cf7` os voltou à identidade antiga.

## O que falta decidir

- O extrator e o checador resolvem a identidade pelo rename que está sendo commitado, lido do índice do git (`git diff
  --cached -M`), antes do índice da master e do `git log --follow`.
- Um teste de CLI que renomeia uma issue e recalcula o `refs` no mesmo commit.
