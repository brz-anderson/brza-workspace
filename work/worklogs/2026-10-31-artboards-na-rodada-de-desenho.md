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

## O teste no chat

Rodada de desenho descartável, pedida pela sessão do terminal do `workspace`, para testar o fluxo de ponta a ponta no
chat do BrzA Studio, sem plano e sem commit do PNG. A tela foi a faixa recolhida da pergunta e da aprovação do chat
estruturado (`NativeChatPromptStrip`, do `a0eefa646e4` no `brza-studio`).

- **A rodada:** três artboards no `ORCA_CHAT_SCRATCH_DIR` — A, a faixa mínima de hoje; B, tipo e progresso; C, ícone e
  ação —, cada um com uma pergunta de título longo e uma aprovação, uma tabela, a recomendação C e
  `Custo: … Se paga: …` em cada opção. Anderson respondeu: "C e já coloque na fila pra implementar".
- **A fila:** a issue
  [A faixa recolhida da pergunta e da aprovação com ícone e ação](../issues/a-faixa-recolhida-com-icone-e-acao.md), no
  `studio`.
- **O `brza shot`** aceitou o caminho do scratch, que tem espaço, nos dois temas: `teste-c.png` e `teste-c-dark.png`,
  2560×442, na largura padrão de 1280 px. Os tokens do tema chegaram ao artboard, no claro e no escuro.
- **O PNG padrão escondeu um defeito do artboard.** A grade `1fr 1fr` com título `nowrap` estoura a coluna. A 1280 px
  não aparece; a 736 px, a largura do chat (`--chat-content-max-width: 46rem`), a segunda coluna sai cortada, e o
  shell do visual esconde a barra de rolagem. Com `minmax(0,1fr)`, o `faixa-c2-icone-acao.html` trunca certo a 736 px.
  O que o chat mostrou, então, era provavelmente o corte, e não o PNG de 1280 px.
- **O `--primary` do tema padrão é neutro** (`#171717` e `#e5e5e5`), e por isso o destaque da alternativa C saiu preto
  ou branco. O artboard não tem `--chat-canvas`: o shell repassa só a lista do painel de plugin, os `--chart-*` e as
  fontes (`native-chat-visual-shell.ts:59-68`).
- **O que Anderson viu no chat:** o `title` e a altura saíram certos, e os três empilhados deram para comparar (1.1).
- **A rodada da norma:** Anderson respondeu "1", e na pergunta que desfez a dúvida, "A opção 1 em todas":
  - 2.1, a sessão confere cada artboard pelo PNG a 736 px antes da rodada;
  - 3.1, o `brza shot` passa a 736 px por padrão, pedido à sessão `tools-kit-shot-736`, aberta pelo `brza sessions`;
  - 4.1, o PNG da alternativa escolhida fica ao lado da issue, `a-faixa-recolhida-com-icone-e-acao.png`, gravado no
    `studio` (`1c079c2`).
- **O `--checkout` relativo falha fora da raiz:** `brza sessions … --checkout .worktrees/tools-kit`, rodado no worktree
  do `workspace`, resolveu o caminho a partir do cwd e devolveu `selector_not_found`. Com o caminho absoluto, abriu.
