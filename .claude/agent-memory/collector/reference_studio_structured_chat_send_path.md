---
name: studio-structured-chat-send-path
description: Onde mora o caminho de envio do chat estruturado do brza-studio (renderer composer -> controller -> host main -> Claude), e atalhos de busca
metadata:
  type: reference
---

Caminho de uma mensagem comum no chat estruturado (repo `~/Projects/brza-studio`, `src/`):
- renderer: `NativeChatStructuredSession.tsx` -> `use-native-chat-structured-composer-send.ts` -> `native-chat-structured-composer-dispatch.ts` -> `use-native-chat-structured-composer-transport.ts` (`send`) -> `use-structured-agent-session.ts` (`send`, `queueEnabled`) -> `use-structured-agent-session-sends.ts` -> `structured-agent-session-message-sender.ts` / `-send-attempt.ts` (RPC `agentSession.send`).
- `delivery: 'queue-if-active'` sai de `structured-agent-session-queue-request.ts`; o host decide em `main/native-chat/agent-session-wire/structured-agent-session-queued-messages.ts` (`structuredQueueHold`: blocked/prompt/working) e `...-queued-send.ts`; sem queue cai em `performSend` (`...-turns.ts`) e o `delivery-loop` entrega ao Claude (`main/claude/claude-structured-dispatch.ts`, stdin stream-json; nenhum cancel de prompt ali).
- prompts do Claude: `main/claude/claude-prompt-registry.ts`, `claude-structured-inbound-control.ts` (canUseTool), cancel do cartao = Stop do turno (`...-prompt-cancel.ts`).

Atalhos que poupam leitura:
- `grep` com `--include=*.test.ts` sem aspas quebra no zsh ("no matches found"): use `--include='*.test.ts'`.
- `src/main/native-chat/agent-session-wire/` tem centenas de arquivos; va direto por `grep -rn "queue-if-active"` / `structuredQueueHold`.
- O que o CLI do Claude faz com uma mensagem no stdin enquanto um canUseTool esta pendente nao esta no repo (e interno ao CLI); so da para afirmar que o host nao cancela nada.
- Teste do hold por prompt no host: `structured-agent-session-queued-gate.test.ts` (so Send-now) e `...-queued-compact.test.ts:155` (compact). Nao ha teste de mensagem comum queue-if-active atras de pergunta pendente (ate 2026-10-31).
