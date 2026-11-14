---
scope:
  - workspace
  - brza-workflow
refs:
  - PLN-017
  - PLN-024
---

# O PLN-024 do prefixo builder/ foi aberto

O pedido de Anderson, em 2026-11-14: abrir o plano da norma que aceita o prefixo `builder/`, sem executar nenhum passo.

## O que se fez

O `brza note plan-open prefixo-builder` no worktree `workstream/workspace` reservou o PLN-024. A linha `created` foi para a `master`, no commit `3903230`. O plano está em [PLN-024: Norma aceita o prefixo builder/ (workstream pessoal de Builder)](../../plans/PLN-024-prefixo-builder/PLN-024-plan.md), com `phase: design` e `status: open`. R1.1 a R1.4 ficaram decididas na abertura. Nenhum P foi executado e o `brza-workflow` não foi editado.

A branch local `builder/bob-the-builder` tinha sido apagada nesta sessão. Anderson pediu para recriá-la. Ela voltou a partir da `master` atual (`3903230`), sem upstream e sem push. Não é a frente deste plano.

Em seguida Anderson fechou a R1.5: a identidade de cada Builder fica no manifesto versionado `.brza/builders/<nome>.toml`, com o schema na norma. A config do worktree passa a ser só gerada e sobrescreve o autor git fixado no `.claude/settings.json` do workspace. A R1.6 continua aberta. O link quebrado de [PLN-017/P5: o brza shot lê visualBaseCss e mantém o literal antigo](2026-11-09-pln-017-p5-brza-shot.md) passou a apontar o PLN-017 na branch `workstream/playground` no GitHub. O resto desse worklog não mudou.

## O que ficou

A resposta de Anderson à R1.6 (rótulo `builder/<nome>` na medição ou só o nome curto). P4 espera essa resposta. P1 e P5 já podem ser pedidos. A criação de `builder/bob-the-builder` pelo `brza note builder` e o plano do Cursor ficam para outro PLN.
