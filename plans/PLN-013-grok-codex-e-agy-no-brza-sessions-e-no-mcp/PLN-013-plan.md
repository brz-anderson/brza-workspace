---
status: open
phase: design
origin: request
description: O brza sessions abre o Grok com nome e espera, e o MCP despacha ao Grok, ao Codex e ao Antigravity com conta e cota por runtime
ready: "não — faltam os itens D das três entregas; isso trava os Passos"
scope:
  - brza-workflow
opened: 2026-11-03
owner: Anderson
priority: high
tags:
  - tooling
---

# PLN-013: O Grok, o Codex e o Antigravity abrem pelo `brza sessions` e recebem tarefas do MCP

- **Retomar:** R1 a R3 respondidas e o Terreno gravado em 2026-11-03. Próximo: os itens `D` das três entregas da R2.3,
  por um `designer`, com os valores da tabela de modelo por runtime da R3.1 como ponto de rodada.

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
| `R3.1`     | o papel do pedido escolhe o modelo e o esforço pela tabela do runtime no `brza.toml`; um worker Codex ou Grok nunca sai com `--model sonnet` | — | `tests/mcp/test_mcp_policy.py` (unidade) |
| `R3.3`     | com a cota do Codex no teto, o worker espera e o `dispatch` devolve a proposta de troca pelo gate; o `accounts.selectCodex` só roda com a aprovação | — | `tests/mcp/test_mcp_gates.py`, `test_mcp_accounts.py` (unidade) |
| `R3.4`     | a sonda diz, para cada runtime, se o `/rename` mandado pelo chat do app chega ao runtime e onde o nome fica em disco | — | a sonda, gravada no plano (manual) |
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

Estrutura, para o Terreno responder com fonte; nenhum vai a Anderson antes de o código dizer. **→ respondidos no
Terreno**, e o que o código não resolveu foi à R3:

1. o `worker-start --agent` aceita `grok` — a ajuda lista `claude, codex, cursor, antigravity, muse, zcode, opencode`
   como exemplo, e o `--model` cita o Grok;
2. o que o `--rename` quer dizer em cada runtime: o título da sessão que o Grok acha com `-r`, e o equivalente no Codex
   e no Antigravity;
3. onde cada runtime grava a sessão, para o `--wait` saber que ela está no ar;
4. por onde o MCP troca a conta do Codex: o `accounts.switch_chat_account` usa o RPC do H3, medido só no Claude.

### Rodada 3 — o modelo, a cota por runtime, a troca do Codex e o `--rename` (enviada 2026-11-03)

> **Apresentado antes:** o Terreno, abaixo. O que mudou desde a R2: o Codex voltou a `session` 1% e não tem segunda
> conta no app (`inactiveCodexAccounts: []`), e o Antigravity está a `weekly` 99%. A sessão conferiu
> `worker-start-validation.ts:146-157`, `policy.py:210-215` e `limits.py:156`; a configuração de chat ou terminal por
> agente não está nos JSON do app, e a sonda dela vai ao primeiro subpasso da E1, sem rodada.

Respondida em 2026-11-03, nesta sessão.

1. **O modelo e o esforço dos workers fora do Claude.** Opções:
   - a política de papéis só no `claude`, e nos outros o `model` e o `effort` do pedido ou o padrão do runtime
     (recomendada) — custo: ~1 h na E1; se paga: no primeiro worker fora do Claude, que sem isso sai com `--model
     sonnet` e falha;
   - uma tabela `policy.roles.<papel>.<runtime>` no `brza.toml` — custo: ~2,5 h e a mudança no `brza.toml`; se paga:
     quando houver modelo por papel no Codex ou no Grok;
   - exigir `model` no pedido fora do Claude — custo: ~0,5 h; se paga: só se o padrão do runtime for ruim.

   **Decidido — "Tabela por runtime".** Os valores de cada papel em cada runtime vão a uma rodada do Desenho.

2. **A conta ativa e a cota por runtime.** Opções:
   - a conta ativa e o uso lidos por runtime, com o Grok e o Antigravity na conta única e a cota pelas janelas
     `session` e `weekly` de topo (recomendada) — custo: ~1,5 h na E2; se paga: já na E2, com o Antigravity a 99%
     retido até a cota renovar;
   - o mesmo, com o Antigravity pelos `buckets` do grupo do modelo — custo: +~1,5 h e um mapa de modelo para grupo; se
     paga: quando os grupos divergirem e o worker parado custar trabalho;
   - só a chave por runtime, sem ler a conta ativa fora do Claude — custo: ~0,5 h; se paga: se o Codex nunca tiver
     segunda conta, e a troca da R2.1 sai.

   **Decidido — "Por runtime, janelas de topo (Recomendado)".**

3. **A troca de conta do Codex.** Opções:
   - segurar o worker e devolver a proposta de troca pelo gate da sessão principal (PLN-003/R5.2), com o
     `accounts.selectCodex` só depois da aprovação, em código e teste, sem prova real (recomendada) — custo: ~1,5 h na E2;
     se paga: quando houver uma segunda conta Codex;
   - só segurar, sem trocar — custo: ~0 h; se paga: se a troca global for risco demais; desfaz a troca da R2.1;
   - trocar sem gate — custo: ~1 h; se paga: nunca, porque a troca global afeta os outros workers e os chats abertos.

   **Decidido — "Segura e propõe pelo gate (Recomendado)".**

4. **O que o `--rename` quer dizer fora do Claude.** Opções:
   - uma sonda de ~0,5 h antes da E3, mandando o `/rename` pelo `agentSession.send` nos três, com a E3 seguindo o que
     ela mostrar e o `--wait` pelo `providerSession.id` (recomendada) — custo: ~0,5 h e o `grok login`; se paga: na E3;
   - só o título da aba, pelo `agentSession.rename`, e o mapa — custo: ~0 h além do `--wait`; se paga: se o correio do
     Claude for o único consumidor do nome do runtime;
   - o Grok fora do `--rename` até o login — custo: parte da R2.2 espera; se paga: se o login demorar.

   **Decidido — "Sonda antes da E3 (Recomendado)".**

## Desenho

### O que este desenho assume

- **R1.3, R2.1, R3.2:** os três runtimes no `dispatch`; a conta ativa e a cota lidas por runtime, pelas janelas de topo
  do `rateLimits`; o Grok e o Antigravity na conta única.
- **R3.1:** o modelo e o esforço por papel e por runtime, numa tabela do `brza.toml`.
- **R3.3:** a troca de conta do Codex passa pelo gate, e o `accounts.selectCodex` só roda aprovado.
- **R2.2, R3.4:** o `--rename` e o `--wait` nos quatro runtimes; o `--wait` pelo `providerSession.id`, o `--rename` pelo
  que a sonda mostrar.
- **R2.3:** três entregas, cada uma com commit e usável: E1 abrir e despachar, E2 a cota e a conta, E3 o `--rename` e o
  `--wait`.

### Terreno

Levantado em 2026-11-03 por um `collector`, só leitura; a sessão conferiu os três primeiros fatos do MCP e o do
`worker-start`.

#### O `worker-start` do app

- **Aceita `grok`, `codex` e `antigravity`.** `brza-studio/src/main/runtime/rpc/methods/orchestration/worker/worker-start-validation.ts:146-157`
  — o `--agent` passa por `isTuiAgent` e pelo `validateOrchestrationAgentLauncher`; o `settings.getAgentLaunch` deu
  `disabledTuiAgents: []`. A lista do `--help` é exemplo.
- **O `--model` e o `--effort` valem nos três.** `orchestration-worker-specs.ts:43-44`; o catálogo do app dá ao Grok os
  modelos 4.7, 4.6 e 4.5, com esforço de `low` a `xhigh`, ao Codex esforço até `ultra`, e ao Antigravity `models: []` e
  esforço `low` a `high`.
- **Chat ou terminal segue a configuração do usuário, sem flag.** `src/main/agent-launch/agent-launch-mode.ts:98-160`.
  No chat, o Grok e o Antigravity vão por ACP (`src/main/acp/acp-launch-specs.ts:297-303`); o Claude e o Codex, por
  adaptador de CLI. O valor atual por agente não sai em RPC de leitura nem nos JSON do app.

#### O MCP

- **Quatro pontos fixos no Claude.** `brza_mcp/tools.py:25` (o enum em `:32`, a recusa em `:192-193`, o padrão em
  `:217`), `cycle.py:22` (usado em `:152`), `accounts.py:24` e `limits.py:225`.
- **A conta ativa é a do Claude para qualquer runtime.** `limits.py:156` (`_active`), `:166-210` (`_account`,
  `_sessions`, `_quota`, `_account_matches`) e `tools.py:140-156` (`normalize_account`).
- **O `accounts.parse` lê só o Claude.** `accounts.py:56-76` lê `claude`, `rateLimits.claude` e
  `rateLimits.inactiveClaudeAccounts`; `usage()` (`:151`) devolve `None` aos outros, o que vira `quota_unknown`.
- **O `_windows` já lê os blocos dos outros.** Rodado contra o `account list --json` real: Codex `session` 1% e `weekly`
  0%; Antigravity `session` 37% e `weekly` 99%, com `buckets` por grupo que ele ignora; Grok `[]`, sem login.
- **A política é toda Claude.** `policy.py:28-30` dá `sonnet` e `opus` aos papéis, e `policy.py:210-215` os põe por cima
  do pedido.
- **O `pick_account` e o `switch_chat_account` não têm chamador** fora dos testes.

#### A conta do Codex

- **Hoje só há a `systemDefault`.** `account list --json`: `codex.accounts = []`, `inactiveCodexAccounts = []`.
- **A troca é global, do app.** `brza-studio/src/main/runtime/rpc/methods/accounts.ts:153-165` — `accounts.selectCodex` e
  `selectCodexForTarget`, com a permissão `accounts-admin`; não há flag de conta no `worker-start`.
- **O `switch_chat_account` não serve ao Codex.** O `prepareAccountSwitch` só existe no adaptador do Claude
  (`claude-structured-session-adapter.ts:153`), e o roteador devolve `unknown-account` aos outros
  (`brza-router-record-methods.ts:10-13`).
- **A conta do Codex vai no `CODEX_HOME`**, que o app aplica pela conta ativa; o resumo da conta Codex não traz `home`.

#### O `--rename` e o `--wait`

- **O caminho do Claude.** `brza-workflow/packages/client/bin/brza-sessions` — o `/rename` como primeiro prompt
  (`:387`), o título da aba pelo `agentSession.rename` (`:401`), o `open` no mapa (`:404`), o `--wait` pelo
  `providerSession.id` (`:193-212`) e pelo `<config>/sessions/<pid>.json` (`:127-151`, `:184-190`), o evento `session`
  (`:417`).
- **Há um id de sessão nos quatro.** O `agentSession.history` devolve `providerSession{key: 'session_id', id}`, rodado
  nos chats reais do Claude, do Codex e do Antigravity; o do Grok, sem login, não traz.
- **O `agentSession.rename` só dá o nome no app**, não no runtime.
- **O nome no runtime, por evidência fraca** (binários e ajuda, nada exercitado pelo chat): o Grok tem `/rename` e acha
  pelo título com `grok -r`; o Codex tem o slash "rename the current thread", com o nome em `~/.codex/session_index.jsonl`
  (`thread_name`); o Antigravity tem `/rename` no `strings` do `agy`.
- **Onde cada um grava a sessão:** o Grok em `~/.grok/sessions/<cwd>/<id>/summary.json`; o Codex em
  `~/.codex/sessions/AAAA/MM/DD/rollout-*.jsonl`; o Antigravity do chat em
  `<dados do app>/antigravity-chat/antigravity-acp/conversations/<uuid>.db`.
- **Bug latente no `list`.** `brza-sessions:244` lê `tab.get('agentSessionAgent')`, e as abas reais trazem `agent`.

#### Os testes

- **O `brza sessions`:** `tests/cli/test_brza_sessions.py`, com os casos fora do Claude em `:364-450`, que hoje asserem
  a recusa do `--rename` e do `--wait`. 4 dos 39 falham com o `BRZA_WORKSPACE` herdado do worktree; a base sai com o
  env limpo.
- **O MCP:** `tests/mcp/test_mcp_dispatch.py:85` (a recusa do `codex`, que a E1 inverte), `test_mcp_cycle.py:78`,
  `test_mcp_limits.py`, `test_mcp_accounts.py:391-406`, `test_brza_quota.py` e a fixture
  `fixtures/orca-account-list.json`. `python3 -m unittest discover -s tests/mcp` → 358 OK.

## Worklogs

- 2026-11-03 — Passos 0 a 2, a R1, a R2, o Terreno e a R3; o plano abriu e a issue irmã nasceu. Parou nos itens `D`.
  [Abertura e entrevista do PLN-013, o Grok no `brza sessions` e no MCP](../../work/worklogs/2026-11-03-pln-013-abertura-e-entrevista.md)
