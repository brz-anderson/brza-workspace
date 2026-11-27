---
name: brza-studio-continue-other-account-lessons
description: Defeito "Continue in another account troca mas não continua" (P79, pós 278) - o que já foi provado em cada camada, harness de teste, onde mora cada peça
metadata:
  type: project
---

- **Provado por teste (passam no HEAD 9eef46284d8)**: o `useNativeChatInterruptedContinuation` real + `NativeChatUsageLimitActionsProvider` + `NativeChatNoticeRow` mandam `agentSession.send` com `usageLimitContinuationOfTurnItemId` após o switch, no chat fixado e no que segue a seleção, com `isWorking` true ou false (`usage/NativeChatUsageLimitContinueAfterSwitch.brza.test.tsx`). O host admite o Continue após `switchAccount` mesmo com a fence velha e sobe o agente na conta nova (`operations/testing/structured-agent-session-account-switch.test.ts`); o seletor global + `releaseIdleChatsOnOtherAccount` também (rig `idleClaudeChat` de `host/testing/...account-switch.test.ts`, só experimento, não commitado).
- **Camadas que NÃO são a causa**: closure velha do `onContinue` (o `continueUsageLimit` velho ainda envia), `holdStructuredAgentSessionSends` (só o `/clear`), divisória "Account switched" (thread scope, não é turno, não muda o corte), `expectedRuntimeFence` velha (o host ignora no send), pino assíncrono (`pinnedClaudeAccountHome` ok).
- **Pontos sem prova (ainda abertos)**: `historyInOtherAccount` no chat que segue a seleção (o transcript só é copiado no switch fixado, `copyClaudeTranscriptsToAccount`); `switchStructuredAccount` devolve false calado em `dropped`; Claude real nunca rodou aqui.
- **Harness de teste do renderer**: mock de `useStructuredAgentSessionAccountSwitch` pelo caminho relativo ao arquivo do teste (`../session/status/...` de dentro de `usage/`); transport de teste exige `runtimeEnvironmentId`; `fetchSettings` real loga erro sem `window.api`, inofensivo.
- **Zsh/macOS**: `sed -i 's/x/a\nb/'` falha em BSD sed, use python; `git grep` e `grep --include=*.ts` sem aspas dão "no matches found".
- O app instalado guarda o journal em `~/Library/Application Support/brza-studio/agent-session-journal.db` (SQLite, `journal_rows.row_json`); estava com dados de 2026-11-02, sem o switch novo.
