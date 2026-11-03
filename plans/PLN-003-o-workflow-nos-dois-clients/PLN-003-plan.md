---
status: in_progress
phase: execution
origin: request
ready: sim — P0 concluído (H1 a H6 medidas e D3–D7 ajustados); próximo passo: P1
estimate_h: 58.0
executed_h: 0.4
remaining_h: 54.5
scope:
  - workspace
  - brza-studio
opened: 2026-10-29
owner: Anderson
tags:
  - tooling
---

# PLN-003: O workflow do workspace roda igual no BrzA Studio e no Orca, por plugins e pelo `brza`

- **Retomar:** P0 concluído em 2026-11-03 (H1 a H6 confirmadas e itens `D3` a `D7` ajustados no [Desenho](PLN-003-design.md)); próximo passo: **P1** (o índice da `master` com `priority`, `blocks` e `deadline` em `scripts/brza/brza-note`).
- **A fila do orquestrador (2026-11-03):** a R9, respondida na sessão `bb0fd632` do `workspace`, fez do coordenador o
  orquestrador e deu a ordem da fila e os três tetos de workers; o Desenho mudou nas premissas, no M8, no M17, na
  regra da fila e no M24 novo (o índice da `master` grava `priority`, `blocks` e `deadline`). Os itens `D` partem daí.
- **Mudou a norma (2026-10-29):** a trava de retomada saiu, e a sessão passou a ser por frente, não por tarefa
  ([Uma sessão por frente de trabalho, sem trava de retomada e com o cache de 1 h](../../work/decisions/uma-sessao-por-frente-e-sem-trava-de-retomada.md)). O Desenho foi ajustado no M2 e na tabela de regras.
- **Mudou a norma (2026-10-30):** as notas saíram da `master`, que guarda só a norma, para as branches
  `workstream/<nome>`, com worktree em `.worktrees/<nome>`, e o `brza note` ganhou o `workstream` e o `sync`
  ([As notas moram em workstreams, e a `master` guarda só a norma](../../work/decisions/as-notas-moram-em-workstreams-e-a-master-guarda-so-a-norma.md)).
  O Desenho foi ajustado no M8 e M24 com o índice da `master`.
- **Mudou o Terreno do plugin do Orca (2026-11-02):** o sistema da `v1.4.246` tem canal worker↔painel, frame isolado
  ligado e manifesto v2, e `terminal.sendText` é só do worker, então a R1.2 ("HTML regenerado") e o C5 ficaram em
  revisão (o Terreno e a matriz do Desenho). Rodada respondida em 2026-11-02: o spike mede os dois caminhos,
  HTML+worker e TSX+worker. O plugin do Orca não contribui skills (reservado e vazio): o veículo delas é o plugin do Claude.
- **O desempatador do M11 (2026-11-03):** rodada respondida na sessão `bb0fd632` do `workspace`, "tev1 + Haiku
  (Recomendado)". A cota fica na tabela; o texto vai ao `tev1:4b` local, e ao Haiku abaixo do limiar de confiança; a
  Jev fica como backend de nuvem opcional. Na fase 2b, calibrar o limiar com empate real; antes do pacote público,
  conferir a licença do `tev1`. A medição e os pontos estão no [Desenho](PLN-003-design.md), em "O desempatador do M11".
- **Dividido:** [PLN-003 — Entrevista](PLN-003-interview.md) · [PLN-003 — Desenho](PLN-003-design.md)

## Pedido

- **Origem:** pedido livre, no chat do BrzA Studio de 2026-10-29. Relaciona-se com o
  [PLN-002](../PLN-002-os-comandos-brza/PLN-002-plan.md), sem depender do P7 dele (R1.4).

"vamos criar um plugin do Orca para o Workspace e um plugin do Claude + MCP para o Workflow e ajustar a CLI `brza` para
que o workflow funcione tanto no client `BrzA Studio` quanto no `Orca`" — Anderson, em 2026-10-29.

Os itens do pedido, numerados para a Cobertura:

1. o plugin do Orca para o Workspace;
2. o plugin do Claude com o MCP para o Workflow — o fluxo do workspace e o recurso Workflow do Claude Code (R1.1);
3. a CLI `brza` ajustada para o workflow funcionar no BrzA Studio e no Orca;
4. a CLI instala e atualiza o app, o plugin do Orca, o plugin do Claude e o MCP, e inicia e para o MCP; e é ela mesma
   instalável por `npm`, `npx`, `pnpm`, `brew`, `pip` e `winget`.

"o `BrzA CLI` deve conseguir instalar/atualizar o app `BrzA Studio`, o plugin do `Orca`, o plugin do `Claude`, o MCP -
iniciar/parar tbm -, como fazemos para que o CLI possa ser instalado com `npm|npx|pnpm|brew|pip|winget install`?" —
Anderson, em 2026-10-29, na mesma sessão.

5. a fila do orquestrador, por prioridade, sob um teto de workers do workspace, das contas e da máquina (R9).

"prioriza a fila considerando a prioridade do pedido - issue high, bloqueia avanço de plano, prazo de entrega curto e
etc -, o limite de workers em paralelo é geral do workspace somado, o cálculo também leva em consideração ritmo das
contas e o recurso disponível na máquina pra limitar workers" — Anderson, em 2026-11-03, na sessão `bb0fd632` do
`workspace`. O pedido veio da issue
[O coordenador se baseia no índice de notas da master](../../work/issues/o-coordenador-le-o-indice-da-master.md), que
fechou lá e passou ao PLN-003 (R9.1).

### Cobertura

| Origem     | Critério de aceite                                                                                      | Passo | Teste (nível) |
| :--------- | :------------------------------------------------------------------------------------------------------ | :---- | :------------ |
| `Pedido 1` | o mesmo `orca-plugin.json` instala nos dois apps e mostra o painel do workspace com planos e notas abertos | P10   | `plugin test` / visual nos dois apps (manual) |
| `Pedido 1` | os comandos do plugin mandam o `brza` certo ao terminal do worktree em foco                             | P10   | integração plugin + terminal (manual) |
| `Pedido 2` | o plugin do Claude traz as skills, os hooks e o MCP do workspace, e sobe nos chats dos dois apps          | P4, P6| carregamento do plugin nos dois apps (integração) |
| `Pedido 2` | o plugin traz roteiros de Workflow do Claude Code para o fluxo do workspace                               | P11   | execução de workflow piloto no chat (integração) |
| `Pedido 4` | `pipx install brza` e `brew install brz-anderson/tap/brza` instalam o CLI, com o `brza` e os `brza-*` no PATH | P3    | instalação limpa em VM / ambiente de teste (sistema) |
| `Pedido 4` | `brza app install` baixa o DMG da release e troca o app; `--from-source` compila da `origin/master`            | P2    | `test_brza_app.py` (unidade) |
| `Pedido 4` | `brza mcp start`, `stop` e `status` controlam o servidor residente                                           | P6    | `test_brza_mcp.py` e healthcheck HTTP (unidade/integração) |
| `Pedido 3` | `brza <sub>` acha o app que está rodando — BrzA Studio ou Orca — sem caminho fixo                        | P2    | `test_brza_cli.py` (unidade) |
| `Pedido 5` | com dois pedidos na fila, o de `deadline` mais próximo sai antes, e o de `blocks` antes do de `priority: high` | P1, P7| `test_orchestrator_queue.py` (unidade) |
| `Pedido 5` | worker novo espera quando o teto do workspace, o da conta e runtime (com a projeção a 90% até o `resetsAt`) ou o da máquina está cheio, e o painel diz qual | P7, P10| `test_orchestrator_limits.py` (unidade) |

## Passos

> Os passos de código são executados sob pedido explícito de Anderson, passo a passo, nas sessões designadas.

### P0 — Medição das hipóteses da fase 0 (H1 a H6)

Executa R7.3, H1–H6 · executor: sessão `pln-003-p0`

Estimado: 3.5 h · Executado: 0.4 h

- [x] **1. Medir H1:** expansão de `${ORCA_AGENT_SESSION_ID}` no header do `.mcp.json` (confirmada no CLI `2.1.317` e no SDK `0.3.284`; exige `"type": "http"` em `D3`).
- [x] **2. Medir H2:** execução de `claude -p` sob processo em background gerenciado por `launchd` (confirmada sem TTY via `setsid()` nos perfis gerenciados; exige omitir `CLAUDE_CONFIG_DIR` na conta `systemDefault` em `D6` e `~/.local/bin` no `PATH` em `D4`).
- [x] **3. Medir H3:** comportamento do `agentSession.switchAccount` em chat ativo (confirmada por RPC no socket local `orca-runtime.json` para sessão em repouso `at-rest`, com cópia de transcripts e 15 testes de unidade verdes; bloqueada em `turnActive`).
- [x] **4. Medir H4:** execução de `orca orchestration` fora do shell com env `ORCA_*` (confirmada injetando `ORCA_AGENT_SESSION_ID` do header `X-Brza-Session` e `ORCA_USER_DATA_PATH` no `env` do subprocesso em `D5`).
- [x] **5. Medir H5:** viabilidade do servidor MCP HTTP/SSE com Python 3 stdlib (confirmada com `ThreadingHTTPServer` atendendo Streamable HTTP `/mcp` e SSE legado `/sse` em `D4`).
- [x] **6. Medir H6:** execução de `workflows/*.js` pelo SDK nos dois apps (confirmada com ferramenta `Workflow` e `local_workflow` no SDK `0.3.284`; gramática AST documentada em `D3`).
- [x] **7. Registrar:** worklog e atualização dos itens `D` afetados no Desenho (`D3` a `D7`).

**Evidência:** [O PLN-003: a medição das hipóteses da fase 0 (P0)](../../work/worklogs/2026-11-03-pln-003-medicao-das-hipoteses-p0.md) e ajustes em `D3`–`D7` no [Desenho](PLN-003-design.md).

### P1 — O índice da `master` com propriedades de ordenação

Executa D2 (M24) · executor: sessão do `tools-kit`

Estimado: 1.0 h · Executado: — h

- [ ] **1. Teste que falha:** `test_brza_note.py` validando extração de `priority`, `blocks` e `deadline` para o `.brza/index.jsonl`.
- [ ] **2. Implementar:** atualizar `scripts/brza/brza-note` para extrair e gravar campos no índice unificado da master.
- [ ] **3. Rodar e ver passar:** suíte de testes de `scripts/brza/tests/test_brza_note.py`.
- [ ] **4. Commit:** commit na branch `workstream/tools-kit`.

**Evidência:** —

### P2 — A CLI `brza` unificada e o despacho nos dois clients

Executa D1 (B1, B2, B3, B5, M23) · executor: sessão do `tools-kit`

Estimado: 5.0 h · Executado: — h

- [ ] **1. Testes que falham:** detecção de client (`BRZA_CLIENT`, env herdado, processo vivo), despacho hierárquico `brza <sub>`, generalização de `tree`/`test` e flags de `app install`.
- [ ] **2. Implementar:** binário unificador `brza` em Python stdlib, preservando `SHELL_SESSIONS_DISABLE=1` no `brza-run`.
- [ ] **3. Rodar e ver passar:** testes de unidade em `test_brza_cli.py`, `test_brza_tree.py` e `test_brza_app.py`.
- [ ] **4. Commit:** commit na branch `workstream/tools-kit`.

**Evidência:** —

### P3 — O repositório público `brz-anderson/brza` e empacotamento (`pipx`, `brew`)

Executa D1 (B4) · executor: sessão do `tools-kit`

Estimado: 4.0 h · Executado: — h

- [ ] **1. Estrutura do repo:** configurar `pyproject.toml` (hatchling/flit, stdlib), entrypoint `brza`.
- [ ] **2. Fórmula Homebrew:** template da fórmula `brza.rb` para o tap `brz-anderson/homebrew-tap`.
- [ ] **3. Testar instalação:** testar `pip install -e .` e conferir comandos no PATH em ambiente limpo.
- [ ] **4. Commit:** commit no repositório `brz-anderson/brza`.

**Evidência:** —

### P4 — O plugin do Claude com skills e hooks de sessão

Executa D3 (B8, M3, M5, M12, M20) · executor: sessão do `tools-kit`

Estimado: 4.5 h · Executado: — h

- [ ] **1. Estrutura do plugin:** criar `plugins/claude/.claude-plugin/plugin.json` e `.mcp.json`.
- [ ] **2. Skills com namespace:** expor skills sob prefixo `brza:`.
- [ ] **3. Agente Codex:** definir `agents/codex.json` invocando `codex exec` com `-s read-only`.
- [ ] **4. Hooks:** hook de nomeação de sessão `pln-NNN-pX` e hook `Stop` longo para `brza notify`.
- [ ] **5. Teste:** carregar plugin no Claude Code de ambos os clients e validar listagem de ferramentas e agentes.
- [ ] **6. Commit:** commit na branch `workstream/tools-kit`.

**Evidência:** —

### P5 — As atualizações na norma do workspace e ARCHITECTURE.md

Executa D9 (R7.2, C1) · executor: sessão do `tools-kit`

Estimado: 2.0 h · Executado: — h

- [ ] **1. Documento de Arquitetura:** redigir `ARCHITECTURE.md` no repositório `brz-anderson/brza`.
- [ ] **2. Atualizar AGENTS.md:** registrar os 3 papéis (consultor livre, executor com gate), referência ao `brza.toml` e norma de sessão por frente.
- [ ] **3. Atualizar CLAUDE.md:** registrar namespace `brza:`, cache de 1 h e ausência de trava de retomada.
- [ ] **4. Commit:** commits correspondentes no workspace e no repo público.

**Evidência:** —

### P6 — O servidor MCP residente em Python stdlib com controle de lifecycle

Executa D4 (B6) · executor: sessão do `tools-kit`

Estimado: 5.0 h · Executado: — h

- [ ] **1. Testes que falham:** inicialização HTTP na porta local 4242, autenticação via Bearer token e controle start/stop/status.
- [ ] **2. Implementar servidor:** daemon HTTP em Python stdlib com rotas SSE/POST do protocolo MCP.
- [ ] **3. Plist do launchd:** template para `~/Library/LaunchAgents/com.brza.orchestrator.plist`.
- [ ] **4. Comandos CLI:** `brza mcp start|stop|status`.
- [ ] **5. Rodar e ver passar:** testes de integração e subida do serviço.
- [ ] **6. Commit:** commit no repositório do projeto.

**Evidência:** —

### P7 — A fila de prioridade SQLite e os três tetos de concorrência

Executa D5 (M8, M13, M14) · executor: sessão do `tools-kit`

Estimado: 6.0 h · Executado: — h

- [ ] **1. Testes que falham:** persistência no SQLite, ordenação (`deadline` > `blocks` > `priority` > chegada) e barramento pelos 3 tetos (workspace, cota 90% projetada, memória livre).
- [ ] **2. Implementar fila:** módulo `queue.py` e integração com `orca orchestration` e ciclo `worker_done`.
- [ ] **3. Rodar e ver passar:** suíte de testes de concorrência e limites.
- [ ] **4. Commit:** commit no repositório do projeto.

**Evidência:** —

### P8 — A política de modelos e esforço com chave de desligamento e gates

Executa D4, D6 (M1, M9, M10, M15, M16) · executor: sessão do `tools-kit`

Estimado: 5.0 h · Executado: — h

- [ ] **1. Testes que falham:** ferramenta `dispatch`, leitura de `brza.toml`, desligamento via `brza_config`, proposição de gate para executor e registro de telemetria `route`.
- [ ] **2. Implementar:** módulo de política e ferramentas MCP correspondentes.
- [ ] **3. Rodar e ver passar:** testes de unidade cobrindo todas as dimensões de política.
- [ ] **4. Commit:** commit no repositório do projeto.

**Evidência:** —

### P9 — O desempate via `tev1:4b` e fallback Haiku com controle de contas

Executa D6 (M6, M7, M11) · executor: sessão do `tools-kit`

Estimado: 4.5 h · Executado: — h

- [ ] **1. Testes que falham:** consulta local ao `tev1:4b` no Ollama, medição de score de confiança e fallback para `claude -p` com Haiku.
- [ ] **2. Implementar:** módulo desempatador integrado ao fluxo de decisão do MCP.
- [ ] **3. Calibração:** validação contra a suíte de 10 casos sintéticos e tarefas em texto livre.
- [ ] **4. Commit:** commit no repositório do projeto.

**Evidência:** —

### P10 — O plugin do Orca com painel declarativo TSX e integração com MCP

Executa D8 (B7, M17) · executor: sessão do `tools-kit`

Estimado: 7.0 h · Executado: — h

- [ ] **1. Migrar spike:** consolidar `spikes/c5-plugin/` para `plugins/orca/` com `ui: "components"`.
- [ ] **2. Visualização de fila:** implementar visualização em TSX mostrando pedidos, prioridades e o teto que segura cada worker parado (M17).
- [ ] **3. Ações via MCP:** conectar botões de controle ao MCP residente via HTTP local no worker (R10.3).
- [ ] **4. Testes:** rodar `plugin check` e validação visual nos dois apps (BrzA Studio e Orca).
- [ ] **5. Commit:** commit no repositório do projeto.

**Evidência:** —

### P11 — O piloto de workflows de fluxo no plugin do Claude

Executa D3 (B9) · executor: sessão do `tools-kit`

Estimado: 2.0 h · Executado: — h

- [ ] **1. Implementar piloto:** criar roteiro de fluxo em `plugins/claude/workflows/review.js`.
- [ ] **2. Validar no chat:** executar nos chats do BrzA Studio e do Orca.
- [ ] **3. Commit:** commit no repositório do projeto.

**Evidência:** —

### P12 — O roteador de sessões multiruntime (`brza sessions`)

Executa D7 (M4, M18, M19) · executor: sessão do `tools-kit`

Estimado: 3.5 h · Executado: — h

- [ ] **1. Testes que falham:** abertura e roteamento com `--agent claude|codex|agy`, argumentos de sandbox e continuidade com `codex_reply`.
- [ ] **2. Implementar:** suporte no `scripts/brza/brza-sessions` seguindo a norma de sessão por frente.
- [ ] **3. Rodar e ver passar:** testes de unidade em `test_brza_sessions.py`.
- [ ] **4. Commit:** commit no repositório do projeto.

**Evidência:** —

### P13 — Os shims universais npm/npx/pnpm

Executa D1 (B10) · executor: sessão do `tools-kit`

Estimado: 2.0 h · Executado: — h

- [ ] **1. Implementar shims:** scripts wrapper em JavaScript delegando para o executável `brza` nativo.
- [ ] **2. Publicar/Empacotar:** validar execução via `npx brza --version`.
- [ ] **3. Commit:** commit no repositório do projeto.

**Evidência:** —

### P14 — Revisão da entrega, testes de ponta a ponta e encerramento

Executa revisão geral contra Cobertura · executor: sessão de revisão

Estimado: 3.0 h · Executado: — h

- [ ] **1. Conferir Cobertura:** validar cada linha da tabela de Cobertura contra o comportamento real nos dois apps.
- [ ] **2. Parecer de revisão:** gerar nota `work/reviews/pln-003-workflow-nos-dois-clients.md`.
- [ ] **3. Documentação e fechamento:** migrar o durável para `ARCHITECTURE.md` e transicionar o plano para `status: done`.

**Evidência:** —

## Regressão

- `brza install --all` continua funcionando e ligando os executáveis existentes em `scripts/brza/`.
- Todos os testes unitários em `scripts/brza/tests` continuam passando sem regressão.
- Worktrees existentes do workspace continuam sendo reconhecidos pelo `brza tree` e `brza note`.
- A geração e sincronização de notas continua sendo validada pelo `check_notes.py` com zero erros e avisos.

## Desvios

*(Nenhum desvio registrado até o momento).*

## Pendências conhecidas

- [As skills de documento da Fixfy num possível plugin do BrzA](../../work/issues/skills-de-documento-da-fixfy-num-plugin.md)
  — o veículo é o plugin do Claude, não o do Orca; o gatilho é de Anderson.
- [O dev watch deixa carregado o plugin que já estava](../../work/issues/o-dev-watch-deixa-carregado-o-plugin-que-ja-estava.md)
  — o fim de um spike roda o `dev unload` nos dois apps e confere o `devPluginPaths`.
- [O --approve do plugin é barrado no modo auto](../../work/issues/o-approve-do-plugin-e-barrado-no-modo-auto.md)
  — fechada em 2026-11-03: passou depois do "Aprovar nos dois apps" de Anderson.
- [O DESIGN.md do BrzA vem do PLN-003](../../work/issues/o-design-md-do-brza-vem-do-pln-003.md) — no workstream
  `brand` (R10.2, R11.1); o PLN-003 não espera por ela.
- [Os passos do MCP no PLN-003 passam ao PLN-009](../../work/issues/os-passos-do-mcp-no-pln-003-passam-ao-pln-009.md)
  — os P6 a P9 daqui passam ao PLN-009; a R5.3 reabre aqui.
- [O CLI do Orca no chat do Studio fala com o Studio](../../work/issues/o-cli-do-orca-no-chat-do-studio-fala-com-o-studio.md)
  — vai ao B1 e à R2.1: o env herdado escolhe o app.
- [Os tipos de plugin faltam no pacote da 1.4.246](../../work/issues/os-tipos-de-plugin-faltam-no-pacote-da-1-4-246.md)
  — o `plugin create` e o `plugin types` quebram nos dois apps.

## Worklogs

- 2026-10-29 — aberto; R1 a R7 fecharam a Entrevista; o Terreno e a matriz foram ao Desenho; o P7 saiu à sessão
  `pln-002-p7`. Parou antes dos itens `D`.
  [O PLN-003: a entrevista do workflow nos dois clients](../../work/worklogs/2026-10-29-pln-003-a-entrevista-do-workflow-nos-dois-clients.md)
- 2026-11-02 — o Terreno do plugin do Orca reescrito contra a `v1.4.246`; o C5 virou hipótese e o spike foi ao `Retomar`.
  [O PLN-003: o Terreno do plugin do Orca na 1.4.246](../../work/worklogs/2026-11-02-pln-003-o-terreno-do-plugin-do-orca-na-1-4-246.md)
- 2026-11-03 — a medição e a rodada do desempatador, do workstream `workspace`, foram ao M11 do Desenho.
  [O PLN-003: o desempatador do M11](../../work/worklogs/2026-11-03-pln-003-o-desempatador-do-m11.md)
- 2026-11-03 — a Rodada 8 decidiu como rodar o spike do C5; o spike ficou parcial, parado na aprovação, com três issues.
  [O PLN-003: o spike do C5 parou na aprovação](../../work/worklogs/2026-11-03-pln-003-o-spike-do-c5-parou-na-aprovacao.md)
- 2026-11-03 — a R9, da sessão do `workspace`, levou a fila do coordenador ao orquestrador; o Desenho mudou no M8, no M17 e no M24.
  [O PLN-003: a fila do orquestrador](../../work/worklogs/2026-11-03-pln-003-a-fila-do-orquestrador.md)
- 2026-11-03 — Anderson aprovou o plugin nos dois apps; o spike do C5 rodou as sete perguntas, e o item 1 passou.
  [O PLN-003: o spike do C5 nos dois apps](../../work/worklogs/2026-11-03-pln-003-o-spike-do-c5-nos-dois-apps.md)
- 2026-11-03 — a R10 e a R11 fecharam o painel de componentes, os botões pelo MCP e o `DESIGN.md` no `brand`.
  [O PLN-003: o painel de componentes](../../work/worklogs/2026-11-03-pln-003-o-painel-de-componentes.md)
- 2026-11-03 — o Desenho ajustado para sessão por frente; itens D1 a D9, hipóteses H1 a H6 e passos P0 a P14 escritos.
  [O PLN-003: os itens D e os passos](../../work/worklogs/2026-11-03-pln-003-itens-d-e-passos-do-workflow-nos-dois-clients.md)
- 2026-11-03 — o P0 mediu e confirmou as hipóteses H1 a H6 da fase 0; ajustes técnicos incorporados aos itens `D3` a `D7` do Desenho.
  [O PLN-003: a medição das hipóteses da fase 0 (P0)](../../work/worklogs/2026-11-03-pln-003-medicao-das-hipoteses-p0.md)
