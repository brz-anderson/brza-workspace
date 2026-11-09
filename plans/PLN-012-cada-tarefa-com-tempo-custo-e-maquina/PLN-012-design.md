# PLN-012 — Desenho

> **Desenho fechado em 2026-11-03**, das rodadas R0 a R4 da Entrevista, no
> [PLN-012](PLN-012-plan.md). O rascunho veio de um `designer`; os fatos marcados `[Fn · …]` têm a fonte na linha.

## O que este desenho assume

- **R0.1, R0.2:** o workstream é o `tools-kit`, em sessão nova.
- **R1.1, R2.1:** a tarefa é o worklog. O `brza note commit` carimba nele o `CLAUDE_CODE_SESSION_ID` e grava um evento
  `task` na medição; a tarefa começa no primeiro turno depois do marco anterior da mesma sessão; o intervalo entre os
  dois é a ociosa da sessão.
- **R1.2:** a máquina é a CPU e o RSS do `claude` com os filhos e netos que saíram, e o rusage do comando do
  `brza run`. A leitura é o `proc_pid_rusage` da `libproc`, e não o `ps -S`, que não soma os filhos de outro processo
  no macOS (D2) — a mesma intenção da R1.2, sem rodada.
- **R1.3:** a tarefa sem turno medido aparece "não medida", e toda lacuna deixada vira issue (D7).
- **R1.4, R3.1:** a medida aparece no `summarize_measurements.py --by-task` e numa seção `## Medida` do worklog, que
  lê o turno em curso no transcript até o commit — "Lê o turno em curso (Recomendado)".
- **R2.2, R2.3:** três tempos — agente, Anderson, pausa acima de 30 min por espera — e o corrido como a soma.
- **R2.4, R3.3:** o resumo mostra os turnos "sem tarefa" por sessão; o `close-task` mostra o que o commit vai fechar e
  os turnos sem tarefa das outras sessões do workstream — "Este commit + outras sessões (Recomendado)".
- **R3.2 (fecha a R0.3):** o worklog não ganha `opened` nem hora em `completed`; a hora fica na `## Medida` — "Não; a
  hora fica na Medida (Recomendado)".
- **R3.4:** a sessão que emendou duas tarefas sem worklog entre elas corta com `brza note commit --until HH:MM` —
  "--until HH:MM (Recomendado)".
- **R4.1:** a medida por tarefa começa no primeiro evento `task` do log, sem dado retroativo — "Começa no deploy
  (Recomendado)".

## Terreno

### O worklog e as datas

- **O frontmatter do worklog guarda só `scope`, `tags` e `refs`; a data mora no nome.** `work/README.md:310-311`.
  `opened` e `completed` são "Data" na tabela comum (`work/README.md:229`, `:231`).
- **O esqueleto do worklog não tem `opened`.** `brza-workflow/bin/brza-note:188-201`, a constante `WORKLOG`.
- **O `close-task` cria o worklog à mão, quando a tarefa fecha**, sem o `brza note new worklog`.
  `brza-workflow/core/.claude/skills/close-task/SKILL.md:30-32`. Por isso um `opened` carimbado na criação marcaria a
  escrita da nota, minutos antes do fim, e o `completed` com hora repete o `git log --format=%aI` do worklog.

### A medição

- **A linha `turn` não diz a tarefa nem o nome da sessão.** As chaves da última linha de
  `.measurements/measurements.jsonl`: `account`, `agents`, `api_calls`, `bridge_session_id`, `cwd`, `denial_reasons`,
  `denials`, `duration_s`, `effort`, `estimated_cost_usd`, `event`, `max_context`, `model`, `plugin_versions`,
  `prompts`, `rounds`, `segment`, `session_id`, `skills`, `timestamp`, `tokens`, `tool_calls`, `workstream`.
- **O `measure.py` não lê CPU nem memória.** `grep -n 'cpu\|rusage\|psutil\|rss'` em
  `brza-workflow/core/.claude/hooks/measure.py` → nada.
- **O `summarize_measurements.py` mora em `core/scripts/`**, e não em `scripts/` do `brza-workflow`.
- **Ligar turno a tarefa hoje é inferência por cwd e hora, e erra.** Entre 18:50 e 21:30 de 2026-11-03, três sessões se
  intercalaram, e sessões rodando em `.worktrees/workspace` escreveram worklogs do `playground` com
  `workstream: workspace` (levantado pela sessão do `playground`).
- **Há sessão sem medida.** 3 dos 6 worklogs do `playground` de 2026-11-03 não têm turno medido (idem).

### O que já liga a sessão à tarefa

- **A sessão enxerga o próprio id.** `CLAUDE_CODE_SESSION_ID` está no ambiente do `Bash` da sessão, e é o mesmo id do
  `claude_session` do mapa de sessões (`08e6c812-…` nesta sessão). Um comando que a sessão roda, como o
  `brza note commit`, pode gravá-lo sem a sessão digitar nada.
- **O transcript guarda o nome da sessão**, nas linhas `custom-title` e `agent-name`
  (`~/.claude/projects/…-tools-kit/4a578e01-….jsonl`: `customTitle: tools-kit-rev-pln009`).
- **O `brza sessions` já liga o nome e o título ao id.** `.sessions/sessions.jsonl`, desde 2026-10-29 22:31: 44
  aberturas (42 Claude, 1 Codex, 1 Antigravity), com o título no padrão "PLN-008 P8: …" e o `claude_session`.
- **Mas o mapa cobre a minoria da medição.** Desde 2026-10-29 22:31: 25 das 100 sessões com turno estão no mapa, com
  US$ 156 dos US$ 394 de turno e US$ 63 dos US$ 258 de subagente.

### A máquina

- **O `man ps` diz que o `-S` soma à CPU de um processo a dos filhos que já saíram, mas isso não vale para outro
  processo**: rodado, não soma (ver os acréscimos abaixo). O processo da sessão é o `claude` (`ps -p $PPID` no
  `Bash`: `/Users/andepb/.local/bin/claude`, 360 MB de RSS).
- **O `brza run` roda o comando numa aba do app, fora da árvore de processos da sessão.**
  `brza-workflow/packages/client/bin/brza-run:1-12`: abre uma aba visível e espera o comando.

### O começo do turno

- **O `duration_s` do turno vai da primeira linha do trecho novo do transcript à última**, e a primeira é o prompt.
  `brza-workflow/core/.claude/hooks/measure.py:342`, `:406-413`. O começo do turno é `timestamp − duration_s`, sem
  campo novo.
- **A espera numa pergunta com opções cai dentro do turno.** A ferramenta segura o turno até a resposta, e o
  `duration_s` soma o tempo de Anderson pensando na rodada (inferido do cálculo acima; a conferir no Desenho).

## Terreno — acréscimos do Desenho

### A máquina

- **O `ps -S` não soma os filhos de outro processo.** Um `bash -c` cujo filho gastou 3 s de CPU sai com `0:00.00` em
  `ps -S -o time -p <bash>`; o `claude` sai igual com e sem `-S` depois de um neto gastar 6 s [F1 · rodado · 95].
- **O `proc_pid_rusage(pid, RUSAGE_INFO_V4)` conta filhos e netos colhidos.** O mesmo `bash`, com o neto
  `sh → python` de 3 s: `child_cpu=3.01s` [F2 · rodado · 95]. No `claude` da sessão, `child_cpu` foi de 33,17 s a
  35,30 s em volta de um comando de 2 s pelo `Bash` [F3 · rodado · 95]. Os tempos vêm em unidade de
  `mach_timebase_info` (125/3 ns nesta máquina); o struct traz também `ri_resident_size` e `ri_phys_footprint`.
- **O `getrusage(RUSAGE_CHILDREN)` de quem espera o comando dá a CPU e o pico da árvore.** Um `zsh → python` que aloca
  300 MB: `cpu=1.03s`, `ru_maxrss=329744384`, em bytes [F5 · rodado · 95]. O pico é o do maior processo, não a soma.
- **O subagente roda no processo da sessão e herda o id dela.** No `Bash` de um `designer`, `PPID` = `CLAUDE_PID` =
  44452, o `claude` da sessão principal, e `CLAUDE_CODE_SESSION_ID` é o da sessão [F4 · rodado · 95].
- **Se o hook herda a `CLAUDE_PID`, não se sabe**; o P1 confere na sessão real [F19 · inferido · 50].

### O tempo

- **A espera da rodada está no transcript e dentro do `duration_s`.** Nesta sessão, as duas perguntas esperaram 459 s
  e 166 s entre o `tool_use` e o `tool_result`, dentro do turno de 21:59:33 a 22:17:30, de 1077 s [F7 · rodado · 95].
  O relógio do turno abre no primeiro pedido e fecha na última linha (`measure.py:338-343`, `:405-409`); o `tool_use`
  do `AskUserQuestion` já é guardado por id (`:371-372`) e casado no resultado (`:376-386`) [F8 · lido · 95].
- **O turno interrompido cai no trecho do seguinte, com a espera dentro.** `measure.py:525-526` [F9 · lido · 95].
- **O subagente cai num turno da mesma sessão.** Das 163 linhas `subagent` do log, 162 têm o `session_id` de uma
  sessão com turno, e 161 começam (`timestamp − duration_s`) dentro de um turno dela [F6 · rodado · 95].

### O worklog e o commit

- **O worklog é commitado mais de uma vez.** Desde 2026-10-29, 151 worklogs: 34 com um commit, 117 com dois ou mais;
  dos 249 commits, 230 tocam um worklog só [F14 · rodado · 90]. O `close-task` manda acrescentar ao worklog de hoje
  (`close-task/SKILL.md:27`) [F17 · lido · 95].
- **A tarefa mora quase toda no turno do commit.** Atribuindo cada commit ao turno do mesmo workstream aberto na hora
  dele (194 de 227 casam), a tarefa mediana tem 88% da duração e 77% do custo nesse turno, e 70 de 158 têm um turno
  só [F15 · rodado · 80]; 34 dos 194 casam com mais de uma sessão [F16 · rodado · 90].
- **O `refs:` é a forma a copiar.** `set_frontmatter_refs` (`brza-note:397-427`) e `prepare_worklog_refs` (`:623-649`)
  rodam antes do `git add` em `commit` (`:676-715`), que não escreve na medição [F10 · lido · 95].
- **O `brza-run` grava só o código de saída.** `run_here` usa `pty.spawn` (`brza-run:91-108`); `run_for_result` grava
  `{'code': code}` (`:122-128`) [F12 · lido · 95].
- **O `provider_session(chat)` liga o chat do app à sessão do Claude.** `brza-sessions:204-212` [F23 · lido · 95].
- **O checador não tem lista fechada de chaves do frontmatter** (`grep` no `check_notes.py`) [F26 · rodado · 85].

## D1 — O carimbo e o marco — `bin/brza-note` (P3)

- **Origem:** R1.1, R2.1, R3.4
- **Contexto:** a tarefa é o worklog; o `brza note commit` deixa no worklog a sessão que o fechou, e na medição o marco
  que corta a sessão em tarefas.

### Como fica

**O frontmatter do worklog** ganha `sessions:`, lista de ids na forma do `refs:`:

```yaml
---
scope:
  - workspace
refs:
  - PLN-012
sessions:
  - 08e6c812-8bb3-42fc-a47f-403fdb472ccd
---
```

- O `brza note commit` acrescenta o `CLAUDE_CODE_SESSION_ID` a `sessions:` de cada worklog pedido, sem repetir, antes do
  `git add` e junto do `refs:`. `set_frontmatter_refs` vira `set_frontmatter_list(text, key, values)`, usado pelos dois.
- Sem `CLAUDE_CODE_SESSION_ID` — terminal de Anderson, Codex, Antigravity, Grok —, o worklog não ganha carimbo, e o
  evento sai com `session_id: null`.

**O evento `task`**, uma linha por commit que tenha worklog, gravada depois do `git commit` e antes do push (também com
`--no-push`), no `.measurements/measurements.jsonl` da raiz do workspace (`brza_root.find`, a `BRZA_WORKSPACE` antes):

```json
{"event": "task", "timestamp": "2026-11-03T22:16:03-03:00",
 "session_id": "08e6c812-8bb3-42fc-a47f-403fdb472ccd", "bridge_session_id": null,
 "chat_id": "claude_2ead5f2f_c37e_41a1_8ef4_a299af008379", "session_name": "tools-kit-produtividade",
 "pid": 44452, "cwd": "/Users/andepb/Projects/brza-workspace/.worktrees/tools-kit", "workstream": "tools-kit",
 "worklogs": ["work/worklogs/2026-11-03-pln-012-abertura-da-produtividade-por-tarefa.md"],
 "commit": "539b744", "until": null}
```

- `chat_id` é o `ORCA_AGENT_SESSION_ID`, quando houver; liga a tarefa ao chat do app mesmo sem `session_id`.
- O commit recusado (checador, nada a commitar, `--until` inválido) não grava evento.

**O corte, `--until HH:MM`** (ou hora ISO): a hora do começo do primeiro turno da tarefa seguinte, como o
`--pending` a mostra (X2); o marco do evento vai à hora dada, gravada em `until`. Ela tem de cair
entre o marco anterior da sessão e agora; fora disso, o commit recusa antes de tocar o worklog. `HH:MM` é de hoje, no
fuso local.

**O marco e a janela:**

- **Cada commit com worklog é um marco da sessão**, qualquer worklog; o marco é o `until` ou, sem ele, o `timestamp`.
  O commit só de plano ou issue não é marco.
- **O segmento k** de uma sessão são os turnos dela cujo começo (`timestamp − duration_s`) cai em
  `[marco k−1, marco k)` — o começo antes do marco, para o turno que começa no `until` ir à tarefa seguinte (X2);
  o primeiro segmento começa no primeiro turno da sessão. O turno que contém o commit fica com
  a tarefa que ele fecha.
- **O worklog commitado mais de uma vez na mesma sessão** soma os segmentos que fecha; o segmento de um commit de outro
  worklog no meio vai a esse outro.
- **O worklog commitado em mais de uma sessão** soma os segmentos de cada uma; `sessions:` lista todas. O corrido é a
  soma por sessão, e não a união do relógio.
- **Dois ou mais worklogs no mesmo commit** dividem o segmento em partes iguais; 230 de 249 commits têm um só [F14].

## D2 — Os três tempos e a máquina no turno — `core/.claude/hooks/measure.py` (P1)

- **Origem:** R2.2, R2.3, R1.2, R3.3
- **Contexto:** o turno precisa trazer a espera de Anderson que o `duration_s` engole [F7], a CPU e o RSS do processo,
  e o começo do pedido, para o aviso do `close-task`.

### Como fica

**A linha `turn` ganha três campos**; a `subagent` não muda:

```json
"waits_s": [459, 166],
"prompt_head": "siga com o `PLN-012`",
"machine": {"pid": 44452, "from": "env", "cpu_self_s": 0.84, "cpu_children_s": 6.13,
            "rss_mb": 357, "footprint_mb": 209}
```

- **`waits_s`:** cada espera de Anderson dentro do turno, em segundos inteiros — a de cada `AskUserQuestion`, do
  `timestamp` da linha do `tool_use` ao da linha do `tool_result`, e, para cada pedido depois do primeiro do trecho que
  não é `isMeta`, o intervalo desde a linha anterior (o turno interrompido).
- **`prompt_head`:** os primeiros 80 caracteres do primeiro pedido do trecho que não é `isMeta`, com as quebras de linha
  trocadas por espaço.
- **`machine`:** o delta da CPU do `claude` desde o último turno do mesmo `pid`, e o RSS no fim do turno.
  - O `pid` vem da `CLAUDE_PID` e, sem ela, subindo os `ppid` até o processo cujo executável se chama `claude`, no
    máximo 6 níveis, por `ps -o ppid=,comm= -p`; `from` diz qual (`env`, `ppid`).
  - A leitura é `proc_pid_rusage(pid, RUSAGE_INFO_V4)` por `ctypes`, só com a biblioteca padrão, convertida pelo
    `mach_timebase_info`.
  - O `state.json` guarda, sob a trava que já existe, `machine:<pid>` → os últimos `cpu_self_s` e `cpu_children_s`; o
    primeiro turno de um `pid` mede desde o começo do processo.
  - Fora do macOS, ou se a leitura falha, `machine` sai `null`, e o resto da linha sai como hoje.

**As contas, no resumo (D4):**

```
agente   = Σ (duration_s − Σ waits_s)                por turno do segmento
anderson = Σ min(w, PAUSE_S)                          w = cada waits_s e cada intervalo entre turnos do segmento
pausa    = Σ max(w − PAUSE_S, 0)                      PAUSE_S = 1800
corrido  = agente + anderson + pausa
ociosa   = do fim do último turno do segmento anterior ao começo do primeiro deste (da sessão)
```

## D3 — A seção `## Custo da tarefa` no worklog — `bin/brza-note` (P3, P7)

- **Origem:** R1.4, R3.1, R3.2; o título, R6.1
- **Contexto:** o worklog leva a medida da tarefa ao git, para sobreviver à troca de máquina; o turno do commit é a
  maior parte dela [F15].

**Descartada — a linha sem o turno do commit** (a forma da R1.4): saía vazia em 70 de 158 tarefas [F15]. **Descartada
— completar no commit seguinte:** a última tarefa da sessão ficaria parcial. **Descartada — `opened` e `completed` com
hora no frontmatter (R3.2):** o `close-task` cria o worklog no fim, e o `opened` marcaria a escrita da nota.

### Como fica

O `brza note commit` escreve a seção como a última do worklog, e a reescreve a cada commit com a medida acumulada da
tarefa — todas as sessões e todos os segmentos até agora:

```markdown
## Custo da tarefa

Corrido 18 min — agente 7 min, Anderson 10 min, pausa 0 · US$ 2,35 (turnos 2,35, subagentes 0,00) · CPU 0,8 s do
`claude` e 6,1 s dos comandos, RSS até 357 MB · 1 turno, 1 sessão · até 22:16 de 2026-11-03, pelo `brza note commit`
```

- **O turno em curso entra até a hora do commit.** O `brza note commit` acha o transcript da sessão
  (`<CLAUDE_CONFIG_DIR ou ~/.claude>/projects/*/<session_id>.jsonl`), lê do byte em que o hook parou (`state.json`) até
  o fim, sem avançar o estado, e mede com o `measure()` do `measure.py`; a CPU em curso é o `proc_pid_rusage` da
  `CLAUDE_PID` menos o `machine:<pid>` do estado. O que o turno fizer depois do commit só aparece no `--by-task`.
- **Sem o transcript**, a linha sai com os turnos fechados e termina em "· sem o turno do commit".
- **Os números:** vírgula decimal; segundos abaixo de 1 min, minutos inteiros até 60 min, "1 h 12 min" acima.
- **Acréscimos na linha:** com `brza run` na tarefa, "· `brza run`: 2 comandos, CPU 14 min, pico 1,8 GB"; dividida,
  "· dividida com 1 outro worklog do commit".
- **Sem sessão**, a seção não é escrita.
- **O título antigo (R6.1):** até o P7 a seção se chamava `## Medida`. O comando reconhece os dois títulos ao
  reescrever e grava sempre o novo, e o worklog com `## Medida` troca no próximo commit dele, sem migração.
- **As datas (R3.2):** o frontmatter não ganha `opened` nem hora em `completed`; a hora do fim é a do "até".
- **A norma** (`core/work/README.md`): a linha `sessions` na tabela de propriedades — "lista dos ids das sessões que
  commitaram o worklog, mantida pelo `brza note commit`" —, e, na seção `work/worklogs/`, o `sessions:` no frontmatter
  e a `## Custo da tarefa` como última seção, escrita pelo comando e não à mão.

## D4 — `summarize_measurements.py --by-task` — `core/scripts/summarize_measurements.py` (P2)

- **Origem:** R1.3, R1.4, R2.4, R3.3, R4.1
- **Contexto:** a tabela que compara tarefas, com as não medidas e os turnos sem tarefa à vista.

**Descartada — `--backfill` retroativo (R4.1):** ligar commit a sessão por workstream e hora erra em 34 de 194
commits [F16], e é a inferência que o Terreno já mostrou falhar.

### Como fica

```
python3 scripts/summarize_measurements.py --by-task [--since AAAA-MM-DD] [--workstream <nome>] [--json]
python3 scripts/summarize_measurements.py --by-task --pending --session <id>
```

- **Começa no primeiro evento `task` do log** (R4.1); o `--since` só pode adiantar.
- **O turno da auditoria (`fact_audit: true`) fica de fora**, como no `--by-workstream`.
- **As funções** `task_segments(rows)` e `task_measure(rows_of_segment)` ficam no módulo, e o `brza-note` as usa por
  `runpy` (como o `sessions_module`, `brza-note:222-225`), para a `## Custo da tarefa` e a tabela darem o mesmo número.
- **Atribuição:** o turno vai ao segmento pelo começo (D1). O `subagent` e o `run` vão ao turno da mesma sessão que
  contém o começo deles (`timestamp − duration_s`) [F6]; fora de turno, ao segmento cujos marcos o contêm; sem sessão
  casada, a "sem tarefa".

**Tabela 1 — Tarefas, por workstream e dia** (o dia é o do nome do worklog):

| Coluna | Conteúdo |
| :-- | :-- |
| workstream, dia, tarefa | a tarefa é o worklog sem a data e sem `.md` |
| sessões, turnos | contagens |
| corrido, agente, Anderson, pausa | `h:mm` |
| US$ turnos, US$ subag., US$ total | soma do `estimated_cost_usd`, com `(+n s/ custo)` como no `money()` |
| CPU `claude`, CPU comandos | minutos, do `machine` |
| `brza run` | n, CPU em minutos, pico em MB |
| RSS máx | MB, o maior `rss_mb` dos turnos |

**Tabela 2 — Tarefas não medidas:** worklog, commit, hora, motivo — `sem sessão` (o `task` sem `session_id`) ou
`sessão sem turno` (a sessão aberta sem a função do shell).

**Tabela 3 — Sessões: ociosa e sem tarefa:** sessão (o `session_name` do `task`, ou os 8 primeiros caracteres do id),
workstream, ociosa (`h:mm`), turnos sem tarefa, US$ sem tarefa, desde. "Sem tarefa" é o turno depois do último marco da
sessão, ou de sessão que nunca commitou worklog.

**`--json`:** `{"tasks": [...], "unmeasured": [...], "sessions": [...]}`, cada tarefa com os campos da tabela 1 e a
lista `segments` (sessão, começo, fim, turnos).

**`--pending --session <id>`** imprime o aviso do `close-task` (D6): os turnos da sessão depois do último marco, com a
hora do começo e o `prompt_head`, o corrido e o custo; e a soma dos turnos sem tarefa das outras sessões do mesmo
workstream cujo último turno tem mais de 2 h. Sai 0 sempre; sem turno pendente, imprime "nada a fechar".

## D5 — O `brza run` mede o comando — `packages/client/bin/brza-run` (P4)

- **Origem:** R1.2
- **Contexto:** o comando roda numa aba do app, fora da árvore do `claude` [F12]; quem o espera é o `brza-run` da aba.

### Como fica

- `run_here` mede o que roda: `time.monotonic()` em volta do `pty.spawn` e, depois dele,
  `resource.getrusage(RUSAGE_CHILDREN)` — a CPU (`ru_utime + ru_stime`) e o pico (`ru_maxrss`, bytes no macOS) [F5].
  Devolve `(code, output, metrics)`.
- `run_for_result` grava `{"code": 0, "duration_s": 312.4, "cpu_s": 845.2, "max_rss_mb": 1840}` no `result.json`.
- `run_in_tab`, o lado de fora, no `Bash` da sessão, lê o `result.json` e grava a linha `run` com o
  `CLAUDE_CODE_SESSION_ID` do ambiente. Sem workspace (`BRZA_WORKSPACE` nem `brza_root`), não grava e avisa no stderr.
- `run_in_chat`, o ▶, grava a linha com `chat_id` e o `session_id` do `provider_session(chat)` [F23], ou `null` se o
  app não responde.

```json
{"event": "run", "timestamp": "2026-11-03T22:50:12-03:00", "session_id": "08e6c812-…", "chat_id": null,
 "mode": "tab", "cwd": "…/brza-studio", "workstream": "tools-kit", "command": "pnpm test",
 "code": 0, "duration_s": 312.4, "cpu_s": 845.2, "max_rss_mb": 1840}
```

- O `command` vai cortado em 200 caracteres. A CPU do `brza-run` de fora, que só espera, cai no `machine` do turno; a
  da aba, só aqui: nada conta duas vezes.

## D6 — O aviso do `close-task` — `core/.claude/skills/close-task/SKILL.md` (P5)

- **Origem:** R2.4, R3.3, R3.4
- **Contexto:** com a R2.1, o commit fecha tudo o que a sessão fez desde o marco anterior; o aviso mostra o que vai
  fechar, para a sessão separar duas tarefas emendadas, e o que ficou sem tarefa noutras sessões.

**Descartada — a leitura literal da R2.4** (os turnos desta sessão sem tarefa): contaria zero na hora do
`close-task`. **Descartada — só este commit (R3.3):** a sessão parada sem worklog só apareceria no resumo.
**Descartada — sem corte (R3.4):** somaria duas tarefas, o que a R2.4 recusou.

### Como fica

Passo novo no `close-task`, entre "1. Situar" e "2. O worklog de hoje":

````markdown
## 2. O que o commit vai fechar

```bash
python3 scripts/summarize_measurements.py --by-task --pending --session "$CLAUDE_CODE_SESSION_ID"
```

A saída lista os turnos desde o último worklog que esta sessão commitou — a hora e o começo do pedido de cada um — e
os turnos sem tarefa das outras sessões do workstream. **Se os turnos listados são de mais de uma tarefa**, feche antes
a mais antiga: o worklog dela e `brza note commit <worklog> --until <HH:MM>`, com a hora do fim do último turno dela; o
resto fica para o worklog da tarefa em curso. **Os turnos sem tarefa das outras sessões** se dizem a quem pediu, numa
linha, sem fechá-los daqui.
````

Exemplo de saída, com os turnos desta sessão depois do commit de worklog das 22:32:31:

```
este commit fecha 3 turnos desde 22:32 (corrido 10 min, US$ 0,65):
  22:32 > Grok CLI da xAI esse
  22:34 precisamos urgentemente adicionar o `grok` no fluxo do `brza sessions` e do `MCP`
  22:41 siga com o `PLN-012`
sem tarefa no workstream tools-kit: 12 turnos em 2 sessões paradas há mais de 2 h (US$ 3,40)
```

Aqui os dois primeiros são do grok: a sessão fecha o worklog dele com `--until 22:35`, e o terceiro fica para o do
Desenho do PLN-012. Os passos seguintes da skill renumeram de 3 a 7; o "Commitar" ganha a menção ao `--until`.

## D7 — As lacunas viram issue — `work/issues/` (P5)

- **Origem:** R1.3
- **Contexto:** "sempre abra issue para lacunas deixadas". As do Codex e do Antigravity e a do Grok já existem.

### Como fica

Uma issue por lacuna da lista final abaixo, aberta pelo `brza note new issue` no `tools-kit`, com `scope:
[brza-workflow]`, `priority: low` e o link para este plano no corpo.
