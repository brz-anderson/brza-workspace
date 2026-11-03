---
scope:
  - workspace
---

# O Terreno do PLN-008 para o Desenho

Anderson pediu retomar o
[PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md).
A leitura das branches locais não encontrou bloqueios ativos, e o checador passou sem erros nem avisos.

Um collector levantou os contratos atuais do CLI, do índice, do checador e da medição no `brza-workflow`.
O [PLN-008 — Desenho](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-design.md) registra o Terreno:
faltam suporte a listas e campos de ordenação no índice, identidades REV/MIG e extração de referências.
O rebuild usa a sessão de quem reconstrói, sem recuperar a autoria antiga.

A medição instalada já resolve `workspace` e `.claude` nesta árvore. A suíte focal de medição passou com 36 testes,
e o collector verificou os 45 testes do índice. Isso não reescreve o diagnóstico histórico da R4.

Na R7, Anderson respondeu "7.1 só `migration-runner` / 7.2.1 / 7.3.1": escolheu `depends_on` opcional em planos,
issues e índice, e `issue:<slug>` no `refs:`. A contraproposta de uma única skill nova volta em R8.1 para confirmar
se ela reúne criação, revisão e execução. Nenhum passo de implementação foi iniciado; o próximo ponto está no
Retomar do plano.

Na R8.1, Anderson confirmou com "sim" a única `migration-runner` reunindo criação, revisão e execução, com revisor
independente. O D1 registra esse contrato; as regras de dependência são o próximo ponto do Desenho.
