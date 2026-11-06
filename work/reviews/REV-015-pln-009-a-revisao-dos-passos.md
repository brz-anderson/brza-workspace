---
status: done
description: As revisões dos passos P1 a P6 do PLN-009 pelo agy e pelo Opus, até 3 rodadas por passo
scope:
  - workspace
opened: 2026-11-03
completed: 2026-11-03
tags:
  - tooling
---

# REV-015: os passos P1 a P6 do PLN-009, revisados pelo agy e pelo Opus

Os seis passos do [PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md),
revisados na versão `brza-workflow@b2c87a6`, o commit que fecha a correção da última rodada. O `agy` revisou com o Gemini
4 Argon (a r1 do P1) e com o Gemini 3.8 Flash (as demais rodadas), até o teto de 3 rodadas por passo; o subagente `reviewer`, da
camada alta (Opus), entrou duas vezes: na medição Flash × Opus da r1 do P2 ao P5 e na rodada final do P1 ao P6. Os
destinos saíram da regra de Anderson de 2026-11-03 ("escolha o encaminhamento dos achados sempre pela opção
`recomendada`"; "prefira sempre optar por `corrigir aqui`"): o que os pareceres deixaram como `issue` ou com rodada foi
corrigido aqui, e o `aceitar como X` foi para o texto do plano. Os commits da entrega são `1dfc9d9` (P1), `084cc62`
(P2), `e7d8fa6` (P3), `8801c77` (P4), `a4ff8db` (P5) e `1fa3e60` (P6); as correções saíram em `f8829f4` (r1 do P1),
`77b917f` (r1 e r2 dos demais) e `b2c87a6` (rodada final).

## Veredito

Os seis passos ficam em pé: os 53 achados importantes distintos (58 contando os que dois revisores acharam) têm destino `corrigido aqui`, e as
correções das rodadas r1 e r2 foram conferidas no código pela rodada final. O Flash das rodadas r2 e r3 aprovou o que o Opus da
rodada final ainda reprovou: 12 achados importantes sobreviveram a ele (1 no P1, 1 no P2, 2 no P3, 3 no P4, 4 no P5, 1
no P6). Dois deles são regressões de um conserto anterior (P3-A9 e P4-A11), e o P4-A9 mostra que o desempatador real
nunca autenticava. O `b2c87a6` não teve revisão própria depois dele. Nenhum revisor conferiu o contrato com o app real.

## P1 — O servidor residente e o ciclo de vida pelo launchd

| Rodada | Revisor | Reais (imp. / sug.) | Falsos | Destinos | Corrigido em |
| :----- | :------ | :------------------ | :----- | :------- | :----------- |
| r1 | Gemini 4 Argon (agy) | 5 / 1 | 2 | corrigido aqui | `f8829f4` |
| r2 | Gemini 3.8 Flash (agy) | 1 / 1 | 8 (6 deles, os da r1 reabertos já corrigidos) | corrigido aqui | `77b917f` |
| r3 | Gemini 3.8 Flash (agy) | 0 / 0 | 4 (2 reabertos já corrigidos) | — | — |
| final | Opus (`reviewer`) | 1 / 4 | 5 | corrigido aqui | `b2c87a6` |

### P1-A1 — O `claude-brza` e o `brza_claude` do shell não exportam o `BRZA_MCP_TOKEN`
> lacuna · importante · confiança 98 · → corrigido aqui (`f8829f4`)

**Evidência:** `claude-brza:67` monta o ambiente só com `BRZA_WORKSPACE`, e `brza.zsh:18` passa só `BRZA_WORKSPACE="$ws"`;
o `git diff c7a9e68 -- packages/client/` sai vazio. A R2.6 e a Cobertura do Pedido 1 (`PLN-009-plan.md:61,140`) exigem o
token.

### P1-A2 — Falta o `brza mcp url`, e a porta não é lida de `[mcp] port` do `brza.toml`
> lacuna · importante · confiança 98 · → corrigido aqui (`f8829f4`)

**Evidência:** `paths.py:41-43` faz só `int(os.environ.get('BRZA_MCP_PORT') or DEFAULT_PORT)`;
`brza-mcp url` → `error: argument cmd: invalid choice: 'url'`, `exit=2`. A R2.2 e o D1 pedem a chave e o comando
(`PLN-009-plan.md:166-167,182`).

### P1-A3 — O plist gerado não grava o `BRZA_WORKSPACE`
> lacuna · importante · confiança 96 · → corrigido aqui (`f8829f4`)

**Evidência:** `launchd.py:35-46` copia só `BRZA_HOME` e `BRZA_MCP_PORT`; o D5 diz que o workspace é gravado no plist
(`PLN-009-plan.md:282-283`). Sem ele, o servidor do launchd não acha o `brza.toml` nem o índice.

### P1-A4 — O pacote quebra no `import` sob o Python 3.9 e o `brza mcp start` não recusa a versão
> bug · importante · confiança 97 · → corrigido aqui (`f8829f4`)

**Evidência:** `/usr/bin/python3 packages/mcp/bin/brza-mcp --help` (3.9.6) aborta em `launchd.py:61` com
`TypeError: unsupported operand type(s) for |`; também em `launchd.py:72` e `registry.py:16`. Nenhum código confere
`sys.version_info < (3, 10)`, que o plano exige (`PLN-009-plan.md:84,171-172`).

### P1-A5 — O `DELETE /mcp` devolve `404`, e a sessão do Streamable HTTP não encerra (X7)
> desvio · importante · confiança 95 · → corrigido aqui (`f8829f4`)

**Evidência:** `server.py:82-83` entrega o `Mcp-Session-Id` no `initialize`, e `server.py:58-66` manda o `DELETE /mcp`
para o `else` com `404`. A especificação pede `200`/`204` ou `405`; o `404` faz o `terminateSession()` do cliente falhar.

### P1-A6 — O `brza mcp status` e o `health()` consultam a 4242 fixa quando rodam fora do workspace
> bug · importante · confiança 94 · → corrigido aqui (`77b917f`)

**Evidência:** `launchd.py:68` resolve a porta por `paths.default_port()`; sem `BRZA_WORKSPACE`, ela devolve 4242. Com
`[mcp] port = 5252`, o `status` imprime `carregado: sim`, `health: não responde` e sai `3`, com o serviço saudável.

### P1-A7 — Com o `brza.toml` ilegível, o `serve` do agente sai com erro e o launchd o reinicia em laço, contra o X36
> bug · importante · confiança 95 · → corrigido aqui (`b2c87a6`)

**Evidência:** `cli.py:113-114` → `paths.py:93-95` → `paths.py:84-85` levanta `SystemExit`; o plist roda o `serve` sem
`--port` (`launchd.py:46`) e tem `KeepAlive: {SuccessfulExit: False}` (`launchd.py:48`). Reproduzido com `"[policy"`
sem fechar: `exit=1`, e o `runtime/` nem é criado. O teste do X36 monta o serviço dentro do processo e passa.

## P2 — A fila por prioridade e os três tetos de workers

| Rodada | Revisor | Reais (imp. / sug.) | Falsos | Destinos | Corrigido em |
| :----- | :------ | :------------------ | :----- | :------- | :----------- |
| r1 | Gemini 3.8 Flash (agy) | 4 / 1 | 3 | corrigido aqui | `77b917f` |
| r1 | Opus (`reviewer`, medição) | 6 / 8 | 5 | corrigido aqui (2 eram `issue`, passaram a corrigidos) | `77b917f` |
| r2 | Gemini 3.8 Flash (agy) | 1 / 0 | 9 | corrigido aqui | `77b917f` |
| r3 | Gemini 3.8 Flash (agy) | 0 / 0 | 4 (1 reaberto já corrigido) | — | — |
| final | Opus (`reviewer`) | 1 / 4 | 5 | corrigido aqui (1 era `issue`) | `b2c87a6` |

### P2-A1 — O escolhido não é reservado, e o mesmo pedido é admitido duas vezes, passando do teto
> bug · importante · confiança 90 · → corrigido aqui (`77b917f`)

**Evidência:** `queue.py:136-149` devolve o escolhido sem mudar o estado, e `queue.py:151-160` (`mark_running`) não
confere `state = 'queued'`. Com `max_workers = 1` e dois pedidos: `dois next_admissible: 1 1` e
`running_count depois de mark_running duplo: 2`.

### P2-A2 — Os pedidos depois do escolhido ficam com `held_by` nulo, e o `status` mostra um pedido parado sem teto
> bug · importante · confiança 95 · → corrigido aqui (`77b917f`)

**Evidência:** `queue.py:141-148` avalia os seguintes como se o escolhido não ocupasse vaga e grava `held = (None, None)`
(Flash r1 A1 e Opus A2). O conserto da r1 foi incompleto e o Flash r2 reabriu: `[(1, None), (2, None), (3, None),
(4, None)]` com `max_workers = 2`; o `_admit` só abria virtualmente o primeiro.

### P2-A3 — O `blocks=[]` explícito é trocado pelo índice da `master`
> bug · importante · confiança 95 · → corrigido aqui (`77b917f`)

**Evidência:** `queue.py:108` (`not blocks`) e `queue.py:111` (`blocks if blocks else …`): a lista vazia, que declara "não
bloqueia", herda os `blocks` do plano e fura a fila, contra "o que veio no `dispatch` vence o índice".

### P2-A4 — O `running_count` zera o resultado quando recebe só `account` ou só `runtime`
> bug · importante · confiança 90 · → corrigido aqui (`77b917f`)

**Evidência:** `queue.py:174-176` usa `args += [account or '', runtime or '']` sempre juntos;
`running_count(account='a1')` vira `WHERE account = 'a1' AND runtime = ''` e conta 0 com workers de `claude` rodando.

### P2-A5 — O teste de outro reset passa com o filtro `resets_at` removido
> lacuna · importante · confiança 95 · → corrigido aqui (`77b917f`)

**Evidência:** `test_mcp_limits.py:153-161` usa 80% → 2%, de inclinação negativa; com o mutante `AND resets_at IS ?`
removido, o `next_admissible` ainda devolve 1. O teste só barra a mistura se a janela velha tiver o valor baixo.

### P2-A6 — A projeção entre duas amostras próximas amplifica o degrau do `usedPercent` inteiro e trava a conta por horas
> bug · importante · confiança 90 · → corrigido aqui (`77b917f`)

**Evidência:** `limits.py:158-168` tira a inclinação sem intervalo mínimo. Sondado: 10% → 11% em 30 s projeta 490, e 29%
→ 30% em 5 min na janela semanal projeta 1469, com a conta travada por 115 min.

### P2-A7 — O grupo de amostras por `resetsAt` exato se parte quando o provedor recalcula os milissegundos
> bug · importante · confiança 85 · → corrigido aqui (`77b917f`)

**Evidência:** `queue.py:193-198` filtra `resets_at IS ?`. A janela `session` tem `resetsAt` `…586` na fixture e `…303` no
`orca account list --json` real; cada mudança zera a base da projeção. Premissa: o valor muda a cada atualização do
provedor.

### P2-A8 — A conta sem dado de uso e sem `max_sessions_per_account` admite sem limite, contra a R2.5
> desvio · importante · confiança 85 · → corrigido aqui (`77b917f`)

**Evidência:** `limits.py:120-133` só segura com `cap is not None`; com config `{}` e `usage` nulo, 10 pedidos saem
`admitidos sem dado e sem chaves: 10 quota_unknown`. A R2.5 pede admitir "só dentro" do teto (`PLN-009-plan.md:136-138`).

### P2-A9 — O uso vem por runtime, só da conta ativa, e a projeção "por conta" só existe para ela (X6 muda o D2)
> desvio · importante · confiança 90 · → corrigido aqui (`77b917f`), no `accounts.py` do P5 (era `issue`)

**Evidência:** o `orca account list --json` real devolve `result.rateLimits.claude`, um objeto só por runtime, e as
contas à parte; para as outras, o `account_quota` cai em `quota_unknown`. O D2 promete que a conta que chega a 90 antes
do reset não recebe worker (`PLN-009-plan.md:214-216`).

### P2-A10 — Uma exceção na passada, depois do escolhido, deixa o pedido `running` sem sessão até o daemon reiniciar
> bug · importante · confiança 82 · → corrigido aqui (`b2c87a6`)

**Evidência:** `queue.py:184-196`: o `_admit` abre o escolhido e segue julgando; o `finally` libera só os virtuais. Com um
`Limits` que levanta no 2º pedido: `estado de a: running | running_count: 1 | orphan_workers: [1]`.

## P3 — As ferramentas `dispatch`, `status` e `config`, com os gates

| Rodada | Revisor | Reais (imp. / sug.) | Falsos | Destinos | Corrigido em |
| :----- | :------ | :------------------ | :----- | :------- | :----------- |
| r1 | Gemini 3.8 Flash (agy) | 3 / 1 | 5 | corrigido aqui | `77b917f` |
| r1 | Opus (`reviewer`, medição) | 6 / 6 | 5 | corrigido aqui | `77b917f` |
| r2 | Gemini 3.8 Flash (agy) | 0 / 0 | 16 (14 reabertos já corrigidos) | — | — |
| final | Opus (`reviewer`) | 2 / 3 | 3 | corrigido aqui | `b2c87a6` |

### P3-A1 — Duas aprovações simultâneas do mesmo gate passam, e a segunda pode devolver à fila um pedido que já corre
> bug · importante · confiança 92 · → corrigido aqui (`77b917f`)

**Evidência:** `tools.py:170-178` confere `approved_at`/`state` fora do `with self.queue.lock` (que começa na linha 179),
e o `set_state(..., 'queued')` (`queue.py:126-129`) grava sem condição. `repro1.py`: `duas aprovacoes simultaneas:
[False, False]`; `repro4.py`: `antes da 2a: running`, depois o pedido volta a `queued`.

### P3-A2 — O pedido `gated` e o registro do gate nascem em duas operações, e a queda entre elas deixa um órfão
> bug · importante · confiança 95 · → corrigido aqui (`77b917f`)

**Evidência:** `tools.py:150-153` faz o `enqueue(state='gated')` e só depois o `INSERT INTO gates`, com o lock solto
entre os dois; o pedido fica `gated` sem gate e sem como aprovar.

### P3-A3 — O `status` omite o `gate_id` e o `reason` dos pedidos `gated`
> lacuna · importante · confiança 95 · → corrigido aqui (`77b917f`); o conserto abriu o P3-A9

**Evidência:** `tools.py:203-214` lista os `gated` só pela tabela `requests`; o `gate_id` mora em `gates`, e o
`dispatch(approved=…)` exige o `gate_id` e recusa o id do pedido.

### P3-A4 — O pedido sem `runtime` escapa do teto de sessões por conta e runtime
> bug · importante · confiança 95 · → corrigido aqui (`77b917f`)

**Evidência:** `tools.py:145-146` grava `runtime` só quando vem; o worker nasce com `''` (`queue.py:159`) e o
`running_count` conta `''` e `'claude'` em separado. Com o teto 1 e um worker `claude`: o pedido com `runtime` sai
`held_by: account_sessions` e o igual sem `runtime`, `held_by: None`.

### P3-A5 — O servidor que o launchd sobe nunca lê o índice da `master`, porque o plist não leva o `BRZA_WORKSPACE`
> bug · importante · confiança 88 · → corrigido aqui (`77b917f`)

**Evidência:** `tools.py:93` e `tools.py:106-108` deixam o `_index` vazio sem a variável; `launchd.py:36-39` só passa
`BRZA_HOME` e `BRZA_MCP_PORT`. O `serve` por subprocesso gravou o `dispatch` com `ref: "PLN-009"` e `priority: None`, sem
erro. Premissa: o servidor de produção é o do `brza mcp start`.

### P3-A6 — Um `deadline` fora de AAAA-MM-DD é aceito no Python 3.11 ou mais e vai para o fim da fila
> bug · importante · confiança 95 · → corrigido aqui (`77b917f`)

**Evidência:** `tools.py:127-131` valida com `date.fromisoformat`, que no 3.11+ aceita `20261105` e `2026-W46-1`, e a
ordem compara texto (`queue.py:71`). No Python 3.15.2: `[('tarde', 1), ('semana', 2), ('cedo-compacto', 3)]`, com o
prazo mais próximo por último.

### P3-A7 — O `config` aceita chave com erro de digitação abaixo de `quota.`, `machine.` e `resolver.` e responde como se tivesse gravado
> desvio · importante · confiança 95 · → corrigido aqui (`77b917f`)

**Evidência:** `tools.py:65-66` aceita qualquer chave que comece por um dos `_PREFIXES`;
`quota.hard_cap_percnt` e `resolver.tev1_min_confidance` voltam `isError: False` com eco da chave, e nada as lê.

### P3-A8 — Nenhum teste falha quando o `serve` deixa de instalar as ferramentas
> lacuna · importante · confiança 95 · → corrigido aqui (`77b917f`)

**Evidência:** mutante numa cópia: apagar `tools.install(REGISTRY)` em `cli.py:15` → `Ran 120 tests … OK`. Os testes do
P3 usam o registro do `ToolsCase` (`tools_support.py:24`), e o `ProcessTest` (`test_mcp_lifecycle.py:326-353`) confere só o
`/health`.

### P3-A9 — O `status` entrega o `gate_id` de todo pedido `gated` a qualquer chamador, e com ele outra sessão aprova o gate
> bug · importante · confiança 92 · → corrigido aqui (`b2c87a6`)

**Evidência:** o encaminhamento do P3-A3 dizia "vale para o `status` do próprio chamador", mas `tools.py:327-329` junta
`gates` a todo `gated` sem filtro, e `tools.py:334,339-340` devolvem `caller`, `task`, `role` e `gate_id`. O `approve` só
confere o chamador gravado (`tools.py:270`), que sai do argumento `caller` quando falta o header (`tools.py:209`).
`repro_gate.py`, caso 1: a sessão `worker-x` vê o `gate_id` e aprova.

### P3-A10 — Em produção, o gate de conta só dispara quando não há troca, e a troca real é recusada
> desvio · importante · confiança 92 · → corrigido aqui (`b2c87a6`), pela recomendada: aceitar o X38; o texto do plano a sessão ajusta

**Evidência:** `cli.py:24,27` sempre passa um `Accounts()`; `tools.py:170-173` recusa a conta que não é a ativa, e
`tools.py:259-260` abre gate para qualquer `account` presente. `repro_gate.py`, caso 2: sem `account` entra direto; com
`adm`, o rótulo da conta ativa, abre gate de "troca" que não troca; com `pessoal`, a troca real, vem `isError`.

## P4 — A política do `brza.toml` e o desempatador `tev1` + Haiku

| Rodada | Revisor | Reais (imp. / sug.) | Falsos | Destinos | Corrigido em |
| :----- | :------ | :------------------ | :----- | :------- | :----------- |
| r1 | Gemini 3.8 Flash (agy) | 2 / 1 | 2 | corrigido aqui; 7 desvios julgados | `77b917f` |
| r1 | Opus (`reviewer`, medição) | 7 / 5 | 4 | corrigido aqui (2 eram `issue`); 4 `aceitar como X` | `77b917f` |
| r2 | Gemini 3.8 Flash (agy) | 0 / 1 | 2 | corrigido aqui | `77b917f` |
| final | Opus (`reviewer`) | 3 / 4 | 4 | corrigido aqui | `b2c87a6` |

### P4-A1 — A proposta do gate lê os argumentos originais e contradiz o modelo e o esforço que a política decidiu
> bug · importante · confiança 95 · → corrigido aqui (`77b917f`)

**Evidência:** `tools.py:152-153` grava o modelo da política, e `tools.py:161-162` monta a proposta de `args`. Sondado:
`dispatch {"role": "executor", "model": "haiku", "effort": "low"}` → proposta `haiku/low`, gravado `sonnet/medium`; o
`approved` roda com `sonnet/medium`. Anderson aprova o gate sem ver o modelo nem o custo.

### P4-A2 — O `choose_account` quebra com `ValueError` quando uma conta candidata tem a lista de janelas vazia
> bug · importante · confiança 95 · → corrigido aqui (`77b917f`)

**Evidência:** `resolver.py:125` faz `max(windows)`; `choose_account({'conta-a': [50], 'conta-nova': []})` →
`ValueError: max() arg is an empty sequence`, caso da conta recém-adicionada sem amostragem.

### P4-A3 — Um `brza.toml` quebrado derruba o `serve` na subida, e o launchd o reinicia em laço
> bug · importante · confiança 95 · → corrigido aqui (`77b917f`)

**Evidência:** `cli.py:16` chama `tools.install(REGISTRY)` fora de `try`; o `Orchestrator.__init__` chama
`sync_limits()` (`tools.py:102,109`) e o `policy.load` levanta `PolicyError` (`policy.py:105-106`). Com `[policy` sem
fechar: traceback, `exit=1`; o X6 só vale depois que o servidor sobe.

### P4-A4 — O `config` grava a sobreposição e responde `isError` quando o `brza.toml` está quebrado
> bug · importante · confiança 95 · → corrigido aqui (`77b917f`)

**Evidência:** `tools.py:241-249` faz o `DELETE`/`INSERT` antes do `sync_limits()`, que levanta. Servidor de pé e arquivo
quebrado: `config {"key": "policy.enforce", "value": false}` → `isError: True`, e `get_overrides()` →
`{'policy.enforce': False}`; a imposição foi desligada mesmo com o erro.

### P4-A5 — Com os padrões do P4, o teto de sessões conta `runtime` ausente e `"claude"` como contas diferentes
> bug · importante · confiança 90 · → corrigido aqui (`77b917f`)

**Evidência:** `policy.py:31` põe `max_sessions_per_account = 2` por baixo (`tools.py:109`); `limits.py:126` agrupa por
`runtime or ''`, e o `dispatch` não preenche o `runtime` (`tools.py:150-151`). Em `e7d8fa6`, 4 consultores sem
`runtime` rodavam todos; em `8801c77`, 2 rodam e 2 ficam em `account_sessions`.

### P4-A6 — Os testes da regra de conta (X3) passam sem a regra de empate e sem o limite exato do teto
> lacuna · importante · confiança 95 · → corrigido aqui (`77b917f`)

**Evidência:** no caso A3 da fixture (`m11_cases.json:88-102`) "menor uso" e "ordem alfabética" dão a mesma resposta.
Mutantes `u - best <= 0` (`resolver.py:130`) e `min(open_, key=open_.get)`: `test_mcp_resolver.py` → `OK`. Nenhum caso
tem janela em exatamente 90 nem diferença de exatamente 5, onde o `tev1` errava (`m11-worklog.md:33-34`).

### P4-A7 — O desempatador não é instanciado em lugar nenhum, e o X7 não tem dono no plano
> desvio · importante · confiança 90 · → corrigido aqui (`77b917f`)

**Evidência:** `git grep -n "Resolver(" 944fa27 -- packages` só acha a docstring (`resolver.py:4`); o `serve` chama
`tools.install(REGISTRY)` sem `resolver` (`cli.py:16`), e o `Orchestrator` guarda `resolver=None` (`tools.py:97`). O
`decide_model` nunca chega ao `tev1` nem ao Haiku.

### P4-A8 — A sugestão à principal é sempre a linha do `architect` (opus/high), contra o motivo da R6.4
> desvio · importante · confiança 85 · → corrigido aqui (`77b917f`), pela recomendada: `suggest_to_main` nasce `false` (era `issue` com rodada)

**Evidência:** `policy.py:154-163` devolve sempre `role_row('architect')`. A R6.4 do PLN-003 só paga "quando a medição
mostrar a principal cara em tarefa mecânica" (`PLN-003-interview.md:303-309`); o X5 faz todo `status` sugerir o modelo mais caro.

### P4-A9 — O Haiku do desempate não autentica: o `claude_env` do `resolver` tira o `USER`, e todo desempate cai no `fallback`
> bug · importante · confiança 95 · → corrigido aqui (`b2c87a6`)

**Evidência:** `resolver.py:59` monta o ambiente só com `HOME`, `PATH` e `LANG`, e `test_mcp_resolver.py:127-128` fixa
`set(env) <= {'HOME', 'PATH', 'LANG'}`. A sonda do H2 rodou com `USER` e `LOGNAME`
(`2026-11-03-pln-003-medicao-das-hipoteses-p0.md:37`). O `claude` 2.1.317 real, com o ambiente mínimo, sai `rc 1`
duas vezes.

### P4-A10 — O `brza.toml` não confere chave nem tipo: a chave com erro de digitação some, e o texto num teto quebra o `dispatch` depois de enfileirar
> bug · importante · confiança 95 · → corrigido aqui (`b2c87a6`)

**Evidência:** `policy.py:97-107` funde o `flatten` sem conferir, enquanto o `config` recusa as mesmas entradas
(`tools.py:41-56,88-104`; X35). `[orchestrator] max_worker = 1` deixa o efetivo em 6 sem erro; `max_workers = "1"` faz o
`dispatch` responder `TypeError: '>=' not supported`; `enforce = "false"` impõe.

### P4-A11 — Com o servidor de pé, o `brza.toml` que quebra afrouxa os tetos para os padrões, sem log; o `policy_error` ninguém lê
> bug · importante · confiança 92 · → corrigido aqui (`b2c87a6`), pela recomendada: o servidor mantém a última configuração lida e escreve o erro no stderr; na subida, sem anterior, os padrões (X36)

**Evidência:** `runtime_break.py`: `antes: 1 1` → `depois do arquivo quebrado: 6 2`, com a saída do `sync_limits` vazia
(`cli.py:30`, `cycle.py:194-195`). `grep -rn policy_error packages tests` só acha as gravações (`tools.py:123,139,141`).

## P5 — O ciclo do worker pelo `orchestration` e a conta por chamada

| Rodada | Revisor | Reais (imp. / sug.) | Falsos | Destinos | Corrigido em |
| :----- | :------ | :------------------ | :----- | :------- | :----------- |
| r1 | Gemini 3.8 Flash (agy) | 3 / 2 | 3 | corrigido aqui; 8 desvios julgados | `77b917f` |
| r1 | Opus (`reviewer`, medição) | 7 / 5 | 3 | corrigido aqui; 2 `aceitar como X` | `77b917f` |
| r2 | Gemini 3.8 Flash (agy) | 0 / 0 (12 correções conferidas) | 3 | — | — |
| final | Opus (`reviewer`) | 4 / 3 | 4 | corrigido aqui (1 era `issue`) | `b2c87a6` |

### P5-A1 — A conta pedida e aprovada no gate não chega ao worker, e o teto a conta na conta pedida
> bug · importante · confiança 95 · → corrigido aqui (`77b917f`)

**Evidência:** `grep -rn "claude_env\|switch_chat_account" packages/ bin/` acha só as definições (`accounts.py:129,166`);
`cycle.py:133-138` monta o `worker-start` sem a conta, e o `worker-start --help` não tem flag de conta. O `dispatch` com
`account: "<ADM>"` abre o gate, Anderson aprova, e o worker abre na conta ativa.

### P5-A2 — O cliente `orca` não abre sob o launchd: o CLI é o nome `orca`, que o PATH do agente não acha
> bug · importante · confiança 92 · → corrigido aqui (`77b917f`)

**Evidência:** `clients.py:14` usa `'cli': 'orca'`; o PATH do plist (`launchd.py:29-32`) não o tem: `env -i PATH="…" which
orca` → exit 1; o binário está em `/Applications/Orca.app/Contents/Resources/bin/orca`. O `FileNotFoundError` vira
`CycleError` (`cycle.py:39-40`) e o pedido `failed`, e não `NoClient`.

### P5-A3 — O fim e o erro do pedido não voltam ao chamador: o `status` só lista `queued`, `gated` e `running`
> lacuna · importante · confiança 92 · → corrigido aqui (`77b917f`)

**Evidência:** `tools.py:212-229` devolve só `queued`, `gated`, `running`, `ceilings` e `suggestion`; o motivo da falha
fica em `Scheduler.errors` (`cycle.py:89,170,173`), um dicionário em memória que ferramenta nenhuma expõe. O D6 (M14)
diz que o `status` do chamador o mostra.

### P5-A4 — Os tetos por conta contam a mesma conta sob chaves diferentes: id, e-mail, rótulo, `''` e runtime ausente
> bug · importante · confiança 90 · → corrigido aqui (`77b917f`)

**Evidência:** `norm.py` com a ADM ativa e `max_sessions_per_account = 1`: `abertos com max_sessions_per_account=1, os tres
na mesma conta ADM: [1, 2, 3]`, e as amostras em três séries. O apelido só se resolve no provedor de uso
(`accounts.py:110-126`); `Limits._sessions`/`_quota` (`limits.py:126-147`) e `mark_running` usam o texto cru.

### P5-A5 — A falha no meio do `open` deixa run, task e terminal órfãos, e o `outcome_unknown` libera o teto com o worker talvez vivo
> bug · importante · confiança 88 · → corrigido aqui (`77b917f`)

**Evidência:** `cycle.py:121-140` cria run e task antes do `worker-start` e só grava o estado depois (`cycle.py:177`);
qualquer `CycleError` marca `failed` sem desfazer (`cycle.py:172-176`). Premissa: o recibo do `brza-studio`
(`worker-start-agent-view.ts:88-103`; `agent-view.test.ts:82-100`) deixa `residualResources: terminal` e manda rodar o
`worker-release`.

### P5-A6 — Os testes não falham com os defeitos que dizem cobrir: o `serve` sem o ciclo, o `kick` que não acorda, a migração e a projeção
> lacuna · importante · confiança 95 · → corrigido aqui (`77b917f`)

**Evidência:** mutantes numa cópia, com `tests/mcp` seguindo `OK`: `cli.py:44` sem o `scheduler.start()`;
`cycle.py:204` com `stop_event.wait` no lugar de `wake.wait`; `queue.py:86` sem o `ALTER TABLE` (X3); `accounts.py:221`
com `projected = usedPercent`.

### P5-A7 — O `X-Brza-Client` é contrato novo com o PLN-003/P4, sem desvio registrado e sem fonte para o valor
> desvio · importante · confiança 85 · → corrigido aqui (`77b917f`)

**Evidência:** `tools.py:156-158` aceita só `studio` ou `orca`, e o D3 e o H1 só têm `X-Brza-Session` e `Authorization`.
Premissa: o `.mcp.json` é um só para os dois apps, com valores por `${VAR}`; nenhuma variável vale `studio` ou `orca`.
Sem o header, `clients.py:19-24` escolhe o Studio quando os dois rodam. O conserto: o header leva `${ORCA_USER_DATA_PATH}`.

### P5-A8 — Uma `task` vazia ou só de espaços derruba o `open` com `IndexError` e trava a fila
> bug · importante · confiança 95 · → corrigido aqui (`77b917f`)

**Evidência:** `cycle.py:128` faz `request['task'].strip().splitlines()[0][:80]`; com `""`, `.splitlines()` é `[]`. O
`tick` só captura `(NoClient, CycleError)`, o `IndexError` chega ao `_loop` e o pedido segue `queued`, relido a cada 15 s.

### P5-A9 — O `brza quota` ignora o `quota.hard_cap_percent` do `brza.toml` e do `config`: o teto mostrado é sempre 90
> bug · importante · confiança 92 · → corrigido aqui (`77b917f`)

**Evidência:** `brza-quota:47` instancia `limits.Limits()` com `config={}`, e `accounts.py:211` cai no 90.0 fixo
(Flash r1 A3 e Opus A9).

### P5-A10 — O `worker-start` com `outcome_unknown` real é abandonado: libera o worker, falha a task e o pedido
> bug · importante · confiança 92 · → corrigido aqui (`b2c87a6`)

**Evidência:** `cycle.py:121-126` tira o `code` de `body['error']` e `cycle.py:156` compara com `start_outcome_unknown`; no
app, o `worker-start` responde sucesso com `result.state = 'outcome_unknown'` e sem `error`
(`brza-studio/src/cli/handlers/orchestration/agent-view.ts:38,57,73-75`; `worker-start-agent-view.ts:101`). O código só
sai no stderr, e o app instalado é igual.

### P5-A11 — O app fechado por 45 s falha todo pedido em curso como "o worker sumiu do cliente"
> bug · importante · confiança 95 · → corrigido aqui (`b2c87a6`)

**Evidência:** `cycle.py:253-254` dá o worker por perdido em qualquer `CycleError` com `body`, contra a docstring
(`cycle.py:245-246`). `worker-show --json` com o app parado → `{"ok":false,"error":{"code":"runtime_unavailable"}}`,
`exit=1`; a simulação: `0 running`, `1 running`, `2 failed o worker sumiu do cliente`.

### P5-A12 — O pedido `running` sem `dispatch`, com a task em `ready`, fica `running` para sempre e prende a vaga
> bug · importante · confiança 85 · → corrigido aqui (`b2c87a6`), pela recomendada: só a recuperação, sem ferramenta `cancel`

**Evidência:** o `save` grava `{'dispatch': None}` antes do `worker-start` (`cycle.py:144-146`); o `orphan_workers` só olha
`session IS NULL` (`queue.py:229-232`), o `poll` só fecha com `completed`/`failed` (`cycle.py:180-184`) e o `_gone` sem
`dispatch` devolve False (`cycle.py:247-249`). `stuck.py`: `running queued workspace 1`, com o seguinte preso.

### P5-A13 — O `X-Brza-Client` com o `ORCA_USER_DATA_PATH` de um perfil que não é o padrão perde o caminho, e o worker abre no app errado
> desvio · importante · confiança 85 · → corrigido aqui (`b2c87a6`)

**Evidência:** `clients.py:29-37` converte o caminho só para `brza-studio` e `orca`, e `cycle.py:111` usa o caminho fixo do
`CLIENTS`. Existem `brza-dev` e `brza-dev-wt` com `orca-runtime.json` próprio; um chat do build de desenvolvimento cai no
Studio de produção.

## P6 — A linha `route` no `measurements.jsonl` e a ponta a ponta

| Rodada | Revisor | Reais (imp. / sug.) | Falsos | Destinos | Corrigido em |
| :----- | :------ | :------------------ | :----- | :------- | :----------- |
| r1 | Gemini 3.8 Flash (agy) | 1 / 1 | 6 | corrigido aqui; 5 desvios `aceitos como X` | `77b917f` |
| r2 | Gemini 3.8 Flash (agy) | 0 / 0 | 8 (2 reabertos já corrigidos) | — | — |
| final | Opus (`reviewer`) | 1 / 2 | 3 | corrigido aqui (o texto, a sessão) | `b2c87a6` |

### P6-A1 — O `Telemetry.workstream()` levanta `TypeError` quando o `workspace` é `None`
> bug · importante · confiança 95 · → corrigido aqui (`77b917f`)

**Evidência:** `telemetry.py:66` passa `self.workspace` (`None`) ao `subprocess.run(['git', '-C', …])`, e o `TypeError` não
é capturado por `(OSError, subprocess.SubprocessError)`. Ocorre sem `BRZA_WORKSPACE` e nos dublês de teste
(`tools_support.py:25`, `test_mcp_gates.py:83`).

### P6-A2 — A linha `admitted` registra uma admissão que não aconteceu e, sem client, inunda o log com `held` e `admitted` a cada volta do ciclo
> bug · importante · confiança 95 · → corrigido aqui (`b2c87a6`)

**Evidência:** `queue.py:179-181` dispara o `on_decision` em toda passada, também na prévia sem reserva
(`next_admissible`, `reserve=False`) que `tools.py:303` (`queued()`) e `tools.py:325` (`status`) chamam; `telemetry.py:119-125`
grava `admitted` embora o `_admit` libere o escolhido (`queue.py:195-196`). No `NoClient`, o `Scheduler.tick`
(`cycle.py:196-208`) faz `release` e repete a passada.

## Sugestões e falsos

Contagens brutas por passo, somando as rodadas e os revisores, antes de unir o mesmo defeito achado por dois:

| Passo | Importantes | Sugestões | Falsos | `aceitar como X` |
| :---- | :---------- | :-------- | :----- | :--------------- |
| P1 | 7 | 6 | 19 | 0 |
| P2 | 12 | 13 | 26 | 0 |
| P3 | 11 | 10 | 29 | 0 |
| P4 | 12 | 11 | 12 | 4 |
| P5 | 14 | 10 | 13 | 2 |
| P6 | 2 | 3 | 17 | 5 |

Os `falso` incluem os "falso (no estado atual)": achado de rodada anterior que o revisor reabriu e que o código já tinha
corrigido. As sugestões que tinham destino `issue` (P2 A5 do final, P5 A5 do final) passaram a `corrigido aqui`. Os pareceres
completos ficaram no scratch da sessão, em `/private/tmp/pln009/`.

## Fora do alcance desta revisão

Nenhum revisor pôde conferir, sem rodar o app, o que depende dele:
- o `--json` real do `orchestration` (`run-create`, `task-create`, `worker-start`, `task-list`, `worker-show`): o P5 o lê
  por `find_key` em qualquer profundidade (X5), e o P5-A10 e o P5-A11 dependem do formato do app;
- o `launchd` real: o plist, o `KeepAlive` e o PATH do agente só se provaram em subprocesso e com `launchctl` falso;
- o `tev1` frio: o teste do `tev1` real é pulado sem o modelo, e o P4-A9 mostra que o Haiku real nunca autenticou;
- o `account list` real de cada app: a fixture ganhou o envelope, mas o miolo é montado, e o uso por conta depende do
  formato de `inactiveClaudeAccounts`, tirado do código do `brza-studio`;
- a troca de conta: o `worker-start` não tem flag de conta, e o P3-A10 aceita a recusa da troca real (X38).
