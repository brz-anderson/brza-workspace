---
scope:
  - brza-studio
date: 2026-10-30
tags:
  - chat
---

# Os ícones de skill e de MCP trocados no chat

Anderson pediu, numa sessão do `brza-workspace` aberta na `master`: "inverta o icone de chamada de skill e de
plaugin/mcp na visualização de chat". Feito no `brza-studio`, commit `f93ab625a66` na `master`, sem plano.

## O que se fez

- **A troca.** A chamada de skill passa a desenhar o `plug`, e a de MCP o `sparkles`, no desktop e no mobile.
  - **A skill:** a categoria BrzA `skill` em `src/shared/native-chat/tools/brza/brza-tool-categories.ts` troca o
    `sparkles` pelo `plug`.
  - **O MCP:** a tabela de cima, `NATIVE_CHAT_TOOL_ICON_NAMES` em
    `src/shared/native-chat/tools/native-chat-tool-icon.ts`, troca o `mcpToolCall` para `sparkles`. Os servidores
    com categoria BrzA própria — Figma, Jira, Confluence, Firebase e context7 — mantêm o ícone deles.
- **O tipo.** As tabelas de glifos de cima já desenham o `plug` e espalham as BrzA por cima, o que dava chave
  repetida. O `plug` entra como `BrzaUpstreamIconName`, e as tabelas BrzA passam a ser tipadas por
  `BrzaGlyphIconName`, sem ele.
- **Os testes.** Cinco arquivos de teste com a expectativa trocada.

## O que rodou e o que deu

- **Testes do desktop:** 5173 passaram, em `src/shared/native-chat` e `src/renderer/src/components/native-chat`, pelo
  `config/vitest.config.ts`.
- **Typecheck:** passa no mobile. No desktop sobra um erro em `src/main/updater/updater-enabled.test.ts`, que acontece
  igual sem a troca.
- **Testes do mobile:** 8 arquivos de `src/session/native-chat/transcript` falham com e sem a troca, porque o mock de
  `lucide-react-native` deles não tem o `GitBranch`.
- **Lint:** oxlint, ast-grep e oxfmt limpos, também no hook de pré-commit.

## Aberto

- **A troca não foi vista no app rodando**, só nos testes.
- **A linha do `mcpToolCall` é de cima**, fora da pasta `brza/`, e entra em conflito no próximo merge do upstream.
- **As 8 falhas do mobile** seguem sem dono.
