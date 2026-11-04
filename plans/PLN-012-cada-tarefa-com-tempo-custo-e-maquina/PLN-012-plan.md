---
status: open
phase: design
origin: request
description: Liga a medição às tarefas, para que cada uma mostre o tempo corrido, o custo de API e o recurso de máquina, e o fluxo se afine por dado.
ready: "não — falta o aceite do corte dos Passos; isso trava a execução"
scope:
  - brza-workflow
opened: 2026-11-03
owner: Anderson
priority: medium
tags:
  - tooling
---

# PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou

- **Retomar:** R1 a R4 respondidas e o Desenho (D1–D7) gravado em 2026-11-03. Próximo: a rodada do corte dos
  Passos P1–P6 (16 h); aceito o corte, os Passos entram aqui e o plano vai a `execution`.
- **Dividido:** [PLN-012 — Desenho](PLN-012-design.md)

## Pedido

- **Origem:** pedido livre de Anderson em 2026-11-03, na sessão "Plano: chat via CLI e plugins" do `playground`,
  trazido à sessão `tools-kit-produtividade` do `tools-kit`. Nasceu de uma rodada sobre gravar data e hora (ISO 8601)
  em `opened` e `completed` do worklog, em que Anderson não escolheu nenhuma opção e trocou a pergunta por este pedido.

> "precisamos de uma forma de medir nossa produtividade, quanto realmente demoramos para executar as tarefas, quanto
> gastamos de recursos em cada tarefa - aqui inclui custo da API, recurso de maquina e tempo corrido - para irmos
> afinando o fluxo"

### Cobertura

| Origem     | Critério de aceite                                                                     | Passo        | Teste (nível)       |
| :--------- | :------------------------------------------------------------------------------------- | :----------- | :------------------ |
| `Pedido 1`, `R1.1`, `R2.1` | O `brza note commit` de um worklog grava o id da sessão nele e um evento `task` na medição, e a tarefa vai do primeiro prompt depois do marco anterior da sessão até esse commit | a planejar | a planejar |
| `Pedido 1`, `R2.2`, `R2.3` | Cada tarefa tem o tempo do agente, o de Anderson e a pausa (o parado acima de 30 min), e o corrido como a soma | a planejar | a planejar |
| `Pedido 2` | Cada tarefa tem o custo de API dos turnos e dos subagentes da janela dela | a planejar | a planejar |
| `Pedido 3`, `R1.2` | Cada tarefa tem a CPU e a memória da sessão, pelo `ps -S` do `claude` no hook, e a dos comandos rodados pelo `brza run` | a planejar | a planejar |
| `Pedido 4`, `R1.4` | `summarize_measurements.py --by-task` compara as tarefas, e o worklog leva uma linha de medida ao fechar | a planejar | a planejar |
| `R1.3`, `R2.4` | A tarefa sem turno medido aparece como "não medida"; os turnos sem worklog, como "sem tarefa", e o `close-task` avisa quantos são; toda lacuna que o plano deixar tem issue | a planejar | a planejar |

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

## Worklogs

- 2026-11-03 — aberto; Rodada 0 transcrita; Terreno levantado; R1 e R2 respondidas; issue do Codex e do
  Antigravity aberta. Parou antes do Desenho.
  [Abertura do PLN-012, a produtividade medida por tarefa](../../work/worklogs/2026-11-03-pln-012-abertura-da-produtividade-por-tarefa.md)
- 2026-11-03 — R3 e R4 respondidas; D1–D7 gravados no `-design`; o `ps -S` trocado pelo `proc_pid_rusage`. Parou na
  rodada do corte dos Passos.
  [Desenho do PLN-012, a medida por tarefa](../../work/worklogs/2026-11-03-pln-012-desenho-da-medida-por-tarefa.md)
