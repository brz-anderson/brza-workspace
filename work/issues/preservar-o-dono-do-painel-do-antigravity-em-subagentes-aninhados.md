---
status: open
description: O PR #37507 do upstream preserva o paneOwner da sessão do Antigravity quando ela dispara subagentes aninhados, evitando que hooks de processos filhos tomem a aba.
scope:
  - brza-studio
priority: high
opened: 2026-11-03
tags:
  - tooling
---

# Preservar o dono do painel do Antigravity em subagentes aninhados

Rastreado do upstream [`stablyai/orca#37507`](https://github.com/stablyai/orca/pull/37507) e da issue
[`stablyai/orca#37505`](https://github.com/stablyai/orca/issues/37505), abertos em 2026-11-02.

## O problema

Quando uma sessão do Antigravity dispara subagentes ou processos de CLI aninhados no mesmo painel, os hooks de processo
convidado podem sobrescrever a identidade do agente dono da aba no servidor e na projeção mobile. Com isso, a aba perde
o vínculo com a sessão principal do Antigravity ou exibe o estado do subagente depois que ele encerra.

## O que o PR #37507 faz

- Captura `ORCA_HOOK_AGENT_PID` (`PPID`) e `agentProcess` no script POSIX `src/main/antigravity/hook-script.ts` e admite
  `antigravity` em `readHookAgentProcess` (`src/main/agent-hooks/server/server-status-identity.ts`), fazendo donos de
  processo ociosos do Antigravity rejeitarem hooks de CLIs convidados aninhados.
- Inclui `paneOwner` (`{ agent, session }`) em `AgentStatusEntry` (`src/shared/agent-status-types.ts`) e nas projeções de
  status do runtime mobile (`src/main/runtime/runtime-mobile-agent-status-builder.ts`).
- Reconstrói o dono da aba em `src/renderer/src/store/slices/agent-status/agent-status-live-entry-main-agent.ts` e na
  elegibilidade do Native Chat mobile (`mobile/src/session/native-chat/mobile-native-chat-eligibility.ts`).

## O que fazer

Avaliar o cherry-pick do [`stablyai/orca#37507`](https://github.com/stablyai/orca/pull/37507) para a `master` do
`brza-studio` ou trazê-lo no próximo sync do upstream, conferindo a preservação do rename `BrzA` em
`src/main/antigravity/hook-script.ts` e `src/main/antigravity/hook-service.ts`.
