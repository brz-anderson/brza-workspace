---
status: open
phase: interview
origin: request
description: O brza sessions abre o Grok com nome e espera, e o MCP despacha ao Grok, ao Codex e ao Antigravity com conta e cota por runtime
ready: "não — falta o Terreno e o Desenho; o primeiro ponto é se o worker-start aceita --agent grok"
scope:
  - brza-workflow
opened: 2026-11-03
owner: Anderson
priority: high
tags:
  - tooling
---

# PLN-013: O Grok, o Codex e o Antigravity abrem pelo `brza sessions` e recebem tarefas do MCP

- **Retomar:** a R1 e a R2 foram respondidas em 2026-11-03, e a entrevista fechou. Próximo: o Terreno, por subagente,
  com os quatro pontos de "Em aberto para o Desenho"; depois, os itens `D` das três entregas da R2.3.

## Pedido

- **Origem:** pedido livre de Anderson em 2026-11-03, na sessão `tools-kit-produtividade`, e conduzido numa sessão
  própria do `tools-kit`. Antes, na mesma sessão, ele pediu "homebrew install grok" e confirmou "Grok CLI da xAI — esse"
  ([Instalação do Grok Build, o agente de terminal da xAI](../../work/worklogs/2026-11-03-instalacao-do-grok-build.md)).
  O plano absorve o roteador multiruntime do
  [PLN-003/P12](../PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md) e os outros runtimes que o
  [PLN-009](../PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md) deixou fora de escopo (o M4), pela R1.1.

"precisamos urgentemente adicionar o `grok` no fluxo do `brza sessions` e do `MCP`" — Anderson, em 2026-11-03.

Os itens do pedido, numerados para a Cobertura, com o corte da R1.2, da R1.3 e da R2:

1. o `brza sessions` abre de verdade o Grok, com título, prompt, mapa e `send`;
2. o `--rename` e o `--wait` passam a valer no Grok, no Codex e no Antigravity (R2.2);
3. o MCP despacha ao Grok, ao Codex e ao Antigravity;
4. o MCP respeita a cota dos três runtimes e troca a conta onde o app lista contas, no Codex (R2.1);
5. a lacuna de medição do Grok fica numa issue irmã da do Codex e do Antigravity.

### Cobertura

Rascunho da abertura: o critério de cada linha é proposta até a rodada que o confirma.

| Origem     | Critério de aceite | Passo | Teste (nível) |
| :--------- | :----------------- | :---- | :------------ |
| `Pedido 1` | `brza sessions <nome> --agent grok --title … --prompt …` abre o chat do Grok no app, grava o `open` no mapa, e `send <nome>` chega a ele | — | `test_brza_sessions` (unidade); abertura no app (manual) |
| `Pedido 2` | com `--agent grok`, `codex` ou `agy`, o `--rename` dá o nome à sessão do runtime, e o `--wait` só anuncia com ela no ar; agente fora dos quatro segue recusado | — | `test_brza_sessions` (unidade); uma abertura de cada no app (manual) |
| `Pedido 3` | o `dispatch` aceita `runtime` `grok`, `codex` e `antigravity`, e o worker abre pelo `worker-start --agent` do runtime | — | `tests/mcp/test_mcp_dispatch.py`, `test_mcp_cycle.py` (unidade); um worker de cada (manual) |
| `Pedido 4` | o worker de cada runtime espera quando a janela do `rateLimits.<runtime>` do app passa do teto, e o `status` diz qual | — | `tests/mcp/test_mcp_limits.py`, `test_mcp_accounts.py` (unidade) |
| `R2.1`     | o worker Codex pode sair numa conta inativa (`inactiveCodexAccounts`) quando a ativa está no teto; o Grok e o Antigravity ficam na conta única | — | `tests/mcp/test_mcp_accounts.py` (unidade) |
| `R2.3`     | cada uma das três entregas sai num commit e serve sozinha: E1 abrir e despachar, E2 a cota e a conta, E3 o `--rename` e o `--wait` | — | o gate de cada entrega |
| `Pedido 5` | a issue irmã existe, no formato da do Codex e do Antigravity | — | o checador de notas |

### Fora de escopo

- **A medição por tarefa do Grok.** Vai à issue irmã
  [O Grok fica sem medida por tarefa](../../work/issues/o-grok-fica-sem-medida-por-tarefa.md), pela R1.4; a do Codex
  e do Antigravity segue em [Codex e Antigravity ficam sem medida por tarefa](../../work/issues/codex-e-antigravity-sem-medida-por-tarefa.md).
- **Várias contas Grok.** O app não lista contas Grok, e a R2.1 deixou o Grok e o Antigravity na conta única; volta
  quando houver uma segunda conta Grok.
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

### Rodada 2 — o alcance da conta, do `--rename` e a ordem das entregas (enviada 2026-11-03)

> **Apresentado antes:** a cota dos três runtimes já sai do app no formato das janelas do Claude — `orca account list
> --json` traz `rateLimits.grok`, `.codex` e `.antigravity`, com `session` e `weekly` (`usedPercent`, `windowMinutes`,
> `resetsAt`), e o Codex estava com a `session` em 97%. O app só lista contas do Claude e do Codex (chaves de topo
> `claude`, `codex`, `opencode`, `devin`; `inactiveCodexAccounts`); o Grok tem o `GROK_HOME` por conta no launch
> (`brza-studio/src/main/acp/acp-launch-specs.ts:163`), mas nenhuma lista. A "conta do Grok" da R1.2 é, hoje, a única.

Respondida em 2026-11-03, nesta sessão.

1. **Conta e cota no MCP para os três.** Opções:
   - a cota dos três pelo `rateLimits`, com troca de conta só no Claude e no Codex, os que o app lista; o Grok e o
     Antigravity na conta única (recomendada) — custo: ~3 h; se paga: hoje, porque o Codex a 97% faria o worker falhar
     sem freio;
   - a cota só do Grok, como a R1.2 literal, e o Codex e o `agy` como `quota_unknown` dentro do teto de sessões — custo:
     ~1,5 h; se paga: agora, com o Codex sem freio;
   - a recomendada mais várias contas Grok pelo `GROK_HOME`, com um passo no `brza-studio` para o `account list` as
     expor — custo: +~3 h e uma sessão no studio; se paga: quando houver uma segunda conta Grok, hoje nunca.

   **Decidido — "Cota dos 3, troca só Codex (Recomendado)".** Precisa a R1.2 no ponto da conta do Grok.

2. **O `--rename` e o `--wait` fora do Grok.** Opções:
   - só no Grok, como a R1.2, com o Codex e o `agy` recusados e uma issue para eles (recomendada) — custo: ~2,5 h; se
     paga: na primeira sessão Grok que outra sessão precisa achar pelo nome;
   - nos três, levantando onde o Codex e o `agy` gravam a sessão e o título — custo: +~3 h; se paga: quando forem
     abertos pelo nome com frequência; hoje, 1 abertura de cada desde 2026-10-29.

   **Decidido — "Nos três".** A E3 passa a ~5,5 h.

3. **A ordem das entregas.** Opções:
   - três entregas, cada uma com commit e usável — E1, o `brza sessions` abre o Grok e o MCP despacha aos três na conta
     padrão (~4,5 h); E2, a cota e a conta (~3 h); E3, o `--rename` e o `--wait` (~2,5 h) (recomendada) — custo: ~0,5 h a
     mais de testes de borda; se paga: a E1 serve no mesmo dia;
   - só o `brza sessions` primeiro (~0,5 h) e o MCP numa entrega única (~9,5 h) — custo: o despacho ao Grok espera ~1
     dia; se paga: hoje, se o urgente for abrir o Grok à mão;
   - uma entrega só, num merge (~10 h) — custo: nada usável antes do fim; se paga: só se as partes não servirem sozinhas.

   **Decidido — "Três entregas (Recomendado)".** Com a R2.2, a soma vai a ~13 h.

### Em aberto para o Desenho

Estrutura, para o Terreno responder com fonte; nenhum vai a Anderson antes de o código dizer:

1. o `worker-start --agent` aceita `grok` — a ajuda lista `claude, codex, cursor, antigravity, muse, zcode, opencode`
   como exemplo, e o `--model` cita o Grok;
2. o que o `--rename` quer dizer em cada runtime: o título da sessão que o Grok acha com `-r`, e o equivalente no Codex
   e no Antigravity;
3. onde cada runtime grava a sessão, para o `--wait` saber que ela está no ar;
4. por onde o MCP troca a conta do Codex: o `accounts.switch_chat_account` usa o RPC do H3, medido só no Claude.

## Worklogs

- 2026-11-03 — Passos 0 a 2, a R1 e a R2; o plano abriu, a issue irmã nasceu e a entrevista fechou. Parou no Terreno.
  [Abertura e entrevista do PLN-013, o Grok no `brza sessions` e no MCP](../../work/worklogs/2026-11-03-pln-013-abertura-e-entrevista.md)
