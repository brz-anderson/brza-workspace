---
scope:
  - brza-studio
tags:
  - chat
---

# Os ícones de skill e de MCP voltam ao que eram

Anderson perguntou com qual ícone o de skill tinha sido trocado e pediu: "reverta". Desfaz a troca do worklog
[Os ícones de skill e de MCP trocados no chat](2026-10-30-icones-de-skill-e-mcp-trocados.md).

## O que se fez

- **O revert.** `git revert --no-commit f93ab625a66` na `master` do `brza-studio`, sem conflito, apesar dos 1575
  commits de upstream que entraram desde então. A chamada de skill volta a desenhar o `sparkles`, e a de MCP o `plug`,
  no desktop e no mobile.
  - **O tipo:** `BrzaUpstreamIconName` e `BrzaGlyphIconName` saem de `brza-tool-categories.ts`, que volta a
    `BrzaToolIconName = BrzaLucideIconName | BrzaBrandLogoIconName`.
  - **O MCP:** o `mcpToolCall` de `NATIVE_CHAT_TOOL_ICON_NAMES` volta a `plug`, e a linha de cima deixa de divergir
    do upstream, o que tira o conflito do próximo merge.
- **O commit.** `brza-studio@e9a3b9745bf`, na `master`, com o push direto. O primeiro push foi recusado porque o
  `563705a7aaf` chegou antes; o `git pull --rebase` passou sem conflito.

## O que rodou e o que deu

- **Testes:** `src/shared/native-chat/tools` e `NativeChatToolRun.identity.test.tsx` → 24 arquivos e 344 testes
  passaram, antes do rebase.
- **Pré-commit:** oxlint, ast-grep e oxfmt limpos.

## Aberto

- **Não rodou o typecheck, nem os testes do mobile, nem depois do rebase.**
- **A reversão não foi vista no app rodando**, só nos testes.
