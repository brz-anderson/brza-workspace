---
status: open
description: Os PRs #41806, #40153 e #37507 preservam a sessão lead contra hooks de subagentes e desembrulham wrappers sh -c de hooks para manter o agente estável na sidebar.
scope:
  - brza-studio
priority: high
opened: 2026-11-03
tags:
  - tooling
---

# Preservar o dono do painel do Antigravity em subagentes aninhados

<!-- pln-014-despacho -->
> **Despacho (PLN-014/R1.1):** classe `ausente` · casa `studio`
> Merge no upstream não muda `status`. PLN-014/R1, 2026-11-12.

Rastreado do upstream [`stablyai/orca#41806`](https://github.com/stablyai/orca/pull/41806) (resolve Issue [`#41857`](https://github.com/stablyai/orca/issues/41857)),
[`stablyai/orca#40153`](https://github.com/stablyai/orca/pull/40153) (endereça Issue [`#40100`](https://github.com/stablyai/orca/issues/40100)),
[`stablyai/orca#37507 (CLOSED sem merge no upstream)`](https://github.com/stablyai/orca/pull/37507) e da issue
[`stablyai/orca#37505 (CLOSED no upstream)`](https://github.com/stablyai/orca/issues/37505).

## O problema

1. **Sobrescrita da identidade do agente dono por processos convidados (`#37507 (CLOSED sem merge no upstream)`):**
   Quando uma sessão do Antigravity dispara subagentes ou processos de CLI aninhados no mesmo painel, os hooks de processo
   convidado podem sobrescrever a identidade do agente dono da aba no servidor e na projeção mobile. Com isso, a aba perde
   o vínculo com a sessão principal do Antigravity ou exibe o estado do subagente depois que ele encerra.
2. **Piscamento e remoção espúria da linha do agente na sidebar por wrapper efêmero `sh -c` (`#40153`):**
   Quando o Antigravity (`agy`) dispara comandos de hook a partir de `~/.gemini/config/hooks.json`, ele executa via `sh -c "<command>"`.
   Como o script de hook do Orca também iniciava com `/bin/sh -c 'ORCA_HOOK_AGENT_PID="${PPID:-}"; ...'`, a variável `${PPID}`
   apontava para o processo envoltório `sh -c` de curta duração em vez do PID real do `agy`. Logo após o término do hook,
   aquele wrapper morria; na tool call seguinte, o Orca consultava o PID anterior, detectava como `exited` e deletava a
   linha ativa do agente da barra lateral (zerando o spinner de trabalho), recriando-a milissegundos depois com o próximo hook.
3. **Notificações falsas de término e status incorreto na aba pai causados por hooks de subagentes (`#41806`, resolve `#41857`):**
   Em conversas com subagentes (como DeepSeek Harness via ponte de Claude-hooks), os eventos de ciclo de vida (`agent/created` e `agent/turn-stopping`)
   eram transmitidos sem discriminar o líder do painel. A finalização de um filho no meio do turno disparava evento `done` e notificações
   na aba pai enquanto o agente principal continuava trabalhando.

## O que o upstream implementa e corrige

- **Preservação de paneOwner (`#37507 (CLOSED sem merge no upstream)`):**
  - Captura `ORCA_HOOK_AGENT_PID` (`PPID`) e `agentProcess` no script POSIX `src/main/antigravity/hook-script.ts` e admite
    `antigravity` em `readHookAgentProcess` (`src/main/agent-hooks/server/server-status-identity.ts`), fazendo donos de
    processo ociosos do Antigravity rejeitarem hooks de CLIs convidados aninhados;
  - Inclui `paneOwner` (`{ agent, session }`) em `AgentStatusEntry` (`src/shared/agent-status-types.ts`) e nas projeções de
    status do runtime mobile (`src/main/runtime/runtime-mobile-agent-status-builder.ts`);
  - Reconstrói o dono da aba em `src/renderer/src/store/slices/agent-status/agent-status-live-entry-main-agent.ts` e na
    elegibilidade do Native Chat mobile (`mobile/src/session/native-chat/mobile-native-chat-eligibility.ts`).
- **Desembrulho de processos wrapper `sh -c` no hook capture (`#40153`):**
  - Em `buildHookProcessCapture` (`hook-process-capture.ts`), tanto em Linux quanto no macOS (`Darwin`), verifica se `orca_agent_pid`
    pertence a uma shell envoltória (`sh`, `dash`, `bash`, `zsh`) contendo `ORCA_HOOK_AGENT_PID=` em sua linha de comando;
  - Desembrulha um nível acima para obter o PPID correspondente (o processo duradouro do `agy`), inspecionando o tempo de
    início do processo real;
  - Mantém a linha do agente e o contador/spinner do worktree absolutamente estáveis durante todo o ciclo de tool calls
    (`PreToolUse` → `PostToolUse` → `PostInvocation`).
- **Ignorar hooks de agentes filhos para proteger a sessão líder do painel (`#41806`, resolve `#41857`):**
  - O listener do painel rastreia a sessão líder e ignora hooks que nomeiem outra sessão, impedindo que encerramentos de filhos disparem notificações ou alterem o estado de execução do painel principal;
  - Trata reinicializações e comandos `resume`/`clear` adotando a nova sessão legítima sem conflitos.

## O que fazer

1. Ignorar hooks de subagentes para preservar a sessão líder do painel contra falsos status `done` e notificações indevidas (`#41806`, resolve `#41857`).
2. Incorporar o desembrulho de wrappers `sh -c` do [`stablyai/orca#40153`](https://github.com/stablyai/orca/pull/40153) para eliminar o piscamento de status do Antigravity na sidebar.
3. Aplicar o cherry-pick do [`stablyai/orca#37507 (CLOSED sem merge no upstream)`](https://github.com/stablyai/orca/pull/37507) para a `master` do
   `brza-studio`, conferindo a preservação do rename `BrzA` em `src/main/antigravity/hook-script.ts` e `src/main/antigravity/hook-service.ts`.
