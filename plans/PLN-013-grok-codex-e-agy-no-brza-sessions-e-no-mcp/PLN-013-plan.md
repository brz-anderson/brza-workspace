---
status: open
phase: design
origin: request
description: O brza sessions abre o Grok com nome e espera, e o MCP despacha ao Grok, ao Codex e ao Antigravity com conta e cota por runtime
ready: "não — falta o aceite do corte em passos (R5)"
estimate_h: 16
executed_h: 0
remaining_h: 16
scope:
  - brza-workflow
opened: 2026-11-03
owner: Anderson
priority: high
tags:
  - tooling
---

# PLN-013: O Grok, o Codex e o Antigravity abrem pelo `brza sessions` e recebem tarefas do MCP

- **Retomar:** a entrevista (R1 a R4), o Desenho e os Passos estão gravados (2026-11-03). Próximo: a R5, o aceite do
  corte em passos; depois, o P1 (a sonda do `worker-start`), só a pedido de Anderson.
- **Dividido:** [PLN-013 — Entrevista](PLN-013-interview.md) · [PLN-013 — Desenho](PLN-013-design.md)

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

| Origem     | Critério de aceite | Passo | Teste (nível) |
| :--------- | :----------------- | :---- | :------------ |
| `Pedido 1` | `brza sessions <nome> --agent grok --title … --prompt …` abre o chat do Grok no app, grava o `open` no mapa, e `send <nome>` chega a ele | P3 | `test_brza_sessions` (unidade); abertura no app (manual) |
| `Pedido 2` | com `--agent grok`, `codex` ou `agy`, o `--wait` só anuncia com o `providerSession.id` no ar; o `--rename` dá o nome à sessão do runtime onde a sonda viu o `/rename` chegar, e só a aba e o mapa, com uma linha `CHECK`, onde não viu (R4.4/P6); agente fora dos quatro é recusado antes de abrir | P3, P8, P9, P10 | `test_brza_sessions` (unidade); a sonda e uma abertura de cada no app (manual) |
| `Pedido 3` | o `dispatch` aceita `runtime` `grok`, `codex`, `antigravity` e `agy`, este normalizado para `antigravity` antes da fila, e o worker abre pelo `worker-start --agent` do runtime | P1, P2 | `test_mcp_dispatch.py`, `test_mcp_cycle.py` (unidade); um worker de cada (manual, P1) |
| `Pedido 4` | o worker de cada runtime espera quando uma janela de topo do `rateLimits.<runtime>` passa do teto, e o `status` diz qual; o Grok, sem janela, fica em `quota_unknown` dentro do teto de sessões, e o `status` cita o `error` do `rateLimits.grok` (R4.2) | P5 | `test_mcp_limits.py`, `test_mcp_accounts.py`, `test_brza_quota.py` (unidade) |
| `R2.1`     | o worker Codex pode sair numa conta inativa (`inactiveCodexAccounts`) quando a ativa está no teto; o Grok e o Antigravity ficam na conta única `systemDefault` | P5, P6 | `test_mcp_accounts.py`, `test_mcp_gates.py` (unidade) |
| `R2.3`     | cada uma das três entregas sai num commit, mesclado na `master` do `brza-workflow`, e serve sozinha: E1 abrir e despachar, E2 a cota e a conta, E3 o `--rename` e o `--wait` | P4, P7, P11 | o gate de cada entrega e as duas revisões |
| `R3.1`, `R4.1` | o papel do pedido escolhe o modelo e o esforço pela linha do runtime no `brza.toml`, com a tabela da R4.1; um worker fora do Claude nunca sai com modelo do Claude nem chama o desempatador Haiku | P2 | `test_mcp_policy.py`, `test_mcp_cycle.py` (unidade); o P1 confere os quatro pares no `worker-start` real |
| `R3.3`, `R4.4` | com a cota do Codex no teto e uma conta inativa abaixo dele, o `dispatch` devolve a proposta de troca pelo gate; o `accounts.selectCodex` só roda na aprovação; o pedido que já espera não abre gate, e o `held_reason` diz que a troca só se propõe num `dispatch` novo | P6 | `test_mcp_gates.py`, `test_mcp_accounts.py` (unidade) |
| `R3.4`     | a sonda diz, para cada runtime, se o `/rename` mandado pelo chat do app roda como comando, onde o nome fica em disco, e o `providerSession.id` ao lado do id do runtime | P8 | a sonda, gravada no plano (manual) |
| `R4.2`     | a issue "o app não lê a cota do Grok" existe | P5 | o checador de notas |
| `Pedido 5` | a issue irmã existe, no formato da do Codex e do Antigravity | — (já aberta na abertura) | o checador de notas |

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


## Passos

Os passos executam a pedido de Anderson. O código vai ao `brza-workflow`, pelo `implementer`, conduzido pela sessão do
> `tools-kit`, numa branch por entrega, cada uma num worktree em `~/Projects/brza-workflow/.worktrees/`, nascida da
> `master` depois do merge da entrega anterior. A revisão de cada entrega vai pelo `reviewer` e por uma sessão Grok como
> segunda revisora, aberta pelo `brza sessions <nome> --agent grok --prompt-file <pedido>`. O merge na `master` do
> `brza-workflow` é com a confirmação de Anderson.
>
> **O gate de cada passo**, no worktree da entrega:
>
> ```bash
> PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/mcp
> ```
>
> ```bash
> env -u BRZA_WORKSPACE -u CLAUDE_PROJECT_DIR PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.cli.test_brza_sessions
> ```
>
> e, no passo de revisão, a suíte do `cli` inteira num ambiente limpo, como no PLN-009:
> `env -i HOME="$HOME" PATH="<dir do python3 3.10+>:/usr/bin:/bin" python3 -m unittest discover -s tests/cli`.
> A base, em 2026-11-03 no `ebb4e7d`: `tests/mcp` → 358 OK; `test_brza_sessions` → 39 OK.

### P1 — E1: a sonda do `worker-start` nos três runtimes

Executa D1, D2 · executor: a sessão do `tools-kit`, pelo `orca orchestration` do Studio

Estimado: 0.75 h · Executado: — h

- [ ] **1. Um worker real de cada runtime**, com o par da R4.1 que mais arrisca: `--agent codex --model gpt-6.1-sol
  --effort low` (modelo fora do catálogo semeado do app), `--agent codex --model gpt-6-astra --effort high`, `--agent
  grok --model grok-4.7 --effort xhigh`, `--agent antigravity --model gemini-4-argon-high` sem `--effort`.
- [ ] **2. Anotar no plano**, por worker: abriu em chat ou em terminal; o `--model` e o `--effort` foram aceitos ou
  recusados, com o código do erro.
- [ ] **3. Aplicar o resultado:** com o `xhigh` recusado, a linha `architect.grok` cai para `high` (R4.1); outra
  recusa vira ponto de rodada antes do P2.

**Evidência:** —

### P2 — E1: os runtimes no `dispatch` e a política por runtime

Executa D1, D2 · executor: `implementer`, pela sessão do `tools-kit`, em `~/Projects/brza-workflow/.worktrees/pln-013-e1`,
branch `feat/pln-013-e1-abrir-e-despachar`

Estimado: 4.5 h · Executado: — h

- [ ] **1. Testes que falham:** os da D1 (`test_mcp_dispatch.py`, `test_mcp_limits.py`, `test_mcp_cycle.py`) e os da
  D2 (`test_mcp_policy.py`, `test_mcp_cycle.py`), com a migração da chave plana nos testes existentes.
- [ ] **2. Implementar** `runtimes.py`, as mudanças em `tools.py`, `cycle.py`, `limits.py`, `accounts.active_id` e
  `policy.py`.
- [ ] **3. Rodar e ver passar:** o gate.
- [ ] **4. Commit** na `feat/pln-013-e1-abrir-e-despachar`.

**Evidência:** —

### P3 — E1: o `brza sessions` abre o Grok

Executa D3 · executor: `implementer`, pela sessão do `tools-kit`, no mesmo worktree; a abertura real, a sessão, com
Anderson conferindo a aba no app

Estimado: 0.5 h · Executado: — h

- [ ] **1. Teste que falha:** `test_unknown_agent_is_refused_before_any_side_effect`; o `grok` nos `subTest` de
  regressão.
- [ ] **2. Implementar** o `AGENTS`, o docstring e o `--help`.
- [ ] **3. Rodar e ver passar:** o gate.
- [ ] **4. Abertura real:** `brza sessions pln-013-sonda-grok --agent grok --title "PLN-013 E1: Grok" --prompt "diga
  oi"`, e `brza sessions send pln-013-sonda-grok "oi de novo"`; Anderson confere que as duas mensagens chegaram.
- [ ] **5. Commit.**

**Evidência:** —

### P4 — E1: a revisão e o merge

Executa D1, D2, D3 · executor: `reviewer` e uma sessão Grok, pela sessão do `tools-kit`; o merge, a pedido de Anderson

Estimado: 0.75 h · Executado: — h

- [ ] **1. Revisão pelo `reviewer`** e **pela sessão Grok**, sobre o diff da `feat/pln-013-e1-abrir-e-despachar`,
  com a suíte do `cli` limpa; os achados se corrigem pelo `implementer`, com commit.
- [ ] **2. Merge na `master` do `brza-workflow`**, com a confirmação de Anderson, e o `brza mcp stop` e `brza mcp
  start` do checkout principal, para o servidor carregar o código novo.
- [ ] **3. Um `dispatch` real** de consultant a cada runtime, pela sessão, e o `status` mostrando os três.

**Evidência:** —

### P5 — E2: a conta e o uso por runtime

Executa D4 · executor: `implementer`, pela sessão do `tools-kit`, em `~/Projects/brza-workflow/.worktrees/pln-013-e2`,
branch `feat/pln-013-e2-cota-e-conta`; a issue, a sessão

Estimado: 2.5 h · Executado: — h

- [ ] **1. Testes que falham:** os da D4 (`test_mcp_accounts.py`, `test_mcp_limits.py`, `test_mcp_dispatch.py`,
  `test_brza_quota.py`), com a fixture `orca-account-list.json` trazendo `codex`, `grok` e `antigravity`.
- [ ] **2. Implementar** o `parse` por runtime, o `Accounts` e o `Limits` com runtime, a `normalize_account`, o
  `quota_unknown` do `status` e o `quota_report`.
- [ ] **3. Rodar e ver passar:** o gate.
- [ ] **4. Commit** na `feat/pln-013-e2-cota-e-conta`.
- [x] **5. A issue da R4.2**, aberta na abertura do Desenho: [O app não lê a cota do Grok](../../work/issues/o-app-nao-le-a-cota-do-grok.md).

**Evidência:** —

### P6 — E2: a troca do Codex pelo gate

Executa D5 · executor: `implementer`, pela sessão do `tools-kit`, no mesmo worktree

Estimado: 1.5 h · Executado: — h

- [ ] **1. Testes que falham:** os da D5 (`test_mcp_gates.py`, `test_mcp_accounts.py`).
- [ ] **2. Implementar** o `codex_switch`, os dois motivos no gate, a ordem do `approve`, o `select_codex` e o
  `held_reason` do Codex.
- [ ] **3. Rodar e ver passar:** o gate.
- [ ] **4. Commit.**

**Evidência:** —

### P7 — E2: a revisão e o merge

Executa D4, D5 · executor: `reviewer` e uma sessão Grok, pela sessão do `tools-kit`; o merge, a pedido de Anderson

Estimado: 0.5 h · Executado: — h

- [ ] **1. Revisão pelo `reviewer`** e **pela sessão Grok**; os achados se corrigem pelo `implementer`, com commit.
- [ ] **2. Merge na `master` do `brza-workflow`**, com a confirmação de Anderson, e o `brza mcp stop` e `brza mcp
  start`.
- [ ] **3. O `brza quota`** real mostra o Codex, o Antigravity e o Grok sem janela, com o `error`.

**Evidência:** —

### P8 — E3: a sonda do `/rename`

Executa D6 · executor: a sessão do `tools-kit`, com Anderson conferindo na tela o que cada chat mostra

Estimado: 0.5 h · Executado: — h

- [ ] **1. A sonda da D6** nos três runtimes, com o `brza sessions` da `master`.
- [ ] **2. Gravar no plano** o resultado por runtime, com o `providerSession.id` e o id do runtime lado a lado.
- [ ] **3. A issue** de cada runtime com sonda negativa (R4.4/P6).

**Evidência:** —

### P9 — E3: o `--wait` nos quatro e o `provider_session`

Executa D6 · executor: `implementer`, pela sessão do `tools-kit`, em `~/Projects/brza-workflow/.worktrees/pln-013-e3`,
branch `feat/pln-013-e3-rename-e-wait`

Estimado: 1.5 h · Executado: — h

- [ ] **1. Testes que falham:** os da D6 em `test_brza_sessions.py`.
- [ ] **2. Implementar** o `provider_session` nos quatro, o `session_map`, o `list --json` e a leitura do agente da
  aba.
- [ ] **3. Rodar e ver passar:** o gate.
- [ ] **4. Commit** na `feat/pln-013-e3-rename-e-wait`.

**Evidência:** —

### P10 — E3: o `--rename` por runtime

Executa D7 · executor: `implementer`, pela sessão do `tools-kit`, no mesmo worktree

Estimado: 2 h · Executado: — h

> A faixa é de 1,5 h, com a sonda negativa nos três, a 3 h, com ela positiva nos três.

- [ ] **1. Testes que falham:** os da D7, só das linhas de `NAMED` que a sonda confirmou, e o da saída do P6.
- [ ] **2. Implementar** o `NAMED`, o `wait_for_name` por runtime e a linha `CHECK`.
- [ ] **3. Rodar e ver passar:** o gate.
- [ ] **4. Commit.**

**Evidência:** —

### P11 — E3: a revisão, o merge e uma abertura de cada

Executa D6, D7 · executor: `reviewer` e uma sessão Grok, pela sessão do `tools-kit`; o merge, a pedido de Anderson;
as aberturas, a sessão, com Anderson conferindo as abas

Estimado: 1 h · Executado: — h

- [ ] **1. Revisão pelo `reviewer`** e **pela sessão Grok**; os achados se corrigem pelo `implementer`, com commit.
- [ ] **2. Merge na `master` do `brza-workflow`**, com a confirmação de Anderson.
- [ ] **3. Uma abertura de cada:** `brza sessions pln-013-<rt> --agent <rt> --rename --wait --prompt "diga oi"` nos
  três, com o `open:` só depois do `providerSession.id`.

**Evidência:** —

### As horas

| Entrega | Passos       | Estimado |
| :------ | :----------- | :------- |
| E1      | P1 a P4      | 6,5 h    |
| E2      | P5 a P7      | 4,5 h    |
| E3      | P8 a P11     | 5 h      |
| Total   |              | 16 h     |

> A E1 sobe de ~4,5 h (R2.3) porque a R3.1 trocou a opção de ~1 h pela tabela de ~2,5 h; a E3 fica na faixa de 4 a
> 5,5 h, com o meio, até a sonda dizer (REV-010/A11).

## Worklogs

- 2026-11-03 — Passos 0 a 2, a R1, a R2, o Terreno e a R3; o plano abriu e a issue irmã nasceu. Parou nos itens `D`.
  [Abertura e entrevista do PLN-013, o Grok no `brza sessions` e no MCP](../../work/worklogs/2026-11-03-pln-013-abertura-e-entrevista.md)

## Revisões

- [REV-010: O Desenho do PLN-013, revisado pela sessão Grok](../../work/reviews/REV-010-pln-013-o-desenho-pelo-grok.md)
  — 2026-11-03, 16 achados: 15 corrigidos no Desenho e o A15 falso.

## Pendências conhecidas

- [O app não lê a cota do Grok](../../work/issues/o-app-nao-le-a-cota-do-grok.md) — da R4.2; o Grok fica em
  `quota_unknown` até o app ler a cota.
