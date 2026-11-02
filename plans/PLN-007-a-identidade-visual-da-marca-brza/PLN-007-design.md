# PLN-007 — Desenho

Do plano [PLN-007: A marca BrzA tem símbolo, logotipo e derivadas a partir da chama do app](PLN-007-plan.md).

## Desenho

### O que este desenho assume

- **R1.2 / R2.2:** guarda-chuva BrzA, monolítico: um símbolo, e a filha (STUDIO, CLI, WORKSPACE) como palavra ao lado.
- **R2.1:** o símbolo é a ilustração do ícone de hoje, com o `}` solto refeito inteiro a partir do `}` do par.
- **R2.3 / R2.4:** a sessão desenha o SVG à mão, com construção geométrica, conferido a 16, 32 e 128 px; a referência é
  o próprio ícone.
- **R2.5:** E2, a borda da logo só no foco do composer.
- **R2.6:** M1, M2, M3 e M5 no chat; o M4 fica fora.
- **R3.1:** L2, o arranjo do selo do `.icns` na Geist; o "ADE" só no ícone.
- **R3.2:** P1, a paleta do ícone, com o `--agent-question` em azul.
- **R3.3:** S1, o traço mono de hoje com o `}` corrigido, para o glifo do chat, o M2 e o M5.
- **R3.4:** a marca entra no app desktop, no CLI e nos READMEs; o mobile e os restos da Orca vão à issue.
- **R4.1:** a fonte da marca mora em `brza-studio/resources/brand/`, e os scripts em `config/scripts/`.
- **R4.2:** a sessão do `brand` desenha o símbolo e os lockups; a sessão do `brza-studio` copia e aplica.
- **R4.3:** o `generate.sh` renderiza do SVG com `rsvg-convert` e `iconutil`, sem o `actool`; o `icon.json` sai do
  caminho do ícone, e a cauda da Orca vai à issue.
- **R4.4:** seis passos e três branches no `brza-studio` — tokens, assets, chat —, com os tokens junto do desenho do
  símbolo e o CLI e os READMEs por último.
- **R5.1:** T1, o tile na grade da Apple, 824 px em (100, 100), raio 185.
- **R5.2:** G2, o `resources/logo.svg` é o A1 colorido, com o tile; os 5 usos perdem o `invert` e o `opacity`.
- **R5.3:** V2, o estado vazio usa o S1 no degradê, sem o tile.
- **R5.4:** o logotipo dentro do app é texto vivo na Geist, o `BrzaWordmark`.
- **R6.1:** W1, o fio de 1 px nos dois estados, com o halo de 3 px a 10% no foco.
- **R6.2:** K2, o botão de enviar no degradê da marca com o composer em foco.
- **R6.3:** N1, o anel de âmbar a laranja até 89%, e o vermelho de alerta de hoje de 90% para cima.
- **R6.4:** H1, a chama do cabeçalho apagada sem foco e no degradê só no painel com foco.
- **R7.1:** o `--agent-question` é `--color-blue-700` no claro e `--color-blue-400` no escuro.
- **R7.2:** o `brza --help` troca o nome na impressão, num arquivo do fork.
- **R8.1:** o estado vazio mantém o título com o nome do agente e o subtítulo de hoje.
- **R8.2:** o passo do CLI e dos READMEs abre de novo a `feat/pln-007-brand-assets` a partir da `master`, depois do chat.

### Terreno

> Conferido em `brza-studio@a70f63b6a92` (o sync do v1.4.246), em 2026-11-02; o inventário de 2026-10-31 está no
> scratch da sessão (`/private/tmp/pln-007/inventario-marca.md`).

#### O ícone e o pipeline

- **O app empacotado só usa o `.icns`.** O `Info.plist` do app instalado tem `CFBundleIconFile icon.icns` e nenhum
  `CFBundleIconName`, e `Contents/Resources` não tem `Assets.car` [F42 · rodado · 95]; o builder aponta para
  `resources/build/icon.icns` (`config/electron-builder.config.cjs:609,692`) [F43 · lido · 95].
- **O `generate.sh` compila o `icon.icon` com o `actool`** (`resources/icon-source/generate.sh:25-31`), apara com o
  `magick` os quatro slots pequenos (`:44-62`), extrai o `build/icon.png` e o `resources/icon.png` com o `sips`
  (`:67-71`) e gera o `.ico` pelo `trim-windows-icon-source.mjs` (`:76`) [F44 · lido · 95]. O `package.json:169` o roda
  como `build:icons` [F45 · lido · 95].
- **O `.icns` de hoje tem duas artes:** tile e chama nos slots de 16 a 64; tile, chama e o selo "BrzA STUDIO ADE" de
  128 para cima [F46 · lido · 90].
- **O tile de hoje ocupa 914×952 em +55+36** no canvas de 1024 do `build/icon.png` [F47 · rodado · 90]; o fio da borda
  tem de 4 a 6 px a 1024 [F48 · rodado · 85] — premissa: amostra de pixel numa linha e numa coluna.
- **O ícone do app** é o `resources/icon.png` (classic, ou o `icon-dev.png` fora do pacote), e o watercolor e o blue são
  `resources/app-icons/orca-{watercolor,blue}.png` (`src/main/app-icon.ts:8-25`) [F49 · lido · 95]. O tray importa
  os dois PNG de template (`src/main/tray/system-tray.ts:2-3`) e carimba o selo de dev por código (`:9`)
  [F50 · lido · 95].
- **O upstream mexe no `brza-studio` toda semana**: 3 merges de 2026-10-24 a 2026-10-27 [F51 · rodado · 95]. Código só
  do fork mora em pastas `brza/` (`components/native-chat/brza/`, `shared/native-chat/tools/brza/`,
  `main/native-chat/brza/`) [F52 · rodado · 95].

#### O vetor e a fonte

- **O traço mono tem 13 subpaths, só com `M`, `C`, `L` e `Z`, em `fill-rule="evenodd"`**; o `}` solto partido são os
  subpaths 6 (x 9,03–10,11, y 16,68–18,43) e 4 (x 9,04–9,63, y 18,83–19,56), e o `}` do par é o 3 (x 13,57–14,46,
  y 17,05–19,57) (`resources/brza-flame-mono.svg`) [F53 · rodado · 95].
- **O `}` refeito rodou como sonda:** o subpath 3 escalado por 1,143 e posto em x=9,06, y=16,68 troca os subpaths 4 e
  6; o SVG fica com 12 subpaths e 7 078 bytes, e a 128 px o `}` lê inteiro
  (`/private/tmp/pln-007/desenho-sondas/brza-flame-mono-fix.svg`) [F54 · rodado · 95].
- **Ferramentas:** há `rsvg-convert`, `magick`, `iconutil`, `sips`, `swift` e `node`; não há `inkscape`, `potrace`,
  `vtracer`, `svgo`, `fontTools` nem o `brotli` do Python [F55 · rodado · 95].
- **O `opentype.js` 2.0.0 do `node_modules` recusa o woff2** ("WOFF2 require an external decompressor library"), e o
  `hb-view` não carrega a fonte [F56 · rodado · 95].
- **O CoreText lê o `Geist-Variable.woff2` e aplica o eixo `wght`:** pelo `swift`, "BrzA" a 100 pt mede 246,9 de avanço
  em `wght=750` e 226,4 em `wght=400` [F57 · rodado · 95].
- **As medidas do L2 aprovado:** horizontal com símbolo de 34 px, "BrzA" a 21 px peso 750 com `letter-spacing:-.2px`,
  a filha a 16 px peso 500 com `.14em` e opacidade `.75`, vão de 9 px; vertical com símbolo de 56 px e vão de 6 px
  (`/private/tmp/pln-007/r3-l2.html`) [F58 · lido · 95].

#### Cor e tokens

- **O `--agent-question` é laranja:** claro `--color-orange-600` e `--agent-question-text` `--color-orange-700`
  (`src/renderer/src/assets/main.css:253,257`); escuro `--color-orange-500` e `--color-orange-300` (`:372-373`);
  expostos em `@theme inline` (`:97-99`) [F59 · lido · 95].
- **O app já usa azul por tema:** `--terminal-pane-locate` é `--color-blue-600` no claro e `--color-blue-400` no escuro
  (`main.css:250,370`) [F60 · lido · 95].
- **Contraste medido:** `#1447e6` dá 6,8:1 no branco e 2,9:1 no `#0a0a0a`; `#C2410C` 5,2:1 no branco; `#FFAA44` 10,5:1
  no `#0a0a0a`; `#F26228` 3,2:1 no branco [F61 · rodado · 90].
- **A norma do app diz que a identidade é monocromática e a cor é do estado** (`docs/STYLEGUIDE.md:5`); token novo vai
  em `:root` e `.dark` e é exposto em `@theme inline` (`:24`) [F62 · lido · 95]. A nota dos logos do chat diz que a
  chama mono nunca é a marca do próprio app (`components/native-chat/brza/brza-brand-logos.md:6`) [F63 · lido · 95].

#### O chat

- **O composer tem borda de largura constante**, "Use a constant container border so focus changes cannot flash it",
  com `rounded-xl border border-chat-composer-border p-1.5 shadow-xs bg-chat-composer-surface [contain:paint]`
  (`NativeChatComposerField.tsx:312-318`) [F64 · lido · 95].
- **O botão de enviar é redondo**, `variant={stops ? 'secondary' : 'default'}`, `size-8 rounded-full`
  (`NativeChatComposerActions.tsx:143-145`) [F65 · lido · 95].
- **O "agente trabalhando" é o `NativeChatTurnActivityLine`:** um `LoadingSpinner` `size-4` e o rótulo em
  `text-chat-foreground` (`NativeChatTurnActivityLine.tsx:61-64`), montado quando há `liveLine`
  (`NativeChatMessageList.tsx:386`) [F66 · lido · 95]. O teste
  `NativeChatMessageList.turn-indicator.test.tsx:115,160` afirma o `size-4`, o `animate-spin` e o `motion-reduce:hidden`
  do spinner [F67 · lido · 95].
- **O `LoadingSpinner` troca o giro por uma ampulheta com `prefers-reduced-motion`** (`LoadingSpinner.tsx:6-10`)
  [F68 · lido · 95].
- **O estado vazio** é um círculo `size-12 bg-accent` com o `MessageSquare` (`NativeChatEmptyState.tsx:25-37`), e o
  título "Start a chat with {agente}" (`shared/native-chat-empty-state.ts:10-13`) [F69 · lido · 95].
- **O anel de contexto** tem 16 px, traço 2 e `stroke="currentColor"`, e de 90% para cima vira `text-destructive`
  (`NativeChatContextUsageRing.tsx:11-16,122,144,153`); fica dentro do composer (`NativeChatComposerActions.tsx:155`)
  [F70 · lido · 90].
- **O cabeçalho do painel do chat não tem título:** é a `pane-title-bar` em `data-chromeless`, transparente e sem
  `pointer-events`, só com as ações à direita, e marca o painel com foco por `data-active-pane`
  (`NativeChatPaneHeader.tsx:44-52`; `assets/terminal.css:349-353`) [F71 · lido · 95].
- **O chat proíbe tamanho arbitrário de fonte e pede utilitário de espaçamento**, que escala com o tamanho do texto
  (`docs/styleguide/native-chat.md`; 3 regras em `config/ast-grep/rules/native-chat-*.yml`) [F72 · lido · 95].

#### O desktop, o CLI e os READMEs

- **Os 5 usos do `resources/logo.svg` o tratam como glifo branco:** barra de título 16 px com `opacity: 0.75` e
  `invert(1)` no claro (`main.css:1117-1127`, `TitlebarLeftControls.tsx:45`); Landing num tile `#12181e` de `size-20`
  com a imagem `size-12` (`Landing.tsx:260-267`); Onboarding `h-7 w-auto shrink-0 invert dark:invert-0`
  (`OnboardingFlow.tsx:235`); menu de ajuda `size-3.5 object-contain invert opacity-55 dark:invert-0`
  (`SidebarSettingsHelpMenu.tsx:266`); ícone de Configurações `object-contain invert dark:invert-0`
  (`orca-logo-settings-icon.tsx:11`) [F73 · lido · 95].
- **O `brza --help` imprime 95 linhas com "orca"**; fora o cabeçalho e o `Usage`, são exemplos de comando e
  identificadores que ficam (`orca://pair`, `ORCA_PAIRING_CODE`) [F74 · rodado · 95]. O `help.ts` imprime o texto raiz
  em `:29`, o de comando em `:14` e o de grupo em `:19`, e monta `orca ${…}` em `:33,67,78` [F75 · lido · 95]. Testes do
  CLI afirmam "Usage: orca …" em mensagens de erro dos handlers (`src/cli/skills.test.ts:189`,
  `src/cli/handlers/core.test.ts:199`) [F76 · lido · 95].
- **Os dois repositórios são públicos**, e o `raw.githubusercontent.com` serve SVG como `image/svg+xml`
  [F77 · rodado · 95]. O `README.md` do workspace não está no `.brza/core.lock` (`.brza/core.lock:29-34`)
  [F78 · lido · 95].

### D1 — O símbolo mestre e as variantes — `brza-studio/resources/brand/`

- **Origem:** R2.1, R2.3, R2.4, R4.1, R4.2, R5.1, R5.2
- **Contexto:** não há vetor da ilustração; o ícone, o `logo.svg`, a Landing e os lockups precisam de uma fonte só, que
  o upstream não toque.
- **Protótipo:** [o `}` refeito](PLN-007-simbolo-a1-chave.png) · [o tile na grade da Apple](PLN-007-tile-t1.png)

#### Como fica

```text
resources/brand/
  README.md                    # a construção, as cores, o que se gera de quê e o comando
  brza-symbol.svg              # mestre: tile grafite + chama, sem selo
  brza-symbol-light.svg        # Light Flame: o mestre com o tile claro
  brza-symbol-dev.svg          # o mestre com o selo azul "D"
  brza-app-icon.svg            # o mestre com o selo "BrzA STUDIO ADE" em paths
  brza-symbol-mono.svg         # S1 (D2), em currentColor
  brza-tray-template.svg       # S1 em preto, no canvas 22×14 do tray
  brza-*-lockup-*.svg          # D3
config/scripts/
  brza-brand-build.mjs         # gera as variantes, os lockups e o resources/logo.svg a partir do mestre
  brza-brand-text.swift        # texto da Geist em path (D3)
```

O mestre, `brza-symbol.svg`, com o tile na grade da Apple (R5.1):

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
  <title>BrzA</title>
  <defs>
    <linearGradient id="brza-fire" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFAA44"/><stop offset=".30" stop-color="#F4902A"/>
      <stop offset=".65" stop-color="#F26228"/><stop offset="1" stop-color="#E04A2B"/>
    </linearGradient>
    <linearGradient id="brza-tile-dark" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#373A41"/><stop offset=".6" stop-color="#2C2D32"/><stop offset="1" stop-color="#19161D"/>
    </linearGradient>
    <linearGradient id="brza-tile-light" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#F6F6F8"/>
    </linearGradient>
    <rect id="brza-tile-shape" x="100" y="100" width="824" height="824" rx="185"/>
    <clipPath id="brza-tile-clip"><use href="#brza-tile-shape"/></clipPath>
    <!-- o } desenhado uma vez: dois arcos de 90° e o bico do meio, em traço de largura fixa convertido em contorno -->
    <path id="brza-brace-close" d="…"/>
  </defs>

  <g id="tile">
    <use href="#brza-tile-shape" fill="url(#brza-tile-dark)"/>
    <g clip-path="url(#brza-tile-clip)">   <!-- o fio e o brilho ficam dentro: o tile segue com 824 px exatos -->
      <use href="#brza-tile-shape" fill="none" stroke="url(#brza-fire)" stroke-width="24"/>  <!-- 12 visíveis: 1,5 px a 128 -->
      <use href="#brza-tile-shape" fill="none" stroke="#FFFFFF" stroke-opacity=".07" stroke-width="8"
           transform="translate(0 12)"/>                                                     <!-- brilho interno, em cima -->
    </g>
  </g>

  <g id="flame" transform="translate(…) scale(…)">   <!-- na grade de 24 do mono -->
    <path id="flame-body"   fill="url(#brza-fire)" d="…"/>                  <!-- contorno externo do subpath 0 -->
    <path id="flame-tongue" fill="#FFAA44" fill-opacity=".55" d="…"/>       <!-- a língua clara do meio -->
    <path id="flame-base-l" fill="url(#brza-fire)" d="…"/>                  <!-- subpath 1 -->
    <path id="flame-base-r" fill="url(#brza-fire)" d="…"/>                  <!-- subpath 2 -->
    <path id="flame-arm"    fill="url(#brza-fire)" d="…"/>                  <!-- subpath 9 -->

    <g id="graph" fill="none" stroke="url(#brza-fire)" stroke-linecap="round">
      <path id="graph-trunk" d="M12 22.1V16.1"/>
      <path id="graph-branch-l" d="…"/> <path id="graph-branch-r" d="…"/>
      <g id="graph-nodes" fill="url(#brza-fire)" stroke="none">
        <circle cx="12" cy="22.1" r=".95"/> <circle cx="12" cy="16.1" r=".95"/> <circle cx="11.4" cy="8.5" r=".75"/> …
      </g>
    </g>

    <g id="glyphs" fill="url(#brza-fire)">
      <path id="prompt" d="…"/>                                                               <!-- >_ : subpaths 11 e 10 -->
      <use id="brace-open"  href="#brza-brace-close" transform="translate(…) scale(-1 1)"/>  <!-- { é o } espelhado -->
      <use id="brace-close" href="#brza-brace-close" transform="translate(…)"/>
      <use id="brace-solo"  href="#brza-brace-close" transform="translate(…) scale(1.143)"/> <!-- o } solto -->
    </g>

    <g id="sparks" fill="url(#brza-fire)">
      <rect x="…" y="…" width="…" height="…" transform="rotate(-35 …)"/> …
    </g>
  </g>
</svg>
```

- **A construção:** o esqueleto vem do traço mono, já registrado sobre o raster, na grade de 24 escalada para o tile de
  824; as camadas de cor (a língua clara, as faíscas) se desenham sobre o `build/icon.png` posto como decalque num
  artboard do scratch, que não vai ao arquivo final. O grafo é traço com `stroke-linecap="round"` e nós em `<circle>`.
- **O `}`** é um desenho só, `#brza-brace-close`, usado três vezes; o solto é o mesmo `}` na escala 1,143, a razão da
  altura do solto (2,88) pela do par (2,52).
- **As variantes saem do mestre pelo `brza-brand-build.mjs`**, que troca só o que muda:

  | Arquivo | O que muda |
  | :------ | :--------- |
  | `brza-symbol-light.svg` | `url(#brza-tile-dark)` → `url(#brza-tile-light)` |
  | `brza-symbol-dev.svg` | mais um `<g id="dev-badge">`: círculo `#1447e6` de r=150 em (800, 800) com o "D" da Geist 700 em path branco |
  | `brza-app-icon.svg` | `#flame` subido e reduzido, e o `<g id="seal">` do D3 com "BrzA STUDIO" e "ADE" em paths, no arranjo do `build/icon.png` de hoje |
  | `brza-tray-template.svg` | o S1 (D2) em `fill="#000"`, `viewBox` 22×14, a chama de 14 de altura centrada |
  | `resources/logo.svg` | cópia do `brza-symbol.svg` (R5.2): o A1 colorido com o tile, a arte sem selo dos slots pequenos |

- **A conferência** (R2.3): `brza shot` de um artboard com o mestre a 16, 32, 128 e 1024 px nos dois temas; o `.icns`
  gerado, no Finder e no Dock.

### D2 — O corte pequeno S1 — `brza-studio/resources/brza-flame-mono.svg`

- **Origem:** R3.3
- **Contexto:** o `}` solto do mono sai partido em dois subpaths; a correção rodou como sonda.
- **Protótipo:** [o corte pequeno](PLN-007-corte-pequeno-s1.png)

#### Como fica

O `d` perde os subpaths 4 e 6 e ganha, no fim, o `}` do par escalado:

```diff
-M9.04 18.83 … Z          (subpath 4: a metade de baixo)
-M9.03 16.68 … Z          (subpath 6: a metade de cima)
+M9.10 19.53C9.06 19.48 9.06 19.35 9.10 19.31C9.11 19.29 9.16 19.25 9.21 19.24C9.38 19.18 9.40 19.11 9.40 18.71C9.42 18.44 9.44 18.34 9.56 18.22L9.67 18.12L9.58 18.03C9.44 17.91 9.43 17.86 9.42 17.49C9.39 17.09 9.37 17.05 9.15 17.00C9.10 16.99 9.10 16.98 9.10 16.85C9.10 16.69 9.11 16.68 9.28 16.71C9.64 16.77 9.72 16.89 9.75 17.42C9.77 17.85 9.78 17.87 9.95 17.96L10.08 18.02L10.07 18.13C10.06 18.25 10.04 18.26 9.92 18.30C9.80 18.34 9.77 18.43 9.75 18.82C9.72 19.26 9.68 19.39 9.50 19.47C9.35 19.54 9.14 19.56 9.10 19.53Z
```

- **O mesmo `d` vai a três arquivos:** `resources/brza-flame-mono.svg`, o `BrzaFlameLogo.tsx`, que repete o `d`, e o
  `resources/brand/brza-symbol-mono.svg`.
- **A nota `brza-brand-logos.md:6`** troca "never as BrzA Studio's own mark" por "the small cut of the BrzA mark
  (PLN-007, S1), drawn monochrome in the tool row".

### D3 — Os lockups L2 e o texto em paths — `brza-studio/resources/brand/`

- **Origem:** R3.1, R2.2, R4.2, R5.4
- **Contexto:** o L2 precisa do texto em path para valer no README; o `opentype.js` e o `hb-view` não leem o woff2, e o
  CoreText lê, com o peso variável.
- **Protótipo:** [o logotipo L2](PLN-007-logotipo-l2.png)

#### Como fica

**O texto vira path pelo CoreText**, no `config/scripts/brza-brand-text.swift`, sem instalar nada (o `swift` vem com o
Xcode):

```text
swift config/scripts/brza-brand-text.swift <woff2> <wght> <tracking-em> <texto>   →  JSON {advance, capHeight, d}
```

- Monta um `CTLine` com `kCTFontVariationAttribute` (`wght`) e `kCTKernAttributeName` (o tracking), para o kerning do
  GPOS valer; percorre os `CTRun` e grava o `CTFontCreatePathForGlyph` de cada glifo na posição do run, com y invertido
  e 2 casas decimais.
- O `brza-brand-build.mjs` chama o script uma vez por texto — "BrzA" peso 750; "STUDIO", "CLI", "WORKSPACE" e "ADE"
  peso 500 com `.14em` — e monta os lockups. Os SVG gerados vão ao git; o script só roda de novo quando o texto ou a
  fonte mudam.

**A geometria**, com H = a altura do símbolo, pelas medidas do L2:

| Medida                      | Horizontal                                                         | Vertical                           |
| :-------------------------- | :----------------------------------------------------------------- | :--------------------------------- |
| Símbolo                     | H                                                                  | H                                  |
| "BrzA" (Geist 750, −0,01em) | corpo 0,62H; o meio da altura de caixa alta no meio do símbolo     | corpo 0,375H, centrado, vão 0,11H  |
| Filha (Geist 500, +0,14em)  | corpo 0,47H, mesma linha de base, a 0,5em do "BrzA"                | corpo 0,29H, centrada, vão 0,11H   |
| Vão símbolo–texto           | 0,265H                                                             | —                                  |
| "A" de "BrzA"               | `url(#brza-fire)`                                                  | `url(#brza-fire)`                  |

**As cores por tema** — o SVG num `<img>` não herda `currentColor`, então cada tema é um arquivo:

| Tema   | Símbolo                  | "Brz"     | Filha (a opacidade `.75` do L2, chapada) |
| :----- | :----------------------- | :-------- | :--------------------------------------- |
| escuro | `brza-symbol.svg`        | `#FAFAFA` | `#BCBCBC`                                |
| claro  | `brza-symbol-light.svg`  | `#0A0A0A` | `#474747`                                |

**Os arquivos:** `brza-lockup-{horizontal,vertical}-{dark,light}.svg`, só "BrzA", e
`brza-{studio,cli,workspace}-lockup-{horizontal,vertical}-{dark,light}.svg` — 16 ao todo. O "ADE" só entra no
`brza-app-icon.svg` (D1).

**Dentro do app, o logotipo é texto vivo** (R5.4), em `src/renderer/src/components/brza/BrzaWordmark.tsx`:

```tsx
export function BrzaWordmark({
  daughter,
  layout = 'horizontal',
  className
}: {
  daughter?: 'Studio' | 'CLI' | 'Workspace'
  layout?: 'horizontal' | 'vertical'
  className?: string
}): React.JSX.Element {
  return (
    <span
      className={cn('brza-wordmark', layout === 'vertical' && 'brza-wordmark--vertical', className)}
      aria-label={daughter ? `BrzA ${daughter}` : 'BrzA'}
    >
      <span aria-hidden="true" className="brza-wordmark-mother">
        Brz<span className="brza-wordmark-a">A</span>
      </span>
      {daughter ? (
        <span aria-hidden="true" className="brza-wordmark-daughter">
          {daughter}
        </span>
      ) : null}
    </span>
  )
}
```

```css
/* PLN-007 L2: the BrzA lockup as live Geist text. */
.brza-wordmark { display: inline-flex; align-items: baseline; gap: 0.5em; }
.brza-wordmark--vertical { flex-direction: column; align-items: center; gap: 0.15em; }
.brza-wordmark-mother { font-weight: 750; letter-spacing: -0.01em; }
.brza-wordmark-a { background: var(--brand-gradient); -webkit-background-clip: text; background-clip: text; color: transparent; }
.brza-wordmark-daughter { font-size: 0.76em; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase; opacity: 0.75; }
```

### D4 — Os tokens P1 e o `--agent-question` azul — `brza-studio/src/renderer/src/assets/main.css`

- **Origem:** R3.2, R7.1
- **Contexto:** não há token de marca; o laranja do `--agent-question` colide com a borda do E2 e com o anel do M3; a
  norma do app guarda a cor para o estado.
- **Protótipo:** [a paleta P1](PLN-007-paleta-p1.png)

#### Como fica

```css
:root {
  /* PLN-007: the BrzA mark. Constant across themes; only for the mark and the chat's brand moments. */
  --brand-amber: #ffaa44;
  --brand-orange: #f26228;
  --brand-ember: #e04a2b;
  --brand-graphite: #2c2d32;
  --brand-gradient: linear-gradient(180deg, #ffaa44 0%, #f4902a 30%, #f26228 65%, #e04a2b 100%);
  /* Per theme: the brand colour that passes text contrast. */
  --brand-text: #c2410c;
  --brand-sheen: #c2410c;
  --chat-composer-focus-fill: linear-gradient(var(--chat-composer-surface), var(--chat-composer-surface));
  --chat-composer-focus-glow: 0 0 0 3px color-mix(in srgb, var(--brand-orange) 10%, transparent);

-  --agent-question: var(--color-orange-600);
+  --agent-question: var(--color-blue-700);
-  --agent-question-text: var(--color-orange-700);
+  --agent-question-text: var(--color-blue-800);
}

.dark {
  --brand-text: #ffaa44;
  --brand-sheen: #ffaa44;
  --chat-composer-focus-fill: linear-gradient(180deg, #373a41 0%, #2c2d32 60%, #25252b 100%);
  --chat-composer-focus-glow: inset 0 1px 0 rgb(255 255 255 / 0.07), 0 0 0 3px color-mix(in srgb, var(--brand-orange) 10%, transparent);

-  --agent-question: var(--color-orange-500);
+  --agent-question: var(--color-blue-400);
-  --agent-question-text: var(--color-orange-300);
+  --agent-question-text: var(--color-blue-300);
}

@theme inline {
  --color-brand-amber: var(--brand-amber);
  --color-brand-orange: var(--brand-orange);
  --color-brand-ember: var(--brand-ember);
  --color-brand-graphite: var(--brand-graphite);
  --color-brand-text: var(--brand-text);
}
```

- **As constantes da marca ficam só em `:root`**, que também vale com `.dark` na raiz; o comentário diz por quê, já que
  a norma do app pede os dois blocos.
- **O `--agent-working` amarelo fica como está**: é o estado de trabalho dos glifos fora do chat.
- **A norma do app ganha o papel `brand`** em `docs/styleguide/color.md`, na tabela de papéis: "`brand-*` — the BrzA
  mark and the chat's brand moments (composer focus rim and send button, empty state, working flame, context ring,
  pane flame). Never for state, actions or warnings." O `docs/STYLEGUIDE.md:5` ganha uma frase que aponta a exceção.

### D5 — E2, a borda e o botão no foco — `NativeChatComposerField.tsx:312-318`, `NativeChatComposerActions.tsx:143-145` e `main.css`

- **Origem:** R2.5, R6.1, R6.2
- **Contexto:** a borda tem largura constante de propósito; o botão de enviar é o `primary`, redondo, de 32 px.
- **Protótipo:** [a borda no foco](PLN-007-borda-do-chat-e2.png) · [o fio de 1 px](PLN-007-borda-fio-w1.png) ·
  [o botão no degradê](PLN-007-botao-k2.png)

#### Como fica

```diff
             className={cn(
               // Use a constant container border so focus changes cannot flash it.
               'rounded-xl border border-chat-composer-border p-1.5 shadow-xs',
               'bg-chat-composer-surface',
+              'brza-composer-focus',
               // Contain caret-blink repaint to the composer; keep 4px slack around overhanging attachment buttons, while menus use portals.
               '[contain:paint]'
             )}
```

```diff
       variant={stops ? 'secondary' : 'default'}
       size="icon"
       className="size-8 rounded-full pointer-coarse:size-10"
+      data-brza-send={stops ? undefined : ''}
     >
```

```css
/* PLN-007 E2: the brand rim on focus; the 1px width stays, so focus never shifts the layout. */
.brza-composer-focus:focus-within {
  border-color: transparent;
  background: var(--chat-composer-focus-fill) padding-box, var(--brand-gradient) border-box;
  box-shadow: var(--chat-composer-focus-glow);
}
/* PLN-007 K2: the send button takes the brand gradient while the composer has focus. */
.brza-composer-focus:focus-within [data-brza-send]:not(:disabled) {
  background: var(--brand-gradient);
  color: #fff;
}
```

- O fio fica em 1 px nos dois estados, e o peso a mais no foco vem do halo de 3 px a 10% (W1).
- O botão em "parar" segue no `secondary`, e o desabilitado segue como está; só o enviar habilitado ganha o degradê
  (K2), com a seta branca a 3,2:1 sobre o laranja.

### D6 — A marca no chat: M1, M2, M3 e M5 — `components/native-chat/`

- **Origem:** R2.6, R5.3, R5.4, R6.3, R6.4
- **Contexto:** os riscos do M3 (o laranja perto do composer em foco e do aviso de pergunta) e do M5 (ruído com vários
  chats) vieram da R2.6; a P1 e a N1 fecham o do M3, e a H1 o do M5.
- **Protótipo:** [M1](PLN-007-marca-no-chat-m1.png) · [o S1 no estado vazio](PLN-007-estado-vazio-v2.png) ·
  [M2](PLN-007-marca-no-chat-m2.png) · [o anel N1](PLN-007-anel-n1.png) · [a chama H1](PLN-007-cabecalho-h1.png)

#### O glifo comum

O S1 vira máscara sobre o degradê, sem `id` de gradiente por instância, em `main.css`:

```css
/* PLN-007 S1: the small mark as a mask over the brand gradient. */
.brza-flame-glyph {
  background: var(--brand-gradient);
  mask: url('../../../../resources/brza-flame-mono.svg') center / contain no-repeat;
}
```

#### M1 — o estado vazio (`NativeChatEmptyState.tsx:25-37`)

```diff
-      <div className={kind === 'error' ? '…' : 'flex size-12 items-center justify-center rounded-full bg-accent text-accent-foreground'}>
-        {kind === 'error' ? <TriangleAlert className="size-6" /> : <MessageSquare className="size-6" />}
-      </div>
+      {kind === 'empty' ? (
+        <>
+          <span aria-hidden="true" className="brza-flame-glyph size-12" />
+          <BrzaWordmark daughter="Studio" className="text-sm text-chat-foreground-strong" />
+        </>
+      ) : (
+        <div className={…as hoje…}>…</div>
+      )}
```

- O S1 no degradê, sem o tile, a 48 px (V2), e o `BrzaWordmark` em texto vivo (R5.4). O `loading`, o `error` e o
  `not-agent` ficam como estão.
- **O texto abaixo do logotipo no estado vazio** fica o de hoje: o título com o nome do agente e o subtítulo, embaixo
  do símbolo e do `BrzaWordmark` (R8.1; F69). Os artboards do M1 e da V2 mostravam uma linha só, e a linha deles não
  vale.

#### M2 — o agente trabalhando (`NativeChatTurnActivityLine.tsx:61-64`)

```diff
-        <LoadingSpinner className="size-4 shrink-0" />
-        <span id={labelId} className="min-w-0 truncate text-chat-foreground">
+        <span aria-hidden="true" data-brza-working-flame="" className="brza-flame-glyph brza-working-flame size-4.5 shrink-0" />
+        <span id={labelId} className="brza-working-label min-w-0 truncate text-chat-foreground">
```

```css
@keyframes brza-flame-flicker {
  0%, 100% { transform: scale(1, 1) skewX(0deg); }
  30% { transform: scale(0.97, 1.04) skewX(-1.5deg); }
  60% { transform: scale(1.02, 0.97) skewX(1deg); }
}
@keyframes brza-label-sheen { from { background-position: 100% 0; } to { background-position: -100% 0; } }
.brza-working-flame { transform-origin: 50% 90%; animation: brza-flame-flicker 1.4s ease-in-out infinite; }
.brza-working-label {
  background: linear-gradient(90deg, var(--chat-foreground) 0 35%, var(--brand-sheen) 50%, var(--chat-foreground) 65% 100%);
  background-size: 250% 100%;
  -webkit-background-clip: text; background-clip: text; color: transparent;
  animation: brza-label-sheen 2.4s linear infinite;
}
@media (prefers-reduced-motion: reduce) {
  .brza-working-flame { animation: none; }
  .brza-working-label { animation: none; background: none; color: var(--chat-foreground); }
}
```

- `size-4.5` dá os 18 px da R3.3 no texto padrão e escala com ele. Com movimento reduzido, a chama fica parada no
  degradê e o rótulo, na cor de hoje — o mesmo contrato do `LoadingSpinner`.
- A faixa que corre usa o `--brand-sheen`, `#C2410C` no claro e `#FFAA44` no escuro; o resto do rótulo fica na cor de
  hoje.

#### M3 — o anel de contexto (`NativeChatContextUsageRing.tsx:139-158`)

```diff
+  const gradientId = useId()
   …
             <svg … className="-rotate-90">
+              <defs>
+                <linearGradient id={gradientId} gradientUnits="userSpaceOnUse" x1="0" y1="0" x2={RING_SIZE} y2="0">
+                  <stop offset="0" stopColor="var(--brand-amber)" />
+                  <stop offset="1" stopColor="var(--brand-orange)" />
+                </linearGradient>
+              </defs>
               <circle … stroke="currentColor" className="opacity-25" />
               <circle
-                stroke="currentColor"
+                stroke={critical ? 'currentColor' : `url(#${gradientId})`}
```

- Até 89%, o traço vai de âmbar a laranja, sem a brasa; de 90% para cima, segue o `text-destructive` de hoje, chapado
  (N1). O anel cheio vira outro estado, distinto da borda em foco; o aviso de pergunta já é azul (D4).

#### M5 — a chama no cabeçalho do painel (`NativeChatPaneHeader.tsx:44-52`)

```diff
     <div className="pane-title-bar z-20" data-chromeless="" data-active-pane={focused ? '' : undefined} …>
+      <span aria-hidden="true" className="brza-flame-glyph brza-pane-flame size-3.25" />
       <div className="pane-title-actions ml-auto flex shrink-0 items-center gap-0">
```

```css
.brza-pane-flame { margin-left: 6px; background: var(--chat-foreground-faint); }
.pane-title-bar[data-active-pane] .brza-pane-flame { background: var(--brand-gradient); }
```

- No painel sem foco, a chama é mono, na cor apagada do chrome; só o painel com foco a pinta no degradê (H1), e ela diz
  qual chat recebe o teclado. `size-3.25` dá os 13 px da R3.3.

### D7 — A marca no app desktop

- **Origem:** R3.4, R4.3, R5.1, R5.2
- **Contexto:** o `icon.json` aponta para a cauda da Orca; o app empacotado só usa o `.icns`, que tem duas artes; o
  `logo.svg` passa a ser o A1 colorido.
- **Protótipo:** [o A1 na barra de título](PLN-007-logo-svg-g2.png) · [o tile na grade da Apple](PLN-007-tile-t1.png)

#### Como fica

**O `generate.sh` renderiza do SVG, sem o `actool`** (R4.3):

```bash
# resources/icon-source/generate.sh — o corpo novo, depois do cabeçalho
RSVG_BIN=$(command -v rsvg-convert || true)
if [ -z "$RSVG_BIN" ]; then
  echo "Error: rsvg-convert is required to render the BrzA icons." >&2
  echo "Install with: brew install librsvg" >&2
  exit 1
fi
BRAND_DIR="$RESOURCES_DIR/brand"
ICONSET_DIR="$TMP_DIR/icon.iconset"; mkdir -p "$ICONSET_DIR"
render() { "$RSVG_BIN" -w "$2" -h "$3" "$BRAND_DIR/$1" -o "$4"; }

for spec in 16:icon_16x16 32:icon_16x16@2x 32:icon_32x32 64:icon_32x32@2x; do
  render brza-symbol.svg "${spec%%:*}" "${spec%%:*}" "$ICONSET_DIR/${spec#*:}.png"     # tile e chama, sem selo
done
for spec in 128:icon_128x128 256:icon_128x128@2x 256:icon_256x256 512:icon_256x256@2x 512:icon_512x512 1024:icon_512x512@2x; do
  render brza-app-icon.svg "${spec%%:*}" "${spec%%:*}" "$ICONSET_DIR/${spec#*:}.png"   # com o selo
done
iconutil -c icns "$ICONSET_DIR" -o "$BUILD_DIR/icon.icns"
cp "$ICONSET_DIR/icon_512x512@2x.png" "$BUILD_DIR/icon.png"
render brza-symbol.svg        256  256  "$RESOURCES_DIR/icon.png"
render brza-symbol-dev.svg    256  256  "$RESOURCES_DIR/icon-dev.png"
cp "$BUILD_DIR/icon.png"                "$RESOURCES_DIR/app-icons/orca-watercolor.png"
render brza-symbol-light.svg  1024 1024 "$RESOURCES_DIR/app-icons/orca-blue.png"
render brza-tray-template.svg 22   14   "$RESOURCES_DIR/tray/orca-menu-barTemplate.png"
render brza-tray-template.svg 44   28   "$RESOURCES_DIR/tray/orca-menu-barTemplate@2x.png"
node "$PROJECT_DIR/config/scripts/trim-windows-icon-source.mjs"   # o .ico, como hoje
```

- O `magick` deixa de ser exigido, e o `rsvg-convert` passa a ser.
- O `icon.icon` deixa de ser lido e fica intocado; a cauda da Orca para que o `icon.json` aponta vai à
  [issue dos restos da Orca](../../work/issues/os-restos-da-orca-a-vista-no-brza-studio.md), junto dos nomes `orca-*`
  dos arquivos, que ficam porque renomear toca os imports do upstream.

**O `logo.svg` colorido e os seus 5 usos** (R5.2):

| Lugar | Hoje | Fica |
| :---- | :--- | :--- |
| Barra de título Win/Linux (`main.css:1117-1127`) | 16 px, `opacity: 0.75`, `invert(1)` no claro | 16 px, sem o `opacity` e sem a regra do `invert` |
| Landing (`Landing.tsx:260-271`) | tile `#12181e` `size-20` com a imagem `size-12`, h1 "BrzA Studio" | `<img src={logo} className="size-20" alt="BrzA Studio">` sem o tile de hex nem a sombra; o h1 vira `<BrzaWordmark daughter="Studio" className="text-4xl text-foreground" />` |
| Onboarding (`OnboardingFlow.tsx:235-239`) | `h-7 w-auto shrink-0 invert dark:invert-0` + "BrzA Studio" | `size-7 shrink-0` + `<BrzaWordmark daughter="Studio" />` |
| Menu de ajuda (`SidebarSettingsHelpMenu.tsx:266`) | `size-3.5 object-contain invert opacity-55 dark:invert-0` | `size-3.5 object-contain` |
| Configurações (`orca-logo-settings-icon.tsx:11`) | `object-contain invert dark:invert-0` | `object-contain` |

**O tray e o seletor:** o tray recebe os PNG do `generate.sh`, do S1, e o selo de dev segue o `tray-dev-badge`; o
seletor de ícone (`shared/app-icon.ts:1-5`) mantém os rótulos Flame, BrzA Studio ADE e Light Flame, com os PNG novos.

### D8 — O CLI e os READMEs

- **Origem:** R3.4, R7.2
- **Contexto:** o `brza --help` tem 95 linhas com "orca", e o texto do help é o arquivo que o upstream mais edita.

#### Como fica

**A troca na impressão**, num arquivo só do fork, `src/cli/brza/cli-display-name.ts`:

```ts
// The fork ships the same CLI as `brza`; the upstream help text keeps `orca`.
const COMMAND_NAME = /(^|[\s`$(])orca(?=\s|`|$)/gm

export function withBrzaCommandName(text: string): string {
  return text.replace(COMMAND_NAME, '$1brza')
}
```

```diff
-    console.log(formatCommandHelp(exactSpec))
+    console.log(withBrzaCommandName(formatCommandHelp(exactSpec)))
 …
-    console.log(formatGroupHelp(specs, commandPath))
+    console.log(withBrzaCommandName(formatGroupHelp(specs, commandPath)))
 …
-  console.log(ROOT_HELP_TEXT)
+  console.log(withBrzaCommandName(ROOT_HELP_TEXT))
```

- Só nos três `console.log` do `help.ts:14,19,29`: o `formatCommandHelp` e o `formatGroupHelp` seguem devolvendo
  `orca`, e os testes que os afirmam não mudam. As mensagens de erro dos handlers ("Usage: orca …") ficam fora.
- Troca `orca open`, `` `orca terminal list` `` e o cabeçalho; deixa `orca://pair`, `ORCA_PAIRING_CODE` e `orca.yaml`.
- O `root-help-text-primary.ts:2` passa de `'orca'` a `'BrzA CLI'`, a filha do L2 em texto.

**O README do `brza-studio`** (`README.md:1-3,11-12`):

```html
<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="resources/brand/brza-studio-lockup-horizontal-dark.svg" />
    <img src="resources/brand/brza-studio-lockup-horizontal-light.svg" alt="BrzA Studio" height="64" />
  </picture>
</h1>
```

E os badges passam de `F26B1D` a `F26228`, o laranja da P1.

**O README do `brza-workspace`**, na `master`, com o lockup servido do `brza-studio` pelo raw, sem arquivo novo na
`master` do workspace:

```html
<h1>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/brz-anderson/brza-studio/master/resources/brand/brza-workspace-lockup-horizontal-dark.svg" />
    <img src="https://raw.githubusercontent.com/brz-anderson/brza-studio/master/resources/brand/brza-workspace-lockup-horizontal-light.svg" alt="BrzA Workspace" height="48" />
  </picture>
</h1>
```
