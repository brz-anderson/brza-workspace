---
name: base-de-estimativa-brza-sessions
description: Base para estimar horas de mudança no brza sessions e de passo de skill, e o cuidado para rodar os testes dele dentro de uma sessão do workspace
metadata:
  type: reference
---

**Base de horas.** No PLN-013 (`tools-kit`), os passos do `brza sessions` saíram entre 50% e 100% do estimado:

| Passo | Estimado | Executado |
| :---- | -------: | --------: |
| P3, abrir o Grok | 0,5 h | 0,5 h |
| P9, o `--wait` | 1,5 h | 0,75 h |
| P10, o `--rename` | 2 h | 1 h |
| Revisão e merge | ~1 h | ~1 h |

As linhas `Estimado`/`Executado` estão em `workstream/tools-kit:plans/PLN-013-…/PLN-013-plan.md`. Use essa faixa como
teto e piso ao estimar verbo novo no `brza-sessions`. Ao estimar tarefa daqui, confira se apareceu medição mais
recente.

**Testes.** Os de `~/Projects/brza-workflow/tests/cli/test_brza_sessions.py` falham em 4 casos de checkout relativo
quando a sessão tem a `BRZA_WORKSPACE`. Rode com `env -u BRZA_WORKSPACE` para ver a linha de base verde. Em 2026-11-08,
passaram 47.

A estimativa do D2 do CLI de 2026-11-08 foi 11,5 h; registre aqui o executado quando o `tools-kit` fechar, para
calibrar. Ver [[criterio-cliente-com-shell]].

**Passos de skill saem mais baratos ainda.** No PLN-017 (playground), a skill `meeting-runner` (P1) teve 10,5 h
estimadas e ~4 h executadas, e o painel (P2) 6,5 h e ~2 h, ambos sem medição; o P5 (`brza shot`), 1 h e 0,174 h pela
janela da sessão executora. Na proposta de Passos do PLN-021 (2026-11-09) usei as faixas que as rodadas já tinham
apresentado (41 h no total) e levei a calibração (~35%) como pergunta, sem trocar o número sozinho. Registre aqui o que
Anderson escolheu e o executado do PLN-021 quando fechar.
