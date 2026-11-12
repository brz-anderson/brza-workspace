---
name: brza-studio-sync-256-chat-ui-lessons
description: Lições do g1-chat-ui do sync v1.4.256 (reorganização em subpastas do native-chat): tsc com TS 7 e marcadores, import de símbolo movido, fork duplicado
metadata:
  type: project
---

- **O `node_modules/.bin/tsc` é o TS 7 nativo, sem API JS**; marcador de conflito em outro grupo (`TS1185`) esconde o semântico. Use um `config/tsconfig.<tmp>.json` que estende o `tsconfig.web.json` com `include` só das pastas suas (`native-chat/**`, `settings/appearance/chat/**`, `preload/api*`) e apague ao fim.
- **O `fix-imports-g3.py` (em `/private/tmp/brza-sync-<v>/`) só conserta módulo que sumiu** (por nome único). Não conserta símbolo que mudou de módulo (`captureNativeChatComposerFocusIntent`, `NativeChatLiveSession`, `NativeChatFileLinkContext`, `structuredAgentSessionDraftScopeKey`...): ache com `git grep -n "export.*<símbolo>" <tag> -- src` e corrija o import, e os `vi.mock` do teste junto.
- **Arquivo do fork que o upstream renomeou aparece `UU` no caminho novo**; `git diff <base> HEAD -- <caminho velho>` mostra o que o fork mudou (ache o velho por `git ls-tree -r HEAD | grep "/<nome>$"` na raiz do repo, não em subpasta).
- **O auto-merge deixa `translate(` sem import em arquivo que o upstream passou a `useTranslate()`** (`ChatBehaviorSetting`, `NativeChatPromptCollapse`): o `tsc` acusa TS2304; troque por `t(`.
- **O upstream apaga testes "de baixo valor" que o fork reescreveu**: se o teste cobre comportamento do fork (120 colunas, faixa recolhida), mantenha o lado "ours" e restitua os imports/constantes (`fireEvent`, `waitFor`, `ASK_CALL`) que o corte do upstream tirou.
- **Seletor de tema de Configurações virou popover** (`SettingsSearchableSelect`): teste que acha `Search terminal themes` precisa clicar no combobox e usar `role=option`.
- **Duas features iguais de novo**: o Fork do upstream (`use-native-chat-fork`) e o Bifurcar do fork convivem montados (provider do fork aninha o do upstream); ponto de rodada, não decisão.
- **`git add` falha às vezes com `index.lock`** (outro agente): use laço com retentativa.
- Relacionadas: [[brza-studio-sync-251-lessons]], [[brza-studio-upstream-merge-conflicts]].
