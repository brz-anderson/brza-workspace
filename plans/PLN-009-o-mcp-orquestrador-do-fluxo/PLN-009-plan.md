---
status: in_review
phase: review
origin: plan
origin_ref: PLN-003
description: O servidor MCP residente gerencia o fluxo com fila de prioridade sob três tetos, política declarativa e desempate com tev1 e Haiku
ready: sim
estimate_h: 31.3
executed_h: 4.3
remaining_h: 2.0
scope:
  - workspace
  - brza-studio
opened: 2026-11-03
owner: Anderson
priority: high
tags:
  - tooling
---

# PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients

- **Retomar:** P1 a P8 `[x]`; C1 aprovado no launchd real (R7).
  Código em `brza-workflow@007383a`, branch `feat/pln-009-mcp`: MCP 358 OK (um pulado), CLI limpo 445 OK.
  Faltam C2 a C4, com Anderson; confirmar o pré-requisito do C3 com a sessão do PLN-003; e a confirmação
  de Anderson para o merge na `master` do `brza-workflow`. Depois do merge, `brza install --mcp --relink` do checkout
  principal, porque os links de `~/.local/bin` apontam o worktree da `feat`.

## Pedido

- **Origem:** [PLN-003: O workflow do workspace roda igual no BrzA Studio e no Orca, por plugins e pelo `brza`](../PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md),
  por pedido de Anderson em 2026-11-03: "crie um plano só pro `MCP`". O que o MCP deve fazer vem das palavras dele no
  PLN-003.

"o MCP é o orquestrador/coordenador, é por ele - rodando um agente - que decide qual sessão chamar, com qual conta e por
qual runtime, funcionando como um semaforo enfileirando chamadas, tbm decide o modelo/esforço da sessão (pode ser
desativado), em resumo, é o coração do fluxo" — Anderson, em 2026-10-29, na R4.1 do PLN-003.

"o `BrzA CLI` deve conseguir instalar/atualizar o app `BrzA Studio`, o plugin do `Orca`, o plugin do `Claude`, o MCP -
iniciar/parar tbm -" — Anderson, em 2026-10-29, no Pedido do PLN-003.

"prioriza a fila considerando a prioridade do pedido - issue high, bloqueia avanço de plano, prazo de entrega curto e
etc -, o limite de workers em paralelo é geral do workspace somado, o cálculo também leva em consideração ritmo das
contas e o recurso disponível na máquina pra limitar workers" — Anderson, em 2026-11-03, na R9 do PLN-003.

Os itens do pedido, numerados para a Cobertura:

1. o MCP residente, que a CLI inicia e para;
2. o MCP decide qual sessão chamar, com qual conta e por qual runtime;
3. o semáforo enfileira as chamadas, pela prioridade do pedido — issue high, o que bloqueia plano, o prazo curto;
4. o limite de workers soma o do workspace, o ritmo das contas e o recurso da máquina;
5. o MCP decide o modelo e o esforço da sessão, e isso pode ser desativado;
6. o MCP decide "rodando um agente" — o desempatador da rodada do M11;
7. o consultor roda livre, e o executor e a troca de conta passam pelo gate da sessão principal (PLN-003/R5.2).

### Cobertura

| Origem     | Critério de aceite | Passo | Teste (nível) |
| :--------- | :----------------- | :---- | :------------ |
| `Pedido 1` | `brza mcp start`, `stop` e `status` gravam o plist, chamam o `launchctl` e conferem o `/health`; o servidor sobe e para limpo por `SIGTERM` | P1 | `tests/mcp/test_mcp_lifecycle.py` (unidade, `launchctl` trocado); C1 (manual, launchd real) |
| `Pedido 1` | requisição sem Bearer válido recebe 401; o token nasce `0600` | P1 | `tests/mcp/test_mcp_auth.py` (unidade) |
| `Pedido 1` | o `brza install --mcp` liga o `brza-mcp`, e o chat recebe o `BRZA_MCP_TOKEN` | P1 | `tests/cli/test_brza_install.py`, `tests/cli/test_brza_shell.py` (unidade) |
| `Pedido 2` | o `dispatch` identifica a sessão chamadora pelo `X-Brza-Session` e devolve o pedido enfileirado | P3 | `tests/mcp/test_mcp_dispatch.py` (unidade) |
| `Pedido 2` | o worker admitido abre pelo `orca orchestration` com o env do H4, e o fim volta ao chamador | P5 | `tests/mcp/test_mcp_cycle.py` (unidade, CLI do client trocada) |
| `Pedido 2` | a conta da chamada vai no `CLAUDE_CONFIG_DIR`, omitido na `systemDefault`; o `brza quota` mostra o uso por conta | P5 | `tests/mcp/test_mcp_accounts.py`, `tests/mcp/test_brza_quota.py` (unidade) |
| `Pedido 3` | com dois pedidos, o de `deadline` mais próximo sai antes, e o de `blocks` antes do de `priority: high` | P2 | `tests/mcp/test_mcp_queue.py` (unidade) |
| `Pedido 4` | worker novo espera quando o teto do workspace, o de sessões por conta e runtime ou a projeção a 90% está cheio, e o `status` diz qual | P2 | `tests/mcp/test_mcp_limits.py` (unidade) |
| `Pedido 4` | a máquina só registra memória livre, swap e CPU, sem segurar, enquanto o `brza.toml` não der o número | P2 | `tests/mcp/test_mcp_limits.py` (unidade) |
| `Pedido 5` | a tarefa segue o modelo e o esforço do `brza.toml`, e a chave de desligamento devolve o pedido sem imposição | P4 | `tests/mcp/test_mcp_policy.py` (unidade) |
| `Pedido 5` | cada decisão de rota grava uma linha `event: "route"` no `.measurements/measurements.jsonl` do workspace | P6 | `tests/mcp/test_mcp_telemetry.py` (unidade) |
| `Pedido 6` | a tabela decide a cota; o texto vai ao `tev1:4b` e, sem limiar calibrado ou abaixo dele, ao Haiku; sem Ollama, vai direto ao Haiku sem travar | P4 | `tests/mcp/test_mcp_resolver.py` (unidade, Ollama e `claude` trocados); C2 (manual, `tev1` real) |
| `Pedido 7` | papel diferente de `consultant` devolve proposta de gate e não abre worker; a conta diferente da ativa é recusada enquanto o `worker-start` não levar conta (X38, R6.1) | P3 | `tests/mcp/test_mcp_gates.py` (unidade) |

### Fora de escopo

- **Outros runtimes (Codex, `agy`), o M4:** fase 3; ficam no PLN-003/P12. O `dispatch` aceita só `runtime: "claude"` e
  recusa o resto com erro claro.
- **O `.mcp.json` do plugin do Claude:** é do PLN-003/P4; daqui sai só o `brza mcp url`, que ele usa.
- **O painel do Orca (R10.3):** o PLN-003/P10 consome o `status` deste plano.

## Pré-requisitos

- **O índice da `master` com `priority`, `blocks` e `deadline` (PLN-003/P1):** sem ele, a fila usa só os campos que o
  `dispatch` recebe. Não trava o P2; trava o caso C3.
- **Python 3.10 ou mais** no interpretador que roda `brza mcp start`, que o plist fixa.
- **Ollama com o `tev1:4b`**, só para o C2; a ausência é coberta pelo fallback.

## Entrevista

### Rodada 1 — onde mora o código e quem é o dono do trabalho (enviada 2026-11-03)

> **Apresentado antes:** a R5.3 do PLN-003 decidiu "o repositório próprio `brz-anderson/brza`"
> (`PLN-003-interview.md:253-260`, 2026-10-29), que não existe no GitHub (`gh repo view brz-anderson/brza` → "Could not
> resolve to a Repository"); o `brza-workflow` nasceu depois, em 2026-10-31 (PLN-006/P1), com `packages/client`,
> `bin/brza-*` e o `brza install`. Os P6 a P9 do PLN-003 (`PLN-003-plan.md:171-222`) repetem os P1 a P5 deste plano, e
> o PLN-003 não aponta para cá.

Respondida em 2026-11-03, na sessão do `tools-kit` que retomou o plano.

1. **Onde mora o código do MCP.** Opções:
   - `~/Projects/brza-workflow/packages/mcp/`, com o `bin/brza-mcp` ligado pelo `brza install`, reabrindo a R5.3
     (recomendada). Custo: ~0 agora; o PLN-003 P3 passa a publicar o `brza-workflow`. Se paga: agora;
   - um repositório local `~/Projects/brza`, sem push. Custo: ~15 min e uma segunda base de testes e instalação. Se
     paga: na 1ª publicação no PyPI, se o pacote tiver de ser separado do núcleo;
   - o PLN-003 P3 antes, publicando `brz-anderson/brza`. Custo: ~4 h e um push público sem código. Se paga: na 1ª
     publicação;
   - esperar. Custo: 22,5 h paradas. Se paga: nunca, por si.

   **Respondida — "brza-workflow (Recomendado)".** Reabre a PLN-003/R5.3 para o código do MCP.

2. **Quem é o dono do trabalho do MCP.** Opções:
   - o PLN-009; uma issue pede à sessão do PLN-003 que marque os P6 a P9 como `[-]` → PLN-009 (recomendada). Custo:
     ~10 min na sessão do PLN-003. Se paga: agora;
   - os dois, com ponteiro. Custo: marcar duas vezes. Se paga: nunca;
   - volta ao PLN-003, e este plano vira `dropped`. Custo: perde o plano próprio. Se paga: só se o MCP não precisar de
     frente própria.

   **Respondida — "PLN-009 (Recomendado)".**

### Rodada 2 — os pontos da revisão do Desenho (2026-11-03)

> **Apresentado antes:** o parecer [REV: o Desenho do PLN-009 antes da execução](../../work/reviews/pln-009-o-desenho-antes-da-execucao.md),
> com 14 achados e quatro pontos para rodada.

Respondida em 2026-11-03, nesta sessão, pela regra que Anderson deu antes dela: "escolha o encaminhamento dos achados
sempre pela opção `recomendada`" e "prefira sempre optar por `corrigir aqui`". As opções estão no parecer, com o custo.

1. **Para onde vão o M6, o M7, o M13, o M14 e a PLN-003/R6.4** (A2, A3). **Respondida — a recomendada:** entram neste
   plano, num D6 "o ciclo e a conta", com o `brza quota` como verbo; ~7 h a mais.
2. **Os limiares sem rodada** (A6). **Respondida — as duas recomendadas:** a porta é chave do `brza.toml`, `4242` o
   padrão, sem fallback automático; os tetos da máquina e a confiança do `tev1` nascem como chaves sem valor imposto —
   a máquina só registra até a medição dar o número, e o `tev1` manda tudo ao Haiku até a calibração da fase 2b.
3. **O `tev1:4b` ocupa 7,7 GB carregado** (A6). **Respondida — a recomendada:** o desempate não conta no teto de
   workers, e o `keep_alive` do Ollama fica em 1 min.
4. **Onde vai a linha `route`** (D5). **Respondida — a recomendada:** no `.measurements/measurements.jsonl` do
   workspace, com `event: "route"`.
5. **A conta sem dado de uso e o teto de sessões** (A9), sem opção no parecer. **Escolha desta sessão, pela regra de
   preferir `corrigir aqui`:** o teto de sessões por conta e runtime da PLN-003/R7.1 entra como chave; a conta sem dado
   de uso admite worker só dentro dele, com a linha `route` dizendo `quota_unknown`. Revisável por Anderson.
6. **Como o chat põe o token no `Authorization`** (A12), sem opção no parecer. **Escolha desta sessão, pela mesma
   regra:** o `claude-brza` e a função `claude` exportam `BRZA_MCP_TOKEN`, lido do arquivo, quando ele existe.
   Revisável por Anderson.

### Rodada 3 — o revisor do laço sem a cota do `agy` (enviada 2026-11-03)

> **Apresentado antes:** o `agy` esgotou a cota individual do Gemini 4 Argon (volta em ~164 h) e do Claude Opus (volta
> em ~5 h) nas rodadas 1 do P2 a P4 e na 2 do P1, que não rodaram; só o Gemini 3.8 Flash ainda respondia.

Respondida em 2026-11-03, na sessão do `tools-kit`.

1. **Com que revisor segue o laço.** Opções:
   - o `gemini-3.8-flash-high` no `agy`, e uma rodada final de cada passo pelo Opus quando a cota voltar, antes do `[x]`
     (recomendada). Custo: uma rodada a mais por passo e a camada rápida no meio do laço. Se paga: agora;
   - esperar o Opus. Custo: ~5 h de espera no laço. Se paga: se a camada alta em toda rodada importa mais que o prazo;
   - só o Flash. Custo: revisão na camada rápida, contra a norma. Se paga: se a cota do Opus tiver de ficar para outro
     trabalho;
   - o `reviewer` do Claude, fora do `agy`. Custo: sai da instrução de usar o `agy`. Se paga: agora, sem esperar.

   **Respondida — "Flash agora, Opus depois (Recomendado)".**

### Rodada 4 — a medição Flash × Opus e os achados que pediam escolha (2026-11-03)

> **Apresentado antes:** o pedido de Anderson, "compare os achado do `Gemini Flash 3.8` e do `Opus 5.5`, registre como
> medição".

Respondida em 2026-11-03, na sessão do `tools-kit`.

1. **De onde vem a revisão do Opus.** Opções: o Opus pelo `agy`, quando a cota voltar (recomendada); o `reviewer` do
   Claude Code, agora; só o que já existe. **Respondida — "Opus pelo reviewer, agora".** O Opus revisou os mesmos
   commits do P2 a P5 com o mesmo prompt do Flash.
2. **Onde fica o registro.** Opções: o log e o worklog (recomendada); só o worklog; uma nota de medição própria.
   **Respondida — "Log e worklog (Recomendado)".**
3. **Os achados que pediam escolha**, pela regra de Anderson ("opção `recomendada`", "prefira `corrigir aqui`"):
   P2 O-A6 e O-A7 corrigidos no P5 (o uso por conta, e o pedido sem conta vale a ativa); P4 O-A7, a recomendada
   (`suggest_to_main` nasce `false`); P4 O-A8, corrigido o que cabe (o `choose_account` pelo cálculo do `Limits`), e "o
   MCP propõe a conta" numa issue; P5 O-A7, o conserto proposto (o client sai do `ORCA_USER_DATA_PATH` no header).

### Rodada 5 — a rodada final sem o Opus do `agy` (2026-11-03)

> **Apresentado antes:** Anderson avisou que "a cota do semanal `Opus` no `agy` reseta daqui 3 dias e já está em 93%";
> o Argon volta em ~7 dias. As seis rodadas finais da R3 não cabem.

Respondida em 2026-11-03, na sessão do `tools-kit`.

1. **Com que revisor vai a rodada final, a que dá o `[x]`.** Opções: seis `reviewer` Opus do Claude Code, um por passo
   (recomendada; ~6 × 130 a 175 mil tokens; se paga agora); um `reviewer` Opus para a entrega inteira (~250 a 350 mil
   tokens, um contexto só); esperar o Opus do `agy` (~3 dias); fechar com o Flash (perde ~3 de cada 4 achados
   importantes, pela medição). **Respondida — "reviewer Opus, por passo (Recomendado)".** Substitui a rodada final da
   R3.

### Rodada 6 — os pontos da rodada final pelo Opus (2026-11-03)

> **Apresentado antes:** os pareceres da rodada final (R5), um por passo, com 4 pontos para rodada e 3 achados que o
> revisor mandaria a issue.

Respondida em 2026-11-03, nesta sessão, pela regra de Anderson ("opção `recomendada`", "prefira `corrigir aqui`").

1. **A troca de conta no gate (P3 A2).** **Respondida — a recomendada:** aceitar o X38 e ajustar o texto; o gate de
   conta só abre quando a conta difere da ativa, e a troca real segue recusada enquanto o `worker-start` não levar conta.
2. **O `brza.toml` que deixa de ler com o servidor de pé (P4 A3).** **Respondida — a recomendada:** mantém a última
   configuração lida e escreve o erro no stderr; na subida, sem anterior, os padrões (X36).
3. **A conta gravada no `dispatch` envelhece até a abertura (P5).** **Respondida — a recomendada:** o pedido sem
   `account` grava `''`, e o `Limits` o trata como a ativa da hora da admissão (o X34 revisto).
4. **Como sai o pedido `running` preso (P5 A3).** **Respondida — a recomendada:** só a recuperação, no `start()` e
   depois de N voltas sem `dispatch`; sem ferramenta `cancel`.
5. **Os achados que iam a issue** (P2 A5, P5 A5): pela preferência por `corrigir aqui`, corrigidos na branch integrada,
   que já tem os passos que eles tocam.

### Rodada 7 — o que o C1 achou no launchd real (2026-11-03)

> **Apresentado antes:** o C1 passou no roteiro, mas o `stop` deixava o plist com `RunAtLoad`, e o login subiria o
> serviço de novo; e a fila real tinha dois pedidos de teste de 04:55 (`t`, caller `s`), um deles despachado ao Studio
> na subida e recusado com `session_caller_unknown`, sem efeito.

Respondida por Anderson em 2026-11-03, nesta sessão.

1. **O plist depois do `stop`.** **Respondida — a recomendada:** "P8: stop apaga plist" — o `stop` apaga o plist depois
   do `bootout` e espera o agente descarregar; o `start` volta a gravá-lo; o C1 se refaz antes do merge.
2. **Os pedidos de teste na fila real.** **Respondida — a recomendada:** "Copiar e zerar a fila" — a
   `orchestrator.db` copiada para o scratch da sessão (`orchestrator.db.c1-residuo`) e apagada.

## Desenho

### O que este desenho assume

- **PLN-003/R4.1:** o MCP é o coordenador do fluxo, com um agente que roteia e uma fila.
- **PLN-003/R5.2:** o consultor roda livre; o executor e a troca de conta passam pelo gate da sessão principal.
- **PLN-003/R6.3 e R6.4:** a política mora num `brza.toml`; o MCP decide o modelo da sessão que abre e sugere à
  principal, por aviso.
- **PLN-003/R7.1 e R9.1–R9.4:** a fila e os três tetos.
- **O P0 do PLN-003 (H1 a H6), medido em 2026-11-03** ([O PLN-003: a medição das hipóteses da fase 0 (P0)](../../work/worklogs/2026-11-03-pln-003-medicao-das-hipoteses-p0.md)):
  os ajustes valem como requisito.
- **R1 e R2 deste plano.**

### D1 — O servidor residente e o ciclo de vida (`packages/mcp/brza_mcp/server.py`, `launchd.py`, `bin/brza-mcp`)

- **Origem:** PLN-003/R3.4, PLN-003/B6, R1.1, R2.2, R2.6; H1, H2 e H5 do P0.
- **Repositório:** `~/Projects/brza-workflow`, pacote `packages/mcp/brza_mcp/` e executável `packages/mcp/bin/brza-mcp`
  (R1.1). O `brza install --mcp` o liga em `~/.local/bin`, e o `brza mcp <verbo>` chega a ele pelo despacho `brza-<sub>`
  do CLI do app.
- **Servidor:** `http.server.ThreadingHTTPServer` com `protocol_version = "HTTP/1.1"` e `Content-Length` explícito,
  porque o Claude Code mantém um `GET /mcp` (SSE) aberto em paralelo aos `POST /mcp` (H5). Streamable HTTP: `POST /mcp`
  (JSON-RPC: `initialize`, `notifications/*` → 202, `ping`, `tools/list`, `tools/call`; método desconhecido, como o
  `server/discover` que o Claude Code manda primeiro, → `-32601`) e `GET /mcp` (SSE com keep-alive). `GET /health`.
- **Porta:** só em `127.0.0.1`; a chave `[mcp] port` do `brza.toml`, `4242` por padrão, sem fallback automático: porta
  ocupada é erro (R2.2). `brza mcp url` imprime a URL, para o `.mcp.json` do PLN-003/P4.
- **Token:** `~/.brza/runtime/mcp.token`, criado `0600` na primeira subida; toda rota exige o Bearer, senão 401.
  `brza mcp token` o imprime; o `claude-brza` e a função `claude` do pacote do cliente exportam `BRZA_MCP_TOKEN` a partir
  dele (R2.6), para o `"Authorization": "Bearer ${BRZA_MCP_TOKEN}"` do `.mcp.json` (H1).
- **Launchd:** `~/Library/LaunchAgents/com.brza.orchestrator.plist`, com `ProgramArguments` fixando o interpretador que
  rodou o `brza mcp start` (3.10 ou mais; o `/usr/bin/python3` é o 3.9.6), `EnvironmentVariables` com `HOME` e um `PATH`
  que tem `~/.local/bin` (H2), `KeepAlive` só em saída com erro, e os logs em `~/.brza/runtime/`.
- **A base `~/.brza`** troca por `BRZA_HOME`, e o diretório dos LaunchAgents por `BRZA_LAUNCH_AGENTS_DIR`: é assim que
  os testes ficam fora do estado da máquina.

```text
brza mcp start   # grava o plist, launchctl bootstrap gui/<uid>, espera o /health
brza mcp stop    # launchctl bootout gui/<uid>/com.brza.orchestrator
brza mcp status  # carregado? /health responde? sai 0 de pé, 3 parado
brza mcp token   # imprime o token
brza mcp url     # imprime http://127.0.0.1:<porta>/mcp
brza mcp config [<chave> [<valor>]]   # D4, a chave de desligamento
```

### D2 — A fila e os três tetos (`packages/mcp/brza_mcp/queue.py`, `limits.py`)

- **Origem:** PLN-003/R7.1, PLN-003/R9.1–R9.4, PLN-003/M8, PLN-003/M24, R2.2, R2.3, R2.5.
- **Armazenamento:** SQLite da stdlib em `~/.brza/orchestrator.db`, tabelas `requests` e `workers`.
- **De onde vêm `deadline`, `blocks` e `priority`:** do `dispatch` (D3), quando vêm; senão, do índice da `master` pelo
  `ref` do pedido (`PLN-NNN`, o caminho da issue), lendo a última linha de cada `id` no `.brza/index.jsonl` — que é um
  log de eventos, e não um retrato. Sem nenhum dos dois, o pedido entra sem eles.
- **A ordem (R9.2):** `deadline` mais próximo; depois quem tem `blocks`; depois `priority` (`high`, `medium`, `low`,
  ausente por último); depois a chegada.
- **Os tetos (R9.3: o menor manda):**
  - **workspace:** `[orchestrator] max_workers`;
  - **conta e runtime:** `[quota] max_sessions_per_account` (R7.1) e a projeção — a variação do `usedPercent` até o
    `resetsAt`; a conta que chega a `hard_cap_percent` (90) antes do reset não recebe worker. A conta sem dado de uso
    admite só dentro do teto de sessões, com `quota_unknown` na linha `route` (R2.5). O uso vem do `orca account list
    --json` do client detectado, pelo D6, por conta: a ativa em `rateLimits.claude` e as outras em
    `inactiveClaudeAccounts`; o pedido sem `account` conta como a ativa (R4.3);
  - **máquina:** memória livre, swap e CPU medidos a cada admissão. As chaves `[machine] min_free_mem_gb`,
    `max_swap_gb` e `max_cpu_percent` nascem sem valor: sem valor, a máquina só registra na linha `route` e não segura
    (R2.2).
- **O desempatador não conta como worker** (R2.3).
- **O `status`** diz, para cada pedido parado, o teto que o segura.

### D3 — As ferramentas MCP, o despacho e os gates (`packages/mcp/brza_mcp/tools.py`)

- **Origem:** PLN-003/R4.1, PLN-003/R5.2, PLN-003/M1, PLN-003/M12, PLN-003/M15, H1.
- **Quem chamou:** o header `X-Brza-Session` (H1), e o argumento `caller` quando o header falta. **De que client:** o
  header `X-Brza-Client: ${ORCA_USER_DATA_PATH}`, de que o MCP tira o client (Studio ou Orca) e o `ORCA_USER_DATA_PATH`
  do H4 (R4.3).
- **Os gates (R5.2, M15):** só `role: "consultant"` entra direto na fila. Qualquer outro papel — o executor, o
  arquiteto, o desconhecido — devolve `{"gate": {...}}` com a proposta, sem abrir worker; a sessão principal pergunta a
  Anderson e chama `dispatch` de novo com `approved: <id do gate>`. **A troca de conta** é recusada com erro claro
  enquanto o `worker-start` não levar conta (X20, X38, R6.1); a conta igual à ativa entra como se não viesse.
- **As ferramentas:**

```json
{"name": "dispatch", "inputSchema": {"type": "object", "required": ["task", "role"], "properties": {
  "task": {"type": "string"}, "role": {"type": "string"}, "target": {"type": "string"},
  "runtime": {"enum": ["claude"]}, "model": {"type": "string"}, "effort": {"type": "string"},
  "account": {"type": "string"}, "ref": {"type": "string"}, "deadline": {"type": "string", "format": "date"},
  "blocks": {"type": "array", "items": {"type": "string"}}, "priority": {"enum": ["high", "medium", "low"]},
  "caller": {"type": "string"}, "approved": {"type": "string"}}}}
{"name": "status", "inputSchema": {"type": "object", "properties": {}}}
{"name": "config", "inputSchema": {"type": "object", "properties": {"key": {"type": "string"}, "value": {}}}}
```

### D4 — A política e o desempatador (`brza.toml`, `packages/mcp/brza_mcp/policy.py`, `resolver.py`)

- **Origem:** PLN-003/R5.1, PLN-003/R6.3, PLN-003/R6.4, PLN-003/M9, PLN-003/M10, PLN-003/M11, R2.2, R2.3; H2.
- **O `brza.toml`** fica na raiz do workspace e é lido por `tomllib`, ou pelo `parse_toml` do `brza-workflow` abaixo do
  3.11. Os papéis seguem a R5.2: `consultant`, `executor`, `architect`.

```toml
[mcp]
port = 4242

[orchestrator]
max_workers = 6

[policy]
enforce = true            # a chave de desligamento (M10); false devolve o pedido sem imposição
suggest_to_main = false   # R6.4; nasce desligada até haver sinal do que a principal faz (R4.3)

[policy.roles.consultant]
model = "sonnet"
effort = "low"

[policy.roles.executor]
model = "sonnet"
effort = "medium"

[policy.roles.architect]
model = "opus"
effort = "high"

[quota]
soft_cap_percent = 55     # PLN-003/R7.1
hard_cap_percent = 90     # PLN-003/R7.1, R9.4
max_sessions_per_account = 2

[machine]                 # sem valor: só registra (R2.2)
# min_free_mem_gb =
# max_swap_gb =
# max_cpu_percent =

[resolver]
ollama_url = "http://127.0.0.1:11434"
tev1_model = "tev1:4b"
tev1_keep_alive = "1m"    # R2.3
# tev1_min_confidence =   # sem valor: tudo ao Haiku até a calibração da fase 2b (R2.2)
haiku_max_budget_usd = 0.01   # o da sonda do H2, que custou de US$ 0,0016 a 0,0039
```

- **O desempate (M11):** a tabela decide o que é determinístico (papel, cota); o texto ambíguo vai ao `tev1:4b`
  (`POST /v1/systemone`), e ao Haiku quando o limiar não tem valor ou a confiança fica abaixo dele, por `claude -p --model
  haiku --effort low --output-format json --json-schema … --max-budget-usd <chave> --no-session-persistence`. Sem
  Ollama, ou com erro dele, vai direto ao Haiku; sem `claude`, fica a tabela, e a linha `route` diz o motivo.

### D5 — A telemetria `route` (`packages/mcp/brza_mcp/telemetry.py`)

- **Origem:** PLN-003/M16, R2.4.
- **Onde:** `<workspace>/.measurements/measurements.jsonl`, o mesmo log do hook de medição, com `event: "route"`. O
  workspace é o `BRZA_WORKSPACE` do `brza mcp start`, gravado no plist.
- **A linha:**

```json
{"ts": "2026-11-03T12:00:00Z", "event": "route", "workstream": "tools-kit", "caller": "<X-Brza-Session>", "request": 12, "decision": "admitted", "model": "sonnet", "effort": "low", "account": "dot-claude-adm", "reason": "policy", "held_by": null, "machine": {"free_mem_gb": 9.1, "swap_gb": 0.4, "cpu_percent": 31}, "resolver": null}
```

### D6 — O ciclo e a conta (`packages/mcp/brza_mcp/cycle.py`, `accounts.py`, `bin/brza-quota`)

- **Origem:** PLN-003/M6, PLN-003/M7, PLN-003/M13, PLN-003/M14, R2.1; H2, H3 e H4.
- **O ciclo (M13, H4):** o worker admitido abre pelo `orca orchestration` do client detectado (`run-create`,
  `task-create`, `worker-start`), com `ORCA_AGENT_SESSION_ID` (o `X-Brza-Session`) e `ORCA_USER_DATA_PATH` do client no
  `env` do subprocesso; sem eles, o `run-create` cai noutro terminal ou falha (`no_active_sender_terminal`).
- **O fim volta ao chamador (M14):** o `worker_done` muda o pedido para `done` e libera o teto; o `status` do chamador
  o mostra.
- **A conta (M6, H2, H3):** o `claude -p` de uma conta gerenciada recebe `CLAUDE_CONFIG_DIR` do perfil; o da
  `systemDefault` vai sem a variável. A troca numa sessão de chat é o RPC `agentSession.switchAccount`, só em repouso, e
  passa pelo gate.
- **O `brza quota` (M7):** lê o `orca account list --json` e mostra, por conta, o `usedPercent`, o `resetsAt` e a
  projeção; `--json` para o MCP.

## Passos

> Os passos executam a pedido de Anderson (2026-11-03: "execute todos os passos que não dependem de decisões minhas"),
> no worktree `~/Projects/brza-workflow/.worktrees/pln-009-mcp`, branch `feat/pln-009-mcp`; o commit vai a essa branch
> (enviada ao `origin` depois do `[x]`). Cada passo só recebe `[x]` depois do laço de revisão pelo `agy`. O gate é
> `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/mcp` e `-s tests/cli`, este num ambiente limpo
> (`env -i HOME="$HOME" PATH="<dir do python3 3.10+>:/usr/bin:/bin"`), pela issue dos testes no chat.

### P1 — O servidor residente e o ciclo de vida

Executa D1 · executor: `implementer`, pela sessão do `tools-kit`

Estimado: 5.0 h · Executado: 0.7 h

- [x] **1. Testes que falham:** `tests/mcp/test_mcp_auth.py` (sem header, token errado → 401; token `0600`) e
  `tests/mcp/test_mcp_lifecycle.py` (`initialize`, 202, `-32601`, SSE, porta ocupada, plist, `start`/`stop`/`status` com
  o `launchctl` trocado, `serve` parado por `SIGTERM`).
- [x] **2. Implementar o servidor e o `brza-mcp`.**
- [x] **3. O `brza install --mcp` e o `BRZA_MCP_TOKEN` no `claude-brza` e na função `claude`.**
- [x] **4. Rodar e ver passar:** o gate.
- [x] **5. Commit** no `brza-workflow`, branch `feat/pln-009-mcp`.
- [x] **6. Revisão pelo `agy`** até 3 rodadas.

**Evidência:** `brza-workflow@1dfc9d9`, correções `f8829f4`, `77b917f` e `b2c87a6`; `tests/mcp` → 346 OK, `tests/hooks` → 290 OK, `tests/cli` limpo → 445 OK (no `b2c87a6`); revisão: Argon r1 (6 corrigidos), Flash r2 e r3, Opus final (5 corrigidos) — [REV: os passos P1 a P6 do PLN-009, revisados pelo agy e pelo Opus](../../work/reviews/pln-009-a-revisao-dos-passos.md). O `launchd` real fica no C1.

### P2 — A fila e os três tetos

Executa D2 · executor: `implementer`, pela sessão do `tools-kit`

Estimado: 5.5 h · Executado: 0.5 h

- [x] **1. Testes que falham:** `tests/mcp/test_mcp_queue.py` (persistência; a ordem `deadline` > `blocks` > `priority`
  > chegada; o índice lido pelo `ref`, com o log reduzido à última linha) e `tests/mcp/test_mcp_limits.py` (cada teto
  segura e o `status` diz qual; a conta sem uso dentro do teto de sessões; a máquina sem valor só registra).
- [x] **2. Implementar a fila e os tetos.**
- [x] **3. Rodar e ver passar:** o gate.
- [x] **4. Commit.**
- [x] **5. Revisão pelo `agy`** até 3 rodadas.

**Evidência:** `brza-workflow@084cc62`, correções `77b917f` e `b2c87a6`; `tests/mcp` → 346 OK, `tests/hooks` → 290 OK, `tests/cli` limpo → 445 OK (no `b2c87a6`); revisão: Flash e Opus r1 (medição, R4), Flash r2 e r3, Opus final — [REV: os passos P1 a P6 do PLN-009, revisados pelo agy e pelo Opus](../../work/reviews/pln-009-a-revisao-dos-passos.md).

### P3 — As ferramentas, o despacho e os gates

Executa D3 · executor: `implementer`, pela sessão do `tools-kit`

Estimado: 4.5 h · Executado: 0.5 h

- [x] **1. Testes que falham:** `tests/mcp/test_mcp_dispatch.py` (o schema, o `X-Brza-Session` e o `caller`, o
  `runtime` fora de `claude` recusado) e `tests/mcp/test_mcp_gates.py` (só o consultor entra; o resto devolve gate; a
  conta diferente da ativa é recusada (X38); o `approved` admite).
- [x] **2. Implementar `dispatch`, `status` e `config`.**
- [x] **3. Rodar e ver passar:** o gate.
- [x] **4. Commit.**
- [x] **5. Revisão pelo `agy`** até 3 rodadas.

**Evidência:** `brza-workflow@e7d8fa6`, correções `77b917f` e `b2c87a6`; `tests/mcp` → 346 OK, `tests/hooks` → 290 OK, `tests/cli` limpo → 445 OK (no `b2c87a6`); revisão: Flash e Opus r1, Flash r2, Opus final — [REV: os passos P1 a P6 do PLN-009, revisados pelo agy e pelo Opus](../../work/reviews/pln-009-a-revisao-dos-passos.md).

### P4 — A política e o desempatador

Executa D4 · executor: `implementer`, pela sessão do `tools-kit`

Estimado: 5.0 h · Executado: 0.5 h

- [x] **1. Testes que falham:** `tests/mcp/test_mcp_policy.py` (o `brza.toml` no 3.10 e no 3.11; o `enforce = false`;
  o `brza mcp config`) e `tests/mcp/test_mcp_resolver.py` (Ollama e `claude` trocados por dublês: o `tev1` sem limiar
  manda ao Haiku; sem Ollama, direto ao Haiku; sem `claude`, fica a tabela; o `keep_alive`).
- [x] **2. Implementar.**
- [x] **3. Os casos do M11 no git:** `tests/mcp/fixtures/m11_cases.json`, refeitos a partir da medição do M11 (os
  scripts dela ficaram fora do git).
- [x] **4. Rodar e ver passar:** o gate.
- [x] **5. Commit.**
- [x] **6. Revisão pelo `agy`** até 3 rodadas.

**Evidência:** `brza-workflow@8801c77`, correções `77b917f` e `b2c87a6`; `tests/mcp` → 346 OK, `tests/hooks` → 290 OK, `tests/cli` limpo → 445 OK (no `b2c87a6`); casos do M11 em `tests/mcp/fixtures/m11_cases.json` (o `tev1` real: 9/10); revisão: Flash e Opus r1, Flash r2, Opus final — [REV: os passos P1 a P6 do PLN-009, revisados pelo agy e pelo Opus](../../work/reviews/pln-009-a-revisao-dos-passos.md). O `tev1` frio fica no C2.

### P5 — O ciclo e a conta

Executa D6 · executor: `implementer`, pela sessão do `tools-kit`

Estimado: 7.0 h · Executado: 0.6 h

- [x] **1. Testes que falham:** `tests/mcp/test_mcp_cycle.py` (a CLI do client trocada recebe o env do H4; o
  `worker_done` libera o teto), `tests/mcp/test_mcp_accounts.py` (o `CLAUDE_CONFIG_DIR` omitido na `systemDefault`) e
  `tests/mcp/test_brza_quota.py` (a projeção a partir de um JSON gravado do `orca account list`).
- [x] **2. Implementar o ciclo, a conta e o `brza-quota`.**
- [x] **3. Rodar e ver passar:** o gate.
- [x] **4. Commit.**
- [x] **5. Revisão pelo `agy`** até 3 rodadas.

**Evidência:** `brza-workflow@a4ff8db`, correções `77b917f` e `b2c87a6`; `tests/mcp` → 346 OK, `tests/hooks` → 290 OK, `tests/cli` limpo → 445 OK (no `b2c87a6`); revisão: Flash e Opus r1, Flash r2, Opus final — [REV: os passos P1 a P6 do PLN-009, revisados pelo agy e pelo Opus](../../work/reviews/pln-009-a-revisao-dos-passos.md). O `--json` real do `orchestration` fica no C4.

### P6 — A telemetria `route` e a ponta a ponta

Executa D5 · executor: `implementer`, pela sessão do `tools-kit`

Estimado: 3.0 h · Executado: 0.4 h

- [x] **1. Testes que falham:** `tests/mcp/test_mcp_telemetry.py` (a linha `route` no `measurements.jsonl` de um
  workspace temporário) e `tests/mcp/test_mcp_e2e.py` (servidor de verdade, `dispatch` de dois pedidos com os tetos e
  o desempate trocados).
- [x] **2. Implementar.**
- [x] **3. Rodar e ver passar:** o gate.
- [x] **4. Commit.**
- [x] **5. Revisão pelo `agy`** até 3 rodadas.

**Evidência:** `brza-workflow@1fa3e60`, correções `77b917f` e `b2c87a6`; `tests/mcp` → 346 OK, `tests/hooks` → 290 OK, `tests/cli` limpo → 445 OK (no `b2c87a6`); revisão: Flash r1 e r2, Opus final — [REV: os passos P1 a P6 do PLN-009, revisados pelo agy e pelo Opus](../../work/reviews/pln-009-a-revisao-dos-passos.md).

### P7 — Corrigir conta e perfil encontrados na revisão da entrega

Executa D2, D3 e D6 · executor: subagente `implementer`, com revisão independente

Estimado: 0,5 h · Executado: 0,3 h

- [x] **1. Reproduzir A1 e A2:** três regressões falharam antes no `b2c87a6`.
- [x] **2. Corrigir:** revalidar conta explícita na admissão; fixar a conta do worker; preservar perfil nas contas e no cache.
- [x] **3. Revisar e testar:** revisor independente, 63 testes pontuais OK; MCP 349 OK (um pulado).
- [x] **4. Commit:** `brza-workflow@354d004`, na `feat/pln-009-mcp`.

**Evidência:** [REV: a entrega do PLN-009 contra o Pedido e a Cobertura](../../work/reviews/pln-009-a-revisao-da-entrega.md).
O gate MCP rodou no worktree real, com leitura de `sysctl` liberada. Desvios X46 e X47.

### P8 — O `stop` apaga o plist e espera o agente descarregar

Executa R7.1 e D1 · executor: subagente `implementer`, com revisão pelo `agy` e pelo `reviewer`

Estimado: 0,8 h · Executado: 0,8 h

- [x] **1. Testes antes:** 6 testes novos do `stop`; 4 falharam e 2 deram erro no `354d004`.
- [x] **2. Corrigir:** o `stop` apaga o plist depois do `bootout`, espera o descarregamento e apaga o plist órfão.
- [x] **3. Revisar:** r1 pelo `agy` (Flash, 6 achados) e pelo `reviewer` (Opus, 4 achados), em paralelo; 5 corrigidos
  aqui na r2, a corrida `start` × `stop` em issue; r2 pelo `agy` sem achado.
- [x] **4. Refazer o C1:** no launchd real, com o `stop` novo.
- [x] **5. Commit:** `brza-workflow@007383a`, na `feat/pln-009-mcp`.

**Evidência:** `tests/mcp` → 358 OK (um pulado), `tests/cli` limpo → 445 OK, `test_mcp_lifecycle` em 8 s (o teste do
`start` depois do `stop` levava 15 s e passava com o `start` falhando); pareceres na seção do P8 de
[REV: a entrega do PLN-009 contra o Pedido e a Cobertura](../../work/reviews/pln-009-a-revisao-da-entrega.md). Desvio X48.

### Casos manuais

- **C1 — O launchd real:** `brza install --mcp`, `brza mcp start`, `brza mcp status` → 0, `curl` do `/health` com o
  token, `brza mcp stop`, `brza mcp status` → 3. Com Anderson, porque carrega um LaunchAgent na máquina.
  - **Observado (2026-11-03, `354d004`):** o roteiro passou — `status` 3 → `start` 0 (pid 77306) → `status` 0 →
    `/health` 200 com o token, 401 sem ele e com token errado, só em `127.0.0.1:4242` → `stop` 0 → `status` 3 → `stop`
    repetido 0. Dois achados (R7): o plist ficava com `RunAtLoad` depois do `stop`; e a subida despachou um pedido de
    teste da fila real, recusado pelo Studio sem efeito.
  - **Observado (2026-11-03, `007383a`, depois do P8):** `status` 3 → `start` 0 (pid 29443), plist gravado → `status`
    0 → `/health` 200 com o token e 401 sem ele → `stop` 0 em 1 s, plist apagado → `status` 3 logo depois, porta livre,
    `launchctl print` 113 → `stop` repetido 0. Fila nova vazia.
  - **Veredito:** aprovado.
- **C2 — O `tev1` real:** um desempate com o Ollama de pé, frio e carregado, medindo o tempo.
- **C4 — O ciclo real:** um `dispatch` de consultor no Studio abre run, task e worker, e o `--json` de cada verbo traz
  as chaves que o `cycle.py` procura (X24); o fim volta pelo `task-list`.
- **C3 — A fila pelo índice:** depois do PLN-003/P1, dois pedidos com `ref` de notas com `priority` e `deadline`.

## Regressão

- **O `brza` sem o servidor:** os outros `brza <sub>` seguem iguais com o MCP parado. Como se confere: o gate
  `tests/cli` verde.
- **A sessão que não usa o orquestrador:** nada muda sem o `.mcp.json` do plugin. Como se confere: o
  `claude-brza` sem o token exporta só o que já exportava (`tests/cli/test_brza_shell.py`).
- **Sem Ollama, sem `tev1`, sem `claude`:** o pedido não trava. Como se confere: `tests/mcp/test_mcp_resolver.py`.

## Desvios

- **X1 — A porta padrão troca por `BRZA_MCP_PORT`.** Para o teste de `start`/`status` não depender da 4242 real; a
  precedência é `--port` > `BRZA_MCP_PORT` > `[mcp] port` > 4242. Afeta P1 e D1.
- **X2 — O plist leva `BRZA_HOME` e `BRZA_MCP_PORT` quando estão no ambiente do `start`.** A base do agente é a mesma
  de quem o subiu. Afeta P1.
- **X3 — `GET /mcp` sem `Accept: text/event-stream` responde 406**, como o Streamable HTTP pede. Afeta P1.
- **X4 — `brza mcp start --timeout` (15 s) e `bootstrap` repetido até 5 vezes**, porque o `bootout` termina de forma
  assíncrona. Afeta P1.
- **X5 — `brza mcp stop` com o agente descarregado sai 0.** Idempotente. Afeta P1.
- **X6 — A revisão do `agy` roda com o `claude-opus-5-5-high`, e não com o Gemini 4 Argon.** A cota do Argon (high e
  medium) acabou na 1ª rodada do P2, com reset em ~164 h; o Opus pelo `agy` mantém o `agy` e a camada alta. Afeta o
  laço de revisão de todos os passos. Substituído pela R3.

Os desvios abaixo foram propostos pelo `implementer` e aceitos na rodada 1 de revisão de cada passo (os pareceres estão
em [Revisões](#revisões)); "com correção" quer dizer que o passo ganhou o conserto que a revisão pediu.

- **X7 — O `pending()` lista só os `queued`; os `gated` vão à parte no `status`.** Afeta P2 e D2.
- **X8 — Só o pedido que um teto segura recebe `held_by`, com a coluna `held_reason`.** Afeta P2 e D2.
- **X9 — A avaliação para no primeiro teto que segura** (workspace, sessões, cota, máquina). Afeta P2 e D2.
- **X10 — `hard_cap_percent` sem valor vale 90**, o do D4. Afeta P2 e D2.
- **X11 — A memória livre é livre + inativa + especulativa do `vm_stat`; a CPU é o `getloadavg()[0]` por núcleo.** Afeta P2.
- **X12 — O `dispatch` recusa argumento fora do schema**, para um `acount` não escapar do gate. Afeta P3 e D3.
- **X13 — `config` com `value: null` apaga a sobreposição; o tipo do valor se confere pela chave** (com correção). Afeta P3.
- **X14 — Com `approved`, vale a proposta guardada no gate, e não a `task`/`role` da 2ª chamada** (com correção). Afeta P3.
- **X15 — A resposta do `dispatch` leva `held_reason`; o `config` gravado vale nos tetos na hora** (com correção). Afeta P3.
- **X16 — O `parse_toml` do núcleo não lê float, e o `policy` contorna sem tocar no `core`.** Afeta P4.
- **X17 — O `config` não muda `policy.roles.*`**: os papéis só pelo `brza.toml`. Afeta P4 e D4.
- **X18 — A regra de conta do `choose_account`**: descarta a janela no teto, prefere a menos cheia e desempata em 5 pontos
  pela ordem alfabética, agora pelo mesmo cálculo do `Limits` (com correção). Afeta P4 e D4.
- **X19 — A camada vira papel: alta → `architect`, média → `executor`, rápida → `consultant`.** Afeta P4 e D4.
- **X20 — O `worker-start` não tem flag de conta**: a conta vai só ao `claude -p`, e o `dispatch` recusa `account`
  diferente da ativa com erro claro (com correção). Afeta P5 e D6.
- **X21 — O fim do worker é sabido pelo `task-list`, a cada 15 s**: não há `worker_done` por mensagem no CLI. Afeta P5 e D6.
- **X22 — A coluna `requests.client`, com migração.** Afeta P5.
- **X23 — O `switch_chat_account` não se liga ao gate**: o `dispatch` não tem a sessão alvo (com correção). Afeta P5 e D6.
- **X24 — O `--json` do `run-create`, `task-create`, `worker-start` e `task-list` não foi conferido sem run real**: o
  `cycle.py` procura as chaves em qualquer profundidade. Fica para o C4. Afeta P5.
- **X25 — Sem client conhecido, o pedido fica `queued` com o erro no `status`** (com correção). Afeta P5.
- **X26 — A conta se resolve por id, e-mail ou rótulo; o formato de `inactiveClaudeAccounts` vem do `brza-studio`.** Afeta P5.
- **X27 — A linha `route` usa `timestamp`, como o hook, e não o `ts` do exemplo do D5.** Afeta P6 e D5.
- **X28 — O `workstream` da linha `route` sai da branch do `BRZA_WORKSPACE` do daemon**, e não do workstream de quem
  pediu, que o `dispatch` não recebe. Afeta P6 e D5.
- **X29 — As decisões da linha `route` vão além de `admitted`**: `policy`, `resolved`, `queued`, `gated`, `approved`,
  `held`, `done`, `failed`, com as chaves `measures`, `gate`, `passthrough` e `machine.enforced`. Afeta P6 e D5.
- **X30 — O gancho `Queue.on_decision` é atributo único.** Afeta P6.
- **X31 — O `build` nasce sem o desempatador; só o `serve` o liga.** Afeta P6.

Os desvios abaixo vieram da rodada de correção (`brza-workflow@77b917f`), aceitos na rodada seguinte do Flash.

- **X32 — O `status` traz `finished` (os 10 últimos do chamador) e o `error` de cada pedido em fila.** Afeta P5 e D3.
- **X33 — O `dispatch` e o `approved` devolvem `model`, `effort` e `reason`; a proposta do gate leva o `reason`.** Afeta
  P3, P4 e D3.
- **X34 — O pedido sem `account` grava `''`, e o `Limits` o trata como a conta ativa da hora da admissão** (revisto
  pela R6.3; antes gravava a ativa da hora do `dispatch`). Afeta P2, P5 e D2.
- **X35 — O `config` tem lista fechada de chaves, com tipo e faixa.** Afeta P3, P4 e D4.
- **X36 — Com o `brza.toml` ilegível, o servidor sobe com os padrões e as três ferramentas respondem `isError` com o
  caminho.** Afeta P4 e D4.
- **X37 — A vaga do escolhido sai reservada no mesmo lock (`admit_next`, `release`, `set_session`), e o `Limits.scope()`
  lê o uso e a máquina uma vez por passada.** Afeta P2, P5, D2 e D6.
- **X38 — A conta que não é a ativa é recusada no `dispatch`**, e não só gateada, porque o `worker-start` não leva conta
  (X20). Afeta P5 e D6.
- **X39 — A limpeza do `worker-start` que falha usa `worker-release --dispatch` e `task-update --status failed`**, flags
  lidas no CLI do `brza-studio` e não executadas. Fica para o C4. Afeta P5.

Os desvios abaixo vieram da correção da rodada final (`brza-workflow@b2c87a6`), sem nova revisão: o teto de 3 rodadas
por passo foi atingido, e a prova é o gate com os testes vistos falhando antes.

- **X40 — O `status` aceita `caller` opcional, com a precedência do `dispatch`.** Afeta P3, P5 e D3.
- **X41 — O gate de conta só abre quando a conta difere da ativa, ou sem leitor de contas** (o X38, aceito na R6.1).
  Afeta P3 e D3.
- **X42 — O `X-Brza-Client` com a pasta de um perfil que tem `orca-runtime.json` vira o client `studio`, com o caminho
  guardado no pedido** (`requests.user_data`). Afeta P5 e D3.
- **X43 — O `brza.toml` é conferido pela tabela do `config`, mais `mcp.port` e `policy.roles.<papel>.{model,effort}`**,
  só nos namespaces do MCP. Afeta P4 e D4.
- **X44 — O gate guarda o `policy_reason`, e o `approved` devolve o `reason`**, como o X33 prometia. Afeta P3 e P4.
- **X45 — A linha `admitted` sai depois do `open` que deu certo, e não da prévia do `status`.** Afeta P6 e D5.

- **X46 — A conta explícita é reconferida na admissão**; divergência deixa o pedido na fila com `account_active`.
  O worker guarda a conta resolvida; pedido implícito continua `''` até admitir. Corrige A1, sem trocar conta (X38).
- **X47 — As contas e o cache preservam `user_data`**, como a abertura do worker já fazia (X42). Corrige A2.
- **X48 — O `stop` apaga o plist e espera o descarregamento até 25 s (`--timeout`)**, acima do `ExitTimeOut` de 20 s do
  launchd; o `bootout` que falha com o agente já fora conta como descarregado, e com o agente carregado mantém o plist.
  O D1 dizia só `bootout`. Afeta P1 e D1 (R7.1).

## Worklogs

- 2026-11-03 — plano criado e desenhado a partir da extração do componente MCP do PLN-003.
  [O PLN-009: abertura do plano do MCP residente](../../work/worklogs/2026-11-03-pln-009-abertura-do-plano-do-mcp-residente.md)
- 2026-11-03 — R1 a R4; o Desenho revisado e reescrito; P1 a P6 implementados, em revisão pelo `agy` (sem `[x]`); a
  medição Flash × Opus; R5 e R6, a rodada final pelo Opus e a correção dela; P1 a P6 `[x]`, e o plano em revisão.
  Travou na cota do `agy` (R3, R5).
  [O PLN-009: a execução do P1 a P6 e a revisão pelo `agy`, com a medição Flash × Opus](../../work/worklogs/2026-11-03-pln-009-execucao-e-revisao-pelo-agy.md)

- 2026-11-03 — revisão independente da entrega; A1 a A3 corrigidos e P7 concluído.
  [O PLN-009: a revisão da entrega e a correção da conta e do perfil](../../work/worklogs/2026-11-03-pln-009-revisao-da-entrega-conta-e-perfil.md)

- 2026-11-03 — C1 no launchd real; R7; P8 (o `stop` apaga o plist) e o C1 refeito, aprovado.
  [O PLN-009: o C1 no launchd real e o stop que apaga o plist](../../work/worklogs/2026-11-03-pln-009-c1-no-launchd-real.md)

## Revisões

- [REV: o Desenho do PLN-009 antes da execução](../../work/reviews/pln-009-o-desenho-antes-da-execucao.md) —
  2026-11-03, 14 achados, todos com destino.
- [REV: os passos P1 a P6 do PLN-009, revisados pelo agy e pelo Opus](../../work/reviews/pln-009-a-revisao-dos-passos.md) —
  2026-11-03, 3 rodadas por passo, todos os achados com destino.

- [REV: a entrega do PLN-009 contra o Pedido e a Cobertura](../../work/reviews/pln-009-a-revisao-da-entrega.md) —
  2026-11-03, três achados corrigidos; delta revisado; C1 a C4 pendentes.

## Pendências conhecidas

- [Os passos do MCP no PLN-003 passam ao PLN-009](../../work/issues/os-passos-do-mcp-no-pln-003-passam-ao-pln-009.md)
  — de R1.2 e A2; a sessão do PLN-003 marca os P6 a P9 como passados a este plano e reabre a R5.3.
- [Os testes do brza-workflow falham quando rodam dentro do chat do BrzA Studio](../../work/issues/testes-do-brza-workflow-falham-dentro-do-chat-do-app.md)
  — no P1, 20 falhas do `tests/cli` vindas do ambiente do chat; o gate deste plano roda o `tests/cli` em ambiente limpo.
- [O MCP propõe a conta do pedido](../../work/issues/o-mcp-propoe-a-conta-do-pedido.md) — de R4.3 (P4 O-A8); o
  `choose_account` sem chamador, até a decisão.
- [O start e o stop do MCP concorrentes](../../work/issues/o-start-e-o-stop-do-mcp-concorrentes.md) — do P8 (Flash 5,
  Opus A3); sem trava entre processos, até a primeira automação que chame os dois verbos.
- [Os pareceres do PLN-009 sem número REV](../../work/issues/os-pareceres-do-pln-009-sem-numero-rev.md) — da MIG-001
  do `workspace`; os três pareceres de `work/reviews/` ganham o `REV-NNN` antes do fechamento deste plano.

## Fechamento

- [x] Todo passo `[x]`, com revisão independente e os achados com destino (R3 a R6; P7; P8).
- [ ] Os casos C1 a C4 com o Observado e o veredito.
- [ ] O `feat/pln-009-mcp` integrado à `master` do `brza-workflow`, com a confirmação de Anderson.
- [ ] A R5.3 reaberta no PLN-003, e os P6 a P9 de lá passados a este plano.
