---
status: open
phase: interview
origin: request
ready: não — falta desenhar o orquestrador (R4.1) e escrever o Desenho
scope:
  - workspace
  - brza-studio
opened: 2026-10-29
owner: Anderson
tags:
  - tooling
---

# PLN-003: O workflow do workspace roda igual no BrzA Studio e no Orca, por plugins e pelo `brza`

- **Retomar:** as rodadas 1 a 5 fecharam o escopo, a CLI, a distribuição, o painel, as skills, os roteiros e o
  orquestrador. A matriz feature × frente está no scratch da sessão e vai ao Desenho. A rodada 6 mandou o P7 a uma sessão
  nova, `pln-002-p7`. Falta a rodada 7 — o escopo do semáforo e a casa da arquitetura e do contrato — e então o Desenho.

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

### Cobertura

> Rascunho: os critérios são propostas até a rodada que os confirma; o passo e o teste saem do Desenho.

| Origem     | Critério de aceite                                                                                      | Passo | Teste (nível) |
| :--------- | :------------------------------------------------------------------------------------------------------ | :---- | :------------ |
| `Pedido 1` | o mesmo `orca-plugin.json` instala nos dois apps e mostra o painel do workspace com planos e notas abertos | —     | —             |
| `Pedido 1` | os comandos do plugin mandam o `brza` certo ao terminal do worktree em foco                             | —     | —             |
| `Pedido 2` | o plugin do Claude traz as skills, os hooks e o MCP do workspace, e sobe nos chats dos dois apps          | —     | —             |
| `Pedido 2` | o plugin traz roteiros de Workflow do Claude Code para o fluxo do workspace                               | —     | —             |
| `Pedido 4` | `pipx install brza` e `brew install brz-anderson/tap/brza` instalam o CLI, com o `brza` e os `brza-*` no PATH | —     | —             |
| `Pedido 4` | `brza app install` baixa o DMG da release e troca o app; `--from-source` compila da `origin/master`            | —     | —             |
| `Pedido 4` | `brza mcp start`, `stop` e `status` controlam o servidor residente                                           | —     | —             |
| `Pedido 3` | `brza <sub>` acha o app que está rodando — BrzA Studio ou Orca — sem caminho fixo                        | —     | —             |

## Entrevista

### Rodada 1 — o escopo (enviada 2026-10-29)

**Apresentado antes:**
- **O sistema de plugins do Orca existe e é do upstream**, herdado pelo BrzA Studio: manifesto `orca-plugin.json`
  (`brza-studio/src/shared/plugins/plugin-manifest.ts`), com `panels`, `commands`, `events`; capacidades fechadas —
  `workspace:read`, `terminal:send`, `notifications:show`, `storage`, `secrets`, `events:subscribe`, `settings:own`
  (`plugin-capabilities.ts:7-15`). Nenhuma lê arquivo nem chama o CLI. Cada app lê o próprio `userData`.
- **A CLI `brza` fora do app só serve ao BrzA Studio**: caminhos fixos em `scripts/brza/brza_runtime.py:15-23`; dentro
  de um terminal de qualquer app, `cli_command()` e `user_data()` já seguem `ORCA_CLI_COMMAND` e `ORCA_USER_DATA_PATH`.
  O despacho `brza X` → `brza-X` só existe no fork (`brza-studio/src/cli/external-subcommand.ts`).
- **Não há MCP próprio** (`AGENTS.md`, `CLAUDE.md`); a issue `codex-como-subagente-no-chat-do-claude.md` propõe um.
- **O PLN-002 está bloqueado no P7** (`brza sessions`).

Respondida em 2026-10-29, no chat do BrzA Studio.

1. **O que é o "Workflow".** Opções:
   - o fluxo do workspace — planos, notas, worklogs, sessões, os `brza-*` (recomendada). Custo: ~0,5 h para delimitar.
     Se paga: no desenho do MCP;
   - o recurso Workflow do Claude Code, roteiros `agent()` no plugin. Custo: alto. Se paga: só para roteiros multi-agente
     pelo app;
   - os dois. Custo: dobra o escopo. Se paga: numa fase posterior.

   **Decidido — os dois.**

2. **O que o plugin do Orca faz.** Opções:
   - painel com planos, notas e worklogs abertos, mais comandos que mandam `brza` ao terminal; o mesmo manifesto nos
     dois apps (recomendada). Custo: ~6–10 h, mais ~1 h para medir o fs do worker antes. Se paga: na 1ª versão, nos dois
     apps;
   - só comandos e eventos. Custo: ~3 h. Se paga: agora, sem a visão do estado do workspace;
   - sem plugin do Orca. Custo: ~0. Se paga: se a interface do app não for o objetivo.

   **Decidido — painel e comandos.**

3. **O que o MCP expõe.** Opções:
   - as operações do fluxo, tipadas sobre o `brza_runtime`, em stdio, no plugin do Claude (recomendada). Custo: ~1–2 h
     por ferramenta. Se paga: quando a ferramenta com schema bater o Bash;
   - só o que a CLI não alcança — estado do app, `agentSession`, cartões no chat. Custo: ~4 h. Se paga: no 1º uso;
   - um MCP dentro do app. Custo: alto, muda o fork. Se paga: depois, e só no BrzA Studio.

   **Resposta:** "meça prós e contras dos 3 e registre no plano" — as três vão ao Desenho como alternativas medidas, e a
   escolha volta numa rodada.

4. **Onde o plano mora.** Opções:
   - `PLN-003`, sem depender do P7 do PLN-002 (recomendada). Custo: retrabalho se o P7 mudar o contrato. Se paga: agora;
   - `PLN-003` com a parte de sessões depois do P7. Custo: espera a 2d. Se paga: quando o P7 fechar;
   - estender o PLN-002. Custo: plano bloqueado fica maior. Se paga: nunca.

   **Decidido — `PLN-003`, sem depender do P7.**

### Rodada 2 — a CLI `brza` nos dois clients (enviada 2026-10-29)

**Apresentado antes:**
- **Dentro de um terminal ou chat de qualquer app**, `cli_command()` e `user_data()` seguem `ORCA_CLI_COMMAND` e
  `ORCA_USER_DATA_PATH` (`scripts/brza/brza_runtime.py:31-36`); fora deles, caem no BrzA Studio fixo (`:18-20`).
- **O despacho `brza X`** só existe no fork; o Orca não tem `brza` no bundle, e `orca sessions` dá `Unknown command`.
- **O `brza app`, `dev`, `tree` e `test`** exigem o `git-common-dir` do `brza-studio` (`brza-dev:54`, `brza-test:57`).
- **O `brza install --chat-command`** grava o `agentCmdOverrides.claude` só no BrzA Studio, e o doctor confere só lá
  (`brza-doctor:103-112`).

Respondida em 2026-10-29, no chat do BrzA Studio.

1. **Como o `brza` acha o client fora do app.** Opções:
   - o env do app, depois `BRZA_CLIENT=studio|orca`, depois o app cujo `orca-runtime.json` tem pid vivo, depois o BrzA
     Studio; com os dois vivos e sem `BRZA_CLIENT`, falha e pede a escolha (recomendada). Custo: ~2–3 h com testes. Se
     paga: agora, nos terminais de fora;
   - só `BRZA_CLIENT` explícito, com o BrzA Studio de padrão. Custo: ~1 h, e o valor mantido no shell. Se paga: se o
     Orca quase não for usado fora do app;
   - só o env do app. Custo: zero. Se paga: se o Orca for usado só pelo terminal dele.

   **Decidido — o env, depois o app vivo.**

2. **Como o workflow chama os comandos no Orca.** Opções:
   - um `brza` do workspace em `~/.local/bin`, que despacha aos `brza-*` e repassa o resto ao CLI do client detectado;
     no chat do BrzA Studio o `bin` do app vence no PATH (recomendada). Custo: ~1–2 h e um teste de PATH nos dois apps.
     Se paga: no 1º uso do Orca como client;
   - `brza-X` direto no Orca. Custo: zero agora; as skills ficam com duas formas. Se paga: se o Orca for secundário;
   - PR do despacho ao upstream. Custo: revisão externa, sem prazo. Se paga: improvável.

   **Decidido — o `brza` próprio em `~/.local/bin`.**

3. **O `app`, `dev`, `tree` e `test` no Orca.** Opções:
   - ficam só do BrzA Studio, com mensagem clara no Orca; o workflow nos dois clients é `note`, `sessions`, `run`,
     `doctor`, `install` (recomendada). Custo: ~0,5 h. Se paga: agora;
   - generalizar o `tree` e o `test` para qualquer repositório aberto no client. Custo: ~4–6 h, e mexe no que o PLN-002
     fixou para eles (R1.2, R1.4 de lá). Se paga: quando outro repositório for trabalhado pelo mesmo fluxo.

   **Decidido — generalizar o `tree` e o `test`.** O `app` e o `dev` ficam só do BrzA Studio.

4. **O `install` e o `doctor` no Orca.** Opções:
   - agem no client detectado, com `--client studio|orca|all` (recomendada). Custo: ~1–2 h. Se paga: na 1ª sessão do
     workspace aberta pelo chat do Orca, que hoje subiria sem hooks nem identidade;
   - sempre nos dois. Custo: ~1 h; mexe no Orca mesmo sem uso. Se paga: se os dois forem usados todo dia.

   **Decidido — no client detectado, com `--client`.**

### Rodada 3 — a distribuição do CLI (enviada 2026-10-29)

**Apresentado antes:**
- **Os 10 scripts são Python só com a biblioteca padrão**; o macOS está preso em `brza_runtime.py:63` (`AF_UNIX`),
  `brza-run:31` (`pty`) e em `brza-app` e `brza-doctor` (`/Applications`, `plistlib`).
- **O nome `brza` está livre** no npm, no PyPI e no Homebrew core (404 nos três registros, 2026-10-29).
- **O `brza-studio` é público**, com a release `v1.4.242.alpha.1` em pré-release e CI de build para mac e Windows;
  o `brza app install` de hoje compila da `origin/master`.
- **O MCP stdio não tem processo próprio**: o `claude` o inicia e encerra por sessão; iniciar e parar só tem sentido
  literal num servidor residente.

Respondida em 2026-10-29, no chat do BrzA Studio.

1. **Quem instala pelos gerenciadores.** Opções:
   - público, por fases: pip, pipx e uv (PyPI) e brew (tap `brz-anderson/homebrew-tap`), só macOS; depois npm, npx e
     pnpm; o winget depois do porte para Windows (recomendada). Custo: ~4–6 h na fase 1, e o cuidado de não vazar caminho
     pessoal no pacote. Se paga: na 1ª instalação fora desta máquina;
   - os cinco canais já. Custo: ~20–30 h, com o porte para Windows e um binário por plataforma. Se paga: só com usuário
     Windows em vista;
   - só para Anderson, sem registro: pipx e uv do git e a fórmula num tap. Custo: ~2 h. Se paga: agora, sem outros
     instalarem.

   **Decidido — público, por fases.**

2. **A forma do pacote.** Opções:
   - Python stdlib com shims: `pyproject` com o console script `brza` e os `brza-*`; a fórmula do brew instala do PyPI; o
     pacote npm é um shim que chama o `python3` (recomendada). Custo: ~4 h; o npm exige `python3` na máquina. Se paga: na
     fase 1, sem reescrever as 1855 linhas nem os testes;
   - reescrever em TypeScript, com binário único por `bun build --compile`. Custo: ~20–25 h. Se paga: quando o winget e o
     npm pesarem mais que o pip;
   - binário único do Python (PyInstaller) por plataforma. Custo: ~8–10 h de CI, e assinatura no macOS. Se paga: na fase
     do winget.

   **Decidido — Python stdlib com shims.**

3. **De onde o `brza` instala e atualiza o app.** Opções:
   - da release do GitHub, com `--from-source` para o build da `origin/master` de hoje (recomendada). Custo: ~3 h no CLI
     e uma release com DMG por versão; sem assinatura nem notarização, o Gatekeeper avisa. Se paga: na 1ª máquina sem o
     repositório;
   - só build da fonte. Custo: ~0. Se paga: só enquanto for Anderson, nesta máquina;
   - cask no tap, chamado pelo `brza`. Custo: ~2 h e a release com DMG; só macOS. Se paga: se o brew for o canal
     principal.

   **Decidido — a release, com `--from-source`.**

4. **O que é iniciar e parar o MCP.** Opções:
   - stdio: o `claude` inicia por sessão; `brza mcp enable|disable|status` liga e desliga no projeto, e `brza mcp serve`
     roda à mão (recomendada). Custo: ~1 h. Se paga: agora, sem processo residente;
   - HTTP residente: servidor local no `launchd`, com `brza mcp start|stop|status`, comum às sessões e aos apps. Custo:
     ~4–6 h, mais porta, token e o serviço do `launchd`. Se paga: se várias sessões precisarem de estado comum.

   **Decidido — HTTP residente.** Consequência a levar ao Desenho: o servidor não herda o `ORCA_*` do chat, então acha o
   client pela detecção da R2.1 e precisa saber de que sessão vem cada chamada.

### Rodada 4 — o MCP, o painel, as skills e os roteiros (enviada 2026-10-29)

**Apresentado antes:**
- **Plugin do Orca:** o worker é Node completo, sem sandbox (`brza-studio/src/main/plugins/plugin-host-process.ts`); o
  painel é iframe com `connect-src 'none'` (`src/shared/plugins/plugin-panel-shell.ts:9`), sem canal do worker para ele
  (`plugin-host-protocol.ts`), e chama só `readContext` (sem o caminho), `terminal.sendText` e `notifications.show`. Os
  dois apps têm o mesmo sistema, ligado; o Orca 1.4.244 aceita também o manifesto v2, o fork só o v1.
- **MCP:** o chat dos dois apps sobe o `claude` pelo SDK com `settingSources` de projeto
  (`src/main/claude/claude-structured-launch-resolution.ts:43,74`), sem injetar MCP; o `rpc()` respondeu contra o Orca
  1.4.244. A1 ~9 h, A2 com a premissa caída, A3 ~10–27 h só no fork. Com o HTTP residente, o servidor não herda o
  `ORCA_*` do chat.
- **Plugin do Claude:** carrega skills, hooks, `.mcp.json` e `workflows/*.js` (campo `@internal` no binário 2.1.292);
  `env` e `promptCacheTtl` não vão no plugin; `check_notes.py:54` e `measure.py:70-73` acham a raiz pelo `__file__`.

Respondida em 2026-10-29, no chat do BrzA Studio.

1. **A forma do MCP.** Opções:
   - A1, as operações do fluxo, 1ª leva c2, c3 e c1 (recomendada). Custo: ~9 h, mais ~4–6 h do HTTP e a norma. Se paga:
     no 1º c2 ou c3 pelo chat, nos dois apps;
   - A2, o MCP fino. Custo: ~5 h, mais HTTP e norma. Se paga: no 1º c3; vira um A1 recortado;
   - A3, o MCP dentro do app. Custo: ~10–12 h no fork, ~15 h a mais com cartão; nada no Orca. Se paga: só com o cartão de
     subagente pedido;
   - nenhum MCP agora. Custo: 0. Se paga: agora; o c3 espera o P7.

   **Resposta:** "o MCP é o orquestrador/coordenador, é por ele - rodando um agente - que decide qual sessão chamar, com
   qual conta e por qual runtime, funcionando como um semaforo enfileirando chamadas, tbm decide o modelo/esforço da
   sessão (pode ser desativado), em resumo, é o coração do fluxo". Leitura: contraproposta — o MCP deixa de ser uma
   fachada da CLI e vira o coordenador do fluxo, com um agente que roteia por sessão, conta, runtime, modelo e esforço, e
   uma fila. Vai ao levantamento do que o Orca já orquestra e a uma rodada de esclarecimento.

2. **Como o painel mostra planos, notas e worklogs.** Opções:
   - HTML regenerado com os dados embutidos, o plugin em `devPluginPaths` nos dois apps, botões que mandam `brza` ao
     terminal (recomendada). Custo: ~1 sessão de protótipo para provar a remontagem sem novo consentimento. Se paga: no
     protótipo; se falhar, cai na segunda;
   - só botões de `brza`. Custo: ~3 h. Se paga: agora, sem a visão do estado;
   - API push no fork e PR ao upstream. Custo: alto; o manifesto diverge até o upstream aceitar. Se paga: só se o
     contorno não bastar.

   **Decidido — HTML regenerado, na pasta dev.**

3. **Onde moram as skills e os hooks.** Opções:
   - no plugin, com o `.claude/` só com o `settings.json`; namespace `brza:`, raiz por argumento ou env (recomendada).
     Custo: ~3 h, mais `AGENTS.md`, `CLAUDE.md` e o glossário. Se paga: quando o plugin for a fonte única nos dois apps;
   - tudo em `.claude/`, o plugin só com MCP e roteiros. Custo: ~1 h. Se paga: agora, sem levar as skills adiante;
   - duplicar. Custo: ~1 h e divergência. Se paga: nunca.

   **Decidido — no plugin.**

4. **Os roteiros de Workflow.** Opções:
   - piloto em `workflows/*.js` do plugin, o levantamento do Terreno antes dos outros (recomendada). Custo: ~2 h, e o
     risco do `@internal`, mitigado pinando a versão do `claude`. Se paga: no 1º roteiro nos dois apps;
   - só `.claude/workflows/`. Custo: ~1 h. Se paga: agora, sem levar ao público;
   - adiar. Custo: ~0. Se paga: quando a doc cobrir.

   **Decidido — piloto em `workflows/*.js`.**

### Rodada 5 — o orquestrador e as frentes (enviada 2026-10-29)

**Apresentado antes:** depois da R4, Anderson pediu: "sobre a resposta da forma do MCP, meça todas as sugestões
propostas por mim + as sugestões que já estão nas issues e sugira quais features são melhores em qual frente
cli|mcp|plugin|app", e em seguida: "considere tbm que parte da norma de fluxo de trabalho do workspace pode ficar nos
arquivos AGENTS/CLAUDE/DESIGN do próprio workspace". A medição juntou:
- **O que o Orca já orquestra:** a `orchestration` (run, task, dispatch, `worker-start --agent --model --effort`,
  ask/reply, gates) não agenda nem limita concorrência ("does not schedule or place workers", `orca orchestration
  run-create --help`); o `Coordinator` com `maxConcurrent` 4 só é criado pelos gates
  (`brza-studio/src/main/runtime/orchestration/coordinator.ts:37`). O `orca account list --json` dá o uso por conta
  (5 h, semanal). A conta não se escolhe por chamada: o `agentSession.create` não tem campo de conta, e o
  `agentSession.switchAccount` não foi testado. O `claude -p` com `CLAUDE_CONFIG_DIR` é o agente interno sem
  dependência, com precedente em `fixfy/scripts/delegate.py:186`.
- **O inventário das notas:** 34 sugestões (F1–F34), a maior parte da issue
  [O Codex como subagente no chat do Claude](../../work/issues/codex-como-subagente-no-chat-do-claude.md).
- **Os critérios de alocação**, aplicados na ordem: juízo vai à norma; o que roda fora do Claude vai à CLI, que é o
  núcleo; estado comum vai ao MCP; ciclo do Claude ao plugin do Claude; interface nos dois apps ao plugin do Orca; o
  que só se faz dentro do app vai ao app; regra que gasta cota e cabe numa tabela é declarada na norma e imposta pelo
  MCP; no empate, vence o que roda no Orca.
- **As fases:** 0, medir 7 riscos (~3–4 h); 1, CLI, plugin do Claude e norma, sem servidor (~31 h); 2, o MCP
  coordenador só com o runtime Claude (~48 h); 3, outros runtimes e contas (~13 h). A matriz vai ao Desenho.
- **Os conflitos:** a autonomia do orquestrador contra `AGENTS.md` "Uma tarefa, uma sessão" e "Quem pergunta e grava é
  a sessão principal"; o plugin público e o servidor residente contra "O ferramental vive só no escopo do projeto"; o
  correio sem trava de retomada (`CLAUDE.md`) num orquestrador que manda prompt; o roteador e o P7 do PLN-002.

Respondida em 2026-10-29, no chat do BrzA Studio.

1. **Quem decide no orquestrador.** Opções:
   - a tabela de política decide, e um agente Haiku por `claude -p --json-schema` só desempata, atrás da chave
     (recomendada). Custo: ~1,5–2 h de regra e 3–4 h de agente; latência só no empate. Se paga: a regra na fase 2, o
     agente quando a medição mostrar empate;
   - o agente decide toda chamada. Custo: 3–4 h, ~2–6 s e cota a cada `dispatch`. Se paga: só se a tabela não cobrir;
   - regra pura. Custo: 1,5–2 h. Se paga: agora, contra o "rodando um agente" da R4.1.

   **Decidido — a regra, e o agente desempata.**

2. **O que o orquestrador faz sem perguntar.** Opções:
   - o consultor roda direto; abrir executor ou trocar conta devolve proposta, e a sessão principal pergunta
     (recomendada). Custo: 1–2 h e uma seção no `AGENTS.md`. Se paga: na fase 2, no 1º executor;
   - tudo com gate. Custo: 1 h e um clique por chamada. Se paga: agora, sem fila automática;
   - autônomo, reescrevendo as duas seções. Custo: 1 h e o risco de gastar cota sem ver. Se paga: só com o painel da
     fila e o aviso prontos, na fase 3.

   **Decidido — o consultor livre, o executor com gate.**

3. **Onde mora o código público.** Opções:
   - um repositório próprio, `brz-anderson/brza`, com CLI, MCP, os dois plugins e o `DESIGN.md`; o `brza-workspace` fica
     com as notas, os planos e a instância da norma (recomendada). Custo: ~2 h e a CI do pacote. Se paga: na 1ª
     publicação no PyPI;
   - `scripts/brza` do workspace. Custo: ~0,5 h e filtrar o pessoal a cada release. Se paga: agora, com dívida;
   - dentro do `brza-studio`. Custo: ~1 h e o atrito de merge. Se paga: nunca para o Orca.

   **Decidido — o repositório próprio `brz-anderson/brza`.**

4. **O `brza sessions list|send|close`, o P7 do PLN-002.** Opções:
   - o PLN-003 absorve o P7 (recomendada). Custo: 3 h na fase 1. Se paga: na fase 2, no roteador;
   - fazer o P7 no PLN-002 antes da fase 2. Custo: 3 h e a dependência entre planos. Se paga: igual;
   - o MCP fala direto com o app, sem verbo na CLI. Custo: ~1,5 h. Se paga: agora, contra a CLI como núcleo.

   **Resposta:** "P7 agora". Leitura: o P7 não espera — executa já, antes da fase 1 deste plano. Em aberto se ele roda
   no PLN-002 por uma sessão nova, sem a 2d, ou se o PLN-003 o absorve; vai à rodada 6.

### Rodada 6 — o P7, o `DESIGN.md`, a política e o modelo (enviada 2026-10-29)

**Apresentado antes:** a leitura da R5.4 — o P7 executa antes da fase 1 —, e que o executor do P7 no PLN-002 é "a
sessão da 2d, reaberta por Anderson" (`plans/PLN-002-os-comandos-brza/PLN-002-plan.md:257`, R5.2 de lá); por
`AGENTS.md`, esta sessão não executa passo de outro plano.

Respondida em 2026-10-29, no chat do BrzA Studio.

1. **Por onde o P7 roda.** Opções:
   - uma sessão nova, `pln-002-p7`, aberta por esta pelo `brza-sessions`, que faz o P7 no PLN-002 com a combinação do
     D7 feita por ela, sem a 2d (recomendada). Custo: ~3 h estimadas na sessão nova. Se paga: agora; o PLN-002 fecha;
   - Anderson reabre a 2d. Custo: acordar a 2d regrava o cache dela. Se paga: só se ela tiver contexto que as notas não
     guardam;
   - o PLN-003 absorve o P7 e o faz primeiro. Custo: 3 h e reescrever o passo. Se paga: depois do Desenho daqui.

   **Decidido — a sessão nova `pln-002-p7`, aberta por esta.**

2. **O que é o `DESIGN.md`.** Opções:
   - a arquitetura e o contrato entre as frentes, no `brz-anderson/brza` (recomendada). Custo: 2–3 h na fase 2. Se paga:
     no fechamento, como casa dona do Desenho;
   - o design system do painel, no formato do Stitch. Custo: ~1–2 h. Se paga: quando o painel tiver mais de uma tela;
   - sem `DESIGN.md`. Custo: 0. Se paga: nunca.

   **Decidido — o design system do painel.** A arquitetura e o contrato ficam sem casa nomeada: vão a uma rodada
   própria.

3. **Onde mora a tabela de política.** Opções:
   - um `brza.toml`, lido por `tomllib`, que o `AGENTS.md` cita (recomendada). Custo: ~1 h. Se paga: na fase 2;
   - a tabela Markdown do `AGENTS.md`. Custo: ~1 h e parser frágil. Se paga: agora, com uma fonte só;
   - só norma. Custo: 0. Se paga: nunca para a R4.1.

   **Decidido — o `brza.toml`.**

4. **De que sessão o orquestrador decide o modelo.** Opções:
   - só da que ele abre (recomendada). Custo: 0. Se paga: na fase 2;
   - também sugere à principal, por aviso. Custo: ~1 h. Se paga: quando a medição mostrar a principal cara em tarefa
     mecânica;
   - decide a principal. Custo: ~4–6 h no fork, só BrzA. Se paga: fora do PLN-003.

   **Decidido — também sugere à principal.** A principal continua "o de quem a abriu" (`AGENTS.md`); o aviso é sugestão.

## Worklogs

