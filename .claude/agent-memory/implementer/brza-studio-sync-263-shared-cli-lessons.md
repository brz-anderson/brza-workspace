---
name: brza-studio-sync-263-shared-cli-lessons
description: Sync v1.4.263 em shared/cli/config/mobile - helper de bloco diff3, fork-only com import velho, gerador RPC, zsh sem word-split, locale pelo valor da tag
metadata:
  type: project
---

- **Helper de bloco**: um `rb.py` com `re.compile(r'<<<<<<< ours\n(.*?)\|\|\|\|\|\|\| base\n(.*?)=======\n(.*?)>>>>>>> theirs\n', re.S)` e `apply(path, fn(i, ours, base, theirs))` resolve cada bloco por índice; mais seguro que sed (o `sed 's#...#'` com aspas simples dentro falhou duas vezes no macOS e abortou o `&&` seguinte sem aviso).
- **Cadeia `&&` com sed falho engole o python seguinte**: confira com `grep` de marcador depois, não confie que o bloco foi aplicado.
- **Fork-only que o upstream moveu**: arquivos do fork em `src/shared/*.ts`, `src/shared/native-chat/brza/`, `src/shared/native-chat/tools/brza/`, `src/cli/brza/` ficam com import velho sem aparecer como conflito. Varra com um script que resolve import relativo (`./`, `../`) e lista os que não existem; filtre os `UD` (são de outro grupo) e os falsos positivos de template (`generated`, `?raw`, `./panel`, `./worker`).
- **zsh não divide `$VAR` com lista de arquivos**: use `bash -c '…'` para `for f in $OUT`.
- **Gerador do catálogo RPC (`generate-rpc-params-catalog.mjs`) empacota o main**: não roda no meio do sync (outros grupos com import quebrado). Una os imports à mão e deixe o `pnpm generate:rpc-params-catalog` para o fim.
- **`locale-conflicts.md`**: o "nosso" é o valor do HEAD (v256 do upstream, normalmente sem edição do fork); o arquivo no disco já estava com o valor cru da 263. Compare com `git show v1.4.256:` e `v1.4.263:`; só o que o fork criou (como `pt.goToAgent`) é tradução própria. Chave com ponto no nome: walk guloso por prefixo; confirme `json.dumps(indent=2, ensure_ascii=False)+'\n'` idêntico ao arquivo antes de gravar.
- **Teste do upstream reescrito** (`macos-terminal-host-bundle.test.mjs`) e testes apagados: pegue o do upstream e só reponha o teste que é identidade do fork (`electron-builder-config.test.mjs`, imports de `brand-identity`).
- **Entrada velha em `cli-main-entry-names.ts`** (`ipc/command-path/command-path-resolver`) continua exigida por `cli-main-entry-contract.test.ts` e `asarUnpack`; manter e sinalizar.
- Mobile: os arquivos do fork em `mobile/.../transcript/brza/` não se mexem; a fonte de caminho do `src/shared` ganhou um `../` ao descer para `agent-messages/`, `message-content/`, `tool-results/`.
