---
status: open
description: O --approve do trusted-worker, rodado pela sessão no modo auto do Claude Code, é barrado como concessão de permissão; o spike do C5 do PLN-003 parou aí, e a aprovação de plugin não pode ser passo de agente.
scope:
  - workspace
opened: 2026-11-03
owner: Anderson
blocks: Os itens do spike do C5 do PLN-003 que só rodam com o plugin vivo nos apps — 1, 5 e 6, e a parte ao vivo de 2, 3 e 4.
trigger: Anderson roda o dev load com --approve nos dois apps, ou libera a regra de permissão.
tags:
  - tooling
---

# O --approve do plugin é barrado no modo auto

No spike do C5 do [PLN-003](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md), em 2026-11-03, o `dev
load` sem aprovação saiu com `approval_required` (código 3) nos dois apps, com o fingerprint
`ap1-aedbb65284d0297120a721e7e67266a2`. A Rodada 8 (R8.2) escolheu "CLI, com sua aprovação aqui", e o pedido seguinte,
vindo da sessão do `workspace`, mandou rodar o spike até o final.

## O que falhou

```bash
brza plugin dev load . --json --approve ap1-aedbb65284d0297120a721e7e67266a2
```

O classificador do modo auto do Claude Code barrou a chamada: "Permission for this action was denied by the Claude Code
auto mode classifier. Reason: [Permission Grant]". O plugin ficou `status: pending`, e o `plugin shot` recusou os dois
painéis: "local.brza-spike-c5 is waiting for approval, so BrzA Studio shows none of its panels or editors."

## Por que importa

- **O item 7 do C5 mede isso:** a aprovação de um `trusted-worker` não passa por agente no modo auto. O `brza install`
  do plugin (B3, R2.4) precisa de um passo de Anderson, no terminal ou na interface do app, por app.
- **A aprovação está amarrada ao conteúdo:** o fingerprint é o mesmo nos dois apps para os mesmos arquivos, e edição
  depois da aprovação, na pasta dev, não pede outra (o texto do próprio `approval_required`).

## Como destravar

Anderson roda, no terminal, em cada app; o fingerprint muda se os arquivos mudaram, e o `dev load` sem `--approve`
mostra o novo:

```bash
cd "/Users/andepb/Projects/brza-workspace/.worktrees/tools-kit/spikes/c5-plugin" && brza plugin dev load . --json
```

```bash
cd "/Users/andepb/Projects/brza-workspace/.worktrees/tools-kit/spikes/c5-plugin" && env -i HOME="$HOME" PATH="/usr/bin:/bin:$HOME/.local/bin:/opt/homebrew/bin" "/Applications/Orca.app/Contents/Resources/bin/orca" plugin dev load . --json
```

e repete cada um com o `--approve <fingerprint>` que ele imprimir. O `env -i` do segundo é o contorno de
[O CLI do Orca no chat do Studio fala com o Studio](o-cli-do-orca-no-chat-do-studio-fala-com-o-studio.md). Depois disso,
a sessão roda os itens 1 a 7 sem nova aprovação.
