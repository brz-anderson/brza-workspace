---
name: upstream-sync-procedure
description: "Como conduzir um sync do stablyai/orca no brza-studio — rebrand por script, linha de base na tag pura, pela CI, pre-commit no merge"
metadata:
  node_type: memory
  type: project
  originSessionId: 7884383f-7a82-4f9c-a066-e1d749d6c2a6
  modified: 2026-11-26T18:44:07.427Z
---

O sync da v1.4.246 (2026-11-02) teve 404 arquivos em conflito, e o que funcionou fica aqui. O registro inteiro está no
worklog `2026-11-02-sync-da-v1-4-246-do-upstream.md`.

- **O rebrand é a maior parte dos conflitos.** Classifique cada trecho diff3: se a base e o nosso lado diferem só no
  vocabulário do rebrand, a resolução é o lado deles com a mesma troca. Os idiomas vão por merge de três vias, chave a
  chave.
- **Linha de base na tag pura.** O lint roda num worktree `--detach` da tag do upstream; a suíte, na CI, com a tag
  publicada no fork. Compare arquivo a arquivo. Na v1.4.246, já falhavam 39 arquivos de teste e 3 ou 4 passos de lint.
- **O pre-commit morre no commit do merge.** O lint-staged em 18 mil arquivos é morto. Commite o merge com
  `--no-verify` e as correções em commit próprio, com o hook.
- **Cada grupo de conflito vai a um `implementer`, com um brief comum** que traz as decisões das rodadas e as features a
  preservar. Depois, um `reviewer` faz a revisão adversária.

Do sync da v1.4.251 (2026-11-06, 610 conflitos), mais:
- **Os marcadores não saem em diff3 por padrão** neste clone. Antes de classificar, rode
  `git checkout --conflict=diff3 -- <arquivos>`. O `merge.renameLimit` alto não mudou nada.
- **Os `UD` também se classificam:** compare `:1:` e `:2:` com o `rebrand_only`. Os que são só rebrand vão de `git rm`, e
  o resto vai aos `implementer`.
- **Nenhum agente dá `git add` de pasta ou `-A`.** Um deu, e o índice perdeu o `UU` dos outros grupos no meio do
  trabalho. O brief diz isso, e a conferência final procura marcador no conteúdo, não no `git status`.
- **A suíte inteira roda de novo na CI depois dos consertos da revisão.** Um helper `brza/` que só movia texto passou a fazer
  `await` em toda chamada. O microtask a mais inverteu uma ordem testada, e só a suíte pegou.

Do sync da v1.4.256 (2026-11-11, 796 conflitos), mais:
- **A suíte inteira saiu do Mac.** A linha de base e a suíte do merge vêm da CI, pelo `node-next-compat.yml`; no Mac,
  só o alvo. A regra e os comandos estão na norma, em `.claude/rules/workspace.md`.
- **Classifique e aplique o rebrand antes dos grupos:** 341 de 518 `UU` e 219 de 278 `UD` saíram por script, e os
  `implementer` ficaram com 231. O `merge_locales.py` erra quando o rebrand elide ("d'Orca", "Orca가"); confira as
  chaves que ele deixa no "nosso".
- **Feature do fork que o upstream passou a ter** (o Fork de mensagem, o gate do rewind) aparece em mais de um grupo,
  com recomendações opostas. Leia o código do upstream antes da rodada.
- **Quando uma feature do fork sai, procure o receptor que fica.** O Bifurcar saiu, e o schema e o divisor do host
  ficaram sem chamador; o revisor achou. O mesmo vale para os testes de contrato e de cross-version que a citam.

Do sync das v1.4.263 e v1.4.278 (2026-11-18 a 2026-11-26), mais:
- **O scratch em `/private/tmp` some com o reinício do app.** Os scripts (`classify_hunks.py`, `classify_ud.py`,
  `merge_locales.py`, `rebrand_locales.py`), o brief e as rodadas ficam em
  `~/Library/Application Support/brza-studio/chat-scratch/d2b1b1fb0ad353b4ca07993e8c8d65cd/` (e `sync-278/`). Copie de lá
  e grave lá o brief e as rodadas de cada sync.
- **Merge em andamento se commita assim que os conflitos fecham**, antes da rodada dos pontos: um reinício no meio não
  perde o trabalho dos grupos.
- **Tag nova no meio do sync:** mescle a tag nova sobre a branch do sync em curso, não sobre a `master` (375 conflitos
  contra 808 na 278).
- **"O upstream já faz o mesmo" se confere antes da rodada**, lendo o código do upstream. Na 263, o modo ao vivo do
  Antigravity não era o mesmo, e a decisão 3 teve de ser refeita.
- **O bundle web do mobile tem orçamento de carga** (`verify-mobile-web-app-bundle.mjs`); o upstream usa quase todo, e o
  fork tem +128 KiB próprios (R4 da 278). O `pnpm build:mac` é o que pega; rode-o antes do push.
- **Briefs de teste pedem `bash -c` e lista conferida:** um glob vazio no zsh fez um `implementer` rodar a suíte inteira.

**Why:** cada sync fica maior sem isso; a linha de base separa o que é do merge do que já vem quebrado do upstream.

**How to apply:** no próximo sync, comece pela classificação dos conflitos e pela linha de base. Leve também a
conferência de identidade de [[brza-orca-coexistence]].
