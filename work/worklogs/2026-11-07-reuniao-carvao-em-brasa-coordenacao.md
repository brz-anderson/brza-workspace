---
scope:
  - brza-studio
tags:
  - design
refs:
  - PLN-007
  - issue:assinatura-e-voz-da-marca-carvao-em-brasa
  - issue:auditoria-automatica-de-contraste-e-daltonismo-dos-tokens
  - issue:brasa-nas-quatro-filhas-com-tokens-compartilhados-e-cli
  - issue:brasa-que-respira-e-esfria-no-trabalhando
  - issue:enviar-acende-por-disponibilidade-e-foco-neutro
  - issue:erro-e-aviso-fora-do-matiz-da-brasa
  - issue:ideias-ousadas-da-reuniao-carvao-em-brasa
  - issue:rampa-de-texto-quente-separada-da-superficie
  - issue:reuniao-multiagente-com-personas-pelo-brza-sessions
  - issue:simbolo-b-por-tamanho-e-ativos-regerados
  - issue:tema-claro-cinza-de-fogueira
  - issue:teste-de-reconhecimento-da-brasa-contra-a-claude
  - issue:token-proprio-da-acao-de-marca-fora-do-primary
---

# Reunião Carvão em Brasa: a coordenação e a proposta de plano

O pedido de Anderson, em 2026-11-07, na sessão "Rebranding BrzA: Carvão em Brasa" (workstream `playground`): "Você é o
gerente de produto do BrzA Studio, e vai coordenar/comandar uma reunião de rebranding da marca BrzA (…) o foco
principal do 'mini' rebranding é se aproximar mais do tom Carvão em Brasa, com um grafite mais próximo ao carvão e tons
em brasa incandescente", com ao menos três opiniões por assunto, issues dos pontos levantados, worklogs de cada
participante, personas medidas e um plano com confiança medida, até as 22h. Material de apoio: a versão Brasa do
símbolo e do chat (do PLN-007, no workstream `brand`) e a paleta de sete etapas de Anderson.

## O que se fez

### O formato da reunião

Seis personas, cada uma numa sessão de chat do BrzA Studio aberta pela coordenação com `brza sessions <nome> --agent
<runtime> --checkout .worktrees/playground`, e conduzidas por `brza sessions send`. Cada persona escreveu só no seu
worklog; a coordenação leu, conferiu os números, sintetizou e abriu a rodada seguinte. Os pedidos, as sínteses e o
material ficaram em `.sessions/reuniao-brasa/`, fora do git.

| Persona | Arquétipo | Runtime | Worklog |
| :------ | :-------- | :------ | :------ |
| Tição | o Guardião — conservador, protege o PLN-007 | Claude | [Reunião Carvão em Brasa: a participação de Tição, o Guardião](2026-11-07-reuniao-carvao-em-brasa-ticao.md) |
| Faísca | a Provocadora — divergente, ideia ousada | Grok | [Reunião Carvão em Brasa: a participação de Faísca, a Provocadora](2026-11-07-reuniao-carvao-em-brasa-faisca.md) |
| Cinza | o Cético Analítico — só aceita número | Codex | [Reunião Carvão em Brasa: a participação de Cinza, o Cético Analítico](2026-11-07-reuniao-carvao-em-brasa-cinza.md) |
| Lenha | a Engenheira Pragmática — custo e código | Codex | [Reunião Carvão em Brasa: a participação de Lenha, a Engenheira Pragmática](2026-11-07-reuniao-carvao-em-brasa-lenha.md) |
| Fogareiro | o Advogado do Usuário — o dev cansado às 2h | Antigravity | [Reunião Carvão em Brasa: a participação de Fogareiro, o Advogado do Usuário](2026-11-07-reuniao-carvao-em-brasa-fogareiro.md) |
| Fole | a Estrategista de Marca — posicionamento | Claude | [Reunião Carvão em Brasa: a participação de Fole, a Estrategista de Marca](2026-11-07-reuniao-carvao-em-brasa-fole.md) |

**A pauta:** (1) o carvão, a base neutra; (2) a brasa, a escala quente, a semântica e o contraste; (3) o símbolo A, B
ou C; (4) a brasa viva na interface; (5) a narrativa, a voz e o rollout. Seis opiniões por assunto em cada rodada.

| Rodada | Aberta | Fechada | O que produziu |
| :----- | :----- | :------ | :------------- |
| 1 · opinião independente | 20h00 | 20h07 | 30 opiniões, 78 ideias marcadas por ousadia, 28 issues candidatas |
| 2 · debate | 20h05 | 20h12 | votos em nove disputas, 12 ataques, as concessões e 12 ideias "sim, e…" |
| 3 · voto final | 20h09 | 20h16 | votos em 15 propostas, a nota de cada colega, as autoavaliações |
| 4 · mão na massa | 20h11 | 20h17 | a auditoria de 182 pares (Cinza), o mapa de implementação no código (Lenha), as regras de uso e o símbolo por tamanho (Tição), o guia de narrativa (Fole), o roteiro de teste (Fogareiro), cinco conceitos ousados (Faísca) |
| 5 · revisão do plano | 20h20 | 20h22 | a confiança de cada uma no plano, o erro que viu, a mudança que mais a subiria |
| 6 · o símbolo em tamanho real | 20h25 | 20h31 | o julgamento da folha de contato de hoje, A, B e C a 13–64 px, em 1× e 2× |
| 6b · a variante da B | 20h27 | 20h35 | a escolha entre a B com o núcleo de rescaldo largo e a B com o topo claro, as duas sem halo |
| 7 · a confiança final | 20h35 | 20h38 | a confiança de cada uma na v3 do plano e o voto na norma do rótulo da ação |

Um revisor independente (o papel `reviewer`, de fora da reunião) revisou a v2 da proposta em paralelo à rodada 5 e
releu a v3 depois da rodada 7.

A rodada 6 nasceu da rodada 5: o símbolo era a parte mais fraca do plano (64,5), porque ninguém tinha visto a B em
tamanho real. A coordenação renderizou a folha de contato, e a sala viu, por unanimidade, que a de hoje lê melhor a 16
e 32 px e que a B chapada não passa. A coordenação fez duas variantes com o `#FFB088` da paleta (o "rescaldo"), e a
rodada 6b escolheu entre elas.

### O que a coordenação mediu

A coordenação refez todos os contrastes citados e mediu o que a sala não tinha medido (WCAG 2.x; ΔE2000; simulação de
daltonismo de Machado 2009, severidade 1):

- **Os números das personas:** os de Tição (12), Fole (8), Faísca (11) e Cinza batem; o único errado foi do Fogareiro
  (`#9E9B97` sobre `#171615`: citou 5,2:1, são 6,53:1).
- **O erro contra a brasa:** o `#ff6568` de hoje fica a ΔE 10,3 da 07 em deuteranopia; o rosa `#FF7AA2`, a 22,6; o
  carmesim `#FF3366`, a 11,4. **Esse dado causou três viradas na rodada 2.**
- **O aviso também colidia, e ninguém tinha visto:** `#eab308` a ΔE 12,1 da 07 em deuteranopia; `#FACC15`, 17,3.
- **No tema claro:** o aviso ocre legível fica a ΔE 2,2–3,6 da brasa de texto 05 em deuteranopia.
- **O laranja da Claude:** a 07 tem o mesmo matiz (14,4° contra 14,8°), a ΔE 11,8 do `#D97757`.
- **O símbolo pequeno perde contraste:** o pico da chama de hoje contra o tile é 6,01:1; o da brasa, 3,88:1.
- **O pico de luminância do símbolo** (a Faísca mediu os pixels da folha; a coordenação refez com recorte exato no
  Dock escuro): a 16 px, hoje 142, B chapada 97, B com rescaldo largo 142, B com topo claro 125. A Faísca contestou
  na rodada 7 os picos de 64 px (no papel, os quatro chegam a ~225); a medida da coordenação é no Dock escuro, por
  célula posicionada, e os picos batem com a cor mais clara de cada chama (`#FF3D00` dá luma 98; `#FFB088`, 190).
- **O `brza shot` não roda** contra o `brza-studio` atual ("não achei BASE_CSS em
  `src/shared/native-chat/native-chat-visual-shell.ts`"); a folha de contato saiu do Chrome headless.

### As personas: como cada tipo se comportou

| Persona (runtime) | Latência por rodada | Ideias R1 (baixa/média/alta) | Confiança R1 → voto R3 → plano R5 → plano R7 | Viradas | Votos R3 (apoio/ressalva/contra) | Nota dos colegas | Notas que deu |
| :---------------- | :------------------ | :--------------------------- | :-------------------------------------- | :------ | :------------------------------- | :--------------- | :------------ |
| Tição (Claude) | 1–2 min | 17 (11/6/0) | 73 → 78,5 → 76 → 80 | voz, rollout | 8 / 7 / 0 | 8,9 | 7,8 |
| Faísca (Grok) | 4–7 min | 10 (0/4/6) | 70 → 76,3 → 64 → **81** | voz (parcial); a C pela B, pelo dado (R6) | 2 / 11 / 2 | 8,8 | 8,2 |
| Cinza (Codex) | 1,5–6 min | 11 (5/4/2) | 79 → 92 → 77 → 88 | símbolo A → B | 2 / 7 / **6** | **9,1** | 7,8 |
| Lenha (Codex) | 1–4,5 min | 14 (8/6/0) | 87 → 93,4 → 81 → 90 | erro e aviso; o rescaldo radial pelo topo claro (R6b) | 3 / 11 / 1 | 8,4 | 9,0 |
| Fogareiro (Antigravity) | 1–2 min | 10 (3/5/2) | **89 → 93 → 88 → 94** | erro | **12 / 3 / 0** | **6,25** | 8,9 |
| Fole (Claude) | 1–2 min | 16 (4/9/3) | **68** → 75,7 → 74 → 82 | fundo (por argumento do Tição); a C pela B (R6b) | 10 / 5 / 0 | 8,25 | 8,0 |

- **A evidência renderizada moveu quem o argumento não moveu.** Fole e Faísca defenderam a C da rodada 1 à 5; a folha
  de contato tirou a C dos dois em uma rodada. A Faísca foi além: mediu a luminância dos pixels e desempatou a 6b pelo
  número, contra três personas que escolheram a olho.
- **O dado move mais que o argumento.** Das viradas da rodada 2, três vieram da medição de daltonismo (Lenha, Fogareiro
  e todos no aviso) e uma de argumento (Fole, pelo Tição: "o frio do fundo faz a brasa saltar").
- **A confiança não acompanha a evidência.** O Fogareiro (empático, Antigravity) teve a maior confiança da sala (89 a
  98) com a evidência mais fraca: não abriu as imagens na rodada 1, trouxe o único número errado, votou apoio em 12 de
  15 propostas sem nenhum contra, e foi o pior avaliado pelos colegas (6,25) — e o que deu as notas mais generosas.
  A Fole (estrategista) fez o oposto: a menor confiança (68), as ideias mais ousadas, e foi a mais persuadível.
- **O cético é o mais útil.** O Cinza votou contra seis vezes, pegou os erros que mudaram o plano (o placeholder no
  hover, a 05 a 2,76:1, a tritanopia do erro claro, o script que sai com 0) e foi o mais bem avaliado (9,1).
- **O guardião guarda o artefato, não o processo.** O Tição não cedeu no fundo nem no símbolo, mas virou na voz e no
  rollout, e se autoavaliou: "o vício apareceu duas vezes".
- **A provocadora não amolece.** A Faísca manteve as posições minoritárias até a rodada 5 (fundo `#171615`, a C, um
  dia de flag), teve a menor confiança no plano (64), trouxe os achados de código que ninguém viu (o `--primary`
  reescrito pela segunda camada, o diff a 1,03:1 da 06) e foi a mais lenta.
- **A pragmática corrige a coordenação.** A Lenha corrigiu duas atribuições da coordenação e desmontou a premissa do
  "Ask Claude…" (era do protótipo, não do app); a estimativa dela dobrou ao ler o código (8–16 h → 20–33 h).
- **O mesmo runtime converge.** Tição e Fole, os dois no Claude, chegaram sozinhos à mesma ideia na rodada 3 — o CLI e
  um `brand.tokens.json` para as quatro filhas. A personalidade pesa, mas o modelo também; com dois runtimes por duas
  personas, o efeito não se separa.
- **O custo:** as duas sessões Claude custaram cerca de US$ 2,85 (Tição) e US$ 2,42 (Fole) nas cinco rodadas, pela
  medição; as duas Codex leram 3,2 e 3,9 milhões de tokens de entrada (96% em cache) e escreveram 32 mil e 24 mil; o
  Grok e o Antigravity não têm medição.
- **A confiança subiu com a revisão, em todas.** Da v1 (R5) à v3 (R7), a média foi de 76,7 a 85,8, e a Faísca, de 64
  a 81. O revisor independente foi de 60 (v2) a 74 (v3) — **o número de fora da reunião fica 12 pontos abaixo do de
  dentro**, e é o que pesa mais na confiança do plano.
- **Quem pega a contradição do próprio plano são o cético e a pragmática:** na R7, Cinza e Lenha apontaram, cada um
  por si, que o portão 1 pedia 100% e dispensava o mesmo requisito no controle de contraste. O Fogareiro, de novo,
  respondeu "nada".
- **O formato falhou uma vez, por culpa da coordenação:** o briefing dizia "no fim do arquivo" e o pedido da rodada,
  "dentro da seção"; três personas puseram o marcador de fim nos dois lugares.

### A proposta de plano (v3.1, 20h45, não aprovada)

> Rascunho da coordenação, montado com as oito rodadas das seis personas e com a revisão de um revisor independente.
> **Nada aqui está decidido**: as decisões são de Anderson, e a seção "Para Anderson decidir" lista as que a sala não
> fechou. A v1 foi revista pelas personas na rodada 5 (marcas "R5"); a v2, pelo revisor independente (marcas
> "revisor"); o símbolo, pela folha de contato das rodadas 6 e 6b (marcas "R6").

#### O objetivo

Aproximar a marca BrzA do tom Carvão em Brasa sem trocar o traçado: **a interface é carvão onde não há trabalho e
brasa onde há** (o agente trabalhando, a mensagem pronta para ir, a pergunta que espera). A cor muda; o símbolo, o
logotipo e as quatro filhas do PLN-007 ficam.

**Pronto quando:** os portões 1 a 4 da fase 5 passam, a flag `brand.brasa` vira padrão, e o símbolo, os lockups e os
ícones saem regerados do gerador (revisor: o "portão 5" da v2 era o próprio padrão, e a condição ficava circular). O
`brand.tokens.json` do CLI e do Workspace fica para uma etapa posterior, ainda sem estimativa (R5, Lenha).

#### A confiança no plano

| Medida | Resultado |
| :----- | :-------- |
| Confiança das seis personas no plano inteiro (R5, sobre a v1) | **média 76,7**; mediana 76,5; de 64 (Faísca) a 88 (Fogareiro) |
| O revisor independente, de fora da reunião, sobre a v2 | 60; com quatro mudanças, ~78 — a v3 incorporou as quatro |
| A previsão das personas, se cada uma tivesse a mudança que pediu | 85,5 — previsão delas, não medida; sem a da Faísca, que não entrou, 83,2 |
| A parte mais forte | fases 0–3 (tokens, ações, movimento): média 83,3 |
| A parte que mais subiu | fase 4 (símbolo): 64,5 na R5 → **79,7** depois da folha de contato e das variantes (R6, R6b) |
| As medições de sucesso | média 68,5 na R5 |
| **A confiança final das personas na v3 (R7)** | **média 85,8**; mediana 85; de 80 (Tição) a 94 (Fogareiro) — todas subiram, a Faísca de 64 para 81 |
| **O revisor independente na v3** | **74** (era 60 na v2); ~82 com três correções — o secundário na origem do placeholder, o placar da decisão 2 e o recrutamento que caiba nos usuários reais —, que a v3.1 incorpora |

**O que a v3 fez com as mudanças pedidas na R5:** entraram as de Tição (as regras de uso no `README` e conferidas no
portão 2), Cinza (a simulação não substitui a pessoa), Lenha (o CLI fora da fase 6) e Fole (o teste de 5 s na fase 0);
a do Fogareiro (um deuteranope obrigatório) entrou na versão do Cinza — sem a pessoa, o portão 4 passa só como piloto
limitado —; e a da Faísca (gerar a C na fase 4) caiu com a folha de contato, que a própria Faísca mediu.

**Como a confiança foi medida:**

- **Voto da sala (rodada 3):** apoio, apoio com ressalva ou contra, com confiança de 0 a 100. **Índice** = média, nas
  seis, de confiança × peso (apoio 1; ressalva 0,7; contra 0). **Acordo** = quantas não votaram contra. Os contras de
  Cinza em P2, P10 e P13 a P15 eram de método ou de valor; a rodada 3 corrigiu o texto sem revoto, e o índice é anterior
  à correção.
- **Evidência:** *medido* — contraste WCAG 2.x e ΔE2000 com simulação de daltonismo (Machado 2009), conferidos pela
  coordenação, pelo script do Cinza e pelo revisor; o **APCA só pelo script do Cinza**, sem confronto com o pacote
  oficial; *lido no código* — arquivo e linha no `brza-studio`; *renderizado* — a folha de contato, no Chrome, não no
  `iconutil`; *suposto* — sem teste.
- **Confiança da coordenação**, pela regra: alta quando índice ≥ 70 **e** evidência medida ou lida; média quando um dos
  dois falta; baixa quando os dois faltam (revisor: a v2 marcava R2 e R10 como altas e R13 como média, contra a regra).

#### O que a sala fechou

| # | Recomendação | Acordo | Índice | Evidência | Confiança |
| :- | :----------- | :----- | :----- | :-------- | :-------- |
| R1 | **Fundo fica `#1A1B1E` (01) e `#2C2D31` (02)**; o calor do carvão vai para o texto e para a 04 na borda do tile. Cinco de seis; a Faísca segue pelo `#171615`, que dá 5,09:1 sob a 07 contra 4,85 do 01 | 5/6 | 67,6 | medido | média |
| R2 | **Rampa de texto quente, separada da superfície:** primário `#E8E2DC`; **secundário e placeholder na mesma origem, `#C4BEB9`**, porque o chat pinta os dois com a mesma `text-chat-foreground-faint`, misturada a 83% (revisor); desabilitado `#7A746F` | 5/6 | 58,8 | medido | média |
| R3 | **Erro e diff removido no rosa frio `#FF7AA2`** (7,02:1; ΔE 22,6 da 07 em deuteranopia, contra 10,3 do erro de hoje), sempre com ícone, texto e o sinal `−`. O valor votado era o `#FF75A0`; a coordenação trocou pela margem de contraste (7,02 contra 6,81; ΔE 0,98 entre os dois), e o script do Cinza auditou o `#FF75A0` | 6/6 | 77,6 | medido | alta |
| R4 | **Aviso no limão `#FACC15`** (ΔE 17,3 contra 12,1 do de hoje, em deuteranopia); no claro, texto neutro, ícone e fundo tingido | 6/6 | 78,0 | medido | alta |
| R5 | **A ação de marca tem token próprio, `--action-brand`**, fora do `--primary` (o ramo de catálogo da segunda camada reescreve o `--primary`: `native-chat-theme-surface-style.ts:38-39`); rótulo sempre `#1A1B1E`; **uma brasa sólida por região — cabeçalho, transcript, composer e o cartão de aprovação** (R5, Faísca), contada no portão 2 | 6/6 | 76,6 | lido no código + medido | alta |
| R6 | **Código em linha sai da 07:** `#FFB088` no escuro (6,79:1 no pior fundo); neutro `#1A1B1E` no claro | 6/6 | 62,5 | medido (sem a caixa real) | média |
| R7 | **Símbolo B, um só, com o núcleo de rescaldo largo** (R6): a chama vai do `#FFB088` no centro (7,74:1 contra o tile, onde a 07 dá 3,88:1) a `#FF6A33`, 07 e 06 na borda, **sem halo abaixo de 128 px**; tray template; os tiles novos (R5, Tição). Pico de luminância no Dock escuro, medido pela Faísca e conferido pela coordenação — 16 px: hoje 142, B chapada 97, **rescaldo largo 142**, topo claro 125; 32 px: 166, 98, 161, 170; 64 px: 177, 98, 171, 189. O rescaldo largo tem o melhor pior caso; a massa quente média segue mais escura que a de hoje (83 contra 96 a 16 px). A C é a pior a 16, 32 e 64 px. **Regra de saída** (Tição, Lenha): se a B ajustada não ler como a de hoje a 16 e 32 px no teste, o símbolo de hoje fica **inteiro** — em todos os tamanhos, para não criar duas leituras — e a brasa muda só a interface (R7, Tição) | 6/6 na R6 | 55,0 | renderizado | média |
| R8 | **O Enviar acende por disponibilidade** (texto ou anexo válido), sem depender do foco; foco de teclado em anel neutro de 2 px com offset de 2 px | 6/6 | **88,0** | lido no código (`native-chat-composer-send-state.ts:39-59`) | alta — a mais forte da reunião |
| R9 | **Movimento:** só o halo da chama focada respira (2,4 s, opacidade); painéis não focados na 06 parada, e na 07 no hover da superfície elevada, onde a 06 cai a 2,72:1 (R5, Cinza); esfria em 600 ms; com `prefers-reduced-motion`, nada anima; sem fagulha, sem modo noturno | 5/6 | 57,3 | medido + suposto | média |
| R10 | **Voz literal no app, conferida por lint; a voz da marca fora dele**, com a assinatura "BrzA — código em brasa". A cópia "Ask Claude…" **não existe no app** — era do protótipo (`build.py:33`); a cópia real vem do upstream e fica | 6/6 | 67,4 | lido no código | média |
| R11 | **Tema claro "Cinza de Fogueira":** papel `#F6F1EC`, texto `#1A1B1E`, secundário `#5C5650`, brasa de texto `#9A3812` (ver tokens), a 07 só como preenchimento | 6/6 | 74,1 | medido | alta |
| R12 | **A Claude se testa antes de implementar, já na fase 0** (R5, Fole): teste pré-registrado de 5 s com os mockups estáticos e a marca de hoje como controle, separando associação de atribuição; 0/5 sucesso, 1/5 observação, ≥ 2/5 investigação e reteste. Oito matizes a ΔE ≤ 5 da 07 chegam no máximo a ΔE 13,7 da Claude, e os mais vermelhos derrubam o rótulo abaixo de 4,5 (revisor) | 5/6 | 52,9 | medido | média |
| R13 | **Portões e métricas** (ver a fase 5 e "As medições") | 5/6 | 50,6–58,5 | — | baixa |

#### A tabela de tokens v3

**O par medido não é o par renderizado (revisor).** O chat mistura as cores de origem antes de pintar: o placeholder
do composer usa `text-chat-foreground-faint` (`NativeChatComposerField.tsx:383`), que mistura a origem a 83% com o
canvas (`main.css:330,358,684-688`) — o `#A8A29E` da v2 vira `#908B88`, 3,58:1 no hover; e o texto do corpo segue o
controle de contraste do usuário (`native-chat-theme.ts:64-69,137-146`, mix de 56% a 100%) — no mínimo, o `#E8E2DC`
rende 4,01 no 02. A tabela abaixo dá a **origem** e, onde há mix, o **efetivo**; o portão 1 mede o efetivo.

| Papel | Escuro | Claro | Pior contraste (E / C) | Mudou |
| :---- | :----- | :---- | :--------------------- | :---- |
| Canvas / elevada | `#1A1B1E` / `#2C2D31` | `#F6F1EC` / `#FFFFFF` (Faísca contra: "papel de impressora") | — | — |
| Divisória decorativa / funcional | `#454446` / `#8E8C90` | `#D9D1C9` / `#82776D` | funcional 3,62 / 3,27 | — |
| Texto primário | origem `#E8E2DC` → efetivo `#BBB6B2` (mix de 78% no contraste padrão) | `#1A1B1E` | 6,00 no hover elevado / 12,88 | **v3.1:** efetivo, não o HEX cru; abaixo do contraste padrão, a escolha é do usuário e fica fora do aceite (R7) |
| Texto secundário e placeholder | origem `#C4BEB9` → efetivo `#A7A29F` (mix de 83%) | `#5C5650` / `#625C56` (a medir com o mix) | 4,77 no hover elevado / 4,93 | **v3.1:** o `#A8A29E` da v2 virava `#908B88`, 3,58 no hover, no secundário e no placeholder |
| Desabilitado | `#7A746F` | `#9C938B` | isento | — |
| Ação: fundo / rótulo | `#FF3D00` / `#1A1B1E` | idem, com contorno `#82776D` no hover | 4,85 (APCA Lc 40,9: decisão 6) | — |
| Ícone ativo | `#D84315`; no hover, `#FF3D00` | `#A83E15` | 3,10 e 3,40 / 4,67 | — |
| Hover sutil | 05 a 22% | 05 a 12% | decorativo | — |
| Brasa como texto | `#FFB088` | **`#9A3812`** | 6,79 / 5,35 no hover do papel; 4,91 no Tokyo Night Light | **v3:** a `#A83E15` dava 4,30 no Tokyo Night Light do catálogo (revisor) |
| Foco | `#BCBCBC`, 2 px + offset 2 px | `#1A1B1E`, idem | 6,36 / 12,88 | — |
| Erro, diff removido | `#FF7AA2` | `#6E3C5A` (a testar) | 4,91 / 6,39 | — |
| Aviso | `#FACC15` | texto e ícone `#1A1B1E`; tint `#FACC15` a 12% | 7,88 / 14,70 | — |
| Link | `#79C0FF` | `#005EA8`, sublinhado | 6,21 / 4,96 | — |
| Código em linha | `#FFB088` | `#1A1B1E` | 6,79 / 12,88 | — |
| Chama: foco / sem foco | degradê 07 → 06 → 05 (decorativo: a parada 05 dá 2,76) / `#8E8C90` | idem / `#625C56` | sem foco 3,62 / 4,93 | o glifo funcional não depende do degradê |
| Trabalhando, não focado | 06 parada; 07 no hover elevado | 05 parada | 3,10 e 3,40 / 4,67 | — |
| Anel de contexto do composer | `#8E8C90` até 90%; brasa só no limiar crítico | idem | a medir | a 06 o tempo todo estourava a cota (R5, Faísca) |

Nota: `#FF7AA2` contra `#FFB088` dá ΔE 14,8 em deuteranopia e 11,3 em tritanopia, e o `#9A3812` contra o erro claro
`#6E3C5A` dá 14,1 em tritanopia; passam porque o código em linha e a brasa de texto não são sinais — se virarem, os
pares se afastam.

#### As fases

| Fase | Entrega | Horas | Reversível | Confiança (R5) |
| :--- | :------ | :---- | :--------- | :------------- |
| 0 · Base | Linha de base da versão atual (tempos de envio, reconhecimento); **os pares efetivos depois dos mixes** (placeholder a 83%, controle de contraste de 56% a 100%) e nos 26 fundos do catálogo (revisor); a caixa do código em linha e os fundos do diff; **o teste de 5 s com os mockups estáticos: a B com o rescaldo largo, a B com o topo claro e a marca de hoje** (R5, Fole; R6) | 5–7 | — | alta |
| 1 · Tokens | Flag `brand.brasa` reativa num arquivo novo, `NC/brza/use-brza-brand-pilot.ts` (proposto pela Lenha); os primitivos `--brz-*` num arquivo próprio, `brza-brand.css`, para reduzir o conflito com o upstream (R5, Tição); **os semânticos entram pela composição do objeto inline** (`native-chat-appearance-style.ts:88-90`), porque uma folha de estilo não vence o estilo inline que a segunda camada põe na raiz (`NativeChatStructuredSession.tsx:276`) — vale também para o BrzA Dark, que passa pelo ramo de catálogo (revisor; a Lenha já tinha avisado); `--action-brand` no `@theme inline` de `main.css:99-103`; a matriz padrão, BrzA Dark e catálogo, em esquemas opostos, com o editor Markdown fora (R5, Lenha) | 4–6 | sim | alta |
| 2 · Ações | Variante `brand` em `ui/button.tsx` (sem trocar o `default`); Enviar, Continue, Allow, Submit; código em linha; foco; **condicionar à flag a regra de `main.css:1207-1211`**, que pinta o Enviar com o degradê e o branco no foco — a borda do composer em foco (`:1199-1205`) fica, pela regra 5 do Tição (revisor) | 3–5 | sim | alta |
| 3 · Movimento | Halo no cabeçalho focado (`data-native-chat-working`), 06 nos não focados, esfriar em 600 ms, `prefers-reduced-motion`; teste de "brasa presa" | 2–4 | sim | média |
| 4 · Símbolo | A B com o rescaldo largo no gerador `brza-brand-build.mjs` e no `generate.sh` (fonte por tamanho lógico, sem halo abaixo de 128 px); tiles 02 → 01 e o claro `#FFFFFF` → `#F6F1EC`; previews nativos (`iconutil`) a 13/16/32 px em 1× e 2×, contra a de hoje; lockups com `#E8E2DC` e `#A8A29E`; **as oito regras de uso da brasa e a tabela por tamanho no `resources/brand/README.md`** (R5, Tição). As variantes renderizadas estão em `.sessions/reuniao-brasa/entregas/simbolo/` (`BR2-sem-halo.svg`, o rescaldo largo; `BT-sem-halo.svg`, o topo claro) | 3–5 | previews sim | média (R6) |
| 5 · Portões | **(1)** um auditor que **lê os pares efetivos do app** — estilos computados das fixtures das oito cenas, no contraste padrão, nos dois temas, no BrzA Dark e nos 26 fundos do catálogo — e **sai com erro** quando um par reprova: texto ≥ 4,5, ícone ≥ 3, ΔE ≥ 15 entre sinais nas três deficiências, como triagem; o script do Cinza vira a tabela de referência, não o portão (revisor: ele tem os HEX fixos e sai com 0 com 31 reprovações); mais o lint das strings do app (`queim`, `brasa`, `🔥`) (R5, Fole). **(2)** As oito cenas em `grayscale(1)`, com critério de forma e texto e revisão humana; a cota de uma brasa por região contada; as oito regras de uso do Tição conferidas. **(3)** A flag por duas semanas no uso de Anderson, com o ensaio de reversão no meio de um turno; **passa se** a flag não foi desligada por desconforto ou defeito, não houve brasa presa nem regressão de contraste, e cada incômodo anotado foi corrigido ou virou issue. **(4)** O teste com cinco pessoas (ver "As medições"). Passados os quatro, a flag vira padrão | 6–10 | sim | média |
| 6 · Ativos | Empacotamento dos ícones (`icns`, `ico`, tray), lockups das quatro filhas; nota de lançamento com o par cinza → brasa e a regra de captura: toda imagem pública mostra um turno vivo (R5, Fole) | 2–4 | não | média |
| Depois | `brand.tokens.json`, a brasa no BrzA CLI (ANSI 202 de reserva) e no Workspace | a estimar | — | — |

**Total: 25–41 h.** O mapa da Lenha dava 20–33 h; a coordenação somou o teste antecipado (~2 h), os pares efetivos
(~1–2 h) e o auditor que lê o app (~2–4 h) — **esse acréscimo é estimativa da coordenação, não da Lenha**. Exclui as
duas semanas da flag, o recrutamento, o retrabalho e o CLI.

#### As medições de sucesso

| Medida | Meta | Quando |
| :----- | :--- | :----- |
| Pares efetivos de texto ≥ 4,5:1 e de ícone ≥ 3:1, no contraste padrão, nos dois temas, no BrzA Dark e no catálogo | 100% | portão 1, a cada PR |
| Strings do app sem metáfora de fogo em estado, erro, permissão ou cobrança | 0 ocorrências | portão 1 |
| Cenas que funcionam em cinza; cota de uma brasa por região | 8/8; 0 regiões com duas | portão 2 |
| Reconhecimento: a marca aparece uma vez; depois, **o símbolo isolado entre seis chamas de produtos de IA** (ideia da Faísca na R1) | ≥ 4/5 acham o BrzA | fase 0 e portão 4 |
| Associação em 5 s (com wordmark): descrevem como brasa, fogo, carvão ou calor | ≥ 4/5, comparado à marca de hoje | fase 0 e portão 4 |
| Atribuição à Claude, com a marca de hoje como controle | 0/5 sucesso; 1/5 observação; ≥ 2/5 investigação | fase 0 e portão 4 |
| Confusão entre CTA e erro | 0 | portão 4 |
| Tempo até o primeiro envio, contra a base | sem piora clara; a mediana se registra (com cinco pessoas, ±10% fica no ruído — revisor) | portão 4 |
| Desconforto relatado (perguntado, não espontâneo) | cada relato corrigido ou com issue | portão 3 |

- **Quem participa:** o BrzA não tem dez usuários além de Anderson (revisor). A fase 0 e o portão 4 usam devs que não
  usam o BrzA, cinco em cada um e **pessoas diferentes**, senão o portão mede memória; o uso real é o de Anderson, no
  portão 3.
- **Daltonismo:** o portão 4 recruta ao menos uma pessoa com deuteranopia (Fogareiro). Sem ela, o portão passa só como
  piloto limitado, com "validação com pessoas com deficiência de cor: pendente" registrada — a simulação **não**
  substitui a pessoa (Cinza). Cinco pessoas são sinal, não validação.

#### Os riscos

- **O laranja da Claude:** a 07 está a ΔE 11,8 do `#D97757`; a brasa de hoje (`#f26228`) já está a 7,9. A mudança
  afasta, mas não separa, e nenhum matiz vizinho separa sem derrubar o rótulo.
- **O par renderizado não é o par medido:** os mixes e o controle de contraste do usuário mudam a cor de origem. O
  portão 1 mede o efetivo **no contraste padrão**; o controle abaixo do padrão (até 56%, que rende 4,01) é escolha do usuário, **fica fora do aceite** e se registra como limite conhecido (R7, Cinza, Lenha: como estava, o auditor podia barrar o próprio lançamento).
- **O rosa no erro quebra o reflexo "vermelho = erro"** — por isso ícone, texto e sinal `−` são obrigatórios.
- **O símbolo pequeno perde para o de hoje:** a B ajustada chega "quase" à leitura de hoje a 16 px nas seis avaliações;
  a regra de saída protege o pequeno.
- **O conflito com o upstream** (R5, Tição): as fases 1 e 2 tocam `main.css`, `ui/button.tsx` e a composição de tema.
- **A vitrine apaga a marca** (R5, Fole): com a brasa só no que está vivo, toda captura em repouso mostra um app cinza.
- **O APCA do rótulo da ação** (Lc 40,9) — ver a decisão 6.

#### Para Anderson decidir — com o voto das personas

| Decisão | Opções e votos | Recomendação da coordenação |
| :------ | :------------- | :-------------------------- |
| 1. O estado no tray e no Dock | adiar — Tição, Cinza, Lenha; o núcleo do Dock acende enquanto trabalha — Fole, Faísca; ponto estático no tray — Fogareiro. O tray já tem um estado de atenção âmbar (`system-tray.ts:64-93`) | adiar |
| 2. O símbolo | depois da folha de contato (R6b), empate: B com o rescaldo largo, sem halo — Fole, Faísca (pelo pico medido); B com o topo claro, sem halo — Tição, Lenha, Fogareiro (a olho); o rescaldo largo no pequeno e o topo claro a 64 px — Cinza. A C saiu da disputa | B com o rescaldo largo em todos os tamanhos, pelo pior caso medido (161 contra 166 de hoje; o topo claro cai a 125 no 16 px); o topo claro como segundo braço do teste da fase 0 |
| 3. A flag | duas semanas no seu uso — cinco; um dia de cinza e padrão — Faísca | duas semanas |
| 4. O fundo | `#1A1B1E` — cinco; `#171615` — Faísca | `#1A1B1E` |
| 5. Onde o plano mora | `brand`, ao lado do PLN-007 — seis de seis | `brand` |
| 6. A norma do rótulo da ação (revisor) | WCAG 2.x, com rótulo escuro (4,85) e o APCA como aviso — Tição, Cinza, Lenha, Fogareiro, Fole; rótulo de 16 px com peso 700 — Faísca; APCA, com rótulo branco (Lc −66,7, mas 3,55 no WCAG, que reprova o portão 1) — ninguém | WCAG 2.x com rótulo escuro |

### As issues abertas

- [O erro e o aviso saem do matiz da brasa](../issues/erro-e-aviso-fora-do-matiz-da-brasa.md) — `high`
- [A ação de marca tem token próprio, fora do `--primary`](../issues/token-proprio-da-acao-de-marca-fora-do-primary.md) — `high`
- [A rampa de texto quente, separada da rampa de superfície](../issues/rampa-de-texto-quente-separada-da-superficie.md) — `high`
- [A auditoria automática de contraste e daltonismo dos tokens](../issues/auditoria-automatica-de-contraste-e-daltonismo-dos-tokens.md) — `high`
- [O Enviar acende por disponibilidade, e o foco é um anel neutro](../issues/enviar-acende-por-disponibilidade-e-foco-neutro.md) — `medium`
- [O tema claro "Cinza de Fogueira"](../issues/tema-claro-cinza-de-fogueira.md) — `medium`
- [O símbolo B por tamanho e os ativos regerados](../issues/simbolo-b-por-tamanho-e-ativos-regerados.md) — `medium`
- [A brasa que respira e esfria no "trabalhando"](../issues/brasa-que-respira-e-esfria-no-trabalhando.md) — `medium`
- [A brasa se confunde com o laranja da Claude?](../issues/teste-de-reconhecimento-da-brasa-contra-a-claude.md) — `medium`, investigação
- [A reunião multiagente com personas pelo `brza sessions`](../issues/reuniao-multiagente-com-personas-pelo-brza-sessions.md) — `medium`
- [A brasa nas quatro filhas, com tokens compartilhados e o CLI](../issues/brasa-nas-quatro-filhas-com-tokens-compartilhados-e-cli.md) — `low`
- [A assinatura e a voz da marca Carvão em Brasa](../issues/assinatura-e-voz-da-marca-carvao-em-brasa.md) — `low`
- [As ideias ousadas da reunião Carvão em Brasa](../issues/ideias-ousadas-da-reuniao-carvao-em-brasa.md) — `low`

## O que ficou

- **A proposta de plano espera Anderson:** as seis decisões da tabela "Para Anderson decidir" e a aprovação do texto.
  Aprovada, ela vira um PLN no workstream `brand` (seis de seis personas), pela skill `plan-runner`, ao lado do PLN-007.
- **O `brza shot` quebrado** entra na issue do fluxo da reunião, e cabe ao `tools-kit`.
- **A contestação da Faísca sobre os picos de 64 px** fica registrada acima; não muda a recomendação, que se decide no
  16 px.
- **As seis sessões seguem abertas** no BrzA Studio, para consulta; fecham com `brza sessions close reuniao-brasa-<nome>`.
- **O material da reunião fica fora do git**, em `.sessions/reuniao-brasa/` no worktree do `playground`: o briefing, as
  personas, os pedidos das oito rodadas, as sínteses, a proposta de plano, o script de auditoria do Cinza e a folha de
  contato do símbolo.

## Fora do workspace

- **O quê e onde:** seis sessões de chat abertas no BrzA Studio (`reuniao-brasa-ticao`, `-faisca`, `-cinza`, `-lenha`,
  `-fogareiro`, `-fole`), duas no Claude, duas no Codex, uma no Grok e uma no Antigravity. **O risco:** consomem cota
  dos quatro runtimes enquanto recebem mensagem; paradas, só ocupam abas. **Estado:** abertas e paradas. **Como
  desfazer:** `brza sessions close reuniao-brasa-<nome>`.
