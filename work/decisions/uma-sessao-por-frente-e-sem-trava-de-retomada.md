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

# Uma sessão por frente de trabalho, sem trava de retomada e com o cache de 1 h

**A sessão acompanha a frente de trabalho — o plano ou o assunto —, e não a tarefa; a trava de retomada sai, e o cache
da sessão principal fica em 1 h.** Sessão nova abre quando muda o plano ou o assunto, quando o contexto passa de ~200
mil tokens ou a pedido; dentro da frente, a compactação entra no lugar dela. O worklog continua fechando cada tarefa.

Decidido por Anderson em 2026-10-29, na sessão `brza-workspace-b7`: "Desligar (Recomendado)", "Sessão por frente
(Recomendado)", "Manter 1 h (Recomendado)" e, sobre o texto, "Decidido, pode aplicar (Recomendado)".

## Fundamento

O pedido: "precisamos reavaliar o cache e a trava das sessões, assim como o fluxo - cada tarefa, uma sessão -, está mais
atrapalhando que economizando tokens". A medição de 2026-10-27 23h55 a 2026-10-29 20h55, na sessão principal em Opus:

| Medida | Valor |
| :----- | :---- |
| Sessões | 33, com 130 turnos; 8 de um turno só |
| Gasto | US$ 89,79 |
| Primeiro turno das sessões | US$ 45,66, 51% do gasto; em média 73 mil tokens de cache escritos e US$ 1,38 por sessão |
| Trava | barrou 1 vez, US$ 1,40 estimados; só 2 pausas acima de 60 min, ambas com ~55 mil tokens |
| Cache de 1 h | US$ 11,22 a mais na escrita, US$ 19,39 de regravação evitada em 32 pausas de 5 a 60 min |

- **A regra "uma tarefa, uma sessão" custava mais do que poupava.** Cada sessão nova relia a norma, o plano e as notas,
  e retomar uma sessão de 175 mil tokens com o cache vencido custa o mesmo que abrir uma nova, que ainda não tem o
  contexto.
- **A trava quase não agia**, e cobrava o reenvio e a ordem de abrir sessão nova.
- **Recusadas:** a trava só avisando, sem barrar, porque o aviso chega depois que a regravação já foi paga; a trava com
  limiar de 250 mil e 2 h, porque a regravação acima disso não foi medida; a sessão nova opcional, sem critério; o cache
  de 5 min, que custaria uns US$ 8 a mais em dois dias.

## Onde mais está

- **A norma:** `AGENTS.md`, "Uma frente, uma sessão; uma tarefa, um worklog", e o `CLAUDE.md`, "O cache da sessão
  principal dura 1 h".
- **A configuração:** o hook `UserPromptSubmit` saiu do `.claude/settings.json`.
- **O `brza sessions send` sem a trava:** `88d8a3a`, pela sessão `pln-002-p7`.
- **O registro:** [A sessão por frente e a trava de retomada desligada](../worklogs/2026-10-29-a-sessao-por-frente-e-a-trava-desligada.md).
