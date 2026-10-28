---
scope:
  - brza-studio
date: 2026-10-28
tags:
  - chat
---

# O P54 do PLN-001, a imagem da ferramenta extraída para arquivo

Anderson autorizou o P54 do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md)
na sessão do `brza-workspace` de 2026-10-28 ("siga com P54"), só ele: o P55, o P56 e o P57 ficaram fora. O passo rodou
na sessão `pln-001-p54`, aberta no `brza-studio`, direto na `master`, com push e sem PR, como o pedido mandou. Commit
`brza-studio@44ed13bfec9`. A evidência detalhada está no P54 do plano.

## O que se fez

- **A extração.** O `brzaToolResultImages` (`src/main/native-chat/brza/brza-tool-result-images.ts`) lê os blocos `image`
  do `content` do `tool_result`. O base64 vai para `<temp>/brza-tool-images/<sha256 de 16>.<ext>` e volta como
  `image-ref` com o `path`; a URL vira `image-ref` com a `url`; fora de gif, jpeg, png e webp, nada entra.
- **O campo.** `images?: NativeChatImageRefBlock[]` no `NativeChatToolResultBlock`, no corpo `tool-call` do journal e no
  schema do journal, nos dois lugares em que o resultado mora: o corpo `tool-call` e o bloco `tool-result` da mensagem.
  Os dois decoders o preenchem, e a projeção do journal ao renderer o leva.
- **Os testes.** Um arquivo só do BrzA, `brza-tool-result-images.test.ts`, com a extração, os dois decoders, a projeção
  e o schema; os três casos dos decoders falharam pela asserção antes da montagem.

## Os dois pontos "A conferir no passo" do D42

- **A tradução ao vivo é síncrona.** O `journalClaudeMessage` não espera nada, e o `claudeToolResults` devolve o
  resultado na hora. A gravação vai ao mesmo temp do colar (`getPath('temp')`), mas síncrona: `writeFileSync` num
  `.partial` e `renameSync`, e o arquivo que já existe não é regravado. Sem o `AppEnvironment`, cai no `os.tmpdir()`.
- **O relay ao mobile não rejeita o campo.** O `sanitizeNativeChatRpcBlock` espalha o bloco `tool-result`, o journal
  guarda chave desconhecida, e o mobile não valida o bloco por schema. O campo vai no relay, e o mobile o ignora (R36.4).

## Desvios

- **X23** — o `type` das imagens no schema do journal ficou aberto (`z.string()`): o literal `'image-ref'` abria um
  conjunto fechado novo, e o `journal-closed-sets.test.ts` pede, para isso, subir a versão da linha.
- **X24** — os testes do P54.1 e do P54.2 moram num arquivo só do BrzA, com a projeção e o schema, e não no teste dos
  decoders do upstream.
- **X25** — o tipo do journal e a projeção estão no teto de 300 linhas do `max-lines`. O tipo passou a usar o alias
  `BrzaToolCallMetadata`, e a projeção lê `call.callId` em vez de desestruturá-lo, para o campo caber sem suprimir a
  regra.

## O check

O `pnpm check:changed --base=origin/master` deu 20 de 22. Os dois vermelhos são preexistentes:

- o import boundaries, pelo `external-subcommand.ts`, na issue de mesmo assunto;
- 25 testes em 13 arquivos, entre eles o updater, os goldens do sidebar com "Orca server", o `open-uncommitted-entry`
  e o `claude-stop-ack-race`. Rodados na `master` limpa (`9747ac2b68d`, com o P54 no `stash`), falham os mesmos 25.

Os testes relacionados ao que o P54 tocou levam cerca de 30 minutos com dois workers, porque os tipos compartilhados
alcançam uns 58 mil testes. A saída do check corta a lista dos vermelhos. Ela saiu de uma segunda corrida com
`--reporter=json`.

## O que fica

O P55 (a miniatura na linha) e o P56 (a miniatura do texto solto), que esperam a autorização de Anderson. O P55 precisa
ler o `path` no temp pelo acesso de imagem do chat.
