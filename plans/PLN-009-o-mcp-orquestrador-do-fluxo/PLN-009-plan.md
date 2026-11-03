---
status: open
phase: design
origin: plan
origin_ref: PLN-003
description: O servidor MCP residente gerencia o fluxo com fila de prioridade sob três tetos, política declarativa e desempate com tev1 e Haiku
ready: não — aguarda revisão do desenho e aprovação para execução
estimate_h: 22.5
executed_h: 0.0
remaining_h: 22.5
scope:
  - workspace
  - brza-studio
opened: 2026-11-03
owner: Anderson
tags:
  - tooling
---

# PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients

- **Retomar:** o plano foi aberto a partir da extração do componente MCP do [PLN-003](../PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md). O desenho está consolidado com base nas decisões R3.4, R4.1, R5.1, R7.1, R9.1–R9.4 e R10.3 do PLN-003; os passos P1 a P5 aguardam aprovação de Anderson para início da execução.

## Pedido

- **Origem:** [PLN-003: O workflow do workspace roda igual no BrzA Studio e no Orca, por plugins e pelo `brza`](../PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md), por pedido de Anderson em 2026-11-03: "crie um plano só pro `MCP`".

O MCP é o coordenador e orquestrador central do fluxo nos dois aplicativos (BrzA Studio e Orca). É um servidor residente em segundo plano que expõe ferramentas padronizadas para despacho de tarefas, enfileiramento com semáforo sob três tetos, imposição de modelo/esforço e mediação de decisões.

Os itens do pedido, numerados para a Cobertura:

1. Servidor HTTP local residente (127.0.0.1) gerenciado por launchd, com controle CLI (`brza mcp start|stop|status`) e autenticação Bearer token;
2. Protocolo MCP sobre HTTP/SSE com a ferramenta `dispatch` e reconhecimento da sessão chamadora (`X-Brza-Session`);
3. Fila de prioridade persistente (SQLite) com ordenação por `deadline`, `blocks`, `priority` e ordem de chegada;
4. Admissão de workers regulada por três tetos simultâneos: teto do workspace somado, teto por conta/runtime (bloqueando a 90% do consumo projetado até `resetsAt`) e teto da máquina (RAM/swap/CPU);
5. Política declarativa de modelo e esforço em `brza.toml` com chaves de desligamento (`brza mcp config`);
6. Mecanismo de desempate em duas etapas: tabela de regras e cotas, modelo local `tev1:4b` via Ollama (`/v1/systemone`) e fallback Haiku (`claude -p --json-schema`);
7. Gates de aprovação da sessão principal para executores e troca de contas, com registro de telemetria `route`.

### Cobertura

| Origem     | Critério de aceite                                                                                      | Passo | Teste (nível) |
| :--------- | :------------------------------------------------------------------------------------------------------ | :---- | :------------ |
| `Pedido 1` | `brza mcp start`, `stop` e `status` gerenciam o daemon sob `launchd` e respondem na porta local           | P1    | `test_mcp_lifecycle.py` (unidade/integração) |
| `Pedido 1` | conexões sem Bearer token válido são rejeitadas com HTTP 401                                            | P1    | `test_mcp_auth.py` (unidade) |
| `Pedido 2` | a ferramenta `dispatch` aceita tarefas tipadas e identifica a sessão chamadora pelo header ou argumento | P3    | `test_mcp_dispatch.py` (unidade) |
| `Pedido 3` | pedidos com `deadline` mais próximo ou marcados com `blocks` saem na frente de pedidos `priority: high` | P2    | `test_mcp_queue.py` (unidade) |
| `Pedido 4` | novos workers aguardam quando qualquer um dos três tetos atinge o limite, com status explícito          | P2    | `test_mcp_limits.py` (unidade) |
| `Pedido 5` | a tarefa segue o modelo definido em `brza.toml`, e a chave de desligamento desativa a imposição         | P4    | `test_mcp_policy.py` (unidade) |
| `Pedido 6` | a tabela decide a cota; o `tev1` desempata o texto em <0,1 s e repassa ao Haiku se a confiança for baixa| P4    | `test_mcp_resolver.py` (integração) |
| `Pedido 7` | chamada de executor ou troca de conta retorna proposta de gate sem disparar o worker diretamente        | P3, P5| `test_mcp_gates.py` (unidade) |

## Desenho

### D1 — Servidor HTTP residente e controle de ciclo de vida (`packages/mcp/server.py`)

- **Origem:** PLN-003/R3.4, PLN-003/B6.
- **Implementação:** Daemon HTTP local em Python 3 stdlib escutando exclusivamente em `127.0.0.1:4242`.
- **Segurança:** Token criptográfico gerado na primeira inicialização e armazenado em `~/.brza/runtime/mcp.token` com permissão restrita (`0600`).
- **Controle:**
  - Launchd: agente configurado em `~/Library/LaunchAgents/com.brza.orchestrator.plist`.
  - CLI: verbos `brza mcp start`, `brza mcp stop`, `brza mcp status`.

### D2 — Fila de prioridade e os três tetos de concorrência (`packages/mcp/queue.py`)

- **Origem:** PLN-003/R7.1, PLN-003/R9.1–R9.4, PLN-003/M8.
- **Armazenamento:** SQLite stdlib em `~/.brza/orchestrator.db`.
- **Algoritmo de Priorização:**
  1. `deadline` mais próximo.
  2. `blocks` (bloqueadores têm preferência sobre independentes).
  3. `priority` (`high` > `medium` > `low`).
  4. Timestamp de chegada.
- **Regras dos Três Tetos:**
  - **Teto Workspace:** limite global somado de processos ativos.
  - **Teto Conta & Runtime:** consumo obtido via `orca account list --json`. Se o ritmo extrapolado até `resetsAt` alcançar 90%, nenhum novo worker daquela conta é admitido.
  - **Teto Máquina:** memória RAM livre > 4 GB e swap estável; CPU > 90% segura novos disparos.

### D3 — Ferramentas MCP e protocolo de despacho (`packages/mcp/dispatch.py`)

- **Origem:** PLN-003/R4.1, PLN-003/M1, PLN-003/M12, PLN-003/M15.
- **Ferramentas:**
  - `dispatch(task, role, target, model?, effort?, account?)`: submissão de pedidos. Se `role == 'consultant'`, executa de forma autônoma. Se `role == 'implementer'` ou demanda troca de conta, devolve proposta para a sessão principal solicitar aprovação do usuário (gate M15).
  - `status()`: retorna o estado das filas, workers em execução e o teto que está retendo cada pedido pendente.
  - `config(key, value?)`: consulta e altera chaves de bypass e desligamento da política.

### D4 — Política declarativa e o desempatador `tev1` + Haiku (`packages/mcp/policy.py`)

- **Origem:** PLN-003/R5.1, PLN-003/R6.3, PLN-003/M9, PLN-003/M11.
- **Arquivo `brza.toml`:**
  - Mapeia papéis e tarefas para modelo padrão e esforço (`opus`, `sonnet`, `haiku`; `high`, `medium`, `low`).
  - Define cotas e limiares de segurança (soft cap 55%, hard cap 90%).
- **Resolução de Desempates:**
  1. Parâmetros estáticos e cotas são avaliados via tabela determinística.
  2. Dúvidas na classificação do texto da tarefa são submetidas ao modelo local `tev1:4b` via endpoint Ollama (`/v1/systemone`).
  3. Se a confiança calculada ficar abaixo de 0,75, aciona o Haiku com `--max-budget-usd 0.01` via `claude -p --json-schema`.

### D5 — Telemetria e auditoria (`packages/mcp/telemetry.py`)

- **Origem:** PLN-003/M16.
- Toda operação de roteamento, admissão ou bloqueio na fila grava uma linha estruturada em `~/.brza/orchestrator.log` no formato:
  ```json
  {"ts": "2026-11-03T12:00:00Z", "event": "route", "caller": "pln-003", "target": "worker-1", "model": "sonnet", "reason": "policy"}
  ```

## Passos

> Os passos executam sob pedido explícito de Anderson, nas sessões designadas.

### P1 — O servidor HTTP residente em Python stdlib e controle de lifecycle

Executa D1 · executor: sessão do `tools-kit`

Estimado: 4.5 h · Executado: — h

- [ ] **1. Testes que falham:** inicialização HTTP em `127.0.0.1:4242`, Bearer token e comandos start/stop/status.
- [ ] **2. Implementar servidor:** daemon HTTP em Python stdlib com rotas SSE e POST.
- [ ] **3. Plist do launchd:** template para `~/Library/LaunchAgents/com.brza.orchestrator.plist`.
- [ ] **4. Comandos CLI:** `brza mcp start|stop|status`.
- [ ] **5. Rodar e ver passar:** testes de integração de lifecycle.
- [ ] **6. Commit:** na branch de trabalho.

**Evidência:** —

### P2 — A fila SQLite e o controle dos três tetos

Executa D2 · executor: sessão do `tools-kit`

Estimado: 5.5 h · Executado: — h

- [ ] **1. Testes que falham:** persistência no SQLite, ordenação (`deadline` > `blocks` > `priority` > chegada) e retenção pelos três tetos.
- [ ] **2. Implementar fila:** módulo `queue.py` com cálculo de projeção de cota e medição de recursos de máquina.
- [ ] **3. Integração de ciclo:** vinculação com eventos de conclusão (`worker_done`).
- [ ] **4. Rodar e ver passar:** suíte de testes de concorrência e limites.
- [ ] **5. Commit:** na branch de trabalho.

**Evidência:** —

### P3 — As ferramentas MCP, despacho e gates de aprovação

Executa D3 · executor: sessão do `tools-kit`

Estimado: 4.5 h · Executado: — h

- [ ] **1. Testes que falham:** dispatch tipado, leitura de headers `X-Brza-Session`, gates para executores e ferramenta `status`.
- [ ] **2. Implementar ferramentas:** endpoints MCP compatíveis com os clientes.
- [ ] **3. Rodar e ver passar:** testes de integração de despacho e autorização.
- [ ] **4. Commit:** na branch de trabalho.

**Evidência:** —

### P4 — A política declarativa e o desempatador `tev1` + Haiku

Executa D4 · executor: sessão do `tools-kit`

Estimado: 5.0 h · Executado: — h

- [ ] **1. Testes que falham:** parser de `brza.toml`, integração com `brza quota`, chamada local ao `tev1:4b` e fallback Haiku.
- [ ] **2. Implementar:** módulo de resolução e conexão com o Ollama local e `claude -p`.
- [ ] **3. Calibração:** validação contra os casos de teste do M11.
- [ ] **4. Commit:** na branch de trabalho.

**Evidência:** —

### P5 — Telemetria de roteamento, testes de integração e revisão

Executa D5 · executor: sessão do `tools-kit`

Estimado: 3.0 h · Executado: — h

- [ ] **1. Telemetria:** implementação de logs tipados `route` em `~/.brza/orchestrator.log`.
- [ ] **2. Testes de ponta a ponta:** fluxo completo de despacho com concorrência e desempate.
- [ ] **3. Parecer de revisão:** gerar parecer em `work/reviews/pln-009-servidor-mcp.md`.
- [ ] **4. Fechamento:** atualização de status para `done`.

**Evidência:** —

## Regressão

- O servidor MCP não interfere em sessões locais que não utilizam o orquestrador.
- A ausência do Ollama ou do `tev1:4b` causa fallback automático e transparente para a tabela ou Haiku sem travar a requisição.
- Os comandos de CLI `brza` continuam operando normalmente sem o servidor MCP em execução.

## Desvios

*(Nenhum desvio registrado até o momento).*

## Worklogs

- 2026-11-03 — plano criado e desenhado a partir da extração do componente MCP do PLN-003.
  [O PLN-009: abertura do plano do MCP residente](../../work/worklogs/2026-11-03-pln-009-abertura-do-plano-do-mcp-residente.md)
