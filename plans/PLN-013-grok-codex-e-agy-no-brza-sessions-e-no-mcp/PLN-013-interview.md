# PLN-013 — Entrevista

> As rodadas do [PLN-013](PLN-013-plan.md). Só cresce: rodada nova vai ao fim.

### Rodada 1 — o destino, o corte, os outros runtimes e a medição (enviada 2026-11-03)

> **Apresentado antes:** o PLN-003/P12 é o roteador multiruntime do `brza sessions` (`--agent claude|codex|agy`) e não
> começou (`PLN-003-plan.md:217-228`); o PLN-009, em `review` e já mesclado, deixou "Outros runtimes (Codex, `agy`), o
> M4" fora de escopo, apontando para o P12. O `brza sessions` passa o `--agent` ao app sem lista e recusa o `--rename` e o
> `--wait` fora do Claude (`brza-workflow/packages/client/bin/brza-sessions:363-367`). O MCP fixa o Claude em
> `tools.py:25`, `accounts.py:24`, `cycle.py:22` e `limits.py:225`. O app conhece o Grok: o `worker-start` aceita o
> `--model` dele (`orca orchestration worker-start --help`), e ele tem contas (`GrokAccountsSection.tsx`) e cota
> (`src/main/rate-limits/grok-fetcher.ts`). A CLI do Grok tem `-p`, `--output-format`, `-s` e `-r` (`grok help`). O
> `grok login` não foi feito.

Respondida em 2026-11-03, nesta sessão.

1. **Onde mora o trabalho.** Opções:
   - um PLN novo, `high`, que absorve o PLN-003/P12 e o M4 do PLN-009, com o P12 virando `[-]` (recomendada) — custo:
     ~15 min; se paga: agora, porque o urgente não espera o P4 do PLN-003, e o PLN-009 fecha sem reabrir;
   - um passo no PLN-003/P12 — custo: ~5 min, com o urgente furando a ordem de um plano de 24 h restantes; se paga: só
     se o Grok for pequeno;
   - reabrir o PLN-009 — custo: adia o fechamento dele; se paga: nunca, além do que o PLN novo dá;
   - uma issue — custo: ~10 min, sem rodada para as lacunas; se paga: agora, se o corte for só o `brza sessions`.

   **Decidido — "PLN novo (Recomendado)".** O pedido de marcar o P12 vai ao `Retomar` do PLN-003.

2. **O que entra no corte urgente**, com seleção múltipla. Opções:
   - o `brza sessions` abre o Grok (recomendada) — custo: ~0,5 h, depois do `grok login`; se paga: na primeira sessão
     Grok aberta pelo `brza sessions`;
   - o MCP despacha ao Grok, na conta padrão e sem cota, como a PLN-009/R2.5 (recomendada) — custo: ~2,5 h; se paga: na
     primeira tarefa que a fila manda ao Grok;
   - a conta e a cota do Grok no MCP, pelo `GROK_HOME` e pela cota do app — custo: ~4 h; se paga: quando houver mais de
     uma conta Grok ou ele bater limite;
   - o `--rename` e o `--wait` no Grok — custo: ~2 a 3 h, com levantamento antes; se paga: quando a sessão Grok precisar
     ser achada pelo nome fora do mapa.

   **Decidido — as quatro:** "Sessions abre o grok (Recomendado), MCP despacha ao grok (Recomendado), Conta e cota do
   grok no MCP, --rename e --wait no grok". Somadas, ~9,5 h.

3. **O Codex e o Antigravity no MCP.** Opções:
   - uma tabela de runtimes com o Claude e o Grok, e os outros depois, com uma linha e um teste (recomendada) — custo:
     +~0,5 h; se paga: no segundo runtime além do Grok;
   - os três juntos, com teste e abertura real de cada um — custo: +~2 h; se paga: já, se houver despacho ao Codex ou ao
     `agy` pelo MCP nesta semana;
   - só o Grok, numa tupla fixa — custo: ~0 agora e uma refatoração no próximo runtime; se paga: nunca, se outro runtime
     vier.

   **Decidido — "Os três juntos".** Se isso vale também para a conta, a cota, o `--rename` e o `--wait`, vai à R2.

4. **A lacuna de medição do Grok.** Opções:
   - uma issue irmã, no formato da do Codex e do Antigravity (recomendada) — custo: ~10 min; se paga: agora, porque a
     issue antiga não muda de nome e o `move_note` não reescreve link no PLN-012;
   - na issue existente, renomeada pelo `move_note` — custo: ~10 min, com o link reescrito dentro do PLN-012, que outra
     sessão edita; se paga: quando as três lacunas forem resolvidas juntas.

   **Decidido — "Issue irmã (Recomendado)".**

### Rodada 2 — o alcance da conta, do `--rename` e a ordem das entregas (enviada 2026-11-03)

> **Apresentado antes:** a cota dos três runtimes já sai do app no formato das janelas do Claude — `orca account list
> --json` traz `rateLimits.grok`, `.codex` e `.antigravity`, com `session` e `weekly` (`usedPercent`, `windowMinutes`,
> `resetsAt`), e o Codex estava com a `session` em 97%. O app só lista contas do Claude e do Codex (chaves de topo
> `claude`, `codex`, `opencode`, `devin`; `inactiveCodexAccounts`); o Grok tem o `GROK_HOME` por conta no launch
> (`brza-studio/src/main/acp/acp-launch-specs.ts:163`), mas nenhuma lista. A "conta do Grok" da R1.2 é, hoje, a única.

Respondida em 2026-11-03, nesta sessão.

1. **Conta e cota no MCP para os três.** Opções:
   - a cota dos três pelo `rateLimits`, com troca de conta só no Claude e no Codex, os que o app lista; o Grok e o
     Antigravity na conta única (recomendada) — custo: ~3 h; se paga: hoje, porque o Codex a 97% faria o worker falhar
     sem freio;
   - a cota só do Grok, como a R1.2 literal, e o Codex e o `agy` como `quota_unknown` dentro do teto de sessões — custo:
     ~1,5 h; se paga: agora, com o Codex sem freio;
   - a recomendada mais várias contas Grok pelo `GROK_HOME`, com um passo no `brza-studio` para o `account list` as
     expor — custo: +~3 h e uma sessão no studio; se paga: quando houver uma segunda conta Grok, hoje nunca.

   **Decidido — "Cota dos 3, troca só Codex (Recomendado)".** Precisa a R1.2 no ponto da conta do Grok.

2. **O `--rename` e o `--wait` fora do Grok.** Opções:
   - só no Grok, como a R1.2, com o Codex e o `agy` recusados e uma issue para eles (recomendada) — custo: ~2,5 h; se
     paga: na primeira sessão Grok que outra sessão precisa achar pelo nome;
   - nos três, levantando onde o Codex e o `agy` gravam a sessão e o título — custo: +~3 h; se paga: quando forem
     abertos pelo nome com frequência; hoje, 1 abertura de cada desde 2026-10-29.

   **Decidido — "Nos três".** A E3 passa a ~5,5 h.

3. **A ordem das entregas.** Opções:
   - três entregas, cada uma com commit e usável — E1, o `brza sessions` abre o Grok e o MCP despacha aos três na conta
     padrão (~4,5 h); E2, a cota e a conta (~3 h); E3, o `--rename` e o `--wait` (~2,5 h) (recomendada) — custo: ~0,5 h a
     mais de testes de borda; se paga: a E1 serve no mesmo dia;
   - só o `brza sessions` primeiro (~0,5 h) e o MCP numa entrega única (~9,5 h) — custo: o despacho ao Grok espera ~1
     dia; se paga: hoje, se o urgente for abrir o Grok à mão;
   - uma entrega só, num merge (~10 h) — custo: nada usável antes do fim; se paga: só se as partes não servirem sozinhas.

   **Decidido — "Três entregas (Recomendado)".** Com a R2.2, a soma vai a ~13 h.

### Em aberto para o Desenho

Estrutura, para o Terreno responder com fonte; nenhum vai a Anderson antes de o código dizer. **→ respondidos no
Terreno**, e o que o código não resolveu foi à R3:

1. o `worker-start --agent` aceita `grok` — a ajuda lista `claude, codex, cursor, antigravity, muse, zcode, opencode`
   como exemplo, e o `--model` cita o Grok;
2. o que o `--rename` quer dizer em cada runtime: o título da sessão que o Grok acha com `-r`, e o equivalente no Codex
   e no Antigravity;
3. onde cada runtime grava a sessão, para o `--wait` saber que ela está no ar;
4. por onde o MCP troca a conta do Codex: o `accounts.switch_chat_account` usa o RPC do H3, medido só no Claude.

### Rodada 3 — o modelo, a cota por runtime, a troca do Codex e o `--rename` (enviada 2026-11-03)

> **Apresentado antes:** o Terreno, hoje em [PLN-013 — Desenho](PLN-013-design.md). O que mudou desde a R2: o Codex voltou a `session` 1% e não tem segunda
> conta no app (`inactiveCodexAccounts: []`), e o Antigravity está a `weekly` 99%. A sessão conferiu
> `worker-start-validation.ts:146-157`, `policy.py:210-215` e `limits.py:156`; a configuração de chat ou terminal por
> agente não está nos JSON do app, e a sonda dela vai ao primeiro subpasso da E1, sem rodada.

Respondida em 2026-11-03, nesta sessão.

1. **O modelo e o esforço dos workers fora do Claude.** Opções:
   - a política de papéis só no `claude`, e nos outros o `model` e o `effort` do pedido ou o padrão do runtime
     (recomendada) — custo: ~1 h na E1; se paga: no primeiro worker fora do Claude, que sem isso sai com `--model
     sonnet` e falha;
   - uma tabela `policy.roles.<papel>.<runtime>` no `brza.toml` — custo: ~2,5 h e a mudança no `brza.toml`; se paga:
     quando houver modelo por papel no Codex ou no Grok;
   - exigir `model` no pedido fora do Claude — custo: ~0,5 h; se paga: só se o padrão do runtime for ruim.

   **Decidido — "Tabela por runtime".** Os valores de cada papel em cada runtime vão a uma rodada do Desenho.

2. **A conta ativa e a cota por runtime.** Opções:
   - a conta ativa e o uso lidos por runtime, com o Grok e o Antigravity na conta única e a cota pelas janelas
     `session` e `weekly` de topo (recomendada) — custo: ~1,5 h na E2; se paga: já na E2, com o Antigravity a 99%
     retido até a cota renovar;
   - o mesmo, com o Antigravity pelos `buckets` do grupo do modelo — custo: +~1,5 h e um mapa de modelo para grupo; se
     paga: quando os grupos divergirem e o worker parado custar trabalho;
   - só a chave por runtime, sem ler a conta ativa fora do Claude — custo: ~0,5 h; se paga: se o Codex nunca tiver
     segunda conta, e a troca da R2.1 sai.

   **Decidido — "Por runtime, janelas de topo (Recomendado)".**

3. **A troca de conta do Codex.** Opções:
   - segurar o worker e devolver a proposta de troca pelo gate da sessão principal (PLN-003/R5.2), com o
     `accounts.selectCodex` só depois da aprovação, em código e teste, sem prova real (recomendada) — custo: ~1,5 h na E2;
     se paga: quando houver uma segunda conta Codex;
   - só segurar, sem trocar — custo: ~0 h; se paga: se a troca global for risco demais; desfaz a troca da R2.1;
   - trocar sem gate — custo: ~1 h; se paga: nunca, porque a troca global afeta os outros workers e os chats abertos.

   **Decidido — "Segura e propõe pelo gate (Recomendado)".**

4. **O que o `--rename` quer dizer fora do Claude.** Opções:
   - uma sonda de ~0,5 h antes da E3, mandando o `/rename` pelo `agentSession.send` nos três, com a E3 seguindo o que
     ela mostrar e o `--wait` pelo `providerSession.id` (recomendada) — custo: ~0,5 h e o `grok login`; se paga: na E3;
   - só o título da aba, pelo `agentSession.rename`, e o mapa — custo: ~0 h além do `--wait`; se paga: se o correio do
     Claude for o único consumidor do nome do runtime;
   - o Grok fora do `--rename` até o login — custo: parte da R2.2 espera; se paga: se o login demorar.

   **Decidido — "Sonda antes da E3 (Recomendado)".**

### Rodada 4 — os valores e o contrato do Desenho (enviada 2026-11-03, na mensagem)

> **Apresentado antes:** o rascunho do Desenho de um `designer`, com os itens D1 a D7 e os pontos P1 a P7, e o parecer
> da sessão Grok `pln-013-grok-revisor`, com 12 achados
> ([REV-010: O Desenho do PLN-013, revisado pela sessão Grok](../../work/reviews/REV-010-pln-013-o-desenho-pelo-grok.md)).
> Os achados entram no Desenho como correção, sem rodada, com a soma revista para E1 ~6,5 h, E2 ~4,5 h e E3 ~4 a 5,5 h.
> A tabela de modelo e esforço por papel foi mostrada lado a lado: o Claude de hoje, o Codex e o Antigravity do
> `designer`, e o Grok do `designer` e do revisor Grok.

Respondida em 2026-11-03, nesta sessão: "todos recomendados, siga".

1. **Os valores da tabela (P1).** Opções:
   - a coluna Codex e a do Antigravity do `designer`, e a coluna Grok do revisor Grok (recomendada) — custo: ~0 além da
     D2; se paga: no primeiro worker de cada papel. Caiu no ataque: não há medida do gasto do `gpt-6-astra`, e o
     architect do Grok cai para `high` se a sonda da E1 recusar o `xhigh`;
   - a coluna Grok do `designer` (`low`/`medium`/`high`) — custo: ~0; se paga: se o `medium` bastar ao executor, sem
     medida;
   - um modelo só por runtime, mudando o esforço — custo: ~0; se paga: se o `gpt-6-astra` gastar a cota rápido demais;
   - só a linha do Codex — custo: ~0, com o Grok em `high` em todo papel; se paga: até 2026-11-10 no Antigravity.

   **Decidido — a recomendada:**

   | Papel      | Claude            | Codex                  | Grok                | Antigravity             |
   | :--------- | :---------------- | :--------------------- | :------------------ | :---------------------- |
   | consultant | `sonnet`/`low`    | `gpt-6.1-sol`/`low`    | `grok-4.7`/`low`    | `gemini-4-argon-low`    |
   | executor   | `sonnet`/`medium` | `gpt-6.1-sol`/`medium` | `grok-4.7`/`high`   | `gemini-4-argon-medium` |
   | architect  | `opus`/`high`     | `gpt-6-astra`/`high`   | `grok-4.7`/`xhigh`  | `gemini-4-argon-high`   |

2. **A cota do Grok, que o app não lê nem com o login (P2).** Opções:
   - `quota_unknown` dentro do teto de sessões, com o `status` citando o `error` do `rateLimits.grok` e uma issue
     (recomendada pelos dois consultores) — custo: ~0,5 h na D4 e ~10 min da issue; se paga: agora. Caiu: a "cota dos
     3" da R2.1 não vale para o Grok enquanto o app não a ler;
   - um teto de sessões próprio para runtime sem leitura — custo: +~0,5 h e uma chave nova; se paga: quando um worker
     Grok falhar por limite.

   **Decidido — a recomendada.** Precisa a R2.1 no Grok; a issue é
   [O app não lê a cota do Grok](../../work/issues/o-app-nao-le-a-cota-do-grok.md).

3. **O id da sessão do runtime no mapa (P5).** Opções:
   - o `provider_session` nos quatro runtimes, com o `claude_session` só no Claude (recomendada, do revisor Grok) —
     custo: o da D6 e a linha no `session_map`; se paga: no primeiro `list --json` de uma sessão Grok com `--wait`;
   - o `runtime_session` só fora do Claude (do `designer`) — custo: ~0,25 h; se paga: nunca melhor que a primeira.

   **Decidido — a recomendada.**

4. **As convergências**, com seleção múltipla. Opções:
   - P3: a chave plana recusada, e os padrões em `policy.roles.<papel>.claude.*` (recomendada) — custo: ~0,25 h; se
     paga: agora, sem `brza.toml` em disco;
   - P6: com a sonda negativa, o `--rename` dá a aba e o mapa, o `--wait` vai pelo `providerSession.id`, sai um
     `CHECK`, e a issue só abre depois da sonda (recomendada) — custo: ~0 h; se paga: na E3;
   - P7: sem gate no ciclo, e o `status` do Codex retido diz que a troca só vem num `dispatch` novo (recomendada) —
     custo: ~0,5 h; se paga: na primeira cota cheia com pedido já na fila;
   - o alias `agy` no `dispatch` (recomendada pelo `designer`; o revisor Grok o tiraria) — custo: ~5 min; se paga:
     quando um chamador do MCP escrever `agy`.

   **Decidido — as quatro.**
