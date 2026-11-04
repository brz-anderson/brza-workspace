---
scope:
  - workspace
  - brza-workflow
refs:
  - MIG-001
  - PLN-008
  - REV-006
---

# A revisão da entrega do PLN-008 no P7

Anderson pediu "siga" depois do P6, autorizando o P7 do
[PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md).

## A revisão

- O `reviewer`, como subagente isolado e sem as conclusões da sessão, conferiu o Pedido e a Cobertura contra o
  `brza-workflow@7a18392` e as cinco árvores. Relatório temporário em `/private/tmp/pln008-p7/revisao.md`.
- A revisão rodou `tests/cli` com 468 OK sem a `BRZA_WORKSPACE`; com ela, 20 testes falham pela recusa `foreign_cwd`, e
  esse achado é falso. Também rodou `tests/hooks` (288 OK), o notes-checker (26 casos), `scripts/brza/tests` (98 OK), o
  checador nas cinco árvores, sem erros, e os três blocos da MIG-001, com saída 0.
- A sessão refez a evidência de A1, A2, A3 e A6: `check_notes.py:350-368` sem REV e `decision:` em `dep_targets`,
  `core/work/README.md:226` com os dois, `a666e78:bin/brza-note:946-947` com `blocks` escalar, e as duas issues `open`.

## Os destinos, na Rodada 14

- **A1:** aviso no checador, num passo novo P8.
- **A2:** a norma volta ao D2.
- **A4:** o texto do link sai da extração. O D3 foi reaberto e reescrito.
- **A5 e A7:** viraram issues.
- **A6:** as duas issues resolvidas ficaram `done`.
- **A3 e A8:** descartados.

O D2, o D3 e o D7 ganharam a origem R14. O P8 entrou no plano com 2,5 h, e o `estimate_h` foi a 20,5. O número do
parecer saiu do `brza note review-open`: [REV-006: A entrega do PLN-008 contra o Pedido e a Cobertura](../reviews/REV-006-pln-008-p7-a-entrega.md).

## Ponto de parada

O P8 só começa a pedido de Anderson. Ele roda numa sessão de implementação no `brza-workflow` e depois nas sessões
donas de `brand`, `studio`, `playground` e `tools-kit`, para recomitar os 4 worklogs. O fechamento do P7 depende do P8.

## Fora do workspace

- **O quê e onde:** link `/private/tmp/pln008-p7` para o scratch do chat; sondas do revisor em
  `/private/tmp/pln008-p7-sonda/`. **Risco:** nenhum, são temporários. **Estado:** artefatos de conferência. **Como
  desfazer:** apagar os dois caminhos.
