---
scope:
  - brza-studio
tags:
  - design
refs:
  - PLN-007
---

# Reunião Carvão em Brasa: a contraprova de Faísca, a Provocadora, em outro modelo

O pedido de Anderson, em 2026-11-07, na sessão da coordenação ("Rebranding BrzA: Carvão em Brasa"), depois das sete
rodadas: "ajuste o modelo/esforço do agente/sessão, para ficar condizente com o papel dele na reunião; tente
diversificar o máximo o uso de modelo/esforço". Esta é uma sessão nova, de contexto limpo, da persona **Faísca** — a Provocadora —
no agente Grok, com o modelo `grok-4.7-build-fast` e esforço `low` (na reunião, grok-4.7 xhigh). Ela refaz às cegas a rodada 1 e mede a
confiança na proposta de plano, para comparar a mesma persona em outro modelo.

## O que se fez

### Rodada 1: opinião inicial

#### 1. Carvão, a base neutra

- **Posição:** O `#1A1B1E` é cinza de escritório com um sopro frio; o canvas vira `#14110F` e o grafite atual vira o estado apagado.
- **Por quê:** Li no briefing que o azul é o maior canal do `#1A1B1E`, e na paleta de `brasa/brasa.png` o 01 parece grafite de UI, não carvão. A 03 a 1,8:1 sobre o 01 não serve de texto (briefing; o protótipo fugiu para `#BCBCBC`). Suponho que um canvas mais quente e mais escuro segura a brasa sem pintar a tela de laranja.
- **Ideias:**
  - Token `--coal-canvas: #14110F` no fundo do chat; `--coal-ash: #1A1B1E` só em superfície sem foco. `(ousadia: média)`
  - Tema claro não inverte a rampa: folha `#F6F1EC` com uma borda queimada de 8 px em `#6B554B` → `#A83E15` no composer, como papel na beira da brasa. `(ousadia: alta)`
- **Risco:** O canvas quente suja syntax highlight e foto; a rampa nova não foi medida.
- **Confiança:** 74/100

#### 2. Brasa, a escala quente, a semântica e o contraste

- **Posição:** A 07 é o único laranja de ação, com tinta `#1A1410`; erro sai da família e vira rosa frio.
- **Por quê:** Branco sobre `#FF3D00` é 3,5:1 (briefing e a legenda de `brasa/brasa.png`); no mock o botão já usa seta escura. O erro `#ff6568` cola na Incandescente (briefing e `brasa-chat-8`). Suponho que calor = verbo e frio = falha, senão "Continue" e "não deu" são a mesma cor com rótulos diferentes.
- **Ideias:**
  - `--on-ember: #1A1410` no rótulo do CTA 07; branco fica proibido em texto normal sobre a 07. `(ousadia: baixa)`
  - `--status-error: #FF4D8D` no lugar de `#ff6568`; aviso desce de `#eab308` para `#C9A24A` para não gritar junto. `(ousadia: média)`
  - Lei da tela: um só bloco em `#FF3D00` por vista. O resto da escala quente fica em ícone de 16 px ou morre. `(ousadia: alta)`
- **Risco:** Tinta escura em botão pequeno come no antialias; rosa de erro parece produto alheio.
- **Confiança:** 80/100

#### 3. O símbolo

- **Posição:** C. A é adesivo com glow; B é o símbolo de hoje, só mais quente no miolo.
- **Por quê:** Em `simbolo/C.png` a crosta vai da Oculta à Cinza Aquecido e a Incandescente aparece por dentro, com três fagulhas. A e B (`simbolo/A.png`, `B.png`) acendem o tile ou o halo e, a 16 px, viram a mesma mancha laranja. Suponho que a história "carvão com fogo dentro" só existe se a crosta sobreviver; abaixo de 24 px ela não sobrevive.
- **Ideias:**
  - C no ícone do app e no lockup a partir de 24 px; abaixo disso, glifo D: chama sem fagulha, núcleo `#FF3D00`, crosta `#6B554B`, sem halo. `(ousadia: média)`
  - Ícone da dock nasce apagado (`#2C2D31` + crosta `#6B554B`) e o miolo `#FF3D00` acende só enquanto há turno. O tray do macOS mostra estado, não um selo. `(ousadia: alta)`
- **Risco:** A 16 px o C desaba no A; ícone vivo briga com o cache do macOS e some numa dock cheia.
- **Confiança:** 68/100

#### 4. A brasa viva na interface

- **Posição:** O Enviar fica carvão até existir rascunho; aceso o tempo todo, o foco não tem o que contar.
- **Por quê:** A legenda de `brasa-chat-7` admite que, com o primário laranja sempre, o foco muda menos. Hoje o Enviar é cinza e só ganha a marca no foco (briefing). Em `brasa-chat-5` a chama de 18 px treme no degradê e o Parar em 06 a 14% deixa o ícone em 2,8:1 se for para a 05. Suponho que brasa é evento, não wallpaper.
- **Ideias:**
  - Enviar em repouso: fundo `#2C2D31`, seta `#8E8C90`. Com rascunho: fundo `#FF3D00`, seta `#1A1410`. No foco, anel de 1 px `#FF3D00` a 100% e brilho externo a 12%, como o mock já testa. `(ousadia: média)`
  - "Trabalhando": a chama de 18 px respira opacidade 0,65→1 em 2,4 s, uma fagulha, sem degradê no rótulo. Parar usa `#D84315` sólido, não 14%. `(ousadia: baixa)`
  - Aos 90 s sem foco o chrome esfria para `#8E8C90` e só a borda do composer permanece `#A83E15`. A app vai para a brasa coberta. `(ousadia: alta)`
- **Risco:** Enviar apagado parece desabilitado; movimento competir com o texto; esfriar o chrome esconde o produto.
- **Confiança:** 73/100

#### 5. Narrativa, voz e rollout

- **Posição:** A voz fala como quem cuida do fogo, os tokens ganham nome de matéria, e o lançamento é uma noite só no ícone, no "A" e no Enviar.
- **Por quê:** O briefing pede conceito na microcópia e um jeito de medir. A paleta está numerada 01–07 em `brasa/brasa.png`, nome de planilha. Suponho que "Brasa" na interface é muleta: se a cor não se explica sozinha, o rebranding não aconteceu.
- **Ideias:**
  - Tokens `--coal-canvas`, `--ember-crust` (`#A83E15`), `--ember-core` (`#FF3D00`). Microcópia: "A brasa está acesa" no lugar de "Working"; erro em rosa, frase fria, sem metáfora de fogo. `(ousadia: média)`
  - Trinta dias sem a palavra "brasa" na UI. Métrica: 12 pessoas, 5 segundos no ícone C sem wordmark; sucesso se 9 dizem fogo, brasa ou carvão. `(ousadia: alta)`
- **Risco:** Metáfora envelhece no erro e no aviso; renomear token quebra tema. A amostra de 12 mente com facilidade.
- **Confiança:** 62/100

#### A ideia mais ousada desta rodada

O ícone da dock é carvão apagado e o miolo `#FF3D00` só acende com turno vivo: a marca vira estado, não adesivo. Risco: some na dock, destoa do screenshot da loja, e o macOS guarda o ícone velho.

#### Issues candidatas

- **Canvas `#14110F` e grafite `#1A1B1E` só no apagado** — o 01 medido é frio e a 03 não serve de texto — prioridade `high`
- **CTA 07 com tinta `#1A1410` e erro `#FF4D8D`** — branco na 07 fica em 3,5:1 e o vermelho atual cola na brasa — prioridade `high`
- **Símbolo C desde 24 px e glifo sem fagulha abaixo disso** — a crosta é a história e a 16 px ela morre — prioridade `medium`
- **Enviar acende com rascunho; Parar em `#D84315` sólido** — laranja permanente anula o foco e o Parar a 14% falha o ícone — prioridade `medium`
- **Tokens por matéria e teste de 5 segundos com 12 pessoas** — número 01–07 não é voz, e sem métrica o rollout é gosto — prioridade `low`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Carvão | Canvas `#14110F`; o `#1A1B1E` vira cinza apagado | 74 |
| 2. Brasa | Um laranja de ação, tinta escura, erro em rosa frio | 80 |
| 3. Símbolo | C a partir de 24 px; glifo seco abaixo; dock acende com o turno | 68 |
| 4. Interface | Enviar apagado até o rascunho; brasa respira só no trabalhando | 73 |
| 5. Narrativa e rollout | Voz de matéria, uma noite, 9/12 reconhecem fogo em 5 s | 62 |

<!-- fim-rodada-1 -->

### Rodada 2: a confiança na proposta de plano

#### A confiança

| Parte | Confiança (0–100) | Uma linha |
| :---- | :---------------- | :-------- |
| O plano inteiro | 78 | Carvão parado e brasa no verbo; o símbolo virou sobrevivente de 16 px |
| Tabela de tokens | 84 | Pares efetivos, rótulo `#1A1B1E` na 07, erro `#FF7AA2` medido |
| Fases 0–3 (tokens, ações, movimento) | 86 | Enviar por disponibilidade é a R8, a mais viva do plano |
| Fase 4 (símbolo) | 70 | B com rescaldo largo ganha no pico; a crosta da C morreu no número |
| Fases 5–6 (portões, ativos) | 64 | O portão 4 promove um sinal de cinco pessoas a padrão |
| As medições de sucesso | 66 | O teste de 5 s e o controle da Claude prestam; n=5 não fecha |

#### Onde a proposta diverge da sua rodada 1

- Canvas: defendi `#14110F`. A sala ficou no `#1A1B1E` (R1, índice 67,6). Não me convenceu no matiz — o briefing ainda diz que o azul é o maior canal — mas não travo o plano por 0,2 de contraste.
- Símbolo: defendi C. A tabela de luminância da R7 mostra a C pior a 16, 32 e 64 px, e o rescaldo largo empata o pico de hoje (142 a 16 px). Mudei: B com rescaldo largo. A história da crosta não cabe no tamanho que a dock usa.
- Voz e movimento: pedi "A brasa está acesa", fagulha e chrome que esfria aos 90 s. O lint da R10 e a R9 (sem fagulha, sem modo noturno) me convencem; metáfora no erro era o risco que eu mesma escrevi.

#### O erro que a proposta ainda tem

O portão 4, com cinco pessoas, é o que faz a flag virar padrão (fase 5), e o mesmo texto diz que cinco pessoas são sinal, não validação. Um sinal não deveria ser a chave do padrão.

#### O seu voto nas decisões de Anderson

| Decisão | Opção | Confiança |
| :------ | :---- | :-------- |
| 1. Tray e Dock | O núcleo do Dock acende enquanto trabalha; o tray fica template, sem ponto | 63 |
| 2. Símbolo | B com o rescaldo largo em todos os tamanhos | 74 |
| 3. Flag | Um dia de cinza e padrão, não duas semanas | 58 |
| 4. Fundo | `#171615`, o passo quente que a sala mediu (5,09:1 sob a 07) | 61 |
| 5. Onde o plano mora | `brand`, ao lado do PLN-007 | 86 |
| 6. Norma do rótulo da ação | WCAG 2.x com rótulo escuro; APCA só como aviso | 84 |

<!-- fim-rodada-2 -->

## O que ficou

## Fora do workspace

Nada.
