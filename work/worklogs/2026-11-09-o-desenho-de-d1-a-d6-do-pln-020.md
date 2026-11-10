---
scope:
  - workspace
  - brza-workflow
tags:
  - tooling
  - planning
refs:
  - PLN-018
  - PLN-020
sessions:
  - 2477d2a4-7778-41c8-9b3b-fb839339bf9a
---

# O desenho de D1 a D6 do PLN-020: dois consultores, e as rodadas 5 a 8 prontas para enviar

O pedido de Anderson, em 2026-11-09, no workstream `playground`:
- "comece", depois da R4 do [PLN-020: Os fluxos do workspace rodam em qualquer client, pelas skills distribuídas e por verbos do brza-orchestrator](../../plans/PLN-020-os-fluxos-em-qualquer-client-pelo-brza-orchestrator/PLN-020-plan.md);
- depois, "grave as opções no Desenho e as rodadas em Entrevista, retomaremos o plano outro dia".

## O que se fez

### Os dois consultores

Dois `designer` em paralelo, só leitura, contra `brza-workflow@8eb989a`, com as devoluções no scratch:

| Consultor | Itens | O que mudou o desenho |
| :-- | :-- | :-- |
| D1 e D2 | o symlink `.agents/skills` no `core/`, a identidade no `.git/config` | o `brza sync` não leva symlink: grava arquivo com o texto do alvo e quebra no sync seguinte (sonda num `brza-workflow` de teste). O `brza doctor` só confere: quem grava é o `brza install`. O `AGENTS.md` e o `CLAUDE.md` moram no `core/`. As duas estimativas passam de ~1 h para 2 h. |
| D3 a D6 | `close_task`, `start_task`, `index_query`, `decision_record` | 7 tarefas do Codex de hoje, no log real, saíram com `session_id` null. O PLN-018 fechou, mas a linha `turn` do Codex não se grava, porque o hook não está instalado. O daemon está de novo carregado sem processo, e nenhum client tem o servidor configurado. O padrão: o verbo chama `brza note … --json`, a sessão vem em argumento, e nenhum verbo usa o gate do `dispatch`. |

Os consultores gravaram três memórias de papel em `.claude/agent-memory/designer/`:
- uma sobre o verbo como adaptador sobre o CLI;
- uma sobre conferir o comando antes de estimar uma opção de norma;
- e o índice do `MEMORY.md`, que só listava um dos arquivos.

### O que foi ao plano

- **O Desenho foi para `PLN-020-design.md`**, porque o plano passaria das ~400 linhas. Ele leva:
  - o Terreno, com M1–M11 da sonda e T1–T25 dos consultores;
  - o padrão comum dos verbos;
  - D1 a D6, com as alternativas, o custo, quando se paga e o contrato escrito;
  - a estimativa pelas recomendadas, ~25,5 h.
- **As rodadas R5 a R8 foram para a Entrevista, preparadas e não enviadas:** 15 perguntas, das 14 do rascunho dos
  consultores (o ponto 6 do D6 virou duas). Todas as opções têm custo e quando se paga, e a recomendada vem primeiro.
- **O plano** passou a `phase: design`, com o `ready` à espera das rodadas.

Nenhuma rodada foi respondida, e nenhuma decisão foi tomada.

## Retomar

O próximo passo está no `Retomar` do PLN-020: enviar a R5, depois a R6, a R7 e a R8; então gravar o vigente no Desenho
e planejar os passos.

## Custo da tarefa

Corrido 47 min — agente 32 min, quem pediu 15 min, pausa 0 s · US$ 9,26 (turnos 2,99, subagentes 6,27) · CPU 41 s do `claude` e 1 min dos comandos, RSS até 576 MB · 5 turnos, 1 sessão · até 00:00 de 2026-11-10, pelo `brza note commit`
