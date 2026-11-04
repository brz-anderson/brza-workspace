---
status: in_progress
phase: execution
origin: issue
origin_ref: brza-chat-list-read-send-no-studio
description: O brza-studio ganha brza chat list/read/send com cursor, fila e recibos, a navegação de chats pela CLI, pela barra lateral e pela Jump Palette, o Native Chat na API de plugins e o account usage, em fases por prioridade.
ready: sim
estimate_h: 31
executed_h: 1.6
remaining_h: 21.0
priority: high
scope:
  - brza-studio
opened: 2026-11-03
owner: Anderson
tags:
  - chat
  - tooling
---

# PLN-011: Os chats do BrzA Studio se coordenam pela CLI, aparecem na navegação e chegam aos plugins

- **Retomar:** o P4 está fechado em `brza-studio@0de38e7d082`, com REV-011 aprovada pelo Grok, A1/A2 corrigidos
  em `a243520d41f` e R20 implementada e revisada (X5). Próximo passo: P5, `chat send --operation`, no worktree
  `pln-011-chat-cli`, branch `feat/pln-011-chat-cli`, a partir de `0de38e7d0828d5ff77b688d1f3d20373d160522f`.
- **Dividido:** [PLN-011 — Entrevista](PLN-011-interview.md) · [PLN-011 — Desenho](PLN-011-design.md)

## Pedido

- **Origem:** [O `brza chat list/read/send` coordena chats abertos no BrzA Studio](../../work/issues/brza-chat-list-read-send-no-studio.md),
  com as outras frentes em
  [O chat ativo se escolhe pela CLI e aparece na barra lateral e na Jump Palette](../../work/issues/chat-ativo-pela-cli-na-barra-lateral-e-na-jump-palette.md),
  [Os plugins enxergam as sessões de Native Chat](../../work/issues/native-chat-na-api-de-plugins.md) e
  [O `brza account usage` mostra o uso dos limites por conta](../../work/issues/brza-account-usage-na-cli.md); todas
  nascem da issue do `playground`
  [Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](../../work/issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md).

Pedido de 2026-11-03, da sessão "Plano: chat via CLI e plugins" do `playground`:

> abra o plano do workstream `studio` para a coordenação, a navegação e a exposição de chats pela CLI e aos plugins, a
> partir da issue de origem do `playground`.

E o pedido da issue de origem, em "O que fazer":

> Implementar `brza chat list/read/send/focus`, incluir Native Chat na Jump Palette e na seleção da barra lateral, e
> expor Native Chat em `agents.list` no `brza-studio`, alinhando com as necessidades do `brza-workflow`.

### Fases

Na ordem da prioridade, como decidido em R4.2 e R4.3; cada fase fecha a issue dela. A fase 3 saiu do plano em R11.4,
e a numeração das outras fica.

| Fase | Prioridade | Frente | Issue |
| :--- | :--------- | :----- | :---- |
| 1 | `high` | Coordenação: `brza chat list/read/send` com cursor, fila e recibos, pelo porte do `#33115` estendido (R5.2); o `#37774` saiu da fase em R5.1 | [O `brza chat list/read/send` coordena chats abertos no BrzA Studio](../../work/issues/brza-chat-list-read-send-no-studio.md) |
| 2 | `medium` | Navegação: `brza chat focus`, a seleção da barra lateral e a Jump Palette | [O chat ativo se escolhe pela CLI e aparece na barra lateral e na Jump Palette](../../work/issues/chat-ativo-pela-cli-na-barra-lateral-e-na-jump-palette.md) |
| 3 | `medium` | Journal: fora do plano desde a R11.4, pelo `### Fora de escopo` | — |
| 4 | `low` | Plugins: Native Chat em `agents.list` e `agent.status.changed`, e o caminho em `workspace.readContext` | [Os plugins enxergam as sessões de Native Chat](../../work/issues/native-chat-na-api-de-plugins.md) |
| 5 | `low` | `brza account usage` | [O `brza account usage` mostra o uso dos limites por conta](../../work/issues/brza-account-usage-na-cli.md) |

### Cobertura

| Origem | Critério de aceite | Passo | Teste (nível) |
| :----- | :----------------- | :---- | :------------ |
| Fase 1, R5.2, R13.4 | `brza chat list --json` lista os chats abertos com `session`, `handle`, `worktree` e `title`, e o id que `read` e `send` aceitam | P1 | `chat.test.ts` (unidade) |
| Fase 1, R2.1, R6.3, R8.3, R13.4 | `brza chat read --cursor <epoch:sequence>` lê uma página `after` e devolve só o que mudou, com `itemId`, `revision`, `sequence`, `removedItemIds`, `nextCursor` e `hasNewer`; recusa `--limit` junto | P3 | `chat.test.ts`, `chat-cursor.test.ts` (unidade); C1 (manual) |
| Fase 1, R5.3, R8.1, R8.2 | o cursor inválido sai 2 com `cursor_reset: <motivo>`, a página `tail` e o `nextCursor` novos, também no reset repetido | P3 | `chat.test.ts`, um caso por motivo (unidade) |
| Fase 1, R2.2, R5.4, R9.2 | o `send` enfileirado diz a posição, o `nextQueuedMessageId` e `held_by: question\|working\|null`, com `queuePaused` no Stop | P4 | `chat.test.ts`, `chat-queue-hold.test.ts` (unidade); C1 (manual) |
| Fase 1, R6.1, R9.1, R9.3 | o `send` sai 0 em `accepted` e `queued`, 1 em recusa, `rejected`, `returned` e `withdrawn`, 3 em `unknown` e no `pending` que não resolve em 30 s | P4 | `chat-send-outcome.test.ts`, `chat.test.ts` (unidade) |
| Fase 1, R6.2, R13.4 | `send --operation <id>` com o mesmo texto devolve o gravado sem reenviar, e o `unknown` continua `unknown` | P5 | `chat.test.ts` (unidade); C1 (manual) |
| Fase 1, R6.3 | o `send` leva o `ORCA_AGENT_SESSION_ID` como origem do coordenador e o `expectedRuntimeFence` lido do histórico | P2, P4 | `client-execution-host.test.ts`, `chat.test.ts` (unidade); C1 (manual) |
| Fase 2, R10.1 | `brza chat focus --session <id>` traz o app à frente com o chat ativo | P8 | teste do roteamento do reveal (unidade); C2 (manual) |
| Fase 2, R10.2 | a barra lateral destaca o chat ativo, qualquer que seja a origem da troca | P9 | testes da barra lateral (unidade); C2 (manual) |
| Fase 2, R10.3 | a Jump Palette lista os chats nas recentes, os acha pelo título e os abre como chat | P10 | testes do builder e da ativação (unidade); C2 (manual) |
| Fase 4, R11.1, R11.2 | `agents.list` e `agent.status.changed` trazem `kind`, `sessionId`, `model` e `providerSessionId` do chat, sem caminho, e o contrato só cresce | P13, P14 | testes da projeção e do schema (unidade) |
| Fase 5, R11.3 | `brza account usage` imprime o uso por conta, em texto e `--json` | P16 | `account-usage-*.test.ts` (unidade) |

### Fora de escopo

- **O `brza sessions` do `brza-workflow` sobre a CLI nova** — os aliases, o retry e o resultado fiel do envio no
  wrapper. Vão ao PLN-010 do `tools-kit`, com `depends_on` neste, como decidido em R4.1.
- **O porte do `stablyai/orca#37774`** (o rascunho do chat de terminal limpo antes do envio). Chega no próximo sync do
  upstream; só se porta antes se o `brza chat send` passar a cobrir chat PTY, como decidido em R5.1.
- **A fase 3, a limpeza do journal fora do thread principal.** Saiu do plano em R11.4 e fica na issue
  [A limpeza do journal de chats sai do thread principal](../../work/issues/limpeza-do-journal-de-chats-fora-do-thread-principal.md),
  com o gatilho "o `#37802` integrado no upstream".
- **O caminho do worktree em `workspace.readContext` e o `cwd` do chat.** Não agora, pela R11.2: volta depois da
  sandbox do worker de plugin, por permissão.

## Restrições

- **Os gates pré-aprovados valem só para `implementer` e `reviewer` com `ref: PLN-011`, na conta ativa** (R7.2). Gate
  de troca de conta ou de outro papel para e vai a Anderson.
- **Do P3 em diante, os workers saem do `brza-mcp`** (R18.1): ele só aceita o runtime `claude`, e a cota da Claude
  segurava o P3. O `brza-mcp` fica de pé, sem pedidos deste plano.
- **O `reviewer` e o `designer` são a sessão Grok 4.7** (R19.2), `grok_18ca2288_cf47_4da8_abf1_781cef5885a6`, com o
  pedido pelo `orchestration send --to orca_session_id:…` e o parecer num arquivo do scratch. O `agy` fica nas rodadas,
  com `gemini-3.8-flash-high`: "a cota do `Argon 4` acabou", nas palavras de Anderson em 2026-11-03.
- **O `brza-mcp` roda o código da `feat/pln-009-mcp`, sem merge** (R7.1): defeito do orquestrador vai ao PLN-009, numa
  issue do `tools-kit`, e não se corrige daqui.

## Pré-requisitos

- **O `brza-mcp` de pé:** `brza-mcp status` → "carregado: sim" e "health: responde". Parado, `brza-mcp start`.
- **A sessão coordenadora é um chat do Studio** (R12.1), com `ORCA_AGENT_SESSION_ID` e `ORCA_USER_DATA_PATH` no
  ambiente, que chama o `/mcp` por HTTP com o Bearer de `~/.brza/runtime/mcp.token` e os headers `X-Brza-Session` e
  `X-Brza-Client`.

## Passos

Cada passo de código roda num worker `implementer` e é revisado por um worker `reviewer` antes do passo seguinte (R7).
O P1 e o P2 rodaram pelo `dispatch` do `brza-mcp`; do P3 em diante, pela R18.1, o `implementer` roda em Codex e o
`reviewer` é a sessão Grok 4.7 (R19.2), pelo `orchestration worker-start` e pelo `orchestration send` do Studio, no
worktree da fase. Os gates dos dois, com `ref: PLN-011`, estão pré-aprovados (R7.2). Cada passo é
um commit verde; o worker roda só o alvo, e a suíte inteira roda uma vez, no merge de cada fase, pela coordenação.

### Fase 1 — coordenação

Branch `feat/pln-011-chat-cli`, worktree `~/Projects/brza-studio/.worktrees/pln-011-chat-cli`, nascido da `master`
`8f41dd56a33`.

Preparação do worktree, uma vez, no início do P1:

```bash
cd "$HOME/Projects/brza-studio" && git worktree add .worktrees/pln-011-chat-cli -b feat/pln-011-chat-cli master
```

```bash
cd "$HOME/Projects/brza-studio/.worktrees/pln-011-chat-cli" && pnpm install --offline --frozen-lockfile
```

#### P1 — O porte do `#33115`, sozinho

Executa D1 · executor: worker `implementer` do `brza-mcp`, no worktree do `brza-studio`

Estimado: 1,5 h · Executado: 0,3 h, com a revisão

- [x] **1. Teste que falha** — antes do porte, `src/cli/handlers/chat.test.ts` não existe; o teste chega com o diff e
      falha só se o porte quebrar.
- [x] **2. Aplicar** — `gh pr diff 33115 -R stablyai/orca | git apply --3way`, conferindo que a cabeça ainda é
      `a007c29e248` (`gh pr view 33115 -R stablyai/orca --json headRefOid`).
- [x] **3. Rodar e ver passar** —
      `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts src/cli/handlers/chat.test.ts src/cli/handler-group-manifest.test.ts --maxWorkers=2`;
      `pnpm verify:bundled-skill-guides`; `pnpm tc:cli`; `pnpm check:changed --base=origin/master --maxWorkers=2`.
- [x] **4. Commit** — `feat(cli): porta chat list/read/send do stablyai/orca#33115`, com o trailer
      `Upstream: stablyai/orca#33115 @ a007c29e248`. Nenhuma linha nossa no commit.
- [x] **5. Revisão independente** — um worker `reviewer` do `brza-mcp`, com `ref: PLN-011/P1`, revisa o commit
      contra o D e a Cobertura; o parecer vai a `work/reviews/` (`brza note review-open`), e cada achado tem destino
      antes do passo seguinte.

**Evidência:** `brza-studio@f633ec3e307` (o porte, cabeça `a007c29e248` conferida) e `brza-studio@df8adc29574` (X2) ·
o vitest de `chat.test.ts` e `handler-group-manifest.test.ts` → 17 passed (11 + 6); `worktree-ps-*` → 9 passed;
`pnpm verify:bundled-skill-guides`, `pnpm tc:cli` → exit 0; `pnpm check:changed` → 22/22 depois do X2 ·
[REV-007: o P1 do PLN-011, o porte do `#33115`](../../work/reviews/REV-007-pln-011-p1-porte-33115.md), aprova com o A1
corrigido no D1

#### P2 — A origem do coordenador no `agentSession.send`

Executa D2 · executor: worker `implementer` do `brza-mcp`, no worktree do `brza-studio`

Estimado: 1 h · Executado: 0,3 h, com a revisão

- [x] **1. Teste que falha** — em `src/cli/runtime/client-execution-host.test.ts`: `evidenceSent(client, 'agentSession.send')`
      igual a `{ agentSessionId: CALLER_CHAT }` (falha hoje: `undefined`); `agentSession.history` continua `undefined`; o
      caso WSL e o pareado com `agentSession.send` continuam sem evidência.
- [x] **2. Implementar** — o diff do D2.
- [x] **3. Rodar e ver passar** —
      `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts src/cli/runtime/client-execution-host.test.ts src/cli/runtime-client.test.ts --maxWorkers=2`; `pnpm tc:cli`.
- [x] **4. Commit** — `feat(cli): agentSession.send leva o chat chamador como coordenador`.
- [x] **5. Revisão independente** — um worker `reviewer` do `brza-mcp`, com `ref: PLN-011/P2`, revisa o commit
      contra o D e a Cobertura; o parecer vai a `work/reviews/` (`brza note review-open`), e cada achado tem destino
      antes do passo seguinte.

**Evidência:** `brza-studio@63aa99c2505` e `brza-studio@594c4a7e13c` (o A1) · o teste novo falha na `df8adc29574` (1
failed, 7 passed) e passa no commit; `client-execution-host` e `runtime-client` → 24 passed; a regressão de terminal e
chat → 73 passed; `pnpm tc:cli` → exit 0; `pnpm check:changed --force` → 22/22 ·
[REV-008: o P2 do PLN-011, a origem do coordenador no `agentSession.send`](../../work/reviews/REV-008-pln-011-p2-origem-do-coordenador.md)

#### P3 — `chat read` com cursor, ids e reset

Executa D3, D6 · executor: worker `implementer` em Codex (R18.1), no worktree do `brza-studio`

Estimado: 3,5 h · Executado: 0,3 h, com a revisão

- [x] **1. Testes que falham** — em `src/cli/handlers/chat.test.ts`, com o `fakeClient` do `#33115`:
      - sem `--cursor`: `entries` com `itemId`, `revision`, `sequence`; `nextCursor` = `liveCursor` formatado; `hasNewer: false`;
      - `--cursor e:9`: uma chamada `after` com `cursor: { epoch: 'e', sequence: 9 }` e `limit: 200`; `nextCursor` =
        `window.nextCursor`; `hasNewer` da página; `removedItemIds` passa;
      - um caso por motivo de reset (`epoch_changed`, `cursor_ahead`, `cursor_compacted`, `journal_gap`,
        `schema_unreadable`): `cursor_reset` no JSON, `entries` da página `tail`, `nextCursor` = `liveCursor`, e
        `process.exitCode` igual a 2, pela R8.1;
      - cursor malformado (`abc`, `e:-1`, `:3`): `invalid_argument`, sem chamada ao host;
      - epoch com `:` (`a:b:7`) vira `{ epoch: 'a:b', sequence: 7 }`;
      - reset `cursor_compacted` duas vezes seguidas → as duas saem 2, com a página `tail`, e o guia diz "leia sem `--cursor`" (R8.2);
      - `--cursor` com `--limit`: recusado com `invalid_argument`, pela R8.3.
      E `src/cli/brza/chat-cursor.test.ts` para o parse e o formato.
- [x] **2. Implementar** — `src/cli/brza/chat-cursor.ts`; o ramo `--cursor` no `chat read`; os ids no
      `chatTranscript` (o tipo de entrada ganha `itemId`, `revision`, `sequence`); o `nextCursor` e o `hasNewer` no
      resultado; o spec e a linha do guia (D6), e `pnpm generate:bundled-skill-guides`.
- [x] **3. Rodar e ver passar** —
      `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts src/cli/handlers/chat.test.ts src/cli/brza/chat-cursor.test.ts --maxWorkers=2`;
      `pnpm verify:bundled-skill-guides`; `pnpm tc:cli`; `pnpm check:changed --base=origin/master --maxWorkers=2`.
- [x] **4. Commit** — `brza-studio@77a1cca1af2` (`feat(cli): chat read --cursor lê só o que mudou e avisa o cursor_reset`);
      correções dos achados em commit separado `brza-studio@a7099022850`.
- [x] **5. Revisão independente** — a sessão Grok 4.7, `reviewer` (R19.2), com `ref: PLN-011/P3`, revisa os dois commits
      contra o D e a Cobertura; o parecer vai a `work/reviews/` (`brza note review-open`), e cada achado tem destino
      antes do passo seguinte. Antigravity também revisou o commit inicial e aprovou sem achados.

**Evidência:** `brza-studio@77a1cca1af2` + `brza-studio@a7099022850` · teste alvo → 31/31 passed;
`pnpm verify:bundled-skill-guides`, `pnpm tc:cli`, `pnpm check:changed --base=origin/master --maxWorkers=2 --force`
→ 22/22; `oxlint` e `oxfmt --check` passaram · REV-009 aprovada. Os três achados A1–A3 do Grok sobre o primeiro
commit estão resolvidos no segundo.

#### P4 — `chat send` com estado, códigos de saída e fila

Executa D4, D6 · executor: worker `implementer` em Codex (R18.1), no worktree do `brza-studio`

Estimado: 4 h · Executado: 0,7 h, com a revisão

- [x] **1. Testes que falham** — `src/cli/brza/chat-send-outcome.test.ts`, uma linha da tabela do D4 por caso; e em
      `src/cli/handlers/chat.test.ts`:
      - `queued` com página seguinte de `actionablePromptIds: ['p1']` → `held_by: 'question'`, `queuePosition`,
        `nextQueuedMessageId`, saída 0;
      - `queued` com `working: true` e sem prompt → `held_by: 'working'`;
      - `queuePause: { reason: 'stopped' }` → `held_by: null`, `queuePaused: true`; fila escoada → `held_by: null` (R9.2);
      - replay `returned` ou `withdrawn` → `rejected`, 1 (R9.3);
      - `queued` com prompt e `working` → `question` (o prompt vence);
      - `accepted` → 0; `rejected` → 1; `pending` resolvido em até 30 s → o estado resolvido; sem resolver → 3, pela R9.1, com relógio falso; `unknown` → 3;
      - recusa do host → resultado `refused`, saída 1 (substitui o teste do `#33115` que esperava erro lançado);
      - `agent_session_operation_unknown` → `unknown`, 3;
      - o `call` do `send` rejeita com `RuntimeClientError('runtime_timeout')` → `unknown`, 3, com o
        `operation` no resultado;
      - a origem: com `ORCA_AGENT_SESSION_ID` no ambiente, a chamada do `send` sai pelo `client.call` sem mudar os
        parâmetros (a evidência é do D2, conferida no P2); o `envelope.expectedRuntimeFence` é o `fence` do `tail`.
- [x] **2. Implementar** — `src/cli/brza/chat-send-outcome.ts`, `src/cli/brza/chat-queue-hold.ts`, o `history tail`
      depois de `queued`, o `process.exitCode` depois do `printResult`, o spec e as linhas do guia (D6).
- [x] **3. Rodar e ver passar** —
      `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts src/cli/handlers/chat.test.ts src/cli/brza/chat-send-outcome.test.ts src/cli/brza/chat-queue-hold.test.ts --maxWorkers=2`;
      `pnpm verify:bundled-skill-guides`; `pnpm tc:cli`; `pnpm check:changed --base=origin/master --maxWorkers=2`.
- [x] **4. Commit** — `feat(cli): chat send diz o estado da entrega, o motivo da fila e sai pelo código do estado`.
- [x] **5. Revisão independente** — a sessão Grok, `reviewer` (R19.2), com `ref: PLN-011/P4`, revisa o commit
      contra o D e a Cobertura; o parecer vai a `work/reviews/` (`brza note review-open`), e cada achado tem destino
      antes do passo seguinte.

**Evidência:** `brza-studio@55225f8cb878`, `ed5bf0283e1`, `a243520d41f` e `0de38e7d082` · 79 testes do alvo,
62 de regressão terminal; guias, tc:cli, lint e hooks aprovados; `pnpm check:changed --base=origin/master
--maxWorkers=2 --force` → 22/22 · REV-011 aprovada. Inclui os dois achados corrigidos e o complemento R20 (X5).

#### P5 — `chat send --operation`

Executa D5, D6 · executor: worker `implementer` em Codex (R18.1), no worktree do `brza-studio`

Estimado: 2 h · Executado: — h, com a revisão

- [ ] **1. Testes que falham** — em `src/cli/handlers/chat.test.ts`:
      - com `--operation <id>`, o `envelope.clientOperationId` é o id dado e o `payloadFingerprint` é igual ao da
        primeira tentativa com o mesmo texto (os dois montados pela mesma chamada, e comparados);
      - o mesmo id com `replayed: true` e o valor gravado → o estado do valor, sem segundo `send` (uma só chamada
        `agentSession.send` no mock);
      - id malformado → `invalid_argument`, nenhuma chamada ao host;
      - recusa `operationIdReused` → `refused`, 1;
      - replay que responde `agent_session_operation_unknown` → `unknown`, 3, nas duas tentativas;
      - sem a flag, o `operation` impresso casa com o regex do gerador.
- [ ] **2. Implementar** — `src/cli/brza/chat-operation-id.ts` (o regex e o parse), a flag no spec e no handler, a nota
      do limite do `delivery` (D5) no spec e a linha do guia (D6).
- [ ] **3. Rodar e ver passar** —
      `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts src/cli/handlers/chat.test.ts src/cli/brza/chat-operation-id.test.ts --maxWorkers=2`;
      `pnpm verify:bundled-skill-guides`; `pnpm tc:cli`; `pnpm check:changed --base=origin/master --maxWorkers=2`.
- [ ] **4. Commit** — `feat(cli): chat send --operation repete o envio sem reenviar`.
- [ ] **5. Revisão independente** — a sessão Grok, `reviewer` (R19.2), com `ref: PLN-011/P5`, revisa o commit
      contra o D e a Cobertura; o parecer vai a `work/reviews/` (`brza note review-open`), e cada achado tem destino
      antes do passo seguinte.

**Evidência:** `brza-studio@<sha>` · os comandos acima → N passed · REV-NNN

#### P6 — O caso manual C1 no app de dev

Executa D2, D3, D4, D5 · executor: Anderson

Estimado: 0,5 h · Executado: — h — o preço que a R6.4 deu, "cerca de 30 min de Anderson".

- [ ] **1. Subir o app de dev e a CLI** — no worktree: `pnpm dev`, e em outro terminal `pnpm run build:cli`; a CLI de
      dev é `pnpm orca-dev …`, que aponta o perfil do `pnpm dev` deste worktree (`config/scripts/orca-dev.mjs`).
- [ ] **2. Rodar o caso manual C1** da tabela abaixo e preencher Observado e veredito, com o print pelo
      `brza print plans/PLN-011-chats-pela-cli-e-plugins/PLN-011-C1.png --app`.

#### P7 — O merge da fase 1 na `master` do `brza-studio`

Executa D1 a D6 · executor: a sessão coordenadora

Estimado: 1 h · Executado: — h

- [ ] **1. Suíte inteira, uma vez** — no worktree, `pnpm test --maxWorkers=2`, sozinha na máquina, comparada à linha de
      base da `master`.
- [ ] **2. Merge** — `feat/pln-011-chat-cli` na `master`, com o push; o `brza install` da CLI, se a CLI instalada vem do
      checkout.
- [ ] **3. Fechar a issue da fase** — `brza-chat-list-read-send-no-studio` a `done`, com `completed` e a linha do
      merge.

**Evidência:** `brza-studio@<sha do merge>` · a suíte → N passed, a mesma base de falhas da `master`

### Fase 2 — navegação

Branch `feat/pln-011-chat-nav`, worktree `~/Projects/brza-studio/.worktrees/pln-011-chat-nav`, nascido da `master` com
a fase 1.

#### P8 — `brza chat focus` pelo `terminal.reveal`

Executa D7 · executor: worker `implementer` em Codex (R18.1), no worktree do `brza-studio`

Estimado: 2,5 h · Executado: — h, com a revisão

- [ ] **1. Testes que falham** — o roteamento do `ui:revealTerminalPane` com o `tabId` de um chat ativa a aba
      `agent-session` e confirma; com o de terminal, o caminho de hoje; com aba inexistente, não confirma. Na CLI,
      `chat focus` resolve a sessão e chama `terminal.reveal` com o `tabId` do chat; chat inexistente sai 1.
- [ ] **2. Implementar** — o ramo do D7 no renderer, o `chat focus` no handler, no spec e no guia.
- [ ] **3. Rodar e ver passar** — os arquivos de teste tocados, pelo `node config/scripts/run-vitest.mjs run --config
      config/vitest.config.ts <arquivos> --maxWorkers=2`; `pnpm tc:cli`; `pnpm check:changed --base=origin/master
      --maxWorkers=2`.
- [ ] **4. Commit** — `feat(chat): brza chat focus abre o chat pelo terminal.reveal`.
- [ ] **5. Revisão independente** — a sessão Grok, `reviewer` (R19.2), `ref: PLN-011/P8`, parecer em `work/reviews/`.

**Evidência:** `brza-studio@<sha>` · os comandos acima → N passed · REV-NNN

#### P9 — A barra lateral segue a aba ativa

Executa D8 · executor: worker `implementer` em Codex (R18.1), no worktree do `brza-studio`

Estimado: 2,5 h · Executado: — h, com a revisão

- [ ] **1. Testes que falham** — a seleção da barra lateral muda quando a aba ativa passa a um chat por runtime, por
      atalho e por notificação; o destaque por workspace vale para `agent-session` e segue valendo para `terminal`.
- [ ] **2. Implementar** — o D8: a seleção derivada da aba ativa e o `focused-agent-row-highlight.ts` com
      `agent-session`.
- [ ] **3. Rodar e ver passar** — os testes tocados e `pnpm check:changed --base=origin/master --maxWorkers=2`.
- [ ] **4. Commit** — `fix(sidebar): a seleção de agentes segue o chat ativo`.
- [ ] **5. Revisão independente** — a sessão Grok, `reviewer` (R19.2), `ref: PLN-011/P9`, parecer em `work/reviews/`.

**Evidência:** `brza-studio@<sha>` · os comandos acima → N passed · REV-NNN

#### P10 — Native Chats na Jump Palette

Executa D9 · executor: worker `implementer` em Codex (R18.1), no worktree do `brza-studio`

Estimado: 3 h · Executado: — h, com a revisão

- [ ] **1. Testes que falham** — o builder inclui a aba `agent-session` nas recentes e a acha pelo título; a ativação
      abre o chat, e não um arquivo.
- [ ] **2. Implementar** — o D9.
- [ ] **3. Rodar e ver passar** — os testes tocados e `pnpm check:changed --base=origin/master --maxWorkers=2`.
- [ ] **4. Commit** — `fix(palette): a Jump Palette lista e acha os Native Chats`.
- [ ] **5. Revisão independente** — a sessão Grok, `reviewer` (R19.2), `ref: PLN-011/P10`, parecer em `work/reviews/`.

**Evidência:** `brza-studio@<sha>` · os comandos acima → N passed · REV-NNN

#### P11 — O caso manual C2 no app de dev

Executa D7, D8, D9 · executor: Anderson

Estimado: 0,5 h · Executado: — h — o preço que a R10.4 deu, "~20 min de Anderson no app".

- [ ] **1. Rodar o C2** da tabela de Casos manuais, com o print pelo `brza print
      plans/PLN-011-chats-pela-cli-e-plugins/PLN-011-C2.png --app`.

#### P12 — O merge da fase 2

Executa D7 a D9 · executor: a sessão coordenadora

Estimado: 1 h · Executado: — h

- [ ] **1. Suíte inteira, uma vez**, como no P7.
- [ ] **2. Merge** na `master`, com o push.
- [ ] **3. Fechar a issue** `chat-ativo-pela-cli-na-barra-lateral-e-na-jump-palette`.

**Evidência:** `brza-studio@<sha do merge>` · a suíte → N passed

### Fase 4 — plugins

Branch `feat/pln-011-plugin-chats`, worktree `~/Projects/brza-studio/.worktrees/pln-011-plugin-chats`.

#### P13 — A conferência no app: o chat já aparece em `agents.list`?

Executa D10 · executor: worker `implementer` em Codex (R18.1)

Estimado: 1 h · Executado: — h

- [ ] **1. Teste de projeção** — um teste de unidade de `plugin-workspace-projection.ts` com um snapshot do hook server
      que traz a linha de um chat estruturado; registra se a linha sai em `agents.list` e com que campos.
- [ ] **2. Registrar** — o resultado vai ao `## Desvios` como fato, e decide se o P14 inclui a linha ou só os campos.

**Evidência:** o teste e o resultado, em `arquivo:linha`

#### P14 — Os campos opcionais do chat

Executa D10 · executor: worker `implementer` em Codex (R18.1), no worktree do `brza-studio`

Estimado: 3,5 h · Executado: — h, com a revisão

- [ ] **1. Testes que falham** — a linha do chat em `agents.list` traz `kind: 'chat'`, `sessionId`, `model` e
      `providerSessionId`; a de terminal traz `kind: 'terminal'` e os campos de hoje; o `agent.status.changed` do chat
      traz os mesmos; `workspace.readContext` continua sem `path` (R11.2); o schema público só cresce.
- [ ] **2. Implementar** — o D10, o schema em `plugin-host-api-panel-methods.ts` e no evento, e a doc em
      `docs/reference/plugin-host-api.md`.
- [ ] **3. Rodar e ver passar** — os testes de `src/main/plugins` e `src/shared/plugins` tocados, e `pnpm check:changed
      --base=origin/master --maxWorkers=2`.
- [ ] **4. Commit** — `feat(plugins): os chats nativos em agents.list e agent.status.changed`.
- [ ] **5. Revisão independente** — a sessão Grok, `reviewer` (R19.2), `ref: PLN-011/P14`, parecer em `work/reviews/`.

**Evidência:** `brza-studio@<sha>` · os comandos acima → N passed · REV-NNN

#### P15 — O merge da fase 4

Executa D10 · executor: a sessão coordenadora

Estimado: 1 h · Executado: — h

- [ ] **1. Suíte inteira, uma vez**; **2. Merge** na `master`; **3. Fechar a issue** `native-chat-na-api-de-plugins`.

**Evidência:** `brza-studio@<sha do merge>` · a suíte → N passed

### Fase 5 — `account usage`

Branch `feat/pln-011-account-usage`, worktree `~/Projects/brza-studio/.worktrees/pln-011-account-usage`.

#### P16 — O porte do `#37467`

Executa D11 · executor: worker `implementer` em Codex (R18.1), no worktree do `brza-studio`

Estimado: 1,5 h · Executado: — h, com a revisão

- [ ] **1. Aplicar** — `gh pr diff 37467 -R stablyai/orca | git apply --3way`, com a cabeça conferida pelo
      `gh pr view 37467 -R stablyai/orca --json headRefOid`; o conflito de `src/cli/root-help-text-primary.ts` fica com
      "BrzA Studio host", e as strings "Orca host/runtime" do PR passam a "BrzA Studio".
- [ ] **2. Rodar e ver passar** — `src/cli/handlers/account-usage-command.test.ts` e
      `src/cli/handlers/account-usage-format.test.ts`, com as expectativas de texto acertadas ao rebrand; `pnpm tc:cli`.
- [ ] **3. Commit** — `feat(cli): porta account usage do stablyai/orca#37467`, com o trailer `Upstream:`.
- [ ] **4. Revisão independente** — a sessão Grok, `reviewer` (R19.2), `ref: PLN-011/P16`, parecer em `work/reviews/`.

**Evidência:** `brza-studio@<sha>` · os comandos acima → N passed · REV-NNN

#### P17 — O merge da fase 5 e o fechamento

Executa D11 · executor: a sessão coordenadora

Estimado: 1 h · Executado: — h

- [ ] **1. Suíte inteira, uma vez**; **2. Merge** na `master`; **3. Fechar a issue** `brza-account-usage-na-cli`.
- [ ] **4. Fechar o plano**, pela `references/close.md` da `plan-runner`.

**Evidência:** `brza-studio@<sha do merge>` · a suíte → N passed

## Casos manuais

| ID  | Critério | Passos | Esperado | Observado | Veredito |
| :-- | :------- | :----- | :------- | :-------- | :------- |
| C1  | R2.1, R2.2, R5.4, R6.1, R6.2, R6.3: o coordenador lê por cursor, envia, vê a fila retida e a origem | No app de dev, dois chats Claude: A (coordenador) e B (alvo). 1) `pnpm orca-dev chat list --json` e anote o `session` dos dois. 2) Em B, peça uma tarefa longa (ex.: "liste os arquivos de src/cli um a um, devagar"). 3) `ORCA_AGENT_SESSION_ID=<A> pnpm orca-dev chat send --session <B> --text "pare e resuma" --json; echo "saída $?"`. 4) Em B, peça uma pergunta com opções e deixe sem responder; repita o passo 3. 5) `pnpm orca-dev chat read --session <B> --json`, anote o `nextCursor`; responda a pergunta em B; `pnpm orca-dev chat read --session <B> --cursor <nextCursor> --json`. 6) Repita o passo 3 com `--operation <operation do passo 4>`. | 3) `delivery: queued`, `held_by: working`, saída 0. 4) `held_by: question`, saída 0. Em B, a mensagem aparece como tarefa de A, não como de pessoa. 5) só as entradas depois do cursor, com a resposta e a nova revisão da pergunta (`pending: false`), `hasNewer` e `nextCursor`. 6) `replayed: true`, saída 0, e nenhuma mensagem nova em B. | | |
| C2  | R10.2, R10.3, R10.4: o `focus`, a barra lateral e a Jump Palette seguem o chat | No app de dev, dois chats e um terminal. 1) Com outra janela na frente, `pnpm orca-dev chat focus --session <B>`. 2) Troque para o chat A pelo atalho de aba e depois pela notificação de B. 3) Na Jump Palette, busque o título de B e abra. | 1) o app vem à frente com B ativo. 2) a barra lateral destaca o chat da tela a cada troca. 3) B aparece nas recentes e na busca, e abre como chat. | | |

## Regressão

- **`worktree ps` não muda.** O `chat list` só lê a resposta dele. Como se confere: `src/cli/worktree-ps-*.test.ts` e
  `src/cli/handler-group-manifest.test.ts`, no P1.
- **`terminal read` e `terminal send` não mudam**, nem o código de saída do `terminal send`. Como se confere:
  `src/cli/handlers/terminal.test.ts`, `src/cli/terminal-read-screen.test.ts`, `src/cli/index-terminal-commands.test.ts`,
  no P2 e no P4.
- **O `agent.launch` e o `agent.launchReplay` levam a mesma evidência, e nada mais a leva.** Como se confere: os três
  casos de `src/cli/runtime/client-execution-host.test.ts:134-161`, no P2.
- **O código de saída dos outros comandos fica 1 no erro, e o do `plugin` fica o dele** (`src/cli/cli-exit-code.ts`):
  o D3 e o D4 põem o `process.exitCode` dentro do handler, sem tocar o `cliErrorExitCode`.
- **O envio do próprio chat segue como de pessoa** (`userSend`) (F8): um teste do P4 com
  `ORCA_AGENT_SESSION_ID` igual ao `--session` não muda os parâmetros; a regra é do host e não muda.

## Desvios

- **X1 — A fase 1 nasce da `origin/master` `50333c6ffd5`, e não da `8f41dd56a33`.** A `master` local estava um commit
  atrás (o tema BrzA Dark, PLN-007), sem relação com a CLI; afeta P1.
- **X2 — O lint do porte num commit nosso.** O `check:changed` falha no `src/cli/handlers/chat.test.ts:78` do próprio
  `#33115` (`consistent-type-assertions`); o porte fica intacto em `brza-studio@f633ec3e307`, e o guard vai em
  `brza-studio@df8adc29574`; afeta P1 e D1.
- **X3 — O cursor é `--cursor`, e não `--since`.** A R13.4, às cegas, reabriu a R8.4 só no nome do cursor; o D3, o D6, o
  P3, a Cobertura e o C1 foram reescritos. O PLN-010 do `tools-kit` chama `brza chat read --cursor`.
- **X4 — Do P3 em diante, os workers saem do `brza-mcp`.** A cota da Claude reteve o P3 (pedido 7); pela R18.1, Codex
  implementa e Antigravity revisa. O pedido 7 foi cancelado no SQLite da fila, sem ferramenta para isso, o que virou
  a issue `o-mcp-nao-cancela-pedido-na-fila` do `tools-kit`; afeta P3 a P16.

- **X5 — Transporte das releituras após o envio (P4).** O Grok apontou a lacuna não definida em D4; a R20, respondida
  pelo agy às cegas, preserva polls pending até o teto original de 30 s e recibos queued com metadados indisponíveis
  explícitos. D4/D6 complementados; implementação e revisão seguem no P4.

## Worklogs

- 2026-11-03 — abertura: as cinco issues das frentes, o PLN-011 com as fases e as R1 a R4 do `playground`; R5 e
  R6 fecham a entrevista da fase 1, e o `#37774` sai dela; R7 com Anderson e R8 a R11 pelo `agy`; Desenho e P1 a P17
  gravados, o `brza-mcp` de pé e a R12 refaz a R7.3. Parou antes do P1, com a coordenadora aberta.
  [PLN-011: abertura do plano dos chats pela CLI e pelos plugins](../../work/worklogs/2026-11-03-pln-011-abertura-chats-pela-cli-e-plugins.md)
- 2026-11-03 — execução: o P1 e o P2 fecham pelo `brza-mcp` (X1, X2, REV-007, REV-008); as R13 a R16 às cegas, com
  a R13.4 em acordo na volta 1 (X3); a R17 manda o A2 da REV-008 a uma issue; a R18 e a R19 passam os workers a Codex
  e a revisão à sessão Grok (X4); o P3 commitado e revisado, com os achados do Grok por corrigir; a coordenação passa
  a uma sessão Codex.
  [PLN-011: execução dos passos pela sessão coordenadora](../../work/worklogs/2026-11-03-pln-011-execucao.md)
- 2026-11-03 — coordenação em Codex: P3 corrigido e fechado em `a7099022850`, com REV-009 aprovada; próximo P4.
  [PLN-011: execução dos passos pela sessão coordenadora](../../work/worklogs/2026-11-03-pln-011-execucao.md)

- 2026-11-04 — P4 com cobertura complementar em `ed5bf0283e1`, corrigindo a pausa da fila; revisão pedida ao Grok.
  [PLN-011: cobertura e revisão do P4](../../work/worklogs/2026-11-04-pln-011-execucao.md)

- 2026-11-04 — P4 fechado em `0de38e7d082` com REV-011, incluindo R20; próximo P5.
  [PLN-011: cobertura e revisão do P4](../../work/worklogs/2026-11-04-pln-011-execucao.md)

## Revisões

- [REV-007: o P1 do PLN-011, o porte do `#33115`](../../work/reviews/REV-007-pln-011-p1-porte-33115.md) — aprova; A1
  (a contagem de testes do D1) corrigido aqui.
- [REV-008: o P2 do PLN-011, a origem do coordenador no `agentSession.send`](../../work/reviews/REV-008-pln-011-p2-origem-do-coordenador.md)
  — aprova; A1 (a cobertura do WSL e do pareado) corrigido em `brza-studio@594c4a7e13c`; A2 vai à issue, pela R17.1.
- [REV-009: P3 do PLN-011, `chat read` com cursor, ids e reset](../../work/reviews/REV-009-pln-011-p3-chat-read-cursor.md)
  — aprova; A1–A3 da revisão inicial corrigidos em `brza-studio@a7099022850`.

- [REV-011: P4 do PLN-011, estados e fila do `chat send`](../../work/reviews/REV-011-pln-011-p4-chat-send.md)
  — aprova; A1/A2 corrigidos em `a243520d41f`, lacuna de transporte resolvida na R20 e em `0de38e7d082`.

## Pendências conhecidas

- [O `--session` do `brza chat` recusa o endereço `orca_session_id:<id>`](../../work/issues/chat-session-recusa-o-endereco-orca-session-id.md)
  — o A2 da REV-008, com gatilho (R17.1).

## Fechamento

- [ ] Todo passo `[x]` com evidência, ou `[-]` com motivo.
- [ ] Todo achado com destino que existe.
- [ ] Um resumo por commit ou PR do `brza-studio` da entrega, com o link do plano: os achados e o destino de cada um.
- [ ] O durável saiu para a casa dona e está em `## Decisões` e `## Documentação`.
- [ ] As decisões que o plano respondeu estão `done`, citando a rodada.
- [ ] As issues das fases 1, 2, 4 e 5 estão `done`, com `completed`.
- [ ] `status: done`, `phase: closed` e `completed` no frontmatter.
