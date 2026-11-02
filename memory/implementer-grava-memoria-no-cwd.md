---
name: implementer-grava-memoria-no-cwd
description: o implementer grava a memória em .claude/agent-memory/ relativo ao cwd dele; na sessão do chat, o cwd é o scratch, então a memória cai fora do workstream
metadata:
  type: feedback
---

O `implementer` (e os outros papéis com `memory: project`) grava em `.claude/agent-memory/<papel>/` **relativo ao diretório
de trabalho**. Na sessão do chat do BrzA Studio o cwd da sessão é o scratch (`…/chat-scratch/<hash>/pln-007`), e o agente o
herda: nos P4, P5 e P6 do PLN-007, o P4 gravou no workstream, e o P5 e o P6 gravaram em `/private/tmp/pln-007/.claude/`.

**Why:** a memória de papel é do workstream e vai ao commit pelo `brza note commit`; a que cai no scratch some com ele e
não entra na medição.

**How to apply:** no pedido ao `implementer`, diga o caminho absoluto da memória do papel
(`~/Projects/brza-workspace/.worktrees/<workstream>/.claude/agent-memory/implementer/`) e confira, na devolução, onde ela
foi parar; se caiu no scratch, mova para o workstream antes do commit.
