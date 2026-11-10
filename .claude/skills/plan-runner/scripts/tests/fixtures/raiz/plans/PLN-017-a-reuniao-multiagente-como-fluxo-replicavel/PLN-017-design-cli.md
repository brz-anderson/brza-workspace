# PLN-017 — Desenho: as primitivas do `brza sessions` (D2)

## D2 — O `brza sessions` para a reunião — `brza-workflow/packages/client/bin/brza-sessions` e `scripts/brza/brza-shot`

Consultor: o papel `designer`, 2026-11-08. Marcas `[Fn|Cn · tipo · confiança]`;
`BW` = `~/Projects/brza-workflow`, `BS` = `~/Projects/brza-studio`, `WS` = `~/Projects/brza-workspace`.
O que está marcado **[ponto para rodada]** é escolha sem lastro, que vai à rodada antes de virar texto do plano.

- **Origem:** R1.2 ("brza sessions primeiro"), com R1.3 (o painel lê os dados do CLI) e R1.4 (a narração diz quem
  respondeu e quem falta, na hora).
- **Contexto:** a reunião rodou com um `launch.py` que remenda o `brza sessions` por monkeypatch [F5 · lido · 98], com
  `sent: true` sem recibo [F6 · lido · 98] e o fim de rodada por `grep` do marcador; a latência e o custo fora do Claude
  saíram à mão.

### Levantamento (o que este desenho usa)

- O `brza sessions` tem os verbos `open, list, send, title, close` (`BW/packages/client/bin/brza-sessions:71`). [F1 · lido · 98]
- O `open` chama `brza agent launch --agent --surface chat --worktree [--prompt]`, sem `--model`/`--effort`
  (`brza-sessions:456-457`). [F2 · lido · 98]
- O `brza agent launch` aceita `--model` e `--effort`, o `--effort` exige `--model`, e valem nas duas superfícies
  (`BS/src/cli/specs/agent-launch.ts:9,25`; `brza agent launch --help` rodado). [F3 · lido · 97]
- O `record('open')` não grava o `agent` do Claude nem `model`/`effort` (`brza-sessions:471-472`), e o `session_map()` só
  dobra `name, title, opened, claude_session, provider_session, agent` (`brza-sessions:101-110`). [F4 · lido · 97]
- O `launch.py` troca `m.brza` (anexa `--model/--effort` ao `agent launch`) e `m.record` (grava `model/effort` no
  `open`) e chama `main()` (`WS/.worktrees/playground/.sessions/reuniao-mcp-remoto/launch.py:9-21`). [F5 · lido · 98]
- O `send_command` imprime `sent: true` sempre (`brza-sessions:341-346`), e o `send_to_chat` descarta o resultado do
  `agentSession.send` (`BW/bin/brza_runtime.py:141-145`). [F6 · lido · 98]
- O `clientOperationId` nasce novo a cada envio, `f'{now_ms}-{entropy}'` (`brza_runtime.py:130-135`); não há
  `--operation`. [F7 · lido · 97]
- O resultado de mutação do app é `{ok: true, replayed, fence, cursor, value}` ou `{ok: false, refusal}`
  (`BS/src/shared/agent-session/agent-session-wire.ts:299-308`); o `rpc()` só levanta erro quando o `ok` do transporte
  é falso (`brza_runtime.py:115-117`), e por isso a recusa do envio passa calada hoje. [F8 · lido · 88] (premissa: o host
  põe a recusa dentro do `result`, como o `brza chat send` da branch a lê em `submissionResult.ok`)
- O valor do `agentSession.send` é `{clientMessageId, submission}` ou `{clientMessageId, queued: {messageId, position,
  state}}` (`agent-session-wire.ts:325-333`). [F9 · lido · 95]
- O `brza chat send` da branch `feat/pln-011-chat-cli` devolve `operation, replayed, delivery, submission.state,
  clientMessageId, queuePosition, refusal`, e o timeout vira `unknown` (`BS@feat/pln-011-chat-cli:src/cli/handlers/chat.ts:206-283`). [F10 · lido · 92]
- A spec dessa branch: saída 0/1/3, `--operation` com 13 dígitos, hífen e 32 hex, o mesmo formato do `brza_runtime`;
  `chat read --cursor` com `cursor_reset` saindo 2; `chat list` com estado e última resposta
  (`BS@feat/pln-011-chat-cli:src/cli/specs/chat.ts:7,25-26,42-44`). [F11 · lido · 95]
- A R1.4 do PLN-010, literal: "**O app sem o `brza chat`:** falha com aviso (recomendada) — erro que pede o build com o
  `brza chat`, sem reserva; […] reserva pelo `rpc` de hoje — custo: ~3 h, dois transportes e testes em dobro; se paga:
  se o Orca precisar do `brza sessions` antes do `#33115`. **Decidido — falha com aviso (Recomendado).**", e a linha de
  Cobertura "sem o `brza chat` no app alvo, os comandos saem com erro que pede o build com ele, sem cair no `rpc` antigo"
  (`workstream/tools-kit:plans/PLN-010-…/PLN-010-plan.md:165-171,70`). [F12 · lido · 97]
- O PLN-010 decidiu a saída do `send` por estado — 0 enfileirada ou `accepted`, 1 `rejected` e erro, 75 `pending` ou
  `unknown` (R2.1) — e a operação explícita (R2.2) (`PLN-010-plan.md:182-198`); a branch do Studio usa 3, não 75, e 2,
  não 65, para o cursor (F11). [F13 · lido · 96]
- O `agentSession.setOption` recebe `{envelope, key, value}`
  (`BS/src/shared/rpc-contract/structured-agent-session-params.ts:205-209`). [F14 · lido · 97]
- As chaves são `model` e `effort` nos três adaptadores: Claude (`BS/src/main/claude/structured/launch/claude-structured-options.ts:62`),
  Codex (`BS/src/main/codex/structured/turns/codex-turn-option-keys.ts:2`) e ACP, que serve o Grok e o Antigravity
  (`BS/src/main/acp/acp-structured-options.ts:77,142-147`). [F15 · lido · 92]
- No Claude, escrever `model` retira a confirmação de `effort` e `fastMode` (`claude-structured-options.ts:69-77`); por
  isso o `effort` vai depois do `model`, numa segunda chamada. [F16 · lido · 85] (premissa: retirar a confirmação quer
  dizer que o `effort` anterior não vale para o modelo novo)
- O renderer monta o fingerprint do `setOption` como o do `send`: `{method, sessionId, fields: {key, value}}`
  (`BS/src/renderer/src/lib/agent-session/launch/structured-agent-session-launch-options.ts:135-153`). [F17 · lido · 95]
- As abas do `session.tabs.listAll` trazem `chatStatus` com `state`, `updatedAt`, `evidenceObservedAt` e `mainAgent`; uma
  aba de chat veio sem `chatStatus` (leitura só, nesta execução). [F18 · rodado · 95]
- Os estados são `working, blocked, waiting, done` (`BS/src/shared/agent-status/contracts/agent-status-types.ts:29`). [F19 · lido · 97]
- A página do `agentSession.history` traz `queuedMessages`, `nextQueuedMessageId` e `hostNow`
  (`agent-session-wire.ts:100-108`), e o `HistoryParams` aceita `cursor` e `limit`
  (`structured-agent-session-params.ts:329-336`). [F20 · lido · 95]
- O `agentSession.subscribeTurnCompletions` é streaming e "missed edges never replay"
  (`BS/src/main/runtime/rpc/methods/structured-agent-session-turn-completion-stream.ts:1,42-46`); o `rpc()` lê uma
  linha só da resposta (`brza_runtime.py:104-112`). [F21 · lido · 93]
- O `chats()` chama o `agentSession.history` por aba de Claude, a cada `list` (`brza-sessions:302`). [F22 · lido · 97]
- Os testes do `brza sessions` estão em `BW/tests/cli/test_brza_sessions.py` (760 linhas; `FakeApp`, `CommandTest.run_main`,
  o mapa num temporário): 47 passam com `env -u BRZA_WORKSPACE`; com a `BRZA_WORKSPACE` da sessão, 4 falham nos testes
  de checkout relativo. [F23 · rodado · 97]
- O `send_to_chat` tem três chamadores: `brza-sessions:343`, `brza-sessions:479` e `brza-run:115`. [F24 · rodado · 97]
- A branch do PLN-012 (`feat/pln-012-medida-por-tarefa`) muda `measure.py`, `summarize_measurements.py` e `brza-run`, e
  não toca `brza-sessions` nem `brza_runtime.py` (`git diff --stat master...`). [F25 · rodado · 95]
- O rollout do Codex: a primeira linha é `session_meta` com o id da sessão, o nome do arquivo termina no id, o
  `token_count` pode vir com `info: null`, e o `task_complete` traz `error` quando a cota acaba
  (`~/.codex/sessions/2026/11/07/rollout-2026-11-07T21-41-43-….jsonl`). [F26 · rodado · 93]
- O `agrega.py` da coleta já extrai `task_started`/`task_complete` e o último `token_count.info.total_token_usage`
  (`/private/tmp/wf-improv/processo/agrega.py:27-31`). [F27 · lido · 92]
- A issue `codex-e-antigravity-sem-medida-por-tarefa` (tools-kit, `low`) estima medir o Codex no hook em "6 h ou mais",
  com "outro formato e outra tabela de preço", e pede primeiro "saber onde o Codex e o `agy` gravam a sessão, os tokens"
  (`workstream/tools-kit:work/issues/codex-e-antigravity-sem-medida-por-tarefa.md:27-33`). [F28 · lido · 95]
- Grok grava tokens e `costUsdTicks` por sessão e turno em `~/.grok/sessions/<cwd URL-encoded>/<UUID>/usage.json`, conferidos no F20 do Desenho em 2026-11-09. A busca anterior era incompleta; Antigravity não foi reconferido. O contrato implementado de `usage` ainda retorna Grok como `unmeasured`; a integração fica na [O custo e os tokens do Grok entram nas medições da reunião](../../work/issues/custo-e-tokens-do-grok-nas-medicoes-da-reuniao.md). [F29 · corrigido · rodado · 95 para presença dos campos]
- O `brza-shot` só junta literais `'…'` (`WS/scripts/brza/brza-shot:162-166`), e o Studio passou a
  `function visualBaseCss(fitFrame)`, com template `${scrollbars}`, e `const BASE_CSS = visualBaseCss(true)`
  (`BS/src/shared/native-chat/native-chat-visual-shell.ts:101-106`). [F30 · lido · 97]
- O `brza-shot` não está no `.brza/core.lock`: é do `brza-workspace`, e se edita na `master` dele, não no
  `brza-workflow`. Os 17 testes dele passam, e a fixture usa a forma antiga (`scripts/brza/tests/test_brza_shot.py:66-68`). [F31 · rodado · 92]
- No PLN-013, os passos do `brza sessions` saíram entre metade e o total do estimado: P3 0,5/0,5 h, P9 1,5/0,75 h, P10
  2/1 h, revisões P4 0,75/1 h e P11 1/1 h (`workstream/tools-kit:plans/PLN-013-…/PLN-013-plan.md:152,174,276,293,311`). [F32 · lido · 95]
- O `--json` do `list` é o contrato do roteador do PLN-003, e o arquivo do mapa não é (`brza-sessions:48-50`); o teste
  compara o dicionário inteiro de uma sessão (`test_brza_sessions.py:193-197`). [F33 · lido · 95]
- O gerador do painel (outro consultor) lê por persona `sessao, runtime, modelo, esforco, estado, respondeu_as,
  latencia_s, latencia_fonte, trabalhando_s, custo_usd, tokens{entrada, cache}`
  (`/private/tmp/wf-improv/desenho/estado-r3.json`; `panel_proto.py:60-99`). [F34 · lido · 90]

### As alternativas

> **Gatilho:** bifurcação. Os custos em horas têm por base o PLN-013 [F32], onde o executado ficou entre 50% e 100% do
> estimado; por isso cada estimativa abaixo é teto, não meta.

#### (a) O `read`

**Decidido em R3.1 (2026-11-08): A3, o `read --last` pelo `rpc`, junto do recibo e da `--operation`.** A1 e A2 caem; A4 segue no PLN-010 para o `read` completo.

##### A1 — Não entra agora: a posição sai do worklog da persona, por arquivo, e o `read` fica no PLN-010 (recomendada)

- **Custo:** 0 h de código [C1 · inferido · 75]; o `wait` dá o estado (`blocked`, falha do Codex), e o coordenador lê a
  seção do worklog, como a reunião já faz. Estreita o texto da R1.2, que nomeava o `read`. **Se paga:** agora, porque a
  narração da R1.4 — posição e confiança por persona — sai das tabelas do worklog, não do chat [C2 · inferido · 75].
  **Reabre:** o texto da R1.2.

##### A2 — `read <nome> [--limit N] [--since <cursor>]` pelo `rpc`, agora

- **Custo:** ~3 h [C3 · inferido · 60]: portar o `chatTranscript` da branch do Studio, mais o cursor e o `cursor_reset`;
  e cada sincronização do upstream pode mover a forma do journal, como o commit `f3cca185afa` da branch mostra
  ("brza chat follows the journal identity […] the v1.4.251 sync moved"). Revoga a R1.4 do PLN-010 para a leitura
  [F12]. **Se paga:** quando uma persona travar numa pergunta (`blocked`) ou numa falha que não escreveu no worklog.
  **Reabre:** PLN-010 R1.4 e R1.3 (o cursor fica com quem chama).

##### A3 — `read <nome> --last` mínimo: só a última resposta, sem cursor, pelo `rpc`

- **Custo:** ~1 h [C4 · inferido · 65]: `agentSession.history` `tail`, o último item de texto do assistente ou a
  pergunta pendente. Revoga a R1.4 só para isso. **Se paga:** na primeira persona `blocked` ou que terminou o turno sem
  marcador. **Reabre:** PLN-010 R1.4, em parte.

##### A4 — Esperar o `brza chat read` do PLN-011/PLN-010

- **Custo:** 0 h aqui [C5 · inferido · 80] (premissa: o PLN-010 entrega sem mudança de escopo); sem prazo: o PLN-011
  está parado no C1 de Anderson e o PLN-010 em `ready: não` [F12]. **Se paga:** quando o Studio fundir a
  `feat/pln-011-chat-cli`. **Reabre:** nada. (A1 já inclui esta espera.)

#### (b) O fim de rodada

**Decidido em R3.2 (2026-11-08): B1.**

##### B1 — `wait` por `state`, com a fila e o `updatedAt`, e o marcador como confirmação opcional (recomendada)

- **Custo:** ~2,5 h [C6 · inferido · 70]: polling do `listAll` (sem o `history` por aba que o `list` faz [F22]); a
  regra de fim descrita em "Como fica". **Se paga:** agora: vale nos quatro runtimes sem depender de a persona obedecer,
  e a falha do Codex aparece na hora, não no timeout. **Reabre:** nada.

##### B2 — Só marcador em arquivo (o `grep` formalizado)

- **Custo:** ~1 h [C7 · inferido · 75]; depende da persona escrever no lugar certo, que já falhou (três personas
  puseram o marcador em dois lugares, `processo/levantamento.md` fricção 1), e a persona que caiu só aparece no
  `--timeout`. **Se paga:** agora, para reunião só de personas Claude disciplinadas. **Reabre:** nada.

##### B3 — `brza orchestration check --wait`, com as personas mandando `brza orchestration send`

- **Custo:** 0 h de código [C8 · inferido · 55]; um comando por persona por rodada e um `run-create` por reunião, e não
  sondei se um chat aberto por `agent launch` manda à caixa do Run. **Se paga:** só se a reunião passar a correr num
  Run. **Reabre:** a R1.2 (o fluxo sai do `brza sessions`).

#### (c) A entrega ao `tools-kit`

**Assumido como recomendação, sem rodada: C1.**

##### C1 — Uma issue "o `brza sessions` para a reunião", com este D como conteúdo (recomendada)

- **Custo:** uma issue agora [C9 · inferido · 85] (premissa: a sessão do `tools-kit` executa sem abrir plano, como fez
  em issues `low` do PLN-013); o `shot` vai à parte, na `master` do `brza-workspace` [F31]. **Se paga:** agora: é o que
  a R1.1 decidiu. **Reabre:** nada.

##### C2 — Emendar o PLN-010

- **Custo:** uma rodada no PLN-010 para mudar o `depends_on` e a R1.4; enquanto isso, as primitivas herdam o bloqueio
  do PLN-011 [C10 · inferido · 80] (premissa: o PLN-010 não muda de `ready` sem a R5 do PLN-011). **Se paga:** só se
  o `read` e o recibo fossem o centro do pedido. **Reabre:** a R1.1 e o PLN-010.

##### C3 — Um plano novo no `tools-kit`

- **Custo:** abertura e entrevista lá, que repetem as rodadas daqui; ~1 h de sessão antes da primeira linha de código
  [C11 · inferido · 60]. **Se paga:** se a execução passar de um dia ou se partir em entregas. **Reabre:** a R1.1.

#### (d) A medição

**Decidido em R3.2 (2026-11-08): D1.**

##### D1 — Latência no mapa e `usage` com o Codex pelo rollout; Grok e Antigravity `unmeasured` (recomendada)

- **Custo:** ~2 h [C12 · inferido · 70]: 0,5 h do evento `turn` no `wait` e 1,5 h do `usage` (o `agrega.py` já prova a
  leitura [F27]). Não toca o `measure.py`. **Se paga:** na próxima reunião com Codex, que na reunião B somou 10,8 M de
  tokens de entrada sem US$ (`processo/levantamento.md` §3.4). **Reabre:** nada; responde em parte o item 1 da issue
  do Codex [F28].

##### D2 — Só latência no mapa

- **Custo:** ~0,5 h [C13 · inferido · 75]. **Se paga:** agora, mas o custo do Codex segue à mão. **Reabre:** nada.

##### D3 — Nada até o PLN-012 fechar

- **Custo:** 0 h [C14 · inferido · 85] (premissa: o PLN-012 segue só com o Claude, como a R1.3 dele decidiu [F28]).
  **Se paga:** nunca para o Codex, o Grok e o Antigravity, que o PLN-012 deixou fora. **Reabre:** nada.

#### (e) O `brza shot`

**Assumido como recomendação, sem rodada: E1.**

##### E1 — Avaliar `visualBaseCss(<arg>)` no Python: o ternário de `scrollbars` e o template (recomendada)

- **Custo:** ~1 h [C15 · inferido · 75], e acompanha o Studio na próxima refatoração, como hoje. **Se paga:** na
  próxima reunião com disputa visual. **Reabre:** nada.

##### E2 — Rodar a função pelo `node`, extraída do arquivo

- **Custo:** ~1,5 h [C16 · inferido · 60] e o `node` como dependência do `brza shot`; aguenta mudança no template, não
  na forma da função. **Se paga:** se o Studio mexer no CSS base com frequência. **Reabre:** nada.

### Como fica

> O artefato como vai ao `--help`. A forma do recibo e do `read` segue a do `brza chat` da branch do Studio [F10, F11],
> para que o PLN-010 troque só o transporte. Os códigos de saída seguem a R2.1 do PLN-010 (0/1/75) [F13], e não os 0/1/3
> da branch: **[ponto para rodada, decidido aqui como recomendação: a R2.1 vale até o PLN-010 rever]**.

```text
brza sessions <nome> [--agent A] [--title T] [--rename] [--checkout C]
                     [--prompt P | --prompt-file F] [--model M [--effort E]] [--wait] [--dry-run]
brza sessions list   [--prefix P] [--json]
brza sessions send   <nome>… (--text T | --file F) [--prefix P] [--operation ID] [--json]
brza sessions send   <nome> <texto> [--json]                          # a forma de hoje, mantida
brza sessions wait   <nome>… [--prefix P] [--marker ARQUIVO:REGEX]… [--any] [--timeout S] [--json]
brza sessions model  <nome> <modelo> [--effort E] [--json]
brza sessions read   <nome> --last [--json]
brza sessions usage  <nome>… [--prefix P] [--json]
brza sessions title  <nome> <título> [--json]
brza sessions close  (<nome> | --prefix P) [--force] [--json]
```

O mapa ganha três eventos, todos fora do contrato [F33]: `open` passa a ter `agent` sempre, e `model`/`effort`;
`send` (`name, chat, operation, delivery, message_id`); `turn` (`name, chat, sent_at, ended_at, latency_s, outcome,
marker`); e `model` (`name, chat, model, effort`).

#### `open --model --effort`

- **Menor mudança:** o argparse ganha `--model` e `--effort` (`brza-sessions:408-421`); o `--effort` sem `--model` sai
  1 antes do launch, como o `agent launch` [F3]; o launch anexa os dois (`:456-457`); o `record('open')` grava
  `agent`, `model`, `effort` (`:471-472`); o `session_map()` dobra os três (`:102-103`); o `--dry-run` os mostra
  (`:446-449`). O `launch.py` sai.
- **Teste que falha antes:** em `CommandTest`, `test_open_passes_model_and_effort_to_the_launch_and_records_them`
  (`self.launches[-1]` termina em `'--model', 'gpt-6-astra', '--effort', 'xhigh'`; `self.read_map()[-1]` tem os dois) e
  `test_effort_without_model_is_refused_before_any_launch` (`self.launches == []`, saída 1).
- **Estimado:** 0,5 h [C17 · inferido · 80] (premissa: a base é o P3 do PLN-013, 0,5/0,5 h, de tamanho igual [F32]).
- **Reabre:** nada. A tabela por papel do MCP (PLN-013 R3.1/R4.1) segue só no MCP: aqui a persona escolhe o modelo.

#### `list`

- **Menor mudança:** o `chats()` (`brza-sessions:305-309`) acrescenta `agent`, `model`, `effort` (do mapa),
  `updated_at` (`chatStatus.updatedAt` [F18]), `last_latency_s` e `last_turn_at` (do último `turn` do mapa); `--prefix`
  filtra; a linha de texto ganha agente e modelo (`:336-337`).
- **Teste que falha antes:** `test_list_names_each_chat_by_the_last_rename_in_its_transcript` compara o dicionário
  inteiro (`test_brza_sessions.py:193-197`) e falha até ganhar as chaves novas; mais
  `test_list_folds_model_effort_and_the_last_turn_from_the_map`.
- **Estimado:** 0,5 h [C18 · inferido · 75].
- **Reabre:** o contrato do roteador do PLN-003 [F33], com chaves só acrescentadas **[ponto para rodada, decidido aqui
  como recomendação: chave nova não quebra o roteador; não li o parser dele]**.

#### `send <nome>… --text|--file [--operation]`

- **Menor mudança:**
  - `brza_runtime.send_to_chat` passa a devolver o resultado, com `operation` opcional (`brza_runtime.py:130-145`);
    os chamadores que ignoram o retorno, inclusive o `brza-run:115`, seguem iguais [F24], e não há conflito com a
    branch do PLN-012 [F25].
  - O `send_command` (`brza-sessions:341-346`) monta o recibo como o `brza chat send` [F10]: `queued` (com `position` e
    `message_id`), `accepted`, `rejected` (com o `refusal`, quando `ok: false` [F8]) ou `unknown` (timeout do `rpc`).
  - Vários nomes ou `--prefix`, com `--text` ou `--file`; a forma posicional de hoje fica.
  - `--operation` só com um nome; com vários, o recibo dá uma `operation` por nome.
  - Cada envio grava `send` no mapa. É o início da latência, não estado de retry: a R2.2 do PLN-010 segue.
  - Saída: 0 se todos `queued`/`accepted`, 1 se algum `rejected`, 75 se algum `unknown`, e o pior vence.
- **Teste que falha antes:** `test_send_queues_the_text_to_the_chat_found_by_name` (`test_brza_sessions.py:213-220`)
  espera `{'sent': True…}` e passa a esperar o recibo; mais `test_a_refused_send_exits_one_with_the_refusal` (o
  `FakeApp` devolve `{'ok': False, 'refusal': …}` no `agentSession.send`), `test_send_to_many_names_reads_the_file_once`,
  `test_operation_is_reused_and_a_replay_says_replayed` e `test_send_records_the_send_event`.
- **Estimado:** 2 h [C19 · inferido · 70]: 0,5 h dos códigos e 1 h da operação, como a R2.1 e a R2.2 do PLN-010
  estimaram [F13], e 0,5 h dos vários nomes e do `--file`.
- **Reabre:** a R1.4 do PLN-010, para o recibo pelo `rpc` até o `brza chat` chegar: **[ponto para rodada — pergunta 1]**.

#### `wait <nome>… [--marker] [--any] [--timeout]`

- **Menor mudança:** função nova, com polling de `session.tabs.listAll` a cada 2 s [C20 · inferido · 70], sem o
  `history` por aba do `chats()` [F22]: o nome sai do mapa.
  - **Fim de turno por chat:** o estado é `done` ou `waiting` [F19], o `updatedAt` passa do `at` do último `send` desse
    chat e, se o recibo foi `queued`, o `message_id` já saiu do `queuedMessages` da página [F20], numa consulta por chat
    enfileirado. Sem isso, o fim do turno anterior da persona atrasada contaria como resposta (o Grok ficou uma rodada
    atrás na reunião B).
  - **Os outros desfechos:** `blocked` sai como `blocked`. No Codex, o `task_complete` com `error` no rollout sai
    `failed`, com a mensagem, por exemplo a cota [F26].
  - **O marcador:** com `--marker ARQUIVO:REGEX`, o turno que terminou sem ele sai `ended_without_marker`.
  - **A saída:** `--any` volta no primeiro que terminar, para a narração da R1.4, chamando de novo com os que faltam.
    Sai 0 com todos prontos, 75 no timeout com alguém pendente, 1 em erro.
  - **O que grava:** cada fim grava `turn` no mapa.
  - **O texto:** uma linha por persona, `done:     reuniao-cinza  89 s` e `faltam:   reuniao-faisca  working há 4m10s`.
  - **O `--json`:** `{"done": [{name, agent, model, effort, outcome, ended_at, latency_s, latency_source: "poll"}],
    "pending": [{name, state, elapsed_s}], "timed_out"}`, o que o gerador do painel lê [F34].
- **Teste que falha antes:** um `FakeApp` com a sequência de `chatStatus`:
  - `test_wait_ignores_a_done_older_than_the_send`;
  - `test_wait_waits_for_the_queued_message_to_leave_the_queue`;
  - `test_wait_any_returns_on_the_first_and_names_the_rest`;
  - `test_wait_times_out_with_75_and_the_pending_list`;
  - `test_wait_reports_a_codex_turn_that_failed_on_quota` (rollout de fixture);
  - `test_wait_flags_a_turn_without_the_marker`;
  - `test_wait_records_the_turn_with_its_latency`.
- **Estimado:** 2,5 h [C21 · inferido · 70] (premissa: o P9 do PLN-013, o `--wait` de abertura, levou 0,75 h de 1,5 h
  [F32]; este tem quatro condições e a fila).
- **Reabre:** nada. **A conferir na sonda:** que o `updatedAt` muda ao entrar em `working` e que o `state` do Grok e do
  Antigravity é fiel [C22 · inferido · 60].

#### `model <nome> <modelo> [--effort]`

- **Menor mudança:** generalizar o `send_mutation` num `mutation(method, session_id, fields, fence, operation)`
  (`brza_runtime.py:130-138`), com o fingerprint do renderer [F17]. Depois:
  - `agentSession.setOption` com `key: 'model'` e, em seguida, com `key: 'effort'` [F14, F15, F16];
  - a recusa sai 1 com o `refusal`, e a do Antigravity sobre modelo explícito é esperada;
  - grava `model` no mapa, e o `list` mostra o modelo novo.
- **Teste que falha antes:** `test_model_sets_model_then_effort_with_the_app_fingerprint` e
  `test_a_refused_model_exits_one_and_records_nothing`.
- **Estimado:** 1 h [C23 · inferido · 70].
- **Reabre:** nada. O modelo vale do próximo turno em diante, como diz o `AgentSessionOptionsResult` ("effective
  next-turn values").

#### `read <nome> --last` (R3.1)

- **Menor mudança:** função nova sobre o `agentSession.history` com `limit` pequeno e sem cursor [F20]: devolve o último
  item de texto do assistente ou, com o `state` em `blocked`, a pergunta pendente; `--json` com `{name, state, last:
  {role, text, at}, queued}`. Sem cursor e sem `--since`: o `read` completo fica no PLN-010.
- **Teste que falha antes:** `test_read_last_returns_the_last_assistant_text` e
  `test_read_last_on_a_blocked_chat_returns_the_pending_question`, com a página do `history` no `FakeApp`.
- **Estimado:** 1 h [C4].
- **Reabre:** a R1.4 do PLN-010, só para a última resposta, junto do recibo; a exceção vai escrita lá.

#### `close --prefix`

- **Menor mudança:** o `close` (`brza-sessions:358-370`) aceita `--prefix`; laço sobre os nomes; `--json` com
  `{"closed": […], "refused": […]}`; sai 1 se algum chat `working` ficou sem `--force`.
- **Teste que falha antes:** `test_close_prefix_closes_the_idle_and_refuses_the_working`.
- **Estimado:** 0,5 h [C24 · inferido · 80] (premissa: o laço sobre o `close_command` que já existe).
- **Reabre:** nada.

#### `usage <nome>…` — a medição por runtime

- **Menor mudança:** verbo novo, só leitura, sem tocar o `measure.py`.
  - **Claude:** soma `estimated_cost_usd` e tokens das linhas `turn` do `.measurements/measurements.jsonl` com o
    `session_id` igual ao `claude_session`.
  - **Codex:** acha `~/.codex/sessions/**/rollout-*-<provider_session>.jsonl` [F26] e devolve o último
    `token_count.info.total_token_usage` (entrada, cache, saída, raciocínio), as durações por turno e o erro do
    último `task_complete`. Só tokens, sem US$.
  - **Grok e Antigravity:** `{"measured": false, "reason": "unmeasured"}` no contrato desta entrega. Para Grok, é limitação da implementação, não ausência de dados em disco (F29 corrigido); integração registrada como pendência.
  - **O `--json`:** dá ao painel `custo_usd` ou `tokens` por persona [F34].
- **Teste que falha antes:** `test_usage_sums_claude_turns_by_session`, `test_usage_reads_the_last_codex_token_count`
  (rollout de fixture com `info: null` antes do último) e `test_usage_marks_grok_and_antigravity_unmeasured`.
- **Estimado:** 1,5 h [C25 · inferido · 70] (premissa: o porte das 10 linhas do `agrega.py` [F27] com fixture).
- **Reabre:** nada. **A colisão com o PLN-012:** não há. A latência da reunião fica no mapa do `brza sessions`, e não
  no hook; o `measure.py` segue do PLN-015 e do PLN-012, nessa ordem; o leitor do rollout pode subir ao
  `brza_runtime` quando a issue do Codex [F28] decidir medir por tarefa.

#### O `brza shot`

- **Menor mudança:** no `brza-shot`, ao lado do `string_concat` (`brza-shot:162-166`), um `base_css_call` que acha
  `const BASE_CSS = visualBaseCss(<true|false>)`, lê na função o `const scrollbars = fitFrame ? '<a>' : '<b>'` e o
  template, e troca `${scrollbars}` pelo ramo do argumento [F30]. O literal antigo continua aceito; outra forma sai
  com o `ShotError` de hoje.
- **Teste que falha antes:** em `scripts/brza/tests/test_brza_shot.py`,
  `test_base_css_is_read_from_the_visual_base_css_call`, com a fixture `VISUAL` na forma nova (`:66-68`); o
  `test_parts_come_from_the_studio_code` fica na forma antiga.
- **Estimado:** 1 h [C26 · inferido · 75]. **Onde:** `master` do `brza-workspace` [F31], não o `brza-workflow`.
- **Reabre:** nada.

#### A sonda, antes do código

- Com chats reais, uma vez:
  - o `setOption` `model` num Claude e num Codex;
  - o reenvio com a mesma `operation` depois de o fence mudar, para ver se o host devolve `replayed` ou recusa;
  - o `updatedAt` ao entrar em `working`;
  - o `state` de um Grok e de um Antigravity num turno.
- **Estimado:** 0,5 h [C27 · inferido · 70].

#### O que o embrulho do MCP reaproveitaria (só anotação, R1.2)

1. Cada ferramenta (`open`, `send`, `wait`, `list`, `model`, `usage`, `close`) chama o verbo com `--json`, e o JSON do
   CLI é o contrato dela.
2. O `wait` vira long-poll com `--any` e `--timeout` abaixo do timeout do cliente MCP.
3. O `open` com `--model/--effort` contorna a política por papel; o MCP precisaria de uma bandeira explícita para isso.
4. O chamador vira `ORCA_AGENT_SESSION_ID` no ambiente do subprocesso, para a origem do coordenador.
5. Nada do mapa muda: o MCP escreve nele pelo mesmo CLI.

### Estimado (A3, B1, C1, D1, E1, pelas rodadas)

| Item | Horas |
| :--- | ----: |
| Sonda | 0,5 [C27] |
| Base comum (`mutation()`, seletor `nomes`/`--prefix`, eventos do mapa) | 0,5 [C28 · inferido · 70] |
| `open --model --effort` | 0,5 [C17] |
| `list` | 0,5 [C18] |
| `send` | 2 [C19] |
| `wait` (com o evento `turn`) | 2,5 [C21] |
| `model` | 1 [C23] |
| `read --last` (R3.1) | 1 [C4] |
| `close --prefix` | 0,5 [C24] |
| `usage` | 1,5 [C25] |
| Revisão e merge | 1 [C29 · inferido · 80] (premissa: como o P4 e o P11 do PLN-013 [F32]) |
| **Subtotal `brza-workflow`** | **11,5** |
| `brza shot` (`brza-workspace`) | 1 [C26] |
| **Total** | **12,5 h** [C30 · inferido · 70], com o `read --last` da R3.1; pelo PLN-013 [F32], o executado deve ficar entre 6,5 e 12,5 h |

### O que este desenho assume (decidido como recomendação, sem rodada)

- A entrega vai numa issue única no `tools-kit` (C1), que é o que a R1.1 decidiu; o `shot` vai à `master` do
  `brza-workspace`, na mesma issue ou à parte.
- O `shot` pela E1.
- A forma do recibo e do JSON do `wait` segue a do `brza chat send` da branch do Studio [F10]; os códigos seguem a R2.1
  do PLN-010 (75), não os da branch (3).
- O `list` mostra o modelo pedido (mapa), não o que o runtime relata (`agentSession.options`, `current.reportedModel`),
  para não somar uma chamada por chat a cada `list`.
- O `wait` faz polling e não usa o `subscribeTurnCompletions`, porque o `rpc()` lê uma linha só e o stream perde as
  bordas que passaram antes da assinatura [F21].
- A latência do mapa tem a precisão do polling (2 s); a exata do Claude e do Codex sai do `usage`.
- O `--persona` não entra: a persona cabe no `--prompt-file`.
- O fallback de runtime quando a cota cai (P14 do levantamento) não entra; o `wait` só a mostra como `failed`.

### Revisão pela R5 e R6: o ciclo de vida das personas (2026-11-08)

A R5 trouxe o requisito ("as sessões abertas pelo coordenador devem abrir como o `orca-orchestrator` faz, fechando sozinho 2min após não ser mais necessário, com o botão de `manter aberta` acima do input de conversa do chat") e a R6 escolheu a via. O que muda neste D2, verbo a verbo; o que não é citado fica como desenhado acima.

#### O terreno do mecanismo (`brza-studio@8abbde720ce`, só leitura)

- **O prazo de 2 min** é `WORKER_TERMINAL_AUTO_RELEASE_GRACE_MS`, em `src/main/runtime/orchestration/db/worker-terminal/worker-terminal-auto-release.ts:10`. [L1 · lido · 95]
- **Só o `worker_done` aceito arma o prazo** (`worker-report-settlement.ts:280-281`); o fim de turno de um chat sem `worker_done` não arma nada, e o host avisa a coordenação com "Worker stopped without reporting" (`worker-turn-stop-report.ts:74-130`). [L2 · lido · 95]
- **O worker em trabalho suspende a contagem**, que recomeça com mais 2 min ao repousar (`worker-auto-release-activity.ts:32-55`); "Keep open" e `worker-keep-open` a cancelam (`worker-terminal-user-keep.ts:55-119`, `worker-keep-open.ts:16-50`); no prazo, a liberação fecha a sessão do chat e retira a aba, sem remover o worktree (`structured-agent-session-close.ts`). [L3 · lido · 90]
- **A faixa com o botão** é `NativeChatStructuredWorkerLifetimeStrip.tsx`, montada por `NativeChatStructuredComposerTabStrips.tsx:21`; só aparece em aba com Dispatch (`renderer/src/lib/worker-auto-close.ts:85-125`); o `relation: 'worker'` não entra na decisão. Um chat de `agent launch` não a recebe sem código novo. [L4 · lido · 95]
- **`worker-start --spec` sem Run cria um** (`worker-start-authority.ts:58-85`); o chamador precisa de identidade: `ORCA_AGENT_SESSION_ID`, `ORCA_TERMINAL_HANDLE` ou terminal ativo inequívoco no cwd (`terminal-identity.ts:15-115`). [L5 · lido · 85]
- **A superfície segue `nativeChatProviders[agente]` ou `agentDefaultSurface`** (`structured-native-chat-launch-route.ts:58-64`); não há `--surface` no `worker-start`; o padrão de fábrica é terminal (`default-global-settings.ts:151`); o worker em chat nasce sem foco. Anderson confirmou em R6.3 que os quatro agentes estão em Chat. [L6 · lido · 95]
- **O `--spec` vira a Task**, e o preâmbulo do Orca, com o `worker_done` a enviar, chega como turno do coordenador (`relation: 'coordinator'`). [L7 · lido · 85]
- **A coordenação espera por `orchestration check --wait [--types …]`** e lê com `worker-show` e `worker-read`. [L8 · rodado · 90]
- **`--display-name` e `--name` só nomeiam worktree novo** e são recusados em worktree existente: o chat do worker não tem título pelo `worker-start`; o `brza sessions` segue dono do nome no mapa. [L9 · lido · 90]
- **Dar o ciclo de vida ao `agent launch`** tocaria armazenamento do prazo sem Dispatch, gatilho de fim de turno, scheduler, RPC de keep-open por sessão, o portão do renderer e a flag: cerca de 1 300 linhas, 20 a 40 h, com conflito alto no sync do upstream. [L10 · inferido · 60]
- **A híbrida** (`agent launch --surface chat` e depois `worker-start --terminal orca_session_id:<chat> --spec …`) daria `worker_done` e mailbox, mas o terminal reusado nunca é fechado pela liberação, e o custódio só se grava para terminal criado (`local-worker-start.ts:198`): provavelmente sem fechamento automático. A sonda decide. [L11 · lido · 75]

#### Como fica, pela R6

| Verbo | Antes (R3) | Agora (R5 e R6) |
| :---- | :--------- | :-------------- |
| `open` | `agent launch --surface chat --model --effort` | **P4a.0, a sonda:** a híbrida; se o `autoReleaseAt` não valer para terminal reusado, **a via A**: `worker-start --spec <prompt> --agent <runtime> --model <m> --effort <e> --worktree path:<checkout>`, como o `cycle.py:136-167` do MCP. O mapa grava `dispatch`, `orca_session_id`, `model`, `effort`. A identidade do chamador vem do `ORCA_AGENT_SESSION_ID` da sessão de coordenação (no chat do Studio existe; fora dele, a sonda diz). O nome da persona segue no mapa do `brza sessions`, porque o worker não ganha título |
| `send` | `agentSession.send` com recibo e `--operation` pelo `rpc` (R3.1) | igual para texto livre; **a rodada pode ir por `brza orchestration send --to <dispatch>`**, que chega como "Task from coordinator" e resolve a mensagem como turno da pessoa (F38); a sonda diz qual chega melhor ao chat do worker |
| `wait` | polling de `listAll` por estado, fila e `updatedAt` (R3.2) | **`brza orchestration check --peek --wait --types status,worker_done`**, com recuperação somente leitura por `--all` de eventos já entregues. Adaptação ao contrato instalado, conferido em 2026-11-09: `message` não é tipo válido. O script não consome nem confirma a mailbox; só conclui rodada por evento identificado pelo Dispatch e pela rodada, nunca por status genérico. Cada persona envia `status` ao fechar a rodada e `worker_done` só no encerramento (R6.2). O fallback por estado e fila continua para chat sem Dispatch e para expor `blocked`/`failed` |
| `read --last` | `agentSession.history` | igual; `worker-read` como alternativa para o worker |
| `close` | `agentSession.close` por nome ou `--prefix` | **R7.1:** para Dispatch ativo, pede `worker_done` por mailbox e retorna `closing`, sem afirmar fechamento. `--force` solicita parada guardada, confirma `stopped` e settlement antes de `worker-release`, respeitando identidade, custódia e Keep open. `stop_unknown` expõe incerteza, sem repetição cega ou abandono. Para settled, usa `worker-release` e relata o resultado real, inclusive retained. O fechamento automático após `worker_done` e o botão "manter aberta" continuam; `worker-keep-open` mantém por comando. Chat legado sem Dispatch preserva `close` e `--force` atuais |
| `list` | agente, modelo, esforço, último turno | mais `dispatch` e `auto_release_at`, do `worker-show` |
| `model`, `usage` | como desenhado | iguais; o `usage` do Codex acha o rollout pelo `provider_session` do worker |

#### O que isso muda no resto

- **A alternativa B3 de (b), o `check --wait`, passa a ser a escolhida**, e B1 vira fallback; a estimativa do `wait` (2,5 h) se redistribui para a sonda e a abertura.
- **O MCP e o `brza sessions` convergem**: os dois abrem por `worker-start`; o embrulho MCP (R1.2) fica mais barato.
- **O risco do nome:** a persona não tem título no chat; o `brza sessions title` só vale no Codex (issue do PLN-013). O painel do D3 mostra o nome pelo mapa.
- **O risco do preâmbulo:** o prompt da persona chega depois do preâmbulo do Orca, como turno do coordenador; o briefing da skill passa a contar com isso (o `worker_done` que o preâmbulo pede é o do encerramento, não o de cada rodada).
- **Remoto (`--on`) é só terminal:** a reunião com persona em outra máquina fica fora da v1.

#### Estimado revisto (P4a)

| Item | Horas |
| :--- | ----: |
| P4a.0, a sonda da híbrida e da superfície por agente | 1 a 2 |
| `open` pela via decidida, com o mapa | 2 |
| `send` com recibo e `--operation`, e o envio pela mailbox | 2 |
| `wait` sobre `check --wait`, com o fallback | 1,5 |
| `read --last` | 1 |
| `close` por `worker-release` e `worker-keep-open` | 1 |
| Revisão e merge | 1 |
| **P4a** | **10 (teto)** [C34 · inferido · 60]; a base é a tabela anterior mais os 6 a 12 h da via A estimados pelo `collector` |

### O que as rodadas decidiram

R3, 2026-11-08: o recibo, a `--operation` e o `read --last` pelo `rpc`, como transição até o `brza chat` (exceção à R1.4 do PLN-010, a escrever lá); o `wait` por estado, fila e `updatedAt`; a latência no mapa e o `usage` com o Codex pelo rollout. **R5 e R6, 2026-11-08:** as personas abrem com o ciclo de vida dos workers do Orca (a sonda da híbrida decide entre ela e o `worker-start` puro); o fim de rodada é uma mensagem de mailbox da persona e o `worker_done` vai só no encerramento, então o `wait` vira `check --wait`; os quatro agentes estão em Chat. As perguntas, como foram feitas, ficam abaixo; o texto das respostas está na Entrevista do plano.

### Como foi perguntado (R3)

1. **O recibo e a `--operation` do `send` pelo `rpc` agora, com a forma do `brza chat send`?** A R1.4 do PLN-010 recusou
   a *reserva* pelo `rpc` [F12]; isto é *transição*, que o PLN-010 troca pelo `brza chat` quando chegar.
   1. Sim: transição pelo `rpc`, com a forma e a operação do `brza chat` (Recomendado). `Custo:` 2 h agora [C19], mais
      ~0,5 h no PLN-010 para trocar o transporte [C31 · inferido · 65], e a exceção à R1.4 escrita no PLN-010. `Se paga:`
      na próxima reunião, porque o `wait` precisa do `message_id` do recibo `queued` para não contar o turno anterior.
   2. Só o envio a vários nomes, sem recibo novo. `Custo:` 0,5 h [C32 · inferido · 75]; o `wait` perde a checagem da
      fila e passa a exigir o marcador para a persona atrasada. `Se paga:` agora, até o PLN-010.
   3. Esperar o `brza chat send`. `Custo:` 0 h aqui; o `sent: true` cego continua sem prazo [C33 · inferido · 80]
      (premissa: o PLN-011 segue parado no C1). `Se paga:` quando o Studio fundir a branch.
2. **O `read`, que a R1.2 nomeou** (alternativas em (a)):
   1. Não entra: a posição sai do worklog, e o `read` fica no PLN-010 (Recomendado). `Custo:` 0 h [C1]; o coordenador
      não vê a pergunta de uma persona `blocked` sem abrir a aba. `Se paga:` agora.
   2. `read --last` mínimo pelo `rpc`. `Custo:` ~1 h [C4] e exceção à R1.4. `Se paga:` na primeira persona `blocked`
      ou sem marcador.
   3. `read` completo com cursor pelo `rpc`. `Custo:` ~3 h [C3], manutenção a cada sync do journal, e revoga a R1.4.
      `Se paga:` só se a reunião ler o chat a cada rodada, o que hoje não faz.
3. **O fim de rodada** (alternativas em (b)):
   1. `wait` por estado, fila e `updatedAt`, com o marcador como confirmação (Recomendado). `Custo:` 2,5 h [C21].
      `Se paga:` agora, nos quatro runtimes.
   2. Só marcador. `Custo:` 1 h [C7]; a persona que caiu só aparece no timeout. `Se paga:` agora, com personas
      disciplinadas.
   3. `brza orchestration check --wait`. `Custo:` 0 h de código, um comando por persona por rodada, viabilidade não
      sondada [C8]. `Se paga:` só numa reunião em Run.
4. **A medição** (alternativas em (d)):
   1. Latência no mapa e `usage` com o Codex pelo rollout (Recomendado). `Custo:` 2 h [C12]. `Se paga:` na próxima
      reunião com Codex.
   2. Só latência. `Custo:` 0,5 h [C13]. `Se paga:` agora, com o custo do Codex à mão.
   3. Nada até o PLN-012. `Custo:` 0 h [C14]. `Se paga:` nunca para Codex, Grok e Antigravity.
