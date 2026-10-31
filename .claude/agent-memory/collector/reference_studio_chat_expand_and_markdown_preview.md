---
name: studio-chat-expand-and-markdown-preview
description: Onde mora o expandir do bloco de código do chat, o renderizador de Markdown do editor (olho/lápis) e o que é reaproveitável fora do editor (brza-studio, 2026-10-31)
metadata:
  type: reference
---

Repo `~/Projects/brza-studio`, `src/renderer/src/components/`:
- O botão expandir NÃO está no `native-chat/NativeChatCodeBlock.tsx` (esse só tem quebra, Run e copiar). Está em `native-chat/brza/BrzaExpandLayer.tsx`, camada delegada por DOM (hover na raiz `[data-native-chat-root]`, só aparece se o bloco rola), montada por `brza/BrzaNativeChatDock.tsx` <- `NativeChatContextClearFade.tsx`. Compartilhada com saída de ferramenta, diffs e aprovação (atributo `data-native-chat-code-content`). Recebe elemento DOM, não props React.
- Editor: olho = `editor/MarkdownPreview.tsx` (acoplado ao store); núcleo só-string = `editor/MarkdownPreviewBody.tsx` (já usado em `IpynbCellEditor.tsx` com `components={}`); lápis = Tiptap `RichMarkdownEditor` (exige arquivo, não serve para string). Seletor `editor/EditorViewToggle.tsx` é controlado e sem store.
- Tema: `editor/use-markdown-surface-theme.ts` + `markdown-surface-theme.ts` (P60 do PLN-001).
- O chat renderiza mensagens com `NativeChatMarkdown` -> `sidebar/CommentMarkdown.tsx`, outro renderizador (não o do editor).
- Mobile não tem expandir de código (só `Maximize2` do visual inline).
- Plano: P25 (olho) e P60 (tema) em `plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md`; D20/D47 no `-design.md`.
- Atalho: `grep -rn "data-native-chat-code-content"` mostra todas as superfícies que o expandir atende.
- Pedido do usuário citava "expandir, quebra e copiar" no bloco: o expandir é o botão flutuante, não parte da barra montada pelo componente; confira o componente certo antes de assumir.
