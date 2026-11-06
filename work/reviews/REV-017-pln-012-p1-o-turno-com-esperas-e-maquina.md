---
status: done
description: As revisões do P1 do PLN-012 — o turno com as esperas, o começo do pedido e a máquina —, com os achados e o destino de cada um
scope:
  - brza-workflow
opened: 2026-11-06
completed: 2026-11-06
tags:
  - tooling
---

# REV-017: O P1 do PLN-012, revisado pelo agy e pelo reviewer

O parecer do P1 do
[PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md),
que executa o D2 em `core/.claude/hooks/measure.py` do `brza-workflow`, na branch `feat/pln-012-p1`. Três rodadas pelo
`agy` (`gemini-3.8-flash-high`, `--mode plan`, com o corpo do `reviewer` no prompt) e uma rodada final pelo subagente
`reviewer` do Claude Code (Opus), com uma conferência da correção pelo mesmo `reviewer`. Os achados de código foram ao `implementer`; todos
saíram `corrigido aqui`. Os pareceres completos ficaram no scratch da sessão (`/tmp/pln012-p1/agy-r{1,2,3}.md`).

## As rodadas

| Rodada | Revisora | Diff | Achados | Destino |
| :----- | :------- | :--- | :------ | :------ |
| 1 | `agy` | `591f0ed..2c80b3d` | A1, A2, A3 | corrigido em `f8ed8a8` |
| 2 | `agy` | `591f0ed..f8ed8a8` | A4 | corrigido em `9b5b272` |
| 3 | `agy` | `591f0ed..9b5b272` | nenhum; os 5 desvios se sustentam | — |
| final | `reviewer` (Opus) | `591f0ed..9b5b272` | A, B, C, D | corrigido em `8bffb20` |
| conferência | `reviewer` (Opus) | `9b5b272..8bffb20` | A–D fechados; E e o ponto F | corrigido em `7f38397` |

## Os achados

- **A1 · alta · 95 — o delta de CPU negativo caía no acumulado.** A marca `machine:<pid>` era arredondada a 4 casas;
  um turno sem CPU dava delta de `-1e-5` e a regra `d if d >= 0 else r[key]` devolvia a CPU da vida inteira do
  `claude`. Agora a marca guarda o float exato e o delta do mesmo processo é `max(d, 0)`.
- **A2 · média · 95 — o comando de skill não era reconhecido.** O `/plan-runner` grava `<command-message>` antes do
  `<command-name>`; o `match` falhava e o comando virava o `prompt_head`.
- **A3 · média · 90 — o `<system-reminder>` contava como pedido**, com espera falsa e `prompt_head` errado.
- **A4 · baixa · 82 — a tag `<command-name>` citada no corpo de um pedido o tornava comando.** O `agy` recomendou issue;
  saiu `corrigido aqui` pela memória do workstream ("prefira sempre optar por `corrigir aqui`"), com a regex ancorada
  `COMMAND_LINE`, também no `head_of`.
- **A · média · 95 — o resumo da compactação (`isCompactSummary`) virava o `prompt_head`.** As 4 compactações dos 400
  transcripts mais recentes davam "This session is being continued…" no lugar do pedido.
- **B · média · 95 — o modo `!`.** `<bash-stdout>` e `<bash-stderr>` contavam como pedido, e o caveat com data fora de
  ordem punha a espera antes do relógio: um trecho real dava `waits_s [120]` com `duration_s 33`, e o `agente` do D4
  sairia −87 s. Agora a saída não é pedido, o `<bash-input>` sai como "! comando" e nenhuma espera começa antes do
  `start` do trecho.
- **C · baixa · 90 — o caveat `isMeta` era a "linha anterior".** Ele vem com a data do comando local que antecede, e a
  espera que terminava num `/model` ou `/compact` sumia; 83 min parados contavam como agente num caso real. A linha
  `isMeta` não atualiza mais a linha anterior da conversa.
- **D · baixa · 95 — o filtro de `origin.kind` não tinha teste que o barrasse** (a mutação `if False:` passava). Teste
  com `origin.kind: peer` e texto comum.
- **E · baixa · 95 — o recorte da espera ao `start` não tinha teste que o barrasse:** a fixture tinha uma linha que já
  movia a linha anterior para dentro do relógio. A fixture mudou, e a mutação do recorte agora derruba o teste (129 contra
  `duration_s` 33).
- **F (ponto para rodada, pela opção recomendada) — o `! comando` disputava o `prompt_head` com o pedido escrito.** Ele
  agora é como o `/comando`: só vira o head quando o trecho não tem outro pedido.

## Hipóteses que caíram

- O struct `rusage_info_v4` e a conversão pelo `mach_timebase_info`: batem com o `sys/resource.h` do SDK e com o
  `time.process_time()` (razão 0,99); o buffer tem folga sobre os 296 bytes do flavor 4.
- A trava do `state.json`: o `ps` roda fora dela; a marca é lida e escrita sob o mesmo `flock`.
- A linha `subagent` e o avanço da leitura: sem mudança.
- A espera da pergunta e a de um pedido novo contadas duas vezes: em 377 `AskUserQuestion` reais, nenhum pedido chegou
  com uma pendente; o pedido digitado no meio do turno chega como `attachment` `queued_command`.
- A `CLAUDE_PID` herdada ou velha [F19]: o Claude Code 2.1.319 põe `CLAUDE_PID: String(process.pid)` no ambiente de
  todo hook (`strings` no binário). O P6 deve ver `machine.from: "env"`.
- A interface para o P3: `machine_of(pid, origin, last)` devolve a máquina do turno em curso e a marca, que o P3
  descarta; ela levanta quando a leitura falha.

## Os desvios do D2

Os cinco desvios do texto do D2, julgados nas rodadas 2, 3 e final, se sustentam; estão no worklog do passo.

## Verificação

- `python3 -m unittest discover -s tests/hooks` → 317 OK em `brza-workflow@7f38397`.
- O `measure()` sobre os 400 transcripts mais recentes de `~/.claude/projects`, cortados em cada
  `stop_hook_summary` (1335 trechos com chamada à API): nenhum trecho com `Σ waits_s > duration_s`, nenhum
  `prompt_head` de compactação, nenhuma espera perdida por caveat nem contada no modo `!`.
