---
status: in_progress
phase: execution
origin: request
ready: sim
estimate_h: 20.75
executed_h: 3.6
remaining_h: 0
scope:
  - brza-studio
  - workspace
opened: 2026-10-31
owner: Anderson
tags:
  - design
---

# PLN-007: A marca BrzA tem símbolo, logotipo e derivadas a partir da chama do app

- **Retomar:** os seis passos executados; P1 a P6 estão na `master` do `brza-studio` (o P6 em `5c286937e0c`) e o README
  do workspace na `master` daqui (`b30b6bc`). Há o commit `release: v1.4.246-alpha.1` (`6d47623`) e a tag anotada
  `v1.4.246-alpha.1`, **só locais**, e o DMG final em
  `~/Projects/brza-studio/dist/brza-studio-1.4.246-alpha.1-macos-arm64.dmg`. O plano **não fecha** (`status` segue
  `in_progress`) até Anderson conferir o DMG (os casos C1 a C8 no app), dar o push do commit e da tag e decidir o `.ico` de
  6 ou 7 quadros; depois, `status: done`, `phase: closed` e `completed`.
- **Dividido:** [PLN-007 — Entrevista](PLN-007-interview.md) · [PLN-007 — Desenho](PLN-007-design.md)

## Pedido

- **Origem:** pedido livre, na sessão do workstream `workspace` de 2026-10-31, que respondeu a R1 e abriu o
  workstream `brand`; o plano é aberto na sessão do `brand` no mesmo dia.

> "Vamos planejar a identidade visual da marca `BrzA`, partindo do ícone do app para montar a logo."

Na sessão do `brand`, no mesmo dia, durante a R2:

> 2. "faça um desenho da borda do chat do `BrzA Studio` igual a borda da logo"
>
> 3. "vamos continuar nessa linha de adicionar mais da marca no chat"

### Cobertura

> Rascunho da abertura: os critérios são propostas e se fecham no Planejar, com o passo e o teste.

| Origem     | Critério de aceite                                                                                     | Passo | Teste (nível)                         |
| :--------- | :----------------------------------------------------------------------------------------------------- | :---- | :------------------------------------ |
| `R2.1`     | O símbolo BrzA é a ilustração do ícone atual, com o `}` solto refeito inteiro                           | —     | conferência a 1024 e a 256 px (manual) |
| `R2.3`     | O símbolo existe em SVG desenhado pela sessão, com paths, conferido a 16, 32 e 128 px                  | —     | `brza shot` e abrir o SVG (manual)    |
| `R3.1`     | O logotipo BrzA existe em SVG, no arranjo L2, para as 4 filhas, na horizontal e na vertical, nos 2 temas | —     | conferência dos artboards (manual)    |
| `R3.3`     | O corte pequeno é o traço mono de hoje, com o `}` corrigido, e serve ao glifo do chat, ao M2 e ao M5    | —     | conferência a 13, 16 e 18 px (manual) |
| `R2.2`     | BrzA Studio, o CLI `brza` e o workspace usam o símbolo único, com o nome da filha ao lado da palavra   | —     | conferência dos artboards (manual)    |
| `R2.5`     | O composer do chat ganha a borda da logo só no foco, nos dois temas                                    | —     | conferência no app (manual)           |
| `R2.6`     | O chat mostra a marca no estado vazio, no agente trabalhando, no anel de contexto e no cabeçalho      | —     | conferência no app (manual)           |
| `R3.2`     | A paleta P1 vira tokens nos dois temas, e o `--agent-question` passa a azul                             | —     | conferência no app (manual)           |
| `R3.4`     | O ícone do app sai do SVG do símbolo pelo `generate.sh`, e o tray, a barra de título, a Landing e o Onboarding usam a marca | — | `resources/icon-source/generate.sh` e conferência no app (manual) |
| `R3.4`     | O `brza --help` não imprime "orca", e os READMEs do `brza-studio` e do `brza-workspace` levam o logotipo | —     | `brza --help` (manual)                |

### Fora de escopo

- **Aplicar a marca no código do `brza-studio`.** Cada aplicação é passo de código, executado numa sessão do
  `brza-studio`, na branch `<tipo>/pln-007-<slug>`; aqui fica o pedido.
- **O app mobile e os restos da Orca à vista** (R3.4). Foram à
  [issue dos restos da Orca](../../work/issues/os-restos-da-orca-a-vista-no-brza-studio.md).
- **O cursor e a seleção em laranja no chat** (M4, R2.6). Recusado na rodada; sem destino.
- **Os testes e2e de SQLite que falham na `master` do `brza-studio`**, achados na conferência do P4. Foram à
  [issue dos testes e2e de SQLite](../../work/issues/os-testes-e2e-de-sqlite-falham-na-master-do-brza-studio.md).
- **O `brza shot` quebrado pelo merge do upstream v1.4.246 no `brza-studio`.** Foi à
  [issue do brza shot](../../work/issues/brza-shot-quebra-com-os-tokens-do-painel-movidos.md); o Desenho segue com uma
  cópia corrigida no scratch.

## Passos

Os itens `D` estão em [PLN-007 — Desenho](PLN-007-design.md). O desenho do símbolo e dos lockups é da sessão do
`brand` (R4.2); a aplicação é de uma sessão do `brza-studio`, nas três branches da R4.4. Cada passo só executa a pedido
explícito de Anderson. O P3 não depende do símbolo e pode correr junto do P1.

### P1 — O símbolo A1, as variantes e o corte S1

Executa D1 (o desenho) e D2 (o `d` corrigido) · executor: sessão do `brand`, no scratch

Estimado: 6,5 h · Executado: 0,25 h

- [x] **1. O S1** — o `d` corrigido do D2 em `/private/tmp/pln-007/brand/brza-symbol-mono.svg`, conferido a 13, 16, 18
      e 32 px pelo `brza shot` de um artboard, nos dois temas.
- [x] **2. O mestre** — `brza-symbol.svg` no tile T1, com o esqueleto do mono e as camadas de cor sobre o
      `build/icon.png` como decalque; o `}` em `#brza-brace-close`, usado três vezes.
- [x] **3. As variantes** — o `brza-brand-build.mjs` gera o claro, o dev, o com selo (o selo entra no P2), o tray e o
      `logo.svg`, a partir do mestre.
- [x] **4. A conferência** — artboard com o mestre e as variantes a 16, 32, 128 e 1024 px, nos dois temas, conferido
      pelo PNG antes da rodada: `brza shot <artboard>.html <scratch>/p1-simbolo.png --width 736`.
- [x] **5. A rodada do símbolo** — aprovação do texto e do artboard; o PNG aprovado vai à pasta do plano como
      `PLN-007-simbolo-a1.png`.
- [x] **6. Commit** — o PNG e a linha do plano, pelo `brza note commit`.

**Evidência:** `brza shot` do artboard do mestre, das variantes, do S1 (13, 16, 18 e 32 px) e do tray, nos dois temas, em
[`PLN-007-simbolo-a1.png`](PLN-007-simbolo-a1.png); `magick compare -metric AE` do traço mono original contra a chama do
mestre, a 1024 px, dá 347 px de 1 milhão, todos no `}` solto e no `{`, que são a correção do D2 e o espelho; o S1 gerado
tem 12 subpaths e o solto em 9,06–10,08 × 16,68–19,56, igual à sonda do Desenho. O 1024 px saiu pelo `rsvg-convert`, e
não pelo artboard, que tem 736 px. A aprovação é a [R10](PLN-007-interview.md), e o commit é `f1f7fe6` em `workstream/brand`. A fonte e o gerador estão em
`PLN-007-fonte-da-marca/`; o `brza-brand-build.mjs` regenera os SVG idênticos, pixel a pixel. O mestre sai sem a língua
clara e sem as faíscas do D1, por decisão da R10.

### P2 — Os lockups L2 e o texto em paths

Executa D3 (o script de texto e os 16 SVG) · executor: sessão do `brand`, no scratch

Estimado: 2,5 h · Executado: 0,4 h

- [x] **1. O texto em path** — o `brza-brand-text.swift` devolve o JSON de "BrzA" (750), "STUDIO", "CLI", "WORKSPACE"
      (500, `.14em`); a prova é o avanço de "BrzA" a 100 pt dar ~246,9 em 750.
- [x] **2. Os lockups** — o `brza-brand-build.mjs` monta os 16 `*-lockup-*.svg` e o `<g id="seal">` do
      `brza-app-icon.svg`, pela tabela de geometria do D3.
- [x] **3. A conferência** — artboard com as 4 filhas, horizontal e vertical, nos 2 temas, ao lado do PNG do L2, pelo
      `brza shot`.
- [x] **4. A rodada dos lockups** — aprovação; o PNG vai à pasta do plano como `PLN-007-lockups-l2.png`. Aprovado na
      [R11](PLN-007-interview.md), com o selo sem o "ADE".
- [x] **5. Commit** — o PNG e a linha do plano, pelo `brza note commit`; a fonte dos lockups está em
      `PLN-007-fonte-da-marca/`.

**Evidência:** `swift brza-brand-text.swift <woff2> 750 0 BrzA` dá `advance` 246,91 (a prova do Desenho)
e `capHeight` 71; em `wght` 400, 226,4. O `brza-brand-build.mjs` gera os 16 `*-lockup-*.svg` e o `brza-app-icon.svg` com o
`<g id="seal">`. O artboard foi conferido pelo `brza shot` a 736 px, nos dois temas
([`PLN-007-lockups-l2.png`](PLN-007-lockups-l2.png)), ao lado do L2 da R3; a primeira passada estourou a
fila dos verticais, e foi corrigida. O `rsvg-convert` renderiza o ícone com selo e um lockup sem erro, e é com ele que o
P4 gera o `.icns`. **O selo do ícone saiu sem o "ADE"**, a pedido de Anderson em 2026-11-02, e o grupo chama e texto
desceu 36 px para ficar centrado no tile (margem de ~125 px em cima e embaixo); o `brza-app-icon.svg` foi regenerado.
**Desvio:** o `kCTKernAttributeName` zero desliga o kerning, então o `advance` do "BrzA" a
`tracking 0` é a soma dos avanços; com o `-0,01 em` dos lockups o kerning vale, como no texto vivo do `BrzaWordmark`.

### P3 — Os tokens P1 e o aviso de pergunta azul

Executa D4 · executor: sessão do `brza-studio`, branch `feat/pln-007-brand-tokens`

Estimado: 1,25 h · Executado: 0,3 h

- [x] **1. A conferência que falha antes** — sem teste novo, porque token de CSS não tem lógica
      (`docs/agents-md-refs/test-antipatterns.md`): `grep -c 'agent-question: var(--color-orange' src/renderer/src/assets/main.css`
      dá 2 antes e deve dar 0; `grep -c -- '--brand-gradient' src/renderer/src/assets/main.css` dá 0 antes.
- [x] **2. Implementar** — os tokens e o `@theme inline` do D4; o papel `brand` em `docs/styleguide/color.md` e a frase
      no `docs/STYLEGUIDE.md:5`.
- [x] **3. Rodar e ver passar** — `pnpm check:changed --maxWorkers=2`; `pnpm fixtures:shot native-chat/NativeChatQuestionCard --theme both`,
      com o aviso em azul nos dois temas.
- [x] **4. Commit** — `feat(brand): BrzA brand tokens and a blue agent-question (PLN-007 P3)`, e o merge na `master`.

**Evidência:**

- **1:** o `grep` do laranja deu 2 e o do `--brand-gradient` deu 0, antes; depois, 0 e 1 (a definição).
- **2:** `41bfe6d1d4e` no `brza-studio`: `src/renderer/src/assets/main.css` (`:root`, `.dark`, `@theme inline`),
  `docs/styleguide/color.md` (a linha `brand-*`) e `docs/STYLEGUIDE.md:5`. `oxfmt --check` dos três: passa. Os
  `--chat-composer-focus-*` que o D4 mostra como contexto não existiam e ficaram para o D5, no P5.
- **3:** `pnpm check:changed --base=master --maxWorkers=2` (não há `origin/main` no clone): 21 de 21 passam, depois do
  conserto do `path-literal-ratchet`, que já falhava na `master` com as mesmas duas mensagens e era dos workflows do
  sync do v1.4.246 (`computer-e2e.yml` e `pr.yml` apontavam para `src/main/providers/local-pty/`, que não existe);
  conserto em `a3a89e3aaf5`. **Desvio:** o `fixtures:shot native-chat/NativeChatQuestionCard --theme both` rodou (6 PNG,
  saída 0), mas o cartão de pergunta do chat não usa o `--agent-question` e não mostra o azul; o azul foi conferido no
  `pnpm fixtures:shot AgentStateDot:allStates --theme both --scale 2`, no ícone de "Requer atenção" e no de "Aguardando
  entrada", azul nos dois temas. O P5 e a Regressão devem citar o `AgentStateDot:allStates` onde dizem "o
  `fixtures:shot` do P3".
- **4:** `41bfe6d1d4e` e `a3a89e3aaf5`, fast-forward na `master` do `brza-studio`, `git push origin master`
  (`a70f63b6a92..a3a89e3aaf5`).
- **No app vivo:** `ORCA_BACKGROUND_LAUNCH=1 pnpm dev:fresh -- --remote-debugging-port=9477`, perfil temporário, janela
  fora da tela, lido por CDP. Claro: `--agent-question` `oklch(48.8% 0.243 264.376)` (blue-700) e
  `--agent-question-text` `oklch(42.4% 0.199 265.638)` (blue-800). Escuro, com a classe `.dark` alternada e
  restaurada: `oklch(70.7% 0.165 254.624)` (blue-400) e `oklch(80.9% 0.105 251.813)` (blue-300). Um elemento com
  `text-agent-question` pinta exatamente essas cores, e o `--brand-text` alterna `#c2410c` e `#ffaa44`. O app abriu na
  tela de boas-vindas, sem laranja. O app e o perfil temporário foram encerrados e removidos.
- **Com um agente de verdade:** a pedido de Anderson, um workspace descartável (`repo add` pelo `out/bin/orca-dev`) e
  `agent launch --agent claude --surface terminal --model claude-haiku-5-5`, com um prompt que usa a ferramenta
  `AskUserQuestion`. O Claude (Haiku 5.5) parou na pergunta "Where should this run?", e o sidebar mostrou o ícone de
  pergunta no cabeçalho "Projetos" e na linha do agente, os dois `text-agent-question`, lidos no DOM:
  `oklch(0.488 0.243 264.376)` no claro e `oklch(0.707 0.165 254.624)` no escuro; recortes nos dois temas. O sino
  laranja ao lado do `main` é `text-amber-500`, outro token, e não muda no P3. Não se exercitaram o cartão do kanban,
  a atividade nem o cartão de pergunta do chat: só o sidebar, com um agente de terminal. A pergunta ficou sem resposta,
  o terminal e o app foram encerrados, e o workspace descartável, removido.
- **Limpeza:** o worktree `.worktrees/pln-007-brand-tokens` e a branch `feat/pln-007-brand-tokens` foram removidos, a
  branch sem cópia no `origin` e já contida na `master` (`a3a89e3aaf5`).

### P4 — Os assets no app desktop

Executa D1 e D2 (a cópia ao repositório), D3 (os SVG e o `BrzaWordmark`) e D7 · executor: sessão do `brza-studio`,
branch `feat/pln-007-brand-assets`, depois do P1 e do P2

Estimado: 4,5 h · Executado: 1 h

- [x] **1. A conferência que falha antes** — `magick resources/build/icon.png -alpha extract -threshold 50% -format '%@' info:`
      dá `914x952+55+36` hoje e deve dar `824x824+100+100`; `git grep -n 'invert' -- src/renderer/src/components/Landing.tsx src/renderer/src/components/onboarding/OnboardingFlow.tsx src/renderer/src/components/sidebar/SidebarSettingsHelpMenu.tsx src/renderer/src/components/settings/orca-logo-settings-icon.tsx`
      acha os usos que invertem o `logo.svg` e deve achar nenhum.
- [x] **2. Copiar a fonte** — `resources/brand/` e os dois scripts de `config/scripts/`, aprovados no P1 e no P2; o `d`
      do D2 no `resources/brza-flame-mono.svg` e no `BrzaFlameLogo.tsx`; a frase da `brza-brand-logos.md:6`.
- [x] **3. O pipeline** — o `generate.sh` do D7; `pnpm build:icons` gera o `.icns`, o `build/icon.png`, o
      `icon.png`, o `icon-dev.png`, os dois `app-icons/orca-*.png`, os dois PNG do tray e o `.ico`.
- [x] **4. O `logo.svg` e o logotipo** — o `logo.svg` colorido e os 5 usos sem `invert` e `opacity`; o `BrzaWordmark`
      em `components/brza/` e o CSS dele; a Landing e o Onboarding do D7.
- [x] **5. Rodar e ver passar** — a conferência do 1; `iconutil -c iconset resources/build/icon.icns -o "$TMPDIR/brza.iconset" && ls "$TMPDIR/brza.iconset" | wc -l`
      → 10; `magick identify resources/build/icon.ico | wc -l` → 7; `pnpm check:changed --maxWorkers=2`.
- [-] **6. Casos manuais** — C5, C7 e C8. Feitos pelo `brza shot`, que prova o visual e não o app; o Dock, a barra de título
      do Windows e o tray de verdade seguem com Anderson. Motivo: o `brza shot` converte um artboard, não abre o app.
- [x] **7. Commit** — `feat(brand): the BrzA symbol, icon pipeline and wordmark (PLN-007 P4)`, e o merge na `master`.

**Evidência:**

- **1:** antes, `914x952+55+36` e 3 usos de `invert` (a Landing usava o tile `#12181e`, e não o `invert`); depois,
  `824x824+100+100` e nenhum `invert`.
- **2:** o gerador, adaptado ao S1 de 12 subpaths, dá `magick compare -metric AE` **0** nos 23 SVG (22 de `resources/brand/`
  e o `logo.svg`) contra a fonte aprovada; o mono e o tray saem idênticos byte a byte. O `d` do D2 está em
  `resources/brza-flame-mono.svg` e no `BrzaFlameLogo.tsx`.
- **3:** `pnpm build:icons`, saída 0, gerou o `.icns` (10 fatias, de 16 a 1024), `build/icon.png`, `icon.png`,
  `icon-dev.png`, os dois `app-icons`, os dois PNG do tray e o `.ico`. Os PNG foram lidos: sem faíscas, e o selo é só
  "BrzA STUDIO" nas fatias de 128 para cima.
- **4:** os 5 usos do `logo.svg` sem `invert` nem `opacity`; o `BrzaWordmark` e o teste dele, de 2 casos; o h1 da Landing
  e o do Onboarding usam o wordmark.
- **5:** `iconutil -c iconset` → 10; `magick identify icon.ico` → **6, não 7** (desvio abaixo). O `pnpm check:changed
  --base=master` deu 26 de 27: o `unit tests` falhou em 3 testes de 4 arquivos e2e, com "unable to open database file", e
  os mesmos 4 arquivos falham na `master` `a3a89e3aaf5`, isolados; foi à issue. O `implementer` rodou 24 de 24 antes da troca
  do rótulo do seletor, que ampliou o conjunto de testes.
- **7:** `1bfb496aebf`, fast-forward na `master` do `brza-studio`, `git push origin master`
  (`a3a89e3aaf5..1bfb496aebf`); o worktree e a branch foram removidos.
- **Desvios:** (a) o `.ico` tem 6 quadros: o `trim-windows-icon-source.mjs` emite `[256,128,64,48,32,16]`, e o 7º (24 px)
  do arquivo antigo vinha de um pipeline anterior — **aberto para Anderson**: acrescentar o 24 ao `ICO_FRAME_SIZES`, que é
  script e teste do upstream; (b) o `BrzaWordmark` entrou na allowlist de localização, e as duas chaves de i18n que a
  Landing e o Onboarding deixaram de usar foram apagadas das 11 línguas; (c) a Landing mantém o `<h1>` e o `alt` que já
  tinha; (d) a frase de `brza-brand-logos.md` ficou truncada, e o P5 a reescreve; (e) o rótulo "BrzA Studio ADE" do seletor
  virou "BrzA Studio", a pedido de Anderson.



### P5 — A marca no chat

Executa D5 e D6 · executor: sessão do `brza-studio`, branch `feat/pln-007-brand-chat`, depois do P3 e do P4 (nas duas, os merges já tinham saído)

Estimado: 4,5 h · Executado: 0,9 h

- [x] **1. Testes que falham**
  - `NativeChatMessageList.turn-indicator.test.tsx:115,160` passa a afirmar o `[data-brza-working-flame]` com
    `size-4.5` e o rótulo com `brza-working-label`, no lugar do `animate-spin`; falha com o spinner de hoje.
  - `NativeChatContextUsageRing.test.tsx` ganha o caso de 60%, com o traço em `url(#…)`, e o de 95%, com
    `currentColor` e `text-destructive`; o de 60% falha hoje.
- [x] **2. Implementar** — E2 e K2 (D5); M1, M2, M3 e M5, com o `.brza-flame-glyph` (D6).
- [x] **3. Rodar e ver passar** — `pnpm test src/renderer/src/components/native-chat/NativeChatMessageList.turn-indicator.test.tsx src/renderer/src/components/native-chat/NativeChatContextUsageRing.test.tsx`;
      `pnpm check:changed --maxWorkers=2`; `pnpm fixtures:shot 'native-chat/*' --theme both`.
- [-] **4. Casos manuais** — C1 a C4 e C6. Vistos nos componentes reais pelo `pnpm fixtures:shot`, que prova o visual e
      não o app; o foco de teclado, o flicker, o "Reduzir movimento" e os vários painéis seguem com Anderson. Motivo: um PNG
      estático não mostra movimento nem troca de foco.
- [x] **5. Commit** — `feat(native-chat): the BrzA mark in the chat (PLN-007 P5)`, e o merge na `master`.

**Evidência:**

- **1:** antes de implementar, `pnpm test <turn-indicator> <ContextUsageRing>` deu 3 falhas e 28 passes: o caso de 60% do
  anel (o `linearGradient` não existia) e dois do indicador, que ainda achavam o rótulo `min-w-0 truncate
  text-chat-foreground`, sem `brza-working-label`. O caso de 95% passa nos dois estados, é guarda de regressão. As
  afirmações do spinner eram quatro (linhas ~115, ~160, ~271 e ~383), e não duas.
- **2:** E2 e K2 (D5), o glifo comum, M1, M2, M3 e M5 (D6), em `786f4b56ff9`. Um teste a mais, não pedido, em
  `NativeChatComposerActions.test.tsx`: o `data-brza-send` existe no enviar e não no "parar".
- **3:** os dois arquivos, 31 testes passando; o pacote `native-chat` inteiro, 389 arquivos e 3 902 testes;
  `pnpm check:changed --force --base=master --maxWorkers=2`, rodado pela sessão `brand`, sem o cache: 24 de 24 em 61,8 s.
  O `fixtures:shot 'native-chat/*' --theme both` gerou os PNG; o `AgentStateDot:allStates --scale 2` mostra o aviso de
  pergunta azul nos dois temas.
- **5:** `786f4b56ff9`, fast-forward na `master` do `brza-studio`, push `1bfb496aebf..786f4b56ff9`; o worktree e a branch
  foram removidos.
- **Desvios:** (a) o `NativeChatBrandMark.fixture.tsx`, um fixture só de dev, ficou: o `native-chat/*` não tinha
  fixture para o estado vazio, o composer, a atividade e o cabeçalho; (b) os tokens do foco do composer saíram do `:root`
  e do `.dark` do D4 e foram para os blocos de esquema do chat (`:root, .native-chat-appearance[…='light']` e
  `.dark, .native-chat-appearance[…='dark']`), porque um `var()` declarado em `:root` se resolve ali e um chat de esquema
  oposto ao do app saía com o fundo errado, nos dois sentidos — reproduzido num caso novo do fixture e conferido depois
  do conserto; (c) o `lint:design-system` aponta o `rounded-full` do botão de enviar, que já existia e vem do upstream.



### P6 — O CLI e os READMEs

Executa D8 · executor: o `implementer`, na branch `feat/pln-007-brand-cli` (a R11 trocou a `feat/pln-007-brand-assets` da
R8.2, porque a de assets já tinha ido à `master`), para o `brza-studio`; a sessão do `brand`, para o README do workspace
na `master`

Estimado: 1,5 h · Executado: 0,75 h

- [x] **1. Teste que falha** — `src/cli/brza/cli-display-name.test.ts`: o `printHelp(specs)` raiz, com o
      `console.log` espiado, não imprime linha que case `(^|\s)orca\s` e segue imprimindo `orca://pair` e
      `ORCA_PAIRING_CODE`; falha hoje no cabeçalho `orca`.
- [x] **2. Implementar** — o `cli-display-name.ts` e os três `console.log` do `help.ts:14,19,29`; o
      `root-help-text-primary.ts:2` como `'BrzA CLI'`; o `<picture>` e os badges `F26228` no `README.md`.
- [x] **3. Rodar e ver passar** — `pnpm test src/cli/brza/cli-display-name.test.ts src/cli/skills.test.ts src/cli/handlers/core.test.ts`;
      `pnpm tc:cli`; depois do build instalado,
      `"/Applications/BrzA Studio.app/Contents/Resources/bin/brza" --help | grep -c -E '(^|\s)orca\s'` → 0.
- [x] **4. Commit no `brza-studio`** — `feat(cli): brza --help says brza; the README carries the BrzA lockup (PLN-007 P6)`,
      e o merge na `master`.
- [x] **5. O README do workspace** — o `<picture>` do D8 na `master` do workspace, com `git add README.md`, commit e
      push; a prova é `curl -sI` das duas URLs do raw devolver `200` e `image/svg+xml`.

**Evidência:**

- **5:** `curl -sI` das duas URLs do raw (`…/brza-studio/master/resources/brand/brza-workspace-lockup-horizontal-{dark,light}.svg`)
  deu `HTTP/2 200` e `content-type: image/svg+xml`, depois do merge do P4; o `<picture>` do D8 está no título do `README.md`
  da `master` do workspace, em `b30b6bc`, com push. 
- **1:** com um stub que devolvia o texto sem trocar, `cli-display-name.test.ts` deu 3 falhas e 1 passe; o root help trazia o
  cabeçalho `orca`, `Usage: orca <command> [options]` e `$ orca open`, 90 linhas casando. A regex do plano,
  `(^|\s)orca\s`, não pega o cabeçalho `orca` sozinho na linha, e o teste usa `(^|\s)orca(\s|$)`.
- **2:** `src/cli/brza/cli-display-name.ts` (com o `withBrzaCommandName` do D8), os três `console.log` do `help.ts`, o
  `root-help-text-primary.ts` como `'BrzA CLI'`, o `<picture>` e os badges `F26228` no `README.md`.
- **3:** `pnpm test src/cli/brza/cli-display-name.test.ts src/cli/skills.test.ts src/cli/handlers/core.test.ts`, 27 testes;
  `pnpm tc:cli`, saída 0; `pnpm test src/cli` inteiro, 213 arquivos e 2 439 testes; `pnpm check:changed --force
  --base=master`, rodado pela sessão `brand`, 19 de 19 em 29,6 s. O CLI local (`pnpm build:cli`, depois `orca-dev --help |
  grep -c -E '(^|\s)orca\s'`) deu **0**. O mesmo `grep` no `brza` empacotado no DMG final (`1.4.246-alpha.1`, montado somente leitura) deu **0**, e o
  `--help` começa com `BrzA CLI`; o `/Applications/BrzA Studio.app` instalado só ganha isso quando Anderson instalar o DMG.
- **4:** `5c286937e0c`, fast-forward na `master` do `brza-studio`, push `786f4b56ff9..5c286937e0c`; o worktree e a branch foram
  removidos. Mais um commit, `cec12c519c4`, conserta a frase de `brza-brand-logos.md` que o D2 mandava e que ficou
  desencontrada: só o `brza-logo` é o corte pequeno da marca.
- **Desvio:** 11 asserções de help impresso, em 6 arquivos de teste existentes, passaram de `orca` a `brza`
  (`skills.test.ts`, `computer.test.ts`, `file.test.ts`, `terminal-set-pane-title.test.ts`,
  `index-automation-run-output.test.ts` e `index.test.ts`), porque eles leem o help por `main(['--help'])` ou `printHelp`,
  que agora imprime `brza`. O plano dizia "sem mudança" para o `skills.test.ts` e o `core.test.ts`; o `core.test.ts`
  ficou intacto. Mantido, pela opção recomendada, porque sem isso o `check:changed` fica vermelho.


## Regressão

- **O `.icns` segue com duas artes:** sem selo de 16 a 64 px e com selo de 128 para cima. Como se confere: o
  `iconutil -c iconset` do P4 e os 10 PNG abertos.
- **O `.ico` tem 6 quadros**, de 16 a 256 (o 24 px não sai do `trim-windows-icon-source.mjs`). Como se confere:
  `magick identify resources/build/icon.ico`. Aberto: acrescentar o 24, decisão de Anderson.
- **O seletor de ícone** segue com Flame, BrzA Studio e Light Flame, e cada um troca o ícone do Dock; o
  `icon-dev.png` segue fora do pacote. Como se confere: Configurações, o seletor, as três opções, no app de dev e no
  instalado.
- **O tray** segue como template monocromático, com o carimbo de dev e o ícone de atenção. Como se confere: C8.
- **O `brza --help` segue mostrando `orca://pair`, `ORCA_PAIRING_CODE` e `ORCA_ENVIRONMENT`**, e as mensagens de erro
  dos handlers seguem "Usage: orca …". Como se confere: o teste do P6 e `src/cli/handlers/core.test.ts`, que ficou sem
  mudança; as asserções de help impresso dos outros seis arquivos de teste passaram de `orca` a `brza`.
- **O anel crítico**: de 90% para cima, o `text-destructive`, o rótulo `aria` e o popover como hoje. Como se confere:
  o caso de 95% do P5.
- **O composer não pula no foco**: a borda tem 1 px em repouso e em foco; o botão "parar" segue `secondary`, e o
  desabilitado segue como hoje. Como se confere: C1 e C2.
- **O aviso de pergunta só muda de cor**, em todo lugar que usa o `--agent-question` (barra lateral, kanban, atividade,
  cartão de pergunta). Como se confere: o `AgentStateDot:allStates` do P3 (o `fixtures:shot` do `NativeChatQuestionCard` não exercita o
  token) e uma pergunta real de agente no app.
- **O `LoadingSpinner` fora da linha de atividade e o `NativeChatLoadingCue` seguem como estão.** Como se confere:
  `NativeChatQueuedMessageList.test.tsx` e `NativeChatToolRun.test.tsx` sem mudança.
- **Os glifos `brza-logo` nas linhas de ferramenta seguem monocromáticos em `currentColor`.** Como se confere:
  `brza-tool-glyphs.test.tsx`.
- **O estado vazio em `loading`, `error` e `not-agent` segue como está.** Como se confere: o chat recém-aberto, com erro
  de leitura e num terminal sem agente.

## Worklogs

- 2026-10-31 — aberto; R1 gravada como chegou da sessão do `workspace`; Terreno pelo `collector`; R2 fechada, com os
  pedidos 2 e 3 da borda e da marca no chat; R3 fechada, com a issue dos restos da Orca. Parou antes do Desenho.
  [PLN-007: a abertura da marca BrzA](../../work/worklogs/2026-10-31-pln-007-a-abertura-da-marca-brza.md)
- 2026-11-02 — Desenho rascunhado pelo `designer`, 8 itens `D` e 14 pontos; R4 a R8 fechadas; Desenho gravado; R9, o aceite; P1 e P2 aprovados (R10, R11); P3 a P6 executados e na `master` do `brza-studio`; o build local para a conferência de Anderson.
  [PLN-007: o Desenho da marca BrzA](../../work/worklogs/2026-11-02-pln-007-o-desenho-da-marca-brza.md)
- 2026-11-02 — P3 executado no `brza-studio`: os tokens da marca, o `--agent-question` azul, o conserto do
  `path-literal-ratchet`, o merge e o push na `master`. Falta a conferência com uma pergunta real de agente.
  [PLN-007: os tokens da marca e o aviso de pergunta azul](../../work/worklogs/2026-11-02-pln-007-os-tokens-da-marca.md)

## Documentação

- [`resources/brand/README.md`](https://github.com/brz-anderson/brza-studio/blob/master/resources/brand/README.md), no
  `brza-studio`: a construção do símbolo, as cores, o que se gera de quê e o comando.
- O papel `brand` da norma de cor do `brza-studio`, em `docs/styleguide/color.md`, e a exceção em `docs/STYLEGUIDE.md:5`.
- O README do `brza-studio` e o do `brza-workspace` levam o lockup BrzA.

## Pendências conhecidas

- [O .ico do app sai com 6 quadros, sem o de 24 px](../../work/issues/o-ico-do-app-sai-com-6-quadros-sem-o-24px.md).
- [Os testes e2e de SQLite falham na master do brza-studio](../../work/issues/os-testes-e2e-de-sqlite-falham-na-master-do-brza-studio.md).
- [Os restos da Orca à vista no BrzA Studio](../../work/issues/os-restos-da-orca-a-vista-no-brza-studio.md), agora com a
  cauda do `icon.json` e os nomes `orca-*`.
- [O brza sessions abre na conta ativa do app](../../work/issues/o-brza-sessions-abre-na-conta-ativa-do-app.md).
- **Os casos manuais C1 a C8, no app**, com Anderson, no DMG final.
- **O push do commit `6d47623` e da tag `v1.4.246-alpha.1`** ao origin do `brza-studio`, que espera a conferência de Anderson.

## Casos manuais

| ID  | Critério | Passos | Esperado | Observado | Veredito |
| :-- | :------- | :----- | :------- | :-------- | :------- |
| C1  | R6.1: o fio e o halo no foco, sem corte do `[contain:paint]` | Focar o composer no tema escuro e no claro; anexar uma imagem com o foco | Fio de 1 px no degradê, halo de 3 px visível fora da borda e sem corte; nada se desloca ao focar | Pelo `fixtures:shot` ([PNG](PLN-007-casos-c1-c4-c6.png)): o composer real em repouso (1 px cinza) e em foco (fio em degradê âmbar a laranja, halo de 3 px, fundo branco no claro e grafite no escuro); num chat de esquema oposto ao do app, o fundo acompanha o chat. O composer não mudou de tamanho entre os dois estados. | visto no componente real; o foco de teclado e o corte do `[contain:paint]` com anexo seguem pendentes no app |
| C2  | R6.2: o botão de enviar no degradê só no foco | Com foco e texto; sem foco; com o agente rodando ("parar"); com o composer vazio | Degradê só com foco e o enviar habilitado; "parar" `secondary`; desabilitado como hoje | Pelo `fixtures:shot` ([PNG](PLN-007-casos-c1-c4-c6.png)): o enviar é preto/branco em repouso e laranja com a seta branca no foco; o teste novo afirma que o `data-brza-send` não existe no "parar". | visto no componente real; "parar" e desabilitado no app seguem pendentes |
| C3  | R2.6/H1: a chama do M5 não cobre a transcrição | Rolar a transcrição até o topo e parar no meio de uma mensagem | A chama de 13 px no canto não cobre texto legível | Não verificável por PNG: a chama de 13 px sobre a transcrição rolando pede o app. | pendente no app |
| C4  | R6.4: a chama colorida só no painel com foco | Três chats lado a lado; trocar o foco do do meio para o da direita | Só o painel com foco tem a chama no degradê; a cor acompanha a troca | Pelo `fixtures:shot` ([PNG](PLN-007-casos-c1-c4-c6.png)): o cabeçalho do painel com foco tem a chama em degradê, e sem foco, cinza apagada; sem título. | visto no componente real; a troca de foco entre três painéis segue pendente no app |
| C5  | R5.1: o ícone no Dock e no Finder, na grade da Apple | Instalar o build do P4; ver o Dock, o Cmd-Tab e o Finder | Sem caixa cinza; do tamanho dos ícones vizinhos | Pelo `brza shot` ([PNG](PLN-007-casos-c5-c7-c8.png)): a fatia de 1024 do `.icns` gerado, com o selo, ao lado de vizinhos de mentira na grade da Apple, sem caixa cinza e com o tile do mesmo tamanho; a de 64, sem selo. Sem faíscas. | visto no artboard; o Dock, o Cmd-Tab e o Finder seguem pendentes no app |
| C6  | R2.6: o M2 parado com movimento reduzido | Ativar "Reduzir movimento" no macOS; mandar um prompt | A chama parada no degradê e o rótulo sem brilho, na cor de hoje | Não verificável por PNG: o `prefers-reduced-motion` e o flicker são movimento. | pendente no app |
| C7  | R5.2: o `logo.svg` colorido a 16 px na barra de título | No Windows ou no Linux, com barra de título própria, nos dois temas | O A1 com o tile lê como a marca, sem `invert` | Pelo `brza shot` ([PNG](PLN-007-casos-c5-c7-c8.png)): o `logo.svg` colorido a 14, 16, 28 e 80 px, nos dois temas, sem `invert`; a 16 px lê como o tile com a chama. | visto no artboard; a barra de título do Windows ou do Linux segue pendente |
| C8  | R3.4: o tray do S1 | Barra de menus clara e escura; o app de dev; um aviso de atenção | Template monocromático que segue o tema; o carimbo de dev e o de atenção aparecem | Pelo `brza shot` ([PNG](PLN-007-casos-c5-c7-c8.png)): o `orca-menu-barTemplate` e o `@2x` em menu claro e escuro (o tinge do macOS simulado por `invert`); a chama S1 em preto lê nos dois. | visto no artboard; o tray de verdade, o carimbo de dev e o aviso de atenção seguem pendentes no app |

## Fechamento

- [x] Todo passo `[x]` com evidência, ou `[-]` com motivo.
- [x] Todo achado com destino que existe.
- [x] Um resumo por commit do `brza-studio` da entrega, com o link do plano: os achados e o destino de cada um. O P4, o
      P5 e o P6 levam o corpo; o P3 (`41bfe6d1d4e`), feito noutra sessão, não leva o link do plano, e a `master` não se reescreve.
- [x] O durável saiu para a casa dona e está em `## Documentação`: o `resources/brand/README.md` e o papel `brand` da
      norma de cor do `brza-studio`.
- [ ] `status: done`, `phase: closed` e `completed` no frontmatter.
