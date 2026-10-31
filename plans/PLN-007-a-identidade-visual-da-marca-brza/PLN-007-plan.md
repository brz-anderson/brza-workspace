---
status: open
phase: design
origin: request
ready: não — faltam o Desenho e os Passos
scope:
  - brza-studio
  - workspace
opened: 2026-10-31
owner: Anderson
tags:
  - design
---

# PLN-007: A marca BrzA tem símbolo, logotipo e derivadas a partir da chama do app

- **Retomar:** entrevista fechada (R1–R3). Próximo: o Desenho — os itens `D` do SVG do símbolo A1, do corte S1, dos
  lockups L2, dos tokens P1, da marca no chat (E2, M1, M2, M3, M5) e das aplicações do desktop, do CLI e dos READMEs.

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

## Worklogs

- 2026-10-31 — aberto; R1 gravada como chegou da sessão do `workspace`; Terreno pelo `collector`; R2 fechada, com os
  pedidos 2 e 3 da borda e da marca no chat; R3 fechada, com a issue dos restos da Orca. Parou antes do Desenho.
  [PLN-007: a abertura da marca BrzA](../../work/worklogs/2026-10-31-pln-007-a-abertura-da-marca-brza.md)
