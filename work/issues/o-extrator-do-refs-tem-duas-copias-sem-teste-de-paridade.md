---
status: open
description: O extrator do refs do D3 existe no brza-note e no checador, sem teste que confira que os dois dão o mesmo resultado.
scope:
  - brza-workflow
opened: 2026-11-03
owner: Anderson
tags:
  - tooling
---

# O extrator do refs tem duas cópias sem teste de paridade

Origem: achado A5 de [REV-006: A entrega do PLN-008 contra o Pedido e a Cobertura](../reviews/REV-006-pln-008-p7-a-entrega.md),
na revisão do [PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md).

## O problema

O D3 está implementado duas vezes no `brza-workflow`: em `bin/brza-note:180-187,536-596`, que o `brza note commit` e o
`scripts/migrate_pln008.py` usam, e em `core/.claude/skills/notes-checker/scripts/check_notes.py:72-79,417-460`. Na
revisão, as duas concordaram em 121 de 121 worklogs, mas nenhum teste confere isso, e o checador não compara o `refs`
gravado com o calculado: uma divergência não barra nada.

## O que falta decidir

- Um teste de paridade que rode as duas cópias sobre as mesmas entradas da tabela do D3, ou uma cópia só, importada
  pelo outro lado.
- A mudança da A4, no P8 do PLN-008, já mexe nas duas cópias: é o momento de menor custo para isso.
