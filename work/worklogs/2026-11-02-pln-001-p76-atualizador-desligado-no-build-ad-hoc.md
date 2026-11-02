---
scope:
  - brza-studio
date: 2026-11-02
tags:
  - release
---

# P76: o atualizador desligado no build ad hoc

O P76 do PLN-001, do pedido 39 (R65.3), feito pela sessão `pln-001-pedido-39-atualizador` no worktree
`.worktrees/pln-001-pedido-39-atualizador` do `brza-studio`. Commit
[`cdce032d264`](https://github.com/brz-anderson/brza-studio/commit/cdce032d264), na `master`, com o push direto
(`e9a3b9745bf..cdce032d264`). A issue é
[O atualizador está ligado no build ad hoc, sem manifesto para ler](../issues/o-atualizador-esta-ligado-no-build-ad-hoc.md).

## O que se fez

- **Os "A conferir no passo" do D59, lidos no código antes de escrever.** A leitura do D59 se sustentou, e nada voltou
  como pergunta. A versão não distingue o bundle ad hoc (`1.4.246-alpha.1` não tem o sufixo `-local`), e uma constante do
  `electron-vite` nasce antes da decisão de assinatura, que mora no `electron-builder.config.cjs`. O `afterPack` do
  darwin já escreve arquivos em `Resources`, então estampa o marcador `ad-hoc-signed` quando a identidade é `-`.
  Identidade nomeada (`CSC_NAME`) e release não têm o marcador, e o atualizador deles liga.
- **O código.** `src/main/updater/ad-hoc-signed-build.ts` (o leitor, só no macOS), a guarda do
  `updater-enabled.ts` ampliada, e `config/scripts/mac-ad-hoc-marker.cjs` chamado no `afterPack`. O nudge a `onorca.dev`
  e o `fetchChangelog` já ficavam atrás do `isUpdaterEnabled()`: o passo 3 virou a guarda mais um teste que o prende.
- **Os testes, antes do código.** Os três arquivos novos ou tocados falharam (dois por módulo ausente, um pela
  asserção); depois, 25 passed no conjunto. O teste do nudge no `updater.nudge-campaign.test.ts` falha sem a guarda
  ampliada, o que prova que ele a prende.
- **Os gates.** `pnpm check:changed --base=origin/master --maxWorkers=2` → 22 de 22 verdes. Rebase sobre o
  `e9a3b9745bf` (só chat nativo) e push direto.

## Desvios

- **X67 — o marcador em `Resources`, e o teste da guarda com o leitor mockado.** Está no plano. O P76.2 falava em
  testar a versão `1.4.246-alpha.1` "sem identidade de assinatura"; um teste de unidade não assina bundle.

## O que ficou aberto

- **O app já instalado (`1.4.246-alpha.1`) não ganha o desligamento:** ele foi empacotado sem o marcador. Só o build
  novo, como o da `v1.4.246-alpha.2`, o tem, desde que seja empacotado a partir desta `master`.
- **O C29 é de Anderson, no build novo, e não está marcado.** Sem o breadcrumb `updater_macos_installer_scheduling_configured`
  e sem GET a `onorca.dev` no log. A issue fica `open` até lá.
- **O marcador só se prova no bundle empacotado.** Não montei o build nem rodei o app, como combinado.
- **Um build assinado de verdade, quando existir, liga o atualizador:** sem `CSC_NAME`, o release não tem marcador. Se
  alguém assinar um build com `CSC_NAME` e ele não atualizar, o motivo é outro (o feed, o manifesto).
