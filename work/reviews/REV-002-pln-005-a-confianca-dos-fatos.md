---
status: done
scope:
  - workspace
opened: 2026-10-31
completed: 2026-10-31
tags:
  - tooling
---

# REV-002: PLN-005 — a confiança dos fatos do desenho

O parecer da entrega do
[PLN-005: A confiança dos fatos do desenho se mede contra o que se sustentou](../../plans/PLN-005-a-confianca-dos-fatos-do-desenho/PLN-005-plan.md),
na versão `brza-workspace@13a291a` da `master`. O revisor foi o `reviewer`, chamado pela sessão do workstream
`workspace`, que não executou os passos; a sessão refez a evidência do A1, do A2, do A3, do A4, do A6, do A7 e do A10
antes da rodada, e os destinos saíram da R11 do plano, com Anderson.

- **Alvo:** a entrega do PLN-005 na `master` (`2e8ea67..13a291a`), contra o `## Pedido`, a Cobertura, as rodadas R1–R10,
  o Desenho D1–D6, os passos P1–P8 e P10 e os desvios X1–X3.
- **Revisor:** `reviewer`, em 2026-10-31.
- **O que rodou:** `python3 -m unittest discover -s .claude/hooks/tests` → `Ran 176 tests … OK`;
  `python3 scripts/summarize_measurements.py --facts` → saída 0; `python3 scripts/fact_outcome.py --pending --workstream all`
  → 3 fatos, saída 0; as duas auditorias reais do log (`ab5aa7e0d74df08e7` e `a84d7b5c9b0c163a5`) e as sessões do
  auditor (`b58ede94…` e `c8241650…`); mutações do `fact_audit.py` numa cópia em `/private/tmp/pln005-p9/mut/`.

## Veredito

O mecanismo funciona de ponta a ponta — duas auditorias reais, a pasta da rodada vazia depois delas, 176 testes verdes
—, mas mede menos do que diz: o fato chega ao auditor cortado (A1) e o `holds` sai às vezes sem leitura (A2), os dois
na faixa que o `--facts` mostra. Dez achados reais, todos `corrigido aqui` (o A1, o A2, o A6, o A7, o A8 e o A10 no
P11; o A3, o A4, o A5 e o A9 pela sessão); cinco hipóteses conferidas e falsas.

## Achados

### A1 — O fato chega ao auditor cortado nos 300 primeiros caracteres da linha, sem o fim da afirmação nem a marca

> bug · importante · confiança 95 · → corrigido aqui

**Evidência:** `.claude/hooks/fact_audit.py:136-139` — o `line_of` corta a linha do começo, `[:TEXT_LIMIT]`, e o mesmo
texto vai ao arquivo da rodada (`:215`), que é tudo o que o Haiku lê do fato. A regra dos papéis põe a marca "logo
depois do que afirma" (`.claude/agents/collector.md:15`), e o `collector` real escreve parágrafos longos:
- `marks_of(sources_of(…))` sobre o transcript de `ab5aa7e0d74df08e7` → 28 fatos, **24 com o texto de 300 caracteres
  e sem a própria marca**; no log, 17 de 25 desse agente e 2 de 22 do `a84d7b5c9b0c163a5`.
- O F1 tem 398 caracteres; a afirmação central, "O expandir NÃO é montado por ele", começa no caractere 357. O
  `fact_check` do F1 é `holds` e o `why` cita só o que cabe nos 300 ("As linhas 38-47, 54-64 e 90-112 e o gate de
  shell…").
- O F8 tem 513 caracteres; o copiar (`:154-159`, no 412) e o fechar (`:137-152`, no 486) ficaram fora. O `why` do
  `holds` lista `:116`, `:170-172`, `:113` e `:199-201` — o último termina no caractere 289.
- O auditor não abriu o agregado (`/private/tmp/brza-pedido-preview-md/levantamento.md`) para recuperar a linha: as 14
  chamadas da sessão `b58ede94-1a7d-4f05-8537-186d531f0328` são o arquivo da rodada e o código do `brza-studio`.

O `holds` sai sobre o prefixo, e a cauda falsa de um fato não aparece no acerto. O teste
`test_text_of_a_fact_stops_at_300_characters` (`test_fact_audit.py`) fixa o corte do começo, com a marca perdida.

### A2 — O `holds` do Haiku sai sem o auditor abrir o arquivo citado, e nada no mecanismo o distingue do verificado

> lacuna · importante · confiança 90 · → corrigido aqui (R11.2, P11)

**Evidência:** cruzando cada `fact_check` com as chamadas de ferramenta da sessão do auditor (o nome do arquivo citado
no `text` contra o `input` de cada `Read`, `Grep` e `Glob`):
- `b58ede94…` (auditoria de `ab5aa7e0d74df08e7`, 14 chamadas): `holds` em F2 (`NativeChatContextClearFade.tsx`,
  `BrzaNativeChatDock.tsx`), F11 (`BrzaExpandLayer.test.tsx`), F13 (`MarkdownPreviewBody.tsx`,
  `markdown-preview-plugins.ts`), F18 (`EditorViewToggle.tsx`) e F28 (`mobile-markdown-blocks.tsx`,
  `MobileNativeChatVisual.tsx`) sem nenhuma chamada a esses arquivos. O `why` do F28 reescreve o `text`: "`:3,85-88`"
  vira "`:3 e :87`".
- `c8241650…` (auditoria de `a84d7b5c9b0c163a5`, 24 chamadas): `holds` em F7 (`brza-app`, `brza-dev`, `brza-test`,
  `brza-tree`, `brza-shot`) e F18 (`brza-install`) sem abrir os scripts.

São 7 dos ~35 `holds` das duas rodadas, quase todos na faixa 90+ `lido`, a que o `--facts` mostra com 90,3%. O prompt
pede para refazer "sem confiar no `text`" (`fact_audit.py:72`), mas o `fact_check` não guarda o que foi aberto, e o
resumo conta o `holds` como acerto. A premissa da R1.3 ("amostra sem viés") não se sustenta sem essa conferência.

### A3 — O `CLAUDE.md` diz que o teto da auditoria é US$ 0,25 fixo, e o código o faz por fato desde a R10.2

> desvio · sugestão · confiança 95 · → corrigido aqui

**Evidência:** `CLAUDE.md:125-126` — "teto de US$ 0,25 e 10 min"; `.claude/hooks/fact_audit.py:244-246` —
`max(BUDGET_MIN, BUDGET_PER_FACT * facts)`, decidido na R10.2. O P10 (`13a291a`) mudou o código e os papéis, e não o
`CLAUDE.md` (`git diff 4c92097 13a291a --stat` → só os papéis, o `fact_audit.py` e o teste).

### A4 — A evidência do P7 diz que nenhuma linha nova de prosa passa de 120 colunas, e uma tem 161

> desvio · sugestão · confiança 95 · → corrigido aqui

**Evidência:** `CLAUDE.md:125` tem 161 caracteres (contados com `len()` do Python, na `master` e em `4c92097`). O plano
afirma o contrário no P7 (`PLN-005-plan.md:617-618`), e a regra é a da `agent-instructions-writer`
(`.claude/skills/agent-instructions-writer/SKILL.md:47`). As linhas 116-122 com 135 são da tabela.

### A5 — Três mudanças no Desenho aceito não voltaram a rodada, e o D1 ficou com o texto antigo

> desvio · sugestão · confiança 92 · → corrigido aqui

**Evidência:** a regra é `conduct.md:44` — "Desvio que muda um `D` vira rodada antes de seguir: no `PLN`, o `D` é
reescrito no lugar, com a origem nova".
- **X1** mudou o D2 ("tira as marcas da última mensagem de texto", no plano aceito `d39008c`, linha 249, para o
  `SubagentHandback`); o plano diz que "não voltou à Entrevista" (`PLN-005-plan.md:667`), e a origem do D2 segue
  "R1.3, R2.1, R3.1, R3.2" (`:407`).
- **X2** mudou o D3 ("o `workstream` do cwd", `d39008c`, linha 279, para o do fato) sem rodada; a R8 não o cita.
- **O P2.2** mudou o D1 ("no fim da linha" para "logo depois do que afirma") sem `X`, e o D1 ainda diz "no fim da linha"
  (`PLN-005-plan.md:389`). Essa mudança é a que leva ao A1: a marca no meio do parágrafo deixa a linha longa.

### A6 — O `--pending` rodado do checkout da `master` diz "nenhum fato a conferir", sem aviso, com 3 pendentes no log

> bug · sugestão · confiança 92 · → corrigido aqui

**Evidência:** `cd ~/Projects/brza-workspace && python3 scripts/fact_outcome.py --pending` → "nenhum fato a conferir",
saída 0; no mesmo log, `--workstream all` lista 3. O `measure.workstream_of` devolve `master` no checkout da `master`
(`measure.py`, docstring), e o aviso da R8.1 só sai com o workstream vazio (`scripts/fact_outcome.py:236-240`). O
`README.md` põe o comando no bloco dos comandos da raiz, sem `--workstream`.

### A7 — Num terminal do worktree, o `fact_outcome.py` e o `--facts` leem o `.measurements/` do worktree e dizem que não há nada

> bug · sugestão · confiança 88 · → corrigido aqui (R11.4, P11)

**Evidência:** premissa: o comando roda num terminal, e não pela sessão — o `~/.zshrc:52` define a `BRZA_WORKSPACE` sem
`export`, e o ▶ do chat roda no terminal do worktree. Com ela fora do ambiente, a raiz cai em `scripts/..`
(`scripts/fact_outcome.py:29`), que no worktree é o próprio worktree. `cd .worktrees/workspace && env -u BRZA_WORKSPACE
python3 scripts/fact_outcome.py --pending --workstream all` → "nenhum fato a conferir", saída 0; `env -u BRZA_WORKSPACE
python3 scripts/summarize_measurements.py --facts` → "nenhum fato marcado ainda". O worktree tem um
`.measurements/measurements.jsonl` de 2 linhas, de 06:32, e por isso nem o "nenhum log" aparece. O `read_log` do
`fact_outcome.py:71-72` trata o log ausente como vazio. O padrão de raiz é o do `summarize_measurements.py`, anterior
ao plano.

### A8 — O teste do timeout passa sem o `killpg`, e não barra o defeito que o comentário diz barrar

> lacuna · sugestão · confiança 95 · → corrigido aqui

**Evidência:** numa cópia em `/private/tmp/pln005-p9/mut/`, trocar `os.killpg(process.pid, signal.SIGKILL)`
(`fact_audit.py:265`) por `process.kill()` → `Ran 48 tests … OK`; tirar o `start_new_session=True` do `call_claude`
(`:260`) → `OK`. O `test_timeout_is_an_error_and_exits_zero` usa um espião sem filho: matar só o processo basta. O caso
que o `killpg` cobre — o neto com o pipe aberto, ou o servidor MCP do `context7` que o `claude -p` sobe — não tem teste.

### A9 — A Regressão confere a duração do hook pelo `duration_s`, que é a do subagente, e não a do hook

> lacuna · sugestão · confiança 90 · → corrigido aqui

**Evidência:** `PLN-005-plan.md:658-659` — "um `subagent` real com `duration_s` igual ao de antes". O `duration_s` é a
diferença entre o primeiro e o último timestamp do transcript (`measure.py:394-398`), e não muda com o hook. O que pode
mudar é a espera do `measure.py subagent` pela trava, que o `fact_audit.py stop` agora segura durante o `settle`
(`fact_audit.py:195-198`, `measure.py:192-202`).

### A10 — O teto por fato da R10.2 foi decidido com uma amostra, e a segunda, já no log, usou 82% dele

> lacuna · sugestão · confiança 90 · → corrigido aqui (R11.3, P11)

**Evidência:** a R10 apresentou só a auditoria de `ab5aa7e0d74df08e7` (US$ 0,157 por 24, ~0,0065 por fato;
`PLN-005-plan.md:290-293` e `fact_audit.py:64`). A de `a84d7b5c9b0c163a5` gravou `fact_audit` às 10:10:06, antes do
commit do P10 (10:18:39): US$ 0,205 por 21 fatos, 0,0098 por fato e 25 turnos. Com o teto de hoje, `budget_usd(21)` →
`0.25`: a rodada gastou 82% do teto. O corte devolve o `result` nulo (P1) e perde todos os vereditos da rodada.

### A11 — O processo solto pelo `stop` fica órfão, corre com outro pelo arquivo ou deixa o arquivo da rodada

> bug · importante · confiança 90 · → falso

**Por que é falso:** o `run` apaga o arquivo no `finally`, o nome leva o offset gravado sob a trava, e o `claude -p`
roda na própria sessão de processo, morta pelo grupo no timeout.

**Evidência:** `fact_audit.py:336-340` (o `os.remove` no `finally`), `:213-218` (o offset salvo antes de gravar
`<agent_id>-<offset>.json`), `:258-268` (`start_new_session=True` e `os.killpg`); `ls .measurements/fact-audit/` →
vazio depois das duas auditorias reais. Sobra um caso: o `Popen` do `stop` que falha deixa o arquivo, e vira
`hook_error`, sem silêncio.

### A12 — A trava do `State`, compartilhada com o `measure.py`, segura ou derruba o `SubagentStop`

> bug · importante · confiança 85 · → falso

**Por que é falso:** o `stop` não aninha dois `State`, solta o processo fora da trava, e nas duas devoluções reais a
captura saiu 1 s depois da medição, longe do `timeout: 10`.

**Evidência:** `fact_audit.py:195-222` (um `with` só; o `Popen` depois dele); `measure.py:151-153` (a trava aceita
outro arquivo de estado); no log, `subagent` 10:05:07 → `fact_capture` 10:05:08 e `subagent` 10:07:54 →
`fact_capture` 10:07:55; nenhum `hook_error` de `fact_audit:*`. A premissa é que o `settle` e o git ficam abaixo de
uns 9 s; a espera que a trava acrescenta ao `measure.py` está no A9.

### A13 — O `text` e a saída dos comandos vazam do transcript para fora

> bug · importante · confiança 95 · → falso

**Por que é falso:** tudo fica no `.measurements/`, fora do git, e o conteúdo já está no transcript local e já passou
pela API.

**Evidência:** `.gitignore:1` → `.measurements/`; o arquivo da rodada, com as saídas de até 4 mil caracteres, é apagado
ao fim (`fact_audit.py:336-340`). O defeito real do `text` é o corte, no A1.

### A14 — No worktree do `brza-studio`, a auditoria roda com outro modelo ou sem permissão de leitura

> bug · importante · confiança 90 · → falso

**Por que é falso:** o `run` herda o ambiente da sessão, com o modelo do Haiku 5.5, e o modo de permissão vem da
configuração de usuário, que vale em qualquer cwd.

**Evidência:** `echo $ANTHROPIC_DEFAULT_HAIKU_MODEL` num processo filho da sessão → `claude-haiku-5-5`;
`~/.claude/settings.json:6-7` → `"defaultMode": "auto"`; o `brza-studio/.claude/settings*.json` não tem `hooks`; a
auditoria de `ab5aa7e0d74df08e7` leu o código em `~/Projects/brza-studio/…` e rodou em `claude-haiku-5-5`. Sem o `Stop`
do workspace lá, a sessão `-p` só não grava o `turn`, cujo custo o `fact_audit` já traz.

### A15 — O `--since` do `--facts` corta o desfecho que chega depois da data

> bug · importante · confiança 95 · → falso

**Por que é falso:** com `--facts`, o log é lido inteiro e só o `fact` se filtra pela data; o último `fact_outcome` e o
último `fact_check` valem de qualquer dia.

**Evidência:** `scripts/summarize_measurements.py:509` — `read_log(…, "" if args.facts else args.since)`;
`test_since_filters_by_the_fact_date_and_an_outcome_arriving_later_still_counts` e
`test_since_and_the_header_in_the_command_line`.
