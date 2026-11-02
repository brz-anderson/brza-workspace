---
scope:
  - brza-studio
date: 2026-11-02
tags:
  - release
---

# P77: os quatro pequenos consertos depois do sync da v1.4.246

O P77 do PLN-001, do pedido 39 (R65.4), feito pela sessão `pln-001-pedido-39-consertos` no worktree
`.worktrees/pln-001-pedido-39-consertos` do `brza-studio`. Commit
[`ecc4a13d456`](https://github.com/brz-anderson/brza-studio/commit/ecc4a13d456), na `master`, com o push direto
(`2738100d3f5..ecc4a13d456`). A issue é
[Pequenos consertos do fork depois do sync da v1.4.246](../issues/pequenos-consertos-do-fork-depois-do-sync-da-v1-4-246.md).

## O que se fez

- **Os "A conferir no passo" do D60, lidos no código antes de escrever.** A leitura se sustentou, e nada voltou como
  pergunta; só o tamanho do `asarUnpack` mudou (X68).
- **CLI empacotado.** O `packaged-cli-assets.test.ts` falhava com `Cannot find module './command-path-directory'`, e
  depois `'../lazy-worker-thread-host'`. O `asarUnpack` ganhou os 4 módulos do fecho do resolvedor. O build real emite
  chunks, e `out/main/chunks/**` já é desempacotado, então ele tende a sair autocontido (inferido).
- **Contrato cruzado.** As 5 chamadas do fork no `STRUCTURED_CALLS`, os params em `paramsFor` e um spy de
  `switchAccount` no host de teste (X69). O arquivo passou 40 de 40, na contagem 51 = 51.
- **Coreano.** 10 ocorrências de `ORCA` em 9 linhas do `ko.json` viraram `BrzA Studio`; os `ORCA_*` ficaram.
- **Fundo do código do Markdown.** O `markdownSurfaceTheme` compara com o modo que o Monaco pinta, via um
  `useMonacoDark` tirado do `useMonacoTheme` (X70). O teste novo falhou com a lógica antiga e passa com a nova.
- **Gates.** Pela regra da suíte completa uma vez, no merge: só `pnpm check:changed --base=origin/master
  --maxWorkers=2` (24 de 25 verdes), mais `tc:web` e `tc:node` depois do rebase. Suíte inteira: roda no merge, pela
  coordenação.

## Desvios

- **X68, X69 e X70**, todos no plano.

## O que ficou aberto

- **O C30 é de Anderson, no build novo, e não está marcado.** `brza foo` pelo app empacotado (o teste unitário usa `tsc`
  solto, e não prova o build real), o Markdown no modo código com o "Match Terminal" invertido e o coreano.
- **Duas falhas que não são deste commit.** `cross-version-structured-attention-frames.unit.test.ts` não carrega: a
  harness importa `src/shared/structured-agent-session-projection.ts` da v1.4.246, que a tag tem em
  `src/shared/agent-session/view/` (herdado, como as suítes que a issue já deixa de fora). E o teste do launcher macOS
  em `packaged-cli-assets.test.ts` falha com `TMPDIR` em `/var/folders` (symlink); com `TMPDIR` real passa 6 de 6.
- **A issue fica `open` até o C30.**
