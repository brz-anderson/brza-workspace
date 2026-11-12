---
scope:
  - workspace
tags:
  - tooling
  - planning
refs:
  - PLN-021
sessions:
  - 01a1c7c8-3571-7120-bb0f-1125dc3e36ea
---

# O PLN-021: o código em inglês do P11

Os subpassos 2 e 4 do [PLN-021: O plano roda por uma sessão coordenadora, com scripts de apoio e artboards de tela](../../plans/PLN-021-o-plano-coordenado-e-os-artboards/PLN-021-plan.md). O código do subpasso 1 e do 3 já estava no `4350325`. O registro desses dois subpassos está em [O PLN-021: os defeitos do P11.1](2026-11-10-pln-021-p11-1-os-defeitos.md).

## O que se fez

- **O rename** de arquivo, função, classe, variável e chave de dado em `.claude/scripts/skillkit/`, `plan-runner/scripts/` e `screen-artboards/scripts/`, com as skills e o Desenho no mesmo vocabulário. Commit `0797029`.
- **A `meeting-runner`** só na fronteira do kit: `common.py`, `launch_persona.py`, `panel.py` e `tally.py`. O `_legacy_measure` traduz as chaves inglesas da medida para as que o tally já grava.
- **Três rodadas de revisão** do `reviewer` (Claude Opus). A rodada 3 trouxe A16–A19 (docstring e nome); A20–A25 caíram como falso. As quatro suítes: 56, 193, 56 e 323.
- **O que ficou de propósito:** `execucao.json`, `pedido.md`, `answered.data`, `last_send["origem"]`, os valores de protocolo e os rótulos de documento. O X10 registra `origem` e `data` como proposta, sem decisão.

## O que ficou aberto

- **O P9**, o aceite manual, a pedido de Anderson.
- **O X10**, se Anderson quiser a rodada sobre `origem` e `data`.

## Fora do workspace

- **O quê e onde:** `~/.npm/_logs/2026-11-10T16_39_22_141Z-debug-0.log`, deixado por um `npm test --grep=#12` na pasta `plan-runner/scripts` durante a revisão.
- **O risco:** log de depuração no diretório do usuário; o comando falhou porque essa pasta não tem `package.json`. Não altera o repositório.
- **Estado:** o arquivo segue no disco.
- **Como desfazer:** apagar o arquivo.

## Custo da tarefa

Não medida — sessão sem turno medido · até 00:04 de 2026-11-12, pelo `brza note commit` · sem o turno do commit
