---
status: in_progress
phase: execution
origin: request
ready: sim
estimate_h: 9
executed_h: 0.4
remaining_h: 8
scope:
  - workspace
opened: 2026-10-31
owner: Anderson
tags:
  - tooling
---

# PLN-005: A confiança dos fatos do desenho se mede contra o que se sustentou

- **Retomar:** P1 e P2 feitos; o próximo é o P3, a captura, pelo `implementer`, a pedido de Anderson.

## Pedido

- **Origem:** pedido livre, na sessão do workstream `workspace` de 2026-10-31.

> "encontrar um mecanismo de medir tbm a confiança dos fatos coletados das sugestões de desenho"

### Cobertura

| Origem             | Critério de aceite                                                                                                                               | Passo | Teste (nível)                                                     |
| :----------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- | :---- | :---------------------------------------------------------------- |
| `Pedido 1`, R1.1–2 | Cada fato do `designer` e do `collector`, e cada custo e "se paga" das opções do `designer`, sai com a marca de id, tipo de evidência e confiança | P2 | o parser de marcas sobre uma devolução de fixture (unidade)       |
| `Pedido 1`, R1.3   | Cada marca da devolução vira uma linha no `measurements.jsonl`, com o `agent_id`, o tipo e a confiança                                           | P3 | o hook sobre um transcript de fixture (unidade)                   |
| R1.3, R2.1         | A devolução do `designer` e do `collector` solta a auditoria Haiku em segundo plano, sem segurar o hook                                          | P4, P8 | o disparo com o `claude` trocado por um espião (unidade); uma devolução real gera o veredito (manual) |
| R1.3, R2.2         | A sessão registra o desfecho de um fato "a conferir" ou de um custo pelo `scripts/fact_outcome.py`                                              | P5, P7 | o script grava a linha e recusa id que não existe (unidade)       |
| `Pedido 1`         | O resumo mostra o acerto por faixa de confiança, por papel e por tipo de evidência                                                               | P6 | o resumo sobre um log de fixture (unidade)                        |

### Fora de escopo

- **A marca nos achados do `reviewer`.** Ele já dá a confiança em número (`.claude/agents/reviewer.md:17`); medir o
  acerto dele fica para depois que este mecanismo tiver amostra.
- **A marca nos agentes do Codex e do `agy`.** Os papéis deles são do PLN-004.

## Entrevista

### Rodada 1 — escopo, marca e desfecho (enviada 2026-10-31)

**Apresentado antes**, na sessão do workstream `workspace`:
- Só o `reviewer` dá confiança em número, de 0 a 100, com corte em 80 (`.claude/agents/reviewer.md:17`). O `designer`
  e o `collector` dão só a fonte; fato sem fonte é "inferência" (`.claude/agents/collector.md:15`) ou "a conferir"
  (`.claude/agent-memory/designer/feedback_medir-antes-de-desenhar.md`). Ninguém confere depois se o fato se
  sustentou.
- O melhor argumento contra a confiança do `reviewer` foi o número dado pelo mesmo modelo que escreve o achado
  (`work/worklogs/2026-10-31-o-porte-das-skills-da-fixfy.md:49`): medir o acerto responde a ele.
- O único fato errado registrado do `designer` foi uma estimativa de custo: o symlink do `hooks.json` saiu "barato" e
  não rodou (`.claude/agent-memory/designer/feedback_custo-de-symlink-com-confianca.md`).
- O evento `subagent` não guarda o conteúdo da devolução (`.claude/hooks/measure.py:434-476`), mas já lê o transcript
  do subagente.
- Volume: 5 rodadas do `designer` (média de US$ 1,79) e 6 do `collector` (US$ 1,71) no log até 2026-10-31; com uns 10
  fatos por rodada, umas 100 amostras em uma ou duas semanas.
- O mecanismo proposto: a marca `F3 · lido · 90` em cada fato; o hook grava um evento por marca; um Haiku refaz a
  evidência; o resumo mostra o acerto por faixa.

Respondida em 2026-10-31.

1. **Escopo**, seleção múltipla. Opções:
   - fatos do `designer` (recomendada) — custo: uma regra no `designer.md` e umas 10 marcas por devolução, quase sem
     token a mais; se paga: com umas 50 amostras, quando se vê se o 90 dele acerta 9 em 10;
   - fatos do `collector` — custo: a mesma regra no `collector.md`, o papel de mais volume; se paga: na mesma fase, mais
     cedo, porque dá mais amostra;
   - custos e "se paga" das opções — custo: a marca em cada opção, com o desfecho só conhecido na fase em que o custo se
     cobra; se paga: tarde, mas é o único erro já registrado.

   **Decidido — as três.**

2. **Marca.** Opções:
   - número e tipo, como `F3 · lido · 90`, na régua do `reviewer` (recomendada) — custo: uma regra no papel e um parser
     simples no hook; se paga: na primeira leitura de calibração, porque o número é o que se compara com o acerto;
   - só o tipo de evidência — custo: menor, e foge do número dado pelo mesmo modelo; se paga: mede o acerto por tipo,
     mas nunca diz se a confiança está calibrada.

   **Decidido — "Número e tipo (Recomendado)".**

3. **Desfecho.** Opções:
   - um Haiku audita e a sessão registra (recomendada) — custo: uns US$ 0,02 por auditoria, estimados pela tabela do
     Haiku 5.5 (~450 mil tokens, quase todos em cache), e um comando novo; se paga: em umas duas semanas, com amostra
     sem viés;
   - só a sessão registra — custo: zero em tokens, e depende de disciplina; se paga: talvez nunca, porque só o fato que
     caiu aparece e o acerto sai inflado;
   - só na revisão do `reviewer` — custo: aproveita a revisão (~US$ 2,27 em Opus), só nos planos revisados; se paga:
     devagar, com uma revisão até hoje.

   **Decidido — "Haiku audita + sessão (Recomendado)".**

### Rodada 2 — disparo, comando e caminho (enviada 2026-10-31)

**Apresentado antes:** o auditor não refaz o comando de um fato `rodado`, porque refazer o comando de outro agente em
segundo plano pode mudar estado; ele confere a saída que ficou no transcript do subagente. O `brza` é do `tools-kit`
(`AGENTS.md`, "Os de agora"), e um `brza fact` seria pedido a outra sessão.

Respondida em 2026-10-31.

1. **Disparo.** Opções:
   - o hook, em segundo plano (recomendada) — o `SubagentStop` do `designer` e do `collector` solta um
     `claude -p --model haiku` só de leitura, sem bloquear; custo: uns US$ 0,02–0,05 por auditoria, porque a sessão
     `-p` carrega a norma (~25 mil tokens), e o cuidado de não auditar a auditoria; se paga: desde a primeira devolução,
     porque toda devolução é auditada sem depender de disciplina;
   - um papel `auditor` acionado pela sessão — custo: uma chamada a mais por devolução, no mesmo custo de tokens, e
     depende de a sessão lembrar; se paga: só se a disciplina se mantiver, porque a devolução esquecida é amostra
     perdida.

   **Decidido — "O hook, em segundo plano (Recomendado)".**

2. **Comando do desfecho.** Opções:
   - um script deste workstream, `scripts/fact_outcome.py`, ao lado do `summarize_measurements.py`, que grava
     `fact_outcome` no `measurements.jsonl` (recomendada) — custo: um script pequeno com testes, nesta frente; se paga:
     agora, sem esperar o `tools-kit`;
   - `brza fact`, no `tools-kit` — custo: pedido a outra sessão, e espera; se paga: quando o `tools-kit` o fizer, e até
     lá o desfecho fica sem registro.

   **Decidido — "Script deste workstream (Recomendado)".**

3. **Caminho.** Opções:
   - PLN novo, pelo `plan-runner` (recomendada) — custo: o arranque do plano, uns 15–20 min; se paga: na segunda sessão,
     ou quando a calibração for lida, daqui a umas duas semanas, e precisar do porquê;
   - worklog direto, nesta sessão — custo: menor agora; se paga: agora, mas sem `Retomar` nem Cobertura para o que
     ficar pendente na auditoria em segundo plano.

   **Decidido — "PLN novo, pelo plan-runner (Recomendado)".**

### Rodada 3 — onde mora o disparo, o que o parser lê e o lembrete (enviada 2026-10-31)

**Apresentado antes:** o `measure.py` promete "Só mede: nunca bloqueia nem escreve fora de .measurements/"
(`.claude/hooks/measure.py:22`); o `collector` grava o agregado no scratch e devolve só o resumo
(`.claude/agents/collector.md:16`); o desfecho de um fato "a conferir" ou de um custo chega dias depois.

Respondida em 2026-10-31.

1. **Onde mora o disparo.** Opções:
   - um `.claude/hooks/fact_audit.py` com entrada própria no `SubagentStop` (recomendada) — custo: um arquivo e uma
     entrada a mais, e o transcript lido duas vezes, em milissegundos; se paga: agora, porque o `measure.py` segue só
     medindo e a falha da auditoria não vira `hook_error` da medição;
   - dentro do `measure.py` — custo: menos código agora, mas quebra a promessa do docstring; se paga: só na economia de
     um arquivo, nunca no isolamento.

   **Decidido — "fact_audit.py separado (Recomendado)".**

2. **O que o parser lê.** Opções:
   - a devolução e os arquivos que o subagente gravou com `Write` (recomendada) — custo: umas 20 linhas a mais no
     parser e uma auditoria maior, talvez US$ 0,05; se paga: na primeira devolução do `collector`, cujos fatos ficam
     quase todos no agregado;
   - só a mensagem final — custo: menor; se paga: no `designer`, com o `collector` de amostra rasa.

   **Decidido — "Devolução + arquivos gravados (Recomendado)".**

3. **O lembrete do desfecho.** Opções:
   - o `close-task` lista os pendentes, pelo `fact_outcome.py --pending` (recomendada) — custo: um passo na skill e uma
     opção no script, uns segundos por fechamento; se paga: no primeiro fechamento em que uma sonda ou rodada respondeu a
     um fato;
   - sem lembrete — custo: zero; se paga: nunca para os custos, cujo desfecho chega em outra sessão.

   **Decidido — "O close-task lista os pendentes (Recomendado)".**

### Rodada 4 — o aceite do Desenho e do corte (enviada 2026-10-31)

**Apresentado antes:** o plano inteiro, na mensagem, com D1–D6, P1–P9 e a Regressão.

Respondida em 2026-10-31.

1. **Aceite.** Opções:
   - aceitar D1–D6 e P1–P9 como estão (recomendada) — custo: 9 h estimadas e uns US$ 0,02–0,05 por devolução
     auditada, a confirmar no P1; se paga: em umas duas semanas, com ~100 fatos medidos, e o commit sai por passo verde;
   - juntar P3–P6 numa entrega só do `implementer` — custo: um passo de 6 h revisado de uma vez, sem commit por parte;
     se paga: agora, em menos ida e volta, mas a falha do P4 segura o P5 e o P6;
   - só o P1 agora, e o corte depois da sonda — custo: uma rodada a mais; se paga: só se a sonda desmentir o D2.

   **Decidido — "1"**: o plano está aceito em 2026-10-31. A execução segue passo a passo, a pedido.

## Desenho

### O que este desenho assume

- **R1.1:** levam a marca os fatos do `designer`, os do `collector` e os custos e "se paga" das opções do `designer`.
- **R1.2:** a marca é número e tipo, na régua do `reviewer`.
- **R1.3:** um Haiku refaz a evidência dos fatos `rodado`, `lido` e `doc`; a sessão registra o desfecho dos `inferido`,
  dos abaixo de 80 e dos custos.
- **R2.1, R3.1:** o disparo é do hook, em segundo plano, num `fact_audit.py` separado do `measure.py`.
- **R2.2, R3.3:** o desfecho da sessão vai pelo `scripts/fact_outcome.py`, e o `close-task` lista os pendentes.
- **R3.2:** o parser lê a mensagem final e os arquivos gravados com `Write` no trecho do subagente.

### Terreno

#### A medição

- **O evento `subagent` não guarda a devolução.** `.claude/hooks/measure.py:434-476` — soma tokens e custo do
  transcript, que acha por `agent_transcript` (`:425-431`), e lê a partir do offset do `.measurements/state.json`.
- **O hook só mede.** `.claude/hooks/measure.py:23` — e engole toda exceção num `hook_error` (`:723-737`).
- **O `SubagentStop` tem uma entrada só**, `measure.py subagent || true`, com `timeout: 30`
  (`.claude/settings.json`, `hooks.SubagentStop`).
- **O resumo** lê o log de `DEFAULT_DIR` (`scripts/summarize_measurements.py:32`), com `--since`, `--json` e
  `--by-workstream` (`:349-360`); os testes ficam em `.claude/hooks/tests/test_summarize_measurements.py`.
- **O preço do Haiku 5.5** é US$ 0,10/M de entrada e US$ 0,01/M de leitura de cache até 100 mil tokens por pedido
  (`.claude/hooks/measure.py:47-56`).

#### O `claude -p`

- **A sessão `-p` da auditoria**, sondada no P1 com o `claude` 2.1.316, no worktree do `workspace`:
  - **O modelo** é o `claude-haiku-5-5` com `--model haiku`.
  - **As ferramentas** são as do `--tools` (`Glob`, `Grep`, `Read`, `WebFetch`) mais as duas do MCP do `context7`, que
    o projeto habilita; todas são de leitura. O `permissionMode` herdado é `auto`.
  - **O custo** de três fatos foi US$ 0,0056, em 4 turnos e 9,6 s — abaixo dos US$ 0,02–0,05 estimados na R1.3.
  - **A saída** `--output-format json` é um objeto com `result`, `total_cost_usd`, `num_turns`, `duration_ms`,
    `is_error`, `subtype` e `modelUsage`.
  - **O `--max-budget-usd`** corta depois do pedido que passa do teto: saída 1, `subtype: error_max_budget_usd`,
    `terminal_reason: budget_exhausted`, `result` nulo e o custo gasto no `total_cost_usd` (US$ 0,0029 num teto de
    US$ 0,001).
  - **Os hooks do projeto rodam** na sessão `-p` e enxergam o `BRZA_FACT_AUDIT=1`; o `Stop` dela gravou um `turn`
    `claude-haiku-5-5` de US$ 0,01 no `workstream` `workspace` — o custo em dobro que o D6 tira do resumo.

#### Os papéis e a skill

- **A régua de confiança** está em `.claude/agents/reviewer.md:17-19`. O `designer` pede a fonte só no levantamento
  (`.claude/agents/designer.md:21-23`); o `collector`, em cada fato (`.claude/agents/collector.md:15`).
- **O `close-task`** tem o passo `## 3. O pendente` (`.claude/skills/close-task/SKILL.md:39-43`).

### D1 — A marca — `.claude/agents/designer.md`, `.claude/agents/collector.md` (P2)

- **Origem:** R1.1, R1.2, R3.2
- **Contexto:** o hook só mede o que acha escrito numa forma fixa; a régua é a do `reviewer`, para que as duas
  confianças se leiam igual.

#### Como fica

No `designer.md`, depois de "A recomendação leva o argumento…"; no `collector.md`, no lugar de "Cada fato vai com a
fonte…", sem a parte dos custos:

```markdown
- **Cada fato e cada custo levam a marca no fim da linha**, `[F3 · lido · 90]`, também no agregado do scratch:
  - o id: `F` para fato, `C` para custo ou "se paga", numerados na devolução e continuados na retomada;
  - o tipo de evidência: `rodado`, o comando rodou nesta execução; `lido`, o `arquivo:linha` foi aberto nesta execução;
    `doc`, a URL ou a documentação foi lida nesta execução; `inferido`, sem fonte direta;
  - a confiança, de 0 a 100, na régua do `reviewer`: 90 ou mais, verificado direto; de 80 a 89, com a premissa
    escrita; abaixo de 80, a conferir. O `inferido` fica abaixo de 80.

  Um Haiku refaz a evidência dos `rodado`, `lido` e `doc` depois da devolução; o desfecho dos outros vem da sonda ou da
  rodada. O acerto por faixa se mede.
```

A redação final passa pela `agent-instructions-writer`, que decide se a régua sobe ao `AGENTS.md`, em "A devolução do
subagente", e os papéis só apontam.

### D2 — A captura e a auditoria — `.claude/hooks/fact_audit.py` (P3, P4)

- **Origem:** R1.3, R2.1, R3.1, R3.2
- **Contexto:** o hook não pode segurar o fim do subagente; a auditoria leva minutos.

#### Como fica

Uma entrada a mais no `SubagentStop`, depois da do `measure.py`:

```json
{"type": "command", "command": "${BRZA_PYTHON:-python3} \"${BRZA_WORKSPACE:-$CLAUDE_PROJECT_DIR}/.claude/hooks/fact_audit.py\" stop || true", "timeout": 10}
```

O script tem dois modos e importa do `measure.py` o `agent_transcript`, o `read_from`, o `write`, o `now` e o
`workstream_of`:

- **`stop`**, no hook:
  1. sai sem nada com `BRZA_FACT_AUDIT` no ambiente (a própria auditoria) ou com `agent_type` fora de `designer` e
     `collector`;
  2. lê o trecho novo do transcript, pelo offset próprio em `.measurements/fact-audit-state.json`;
  3. tira as marcas da última mensagem de texto do assistente e do `content` de cada `Write` do trecho, pela expressão
     `\[([FC])(\d+) · (rodado|lido|doc|inferido) · (\d{1,3})\]`; o `[F` ou `[C` seguido de dígito que não casa conta
     como marca malformada;
  4. grava um evento `fact` por marca — `agent_id`, `agent_type`, `session_id`, `workstream`, `fact_id`, `kind`,
     `confidence`, `text` (a linha da marca, até 300 caracteres), `source` (`reply` ou o caminho do arquivo) — e um
     `fact_capture` por trecho, com o total, as malformadas e se a devolução veio sem marca;
  5. com algum `rodado`, `lido` ou `doc`, grava em `.measurements/fact-audit/<agent_id>-<offset>.json` os fatos, o
     `cwd` do subagente e, para os `rodado`, o comando e a saída de cada `Bash` do trecho (até 4 mil caracteres cada), e
     solta `fact_audit.py run <arquivo>` com `start_new_session=True` e a saída no `/dev/null`. Sai.
- **`run`**, em segundo plano:
  1. roda, no `cwd` do subagente, com `BRZA_FACT_AUDIT=1` e limite de 10 min:
     `claude -p --model haiku --tools Read,Grep,Glob,WebFetch --add-dir <dir do arquivo> --output-format json --max-budget-usd 0.25 "<prompt>"`;
  2. o prompt manda refazer a evidência de cada fato — abrir o `arquivo:linha`, a URL, ou ler a saída gravada do
     comando — e devolver uma linha JSON por fato: `{"id": "F3", "verdict": "holds|fails|unknown", "why": "…"}`;
  3. grava um `fact_check` por veredito e um `fact_audit` por rodada, com o custo e a duração do JSON de saída, o número
     de fatos e o erro, quando houver. A falha nunca levanta: vira `fact_audit` com `error`.

### D3 — O desfecho da sessão — `scripts/fact_outcome.py` (P5)

- **Origem:** R1.3, R2.2, R3.3

#### Como fica

```bash
python3 scripts/fact_outcome.py <agent_id>:F3 fails "a sonda do R8.1 não rodou o hook" --ref PLN-004/R8.1
python3 scripts/fact_outcome.py --pending [--workstream <nome>] [--since AAAA-MM-DD]
python3 scripts/fact_outcome.py --list <agent_id>
```

- **Registrar:** aceita o prefixo único do `agent_id`; recusa, com saída 2, o fato que não está no log; grava
  `fact_outcome` com o `verdict` (`holds` ou `fails`), o porquê, a `ref` e o `workstream` do cwd.
- **`--pending`:** os `fact` `inferido`, abaixo de 80 ou `C`, sem `fact_outcome`, do workstream do cwd por padrão, com
  o id, a data, a confiança e o texto.
- **`--list`:** todos os fatos da devolução, com o veredito do Haiku e o da sessão.

### D4 — O acerto por faixa — `scripts/summarize_measurements.py --facts` (P6)

- **Origem:** Pedido 1, R1.2

#### Como fica

Uma tabela por papel, faixa (90+, 80–89, <80) e tipo: fatos, com desfecho, `holds` em %, a confiança média e a
distância entre as duas. O desfecho da sessão vence o do Haiku; `unknown` conta à parte e fica fora do acerto. Abaixo,
as devoluções sem marca, as marcas malformadas e o custo somado das auditorias. Com `--json`, o mesmo em JSON.

### D5 — O lembrete — `.claude/skills/close-task/SKILL.md` (P7)

- **Origem:** R3.3

#### Como fica

No `## 3. O pendente`, um item a mais:

```markdown
- **Os fatos a conferir:** `python3 scripts/fact_outcome.py --pending` lista os fatos `inferido`, abaixo de 80 e os
  custos do workstream sem desfecho. O que a sonda, a rodada ou a execução da tarefa respondeu vai ao
  `fact_outcome.py` com a `--ref`; o resto fica.
```

### D6 — A norma e a sessão da auditoria — `CLAUDE.md`, `.claude/hooks/measure.py` (P4, P7)

- **Origem:** R2.1
- **Contexto:** a sessão `-p` da auditoria roda no workspace e o `Stop` dela vira uma linha `turn`, que somaria o custo
  da auditoria duas vezes.

#### Como fica

- O `measure.py` marca `"fact_audit": true` no `turn` com `BRZA_FACT_AUDIT` no ambiente, e o resumo deixa essa linha
  fora do custo da sessão principal.
- A tabela do hook de medição, no `CLAUDE.md`, ganha as linhas `fact`, `fact_capture`, `fact_check`, `fact_audit` e
  `fact_outcome`, e a seção diz que o `fact_audit.py` é o único hook que solta processo.

## Passos

### P1 — A sonda do `claude -p`

Executa D2 · executor: a sessão que conduz

Estimado: 0.5 h · Executado: 0.2 h

- [x] **1.** No scratch, rodar a linha do D2 com um fato `lido` de fixture e conferir: o modelo é o Haiku 5.5, o JSON
  traz o custo e o resultado, só as ferramentas dadas existem, o `--max-budget-usd` corta, e o `Stop` do projeto roda
  e enxerga `BRZA_FACT_AUDIT`.
- [x] **2.** O que divergir do D2 volta à Entrevista antes do P3. Nada desmente o D2: o MCP do `context7` entra junto,
  só de leitura, e a saída 1 do teto é a falha que o D2 já manda gravar como `fact_audit` com `error`.

**Evidência:** fixture com três fatos em `/private/tmp/pln005-p1/facts.json` (`F1 lido` verdadeiro, `F2 lido` falso,
`F3 rodado` com a saída gravada). `BRZA_FACT_AUDIT=1 claude -p --model haiku --tools Read,Grep,Glob,WebFetch --add-dir
… --settings <espião do Stop> --output-format stream-json --verbose --max-budget-usd 0.25` → `success`, US$ 0,0056,
`F1 holds`, `F2 fails` ("o timeout é 30, não 60"), `F3 holds` sem rodar o comando; espião: `audit=1`. O mesmo com
`--max-budget-usd 0.001` → saída 1, `error_max_budget_usd`. O `F1` voltou `holds` com a nota "na linha 23 e não na
22": a citação `measure.py:22` deste plano estava errada, e o Terreno foi corrigido.

### P2 — A marca nos papéis

Executa D1 · executor: a sessão que conduz, pela `agent-instructions-writer`, na `master`

Estimado: 0.5 h · Executado: 0.2 h

- [x] **1.** A régua fica nos dois papéis, e não sobe ao `AGENTS.md`: só pesa quando eles rodam, e o `AGENTS.md` paga
  em toda sessão. Nenhuma outra linha da norma cita a marca (`git grep` por `inferência`, `a conferir` e `[F`).
- [x] **2.** A marca vai "logo depois do que afirma", e não "no fim da linha" do D1, porque o custo e o "se paga" de uma
  opção dividem a linha `Custo: … Se paga: …`; no `collector`, a regra substitui "Fato sem fonte é inferência".

**Evidência:** `master@68a925c` — `.claude/agents/designer.md:19-30` e `.claude/agents/collector.md:15-24`; a expressão
do D2 casa o exemplo `[F3 · lido · 90]` dos dois arquivos, e a maior linha tem 118 colunas; `brza note sync` →
`studio`, `tools-kit` e `workspace` mesclados e enviados.

### P3 — A captura

Executa D2 (`stop`, sem soltar o processo) · executor: `implementer`, com os testes em
`.claude/hooks/tests/test_fact_audit.py`

Estimado: 2 h · Executado: — h

- [ ] **1. Teste que falha:** um transcript de fixture com marcas na devolução e num `Write` gera os `fact` e o
  `fact_capture`; um papel fora da lista e o ambiente com `BRZA_FACT_AUDIT` não geram nada; a marca malformada conta.
- [ ] **2. Implementar.**
- [ ] **3. Rodar** — `python3 -m unittest discover .claude/hooks/tests`.

### P4 — A auditoria em segundo plano

Executa D2 (o arquivo, o disparo e o `run`) e D6 (o `turn` marcado) · executor: `implementer`

Estimado: 2 h · Executado: — h

- [ ] **1. Teste que falha:** com o `claude` trocado por um espião no `PATH`, o `stop` volta antes do espião terminar,
  e o `run` grava um `fact_check` por linha do espião e o `fact_audit` com o custo; com o espião falhando, só o
  `fact_audit` com `error`.
- [ ] **2. Implementar**, com a entrada no `.claude/settings.json`.
- [ ] **3. Rodar** — `python3 -m unittest discover .claude/hooks/tests`.

### P5 — O desfecho da sessão

Executa D3 · executor: `implementer`, com os testes em `.claude/hooks/tests/test_fact_outcome.py`

Estimado: 1 h · Executado: — h

### P6 — O acerto por faixa

Executa D4 · executor: `implementer`, nos testes de `test_summarize_measurements.py`

Estimado: 1 h · Executado: — h

### P7 — O lembrete e a norma

Executa D5 e D6 (o `CLAUDE.md`) · executor: a sessão que conduz, pela `agent-instructions-writer`, na `master`

Estimado: 0.5 h · Executado: — h

### P8 — A prova numa devolução real

Executa D1–D4 · executor: a sessão que conduz

Estimado: 0.5 h · Executado: — h

- [ ] **1.** Uma devolução do `designer` com marcas gera os `fact`, e em até 10 min os `fact_check` e o `fact_audit`;
  o `--facts` mostra a linha dela.

### P9 — A revisão

Executa D1–D6 · executor: `reviewer`, com o parecer em `work/reviews/pln-005-a-confianca-dos-fatos.md`

Estimado: 1 h · Executado: — h

## Regressão

- **O `measure.py` segue só medindo** e o `SubagentStop` dele não muda de duração. Como se confere: os testes de
  `.claude/hooks/tests/test_measure.py` e um `subagent` real com `duration_s` igual ao de antes.
- **O resumo sem `--facts` não muda.** Como se confere: `test_summarize_measurements.py`.

## Worklogs

- 2026-10-31 — aberto; R1–R3 respondidas; D1–D6 e P1–P9 escritos. Aceito na R4; P1 feito, a sonda confirmou o D2; P2 feito. Parou antes do P3.
  [PLN-005: a abertura da confiança dos fatos do desenho](../../work/worklogs/2026-10-31-pln-005-a-abertura-da-confianca-dos-fatos.md)
