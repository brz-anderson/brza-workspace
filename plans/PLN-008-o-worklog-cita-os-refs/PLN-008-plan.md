---
status: open
phase: design
origin: request
description: O brza note commit preenche o refs do worklog com os IDs que ele cita, e revisão e migração ganham REV-NNN e MIG-NNN
ready: não — R12 fechou a listagem; falta consolidar os demais contratos e aceitar o corte em Passos
scope:
  - workspace
opened: 2026-11-03
owner: Anderson
tags:
  - tooling
---

# PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca

- **Retomar:** R12 fechou o `brza note ls`: abertos e `opened` recente primeiro, índice local por padrão;
  `--refresh` atualiza antes de listar, com falha explícita. D1 a D6 registram os contratos fechados. Próximo:
  consolidar numeração, preenchimento do acervo e índice; levar o corte em Passos ao aceite.
- **Dividido:** [PLN-008 — Entrevista](PLN-008-interview.md) · [PLN-008 — Desenho](PLN-008-design.md)

## Pedido

- **Origem:** pedido livre, na sessão `workspace` de 2026-11-03 (bb0fd632).

"Proposta: colocar o campo tags no frontmatter do worklogs/ com tags por plano, revisão, migração e etc, afim de
facilitar a busca por conteúdo relacionado. Ex: o worklog de agora, do plano 003, tags: - pln-003 - mig-001" —
Anderson, em 2026-11-03.

Os itens, numerados para a Cobertura:

1. o worklog diz, no frontmatter, a que plano, issue, revisão e migração se refere, para achar o conteúdo relacionado;
2. a revisão tem ID próprio, `REV-NNN`, e as 4 que existem são renumeradas (R2.2);
3. a migração tem ID próprio, `MIG-NNN`, na forma da R3;
4. as skills criam, revisam e executam essas notas.

"Temos também que criar/adaptar skills para a criação, revisão e execução dessas novas notas" — Anderson, em
2026-11-03, na mesma sessão, depois da R3.

5. o frontmatter das notas e o índice servem ao coordenador do PLN-003 (R4, R5).

"E o sessionId, runtime e infos assim no frontmatter do worklogs/ ou outras notas, faça um levantamento geral de como o
frontmatter das notas pode melhorar visando um nelhor desempenhi no fluxo do coordenador" — Anderson, em 2026-11-03, na
mesma sessão.

### Cobertura

> Rascunho: o passo e o teste saem do Desenho.

| Origem     | Critério de aceite                                                                                                   | Passo | Teste (nível) |
| :--------- | :------------------------------------------------------------------------------------------------------------------- | :---- | :------------ |
| `Pedido 1` | o `brza note commit` grava no `refs:` de cada worklog os IDs que o corpo linka ou cita, sem ninguém escrever à mão     | —     | —             |
| `Pedido 1` | o checador barra o `refs:` com ID que não existe em nenhum workstream                                                  | —     | —             |
| `Pedido 1` | os worklogs que existem ganham o `refs:` por um preenchimento automático                                               | —     | —             |
| `Pedido 2` | toda revisão de `work/reviews/` tem `REV-NNN`, numerado em sequência pelo índice, e as 4 de hoje são REV-001 a REV-004 | —     | —             |
| `Pedido 3` | a migração é issue `type: migration`, `work/issues/MIG-NNN-<assunto>.md`, com o molde da R3.3, e a MIG-001 é a renumeração das revisões | — | — |
| `Pedido 4` | a única `migration-runner` cria, revisa e executa a MIG até o critério de conclusão, com revisor independente (R8.1) | — | — |
| `Pedido 4` | a revisão nasce com o `REV-NNN` pela skill que a escreve, a `plan-runner` em `references/conduct.md` | — | — |
| `R4.1` | toda linha do `measurements.jsonl` dentro de um worktree tem `workstream`, a conta não sai `home`, e o `session` do índice resolve sempre que a sessão tem nome | — | — |
| `R4.2` | o `brza note commit` avisa, sem barrar, a issue ou o plano aberto sem `priority` | — | — |
| `R4.3` | a linha do índice grava `priority`, `blocks`, `deadline`, `owner`, e no plano `estimate_h` e `remaining_h`; o `index --rebuild` refaz as antigas | — | — |
| `R5.2` | a issue aceita `estimate_h` opcional, e o índice a grava | — | — |
| `R5.3` | os worklogs perdem o `date`, mantêm o `tags`, e o checador avisa o `date` | — | — |
| `R6.1` | o `brza note ls` lista issues e decisões de todos os workstreams, pelo índice, ordenadas por `opened`, `priority` ou `deadline` | — | — |
| `R7.2` | planos e issues aceitam `depends_on` opcional, também gravado no índice | — | — |
| `R9.1` | só `done` satisfaz uma dependência; `dropped` exige revisão explícita da relação | — | — |
| `R9.2` | o checador barra dependência com alvo inexistente, autorreferência ou ciclo, inclusive entre workstreams | — | — |
| `R10` | refs é extraído fora de cercas, preserva crases inline, links e citações históricas; menção textual desconhecida avisa sem entrar no campo | — | — |
| `R12` | ls mostra abertos por padrão, ordena por opened recente primeiro e usa índice local; --refresh atualiza com falha explícita | — | — |

### Fora de escopo

- **Os IDs em `tags`, como na proposta.** Ficou o campo `refs:` (R1.1); o `tags` segue só para assunto, no vocabulário
  fechado do checador.
- **Uma pasta `work/migrations/` e o MIG como plano.** Perderam na R3.2.
- **`session_id`, runtime, conta e modelo no frontmatter.** Ficam na medição e no `brza sessions` (R4.1).

## Entrevista

[PLN-008 — Entrevista](PLN-008-interview.md)

## Worklogs

- 2026-11-03 — aberto; R1 a R6 fecharam a Entrevista; parou antes do Terreno.
  [A abertura do PLN-008: o refs nos worklogs, o REV e o MIG](../../work/worklogs/2026-11-03-pln-008-a-abertura-do-refs-do-rev-e-do-mig.md)
- 2026-11-03 — retomada; Terreno conferido; R7 a R12 respondidas; D1 a D6 registram os contratos fechados.
  [O Terreno do PLN-008 para o Desenho](../../work/worklogs/2026-11-03-pln-008-o-terreno-para-o-desenho.md)
