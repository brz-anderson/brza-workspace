---
name: brza-studio-sync-263-chat-ui-lessons
description: Lições do g1-chat-ui do sync v1.4.263 - nome repetido entre fork e upstream, dono de editor por aba, linha de limite de uso, max-lines exato, testes que o padrão 13px envelhece
metadata:
  type: project
---

- **Fork e upstream criam o mesmo nome em pastas diferentes** (`NativeChatStructuredPromptCard`): mova o do fork para `brza/` com nome novo; fica um arquivo do upstream sem uso, e isso é aceito.
- **O upstream passou o editor da caixa a um dono por aba** (`useNativeChatComposerEditor`, editor criado uma vez por escopo). O modo Markdown do fork precisa de `variant` no dono para recriar o editor ao trocar o modo; o placeholder vem do `aria-label` do editorProps, não de ref do componente.
- **Linha de limite de uso virou `NativeChatUsageLimitRow`**: o P79 (Continuar em outra conta) vai no slot `tools` e ao lado do Continue; o teste do fork precisa de `usageLimit.resetsAt` futuro para a fase "waiting".
- **Session com exatamente 400 linhas contadas**: esconda a parte do fork num hook de `brza/` que devolve tupla `[prompt, slot]`; cada linha a mais do fork estoura.
- **O padrão de 13px e a fonte do sistema envelhecem testes do fork** (`22*size/13`, chars por linha 53, `--chat-font-family` contém `system-ui`); contagem de visitas do índice de remetente passou a 10n.
- **O tsc inteiro da web roda em ~70 s** quando nenhum grupo deixa marcador; `grep` pelos seus caminhos basta. O `/private/tmp/brza-sync-<v>/fix-imports-g3.py` com o regex de alvo trocado conserta módulos sumidos; os de nome ambíguo (`runtime-client-target`, `@/lib/utils`) são à mão.
- Helpers de teste que o upstream apagou (`*-test-viewport`, `*-test-support`) quebram testes `brza/`: é do grupo UD.
