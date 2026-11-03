---
scope:
  - workspace
refs:
  - PLN-004
---

# O PLN-004: a R12.2 fecha e o plano se divide

Anderson respondeu "recomendado" à R12.2 revista, em 2026-11-03, na sessão `workspace`. O plano é o
[PLN-004: O Codex e o `agy` trabalham no fluxo do workspace como o Claude](../../plans/PLN-004-o-codex-e-o-agy-no-fluxo/PLN-004-plan.md);
o dia anterior está em
[O PLN-004: a revisão do plano contra a migração ao brza-workflow](2026-11-02-pln-004-a-revisao-contra-o-pln-006.md).

## O que se fez

- **A R12.2 decidida:** o Claude é o runtime padrão de revisão nos três focos; o `agy` e o Codex entram como segundo
  passe, pedido por quem pede, com `--runtime` além do `--focus`; não há mapa foco → runtime. A medição que a sustenta
  está no worklog de ontem: o recall do `agy` no defeito foi de 0,40 a 0,20 entre as duas execuções, e o do Claude de
  0,20 a 0,30, então a vantagem que justificaria dobrar o defeito não se repetiu; a convenção do Claude ficou em 1,00
  nas duas.
- **O plano se dividiu**, como manda o `plans/README.md` (passava de 400 linhas, e tinha 670): a Entrevista, R1 a R12,
  foi para [PLN-004 — Entrevista](../../plans/PLN-004-o-codex-e-o-agy-no-fluxo/PLN-004-interview.md), e o `-plan` ficou
  com 92 linhas. O `Retomar` foi reescrito, e o checador das notas passa sem erro nem aviso.

- **O `designer` reescreveu o Desenho** (`pln-004-design-v2.md`, no scratch) e devolveu 11 pontos sem lastro, em 4
  rodadas. A **R13** e a **R14** foram respondidas e gravadas na Entrevista: a norma do pacote fica no pacote, o sync
  renderiza o `.toml`, o `codex-brza` usa o `tomllib`, o mapa do `agy` vai por `pro`/`flash` no papel e
  `gemini-4-argon-high` na revisão, e o Codex revisa em `gpt-6-astra` com `high` (variante de Anderson, sem o `high`
  medido).

## O que ficou

- **A R15 e a R16**, paradas por pedido de Anderson ("sem mais rodadas, por ora"): a delegação (P5 a P7) e a medição
  e a máquina (P8 a P11), no fim do `pln-004-design-v2.md`. Depois, o Desenho vai à aprovação na mensagem, em 3 partes,
  antes de virar `PLN-004-design.md`; na gravação, corrigir no `-plan` o "Fora de escopo" (ainda manda o código ao
  `tools-kit`) e a Cobertura (ainda diz "um foco por runtime").
- **O turno do `agy` com `model: pro`**, que lê o `modelName` do `Stop`, fica para o D7 (R14.1).
- **O `high` do Codex não foi medido:** a R12.2 mediu só `xhigh`.
