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

- **A R15 e a R16** foram respondidas e gravadas. R15: o `brza delegate` usa o papel e o `--runtime` é obrigatório. A
  15.3 virou a contraproposta de Anderson, o `.brzAgents`, e um `collector` mediu o custo (36 arquivos e 104 linhas no
  `brza-workflow`, nenhum no `brza-studio`; o Claude, o Codex e o `agy` leem `agents` e `skills` por link; o D15 falha
  na transição de diretório para link; a gravação da memória do subagente pelo link foi negada em 3 de 3 `claude -p`).
  R16: `agents`, `skills` e `memory` em `.brzAgents/`, a memória literal (16.1.3, não a recomendada), o link de
  diretório para as skills e o D15 emendado.

## O que ficou

- **A sonda de saída da memória** (regra de permissão com caminho absoluto, `--add-dir`, link só no nível do papel,
  hook): com o `collector`, em `/private/tmp/pln004/brz-agents/levantamento-memoria.md`. Sem saída, a 16.1 volta a
  Anderson antes do Desenho.
- **A R17**, a medição e a máquina (P8 a P11), e o **Desenho reescrito com o `.brzAgents`**, que vai à aprovação na
  mensagem, em 3 partes, antes de virar `PLN-004-design.md`; na gravação, corrigir no `-plan` o "Fora de escopo" (ainda
  manda o código ao `tools-kit`) e a Cobertura (ainda diz "um foco por runtime"), e a revisão do Codex no D11 para `high`.
- **O turno do `agy` com `model: pro`**, que lê o `modelName` do `Stop`, fica para o D7 (R14.1).
- **O `high` do Codex não foi medido:** a R12.2 mediu só `xhigh`.
- **A migração para o `.brzAgents`** muda o `core/` do `brza-workflow` (16 `git mv`, 14 fixtures do ouro, o sync) e,
  com a memória literal, `git mv` de 55 arquivos de memória em 4 branches; tudo a executar só a pedido de Anderson.
