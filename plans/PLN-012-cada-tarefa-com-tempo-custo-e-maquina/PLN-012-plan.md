---
status: in_progress
phase: execution
origin: request
description: Liga a medição às tarefas, para que cada uma mostre o tempo corrido, o custo de API e o recurso de máquina, e o fluxo se afine por dado.
ready: sim
estimate_h: 16
executed_h: 3.5
remaining_h: 7
scope:
  - brza-workflow
opened: 2026-11-03
owner: Anderson
priority: medium
tags:
  - tooling
---

# PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou

- **Retomar:** em 2026-11-06, P1, P2 e P4 fecharam e estão na integração `feat/pln-012-medida-por-tarefa`, com o P5
  (`0a6f181`, as três suítes verdes); as sessões dos passos foram fechadas e as branches deles apagadas. Próximo: o P3,
  a pedido de Anderson, num worktree saído da integração, com o P5.6 junto; depois o merge na `master` (P5.4) e o P6.
- **Dividido:** [PLN-012 — Desenho](PLN-012-design.md)

## Pedido

- **Origem:** pedido livre de Anderson em 2026-11-03, na sessão "Plano: chat via CLI e plugins" do `playground`,
  trazido à sessão `tools-kit-produtividade` do `tools-kit`. Nasceu de uma rodada sobre gravar data e hora (ISO 8601)
  em `opened` e `completed` do worklog, em que Anderson não escolheu nenhuma opção e trocou a pergunta por este pedido.

> "precisamos de uma forma de medir nossa produtividade, quanto realmente demoramos para executar as tarefas, quanto
> gastamos de recursos em cada tarefa - aqui inclui custo da API, recurso de maquina e tempo corrido - para irmos
> afinando o fluxo"

### Cobertura

| Origem | Critério de aceite | Passo | Teste (nível) |
| Origem | Critério de aceite | Passo | Teste (nível) |
| :-- | :-- | :-- | :-- |
| `Pedido 1`, `R1.1`, `R2.1` | O `brza note commit` de um worklog grava `sessions:` nele e um evento `task`, e a tarefa vai do primeiro turno depois do marco anterior da sessão ao commit, com o intervalo entre os dois como ociosa da sessão | P3, P2 | `test_brza_note` e `test_summarize_measurements` (unidade); P6 (manual) |
| `Pedido 1`, `R2.2`, `R2.3` | Cada tarefa tem o tempo do agente, o de Anderson e a pausa acima de 30 min por espera, com as esperas da rodada e da interrupção lidas no transcript, e o corrido como a soma | P1, P2 | `test_measure` e `test_summarize_measurements` (unidade); P6 contra o transcript (manual) |
| `Pedido 2` | Cada tarefa tem o custo de API dos turnos e dos subagentes, cada subagente no turno da sessão que contém o começo dele | P2 | `test_summarize_measurements` (unidade) |
| `Pedido 3`, `R1.2` | Cada turno traz a CPU do `claude` e dos filhos e o RSS, pelo `proc_pid_rusage`, e cada `brza run` grava a CPU, o pico e a duração do comando com a sessão que o chamou | P1, P4 | `test_measure` e `test_brza_scripts` (unidade); P1.4 na sessão real (manual) |
| `Pedido 4`, `R1.4` | `summarize_measurements.py --by-task` compara as tarefas por workstream e dia | P2 | `test_summarize_measurements` (unidade); P6 (manual) |
| `R3.1` | A `## Medida` do worklog traz a tarefa até o commit, com o turno em curso lido no transcript, e bate com o `--by-task` | P3, P6 | `test_brza_note` (unidade); P6 (manual) |
| `R0.3`, `R3.2` | O worklog não ganha `opened` nem hora em `completed`; a hora do fim está na `## Medida` | P3 | `test_brza_note` (unidade) |
| `R1.3`, `R2.4` | A tarefa sem turno medido aparece "não medida", e os turnos depois do último marco de cada sessão, "sem tarefa" | P2 | `test_summarize_measurements` (unidade) |
| `R3.3` | O `close-task` mostra os turnos que o commit vai fechar e os sem tarefa das outras sessões do workstream | P2, P5 | `test_summarize_measurements` (unidade); P6 (manual) |
| `R3.4` | `brza note commit --until HH:MM` põe o marco na hora dada, e recusa a hora fora da janela | P3, P2 | `test_brza_note` e `test_summarize_measurements` (unidade) |
| `R4.1` | O `--by-task` começa no primeiro evento `task` do log | P2 | `test_summarize_measurements` (unidade) |
| `R1.3` | Toda lacuna da lista tem issue aberta | P5 | `brza note ls` com as issues (manual) |

### Fora de escopo

- **Mudar o fluxo a partir dos números.** O plano entrega a medida; o afinar é de cada plano ou decisão que a usar.
- **Medir o Codex e o Antigravity.** Foi para
  [Codex e Antigravity ficam sem medida por tarefa](../../work/issues/codex-e-antigravity-sem-medida-por-tarefa.md),
  pela R1.3.

## Restrições

- **O código é do `brza-workflow`.** `core/.claude/hooks/measure.py`, `core/scripts/summarize_measurements.py`,
  `bin/brza-note` e `core/.claude/skills/close-task/SKILL.md` se editam lá e chegam aos workspaces pelo `brza sync`;
  editados aqui, travam o sync seguinte.
- **Nada do `playground` se edita por este plano.**

## Entrevista

### Rodada 0 — o que a sessão do `playground` já respondeu (respondida em 2026-11-03)

Respondida em 2026-11-03, na sessão "Plano: chat via CLI e plugins" do `playground`, e trazida no pedido que abriu
esta sessão.

1. **Workstream.** **Decidido — "tools-kit (Recomendado)"**: o que muda mora no `brza-workflow`.
2. **Quando.** **Decidido — "Sessão nova agora (Recomendado)"**.
3. **A forma das datas no worklog.** Anderson não escolheu nenhuma das opções sobre gravar data e hora em `opened` e
   `completed`, e trocou a pergunta pelo pedido acima. A forma das datas passa a ser parte deste desenho.

### Rodada 1 — a tarefa, a máquina, o que não se mede e onde aparece (enviada 2026-11-03)

> **Apresentado antes:** o Terreno, em três achados: a sessão tem o próprio id no ambiente (`CLAUDE_CODE_SESSION_ID`),
> e o `brza note commit` pode gravá-lo no worklog sozinho; o mapa do `brza sessions` cobre 25 das 100 sessões medidas
> desde 2026-10-29, com ~40% do custo de turno; o `ps -S` dá a CPU do `claude` e dos filhos que já saíram, e o
> `brza run` roda fora dessa árvore.

Respondida em 2026-11-03, na sessão `tools-kit-produtividade`.

1. **O que conta como uma tarefa, e onde ela começa e termina.** Opções, cada uma com o preço apresentado:
   - o worklog, carimbado (recomendada) — o `brza note commit` grava no worklog o id da sessão, como faz com o
     `refs:`, e um evento na medição; a tarefa vai do marco anterior da mesma sessão, ou do início dela, ao commit;
     separa tarefas encadeadas e dispensa marcar o início — custo: ~4 h no `brza-note`, no `measure.py` e no
     `summarize_measurements.py`, com testes; se paga: na primeira semana, para toda sessão Claude; a tarefa sem
     worklog cai na seguinte;
   - a sessão do `brza sessions`, pelo título "PLN-NNN Pn" do mapa — custo: ~2 h, só no `summarize`; se paga: agora,
     retroativo a 2026-10-29; cobre 25 de 100 sessões (~40% do custo), e a sessão que encadeia tarefas vira uma só;
   - o passo `P` do plano, com início e fim marcados nele — custo: ~3 h e um campo à mão; se paga: só no trabalho de
     plano;
   - início e fim explícitos, por `brza task start`/`stop` — custo: ~3 h e o hábito; se paga: só quando ninguém
     esquece.

   **Resposta:** "na opção 1, oq acontece com sessão que ficou ociosa entre uma tarefa e outra". Leitura: a opção 1
   interessa, mas falta dizer onde vai o tempo parado; vai à rodada 2. **→ fechada em R2.1**: o worklog, carimbado,
   com o começo no primeiro prompt depois do marco.

2. **Como medir a máquina** (seleção múltipla). Opções:
   - a CPU da sessão (recomendada) — o hook lê, no fim de cada turno, o `ps -S` do `claude` (a CPU dele e dos filhos
     que saíram, com testes e builds pelo `Bash`) e o RSS, e grava a diferença por turno — custo: ~2 h; se paga: no
     primeiro passo; não vê processo em segundo plano que não terminou;
   - o `brza run` mede (recomendada) — grava a CPU, a memória de pico e a duração do comando, com o id da sessão que
     chamou — custo: ~1,5 h; se paga: quando testes e builds do `brza-studio` passam por ele;
   - amostra da máquina inteira por um daemon do launchd, dividida pela janela da tarefa — custo: ~4 h e um daemon
     sempre ligado; se paga: só com uma sessão por vez;
   - fora deste plano, numa issue — custo: nenhum agora; se paga: nunca, para esta parte do pedido.

   **Decidido — a CPU da sessão e o `brza run` mede**, as duas.

3. **As sessões sem medida e os outros runtimes.** Opções:
   - lacuna à vista (recomendada) — o resumo lista a tarefa sem turno medido como "não medida", com o tempo corrido
     que houver; Codex e Antigravity vão a uma issue — custo: ~0,5 h; se paga: agora;
   - medir Codex e Antigravity neste plano, pelos logs deles — custo: 6 h ou mais; se paga: quando pesarem no gasto
     (hoje, 2 de 44 aberturas);
   - ignorar — custo: nenhum; se paga: nunca.

   **Decidido — lacuna à vista**, com o acréscimo de Anderson: "opção 1, mas sempre abra issue para lacunas
   deixadas". Toda lacuna de medida que o plano deixar — Codex, Antigravity, sessão aberta sem a função do shell, o
   que o Desenho não cobrir — ganha uma issue.

4. **Onde aparece.** Opções:
   - resumo e worklog (recomendada) — o `summarize_measurements.py --by-task` mostra a tabela comparada, e o
     `brza note commit` escreve uma linha de medida no worklog quando a tarefa fecha — custo: ~2 h; se paga: na
     primeira troca de máquina, porque `.measurements/` fica fora do git; a linha não traz o turno do próprio commit;
   - só no resumo — custo: ~1 h; se paga: agora, mas fora do git;
   - só no worklog — custo: ~1,5 h; se paga: nunca, para comparar tarefas.

   **Decidido — resumo e worklog.**

### Rodada 2 — o tempo parado entre tarefas e dentro delas (enviada 2026-11-03)

> **Apresentado antes:** a resposta à pergunta da R1.1. Na opção 1 como estava, a tarefa começaria no commit da
> anterior, e o tempo parado entre as duas cairia na seguinte: uma noite parada inflaria a tarefa da manhã. O hook já
> sabe quando o turno começa (`timestamp − duration_s`, `measure.py:406-413`), e a tarefa pode começar no primeiro
> prompt depois do commit anterior, sem marca à mão. Sobra a pausa no meio da tarefa.

Respondida em 2026-11-03, na sessão `tools-kit-produtividade`.

1. **Onde começa a tarefa.** Opções:
   - no primeiro prompt depois do marco (recomendada) — o tempo entre o commit da tarefa anterior e o prompt seguinte
     não é de nenhuma tarefa, e aparece como "ociosa" da sessão — custo: nenhum além das ~4 h da R1.1; se paga: na
     primeira noite parada;
   - no marco anterior — o tempo parado entra na seguinte — custo: nenhum; se paga: nunca, para comparar.

   **Decidido — no primeiro prompt depois do marco.** Com isso, a R1.1 fecha no worklog carimbado pelo
   `brza note commit`.

2. **A pausa dentro da tarefa.** Opções:
   - agente, Anderson e pausa (recomendada) — três tempos e a soma deles, o corrido: o do agente, os turnos sem a
     espera nas rodadas; o de Anderson, a espera entre um turno e o prompt seguinte e a espera nas rodadas, até o
     limiar; a pausa, o que passa do limiar — custo: +1,5 h, para ler a espera da rodada no transcript; se paga: na
     primeira comparação, porque mostra se a demora foi do agente ou da espera;
   - o corrido sem as pausas, um número só — custo: +0,5 h; se paga: agora, mas não separa o agente de Anderson;
   - o corrido bruto — custo: nenhum; se paga: só em tarefa curta e contínua.

   **Decidido — agente, Anderson e pausa**, com o corrido como a soma.

3. **O limiar da pausa.** Opções, todas sem custo, porque é uma constante:
   - 30 min (recomendada) — se paga: agora; a leitura de uma rodada grande cabe, e o almoço ou a noite fica fora;
   - 15 min — se paga: só se as rodadas forem curtas; a leitura de um rascunho longo vira pausa;
   - 60 min — se paga: só se as esperas longas forem trabalho; uma reunião de 50 min conta como tempo de Anderson.

   **Decidido — 30 min.**

4. **Os turnos que nenhum worklog fecha.** Opções:
   - "sem tarefa" e aviso (recomendada) — o resumo os mostra como "sem tarefa", por sessão, e o `close-task` diz
     quantos turnos da sessão ficaram sem tarefa antes de fechar — custo: ~1 h; se paga: na primeira vez que o worklog
     ficar para depois;
   - só "sem tarefa" no resumo — custo: ~0,5 h; se paga: agora, mas só quem abre o resumo vê;
   - somam à tarefa seguinte — custo: nenhum; se paga: nunca, porque mistura duas tarefas.

   **Decidido — "sem tarefa" e aviso.**

### Rodada 3 — a linha do worklog, as datas, o aviso e o corte (enviada 2026-11-03)

> **Apresentado antes:** o levantamento do `designer`. O `ps -S` não soma a CPU dos filhos de outro processo
> (conferido pela sessão: 0:00.01 depois de um filho de 2 s); o `proc_pid_rusage` da `libproc` soma
> (`child_cpu=2.02s`), e substitui o `ps -S` sem rodada, com a mesma intenção da R1.2. Na mediana, o turno do commit
> tem 77% do custo e 88% da duração da tarefa, e 70 de 158 tarefas têm um turno só. A espera da rodada se lê no
> transcript, entre a pergunta e a resposta, e cai dentro do `duration_s` (459 s e 166 s nesta sessão). Os subagentes
> rodam no processo da sessão e levam o id dela (161 de 163 começam dentro de um turno da sessão). Esta sessão emendou
> duas tarefas: os turnos do Grok cairiam na tarefa do Desenho. Decididos no rascunho, por não mudarem o resultado: o
> campo `sessions:`, na forma do `refs:`; cada commit de worklog é um marco; dois worklogs no mesmo commit dividem o
> trecho em partes iguais.

Respondida em 2026-11-03, na sessão `tools-kit-produtividade`.

1. **A linha de medida e o turno do commit** (reabre a R1.4 no ponto do turno do commit). Opções:
   - lê o turno em curso (recomendada) — o `brza note commit` lê o transcript da sessão até o commit, sem mexer no
     estado do hook, e a CPU pelo processo da sessão — custo: +1,5 h no passo do commit; se paga: no primeiro commit;
     sem isso, 44% das tarefas saem com a linha vazia;
   - sem o turno do commit, como na R1.4 — custo: nada além das ~2 h; se paga: nunca na tarefa de um turno só;
   - completa no commit seguinte da mesma sessão — custo: +1 h e um commit que reescreve o worklog de outra tarefa;
     se paga: só quando a sessão commita de novo.

   **Decidido — lê o turno em curso.**

2. **As datas do worklog** (fecha a R0.3). Opções:
   - não; a hora fica na `## Medida` (recomendada) — sem `opened` e sem hora em `completed`; o começo e o fim ficam na
     seção `## Medida` do worklog e no evento `task` — custo: nenhum; se paga: agora, porque o worklog nasce no fim;
   - `opened` e `completed` com hora ISO, tirados da medição — custo: ~1 h e uma linha na norma; se paga: só se alguém
     ler a hora no frontmatter, que nem o checador nem o índice leem.

   **Decidido — não; a hora fica na `## Medida`.**

3. **O aviso do `close-task`** (completa a R2.4, cuja leitura literal contaria zero). Opções:
   - este commit e as outras sessões (recomendada) — os N turnos que este commit fecha, desde HH:MM, com o começo de
     cada prompt, e os "sem tarefa" das outras sessões do workstream paradas há mais de 2 h — custo: ~1,5 h; se paga:
     na primeira emenda, como já houve nesta sessão;
   - só este commit — custo: ~1 h; se paga: na primeira emenda;
   - a leitura literal da R2.4 — custo: ~0,5 h; se paga: nunca, porque conta zero.

   **Decidido — este commit e as outras sessões.**

4. **Duas tarefas emendadas sem worklog entre elas.** Opções:
   - `brza note commit <worklog> --until HH:MM` (recomendada) — o marco vai à hora dada, entre o marco anterior e
     agora, e os turnos depois dela ficam para o próximo commit — custo: ~1 h; se paga: na primeira emenda que o aviso
     mostrar;
   - sem corte, com issue — custo: nenhum; se paga: nunca, para separar.

   **Decidido — `--until HH:MM`.**

### Rodada 4 — o histórico (enviada 2026-11-03)

> **Apresentado antes:** ligar os worklogs antigos à sessão pelo workstream e pela hora casa 194 de 227 commits desde
> 2026-10-29; 34 deles batem com mais de uma sessão, e 33 com nenhuma.

Respondida em 2026-11-03, na sessão `tools-kit-produtividade`.

1. **O dado de antes do deploy.** Opções:
   - começa no deploy (recomendada) — a medida por tarefa começa no primeiro evento `task` — custo: nenhum; se paga:
     agora, sem herdar a inferência por hora;
   - `--backfill` inferido, com a tarefa marcada "inferida" — custo: ~2 h; se paga: na primeira comparação antes e
     depois de uma mudança de fluxo, mas com 34 commits ambíguos e 33 sem par.

   **Decidido — começa no deploy.**

### Rodada 5 — o corte dos Passos (enviada 2026-11-03)

> **Apresentado antes:** o texto inteiro dos Passos P1–P6, da Cobertura, da Regressão e das 10 lacunas que viram
> issue, na mensagem, com a pergunta em texto, sem a ferramenta.

Respondida em 2026-11-06, na sessão `tools-kit-produtividade`.

1. **O corte.** Opções:
   - aceitar P1 a P6, 16 h (recomendada) — custo: 16 h numa sessão do `brza-workflow`, um commit por passo; se paga:
     no P3, com a medida por tarefa pronta para a primeira comparação; o P4 e o P5 completam a máquina e o aviso;
   - juntar P1–P3 num passo só, 11,5 h — custo: o mesmo, com uma revisão maior; se paga: só se a revisão por passo
     pesar mais que o código;
   - dividir em duas fases, P1–P3 e P6 agora, P4 e P5 depois — custo: o `brza run` e o aviso ficam para depois; se
     paga: só com urgência de ter o número, com a R3.3 e a R3.4 pela metade no intervalo.

   **Decidido — "aceito o corte"**: P1 a P6, 16 h. É o aceite do plano.

## Passos

> O código é do `brza-workflow`. P1 a P4 e a parte de código do P5 são de uma sessão aberta no
> `~/Projects/brza-workflow`, na branch `feat/pln-012-medida-por-tarefa`, com revisão do `reviewer` antes de cada `[x]`;
> chegam aos workspaces pelo `brza sync`. Ordem: P1 → P2 → P3; P4 independe de P2 e P3; P5 depois de P2; P6 por último.

### P1 — O turno com as esperas, o começo do pedido e a máquina

Executa D2 · executor: sessão do `brza-workflow`, na `feat/pln-012-medida-por-tarefa`

Estimado: 3.5 h · Executado: 1.1 h

- [x] **1. Teste que falha** — `tests/hooks/test_measure.py`: transcript com um `AskUserQuestion` respondido 459 s
  depois e um segundo pedido depois de 120 s parado → `waits_s == [459, 120]`; pedido `isMeta` não gera espera;
  `prompt_head` cortado em 80, sem quebra de linha; `machine` com o `proc_pid_rusage` falso — dois turnos do mesmo `pid`
  dão o delta, `CLAUDE_PID` ausente dá `from: "ppid"`, leitura que falha dá `null` e a linha sai.
- [x] **2. Implementar** — `measure()`, `turn()`, `machine_of(pid)`, `claude_pid()`.
- [x] **3. Rodar e ver passar** — `python3 -m unittest discover -s tests/hooks`
- [-] **4. Conferir na sessão real** — movido ao P6, que roda depois do `brza sync`; — depois do `brza sync`, um turno com um comando de 2 s de CPU: `machine.from`
  diz se o hook herda a `CLAUDE_PID` [F19], e `cpu_children_s` ≥ 2.
- [x] **5. Commit**

**Evidência:** `brza-workflow@7f38397` (`feat/pln-012-p1`), juntado na integração em `9e82bb1` ·
`python3 -m unittest discover -s tests/hooks` → 317 OK · revisão:
[REV-017: O P1 do PLN-012, revisado pelo agy e pelo reviewer](../../work/reviews/REV-017-pln-012-p1-o-turno-com-esperas-e-maquina.md) ·
desvios do D2 no worklog (X3)

### P2 — `--by-task` e o `--pending`

Executa D4 · executor: sessão do `brza-workflow`, na `feat/pln-012-medida-por-tarefa`

Estimado: 4.0 h · Executado: 1.3 h

- [x] **1. Teste que falha** — `tests/hooks/test_summarize_measurements.py`, com o caso desta sessão em fixture (5
  turnos, 3 `task`, 2 subagentes): a abertura do PLN-012 com agente 452 s, Anderson 625 s, pausa 0; o grok com T2;
  ociosa 13,8 min; T3–T5 "sem tarefa". E: espera de 50 min → 30 de Anderson e 20 de pausa; dois worklogs num commit →
  metade cada; `task` sem sessão → "não medida"; `until` desloca o marco; turno antes do primeiro `task` fica de fora;
  turno `fact_audit` fica de fora; `--pending --session` lista os turnos depois do último marco e as outras sessões
  paradas há mais de 2 h.
- [x] **2. Implementar** — `task_segments`, `task_measure`, as três tabelas, o `--json`, o `--pending --session`.
- [x] **3. Rodar e ver passar** — `python3 -m unittest tests/hooks/test_summarize_measurements.py`
- [x] **4. Commit**

**Evidência:** `brza-workflow@a4e98bf` (`feat/pln-012-p2`), juntado na integração em `5ecddfe` ·
`python3 -m unittest discover -s tests/hooks -p test_summarize_measurements.py` → 79 OK (o comando do plano não acha o
`repo_fixture`) · revisão:
[REV-020: O P2 do PLN-012, o --by-task e o --pending, revisado pelo agy e pelo Opus](../../work/reviews/REV-020-pln-012-p2-by-task-e-pending.md) ·
desvios no worklog (X4)

### P3 — O carimbo, o `task`, o `--until` e a `## Medida`

Executa D1, D3 · executor: sessão do `brza-workflow`, na `feat/pln-012-medida-por-tarefa`

Estimado: 4.0 h · Executado: — h

- [ ] **1. Teste que falha** — `tests/cli/test_brza_note.py`: commit com `CLAUDE_CODE_SESSION_ID` → `sessions:` no
  frontmatter, sem repetir no segundo commit, e sem `opened`; linha `task` no log da `MEASURE_DIR`, também com
  `--no-push`; sem a variável → sem carimbo, sem `## Medida` e `session_id: null`; commit recusado → sem evento;
  `--until` fora da janela recusa sem tocar o worklog; `## Medida` reescrita no segundo commit, com o turno em curso lido
  de um transcript de fixture, e com "sem o turno do commit" quando o transcript falta; o `state.json` não muda.
- [ ] **2. Implementar** — `set_frontmatter_list`, `write_task_event`, `--until`, `measure_line` (pelo `runpy` do
  resumo e do `measure.py`).
- [ ] **3. Rodar e ver passar** — `python3 -m unittest tests/cli/test_brza_note.py tests/cli/test_brza_note_index.py`
- [ ] **4. Commit**

**Evidência:** `brza-workflow@<sha>` · `python3 -m unittest tests/cli/test_brza_note.py tests/cli/test_brza_note_index.py` → N passed

**Do P1 e do P2, para o P3:** `machine_of(pid, origin, last)` é puro e devolve `(machine, marca)`, para o turno em curso
sem gravar a marca; `measure(lines)` devolve `waits_s` e `prompt_head` no 2º dicionário. O resumo exporta
`task_segments`, `task_measure`, `aggregate_by_task`, `parse_time` e `human_duration`; a `## Medida` sai de
`aggregate_by_task(rows)["tasks"]`, filtrado pelo worklog, para bater com a tabela na divisão por n (REV-020). O
segmento é `[marco anterior, marco)` (X2), a chave do tempo humano é `requester_s` e o texto diz "quem pediu" (X6).

### P4 — O `brza run` mede

Executa D5 · executor: sessão do `brza-workflow`, na `feat/pln-012-medida-por-tarefa`

Estimado: 1.5 h · Executado: 1.1 h

- [x] **1. Teste que falha** — `tests/cli/test_brza_scripts.py`: `run_here` com um comando que gasta CPU e aloca
  memória → `cpu_s > 0`, `max_rss_mb > 0`, `duration_s > 0`; `run_in_tab` com `result.json` de fixture → linha `run`
  com o `session_id` do ambiente; sem workspace → sem linha e aviso no stderr; os blocos impressos não mudam.
- [x] **2. Implementar**
- [x] **3. Rodar e ver passar** — `python3 -m unittest tests/cli/test_brza_scripts.py`
- [x] **4. Commit**

**Evidência:** `brza-workflow@aa752e6` (`feat/pln-012-p4`), juntado na integração em `2602b6d` ·
`python3 -m unittest tests/cli/test_brza_scripts.py` → 41 OK · revisão:
[REV-019: A revisão do P4 do PLN-012, o brza run que mede](../../work/reviews/REV-019-pln-012-p4-o-brza-run-mede.md) ·
desvios do D5 no worklog (X5)

### P5 — O `close-task`, a norma e as issues

Executa D6, D7 e a norma do D3 · executor: sessão do `brza-workflow` (skill e norma), e a sessão que conduz (issues)

Estimado: 2.0 h · Executado: — h

- [x] **1. Teste que falha** — `tests/notes-checker`: worklog com `sessions:` e `## Medida` passa sem aviso.
- [x] **2. Escrever** — o passo "2. O que o commit vai fechar" do `close-task`; a linha `sessions` e a `## Medida` no
  `core/work/README.md`; no `CLAUDE.md` do adaptador, os eventos `task` e `run` na tabela do hook e o `--by-task` no
  resumo.
- [x] **3. Rodar e ver passar** — `python3 tests/notes-checker/run.py`
- [ ] **4. Commit** — no `brza-workflow`, e merge da `feat/pln-012-medida-por-tarefa` na `master` dele depois da
  revisão. Commit feito em `feat/pln-012-p5@22805fb` e juntado na integração em `cbbe0bd`; falta o merge na `master`,
  que espera o P1 a P4.
- [x] **5. Abrir as issues** das lacunas, pela sessão que conduz, com `brza note new issue` e `brza note commit` —
  as 10 de `## Pendências conhecidas`, em 2026-11-06.
- [ ] **6. O `--workstream` no `--pending` do `close-task`** — sem ele, a sessão cujo único turno está em curso fica
  sem a linha das outras sessões paradas (REV-020, A4). Vai junto do P3.

**Evidência:** `brza-workflow@<sha>` · `python3 tests/notes-checker/run.py` → N passed · as issues no
`tools-kit@<sha>` · código e norma em `brza-workflow@22805fb` (`feat/pln-012-p5`); revisão: [REV-018: A revisão do P5 do PLN-012, o close-task e a norma](../../work/reviews/REV-018-pln-012-p5-o-close-task-e-a-norma.md)

### P6 — Uma tarefa medida de ponta a ponta

Executa a conferência de D1–D6 · executor: sessão que conduz, com Anderson

Estimado: 1.0 h · Executado: — h

- [ ] **1. `brza sync`** no workspace, e conferir que o `.brza/core.lock` aponta o merge do P5.
- [ ] **2. Uma tarefa real** com rodada, subagente e `brza run`, fechada pelo `close-task`: o aviso aparece, e o
  worklog sai com `sessions:` e `## Medida`.
- [ ] **3. Conferir** — a `## Medida` e a linha do `python3 scripts/summarize_measurements.py --by-task` batem entre si,
  e com o transcript (as esperas lidas à mão), dentro de 5%.

**Evidência:** o worklog da tarefa · a saída do `--by-task`

**Total estimado:** 16 h (P1 3,5 + P2 4 + P3 4 + P4 1,5 + P5 2 + P6 1) contra ~12,5 h somadas
nas R1 e R2; a diferença é a R3.1 (+1,5 h), a R3.3 (+0,5 h), a R3.4 (+1 h) e as issues (+0,5 h).

## Regressão

- **A linha `turn` e a `subagent` mantêm todos os campos de hoje**, e o hook nunca falha nem bloqueia: `machine`
  `null` quando a leitura falha. Como se confere: `python3 -m unittest discover -s tests/hooks` (os testes de hoje do
  `test_measure.py` e do `test_measure_workstream.py` sem mudança).
- **O estado de leitura do transcript avança como hoje**, e a leitura do `brza note commit` não o avança. Como se
  confere: o teste do P3 que compara o `state.json` antes e depois do commit.
- **O resumo sem `--by-task` sai igual**: o relatório padrão, o `--by-workstream` e o `--facts` ignoram `task` e `run`,
  sem contá-los como `hook_error`. Como se confere: `python3 -m unittest tests/hooks/test_summarize_measurements.py`, e
  a saída do `summarize_measurements.py` sobre uma cópia do log de hoje igual antes e depois (`diff`).
- **O `brza note commit` commita só os caminhos dados, extrai o `refs:` e grava o índice como hoje**; sem
  `CLAUDE_CODE_SESSION_ID`, o worklog commitado é o mesmo de hoje byte a byte. Como se confere:
  `python3 -m unittest tests/cli/test_brza_note.py tests/cli/test_brza_note_index.py`.
- **O `close-task` mantém os passos de hoje e a trava do `/compact` não muda.** Como se confere:
  `python3 -m unittest tests/hooks/test_compact_guard.py`, e a leitura do diff da skill.
- **O `brza run` imprime os mesmos blocos, sai com o código do comando e fecha a aba com 0**; o `result.json` continua
  com `code`. Como se confere: `python3 -m unittest tests/cli/test_brza_scripts.py`.
- **O checador aceita o worklog novo e o antigo.** Como se confere: `python3 tests/notes-checker/run.py`, e `python3 .claude/skills/notes-checker/scripts/check_notes.py` no `tools-kit` depois do
  `brza sync`.

## Desvios

- **X1 — P1, P2, P4 e P5 em paralelo, cada um na sua branch.** Anderson pediu em 2026-11-06 "inicie os passos em
  paralelo"; o corte previa P1 → P2 → P3 e o P5 depois do P2. O P2 e o P5 se escrevem contra o contrato do D1, do D2 e
  do D4, e cada passo vai a `feat/pln-012-<pN>`, que esta sessão junta em `feat/pln-012-medida-por-tarefa`; a `master`
  do `brza-workflow` só recebe a integração no fim do P5, como estava. Afeta P1–P5.
- **X2 — O segmento passa a `[marco anterior, marco)`, e o `--until` leva o começo do primeiro turno da tarefa
  seguinte.** O P5 (REV-018, A15) fixou no `close-task` a hora que o `--pending` mostra, e não a do fim do último turno,
  que o aviso não mostra e que, cortada no minuto, pode cair antes do começo do turno. Com o intervalo fechado à
  direita, o turno que começa no `until` ficaria na tarefa anterior. A R3.4 não muda. Afeta D1, P2 e P3; o P2 foi
  avisado por correio em 2026-11-06.
- **X3 — Os desvios do P1 ao D2** estão no worklog dele, com o porquê (seis). Afeta P3, pelo `machine_of` puro.
- **X4 — Os desvios do P2 ao D4** estão no worklog dele: o X2 aplicado, o comando de teste por `discover`, o formato do
  `--pending` e as seis escolhas que o D4 não fixava.
- **X5 — Os desvios do P4 ao D5** estão no worklog dele (lá numerados X1–X5): a CPU como diferença em volta do comando,
  o `provider_session` copiado, o workstream pelo `measure.py`, o cwd guardado antes do comando e o `ru_maxrss` em KB no
  Linux.
- **X6 — "Anderson" sai do `core/`.** O P1 e o P2 escreveram o nome no `measure.py` e no resumo, e o `brza init`, que
  recusa nome de workspace no que escreve, falhou 43 vezes no `test_brza_init` do conjunto. A chave vira `requester_s`,
  a coluna "quem pediu" (`brza-workflow@0a6f181`). O D2, o D3 e o D4 dizem "Anderson" no texto; o código diz "quem
  pediu". Afeta P3 e a `## Medida`.

## Pendências conhecidas

- [A sessão aberta sem a função do shell fica sem medida por tarefa](../../work/issues/sessao-sem-a-funcao-do-shell-fica-sem-medida-por-tarefa.md) — D7, P5.5.
- [A espera de permissão de ferramenta conta como tempo do agente](../../work/issues/espera-de-permissao-conta-como-tempo-do-agente.md) — D7, P5.5.
- [A memória dos comandos rodados pelo Bash não se mede](../../work/issues/memoria-dos-comandos-do-bash-nao-se-mede.md) — D7, P5.5.
- [O processo em segundo plano entra na CPU só quando sai](../../work/issues/processo-em-segundo-plano-entra-na-cpu-so-quando-sai.md) — D7, P5.5.
- [O commit de worklog fora do brza note commit não marca tarefa](../../work/issues/commit-de-worklog-fora-do-brza-note-nao-marca-tarefa.md) — D7, P5.5.
- [O /clear pode partir a tarefa em duas sessões](../../work/issues/clear-pode-partir-a-tarefa-em-duas-sessoes.md) — D7, P5.5.
- [O worklog renomeado muda a chave da tarefa](../../work/issues/worklog-renomeado-muda-a-chave-da-tarefa.md) — D7, P5.5.
- [A CPU do subagente em segundo plano cai no turno em que ele termina](../../work/issues/cpu-do-subagente-em-segundo-plano-cai-no-turno-errado.md) — D7, P5.5.
- [O ▶ do brza run sem resposta do app grava o comando sem sessão](../../work/issues/brza-run-sem-resposta-do-app-grava-sem-sessao.md) — D7, P5.5.
- [O pico do brza run é o do maior processo, não o da árvore](../../work/issues/pico-do-brza-run-e-o-do-maior-processo.md) — D7, P5.5.
- [O brza-run copia o provider_session e lê o workstream pelo hook de medição](../../work/issues/o-brza-run-copia-o-provider-session-e-le-o-workstream-pelo-hook.md) — do REV-019, no P4.
- [O aviso do --pending soma as sessões paradas de qualquer idade](../../work/issues/o-pending-mostra-sessoes-paradas-sem-teto-de-idade.md) — do REV-020, no P2.

## Revisões

- 2026-11-06 — P1, o turno com as esperas e a máquina: três rodadas do agy e a final do reviewer; 9 achados e o ponto F
  corrigidos aqui. [REV-017: O P1 do PLN-012, revisado pelo agy e pelo reviewer](../../work/reviews/REV-017-pln-012-p1-o-turno-com-esperas-e-maquina.md)
- 2026-11-06 — P4, o brza run que mede: duas rodadas do agy e a final do reviewer; seis corrigidos aqui, dois à issue.
  [REV-019: A revisão do P4 do PLN-012, o brza run que mede](../../work/reviews/REV-019-pln-012-p4-o-brza-run-mede.md)
- 2026-11-06 — P2, o --by-task e o --pending: três rodadas do agy e a final do reviewer; um ponto à issue.
  [REV-020: O P2 do PLN-012, o --by-task e o --pending, revisado pelo agy e pelo Opus](../../work/reviews/REV-020-pln-012-p2-by-task-e-pending.md)
- 2026-11-06 — P5, o `close-task` e a norma: duas rodadas do agy e a final do reviewer, aprovado com correções aplicadas.
  [REV-018: A revisão do P5 do PLN-012, o close-task e a norma](../../work/reviews/REV-018-pln-012-p5-o-close-task-e-a-norma.md)

## Worklogs

- 2026-11-03 — aberto; Rodada 0 transcrita; Terreno levantado; R1 e R2 respondidas; issue do Codex e do
  Antigravity aberta. Parou antes do Desenho.
  [Abertura do PLN-012, a produtividade medida por tarefa](../../work/worklogs/2026-11-03-pln-012-abertura-da-produtividade-por-tarefa.md)
- 2026-11-03 — R3 e R4 respondidas; D1–D7 gravados no `-design`; o `ps -S` trocado pelo `proc_pid_rusage`. Parou na
  rodada do corte dos Passos.
  [Desenho do PLN-012, a medida por tarefa](../../work/worklogs/2026-11-03-pln-012-desenho-da-medida-por-tarefa.md)
- 2026-11-06 — R5.1: corte aceito, P1–P6 (16 h); Passos, Cobertura e Regressão gravados; `phase: execution`.
  [Aceite do corte do PLN-012](../../work/worklogs/2026-11-06-pln-012-aceite-do-corte.md)
- 2026-11-06 — X1: P1, P2, P4 e P5 abertos em paralelo, cada um na sua sessão e branch; P5.5 feito, com as 10 issues.
  [Os passos do PLN-012 em paralelo](../../work/worklogs/2026-11-06-pln-012-passos-em-paralelo.md)
- 2026-11-06 — P5 (código e norma) fechado em `feat/pln-012-p5`, sha `22805fb`: close-task, `core/work/README.md` e `CLAUDE.md`; desvio do `--until` no D6.
  [O P5 do PLN-012, o close-task e a norma](../../work/worklogs/2026-11-06-pln-012-p5-o-close-task-e-a-norma.md)
- 2026-11-06 — P1 fechado em `feat/pln-012-p1@7f38397`, 1,1 h; o subpasso 4 vai ao P6.
  [O P1 do PLN-012, o turno com as esperas, o começo do pedido e a máquina](../../work/worklogs/2026-11-06-pln-012-p1-o-turno-com-esperas-e-maquina.md)
- 2026-11-06 — P2 fechado em `feat/pln-012-p2@a4e98bf`, 1,3 h, com o X2.
  [O P2 do PLN-012, o --by-task e o --pending no resumo da medição](../../work/worklogs/2026-11-06-pln-012-p2-by-task-e-pending.md)
- 2026-11-06 — P4 fechado em `feat/pln-012-p4@aa752e6`, 1,1 h.
  [O P4 do PLN-012, o brza run que mede](../../work/worklogs/2026-11-06-pln-012-p4-o-brza-run-mede.md)
