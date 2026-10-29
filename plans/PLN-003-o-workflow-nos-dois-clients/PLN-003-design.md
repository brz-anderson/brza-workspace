# PLN-003 — Desenho

> **Rascunho.** O Terreno e a matriz vêm do levantamento e da medição de 2026-10-29. Os itens `D` ainda não foram
> escritos: saem da matriz na próxima sessão, com os riscos da fase 0 marcados como hipóteses (R7.3).

## O que este desenho assume

- **R1.1:** o "Workflow" são os dois — o fluxo do workspace e o recurso Workflow do Claude Code.
- **R1.2, R4.2:** o plugin do Orca tem painel e comandos; o painel é HTML regenerado, numa pasta em `devPluginPaths`.
- **R1.4, R6.1:** o PLN-003 não espera o P7; o P7 roda já, na sessão `pln-002-p7`.
- **R2.1:** o client se acha pelo env do app, depois `BRZA_CLIENT`, depois o app vivo.
- **R2.2:** um `brza` próprio em `~/.local/bin` despacha aos `brza-*` e repassa o resto ao CLI do client.
- **R2.3:** o `tree` e o `test` valem para qualquer repositório; o `app` e o `dev` ficam do BrzA Studio.
- **R2.4:** `install` e `doctor` agem no client detectado, com `--client studio|orca|all`.
- **R3.1, R3.2:** o CLI é público, por fases — pip e brew, depois npm, depois winget —, em Python stdlib com shims.
- **R3.3:** o app se instala da release do GitHub, com `--from-source`.
- **R3.4:** o MCP é um servidor HTTP residente, com `brza mcp start|stop|status`.
- **R4.1:** o MCP é o orquestrador do fluxo — sessão, conta, runtime, fila, modelo e esforço.
- **R4.3, R4.4:** skills e hooks vão ao plugin do Claude, com `brza:`; o Workflow começa por um piloto em
  `workflows/*.js`.
- **R5.1, R5.2:** a tabela decide e um agente desempata; o consultor roda direto, o executor passa por gate.
- **R5.3:** o código público mora em `brz-anderson/brza`; o workspace fica com notas, planos e a instância da norma.
- **R6.2, R7.2:** o `DESIGN.md` é o design system do painel; a arquitetura e o contrato vão a um `ARCHITECTURE.md`.
- **R6.3:** a política mora num `brza.toml`, que o `AGENTS.md` cita.
- **R6.4:** o orquestrador decide o modelo do que abre e sugere à sessão principal, por aviso.
- **R7.1:** o semáforo é por conta e por runtime, pelo `usedPercent`.

## Terreno

### O plugin do Orca

- Worker: child_process.fork, Node completo sem sandbox (plugin-host-process.ts); env só PATH/HOME/LANG/TZ/TMP (WORKER_ENV_ALLOWLIST, plugin-worker-env.ts); max 5 workers, 30 s por comando. Igual no Orca 1.4.244.
- Painel: iframe sandbox allow-scripts, srcdoc; CSP connect-src 'none' (plugin-panel-shell.ts:9); HTML de panel.entry relido a cada open, até 10 MB.
- Sem canal worker→painel (plugin-host-protocol.ts). Painel chama só workspace.readContext, terminal.sendText, notifications.show (plugin-host-api.ts panel:true). 64 KB/msg, 30 msg/10 s.
- readContext: {branch, displayName, terminals[{id}]} sem caminho (plugin-host-method-bindings.ts:~70-85). sendText exige terminal existente do worktree em foco, ≤4096 chars; não abre terminal.
- Eventos: worktree.created {worktreeId,path,branch}, removed {worktreeId,path}, agent.status.changed.
- Compat: Orca 1.4.244 aceita manifestVersion 1 e 2; fork só 1. engines '>=1.4.242' serve aos dois. upstream/main renomeou storage→storage:own, secrets→secrets:own.
- Instalação: devPluginPaths por app (hoje [] nos dois), mutável sem hash; ou local-path (copia, imutável). Consent por app. pluginSystemEnabled=true nos dois.
- Contorno não testado: regravar panel.html na pasta dev com os dados embutidos.
- Subagente rodou git fetch upstream no brza-studio (upstream/main → 12f9f8175cc).

### O MCP e o chat

- Chat Claude dos dois apps: claude-agent-sdk stream-json (claude-stream-json-connection.ts:35), settingSources user/project/local (claude-structured-launch-resolution.ts:43,74); app injeta só o plugin de visuais (:268); ClaudeStructuredSdkOptions sem mcpServers (:50-67). mcpServers:[] é só ACP. Upstream igual (:41,:258).
- Prova: context7 chega a este chat pelo enabledPlugins do projeto. MCP stdio herda env do claude (ORCA_CLI_COMMAND, ORCA_USER_DATA_PATH, ORCA_AGENT_SESSION_ID).
- Overrides: BrzA claude-brza; Orca claude-orca (fixfy/scripts/orca/claude-orca, fora da Fixfy roda claude puro) → no Orca, plugin sobe com cwd no workspace, não em checkout do brza-studio.
- rpc('settings.getAgentLaunch') testado contra Orca 1.4.244: ok. Orca CLI tem terminal create|read|send, agent launch --surface chat.
- Sem método de cartão no chat; cartão = AgentJournalProducerLinkage (agent-session-journal-types.ts:364), muda o app.
- Norma: AGENTS.md:50-52, CLAUDE.md:49-51 (só context7). Padrão extraKnownMarketplaces directory em brza-studio/.claude/settings.json.
- Tabela casos: c1 nota; c2 sessão; c3 msg a sessão (sem comando, P7); c4 terminal→chat; c5 Orca.
- A1 fluxo ~9 h est (~3 h exec), dois apps; A2 fino ~5 h, premissa caiu (CLI já alcança agentSession; cartão exige app); A3 no app ~10-12 h +15 h cartão, só BrzA. Recomendação A1, leva c2,c3,c1; c4 no Bash.
- Pontos: stdio Python sem dep vs pacote mcp; Orca em checkout brza-studio (aceitar / claude-orca delega / override); plugin via marketplace de diretório + enabledPlugins + reescrever norma; pasta do plugin.

### O plugin do Claude

- Plugin: .claude-plugin/plugin.json + commands/ agents/ skills/ hooks/hooks.json .mcp.json; binário 2.1.292 aceita workflows/*.js (nome <plugin>:<meta.name>), campo workflows @internal, sem doc pública.
- Hooks/.mcp.json com ${CLAUDE_PLUGIN_ROOT}, CLAUDE_PLUGIN_DATA, CLAUDE_PROJECT_DIR. settings de plugin: só agent, subagentStatusLine → env/promptCacheTtl ficam no settings.json.
- Skill de plugin ganha namespace (brza:plan-runner).
- measure.py:70-73 ROOT=MEASURE_DIR|BRZA_WORKSPACE|__file__; check_notes.py:54 raiz por 4 '..' → quebra no cache de plugins.
- Chat: SDK, pathToClaudeCodeExecutable = agentCmdOverrides.claude (structured-agent-command-resolution.ts:29); app só injeta native-chat-visuals; upstream igual.
- Vias: --plugin-dir no claude-brza (:70-72) | enabledPlugins + extraKnownMarketplaces directory no settings do projeto | escopo de usuário (hooks em todo repo; fere CLAUDE.md).
- Nenhum .claude/workflows/ em lugar nenhum. Candidatos: revisão de plano; Terreno (laço consultor); retomar; conferência de fechamento; fim de sessão.
- Norma: AGENTS.md "ferramental só no projeto", CLAUDE.md "plugins só aqui"; skills com namespace mudam o glossário.

### O orquestrador

- Orca orchestration (CLI 1.4.244 e fork): run/task/dispatch/worker-start/ask/reply/gates, SQLite no main (src/main/runtime/orchestration/db/). "Run ... does not schedule or place workers". Coordinator.maxConcurrent=4 (coordinator.ts:37,243) só instanciado em gates.ts:32; coordinator-start/stop aposentados (dispatch-handlers.ts:71).
- worker-start --agent --model --effort; agent launch --agent --model --effort --surface; sem flag de conta. agentSession.create sem conta; accounts.selectClaude global (accounts.ts:142); agentSession.switchAccount move chat (não testado). capability agent-session.account-env.v1 (agent-session-create-capabilities.ts:15-16).
- Contas app: Claude admin@ e anderson@ (Fixfy), Codex pessoal; activeAccountId null. orca account list --json devolve usedPercent/resetsAt (session 5h, weekly, fableWeekly) por conta — sinal p/ semáforo. measure.py:84-87 account()=basename(CLAUDE_CONFIG_DIR) → contas do app viram 'home' (defeito). failure: 0 linhas.
- measurements 7d: 178 linhas; turn opus .claude 117, home 9; subagent sonnet 11.
- Agente interno: claude -p --model --effort --output-format json --json-schema --max-budget-usd; precedente fixfy/scripts/delegate.py:186 com CLAUDE_CONFIG_DIR; quota.py route (55%/90%). Python sem anthropic; sem API key.
- Quem chamou: .mcp.json expande ${VAR} em url/headers de http (doc code.claude.com/docs/en/mcp); header X-Brza-Session: ${ORCA_AGENT_SESSION_ID}; não testado.
- Riscos a medir: claude -p, expansão no .mcp.json, switchAccount.
- Pontos: agente decide (regra+agente desempata Sonnet / tudo / regra pura / Opus); chamada na fila (abrir sessão+worker-start+send / +Agent / só abrir / toda); semáforo (por conta via usedPercent / global / conta+runtime); desativar (só modelo/esforço / agente / tudo); reaproveitar orchestration (ciclo de vida sim, roteamento não); conta por chamada (-p CLAUDE_CONFIG_DIR + switchAccount / só -p / flag no fork).

### As sugestões das notas

Sessões e correio
- F1 brza sessions list|send|close por nome — PLN-002-plan.md:255-269 (P7 bloqueado); cli. Orca: precisa do CLI do client.
- F2 correio entre contas (SendMessage não cruza contas) — I:codex-como-subagente-no-chat-do-claude.md:74-75; supõe MCP do app.
- F3 criar worktree+sessão como ferramenta tipada — codex-como-subagente:75; supõe MCP do app.
- F4 nome automático do chat "PLN-001 · P42" (chat-namer) — I:scripts-da-fixfy-fora-do-port-para-o-brza.md:23; cli/script.
- F5 nome da sessão para o brza note (X3) — PLN-002-plan.md:310-312; cli.
Subagentes e runtimes
- F6 Codex como cartão de subagente via agente Claude que roda codex exec (caminho 1) — codex-como-subagente:27-33; agente do plugin do Claude.
- F7 colega de equipe (agent teams) embrulha Codex — :35-47; flag do Claude.
- F8 passos do Codex dentro do cartão via MCP do app (brza.codex_run, linhas filhas do tool_use_id), ~15 h — :49-66; MCP do app + app.
- F9 codex_reply(thread,msg) — :70-71; MCP do app.
- F10 delegar ao agy pela ACP do app, ferramenta "delegar ao runtime" — :72-73; MCP do app.
- F11 chat só orquestra, subagente vira sessão de terminal com cartão — :91-112; mcp+cli+app.
- F12 consultor (Agent nativo) × executor (sessão de terminal) escolhido pelo orquestrador — :114-125; mcp+agente do plugin.
- F13 delegate.py portado — scripts-da-fixfy:24 (gatilho medição Fixfy 2026-10-30); cli.
- F14 quota.py (cota por conta) — scripts-da-fixfy:25 (gatilho: mais de uma conta no mesmo trabalho); cli.
- F15 sandbox do Codex como argumento, visível no canUseTool — codex-como-subagente:127-134,155; MCP do app.
- F16 "Selecionar automaticamente" modelo/esforço no seletor — PLN-001-plan.md:59-60,118; app.
Notas e planos
- F17 brza note (feito, P6). F18 brza ship (rebase, testes, push) — PLN-002-plan.md:64-66, fora. F19 fanout/status da Run — usar orca orchestration. F20 brza tree --list órfãos. F21 canonicalize para o runtime — os-comandos-brza:71-72.
App e instalação
- F22 despacho brza X (feito, fork). F23 import boundaries vermelho (external-subcommand → @orca/process-host) — I:import-boundaries-vermelho...:34-36; app. F24 app install confirma antes de sobrescrever. F25 ajuda/CLAUDE.md para brza install/run. F26 SHELL_SESSIONS_DISABLE=1 no brza-run — I:brza-run-imprime-saving-session...:55-67; cli. F27 telemetria optedIn — scripts-da-fixfy:30-34; app/config. F28 plugins da Fixfy (painel, ▶, ⤢, /rename) viram plugins do Orca — fixfy decision orca-fixfy-congelado...:35-38. F29 orca-close-idle/restart/patch descartados com gatilho.
Notificação e remoto
- F31 brza notify (Lembretes do iCloud) — I:brza-notify-avisa-no-iphone-pelos-lembretes.md:10-44; cli. F32 hook Stop de turno longo → notify; hook do plugin. F33 Tailscale/Remote Orca Server — I:tailscale-para-acesso-remoto-ao-brza-studio.md; infra. F34 notas do funnel.
Conflito: issue do Codex (A3 MCP no app, só BrzA) × R3.4/R4.1 (MCP residente fora do app, dois clients); AGENTS.md ferramental só no projeto.
work/decisions, notes, reviews, wiki/guides vazios.

## A matriz feature × frente

Insumos: PLN-003-plan.md (R1–R4), terreno-*.md, inventario-issues.md (F1–F34), AGENTS.md, CLAUDE.md, work/README.md,
plans/README.md, plan-runner, notes-checker, memória `abrir-sessao-nova-pelo-brza-sessions.md`.
Horas: estimadas, na régua do PLN-002 (1,5–3 h estimado por `brza-*`, 0,2–0,7 h executado; razão ~0,15–0,25).

### Critérios de alocação (aplicados nesta ordem; o primeiro que casa decide)

- **C1 Julgamento** — texto que o agente segue e que depende de juízo → norma. Neutro de runtime → `AGENTS.md`;
  mecânica do Claude → `CLAUDE.md`; forma de nota → `work/README.md`/`plans/README.md`; procedimento que se repete → skill.
- **C2 Fora do Claude** — precisa rodar no terminal, no Codex/agy, num script, no launchd, ou sem servidor no ar → cli.
  A cli é o núcleo: toda ação do mcp é uma função do `brza_runtime` que a cli também expõe como verbo.
- **C3 Estado comum** — precisa de estado entre sessões, contas ou apps ao mesmo tempo (fila, cota, quem chamou,
  decisão consistente) → mcp.
- **C4 Ciclo do Claude** — evento de hook, skill, definição de agente com modelo, roteiro `agent()`, `.mcp.json` →
  plugin do Claude.
- **C5 UI nos dois apps** → plugin do Orca.
- **C6 Dentro do app** — `tool_use_id`/cartão, seletor nativo, estado sem RPC → app (fork); só BrzA; entra só sem contorno.
- **C7 Imposição** — regra cuja violação gasta cota, dinheiro ou cache e que cabe numa tabela → a norma declara a
  regra e a tabela, e o mcp (ou hook) impõe lendo a tabela. Regra de juízo fica só no texto (C1).
- **C8 Desempate** — vence a frente que roda no Orca upstream; com o mesmo "se paga", vence a mais barata.

### Base já decidida (R1–R4), frente fixa

| ID | Feature | Origem | Frente(s) e papel | h | Se paga | Orca? | Critério |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| B1 | `brza` próprio + detecção env → app vivo; canonicalize | R2.1, R2.2; F21, F22 | cli | 3–5 | fase 1, no 1º uso do Orca | sim | C2 |
| B2 | `tree`/`test` generalizados; `tree --list` órfãos | R2.3; F20 | cli | 4–6 +1 | fase 1 | sim | C2 |
| B3 | `install`/`doctor` no client detectado; ajuda | R2.4; F25 | cli + `CLAUDE.md` (o que o install liga) | 1,5–2,5 | fase 1, 1ª sessão no chat do Orca | sim | C2, C1 |
| B4 | pacote pip+pipx+uv e brew | R3.1, R3.2 | cli | 4–6 | fase 1, 1ª instalação fora | — | C2 |
| B5 | `app install` pela release, `--from-source`, confirma antes | R3.3; F24 | cli | 3–3,5 | fase 1, 1ª máquina sem o repo | não (só o app BrzA) | C2 |
| B6 | servidor HTTP residente, launchd, porta, token, `brza mcp start/stop/status` | R3.4 | mcp + verbo na cli | 4–6 | fase 2 | sim | C3 |
| B7 | painel HTML regenerado + comandos `brza` | R1.2, R4.2; F28 (painel) | plugin do Orca (mostra) + cli `brza panel render` (gera) + mcp (regera a cada mudança de estado) | 6–10 | fase 2 | sim | C5, C2 |
| B8 | skills e hooks no plugin, `brza:`; raiz por env | R4.3 | plugin do Claude + `CLAUDE.md`/glossário | 3 +1 (raiz do `measure.py`/`check_notes.py`) | fase 1 | sim | C4 |
| B9 | piloto `workflows/*.js` (Terreno) | R4.4 | plugin do Claude | 2 | fase 2 | sim, a medir (`@internal`) | C4 |
| B10 | shim npm/npx/pnpm | R3.1 | cli | 2 | fase 3 | — | C2 |

### O orquestrador (R4.1) fundido com as issues

Alternativas viáveis na coluna "Alt"; o porquê em uma linha.

| ID | Feature | Origem | Frente(s) e papel | Alt | h | Se paga | Orca? | Critério | Porquê |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| M1 | Ferramenta `dispatch`: pedido tipado (tarefa, classe consultor/executor, alvo, runtime/conta/modelo opcionais) | R4.1; F3, F11 (sem cartão), F12 | mcp decide + plugin do Claude (a definição do agente declara a classe) + `AGENTS.md` (os três papéis) | só cli `brza dispatch` sem estado | 2–3 | fase 2, no 1º encadeamento | sim | C3 + C1 | é a porta única do "coração"; sem estado não há fila |
| M2 | Roteador de sessão: achar por nome, abrir worktree+sessão, mandar, fechar; respeita a trava de cache | R4.1; F1 (P7), F2, F3, F5 | cli (verbos `brza sessions list/send/close/open`) + mcp (escolhe) | `orca terminal` direto do mcp | 3 (P7) + 1,5 | fase 1 (cli) / fase 2 (mcp) | sim (`orca terminal`, `agent launch`) | C2 + C3 | o verbo serve ao terminal e ao Codex; a escolha precisa ver todas as sessões |
| M3 | Nome de sessão como chave (`pln-NNN-pX`), chat-namer, `/rename` | F4, F5, F28 | `plans/README.md` (convenção) + hook do plugin (nomeia no arranque) + cli `brza sessions rename` | só convenção | 1,5–2 | fase 1 | parcial, a medir (rename de aba pela CLI) | C1 + C4 | o roteador acha sessão pelo nome; nome solto quebra o roteamento |
| M4 | Escolha de runtime (Claude/Codex/agy) | R4.1; F10, F11 | mcp (regra) + cli `sessions open --agent` | ACP do app (F10 original) | 2–3 (+1 agy) | fase 3 | sim (`agent launch --agent`, `worker-start --agent`) | C3 | depende de M2 e de M8; Codex/agy ainda raros |
| M5 | Codex como cartão via agente Claude que roda `codex exec` | F6 | plugin do Claude (agent `brza:codex`, `-s read-only` por padrão) | M4 (sessão de terminal) | 1–1,5 | fase 2, 1ª revisão pelo Codex | sim | C4 | dá o cartão nativo sem tocar o app |
| M6 | Conta por chamada | R4.1; F13 | mcp decide; cli executa `claude -p` com `CLAUDE_CONFIG_DIR`; chat por `agentSession.switchAccount` | flag de conta no fork | 2–4 | fase 2 (só consultor `-p`) / fase 3 (sessão) | a medir (`switchAccount`) | C3 | `agentSession.create` não tem conta; `-p` tem |
| M7 | Sinal de cota por conta | R4.1; F14 | cli `brza quota` (sobre `orca account list --json`) + mcp consome | ler o JSON no mcp sem verbo | 1,5 | fase 2 | sim | C2 | o verbo serve ao humano e ao Codex; o mcp só lê |
| M8 | Fila/semáforo por conta e runtime, persistente (SQLite stdlib) | R4.1 | mcp | global; só por conta | 4–6 | fase 2, 1º choque de cota | sim | C3 | o `Coordinator.maxConcurrent` do Orca só vive em gates (terreno-orquestrador) |
| M9 | Modelo/esforço pela política "O modelo segue a tarefa" | R4.1; F16 (parte) | `AGENTS.md` (prosa) + arquivo de política (tabela) + mcp (impõe no que abre) | só norma; mcp lê a tabela do `AGENTS.md` | 1,5–2 | fase 2 | sim (`--model --effort`) | C7 | hoje a regra é só texto e a medição mostra Opus em tudo |
| M10 | Chave de desligamento por dimensão (modelo/esforço, agente, tudo → passthrough) | R4.1 | mcp (config) + cli `brza mcp config` | só env | 0,5–1 | fase 2 | sim | C3 | "pode ser desativado" é requisito do pedido |
| M11 | Agente interno que desempata (`claude -p --json-schema`, Haiku/Sonnet, `--max-budget-usd`) | R4.1 | mcp | agente em toda chamada; regra pura | 3–4 | fase 2b, quando a medição mostrar empate | sim | C3 | regra é grátis e instantânea; o agente paga só no empate |
| M12 | Quem chamou: header `X-Brza-Session: ${ORCA_AGENT_SESSION_ID}` + client | R3.4 (consequência); R4.1 | plugin do Claude (`.mcp.json`) + mcp | argumento `caller` na ferramenta | 1–2 | fase 2 | sim, a medir | C4 + C3 | residente não herda `ORCA_*` |
| M13 | Ciclo de vida pelo `orca orchestration` (task, dispatch, worker-start, ask/reply, worker_done) | R4.1; F19 | mcp chama a cli do client detectado | reimplementar no mcp | 3–4 | fase 2 | sim | C3 + C8 | reaproveita o ciclo; o roteamento é nosso ("does not schedule or place workers") |
| M14 | O fim volta ao chamador (espera × aviso; turno ocioso) | F11 | mcp (via `worker_done`) | bloquear até o fim | 2–3 | fase 2 | sim | C3 | sem isso o executor vira fogo-e-esquece |
| M15 | Gate de aprovação (abrir executor, trocar conta) | conflito K3 | `AGENTS.md` (quando) + mcp devolve proposta + sessão principal pergunta | gate do `orca orchestration` | 1–2 | fase 2 | sim | C1 + C3 | preserva "quem pergunta é a principal" |
| M16 | Medição do roteamento + conserto da conta `home` | R4.1; AGENTS.md:93-94 | hook `measure.py` (conserto) + mcp (linha `route`) | — | 0,5 + 1,5 | fase 1 (conserto) / fase 2 | sim | C3 | "a política se revê pela medição"; hoje conta errada |
| M17 | Fila e sessões no painel | R4.1 + R4.2 | plugin do Orca (mostra o HTML que o mcp regera) | — | 1–2 | fase 2 | sim | C5 | o semáforo invisível vira mistério |
| M18 | `codex_reply(thread, msg)` | F9 | mcp | `codex exec resume` pela cli | 1–2 | fase 3 | sim | C3 | estado da thread entre chamadas |
| M19 | Sandbox do Codex como argumento | F15 | mcp (impõe) | config do Codex | 1 | fase 3 | sim | C7 | a sandbox fica visível no `canUseTool` |
| M20 | Aviso ao celular (notify + hook Stop de turno longo; gate pendente) | F31, F32 | cli `brza notify` + hook do plugin + mcp chama | — | 2–3 | fase 3 | sim (macOS) | C2 + C4 | gate parado precisa chamar Anderson |
| M21 | "Selecionar automaticamente" no seletor | F16 | app | M9 cobre o que o orquestrador abre | 4–6 (não medido) | fora → issue | não | C6 | toca a principal, que segue "o de quem a abriu" |
| M22 | Passos do Codex dentro do cartão (`tool_use_id`) | F8, F11 (cartão) | app | — | ~15 | fora → issue | não | C6 | só BrzA, atrito de merge |
| M23 | `SHELL_SESSIONS_DISABLE=1` no `brza-run` | F26 | cli | — | 0,3 | fase 1 | sim | C2 | conserto pequeno no que o executor usa |

Saíram por não serem de fluxo ou por já resolvidos: F7 (flag experimental), F17 (feito), F18 (`ship`, já fora no
PLN-002), F22 (substituído por B1), F23 (bug do fork), F27 (telemetria), F29 (descartados com gatilho), F30 (não
descrita no inventário; não é de fluxo), F33 (Tailscale; o mcp escuta só em 127.0.0.1), F34 (funnel).

### Regra × mecanismo (onde cada regra mora e quem a impõe)

| Regra | Texto em | Imposta por |
| :-- | :-- | :-- |
| O modelo segue a tarefa | `AGENTS.md` (prosa) | mcp lendo o arquivo de política (M9) |
| Uma tarefa, uma sessão | `AGENTS.md` | roteador (M2) prefere sessão nova a acordar sessão grande parada |
| Trava de retomada | `CLAUDE.md` | hook `resume_guard.py` + roteador (o correio não passa pela trava, `CLAUDE.md:85`) |
| Quem pergunta é a principal | `AGENTS.md` | mcp devolve proposta (M15); nunca pergunta |
| Nome de sessão | `plans/README.md` | hook do plugin (M3) |
| Abrir sessão nova pela própria sessão | só na memória do agente | migra para `CLAUDE.md`/`AGENTS.md`; o roteador vira o caminho |
| Vocabulários de nota | `work/README.md` | `check_notes.py` (já) |

### DESIGN.md — proposta

Casa dona do durável do Desenho do PLN-003 (`plans/README.md:37`): arquitetura e contrato entre as frentes. Não é
regra de comportamento (isso é `AGENTS.md`) nem mecânica do Claude (`CLAUDE.md`).

1. Para que serve e para quem (agente e humano que mexem no ferramental)
2. As frentes e o dono de cada uma (cli núcleo, mcp coordenador, plugins, app) + os critérios C1–C8
3. Fluxo de uma chamada: pedido → quem chamou → política → fila → runtime/conta/modelo → ciclo → fim → medição
4. Contrato do mcp: ferramentas, schemas, erros, header `X-Brza-Session`, token, porta
5. Contrato da cli: verbos estáveis que o mcp e os plugins chamam; saída `--json`
6. A política: arquivo, campos, chave de desligamento, precedência pedido > política > padrão
7. Estado: fila (SQLite), onde mora, o que sobrevive a reinício
8. Regra × mecanismo (a tabela acima)
9. Compatibilidade: BrzA Studio × Orca upstream; o que é só do fork
10. Segurança: 127.0.0.1, token, o que o agente interno pode fazer
11. Medição: linhas `route`, como rever a política

Leitura alternativa: DESIGN.md no formato de design system para agentes de UI (o do Google Stitch), para o painel HTML.
