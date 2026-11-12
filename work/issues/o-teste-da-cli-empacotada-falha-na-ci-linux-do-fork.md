---
status: open
description: O "loads worktree link validation from the installed CLI" do packaged-cli-assets.test.ts falha na CI Linux do fork, no projeto bun, com stdout vazio; passa no Mac e na tag pura do upstream.
scope:
  - brza-studio
opened: 2026-11-11
priority: medium
tags:
  - ci
  - cli
---

# O teste da CLI empacotada falha na CI Linux do fork

## O pedido

O sync da v1.4.256 ([O sync da v1.4.256 do upstream, que tirou o Bifurcar do fork](../worklogs/2026-11-11-sync-da-v1-4-256-do-upstream.md))
levou a suíte completa ao `node-next-compat.yml`, pela norma nova. A tag pura passou inteira, e a branch do sync ficou
com um teste vermelho que já falhava na `master` do fork antes do sync. O push seguiu pela R4, e o teste ficou aqui.
É o tipo de falha que [O CI agendado do `brza-studio` falha sem ninguém ver](../../../playground/work/issues/o-ci-agendado-do-brza-studio-falha-sem-ninguem-ver.md)
descreve.

## O que se sabe

- **O teste:** `src/main/cli/packaged-cli-assets.test.ts`, "loads worktree link validation from the installed CLI". Ele
  compila a CLI com `tsc`, empacota pelo `asarUnpack` do `config/electron-builder.config.cjs` e roda
  `out/cli/index.js worktree create … --pr 0 --json` com o `process.execPath`, que na CI é o Bun. O stdout sai vazio, e o
  `JSON.parse` dá "Unexpected EOF".
- **Onde falha:**
  - na CI diária da `master` `049a890a837`, rodada 43071063005, junto com o
    `orcad-remote-launch-address-space.test.ts`;
  - na branch `sync/v1.4.256` (`2b490c84526`), rodada 43124774284, nos dois Node.
- **Onde passa:** na `v1.4.256` pura (rodada 43122587247) e no Mac, tanto no `node-shared` quanto pelo `pnpm test`
  dentro do Bun.
- **Uma causa achada e resolvida no sync:** no Mac, o stderr mostrava `Cannot find module './command-path-directory'`,
  porque a CLI do fork carregava o resolver do `main`. O `2b490c84526` trocou isso por uma busca no PATH em
  `src/cli/brza/external-subcommand-path.ts`, e no Mac o teste passou. Na CI Linux, continuou falhando.
- **Falta saber:** o stderr da CLI na CI. O teste só o mostra quando o código de saída não é 1.

## O que fazer

1. Rodar o teste num container Linux com o Bun, ou empurrar uma branch que imprima o `result.stderr`, e ler a causa.
2. Consertar no fork: um módulo do fork carregado pela CLI que não vai no pacote, ou algo próprio do Linux.
3. Conferir na rodada seguinte da CI diária que a `master` passa a sair verde, fora o `orcad`, se ele for instável.
