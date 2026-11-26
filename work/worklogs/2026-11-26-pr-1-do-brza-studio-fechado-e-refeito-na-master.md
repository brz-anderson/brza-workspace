---
scope:
  - brza-studio
tags:
  - ci
sessions:
  - 5f596faf-ab1f-41f4-91fc-9ab63eb31c3a
---

# O PR #1 do brza-studio, fechado e refeito na master

O pedido de Anderson, em 2026-11-26: "https://github.com/brz-anderson/brza-studio/pull/1 verifique as alterações feitas
nesse PR e se ainda são necessárias". O PR, de um agente do Cursor aberto em 2026-11-12 sobre `c470dda8a46`, corrigia as
falhas recorrentes do CI da branch padrão depois do rebrand: 86 arquivos, +577/−274. Feito na sessão do workstream
`studio`, logo depois do [sync das v1.4.263 e v1.4.278](2026-11-26-sync-das-v1-4-263-e-v1-4-278-do-upstream.md).

## A avaliação

Um `reviewer` comparou cada mudança com a `master` de então (`609bfbffaba`):
- **Não dava para mesclar:** 51 conflitos, e 36 dos 86 arquivos não existiam mais — o upstream cortou a suíte E2E de
  1.065 para 129 arquivos (#46786).
- **As falhas agendadas eram todas de `c470dda8a46`**, a base do PR; nenhuma rodada agendada tinha visto a `master` nova.
- **Obsoleto ou já resolvido:** os textos de ~30 specs E2E apagados; a `v1.4.224` no `e2e.yml`; o teste do serve
  headless; os casos de sinal da CLI no Linux; o Notepad (upstream #42165); a nota ao lado de tabela (upstream #46198);
  a semeadura do prompt e o placeholder (as pills apagadas eram defeito da própria refatoração do PR).
- **Ainda valia:** o contrato do AppImage (só aceitava `orca-linux*`, e todo build Linux do fork parava); os scripts do
  deb/rpm com `/opt/Orca`; os nomes do Orca no empacotamento do `pr.yml`; os ratchets de `translate()` (10 arquivos) e do
  React Compiler (5) no chat do fork; 21 arquivos fora do `oxfmt`.
- **Novo, fora do PR:** o spec golden de Markdown ia falhar no E2E seguinte, porque o padrão do fork é a prévia; e o sync
  tinha devolvido duas mensagens da CLI para "Orca" (`cli-error.ts:143`, `browser-identity.ts:33`).

## A rodada

Respondida por Anderson em 2026-11-26, pelo AskUserQuestion, nesta sessão:
- PR #1: "Fechar e refazer os 6 itens (Recomendado)";
- runners: "Desabilitar no fork (Recomendado)";
- tag antiga: "Empurrar a tag ao fork (Recomendado)";
- Markdown: "Arquivo novo no rico + spec escolhe o rico (Recomendado)".

## O que se fez

- **`0849f8b4253`**, por fast-forward na `master` do `brza-studio` (`609bfbffaba..0849f8b4253`):
  - o contrato do AppImage aceita `brza-studio-linux*`, com `static-appimage-package-contract.brza.test.mjs`;
  - `after-install.sh` e `after-remove.sh` com `/opt/BrzA Studio`;
  - o `pr.yml` com o AppImage, o `/opt` e o `.exe` do BrzA;
  - "BrzA Studio" em `cli-error.ts:141,143` e `browser-identity.ts:33`, com `cli-error.brza.test.ts`;
  - `useTranslate()` nos 10 arquivos; o `try/finally` fora dos componentes e hooks em 5; `--prune` no baseline do React
    Compiler;
  - `oxfmt` nos 21 arquivos;
  - o `.md` recém-criado abre no editor rico, só quando é Markdown (`untitled-file-creation.ts`, com
    `untitled-file-creation.brza.test.ts`); o existente segue na prévia (D20). O spec golden
    `golden-journeys/golden-file-open-edit-save.spec.ts` escolhe o modo rico.
- **O PR #1 foi fechado sem mesclar**, com um comentário que lista o que foi refeito e o que ficou de fora.
- **A tag `v1.4.199` foi ao origin**, para o job `cross-version-wire`.
- **Os workflows `ci-cache-warmup.yml`, `computer-macos-native.yml` e `performance-contracts.yml` foram desabilitados**
  no fork; nunca achavam runner (macOS e Blacksmith) e falhavam todo dia.

## Os testes

- **No Mac:** typecheck com 0 erros; lint com 48 de 49 (só `check:code-quality:changed`, do ambiente, que passa com
  `ORCA_CODE_QUALITY_BASE=609bfbffaba`); os ratchets de render-path translate, React Compiler, memo-translate e max-lines
  verdes; `oxfmt --check .` limpo; 95 arquivos e 490 testes verdes em `native-chat` e `settings`.
- **Na CI, em `0849f8b4253`:** suíte unitária verde (45881031829). E2E (45881067203): o spec golden de Markdown passou; na
  1ª tentativa falharam `golden-shell-after-agent-exit` e `card-title-rename`; na 2ª, só o `card-title-rename`.
- **E2E de comparação:** na `master` `609bfbffaba` (45883006756) falharam o spec golden de Markdown e o `card-title-rename`;
  na `v1.4.278` pura (45884819201), só o `card-title-rename`. Ele é do upstream, e o `golden-shell-after-agent-exit` é
  instável.

## O que ficou

- **O `card-title-rename` vermelho** ("double-click renames the active new-style card") vem do upstream; o E2E agendado
  vai marcar falha até o upstream consertar.
- **Os três workflows desabilitados** ficam assim até alguém religar com `gh workflow enable`.

## Fora do workspace

- **Os workflows `ci-cache-warmup.yml`, `computer-macos-native.yml` e `performance-contracts.yml` do `brz-anderson/brza-studio`, desabilitados.**
  - **Risco:** os caches de CI e os contratos de desempenho deixam de rodar no fork.
  - **Estado:** ativo.
  - **Como desfazer:** `gh workflow enable <arquivo> -R brz-anderson/brza-studio`.
- **A tag `v1.4.199` no origin (`brz-anderson/brza-studio`).**
  - **Risco:** nenhum.
  - **Estado:** ativo.
  - **Como desfazer:** `git push origin :refs/tags/v1.4.199`.
- **O PR #1 fechado, com comentário, e a branch `fix/pr1-redo` no origin.**
  - **Risco:** nenhum; o PR pode ser reaberto.
  - **Estado:** ativo.
  - **Como desfazer:** `gh pr reopen 1 -R brz-anderson/brza-studio`; `git push origin --delete fix/pr1-redo`.
- **Quatro rodadas disparadas à mão** (`node-next-compat.yml` na branch; `e2e.yml` na branch, na `master` e na tag, mais
  uma 2ª tentativa).
- **O `node_modules` do clone principal `~/Projects/brza-studio` foi reinstalado** pelo `reviewer`, ao rodar um `pnpm run`
  (tsrs 0.18→0.23, vitest 5.0.5→5.1.0, zustand 5.0.15→5.1.0), para casar com o lockfile da `master`. Nenhum arquivo
  versionado mudou.
  - **Risco:** nenhum.
  - **Estado:** ativo.
- **O worktree `pr1-redo` do `brza-studio`**, criado e removido.

## Custo da tarefa

Corrido 37 min — agente 7 min, quem pediu 30 min, pausa 0 s · US$ 3,00 (turnos 1,76, subagentes 1,24) · CPU 31 s do `claude` e 7 min dos comandos, RSS até 537 MB · 5 turnos, 1 sessão · dividida com 1 outro worklog do commit · até 17:03 de 2026-11-26, pelo `brza note commit`
