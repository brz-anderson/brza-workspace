---
name: studio-orchestration-map
description: Onde mora o ciclo de vida de worker (auto-release, Keep open, worker-start) no ~/Projects/brza-studio e atalhos de busca (2026-11-08)
metadata:
  type: reference
---

- Auto-release do worker: `src/main/runtime/orchestration/db/worker-terminal/worker-terminal-auto-release.ts` (2 min, arma/suspende/reinicia), `worker-terminal-user-keep.ts` (Keep open e estado), `src/main/runtime/orchestration/worker-auto-release-activity.ts` (turno do chat), scheduler em `.../orchestration/worker-terminal-auto-release-scheduler.ts`. Arma só em `dispatch-context/worker-report-settlement.ts` (`worker_done` aceito); fim de turno sem `worker_done` só gera mensagem (`worker-turn-stop-report.ts`).
- Botão no chat: `renderer/src/lib/worker-auto-close.ts` + `components/native-chat/NativeChatStructuredWorkerLifetimeStrip.tsx`; só aparece com contexto de orquestração (Dispatch) da aba.
- Superfície do `worker-start` não tem flag: `agent-launch-mode.ts` `decideAgentLaunchMode` + `shared/structured-native-chat-launch-route.ts:58` (`nativeChatProviders[agente]` ou `agentDefaultSurface`; padrão de fábrica terminal).
- `grep --include=*.ts` sem aspas quebra no zsh da ferramenta: use `--include='*.ts'`. O settings do usuário (`agentDefaultSurface`) não está em arquivo JSON sob `~/Library/Application Support/brza-studio`; não dá para ler o ajuste efetivo por lá.
- O binário `brza` do app (`/Applications/BrzA Studio.app/Contents/Resources/bin/brza`) dá `--help` de todos os verbos sem abrir nada; é a fonte mais rápida das notas de uso. "Hand-back from" no renderer é de subagente Claude, não de `worker_done`.
- `brza sessions` (`~/Projects/brza-workflow/packages/client/bin/brza-sessions`) tem mapa próprio de sessões (open/title/session/close); chat aberto por outro caminho não entra.
