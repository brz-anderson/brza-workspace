---
scope:
  - brza-studio
  - workspace
---

# PLN-007: a abertura da marca BrzA

Anderson pediu, na sessão do workstream `workspace`, o plano da identidade visual da marca BrzA, "partindo do ícone do
app para montar a logo", e respondeu ali a R1: o workstream novo `brand`, o guarda-chuva BrzA e o `PLN`. O plano é
[PLN-007: A marca BrzA tem símbolo, logotipo e derivadas a partir da chama do app](../../plans/PLN-007-a-identidade-visual-da-marca-brza/PLN-007-plan.md).

## O que se decidiu

A R1, gravada como chegou da sessão do `workspace`. O número subiu na `master` em `d85c783`.

A R2, com artboards no chat: o símbolo é a ilustração do ícone de hoje (A1), com o `}` solto refeito inteiro; a marca é
monolítica (B1); a sessão desenha o SVG à mão; a referência é o próprio ícone. No meio da rodada, Anderson pediu a borda
do chat igual à da logo e mais marca no chat: ficaram a borda só no foco do composer (E2) e a marca no estado vazio, no
agente trabalhando, no anel de contexto e no cabeçalho (M1, M2, M3, M5). O cursor e a seleção laranja (M4) ficaram de
fora. O M3 e o M5 entraram contra a recomendação, e os riscos deles vão ao Desenho.

## O que se levantou

- O `collector` corrigiu o levantamento da R1: o PNG embrulhado em SVG é o `resources/logo.svg`, e o
  `icon-source/icon.icon/Assets/logo.svg` é a cauda da Orca, para onde o `icon.json:30` aponta — o `generate.sh` de
  hoje troca a chama pela Orca. A sessão conferiu por amostra esse fato, o md5 do 1024 e a origem do traço mono.
- A correção do `}` foi prototipada no scratch, colando o `}` do par da direita, escalado, sobre o solto, no raster de
  1024 e no de 256 px. Nada foi gravado no `brza-studio`.
- O `brza print --app` não tirou o print do app: falta a permissão de Gravação de Tela. O "hoje" dos artboards do chat
  saiu do código.

## A R3

Na R3, a entrevista fechou. O logotipo é o arranjo do selo do `.icns` (L2). A paleta é a do ícone, e o aviso de
pergunta do agente passa a azul (P1). O corte pequeno é o traço mono de hoje, com o `}` corrigido (S1). A marca entra no
app desktop, no CLI e nos READMEs. O mobile e os restos da Orca foram a
[Os restos da Orca à vista no BrzA Studio](../issues/os-restos-da-orca-a-vista-no-brza-studio.md), gravada aqui no
`brand`, e não no `studio`: pedido de outro workstream não entra nesta sessão.

Os três artboards L não carregaram no chat na primeira ida: tinham ~630 KB cada, com a imagem do símbolo repetida em
base64. Com a imagem uma vez só, em classe CSS, caíram a ~130 KB e carregaram. O plano foi a `phase: design`.
