---
status: done
scope:
  - workspace
opened: 2026-10-29
decided: 2026-10-29
decided_by: Anderson
tags:
  - tooling
---

# A sessão que conversa por correio abre com o `--rename`

**Quem abre sessão pelo `brza sessions` passa `--rename` quando ela vai mandar ou receber correio; a sessão que só
recebe a tarefa e devolve em arquivo abre sem ele, com o título da aba no `--title`.** O `/rename` dá à sessão do
Claude o nome que o correio usa; sem ele, ela entra no correio com um nome automático, como `brza-workspace-5b`, que
ninguém sabe antes de abrir.

Decidido por Anderson em 2026-10-29, na sessão `pln-002-sessions-rename`: "Sim, e a regra vai à memória e à ajuda
(Recomendado)" (PLN-002/R13.4), "A R13.4, o --rename para o correio", no Fechamento, e, sobre o texto, "2.1", à opção
"Decidido, pode gravar (Recomendado)", com o texto inteiro na mensagem. A primeira resposta sobre o texto, dada na caixa
de perguntas que o escondia, foi desfeita.

## Fundamento

- O pedido 8 do PLN-002 tirou o `/rename` do padrão do `brza sessions`, que passou a nomear só a aba.
- O correio endereça a sessão pelo nome dela (`CLAUDE.md`, a tabela do vocabulário).
- Medido no PLN-002/P9.1: a sessão aberta sem `/rename` apareceu no `ListAgents` como `brza-workspace-5b`, e a mensagem
  dela chegou com `from-name="brza-workspace-5b"`.

## Onde vale

- A ajuda do `scripts/brza/brza-sessions`, que traz a regra.
- A memória de abrir sessão pelo `brza sessions`, do Claude Code.
- Decidido em PLN-002/R13.4, no
  [PLN-002: Os passos manuais que se repetem entre sessões viram comandos `brza`](../../plans/PLN-002-os-comandos-brza/PLN-002-plan.md).
