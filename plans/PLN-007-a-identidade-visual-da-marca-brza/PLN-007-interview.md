# PLN-007 — Entrevista

Do plano [PLN-007: A marca BrzA tem símbolo, logotipo e derivadas a partir da chama do app](PLN-007-plan.md).

## Entrevista

### Rodada 1 — workstream, alcance e destino (enviada 2026-10-31)

**Apresentado antes**, na sessão do workstream `workspace`:
- O ícone atual veio do rebrand de 2026-10-27, `brza-studio@b2918da` ("New flame icon: full artwork from 128 px up,
  the flame alone below that, a light variant, a dev badge, a monochrome tray template and title-bar mark"): uma chama
  laranja e vermelha em degradê com um grafo de commits por dentro, um `>_`, um `{}` e faíscas, sobre um quadrado
  grafite com borda laranja (`brza-studio/resources/icon.png`, 256 px). O de dev, `resources/icon-dev.png`, leva um
  selo azul "D".
- Não há fonte vetorial do ícone: o `resources/icon-source/icon.icon/Assets/logo.svg` é um PNG de 391×512 (a chama
  branca chapada) dentro de um `<image>` de SVG; o `icon.json` do Icon Composer fica ao lado, e o
  `resources/icon-source/generate.sh` gera o `.icns` e os PNGs.
- O seletor de ícone, em `src/shared/app-icon.ts:1`, oferece "Flame" (classic), "BrzA Studio ADE" (watercolor) e
  "Light Flame" (blue), mas os arquivos de `resources/app-icons/` seguem `orca-blue.png` e `orca-watercolor.png`.
- Nenhum workstream tem plano ou nota de marca.

Respondida em 2026-10-31, na sessão do workstream `workspace`.

1. **Workstream do plano.** Opções: `studio` (recomendada), workstream novo `brand`, `workspace`.

   **Decidido — "Workstream novo `brand`".** O `workstream/brand` foi criado pelo `brza note workstream brand` na
   mesma sessão.

2. **Alcance.** Opções: o guarda-chuva BrzA (recomendada) e as outras apresentadas na sessão do `workspace`.

   **Decidido — "Guarda-chuva BrzA (Recomendado)"**: uma marca-mãe BrzA, com símbolo e logotipo, e as derivadas BrzA
   Studio, o CLI `brza` e o workspace.

3. **Destino.** Opções: `PLN` (recomendada) e as outras apresentadas na sessão do `workspace`.

   **Decidido — "PLN (Recomendado)"**, o `PLN-007`.

As opções completas e os custos da R1 ficaram na sessão do `workspace`; aqui está o que chegou no pedido.

**Corrigido no levantamento da R2:** o PNG de 391×512 embrulhado em SVG é o `resources/logo.svg:1`, e não o do Icon
Composer. O `resources/icon-source/icon.icon/Assets/logo.svg` é um SVG do Inkscape com a cauda da Orca, do upstream, e
o `icon.json:30` aponta para ele: rodar o `generate.sh` hoje troca a chama pela Orca.

### Rodada 2 — símbolo, arquitetura, vetor, referências e a marca no chat (enviada 2026-10-31)

**Apresentado antes**, pelo levantamento do `collector` (agregado no scratch da sessão, conferido por amostra):
- A arte-mãe é só raster, o `resources/build/icon.png` de 1024 px, igual ao `resources/app-icons/orca-watercolor.png`
  (md5 igual); o `b2918da` não deixou arquivo-fonte. O único vetor da chama é o `resources/brza-flame-mono.svg`, 24 px
  e 13 subpaths, "traced from resources/build/icon.png" (`BrzaFlameLogo.tsx:1`).
- Já existe um logotipo, em raster: os slots de 128 px para cima do `.icns` levam "BrzA STUDIO ADE", com o "A" laranja.
- Não há cor de marca no código: os tokens são o cinza do shadcn (`main.css:192-224,304-365`); o único hex de marca é
  o `F26B1D` dos badges do `README.md:11-12`. O ícone, por amostra, vai de `#FEAE30` a `#EC5D35` sobre `#2C2D32`. A UI
  usa a Geist (`main.css:14-21`) e a SF Mono.
- O laranja já avisa a pergunta do agente: `--agent-question` (`main.css:228,339`).
- Restos da Orca à vista: o app mobile, 2 helpers do `.app`, o `<title>` dos HTML, o `brza --help` e os pacotes Linux.
- Artboards: R2.1 com A1, A2 (o traço mono sem o `>_` e o `{}`) e A3 (esboço), a 128, 32 e 16 px; R2.2 com B1, B2 e
  B3. A R2.5 e a R2.6 vieram depois dos pedidos 2 e 3, com a borda do ícone medida no PNG de 1024 px — fio de âmbar
  `#FFAA44` a `#E04A2B`, brilho interno de 1 px, grafite de `#373A41` a `#19161D` — e o composer de hoje,
  `rounded-xl border border-chat-composer-border` (`NativeChatComposerField.tsx:250`).

Respondida em 2026-10-31, na sessão do `brand`.

1. **O destino do símbolo.** Opções:
   - A2 Simplificar, chama e grafo sem o `>_`, o `{}` e as faíscas, com um corte de silhueta a 16 px (recomendada) —
     custo: ~3–4 h para redesenhar limpo e ~1 h para o corte; se paga: já, no `generate.sh`, no tray e no glifo do chat;
   - A3 Redesenhar, chama geométrica com um ramo de commit vazado — custo: ~3–5 h, com mais rodadas; se paga: quando a
     marca for a público;
   - A1 Preservar, a ilustração inteira — custo: ~4–6 h para vetorizar o degradê e as faíscas, e ainda pede a versão
     pequena; se paga: nunca como símbolo, só como ilustração do ícone.

   **Resposta:** "A1 - apenas corrija a valha no }". **Decidido — A1**, com uma correção só: o `}` solto, à esquerda do
   tronco, que no raster sai partido ao meio, com a metade de baixo borrada. A proposta da correção refaz o `}` inteiro,
   a partir do `}` do par da direita, no tamanho do solto: [a correção a 1024 e a 256 px](PLN-007-simbolo-a1-chave.png),
   antes à esquerda e depois à direita.

2. **A arquitetura mãe e filhas.** Opções:
   - B1 Monolítica, um símbolo e a filha como palavra ao lado (recomendada) — custo: o menor; se paga: já;
   - B2 Endossada, um símbolo por filha com o selo "por BrzA" — custo: +4–6 h; se paga: só com as filhas distribuídas
     em separado, hoje nunca;
   - B3 Cor por filha — custo: ~1 h por cor, e a chama verde ou azul perde o sentido; se paga: com as filhas lado a lado.

   **Resposta:** "B1". **Decidido — B1 Monolítica.**

3. **Quem produz o vetor.** Opções:
   - a sessão desenha o SVG à mão, com construção geométrica, conferido pelo `brza shot` a 16, 32 e 128 px (recomendada)
     — custo: as horas da R2.1, nos passos; se paga: já, no `icon.json` e no `generate.sh`;
   - vetorizar o raster de 1024 px (`vtracer` ou `potrace`) e a sessão limpar — custo: ~1–2 h e o `brew install`, com
     dezenas de paths irregulares; se paga: só com o A1.

   **Resposta:** "2.3 e 2.4 a 1". **Decidido — a sessão desenha o SVG à mão.** Com o A1, é o caminho de ~4–6 h que a
   R2.1 apresentou para a ilustração inteira.

4. **Referências visuais** (múltipla). Opções:
   - o próprio ícone, quente, degradê laranja a vermelho, grafite (recomendada) — custo: nenhuma pesquisa, e uma versão
     chapada para 16 px e o tray; se paga: já;
   - dev tools de símbolo chapado (Linear, Vercel, Raycast, Warp) — custo: o degradê vira acento, ~1 h a mais na paleta;
     se paga: no tray, no favicon e no glifo do chat;
   - terminal e monoespaçada — custo: a marca puxa para o CLI; se paga: no README e no `brza --help`;
   - as referências de Anderson — custo: uma volta a mais; se paga: com direção que as outras não cobrem.

   **Resposta:** "2.3 e 2.4 a 1". **Decidido — o próprio ícone.**

5. **A borda do chat**, do pedido 2. Opções:
   - E2, a borda da logo só no foco do composer (recomendada) — custo: ~1 h numa sessão do `brza-studio`; se paga: já;
     o laranja fixo diluiria o `--agent-question`;
   - E1, a borda da logo sempre — custo: ~1 h; se paga: já, se a marca à vista valer mais que o aviso;
   - E3, o painel inteiro emoldurado — custo: ~2–3 h, estimado sem medir o layout; se paga: quando o chat for vitrine.

   **Resposta:** "E2 e vamos continuar nessa linha de adicionar mais da marca no chat". **Decidido — E2**:
   [a borda do chat no foco](PLN-007-borda-do-chat-e2.png). A segunda metade é o pedido 3, que abriu a R2.6.

6. **Mais marca no chat** (múltipla), do pedido 3, com o símbolo A2 provisório nos artboards. Opções:
   - M1, o símbolo e "BrzA Studio" no estado vazio (recomendada) — custo: ~1 h; se paga: já, a cada chat novo;
   - M2, a chama que tremula e o rótulo com brilho âmbar enquanto o agente trabalha, sem movimento com
     `prefers-reduced-motion` (recomendada) — custo: ~1–2 h; se paga: já, é o estado mais visto;
   - M4, o cursor e a seleção em laranja (recomendada) — custo: ~0,5 h; se paga: já;
   - M3, o anel de contexto no degradê — custo: ~0,5 h; o anel fica dentro do composer laranja no foco, e a 90% o
     vermelho se confunde com o aviso de pergunta; se paga: só com o anel longe do composer;
   - M5, a chama no cabeçalho do painel — custo: ~0,5 h; repete em todo painel o que o ícone já diz; se paga: com
     painéis de vários tipos lado a lado, hoje nunca.

   **Resposta:** "todos menos o M4". **Decidido — M1, M2, M3 e M5**:
   [M1](PLN-007-marca-no-chat-m1.png) · [M2](PLN-007-marca-no-chat-m2.png) · [M3](PLN-007-marca-no-chat-m3.png) ·
   [M5](PLN-007-marca-no-chat-m5.png). O M3 e o M5 entraram contra a recomendação: o anel cheio sem colidir com o
   `--agent-question` nem com o composer em foco, e a chama que não vira ruído com vários chats abertos, vão ao Desenho.

**Em aberto para a R3:** o logotipo e a tipografia, a partir do "BrzA STUDIO ADE" do `.icns` e da Geist; a paleta; onde
a marca aparece, com os restos da Orca neste plano ou numa issue; e o corte pequeno do A1 — o glifo do chat, o M2 a
18 px e o M5 a 13 px, onde a ilustração inteira não lê: o traço mono de hoje, ou outra silhueta.

### Rodada 3 — logotipo, paleta, corte pequeno e onde a marca aparece (enviada 2026-10-31)

**Apresentado antes:** seis artboards, com o símbolo A1 de `}` corrigido nos lockups e a Geist do app
(`src/renderer/src/assets/fonts/Geist-Variable.woff2`) embutida. O contraste medido: o `#F26228` dá 3,2:1 sobre branco e
não serve a texto pequeno no claro, e por isso a paleta ganhou o `#C2410C` (5,2:1); o `#FFAA44` dá 10,5:1 sobre
`#0a0a0a`. O corte "só a silhueta" saiu antes da rodada: o contorno do traço mono já carrega o grafo vazado. Os L não
carregaram no chat na primeira ida — ~630 KB cada, com a imagem repetida —; foram de novo com ~130 KB.

Respondida em 2026-10-31, na sessão do `brand`.

1. **O logotipo e a tipografia.** Opções:
   - L2, o arranjo do selo "BrzA STUDIO ADE" do `.icns`, na Geist, com a filha em caixa alta espaçada e o "ADE" só no
     ícone (recomendada) — custo: ~2–3 h para os lockups em SVG, texto em paths, 4 filhas, 2 arranjos e 2 temas; se
     paga: já, o logotipo bate com o ícone;
   - L1, a Geist com a filha em peso regular — custo: o mesmo; se paga: já, se o selo não for a referência;
   - L3, a monoespaçada — custo: o mesmo, e puxa a marca para o CLI, contra a R2.4; se paga: só no README e no CLI.

   **Resposta:** "L2 e S1". **Decidido — L2**: [o logotipo L2](PLN-007-logotipo-l2.png).

2. **A paleta**, âmbar `#FFAA44`, laranja `#F26228`, brasa `#E04A2B`, laranja texto `#C2410C` e grafite `#2C2D32`, com o
   degradê como assinatura. Opções:
   - P1, e o `--agent-question` passa ao azul que o app já usa (`#1447e6`) (recomendada) — custo: ~1 h numa sessão do
     `brza-studio`, os tokens `--brand-*` e o aviso nos dois temas; se paga: já, e resolve o choque do M3 que a R2.6
     mandou ao Desenho;
   - P2, e o `--agent-question` fica laranja — custo: ~0,5 h; se paga: nunca resolve o choque.

   **Resposta:** "P1". **Decidido — P1**: [a paleta P1](PLN-007-paleta-p1.png).

3. **O corte pequeno do símbolo**, para o glifo do chat, o M2 e o M5. Opções:
   - S1, o traço mono de hoje, com o `}` solto corrigido também nele (os subpaths 4 e 6 do `brza-flame-mono.svg`)
     (recomendada) — custo: quase nenhum agora, e o traço é refeito junto com o SVG da R2.3; se paga: já;
   - S2, a chama e o grafo sem o `>_` e o `{}` — custo: ~0,5 h; se afasta do A1; se paga: só acima de 24 px.

   **Resposta:** "L2 e S1". **Decidido — S1**: [o corte pequeno](PLN-007-corte-pequeno-s1.png), o S1 à esquerda.

4. **Onde a marca aparece** (múltipla), pela ferramenta de pergunta. Opções:
   - o app desktop: o ícone, com o `icon.json` e o `generate.sh` no SVG novo, o tray, a barra de título, a Landing e o
     Onboarding (recomendada) — custo: ~3–5 h numa sessão do `brza-studio`, depois do SVG; se paga: já;
   - o CLI e os READMEs: o `brza --help` sem "orca" (`src/cli/root-help-text-primary.ts:2-4`) e o logotipo no README
     do `brza-studio` e no do `brza-workspace` (recomendada) — custo: ~1–2 h; se paga: já;
   - o app mobile — custo: ~4–8 h, estimado pelo inventário; se paga: quando o mobile entrar no uso;
   - os restos da Orca à vista neste plano; sem esta opção, viram issue — custo: ~3–6 h, com risco nos merges do
     upstream; se paga: com outro usuário além de Anderson.

   **Resposta:** "App desktop (Recomendado), CLI e READMEs (Recomendado)". **Decidido — o app desktop e o CLI e os
   READMEs.** O mobile e os restos da Orca foram à
   [issue dos restos da Orca](../../work/issues/os-restos-da-orca-a-vista-no-brza-studio.md), gravada no `brand`, com
   `scope: brza-studio`.

**A entrevista fecha aqui.** Nada de estrutura ficou aberto; os riscos do M3 e do M5 vão ao Desenho, e o do M3 já perde
metade com a P1.

### Rodada 4 — a fonte da marca, quem desenha, o pipeline do ícone e o corte (enviada 2026-11-02)

**Apresentado antes:** o rascunho do Desenho pelo `designer`, com 8 itens `D` e 14 pontos para rodada, conferido por
amostra pela sessão: o app instalado só leva o `Resources/icon.icns`, sem `Assets.car` nem `CFBundleIconName` no
`Info.plist`; o Icon Composer gera uma arte só para todos os tamanhos, e o `.icns` de hoje tem duas — sem o selo
abaixo de 128 px, com o selo de 128 para cima; o `#1447e6` dá 2,9:1 sobre `#0a0a0a`; o cabeçalho do painel do chat não
tem título e marca o painel com foco por `data-active-pane` (`NativeChatPaneHeader.tsx:43`); o "agente trabalhando" é
o `LoadingSpinner` do `NativeChatTurnActivityLine.tsx:61`. Os pontos vão em três rodadas: esta, de estrutura, pela
ferramenta; as de tela, com artboards.

Respondida em 2026-11-02, na sessão do `brand`, pela ferramenta de pergunta.

1. **Onde moram os SVG mestres e os scripts.** Opções:
   - `brza-studio/resources/brand/`, com os scripts em `config/scripts/` (recomendada) — custo: ~0,25 h, sem conflito,
     porque o upstream não tem a pasta; se paga: já, o `generate.sh`, a Landing e o README leem do próprio repositório;
   - a pasta do PLN-007 no `brand` — custo: uma cópia de ~0,25 h a cada ida ao `brza-studio`, com duas fontes que
     divergem; se paga: nunca, para o app;
   - `resources/icon-source/`, ao lado do `icon.icon` — custo: o da primeira e conflito numa pasta que o upstream mexeu 3
     vezes em 4 dias; se paga: nunca, além da primeira.

   **Resposta:** "brza-studio/resources/brand/ (Recomendado)". **Decidido.**

2. **Quem desenha o SVG do A1 e os lockups L2.** Opções:
   - esta sessão do `brand`, no scratch, com a aprovação por artboard aqui, e a sessão do `brza-studio` só copia
     (recomendada) — custo: ~7,5–10,5 h aqui; se paga: já, o contexto e os artboards estão nesta sessão;
   - uma sessão do `brza-studio`, na branch `feat/pln-007-brand-assets` — custo: as mesmas horas e o arranque de uma
     sessão nova; se paga: só se o desenho tiver de nascer no commit da aplicação.

   **Resposta:** "Esta sessão do brand (Recomendado)". **Decidido.** O desenho é da sessão do `brand`; a aplicação
   segue no `brza-studio`, como o Fora de escopo diz.

3. **O pipeline do ícone.** Opções:
   - o `generate.sh` renderiza cada slot do SVG com o `rsvg-convert` e monta o `.icns` com o `iconutil`, sem o `actool`;
     o mesmo script gera o tray, o `icon-dev.png` e os PNG do seletor; o `icon.icon` fica parado e vai à issue dos
     restos da Orca (recomendada) — custo: ~1,5 h; se paga: já, e mantém as duas artes;
   - o `icon.json` no SVG, com o `actool` — custo: ~1 h, o selo ilegível a 16 e 32 px, e o tray, o dev e o Light Flame
     fora do script; se paga: só com o `Assets.car` empacotado;
   - o `actool` nos slots grandes e o `rsvg-convert` nos 4 pequenos — custo: ~2 h e dois caminhos; se paga: nunca, sem
     `Assets.car`.

   **Resposta:** "rsvg-convert + iconutil (Recomendado)". **Decidido.** Reabre o "com o `icon.json`" da R3.4: o
   `icon.json` deixa de ser o caminho do ícone, e a cauda da Orca para que ele aponta vai à issue.

4. **O corte da execução**, ~17–24 h. Opções:
   - seis passos e três branches no `brza-studio` — tokens, assets, chat —, com os tokens junto do desenho do símbolo e
     o CLI e os READMEs por último (recomendada) — custo: ~17–24 h, em três merges; se paga: nos tokens, o azul do aviso
     tira o choque do M3 antes do chat;
   - uma branch só, depois do símbolo aprovado — custo: o mesmo, com os tokens esperando; se paga: se um merge só valer
     mais;
   - o chat primeiro, com o S1 de hoje — custo: ~0,5 h a mais para refazer o M1; se paga: para ver a marca no chat antes.

   **Resposta:** "Seis passos, três branches (Recomendado)". **Decidido.**

### Rodada 5 — o tile, o `logo.svg`, o símbolo do estado vazio e o logotipo no app (enviada 2026-11-02)

**Apresentado antes:** três artboards, conferidos pelo PNG — o ícone num Dock de mentira, entre ícones na grade da
Apple, a 64 e 96 px; a barra de título com o `logo.svg` a 16 px nos dois temas; o estado vazio com o símbolo a 48 px e
o L2 na Geist. O tile de hoje ocupa 914 px no canvas de 1024 (`magick … -format %@` → `914x952+55+36`). A caixa cinza
do macOS 26 para o ícone fora da grade veio de resultados de busca, sem as páginas abertas, e foi dita assim.

Respondida em 2026-11-02, na sessão do `brand`.

1. **A grade do tile.** Opções:
   - T1, a grade da Apple, 824 px, o ícone ~10% menor que hoje (recomendada) — custo: nenhum a mais, no D1; se paga:
     já;
   - T2, a caixa de hoje, 914 px — custo: nenhum; se paga: sem caixa cinza no Dock e com o ícone maior preferido.

   **Resposta:** "5.1.1". **Decidido — T1**: [a grade da Apple](PLN-007-tile-t1.png).

2. **O `logo.svg`**, na barra de título, no menu de ajuda e em Configurações. Opções:
   - G1, o S1 chapado, branco no escuro e preto no claro, sem mudar código, porque os 5 usos já invertem
     (recomendada) — custo: ~0,25 h; se paga: já, segue o chrome monocromático da norma do app;
   - G2, o A1 colorido, com o tile — custo: ~1 h, os 5 usos perdem o `invert` e o `opacity`, e a 16 px a ilustração
     vira mancha; se paga: nunca, a 16 px.

   **Resposta:** "5.2.2". **Decidido — G2**, contra a recomendação: [o A1 na barra de título](PLN-007-logo-svg-g2.png).
   A 16 px entra a arte sem selo dos slots pequenos do `.icns`.

3. **O símbolo do estado vazio (M1).** Opções:
   - V1, o A1 com o tile, o mesmo do ícone e do L2 (recomendada) — custo: nenhum a mais; se paga: já;
   - V2, o S1 no degradê, sem o tile, como o artboard do M1 da R2.6 — custo: nenhum a mais, reaproveita a chama do M2;
     se paga: se o tile pesar no tema claro.

   **Resposta:** "5.3.2". **Decidido — V2**: [o S1 no degradê](PLN-007-estado-vazio-v2.png), como o M1 foi escolhido.

4. **O logotipo dentro do app** — Landing, Onboarding, M1 —, pela ferramenta. Opções:
   - texto vivo na Geist, um componente `BrzaWordmark` com as medidas do L2 (recomendada) — custo: ~0,5 h; se paga: já,
     segue o tema e o tamanho do texto;
   - o SVG do lockup como imagem — custo: ~0,25 h, um arquivo por tema, sem acompanhar o texto; se paga: só fora do
     app, no README.

   **Resposta:** "Texto vivo na Geist (Recomendado)". **Decidido.**

### Rodada 6 — a borda, o botão, o anel e a chama no cabeçalho (enviada 2026-11-02)

**Apresentado antes:** quatro artboards, conferidos pelo PNG com a cópia corrigida do `brza shot` — o composer em
repouso e em foco, nos dois temas; o botão de enviar no foco; o anel a 30, 60, 90 e 97% e a 93% dentro do composer; três
chats lado a lado, com o do meio em foco. A borda do composer tem largura constante de propósito, "Use a constant
container border so focus changes cannot flash it" (`NativeChatComposerField.tsx:251`); o anel cheio já vai ao
`text-destructive`; o painel com foco já leva `data-active-pane` (`NativeChatPaneHeader.tsx:43`).

Respondida em 2026-11-02, na sessão do `brand`.

1. **A largura do fio no foco (E2).** Opções:
   - W1, 1 px nos dois estados, com um halo de 3 px a 10% no foco (recomendada) — custo: ~1 h, no D5; se paga: já, nada
     pula ao focar;
   - W2, 1,5 px nos dois estados, como o protótipo da R2.5 — custo: o mesmo, e a borda em repouso engrossa em todo chat;
     se paga: se o fio fino não segurar o degradê no claro.

   **Resposta:** "6.1.1". **Decidido — W1**: [o fio de 1 px](PLN-007-borda-fio-w1.png).

2. **O botão de enviar com o composer em foco.** Opções:
   - K1, o `primary` de hoje, que a norma do app reserva à ação (recomendada) — custo: nenhum; se paga: já;
   - K2, o degradê da marca, branco sobre laranja a 3,2:1, o bastante para um ícone — custo: ~0,25 h; se paga: se o
     foco do composer for o momento mais forte da marca.

   **Resposta:** "6.2.2" e "refaça o artboard do 6.2 com o botão redondo". **Decidido — K2**, contra a recomendação. O
   botão do app já é redondo, `size-8 rounded-full` (`NativeChatComposerActions.tsx:145`): os artboards da R2.5 e da
   R6 o tinham desenhado quadrado e de 24 px, e o da R6.2 foi refeito fiel ao código:
   [o botão no degradê](PLN-007-botao-k2.png). O PNG do E2 da R2.5 fica como foi aprovado, com o botão errado.

3. **O anel de contexto a partir de 90% (M3).** Opções:
   - N1, de âmbar a laranja até 89% e, de 90% para cima, o vermelho de alerta de hoje, chapado (recomendada) — custo:
     ~0,5 h; se paga: já, o anel cheio vira outro estado;
   - N2, o degradê que esquenta até a brasa — custo: ~0,5 h, e some o aviso de contexto cheio; se paga: nunca.

   **Resposta:** "6.3.1". **Decidido — N1**: [o anel](PLN-007-anel-n1.png). Com a P1, fecha o risco do M3 da R2.6.

4. **A chama no cabeçalho com vários chats (M5).** Opções:
   - H1, apagada sem foco e no degradê só no painel com foco (recomendada) — custo: ~0,5 h; se paga: já, diz qual chat
     recebe o teclado;
   - H2, no degradê em todos — custo: ~0,5 h; se paga: só com um chat aberto;
   - H3, só no painel com foco — custo: ~0,5 h, aparece e some a cada troca; se paga: se a apagada for ruído.

   **Resposta:** "6.4.1". **Decidido — H1**: [a chama no cabeçalho](PLN-007-cabecalho-h1.png). Fecha o risco do M5 da
   R2.6.

### Rodada 7 — o azul no escuro e o `brza --help` (enviada 2026-11-02)

**Apresentado antes:** o `#1447e6` da P1 dá 2,9:1 sobre `#0a0a0a`; o `--terminal-pane-locate` já usa o
`--color-blue-400` no escuro. O `brza --help` imprime "orca" em 95 linhas, e o upstream editou o texto do help 3 vezes
em 5 dias.

Respondida em 2026-11-02, na sessão do `brand`, pela ferramenta de pergunta.

1. **O azul do `--agent-question` no escuro.** Opções:
   - `#1447e6` (blue-700) no claro e `--color-blue-400` no escuro (recomendada) — custo: ~0 h a mais nos tokens; se
     paga: já, o glifo passa de 3:1 no escuro;
   - `#1447e6` nos dois temas — custo: nenhum, e o glifo fica abaixo de 3:1 no escuro; se paga: nunca, no escuro.

   **Resposta:** "blue-700 no claro, blue-400 no escuro (Recomendado)". **Decidido.** Ajusta a P1 da R3.2 no escuro.

2. **O `brza --help` sem "orca".** Opções:
   - a troca na impressão, num arquivo do fork (`src/cli/brza/cli-display-name.ts`), com o cabeçalho "BrzA CLI", e
     `orca://pair` e `ORCA_*` como estão (recomendada) — custo: ~1 h, com o teste; se paga: já, e a cada merge;
   - editar as 95 linhas — custo: ~1–1,5 h e conflito a cada merge que tocar o texto; se paga: nunca, além da primeira;
   - só as linhas 2 a 4 — custo: ~0,1 h, e os exemplos seguem `orca open`; se paga: já, só para o cabeçalho.

   **Resposta:** "Troca na impressão (Recomendado)". **Decidido.**

**Os 14 pontos do rascunho do `designer`** têm resposta, da R4 à R7.

### Rodada 8 — o texto do estado vazio e a branch do CLI (enviada 2026-11-02)

**Apresentado antes:** a reescrita do Desenho pelo `designer`, com dois pontos que nenhuma rodada cobriu. A sessão
conferiu no `brza-studio@a70f63b6a92` que o estado vazio tem título e subtítulo (`NativeChatEmptyState.tsx:38-41`), que
o teste do indicador afirma o `animate-spin` (`NativeChatMessageList.turn-indicator.test.tsx:115`) e que o help sai por
três `console.log` (`src/cli/help.ts:14,19,29`).

Respondida em 2026-11-02, na sessão do `brand`, pela ferramenta de pergunta.

1. **O texto abaixo do logotipo no estado vazio (M1).** Opções:
   - o título com o nome do agente e o subtítulo de hoje (recomendada) — custo: nenhum; se paga: já, o chat segue dizendo
     com qual agente se fala, e as traduções não mudam;
   - uma linha só, como nos artboards do M1 e da V2 — custo: ~0,25 h e uma chave de tradução a menos; se paga: com o
     nome do agente à vista em outro lugar do painel.

   **Resposta:** "Título e subtítulo de hoje (Recomendado)". **Decidido.**

2. **A branch do passo do CLI e dos READMEs.** Opções:
   - abrir de novo a `feat/pln-007-brand-assets` a partir da `master`, depois do chat (recomendada) — custo: nenhum a
     mais; se paga: já, mantém as três branches e a ordem da R4.4;
   - junto do passo dos assets, antes do chat — custo: ~0 h, contra o "por último"; se paga: se um merge a menos valer
     mais que a ordem;
   - uma quarta branch, `feat/pln-007-brand-cli` — custo: um merge a mais; se paga: nunca, além da primeira.

   **Resposta:** "De novo a de assets (Recomendado)". **Decidido.**

**O Desenho fecha aqui**, em [PLN-007 — Desenho](PLN-007-design.md).

### Rodada 9 — o aceite do corte (enviada 2026-11-02)

**Apresentado antes:** o Desenho inteiro, gravado em `PLN-007-design.md`, e o texto dos seis passos, da Regressão e
dos Casos manuais, na mensagem, com ~20,75 h — 9 h na sessão do `brand` e 11,75 h no `brza-studio`.

Respondida em 2026-11-02, na sessão do `brand`, na mensagem.

1. **O corte da execução.** Opções:
   - aceitar os seis passos como estão (recomendada) — custo: ~20,75 h; se paga: no P3, o primeiro merge, que tira o
     laranja do aviso de pergunta;
   - juntar o P1 e o P2 numa rodada de aprovação — custo: ~0,25 h a menos, e um ajuste no símbolo refaz os lockups antes
     de serem vistos; se paga: para ver símbolo e logotipo juntos;
   - dividir o P4 em pipeline do ícone e `logo.svg` com o logotipo — custo: ~0,5 h e um merge a mais; se paga: se o
     pipeline travar.

   **Resposta:** "aceito". **Decidido — os seis passos**: é o aceite do plano, em 2026-11-02. O aceite não autoriza a
   execução; cada passo espera o pedido de Anderson.
