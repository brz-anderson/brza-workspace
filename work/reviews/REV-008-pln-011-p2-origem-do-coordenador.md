---
status: done
scope:
  - brza-studio
opened: 2026-11-03
completed: 2026-11-03
tags:
  - chat
  - tooling
---

# REV-008: o P2 do PLN-011, a origem do coordenador no `agentSession.send`

O parecer do P2 do
[PLN-011: Os chats do BrzA Studio se coordenam pela CLI, aparecem na navegação e chegam aos plugins](../../plans/PLN-011-chats-pela-cli-e-plugins/PLN-011-plan.md),
na versão `brza-studio@63aa99c2505`, sobre a `df8adc29574`. Revisou contra o D2, o P2, a Cobertura e a Regressão um
worker `reviewer` do `brza-mcp` (pedido 6, Opus), que não executou o passo.

## Veredito

Aprova com um achado de cobertura, já corrigido em `brza-studio@594c4a7e13c`. O diff é o do D2, linha por linha
(`client.ts` +8/−3, o teste +9). O remoto não manda a evidência (`!this.remote`), o WSL também não
(`orchestration-compatibility-envelope.ts:20-28`), e o `agentSession.history` e o `terminal.*` ficam fora do conjunto.
O `agentLaunchCaller` não foi renomeado.

No host, o envio do próprio chat segue `userSend`: com `callerChatSessionId(context) === params.envelope.sessionId`, o
`coordinator` fica `undefined` (`structured-agent-session-send-compatibility.ts:21-34`). O caso do terminal que não é
chat e herda o id não existe, porque `getInheritedAgentSessionStampEnvKeysToDelete`
(`src/main/ipc/pty/host-env/pi-agent.ts:145-155`) apaga o `ORCA_AGENT_SESSION_ID` de todo pane.

O implementer relatou que o diff já estava no worktree, sem commit, quando ele abriu, e que provou a falha revertendo o
`client.ts`. O revisor refez a prova do zero: com o `client.ts` da `df8adc29574`, 1 teste falha e 7 passam; com o
commit, todos passam. O worktree terminou limpo.

## Achados

### A1 — O teste não confere o `agentSession.send` no WSL nem no servidor pareado

> lacuna · sugestão · confiança 95 · → corrigido aqui

**Evidência:** o caso WSL (`src/cli/runtime/client-execution-host.test.ts:153-162`) e o pareado (`:164-173`) só chamavam
`agent.launchReplay`, e o P2, passo 1, e o D2 pedem também o `agentSession.send`. Corrigido em
`brza-studio@594c4a7e13c`, só no teste: `client-execution-host` e `runtime-client` → 24 passed; `pnpm check:changed
--base=origin/master --maxWorkers=2 --force` → 22/22.

### A2 — O `--session` corta o endereço `orca_session_id:<id>` no primeiro `:`

> lacuna · sugestão · confiança 90 · → issue [O `--session` do `brza chat` recusa o endereço `orca_session_id:<id>`](../issues/chat-session-recusa-o-endereco-orca-session-id.md)

**Evidência:** `src/cli/chat-sessions.ts:34`, no código do porte (P1), faz `withoutHandle.split(':')[0]`. Com
`orca_session_id:<id>`, a forma de endereço da orquestração (`src/shared/orchestration-party-identity.ts:3-10`), a
sessão fica `orca_session_id`, e o host a recusa. O revisor a deu como observação fora do P2; a sessão coordenadora
conferiu a linha. O destino saiu da R17.1, às cegas, com acordo na volta 1.

## O que rodou e o que deu

- A prova na base: o `client.ts` da `df8adc29574` sobre o do commit → 1 falha, 7 passam (`:149`, `expected undefined
  to deeply equal { agentSessionId: … }`); depois o `git checkout`, e o `git status --short` vazio.
- `run-vitest … client-execution-host.test.ts runtime-client.test.ts` → 24/24 passed.
- `run-vitest … handlers/terminal.test.ts terminal-read-screen.test.ts index-terminal-commands.test.ts handlers/chat.test.ts`
  → 73/73 passed.
- `pnpm tc:cli` → exit 0; `pnpm check:changed --base=origin/master --maxWorkers=2 --force` → 22/22, exit 0.
