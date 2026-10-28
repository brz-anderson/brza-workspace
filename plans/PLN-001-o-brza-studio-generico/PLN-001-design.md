# PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat — Desenho

O desenho do [PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](PLN-001-plan.md). O
que este desenho assume e o Terreno medido em 2026-10-24 estão no desenho do PLN-025 do workspace da Fixfy
(`plans/PLN-025-orca-desktop-cli-app-e-web/PLN-025-design.md`); os itens D1 a D35 vieram de lá, pelo PLN-029 da Fixfy,
com os IDs de antes (PLN-025/R28.2), e os D36 a D41 são daqui, de 2026-10-27. Nos itens D1 a D35, o nome do
repositório nos caminhos é o de hoje, `brza-studio/…`, e não o de antes do rebrand.

### D1 — O build local, assinado — `brza-studio/config/scripts/build-mac-local.mjs` (P1, PLN-028/P5)

- **Origem:** R6.1, R7.2, R8
- **Como fica:** `pnpm run build:mac` sai do clone limpo ao `.app` sem passo à mão: instala as dependências de
  `mobile/`, chama o `swift` com `--build-system native` e empacota só arm64. A identidade de assinatura vem de variável
  (`CSC_NAME`); sem ela, o build sai ad hoc com `codesign --force --deep -s -`, para servir a projetos fora da Fixfy. Com a
  `CSC_NAME` posta, o build sai assinado com a identidade dela, com o hardened runtime.

### D2 — O atualizador desligado — `brza-studio/src/main/updater/` (P2)

- **Origem:** R10.2
- **Como fica:** um predicado único, `isUpdaterEnabled()`, falso no build local, no lugar das 6 guardas
  `!app.isPackaged` (`updater-setup.ts:139`, `updater-scheduling.ts:67`, `updater-menu-checks.ts:17`,
  `updater-build-selection.ts:92`, `updater-remote-status.ts:20`, `updater-nudge.ts:9`). A versão nova chega por
  sincronização e build (PLN-025/D4).

### D6 — O tema Islands Dark no Monaco e no Shiki — `brza-studio/src/renderer/src/lib/` (P6)

- **Origem:** Pedido 5, R7.2
- **Como fica:** `monaco-setup.ts` registra o tema com `defineTheme`, com as cores de
  `~/.config/orca-themes/patch_orca_monaco.py:49-90`, e os 6 `vs-dark` passam a usá-lo; o `syntax-highlighter.ts` troca
  o `dark-plus` pelo mesmo tema.

### D20 — O olho no visualizador de Markdown — `brza-studio/src/renderer/src/components/editor/` (P25)

- **Origem:** pedido 14, R19
- **Como fica:** na aba do arquivo Markdown, a barra mostra o olho, o lápis e o código, nessa ordem
  (`MARKDOWN_EDIT_VIEW_MODES = ['preview', 'rich', 'source']`), e o `getDefaultMarkdownViewMode` devolve `preview`. O
  olho é o modo `preview` que o Orca já tem: renderizado e só leitura, em linha pelo `EditorMarkdownFileSurface.tsx`. O
  modo escolhido por arquivo continua guardado e vence o padrão. A aba de diff segue com o código e o lápis, e o padrão
  `source`; a aba de prévia dedicada (`editor.markdownPreview`) não muda.

### D21 — O build local de Windows — `brza-studio/config/scripts/build-win-local.mjs` (P26, P27)

- **Origem:** pedido 15, R20
- **Como fica:** `pnpm run build:win` sai do clone limpo a um instalador NSIS x64 sem passo à mão: instala o `mobile/`,
  roda o `build:desktop` e o `ensure:electron-runtime` e chama o `electron-builder --win --x64` com a
  `ORCA_LOCAL_BUILD_VERSION` carimbada pelo mesmo `createLocalBuildVersion` do D1, o que desliga o atualizador (D2). O
  instalador sai sem assinatura, com o aviso do SmartScreen; os canais oficiais do upstream (`ORCA_WIN_*`) não mudam. No
  Windows se instala só o `brza-studio`, sem o código da Fixfy.

### D27 — A barra da mensagem do agente e o Bifurcar — `brza-studio/src/main/claude/` e `…/native-chat/` (P33, P34)

- **Origem:** pedido 19, R25.3, R26.2
- **Como fica:** a barra do `NativeChatAgentControls` (`NativeChatTranscriptChrome.tsx:263-294`), que hoje só recebe o
  Markdown, a hora e o rolar ao topo, passa a receber o id da mensagem pelo `NativeChatAssistantMessageRow.tsx:93`, e
  ganha os botões dos D27 a D29. O Bifurcar corta o transcript no uuid da mensagem pelo `forkSession(sessionId,
  {upToMessageId})` do SDK (`sdk.d.ts:831`), com o mapeamento do id da linha ao uuid que o rewind já faz
  (`claude-rewind-fork.ts`), e abre a sessão nova com `resume` no fork, numa aba nova do mesmo worktree, como o
  bifurcar do claude.ai. A conversa de origem não muda.

### D28 — O Novo Chat a partir da mensagem — `brza-studio/…/native-chat/` (P34)

- **Origem:** pedido 20, R25.3
- **Como fica:** o botão abre uma aba nova de chat no mesmo worktree pelo `launchAgentInNewTab`, com a mensagem clicada
  como rascunho na caixa (`promptDelivery: 'draft'`, `agent-launch-prompt-delivery.ts:12-25`), sem enviar. A mensagem
  longa se confere no `canMirrorLaunchDraftToNativeChat`.

### D29 — O Fixar Capítulo na régua de prompts — `brza-studio/…/native-chat/` (P35)

- **Origem:** pedido 21, R26.1
- **Como fica:** o capítulo é o prompt do usuário e a resposta do agente. O botão na barra da resposta vem marcado e
  fixa ou desafixa o capítulo; a régua de prompts (`native-chat-message-rail-items.ts`,
  `structured-agent-session-rail-outline.ts`) destaca os fixados, e a prévia dela mostra o capítulo. O estado é por
  sessão, no renderer.

### D30 — O seletor de conta — `brza-studio/src/main/claude/`, `src/main/claude-accounts/` e `…/native-chat/` (P36)

- **Origem:** pedido 22, R25.3, R26.3
- **Como fica:** ao lado do seletor de modelo e esforço (`NativeChatComposerActions.tsx:140-150`), um seletor lista as
  contas Claude do Orca (`src/main/claude-accounts/`), como o `claude|adm` do terminal. A troca segue o molde do
  `/clear`: a mesma aba e a mesma sessão do Orca, com uma sessão nova do Claude por baixo e um divisor "Conta trocada -
  <conta>", irmão do "Contexto limpo" (`NativeChatNoticeRow.tsx:75-94`). O contexto vai fiel: o main copia o `.jsonl`
  da sessão para o `projects/` da conta nova e retoma por `resume`. A conta deixa de ser identidade fixa da sessão
  nesse caminho: a recusa `identityMismatch` (`agent-session-reservation-admission.ts:197-202`) e o
  `historyInOtherAccount` (`claude-structured-launch-home.ts:44-69`) abrem exceção para a troca. Se o `~/.claude-adm`
  não entrar como conta do Orca, o registro dele vem antes.
- **Para depois:** a opção "Selecionar automaticamente" no seletor de modelo e esforço, por rodada própria.

### D31 — As sugestões de ortografia no botão direito — `brza-studio/src/main/window/` (P37)

- **Origem:** pedido 23, R25.3
- **Como fica:** o menu do botão direito já lista até 5 sugestões e troca a palavra
  (`editable-context-menu.ts:200-235`), com o corretor do macOS. O passo confere na caixa de texto do chat, em pt-BR; se
  as sugestões não aparecerem, corrige o que as esconde — o idioma ou o menu próprio do chat
  (`use-native-chat-context-menu.tsx`).

### D32 — O Markdown na caixa de texto — `brza-studio/…/native-chat/NativeChatPromptEditor.tsx` e as configurações (P38)

- **Origem:** pedido 24, R25.3
- **Como fica:** um switch "Modo de visualização Markdown" nas configurações de chat (`ChatBehaviorSetting.tsx`), com a
  chave em `global-settings-types.ts` e o padrão desligado em `default-global-settings.ts`. Ligado, a caixa de texto,
  que já é Tiptap (`NativeChatPromptEditor.tsx:21`), ganha as extensões de formatação do modo de edição do visualizador
  de Markdown e mostra o texto já formatado; o que se envia segue em Markdown, com as pílulas de arquivo, imagem e
  skill.

### D33 — O Editar na mensagem do usuário — `brza-studio/…/native-chat/NativeChatUserMessageRow.tsx` (P39)

- **Origem:** pedido 25, R25.1, R25.2
- **Como fica:** a barra da mensagem enviada (`NativeChatUserMessageRow.tsx:24-60`), que já tem o copiar, a hora e o
  rewind, ganha o Editar: a mensagem vai à caixa de texto, sozinha se a caixa estiver vazia, abaixo do rascunho se
  houver um, e o foco vai à caixa. O Enviar agora fica no cartão da fila (`NativeChatQueuedMessageCard.tsx:133-146`),
  como já é.

### D34 — O Continuar em outra conta, no aviso de limite — `brza-studio/…/native-chat/` (P40)

- **Origem:** pedido 26, R27.1, R27.2
- **Como fica:** na linha do aviso de limite (`NativeChatNoticeRow.tsx:149-171`), ao lado do Continuar, o botão
  "Continuar em" abre um menu com as outras contas do seletor do D30. A escolha faz a troca do D30 — o transcript
  copiado, o `resume` e o divisor "Conta trocada - <conta>" — e, só depois que a sessão nova sobe, envia o mesmo
  Continuar do `continueUsageLimit` (`NativeChatInterruptedContinue.tsx`), "Continue where you left off.". Se a troca
  falha, nada é enviado, e o erro vai ao aviso da caixa de texto, como o do Continuar.

### D35 — O Retomar automaticamente, no aviso de limite — `brza-studio/src/main/` e `…/native-chat/` (P41)

- **Origem:** pedido 26, R27.3, R27.4
- **Como fica:** ao lado do Continuar, o botão "Retomar automaticamente" aparece quando a falha traz o `resetsAt`
  (`shared/agent-session-usage-limit.ts`). O clique grava no main, persistida, uma retomada para o `resetsAt` + 1 min,
  com a sessão e o turno do corte; na hora, o main envia o mesmo Continuar no mesmo chat e na conta que ele estiver.
  A linha passa a mostrar "Retomada às HH:MM · Cancelar", e qualquer mensagem enviada antes cancela a retomada. Com o
  Orca fechado na hora, a retomada vencida dispara ao abrir, junto da retomada do restart
  (`native-chat-resume-on-restart-store.ts`), só se o chat ainda está no corte do limite, sem mensagem depois.
- **Descartada:** a Automação do Orca (`main/automations/`), que é cron recorrente e abre um agente novo, sem continuar
  o chat; e o timer no renderer, que morre ao fechar a janela (R27.3).

### D36 — O "Perguntou:" em cor de destaque — `brza-studio/src/renderer/src/components/native-chat/NativeChatAwaitingInputRow.tsx` (P42)

- **Origem:** pedido 27, R29.1
- **Como fica:** o texto da pergunta do agente passa de `text-chat-foreground` à cor `primary` do tema, a mesma do ✓ de
  opção escolhida, nos três pontos: a linha fechada (`:76`), a pergunta aberta (`:113`) e a lista de perguntas
  (`:118`).

### D37 — A base dos ícones de marca — `brza-studio/src/shared/native-chat/tools/` e `…/native-chat/NativeChatToolIcon.tsx` (P43)

- **Origem:** pedido 27, R29.4
- **Como fica:** as categorias novas moram num módulo do BrzA, por exemplo `src/shared/native-chat/tools/brza/`, com
  uma linha de montagem no `CATEGORY_BY_ROW_WORD` (`native-chat-tool-icon.ts:58`), arquivo do upstream, para os merges
  de `stablyai/orca` seguirem com conflito pequeno. Os ícones genéricos são lucide; o SVG de marca (git, GitHub, Jira,
  Figma, Firebase) vem de um componente do BrzA só no desktop, pelo `NATIVE_CHAT_TOOL_GLYPHS`, e o mobile
  (`lucide-react-native`, que compartilha os ids de ícone) cai no lucide equivalente. A licença de cada logo se confere
  antes de trazer, por exemplo o Simple Icons, CC0.

### D38 — Os comandos de shell com ícone e título por categoria — `brza-studio/src/shared/native-chat/tools/brza/` (P44 a P47)

- **Origem:** pedido 27, R29.2
- **Como fica:** o comando de shell vira a categoria pelo input, como o `runsOrcaBrowserCommand` já faz com `orca
  browser …`. `git`: GitBranch ou GitCommit pelo subcomando, título "git commit — <mensagem>", e o clique no hash abre
  o diff do commit no visualizador. `gh` de PR e issue: GitPullRequest, título "PR #123 — <título>" e um chip que abre
  o PR no navegador. Testes (`vitest`, `run-vitest.mjs`, `flutter test`, `pytest`): FlaskConical, com passou/falhou
  contado no título a partir da saída. Pacotes e build (`pnpm`, `npm`, `flutter pub`, build): Package ou Hammer, só
  ícone e título, sem interação.
- **A perguntar a Anderson:** o comando que casa com mais de uma categoria, como `git` dentro de `&&`, e o formato
  exato do chip e do título.

### D39 — As ferramentas de MCP e do agente com ícone e título — `brza-studio/src/shared/native-chat/tools/brza/` (P48 a P51)

- **Origem:** pedido 27, R29.3
- **Como fica:** a chamada MCP chega identificada pelo `NativeChatMcpIdentity`. Jira e Confluence: chip com a chave do
  card (`FIX-123`) ou o título da página, que abre no navegador. Skill: Sparkles e "Skill · <nome>". Figma: logo, nome
  do nó e miniatura do `get_screenshot` na linha. Firebase e Context7: Flame e BookOpen, com o nome do projeto ou da
  biblioteca no título, sem interação.

### D40 — Os blocos de código e as tabelas com 120 colunas na largura total — `brza-studio/…/native-chat/` (P52)

- **Origem:** pedido 28, R30.1, R30.2
- **Como fica:** só com `width === 'full'` (`native-chat-appearance-style.ts:77` e `:88`), uma variável, por exemplo
  `--chat-wide-block-width`, posta só nesse ramo e lida pelo bloco (`NativeChatCodeBlock.tsx:46` e `:62`) e pela tabela
  (`native-chat-markdown.css:25` e `:64`), num módulo ou CSS do BrzA com uma linha de montagem nos arquivos do upstream.
  Todo bloco e toda tabela têm exatamente `120ch` mais o padding do bloco, mesmo curtos; num painel mais estreito
  encolhem até 100% da coluna e rolam na horizontal; o texto corrido segue na largura total. O `ch` é medido na fonte
  mono do chat (`--chat-code-font-size`), também na tabela, para as bordas se alinharem. "Normal" e "Larga" não mudam.
- **A perguntar a Anderson:** o alinhamento do bloco quando sobra espaço (à esquerda, com o texto, ou centralizado), e
  se o diff e a saída de ferramenta seguem a mesma regra.

### D41 — Os links do chat em azul claro — `brza-studio/src/renderer/src/components/native-chat/native-chat-markdown.css` (P53)

- **Origem:** pedido 29, R31.1
- **Como fica:** `.native-chat-markdown a` (`:18`) passa de `color: var(--chat-foreground-strong)` a uma variável
  `--chat-link`, `#79C0FF` no tema escuro e `#0969DA` no claro. O sublinhado segue com 40% da cor
  (`color-mix(in srgb, currentColor 40%, transparent)`), e a mensagem com tom `faint` segue herdando a cor (`:55`).
