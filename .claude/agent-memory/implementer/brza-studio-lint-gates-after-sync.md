---
name: brza-studio-lint-gates-after-sync
description: Como corrigir as travas do pnpm lint do brza-studio depois de um merge do upstream (max-lines, anti-slop, focus-read) e armadilhas de ambiente
metadata:
  type: project
---

- **max-lines conta só linha de código** (sem branco nem comentário): `.oxlintrc.json` dá 300 `.ts`, 400 `.tsx`, 800 teste.
  Para saber se o upstream já passa, grave `git show <tag>:<arq>` num vizinho `*.zzupstream.ts` e rode o oxlint nele
  (apague depois); o `.tsx`/teste só casa o limite certo se o nome terminar em `.test.tsx`.
- **Não cabe `/* oxlint-disable max-lines */`**: o `check-max-lines-ratchet` barra bypass novo. Divida: o trecho do fork vai
  para um módulo vizinho (`brza/` no native-chat; `config/build-plugins/` não tem `brza/`), o teste vira outro arquivo.
- **Rebrand pode estourar o limite**: trocar "Orca" por "BrzA Studio" quebra a linha no oxfmt (+2 linhas). Encurtar a
  frase sem mexer na marca resolve; confira que nenhum teste casa a mensagem.
- **focus-read-ratchet**: `openHttpLink` é leitor da configuração (conta por chamada). O padrão de dono é
  `openOwnedHttpLink(url, { sourceOwner })`, com `resolveNativeChatHttpLinkSourceOwner(useAppStore.getState(), worktreeId)`
  e o `worktreeId` do `NativeChatMarkdownImageOwnerContext`.
- **anti-slop**: `object` como parâmetro vira tipo nomeado (`Pick<Host, …>` serve); `Reflect.get` num método privado do
  tiptap vira cast para um tipo nomeado de uma propriedade opcional.
- **`pnpm tc` não roda o projeto node se qualquer arquivo tiver erro de sintaxe** (varredura de outro agente quebra
  arquivos); tipe só os seus com um `tsconfig` temporário que estende `config/tsconfig.node.json` (`composite:false`,
  `noEmit`, `include` curto) e rode `node_modules/.bin/tsc -p`. Apague-o depois.
- **No zsh, `$(cat lista)` não separa palavras**: use `${=VAR}`. `bun` não está no PATH fora do `pnpm`; rode o oxlint
  com `node node_modules/oxlint/bin/oxlint`.
