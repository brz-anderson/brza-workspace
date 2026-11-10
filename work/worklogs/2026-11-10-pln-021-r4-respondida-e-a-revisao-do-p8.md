---
scope:
  - workspace
tags:
  - tooling
  - planning
refs:
  - PLN-021
  - REV-026
sessions:
  - a68db12c-b7b9-4389-ad70-7f3fd12f27e8
---

# O PLN-021: a R4 respondida, o P7 reaberto e a revisão do P8

Retomada do [PLN-021: O plano roda por uma sessão coordenadora, com scripts de apoio e artboards de tela](../../plans/PLN-021-o-plano-coordenado-e-os-artboards/PLN-021-plan.md)
pelo `plan-runner` v2. O `plan_state.py` abriu limpo, com a R4 sem resposta e o P8 como próximo.

## O que se fez

- **A R4 levada a Anderson** em três rodadas de pergunta com opções (pontos 1 a 4, 5 a 8, escolhas menores) e gravada como
  **Rodada 5** pelo `round_log.py`. O script só acrescenta rodada nova, então a R4 ficou com a linha "Sem resposta" e a R5
  diz que vale ela.
  - **Respostas literais:** "todos recomendado" (R4.1 a R4.4); "4.6.2 / restante recomendado" (R4.5 a R4.9).
  - **A divergência:** a R4.6.2 (o desktop do `brza-studio` com os tokens vivos do Orca) contrariava o que o P7 escreveu.
- **O P7 reaberto** ("reabrir o P7 e rodar o P8"): o `implementer` fez o desktop do `brza-studio` usar os tokens vivos
  (`.sa-art[data-live]`, `--scheme` vira erro ali, o `shot` injeta o fallback só no PNG), com 55 testes. A SKILL, as references e o
  D7 foram atualizados pela coordenação (X6).
- **O P8**, pelo `reviewer` (Opus): [REV-026](../reviews/REV-026-pln-021-p1-a-p7.md), com 12 achados importantes, 6 sugestões e
  5 falsos. A coordenação refez A1, A2, A3 e A10 antes de levá-los.
- **A Rodada 6**, todos na primeira opção: o código vai ao **P11** (os defeitos do REV e o código em inglês); o plano e as
  skills foram corrigidos na coordenação (A6, A7 como X7, A8, A9, A16 a A18); o A12 foi descartado; o ajuste do P7 entrou no
  X1/X6, o navegador segue o pacote e o `Executado` se mede pelo `--by-task` no P10.
- **O plano:** P8 `[x]`, o P11 novo (6 h), os desvios X6 a X8 e a seção `## Revisões`; o `--fix` deu 47 h estimadas e 8 h restantes.

## O que se decidiu

- **R6.5, de Anderson:** "todos na primeira opção + um ajuste: todo o código deve ser em inglês, incluindo nomes de arquivos,
  métodos, classes e variáveis, em pt-BR somente docstrings e conteúdo que retorne ao usuário, como um retorno de texto".
- **O escopo:** "a norma de nomenclatura em inglês engloba todo o ecossistema `BrzA`". A regra subiu à norma comum e a
  memória do workstream saiu. Confirmado por Anderson: "confirmado, os 3".

## Fora do workspace

- `~/Projects/brza-workflow/core/AGENTS.md`: o parágrafo "Todo código do ecossistema BrzA é em inglês" (`45e6013`, push em `master`).
- `~/Projects/brza-studio/AGENTS.md`: a linha em Repo Rules (`049a890a837`, push em `master`).
- O `brza sync` neste workspace trouxe a norma (`a176ecd`, push) e levou o merge aos workstreams.

## O que ficou aberto

- **O P11** espera o pedido de Anderson; o P9 depende dele.
- **A18** (a R5 com "(seleção múltipla)" duplicado e a sessão como UUID solto) não foi corrigido.
- **O código do P7 reaberto** (`.claude/skills/screen-artboards/`) e as skills ajustadas estão no disco, sem commit: não são
  nota e não vão pelo `brza note commit`.

## Custo da tarefa

Corrido 12 h 39 min — agente 9 min, quem pediu 53 min, pausa 11 h 38 min · US$ 7,83 (turnos 2,68, subagentes 5,15) · CPU 3 min do `claude` e 4 min dos comandos, RSS até 510 MB · 9 turnos, 1 sessão · até 13:04 de 2026-11-10, pelo `brza note commit`
