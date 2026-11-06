---
scope:
  - brza-workflow
refs:
  - PLN-012
  - REV-017
---

# O P1 do PLN-012, o turno com as esperas, o começo do pedido e a máquina

O pedido de Anderson, em 2026-11-06, na sessão "Plano: medir a produtividade por tarefa (tools-kit)": "inicie os
passos em paralelo". A sessão `pln012-p1` executou o P1 do
[PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md),
que executa o D2, no worktree `.worktrees/pln-012-p1` do `brza-workflow`, na branch `feat/pln-012-p1`, saída da
`feat/pln-012-medida-por-tarefa` (`591f0ed`).

## O que se fez

- **A linha `turn` ganha três campos** em `core/.claude/hooks/measure.py`; a `subagent` não muda:
  - `waits_s`: a espera de cada `AskUserQuestion`, do `tool_use` ao `tool_result`, mesmo recusada, e a de cada
    pedido depois do primeiro do trecho, desde a linha anterior da conversa;
  - `prompt_head`: os 80 primeiros caracteres do primeiro pedido, numa linha;
  - `machine`: `{pid, from, cpu_self_s, cpu_children_s, rss_mb, footprint_mb}`, pelo `proc_pid_rusage(pid,
    RUSAGE_INFO_V4)` por `ctypes`, convertido pelo `mach_timebase_info`. O pid vem da `CLAUDE_PID` (`env`) ou da subida
    pelos `ppid` até o executável `claude`, em até 6 níveis (`ppid`). O delta é contra a marca `machine:<pid>` do
    `state.json`, gravada sob a trava que já existia. A leitura que falha deixa `machine: null`, e a linha sai.
- **As funções:** `measure()` devolve `waits_s` e `prompt_head` no segundo dicionário. `turn()` grava os três campos.
  `claude_pid()`, `ps_entry(pid)`, `proc_pid_rusage(pid)` e `machine_of(pid, origin, last)` são novas. O
  `machine_of` é puro: devolve a máquina e a marca nova, e o P3 pode chamá-lo para o turno em curso sem gravar estado.
- **Os testes**, em `tests/hooks/test_measure.py`: 26 novos, nas classes `WaitsAndHeadTest`, `MachineTest` e
  `RealRusageTest`. A última roda a leitura de verdade no macOS e confere que um filho de 0,4 s de CPU aparece em
  `cpu_children_s`.
- **Conferido na máquina:** sem a `CLAUDE_PID`, a subida pelos `ppid` achou o `claude` desta sessão (91260, o mesmo da
  `CLAUDE_PID`), com 6,49 s de CPU própria, 12,14 s dos filhos e 387 MB de RSS.
- **Revisão:** três rodadas do `agy` e uma final do `reviewer` (Opus), no
  [REV-017: O P1 do PLN-012, revisado pelo agy e pelo reviewer](../reviews/REV-017-pln-012-p1-o-turno-com-esperas-e-maquina.md).
  Os 9 achados (A1–A4, A–E) e o ponto F foram corrigidos aqui pelo `implementer`, e nenhum foi a issue.

## Os desvios do D2

O texto do D2 foi seguido, salvo estes desvios, que as rodadas julgaram sustentados:

1. **A "linha anterior" da espera é a última linha `user` ou `assistant` que não é `isMeta`.** Nos transcripts reais,
   a `queue-operation` e o `hook_success` do próprio pedido vêm logo antes dele, em 446 e 123 de 200 transcripts, e
   zerariam a espera. O caveat `isMeta` vem com a data do comando que antecede (achado C).
2. **Não são pedido**, nem para a espera nem para o `prompt_head`:
   - `<local-command-stdout>`/`stderr`, `<bash-stdout>`/`stderr`, `[Request interrupted by user…`,
     `<task-notification>` e `<system-reminder>`;
   - a linha `isCompactSummary`;
   - a linha com `origin.kind` diferente de `human`.

   Nenhuma delas é pedido de Anderson. A marca da interrupção conta como linha anterior, e por isso o pedido que
   segue um Esc espera desde ela.
3. **O `prompt_head` pula o comando digitado.** Comando é a linha que começa por `<command-name>`, ou por
   `<command-message>` e depois `<command-name>`. O comando só vira o `prompt_head`, como "/nome args", quando o trecho
   não tem outro pedido. A sessão aberta pelo `brza sessions --rename` começa por `/rename`, que esconderia o pedido
   real do aviso do `close-task` (D6). O `<bash-input>` é pedido, e sai como "! comando", mas, como o `/comando`, só vira o head sem pedido escrito.
4. **A espera que arredonda a 0 s fica fora da lista**, como o pedido colado no `/rename` que abre a sessão.
5. **A marca `machine:<pid>` guarda também o `start` do processo.** Um pid reaproveitado mede desde o começo do processo
   novo, e o delta do mesmo processo nunca é negativo.
6. **Nenhuma espera de pedido começa antes do `start` do trecho.** O caveat e o `<bash-input>` vêm com data fora de
   ordem, e sem isso a soma das esperas passava do `duration_s` (achado B).

**Ficou fora do passo:** a linha do `turn` na tabela do hook, no `core/CLAUDE.md`, é do P5, que edita esse arquivo.

## Evidência

- `brza-workflow@7f38397`, na `feat/pln-012-p1`, com push. Os commits do passo são `2c80b3d` (o P1), `f8ed8a8` (A1–A3),
  `9b5b272` (A4), `8bffb20` (A–D) e `7f38397` (E–F).
- `python3 -m unittest discover -s tests/hooks` → 317 OK. Os testes de hoje do `test_measure.py` e do
  `test_measure_workstream.py` passam sem mudança, como a Regressão pede.
- O `measure()` rodou sobre os 400 transcripts mais recentes, em 1335 trechos com chamada à API. Nenhum trecho tem
  `Σ waits_s > duration_s`, e nenhum tem o resumo da compactação como `prompt_head`.
- **Executado:** 1,1 h, das 18:22 às 19:27.

## O que ficou

- **O subpasso 4, a conferência na sessão real, fica para o P6.** Depois do `brza sync`, um turno com um comando de
  2 s de CPU: `machine.from` deve sair `env` (o Claude Code 2.1.319 põe a `CLAUDE_PID` no ambiente de todo hook, lido
  no binário), e `cpu_children_s` ≥ 2.
- Juntar a `feat/pln-012-p1` na `feat/pln-012-medida-por-tarefa` e marcar o `[x]` do P1 no plano: é da sessão que
  conduz.
