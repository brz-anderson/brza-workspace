---
scope:
  - brza-workflow
refs:
  - PLN-012
  - REV-019
  - issue:o-brza-run-copia-o-provider-session-e-le-o-workstream-pelo-hook
---

# O P4 do PLN-012, o brza run que mede

O pedido de Anderson, em 2026-11-06, na sessão "Plano: medir a produtividade por tarefa (tools-kit)", trazido à
sessão `pln012-p4`: "inicie os passos em paralelo". É o P4 do
[PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md),
"O `brza run` mede", que executa o D5.

## O que se fez

- **O `run_here` mede o comando.** Ele lê o `getrusage(RUSAGE_CHILDREN)` antes e depois do `pty.spawn`, e o
  `time.monotonic()` em volta dele. Devolve `(code, output, metrics)`, com `duration_s`, `cpu_s` (usuário e sistema) e
  `max_rss_mb`.
- **O `run_for_result` grava as métricas no `result.json`**, que continua com o `code`:
  `{"code", "duration_s", "cpu_s", "max_rss_mb"}`.
- **O lado de fora grava a linha `run`** no `.measurements/measurements.jsonl` da raiz do workspace, achada pelo
  `brza_root.find`, com a `BRZA_WORKSPACE` antes:
  - o `run_in_tab` grava com o `CLAUDE_CODE_SESSION_ID` do ambiente;
  - o `run_in_chat`, o ▶, grava com o `chat_id` e o `session_id` do `provider_session(chat)`, ou `null`;
  - a linha leva `event`, `timestamp`, `session_id`, `chat_id`, `mode`, `cwd`, `workstream`, `command` (até 200
    caracteres), `code`, `duration_s`, `cpu_s` e `max_rss_mb`.
- **A medida nunca muda o resultado.** Sem workspace, ou quando a gravação falha, a linha não sai e o stderr avisa. Os
  blocos impressos, o código de saída e o fechamento da aba com 0 ficam como estavam.
- **Os testes:** o `tests/cli/test_brza_scripts.py` passou de 27 para 41. Os 14 novos cobrem:
  - a CPU, o pico e a duração de um comando que gasta 0,3 s e aloca 80 MB, e a CPU como diferença;
  - o `result.json` com o `code` e as métricas;
  - a linha da aba com a sessão do ambiente, com o comando real e com o `result.json` de fixture;
  - o workstream de um worktree `workstream/demo`;
  - sem workspace, e com o log que não se grava;
  - o ▶ com a sessão do app, sem o app, com o `result` nulo, com o `KeyError` do runtime, sem workspace e com o
    comando que apaga o próprio cwd.
- **A revisão** foi em duas rodadas do `agy` (Gemini 3.8 Flash high) e na rodada final do `reviewer` do Claude Code,
  que também conferiu as correções. O parecer é
  [REV-019: A revisão do P4 do PLN-012, o brza run que mede](../reviews/REV-019-pln-012-p4-o-brza-run-mede.md):
  - seis achados `corrigido aqui`, todos feitos pelo subagente `implementer` e conferidos;
  - dois que vão à issue
    [O brza-run copia o provider_session e lê o workstream pelo hook de medição](../issues/o-brza-run-copia-o-provider-session-e-le-o-workstream-pelo-hook.md).
- **Executado:** 1,1 h, de 18:22 a 19:30.

## Evidência

- `brza-workflow@aa752e6`, na branch `feat/pln-012-p4`, com push. Os commits do passo são `c0554e6`, `d768a63`,
  `4292746` e `aa752e6`, todos com `brz.anderson.pereira@gmail.com`.
- `python3 -m unittest tests/cli/test_brza_scripts.py` → `Ran 41 tests`, OK.
- `python3 -m unittest discover -s tests/cli` → `Ran 506 tests`, OK.
- O teste que falha veio antes do código: sobre `591f0ed`, os 8 primeiros testes novos falharam (7 FAIL, 1 ERROR), e
  os de antes passaram.

## Desvios do D5

- **X1 — A CPU é a diferença em volta do comando**, e não só o "depois" do D5. O processo do `brza-run` já colheu filhos
  `git` no import do `brza_runtime` (0,012 s), e na suíte os filhos se somam. Um teste prende a diferença.
- **X2 — O `provider_session` é uma cópia** do `brza-sessions:244-250`, e não um import. O `brza-sessions` não se
  importa, porque o nome tem hífen, e o `runpy` dele traria o resto do script. A cópia aceita o `result` nulo e pega as
  exceções do envio vizinho; a unificação vai à issue.
- **X3 — O `workstream` vem do `workstream_of` do `measure.py`, por `runpy`**, para a linha `run` casar com as do
  `turn`. O D5 não diz de onde vem. A extração para o `brza_root` vai à issue, porque o P1 edita o `measure.py` em
  paralelo.
- **X4 — O ▶ guarda o cwd antes do comando**, porque o comando pode apagá-lo (REV-019 A1). O D5 diz só que o ▶ grava a
  linha.
- **X5 — O `ru_maxrss` vem em bytes no macOS e em KB no Linux**, e os dois se convertem para MB. O F5 só fala do
  macOS.
- **O `chat_id` da aba sai `null`**, como no exemplo do D5, mesmo com o `ORCA_AGENT_SESSION_ID` no ambiente. Isso não é
  desvio; fica escrito porque a revisão perguntou.

## O que ficou

- A issue da cópia do `provider_session` e do `runpy` do `measure.py`.
- A memória do `reviewer` em `.claude/agent-memory/reviewer/` foi gravada pelo `reviewer` deste passo e pelo do P1,
  nos mesmos arquivos. Ela fica fora deste commit, para a sessão que conduz juntar.
- O `[x]` do P4, o `Executado` e as horas do plano são da sessão que conduz.

## Fora do workspace

Nada mudou fora do workspace e do `brza-workflow`; os pedidos e as devoluções da revisão ficaram em `/private/tmp/pln012-p4/`.
