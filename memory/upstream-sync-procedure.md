---
name: upstream-sync-procedure
description: "Como conduzir um sync do stablyai/orca no brza-studio — rebrand por script, linha de base na tag pura, pela CI, pre-commit no merge"
metadata:
  node_type: memory
  type: project
  originSessionId: 7884383f-7a82-4f9c-a066-e1d749d6c2a6
  modified: 2026-11-11T23:23:38.816Z
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

**Why:** cada sync fica maior sem isso; a linha de base separa o que é do merge do que já vem quebrado do upstream.

**How to apply:** no próximo sync, comece pela classificação dos conflitos e pela linha de base. Leve também a
conferência de identidade de [[brza-orca-coexistence]].
