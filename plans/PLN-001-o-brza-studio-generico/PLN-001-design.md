# PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat — Desenho

O desenho do [PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](PLN-001-plan.md). O
que este desenho assume e o Terreno medido em 2026-10-24 estão no desenho do PLN-025 do workspace da Fixfy
(`plans/PLN-025-orca-desktop-cli-app-e-web/PLN-025-design.md`); os itens D1 a D35 vieram de lá, pelo PLN-029 da Fixfy,
com os IDs de antes (PLN-025/R28.2), e os D36 a D50 são daqui, de 2026-10-27 a 2026-10-29. Nos itens D1 a D35, o nome do
repositório nos caminhos é o de hoje, `brza-studio/…`, e não o de antes do rebrand.

### O que este desenho assume

- **D1 a D35:** o que assumem está no desenho do PLN-025 da Fixfy
  (`~/Projects/fixfy/plans/PLN-025-orca-desktop-cli-app-e-web/PLN-025-design.md`), como a introdução diz.
- **R29.1:** o texto da pergunta no "Perguntou:" ganha a cor de destaque do tema (`primary`, a do ✓).
- **R29.2:** git, gh (PR e issue), testes e pacotes e build ganham ícone e título próprios.
- **R29.3:** Jira e Confluence, Skill, Figma e Firebase e Context7 ganham ícone e título próprios.
- **R29.4:** os ícones são lucide, com logos SVG de marca só no desktop; o mobile cai no lucide.
- **R30.1:** em "largura total", todo bloco e toda tabela têm sempre 120 colunas mais o padding, com rolagem no
  estreito.
- **R30.2:** a coluna da tabela se mede na fonte de código do chat.
- **R31.1:** o link do chat é `#79C0FF` no escuro e `#0969DA` no claro, com o sublinhado a 40%.
- **R35.1:** logos de marca: o Git novo, e o GitHub e o Jira reusados; o Figma e o Firebase ficam no lucide.
- **R36.1:** o pedido 30 é a imagem de ferramenta; o `![]()`, o anexo e o ampliar que existem viram conferência.
- **R36.2:** a imagem da ferramenta se extrai para arquivo no main, com a referência no resultado.
- **R36.3:** a miniatura aparece com a linha fechada, ~96 px de altura, abaixo do título, e o clique amplia.
- **R36.4:** a imagem de ferramenta é só do desktop agora; o mobile segue sem ela.
- **R37.1:** no comando composto vale a ordem fixa por peso, testes > gh > git > pacotes e build > `brzaCli`.
- **R37.2:** o gerenciador que roda `test`, `vitest`, `jest` ou o `run-vitest.mjs` é testes, e o resto é pacotes e
  build.
- **R38.1:** o hash do `git commit`, lido da saída, abre o diff do commit, por uma `openCommitByHash` do BrzA.
- **R38.2:** o passou/falhou sai do rodapé se ele chegou; na saída cortada, só o estado.
- **R38.3:** o site do chip do Jira sai do `cloudId` se for domínio, senão do Jira do app; sem nenhum, o chip só copia.
- **R38.4:** a miniatura do `get_screenshot` do Figma fica para o pedido 30.
- **R39.1:** o arquivo da imagem extraída fica no temp do sistema, como o colar.
- **R39.2:** o caminho ou a URL de imagem solto no texto vira miniatura abaixo do parágrafo.
- **R39.3:** a URL http(s) de imagem carrega sozinha, como o `![]()` de hoje.
- **R39.4:** a linha mostra até 4 miniaturas, com um "+N" que abre as demais.
- **R40.1:** o `git` leva o logo do Git, e o `git commit`, o `git-commit-horizontal`.
- **R40.2:** títulos e chips no conjunto A, com chip.
- **R40.3:** o resultado no título vai em português.
- **R40.4:** commit e push na `master` com os testes verdes, os worktrees em `brza-studio/.worktrees/`, e o P50 de
  Sonnet.
- **R41.1:** no composto com navegador vale o globo do upstream; as categorias do BrzA só entram fora dele.
- **R41.2:** a corrida com vários `git` e um `git commit` mostra o logo do Git.
- **R41.3:** no mobile entram só o ícone lucide e o título; os chips ficam no desktop.
- **R42.1:** o "+N" abre a linha, com todas as imagens em faixa com quebra.
- **R42.2:** a miniatura do texto solto aparece ao terminar a mensagem, como o Mermaid.
- **R43.1:** Package nos pacotes (`install`, `add`, `pub get`) e Hammer no build (`build`, `run build`,
  `flutter build`).
- **R43.2:** o Confluence ganha o lucide `file-text`, novo nas tabelas de glifos do desktop e do mobile.
- **R44.1:** o chip do Confluence lê título e URL de forma defensiva; a URL pelo id e a saída do `getConfluencePage` são
  suposição até a conferência.
- **R48.1:** o chat ganha um seletor de tema, com o catálogo de temas do terminal.
- **R48.2:** o Markdown e o terminal têm um interruptor "Seguir o chat" cada um.
- **R48.3:** a fonte e o tamanho do chat valem no olho e no lápis; o terminal e o modo código levam só as cores e o
  fundo.
- **R48.4:** o "igualar ao terminal" sai, migrado sem mudar a tela.
- **R49.1:** o Markdown com o "Seguir o chat" desligado tem um seletor de tema próprio.
- **R49.2:** o tema do chat é um par escuro e claro, pelo claro/escuro do app, como o do terminal.
- **R49.3:** o padrão do chat é o "Padrão do BrzA", o visual de hoje.
- **R49.4:** o modo código segue o fundo e o claro/escuro do chat, com a sintaxe Islands Dark e light-plus.
- **R50.1:** a mensagem do Claude Code entre sessões ganha um leitor do BrzA e o cartão do Orca de 2026-10-29.
- **R50.2:** entram o correio entre sessões e a devolução de subagente.
- **R50.3:** o clique no remetente abre a aba da sessão dele, se aberta.
- **R51.1:** a devolução tem o rótulo "Devolução de <nome>".

### D1 — O build local, assinado — `brza-studio/config/scripts/build-mac-local.mjs` (P1, PLN-028/P5)

- **Origem:** R6.1, R7.2, R8
- **Contexto:** o build da medição tinha três contornos e deixava o `.app` sem assinatura válida, e o pedido do Keychain
  parou a medição (R6, R8 da Fixfy); pela R7.2, o que serve a projeto fora da Fixfy mora aqui (pedido 1).

#### Como fica

`pnpm run build:mac` sai do clone limpo ao `.app` sem passo à mão: instala as dependências de `mobile/`, chama o `swift`
com `--build-system native` e empacota só arm64. A identidade de assinatura vem de variável (`CSC_NAME`); sem ela, o
build sai ad hoc com `codesign --force --deep -s -`, para servir a projetos fora da Fixfy. Com a `CSC_NAME` posta, o
build sai assinado com a identidade dela, com o hardened runtime.

### D2 — O atualizador desligado — `brza-studio/src/main/updater/` (P2)

- **Origem:** R10.2
- **Contexto:** o atualizador aponta para as releases do upstream, sem opção que o desligue (R6 da Fixfy); o build local
  adotado de vez fica sem check antes do primeiro que traria o upstream de volta (R10.2).

#### Como fica

Um predicado único, `isUpdaterEnabled()`, falso no build local, no lugar das 6 guardas `!app.isPackaged`
(`updater-setup.ts:139`, `updater-scheduling.ts:67`, `updater-menu-checks.ts:17`, `updater-build-selection.ts:92`,
`updater-remote-status.ts:20`, `updater-nudge.ts:9`). A versão nova chega por sincronização e build (PLN-025/D4).

### D6 — O tema Islands Dark no Monaco e no Shiki — `brza-studio/src/renderer/src/lib/` (P6)

- **Origem:** Pedido 5, R7.2
- **Contexto:** pedido 5: "arquivos de código - e blocos de código - seguem o tema Islands Dark do Android Studio"; hoje
  o Monaco usa `vs-dark` e o Shiki, `dark-plus`.

#### Como fica

`monaco-setup.ts` registra o tema com `defineTheme`, com as cores de `~/.config/orca-themes/patch_orca_monaco.py:49-90`,
e os 6 `vs-dark` passam a usá-lo; o `syntax-highlighter.ts` troca o `dark-plus` pelo mesmo tema.

### D20 — O olho no visualizador de Markdown — `brza-studio/src/renderer/src/components/editor/` (P25)

- **Origem:** pedido 14, R19
- **Contexto:** pedido 14: a barra do visualizador de Markdown tem o `<>` do código e o lápis da visualização
  renderizada com edição; falta o olho, renderizado e sem edição, como o padrão.

#### Como fica

Na aba do arquivo Markdown, a barra mostra o olho, o lápis e o código, nessa ordem
(`MARKDOWN_EDIT_VIEW_MODES = ['preview', 'rich', 'source']`), e o `getDefaultMarkdownViewMode` devolve `preview`. O olho
é o modo `preview` que o Orca já tem: renderizado e só leitura, em linha pelo `EditorMarkdownFileSurface.tsx`. O modo
escolhido por arquivo continua guardado e vence o padrão. A aba de diff segue com o código e o lápis, e o padrão
`source`; a aba de prévia dedicada (`editor.markdownPreview`) não muda.

### D21 — O build local de Windows — `brza-studio/config/scripts/build-win-local.mjs` (P26, P27)

- **Origem:** pedido 15, R20
- **Contexto:** pedido 15: "o orca-dev está com todas as alterações prontas para buildar no windows?"; o
  `build-win-local.mjs` não existia (P26), e o build local de um comando era o do Mac (D1).

#### Como fica

`pnpm run build:win` sai do clone limpo a um instalador NSIS x64 sem passo à mão: instala o `mobile/`, roda o
`build:desktop` e o `ensure:electron-runtime` e chama o `electron-builder --win --x64` com a `ORCA_LOCAL_BUILD_VERSION`
carimbada pelo mesmo `createLocalBuildVersion` do D1, o que desliga o atualizador (D2). O instalador sai sem assinatura,
com o aviso do SmartScreen; os canais oficiais do upstream (`ORCA_WIN_*`) não mudam. No Windows se instala só o
`brza-studio`, sem o código da Fixfy.

### D27 — A barra da mensagem do agente e o Bifurcar — `brza-studio/src/main/claude/` e `…/native-chat/` (P33, P34)

- **Origem:** pedido 19, R25.3, R26.2
- **Contexto:** pedido 19: o Bifurcar "funciona como o bifurcar do claude.ai (inicia uma nova sessão a partir desse
  ponto, com tudo oq tiver acima)"; a barra de hoje só recebe o Markdown, a hora e o rolar ao topo.

#### Como fica

A barra do `NativeChatAgentControls` (`NativeChatTranscriptChrome.tsx:263-294`), que hoje só recebe o Markdown, a hora e
o rolar ao topo, passa a receber o id da mensagem pelo `NativeChatAssistantMessageRow.tsx:93`, e ganha os botões dos D27
a D29. O Bifurcar corta o transcript no uuid da mensagem pelo `forkSession(sessionId, {upToMessageId})` do SDK
(`sdk.d.ts:831`), com o mapeamento do id da linha ao uuid que o rewind já faz (`claude-rewind-fork.ts`), e abre a sessão
nova com `resume` no fork, numa aba nova do mesmo worktree, como o bifurcar do claude.ai. A conversa de origem não muda.

### D28 — O Novo Chat a partir da mensagem — `brza-studio/…/native-chat/` (P34)

- **Origem:** pedido 20, R25.3
- **Contexto:** pedido 20: o Novo Chat "abre uma nova sessão assim como o Bifurcar, mas levando apenas a mensagem
  clicada".

#### Como fica

O botão abre uma aba nova de chat no mesmo worktree pelo `launchAgentInNewTab`, com a mensagem clicada como rascunho na
caixa (`promptDelivery: 'draft'`, `agent-launch-prompt-delivery.ts:12-25`), sem enviar. A mensagem longa se confere no
`canMirrorLaunchDraftToNativeChat`.

### D29 — O Fixar Capítulo na régua de prompts — `brza-studio/…/native-chat/` (P35)

- **Origem:** pedido 21, R26.1
- **Contexto:** pedido 21: o Fixar Capítulo "vem marcado por padrão e fixa/desafixa o capitulo (capitulo = prompt do
  usuário + resposta do agente)", e os marcados ficam na sessão flutuante, "como já é hoje".

#### Como fica

O capítulo é o prompt do usuário e a resposta do agente. O botão na barra da resposta vem marcado e fixa ou desafixa o
capítulo; a régua de prompts (`native-chat-message-rail-items.ts`, `structured-agent-session-rail-outline.ts`) destaca
os fixados, e a prévia dela mostra o capítulo. O estado é por sessão, no renderer.

### D30 — O seletor de conta — `brza-studio/src/main/claude/`, `src/main/claude-accounts/` e `…/native-chat/` (P36)

- **Origem:** pedido 22, R25.3, R26.3
- **Contexto:** pedido 22: ao lado do seletor de modelo e esforço, um seletor de conta que lista as contas "da mesma
  forma que hoje lista `claude|adm` no terminal", e a troca continua no mesmo chat com o contexto injetado.

#### Como fica

Ao lado do seletor de modelo e esforço (`NativeChatComposerActions.tsx:140-150`), um seletor lista as contas Claude do
Orca (`src/main/claude-accounts/`), como o `claude|adm` do terminal. A troca segue o molde do `/clear`: a mesma aba e a
mesma sessão do Orca, com uma sessão nova do Claude por baixo e um divisor "Conta trocada - <conta>", irmão do "Contexto
limpo" (`NativeChatNoticeRow.tsx:75-94`). O contexto vai fiel: o main copia o `.jsonl` da sessão para o `projects/` da
conta nova e retoma por `resume`. A conta deixa de ser identidade fixa da sessão nesse caminho: a recusa
`identityMismatch` (`agent-session-reservation-admission.ts:197-202`) e o `historyInOtherAccount`
(`claude-structured-launch-home.ts:44-69`) abrem exceção para a troca. Se o `~/.claude-adm` não entrar como conta do
Orca, o registro dele vem antes.

- **Para depois:** a opção "Selecionar automaticamente" no seletor de modelo e esforço, por rodada própria.

### D31 — As sugestões de ortografia no botão direito — `brza-studio/src/main/window/` (P37)

- **Origem:** pedido 23, R25.3
- **Contexto:** pedido 23: o menu do botão direito deve listar "sugestões para palavras digitadas errado"; o menu já
  lista até 5 sugestões (`editable-context-menu.ts:200-235`).

#### Como fica

O menu do botão direito já lista até 5 sugestões e troca a palavra (`editable-context-menu.ts:200-235`), com o corretor
do macOS. O passo confere na caixa de texto do chat, em pt-BR; se as sugestões não aparecerem, corrige o que as esconde
— o idioma ou o menu próprio do chat (`use-native-chat-context-menu.tsx`).

### D32 — O Markdown na caixa de texto — `brza-studio/…/native-chat/NativeChatPromptEditor.tsx` e as configurações (P38)

- **Origem:** pedido 24, R25.3
- **Contexto:** pedido 24: um switch nas configs de chat, desabilitado por padrão, que faz a caixa de mensagem
  renderizar "como o modo de edição do visualizador de markdown, já formatado".

#### Como fica

Um switch "Modo de visualização Markdown" nas configurações de chat (`ChatBehaviorSetting.tsx`), com a chave em
`global-settings-types.ts` e o padrão desligado em `default-global-settings.ts`. Ligado, a caixa de texto, que já é
Tiptap (`NativeChatPromptEditor.tsx:21`), ganha as extensões de formatação do modo de edição do visualizador de
Markdown e mostra o texto já formatado; o que se envia segue em Markdown, com as pílulas de arquivo, imagem e skill.

### D33 — O Editar na mensagem do usuário — `brza-studio/…/native-chat/NativeChatUserMessageRow.tsx` (P39)

- **Origem:** pedido 25, R25.1, R25.2
- **Contexto:** pedido 25: as mensagens do usuário ganham uma barra inferior, como a do agente, com o Copiar, o Enviar
  agora (na fila) e o Editar, que "copia a mensagem direto na caixa de digitação".

#### Como fica

A barra da mensagem enviada (`NativeChatUserMessageRow.tsx:24-60`), que já tem o copiar, a hora e o rewind, ganha o
Editar: a mensagem vai à caixa de texto, sozinha se a caixa estiver vazia, abaixo do rascunho se houver um, e o foco vai
à caixa. O Enviar agora fica no cartão da fila (`NativeChatQueuedMessageCard.tsx:133-146`), como já é.

### D34 — O Continuar em outra conta, no aviso de limite — `brza-studio/…/native-chat/` (P40)

- **Origem:** pedido 26, R27.1, R27.2
- **Contexto:** pedido 26: ao lado do Continuar, no aviso "Claude atingiu seu limite de sessão", o "Continuar em
  <seletor de conta>" "faz a mesma coisa que o seletor de conta do chat".

#### Como fica

Na linha do aviso de limite (`NativeChatNoticeRow.tsx:149-171`), ao lado do Continuar, o botão "Continuar em" abre um
menu com as outras contas do seletor do D30. A escolha faz a troca do D30 — o transcript copiado, o `resume` e o divisor
"Conta trocada - <conta>" — e, só depois que a sessão nova sobe, envia o mesmo Continuar do `continueUsageLimit`
(`NativeChatInterruptedContinue.tsx`), "Continue where you left off.". Se a troca falha, nada é enviado, e o erro vai ao
aviso da caixa de texto, como o do Continuar.

### D35 — O Retomar automaticamente, no aviso de limite — `brza-studio/src/main/` e `…/native-chat/` (P41)

- **Origem:** pedido 26, R27.3, R27.4
- **Contexto:** pedido 26: o "Retomar automaticamente" "adiciona uma tarefa agendada que dispara ao resetar o limite da
  conta, continuando a tarefa".

#### As alternativas

- **Descartada:** a Automação do Orca (`main/automations/`), que é cron recorrente e abre um agente novo, sem continuar
  o chat; e o timer no renderer, que morre ao fechar a janela (R27.3).

#### Como fica

Ao lado do Continuar, o botão "Retomar automaticamente" aparece quando a falha traz o `resetsAt`
(`shared/agent-session-usage-limit.ts`). O clique grava no main, persistida, uma retomada para o `resetsAt` + 1 min, com
a sessão e o turno do corte; na hora, o main envia o mesmo Continuar no mesmo chat e na conta que ele estiver. A linha
passa a mostrar "Retomada às HH:MM · Cancelar", e qualquer mensagem enviada antes cancela a retomada. Com o Orca fechado
na hora, a retomada vencida dispara ao abrir, junto da retomada do restart (`native-chat-resume-on-restart-store.ts`),
só se o chat ainda está no corte do limite, sem mensagem depois.

### D36 — O "Perguntou:" em cor de destaque — `brza-studio/src/renderer/src/components/native-chat/NativeChatAwaitingInputRow.tsx` (P42)

- **Origem:** pedido 27, R29.1
- **Contexto:** pedido 27: "no bloco de Perguntou: no chat, as perguntas do agente ficam da mesma cor do texto normal
  (branco)"; o texto usa `text-chat-foreground` em `NativeChatAwaitingInputRow.tsx:76`, `:113` e `:118`.

#### Como fica

O texto da pergunta do agente passa de `text-chat-foreground` à cor `primary` do tema, a mesma do ✓ de opção escolhida,
nos três pontos: a linha fechada (`:76`), a pergunta aberta (`:113`) e a lista de perguntas (`:118`).

### D37 — A base dos ícones de marca — `brza-studio/src/shared/native-chat/tools/` e `…/native-chat/NativeChatToolIcon.tsx` (P43)

- **Origem:** pedido 27, R29.4, R35.1
- **Contexto:** pedido 27: "mais icones/titulos personalizados […] git com o icone do git, jira e etc"; a categoria do
  ícone sai de `native-chat-tool-icon.ts:58`, arquivo do upstream, e os ícones são lucide, compartilhados com o mobile.

#### Como fica

As categorias novas moram num módulo do BrzA, por exemplo `src/shared/native-chat/tools/brza/`, com uma linha de
montagem no `CATEGORY_BY_ROW_WORD` (`native-chat-tool-icon.ts:58`), arquivo do upstream, para os merges de
`stablyai/orca` seguirem com conflito pequeno. Os ícones genéricos são lucide; o SVG de marca vem de um componente do
BrzA só no desktop, pelo `NATIVE_CHAT_TOOL_GLYPHS`, e o mobile (`lucide-react-native`, que compartilha os ids de ícone)
cai no lucide equivalente. Os logos de marca são o do git, novo (traço do Simple Icons, CC0, com a atribuição CC BY 3.0
de Jason Long ao lado), e o `GitHubIcon` e o `JiraIcon` que o upstream já tem. O Figma e o Firebase ficam no lucide
(`pen-tool` e `flame`) também no desktop, porque as diretrizes de marca deles proíbem mudar a cor, e o glifo do chat é
monocromático; a API deixa ligar o logo depois com uma linha, se houver permissão.

### D38 — Os comandos de shell com ícone e título por categoria — `brza-studio/src/shared/native-chat/tools/brza/` (P44 a P47)

- **Origem:** pedido 27, R29.2, R37.1, R37.2, R38.1, R38.2, R40.1 a R40.3, R41.1 a R41.3, R43.1
- **Contexto:** pedido 27: ícone e título próprios nos comandos; hoje vale a primeira categoria da lista que casar com o
  comando inteiro (`brza-tool-categories.ts:48` e `:112`), e o título só lê o input (R37, R38).

#### Como fica

O comando de shell vira a categoria pelo input, segmento a segmento (o `splitUnquotedSegments` de
`orca-browser-cli-commands.ts`), e no composto vale a de mais peso: testes > gh > git > pacotes e build > `brzaCli`
(R37.1). O comando de navegador mantém o globo do upstream, e nenhuma categoria do BrzA entra nele (R41.1). O título lê
a saída: o `brzaToolLineTitle` passa a receber o `result` que o `nativeChatToolLineLabel` já tem
(`native-chat-tool-line-label.ts:69-72` e `:144`). O resultado no título vai em português (R40.3).

- **`git`:** o logo do Git (`git-logo`) em todo subcomando, e o `git commit` com o `git-commit-horizontal` (R40.1); a
  corrida de git leva o logo, mesmo com um commit dentro (R41.2). O commit tem o título "git commit — <1ª linha da
  mensagem>" e o chip com o hash curto, lido da saída (`[branch abc1234]`), que abre o diff do commit no visualizador
  por uma `openCommitByHash` do BrzA, sobre o `getRuntimeGitCommitCompare` e o `openCommitAllDiffs`, no worktree do chat
  (R38.1). Os outros subcomandos ficam com o texto do comando, como hoje.
- **`gh` de PR e issue:** GitPullRequest, "PR #123 — <título>" e "Issue #45 — <título>", com o número pela URL na saída
  e o título pelo `--title` ou pela saída, e o chip "#123" que abre no navegador pelo `openNativeChatWebLink`.
- **Testes:** `vitest`, `run-vitest.mjs`, `flutter test`, `pytest` e o gerenciador que roda `test`, `vitest`, `jest` ou
  o `run-vitest.mjs` (R37.2): FlaskConical, com "<executor> — 12 passaram, 1 falhou" pelo rodapé, quando ele está na
  parte da saída que chegou, e só "passou" ou "falhou" pelo `isError` ou `exitCode` na saída cortada (R38.2).
- **Pacotes e build:** `pnpm`, `npm` e `flutter pub` com `install`, `add` ou `get`, e o build: Package nos pacotes e
  Hammer no build (`build`, `run build`, `flutter build`) (R43.1), com o texto do comando como hoje, sem interação.
- **Mobile:** o ícone lucide e o título; os chips ficam só no desktop (R41.3).

### D39 — As ferramentas de MCP e do agente com ícone e título — `brza-studio/src/shared/native-chat/tools/brza/` (P48 a P51)

- **Origem:** pedido 27, R29.3, R35.1, R38.3, R38.4, R40.2 a R40.4, R41.3, R43.2
- **Contexto:** pedido 27: ícone e título próprios, "jira e etc"; o MCP da Atlassian traz `cloudId` e `issueIdOrKey`,
  sem a URL, e o nome do nó do Figma não vem no input, só o `nodeId` (R38).

#### Como fica

A chamada MCP chega identificada pelo `NativeChatMcpIdentity`, e o título lê a saída como no D38.

- **Jira e Confluence** (servidor `/atlassian/i`): o Jira com o `jira-logo` (R35.1), "FIX-123 — <resumo, se vier na
  saída>" e o chip com a chave; o Confluence com o `file-text` do lucide (R43.2), "<título da página>" e o chip da
  página. O chip abre no navegador: o site sai do `cloudId` quando ele é domínio (`x.atlassian.net`), senão do `siteUrl`
  da conexão nativa do Jira no app (`JiraSite.siteUrl`), e sem nenhum o chip só copia a chave (R38.3). Só no desktop
  (R41.3).
- **Skill:** Sparkles e "Skill · <nome>" (P49).
- **Figma:** o `pen-tool` e "Figma · <nome do nó, ou o `nodeId`>", com o nome quando a saída o traz. A miniatura do
  `get_screenshot` sai pelo pedido 30, em PLN-001/D43 (R38.4).
- **Firebase e Context7:** Flame e BookOpen, com o nome do projeto ou da biblioteca no título, sem interação (P51).

### D40 — Os blocos de código e as tabelas com 120 colunas na largura total — `brza-studio/…/native-chat/` (P52)

- **Origem:** pedido 28, R30.1, R30.2
- **Contexto:** pedido 28: "blocos de código - ``` - e as tabelas, largura sempre de 120 colunas + padding, quando
  selecionado `largura total`"; "Total" é `width === 'full'`, e o `<pre>` usa `max-w-full`
  (`NativeChatCodeBlock.tsx:62`).

#### Como fica

Só com `width === 'full'` (`native-chat-appearance-style.ts:77` e `:88`), uma variável, por exemplo
`--chat-wide-block-width`, posta só nesse ramo e lida pelo bloco (`NativeChatCodeBlock.tsx:46` e `:62`) e pela tabela
(`native-chat-markdown.css:25` e `:64`), num módulo ou CSS do BrzA com uma linha de montagem nos arquivos do upstream.
Todo bloco e toda tabela têm exatamente `120ch` mais o padding do bloco, mesmo curtos; num painel mais estreito encolhem
até 100% da coluna e rolam na horizontal; o texto corrido segue na largura total. O `ch` é medido na fonte mono do chat
(`--chat-code-font-size`), também na tabela, para as bordas se alinharem. "Normal" e "Larga" não mudam.
Quando sobra espaço, o bloco fica à esquerda, com o texto; o diff de edição (`NativeChatDiffView` e as linhas do
`NativeChatDiffCard`) e os diagramas e visuais (o Mermaid e o `NativeChatInlineVisual`) seguem a regra, e a saída de
ferramenta não (P52, resposta de 2026-10-27).

### D41 — Os links do chat em azul claro — `brza-studio/src/renderer/src/components/native-chat/native-chat-markdown.css` (P53)

- **Origem:** pedido 29, R31.1
- **Contexto:** pedido 29: "links no chat, na cor azul padrão de link, mais clarinho"; o link usa hoje
  `--chat-foreground-strong` (`native-chat-markdown.css:18`).

#### Como fica

`.native-chat-markdown a` (`:18`) passa de `color: var(--chat-foreground-strong)` a uma variável `--chat-link`,
`#79C0FF` no tema escuro e `#0969DA` no claro. O sublinhado segue com 40% da cor
(`color-mix(in srgb, currentColor 40%, transparent)`), e a mensagem com tom `faint` segue herdando a cor (`:55`).

### D42 — A imagem da ferramenta extraída para arquivo — `brza-studio/src/main/native-chat/brza/` e `src/shared/native-chat-types.ts` (P54)

- **Origem:** pedido 30, R36.1, R36.2, R36.4, R39.1
- **Contexto:** o `tool_result` do Claude traz a imagem do `Read`, do `get_screenshot` do Figma e do print do browser
  como bloco `image` em base64. Os dois decoders ficam só com o texto: o do turno ao vivo
  (`claude-structured-item-translation.ts:127-143`, `resultText`) e o do histórico lido do transcript
  (`transcript-record-blocks.ts:8-34`, `toolResultOutput`). O base64 não vai ao journal, que corta o que passa do limite
  (`journal-payload-bounds.ts:44-51`).

#### Como fica

- **A extração.** Uma função do BrzA, por exemplo `brzaToolResultImages(content)` em
  `src/main/native-chat/brza/brza-tool-result-images.ts`, lê do `content` do `tool_result` os blocos
  `{ type: 'image', source: { type: 'base64', media_type, data } }`.
  - Grava cada um no temp do sistema, como o colar (`clipboard-image-temp-file.ts:44`, `getPath('temp')`), e devolve
    `NativeChatImageRefBlock[]` com o `path`.
  - O bloco com `source.type: 'url'` vira `image-ref` com a `url`, sem arquivo.
  - Só entram os tipos que o envio já aceita (`claude-structured-dispatch-content.ts:105-111`: gif, jpeg, png e webp).
- **O nome do arquivo sai do digest do conteúdo**, por exemplo `brza-tool-images/<sha256 de 16>.<ext>`. Assim a mesma
  imagem decodificada duas vezes, ao vivo e no histórico, não duplica o arquivo. E o arquivo que o macOS limpou do temp
  volta quando a chamada é decodificada de novo do transcript. Sem essa nova decodificação, a miniatura cai no "Preview
  unavailable", como o anexo (R39.1).
- **O campo.** O `NativeChatToolResultBlock` (`native-chat-types.ts:94-104`) e o corpo `tool-call` do journal
  (`agent-session-journal-types.ts:132`) ganham `images?: NativeChatImageRefBlock[]`. Os dois decoders o preenchem, com
  uma linha de montagem cada, e a projeção do journal ao renderer leva o campo. Nos arquivos do upstream entram só a
  montagem e o campo opcional.
- **O mobile não muda** (R36.4): o campo é opcional, e o mobile segue sem ele.
- **A conferir no passo, sem rodada:** se a tradução ao vivo é síncrona, a gravação vai pelo mesmo caminho do colar. Se
  o relay ao mobile rejeitar campo desconhecido, o campo fica fora do relay.

### D43 — A miniatura na linha da ferramenta — `brza-studio/src/renderer/src/components/native-chat/brza/` e `NativeChatToolLine.tsx` (P55)

- **Origem:** pedido 30, R36.3, R39.4, PLN-001/R38.4 (o P50.2), R42.1
- **Contexto:** a imagem extraída (D42) precisa aparecer na linha da ferramenta; o ampliar já existe
  (`MarkdownImageLightbox.tsx`, `PanZoomImageDialog.tsx`), mas o `PanZoomImageDialog` mostra uma imagem só (`:64`), sem
  navegação (R39.4).

#### Como fica

- **O lugar.** Um componente do BrzA, por exemplo `BrzaToolImageStrip`, montado por uma linha em
  `NativeChatToolLine.tsx`, logo abaixo do título e fora da parte que abre e fecha (o corpo aberto está em `:75`). As
  miniaturas aparecem com a linha fechada.
- **O tamanho.** Altura de ~96 px, largura pela proporção, lado a lado. Até 4 miniaturas; da quinta em diante, um "+N"
  no lugar da quinta (R39.4), cujo clique abre o corpo da linha, com todas as imagens em faixa com quebra (R42.1).
- **A leitura e o clique.** Cada miniatura reusa o `ExpandableMarkdownImage` (`MarkdownImageLightbox.tsx:28`), que
  amplia no `PanZoomImageDialog` com pan e zoom. A leitura do arquivo é a do `NativeChatMarkdownImage`: o
  `useLocalImageSrc` com o acesso `chat-image` (`:42` e `:134-141`) e a carga perto da tela
  (`observeTranscriptVisibility`, `:142`). O arquivo que sumiu do temp mostra o "Preview unavailable" (`:215-219`).
- **O que cobre:** o `Read` de imagem, o print do browser e o `get_screenshot` do Figma, que é o P50.2 (PLN-001/R38.4).

### D44 — A miniatura do caminho ou da URL de imagem solto no texto — `brza-studio/src/renderer/src/components/native-chat/brza/` e `NativeChatMarkdown.tsx` (P56)

- **Origem:** pedido 30, R39.2, R39.3, R42.2
- **Contexto:** o texto já faz link de caminho de arquivo que existe, na prosa e no código inline
  (`comment-markdown-native-chat-file-links.ts:255`, `inlineCodeFileLink`), pelo `linkifyFilePaths`
  (`NativeChatMarkdown.tsx:105` e `:125`). O `[x](a.png)` e a URL http(s) já são links do Markdown.

#### Como fica

- **O que vira miniatura.** Um plugin remark do BrzA, ligado pelos `remarkPlugins` da extensão de imagem
  (`NativeChatMarkdown.tsx:68`), acha no parágrafo o link cujo alvo termina em extensão de imagem
  (`src/shared/image-file-extensions.ts`). O link fica, e depois do parágrafo entra um nó que um componente do BrzA
  desenha com o `NativeChatMarkdownImage`.
- **A mesma imagem aparece uma vez por mensagem**, na primeira menção, e o `![]()` da mesma imagem conta como menção.
- **Só aparece se abre.** O caminho que não abre e a URL que falha não mostram nada, ao contrário do `![]()`, que mantém
  o "Preview unavailable". A URL remota carrega sozinha, como o `![]()` (R39.3).
- **O bloco de código cercado fica de fora**, e a mensagem em streaming só ganha a miniatura ao terminar, como o Mermaid
  (`NativeChatMarkdown.tsx:141`, `renderMermaid={!streaming}`; R42.2).

### D45 — O tema do chat — `brza-studio/src/shared/native-chat-appearance-settings.ts` e `…/native-chat/native-chat-appearance-style.ts` (P58)

- **Origem:** pedido 31, R48.1, R48.4, R49.2, R49.3
- **Contexto:** o chat não tem tema próprio. O `NativeChatAppearanceSettings` tem a fonte, os tamanhos, a largura, o
  contraste e o `matchTerminalInterface` (`src/shared/native-chat-appearance-settings.ts:3-16`). Com essa chave ligada,
  o `nativeChatAppearanceStyle` lê o tema do terminal, fixa o esquema e remapeia `--background`, `--card` e `--border`
  a partir do canvas (`native-chat-appearance-style.ts:105-158`). O canvas é `color-mix` da frente sobre o fundo, a
  `--chat-canvas-mix` (`main.css:576-584`). O terminal escolhe o par escuro e claro pelo tema do app
  (`src/shared/terminal-theme-selection.ts:25-35`).

#### Como fica

- **O campo.** O `NativeChatAppearanceSettings` ganha o par de temas, na forma do terminal: um tema escuro, o claro
  ligado ou não, e o tema claro (`terminalThemeDark`, `terminalUseSeparateLightTheme` e `terminalThemeLight`,
  `global-settings-types.ts:123-127`). O valor é o nome de um tema do catálogo do terminal, incluídos os temas
  personalizados, ou o "Padrão do BrzA", que é o padrão (R49.3).
- **O resolvedor.** Uma função compartilhada, no `src/shared/`, devolve o tema efetivo do chat: o fundo, a frente, as
  cores ANSI e o esquema. A escolha entre o escuro e o claro segue a regra do `selectTerminalTheme`. O "Padrão do BrzA"
  dá o fundo e a frente de hoje do app (`--background` e `--foreground`, `main.css:192-195` e `:304-306`) e as cores
  ANSI do tema padrão do terminal. O P59 e o P60 leem só esta função.
- **O estilo.** O caminho de hoje do "igualar ao terminal" passa a ler o resolvedor no lugar do terminal: o esquema,
  pelo `isTerminalBackgroundLight` do fundo, e o remapeamento das variáveis. O "Padrão do BrzA" não fixa esquema e
  segue a raiz, como hoje. O contraste continua valendo, pela mesma fórmula do canvas; a fonte e o tamanho do chat
  deixam de ser os do terminal.
- **A migração.** Na carga das configurações (`normalize-loaded-global-settings.ts:72`), o `matchTerminalInterface`
  ligado vira: o par de temas do terminal como o do chat, a fonte e o tamanho do terminal como os do chat, o contraste
  em 100 e o terminal seguindo o chat (D46). A chave sai. Desligado, o chat fica no "Padrão do BrzA".
- **A tela.** Na seção do chat (`AppearanceChatSection.tsx`), o interruptor "igualar ao terminal"
  (`AppearanceChatContrastControls.tsx:34-39`) dá lugar ao seletor do tema escuro, ao "Tema claro separado" e ao
  seletor do claro, como no terminal (`TerminalThemeSections.tsx:91-103`). A fonte, os tamanhos e o contraste ficam
  sempre ativos, sem o "Set by terminal interface" (`AppearanceChatSection.tsx:72-76`, `:90-96`).

#### A conferir no passo

- O web e o mobile leem o `nativeChatAppearance` (`src/renderer/src/web/web-native-chat-appearance-settings.test.ts`).
  O campo novo não pode quebrá-los, e o mobile não ganha o tema agora.
- O atalho Cmd +/- do tamanho do chat (`native-chat-font-size.ts:15-17`) era ignorado com o "igualar"; sem a chave,
  ele volta a valer sempre.

### D46 — O terminal segue o chat — `brza-studio/src/shared/terminal-theme-selection.ts` e `…/terminal-pane/terminal-appearance.ts` (P59)

- **Origem:** pedido 31, R48.2, R48.3
- **Contexto:** o tema do xterm sai do `selectTerminalTheme` e do `resolveConfiguredTerminalColors`
  (`terminal-theme-selection.ts:25-35`, `:62-74`), e o `applyTerminalAppearance` escreve o tema, a fonte e o fundo do
  painel (`terminal-appearance.ts:135-232`) a cada mudança das configurações (`use-terminal-pane-lifecycle.ts:93-117`).

#### Como fica

- **O interruptor.** Um campo booleano nas configurações globais, "Seguir o chat", ligado por padrão, com o
  interruptor em `TerminalThemeSections.tsx`. Ligado, os seletores de tema do terminal ficam desabilitados e guardam a
  escolha de antes.
- **Ligado.** O tema do xterm é o do resolvedor do D45: as cores ANSI do tema do chat e o fundo do canvas efetivo do
  chat, com o contraste. A fonte, o tamanho, o peso e a altura de linha são os do terminal (R48.3). Os overrides de cor
  e a opacidade do fundo continuam valendo por cima.
- **Desligado.** O terminal de hoje, sem mudança.

### D47 — O visualizador de Markdown segue o chat — `brza-studio/src/renderer/src/components/editor/` e `src/renderer/src/assets/` (P60)

- **Origem:** pedido 31, R48.2, R48.3, R49.1, R49.4
- **Contexto:** o olho não declara fundo e herda o `bg-background` do `body`, `#0a0a0a` no escuro
  (`markdown-preview.css:1-8`, `MarkdownPreviewSurface.tsx:86`, `main.css:662`); o lápis usa o `--editor-surface`,
  `#1e1e1e` (`rich-markdown-editor.css:9,18`); o modo código, o Islands Dark, `#191A1C` (`MonacoEditor.tsx:277`,
  `islands-dark-theme.ts:9,30`). Os três seguem o claro/escuro do app pelo `useDocumentDarkTheme`
  (`use-document-dark-theme.ts:4-8`). A fonte do olho e do lápis é a do app, no tamanho do editor
  (`use-markdown-preview-source-foundation.ts:153`, `rich-markdown-editor.css:498`).

#### Como fica

- **O interruptor e o tema próprio.** Um campo booleano "Seguir o chat", ligado por padrão, e um par de temas próprio
  do Markdown, na forma do D45, nas configurações do editor, ao lado do `EditorFontFamilySetting`. O seletor só fica
  ativo com o interruptor desligado (R49.1).
- **O esquema.** Um hook do Markdown no lugar do `useDocumentDarkTheme` dá o esquema do chat com o interruptor ligado,
  e o do tema próprio com ele desligado. O `markdown-dark`/`markdown-light` do olho e o tema do Monaco leem esse hook.
- **O fundo.** Ligado, os três modos usam o canvas efetivo do chat; desligado, o fundo do tema próprio. O olho ganha
  fundo explícito, o lápis troca o `--editor-surface` pelo mesmo valor, e o Monaco usa um tema derivado do Islands
  Dark ou do light-plus com o fundo trocado. A sintaxe não muda (R49.4).
- **A tipografia.** Ligado, o olho e o lápis usam a fonte e o tamanho do texto do chat (`--chat-font-family`,
  `--chat-font-size`), e o código dentro deles, a fonte de código do chat. O modo código usa a fonte de código do
  chat, que é a do terminal, e mantém o tamanho do editor (R48.3). O zoom do editor continua somando ao tamanho.
  Desligado, a tipografia de hoje.

### D48 — O leitor do BrzA para a mensagem de outra sessão — `brza-studio/src/main/native-chat/brza/` e `transcript-line-decoders-claude.ts` (P62)

- **Origem:** pedido 32, R50.1, R50.2, R51.1
- **Contexto:** o Claude Code entrega a mensagem de outra sessão num turno `isMeta`, com "Another Claude session sent a
  message:" e o `<agent-message from="…">`, e o leitor descarta todo turno `isMeta` que não é imagem
  (`transcript-line-decoders-claude.ts:108-109`). A devolução de subagente chega no mesmo envelope, com "[Subagent
  hand-back]" e o relatório recuado. A mensagem do usuário já aceita um remetente (`from: AgentMessageSource`,
  `NativeChatAgentMessageRow.test.tsx:20-29`), e a linha desenha "Message from <nome>"
  (`NativeChatAgentMessageSenders.tsx:35`).

#### Como fica

- **O leitor.** Uma função do BrzA reconhece o envelope e devolve o remetente, o texto sem o envelope e o tipo:
  mensagem ou devolução. O descarte do `isMeta` em `:108` ganha uma linha que pergunta antes a essa função.
- **A mensagem.** Vira uma mensagem do usuário com o `from` do remetente, no histórico e ao vivo. O nome é o `from=` do
  envelope: o nome da sessão, ou o ID do subagente.
- **O rótulo.** "Mensagem de <nome>" para a mensagem e "Devolução de <nome>" para a devolução, no `pt.json`, com o
  inglês no `en.json`.

#### A conferir no passo

- Se o caminho ao vivo recebe o turno `isMeta`, ou se a mensagem só aparece pelo transcript.
- Se o `AgentMessageSource` comporta o tipo devolução sem mudar o contrato do upstream, ou se o tipo vai num campo do
  BrzA.

### D49 — O cartão do Orca para as mensagens entre agentes — o `7321b066e83` do upstream (P63)

- **Origem:** pedido 32, R50.1
- **Contexto:** o upstream de 2026-10-29 troca a linha "Message from" por um cartão com o status do remetente
  (`7321b066e83`, #34824): `NativeChatAgentMessageCard.tsx`, a relação do remetente no main
  (`src/main/runtime/orchestration/agent-message-relation.ts`) e dois módulos do `src/shared/agent-session/` que não
  existem aqui. O `upstream/main` está 1021 commits à frente da `master`.

#### Como fica

- **O commit vem com `cherry-pick -x`**, para o próximo sync reconhecer, mais os arquivos de que ele depende. Cada
  arquivo além do commit vira um desvio `X`.
- **O cartão lê também o remetente do D48.** A sessão do Claude Code não tem o status do correio do Orca; o cartão
  mostra o que tiver, e o que faltar fica de fora, sem erro.

### D50 — O clique no remetente abre a aba da sessão — `brza-studio/src/renderer/src/components/native-chat/` (P64)

- **Origem:** pedido 32, R50.3
- **Contexto:** o clique no remetente do Orca abre o terminal dele pelo `openAgentMessageSender`
  (`NativeChatAgentMessageRow.test.tsx:11-12`). A sessão do Claude Code tem só o nome.

#### Como fica

- O clique procura, entre as abas de chat abertas, a da sessão com aquele nome, e a foca. Sem aba, o nome fica sem
  ação.

#### A conferir no passo

- De onde vem o nome da aba: o `/rename` que o `brza-sessions --wait` espera, o `--name` do Claude Code, ou o título da
  aba. A busca usa o que o app guardar.
