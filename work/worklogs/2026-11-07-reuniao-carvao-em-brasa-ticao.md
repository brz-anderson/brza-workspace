---
scope:
  - brza-studio
tags:
  - design
refs:
  - PLN-007
---

# Reunião Carvão em Brasa: a participação de Tição, o Guardião

O pedido de Anderson, em 2026-11-07, na sessão da coordenação ("Rebranding BrzA: Carvão em Brasa"): "coordenar uma
reunião de rebranding da marca BrzA (…) se aproximar mais do tom Carvão em Brasa, com um grafite mais próximo ao carvão e
tons em brasa incandescente". Este é o registro de **Tição** — persona o Guardião, no agente Claude —, aberto pela coordenação com
`brza sessions reuniao-brasa-ticao`. A pauta e as regras estão no briefing da reunião; cada rodada é uma seção abaixo.

## O que se fez

### Rodada 1: opinião inicial

Abri as imagens: `brasa/brasa.png`, `brasa/simbolo/A.png`, `B.png`, `C.png` e `brasa/chat/brasa-chat-7-composer.png` e
`-8-avisos.png`. Medi os contrastes (WCAG 2.x, luminância relativa) com um script no scratch; os números marcados
"medi" saem dele. Suposição declarada: a tremulação e o degradê âmbar → vermelho do PLN-007 foram escolhidos para ler
como chama, e não por acaso; não reli o plano nesta rodada.

#### 1. Carvão, a base neutra

- **Posição:** fica o `#1A1B1E` de fundo, sem trocar; o que falta é a rampa de texto, não um carvão novo.
- **Por quê:** medi `#1A1B1E` sob o branco a 17,2:1 e sob a 07 a 4,85:1 — a base já sustenta a brasa. Um carvão
  aquecido, `#1C1A19`, daria 17,3 e 4,89: ganho de contraste nulo, e todo cartão, borda e captura de tela mudam. A falha
  real é a 03 como texto (1,8:1, lido no briefing). Suponho que o subtom frio do 01 é o que faz a brasa saltar, por
  oposição; aquecê-lo encurta essa distância.
- **Ideias:**
  - Dois tokens de texto fora da rampa de superfície: `--text-primary #E8E4E0` (medi 13,7:1) e
    `--text-secondary #A39E99` (medi 6,5:1); a 03 fica só para divisória e ícone inativo. `(ousadia: baixa)`
  - A 04 Cinza Aquecido deixa de ser "etapa" e vira só o tom de borda do tile do símbolo — resolve o salto 03 → 04 sem
    inventar etapa intermediária. `(ousadia: baixa)`
  - Tema claro: "Carvão em Brasa" no claro é papel com carvão por cima — fundo `#F5F1EC`, texto `#1A1B1E` (medi 15,3:1),
    brasa de texto na 05 `#A83E15` (medi 5,55:1); a 07 no claro só em superfície, nunca em texto (3,15:1). `(ousadia: média)`
- **Risco:** a sala ler "não trocar o fundo" como "não fazer o rebranding"; o carvão pode parecer o grafite de sempre.
- **Confiança:** 75/100

#### 2. Brasa, a escala quente, a semântica e o contraste

- **Posição:** a 07 entra como CTA com texto escuro e só onde há uma ação a disparar; o erro sai do vermelho-laranja.
- **Por quê:** medi `#1A1B1E` sobre a 07 a 4,85:1 (passa AA normal) e o branco a 3,55:1 (não passa) — o texto escuro é
  obrigatório, não estético. Medi o erro `#ff6568` contra a 07 a **1,24:1**: as duas só se separam pela matiz, e quem
  tem deficiência de vermelho-verde não as separa. Isso não é colisão de gosto; é perda de semântica.
- **Ideias:**
  - Erro para `--danger #FF7AA2` (rosa frio; medi 7,0:1 no 01 e 1,45:1 contra a 07, com matiz longe), sempre com o
    ícone ⓘ que já existe — a cor deixa de ser o único sinal. `(ousadia: média)`
  - Regra "uma brasa por tela": no máximo um elemento na 07 cheia por vista; o resto da brasa fica em 05/06 a ≤22% de
    opacidade, como o accent do protótipo. `(ousadia: baixa)`
  - A 06 nunca leva texto (4,4:1 com branco, lido); fica para ícone ativo e para o anel de contexto. `(ousadia: baixa)`
  - O aviso `#eab308` fica (medi 8,98:1); é âmbar, primo da chama antiga, e não colide com a 07. `(ousadia: baixa)`
- **Risco:** o rosa do erro pode parecer estranho à família quente e ser lido como "cor de outra marca".
- **Confiança:** 80/100

#### 3. O símbolo

- **Posição:** **B — Núcleo incandescente**, porque é a menor mudança que acende o símbolo sem mexer na silhueta nem no tile.
- **Por quê:** nas imagens, A e B mantêm a geometria do PLN-007; C escurece a crosta e a chama perde massa — lido em
  `C.png`, a 32 px a crosta já some no tile. A muda o tile ("aceso por baixo"), e o tile é o que liga as quatro filhas
  no lockup; B deixa o tile no grafite, como hoje. Em 16 px os três viram a mesma mancha laranja (lido em `A/B/C.png`):
  quem decide o tamanho pequeno é a versão plana, não o tratamento. Suposição: o tray do macOS usa imagem *template*
  monocromática, então nenhum dos três chega lá.
- **Ideias:**
  - B com o halo só a partir de 64 px; de 32 px para baixo, a chama em cor chapada 07 → 05, sem halo. `(ousadia: baixa)`
  - O tray continua o glifo mono de 16–18 px do PLN-007 (lido: "mono 18" em `brasa.png`), sem cor. `(ousadia: baixa)`
  - O "A" do wordmark leva o mesmo degradê do núcleo do B, para que símbolo e logotipo mudem juntos e numa só troca. `(ousadia: média)`
- **Risco:** B é o menos memorável dos três; se a sala quer que o rebranding *se veja*, C ganha no impacto.
- **Confiança:** 70/100

#### 4. A brasa viva na interface

- **Posição:** o Enviar fica cinza em repouso e ganha a 07 quando há texto para mandar; a brasa vive no estado, não na decoração.
- **Por quê:** hoje o Enviar ganha a marca no foco (lido no briefing). O próprio protótipo admite que, laranja o tempo
  todo, "o foco muda menos" (lido em `brasa-chat-7-composer.png`). Um sinal que nunca muda deixa de informar. Suposição:
  a tremulação do "trabalhando" já é reconhecida pelos usuários do app e não deve sumir.
- **Ideias:**
  - `NativeChatComposerActions`: Enviar `--surface-2` em repouso → 07 com seta `#1A1B1E` quando o campo tem texto; o foco
    sem texto só acende a borda. `(ousadia: baixa)`
  - "Trabalhando" troca a tremulação por **brasa que respira**: opacidade 0,82 ↔ 1 e brilho 07 a 0 ↔ 12%, ciclo de
    2,4 s; com `prefers-reduced-motion`, fica acesa e parada. `(ousadia: média)`
  - Ao terminar, a chama **esfria**: 600 ms do degradê ao cinza `#8E8C90` (medi 5,17:1) — o fim do trabalho vira cena. `(ousadia: média)`
  - Fagulha nenhuma no chat: movimento decorativo em área de leitura cansa em sessão longa. `(ousadia: baixa)`
- **Risco:** o "esfriar" pode ser lido como erro ou desconexão se o tempo for longo demais.
- **Confiança:** 72/100

#### 5. Narrativa, voz e rollout

- **Posição:** "Carvão em Brasa" é conceito de paleta e de estado, não slogan novo; lança-se como troca de cor, numa
  versão, sem renomear nada.
- **Por quê:** o PLN-007 acabou de fixar símbolo, logotipo e as quatro filhas; um segundo rebranding de voz em menos de
  um ciclo gasta o reconhecimento que ainda está sendo construído. Suponho que a base de usuários é pequena e técnica,
  e que microcópia "poética" em erro irrita quem está trabalhando.
- **Ideias:**
  - Tokens por papel, não por poesia: `--accent`, `--accent-strong`, `--accent-subtle`, `--danger`, `--surface-1..3`; os
    nomes "Brasa Viva" etc. ficam só no guia da marca, para que a próxima recoloração não renomeie código. `(ousadia: baixa)`
  - Uma frase de voz, só no estado vazio: "A brasa está acesa." no lugar do convite atual; nenhuma outra microcópia
    muda. `(ousadia: média)`
  - Rollout em uma versão do app, com o CLI e o workspace recebendo só o símbolo novo na mesma semana; nota de versão
    de uma linha. `(ousadia: baixa)`
  - **Métricas:** (a) auditoria automática de contraste: 100% dos pares de texto ≥ 4,5:1 nos dois temas, zero
    regressão; (b) teste de reconhecimento com 5 pessoas: acham o ícone no Dock entre 10 em ≤ 2 s, em paridade com o
    ícone atual; (c) zero relato de "erro confundido com destaque" no primeiro mês.
- **Risco:** lançar sem barulho pode fazer a mudança passar despercebida e não render nada à marca.
- **Confiança:** 68/100

#### A ideia mais ousada desta rodada

**A brasa só acende no que está vivo.** Em repouso, a interface inteira é carvão e cinza — nenhum laranja, nem no
Enviar, nem no cabeçalho; a 07 aparece só quando o agente trabalha, quando há algo para mandar, ou quando uma pergunta
espera resposta. A cor vira estado e deixa de ser enfeite. Risco: numa captura de tela em repouso, a marca some, e o
app parece genérico.

#### Issues candidatas

- **Erro sai do vermelho-laranja para `#FF7AA2`** — 1,24:1 contra a 07 apaga a semântica do erro — prioridade `high`
- **Tokens de texto `--text-primary` e `--text-secondary` fora da rampa** — a 03 não passa como texto (1,8:1) — prioridade `high`
- **Tema claro do Carvão em Brasa** — a paleta não tem tons claros; proposta `#F5F1EC` com brasa de texto na 05 — prioridade `medium`
- **Símbolo B com versão plana ≤ 32 px** — o halo vira mancha em tamanho pequeno — prioridade `medium`
- **Brasa que respira e esfria no "trabalhando"** — trocar a tremulação, com `prefers-reduced-motion` — prioridade `low`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Carvão | Fica o `#1A1B1E`; criam-se dois tokens de texto; claro = papel `#F5F1EC` com carvão | 75 |
| 2. Brasa | 07 só em CTA, com texto escuro; erro vai ao rosa frio `#FF7AA2`; uma brasa por tela | 80 |
| 3. Símbolo | B, com versão plana ≤ 32 px e o tray mono | 70 |
| 4. Interface | Enviar cinza em repouso, 07 com texto; brasa respira e esfria | 72 |
| 5. Narrativa e rollout | Troca de cor numa versão, tokens por papel, medida por contraste e reconhecimento | 68 |

<!-- fim-rodada-1 -->

### Rodada 2: debate

Li a síntese e a rodada 1 de Cinza, Lenha, Fogareiro e Fole; a da Faísca não estava no worklog dela às 21h. Medi o
ΔE2000 (mesma fórmula da síntese: a 07 contra `#D97757` bate os 11,8): o laranja de hoje, `#f26228`, fica a **7,9**
da Claude, e o âmbar do topo, `#ffaa44`, a 21,3. O `#171615` dá 5,09:1 sob a 07 (medi).

#### As disputas

- **D1:** (a) — carvão quente custa todas as capturas e cartões para ganhar 0,04 de contraste (4,85 → 4,89); o
  `#171615` dá 5,09, ainda sem ganho que pague trocar a base. Fole mesmo diz: "o valor real está na rampa de texto". — 75/100
- **D2:** (b), no `#A8A29E` — cedo o meu `#A39E99`: a síntese mediu 5,18:1 no cartão 02, raspando; o `#A8A29E` dá 5,45.
  `#BCBCBC` é cinza do protótipo, sem família nem história. — 75/100
- **D3:** (b), `#FF7AA2` ou `#FF75A0` — o atual dá ΔE 10,3 em deuteranopia, abaixo do limiar de 15; o rosa dá 22,6.
  Manter um erro que parte dos usuários não separa do CTA não é conservar, é negligenciar. — 85/100
- **D4:** (c), `#FACC15` — fato novo e decisivo: `#eab308` cai a 12,1 em deuteranopia, `#F5B841` a 13,7, ambos abaixo
  de 15. Se é para mexer, que seja uma vez e no valor que passa (17,3). — 65/100
- **D5:** (b) — B não muda a silhueta nem o tile, que liga as quatro filhas; um símbolo só, como o PLN-007 fixou. — 75/100
- **D6:** (a) — respirar e esfriar já é toda a narrativa; fagulha por ferramenta e cor que muda com a hora são
  movimento e variação sem estado novo a comunicar. — 78/100
- **D7:** (a) — viro: a minha frase do estado vazio é a novidade pela novidade de que eu mesmo desconfio. — 70/100
- **D8:** (a) — a colisão não nasce com a brasa: `#f26228` já está a 7,9 da Claude e a 07 se afasta para 11,8. O que
  separava era o âmbar do topo (21,3); não se gasta grau da 07 por isso. — 65/100
- **D9:** (a) — viro: duas semanas de flag no uso de Anderson custam pouco, e reverter depois de lançado é mudar a
  marca duas vezes para quem já a conhece — o pior custo que um guardião aceita. — 72/100

#### Os ataques

1. **Fole, no símbolo (C e o sistema de duas leituras).** O PLN-007 fechou *um* símbolo para quatro filhas; a C no
   grande e a B no pequeno são duas marcas a manter, e o próprio Fole admite que "o glifo pequeno pode virar uma terceira
   marca". Em `C.png` a crosta já some a 32 px, e a C é a mais escura no Dock escuro. **Derruba o ataque:** o teste de
   5 s com 5 pessoas reconhecer a C e o glifo como a mesma marca em ≥ 4/5, com o reconhecimento da C acima do da B.
2. **Fogareiro, na interface (Brasa Noturna).** A cor da marca passa a depender da hora e de quanto tempo a sessão
   está aberta: a captura das 23h não é a das 15h, e o macOS já aquece a tela inteira pelo Night Shift — o app
   aqueceria duas vezes. **Derruba o ataque:** relatos de desconforto com a 07 à noite em quem tem o Night Shift ligado,
   ou a métrica "zero queixas por fadiga" do próprio Fogareiro estourando no piloto.

#### A concessão

- **Cinza, Lenha e Fogareiro, na voz literal:** saio da frase "A brasa está acesa." — a microcópia não muda.
- **Fole, Lenha e Cinza, na flag:** troco "uma versão direto" pela flag `brand.brasa` de duas semanas.
- **Fole, no `#A8A29E`:** os números da síntese no cartão 02 mostram que o meu `#A39E99` raspava.

#### "Sim, e…"

- **Sobre a brasa única de Lenha:** a brasa que respira é a chama de 13 px que o cabeçalho do painel *já tem* — nenhum
  elemento novo. Com vários painéis, só o focado respira; os outros que trabalham ficam acesos e parados, na 05. `(ousadia: baixa)`
- **Sobre o piloto sem cor de Cinza:** em vez de piloto, um teste permanente — as 8 cenas do chat renderizadas com
  `filter: grayscale(1)` no CI, e cada par de estados (repouso/foco, CTA/erro, aviso/info) tem de diferir em ≥ 3:1 de
  luminância ou por ícone. Vira a garantia de que nenhum estado depende só da cor. `(ousadia: média)`

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :------------ |
| 1. Carvão | Fica `#1A1B1E`; texto secundário `#A8A29E` | 75 | 75 | ajustou | Fole e a síntese (5,18 no 02) |
| 2. Brasa | 07 com texto escuro; erro rosa frio; aviso `#FACC15` | 80 | 82 | ajustou | a síntese (aviso a 12,1 em deuteranopia) |
| 3. Símbolo | B, um símbolo só, chapado ≤ 32 px | 70 | 75 | não | — |
| 4. Interface | Respirar e esfriar, só no painel focado | 72 | 76 | ajustou | Lenha |
| 5. Narrativa e rollout | Microcópia literal; flag `brand.brasa` de 2 semanas | 68 | 72 | virou | Cinza, Lenha, Fogareiro, Fole |

<!-- fim-rodada-2 -->

### Rodada 3: voto final

#### O voto em cada proposta

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| P1 | apoio | — | 85 |
| P2 | apoio com ressalva | O terciário `#7A746F` (3,74) no placeholder reprova o portão 1 da P14 ("100% texto ≥ 4,5"): isentar por escrito ou subir o tom | 78 |
| P3 | apoio | — | 88 |
| P4 | apoio | — | 82 |
| P5 | apoio | É o que protege o catálogo de temas (F61 da Faísca) sem tocar no `--primary` | 85 |
| P6 | apoio com ressalva | `#FFB088` é uma nona cor; prefiro o código em linha no texto primário neutro, sem matiz novo, e só adotar o rescaldo se o neutro não destacar | 60 |
| P7 | apoio | — | 86 |
| P8 | apoio com ressalva | Só no tray; o ícone do Dock é a marca e fica estático. Suponho que o ponto colorido tira o tray do *template*, e então o ponto vai na 05/07 só quando trabalha | 58 |
| P9 | apoio | — | 82 |
| P10 | apoio | — | 88 |
| P11 | apoio com ressalva | Trocar o "Ask Claude…" pode vir do upstream; conferir se a cópia é nossa antes de mexer, para não brigar a cada sync | 75 |
| P12 | apoio | — | 76 |
| P13 | apoio com ressalva | Incluir a marca de hoje como base: `#f26228` já está a ΔE 7,9 da Claude; se hoje ninguém confunde, a 07 (11,8) não confundirá | 80 |
| P14 | apoio com ressalva | Medir a linha de base da versão atual antes do portão 4, senão "10% acima da base" não tem base | 84 |
| P15 | apoio com ressalva | "0/5 atribuem à Claude" só no símbolo isolado; na tela com o nome Claude à vista, a meta mede o rótulo, não a cor. "0 queixas" com um usuário é sinal, não prova | 70 |

#### O que me faria mudar de ideia

- **P3 (88):** um teste de tarefa em que deuteranopes leiam o rosa como "não é erro" mais vezes que o `#ff6568`.
- **P10 (88):** o piloto mostrar a respiração notada mais tarde que a tremulação de hoje, ou o esfriar lido como falha.

#### A última ideia

**Um só `brand.tokens.json` para as quatro filhas, com o CLI dentro** — ninguém falou do BrzA CLI. No terminal, a 07
vai em truecolor e cai para o ANSI 256 mais próximo (202, `#ff5f00`), o erro rosa para o 211 (`#ff87af`); o portão 1 da
P14 audita app, CLI e workspace juntos, para as filhas não derivarem. `(ousadia: baixa)` Risco: no terminal de 16 cores
a brasa vira o vermelho do erro; ali só o erro leva cor.

#### Os colegas

| Persona | A contribuição mais útil dela, em uma linha | Nota de 0 a 10 |
| :------ | :------------------------------------------ | :------------- |
| Faísca | Os fatos de código: o `--primary` reescrito pelo tema e o diff que colide com a 06 (1,03:1) | 8 |
| Cinza | O piloto sem cor, que virou portão permanente no CI, e o rigor de separar medida de suposição | 9 |
| Lenha | A brasa única no painel ativo e o anel de foco neutro, separado da marca | 8 |
| Fogareiro | O Enviar que só acende com conteúdo e o usuário cansado às 3h como teste de tudo | 6 |
| Fole | O matiz da Claude, o fato mais incômodo da sala, e a rampa de texto quente | 8 |

#### Autoavaliação

Fiel: guardei o fundo, um símbolo só nas quatro filhas, o token próprio em vez do `--primary` e a menor mudança em cada
voto. Saí da persona ao apoiar erro e aviso novos — mas ali a ruptura provou o ganho com dado, que é a regra de Tição.
O vício apareceu duas vezes: a frase do estado vazio era novidade minha, e o "aceitar" na Claude foi em parte hábito.

<!-- fim-rodada-3 -->

### Rodada 4: entrega — Regras de uso da marca Carvão em Brasa

Fontes, lidas em `~/Projects/brza-studio` (só leitura): `resources/brand/README.md` (as cores e o mapa de geração do
PLN-007), `resources/icon-source/generate.sh:33-53`, `src/main/tray/system-tray.ts:1-93`; e o SVG da B do protótipo
(`material/brasa/simbolo/brza-symbol-brasa-B.svg`). Regra-mãe: **muda a cor, não muda o traçado** — o S1, o tile de
824 px com rx 185, o `{}` e a ausência de fagulha do PLN-007 ficam.

#### O símbolo por tamanho

| Tamanho e uso | Arquivo de origem | Chama | Tile | Halo e borda |
| :------------ | :---------------- | :---- | :--- | :----------- |
| 128–1024 px: ícone do app, Dock (`icns` 128 a 512@2x) | `brza-app-icon.svg`, com o selo | B radial: 07 até .38, 06 em .72, 05 na borda | linear 02 `#2C2D31` → 01 `#1A1B1E` (era `#373A41` → `#19161D`) | halo 06 a 30% → 0, blur 30/1024; borda 24/1024 em 06 → 05 |
| 33–64 px (`icon_32x32@2x`, lockups) | `brza-symbol.svg` | B radial | idem | **sem halo** (a 64 px o blur dá 1,9 px: mancha); borda mantida |
| 17–32 px | `brza-symbol.svg` | **chapada na 07**, sem radial | idem | sem halo; borda some abaixo de 1 px (24/1024 × 32 = 0,75) |
| 16 px (`icon_16x16`, favicon) | `brza-symbol.svg` | chapada 07 | 01 liso | nada; S1 intacto até o teste a 1× e 2× dizer o contrário |
| 48 px, estado vazio (máscara) | `brza-flame-mono.svg` | degradê 07 → 06 → 05 | sem tile | sem halo |
| 13 px, cabeçalho do painel | `brza-flame-mono.svg` | foco: 07 → 06 → 05; sem foco: `#8E8C90`; trabalhando e não focado: 06 parada | — | só o halo da chama focada respira (P10) |
| Tray (`*Template.png`, 22×14) | `brza-tray-template.svg` | preto, *template*, o sistema pinta | — | nada |
| Dev | `brza-symbol-dev.svg` | B | idem | o selo azul `#1447E6` fica: marca a build, e o azul está longe da brasa |
| Claro (`brza-symbol-light.svg`) | idem | B igual (a 07 dá 3,55:1 no branco, passa os 3:1 de gráfico) | `#FFFFFF` → `#F6F1EC` (era `#F6F6F8`) | borda 05 |

- **O tray já tem um estado de atenção âmbar**, que tira o *template* (`system-tray.ts:64-93`, `tray-attention-icon`).
  Fica como está; o estado de "trabalhando" no tray e no Dock é a P8, que está com Anderson.
- **Os nomes `orca-*`** (`app-icons/`, `tray/`) ficam: o README e o `generate.sh:50` dizem que o seletor de ícone do
  upstream os importa. Muda o conteúdo, nunca o nome.

#### O símbolo e a marca no CLI

| Papel | Truecolor | ANSI 256 | 16 cores |
| :---- | :-------- | :------- | :------- |
| "A" do `BrzA`, ação | `#FF3D00` | 202 `#ff5f00` | sem cor, só negrito: a brasa não vira o vermelho do erro |
| Erro | `#FF75A0` | 211 `#ff87af` | 9 (vermelho claro) |
| Aviso | `#FACC15` | 220 `#ffd700` | 11 (amarelo claro) |
| Texto secundário | `#A8A29E` | 248 `#a8a8a8` | 8 (cinza) |

O CLI não desenha a chama: no terminal, a marca é o wordmark `BrzA` com o "A" na brasa. Com `NO_COLOR` ou sem TTY, nada
de cor. Os quatro valores saem do mesmo `brand.tokens.json` do app e do workspace.

#### A brasa na tela: o que pode e o que não pode

1. **Uma brasa sólida por região** (cabeçalho, transcript, composer), só no `--action-brand`: Enviar com conteúdo,
   Continue, Allow, Submit. *Pode:* o Continue no transcript e o Enviar aceso no composer. *Não pode:* o Allow e o
   Submit da mesma pergunta, os dois na 07 — o segundo vai ao neutro.
2. **Rótulo sobre a 07 é sempre `#1A1B1E`.** Nunca branco (3,55:1).
3. **A 06 é ícone e anel, nunca texto**; a 07 não é texto sobre o 02 (3,88:1).
4. **Brasa não é perigo.** Ação destrutiva (apagar, descartar) não usa a 07; o erro é o rosa e o aviso, o limão.
5. **O degradê é só da chama, do "A" do wordmark e da borda do composer em foco.** Nunca em botão, fundo ou texto
   corrido.
6. **Movimento, só o halo da chama focada.** Nada de fagulha, de cor que muda com a hora, nem de brasa animada depois
   do fim do turno.
7. **O símbolo não se recolore, não se estica, não se gira, não ganha contorno nem sombra**, e não sai do tile acima de
   32 px — fora do tile, só a máscara de 13 e de 48 px na interface.
8. **A marca não ocupa o `--primary`**, para não incendiar o catálogo de temas (F61).

#### Os lockups das quatro filhas

- **Fica:** os 23 SVG e os nomes deles, o traçado, "BrzA" em Geist 750, a filha em Geist 500 com +0,14em, o
  horizontal e o vertical, o selo do ícone do app e o gerador `config/scripts/brza-brand-build.mjs`.
- **Muda:** o fogo `brza-fire` (`#FFAA44` → `#E04A2B`) pela B radial, e o "A" pelo linear 07 → 06 → 05. Os tiles mudam
  como na tabela. No escuro, "Brz" passa de `#FAFAFA` para `#E8E2DC` e a filha de `#BCBCBC` para `#A8A29E`; no claro,
  `#0A0A0A` vai a `#1A1B1E` e `#474747` a `#5C5650`.

#### Os ativos a regerar, na ordem

1. As cores do `brza-brand-build.mjs` e a tabela do `resources/brand/README.md`.
2. `node config/scripts/brza-brand-build.mjs`, que regera os 23 SVG de `resources/brand/` e o `resources/logo.svg`.
3. `pnpm build:icons`, que regera `build/icon.icns`, `.ico`, `.png`, `resources/icon.png`, `icon-dev.png`,
   `app-icons/orca-watercolor.png`, `orca-blue.png` e `tray/*Template.png` — o tray deve sair idêntico: conferir pelo
   diff.
4. O `--brand-gradient` e o `--brand-sheen` em `main.css`; a máscara `brza-flame-mono.svg` e o `BrzaFlameLogo.tsx`
   (`currentColor`) não mudam.
5. O `brand.tokens.json` novo, lido pelo app, pelo CLI e pelo workspace.

#### O que ficou de fora e por quê

- **O teste a 13, 16 e 32 px reais, em 1× e 2×:** a regra dos 17–32 px é a hipótese que esse teste confirma ou
  derruba.
- **O favicon:** não achei `rel="icon"` nos `src/renderer/*.html`; suponho que a build web usa o `icon.png`.
- **A brasa como texto no escuro e o código em linha:** ficam com a auditoria de Cinza.
- **Os ícones dentro do tray e do Dock:** a P8 está com Anderson.
- **O gerador:** não li o código do `brza-brand-build.mjs`, só o README dele.

**Confiança na peça:** 74/100

<!-- fim-rodada-4 -->

### Rodada 5: revisão do plano

#### A confiança no plano

| Parte | Confiança (0–100) | Uma linha |
| :---- | :---------------- | :-------- |
| O plano inteiro | 76 | É a menor mudança que entrega o objetivo: traçado intacto, cor por token, tudo reversível até a fase 6 |
| Tabela de tokens v2 | 74 | Medida em 182 pares; o placeholder igual ao secundário e o erro claro `#6E3C5A` "a testar" ainda pesam |
| Fases 0–3 (tokens, ações, movimento) | 78 | Variante `brand` sem tocar o `default` e flag reativa: é o caminho de volta que um guardião quer |
| Fase 4 (símbolo) | 66 | A B segue sem o teste a 13/16/32 px, e a fase cita só o texto dos lockups, não os tiles |
| Fases 5–6 (portões, ativos) | 70 | Os portões vêm antes da fase 6, a única irreversível; falta a regra do CLI em 16 cores |
| As medições de sucesso | 68 | Honestas ao chamar cinco pessoas de sinal; ainda dependem da base da fase 0, que não existe |

#### O erro do plano

Três omissões da minha peça da rodada 4: as oito regras de uso da brasa viraram só "uma brasa por região" (sumiu
"ação destrutiva não usa a 07"); a fase 4 não troca os tiles (`#373A41` → `#19161D` para 02 → 01; claro `#F6F6F8`
para `#F6F1EC`); e a decisão 1 omite que o tray já tem um estado de atenção âmbar (`system-tray.ts:64-93`).

#### A mudança que mais subiria a sua confiança

Gravar as oito regras e a tabela por tamanho no `resources/brand/README.md` como entrega da fase 4, e conferi-las no
portão 2. Sem regra escrita, a marca deriva no primeiro PR de outra frente. **Plano inteiro: 76 → 82.**

#### O risco que o plano não vê

As fases 1 e 2 editam arquivos do upstream (`main.css`, `ui/button.tsx`, a segunda camada de tema); com o radar do
upstream a cada 6 h, cada sync pode abrir conflito na marca. Remédio: uma camada própria, `brza-brand.css`, importada
depois. Suposição: o radar vira merge do upstream.

#### O seu voto nas decisões de Anderson

| Decisão | Opção | Confiança |
| :------ | :---- | :-------- |
| 1. Tray e Dock | Adiar. Viro do "só o tray": ele já tem um estado âmbar de atenção, e um segundo estado colorido competiria com ele | 70 |
| 2. Símbolo | B, com a C como braço do teste de 5 s: toda ruptura tem de provar o ganho, e o teste ou fecha a questão ou mostra que a C ganha | 72 |
| 3. Flag | Duas semanas no uso de Anderson | 80 |
| 4. Fundo | `#1A1B1E` | 82 |
| 5. Onde o plano mora | No workstream `brand`, ao lado do PLN-007 que ele recolore | 85 |

<!-- fim-rodada-5 -->

### Rodada 6: o símbolo em tamanho real

- **Vi as imagens:** sim, `folha-1x.png` e `folha-2x.png`.
- **A ordem de leitura a 16 px:** hoje > A ≈ B > C. Só a de hoje mostra forma; o topo âmbar (6,01:1 no tile) recorta
  a chama, e A, B e C viram um ponto vermelho escuro. A C é o mais apagado.
- **A ordem a 32 px:** hoje > A > B > C. A de hoje mostra o circuito e o `{}`; a base acesa da A segura a silhueta;
  na B o núcleo some no miolo; a crosta da C come a chama.
- **A B passa a 16 e a 32 px?** Não a 16, e a 32 só com ajuste. O pico de 3,88:1 da 07 no tile não recorta a forma; o
  que os separa é a luz que a brasa tirou.
- **O núcleo de rescaldo:** apoio, e estender até 64 px. Não é cor nova: é o `#FFB088` do código em linha, e devolve a
  chama clara do PLN-007 (7,74:1 no tile) — confiança 74.
- **O voto na decisão 2 (símbolo), agora:** B com o núcleo de rescaldo, e a C sai do teste, porque a folha já a mostra
  a pior em 16 e 32 px. Regra de guardião: se a B com rescaldo não ler como a de hoje numa nova folha a 16 e 32 px, o
  símbolo de hoje fica, e a brasa muda só a interface — confiança 72.
- **A confiança na fase 4, agora:** 62 (antes: 66). A evidência mostra que a brasa piora o ícone pequeno, mas o
  remédio é barato e se mede.

<!-- fim-rodada-6 -->

### Rodada 6b: a variante da B

- **Vi as imagens:** sim, `folha-2-1x.png` e `folha-2-2x.png`.
- **A melhor variante a 16 e 32 px:** empate entre a B + rescaldo largo e a B + topo claro, as duas sem halo. A 32 px,
  o circuito e o `{}` voltam; a 16 px a chama ganha forma, mas não o recorte âmbar de hoje — **quase**.
- **A melhor a 64 px:** a B + rescaldo largo, sem halo, que mostra o circuito mais limpo. O halo turva as duas.
- **O voto final no símbolo:** B + topo claro, sem halo. No pequeno, lê como o rescaldo; e mantém a direção do degradê
  do PLN-007, com o claro em cima, de modo que só muda a temperatura. Fica a regra: sem halo abaixo de 128 px —
  confiança 74.
- **A confiança na fase 4, agora:** 70.

<!-- fim-rodada-6b -->

### Rodada 7: a confiança final

- **Confiança no plano inteiro (v3):** 80 (na R5, sobre a v1: 76)
- **O que mais pesou para subir ou descer:** os portões agora medem o par renderizado, com o auditor que lê o app e
  sai com erro e os semânticos pelo objeto inline; e o símbolo ganhou uma regra de saída. Para baixo pesa só o "quase"
  a 16 px.
- **A decisão 6, a norma do rótulo da ação:** WCAG com rótulo escuro (4,85, com o peso ≥ 600 que o plano já pede);
  o branco reprova o portão 1 — confiança 82
- **Algo ainda errado na v3:** a regra de saída da R7 diz "o símbolo de hoje fica no pequeno". A minha diz que o de
  hoje fica *inteiro* e que a brasa muda só a interface; manter o de hoje só no pequeno cria as duas leituras que a
  sala recusou na C.

<!-- fim-rodada-7 -->

## O que ficou

## Fora do workspace

Nada.
