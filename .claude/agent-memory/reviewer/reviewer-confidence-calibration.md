---
name: reviewer-confidence-calibration
description: Achados que caíram ou que pedem premissa na revisão do brza-studio, com a confiança dada e o porquê
metadata:
  type: feedback
---

- **Regressão em arquivo que alguém está editando cai.** Dei 88 aos overrides de cor fora do tema do chat
  (contra o D46 do PLN-001); a sessão de sync corrigiu e pôs no índice durante a revisão. Não reporte sem
  reler o índice no fim.
  **Why:** o worktree do sync é compartilhado com a sessão que resolve o merge.
  **How to apply:** reconfira cada achado com `git show :<caminho>` imediatamente antes do handback.
- **Comportamento do pino P36 em caminho antigo do fork** (login para a conta global): 85, com a premissa de
  que a falha do chat fixado chega como `notSignedIn`/`claudeAccountFolderMissing`. Pré-existente, vai a
  issue, não ao sync.
- **Mudança de nome/identidade vista no código e conferida por comando** (`gh api`, grep da cópia no NSIS):
  90 ou mais.

- **Defeito de caminho de lançamento provado por teste temporário**: 85, não 90, quando a premissa sobre o
  registro (sem `accountSwitch`, sem `resumeCursor`) foi só lida. Teste temporário vai no worktree do sync,
  com nome `zz-reviewer-*`, e é apagado no mesmo comando; confira o `git status` depois.
- **Hipóteses que costumam cair no P36:** retomada agendada na conta global, `acquiredAccount` vazando na
  troca, seletor global na linha de limite de chat fixado. O código do fork já cobre as três; não gaste
  tempo nelas sem um caminho novo do upstream.
- **Colisão de coexistência por recurso em `/tmp` ou `~/.orca`** costuma cair (hash do runtimeDir, shim
  idêntico, ledger de PTY compartilhado de propósito). O que fica é o que é **cifrado por app**.

Related: [[sync-review-patterns]]
