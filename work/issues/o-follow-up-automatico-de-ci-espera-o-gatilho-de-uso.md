---
status: open
description: O desenho do follow-up automático em falha de CI (a ideia do #38950) no brza-workflow fica guardado, com a contenção já escolhida, até haver 5 PRs com check falhando numa semana, contados por dono em todas as contas do gh.
scope:
  - brza-workflow
opened: 2026-11-09
priority: low
tags:
  - tooling
---

# O follow-up automático de CI espera o gatilho de uso, com a contenção já desenhada

Saiu da reunião de verificação do [PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md) (P7), sobre [Resultados de CI no chat e disparo automático de agentes em falhas de PR](resultados-de-ci-no-chat-e-disparo-automatico-de-agentes-em-falhas-de-pr.md). É o destino do item 2 daquela issue, para o workstream `tools-kit`. **Não é pedido de execução** até o gatilho abrir.

## A decisão

Anderson, em 2026-11-09, na sessão de coordenação da reunião: "1A decidido". É a alternativa A da proposta v2: o automático
não se constrói agora, nem em modo sombra. Fica este desenho, com um gatilho medido que o reabre. Votaram A as três
personas: Prumo na R2, Trava e Relance na R3, depois de lerem a taxa de base. O revisor independente deu 78 ao plano.

## Por que esperar

- **0 PRs** em `brz-anderson/brza-studio`, `brza-workflow` e `brza-workspace` (`gh pr list --state all`, 2026-11-09). O
  push vai direto na `master`, sem PR (`AGENTS.md`), e os workflows de `push` do fork filtram `main`. O disparo do
  `#38950` ("PR's checks fail") não teria nenhum evento.
- **A exceção:** 8 PRs no `anderson-fixfy/orca-fixfy` de 24/10 a 27/10, **7 do `fixfy-claude`** (a conta de agente)
  (`gh search prs --owner=anderson-fixfy --created='>=2026-09-01'`). O evento aparece quando um agente abre PRs. Contar
  por `--author=@me` não enxerga esses PRs.
- O `#38950` foi fechado sem merge no upstream. A head real (`ed402736`) tem 163 arquivos e +12.696, e só se lê como
  especificação das regras, não como código a portar.

## O gatilho

**Reabre** quando houver **≥ 5 PRs com check falhando numa mesma semana**, contados por dono (`--owner`) em todas as contas do
`gh auth status`. Quem faz o merge de tag do upstream no `brza-studio` roda um comando só, no checklist do sync, e anota o
número. Abaixo de 5, nada muda.

## A contenção, já escolhida pela sala

| Peça | O quê | Quem trouxe |
| :--- | :---- | :---------- |
| Onde mora | No `brza-workflow`, por `brza orchestration worker-start`; nada de código de disparo no Studio | 3/3 (R1) |
| Sem `git push` | O worker deixa o patch no workspace corrente e para; quem empurra é o humano ou o "Fix with AI" | Trava (R1); 3/3 na R2 |
| A chave de dedupe | `(repo, número do PR, sha, conjunto de checks falhos)`: um disparo por chave | Prumo e Trava (R1) |
| Os tetos por PR | 3 seguidos por PR (push de agente não zera; push humano zera), 6 em 24 h por PR | upstream `#38950`, lido |
| O teto da máquina | Os `CEILINGS` do `packages/mcp/brza_mcp/limits.py:22` (`machine`, `account_sessions`, `account_quota`), mais um contador de arranques em 24 h (*suposto*: 20) | Trava (R1/R2), Prumo (R2) |
| O freio | `worker-stop --dispatch` fecha o terminal; o `--timeout-ms` do `worker-start` é só o prazo de prontidão e não limita o agente | Trava (R1/R2), revisor |
| A entrada do log | O prompt do "Fix with AI" do Studio põe até 150 linhas do log no prompt: o log de CI é entrada não confiável | Trava (R1) |
| Padrão | Desligado por chave de configuração; sem `--keep-open` | Prumo (R1) |

## O que fica em aberto para quando reabrir

- O número do teto da máquina em 24 h (20 é suposição da Trava).
- Se o "sem `git push`" é garantido por permissão do token ou só por texto no spec. A Trava deu 74 à parte do plano em
  que isso é só texto.
- A falha não determinística (flake): se o mesmo check falha e passa no mesmo sha, não é falha.
