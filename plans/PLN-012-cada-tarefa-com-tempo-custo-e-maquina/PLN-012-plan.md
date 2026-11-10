---
status: done
phase: closed
origin: request
description: Liga a medição às tarefas, para que cada uma mostre o tempo corrido, o custo de API e o recurso de máquina, e o fluxo se afine por dado.
ready: sim
estimate_h: 17.75
executed_h: 6.9
remaining_h: 0
scope:
  - brza-workflow
opened: 2026-11-03
completed: 2026-11-09
owner: Anderson
priority: medium
tags:
  - tooling
---

# PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou

- **Retomar:** fechado em 2026-11-09. P1–P8 feitos e a entrega revisada (REV-024). O que ficou para depois está
  nas 12 issues de `## Pendências conhecidas`.
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
| :-- | :-- | :-- | :-- |
| `Pedido 1`, `R1.1`, `R2.1` | O `brza note commit` de um worklog grava `sessions:` nele e um evento `task`, e a tarefa vai do primeiro turno depois do marco anterior da sessão ao commit, com o intervalo entre os dois como ociosa da sessão | P3, P2 | `test_brza_note` e `test_summarize_measurements` (unidade); P6 (manual) |
| `Pedido 1`, `R2.2`, `R2.3` | Cada tarefa tem o tempo do agente, o de Anderson e a pausa acima de 30 min por espera, com as esperas da rodada e da interrupção lidas no transcript, e o corrido como a soma | P1, P2 | `test_measure` e `test_summarize_measurements` (unidade); P6 contra o transcript (manual) |
| `Pedido 2` | Cada tarefa tem o custo de API dos turnos e dos subagentes, cada subagente no turno da sessão que contém o começo dele | P2 | `test_summarize_measurements` (unidade) |
| `Pedido 3`, `R1.2` | Cada turno traz a CPU do `claude` e dos filhos e o RSS, pelo `proc_pid_rusage`, e cada `brza run` grava a CPU, o pico e a duração do comando com a sessão que o chamou | P1, P4 | `test_measure` e `test_brza_scripts` (unidade); P1.4 na sessão real (manual) |
| `Pedido 4`, `R1.4` | `summarize_measurements.py --by-task` compara as tarefas por workstream e dia | P2 | `test_summarize_measurements` (unidade); P6 (manual) |
| `R3.1`, `R6.1` | A `## Custo da tarefa` do worklog traz a tarefa até o commit, com o turno em curso lido no transcript, e bate com o `--by-task` | P3, P6 | `test_brza_note` (unidade); P6 (manual) |
| `R0.3`, `R3.2` | O worklog não ganha `opened` nem hora em `completed`; a hora do fim está na `## Custo da tarefa` | P3, P7 | `test_brza_note` (unidade) |
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

### Rodada 6 — o título da seção do worklog (enviada 2026-11-09)

> **Origem:** Anderson pediu em 2026-11-09, no meio do P6.2: "precisamos de um nome que descreva melhor o intuito da
> seção `# Medida`". O levantamento antes da rodada achou o título em `bin/brza-note:845-846`, em 3 linhas do
> `close-task`, em 3 do `core/work/README.md`, no D3, em 9 linhas de teste e nas fixtures golden, e em 5 worklogs de
> 2026-11-09 (4 no `playground`, 1 no `tools-kit`).

Respondida em 2026-11-09, na sessão `c3083ec5` do `tools-kit`.

1. **O título.** Opções:
   - `## O que a tarefa gastou` (recomendada) — diz o intuito e cobre tempo, dinheiro e máquina; custo: ~30–45 min de
     troca, com testes, revisão e um `brza sync`; se paga: a cada worklog lido;
   - `## Custo da tarefa` — curto; custo: o mesmo; se paga: só se "custo" for lido como tempo e máquina, e não só como
     os US$ que a linha também chama de custo;
   - `## Tempo, custo e máquina` — enumera a linha; custo: o mesmo, e envelhece se outra medida entrar.

   **Respondida — "Custo da tarefa"**: o título passa a `## Custo da tarefa`. O comando aceita os dois títulos ao
   reescrever a seção, para os 5 worklogs com `## Medida` trocarem no próximo commit deles sem migração.
2. **Quando.** Opções: P7 do PLN-012, depois da tarefa do `brza run` (recomendada); junto do conserto do `brza run`;
   issue para depois.

   **Respondida — "P7 do PLN-012, depois desta tarefa (Recomendado)"**.

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

Estimado: 4.0 h · Executado: 0.3 h

- [x] **1. Teste que falha** — `tests/cli/test_brza_note.py`: commit com `CLAUDE_CODE_SESSION_ID` → `sessions:` no
  frontmatter, sem repetir no segundo commit, e sem `opened`; linha `task` no log da `MEASURE_DIR`, também com
  `--no-push`; sem a variável → sem carimbo, sem `## Medida` e `session_id: null`; commit recusado → sem evento;
  `--until` fora da janela recusa sem tocar o worklog; `## Medida` reescrita no segundo commit, com o turno em curso lido
  de um transcript de fixture, e com "sem o turno do commit" quando o transcript falta; o `state.json` não muda.
- [x] **2. Implementar** — `set_frontmatter_list`, `write_task_event`, `--until`, `measure_line` (pelo `runpy` do
  resumo e do `measure.py`).
- [x] **3. Rodar e ver passar** — `PYTHONPATH=tests/cli python3 -m unittest test_brza_note test_brza_note_index`
- [x] **4. Commit**

**Evidência:** `brza-workflow@4119ec1` · note e índice → 154 testes OK; classe final `TaskCommitTest` → 22 testes OK ·
revisão aprovada, com duas regressões corrigidas:
[REV-021: O P3 e o ajuste do P5.6 do PLN-012](../../work/reviews/REV-021-pln-012-p3-carimbo-e-medida.md).
O ambiente de teste inclui `PYTHONDONTWRITEBYTECODE=1`; desvio operacional e exceção de revisão no X7.

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

Estimado: 2.0 h · Executado: 1.0 h (0.9 h anteriores e 0.1 h nesta retomada)

- [x] **1. Teste que falha** — `tests/notes-checker`: worklog com `sessions:` e `## Medida` passa sem aviso.
- [x] **2. Escrever** — o passo "2. O que o commit vai fechar" do `close-task`; a linha `sessions` e a `## Medida` no
  `core/work/README.md`; no `CLAUDE.md` do adaptador, os eventos `task` e `run` na tabela do hook e o `--by-task` no
  resumo.
- [x] **3. Rodar e ver passar** — `python3 tests/notes-checker/run.py`
- [x] **4. Commit** — código e norma em `22805fb`, com P3 e P5.6 em `4119ec1`; integração final `fdf266d` e merge
  revisado na `master` em `d38e7b4`, com push em 2026-11-09. Árvore mesclada: 528 testes de CLI OK.
- [x] **5. Abrir as issues** das lacunas, pela sessão que conduz, com `brza note new issue` e `brza note commit` —
  as 10 de `## Pendências conhecidas`, em 2026-11-06.
- [x] **6. O `--workstream` no `--pending` do `close-task`** — corrigido junto do P3 em `4119ec1`; 17 testes golden
  OK, com diferença textual exata registrada. Cobre a sessão cujo único turno está em curso (REV-020, A4).

**Evidência:** `brza-workflow@d38e7b4` · `python3 tests/notes-checker/run.py` → 113 verificações OK · issues em
`tools-kit@c638345` · código e norma em `brza-workflow@22805fb`, complemento em `4119ec1`; revisões:
[REV-018: A revisão do P5 do PLN-012, o close-task e a norma](../../work/reviews/REV-018-pln-012-p5-o-close-task-e-a-norma.md)
e [REV-021: O P3 e o ajuste do P5.6 do PLN-012](../../work/reviews/REV-021-pln-012-p3-carimbo-e-medida.md).

### P6 — Uma tarefa medida de ponta a ponta

Executa a conferência de D1–D6 · executor: sessão que conduz, com Anderson

Estimado: 1.0 h · Executado: 0.9 h (P6.1 8 min, P6.2 42 min, P6.3 5 min)

- [x] **1. `brza sync`** no workspace, e conferir que o `.brza/core.lock` aponta o merge do P5. — `brza sync` →
  `brza-workspace@015fe77`, `core.lock` em `brza-workflow@db6bd28`, 5 arquivos escritos e os seis workstreams
  mesclados; `git diff --quiet d38e7b4 db6bd28 -- core` → sem diferença, então o core é o do merge do P5.
- [x] **2. Uma tarefa real** com rodada, subagente e `brza run`, fechada pelo `close-task`: o aviso aparece, e o
  worklog sai com `sessions:` e `## Medida`. — a tarefa da pasta solta na `master` e do conserto do `brza run`
  (`brza-workflow@ffa29fe`), com três rodadas, um `collector`, três rodadas do `reviewer` e três `brza run`; o
  `--pending` deu "2 turnos desde 19:06 (corrido 36 min, US$ 2,33 dos turnos e US$ 1,79 de 4 subagentes)" depois do
  X9, e o worklog saiu com `sessions:` e `## Medida`:
  [PLN-012: o P6.2, a pasta solta na master e o brza run que perdia as aspas](../../work/worklogs/2026-11-09-pln-012-p6-2-pasta-solta-e-brza-run.md).
- [x] **3. Conferir** — a `## Medida` e a linha do `python3 scripts/summarize_measurements.py --by-task` batem entre si,
  e com o transcript (as esperas lidas à mão), dentro de 5%. — tarefa do P6.2, em 2026-11-09:
  - **Contra o `--by-task`:** a `## Medida` dá 42 min, 33 de agente, 9 de quem pediu e US$ 5,37. O
    `--by-task --json` dá `elapsed_s` 2543, `agent_s` 2031, `requester_s` 512 e US$ 5,47 (1,9%). A diferença é o
    resto do turno depois do commit das 19:48:08, que o D3 prevê.
  - **Contra o transcript:** as quatro esperas de rodada somam 163 + 56 + 121 + 158 = 498 s, contra 512 s
    (2,8%). Os 14 s a mais são o intervalo entre dois turnos. O corrido, de 19:06:15 a 19:48:38, é 2543 s.
  - **O P1.4:** nos quatro turnos da sessão, `machine.from: env` e `cpu_children_s` de 7,31 a 1026,71.
  - **A tarefa do P6.1** passou de 5% no custo (US$ 0,92 contra 0,99), pelo mesmo resto de turno, num turno de
    8 min.

**Evidência:** o worklog da tarefa · a saída do `--by-task`

### P7 — O título `## Custo da tarefa` e a suíte que não escreve no log real

Executa o D3 reescrito (R6.1) e o conserto do X9 · executor: a sessão que conduz, no `brza-workflow`

Estimado: 1.25 h · Executado: 0.8 h

- [x] **1. Teste que falha** — `tests/cli/test_brza_note.py`: o commit grava `## Custo da tarefa`, e o worklog com
  `## Medida` sai com uma seção só, com o título novo; um teste de guarda roda o `brza note commit` com
  `BRZA_WORKSPACE` e `CLAUDE_CODE_SESSION_ID` de mentira no ambiente e confere que nada se escreve fora do temp. —
  o `implementer` mostrou 5 falhas antes do código, em `TaskCommitTest` e em `NoteEnvironmentIsolationTest`.
- [x] **2. Implementar** — `bin/brza-note` (o `re.split` aceita os dois títulos e grava o novo); o isolamento do
  ambiente nos testes do `brza note`; a skill `close-task`, o `core/work/README.md`, as fixtures golden e o
  `tests/notes-checker/run.py`. — mais o corte que ignora o título dentro de cerca (`without_cost_section`) e o
  teste do `--chat` do `brza-run` sem a `BRZA_WORKSPACE`, pela revisão.
- [x] **3. Rodar e ver passar** — `tests/cli`, `tests/hooks` e `tests/notes-checker`, com a mesma lista de falhas de
  antes do passo (as 22 que a `master` já tinha em 2026-11-09, de `note` e `sessions`) ou menor. — com o ambiente
  da sessão, `python3 -m unittest discover -s tests/cli` → 591 testes e 4 FAIL, todos de `test_brza_sessions`
  (checkout relativo e open), contra os 22 da `master`. Os 18 de `note` vinham do mesmo vazamento de ambiente.
  As linhas `task` e `run` de teste no log real ficaram em 0 antes e 0 depois. `tests/hooks` → 348 OK.
  `tests/notes-checker/run.py` → saída 0.
- [x] **4. Revisão** pelo `reviewer` e **commit**; depois, `brza sync`. — revisão interna em três rodadas: A1 (as
  linhas `run` do teste do `--chat`), A2 (o título dentro de cerca), B1 e B2 (as regras da cerca) e C1 (o comprimento
  da cerca), todos corrigidos aqui; C2 descartado, por ser a volta deliberada ao corte de antes do P7. As 3 linhas
  `run` saíram do log, com backup em `measurements.jsonl.bak-2026-11-09-run`. Commits: `brza-workflow@5642ae8`, com
  o merge em `7afed94`; `brza sync` → `brza-workspace@75c88b0`, com os seis workstreams mesclados.

**Evidência:** o commit no `brza-workflow` · a lista de falhas antes e depois · o `measurements.jsonl` sem `task` novo
depois de rodar a suíte numa sessão

### P8 — Os achados da revisão da entrega

Executa os quatro achados `corrigido aqui` do REV-024 (D1, D3 e o `close-task` do P5) · executor: a sessão que conduz,
no `brza-workflow`

Estimado: 0.5 h · Executado: 0.4 h

- [x] **1. Teste que falha** — `test_the_task_event_carries_the_pid_of_the_session_claude` (A2),
  `test_the_cpu_follows_the_number_rule_of_the_section` (A3) e o assert de CPU de
  `test_current_machine_uses_saved_baseline_without_writing_it`: os três falharam no `7afed94`.
- [x] **2. Implementar** — o `pid` do evento `task` pelo `claude_pid()` do `measure.py` (A2); a CPU da seção pelo
  `human_duration` (A3); o `close-task` e a fixture golden citam também a `## Medida` (A1); o texto do plano e do
  Desenho (A4).
- [x] **3. Rodar e ver passar** — `PYTHONPATH=tests/cli python3 -m unittest test_brza_note test_brza_note_index
  test_brza_scripts` → 210 OK; `tests/hooks` → 348 OK; `tests/notes-checker/run.py` → saída 0.
- [x] **4. Revisão e commit** — a segunda rodada do REV-024 aprovou. Commits: `brza-workflow@829527c`, com o merge em
  `b2b497d`, feito num worktree destacado (X10); `brza sync` → `brza-workspace@ba60bb6`, com os seis workstreams
  mesclados.

**Evidência:** `brza-workflow@b2b497d` · o REV-024

**Total estimado:** 17,75 h (o P8 somado em 2026-11-09, pelo REV-024) contra os 16 h do corte; antes, 17,25 h
(o P7 somado em 2026-11-09, pela R6); antes:
16 h (P1 3,5 + P2 4 + P3 4 + P4 1,5 + P5 2 + P6 1) contra ~12,5 h somadas
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
- **X7 — P3 num clone temporário e revisão interna nesta execução.** Para respeitar o sandbox, o P3 foi implementado
  num clone isolado em `/private/tmp`, saído da integração, e integrado depois. A aprovação automática bloqueou a
  chamada de revisão ao `agy` por possível envio de código privado; Anderson respondeu em 2026-11-09, nesta sessão,
  "Usar somente um subagente interno nesta execução". O `reviewer` independente aprovou P3 e P5.6 após duas correções
  (REV-021). O comando de teste usa `PYTHONPATH=tests/cli` para importar os módulos de teste. Não altera os contratos
  do Desenho nem a preferência durável de revisão.

- **X8 — O contrato do `brza run` mudou no P6.2.** O primeiro `brza run` da tarefa, `bash -c '…'`, rodou partido:
  o `brza-run` juntava os argumentos com espaço, "como no ssh" (contrato documentado e testado desde o D5). Anderson
  escolheu "Consertar aqui" e depois "Trocar o contrato (Recomendado)": um argumento só segue como linha de shell, e
  vários chegam inteiros, citados também quando começam com `=` (`brza-workflow@ffa29fe`). Afeta o D5 e o P4.
- **X9 — A suíte de CLI do `brza-workflow`, rodada dentro de uma sessão, grava `task` no log real.** Os testes do
  `brza note commit` herdam `BRZA_WORKSPACE` e `CLAUDE_CODE_SESSION_ID`: em 2026-11-09, três rodadas da suíte gravaram
  56 marcos falsos desta sessão e 28 da `508e76c8`, que partiram a tarefa do P6.2. Anderson escolheu "Remover, com
  backup (Recomendado)" e "Corrigir no P7 (Recomendado)". Saíram 84 linhas `task` (`cwd` no temp do macOS ou no
  `brza-workflow`), com o backup em `.measurements/measurements.jsonl.bak-2026-11-09`. Afeta o P3 e cria o P7.

- **X10 — O merge do P8 não passou pela `master` local do `brza-workflow`.** No checkout principal havia mudanças
  sem commit de outra sessão (PLN-018: o `GROK_SESSION_ID` no `task_context` do `bin/brza-note`, o
  `brza-sessions`, o `runtime_turn.py`). O merge foi feito num worktree destacado, sobre a `origin/master`, com push
  direto (`b2b497d`), e a `master` local ficou 2 commits atrás. Duas consequências:
  - o `brza note`, que roda daquele checkout, só passa a gravar o pid do `claude` e a CPU nova quando a outra sessão
    commitar e atualizar;
  - as mudanças dela vão conflitar com o P8 na linha `'pid'` do evento `task`.

  O plano do PLN-018 também tinha edições sem commit, então o aviso ficou aqui e no worklog.

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
- 2026-11-09 — P3 e P5.6: revisão interna autorizada por Anderson nesta execução, aprovada após duas correções.
  [REV-021: O P3 e o ajuste do P5.6 do PLN-012](../../work/reviews/REV-021-pln-012-p3-carimbo-e-medida.md)
- 2026-11-09 — a entrega inteira: duas rodadas do `reviewer`; quatro achados corrigidos no P8 e três falsos.
  [REV-024: A revisão da entrega do PLN-012, a medida por tarefa](../../work/reviews/REV-024-pln-012-entrega.md)

## Documentação

- `brza-workflow/core/work/README.md`, a tabela de propriedades (`sessions`) e a seção `work/worklogs/` (o
  `sessions:` e a `## Custo da tarefa`) — P5, P7.
- `brza-workflow/core/.claude/skills/close-task/SKILL.md`, os passos 2 a 7 — P5, P7, P8.
- `brza-workflow/core/CLAUDE.md`, a tabela do hook de medição (`task`, `run`) e o `--by-task` — P5.
- `brza-workflow/packages/client/bin/brza-run`, o docstring com o contrato dos argumentos — P4, X8.

## Fechamento

- [x] Todo passo `[x]` com evidência, ou `[-]` com motivo. O P1.4 foi movido ao P6 e conferido no P6.3.
- [x] Todo achado com destino que existe: REV-017 a REV-021 e REV-024, com as issues em `## Pendências conhecidas`.
- [x] Um resumo por commit ou PR do `brza-studio` da entrega: não se aplica, porque a entrega é só do `brza-workflow` e
      das notas, em commits diretos na `master`.
- [x] O durável saiu para a casa dona e está em `## Documentação`: a norma do `core/` e o contrato do `brza-run`.
      O plano não respondeu nem abriu nota de `work/decisions/`, porque as rodadas decidiram o próprio contrato da
      medida, que mora na norma.
- [x] As decisões que o plano respondeu estão `done`, citando a rodada: não há nota de decisão.
- [x] `status: done`, `phase: closed` e `completed` no frontmatter.

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
- 2026-11-09 — P3, P5.6 e P5.4 concluídos, com merge e push em `brza-workflow@d38e7b4`; 528 testes de CLI OK na
  árvore mesclada. Só o P6 permanece pendente, por pedido de Anderson.
  [PLN-012: o P3 e a integração da medida por tarefa](../../work/worklogs/2026-11-09-pln-012-p3-e-integracao.md)
- 2026-11-09 — P6.1 feito: `brza sync` → `brza-workspace@015fe77`, lock em `brza-workflow@db6bd28`; a tarefa do P6.2
  é a investigação da `master` atrasada.
  [PLN-012: o P6.1, o brza sync que instala a medida por tarefa](../../work/worklogs/2026-11-09-pln-012-p6-1-brza-sync.md)
- 2026-11-09 — P6.2 feito: a pasta solta apagada, o `brza run` com cada argumento inteiro (`brza-workflow@ffa29fe`,
  X8), o log limpo dos `task` de teste (X9), R6.1 respondida e o P7 aberto.
  [PLN-012: o P6.2, a pasta solta na master e o brza run que perdia as aspas](../../work/worklogs/2026-11-09-pln-012-p6-2-pasta-solta-e-brza-run.md)
- 2026-11-09 — P6.3 conferido (1,9% e 2,8%); P7 (`brza-workflow@7afed94`) e P8 (`b2b497d`, X10) entregues; a
  entrega revisada no REV-024; o plano fechado.
  [PLN-012: o P6.3, o P7, o P8 e o fechamento da medida por tarefa](../../work/worklogs/2026-11-09-pln-012-p6-3-p7-p8-e-fechamento.md)
