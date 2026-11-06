---
status: done
description: As rodadas do agy e a final do reviewer sobre o P4 do PLN-012, com os achados e o destino de cada um
scope:
  - brza-workflow
opened: 2026-11-06
completed: 2026-11-06
tags:
  - tooling
---

# REV-019: A revisão do P4 do PLN-012, o brza run que mede

O parecer do P4 do
[PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md),
"O `brza run` mede", que executa o D5. O alvo é a branch `feat/pln-012-p4` do `brza-workflow`, de `591f0ed` a
`aa752e6`, nos arquivos `packages/client/bin/brza-run` e `tests/cli/test_brza_scripts.py`. A régua foi o D5, os fatos
F5, F12 e F23 do Desenho, e o P4, a Cobertura (`Pedido 3`, `R1.2`) e a Regressão do `brza run` no plano.

Houve duas rodadas do `agy -p --model gemini-3.8-flash-high --mode plan`, só leitura, com o corpo do papel `reviewer`.
Depois veio a rodada final do `reviewer` do Claude Code, que também conferiu as correções dela. As devoluções inteiras
ficaram no scratch, em `/private/tmp/pln012-p4/`.

## As rodadas

| Rodada | Revisor | Sobre | Achados | Destino |
| :----- | :------ | :---- | :------ | :------ |
| 1 | `agy` | `c0554e6` | A1 o `workstream_of` pelo `runpy` do `measure.py`; A2 a cópia do `provider_session`; A3 o teste do workstream não rodava o comando; A4 o `result` nulo do RPC derrubava o ▶ | A1 e A2 → issue; A3 e A4 corrigidos em `d768a63` |
| 2 | `agy` | `d768a63` | refez A1 e A2 como issue e A3 e A4 como corrigidos; A3 novo: o ▶ sem workspace não tinha teste | corrigido em `4292746` |
| final | `reviewer` | `4292746` | A1 a A5, abaixo | A1–A3 corrigidos em `aa752e6`, conferidos pelo mesmo `reviewer`; A4 e A5 → issue |

## A revisão final

### A1 — No ▶, o cwd é lido depois do comando, e o comando que apaga o próprio cwd derruba o brza-run

> bug · importante · confiança 90 · → corrigido aqui, em `aa752e6`

**Evidência:** em `packages/client/bin/brza-run:184`, o `record_run(..., Path.cwd(), ...)` ficava fora de qualquer
`try`. A sonda `run_in_chat(f'rmdir {cwd}; exit 3', 'claude_x')` deu `FileNotFoundError`, o código 1 no lugar do 3 e
nenhuma linha. O ▶ abre a aba no worktree do chat (`brza-studio/src/renderer/src/components/native-chat/brza/BrzaRunCodeButton.tsx:32`).
Corrigido: o `cwd` é guardado antes do `run_here` (`brza-run:177`). O teste
`test_chat_mode_keeps_the_line_when_the_command_removes_its_own_cwd` cai na mutação que desfaz a correção.

### A2 — O provider_session só pegava BrzaError, e a falha que o envio tolera derrubava a medida do ▶

> bug · sugestão · confiança 90 · → corrigido aqui, em `aa752e6`

**Evidência:** o `except runtime.BrzaError` ficava na `brza-run:171`, e o envio vizinho pega `(OSError, ValueError,
KeyError, BrzaError)`. Com o `orca-runtime.json` sem `authToken`, a sonda deu `KeyError 'authToken'` e nenhuma linha.
Corrigido: o `except` agora pega `(OSError, ValueError, KeyError, AttributeError, runtime.BrzaError)`. O teste
`test_chat_mode_survives_an_rpc_that_raises_key_error` cai em duas mutações.

### A3 — Nenhum teste prendia a CPU como diferença em volta do comando

> lacuna · sugestão · confiança 95 · → corrigido aqui, em `aa752e6`

**Evidência:** a mutação `round(cpu_of(after), 2)` passava os 38 testes. Corrigido: o teste
`test_the_cpu_is_the_difference_around_the_command` colhe um filho de ~1 s de CPU antes do `run_here('true')` e exige
`cpu_s < 0.5`. A mutação dá `AssertionError: 2.22 not less than 0.5`.

### A4 — A cópia do provider_session já divergiu do original

> desvio · sugestão · confiança 90 · → issue [O brza-run copia o provider_session e lê o workstream pelo hook de medição](../issues/o-brza-run-copia-o-provider-session-e-le-o-workstream-pelo-hook.md)

**Evidência:** o `(found or {})` entrou só em `brza-run:173`. O `packages/client/bin/brza-sessions:250` segue com
`found.get(...)` e levanta `AttributeError` com o `result` nulo, igual no `master`. Mover a função ao `brza_runtime`
obriga a refazer o patch do `rpc` em `tests/cli/test_brza_sessions.py:67,152,261` e a injeção em
`tests/cli/test_brza_note.py:160-164`.

### A5 — O workstream_of carrega o measure.py inteiro pelo runpy

> desvio · sugestão · confiança 90 · → issue [O brza-run copia o provider_session e lê o workstream pelo hook de medição](../issues/o-brza-run-copia-o-provider-session-e-le-o-workstream-pelo-hook.md)

**Evidência:** a chamada custa de 35 a 58 ms (`runpy` e `git`) e dá `tools-kit` no worktree dele. O `except` largo
não esconde uma renomeação, porque o `test_the_line_carries_the_workstream_of_the_cwd` cai com `'workstream': None`.

### A6 — A CPU como diferença, e não só o "depois" do D5, seria um desvio errado

> desvio · importante · confiança 95 · → falso

**Por que é falso:** o import do `brza_runtime` já colhe filhos `git` antes do `pty.spawn`, e a diferença tira esse
gasto do comando.

**Evidência:** o `getrusage(RUSAGE_CHILDREN)` logo depois do import deu cpu 0,012 s e maxrss 4,7 MB.

### A7 — Na aba, o chat_id deveria levar o ORCA_AGENT_SESSION_ID

> desvio · sugestão · confiança 95 · → falso

**Por que é falso:** o exemplo do D5 traz `"chat_id": null, "mode": "tab"`, e o P2 liga a linha pela `session_id`.

**Evidência:** o D5 em `PLN-012-design.md` e o `summarize_measurements.py:611,734-738` do `feat/pln-012-p2`.

### A8 — O ▶ não deveria achar o workspace pelo cwd

> desvio · sugestão · confiança 95 · → falso

**Por que é falso:** o app abre a aba do ▶ no worktree do chat. O defeito estava no momento da leitura, que é o A1.

**Evidência:** `BrzaRunCodeButton.tsx:32`, `startupCwd: context.worktreePath`.

### A9 — A linha run iria a um log diferente do log do hook

> bug · importante · confiança 95 · → falso

**Por que é falso:** o `brza_root.find` leva o worktree do workstream e o do código à raiz do workspace, que é a mesma
`ROOT` do `measure.py`.

**Evidência:** `find` de `.worktrees/tools-kit` dá `brza-workspace` com o papel `notes`, e o de `brza-studio/.worktrees`
dá o mesmo com o papel `code`.

### A10 — O zsh interativo infla a CPU e a duração do comando

> bug · sugestão · confiança 90 · → falso

**Por que é falso:** o custo do `zsh -ic` com o `.zshrc` real fica abaixo de um décimo de segundo.

**Evidência:** `run_here('true')` deu `{'duration_s': 0.06, 'cpu_s': 0.04, 'max_rss_mb': 5}`.

## O que rodou

- `python3 -m unittest tests/cli/test_brza_scripts.py` → 41 OK em `aa752e6`.
- `python3 -m unittest discover -s tests/cli` → 506 OK em `aa752e6`.
- As sondas `probe.py` e `probe2.py` do `reviewer`, que deram os A1 e A2, e as mutações em cópia: cada teste novo cai
  quando a correção dele é desfeita.
