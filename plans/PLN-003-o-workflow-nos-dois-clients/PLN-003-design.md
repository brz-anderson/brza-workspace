# PLN-003 — Desenho

> **Desenho consolidado (2026-11-03).** A matriz e os itens `D` (D1 a D9) foram definidos a partir do Terreno,
> das rodadas R1 a R11 e dos resultados do spike do C5. As hipóteses da fase 0 (H1 a H6, R7.3) foram medidas e
> confirmadas no passo P0 (2026-11-03), com ajustes incorporados aos itens `D3` a `D7`.

## O que este desenho assume

- **R1.1:** o "Workflow" são os dois — o fluxo do workspace e o recurso Workflow do Claude Code.
- **R1.2, R10.1, R10.3:** o plugin do Orca tem painel e comandos. O painel é de componentes (`ui: "components"`), com
  um worker que lê `plans/` e `work/` do worktree da branch em foco; o HTML regenerado da R4.2 saiu, pelo spike do C5.
  Os botões chamam o MCP residente, e por isso só existem na fase 2, com o B6; até lá, o painel só mostra.
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
- **R7.2, R10.2, R11.1:** a arquitetura e o contrato vão a um `ARCHITECTURE.md`. O `DESIGN.md`, o design system da
  R6.2, saiu do PLN-003 e foi ao workstream `brand`, por uma issue de lá: o painel de componentes usa o tema do app.
- **R6.3:** a política mora num `brza.toml`, que o `AGENTS.md` cita.
- **R6.4:** o orquestrador decide o modelo do que abre e sugere à sessão principal, por aviso.
- **R7.1:** o semáforo é por conta e por runtime, pelo `usedPercent`.
- **R9.1–R9.4:** o coordenador do índice da `master` é este orquestrador. A fila ordena por `deadline` próximo, depois
  `blocks`, depois `priority`, depois a chegada. Worker novo só abre sob o menor de três tetos: o geral do workspace,
  somado entre as contas; o por conta e runtime da R7.1, que fica; e o da máquina. O ritmo da conta é o `usedPercent`
  projetado até o `resetsAt`: a conta que chega a 90% antes do reset não recebe worker novo. A máquina limita pela
  memória livre e pelo swap, e a CPU é o segundo sinal.

## Terreno

### O plugin do Orca

Reescrito em 2026-11-02 contra a `v1.4.246`, a base do fork, que é também a versão dos dois apps de Anderson (BrzA Studio `1.4.246-alpha.1`, Orca `1.4.246`, pelo `Info.plist`). A versão de 2026-10-29 era contra o Orca 1.4.244 e envelheceu em seis pontos, marcados **(envelheceu)**. `Fnn` é o fato do levantamento de 2026-11-02 (agregado no scratch, fora do git); a fonte vai ao lado, nos docs de `~/Projects/brza-studio/docs/reference/plugin-*.md` e no código na tag `v1.4.246`. Nada aqui foi rodado nos apps: o que não passou pelo spike do C5 é leitura.

**O que envelheceu**

- **(envelheceu) "Sem canal worker→painel".** Existe: o worker responde com `orca.panels.handle(nome, …)` e empurra com `orca.panels.post`; o painel pergunta com `plugin.request` e escuta com `plugin.on` (no frame HTML são os mesmos métodos, em `orca.plugin`). Pede `main` (`trusted-worker`) e sobe o worker sob demanda. Entrada de até 64 KiB, resposta de até 1 MiB, 30 s por pergunta (teto 120 s), posts de até 256 KiB e 200 por 10 s. Vale para os dois `ui` (`plugin-authoring.md:191-267`; `plugin-host-api.md`, `plugin.request`, desde a API 1.2) [F11, F103]. O "64 KB/msg, 30 msg/10 s" do Terreno antigo cai. O contorno "regravar `panel.html` com os dados embutidos" perde a razão de ser.
- **(envelheceu) O painel chama `terminal.sendText`.** Na 1.4.244 era `panel: true`; na 1.4.246 é só do worker, com o comentário "text plus Enter runs shell commands, so only full-access workers get it" (`src/shared/plugins/workers/plugin-host-api.ts:146-155`, tag `v1.4.246`; `plugin-host-api.md:16`) [F53]. O painel segue com `workspace.readContext`, `notifications.show`, `agents.list` e os eventos. **Consequência:** um plugin só `sandboxed-ui` não manda `brza` ao terminal; os botões da R1.2 exigem worker e `plugin.request`.
- **(envelheceu) O painel é `iframe srcdoc` com `connect-src 'none'`.** Na 1.4.246 o frame isolado vem ligado (`PLUGIN_ISOLATED_FRAMES_DEFAULT = true`, `src/main/plugins/panels/plugin-frame-isolation.ts:9`): um `<webview>` por plugin, partição própria, origem `orca-plugin-frame://<key>/`, rede negada na sessão e não por CSP, proxy de loopback que derruba conexão, WebRTC restrito, download e popup bloqueados (`plugin-isolated-frames.md:12-52`) [F36, F38]. A CSP do frame traz `connect-src 'self' data: blob:`; o `connect-src 'none'` ficou só no `srcdoc` dos clientes web ou com o frame desligado (`plugin-authoring.md:132-134`) [F39]. O HTML não é mais "relido a cada open, até 10 MB": o frame serve vários arquivos, documentos até 16 MiB, `.ts`/`.tsx` transpilados (`plugin-isolated-frames.md`, Serving e Source modules). O que sai do frame é só `orca.shell.openExternal` (clique e aviso por host novo) e `orca.files.saveAs` [F40]. **Inferência [inferido · 80]:** o painel não alcança `127.0.0.1`, porque o proxy fixado derruba até o loopback; então não fala com o MCP residente (R3.4); quem fala é o worker.
- **(envelheceu) "Fork só manifest 1".** O formato 2 é o novo: `manifestVersion: 2`, `execution` obrigatório, `engines.orca >=1.4.245` (`plugin-manifest.md:15-16,30`); o 1 ainda carrega (`:234`) [F97]. A base do fork é a 1.4.246, então o fork lê os dois. O Terreno dizia "Orca 1.4.244 aceita manifestVersion 2"; o doc diz desde a 1.4.245, e a divergência fica sem importância agora. **O `engines` do plugin do PLN-003 passa a `>=1.4.246`** (`ui`, `.ts`/`.tsx`, `settings` e omitir o `publisher` pedem a 1.4.246: `plugin-manifest.md:18,45` e a tabela de `panels`), no lugar de `>=1.4.242`, versão em que o sistema vinha desligado e sem documentação [F84, F95].
- **(envelheceu) "upstream/main renomeou storage→storage:own".** Já na 1.4.246 as capacidades são `workspace:read`, `agent:read`, `terminal:send`, `notifications:show`, `storage:own`, `secrets:own`, `settings:own` (`plugin-manifest.md:196`) [F13].
- **(envelheceu) Os eventos.** `worktree.created {worktreeId,path,branch}` e `worktree.removed` eram os da 1.4.244 (`v1.4.244:src/shared/plugins/plugin-events.ts:44`). Na 1.4.246 o doc lista `workspace.created {workspaceId, kind, path, branch}`, `workspace.removed`, `agent.status.changed {…, state: working|blocked|waiting|done, mainAgent?}` e `workspace.changed {context}`, que entrega o contexto atual a cada novo assinante (`plugin-host-api.md:175-190`) [F15]. `readContext` ganhou `title?` em cada terminal e continua sem caminho (`plugin-host-api.md:36-40`).

**O que segue valendo, sem reconferir** (de 2026-10-29): worker em `child_process.fork`, Node completo (`plugin-host-process.ts`); env só `PATH/HOME/LANG/TZ/TMP` (`plugin-worker-env.ts`; o levantamento confirma o recorte, `:1-16,44`, e que o worker não tem sandbox de arquivo nem de rede) [F50]; no máximo 5 workers e 30 s por comando; `sendText` exige terminal existente do worktree em foco e até 4096 caracteres; `pluginSystemEnabled=true` nos dois apps; `devPluginPaths` por app, hoje `[]` nos dois, mutável sem hash; consentimento por app. Não toquei no `~/.orca` para conferir.

**O que o worker pode fazer no host (API 1.2)**

- Ler o contexto do workspace em foco, listar agentes (`agents.list`) e ouvir o status deles, **digitar em terminal por id**, notificar, e usar `storage`/`secrets`/`settings` próprios [F14, F53]. Não abre workspace, não cria terminal, não lança agente, e não há hook que bloqueie prompt ou chamada de ferramenta [F54].
- **Só no `upstream/main`** (API 1.3, `engines.orca >=1.4.248`): `workspace.list/open`, `editor.open`, `commands.run`, `terminal.create/read`, `agent.launch`, `statusBar.update`; hooks `agent.tool.before` (que só bloqueia no Claude Code), `agent.prompt.before`, `agent.launch.before`, `terminal.send`, `workspace.create.before/after`, `editor.save.before`; `commands[].replaces`; capacidades `workspace:write`, `agent:launch`, `terminal:read` [F55–F60, F105–F108]. **Um plugin com esse `engines` não carrega no fork** enquanto a base for 1.4.246 [F94]. A orquestração (R4.1) fica no MCP e no `brza`.
- **Reservados e vazios, até no `upstream/main`:** `skills`, `mcpServers`, `agentHarnesses`, `taskSources`, `connections`, `sidebarCards` (`plugin-manifest.md:46-53`; `upstream/main:docs/reference/plugin-manifest.md`) [F8, F112]. `hooks` e `statusBarItems` também estão vazios na 1.4.246 e só existem no `upstream/main`. **O plugin do Orca não contribui skills nem MCP; o veículo é o plugin do Claude (R4.3, R4.4), e o plugin do Orca é só UI e eventos.**

**Segurança e consentimento (entram na análise de risco da fase 0)**

- `trusted-worker` só roda depois de aprovação explícita; pela CLI é `--approve <fingerprint>`, vindo de um `approval_required` anterior, sai com código 3 e a skill do Orca manda o agente nunca aprovar sem o pedido exato (`plugin-cli-approval.ts:36-66`; `plugin-authoring.md:493-494`) [F43, F46, F47, F63]. O fingerprint amarra capacidades e a confiança do worker [F45 · lido · 85]; update que pede acesso novo não instala e fica em "Update needs review" [F44].
- O worker tem o acesso do usuário. O `audit.log` registra só as chamadas à API do host (`plugin-audit-log.ts:3,22-23`) [F49]. O painel HTML é "trusted code" e roda no frame isolado.
- Pasta de desenvolvimento: salvar um painel ou um worker **não** pede aprovação de novo; subir capacidade ou perfil de execução, e mudar comando ou atalho, pede (`plugin-authoring.md:436-442`) [F68]. Isso responde, por documento e sem teste, a dúvida da R4 sobre regravar o `panel.html` "sem novo consentimento".

**Autoria e spike**

- O ciclo é do CLI do client: `plugin create --template panel|components|worker-panel`, `plugin dev watch --check --shot`, `plugin dev load|reload|request|emit`, `plugin test|check`, `plugin shot` (PNG do painel mesmo com a janela escondida) e `plugin open`; precisam do app desktop com um workspace aparecendo (`skill-guides/orca-plugin-authoring/references/cli.md:7-31`; `plugin-authoring.md:370-420`) [F61, F62, F64, F65]. No fork o shim `brza` e o `orca` são idênticos, byte a byte, e `ORCA_CLI_COMMAND` aponta ao launcher do app nos terminais gerenciados [F73, F76].
- A skill `orca-plugin-authoring` é embutida no binário e sobe pelo `ORCA skills get orca-plugin-authoring` [F70, F71].
- **Painel de componentes (`ui: "components"`):** módulo TSX que devolve uma árvore do catálogo do Orca (Stack, Text, Button, Table, Tree, Markdown, CodeView…), sem HTML, CSS nem hooks; hot reload preserva os átomos com chave (`plugin-declarative-ui.md:1-60`) [F9, F10]. O Orca o desenha com o tema e o teclado dele: o `DESIGN.md` da R6.2, que descreve um painel HTML, não vale para esse caminho.
- **Testado no spike de 2026-11-03**, nos dois apps: o painel e o `plugin.request`, o `plugin shot` e o `plugin dev` a partir do chat do Studio, o `terminal.sendText` do worker, o alcance do `127.0.0.1` e a cobertura do catálogo de componentes. O resultado está no C5, nos critérios de alocação.

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
- **C5 UI nos dois apps** → plugin do Orca. **Hipótese a medir no P0, reaberta em 2026-11-02** (era critério fixo):
  o Terreno envelheceu, e nada do painel foi testado nos apps. O spike, antes de o desenho do painel fechar, num plugin
  mínimo `trusted-worker`, `engines.orca >=1.4.246`, em pasta dev, pelo CLI do client (`plugin dev watch --check --shot`
  e `plugin shot`), com **dois painéis**, um `ui: "html"` e um `ui: "components"`, e rodado nos dois apps. Responde:
  1. o painel carrega e o `plugin.request` ao worker responde, nos dois apps;
  2. o worker lê planos e notas do worktree e o painel os mostra; o catálogo de componentes (Tree, Markdown, Table) cobre
     o que o HTML mostraria;
  3. o `terminal.sendText` do worker roda um `brza` no terminal em foco, achado pelo `readContext`;
  4. o painel não alcança `127.0.0.1` (inferido) e o worker alcança o MCP residente;
  5. regravar um arquivo do painel na pasta dev recarrega sem nova aprovação (o doc diz que sim);
  6. o `plugin shot` e o `plugin dev` funcionam com a janela escondida na sessão do chat do Studio;
  7. o custo da aprovação `--approve` por app e o que o worker faz que o `audit.log` não registra (entra na análise de
     risco da fase 0).

  Se o item 1 falhar em qualquer dos dois apps, o C5 volta à rodada.

  **O spike rodou em 2026-11-03 nos dois apps — BrzA Studio `1.4.246-alpha.1` e Orca `1.4.247` —, com o item 1
  aprovado nos dois: o C5 não volta à rodada.** O plugin é o de `spikes/c5-plugin/` (R8.1), aprovado pela CLI depois do
  "Aprovar nos dois apps" de Anderson. A evidência está no worklog
  [O PLN-003: o spike do C5 nos dois apps](../../work/worklogs/2026-11-03-pln-003-o-spike-do-c5-nos-dois-apps.md).
  1. **Passa nos dois.** Os dois painéis carregaram, e o `plugin.request` respondeu do worker: `ping` em 0,19 s (Node
     24.22.1), `settled: true`.
  2. **Passa no Studio; no Orca, só o caminho do erro.** No Studio, o worker achou o worktree pela branch em foco e leu
     planos e notas (`brand`: 1 plano e 4 issues; `tools-kit`: 2 planos e 10 notas), e o painel de componentes mostrou o
     mesmo que o HTML, com Tree, Table e Markdown. O `readContext` não traz caminho. No Orca, que só tem os repositórios
     da Fixfy, o painel mostrou o erro do worker ("a branch não é de um worktree do brza-workspace"): o `brza install`
     do plugin precisa cadastrar o `brza-workspace` no Orca. **Medido:** o painel HTML não herda o tema do app (texto
     claro em fundo branco no tema escuro); o de componentes herda.
  3. **Passa nos dois, com duas ressalvas.** O worker escolheu sozinho o terminal sem agente (R8.4), digitou `brza
     --version` e o terminal respondeu, nos dois apps, inclusive pelo botão do painel. **Ressalvas:** o workspace só
     com o chat não tem terminal — o agente do chat sai no `agents.list` com `terminalId: null` —, então o botão não
     tem onde digitar sem abrir um shell antes; e, no terminal do Orca, `brza` é o CLI do BrzA Studio, que vem antes no
     PATH do shell
     ([O CLI do Orca no chat do Studio fala com o Studio](../../work/issues/o-cli-do-orca-no-chat-do-studio-fala-com-o-studio.md)).
  4. **Confirmado nos dois.** O worker alcança `127.0.0.1` (HTTP 200, 15–17 ms). O frame html não alcança: a CSP
     `connect-src 'self' data: blob:` barra o `fetch` antes do proxy. Quem fala com o MCP residente é o worker.
  5. **Passa nos dois.** No Studio, o `dev reload` depois de salvar saiu `already-approved`, sem `needsReconsent`. No
     Orca, o `dev watch --check --shot` emitiu `reloaded`, `check` e `shot` ao salvar, e o painel mostrou "Reloaded". O
     fingerprint `ap1-…` ficou o mesmo depois das edições: ele amarra a pasta, a versão e o acesso, não o conteúdo.
  6. **Passa nos dois.** O `plugin shot` com a janela escondida saiu `settled: true`, sem erros, e a janela não voltou
     à frente. O CLI do Orca, de dentro do chat do Studio, só acha o Orca com o env limpo (a mesma issue do item 3).
  7. **Respondido ao vivo.** A aprovação é uma chamada de CLI por app, com o fingerprint que o `dev load` imprime. No
     modo auto, ela só passou depois da aprovação explícita de Anderson na conversa: sem isso, o classificador barra
     ([O --approve do plugin é barrado no modo auto](../../work/issues/o-approve-do-plugin-e-barrado-no-modo-auto.md)).
     O `audit.log` gravou a aprovação como `cli:local` e cada `terminal.sendText` só com `bytes=14`, sem o texto. Não
     gravou a leitura de `plans/` e `work/`, o `git worktree list`, o HTTP para `127.0.0.1` nem as chamadas de leitura
     (`readContext`, `agents.list`).

  Também saiu do spike:
  - o `dev watch` interrompido emite `unloaded`, mas deixa no `devPluginPaths` a pasta que um `dev load` anterior pôs
    ([O dev watch deixa carregado o plugin que já estava](../../work/issues/o-dev-watch-deixa-carregado-o-plugin-que-ja-estava.md));
  - o pacote da `1.4.246` e o da `1.4.247` não trazem os tipos de plugin
    ([Os tipos de plugin faltam no pacote da 1.4.246](../../work/issues/os-tipos-de-plugin-faltam-no-pacote-da-1-4-246.md));
  - o Orca se atualizou para a `1.4.247` ao fechar, e a base do fork ficou na `1.4.246`.
- **C6 Dentro do app** — `tool_use_id`/cartão, seletor nativo, estado sem RPC → app (fork); só BrzA; entra só sem contorno.
- **C7 Imposição** — regra cuja violação gasta cota, dinheiro ou cache e que cabe numa tabela → a norma declara a
  regra e a tabela, e o mcp (ou hook) impõe lendo a tabela. Regra de juízo fica só no texto (C1).
- **C8 Desempate** — vence a frente que roda no Orca upstream; com o mesmo "se paga", vence a mais barata.

### Base já decidida (R1–R4), frente fixa

| ID | Feature | Origem | Frente(s) e papel | h | Se paga | Orca? | Critério |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| B1 | `brza` próprio + detecção env → app vivo; canonicalize | R2.1, R2.2; F21, F22 | cli | 3–5 | fase 1, no 1º uso do Orca | sim | C2 |
| B2 | `tree`/`test` generalizados; `tree --list` órfãos | R2.3; F20 | cli | 4–6 +1 | fase 1 | sim | C2 |
| B3 | `install`/`doctor` no client detectado; ajuda; no Orca, cadastra o repositório do workspace, que o worker do painel precisa (C5, item 2) | R2.4; F25 | cli + `CLAUDE.md` (o que o install liga) | 1,5–2,5 | fase 1, 1ª sessão no chat do Orca | sim | C2, C1 |
| B4 | pacote pip+pipx+uv e brew | R3.1, R3.2 | cli | 4–6 | fase 1, 1ª instalação fora | — | C2 |
| B5 | `app install` pela release, `--from-source`, confirma antes | R3.3; F24 | cli | 3–3,5 | fase 1, 1ª máquina sem o repo | não (só o app BrzA) | C2 |
| B6 | servidor HTTP residente, launchd, porta, token, `brza mcp start/stop/status` | R3.4 | mcp + verbo na cli | 4–6 | fase 2 | sim | C3 |
| B7 | painel de componentes com worker: planos, notas e worklogs em Tree, Table e Markdown; os botões chamam o MCP (R10.3) | R1.2, R10.1, R10.3; F28 (painel) | plugin do Orca (painel e worker) + mcp (os verbos dos botões, fase 2) | 6–10, sem refazer com a R10 | fase 2 | sim | C5 |
| B8 | skills e hooks no plugin, `brza:`; raiz por env | R4.3 | plugin do Claude + `CLAUDE.md`/glossário | 3 +1 (raiz do `measure.py`/`check_notes.py`) | fase 1 | sim | C4 |
| B9 | piloto `workflows/*.js` (Terreno) | R4.4 | plugin do Claude | 2 | fase 2 | sim (medido no P0, H6) | C4 |
| B10 | shim npm/npx/pnpm | R3.1 | cli | 2 | fase 3 | — | C2 |

### O orquestrador (R4.1) fundido com as issues

Alternativas viáveis na coluna "Alt"; o porquê em uma linha.

| ID | Feature | Origem | Frente(s) e papel | Alt | h | Se paga | Orca? | Critério | Porquê |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| M1 | Ferramenta `dispatch`: pedido tipado (tarefa, classe consultor/executor, alvo, runtime/conta/modelo opcionais) | R4.1; F3, F11 (sem cartão), F12 | mcp decide + plugin do Claude (a definição do agente declara a classe) + `AGENTS.md` (os três papéis) | só cli `brza dispatch` sem estado | 2–3 | fase 2, no 1º encadeamento | sim | C3 + C1 | é a porta única do "coração"; sem estado não há fila |
| M2 | Roteador de sessão: achar por nome, abrir worktree+sessão, mandar, fechar; segue a norma de uma sessão por frente (sem trava de retomada) | R4.1; F1 (P7), F2, F3, F5 | cli (verbos `brza sessions list/send/close/open`) + mcp (escolhe) | `orca terminal` direto do mcp | 3 (P7) + 1,5 | fase 1 (cli) / fase 2 (mcp) | sim (`orca terminal`, `agent launch`) | C2 + C3 | o verbo serve ao terminal e ao Codex; a escolha precisa ver todas as sessões |
| M3 | Nome de sessão como chave (`pln-NNN-pX`), chat-namer, `/rename` | F4, F5, F28 | `plans/README.md` (convenção) + hook do plugin (nomeia no arranque) + cli `brza sessions rename` | só convenção | 1,5–2 | fase 1 | parcial, a medir (rename de aba pela CLI) | C1 + C4 | o roteador acha sessão pelo nome; nome solto quebra o roteamento |
| M4 | Escolha de runtime (Claude/Codex/agy) | R4.1; F10, F11 | mcp (regra) + cli `sessions open --agent` | ACP do app (F10 original) | 2–3 (+1 agy) | fase 3 | sim (`agent launch --agent`, `worker-start --agent`) | C3 | depende de M2 e de M8; Codex/agy ainda raros |
| M5 | Codex como cartão via agente Claude que roda `codex exec` | F6 | plugin do Claude (agent `brza:codex`, `-s read-only` por padrão) | M4 (sessão de terminal) | 1–1,5 | fase 2, 1ª revisão pelo Codex | sim | C4 | dá o cartão nativo sem tocar o app |
| M6 | Conta por chamada | R4.1; F13 | mcp decide; cli executa `claude -p` com `CLAUDE_CONFIG_DIR` (omitido na `systemDefault`); chat em repouso por RPC `agentSession.switchAccount` | flag de conta no fork | 2–4 | fase 2 (só consultor `-p`) / fase 3 (sessão) | sim (medido no P0, H2 e H3) | C3 | `agentSession.create` não tem conta; `-p` e `switchAccount` têm |
| M7 | Sinal de cota por conta | R4.1; F14 | cli `brza quota` (sobre `orca account list --json`) + mcp consome | ler o JSON no mcp sem verbo | 1,5 | fase 2 | sim | C2 | o verbo serve ao humano e ao Codex; o mcp só lê |
| M8 | Fila/semáforo persistente (SQLite stdlib): ordena por `deadline`, `blocks`, `priority` e chegada, lidos do índice da `master` (M24); worker novo só sob o menor de três tetos — o geral do workspace, somado; o por conta e runtime (R7.1), com o ritmo projetado até o `resetsAt` e o corte a 90%; e o da máquina, pela memória livre e o swap, com a CPU como segundo sinal | R4.1, R7.1, R9.2–R9.4 | mcp | global; só por conta; fila por chegada | 4–6, sem refazer com a R9 | fase 2, 1º choque de cota | sim | C3 | o `Coordinator.maxConcurrent` do Orca só vive em gates (terreno-orquestrador); a fila por chegada deixa o pedido que trava um plano atrás do que não trava |
| M9 | Modelo/esforço pela política "O modelo segue a tarefa" | R4.1; F16 (parte) | `AGENTS.md` (prosa) + arquivo de política (tabela) + mcp (impõe no que abre) | só norma; mcp lê a tabela do `AGENTS.md` | 1,5–2 | fase 2 | sim (`--model --effort`) | C7 | hoje a regra é só texto e a medição mostra Opus em tudo |
| M10 | Chave de desligamento por dimensão (modelo/esforço, agente, tudo → passthrough) | R4.1 | mcp (config) + cli `brza mcp config` | só env | 0,5–1 | fase 2 | sim | C3 | "pode ser desativado" é requisito do pedido |
| M11 | Agente interno que desempata: a cota fica na tabela; o texto vai ao `tev1:4b` local (Ollama, `/v1/systemone`) e, abaixo do limiar de confiança, ao Haiku (`claude -p --json-schema`, `--max-budget-usd`) — rodada de 2026-11-03, abaixo | R4.1, R5.1 | mcp | agente em toda chamada; regra pura; só o Haiku; Jev em nuvem, para quem não tem Ollama | 3–4 | fase 2b, quando a medição mostrar empate | sim | C3 | regra é grátis e instantânea; o `tev1` desempata em ~0,09 s, sem custo, e o Haiku paga só na dúvida |
| M12 | Quem chamou: header `X-Brza-Session: ${ORCA_AGENT_SESSION_ID}` + client | R3.4 (consequência); R4.1 | plugin do Claude (`.mcp.json` com `"type": "http"`) + mcp | argumento `caller` na ferramenta | 1–2 | fase 2 | sim (medido no P0, H1) | C4 + C3 | residente não herda `ORCA_*` |
| M13 | Ciclo de vida pelo `orca orchestration` (task, dispatch, worker-start, ask/reply, worker_done) | R4.1; F19 | mcp chama a cli do client detectado | reimplementar no mcp | 3–4 | fase 2 | sim | C3 + C8 | reaproveita o ciclo; o roteamento é nosso ("does not schedule or place workers") |
| M14 | O fim volta ao chamador (espera × aviso; turno ocioso) | F11 | mcp (via `worker_done`) | bloquear até o fim | 2–3 | fase 2 | sim | C3 | sem isso o executor vira fogo-e-esquece |
| M15 | Gate de aprovação (abrir executor, trocar conta) | conflito K3 | `AGENTS.md` (quando) + mcp devolve proposta + sessão principal pergunta | gate do `orca orchestration` | 1–2 | fase 2 | sim | C1 + C3 | preserva "quem pergunta é a principal" |
| M16 | Medição do roteamento + conserto da conta `home` | R4.1; AGENTS.md:93-94 | hook `measure.py` (conserto) + mcp (linha `route`) | — | 0,5 + 1,5 | fase 1 (conserto) / fase 2 | sim | C3 | "a política se revê pela medição"; hoje conta errada |
| M17 | Fila e sessões no painel: a ordem da fila com o motivo de cada posição (`deadline`, `blocks`, `priority`), e o teto que segura cada pedido parado — o do workspace, o da conta e runtime, com a projeção até o `resetsAt`, ou o da máquina | R4.1 + R4.2, R9.2–R9.4 | plugin do Orca (painel de componentes; o worker lê do mcp, R10.1) | — | 1–2 | fase 2 | sim | C5 | o semáforo invisível vira mistério; com três tetos, quem espera precisa saber qual segura |
| M18 | `codex_reply(thread, msg)` | F9 | mcp | `codex exec resume` pela cli | 1–2 | fase 3 | sim | C3 | estado da thread entre chamadas |
| M19 | Sandbox do Codex como argumento | F15 | mcp (impõe) | config do Codex | 1 | fase 3 | sim | C7 | a sandbox fica visível no `canUseTool` |
| M20 | Aviso ao celular (notify + hook Stop de turno longo; gate pendente) | F31, F32 | cli `brza notify` + hook do plugin + mcp chama | — | 2–3 | fase 3 | sim (macOS) | C2 + C4 | gate parado precisa chamar Anderson |
| M21 | "Selecionar automaticamente" no seletor | F16 | app | M9 cobre o que o orquestrador abre | 4–6 (não medido) | fora → issue | não | C6 | toca a principal, que segue "o de quem a abriu" |
| M22 | Passos do Codex dentro do cartão (`tool_use_id`) | F8, F11 (cartão) | app | — | ~15 | fora → issue | não | C6 | só BrzA, atrito de merge |
| M23 | `SHELL_SESSIONS_DISABLE=1` no `brza-run` | F26 | cli | — | 0,3 | fase 1 | sim | C2 | conserto pequeno no que o executor usa |
| M24 | O índice da `master` (`.brza/index.jsonl`) grava `priority`, `blocks` e `deadline` de plano, issue e decisão | R9.2; issue `o-coordenador-le-o-indice-da-master` (workspace) | cli (`brza note commit`, que acrescenta a linha) | o mcp lê o frontmatter de cada branch `workstream/*` | ~1 | fase 1, antes do M8 | sim | C2 | o índice é a visão de todas as frentes num arquivo só; ler as branches a cada pedido custa um `git show` por nota |

Saíram por não serem de fluxo ou por já resolvidos: F7 (flag experimental), F17 (feito), F18 (`ship`, já fora no
PLN-002), F22 (substituído por B1), F23 (bug do fork), F27 (telemetria), F29 (descartados com gatilho), F30 (não
descrita no inventário; não é de fluxo), F33 (Tailscale; o mcp escuta só em 127.0.0.1), F34 (funnel).

### O desempatador do M11 (rodada de 2026-11-03)

A medição é a do worklog
[O desempatador local do M11: o `tev1:4b` no lugar do Haiku](../../work/worklogs/2026-11-03-o-desempatador-local-do-m11.md),
do workstream `workspace` (commit `b67fcea`): a mesma sonda — 10 tarefas em texto livre para a camada e 5 escolhas de
conta por cota, nas duas ordens — no `qwen2.5:7b`, no `qwen2.5:14b`, no `tev1:4b` e no Haiku, num M5 Pro de 24 GB.

| | `qwen2.5:7b` | `qwen2.5:14b` | `tev1:4b` | Haiku |
| :-- | :-- | :-- | :-- | :-- |
| Camada pelo texto | 10/10 | 10/10 | 10/10 (PT e EN) | 10/10 |
| Conta, 5 casos × 2 ordens | 4/10 | 7/10 | 10/10 PT · 8/10 EN | 10/10 |
| Conta, 60 casos aleatórios | — | — | 53/60 PT · 53/60 EN | — |
| Latência mediana, carregado | ~1,1 s | ~2,6 s | ~0,09 s (2,4 s frio) | ~7 s |
| Memória carregado | 6,6 GB | 15 GB, com swap | 7,7 GB | 0 |
| Custo | 0 | 0 | 0 | ~US$ 0,0008 por chamada |

Rodada respondida em 2026-11-03, na sessão `bb0fd632` do `workspace`: **"tev1 + Haiku (Recomendado)"**. A opção dizia:
"Registrar no M11: a cota fica na tabela; o tev1 desempata o texto e manda ao Haiku quando a confiança ficar abaixo do
limiar; a Jev fica como opção de nuvem para o pacote público." Isso detalha a R5.1 ("a regra, e o agente desempata");
não é item `D`.

- **A cota é regra da tabela, não do agente.** O uso semanal e de 5 h, o teto de 90% e a margem de 5 pontos ficam no
  `brza.toml` (R6.3): nenhum modelo local acertou sempre, e o `tev1:4b` errou 7 de 60, todos no teto e na margem.
- **O desempate de texto vai ao `tev1:4b`**, um modelo de decisão do Ollama (`/v1/systemone`), que devolve a
  probabilidade de cada opção sem gerar texto, em ~0,09 s e com 7,7 GB carregado. É determinístico: a segunda rodada
  dos casos fixos deu o mesmo resultado.
- **Abaixo de um limiar de confiança, a chamada vai ao Haiku** por `claude -p --json-schema`, com `--max-budget-usd`.
  A confiança separa, mas não basta sozinha: em PT, mediana de 0,80 nos acertos e 0,37 nos erros, com acerto a 0,02 e
  erro a 0,66.
- **O limiar se calibra com empate real na fase 2b**: as 10 tarefas eram fáceis e as contas, sintéticas.
- **A licença do `tev1` não aparece na página do Ollama**, que também diz que idiomas fora do inglês não foram
  testados; confere-se antes do pacote público (B4).
- **A Jev, da TypeSafe AI**, é o mesmo formato de chamada, em nuvem: fica como backend opcional para quem não tem
  Ollama. Está em acesso antecipado, e a própria TypeSafe a diz fraca em precisão numérica — mais um motivo para a cota
  ficar na tabela.
- **As 3–4 h do M11 são de antes do `tev1`**, e não foram refeitas com o segundo backend.

### Regra × mecanismo (onde cada regra mora e quem a impõe)

| Regra | Texto em | Imposta por |
| :-- | :-- | :-- |
| O modelo segue a tarefa | `AGENTS.md` (prosa) | mcp lendo o arquivo de política (M9) |
| A ordem da fila: `deadline`, `blocks`, `priority`, chegada | `work/README.md` ("As propriedades") | mcp lendo o índice da `master` (M8, M24) |
| Uma frente, uma sessão | `AGENTS.md` | roteador (M2) reutiliza a sessão da frente (nova sessão só ao mudar de frente, > 200 mil tokens ou a pedido) |
| Cache de 1 h (sem trava de retomada) | `CLAUDE.md` | cache de 1 h na sessão principal; sem trava de retomada pelo roteador |
| Quem pergunta é a principal | `AGENTS.md` | mcp devolve proposta (M15); nunca pergunta |
| Nome de sessão | `plans/README.md` | hook do plugin (M3) |
| Abrir sessão nova pela própria sessão | `CLAUDE.md`/`AGENTS.md` | roteador (M2) vira o caminho padrão |
| Vocabulários de nota | `work/README.md` | `check_notes.py` (já) |

### ARCHITECTURE.md — proposta (R7.2)

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

O `DESIGN.md` no formato de design system para agentes de UI (o do Google Stitch) saiu do PLN-003 e foi ao workstream
`brand` (R10.2, R11.1).

## Hipóteses da fase 0 medidas no P0 (R7.3)

As seis hipóteses da fase 0 foram medidas em 2026-11-03 no passo P0
([O PLN-003: a medição das hipóteses da fase 0 (P0)](../../work/worklogs/2026-11-03-pln-003-medicao-das-hipoteses-p0.md)).
Todas foram confirmadas, com ajustes incorporados aos itens `D3` a `D7`.

- **H1 (sobre D3/D4 — M12) — CONFIRMADA (com ajuste em D3):** O Claude Code (`2.1.317`) e o `@anthropic-ai/claude-agent-sdk`
  (`0.3.284`) expandem `${ORCA_AGENT_SESSION_ID}` nos headers HTTP do `.mcp.json` em todas as requisições do protocolo
  (`server/discover`, `initialize`, `notifications/initialized`, `GET /mcp` SSE, `tools/list`, `tools/call`).
  - *Ajuste em D3:* o `.mcp.json` precisa declarar explicitamente `"type": "http"` (ou `"type": "sse"`); sem `"type"`, o
    Claude Code assume `stdio` e ignora o servidor HTTP.
- **H2 (sobre D4/D6 — M6, M11) — CONFIRMADA (com ajuste em D4 e D6):** O `claude -p --model haiku --effort low --output-format json --json-schema ... --max-budget-usd 0.01 --no-session-persistence`
  executa em processo desanexado sem TTY (`start_new_session=True` / `setsid()`, `stdin=DEVNULL`, `cwd=/tmp`, env mínimo de
  `launchd`) em 3,3–4,6 s com `CLAUDE_CONFIG_DIR` apontando aos perfis gerenciados (`~/.claude-adm` e `claude-profiles/<id>/home`).
  - *Ajuste em D6:* para a conta `systemDefault` (`~/.claude`), `CLAUDE_CONFIG_DIR` **deve ser omitido** do `env`; defini-lo
    explicitamente como `~/.claude` muda o sufixo de hash da chave no Keychain do macOS (`Claude Code-credentials-<hash>`)
    e falha com `OAuth session expired`.
  - *Ajuste em D4:* o plist do `launchd` deve incluir `~/.local/bin` no `PATH`.
- **H3 (sobre D6/D7 — M6) — CONFIRMADA (para sessão em repouso via RPC local, com ajuste em D6 e D7):** O método RPC
  `agentSession.switchAccount` no socket local (`orca-runtime.json`) troca a conta de uma sessão existente em repouso
  (`at-rest`), incrementando `fence` e copiando atomicamente o transcript `.jsonl` e a pasta de subagentes para o diretório
  `projects/` da conta de destino (`copyClaudeTranscriptsToAccount`), além de passar nos 15 testes de unidade de
  `claude-account-switch.test.ts` e `structured-agent-session-account-switch.test.ts`.
  - *Ajuste em D6 e D7:* `agentSession.switchAccount` é um método RPC do socket `orca-runtime.json` (exige `MutationEnvelope`),
    não um subcomando da CLI, e recusa troca enquanto um turno está ativo (`reason: "turnActive"`).
- **H4 (sobre D5 — M13) — CONFIRMADA (injetando `ORCA_AGENT_SESSION_ID` no subprocesso, com ajuste em D5):** Chamadas de
  leitura (`run-list`) funcionam sem variáveis `ORCA_*`, mas `run-create`, `task-create` e `task-update` exigem
  `ORCA_AGENT_SESSION_ID` no `env` do subprocesso para vincular a Run ao chat chamador sem cair em `no_active_sender_terminal`
  ou `consumer_fenced` (passar `--from orca_session_id:<id>` sem a variável no `env` é barrado com
  `session_caller_chat_not_declarable`).
  - *Ajuste em D5:* o daemon MCP injeta `ORCA_AGENT_SESSION_ID=<valor do header X-Brza-Session>` e `ORCA_USER_DATA_PATH` no
    `env` de cada subprocesso `orca orchestration`, usando `--task-title` e `--status completed`.
- **H5 (sobre D4 — B6) — CONFIRMADA (com ajuste em D4):** Um servidor MCP em Python 3 stdlib (~160 linhas com
  `http.server.ThreadingHTTPServer`) atende tanto o transporte **Streamable HTTP** (`POST /mcp` + `GET /mcp` SSE) quanto o
  **SSE legado** (`GET /sse` + `POST /messages`) no CLI e no SDK dos dois apps, sem dependências externas.
  - *Ajuste em D4:* usar obrigatoriamente `ThreadingHTTPServer` com `protocol_version = "HTTP/1.1"` e `Content-Length`,
    pois o Claude Code mantém uma conexão `GET /mcp` (SSE) aberta enquanto dispara `POST /mcp` (`tools/list`, `tools/call`)
    em paralelo.
- **H6 (sobre D3 — B9) — CONFIRMADA (com gramática exata em D3):** O `@anthropic-ai/claude-agent-sdk@0.3.284` dos dois apps
  carrega `workflows/*.js` de plugins locais e expõe a ferramenta nativa `Workflow` sem exigir flags extras de ambiente,
  executando subagentes via `await agent(...)` em `local_workflow`.
  - *Ajuste em D3:* o validador AST (Acorn) do Claude Code exige `export const meta = { ... }` literal no topo, proíbe
    qualquer outro `export` (como `export default`; usa-se `return` no nível superior do script) e define `phase("<título>")`
    como instrução simples e `await agent("<prompt>", { label, model, tools, schema })` com o prompt como 1º argumento.

## D1 — O repositório público e a CLI `brza` unificada — `brz-anderson/brza`, `~/.local/bin/brza` (P2, P3)

- **Origem:** R2.1, R2.2, R2.3, R2.4, R3.1, R3.2, R3.3, R5.3, B1, B2, B3, B4, B5, B10, M23.
- **Contexto:** Os comandos hoje vivem dispersos em `scripts/brza/` e dependem de caminhos locais. O usuário precisa de um
  comando único no PATH que funcione igual no BrzA Studio, no Orca e no terminal puro, distribuível via gerenciadores de
  pacotes públicos (`pipx`, `brew`, `npm`).

#### Como fica

1. **Repositório:** `brz-anderson/brza` concentra o código da CLI, do MCP, dos plugins e da documentação de arquitetura.
2. **Despacho hierárquico:** O executável `~/.local/bin/brza` implementa o seguinte algoritmo:
   - Se o subcomando é interno (`install`, `tree`, `test`, `app`, `doctor`, `mcp`, `quota`, `sessions`), executa internamente.
   - Se existe um binário executável `brza-<subcomando>` no PATH, repassa os argumentos a ele.
   - Se nenhuma das anteriores casar, detecta o app ativo (variáveis `BRZA_CLIENT`, env herdado ou processo vivo do Studio/Orca)
     e repassa a chamada ao CLI do respectivo client (`orca <subcomando>` ou `brza <subcomando>`).
3. **Distribuição:**
   - Pacote Python puro (stdlib, sem wheels compiladas): `pip install brza`, `pipx install brza`.
   - Fórmula Homebrew: `brew install brz-anderson/tap/brza`.
   - Shims npm/npx para comandos legados.
4. **Comandos universais:**
   - `brza tree <nome> [--rm] [--list]`: cria/remove worktree em qualquer repositório git com convenção padrão.
   - `brza test`: executa a suíte de testes detectada no repositório.
   - `brza app install [--from-source]`: baixa a release mais recente do GitHub e substitui o app desktop, com confirmação prévia.
   - `brza-run` mantém `SHELL_SESSIONS_DISABLE=1` para evitar saídas espúrias no terminal.

## D2 — O índice da `master` com propriedades de ordenação — `scripts/brza/brza-note` (P1)

- **Origem:** R9.2, M24.
- **Contexto:** A ordenação dos pedidos na fila do orquestrador precisa avaliar `deadline`, `blocks` e `priority` em milissegundos.
  Ler o frontmatter de cada branch `workstream/*` sob demanda custaria múltiplos comandos `git show` a cada tick do semáforo.

#### Como fica

1. O comando `brza note commit` (e `brza note new`) extrai os campos `priority`, `blocks` e `deadline` do frontmatter de notas,
   planos e decisões ao atualizar o branch do workstream.
2. Na sincronização com o índice geral (`.brza/index.jsonl` na branch `master`), cada registro JSON passa a conter:
   ```json
   {"id": "PLN-003", "title": "...", "status": "open", "priority": "high", "blocks": ["PLN-004"], "deadline": "2026-11-15", "workstream": "tools-kit"}
   ```
3. O orquestrador consome diretamente esse arquivo local para calcular as prioridades da fila sem overhead de git.

## D3 — O plugin do Claude com skills, hooks e workflows — `plugins/claude/` (P4, P11)

- **Origem:** R4.3, R4.4, B8, B9, M3, M5, M12, M20.
- **Contexto:** O Claude Code nos dois apps consome extensões via plugin formal (`.claude-plugin/plugin.json`). As ferramentas
  e convenções do workspace devem carregar em qualquer chat iniciado dentro de um worktree.

#### Como fica

1. Estrutura do plugin em `plugins/claude/`:
   ```
   plugins/claude/
   ├── .claude-plugin/plugin.json
   ├── .mcp.json
   ├── agents/
   │   └── codex.json
   ├── hooks/
   │   └── hooks.json
   ├── skills/
   │   ├── plan-runner/
   │   └── notes-checker/
   └── workflows/
       └── review.js
   ```
2. **Namespace:** Todas as skills expostas adotam o prefixo `brza:` (ex.: `brza:plan-runner`, `brza:notes-checker`).
3. **Agente Codex (M5):** O agente `brza:codex` roda `codex exec` com flags `-s read-only` por padrão para revisões de código
   isoladas sem poluir o contexto da conversa principal.
4. **Hooks:**
   - Hook de inicialização: renomeia a sessão para `pln-NNN-pX` ou slug do plano em foco (M3).
   - Hook `Stop` para turnos longos: emite alerta para o iPhone/iCloud via `brza notify` quando uma execução longa conclui (M20).
5. **Configuração MCP (`.mcp.json`, validado em H1):** Conecta ao servidor residente declarando obrigatoriamente `"type": "http"`
   (sem esse campo, o Claude Code assume `stdio` e ignora a URL):
   ```json
   {
     "mcpServers": {
       "brza-orchestrator": {
         "type": "http",
         "url": "http://127.0.0.1:4242/mcp",
         "headers": {
           "X-Brza-Session": "${ORCA_AGENT_SESSION_ID}"
         }
       }
     }
   }
   ```
6. **Gramática de `workflows/*.js` (validada em H6):** Os roteiros em `workflows/` seguem a gramática exigida pelo validador
   AST do Claude Code: `export const meta = { name, description, whenToUse, phases }` literal no topo do arquivo, nenhum outro
   `export` (resultado devolvido com `return` no nível superior do script), `phase("<título>")` como instrução simples e
   `await agent("<prompt>", { label, model, tools, schema })` com o prompt como 1º argumento posicional.

## D4 — O servidor MCP residente e contratos de chamada — `packages/mcp/` (P6, P8)

- **Origem:** R3.4, R4.1, B6, M1, M10, M12, M15, M16.
- **Contexto:** O orquestrador precisa de um ponto central com estado persistente que sirva ao mesmo tempo aos dois aplicativos,
  às sessões de chat e à CLI.

#### Como fica

1. **Daemon HTTP Local (validado em H1, H2 e H5):**
   - Processo residente em Python 3 stdlib baseado em `http.server.ThreadingHTTPServer` (`protocol_version = "HTTP/1.1"` e
     `Content-Length` explícito), escutando exclusivamente em `127.0.0.1:4242` (porta padrão com fallback automático) e
     atendendo tanto Streamable HTTP (`POST /mcp` + `GET /mcp` SSE concorrente) quanto SSE legado (`GET /sse` + `POST /messages`).
   - Gerenciado via `launchd` no macOS (`~/Library/LaunchAgents/com.brza.orchestrator.plist`, com `~/.local/bin` incluído em
     `EnvironmentVariables.PATH` para resolver o binário `claude` em subprocessos desanexados) e comandos de controle:
     `brza mcp start`, `brza mcp stop`, `brza mcp status`.
   - Autenticação por token Bearer armazenado em `~/.brza/runtime/mcp.token` com permissões `0600`.
2. **Ferramentas MCP expostas:**
   - `brza_dispatch(task, role, target, model?, effort?, account?)`: ponto único de despacho de tarefas.
   - `brza_status()`: retorna a visão consolidada da fila, dos workers em execução e dos limites vigentes.
   - `brza_config(key, value?)`: ajusta ou desativa dimensões da política (modelo, esforço, agente desempatador) (M10).
3. **Contratos e Gates (M15):**
   - Papel `consultant`: processa diretamente sem bloqueio.
   - Papel `executor` ou requisição de troca de conta: o MCP gera uma proposta e retorna ao chamador; a sessão principal é
     responsável por solicitar confirmação explícita ao usuário antes de autorizar.
4. **Medição (M16):**
   - Cada decisão de roteamento gera uma entrada de auditoria tipada `route` em `~/.brza/orchestrator.log`, permitindo aferição
     periódica e calibração das políticas.

## D5 — A fila de prioridade e os três tetos de concorrência — `packages/mcp/queue.py` (P7)

- **Origem:** R4.1, R7.1, R9.1–R9.4, M8, M13, M14.
- **Contexto:** Para evitar exaustão de cotas das contas de IA e travamento da máquina de desenvolvimento, o orquestrador
  precisa escalonar a entrada de novos workers considerando múltiplos recursos finitos.

#### Como fica

1. **Armazenamento:** Banco SQLite stdlib em `~/.brza/orchestrator.db` com tabelas `queue`, `workers` e `limits`.
2. **Critério de ordenação da fila (R9.2):**
   O próximo pedido a ser atendido é selecionado pela ordenação:
   1. `deadline` mais próximo (pedidos com data limite de entrega têm prioridade máxima).
   2. `blocks` (pedidos que bloqueiam o avanço de outras frentes têm preferência).
   3. `priority` decrescente (`high` > `medium` > `low`).
   4. Ordem cronológica de chegada (`timestamp`).
3. **Os três tetos de admissão (R9.3, R9.4):**
   Um novo worker só é disparado se satisfizer simultaneamente:
   - **Teto 1 (Workspace):** Total de workers concorrentes não ultrapassa a cota global configurada no workspace.
   - **Teto 2 (Conta e Runtime):** Consumo da conta não atingiu 90%. Projeta-se o ritmo de consumo (`usedPercent` atual em
     relação ao tempo restante até `resetsAt`); se a extrapolação indicar estouro de 90% antes do reset, a conta é congelada
     para novos workers.
   - **Teto 3 (Máquina):** Memória RAM disponível acima de 4 GB e swap estável. Se a CPU estiver sob estresse contínuo (>90%),
     novos disparos aguardam janela de alívio.
4. **Ciclo de vida (validado em H4):** O ciclo é integrado via `orca orchestration` (`run-create`, `task-create --task-title ... --spec ...`,
   `task-update --status completed` e `worker-start`) e sinalizado ao chamador através de `worker_done` (M13, M14). Ao invocar a
   CLI do client em subprocesso, o MCP injeta no `env` o `ORCA_AGENT_SESSION_ID` recebido no header `X-Brza-Session` (H1) e o
   `ORCA_USER_DATA_PATH` do client ativo, garantindo o vínculo da Run com o chat chamador sem depender de terminal ativo.

## D6 — A política de modelos, esforço e o desempatador `tev1` + Haiku — `brza.toml` e `packages/mcp/policy.py` (P8, P9)

- **Origem:** R5.1, R6.3, R6.4, R7.1, M6, M7, M9, M11.
- **Contexto:** "O modelo segue a tarefa" (AGENTS.md). Modelos caros (Opus) só devem ser acionados para tarefas analíticas
  ou orquestração de alto nível; tarefas mecânicas ou de código repetitivo devem rodar em modelos rápidos (Sonnet/Haiku), sob
  controle de cota rígido.

#### Como fica

1. **Configuração `brza.toml`:**
   ```toml
   [orchestrator]
   max_workspace_workers = 6
   
   [policy.roles.consultant]
   default_model = "sonnet"
   default_effort = "low"
   
   [policy.roles.implementer]
   default_model = "sonnet"
   default_effort = "medium"
   
   [policy.roles.architect]
   default_model = "opus"
   default_effort = "high"
   
   [quota.limits]
   soft_cap_percent = 55
   hard_cap_percent = 90
   reset_margin_hours = 6
   ```
2. **Desempate em duas etapas (M11):**
   - **Etapa 1 (Tabela & Regras):** Checagem determinística de parâmetros (tipo de tarefa, tamanho do diff, cota disponível).
   - **Etapa 2 (Decisão Local):** Se a classificação de texto permanecer ambígua, o MCP consulta o modelo de decisão local
     `tev1:4b` via endpoint Ollama (`/v1/systemone`, latência ~0.09s, custo zero).
   - **Fallback Haiku (validado em H2):** Se o escore de confiança do `tev1` ficar abaixo de 0,75, o pedido é repassado ao Haiku
     via `claude -p --model haiku --effort low --output-format json --json-schema ... --max-budget-usd 0.01 --no-session-persistence`.
3. **Seleção de conta por chamada (M6, validada em H2 e H3):**
   - Em chamadas `claude -p` (consultor ou desempatador Haiku), os perfis gerenciados recebem `CLAUDE_CONFIG_DIR` apontando ao
     diretório `home` do perfil (`~/.claude-adm` ou `claude-profiles/<id>/home`), enquanto para a conta `systemDefault`
     (`~/.claude`) a variável `CLAUDE_CONFIG_DIR` **deve ser omitida** do `env` para preservar a leitura de `"Claude Code-credentials"`
     no Keychain do macOS.
   - Em sessões de chat existentes, a troca de conta usa o método RPC `agentSession.switchAccount` no socket local do client e
     só pode ocorrer com a sessão em repouso (`at-rest`).

## D7 — O roteador de sessões e integração de runtimes — `scripts/brza/brza-sessions` e MCP (P12)

- **Origem:** R4.1, M2, M4, M18, M19.
- **Contexto:** As tarefas podem demandar Claude, Codex ou Antigravity CLI. O roteador deve localizar e reutilizar sessões
  abertas sem criar worktrees desnecessários.

#### Como fica

1. **Sessão por frente:** O roteador busca sessões abertas associadas à frente/worktree atual. Uma nova sessão só é criada
   ao mudar de plano/assunto, se o contexto passar de ~200 mil tokens, ou sob solicitação explícita.
2. **Troca de conta em sessão existente (validada em H3):** Quando o orquestrador reutiliza uma sessão de chat aberta em outra
   conta Claude, aguarda a sessão ficar em repouso (`at-rest`) e invoca o método RPC `agentSession.switchAccount` diretamente
   no socket `orca-runtime.json` do client com `MutationEnvelope` (que copia os transcripts `.jsonl` e subagentes para a conta
   de destino antes do próximo turno `--resume`); se a sessão estiver com turno ativo (`turnActive`), o roteador aguarda o fim
   do turno ou abre nova sessão.
3. **Suporte a runtimes:**
   - `brza sessions open <nome> --agent claude|codex|agy`.
   - No runtime Codex: controle do canal via `codex exec`, com argumentos de sandbox isolados (M19) e suporte a continuidade
     de conversas via `codex_reply` (M18).
4. Saída JSON estendida e estável para consumo do orquestrador via CLI.

## D8 — O plugin do Orca com painel de componentes declarativo e integração MCP — `plugins/orca/` (P10)

- **Origem:** R1.2, R10.1, R10.3, B7, M17, C5.
- **Contexto:** Validado no spike do C5: o painel declarativo em TSX (`ui: "components"`) integra-se perfeitamente aos temas
  escuro e claro de ambos os apps e renderiza árvores e tabelas complexas sem as falhas de tema do HTML puro.

#### Como fica

1. **Manifesto (`orca-plugin.json`):**
   ```json
   {
     "manifestVersion": 2,
     "name": "brza-workflow",
     "version": "1.0.0",
     "engines": {
       "orca": ">=1.4.246"
     },
     "execution": {
       "main": "out/worker.js",
       "mode": "trusted-worker"
     },
     "ui": {
       "type": "components",
       "entry": "out/panel.js"
     },
     "capabilities": [
       "workspace:read",
       "terminal:send",
       "notifications:show"
     ]
   }
   ```
2. **Componentes visuais (TSX):**
   - Árvore de navegação de planos e workstreams (`Tree`).
   - Tabela de notas e status (`Table`).
   - Visão consolidada da fila do orquestrador: pedidos pendentes, prioridade calculada e indicador explícito de qual dos
     três tetos (workspace, cota ou máquina) está retendo cada item (M17).
   - Renderização rica de markdown para leitura rápida (`Markdown`).
3. **Comunicação e Ações:**
   - O worker lê o contexto do worktree da branch ativa em disco.
   - O worker consulta o MCP residente em `http://127.0.0.1:4242` para obter o estado das filas e cotas.
   - Botões de ação do painel invocam comandos do MCP via requisições HTTP internas disparadas pelo worker (R10.3).

## D9 — As atualizações na norma do workspace e contrato de arquitetura — `AGENTS.md`, `CLAUDE.md`, `ARCHITECTURE.md` (P5)

- **Origem:** C1, R4.3, R7.2, R9, R10.2, R11.1.
- **Contexto:** Garantir que agentes e desenvolvedores sigam as convenções duráveis do orquestrador, mantendo a integridade
  do modelo de trabalho.

#### Como fica

1. **`ARCHITECTURE.md`:** Documento durável alocado no repositório público `brz-anderson/brza` detalhando os contratos entre
   as frentes (CLI, MCP, Plugin Claude, Plugin Orca) e as garantias de compatibilidade.
2. **`AGENTS.md`:**
   - Formalização dos três papéis: consultores (sem gate), executores (com gate de aprovação da sessão principal), e arquitetos.
   - Fixação da regra "O modelo segue a tarefa", referenciando o arquivo declarativo `brza.toml`.
   - Confirmação da norma "Uma frente, uma sessão; uma tarefa, um worklog".
3. **`CLAUDE.md`:**
   - Definição do uso de skills com prefixo `brza:`.
   - Documentação do cache estendido de 1 h e ausência de trava de retomada.

