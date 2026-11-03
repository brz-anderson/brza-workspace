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

O Desenho segue aberto para as rodadas sobre skills, dependências e identidade das referências; nenhum passo de
implementação foi iniciado. O próximo ponto está no Retomar do plano.
