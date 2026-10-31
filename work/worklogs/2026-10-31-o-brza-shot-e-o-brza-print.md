---
scope:
  - workspace
  - brza-studio
---

# O brza shot e o brza print

O pedido veio da sessão do workstream `workspace`, em 2026-10-31: construir o `brza shot`, que converte em PNG o
artboard escolhido numa rodada de desenho de interface, para a pasta do plano. A rodada de lá, respondida por Anderson,
fechou três pontos:
- "brza shot, fora do app": `brza shot <arquivo.html> <destino.png> [--theme light|dark] [--width 1280]`, no Chrome
  sem janela e com o tema do `main.css`;
- "Na pasta do plano": `plans/PLN-NNN-…/PLN-NNN-<assunto>.png`, com link no item `D`;
- "Sessão nova do tools-kit".

No meio do trabalho, Anderson pediu nesta sessão o `brza print`: "adicionar tbm, ao lado de `brza-shot` um
`brza-print`, pra tirarmos prints quando estivermos fazendo a conferencia".

## O que Anderson respondeu sobre o brza print

- **Alvo**, primeira rodada, em texto livre: "seria para os passos de conferencia de qualquer plano, em qualquer
  projeto, como no `fixfy_app`, por exemplo". As opções eram o dev build pelo CDP, qualquer janela pelo macOS e os
  dois.
- **Alvo**, segunda rodada, já com o `fixfy_flutter` e o simulador à vista: "Simulador, emulador e janela
  (Recomendado)".
- **Destino:** "Pasta do plano, por caso (Recomendado)", `PLN-NNN-C1.png`, com link no Observado do caso.
- **Norma:** "Sim, junto do brza shot (Recomendado)".

## O que se fez

- **`291cf30` na `master`:** `feat(brza): brza shot, o PNG do artboard, e brza print, o print da conferência`.
  - **`scripts/brza/brza-shot`** monta o shell do `buildNativeChatVisualDocument` sem o script de ponte: o
    `<html class>`, o CSP com as CDNs, os tokens no `:root` e o `BASE_CSS`. A lista de tokens, as CDNs e o `BASE_CSS`
    saem do código do `brza-studio`, e o comando para e diz o nome quando o código muda de forma. Os tokens saem do
    `:root` e do `.dark` do `main.css`, na ordem do arquivo, com as cores do `tailwindcss/theme.css` do `node_modules`
    e o `var()` resolvido em Python. O `--background`, o `--foreground` e o `--font-mono` vêm do escopo do chat, como o
    `SCOPED_SOURCES` do app manda. O Chrome roda sem janela, pelo `--remote-debugging-pipe`, com o pipe ligado nos fds
    3 e 4 por um `sh -c exec`. Ele mede a altura como o `measure()` do shell, depois das fontes e do `--wait`, ajusta a
    janela e captura. Além do que a rodada fixou, há o `--scale`, 2 por padrão, o `--wait` em ms, 500 por padrão, e o
    `--force`.
  - **`scripts/brza/brza-print`**, sem opção, acha o único aparelho aberto: o simulador iOS ligado
    (`xcrun simctl io <udid> screenshot`) ou o Android do adb (`adb exec-out screencap -p`). Com mais de um, ou
    nenhum, ele para e lista o que achou. O `--app NOME` captura a janela da frente do app pelo `screencapture -l`, com
    o id lido do CoreGraphics por JXA. O print vai a um temporário e só vira o destino depois de conferido como PNG.
  - **Os testes:** 13 no `test_brza_shot.py`, um deles com o Chrome de verdade, que confere a altura inteira e a cor
    do canto nos dois temas, e 11 no `test_brza_print.py`, com as ferramentas trocadas por falsas. A suíte
    `python3 -m unittest discover -s scripts/brza/tests` deu `Ran 245 tests … OK` no worktree. Na `master`, a suíte
    caiu com o reinício do BrzA Studio, e os 24 testes novos rodaram de novo e passaram.
- **`5dd8254` na `master`:** `docs: a imagem do plano sai pelo brza shot e pelo brza print`, pela skill
  `agent-instructions-writer`:
  - `plans/README.md`, linha **Arquivos**: a imagem fica na pasta do plano, `PLN-001-<assunto>.png` pelo `brza shot` e
    `PLN-001-C1.png` pelo `brza print`;
  - `.claude/skills/plan-runner/references/open-and-plan.md`, Desenhar, passo 4: a alternativa de interface escolhida
    vira PNG pelo `brza shot`, e o item `D` linka a imagem;
  - `.claude/skills/plan-runner/references/plan-template.md`, Casos manuais: o Observado linka o print do
    `brza print`;
  - o `README.md` não lista os comandos do `brza` e ficou como estava.
- **O `brza note sync`** levou a `master` aos três workstreams. No `tools-kit`, o primeiro merge parou nas cópias de
  trabalho dos scripts, sem commit e idênticas às da `master`. Elas saíram, e o segundo sync mesclou.

## A conferência

- **O `brza shot`, num artboard que usa os tokens:** o `--muted-foreground`, o `--card`, o `--border`, o `--radius`, o
  `--primary`, o `--secondary`, o `--destructive`, o `--accent`, do `--chart-1` ao `--chart-5`, e um bloco de 600 px
  para provar a página inteira. O artboard foi capturado nos dois temas, com `--width 900 --scale 1`, e cada PNG saiu
  com 900×939 px:
  - claro: [2026-10-31-o-brza-shot-e-o-brza-print-claro.png](2026-10-31-o-brza-shot-e-o-brza-print-claro.png);
  - escuro: [2026-10-31-o-brza-shot-e-o-brza-print-escuro.png](2026-10-31-o-brza-shot-e-o-brza-print-escuro.png).
- **O fundo do escuro é `#161616`, e não `#0a0a0a`**, porque o `--background` do visual é o `--chat-canvas`, que no
  `.dark` mistura 5% do primeiro plano (`--chat-canvas-mix: 5%`). É o que o chat mostra.
- **O destino que já existe** saiu com `já existe; use --force para sobrescrever`, código 2.
- **O `brza print`, sem opção:** com o simulador iPhone 18 Pro ligado, o print saiu com 1206×2622 px, só com a tela do
  aparelho, que mostrava o login do app da Fixfy.
- **O `brza print --app "brza studio"`** caiu na mensagem da permissão de Gravação de Tela, que o BrzA Studio não tem:
  o `screencapture -l 7858` dá "could not create image from window".
- **O `brza install --all`** ligou o `brza-shot` e o `brza-print`, e o `brza shot --help` e o `brza print --help`
  responderam pelo CLI do app.

## O que ficou aberto

- **O `brza print --app` só funciona depois que Anderson der ao BrzA Studio a permissão de Gravação de Tela**, em
  Ajustes do Sistema › Privacidade e Segurança. O simulador e o Android não dependem dela.
- **O `brza shot` não segue um tema personalizado do app**, como a rodada aceitou.

## Fora do workspace

- **Os links `~/.local/bin/brza-shot`, `~/.local/bin/brza-print` e `~/.local/bin/brza-agents`**, pelo
  `brza-install --all`. O `brza-agents` faltava desde antes, e o `--all` o ligou junto.
  - **Risco:** nenhum além do comando no PATH; cada link aponta para o checkout da `master`.
  - **Estado:** ativos.
  - **Como desfazer:** `rm ~/.local/bin/brza-shot ~/.local/bin/brza-print ~/.local/bin/brza-agents`.
