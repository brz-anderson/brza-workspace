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

Related: [[sync-review-patterns]]
