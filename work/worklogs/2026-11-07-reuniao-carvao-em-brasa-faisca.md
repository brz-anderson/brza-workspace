---
scope:
  - brza-studio
tags:
  - design
refs:
  - PLN-007
---

# Reunião Carvão em Brasa: a participação de Faísca, a Provocadora

O pedido de Anderson, em 2026-11-07, na sessão da coordenação ("Rebranding BrzA: Carvão em Brasa"): "coordenar uma
reunião de rebranding da marca BrzA (…) se aproximar mais do tom Carvão em Brasa, com um grafite mais próximo ao carvão e
tons em brasa incandescente". Este é o registro de **Faísca** — persona a Provocadora, no agente Grok —, aberto pela coordenação com
`brza sessions reuniao-brasa-faisca`. A pauta e as regras estão no briefing da reunião; cada rodada é uma seção abaixo.

## O que se fez

### Rodada 1: opinião inicial

#### 1. Carvão, a base neutra

- **Posição:** O canvas deixa o grafite frio e vira carvão `#14110F` (`--coal-canvas`); o tema claro vira papel de cinzas `#F3EBE4` (`--ash-paper`).
- **Por quê:** No briefing, `#1A1B1E` tem o azul como maior canal (26, 27, 30) e a etapa 03 `#454446` sobre a 01 dá 1,8:1. O protótipo, no `brasa.png`, foge para `#BCBCBC` (9,1:1), fora da paleta, e o lockup claro senta em branco de impressora. Calculei nesta rodada: `#C4B8B0` sobre `#14110F` dá 9,7:1 e `#1A1410` sobre `#F3EBE4` dá 15,5:1. Suposição: o esquema `light` continua no chat (componentes.md, F59); o que acaba é o branco `#fff`.
- **Ideias:**
  - `--coal-canvas: #14110F`, superfície `--coal-raised: #241E1B`, texto secundário `--ash-ink: #C4B8B0`. A 04 `#6B554B` fica na crosta do símbolo: sobre o canvas novo ela dá 2,7:1, então não entra em texto. `(ousadia: média)`
  - E se o claro não fosse claro? Papel `--ash-paper: #F3EBE4`, tinta `#1A1410`, secundário `#5C463C` (7,4:1 nesse papel), cartão `#E7DDD4`. O lockup branco do `brasa.png` sai do material. `(ousadia: alta)`
- **Risco:** Canvas quente briga com o tema de terminal, que reescreve o fundo do chat (`nativeChatThemeSurfaceStyle`, F61). Papel de cinzas pode parecer sujo para quem espera o `#fff` de `main.css`.
- **Confiança:** 76/100

#### 2. Brasa, a escala quente, a semântica e o contraste

- **Posição:** A 07 `#FF3D00` é faísca de ação, com rótulo `#1A1410`; código, aviso e erro usam outros matizes.
- **Por quê:** O briefing mede branco sobre a 07 em 3,5:1 e sobre a 06 em 4,4:1. Calculei `#1A1410` sobre `#FF3D00` = 5,1:1. `#ff6568` sobre `#FF3D00` dá 1,24:1, e o diff removido `#c74e39` sobre `#D84315` dá 1,03:1: erro e brasa são o mesmo calor. Vi a colisão no artboard 8 e o código em linha na 07 no artboard 3. Suposição: "quebrado" pede um matiz frio.
- **Ideias:**
  - `--ember-spark: #FF3D00` com `--coal-ink: #1A1410` no Enviar com rascunho, no Allow once, no Submit e no Continue. A 06 não carrega texto de 14px (4,2:1 no canvas `#14110F`). `(ousadia: média)`
  - Cota de uma faísca por região (cabeçalho, transcript, composer). Código em linha sai da 07 para `--ember-code: #FFB088` (8,6:1 sobre `#2C2420`). Erro e diff removido vão para `--fault-rose: #FF7A9A` (5,6:1 sobre o cartão `#2C2D31`). Aviso `--warning-gold: #F4B000` (7,2:1 nesse cartão). O link fica `#79c0ff`, como no artboard 3. `(ousadia: alta)`
- **Risco:** A rosa pode parecer cosmética numa forja. No artboard 6, Allow e a linha da pergunta acendem juntos; a cota por região segura os dois, uma cota da tela inteira não. Quem lê alerta como vermelho clássico perde o sinal.
- **Confiança:** 81/100

#### 3. O símbolo

- **Posição:** Outra. C da 24px para cima; abaixo, o glifo D, uma fresta só, sem circuito, sem `{}` e sem as três fagulhas.
- **Por quê:** Vi `simbolo/A.png`, `B.png` e `C.png`. A acende o tile por baixo e cai na chama que todo produto de IA já tem. B espalha halo e o 16px vira mancha. C é o desenho que é carvão: crosta da Oculta para a Cinza Aquecido, calor da 07 por dentro. Nas três, o 16px perde o circuito. Suposição, de olho no quadro, sem medir pixel: a chama do painel tem 13px (F12) e o tray vive nessa escala. Outra suposição: o ícone de app é uma peça só.
- **Ideias:**
  - C no estado vazio (48px, artboard 2) e nos lockups: crosta `#A83E15` → `#6B554B`, fresta `#FF3D00`, tile `#14110F`. As três fagulhas só a partir de 48px. `(ousadia: média)`
  - D, máscara `--symbol-spark`, para 13–16px e para o tray. Repouso do tray em `#8E8C90`; a fresta `#FF3D00` abre só com turno vivo. O circuito do PLN-007 fica no tamanho em que ainda é circuito. `(ousadia: alta)`
- **Risco:** D esconde o circuito no dock, onde a marca é mais vista. Fagulha de C a 32px ainda suja o contorno. Tray colorido briga com ícone template do macOS; não verifiquei esse código.
- **Confiança:** 64/100

#### 4. A brasa viva na interface

- **Posição:** Brasa é estado. O Enviar em repouso é carvão; `#FF3D00` entra quando há rascunho, aprovação ou turno vivo.
- **Por quê:** No artboard 7 o Enviar já nasce na 07 e o foco só ganha borda em degradê; a legenda admite que o foco muda menos. O app hoje faz o inverso: cinza em repouso, `--brand-gradient` no foco (F50, `data-brza-send`). A chama sem foco do artboard 1 é `#8E8C90`; a de 18px tremula no degradê e a régua fica cinza (artboard 5). Suposição: o gancho `prefers-reduced-motion` que já para o flicker (F36) também para qualquer respiração nova.
- **Ideias:**
  - Enviar, círculo de 32px: repouso `--coal-raised` com arco de 2px em `#A83E15` e seta `#C4B8B0`; com texto no campo, miolo `#FF3D00` e seta `#1A1410`. A chama de 18px troca o skew de ±3% (F36) por respiração do núcleo, opacidade 0,65 a 1. Sem movimento, núcleo sólido. `(ousadia: alta)`
  - E se a sala inteira esquentasse? Em turno vivo o canvas anda de `#14110F` para `#1C1210` em 8s, com um radial `#FF3D00` a 4% atrás da linha de atividade, e esfria em 1,2s. Deixo na mesa e não defendo: F61 reescreve esse canvas a cada tema. `(ousadia: alta)`
- **Risco:** Enviar apagado com o campo vazio parece botão morto, e a primeira sessão perde o clique. O arco de `#A83E15` sobre `#14110F` dá 3,0:1, no limite de ícone; se falhar, o repouso some.
- **Confiança:** 73/100

#### 5. Narrativa, voz e rollout

- **Posição:** Hex sem voz é fantasia. Três frases nossas carregam "Carvão em Brasa", e a 07 mora num token que o tema de terminal não lava.
- **Por quê:** Os artboards 2 e 7 ainda dizem "Start a conversation with Claude" e "Ask Claude to do anything…". A cópia real está em `NATIVE_CHAT_EMPTY_STATE_COPY`, que o levantamento não abriu. Suposição: o inglês do artboard é o produto. F61 põe `--primary` no foreground do tema, não na marca: pintar `--primary` de `#FF3D00` incendeia o catálogo.
- **Ideias:**
  - Vazio, com a chama C em crosta (fresta na 05, ainda fria): "A brasa está fria." e "Descreva o que vai queimar." Composer: "O que vai para a brasa?" Turno vivo: "A brasa está viva." Tokens: `--coal-canvas`, `--ash-paper`, `--ember-spark`, `--ember-code`, `--fault-rose`. `--primary` fica como está. `(ousadia: alta)`
  - Três noites, três diffs: símbolo C/D e wordmark; Enviar e chama viva; canvas e papel de cinzas. Métrica: 12 pessoas que já conhecem a marca, 5 segundos, 6 chamas de IA na mesa; sucesso é 9 ou mais apontando a crosta C. Trava de 14 dias: o primeiro clique em `[data-brza-send]` não cai mais que 5% contra a semana anterior. Suposição: a taxa ainda não existe; o atributo sim (F50). `(ousadia: média)`
- **Risco:** Metáfora de fogo enjoa no segundo dia e quebra para quem usa o app em inglês. Três noites atrasam um diff único. O teste de 12 pessoas não mede contraste nem clique.
- **Confiança:** 58/100

#### A ideia mais ousada desta rodada

O ícone da dock nasce apagado: glifo D, crosta `#6B554B`, fresta fechada. Com turno vivo a fresta `#FF3D00` abre; ao terminar, esfria em 1,2s. O tray repete o gesto, de `#8E8C90` para a mesma fresta. Risco: o macOS troca a imagem do dock e não anima; a fresta parece badge de erro; com reduced-motion, se o app abrir no meio do turno, o ícone fica na fresta. Suposição: não li o código do ícone de app, só a chama de 13px do painel (F12).

#### Issues candidatas

- **Carvão `#14110F` no canvas e papel de cinzas `#F3EBE4` no claro** — o `#1A1B1E` é frio e a etapa 03 dá 1,8:1 como texto — prioridade `high`
- **Token `--ember-spark` com rótulo `#1A1410`, fora do `--primary`** — branco na 07 dá 3,5:1 e o primary dos temas não é a marca — prioridade `high`
- **Símbolo C da 24px para cima e glifo D abaixo** — circuito e fagulhas somem no 16px dos três quadros — prioridade `high`
- **Erro e diff removido em `--fault-rose: #FF7A9A`** — `#ff6568` sobre `#FF3D00` dá 1,24:1, o mesmo calor — prioridade `high`
- **Enviar em carvão até existir rascunho** — a 07 em repouso faz o foco do artboard 7 mudar pouco — prioridade `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Carvão | Canvas `#14110F` e claro em papel de cinzas `#F3EBE4`; a 03 sai do texto | 76 |
| 2. Brasa | A 07 é ação, com tinta `#1A1410`; erro e diff vão para a rosa | 81 |
| 3. Símbolo | C da 24px para cima; glifo D, sem circuito, no miúdo e no tray | 64 |
| 4. Interface | O Enviar acende com rascunho; a chama respira; o canvas fica quieto | 73 |
| 5. Narrativa e rollout | Três frases da brasa, token próprio, meta de 9 em 12 no teste de 5s | 58 |

<!-- fim-rodada-1 -->

### Rodada 2: debate

A sala esfriou o carvão para ganhar 0,04 e calou a voz para não parecer boba. Os dois consensos estão mornos. O dado de daltonismo, esse sim, eu assino.

#### As disputas

- **D1:** (c) — Tição mediu 5,09:1 de `#171615` sob a 07 e a sala enterrou o (c) com a conta do (b): 4,89 contra 4,85. O azul do `#1A1B1E` (26, 27, 30) não faz a brasa saltar; faz a marca parecer o dark mode de qualquer um. O claro eu aceito na faixa da C4, `#F3F1EE`. — 78/100
- **D2:** (b) `#A8A29E` — 6,83 no 01 e 5,45 no 02, na síntese. Meu `#C4B8B0` foi medido noutro canvas; no cartão eu não tenho o número, então não invento. Este cinza não é o calor da marca. — 70/100
- **D3:** (b) `#FF7AA2` — o melhor par da tabela: ΔE 22,6 em deuteranopia e 7,02:1 no 01. O carmesim do Fogareiro cai a 11,4. Meu `#FF7A9A` era a família certa, sem este ΔE. — 90/100
- **D4:** (c) `#FACC15` — `#eab308` dá 12,1 em deuteranopia e `#F5B841` dá 13,7; o limão dá 17,3 e 11,25:1. Feio numa forja. Pior é o aviso lido como brasa. — 78/100
- **D5:** outra: C a partir de 48px, o vazio (F14); abaixo, fresta chapada, sem núcleo de B; tray template. O corte de 64px do Fole esconde a C na tela em que a marca se apresenta. Tição escreveu na R1 que B é o menos memorável e, na R2, votou B. — 68/100
- **D6:** outra: respirar e esfriar em 600ms no painel ativo, e o Dock acende e apaga no mesmo estado. Sem fagulha por ferramenta. Sem Brasa Noturna: Fole mediu `#E05A20` a ΔE 8,7 da Claude, mais perto que a 07. — 72/100
- **D7:** (b) — uma frase, só no vazio: "A brasa está fria." "Acesa", a frase da R1 de Tição, mente quando o Enviar nasce carvão. "Trabalhando", erro e permissão ficam literais. A sala proibiu metáfora até na única frase que não é operação. — 66/100
- **D8:** (a) — Fole mediu `#FF2E1A` a ΔE 12,4 da Claude, contra 11,8 da 07. Deslocar o matiz não separa. A separação é a 07 rara (C5), não um teste de cinco pessoas que não muda o grau. — 74/100
- **D9:** outra: um dia de cinza, o ensaio de Cinza, e no dia seguinte a brasa é o padrão. Flag de duas semanas no uso de Anderson mede um gosto e chama de rollout. — 63/100

#### Os ataques

1. **Tição, carvão (D1).** O consenso (a) é a conta errada repetida quatro vezes. O ganho de 0,04 é do `#1C1A19`; o `#171615` chega a 5,09:1 sob a 07, e o briefing já disse que o azul é o maior canal. Fundo frio "para a brasa saltar" é o truque de todo app escuro. **Derruba:** gente nomeando `#1A1B1E` de carvão tanto quanto `#171615`, às cegas, ou um mix de tema que um token de canvas não isola.
2. **Lenha, voz (D7).** Ela transformou "erro não é poema" em "o produto não fala". O vazio ainda diz Claude, e essa frase é a colisão da D8 escrita por extenso. Paleta sem uma frase é fantasia com HEX. **Derruba:** a frase do vazio empurrar o tempo até o primeiro Enviar acima dos 10% que ela mesma pôs como trava.

#### A concessão

Tição e a síntese me tiram `#FF7A9A` e `#F4B000`: o erro trava em `#FF7AA2`, o aviso em `#FACC15`. O C7 me tira a fresta colorida do tray; o template monocromático fica, e a fresta viva desce para o Dock. Lenha e Fogareiro me tiram duas das três frases: "Trabalhando" e o erro continuam literais. A frase que sobra é uma, no vazio.

#### "Sim, e…"

- **Tição, a brasa só no que está vivo** (ousadia: média): o anel de contexto, laranja aos 62% no artboard 7 e âmbar o tempo todo no F53, fica carvão até os 90% em que ele já vira crítico, e só então anda de `#A83E15` a `#FF3D00`.
- **Cinza, o piloto sem cor** (ousadia: alta): a primeira sessão depois da troca abre em carvão e a brasa acende no primeiro Enviar que dá certo, uma vez. Com `prefers-reduced-motion`, já abre acesa. Risco: parece quebrado.

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :------------ |
| 1. Carvão | Canvas `#171615`; papel `#F3F1EE`; texto `#A8A29E` | 76 | 78 | ajustou | Fogareiro segurou o (c); Tição mediu 5,09 |
| 2. Brasa | 07 com tinta escura; erro `#FF7AA2`; aviso `#FACC15` | 81 | 88 | ajustou | Tição e a síntese |
| 3. Símbolo | C desde 48px; fresta chapada no miúdo; tray template | 64 | 68 | ajustou | Fole, nas duas leituras, e o C7 |
| 4. Interface | Enviar com rascunho; 600ms; Dock acende; tray não | 73 | 75 | ajustou | Lenha, nos 600ms, e o C7 |
| 5. Narrativa e rollout | Uma frase no vazio; resto literal; cinza de um dia, depois padrão | 58 | 64 | virou | Lenha, Fogareiro, Cinza |

<!-- fim-rodada-2 -->

### Rodada 3: voto final

#### O voto em cada proposta

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| P1 | contra | Canvas `#171615`, medido a 5,09:1 sob a 07. Texto quente não apaga o azul do `#1A1B1E`. | 78 |
| P2 | apoio com ressalva | A rampa serve. `#7A746F` (3,74) só em desabilitado; placeholder fica no `#99938E` ou acima. | 80 |
| P3 | apoio com ressalva | Travar em `#FF7AA2` (7,02:1, ΔE 22,6), não em `#FF75A0`. O diff leva o sinal `−`, não só a cor. | 90 |
| P4 | apoio | Nenhuma. No claro, ícone e fundo tingido: o ocre escuro cola na 05 em deuteranopia. | 82 |
| P5 | apoio com ressalva | O cartão de aprovação é a quarta região: Allow não rouba a cota do Enviar. | 86 |
| P6 | apoio com ressalva | No claro, medir `#FFB088` na caixa real; se falhar 4,5:1, o claro fica neutro. | 84 |
| P7 | contra | C desde 48px no teste de 5s, em pé de igualdade com B. No miúdo, fresta chapada, sem núcleo de B. | 70 |
| P8 | apoio com ressalva | Dock sim, fresta no núcleo. Tray fica template: ponto colorido lê como badge de erro. | 74 |
| P9 | apoio | Nenhuma. Vazio no 02, seta `#8E8C90`; o anel neutro se mede dos dois lados. | 80 |
| P10 | apoio com ressalva | Painel sem foco fica na 06 parada (3,9:1 no briefing). A 05 parada fica em 2,8:1. | 76 |
| P11 | apoio com ressalva | Uma frase no vazio: "A brasa está fria." O resto literal. "Ask Claude" só troca se a string for nossa. | 66 |
| P12 | apoio com ressalva | A superfície elevada do claro não é `#FFFFFF`; senão o papel volta a ser impressora. | 72 |
| P13 | apoio com ressalva | A saída pré-escrita é o papel da 07, nunca o matiz: `#FF2E1A` só chega a ΔE 12,4. | 74 |
| P14 | apoio com ressalva | Portões 1, 2 e 4 ficam. A flag de duas semanas sai: um dia de cinza e a brasa vira padrão. | 68 |
| P15 | apoio com ressalva | "0 queixas" não prova. O teste de 5s compara a crosta C com o B, não só a palavra brasa. | 64 |

#### O que me faria mudar de ideia

- **P3 (90):** pessoas com deficiência de visão de cores, nos fundos reais, com o mesmo ícone e o mesmo texto, reconhecendo `#ff6568` tão bem quanto `#FF7AA2`. Ou o ΔE do rosa contra a 07, no cartão composto, caindo abaixo de 15.
- **P5 (86):** mostrar que `nativeChatThemeSurfaceStyle` (F61) reescreve `--action-brand` como reescreve `--primary`. Aí o token próprio é ficção.

#### A última ideia

**Quatro temperaturas, uma silhueta** `(ousadia: alta)`. No Dock as quatro filhas usam o mesmo carvão; muda a fresta: Studio `#FF3D00`, CLI `#D84315`, Workspace `#A83E15`, BrzA sem fresta. O P7 faz as quatro iguais. Risco: quatro ativos. Teste de 2h: Dock falso, 5 pessoas, "qual é o Studio?"; abaixo de 4 acertos, mata.

#### Os colegas

| Persona | A contribuição mais útil dela, em uma linha | Nota de 0 a 10 |
| :------ | :------------------------------------------ | :------------- |
| Tição | A brasa só no que está vivo, que virou o Enviar por disponibilidade. A conta de 0,04 com que fechou o fundo era o par errado. | 7 |
| Cinza | O piloto sem cor, o único ensaio que pode provar que a cor está mentindo. Virou portão, não opinião. | 9 |
| Lenha | Uma brasa, esfriar em 600ms, anel de foco neutro. O movimento do plano é dela. A voz muda, eu continuo rejeitando. | 8 |
| Fole | Mediu que o matiz não afasta da Claude (ΔE 12,4) e que a noturna aproxima (8,7). Segurou a C quando a sala foi para B. | 9 |
| Fogareiro | Segurou o `#171615` quando os outros quatro entregaram o fundo. A noturna morreu no dado, e ele cedeu no erro. | 8 |

#### Autoavaliação

Fiel ao atacar o canvas frio, o símbolo único e o silêncio do vazio. Saí da persona ao aceitar o limão, o rosa da tabela e o tray mudo: aí mandou o dado. Parei no `#A8A29E` sem medir um secundário mais quente no cartão.

<!-- fim-rodada-3 -->

### Rodada 4: entrega — os conceitos ousados

Cinco conceitos que não entraram em P1–P15 nem nas ideias novas da rodada 3. Cada teste cabe em duas horas. Se falha, o conceito morre.

#### 1. A primeira sessão acende o fogão `(ousadia: alta)`

- **Cena:** depois da atualização o chat abre todo em carvão. No primeiro Enviar que dá certo, a 07 nasce no botão, na chama e no "A", e não apaga mais.
- **Diferencia:** o rebrand é um acontecimento. O plano troca HEX com a pessoa no meio do turno.
- **Risco:** parece bug. Quem perde essa sessão não vê a marca nascer.
- **Teste:** 3 pessoas na build. Se uma achar o app quebrado antes de achar o Enviar, mata. Com `prefers-reduced-motion`, abre já aceso.

#### 2. O anel de contexto fica frio até 90% `(ousadia: média)`

- **Cena:** o anel de 16px (F53) é `#8E8C90` abaixo de 90. Só no limiar crítico, que já existe, corre de `#A83E15` a `#FF3D00`.
- **Diferencia:** no artboard 7 o anel já está laranja aos 62%, roubando a cota da P5. A tabela v1 deixa o anel na 06 o tempo todo.
- **Risco:** o aviso de contexto chega tarde para quem não lê o número.
- **Teste:** duas capturas, 62% e 93%, 5 pessoas, "qual está perto do limite?". Se errarem a de 93%, a brasa precoce volta.

#### 3. Uma frase no vazio `(ousadia: média)`

- **Cena:** estado vazio, chama em crosta (fresta na 05), a linha "A brasa está fria." O subtítulo segue operacional. "Trabalhando", erro e permissão não mudam.
- **Diferencia:** a P11 tira a metáfora do app inteiro. Esta devolve uma frase onde não há tarefa.
- **Risco:** a frase mente se a chama de 48px já estiver na 07. Pode atrasar o primeiro envio.
- **Teste:** 5 pessoas, tempo até o primeiro clique no Enviar, contra o vazio atual. Acima de +10%, a trava da Lenha, a frase sai.

#### 4. Quatro temperaturas, uma silhueta `(ousadia: alta)`

- **Cena:** no Dock, o mesmo carvão. A fresta é que muda: Studio `#FF3D00`, CLI `#D84315`, Workspace `#A83E15`, BrzA sem fresta.
- **Diferencia:** hoje as quatro filhas são a mesma chama, e o P7 confirma. O `brand.tokens.json` também as iguala. Aqui o Dock separa.
- **Risco:** quatro ativos e uma leitura a mais. Briga com o símbolo único do PLN-007.
- **Teste:** Dock falso, 5 pessoas, "qual é o Studio?". Abaixo de 4 acertos, mata e fica uma temperatura.

#### 5. O "A" é o único degradê `(ousadia: média)`

- **Cena:** botão, anel e chama de 13px são chapados. Só o "A" de BrzA carrega 07 → 06 → 05.
- **Diferencia:** o degradê deixa de ser tinta espalhada e vira a letra que já é o nome. A tabela v1 ainda pinta a chama focada com degradê.
- **Risco:** a 14px o degradê no texto vira lama e perde contraste.
- **Teste:** render a 14, 32 e 48px, nos dois temas, em 1×. Se o "A" não se lê a 14px, fica `#FF3D00` chapado.

#### O que ficou de fora e por quê

O canvas `#171615` eu votei contra na P1; repetir aqui é teimosia, o teste de nomeação é que reabre. Fagulha por ferramenta vira chuva, e a Brasa Noturna aproxima da Claude (ΔE 8,7). O link azul `#79c0ff` eu segurei na R1 para não virar terceira brasa. O canvas que esquenta durante o turno eu já tinha abandonado: o F61 reescreve esse fundo. Ponto colorido no tray eu cedi; se houver estado, é no Dock, e isso é a P8, com Anderson.

**Confiança na peça:** 64/100

<!-- fim-rodada-4 -->

### Rodada 5: revisão do plano

#### A confiança no plano

| Parte | Confiança (0–100) | Uma linha |
| :---- | :---------------- | :-------- |
| O plano inteiro | 64 | Portões e `--action-brand` estão sólidos. O plano entrega o símbolo menos memorável e chama isso de continuidade. |
| Tabela de tokens v2 | 76 | Rosa `#FF7AA2`, limão e `#FFB088` fecham. Lc 40,9 no rótulo da 07 e o placeholder igual ao secundário seguram a nota. |
| Fases 0–3 (tokens, ações, movimento) | 82 | Variante `brand`, Enviar por disponibilidade, 06 nos painéis parados, teste de brasa presa. É aqui que o plano acerta. |
| Fase 4 (símbolo) | 40 | Gera só o B, antes do teste. Índice 55, evidência suposta. A C não está no gerador, então não pode ganhar. |
| Fases 5–6 (portões, ativos) | 58 | Portões 1 e 2 filtram de verdade. Duas semanas num uso só, e o empacotamento da fase 6 não volta atrás. |
| As medições de sucesso | 52 | Contraste de 100% eu assino. "Calor" em 4/5 a marca de hoje já passa. Cinco pessoas não separam o B de uma chama genérica. |

#### O erro do plano

A R1 ainda diz "4,85 contra 4,89: ganho nulo". Esse par é o `#1C1A19`. O `#171615`, que Fogareiro e eu defendemos, foi medido a 5,09:1 sob a 07, e esse número não entrou. Também sumiu a quarta região: o cartão de aprovação. Allow e Enviar podem dividir a mesma brasa.

#### A mudança que mais subiria a sua confiança

A fase 4 gera B e C. O portão 4 escolhe às cegas "qual é a BrzA", contra a chama de hoje, e não pela palavra brasa ou calor. A confiança no plano inteiro sobe de 64 para 78.

#### O risco que o plano não vê

A tabela v2 deixa o ícone ativo na 06 o tempo todo. O anel de contexto, laranja aos 62% no artboard 7, é brasa permanente no composer, e a cota "uma por região" não o conta. O lint passa com a cota já estourada.

#### O seu voto nas decisões de Anderson

| Decisão | Opção | Confiança |
| :------ | :---- | :-------- |
| 1. Tray e Dock | Núcleo do Dock acende com o turno; o tray fica template, sem ponto | 74 |
| 2. Símbolo | B com a C no teste de 5 s, em pé de igualdade | 70 |
| 3. Flag | Um dia de cinza e a brasa vira padrão | 66 |
| 4. Fundo | `#171615` | 78 |
| 5. Onde o plano mora | No workstream `brand`, junto do PLN-007. No playground isto vira protótipo | 72 |
<!-- fim-rodada-5 -->

### Rodada 6: o símbolo em tamanho real

- **Vi as imagens:** sim, `folha-1x.png` e `folha-2x.png`, no Dock `#1A1B1E` e no papel `#F6F1EC`.
- **A ordem de leitura a 16 px:** Hoje → B → A → C. O pico de hoje chega a 142; B fica em 97, A em 96, C em 94. Medi a luminância dos pixels quentes na folha 1×, no papel; o Dock repete a ordem.
- **A ordem a 32 px:** Hoje → B → A → C. O núcleo do B é o pico mais alto dos três novos (111); a massa da C é a mais escura (média 68).
- **A B passa a 16 e a 32 px?** só com ajuste. Sem núcleo claro ela perde de hoje nos dois: a 16 px o pico dela é 97 contra 142.
- **O núcleo de rescaldo:** apoio. `#FFB088` no miúdo devolve o contraste que a 07 perdeu, 7,74:1 contra 3,88:1 no tile. Confiança 82.
- **O voto na decisão 2 (símbolo), agora:** B, com esse núcleo até 32 px. A C sai da disputa em pé de igualdade: é a mais escura a 16, 32 e 64. Confiança 76.
- **A confiança na fase 4, agora:** 48 (antes: 40). O B agora tem folha. O chapado na 07, que a fase 4 ainda gera, não passou.

<!-- fim-rodada-6 -->

### Rodada 6b: a variante da B

- **Vi as imagens:** sim, `folha-2-1x.png` e `folha-2-2x.png`.
- **A melhor variante a 16 e 32 px:** B + rescaldo largo, sem halo — quase. O pico empata o de hoje a 16 (142 nos dois temas); a 32 fica em 161 contra 166. A massa continua mais escura.
- **A melhor a 64 px:** B + topo claro, sem halo. A ponta chega no pico de hoje (225); o halo cai para 207.
- **O voto final no símbolo:** rescaldo largo, sem halo, em todos os tamanhos. O 16 px decide, e o topo claro cai para 125 aí. Confiança 80.
- **A confiança na fase 4, agora:** 72
<!-- fim-rodada-6b -->

### Rodada 7: a confiança final

- **Confiança no plano inteiro (v3):** 81 (na R5, sobre a v1: 64)
- **O que mais pesou para subir ou descer:** O símbolo passou a ser o rescaldo que empata o pico a 16 px, com regra de saída, e o portão 1 mede o par efetivo.
- **A decisão 6, a norma do rótulo da ação:** rótulo de 16 px, peso 700 — confiança 68
- **Algo ainda errado na v3:** Os picos de 64 px no Dock (177, 98, 171, 189) são o recorte desalinhado; no papel os quatro batem ~225 e só o halo cai a 207.
<!-- fim-rodada-7 -->

## O que ficou

## Fora do workspace

Nada.
