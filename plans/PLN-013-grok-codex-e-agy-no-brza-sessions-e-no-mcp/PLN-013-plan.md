---
status: open
phase: interview
origin: request
description: O brza sessions abre o Grok com nome e espera, e o MCP despacha ao Grok, ao Codex e ao Antigravity com conta e cota por runtime
ready: "não — falta a R2 (conta e cota por runtime, o --rename e o --wait fora do Grok, a ordem das entregas); isso trava o Desenho"
scope:
  - brza-workflow
opened: 2026-11-03
owner: Anderson
priority: high
tags:
  - tooling
---

# PLN-013: O Grok, o Codex e o Antigravity abrem pelo `brza sessions` e recebem tarefas do MCP

- **Retomar:** a R1 foi respondida em 2026-11-03, e o plano abriu. Próximo: a R2, que trava o Desenho; depois, o Terreno
  por subagente, a começar por "o `worker-start` aceita `--agent grok`?".

## Pedido

- **Origem:** pedido livre de Anderson em 2026-11-03, na sessão `tools-kit-produtividade`, e conduzido numa sessão
  própria do `tools-kit`. Antes, na mesma sessão, ele pediu "homebrew install grok" e confirmou "Grok CLI da xAI — esse"
  ([Instalação do Grok Build, o agente de terminal da xAI](../../work/worklogs/2026-11-03-instalacao-do-grok-build.md)).
  O plano absorve o roteador multiruntime do
  [PLN-003/P12](../PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md) e os outros runtimes que o
  [PLN-009](../PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md) deixou fora de escopo (o M4), pela R1.1.

"precisamos urgentemente adicionar o `grok` no fluxo do `brza sessions` e do `MCP`" — Anderson, em 2026-11-03.

Os itens do pedido, numerados para a Cobertura, com o corte da R1.2 e da R1.3:

1. o `brza sessions` abre de verdade o Grok, com título, prompt, mapa e `send`;
2. o `--rename` e o `--wait` passam a valer no Grok;
3. o MCP despacha ao Grok, ao Codex e ao Antigravity;
4. o MCP escolhe a conta e respeita a cota do Grok;
5. a lacuna de medição do Grok fica numa issue irmã da do Codex e do Antigravity.

### Cobertura

Rascunho da abertura: o critério de cada linha é proposta até a rodada que o confirma.

| Origem     | Critério de aceite | Passo | Teste (nível) |
| :--------- | :----------------- | :---- | :------------ |
| `Pedido 1` | `brza sessions <nome> --agent grok --title … --prompt …` abre o chat do Grok no app, grava o `open` no mapa, e `send <nome>` chega a ele | — | `test_brza_sessions` (unidade); abertura no app (manual) |
| `Pedido 2` | com `--agent grok`, o `--rename` dá o nome à sessão do Grok, e o `--wait` só anuncia com ela no ar; os outros agentes seguem recusados | — | `test_brza_sessions` (unidade); abertura no app (manual) |
| `Pedido 3` | o `dispatch` aceita `runtime` `grok`, `codex` e `antigravity`, e o worker abre pelo `worker-start --agent` do runtime | — | `tests/mcp/test_mcp_dispatch.py`, `test_mcp_cycle.py` (unidade); um worker de cada (manual) |
| `Pedido 4` | o worker Grok espera quando a janela do `rateLimits.grok` do app passa do teto, e o `status` diz qual | — | `tests/mcp/test_mcp_limits.py`, `test_mcp_accounts.py` (unidade) |
| `Pedido 5` | a issue irmã existe, no formato da do Codex e do Antigravity | — | o checador de notas |

### Fora de escopo

- **A medição por tarefa do Grok.** Vai à issue irmã
  [O Grok fica sem medida por tarefa](../../work/issues/o-grok-fica-sem-medida-por-tarefa.md), pela R1.4; a do Codex
  e do Antigravity segue em [Codex e Antigravity ficam sem medida por tarefa](../../work/issues/codex-e-antigravity-sem-medida-por-tarefa.md).
- **O transporte do `brza sessions` pelo `brza chat` do Studio.** É do
  [PLN-010](../PLN-010-brza-sessions-sobre-o-brza-chat/PLN-010-plan.md); este plano usa o transporte que estiver em
  vigor.

## Restrições

- **O PLN-009 fecha sem reabrir.** Este plano não muda a Cobertura dele: o que mexer no MCP entra aqui, com teste
  próprio.
- **O PLN-012 não se toca.** Segue na sessão `tools-kit-produtividade`.

## Pré-requisitos

- **O login do Grok.** `orca account list --json` → `rateLimits.grokAuthConfigured: false`, com o erro "Not signed in to
  Grok — run grok login". Sem ele, nenhuma abertura real nem cota do Grok. Quem faz é Anderson, com `grok login`.
- **O MCP do PLN-009 na `master` do `brza-workflow`**, mesclado em `23d812d`.

## Entrevista

### Rodada 1 — o destino, o corte, os outros runtimes e a medição (enviada 2026-11-03)

> **Apresentado antes:** o PLN-003/P12 é o roteador multiruntime do `brza sessions` (`--agent claude|codex|agy`) e não
> começou (`PLN-003-plan.md:217-228`); o PLN-009, em `review` e já mesclado, deixou "Outros runtimes (Codex, `agy`), o
> M4" fora de escopo, apontando para o P12. O `brza sessions` passa o `--agent` ao app sem lista e recusa o `--rename` e o
> `--wait` fora do Claude (`brza-workflow/packages/client/bin/brza-sessions:363-367`). O MCP fixa o Claude em
> `tools.py:25`, `accounts.py:24`, `cycle.py:22` e `limits.py:225`. O app conhece o Grok: o `worker-start` aceita o
> `--model` dele (`orca orchestration worker-start --help`), e ele tem contas (`GrokAccountsSection.tsx`) e cota
> (`src/main/rate-limits/grok-fetcher.ts`). A CLI do Grok tem `-p`, `--output-format`, `-s` e `-r` (`grok help`). O
> `grok login` não foi feito.

Respondida em 2026-11-03, nesta sessão.

1. **Onde mora o trabalho.** Opções:
   - um PLN novo, `high`, que absorve o PLN-003/P12 e o M4 do PLN-009, com o P12 virando `[-]` (recomendada) — custo:
     ~15 min; se paga: agora, porque o urgente não espera o P4 do PLN-003, e o PLN-009 fecha sem reabrir;
   - um passo no PLN-003/P12 — custo: ~5 min, com o urgente furando a ordem de um plano de 24 h restantes; se paga: só
     se o Grok for pequeno;
   - reabrir o PLN-009 — custo: adia o fechamento dele; se paga: nunca, além do que o PLN novo dá;
   - uma issue — custo: ~10 min, sem rodada para as lacunas; se paga: agora, se o corte for só o `brza sessions`.

   **Decidido — "PLN novo (Recomendado)".** O pedido de marcar o P12 vai ao `Retomar` do PLN-003.

2. **O que entra no corte urgente**, com seleção múltipla. Opções:
   - o `brza sessions` abre o Grok (recomendada) — custo: ~0,5 h, depois do `grok login`; se paga: na primeira sessão
     Grok aberta pelo `brza sessions`;
   - o MCP despacha ao Grok, na conta padrão e sem cota, como a PLN-009/R2.5 (recomendada) — custo: ~2,5 h; se paga: na
     primeira tarefa que a fila manda ao Grok;
   - a conta e a cota do Grok no MCP, pelo `GROK_HOME` e pela cota do app — custo: ~4 h; se paga: quando houver mais de
     uma conta Grok ou ele bater limite;
   - o `--rename` e o `--wait` no Grok — custo: ~2 a 3 h, com levantamento antes; se paga: quando a sessão Grok precisar
     ser achada pelo nome fora do mapa.

   **Decidido — as quatro:** "Sessions abre o grok (Recomendado), MCP despacha ao grok (Recomendado), Conta e cota do
   grok no MCP, --rename e --wait no grok". Somadas, ~9,5 h.

3. **O Codex e o Antigravity no MCP.** Opções:
   - uma tabela de runtimes com o Claude e o Grok, e os outros depois, com uma linha e um teste (recomendada) — custo:
     +~0,5 h; se paga: no segundo runtime além do Grok;
   - os três juntos, com teste e abertura real de cada um — custo: +~2 h; se paga: já, se houver despacho ao Codex ou ao
     `agy` pelo MCP nesta semana;
   - só o Grok, numa tupla fixa — custo: ~0 agora e uma refatoração no próximo runtime; se paga: nunca, se outro runtime
     vier.

   **Decidido — "Os três juntos".** Se isso vale também para a conta, a cota, o `--rename` e o `--wait`, vai à R2.

4. **A lacuna de medição do Grok.** Opções:
   - uma issue irmã, no formato da do Codex e do Antigravity (recomendada) — custo: ~10 min; se paga: agora, porque a
     issue antiga não muda de nome e o `move_note` não reescreve link no PLN-012;
   - na issue existente, renomeada pelo `move_note` — custo: ~10 min, com o link reescrito dentro do PLN-012, que outra
     sessão edita; se paga: quando as três lacunas forem resolvidas juntas.

   **Decidido — "Issue irmã (Recomendado)".**

## Worklogs

- 2026-11-03 — Passos 0 a 2 e a R1; o plano abriu e a issue irmã nasceu. Parou na R2.
  [Abertura e entrevista do PLN-013, o Grok no `brza sessions` e no MCP](../../work/worklogs/2026-11-03-pln-013-abertura-e-entrevista.md)
