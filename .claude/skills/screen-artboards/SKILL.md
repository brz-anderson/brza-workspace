---
name: screen-artboards
description: >-
  Gera artboards de protótipo de tela — web, mobile e desktop — como HTML que o chat do BrzA Studio mostra inline
  (::orca-visual): a tela dentro de uma moldura de aparelho (janela macOS ou Windows, iPhone, Android, navegador em 375,
  768 e 1280), com o pacote de tokens visuais do projeto (o do brza-studio extraído do código, ou o neutro), conferida
  pelo PNG em cada largura e promovida a PNG na pasta do plano ou da issue. Use sempre que for mostrar como uma tela fica
  — "faz um protótipo da tela X", "mostra as alternativas de layout", "mockup do app no celular", "como fica no Windows",
  "artboard", a rodada de Desenho de um plano com opção que muda o que se vê —, mesmo que a palavra "artboard" não
  apareça. Não use para gráfico, diagrama ou painel de dados (use a orca-chat-visuals ou a dataviz) nem para mexer no
  código de verdade do app.
---

# Artboards de tela — protótipo em moldura, com os tokens do projeto

Um artboard é uma tela de mentira que se parece com a de verdade: a moldura do aparelho, as cores, as fontes e os raios
do projeto, e o conteúdo que a alternativa propõe. Ele serve para Anderson escolher entre caminhos olhando, antes de
alguém escrever o código. Por isso a skill cuida de duas coisas que o HTML solto erra sempre:

- **Parecer o app**, pelos tokens do próprio projeto, e não por uma paleta inventada que muda de artboard para artboard.
- **Caber no chat**, que tem 736 px de largura, sem cortar a janela de 1280 px nem estourar a coluna. O `zoom` da
  moldura ajusta a tela à largura, e o PNG é a conferência, porque quem gera o artboard não vê o chat.

`$A` é abreviação de `python3 -I .claude/skills/screen-artboards/scripts`, só nesta página: escreva o comando por extenso, rodado da raiz do worktree (no zsh, `$A/artboard.py` numa variável não se divide e falha). O código de visual e de PNG é
o de `.claude/scripts/skillkit/` (o `brza shot` por baixo).

## Os arquivos e quando ler

| Preciso de… | Leia / rode |
| :-- | :-- |
| escolher a moldura e a largura | `references/frames.md` |
| escrever o corpo da tela (o fragmento HTML) | `references/frames.md`, "O fragmento"; os tokens em `references/tokens.md` |
| um artboard novo | `$A/artboard.py new <slug> --frame macos\|windows\|iphone\|android\|browser --pack brza-studio\|neutral --body tela.html [--letter A --title …]`; `--window-title`, `--url` e `--height` mudam a barra da janela, o endereço e a altura |
| os tokens do projeto, e se derivaram do código | `references/tokens.md`; `$A/tokens.py check brza-studio` |
| extrair o pacote de novo | `$A/tokens.py extract brza-studio` |
| conferir pelo PNG, em cada largura | `$A/artboard.py shot <artboard>.html --out-dir <scratch>` e ler cada imagem |
| levar a escolhida ao plano ou à issue | `$A/artboard.py promote <artboard>.html --plan PLN-NNN --name <assunto>` (ou `--issue <caminho>`) |
| as regras do visual no chat | `references/chat-rules.md` |
| a rodada de Desenho com alternativas de tela | `references/design-round.md` |

## O fluxo

1. **A plataforma e o projeto.** Do pedido: desktop (o BrzA Studio é Electron, macOS e Windows), mobile (iPhone,
   Android) ou web (navegador). O projeto escolhe o pacote: `brza-studio` para o app, `neutral` para wireframe ou projeto
   sem pacote. Projeto novo ganha pacote pelo `tokens.py extract <projeto> --src …` (`references/tokens.md`).
2. **Os tokens em dia.** Com o pacote de um projeto, `$A/tokens.py check <projeto>` antes de desenhar. Deriva não barra o
   artboard — o `new` avisa —, mas diga a Anderson, porque a tela vai sair com a cor velha.
3. **O fragmento.** Escreva só o conteúdo da tela, em HTML com CSS inline que usa `var(--sa-*)` — nunca cor fixa —, num
   arquivo no scratch. A moldura, a barra de título, o notch e o ajuste de largura são do script.
4. **O artboard.** `$A/artboard.py new <slug> --frame … --pack … --body <fragmento> --letter A --title "<rótulo>"`. Ele
   embrulha o fragmento na moldura, escopa os tokens no contêiner do mockup, confere as regras do chat (tamanho, rede,
   `100vh`, tokens do Orca redefinidos) e grava no `ORCA_CHAT_SCRATCH_DIR` (fora do chat, no scratch), imprimindo a
   linha `::orca-visual{file="…" title="A — <rótulo>"}`.
5. **A conferência pelo PNG.** `$A/artboard.py shot <artboard>.html --out-dir <scratch>` tira um PNG por largura (e por
   tema, com `--scheme both`). **Leia cada imagem** antes de mostrar: corte, coluna estourada, texto sobreposto e
   contraste ruim se corrigem no fragmento e se gera de novo, com nome novo.
6. **Mostrar.** Cole a linha `::orca-visual` na mensagem, uma por alternativa, até 8 por resposta. Fora do chat, dê o
   caminho do `.html` e dos PNGs.
7. **Promover a escolhida.** Depois da escolha, `$A/artboard.py promote … --plan PLN-NNN --name <assunto>` grava o PNG em
   `plans/PLN-NNN-…/PLN-NNN-<assunto>.png` (ou ao lado da issue) e imprime o link Markdown para o item `D`. O scratch
   some; o PNG fica no git.

## Regras que valem sempre

- **Tokens escopados no mockup, nunca no `:root`.** O chat injeta os tokens do Orca no `:root`, ao vivo; redefini-los ali
  pinta o chat inteiro com a cor do mockup. O script escopa em `.sa-art[data-pack][data-scheme]`, e o fragmento só lê
  `var(--sa-*)`.
- **Um artboard por alternativa.** Na web, as três larguras vão empilhadas no mesmo artboard, cada uma com o `zoom` dela;
  um artboard por largura estoura o limite de 8 visuais com 3 alternativas (PLN-021/R4.5, recomendada, a confirmar).
- **O tema vem do pacote** (`--scheme light|dark|both`), não do chat: o mockup mostra como o app fica, e não como o chat
  de Anderson está (PLN-021/R4.6, recomendada, a confirmar). No `brza-studio`, `both` mostra os dois lado a lado.
- **Sem rede, sem imagem externa.** Ícone em SVG inline; imagem de conteúdo como bloco cinza com rótulo ou `data:` URL.
- **Conteúdo plausível, curto.** Nomes, números e textos com a cara do app, sem lorem ipsum: a escolha é pelo layout, e
  texto falso esconde o problema de quebra de linha.
- **Telas diferentes não são alternativas.** O `--letter` é só para as opções de uma rodada; telas distintas do mesmo
  pedido (a lista no celular e a página do site) saem sem letra, com o nome da tela no `--title`.
- **Nome novo a cada versão.** O chat guarda o visual pelo nome; regravar no mesmo nome não atualiza a mensagem antiga.
