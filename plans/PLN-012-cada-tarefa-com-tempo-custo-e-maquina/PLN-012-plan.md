---
status: open
phase: interview
origin: request
description: Liga a medição às tarefas, para que cada uma mostre o tempo corrido, o custo de API e o recurso de máquina, e o fluxo se afine por dado.
ready: "não — falta a R1 (o que é a tarefa, a máquina, as sessões não medidas e onde aparece); isso trava o Desenho"
scope:
  - brza-workflow
opened: 2026-11-03
owner: Anderson
priority: medium
tags:
  - tooling
---

# PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou

- **Retomar:** aberto em 2026-11-03, com o Terreno levantado; a R1 foi enviada e espera resposta. Depois dela, o
  Desenho dos itens `D` no `brza-workflow`.

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
| `Pedido 1` | Cada tarefa tem o tempo corrido, do começo ao fim, e não só a soma dos turnos           | a planejar   | a planejar          |
| `Pedido 2` | Cada tarefa tem o custo de API dos turnos e dos subagentes dela                         | a planejar   | a planejar          |
| `Pedido 3` | Cada tarefa tem o recurso de máquina que gastou: CPU e memória                          | a planejar   | a planejar          |
| `Pedido 4` | As tarefas se comparam lado a lado, por workstream e por período, para afinar o fluxo   | a planejar   | a planejar          |

> Os critérios acima são rascunho até a R1 dizer o que é a tarefa e onde o resultado aparece.

### Fora de escopo

- **Mudar o fluxo a partir dos números.** O plano entrega a medida; o afinar é de cada plano ou decisão que a usar.

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

## Desenho

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

## Worklogs

- 2026-11-03 — aberto; Rodada 0 transcrita; Terreno levantado; R1 enviada.
  [Abertura do PLN-012, a produtividade medida por tarefa](../../work/worklogs/2026-11-03-pln-012-abertura-da-produtividade-por-tarefa.md)
