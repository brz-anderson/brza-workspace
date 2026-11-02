---
scope:
  - brza-studio
  - workspace
---

# PLN-007: o Desenho da marca BrzA

O Desenho do
[PLN-007: A marca BrzA tem símbolo, logotipo e derivadas a partir da chama do app](../../plans/PLN-007-a-identidade-visual-da-marca-brza/PLN-007-plan.md),
depois da entrevista fechada em 2026-10-31.

## O que se levantou

O `designer` rascunhou 8 itens `D` e 14 pontos para rodada, no scratch da sessão (`desenho-rascunho.md`), com sondas:
o `}` corrigido no traço mono, o CoreText do `swift` lendo a Geist woff2 com o peso — o `opentype.js` e o `hb-view` não
leem —, e a grade da Apple para o tile. A sessão conferiu por amostra quatro fatos: o app só leva o `.icns`, o
`#1447e6` dá 2,9:1 no escuro, o cabeçalho do painel do chat não tem título, e o "agente trabalhando" é o spinner do
`NativeChatTurnActivityLine`.

## O que se decidiu

A R4, toda na recomendada: a fonte da marca mora em `brza-studio/resources/brand/`; esta sessão do `brand` desenha o
símbolo e os lockups, e o `brza-studio` só copia o aprovado; o `.icns` sai do SVG pelo `rsvg-convert` e o `iconutil`,
sem o `actool`, o que tira o `icon.json` do caminho do ícone; a execução vai em seis passos e três branches.

A R5: o tile na grade da Apple (T1); o `logo.svg` com o A1 colorido (G2) e o estado vazio com o S1 no degradê (V2), os
dois contra a recomendação; o logotipo dentro do app como texto vivo na Geist.

O `brza shot` quebrou no meio da R5: o merge do upstream v1.4.246 no `brza-studio` moveu o
`PANEL_DESIGN_TOKEN_ALLOWLIST` para `src/shared/plugins/frames/plugin-panel-design-tokens.ts`. Os PNGs da R5 já tinham
saído e foram copiados do scratch; o pedido do conserto foi a
[O brza shot quebra com os tokens do painel movidos no brza-studio](../issues/brza-shot-quebra-com-os-tokens-do-painel-movidos.md),
e o Desenho segue com uma cópia corrigida no scratch, conferida igual pixel a pixel.

A R6: o fio de 1 px com halo no foco (W1); o botão de enviar no degradê da marca (K2, contra a recomendação); o anel no
âmbar e laranja até 89% e no vermelho de alerta de 90% para cima (N1); a chama no cabeçalho apagada sem foco e no
degradê com foco (H1). Com a N1 e a H1, os riscos do M3 e do M5 da R2.6 fecharam. Anderson pediu o artboard do botão
"redondo": o botão do app já é `size-8 rounded-full`, e os artboards o tinham desenhado quadrado — refeito, e a lição foi
à memória do workstream.

A R7, na recomendada: o `--agent-question` vai ao blue-700 no claro e ao blue-400 no escuro, porque o `#1447e6` dá
2,9:1 sobre o fundo escuro; o `brza --help` troca o nome na impressão, num arquivo do fork. Os 14 pontos do rascunho
têm resposta, e o `designer` foi retomado para reescrever o Desenho com elas.

O `designer` reescreveu o Desenho com as respostas e trouxe dois pontos novos, que a R8 fechou na recomendada: o
estado vazio mantém o título com o nome do agente e o subtítulo, e o passo do CLI e dos READMEs volta à branch de
assets depois do chat. O Desenho foi a
[PLN-007 — Desenho](../../plans/PLN-007-a-identidade-visual-da-marca-brza/PLN-007-design.md), e o corte em seis passos,
~20,75 h, foi à R9.

A R9: Anderson respondeu "aceito" ao corte em seis passos, ~20,75 h. Os Passos, a Regressão e os Casos manuais foram
ao plano, que passou a `phase: execution`, sem passo executado. O próximo é o P1, nesta sessão, a pedido.

## O conserto do brza shot, em sessão própria

Anderson pediu o conserto da
[issue do brza shot](../issues/brza-shot-quebra-com-os-tokens-do-painel-movidos.md) "em sessão própria, na conta
`admin@fixfy.com.br`". A primeira tentativa, pelo `brza sessions brza-shot-fix --checkout .worktrees/tools-kit`, subiu
na conta padrão, `anderson@fixfy.com.br` (`~/.claude/sessions/77277.json`): o `brza sessions` abre com a conta ativa do
app, e não com a desta sessão, que roda no perfil `8eee0e1b…` do app. A sessão foi fechada com `--force` antes de
commitar e deixou um teste começado em `scripts/brza/tests/test_brza_shot.py`, na `master`, sem commit.

Numa rodada, Anderson escolheu reabrir pelo terminal, com o `adm-claude` (`CLAUDE_CONFIG_DIR=~/.claude-adm`), e deixar o
teste para a sessão nova. A `brza-shot-fix` roda numa aba de terminal do worktree do `tools-kit`, na conta
`admin@fixfy.com.br` (`~/.claude-adm/sessions/99742.json`), com o pedido em `/private/tmp/pln-007/prompt-brza-shot.md`,
e avisa a `brand-24` pelo correio ao terminar. A issue fecha aqui, no `brand`.

## Fora do workspace

- **A pasta do `tools-kit` confiada na conta admin:** o `adm-claude` pediu a confirmação de confiança da pasta
  `/Users/andepb/Projects/brza-workspace/.worktrees/tools-kit`, e a sessão respondeu "Yes, I trust this folder", que
  grava em `~/.claude-adm/.claude.json`.
  - **Risco:** nenhum além do que a conta padrão já tem; a pasta é deste workspace.
  - **Estado:** ativo.
  - **Como desfazer:** apagar a entrada da pasta em `projects` no `~/.claude-adm/.claude.json`.
- **Uma sessão do Claude na conta padrão, fechada:** o chat `claude_18da3d5b…` da `brza-shot-fix`, aberto pelo
  `brza sessions` e fechado pelo `brza sessions close --force`.
  - **Risco:** o teste que ela deixou na `master`, sem commit.
  - **Estado:** encerrada.
  - **Como desfazer:** nada a desfazer; o teste fica para a sessão nova.
- **Uma aba de terminal no worktree do `tools-kit`**, "brza-shot-fix (admin)", aberta pelo `orca terminal create`, com
  o `adm-claude` rodando.
  - **Risco:** nenhum.
  - **Estado:** ativa.
  - **Como desfazer:** fechar a aba quando a sessão terminar.

O conserto voltou: `8d554e7` na `master`, com o arquivo da lista achado pelo import do shell dos visuais; Anderson
relatou os 98 `unittest` passando e o teste novo falhando antes. A sessão conferiu o commit na `origin/master` e rodou o
`brza shot` oficial: o PNG saiu igual ao da cópia do scratch, e a issue fechou.

## A execução do P1, às 16h30

O P1 rodou no scratch (`/private/tmp/pln-007/brand/`), a pedido de Anderson, e fechou na R10, abaixo.

- O `brza-brand-build.mjs` gera o mestre, o claro, o dev, o S1, o tray e o `logo.svg` a partir do
  `resources/brza-flame-mono.svg` de hoje. O `}` solto sai do `}` do par na escala 1,143, em (9,06; 16,68), que é o D2.
- O mestre desenha o `}` uma vez e o usa três vezes, por `<use>` (D1). O `{` é o `}` espelhado.
- **Fora do D1:** a língua clara e as faíscas não entraram. Pedem o traço da arte de hoje, e isso é desenho à mão. A chama
  sai no degradê sólido. Ponto para a rodada.
- **Conferência:** o `brza shot` do `p1-simbolo.html`, a 736 px, mostra o mestre a 16, 32, 128 e 200 px nos dois temas, o S1
  a 13, 16, 18 e 32 px e o tray em 1× e 4×. O 1024 px não cabe no artboard; saiu pelo `rsvg-convert`. Contra o traço
  original, pelo `magick compare`, a diferença fica só no `}` solto e no `{`, que são a correção do D2 e o espelho.
- O P3 abriu às 16h33, pelo agendamento `262ac74e`: sessão `pln-007-brand-tokens` (chat, `claude_cd58c58e_3ab0_46b3_9d9c_4f80e3996a95`),
  checkout `~/Projects/brza-studio`, na conta padrão do app. A sessão confirmou na lista do `brza sessions list`, como
  `working`. Esta sessão não executa passo do `brza-studio`.
- **A opção 2 desenhada para a comparação**, a pedido de Anderson ("quero ver as opções 1 e 2 lado a lado"): o
  `sparks.mjs` rastreia 15 faíscas do `build/icon.png`, registrado sobre o traço mono; a luz de borda é uma aproximação
  da língua clara, e não rastreada. O `p1-opcoes.png` põe as duas no mesmo tile, nos dois fundos, de 240 a 16 px.
- **A R10: Anderson aprovou a opção 1** ("aprovo a opção 1"), a chama no degradê, sem língua clara e sem faíscas. O PNG
  foi à pasta do plano como `PLN-007-simbolo-a1.png`, e a fonte e o gerador, a `PLN-007-fonte-da-marca/`, porque o P4
  copia dali e o scratch não dura. O `Executado` do P1 ficou em 0,25 h, o tempo de relógio do log (16h29 a 16h40), contra
  as 6,5 h estimadas. O P2 espera o pedido de Anderson.

## A execução do P2

Anderson pediu "siga" e, em seguida, "execute o plano até o final, pule os passos que precisarem de decisão minha,
reporte no final". O P2 rodou no scratch e a fonte foi à pasta do plano, renomeada de `PLN-007-fonte-do-simbolo` para
`PLN-007-fonte-da-marca`, porque agora leva também os lockups.

- O `brza-brand-text.swift` devolve o JSON de cada texto pelo CoreText; a prova do Desenho, 246,91 de avanço para "BrzA"
  a 100 px em 750, bateu. O `brza-brand-build.mjs` monta os 16 lockups e o ícone com selo.
- O artboard do P2 estourou na primeira passada: a fila dos quatro lockups verticais passava da largura do painel e
  cortava o "WORKSPACE". Foi corrigida e conferida de novo pelo `brza shot`.
- **O passo 4, a rodada dos lockups, fica para Anderson**, é decisão dele. O P4, o P5 e o P6 correm em branches
  empilhadas no `brza-studio`, sem merge: levam os lockups e o selo.
- O P3 foi feito por outra sessão, conduzida por Anderson: `41bfe6d1d4e` e o conserto do `path-literal-ratchet`
  (`a3a89e3aaf5`), na `master`; o worklog dela está em
  [PLN-007: os tokens da marca e o aviso de pergunta azul](2026-11-02-pln-007-os-tokens-da-marca.md).
