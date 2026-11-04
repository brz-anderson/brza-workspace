---
status: open
description: O brza-note do núcleo guarda o mapa e a flag --bootstrap-pln008 de uma migração única deste workspace.
scope:
  - brza-workflow
opened: 2026-11-03
owner: Anderson
tags:
  - tooling
---

# O núcleo guarda o bootstrap da migração do PLN-008

Origem: achado A7 de [REV-006: A entrega do PLN-008 contra o Pedido e a Cobertura](../reviews/REV-006-pln-008-p7-a-entrega.md),
na revisão do [PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md).

## O problema

O `bin/brza-note` do `brza-workflow` traz `PLN008_BOOTSTRAP` (`:131-178`), com os nomes dos workstreams deste
workspace, e a flag `brza note index --bootstrap-pln008` (`:1410`). A MIG-001 está concluída, e o código não tem mais uso
aqui. Como o `brza-workflow` serve outros workspaces pelo `brza init`, o núcleo carrega uma migração que não é deles.

## O que falta decidir

- Tirar o bootstrap e a flag do núcleo, com os testes que dependem deles, ou movê-los para junto do
  `scripts/migrate_pln008.py`, que já é próprio desta migração.
