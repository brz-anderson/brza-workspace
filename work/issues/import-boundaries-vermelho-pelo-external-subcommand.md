---
status: open
scope:
  - brza-studio
opened: 2026-10-28
priority: medium
tags:
  - tooling
---

# O check de import boundaries está vermelho na master pelo `external-subcommand.ts` do `brza X`

Em 2026-10-28, o `pnpm check:changed --base=origin/master` dos workers do P53.4 e do P40 do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md)
falhou só no "import boundaries", num arquivo que nenhum dos dois tocou:

```console
$ node config/scripts/check-import-boundaries.mjs
[process-host-imports]
src/cli/external-subcommand.ts: new direct child_process import; use @orca/process-host
```

O `import { spawn } from 'node:child_process'` (`src/cli/external-subcommand.ts:1`) veio do `9a81e65c852`, o despacho
`brza X` → `brza-X` do PATH, que é o P0 do
[PLN-002: Os passos manuais que se repetem entre sessões viram comandos `brza`](../../plans/PLN-002-os-comandos-brza/PLN-002-plan.md).
Rodado na `master` em `9a81e65c852`, o gate já sai vermelho.

**Resposta de Anderson** na sessão `pln-001-retomar`, em 2026-10-28, pelo AskUserQuestion: "Seguir, e o conserto vai ao
PLN-002 (Recomendado)". O P53.4 (`1a6cbf3e14c`) e o P40 foram à `master` com o gate vermelho, registrado no relatório
de cada um.

## O pedido

Para a sessão que conduz o PLN-002: trocar o `spawn` do `src/cli/external-subcommand.ts` pelo `@orca/process-host`,
como o gate pede, com o teste do despacho verde, e conferir com
`node config/scripts/check-import-boundaries.mjs`, que deve sair sem a linha do `external-subcommand.ts`.
