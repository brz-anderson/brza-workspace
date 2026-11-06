---
status: done
description: A revisão independente da entrega do PLN-009 contra o Pedido e a Cobertura, com os achados e o delta do P8
completed: 2026-11-03
scope:
  - workspace
opened: 2026-11-03
---

# REV-016: a entrega do PLN-009 contra o Pedido e a Cobertura

Revisão independente do `brza-workflow@b2c87a6`, branch `feat/pln-009-mcp`, contra o
[PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md).

### A1 — A conta explícita envelhece na fila e o worker pode abrir com a cota de outra conta

> bug · importante · confiança 99 · → corrigido aqui (`354d004`)

**Evidência:** `packages/mcp/brza_mcp/tools.py:140-156` confere a conta na entrada;
`limits.py:160-181` consulta a conta explícita sem reconferir a ativa; `cycle.py:140-158` abre sem flag de conta.
Com `Queue` em memória, conta ativa B a 99%, conta pedida A a 1% e `Scheduler` com `FakeCli`,
`tick()` devolveu `[1]` e chamou `worker-start`. O worker abre na B, avaliado pela cota da A.

### A2 — O perfil de desenvolvimento consulta as contas da produção

> bug · importante · confiança 99 · → corrigido aqui (`354d004`)

**Evidência:** `accounts.py:109-116` usa `CLIENTS[name]['user_data']`, enquanto `cycle.py:111-112` usa o
`user_data` do pedido. Uma pasta temporária com `orca-runtime.json` foi preservada no ambiente do worker,
mas o runner falso de `Accounts` recebeu a pasta `brza-studio` de produção. A consulta e o cache precisam
preservar o perfil em todas as leituras, inclusive no gate e nos tetos (X42).

### A3 — O checklist de fechamento omite C4

> lacuna · sugestão · confiança 100 · → corrigido aqui (checklist do plano)

**Evidência:** o plano define C4 em `### Casos manuais`, para comprovar o ciclo real e X24/X39,
mas o `## Fechamento` exige somente C1 a C3. Incluir C4, mantendo-o pendente até a execução real.

## Verificação

No `b2c87a6`: MCP 346 testes, OK, um pulado; hooks 290 OK; CLI em ambiente limpo 445 OK.
Comandos: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/mcp` e o mesmo comando
para `tests/hooks`; CLI com `env -i HOME="$HOME" PATH="$PATH" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/cli`.
O MCP passou após liberar a leitura de `sysctl` negada pelo sandbox; o teste pulado é o `tev1` real.

Toda linha da Cobertura tem teste automatizado correspondente: autenticação, instalação/token, despacho,
fila, tetos, política, telemetria, desempate e gates. O ciclo e a conta têm as lacunas A1/A2.
C1, C2, C3 e C4 continuam sem veredito real. O índice da `master` já contém 15 IDs com `priority`,
sem registros atuais com `blocks` ou `deadline`; o C3 não foi provado, e o PLN-003/P1 ainda consta pendente.
Nenhum worker real, modelo externo, LaunchAgent ou merge foi acionado nesta revisão.

## Revisão da correção

No P7, `brza-workflow@354d004`, três regressões falharam antes e passaram depois. O revisor independente
aprovou o delta, com 63 testes pontuais OK; o gate final no worktree real deu 349 testes MCP, OK (um pulado).
A conta explícita divergente fica retida; a conta resolvida fica no worker; conta e cache usam o perfil correto.
A3 foi corrigido no checklist. Todos os achados têm destino; os casos manuais seguem pendentes.
O cache de contas continua com TTL de 30 s e o CLI não oferece transação de conta com o app: a correção não
prova ausência de troca externa entre a leitura e a abertura. Esse limite permanece para avaliação no C4.

### P8 — O `stop` que apaga o plist

O C1 no launchd real achou o plist com `RunAtLoad` depois do `stop` (PLN-009/R7.1). O P8 o corrigiu, e a correção
foi revisada em duas rodadas, sobre o diff sem commit em cima do `354d004`.

**r1, em paralelo:**
- **O `agy` (`gemini-3.8-flash-high`):** 6 achados.
- **O `reviewer` (Opus):** 4 achados e 1 ponto para rodada.
- **Destinos,** pela recomendada:
  - **O teste do `start` depois do `stop`** passava com o `start` saindo 1 e levava 15 s (Flash 1, Opus A2). →
    corrigido aqui.
  - **O `bootout` que falha com o agente já fora** deixava o plist (Flash 2, ponto do Opus). Agora conta como
    descarregado; com o agente carregado, o plist fica. → corrigido aqui.
  - **O teste do CLI com plist órfão** chamava o `launchd.stop()` antes (Flash 3). → corrigido aqui.
  - **O `stop` sem `timeout` e o prazo de 5 s,** abaixo do `join(5.0)` do scheduler e do `ExitTimeOut` de 20 s do
    launchd (Flash 4 e 6, Opus A1). Agora `stop(timeout=25)` e `--timeout`. → corrigido aqui.
  - **A ajuda e a mensagem do `stop`** não falavam do plist (Opus A4). → corrigido aqui.
  - **A corrida entre `start` e `stop` concorrentes** (Flash 5, Opus A3). → issue
    [O start e o stop do MCP concorrentes](../issues/o-start-e-o-stop-do-mcp-concorrentes.md).

**r2 pelo `agy` (Flash):** sem achado.
- Os 5 achados corrigidos aqui foram conferidos.
- Dos 3 testes novos, 1 falha no código da r1. Os outros 2 barram as mutações M1 e M2 do código novo.

**Gate:**
- `tests/mcp` → 358 OK, um pulado.
- `tests/cli` limpo → 445 OK.
- `test_mcp_lifecycle` em 8 s.

**Commit:** `brza-workflow@007383a`. O C1 refeito com ele foi aprovado.
