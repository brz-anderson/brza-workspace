---
status: open
phase: design
origin: request
description: Liga a medição às tarefas, para que cada uma mostre o tempo corrido, o custo de API e o recurso de máquina, e o fluxo se afine por dado.
ready: "não — falta o Desenho dos itens D no brza-workflow; isso trava os Passos"
scope:
  - brza-workflow
opened: 2026-11-03
owner: Anderson
priority: medium
tags:
  - tooling
---

# PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou

- **Retomar:** R1 e R2 respondidas em 2026-11-03; a entrevista fechou a estrutura. Próximo: o Desenho, por um
  `designer` com o Terreno — o carimbo no worklog, o evento `task`, os três tempos, a CPU no hook e no `brza run`, o
  `--by-task` e a linha no worklog —, com os pontos em aberto listados em "O que este desenho assume".

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

## Desenho

### O que este desenho assume

- **R1.1, R2.1:** a tarefa é o worklog. O `brza note commit` carimba nele o `CLAUDE_CODE_SESSION_ID` e grava um evento
  na medição; a tarefa começa no primeiro prompt depois do marco anterior da mesma sessão.
- **R2.2, R2.3:** três tempos — agente, Anderson, pausa acima de 30 min — e o corrido como a soma.
- **R1.2:** a máquina é a CPU e o RSS do `claude` com os filhos que saíram (`ps -S`, no hook) e o rusage do comando do
  `brza run`.
- **R1.3, R2.4:** "não medida" e "sem tarefa" ficam à vista; o `close-task` avisa os turnos sem tarefa; toda lacuna
  deixada vira issue.
- **R1.4:** o resultado aparece no `summarize_measurements.py --by-task` e numa linha do worklog.
- **R0.3:** a forma das datas do worklog sai daqui. A leitura desta sessão é que o worklog não ganha `opened` nem hora
  em `completed`: o começo e o fim saem da medição e do carimbo. Vai ao Desenho como ponto a confirmar.

**Em aberto para o Desenho** (rascunho do `designer`, depois rodada):
- o nome e a forma do carimbo no frontmatter (`sessions:`, como o `refs:`) e do evento na medição;
- o worklog que recebe commits em mais de uma sessão, ou mais de um commit na mesma;
- a atribuição do subagente à janela da tarefa — se a linha `subagent` traz o `session_id` da sessão que o chamou;
- como o hook acha o PID do `claude` (subindo os `ppid`) e se o `ps -S` conta os netos, que é o caso do teste
  rodado pelo `Bash`;
- a espera da rodada lida no transcript, entre o `tool_use` da pergunta e o `tool_result`;
- o que entra na linha de medida do worklog, e a do turno do próprio commit, que fica de fora.

### Terreno

#### O worklog e as datas

- **O frontmatter do worklog guarda só `scope`, `tags` e `refs`; a data mora no nome.** `work/README.md:310-311`.
  `opened` e `completed` são "Data" na tabela comum (`work/README.md:229`, `:231`).
- **O esqueleto do worklog não tem `opened`.** `brza-workflow/bin/brza-note:188-201`, a constante `WORKLOG`.
- **O `close-task` cria o worklog à mão, quando a tarefa fecha**, sem o `brza note new worklog`.
  `brza-workflow/core/.claude/skills/close-task/SKILL.md:30-32`. Por isso um `opened` carimbado na criação marcaria a
  escrita da nota, minutos antes do fim, e o `completed` com hora repete o `git log --format=%aI` do worklog.

#### A medição

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

#### O que já liga a sessão à tarefa

- **A sessão enxerga o próprio id.** `CLAUDE_CODE_SESSION_ID` está no ambiente do `Bash` da sessão, e é o mesmo id do
  `claude_session` do mapa de sessões (`08e6c812-…` nesta sessão). Um comando que a sessão roda, como o
  `brza note commit`, pode gravá-lo sem a sessão digitar nada.
- **O transcript guarda o nome da sessão**, nas linhas `custom-title` e `agent-name`
  (`~/.claude/projects/…-tools-kit/4a578e01-….jsonl`: `customTitle: tools-kit-rev-pln009`).
- **O `brza sessions` já liga o nome e o título ao id.** `.sessions/sessions.jsonl`, desde 2026-10-29 22:31: 44
  aberturas (42 Claude, 1 Codex, 1 Antigravity), com o título no padrão "PLN-008 P8: …" e o `claude_session`.
- **Mas o mapa cobre a minoria da medição.** Desde 2026-10-29 22:31: 25 das 100 sessões com turno estão no mapa, com
  US$ 156 dos US$ 394 de turno e US$ 63 dos US$ 258 de subagente.

#### A máquina

- **O `ps -S` do macOS soma à CPU de um processo a dos filhos que já saíram.** `man ps`, flag `-S`. O processo da
  sessão é o `claude` (`ps -p $PPID` no `Bash`: `/Users/andepb/.local/bin/claude`, 360 MB de RSS).
- **O `brza run` roda o comando numa aba do app, fora da árvore de processos da sessão.**
  `brza-workflow/packages/client/bin/brza-run:1-12`: abre uma aba visível e espera o comando.

#### O começo do turno

- **O `duration_s` do turno vai da primeira linha do trecho novo do transcript à última**, e a primeira é o prompt.
  `brza-workflow/core/.claude/hooks/measure.py:342`, `:406-413`. O começo do turno é `timestamp − duration_s`, sem
  campo novo.
- **A espera numa pergunta com opções cai dentro do turno.** A ferramenta segura o turno até a resposta, e o
  `duration_s` soma o tempo de Anderson pensando na rodada (inferido do cálculo acima; a conferir no Desenho).

## Worklogs

- 2026-11-03 — aberto; Rodada 0 transcrita; Terreno levantado; R1 e R2 respondidas; issue do Codex e do
  Antigravity aberta. Parou antes do Desenho.
  [Abertura do PLN-012, a produtividade medida por tarefa](../../work/worklogs/2026-11-03-pln-012-abertura-da-produtividade-por-tarefa.md)
