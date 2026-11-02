---
name: brza-studio-native-chat-validacao
description: Como validar mudança visual do native-chat no brza-studio (fixtures:shot, lint de base quebrada, testes que o prompt não lista)
metadata:
  type: project
---

- `pnpm fixtures:shot 'native-chat/*'` só cobre 4 fixtures (cartão de pergunta, menus, strip, mensagem do agente). Estado vazio, composer, linha de atividade, anel e cabeçalho não têm fixture: para vê-los, escreva um `*.fixture.tsx` ao lado do componente (o cabeçalho precisa de `setup()` criando a aba com `useAppStore.getState().createUnifiedTab` e `makeFolderWorkspace`). O `NativeChatQuestionCard.fixture` já traz o `NativeChatContextUsageRing` a 21%.
- `pnpm lint:ast-grep` e `pnpm lint:design-system` falham aos milhares na base (4253 erros `shadcn(no-restyle)`, inclusive o `rounded-full` do botão de enviar que já existia): filtre por arquivo tocado, não rode como gate. O gate é o `pnpm check:changed --base=master --maxWorkers=2` (24 checks, ~90 s, verde).
- Testes de componente do native-chat rodam com happy-dom e **sem jest-dom em alguns arquivos** (`NativeChatContextUsageRing.test.tsx` usa `vi`/`expect` puros: `toHaveClass` dá "Invalid Chai property"; use `className`). O `turn-indicator.test.tsx` tem jest-dom.
- O `turn-indicator.test.tsx` tem 4 asserções do spinner (linhas ~115, ~160, ~271, ~383), não só as 2 que o plano cita.
- Suíte inteira do pacote: `pnpm test src/renderer/src/components/native-chat --maxWorkers=2` (389 arquivos, ~100 s).
- Token de cor do chat que muda por tema vai nos blocos que o `main.css` já divide: `:root, .native-chat-appearance[data-native-chat-scheme='light']` e `.dark, .native-chat-appearance[...='dark']` (~linhas 449 e 492). Em `:root`/`.dark` sozinhos, o chat com tema de catálogo de esquema oposto ao do app pega a cor errada (provado com o fixture `composerFocusOppositeScheme`). O chat com o tema BrzA padrão não tem o atributo `data-native-chat-scheme`; só tema de catálogo (`followsAppScheme: false`) o põe. Por isso nunca tire o token de `:root`/`.dark`: junte o seletor do atributo a eles.
- Para forçar esquema oposto em fixture: `data-native-chat-scheme` + `nativeChatThemeSurfaceStyle(<NativeChatTheme fabricado com followsAppScheme:false>)` no wrapper `.native-chat-appearance`; o esquema do app lê-se de `document.documentElement.classList.contains('dark')`.
