---
scope:
  - workspace
  - tools-kit
---

# O PLN-003: o desempatador do M11

Pedido da sessão `bb0fd632` do workstream `workspace`, em 2026-11-03: atualizar o M11 do Desenho do
[PLN-003](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md) ("Agente interno que desempata") e o
`Retomar` com a medição e a rodada de lá. A medição está no worklog
[O desempatador local do M11: o `tev1:4b` no lugar do Haiku](2026-11-03-o-desempatador-local-do-m11.md), do
`workspace` (commit `b67fcea`).

## O que se fez

- **[`PLN-003-design.md`](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-design.md), linha do M11:** a
  feature passa a dizer a cota na tabela, o `tev1:4b` no texto e o Haiku abaixo do limiar; a coluna "Alt" ganhou "só o
  Haiku" e a Jev; o "Porquê" ganhou a latência e o custo do `tev1`.
- **A seção nova "O desempatador do M11 (rodada de 2026-11-03)"**, depois da matriz do orquestrador: a tabela da
  medição, a rodada com a resposta literal e os pontos — a cota como regra da tabela, o `tev1:4b` pelo `/v1/systemone`,
  o Haiku abaixo do limiar, a calibração na fase 2b, a licença antes do pacote público (B4) e a Jev como backend de
  nuvem opcional.
- **O `Retomar` do PLN-003** ganhou o item do desempatador, e a seção Worklogs, este worklog.

## A decisão de Anderson

Rodada respondida em 2026-11-03, na sessão `bb0fd632` do `workspace`, com a resposta literal **"tev1 + Haiku
(Recomendado)"**. A opção dizia: "Registrar no M11: a cota fica na tabela; o tev1 desempata o texto e manda ao Haiku
quando a confiança ficar abaixo do limiar; a Jev fica como opção de nuvem para o pacote público." Detalha a R5.1 e
fica no Desenho; não é item `D`.

## O que não foi feito

As 3–4 h do M11 não foram refeitas com o `tev1`, o que ficou escrito no Desenho. Nada rodou nesta sessão: a medição é
toda da sessão do `workspace`.

## Retomar

O plano segue na fase de desenho, com o spike do C5 primeiro, como já dizia o `Retomar` do PLN-003.
