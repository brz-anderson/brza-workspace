---
status: done
scope:
  - workspace
opened: 2026-11-03
completed: 2026-11-03
tags:
  - tooling
---

# REV: o Desenho do PLN-009 antes da execução

O parecer do Desenho do
[PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md),
na versão `brza-workspace@ecd380e` com a R1 em disco, antes de qualquer passo. O revisor foi um subagente `reviewer`, da
camada alta, que não escreveu o plano. Os destinos saíram da R2 do plano, respondida pela regra de Anderson de
2026-11-03 ("escolha o encaminhamento dos achados sempre pela opção `recomendada`"; "prefira sempre optar por
`corrigir aqui`"): 13 achados corrigidos na reescrita do Desenho e dos Passos, e o A14 na issue
[Os passos do MCP no PLN-003 passam ao PLN-009](../issues/os-passos-do-mcp-no-pln-003-passam-ao-pln-009.md).

Alvo: `plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md`, no estado do disco depois do `ecd380e` (2026-11-03) — já com a
Entrevista R1 (R1.1 "brza-workflow", R1.2 "PLN-009") e a `## Pendências conhecidas`, que a sessão principal gravou
durante a revisão. Os números de linha são desse estado (229 linhas). Régua: as rodadas e o Desenho do PLN-003, o
worklog do P0 (não commitado), o molde `.claude/skills/plan-runner/references/plan-template.md` e o `plans/README.md`.

Ordem: do mais grave ao menos. Os achados A2, A3, A6, A9 e A12 dependiam de escolha e foram à R2 do plano; o destino
de cada um diz a resposta.

## Achados

### A1 — O PLN-009 não absorveu nenhum achado medido do P0, e agora diverge do Desenho do PLN-003, que os absorveu no `ecd380e`
> lacuna · importante · confiança 95 · → corrigido aqui

**Evidência:**
- Durante a revisão, o commit `ecd380e` (03:14, "registrar medição das hipóteses do P0 … e ajustes em D3-D7") levou os
  achados ao Desenho do PLN-003: `PLN-003-design.md:474-480` (D4: `ThreadingHTTPServer`, `HTTP/1.1`, `Content-Length`,
  `GET /mcp` SSE concorrente, `~/.local/bin` no `PATH` do plist), `:517-520` (D5: `ORCA_AGENT_SESSION_ID` e
  `ORCA_USER_DATA_PATH` no env do `orca orchestration`), `:557-566` (D6: `claude -p` completo, `CLAUDE_CONFIG_DIR`
  omitido na `systemDefault`, `switchAccount` por RPC só `at-rest`).
- No PLN-009, `grep -n -E 'ThreadingHTTPServer|HTTP/1.1|Content-Length|systemDefault|ORCA_USER_DATA_PATH|at-rest|turnActive|"type"'
  PLN-009-plan.md` → nada. O que falta, achado a achado do P0 (`2026-11-03-pln-003-medicao-das-hipoteses-p0.md`):
  - **H5** (`worklog:80-81`): o D1 (`PLN-009:87-96`) diz só "Python 3 stdlib"; o P1.2 (`:150`) diz "rotas SSE e
    POST", sem o Streamable HTTP (`POST /mcp` + `GET /mcp`) nem o `HTTP/1.1` com `Content-Length`.
  - **H1** (`worklog:31-32`): sem `"type": "http"` o cliente vira stdio e o servidor recebe 0 requisições. É do
    `.mcp.json` (PLN-003/D3), mas o critério do `Pedido 2` (`PLN-009:46`) só se prova com ele.
  - **H2** (`worklog:36-47`): o plist do D1/P1.3 (`:95`, `:151`) não põe `~/.local/bin` no `PATH`; o fallback Haiku do
    D4 (`:129`) não diz com que conta roda nem a regra da `systemDefault`.
  - **H3** (`worklog:57-58`): o gate de "troca de conta" (`:38`, `:116`) existe sem mecanismo de troca.
  - **H4** (`worklog:62-71`): o PLN-009 não tem `orca orchestration` nenhum (ver A2).
- É o custo da cópia: os dois Desenhos descrevem o mesmo `packages/mcp/` e já divergem uma hora depois da extração. Com
  a R1.2 (o PLN-009 é o dono), o Desenho do PLN-009 tem de passar a ser a fonte, e o D4 a D6 do PLN-003 a apontar para
  ele em vez de repetir.

### A2 — Passar os P6 a P9 do PLN-003 ao PLN-009 (R1.2) deixa sem dono o M6, o M7, o M13, o M14 e a R6.4
> lacuna · importante · confiança 90 · → corrigido aqui (R2.1, D6 e P5)

**Evidência:**
- O que os passos que saem cobrem: P7 "Executa D5 (M8, M13, M14)" e "integração com `orca orchestration` e ciclo
  `worker_done`" (`PLN-003-plan.md:188,193`); P9 "Executa D6 (M6, M7, M11)" (`:214`); P8 o M16 (`:201`).
- O que o PLN-009 cobre: `grep -n -E 'M6|M7|M13|M14|R6\.4|orchestration|switchAccount|CLAUDE_CONFIG_DIR|sugere'
  PLN-009-plan.md` → nenhuma linha; só o `worker_done` solto no P2.3 (`:166`) e o `brza quota` do P4.1 (`:191`).
  - **M6** conta por chamada (`claude -p` com `CLAUDE_CONFIG_DIR`, `switchAccount` no chat) — `PLN-003-design.md:237`.
  - **M7** o verbo `brza quota` — `:238`.
  - **M13** o ciclo pelo `orca orchestration` (task, dispatch, worker-start, ask/reply) — `:244`; o PLN-009 não diz
    como um worker é aberto: o `dispatch` "executa de forma autônoma" (`:116`) sem dizer por qual runtime.
  - **M14** o fim volta ao chamador — `:245`.
  - **R6.4** "também sugere à principal", decidida (`PLN-003-interview.md:303-309`) — o D4 do PLN-009 cita a R6.3 e
    não a R6.4 (`:122`).
- A issue `work/issues/os-passos-do-mcp-no-pln-003-passam-ao-pln-009.md:31-36` pede o `[-]` dos quatro passos e não
  diz para onde vão esses cinco itens. Marcados os `[-]`, eles somem dos dois planos.

### A3 — O D2 lê a cota pelo `orca account list --json`, e o P4 testa a "integração com `brza quota`", verbo que não existe e que nenhum passo cria
> desvio · importante · confiança 95 · → corrigido aqui (R2.1, D6)

**Evidência:**
- `PLN-009:109` ("consumo obtido via `orca account list --json`") × `PLN-009:191` ("integração com `brza quota`").
- `brza quota --help` → "Unknown command: quota"; `ls ~/.local/bin | grep brza` e `ls ~/Projects/brza-workflow/bin
  packages/client/bin` → nenhum `brza-quota`.
- O M7 (`PLN-003-design.md:238`) é exatamente essa bifurcação: "cli `brza quota` + mcp consome", com a alternativa "ler
  o JSON no mcp sem verbo". O D2 escolheu a alternativa, o P4 a principal, e nenhum dos dois é rodada.

### A4 — A fila ordena por `deadline`, `blocks` e `priority`, mas o `dispatch` não recebe esses campos e o D2 não diz de onde eles vêm
> lacuna · importante · confiança 90 · → corrigido aqui

**Evidência:**
- A assinatura `dispatch(task, role, target, model?, effort?, account?)` (`PLN-009:116`) não tem nenhum dos três; o D2
  (`:98-106`) dá a ordem e não a fonte.
- O PLN-003 dizia a fonte: "lidos do índice da `master` (M24)" (`PLN-003-design.md:239`, M8; `:255`, M24; D2 em
  `:401-415`), entregue pelo PLN-003/P1, ainda aberto (`PLN-003-plan.md:104-115`).
- `git show master:.brza/index.jsonl | grep -c '"priority"'` → 0 de 60 linhas. O índice também é um log de eventos
  (`"event":"created"|"changed"`), não um retrato: o leitor precisa reduzir pela última linha de cada `id`.
- O PLN-009 não tem `## Pré-requisitos` com o PLN-003/P1, e o `ready` (`:7`) não cita a dependência.

### A5 — O `brza install` não liga `packages/mcp/bin/`, ao contrário do que o D1 afirma, e nenhum passo o muda
> lacuna · importante · confiança 92 · → corrigido aqui

**Evidência:**
- D1: "o executável `bin/brza-mcp` do pacote é ligado em `~/.local/bin` pelo `brza install`" (`PLN-009:90-91`).
- `~/Projects/brza-workflow/bin/brza-install:61-62` (`client_dir()` = `packages/client/bin`), `:71-74` (só `core_dir()`
  e `client_dir()`), `:184` (`--client` "liga todo brza-* de packages/client/bin/"). Não há pasta `packages/mcp`.
- Falta um passo (com teste em `tests/cli/test_brza_install.py`) que ensine o `brza install` a ligar o pacote novo, ou
  o D1 põe o `brza-mcp` em `packages/client/bin/`.

### A6 — Limiares e porta sem rodada: `4242` sem o fallback que o PLN-003 previa, RAM > 4 GB, CPU > 90%, confiança 0,75 e `--max-budget-usd 0.01`
> desvio · importante · confiança 90 · → corrigido aqui (R2.2, R2.3, D1, D2 e D4)

**Evidência:**
- **Porta:** a R3.4 diz "mais porta, token e o serviço do `launchd`", sem número (`PLN-003-interview.md:146-149`); o B6
  idem (`PLN-003-design.md:220`). O PLN-003/D4 dizia "porta padrão com fallback automático" (`:476`); o PLN-009 diz
  "exclusivamente em `127.0.0.1:4242`" (`:92`) e largou o fallback sem registro. Fallback automático também não casa
  com a URL fixa do `.mcp.json` (`PLN-003-design.md:453`): quem escolhe tem de publicar a porta.
- **Máquina:** a R9.4 diz "memória livre e swap, com a CPU como segundo sinal" (`PLN-003-interview.md:418-420`), sem
  número; "> 4 GB", "swap estável" e "> 90%" (`PLN-009:110`) não estão em rodada nenhuma.
- **Confiança 0,75** (`PLN-009:129`): a rodada do M11 manda "o limiar se calibra com empate real na fase 2b"
  (`PLN-003-design.md:290`), e a medição tem erro com confiança 0,66 e acerto com 0,02 (`:288-289`).
- **`--max-budget-usd 0.01`**: a rodada fala só em `--max-budget-usd` (`PLN-003-design.md:287`); o 0,01 é o da sonda
  do P0 (`worklog:38`).

### A7 — O gate do `dispatch` dispara em `role == 'implementer'`, que é o subagente por papel do `AGENTS.md`, e não o executor da R5.2; papel desconhecido não tem regra
> desvio · importante · confiança 90 · → corrigido aqui

**Evidência:**
- `PLN-009:116`: "Se `role == 'consultant'`, executa … Se `role == 'implementer'` … devolve proposta".
- R5.2 decidiu "o consultor livre, o executor com gate" (`PLN-003-interview.md:245-251`); o PLN-003/D4 usa `executor`
  (`PLN-003-design.md:488`) e o D9 fala de "consultores, executores e arquitetos" (`:642`). O próprio PLN-003 já se
  contradiz no `brza.toml` do D6 (`[policy.roles.implementer]`, `[policy.roles.architect]`, `:540-544`).
- `AGENTS.md` ("Cada workstream aprende…", tabela de papéis): `implementer` é subagente da camada média que roda sem
  commit — outra coisa que a sessão-executor do F12 (`PLN-003-design.md:122`).
- Cenário: um pedido com `role: "executor"` ou `role: "architect"` não casa nenhum dos dois ramos; o D3 não diz se
  roda ou se cai no gate. O seguro é "tudo que não é `consultant` passa pelo gate".

### A8 — A Cobertura tem critérios que o teste nomeado não prova, e itens do Pedido sem critério
> lacuna · importante · confiança 90 · → corrigido aqui

**Evidência:**
- **`Pedido 6`** "o `tev1` desempata o texto em <0,1 s" (`PLN-009:50`): os ~0,09 s são a mediana *carregado*; frio são
  2,4 s (`PLN-003-design.md:273`). `curl -s localhost:11434/api/ps` → `{"models":[]}` agora: o primeiro desempate da
  sessão falha o critério. O teste é "integração" e depende de Ollama, do `tev1:4b` e de `claude -p` pago, sem dizer o
  dublê.
- **`Pedido 7`** promete "registro de telemetria `route`" (`:38`); o critério (`:51`) só fala do gate, e o P5.1
  (`:204`) não tem teste que falha. O D5 fica sem linha de Cobertura.
- **`Pedido 5`** promete o verbo `brza mcp config` (`:36`); nenhum critério nem passo o cria (o P3 cria a ferramenta
  `config`, `:117`).
- **`Pedido 1`** "gerenciam o daemon sob `launchd`" (`:44`) em `test_mcp_lifecycle.py` "unidade/integração": o teste
  real carrega um LaunchAgent em `~/Library/LaunchAgents` (estado fora do workspace); falta dizer o isolamento ou um
  caso manual `C1`.
- **Regressão 2** (`:214`, fallback sem Ollama) é comportamento novo sem critério nem teste.

### A9 — O teto por conta e runtime perdeu o "teto de sessões" da R7.1 e não diz o que fazer com conta sem dado de uso
> lacuna · importante · confiança 85 · → corrigido aqui (R2.5, D2)

**Evidência:**
- A opção decidida na R7.1 traz "e um teto de sessões por conta e runtime" (`PLN-003-interview.md:321-329`); a R9.3
  "Não substitui a R7.1" (`:416-417`). O D2 (`PLN-009:109`) só tem a projeção a 90%.
- `orca account list --json`, rodado agora: o uso vem num bloco por provedor (`rateLimits.claude.session|weekly|fableWeekly`
  com `usedPercent` e `resetsAt`) e as outras contas em `rateLimits.inactiveClaudeAccounts`, que veio `[]` com duas
  contas gerenciadas e `activeAccountId: null`. O app busca o uso das inativas sob demanda
  (`brza-studio/src/main/rate-limits/service/service-inactive-accounts.ts:10-20`,
  `src/main/provider-account-services.ts:143-159`). Premissa: a lista vazia é o estado comum enquanto o app não busca.
- O D2 não diz se conta sem dado admite worker (fail-open) ou não (fail-closed), nem de qual client (Studio ou Orca,
  cada um com as suas contas) o daemon lê, sem o env de app (R3.4, `PLN-003-interview.md:151-152`).

### A10 — Os passos não têm o "teste que falha" concreto nem o comando do gate, e o P4 calibra contra casos que ficaram fora do git
> desvio · sugestão · confiança 88 · → corrigido aqui

**Evidência:**
- P4 não tem "Rodar e ver passar" (`PLN-009:185-195`); P5 não tem teste que falha (`:198-208`).
- Os `test_mcp_*.py` da Cobertura não dizem a pasta. No `brza-workflow` o gate é `python3 -m unittest discover -s
  tests/cli` e `-s tests/hooks` (`~/Projects/brza-workflow/README.md:109-117`); um `tests/mcp/` novo não roda nele.
- P4.3 "validação contra os casos de teste do M11" (`:193`): "Os scripts (`tiebreak.py`, `haiku.py`, `decide.py`,
  `decide_rand.py`) e as saídas ficaram no scratch da sessão, fora do git" (`git show
  workstream/workspace:work/worklogs/2026-11-03-o-desempatador-local-do-m11.md`, linhas 47-48).
- "Commit: na branch de trabalho" (`:154`, `:168`, `:181`, `:194`) sem repositório: o código vai ao `brza-workflow`
  (R1.1), cuja `master` está agora com `bin/brza-note` e dois testes sujos de outra sessão (`git -C
  ~/Projects/brza-workflow status --short`); o executor "sessão do `tools-kit`" roda no worktree do workspace.

### A11 — O interpretador do `launchd` não está fixado: com o `PATH` do P0, o `python3` é o 3.9.6 do sistema, sem `tomllib`
> lacuna · sugestão · confiança 85 · → corrigido aqui

**Evidência:**
- `/usr/bin/python3 --version` → 3.9.6; `/usr/bin/python3 -c 'import tomllib'` → `ModuleNotFoundError`.
- O `PATH` do `launchd` na sonda do P0 começa em `/usr/bin` (`worklog:37`); os `bin/brza-*` do `brza-workflow` usam
  `#!/usr/bin/env python3` (`head -1 bin/brza-note`). A R6.3 escolheu `brza.toml` "lido por `tomllib`"
  (`PLN-003-interview.md:296`), que só existe do 3.11; o `brza-workflow` declara "Python 3.10 ou mais" (`README.md:26`)
  e já tem o `brza_root.parse_toml` para o 3.9 (`bin/brza-sync:167`).
- Premissa: o plist chama o `bin/brza-mcp` pelo shebang. O D1/P1.3 (`PLN-009:95`, `:151`) deve fixar o interpretador
  ou usar o `parse_toml`.

### A12 — O token mora num arquivo, e nada diz como o chat o põe no `Authorization`
> lacuna · sugestão · confiança 85 · → corrigido aqui (R2.6, D1)

**Evidência:**
- D1: token em `~/.brza/runtime/mcp.token`, `0600` (`PLN-009:93`).
- A sonda do H1 passou com `"Authorization": "Bearer ${BRZA_MCP_TOKEN}"` no `.mcp.json` (`worklog:22-23`), isto é, por
  variável de ambiente do processo `claude`. Ninguém exporta `BRZA_MCP_TOKEN` hoje (`env | grep ^BRZA_` → só
  `BRZA_WORKSPACE`). O caminho tem de ser escolhido: o `claude-brza` e a função `claude` exportam a variável lida do
  arquivo, ou outro mecanismo. O worker do painel (R10.3) só tem `PATH/HOME/LANG/TZ/TMP` (`PLN-003-design.md:52`) e lê
  o arquivo.

### A13 — A forma foge do molde: Pedido parafraseado, sem "O que este desenho assume", sem `### Fora de escopo`, `## Pré-requisitos` e `## Fechamento`, D sem o artefato
> desvio · sugestão · confiança 88 · → corrigido aqui

**Evidência:**
- O molde: o Pedido vai "Nas palavras de quem pediu, entre aspas, sem paráfrase" (`plan-template.md:81`). Os itens 1–7
  (`PLN-009:32-38`) são desenho — SQLite, Bearer, `tev1:4b`, `/v1/systemone` — e a Cobertura vira circular: prova o
  desenho, não o pedido. As palavras de Anderson existem: a R4.1 (`PLN-003-interview.md:176-178`), o item 4 do Pedido do
  PLN-003 ("iniciar/parar tbm", `PLN-003-plan.md:56-58`) e a R9 (`:62-64`).
- "Seção marcada 'gatilho' só existe quando o gatilho vale; as outras existem sempre" (`plan-template.md:6-7`):
  `### Fora de escopo` (`:93`) e `## Fechamento` (`:277`) não têm gatilho e faltam; `## Pré-requisitos` (`:117`) tem
  gatilho que vale (PLN-003/P1 para o índice, A4; o `.mcp.json` do PLN-003/P4 para haver cliente) e falta.
- `### O que este desenho assume` (`plan-template.md:154`) falta; as decisões aparecem só como "Origem".
- "Cada item mostra o artefato como fica — o contrato em código" (`plan-template.md:149-150`): o D4 não traz o
  `brza.toml` (o PLN-003/D6 traz, `PLN-003-design.md:531-552`), o D3 não traz o schema do `dispatch`.
- A `## Regressão` (`PLN-009:211-215`) não diz "como se confere" em nenhuma linha (`plan-template.md:220`).

### A14 — O PLN-003 ainda não aponta para o PLN-009 nem marca a R5.3 como reaberta
> desvio · sugestão · confiança 95 · → issue (já aberta: `work/issues/os-passos-do-mcp-no-pln-003-passam-ao-pln-009.md`)

**Evidência:**
- `grep -rn PLN-009 plans/PLN-003-o-workflow-nos-dois-clients/` → nada. Os P6–P9 (`PLN-003-plan.md:171-222`) seguem `[ ]`
  com as horas no `remaining_h: 54.5`.
- `grep -n reaberta PLN-003-interview.md` → só a R4.2 e a R6.2; a R5.3 (`:253-260`) segue "Decidido — o repositório
  próprio `brz-anderson/brza`", e o D1 do PLN-003 ainda põe "CLI, do MCP, dos plugins" lá (`PLN-003-design.md:385`).
- `check_notes.py --detail` → `aviso backlink-missing: PLN-003-plan.md — work/issues/os-passos-do-mcp-no-pln-003-passam-ao-pln-009.md`.
- A issue (itens 1–5) cobre isto; o achado fica para conferir que a sessão do PLN-003 o aplique, e para somar o A2 a ela.

## Hipóteses conferidas que caíram

### F1 — "O soft cap de 55% não tem lastro"
> → falso
**Por que é falso:** a opção decidida na R7.1 diz "55% e 90%, como no `quota.py` do workspace de origem".
**Evidência:** `PLN-003-interview.md:321-322` e "Decidido — por conta e por runtime" em `:329`. Fica a lacuna de o D2
não dizer o que o 55% faz (só o 90% tem regra em `PLN-009:109`).

### F2 — "O corte a 90% da projeção não tem lastro"
> → falso
**Por que é falso:** a R9.4 o decidiu.
**Evidência:** `PLN-003-interview.md:418-420`.

### F3 — "O `/v1/systemone` e o `tev1:4b` não existem no Ollama desta máquina"
> → falso
**Por que é falso:** o endpoint responde e o modelo está instalado.
**Evidência:** `curl -s localhost:11434/api/tags` → `['tev1:4b']`; `curl -X POST localhost:11434/v1/systemone -d '{}'` →
HTTP 400 `{"error":"model is required"}`; Ollama `0.40.13`.

### F4 — "O `orca account list --json` não dá `usedPercent` e `resetsAt`"
> → falso
**Por que é falso:** dá, por provedor e janela.
**Evidência:** `orca account list --json` → `result.rateLimits.claude.session.usedPercent`, `.resetsAt`,
`.weekly…`, `.fableWeekly…`. O que falta é o recorte por conta (A9).

### F5 — "O PLN-009 não diz em que repositório o código mora"
> → falso (no estado atual)
**Por que é falso:** a R1.1, gravada durante esta revisão, e o D1 dizem `~/Projects/brza-workflow/packages/mcp/`.
**Evidência:** `PLN-009-plan.md:57-73` e `:90-91`; `gh repo view brz-anderson/brza` → "Could not resolve to a
Repository"; `gh repo view brz-anderson/brza-workflow` → `PUBLIC`.

### F6 — "O `brza mcp` não vai chegar ao `brza-mcp` pelo despacho"
> → falso (nesta máquina)
**Por que é falso:** o `brza` do PATH é o shim do BrzA Studio e despacha `brza <sub>` para o `brza-<sub>`.
**Evidência:** `command -v brza` → `/Applications/BrzA Studio.app/Contents/Resources/bin/brza`; `brza where --help` →
o uso do `brza-where`, `exit=0`; `brza mcp --help` → "Unknown command: mcp" só porque o `brza-mcp` não existe. Numa
máquina só com o Orca, depende do `brza` do PLN-003/P2 — entra no `## Pré-requisitos` do A13.

### F7 — "`origin: plan` com `origin_ref: PLN-003` fere o molde"
> → falso
**Por que é falso:** o `plans/README.md:18` aceita `PLN-NNN` como `origin_ref` de `plan`.
**Evidência:** `check_notes.py` → 0 erros, 1 aviso (o backlink do A14).

### F8 — "O PLN-009 e o PLN-003 duplicam o trabalho sem destino"
> → falso (em parte)
**Por que é falso:** a R1.2 deu o dono ao PLN-009 e a issue leva o pedido à sessão do PLN-003.
**Evidência:** `PLN-009-plan.md:75-83`, `:226-229`; `work/issues/os-passos-do-mcp-no-pln-003-passam-ao-pln-009.md`.
O que sobra é o A2 (o que cai entre os dois) e o A14 (ainda não aplicado).

### F9 — "O P0 está `[x]` no PLN-003 com evidência falsa: o Desenho não tem os ajustes de D3 a D7"
> → falso (no estado atual)
**Por que é falso:** valia às 03:0x, quando o `git diff` do Desenho só mudava o cabeçalho; o commit `ecd380e`, às
03:14, gravou os ajustes.
**Evidência:** `git show ecd380e -- plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-design.md` → H1 a H6 reescritas
como "CONFIRMADA" e os ajustes em `:474-480`, `:517-520`, `:557-566`.

## Pontos para rodada

1. **Para onde vão o M6, o M7, o M13, o M14 e a R6.4 (A2, A3)?**
   1. Entram no PLN-009, com um D6 "o ciclo e a conta" (o `orca orchestration` com o env do H4, o `claude -p` por conta
      com a regra do H2, o `switchAccount` por RPC em repouso do H3, o fim ao chamador) e o `brza quota` como verbo
      (Recomendado). Custo: ~6–9 h a mais no PLN-009 (as horas do M6, M7, M13 e M14 na matriz:
      2–4 + 1,5 + 3–4 + 2–3, `PLN-003-design.md:237-245`), e o PLN-009 passa de 22,5 h para ~30 h. Se paga: no 1º
      executor, porque sem o M13 o `dispatch` não abre worker nenhum.
   2. Ficam no PLN-003, com os P7 e P9 divididos: só a parte de fila e desempate vai ao PLN-009. Custo: ~20 min de
      reescrita nos dois planos e a dependência cruzada entre eles. Se paga: se o PLN-003 tiver sessão própria para
      a fase 2.
   3. Vão a `### Fora de escopo` do PLN-009, com uma issue. Custo: 0 agora; o `dispatch` do PLN-009 entrega fila e
      política sem abrir worker. Se paga: nunca para a R4.1, que pede o MCP como "o coração do fluxo".

2. **Os limiares sem rodada (A6).** Marque mais de uma.
   1. A porta é configurável no `brza.toml`, `4242` o padrão, sem fallback automático; o `brza install` grava a porta
      no `.mcp.json` (Recomendado). Custo: ~0,5 h. Se paga: no 1º conflito de porta.
   2. Os tetos da máquina e a confiança do `tev1` nascem como chaves do `brza.toml` sem valor imposto: a máquina só
      registra (linha `route` com memória livre, swap e CPU) até a medição dar o número, e o `tev1` manda tudo ao Haiku
      até a calibração da fase 2b (Recomendado). Custo: ~0,5 h; na fase 2 a máquina não segura nada. Se paga: na
      fase 2b, com o empate real que a rodada do M11 pede.
   3. Ficam os números do plano (4 GB, 90% de CPU, 0,75, US$ 0,01) como padrão provisório. Custo: 0 agora; um limiar
      sem medição decide quem roda. Se paga: só se a medição confirmar os números.

3. **O `tev1:4b` ocupa 7,7 GB carregado (`PLN-003-design.md:274`), e o teto da máquina corta abaixo de 4 GB livres.**
   1. O desempate não conta no teto de workers, e o `keep_alive` do Ollama fica curto (ex.: 1 min) para devolver a
      memória (Recomendado). Custo: o 1º desempate depois da pausa volta a 2,4 s. Se paga: agora, num M5 Pro de 24 GB
      com mais de dois workers.
   2. O desempate só roda com memória livre acima de 4 GB + 7,7 GB, senão vai direto ao Haiku. Custo: ~US$ 0,0008 a
      0,004 por desempate quando a máquina está cheia. Se paga: quando a medição mostrar a máquina cheia com frequência.
   3. Sem regra. Custo: 0. Se paga: nunca; o desempatador pode disparar o próprio teto.

4. **Onde vai a linha `route` (D5)?**
   1. No `.measurements/measurements.jsonl` do workspace, que o `summarize_measurements.py` já lê, com
      `event: "route"` (Recomendado). Custo: ~1 h no `measure.py`/resumo e um caminho do workspace dentro do daemon. Se
      paga: na 1ª revisão da política, que o `AGENTS.md` manda fazer "pela medição".
   2. No `~/.brza/orchestrator.log`, como no plano. Custo: 0 agora; um segundo log que o resumo não lê. Se paga: só se
      o MCP servir a mais de um workspace.

## O que rodou e o que deu

- `git diff`, `git status` e `git log` no worktree: o PLN-009 mudou durante a revisão (a R1 e as Pendências), e o
  commit `ecd380e` (03:14) gravou o P0 no PLN-003 — o Desenho, o plano e o worklog.
- `grep` dos achados do P0: ausentes no PLN-009; presentes no Desenho do PLN-003 depois do `ecd380e` (A1, F9).
- `curl localhost:11434/api/tags` → `tev1:4b`; `POST /v1/systemone {}` → 400 "model is required"; `/api/ps` → nenhum
  modelo carregado.
- `command -v ollama orca brza brza-quota brza-mcp` → `ollama`, `orca` e `brza` do BrzA Studio; sem `brza-quota` nem
  `brza-mcp`. `brza quota --help` e `brza mcp --help` → "Unknown command". `brza where --help` → despacha.
- `orca account list --json` → uso por provedor em `rateLimits`, `inactiveClaudeAccounts: []`, `activeAccountId: null`.
- `gh repo view brz-anderson/brza` → não existe; `brz-anderson/brza-workflow` → público.
- `ls ~/Projects/brza-workflow/{bin,packages,tests}` e `grep` no `bin/brza-install` → só `packages/client`.
- `/usr/bin/python3 --version` → 3.9.6, sem `tomllib`.
- `git show master:.brza/index.jsonl | grep -c '"priority"'` → 0 de 60.
- `python3 .claude/skills/notes-checker/scripts/check_notes.py --detail` → 0 erros, 1 aviso (`backlink-missing` no
  PLN-003 pela issue nova).
