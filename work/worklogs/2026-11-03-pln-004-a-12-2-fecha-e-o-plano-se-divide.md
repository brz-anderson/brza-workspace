---
scope:
  - workspace
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

## O que ficou

- **O Desenho**, a reescrever: o rascunho (`pln-004-design-rascunho.md`, 556 linhas, no scratch, D1 a D14) ainda conta
  com tudo no `brza-workspace`. Precisa do pacote `packages/runtimes` no `brza-workflow` (R10), do `brza sync`
  aprendendo o modo `120000` e dos papéis e links de skill gerados (R11), dos hooks nos dois runtimes (R11.3), do
  `shell/runtimes.zsh` e do `--focus` mais o `--runtime` no `brza delegate` (R12), do mapa de modelos do `agy` refeito
  (`gemini-4-argon-*`, `gemini-3.8-flash-*`, sem `pro` nem `flash`) e de 4 links de skill; o D13 deixou de existir.
  Depois, vai à aprovação na mensagem, em 3 partes, antes de virar `PLN-004-design.md`.
