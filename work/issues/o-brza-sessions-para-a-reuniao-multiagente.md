---
status: open
description: O `brza sessions` ganha `--model/--effort` na abertura, recibo real e `--operation` no `send`, `wait` por estado e fila, `read --last`, `model`, `usage` por runtime e `close --prefix`, pelo desenho D2 do PLN-017; o `brza shot` volta a ler o CSS do Studio.
scope:
  - brza-workflow
  - workspace
opened: 2026-11-08
priority: high
tags:
  - tooling
---

# O `brza sessions` ganha os verbos da reunião multiagente: modelo na abertura, recibo, `wait`, `read --last`, `model`, `usage` e `close --prefix`

Pedido do [PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md), passos P4a, P4b, P5 e P6, ao workstream `tools-kit` (e à `master` do `brza-workspace`, no P5). O desenho inteiro, verbo a verbo, com a menor mudança em `arquivo:linha`, o teste que falha antes e a estimativa, está em [PLN-017 — Desenho: as primitivas do `brza sessions` (D2)](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-design-cli.md). Esta issue é o pedido; o D2 é o conteúdo.

## O que as rodadas do PLN-017 decidiram (Anderson, 2026-11-08, sessão `workflow-improvements`)

- **R1.2:** "brza sessions primeiro" — as primitivas nascem no CLI; o MCP só as embrulha depois (anotação em D2, "O que o embrulho do MCP reaproveitaria").
- **R3.1:** "Recibo, --operation e read --last pelo rpc" — o `send` devolve o recibo real pelo `rpc` de hoje, na forma do `brza chat send` da branch `feat/pln-011-chat-cli` do Studio, e o `read --last` traz a última resposta ou a pergunta pendente. **É uma exceção de transição à R1.4 do PLN-010** ("falha com aviso, sem cair no `rpc` antigo"), a escrever no PLN-010 (P6): quando o `brza chat` chegar, o PLN-010 troca só o transporte.
- **R3.2:** "wait completo, latência e usage do Codex" — o fim da rodada por estado, fila e `updatedAt`; a latência no mapa do `brza sessions`, não no hook; `usage` soma o Claude pelo `measurements.jsonl` e lê os tokens do Codex no rollout; Grok e Antigravity saem `unmeasured`.
- **R4.1:** "Dividir P4 em envio/espera e medição" — P4a (`open --model`, `send`, `wait`, `read --last`, `close --prefix`, ~8 h) antes de P4b (`list`, `model`, `usage`, ~3,5 h).

## O pedido

### P4a — envio e espera (~8 h)

```text
brza sessions <nome> [--agent A] [--title T] [--rename] [--checkout C]
                     [--prompt P | --prompt-file F] [--model M [--effort E]] [--wait] [--dry-run]
brza sessions send   <nome>… (--text T | --file F) [--prefix P] [--operation ID] [--json]
brza sessions wait   <nome>… [--prefix P] [--marker ARQUIVO:REGEX]… [--any] [--timeout S] [--json]
brza sessions read   <nome> --last [--json]
brza sessions close  (<nome> | --prefix P) [--force] [--json]
```

- **`open --model --effort`:** o argparse ganha os dois (`brza-sessions:408-421`), o launch os anexa (`:456-457`), o `record('open')` grava `agent`, `model` e `effort` (`:471-472`) e o `session_map()` os dobra (`:102-103`). O `--effort` sem `--model` sai 1 antes do launch, como o `brza agent launch`. O `launch.py` da reunião sai.
- **`send`:** o `send_to_chat` passa a devolver o resultado (`brza_runtime.py:130-145`); o recibo é `queued` (com `position` e `message_id`), `accepted`, `rejected` (com o `refusal`, quando `ok: false`) ou `unknown` (timeout). Vários nomes ou `--prefix`, `--text` ou `--file`; a forma posicional de hoje fica. `--operation` só com um nome. Cada envio grava `send` no mapa. Saída 0/1/75 pela R2.1 do PLN-010.
- **`wait`:** polling do `session.tabs.listAll` a cada 2 s, sem o `history` por aba. Fim de turno por chat: estado `done` ou `waiting`, `updatedAt` posterior ao último `send` desse chat e, se o recibo foi `queued`, o `message_id` fora do `queuedMessages`. `blocked` sai `blocked`; `task_complete` com `error` no rollout do Codex sai `failed`. Com `--marker`, o turno sem o marcador sai `ended_without_marker`. `--any` volta no primeiro. Cada fim grava `turn` no mapa, com a latência. Saída 0, 75 no timeout, 1 em erro. O `--json` dá `{"done": [...], "pending": [...], "timed_out"}`, que o gerador do painel lê.
- **`read --last`:** `agentSession.history` com `limit` pequeno, sem cursor: o último texto do assistente ou, em `blocked`, a pergunta pendente. O `read` completo com cursor segue no PLN-010.
- **`close --prefix`:** laço sobre o `close_command`; sai 1 se algum chat `working` ficou sem `--force`.

### P4b — a medição (~3,5 h)

```text
brza sessions list   [--prefix P] [--json]
brza sessions model  <nome> <modelo> [--effort E] [--json]
brza sessions usage  <nome>… [--prefix P] [--json]
```

- **`list`:** `agent`, `model`, `effort` do mapa; `updated_at` do `chatStatus`; `last_latency_s` e `last_turn_at` do último `turn`. Chaves só acrescentadas ao contrato do roteador do PLN-003.
- **`model`:** `agentSession.setOption` com `key: 'model'` e, em seguida, `key: 'effort'` (no Claude, escrever `model` retira a confirmação do `effort`); grava `model` no mapa. A recusa do Antigravity a modelo explícito é esperada.
- **`usage`:** Claude pelas linhas `turn` do `.measurements/measurements.jsonl` com o `claude_session`; Codex pelo último `token_count.info.total_token_usage` do rollout em `~/.codex/sessions/**/rollout-*-<provider_session>.jsonl`, só tokens; Grok e Antigravity `{"measured": false, "reason": "unmeasured"}`. Não toca o `measure.py` (PLN-012 e PLN-015 seguem donos dele).

### P5 — o `brza shot` (~1 h, na `master` do `brza-workspace`)

O `string_concat` de `scripts/brza/brza-shot:162-166` só lê literais; o Studio passou a `const BASE_CSS = visualBaseCss(true)` com template `${scrollbars}` (`brza-studio/src/shared/native-chat/native-chat-visual-shell.ts:101-106`). Um `base_css_call` acha a chamada, lê o ternário e o template e troca `${scrollbars}` pelo ramo do argumento; o literal antigo segue aceito. Teste em `scripts/brza/tests/test_brza_shot.py` com a fixture na forma nova. O `brza-shot` não está no `core.lock`.

### P6 — a emenda ao PLN-010 (~0,5 h)

Registrar no PLN-010 a exceção à R1.4, citando PLN-017/R3.1 com a resposta literal e a data: o recibo, a `--operation` e o `read --last` saem pelo `rpc` até o `brza chat` existir no app alvo; quando existir, o PLN-010 troca o transporte (~0,5 h) e a exceção cai.

## Como se prova

- `python3 -m unittest discover -s tests/cli -p test_brza_sessions.py` no `brza-workflow`, com `env -u BRZA_WORKSPACE` (com a variável da sessão, quatro testes de checkout relativo falham por ambiente): os 47 de hoje mais os novos do D2, um por verbo.
- A sonda com chats reais, uma vez, antes do código: o `setOption` `model` num Claude e num Codex; o reenvio com a mesma `operation` depois de o fence mudar; o `updatedAt` ao entrar em `working`; o `state` de um Grok e de um Antigravity num turno.
- Uma reunião curta (P7 do PLN-017) rodando sem o `launch.py`.

## O que fica de fora

- O embrulho MCP dos verbos (R1.2: depois de duas reuniões pelo CLI).
- O `read` completo com cursor e o recibo pelo `brza chat` (PLN-010, bloqueado no PLN-011).
- O fallback de runtime quando a cota cai: o `wait` só o mostra como `failed`; a troca é da skill (manifesto com `fallback`).
- Medir o Codex em US$ (issue `codex-e-antigravity-sem-medida-por-tarefa` do `tools-kit`).
