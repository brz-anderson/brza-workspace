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

- **Entrada de build que aponta a arquivo inexistente**: 90, com a premissa de que o Rollup recusa
  `input` não resolvido. Reforça: o app instalado em `/Applications/BrzA Studio.app/…/app.asar.unpacked`
  mostra o que o build de fato emite (leitura, sem rodar build).
- **Hipóteses que caíram no sync da 251** (não gaste tempo sem caminho novo): retomada automática
  do upstream em chat fixado (vai pelo envio comum, que lê `record.accountSwitch`); componente do
  brief que "sumiu" na junção mas o próprio fork tinha tirado antes (confira `git log --all -S`);
  cherry-pick posterior "vai conflitar" (simule com `git merge-tree --write-tree --merge-base`).
- **Falha de teste vista só por outro agente, sob carga**: abaixo de 80 sem rodar; vai a ponto
  para rodada, conferida contra o `test-base.failed` da tag pura.
- **Corrida de escrita assíncrona contra leitura no renderer** (sync da 256): 82, não 90. A
  janela foi provada pela leitura (caminho devolvido antes da escrita, falha em cache no
  leitor); que ela se abra na prática ficou como premissa escrita, sem medição.
- **Token faltando num porte do upstream**: 85, com a premissa de que um tema de plugin define
  o token (provada por `plugin-theme-artifact.ts`), mas sem reproduzir no app.
- **Hipóteses que caíram no sync da 256:** "teste do fork perdido" que só mudou de título e de
  pasta (procure pelo corpo, não pelo título); asserção de teste cortada pelo conserto porque o
  upstream mudou o comportamento (confira o teste novo do upstream); campo descartado por um
  spread trocado por função `brza/` (confira o tipo: hoje cobre tudo).
- **Commit novo no meio da revisão** (sync da 278): a sessão do sync commitou `9b93796a198` enquanto
  eu lia; a contagem do mobile mudou de 9 para 19 chaves. Rode `git log -1` no começo e de novo antes
  do handback, e diga em que commit cada número foi tirado.
- **Hipóteses que caíram no sync da 278** (não gaste tempo sem caminho novo): o pino assíncrono sem
  `await` (único chamador espera); a desinstalação do upstream apagando `~/.orca` (detecta o Orca e
  mantém); marcador de dock (`data-native-chat-dock-contents`) faltando no cartão do fork (o upstream
  também o perde atrás do anchor do slot de subagente — dei ~75, ficou de fora como achado).
- **Comparador de mensagem com "Orca" contra produtor "BrzA Studio"**: 92, lido dos dois lados; o
  efeito (tradução perdida) é dedução direta do `return normalized`, sem precisar rodar.
- **Ferramentas barradas no papel:** script inline (python, node -e) e redirecionar para o scratch da
  sessão são recusados pelo hook; `>` para `/tmp/rv278/` passa. O cruzamento de linhas sai com
  `awk` + `sort` + `join -v1` (`LC_ALL=C`), sem script.
- **`pnpm run <script>` no clone principal reinstala o `node_modules`** quando o lockfile mudou
  (verify-deps-before-run). Na revisão do PR #1, isso aconteceu sem pedir. O hook barra `node <script>`
  mas deixa passar `pnpm run`. Para ratchet ou oxfmt, prefira `node_modules/.bin/<bin>`, ou confira
  antes o `node_modules/.modules.yaml` contra o lockfile, e diga o efeito na devolução.
- **Conserto de upstream já coberto por outro caminho** (Notepad pelo Win32 em vez do TextPattern;
  trilho fixo do CSS de nota): 80-82, com a premissa escrita. Procure com `git log -S` a função nova
  e confira se ela veio depois da base do PR (`merge-base --is-ancestor`).
- **Spec E2E do upstream contra um padrão do fork** (preview × `.rich-markdown-editor`): 85. A
  premissa é que o perfil de E2E não grava a preferência; confira o
  `e2e-completed-onboarding-profile.ts`.
- **Branch reescrita no meio da revisão** (PLN-026, 2026-11-26): o que estava sem commit no
  worktree no começo virou o `rebase --autosquash`. Compare o `git diff <antigo> <novo>` com o
  `git diff` sujo que você viu (`diff - <(...)`) e revise contra o HEAD novo.
- **Teste intermitente provado por repetição** (8 rodadas, 1 falha registrada): 95. Que a mesma
  janela não exista em produção, lido pela ordem de gravação do provider: 85.
- **Timer que dispara cedo contra o `Date.now()`** (P5 do PLN-026): 300 timers marcados num laço
  apertado → 94 disparam 1 ms antes; o caminho real do fallback, repetido 20 vezes → 0. Ficou abaixo
  de 80 e fora dos achados. Não reabra sem medir no caminho real.
- **Corrida provada com `deps` embrulhado** (o Cancelar durante o veredito): 88, não 90. O mecanismo
  foi rodado; que a janela dure a troca inteira foi lido (o `run` no `serialize`).
- **Ramo de UI morto lido em 4 elos** (`latest…Cut` → `usageLimitTurnItemId` → `active` → `slotKey`):
  90, sem rodar o renderer.
- **zsh**: `$r:src/...` também quebra em `git show`/`git grep` com `$r` antes de `:`; use `"${r}:…"`.

Related: [[sync-review-patterns]]
