---
scope:
  - brza-studio
  - workspace
refs:
  - PLN-007
  - issue:brza-shot-quebra-com-os-tokens-do-painel-movidos
  - issue:o-brza-sessions-abre-na-conta-ativa-do-app
  - issue:o-ico-do-app-sai-com-6-quadros-sem-o-24px
  - issue:os-testes-e2e-de-sqlite-falham-na-master-do-brza-studio
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
- **O selo sem o "ADE":** Anderson pediu o selo do ícone só com "BrzA STUDIO". O `brza-brand-build.mjs` perdeu o texto
  "ADE", e o grupo chama e texto desceu 36 px para ficar centrado no tile; com só o "ADE" removido, sobravam 161 px
  embaixo e 90 em cima. O `brza-app-icon.svg` foi regenerado, o artboard e o rascunho do PNG também, e o `implementer`
  do P4 foi avisado para regenerar o ícone e rodar de novo o `pnpm build:icons`. O rótulo "BrzA Studio ADE" do seletor
  de ícone do app não foi tocado: é texto do `shared/app-icon.ts`, e trocá-lo é decisão de Anderson.
- **A R11: Anderson aprovou os lockups e o selo** ("aprovado, com as mudanças solicitadas"), com o selo "BrzA STUDIO" e o
  `.icns` sem faíscas. O PNG foi à pasta do plano como `PLN-007-lockups-l2.png`, e o P2 fechou, com `Executado` de 0,4 h
  contra as 2,5 h estimadas. As perguntas 2, 3 e 4 (merges, README do workspace, branch do P6) vieram depois: "o restante segue com as
  recomendadas" — merges em ordem, um por vez, com os checks; README depois do merge do P4; branch nova empilhada no P6.
  O artboard só renderizou no chat depois de copiado para a raiz do scratch; a lição foi à memória do workstream.

## A execução do P4 e o README do workspace

O P4 correu num `implementer`, com o pedido em `/private/tmp/pln-007/prompt-p4.md`; a sessão conferiu o diff, rodou o
`check:changed` por conta própria e commitou. Anderson pediu antes o rótulo "BrzA Studio" no seletor de ícones, e o
`implementer` recebeu as duas mudanças que chegaram no meio (o selo sem "ADE" e o `.icns` sem faíscas).

- O gerador adaptado ao S1 deu AE 0 nos 23 SVG contra a fonte aprovada; o `.icns` tem 10 fatias, sem faíscas, e o `.ico`,
  6 quadros, não 7. O 7 do plano vinha do arquivo antigo; o script do upstream só emite 6. Ficou aberto para Anderson.
- O `check:changed` da sessão deu 26 de 27: 3 testes e2e de SQLite falham, e os mesmos quatro arquivos falham na `master`
  `a3a89e3aaf5`, isolados. Foram a uma [issue](../issues/os-testes-e2e-de-sqlite-falham-na-master-do-brza-studio.md).
  O `implementer` tinha visto 24 de 24 porque o conjunto de testes dele era menor; a troca do rótulo, em `shared/app-icon.ts`,
  puxou 5 372 arquivos.
- Merge do P4 na `master` do `brza-studio`, `1bfb496aebf`, fast-forward e push, como a R11 mandou (em ordem, com os checks).
  Depois, o README do workspace: as duas URLs do raw deram `200` e `image/svg+xml`, e o `<picture>` foi à `master` daqui,
  `b30b6bc`.
- **C5, C7 e C8** foram feitos pelo `brza shot`, a pedido de Anderson ("rode os casos manuais utilizando o `brza shot`"):
  o PNG está em `PLN-007-casos-c5-c7-c8.png`, e o veredito diz "visto no artboard", porque o `brza shot` converte um
  artboard e não abre o app. Na primeira passada o dock pequeno usou a arte de 1024 reduzida, com o selo, e o `.icns` não
  leva selo até 64 px; foi corrigido para a fatia real de 64.
- Duas issues: [o `brza sessions` abre na conta ativa do app](../issues/o-brza-sessions-abre-na-conta-ativa-do-app.md),
  e dois itens a mais na dos restos da Orca (a cauda do `icon.json` e os nomes `orca-*`).
- O P5 partiu da `master`, num `implementer`, e o P6 do `brza-studio` espera o merge dele.

## Fora do workspace

- **O worktree `.worktrees/pln-007-brand-assets` e a branch `feat/pln-007-brand-assets` do `brza-studio`**, removidos
  depois do merge; **risco:** nenhum, a branch estava contida na `master`; **estado:** removidos; **como desfazer:**
  `git worktree add` a partir do `1bfb496aebf`.
- **Dois pushes à `master`:** `a3a89e3aaf5..1bfb496aebf` no `brza-studio` e `3c40096..b30b6bc` no `brza-workspace`.

## A execução do P5

O P5 correu num `implementer`, com o pedido em `/private/tmp/pln-007/prompt-p5.md`, partindo da `master` com o P3 e o P4.
Os testes que falham vieram primeiro, e depois o E2, o K2 e os quatro momentos do chat.

- **O conserto que a sessão pediu ao `implementer`:** os tokens do foco do composer, no `:root` e no `.dark` do D4,
  resolvem ali o `var()`; num chat de esquema oposto ao do app, o fundo saía com a cor errada nos dois sentidos.
  Reproduzido num caso novo do fixture, e corrigido movendo os tokens para os blocos de esquema do chat. O Desenho
  mostrava os tokens no `:root`, e esse trecho do D4 não vale.
- O `fixtures:shot` que o plano manda (`native-chat/*`) só tinha 4 fixtures; o `implementer` criou o
  `NativeChatBrandMark.fixture.tsx` para ver o estado vazio, o composer, a atividade, o anel e o cabeçalho, e ele ficou.
- O `check:changed` da sessão, forçado (sem o cache), deu 24 de 24. O merge na `master` do `brza-studio` foi `786f4b56ff9`,
  fast-forward e push.
- **Os casos do chat (C1 a C4 e C6)** foram vistos nos componentes reais pelo `fixtures:shot`, a pedido de Anderson de
  rodar os manuais com ferramenta, e não pelo `brza shot`: ele converte um artboard, e o fixture é o componente de
  verdade. O PNG está em `PLN-007-casos-c1-c4-c6.png`. O C3 e o C6 não dá para ver em imagem parada e ficam pendentes.
- **O build local:** Anderson pediu o "build dev" para conferir, e a sessão gerou o `.app` pelo `pnpm build:mac`
  (`dist/mac-arm64/BrzA Studio.app`), na `master`, depois do merge do P5.
- A memória do `implementer` do P5 tinha ido ao scratch e foi movida para `.claude/agent-memory/implementer/` do workstream.

## Fora do workspace

- **O worktree `.worktrees/pln-007-brand-chat` e a branch `feat/pln-007-brand-chat` do `brza-studio`**, removidos depois do
  merge; **risco:** nenhum, a branch estava contida na `master`; **estado:** removidos; **como desfazer:** `git worktree add`
  a partir do `786f4b56ff9`.
- **O push à `master` do `brza-studio`:** `1bfb496aebf..786f4b56ff9`.
- **O build local em `~/Projects/brza-studio/dist/`:** o `pnpm build:mac` regrava `dist/mac-arm64` e os helpers nativos;
  **risco:** nenhum, `dist/` está no `.gitignore`; **estado:** ativo; **como desfazer:** apagar `dist/`.

## O build local, o P6 e o fechamento do que dá para fechar

- **O primeiro `pnpm build:mac` falhou** com `ENOENT … .worktrees/pln-007-brand-cli/…/cli-display-name.test.ts`: o
  `electron-builder` varre a pasta do projeto, o worktree do `implementer` do P6 mora dentro dela, e um arquivo dele sumiu no
  meio do empacotamento. A sessão tinha dito que o build ia terminar; o aviso de "concluído" da ferramenta enganou, porque o
  comando terminava num `echo`, e o código de saída real, 1, só estava no log. O build refeito num worktree à parte,
  `.worktrees/pln-007-build`, em 3 minutos, deu o `.app` (`1.4.246-local.…786f4b56ff9e`, ad hoc), com o `icon.icns` igual ao
  do repositório.
- **O P6** correu num `implementer`: o `check:changed` forçado deu 19 de 19, e o merge na `master` do `brza-studio` foi
  `5c286937e0c`. 11 asserções de help impresso em 6 arquivos de teste existentes passaram de `orca` a `brza`; fica, pela
  recomendada. Um commit a mais, `cec12c519c4`, corrigiu a frase de `brza-brand-logos.md`, que o próprio D2 tinha pedido e
  que ficou desencontrada.
- **O plano não fecha**: os casos manuais no app e o `grep -c` do P6 no binário instalado são de Anderson, e o `.ico` com
  6 quadros virou [issue](../issues/o-ico-do-app-sai-com-6-quadros-sem-o-24px.md). Os seis passos têm `[x]` ou `[-]` com
  evidência, e o `Executado` soma 3,6 h contra as 20,75 h estimadas.
- **A memória do `implementer` caiu no scratch** nos P5 e P6, porque o cwd dele é o do chat; foi movida para o workstream, e a
  lição foi à memória da sessão.

## Fora do workspace

- **O worktree `.worktrees/pln-007-brand-cli` e a branch `feat/pln-007-brand-cli` do `brza-studio`**, removidos depois do merge;
  **risco:** nenhum; **estado:** removidos; **como desfazer:** `git worktree add` a partir do `5c286937e0c`.
- **O worktree `.worktrees/pln-007-build` do `brza-studio`**, com o `.app` em `dist/mac-arm64/` (685 MB), para a conferência de
  Anderson; **risco:** nenhum, `dist/` está no `.gitignore`; **estado:** ativo; **como desfazer:** `git worktree remove
  --force .worktrees/pln-007-build` no `brza-studio`, depois da conferência.
- **Dois pushes à `master` do `brza-studio`:** `786f4b56ff9..5c286937e0c` e `5c286937e0c..cec12c519c4`.
- **(Ver a seção seguinte: o build local em `.worktrees/pln-007-build` foi removido, e o DMG final está em `dist/`.)**

## A versão `1.4.246-alpha.1`: a tag e o DMG final

Anderson pediu "a tag `v<upstream-version>-alpha.1` e o DMG final da versão", com o worktree removido, para conferir na versão
final. A versão do upstream no `package.json` é `1.4.246`.

- **O commit e a tag.** Seguindo o precedente da `v1.4.242.alpha.1` (um commit `release:` que só muda o `package.json` para
  a forma SemVer, e uma tag anotada), `6d47623` troca `1.4.246` por `1.4.246-alpha.1`, e a tag anotada
  `v1.4.246-alpha.1`, com o hífen que Anderson pediu (a anterior usava ponto), aponta para ele. **Não foram ao origin:** tag é
  publicação, e Anderson ainda vai conferir. Os workflows do repositório só têm `workflow_dispatch` e tags `mobile-*`, então o
  push não dispara build. O push é `git -C ~/Projects/brza-studio push origin master v1.4.246-alpha.1`.
- **Um erro no caminho:** a primeira tentativa quebrou num `git rev-parse --short` com dois argumentos, as linhas seguintes
  rodaram soltas, e a tag foi criada em `cec12c519c4`, sem a mudança de versão. Foi apagada na hora, só existiu localmente, e
  refeita com `set -e`, conferindo que a tag e o `HEAD` apontam para o mesmo commit.
- **O DMG.** A `build:mac:release` exige as credenciais de assinatura e notarização da Apple; o alpha anterior foi um build local
  ad hoc, com o sufixo `-local`. O DMG final usou a mesma cadeia do `build:mac --dmg`, **sem** o `ORCA_LOCAL_BUILD_VERSION`,
  num worktree na tag: `latest-mac.yml` com `version: 1.4.246-alpha.1`, ad hoc, sem notarização, 250 MB. Montado somente
  leitura: versão `1.4.246-alpha.1`, `icon.icns` igual ao do repositório, `codesign --verify --deep --strict` passa, e o `brza`
  empacotado dá 0 linhas de `orca` como comando. O `spctl` rejeita, como esperado para um build sem notarização; um DMG
  baixado, e não copiado, pede "Abrir" com o botão direito ou `xattr -dr com.apple.quarantine`.

## Fora do workspace

- **O commit `6d47623` e a tag `v1.4.246-alpha.1` no `brza-studio`**, só locais; **risco:** a `master` local fica 1 commit à
  frente do origin; **estado:** ativos; **como desfazer:** `git tag -d v1.4.246-alpha.1` e `git reset --hard HEAD~1`, antes do
  push.
- **O DMG `~/Projects/brza-studio/dist/brza-studio-1.4.246-alpha.1-macos-arm64.dmg`**; **risco:** nenhum, `dist/` está no
  `.gitignore`; **estado:** ativo; **como desfazer:** apagar o arquivo.
- **O worktree `.worktrees/pln-007-build` do `brza-studio`**, removido com o `.app` de 685 MB; **estado:** removido. O build que
  falhou antes também tinha apagado o `.app` local anterior de `dist/mac-arm64`, e deixado um `Electron.app` cru, que foi
  removido: **risco:** nenhum, são artefatos regeneráveis, e o DMG do alpha anterior ficou em `dist/`.
- **O `pnpm install` que o gancho do repositório rodou** no checkout principal ao mudar o `package.json`: compilou os módulos
  nativos do Windows; **risco:** nenhum.
