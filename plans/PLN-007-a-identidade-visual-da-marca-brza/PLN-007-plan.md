---
status: open
phase: interview
origin: request
ready: não — faltam a entrevista, o Desenho e os Passos
scope:
  - brza-studio
  - workspace
opened: 2026-10-31
owner: Anderson
tags:
  - design
---

# PLN-007: A marca BrzA tem símbolo, logotipo e derivadas a partir da chama do app

- **Retomar:** R1 e R2 fechadas: A1 com o `}` refeito, B1, vetor à mão, referência o próprio ícone, E2 e M1, M2, M3
  e M5 no chat. Próximo: a R3, com o logotipo e a tipografia, a paleta, onde a marca aparece e o corte pequeno do A1.

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
| `Pedido 1` | O logotipo BrzA existe em vetor, com o símbolo e a palavra, nos arranjos decididos                      | —     | conferência dos artboards (manual)    |
| `R2.2`     | BrzA Studio, o CLI `brza` e o workspace usam o símbolo único, com o nome da filha ao lado da palavra   | —     | conferência dos artboards (manual)    |
| `R2.5`     | O composer do chat ganha a borda da logo só no foco, nos dois temas                                    | —     | conferência no app (manual)           |
| `R2.6`     | O chat mostra a marca no estado vazio, no agente trabalhando, no anel de contexto e no cabeçalho      | —     | conferência no app (manual)           |
| `R1.2`     | A paleta e a tipografia estão fixadas com os valores, e os pontos em que a marca aparece as usam        | —     | conferência no app (manual)           |
| `Pedido 1` | O ícone do app sai da mesma fonte vetorial que o símbolo, pelo `generate.sh`                            | —     | `resources/icon-source/generate.sh` (manual) |

### Fora de escopo

- **Aplicar a marca no código do `brza-studio`.** Cada aplicação é passo de código, executado numa sessão do
  `brza-studio`, na branch `<tipo>/pln-007-<slug>`; aqui fica o pedido.

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

## Worklogs

- 2026-10-31 — aberto; R1 gravada como chegou da sessão do `workspace`; Terreno pelo `collector`; R2 fechada, com os
  pedidos 2 e 3 da borda e da marca no chat. Parou antes da R3.
  [PLN-007: a abertura da marca BrzA](../../work/worklogs/2026-10-31-pln-007-a-abertura-da-marca-brza.md)
