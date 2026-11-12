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

# O PLN-021: os oito achados de texto

A Rodada 8 do [PLN-021: O plano roda por uma sessão coordenadora, com scripts de apoio e artboards de tela](../../plans/PLN-021-o-plano-coordenado-e-os-artboards/PLN-021-plan.md). Anderson respondeu "aplicar agora": aplicar os oito achados de texto agora, antes do P9.

## O que se fez

- **A1.** A Cobertura nomeia o passo e o teste de cada linha. Os C1–C4 estão em `## Casos manuais`, com Observado e Veredito em "—".
- **A2.** O Desenho cita as rodadas que fecharam cada contrato. Saíram os títulos "Em aberto" e as marcas `[sem lastro, menor]` das escolhas da R5.9.
- **A5.** O P9 lista os C1–C4, a sonda de permissão do X7 e a prova do `CODEX_MODEL`. O P10 lista o `close_check.py` e a medida pelo `--by-task` (R6.4). Os dois passos não foram executados.
- **A6.** O worklog do P11.1, que o `ac36476` não tinha: [O PLN-021: os defeitos do P11.1](2026-11-10-pln-021-p11-1-os-defeitos.md).
- **A7.** A linha `Executa` do P11 diz que a coordenação abriu a sessão, e que o `executor.py` não abriu o P11.
- **A8.** O Desenho acompanha o código: `wait_brza` devolve `(rc, dict)`, `list_states` recebe `cmd` e `ids`, o `veredito` fica no `executor.py`, o `open` exige `--checkout` ou `--tree`, o molde traz `cobre:`, e o `--apply` sem essa linha não roda e não grava.
- **A9.** `RE_DATE` em `plan_md.py`, `strip_measurement(text)` e `HERE` no README do kit, e `HERE` no trecho de import do kit no Desenho. O `AQUI` que descreve a `meeting-runner` ficou.
- **A10.** A ordem dos passos é P8 → P11 → P9 → P10.

## O que ficou aberto

- **O P9**, a pedido de Anderson: os C1–C4, a sonda do X7 e a prova do `CODEX_MODEL`.
- **O P10**, o fechamento e a medida pelo `--by-task`.
- **O X10**, proposta sobre `last_send["origem"]` e `answered.data`, sem decisão.
- **A linha `cobre:` vazia** (a chave existe e não traz número) continua aplicando e não marca subpasso. Não entrou nos oito.
- **O marcador `parado` junto de uma evidência sem `cobre:`** continua nas duas frases. Ficou de fora: a confiança ficou perto de 65.

## Custo da tarefa

Não medida — sessão sem turno medido · até 00:04 de 2026-11-12, pelo `brza note commit` · sem o turno do commit
