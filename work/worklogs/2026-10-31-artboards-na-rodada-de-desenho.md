---
scope:
  - workspace
  - brza-studio
---

# Os artboards na rodada de desenho de interface

Anderson perguntou, na sessão `workspace`, se o chat podia mostrar os artboards de um artefato na rodada de desenho de
interface, como numa sessão do Cowork. A sessão não conseguiu abrir o link do Cowork, que é privado.

## O que o chat do BrzA Studio já faz

- **HTML vivo na resposta:** a skill embutida `orca-chat-visuals`
  (`resources/native-chat-visuals/skills/orca-chat-visuals/SKILL.md`, no `brza-studio`) grava um `.html` no
  `ORCA_CHAT_SCRATCH_DIR`, e a linha `::orca-visual{file="…" title="…"}` monta a página na mensagem, com o tema do app.
  Até 8 por resposta e 512 KB cada; o shell injeta os tokens do tema ativo
  (`src/shared/native-chat/native-chat-visual-shell.ts`).
- **Imagem:** `![alt](caminho)` mostra a miniatura e amplia ao clicar (`NativeChatMarkdownImage.tsx`), também com
  arquivo do scratch do chat.
- **O interruptor** `nativeChatVisuals.isEnabled` existe; a sessão não conferiu se está ligado no perfil.

## As rodadas

- **O caminho:** das três opções — o `::orca-visual` que já existe, uma captura em PNG ou um componente de galeria no
  app —, Anderson respondeu: "opção 1 + um mecanismo para podermos converter a opção escolhida em PNG para ser salva nas
  notas".
- **O mecanismo:** as quatro respostas foram as recomendadas — "brza shot, fora do app", o PNG "Na pasta do plano", a
  regra na "Norma, na skill plan-runner" e o script numa "Sessão nova do tools-kit".

## O que foi feito

- **A norma**, na `master` (`89f8fe1`), em `.claude/skills/plan-runner/references/open-and-plan.md`, Desenhar, passo 3:
  a rodada do Desenho vai na mensagem, em texto, e cada alternativa de interface é um artboard `::orca-visual` com a
  letra da opção no `title`; fora do chat, o artboard vai ao scratch e a rodada leva o caminho. O `brza note sync`
  levou a norma ao `studio`, ao `tools-kit` e ao `workspace`.
- **A memória** "A rodada do Desenho vai no chat" subiu à norma nesse passo e saiu de `memory/`.
- **O `brza shot`** foi pedido à sessão `tools-kit-brza-shot`, aberta pelo `brza sessions` no worktree do `tools-kit`,
  com a especificação e o terreno. Ela também propaga à norma o trecho do PNG — o passo 4 do Desenhar e a linha
  **Arquivos** do `plans/README.md` —, que ficou fora daqui para a norma não apontar para um comando que ainda não roda.
