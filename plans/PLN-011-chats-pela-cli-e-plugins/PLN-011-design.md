# PLN-011 — Desenho

O Desenho do [PLN-011: Os chats do BrzA Studio se coordenam pela CLI, aparecem na navegação e chegam aos plugins](PLN-011-plan.md).
A fase 1 (D1 a D6) saiu do rascunho de um `designer`, conferido no `brza-studio@8f41dd56a33`, com as respostas da R8 e
da R9 aplicadas; as fases 2, 4 e 5 (D7 a D11), do levantamento de um `collector` e das respostas da R10 e da R11. As
marcas `[F… · lido · …]` são a evidência do levantamento de cada fato. A fase 3 saiu do plano em R11.4.

## Fase 1 — coordenação

### O que este desenho assume

- **R5.1:** o `#37774` fica fora da fase 1.
- **R5.2:** o porte do `stablyai/orca#33115` vai num commit separado; cursor, recibo e motivo da fila vêm depois.
- **R5.3:** cursor inválido sai com código não zero e `cursor_reset: <motivo>`, com a página `tail` e o `nextCursor` novos.
- **R5.4:** depois de `queued`, um `history tail`; o JSON traz a posição, o `nextQueuedMessageId` e `held_by: question|working`.
- **R6.1:** `send` sai 0 em `accepted` e `queued`, 1 em recusa e `rejected`, 3 em `pending` e `unknown`; o JSON traz sempre
  `delivery` e `submission.state`.
- **R6.2:** o id da operação faz replay sem reenvio, e o `send` o imprime; o nome da flag e do campo vem da R13.4.
- **R6.3:** cursor opaco `epoch:sequence`; `--json` com `itemId`, `revision`, `sequence`, `nextCursor`, `hasNewer`; origem do
  coordenador pelo `ORCA_AGENT_SESSION_ID`; `expectedRuntimeFence` lido do histórico antes do envio.
- **R6.4:** prova por `chat.test.ts`, teste do `client.ts` e o caso manual C1.
- **R8.1:** `cursor_reset` sai 2. **R8.2:** o reset repetido se aceita e se documenta. **R8.3:** `--cursor` lê uma
  página `after` de 200 linhas, recusa `--limit` e traz `removedItemIds`. **R13.4**, que reabre a R8.4 só no nome
  do cursor: as flags são `--cursor` e `--operation`, e o recibo traz `operation`.
- **R13 a R16** refazem as R8 a R11 às cegas e confirmam todas as outras escolhas.
- **R9.1:** o `pending` se espera até 30 s, relendo o `tail` a cada 500 ms. **R9.2:** `held_by: question | working |
  null`, com `queuePaused: true` na pausa. **R9.3:** o replay `returned` ou `withdrawn` sai 1, `rejected`. **R9.4:** a
  extensão mora em `src/cli/brza/`.

### Terreno (só o que este rascunho acrescenta ao `pln011-fase1-terreno.md`)

#### O porte

- O `#33115` segue aberto, com a cabeça em `a007c29e248` e a última atualização em 2026-11-02; o `gh pr diff` de agora é
  idêntico ao `pr33115.diff` do scratch. [F1 · rodado · 95]
- O `git apply --cached --3way` do diff num índice temporário sobre `8f41dd56a33` aplica os 11 arquivos, +761/−4, sem
  conflito. [F2 · rodado · 95]
- O texto de ajuda do fork continua com `orca`, e a exibição troca por `brza`: `src/cli/brza/cli-display-name.ts:1-6`. O
  porte não precisa de rebrand. [F3 · lido · 92]
- O `src/cli/bundled-skill-guides.ts` é gerado de `skill-guides/*.md`; `pnpm verify:bundled-skill-guides` confere e
  `pnpm generate:bundled-skill-guides` regrava (`package.json:89-90`). [F4 · lido · 95]
- O código só do fork mora em pastas `brza/` (`src/cli/brza`, `src/main/runtime/rpc/brza`, `src/shared/native-chat/brza`
  e outras seis). [F5 · rodado · 95]

#### A origem do coordenador

- A CLI só manda a evidência do chat chamador em `agent.launch` e `agent.launchReplay`
  (`src/cli/runtime/client.ts:58`), e só quando não é remota e há evidência (`client.ts:140-142`). [F6 · lido · 95]
- A evidência sai do `ORCA_AGENT_SESSION_ID` e some quando o ambiente traz `host` (WSL):
  `src/cli/runtime/orchestration-compatibility-envelope.ts:20-28`. [F7 · lido · 95]
- No host, o `send` vira tarefa do chat chamador (`body.from = chatTaskSource(...)`) quando o chamador é a CLI local e o
  chat chamador é outro; o envio do próprio chat segue como de pessoa (`userSend`):
  `src/main/runtime/rpc/methods/structured-agent-session-send-compatibility.ts:21-34` e `caller-chat-sender.ts:11-18`. [F8 · lido · 95]
- O teste de hoje da evidência é `src/cli/runtime/client-execution-host.test.ts:134-141`, que já confere que
  `terminal.list` não leva nada. [F9 · lido · 95]

#### O estado do envio

- Os estados da submissão são `pending`, `accepted`, `rejected` e `unknown`
  (`src/shared/agent-session/journal/agent-session-journal-types.ts:396`). [F10 · lido · 95]
- O resultado do `send` é `{ clientMessageId, submission }` ou `{ clientMessageId, queued: { messageId, position, state } }`,
  e o `state` do recibo da fila é `waiting | dispatched | returned | withdrawn`, os três últimos só em replay
  (`src/shared/agent-session/agent-session-wire.ts:317-326`). [F11 · lido · 95]
- O envelope do resultado traz `replayed`, `fence` e `cursor`, ou `{ ok: false, refusal }` (`agent-session-wire.ts:292-301`). [F12 · lido · 95]
- **Para a CLI local, o host responde na admissão, sem esperar a entrega ao provedor:** o
  `sendStructuredAgentSessionForClient` devolve o resultado direto quando `context.clientKind === undefined`
  (`structured-agent-session-send-compatibility.ts:36-44`), e a CLI local não declara `clientKind`
  (`rpc-caller-identity.ts:36`). [F13 · lido · 92]
- O cliente que não espera recebe `dispatchState: 'pending'` antes do handover
  (`src/main/runtime/rpc/methods/structured-agent-session-legacy-command-wait.test.ts:85-90`). [F14 · lido · 90]
- Daí, o envio da CLI a um chat parado deve voltar `pending` no caso comum, e não `accepted`; não rodei no app. [F15 · inferido · 70]
- O host atual ignora o `expectedRuntimeFence`, e o mais velho ainda confere
  (`src/shared/agent-session/lifecycle/agent-session-mutation-envelope.ts:66`). [F16 · lido · 95]
- A CLI não trata `agentSession.send` como mutação durável, e por isso o timeout dele não ganha recuperação
  (`src/shared/orchestration-rpc-contract.ts:84-86`). O timeout de transporte sai como `runtime_timeout`
  (`src/cli/runtime/transport.ts:60-64`). [F17 · lido · 90]

#### O replay

- O `payloadFingerprint` do `send` cobre o `sessionId`, o corpo sem o `from` e os campos de controle (`delivery`,
  `options`, `selection`), e não cobre o `expectedRuntimeFence`
  (`src/shared/agent-session/requests/structured-agent-session-send-mutation.ts:40-44,65-88`). [F18 · lido · 93]
- O corpo guarda o texto com `trimEnd()` (`structured-agent-session-send-mutation.ts:113`). [F19 · lido · 95]
- O `clientOperationId` tem a forma `<13 dígitos de ms>-<32 hex>`
  (`src/shared/agent-session/lifecycle/structured-agent-session-mutation.ts:73-83`). [F20 · lido · 95]
- O ledger responde pelo par (chamador, id): mesmo fingerprint, replay; outro, `agent_session_operation_conflict` com
  `operationIdReused`; id nunca visto com mais de 24 h, `agent_session_operation_expired`
  (`src/shared/agent-session/lifecycle/agent-session-operation-ledger.ts:209-222`;
  `agent-session-host-authority.ts:35`). [F21 · lido · 93]
- A chave do chamador da CLI local é uma só, `trusted-local:runtime`, para qualquer processo
  (`src/main/runtime/rpc/rpc-caller-identity.ts:40-43`). [F22 · lido · 92]
- O replay de desfecho desconhecido devolve a recusa `agent_session_operation_unknown`, sem rodar de novo
  (`src/main/native-chat/agent-session-wire/structured-agent-session-replay-outcome.ts:17-23,45-54`). [F23 · lido · 93]

#### O cursor

- A página traz `epoch`, `fence`, `window.{oldest,newest,nextCursor}`, `liveCursor`, `hasNewer`, `removedItemIds`,
  `queuedMessages`, `queuePause`, `nextQueuedMessageId` (`agent-session-wire.ts:75-115`) e `actionablePromptIds` e
  `working` (`src/shared/agent-session/requests/agent-session-current-work-wire.ts:3-8`). [F24 · lido · 95]
- Na página `tail` e na do reset, o `window.nextCursor` aponta o item mais velho, para paginar para trás
  (`src/main/native-chat/agent-session-wire/agent-session-history-page.ts:127,177-179`); a cabeça do journal está no
  `liveCursor` (`agent-session-history-page.ts:321`). [F25 · lido · 92]
- Na página `after`, o `window.nextCursor` é a última sequência lida (`agent-session-history-page.ts:285`). [F26 · lido · 92]
- O `epoch` é um identificador qualquer, não vazio e sem espaço nas pontas
  (`src/shared/rpc-contract/structured-agent-session-identifiers.ts:12-24`); o parse do `epoch:sequence` corta no
  último `:`. [F27 · lido · 92]
- O `after` devolve `cursor_compacted` sempre que o cursor está no epoch atual e a visão tem `normalizationKey`
  não vazio, salvo com `rowReplay` (`agent-session-history-page.ts:87-95`). [F28 · lido · 92]
- Para a CLI local, o RPC passa `replaceNormalizedHistory = true`, e daí `rowReplay = false`
  (`src/main/runtime/rpc/methods/structured-agent-session.ts:204-208`; `structured-agent-session-history-capability.ts`;
  `structured-agent-session-current-requests.ts:7-13`; `structured-agent-session-history-result.ts:37`). [F29 · lido · 90]
- O `normalizationKey` fica não vazio quando há um hand-off da fila em dúvida, gravado por `foldQueuedHandOffInDoubt`
  (`src/main/native-chat/agent-session-journal/journal-public-read.ts:54-62`; `journal-submission-fold.ts:78-82`). [F30 · lido · 90]
- O `HistoryParams` é `strict` e aceita `limit` até 200 (`src/shared/rpc-contract/structured-agent-session-params.ts:319-326`;
  `agent-session-wire.ts:51`). [F39 · lido · 95]
- Daí, na sessão que teve um hand-off da fila em dúvida, todo `chat read --cursor` volta `cursor_compacted` até o
  epoch mudar; não medi quantas sessões têm isso. [F31 · inferido · 75]

#### A fila

- O host retém a fila por `blocked`, `prompt` ou `working`, e `prompt` vence `working`
  (`src/main/native-chat/agent-session-wire/structured-agent-session-queued-messages.ts:42-58`). [F32 · lido · 95]
- A pausa da fila publicada é só `{ reason: 'stopped' }`
  (`src/shared/agent-session/requests/agent-session-queued-message-wire.ts:12`). [F33 · lido · 95]
- `prompt` cobre aprovação e pergunta: o `actionablePromptIds` lista as duas (`agent-session-current-work-wire.ts:4-5`). [F34 · lido · 90]
- No recibo, `returned` é o envio que falhou e voltou à fila como cartão, e `withdrawn` é o cartão retirado, como no
  `/clear`. A premissa é a leitura de `agent-session-queued-message-wire.ts:47` e
  `src/main/native-chat/agent-session-journal/journal-context-clear.ts:28`, sem teste rodado. [F35 · lido · 85]

#### Os códigos de saída da CLI

- Só o `plugin` tem código próprio; todo erro lançado sai 1 (`src/cli/cli-exit-code.ts:3-13`). [F36 · lido · 95]
- O `terminal send` imprime o resultado e depois põe `process.exitCode = 1` quando não foi aceito
  (`src/cli/handlers/terminal-send.ts:104-110`). É o molde para sair não zero com o JSON no stdout. [F37 · lido · 95]
- O erro com `--json` sai como `{ id, ok: false, error: { code, message, data } }` (`src/cli/cli-error.ts:180-205`). [F38 · lido · 92]

---

### D1 — O porte do `#33115` — `src/cli/handlers/chat.ts` e mais 10 arquivos (P1)

- **Origem:** R5.2
- **Contexto:** a base da fase é o PR do upstream como está, num commit só dele, para que o sync que trouxer o PR
  fundido mostre só a nossa extensão como diferença.

#### Como fica

Os 11 arquivos do diff, sem mudar uma linha: (F2)

| Arquivo | O quê |
| :------ | :---- |
| `src/cli/chat-sessions.ts` (novo) | `parseChatSessionSelector`, `listChatSessions`, `chatTranscript`, `formatChatList`, `formatChatRead` |
| `src/cli/handlers/chat.ts` (novo) | `CHAT_HANDLERS`: `chat list`, `chat read`, `chat send` |
| `src/cli/handlers/chat.test.ts` (novo) | 11 testes (A1 da REV-007) |
| `src/cli/specs/chat.ts` (novo) | `CHAT_COMMAND_SPECS` |
| `src/cli/specs/index.ts` | registra os specs |
| `src/cli/handler-group-manifest.ts` | grupo `chat` |
| `src/cli/root-help-text-primary.ts` | três linhas em "Agents:" |
| `src/main/startup/cli-command-names.ts` | `'chat'` |
| `skill-guides/orca-cli.md` e `src/cli/bundled-skill-guides.ts` | a seção "Chats" e o handoff por `chat send` |
| `docs/site/content/docs/cli/reference.mdx` | a seção "Chats" |

O commit leva o trailer `Upstream: stablyai/orca#33115 @ a007c29e248`. O gerado se confere com
`pnpm verify:bundled-skill-guides` e, se divergir pelo drift de texto, se regrava com
`pnpm generate:bundled-skill-guides`. (F4)

---

### D2 — A origem do coordenador no `agentSession.send` — `src/cli/runtime/client.ts` (P2)

- **Origem:** R6.3
- **Contexto:** o host já lê a evidência no `send` (F8), e a CLI só a manda no `agent.launch` (F6).

#### Como fica

```diff
-// The host records the launched agent in the caller's chat; older hosts ignore the evidence.
-const AGENT_LAUNCH_METHODS: ReadonlySet<string> = new Set(['agent.launch', 'agent.launchReplay'])
+// The host records the launched agent in the caller's chat, and a chat-to-chat send as that chat's
+// task; older hosts ignore the evidence.
+const CALLER_CHAT_METHODS: ReadonlySet<string> = new Set([
+  'agent.launch',
+  'agent.launchReplay',
+  'agentSession.send'
+])
@@
-      : AGENT_LAUNCH_METHODS.has(method) && !this.remote && this.agentLaunchCaller
+      : CALLER_CHAT_METHODS.has(method) && !this.remote && this.agentLaunchCaller
         ? { orchestrationCompatibilityEvidence: this.agentLaunchCaller }
         : {}
```

- **Fica igual:** remoto não manda; WSL não manda (F7); `agentSession.history` e `terminal.*` não mandam.
- **Teste** em `src/cli/runtime/client-execution-host.test.ts`, ao lado do de hoje (F9): `agentSession.send` leva
  `{ agentSessionId: CALLER_CHAT }`; `agentSession.history` não leva; a mesma recusa no WSL e no servidor pareado.
- O nome `agentLaunchCaller` fica: renomear o campo toca mais linhas do upstream sem ganho.

---

### D3 — `chat read` com cursor — `src/cli/handlers/chat.ts`, `src/cli/brza/chat-cursor.ts` (P3)

- **Origem:** R2.1, R5.3, R6.3, R8.1 a R8.3, R13.4
- **Contexto:** o `#33115` só lê `tail` e `before`, e o `--json` dele não traz ids, cursor nem `hasNewer`.

#### Como fica

**Uso** (spec em `src/cli/specs/chat.ts`):

```text
orca chat read --session <id-or-handle> [--limit <n>] [--cursor <epoch:sequence>] [--json]

  --cursor   Reads only what changed after this cursor: new entries and new revisions of
             older ones. Pass the nextCursor of the previous read. Without it, the read
             shows the newest entries and returns the cursor to continue from.
  --limit    Without --cursor: the number of entries shown (default 20, max 100).
             Refused together with --cursor.
Exit codes: 0 read; 2 cursor_reset, the cursor no longer applies and the newest
entries are shown instead; 1 any other failure.
```

**O cursor** (`src/cli/brza/chat-cursor.ts`, novo, pela R9.4):

```ts
import type { AgentJournalCursor } from '../../shared/agent-session-journal-identity'

/** "epoch:sequence"; the epoch may contain ":" so the split is at the last one. */
export function formatChatCursor(cursor: AgentJournalCursor): string
export function parseChatCursor(value: string): AgentJournalCursor // RuntimeClientError('invalid_argument') when malformed
```

O texto malformado (sem `:`, sequência não inteira ou negativa, epoch vazio) é `invalid_argument`, saída 1, sem
página: não é um motivo do host. (F27)

**O JSON** (`result`):

```ts
type ChatReadEntry = ChatTranscriptEntry & {
  itemId: string
  revision: number
  sequence: number
}

type ChatReadResult = {
  session: string
  entries: ChatReadEntry[]
  /** Só no modo --cursor: itens que o host apagou depois do cursor (R8.3). */
  removedItemIds: string[]
  /** O cursor para a próxima leitura: "epoch:sequence". */
  nextCursor: string
  /** Há mais depois desta página; leia de novo com nextCursor. */
  hasNewer: boolean
  /** Presente só quando o host recusou o cursor; entries é a página tail nova. */
  cursor_reset?: 'epoch_changed' | 'cursor_ahead' | 'cursor_compacted' | 'journal_gap' | 'schema_unreadable'
}
```

```json
{
  "session": "codex_8eb631ab_59c5_41e4_8672_01cfe0a6fd5f",
  "entries": [
    { "kind": "message", "role": "assistant", "text": "2 failures.", "itemId": "it-91", "revision": 1, "sequence": 42 },
    { "kind": "approval", "text": "Allow git push?", "pending": false, "itemId": "it-88", "revision": 2, "sequence": 40 }
  ],
  "removedItemIds": [],
  "nextCursor": "ep-7f3a:43",
  "hasNewer": false
}
```

**De onde sai cada campo:**

| Modo | Chamada | `entries` | `nextCursor` | `hasNewer` |
| :--- | :------ | :-------- | :----------- | :--------- |
| sem `--cursor` | `tail` e o laço `before` do `#33115` | as `limit` mais novas | `page.liveCursor` da primeira página `tail` (F25) | `false` |
| `--cursor` | um `after` com `limit: 200`, o teto do `HistoryParams` (F39), pela R8.3 | todas as legíveis da página, sem corte | `page.window.nextCursor` (F26) | `page.hasNewer` |
| reset | a página `tail` que o reset traz | as legíveis da página | `page.liveCursor` (F25) | `false` |

- Sem `liveCursor` (host mais velho), o `nextCursor` cai para o `window.newest`, ou `epoch:0` na página vazia, pela
  compatibilidade entre versões que a norma do `brza-studio` exige (`AGENTS.md:61`).
- **O reset repetido** (F28–F31) se aceita, pela R8.2: o guia diz "reset repetido: leia sem `--cursor`", e um teste
  cobre o reset `cursor_compacted` duas vezes seguidas.
- O laço do `#33115` que troca a janela pelo reset no `before` fica como está: ali o reset não é do cursor de quem chamou.
- **Texto:** as linhas do `formatChatRead`, e no fim `next cursor: <epoch:sequence>`, mais
  `more after this page: run again with --cursor <next>` quando `hasNewer`. No reset, a primeira linha vai ao stderr:
  `cursor_reset: <motivo>: the cursor no longer applies; showing the newest entries`.
- **Saída:** o handler imprime o resultado e põe o `process.exitCode`, como o `terminal send` (F37).

---

### D4 — `chat send` com estado, códigos de saída e fila — `src/cli/handlers/chat.ts`, `src/cli/brza/chat-send-outcome.ts` (P4)

- **Origem:** R2.2, R5.4, R6.1, R6.3
- **Contexto:** o `#33115` devolve `submitted` para tudo que não é fila, lança erro na recusa e não traz o motivo da fila.

#### Como fica

**Uso:**

```text
orca chat send --session <id-or-handle> --text <text> [--operation <id>] [--json]

  Sends the text as your message. While the agent works, hosts with a message queue hold
  it until the turn ends; the result says "queued", where it is in the queue and what
  holds it (held_by: question or working).
  Run from an agent chat, the message is recorded as that chat's task.
Exit codes: 0 accepted or queued; 1 refused or rejected, nothing was delivered;
3 pending or unknown, delivery is uncertain: do not resend, retry with the same
--operation or read the chat.
```

**A ordem do envio:**

1. valida `--text` e `--operation` (D5) sem tocar o host;
2. `getCliStatus`: sem host, `runtime_unavailable`, saída 1, nada enviado (como no `#33115`);
3. `history tail limit 1` → `fence` (R6.3; o host atual ignora (F16), o velho confere);
4. `agentSession.send`, com a evidência do D2;
5. resultado `queued` → mais um `history tail limit 1` para a fila (R5.4);
6. resultado `submission.dispatchState === 'pending'` → relê `history tail limit 1` a cada 500 ms, até 30 s, e procura a
   submissão do `clientMessageId` (R9.1); resolvida, vale a tabela abaixo; no teto, `pending`, saída 3.

**O JSON** (`result`), mantendo os nomes do `#33115` e acrescentando:

```ts
type ChatSendResult = {
  session: string
  /** O clientOperationId do envio, que `--operation` repete (R13.4). */
  operation: string
  /** O host devolveu o desfecho gravado, sem novo envio. */
  replayed: boolean
  delivery: 'submitted' | 'queued' | 'refused' | 'unknown'
  submission: {
    state: 'accepted' | 'pending' | 'rejected' | 'unknown' | 'queued' | 'refused'
    reason: string | null
  }
  clientMessageId: string | null
  /** Só com delivery 'queued'. */
  queuePosition?: number
  nextQueuedMessageId?: string | null
  held_by?: 'question' | 'working' | null // R9.2: null com a fila escoada ou pausada
  /** Só quando a fila está parada pelo Stop (R9.2). */
  queuePaused?: boolean
  refusal?: { code: string; message: string }
}
```

```json
{
  "session": "claude_5d0c…",
  "operation": "1793750400000-3f2a9c0e8b7d4a1f9e6c5b4a3d2e1f00",
  "replayed": false,
  "delivery": "queued",
  "submission": { "state": "queued", "reason": null },
  "clientMessageId": "m-1",
  "queuePosition": 1,
  "nextQueuedMessageId": null,
  "held_by": "question"
}
```

**O estado e o código de saída** (`src/cli/brza/chat-send-outcome.ts`, função pura `chatSendOutcome(result)` →
`{ delivery, submission, exitCode }`):

| O host respondeu | `delivery` | `submission.state` | Saída | Fonte |
| :--------------- | :--------- | :----------------- | :---- | :---- |
| `submission.dispatchState: 'accepted'` | `submitted` | `accepted` | 0 | R6.1 |
| `queued`, recibo `waiting` ou `dispatched` | `queued` | `queued` | 0 | R6.1 (F11) |
| `queued`, recibo `returned` ou `withdrawn` (só replay) | `queued` | `rejected` | 1 | R9.3 |
| `submission.dispatchState: 'rejected'` | `submitted` | `rejected` | 1 | R6.1 |
| `ok: false`, qualquer `refusal` menos a de baixo | `refused` | `refused` | 1 | R6.1 |
| `submission.dispatchState: 'pending'`, depois de 30 s de espera | `submitted` | `pending` | 3 | R6.1, R9.1 (F15) |
| `submission.dispatchState: 'unknown'` | `submitted` | `unknown` | 3 | R6.1 |
| `refusal.code: 'agent_session_operation_unknown'` | `unknown` | `unknown` | 3 | R6.2 (F23) |
| o `agentSession.send` lançou erro sem resposta do host (`runtime_timeout`, socket caído) | `unknown` | `unknown` | 3 | derivado de R6.1 ("entrega incerta") e R6.2 (F17) |
| o host respondeu erro RPC (`RuntimeRpcFailureError`) | erro `ok: false` | — | 1 | o pedido não passou da validação |

- A recusa passa a sair como resultado, não como erro lançado, para que o JSON traga sempre `delivery` e
  `submission.state` (R6.1), no molde do `terminal send` (F37). O teste do `#33115` "reports a host refusal as an
  error" muda para conferir o resultado `refused` e a saída 1.
- No erro de transporte, o resultado impresso traz o `operation` e a linha de texto
  `retry without resending: orca chat send --session <s> --text <t> --operation <id>`.

**O `held_by`** (`src/cli/brza/chat-queue-hold.ts`, função pura sobre a página):

```ts
/** Why the host is holding the queue, as a history page shows it. */
export function chatQueueHold(page: AgentSessionHistoryPage): 'question' | 'working' | null {
  if ((page.actionablePromptIds?.length ?? 0) > 0) return 'question' // approval or question (F34)
  if (page.working === true) return 'working'
  return null
}
```

- A ordem segue o host: `prompt` vence `working` (F32). Sem `actionablePromptIds` (host velho, ou lista acima de 8 KB), cai para
  os itens `approval`/`question` com `resolution.state === 'pending'` da página.
- Com `queuePause: { reason: 'stopped' }` (F33), `held_by: null` e `queuePaused: true`; com a fila escoada, `null` (R9.2).

---

### D5 — `--operation` — `src/cli/handlers/chat.ts`, `src/cli/brza/chat-operation-id.ts` (P5)

- **Origem:** R6.2
- **Contexto:** o retry depois de um timeout precisa reconstruir o mesmo `clientOperationId` e o mesmo
  `payloadFingerprint`, para o ledger responder pelo gravado.

#### Como fica

**Uso:** `--operation <id>` — "Retries a send with the operation a previous send printed. With the same text, the
host answers with the recorded result and nothing is sent again; with different text the send is refused."

**Como reconstrói:**

- Sem a flag, o id nasce como hoje: `createStructuredAgentSessionOperationId(randomUUID)` (F20).
- Com a flag, o texto passa pelo mesmo regex do gerador, `^\d{13}-[0-9a-f]{32}$`; fora dele, `invalid_argument`, saída 1,
  nada enviado. (F20)
- A mutação é a mesma chamada do `#33115`, com o id dado no lugar do novo:
  `structuredAgentSessionMessageSendMutation({ sessionId, clientOperationId, expectedRuntimeFence, body: structuredAgentSessionSendBody(text, []), delivery? })`.
  O fingerprint sai do `sessionId`, do corpo e do `delivery`, e não do fence (F18). Por isso o fence se relê a cada
  tentativa sem mudar o fingerprint.
- **Mesmo texto e mesmo `delivery`**: mesmo fingerprint → o ledger devolve o gravado, `replayed: true`, e a tabela do D4
  vale para o valor gravado (F21). O texto passa por `trimEnd()`, então espaço no fim não muda nada (F19).
- **Texto diferente**: `agent_session_operation_conflict` / `operationIdReused` → `refused`, saída 1, nada enviado (F21).
- **Desfecho desconhecido**: `agent_session_operation_unknown` → `unknown`, saída 3, e o próximo replay responde o mesmo
  (F23). Cumpre "o `unknown` continua `unknown`" (Cobertura, R6.2).
- **Id nunca visto pelo host** (a primeira tentativa não chegou): o ledger admite como envio novo, se o id tiver menos de
  24 h; com mais, `agent_session_operation_expired`, saída 1 (F21).
- **Qualquer processo da CLI local** faz o replay, porque a chave do chamador é uma só (F22); o pareado tem a dele.
- **Limite conhecido:** o `delivery` entra no fingerprint e depende da capacidade do host (F18). Se o host ganhar ou
  perder `queued-messages.v2` entre a tentativa e o retry, o retry sai `operationIdReused`. Fica na nota da flag.

---

### D6 — O texto da ajuda, do guia e da referência — `src/cli/specs/chat.ts`, `skill-guides/orca-cli.md`, `docs/site/content/docs/cli/reference.mdx` (P3, P4, P5)

- **Origem:** R6.1, R6.2, R6.3
- **Contexto:** o guia é o que o agente lê para usar a CLI; o código de saída e o cursor só servem a quem os conhece.

#### Como fica

Acréscimo à seção "Chats" do `skill-guides/orca-cli.md`, em inglês como o resto do guia, e o `bundled-skill-guides.ts`
regravado pelo gerador (F4); cada passo leva a sua linha:

```text
- `chat read --cursor <nextCursor>` returns only what changed since the last read; keep the
  `nextCursor` it returns and read again while `hasNewer` is true. Exit 2 with `cursor_reset`
  means the cursor no longer applies: start over from the entries and `nextCursor` it returns.   (P3)
- `chat send` exits 0 when the message was accepted or queued, 1 when nothing was delivered,
  and 3 when delivery is uncertain. On 3, do not resend: retry with
  `--operation <operation>` or read the chat.                                        (P4, P5)
- A queued message reports `held_by`: `question` (an approval or question is waiting) or
  `working` (the current turn has not ended) or null (the queue drained or was stopped,
  with `queuePaused: true`).                                                                     (P4)
- Repeated `cursor_reset` in the same chat: read without `--cursor` and start over.               (P3)
```

---

---

## Fase 2 — navegação

### Terreno

- **O `terminal.reveal` só aceita chamador local** e traz a janela ao primeiro plano pelo relay
  (`src/main/runtime/rpc/methods/terminal/terminal-lifecycle-methods.ts:209-231`; `src/main/window/terminal-pane-reveal-relay.ts:16-33,81`).
- **No renderer ele força terminal:** `src/renderer/src/lib/reveal-terminal-pane.ts:7-18` chama
  `activateTabAndFocusPane`, que faz `setActiveTabType('terminal')` (`src/renderer/src/lib/activate-tab-and-focus-pane.ts:12-30`);
  com a aba de um chat, nada acontece.
- **O chat já tem ativação:** `src/renderer/src/components/dashboard/reveal-dashboard-agent.ts:11-44` e
  `src/renderer/src/lib/agent-session/structured-agent-session-tab-activation.ts:31-52,76-93`.
- **A barra lateral** guarda a seleção num `useState` que só o clique muda
  (`src/renderer/src/components/sidebar/SidebarAgentsList.tsx:49,74-78`); o destaque por workspace exige
  `activeTabType === 'terminal'` (`src/renderer/src/components/sidebar/focused-agent-row-highlight.ts:21-27`).
- **A Jump Palette** aceita cinco tipos sem `agent-session` (`src/renderer/src/lib/workspace-tab-palette-content-type.ts:4-7`),
  descarta o resto antes dos recentes e da busca (`workspace-tab-palette-entry-builder.ts:178-183`) e ativa todo
  não-terminal como arquivo (`workspace-tab-palette-activation.ts:80-92,139-144`).
- Os arquivos são idênticos ao `upstream/main` `f22231dc295`.

### D7 — `brza chat focus` pelo `terminal.reveal` — `src/renderer/src/lib/reveal-terminal-pane.ts`, `src/cli/handlers/chat.ts` (P8)

- **Origem:** R10.1
- **Contexto:** o `#37801` pede um comando público que abra um chat; o RPC local que traz a janela já existe.

#### Como fica

- **No renderer:** o handler do `ui:revealTerminalPane` ganha um ramo: quando o `tabId` é de `agent-session`
  (`structured-agent-session-<sessionId>`), chama a ativação de `reveal-dashboard-agent.ts` em vez de
  `activateTabAndFocusPane`, e só confirma ao relay quando a aba existe. O RPC, os params e a permissão não mudam.
- **Na CLI:** `brza chat focus --session <id-or-handle>`, que resolve a sessão como o `chat read` e chama
  `terminal.reveal` com o `tabId` do chat. Sai 0 com a aba ativa e a janela na frente; 1 quando o chat não existe ou
  o renderer não confirmou.
- O nome `terminal.reveal` fica, enganoso, para não divergir do upstream.

### D8 — A barra lateral segue a aba ativa — `SidebarAgentsList.tsx`, `focused-agent-row-highlight.ts` (P9)

- **Origem:** R10.2
- **Contexto:** dois estados, o do clique e o da aba ativa, divergem quando a aba muda por runtime, atalho ou
  notificação (`#37801`).

#### Como fica

- O `selectedPaneKey` deixa de ser `useState` e passa a ser derivado do estado da aba ativa: com
  `activeTabType === 'agent-session'`, o paneKey do chat; com `terminal`, o do terminal, como hoje.
- O clique só ativa a aba; a seleção vem da aba.
- O `focused-agent-row-highlight.ts` aceita também `agent-session`.

### D9 — Native Chats na Jump Palette, por título e recentes — `workspace-tab-palette-*.ts` (P10)

- **Origem:** R10.3
- **Contexto:** o `#37807`: os chats não aparecem nas recentes nem na busca.

#### Como fica

- `agent-session` entra no conjunto de `workspace-tab-palette-content-type.ts`.
- O `entry-builder` monta a entrada do chat com o título da aba e o `isCurrentWorkspaceTab`.
- A ativação ganha o ramo do chat, pela mesma ativação do D7, em vez de tratá-lo como arquivo.
- Sem busca no conteúdo do transcript.

---

## Fase 4 — plugins

### Terreno

- **`agents.list` sai do snapshot do hook server** (`src/main/startup/main-process-plugins.ts:235`), onde os chats
  publicam (`src/main/agent-hooks/agent-hook-runtime-deps.ts:29-33`; `src/main/agent-hooks/server/server-ingest-structured.ts:107-126,169`).
  É inferido que o chat já aparece; a lacuna provável é metadado.
- **A forma de hoje** é `{terminalId|null, title|null, agent|null, state, stateStartedAt}`
  (`src/main/plugins/workers/plugin-workspace-projection.ts:74-93`; `src/shared/plugins/workers/plugin-host-api-panel-methods.ts:19-37`);
  o evento é `src/shared/plugins/events/plugin-events.ts:46-70`.
- **A Host API 1 é "frozen", e só cresce** (`docs/reference/plugin-host-api.md:211,214`); o minor é o `max(since)`
  (`src/shared/plugins/workers/plugin-host-api.ts:322-324`).
- **O caminho foi omitido de propósito:** "public projections exclude them"
  (`src/main/plugins/workers/plugin-host-service-bindings.ts:65-71`).

### D10 — Campos opcionais do chat em `agents.list` e `agent.status.changed` (P13, P14)

- **Origem:** R11.1, R11.2
- **Contexto:** o `#37615`: um plugin não distingue o chat do terminal nem vê a sessão e o modelo.

#### Como fica

- **Antes de codar, a conferência no app (P13):** um plugin de teste lista `agents.list` com um chat aberto. Se o
  chat não aparecer, o P14 inclui a linha, e não só os campos.
- **Os campos novos, opcionais**, na linha de `agents.list` e no payload de `agent.status.changed`:
  `kind: 'chat' | 'terminal'`, `sessionId`, `model` e `providerSessionId`. Nenhum campo existente muda, e o minor não
  sobe; a doc da Host API ganha os campos.
- **Sem caminho**, pela R11.2: `workspace.readContext` continua sem `path`, e o chat não ganha `cwd` nem
  `transcriptPath`. Volta depois da sandbox do worker, por permissão.

---

## Fase 5 — `account usage`

### D11 — O porte do `#37467` — `src/cli/handlers/account-usage-*.ts` e mais 10 arquivos (P16)

- **Origem:** R11.3
- **Contexto:** o PR aplica com 11 de 12 arquivos limpos; o conflito é o texto do rebrand em
  `src/cli/root-help-text-primary.ts:26-28`, e nada falta no fork (`src/main/runtime/rpc/methods/accounts.ts:131-141`).

#### Como fica

- O diff do `#37467` como está, com o conflito resolvido mantendo "BrzA Studio host" e as strings "Orca host/runtime"
  do PR trocadas por "BrzA Studio", num commit com o trailer `Upstream: stablyai/orca#37467 @ <cabeça>`.
