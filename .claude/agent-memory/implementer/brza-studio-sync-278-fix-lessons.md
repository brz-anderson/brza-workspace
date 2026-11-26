---
name: brza-studio-sync-278-fix-lessons
description: Conserto pós-merge v1.4.278 — restaurar helper de teste por script, teste do fork envelhecido pelo upstream, ratchet de bloqueio, max-lines por extração
metadata:
  type: feedback
---
- **Restaurar helper de teste apagado**: script de fechamento de imports (`git show <commit-do-corte>^:<path>` + busca recursiva de import relativo/`@/` que não existe) e reescrita dos importadores; nome `x.brza.test-support.ts`. Rode sempre depois o `closure` para tirar o que sobrou sem importador (rig ACP inteiro caiu).
- **`git rm` o teste tracked que você apaga**: `rm` solto quebra `check:test-file-runners` (ENOENT no `pnpm lint`).
- **Teste do fork "que passa contra o upstream" nem sempre passa**: rode antes de aceitar o brief. O antigravity do upstream concede full-access no launch; o teste de modo ao vivo era do modelo velho.
- **Corpo de raciocínio no upstream 278**: texto novo entra por revisão salva e vira spans de palavras no fade; teste usa `journalRevision` + `waitFor` + `document.body.textContent`, não `getByText` do texto inteiro. Cartão de mensagem do agente não vem mais dobrado; foco de aprovação cai num botão dentro do card.
- **Ratchet main-blocking-helper**: cobra por referência ao helper no arquivo; dobrar duas chamadas em um helper privado tira a cobrança (router). Código async-ável (pino de conta) vira `await`; o cache de `existsSync` e o mkdir de arranque sobem no baseline com `# why`.
- **max-lines**: extraia o trecho do fork para `brza/` ou vizinho (tipo base, mensagem, hook de fonte); mover uma prop do pai para o filho derivando de outra prop (`markdownDocuments !== undefined`) zera linhas no arquivo do upstream.
- **`oxfmt` num laço sobre `git diff --name-only` pega arquivos de outros agentes**: use só a lista dos seus.
- **`pnpm typecheck` mudo = verde**; confira com `echo $?`. `EditorTypography` não é exportado: use `ReturnType<typeof useEditorTypography>`.
- **`import()` em tipo é proibido pelo oxlint**: `import type { X as XComponent }` + `typeof XComponent`.
