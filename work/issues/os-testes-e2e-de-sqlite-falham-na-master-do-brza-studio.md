---
status: open
description: Quatro arquivos de teste e2e do `brza-studio` falham na `master` com "unable to open database file", com ou sem a mudança de ninguém.
scope:
  - brza-studio
opened: 2026-11-02
priority: low
tags:
  - tooling
---

# Os testes e2e de SQLite falham na master do brza-studio

Quatro arquivos de teste do `brza-studio` falham na `master` (`a3a89e3aaf5`), isolados e sem nenhuma mudança por cima, com
`Error: unable to open database file` (`ERR_SQLITE_ERROR`, `errcode: 14`):

- `tests/e2e/cross-version-wire/cross-version-registered-agents.unit.test.ts`
- `tests/e2e/cross-version-wire/cross-version-structured-attention-frames.unit.test.ts`
- `tests/e2e/cross-version-wire/cross-version-agent-session-wire.unit.test.ts` (o teste "executes every method a
  release-shaped checkout registers")
- `tests/e2e/helpers/persisted-profile-state.unit.test.ts` (dois testes)

Achado em 2026-11-02, na sessão do `brand`, ao conferir o P4 do
[PLN-007: A marca BrzA tem símbolo, logotipo e derivadas a partir da chama do app](../../plans/PLN-007-a-identidade-visual-da-marca-brza/PLN-007-plan.md).
O `pnpm check:changed --base=master` passou em 26 dos 27 checks, e o `unit tests` falhou em 3 testes de 53 873, só nesses
arquivos. Rodados com `pnpm test <os 4 arquivos>` no worktree do P4 e na `master` do checkout principal, deram o mesmo
resultado, nos dois. O `implementer` do P4 não os viu porque o conjunto de testes relacionados dele era menor: o rótulo
do seletor de ícones, em `src/shared/app-icon.ts`, é importado em muitos lugares e ampliou o conjunto para 5 372 arquivos.

A causa não foi investigada. O que se sabe: o erro vem do abrir um banco SQLite, e o `check:changed` do P3, no mesmo dia,
passou 21 de 21, porque a mudança dele não puxava esses testes.

## O pedido

Descobrir por que o SQLite não abre nesses testes (caminho temporário, permissão ou o runtime `bun` do macOS) e
consertar, ou marcá-los como dependentes do ambiente. Enquanto isso, qualquer mudança em módulo muito importado vai
falhar o `check:changed`, sem relação com ela.
