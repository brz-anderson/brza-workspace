---
scope:
  - brza-studio
tags:
  - design
refs:
  - PLN-007
---

# Reunião Carvão em Brasa: a contraprova de Fole, a Estrategista de Marca, em outro modelo

O pedido de Anderson, em 2026-11-07, na sessão da coordenação ("Rebranding BrzA: Carvão em Brasa"), depois das sete
rodadas: "ajuste o modelo/esforço do agente/sessão, para ficar condizente com o papel dele na reunião; tente
diversificar o máximo o uso de modelo/esforço". Esta é uma sessão nova, de contexto limpo, da persona **Fole** — a Estrategista de Marca —
no agente Claude, com o modelo `claude-fable-5-1` e esforço `high` (na reunião, Opus 5.5 high). Ela refaz às cegas a rodada 1 e mede a
confiança na proposta de plano, para comparar a mesma persona em outro modelo.

## O que se fez

### Rodada 1: opinião inicial

Abri `brasa/brasa.png`, `simbolo/A|B|C.png` e os artboards 1, 2, 5, 7 e 8 do chat. Os contrastes que cito como
"medi" saíram da fórmula WCAG 2.x rodada nesta sessão; o que digo dos concorrentes é de memória, sem conferir hoje.

#### 1. Carvão, a base neutra

- **Posição:** o carvão tem que ser quente por dentro — esquentar a base um grau, para `#1B1917`, e nunca mais; a 03 sai
  do texto e a rampa de texto vira cinza-de-cinzas, quente, fora da paleta de sete.
- **Por quê:** o briefing mede que o `#1A1B1E` tem o azul como maior canal: é um grafite de sistema, o mesmo chão de
  Cursor, Vercel e Codex, que ocupam o preto-e-branco frio. "Carvão" promete calor guardado, e um fundo frio desmente a
  frase na primeira tela. Medi: a 07 sobre `#1B1917` dá 4,94:1 (sobre a 01, 4,85) e o branco dá 17,5:1 — a mudança
  não custa contraste. Para o texto secundário, medi `#B5ACA6` a 7,7:1 sobre a 01 e 6,2:1 sobre a 02, e `#C9C1BB` a
  9,7:1: substituem o `#BCBCBC` neutro do protótipo com a mesma legibilidade e com subtom de cinza de fogueira. Suponho
  que o salto da 03 para a 04 só incomoda porque as duas tentam ser texto; como borda (03) e como ponte do símbolo (04),
  o salto é a história, não um defeito.
- **Ideias:** (1) `--carvao-profundo: #1B1917` e `--carvao-queimado: #2A2624` quentes, a 02 só de superfície
  `(ousadia: média)`; (2) rampa de texto própria, `--fg: #F2EDE9`, `--fg-muted: #B5ACA6`, `--fg-faint: #8E8C90`
  (5,2:1 na 01, medi), e a 03 vira só `--border` e ícone inativo `(ousadia: baixa)`; (3) tema claro "Cinza da manhã":
  fundo `#F6F2EE`, papel quente, texto `#1A1B1E` a 15,5:1 (medi), e a brasa escurece para `#C23A12`, que dá 4,8:1 no
  papel (medi) — o mesmo fogo, visto no dia seguinte `(ousadia: alta)`.
- **Risco:** fundo quente em monitor mal calibrado vira marrom sujo, e ao lado do chrome do macOS (neutro) o painel
  pode parecer "amarelado"; o tema claro com brasa escurecida pode ler como uma segunda marca.
- **Confiança:** 72/100

#### 2. Brasa, a escala quente, a semântica e o contraste

- **Posição:** a 07 é a única brasa de verdade; o CTA leva texto escuro (carvão sobre a brasa), o erro sai do
  território da brasa para um rosa frio, e vale a regra "uma brasa por tela".
- **Por quê:** o briefing mede 4,9:1 do `#1A1B1E` sobre a 07 e 3,5:1 do branco — texto escuro no botão não é
  concessão, é o gesto da marca: o carvão em cima da brasa. De memória: o laranja mais próximo no mercado é o
  terracota/argila da Anthropic (um `#D97757` fosco, de papel kraft), e o BrzA Studio é cliente do Claude Code —
  o vizinho mais perigoso de todos. O que nos separa é a saturação e a luz: a 07 queima, a argila é opaca. A 06, que é
  a que mais se aproxima da argila, fica de acento, nunca de marca. A Raycast ocupa o coral `#FF6363`; o vermelho de
  erro `#ff6568` é literalmente esse coral, e colide com os dois. Medi um rosa frio `#FF6B8A` a 6,3:1 sobre a 01.
- **Ideias:** (1) `--color-primary: #FF3D00` com `--color-on-primary: #1A1B1E`; branco sobre a 07 só em ícone e texto
  ≥ 18 px `(ousadia: baixa)`; (2) `--color-danger: #FF6B8A` e a frase da semântica, "brasa é vontade, não é alarme":
  erro frio, aviso continua amarelo `#eab308` (9,0:1, medi), que já é cor de fagulha `(ousadia: média)`; (3) regra "uma
  brasa por tela": em repouso, só um elemento em 07 por viewport (o Enviar); o segundo pedido de 07 cai para a 06, e o
  terceiro para a 05 a 22% `(ousadia: média)`; (4) `--ember-glow` como brilho da 07 a 12%, reservado ao foco e ao
  trabalhando, nunca a cartão `(ousadia: baixa)`.
- **Risco:** erro rosa é pouco usual em ferramenta de dev e pode ser lido como "destaque" e não como falha; a regra de
  uma brasa por tela quebra em listas com vários agentes trabalhando.
- **Confiança:** 76/100

#### 3. O símbolo

- **Posição:** C, o carvão em brasa, como marca-mestra, com o núcleo de B emprestado abaixo de 32 px.
- **Por quê:** A é o símbolo de hoje recolorido — a chama por cima, como Firebase, Hono e metade dos ícones de "hot" do
  mercado; muda a cor, não a ideia. B é uma chama com halo, bonita e genérica. C é o único que conta a frase numa olhada:
  a chama virou carvão e o calor está dentro, pela borda acesa; as três fagulhas são o "fole" soprando. Li nas provas de
  16 px de `C.png` que ele é o mais escuro dos três; a crosta na 05 e na 04 come a luz, e o ícone no dock vira um ponto
  marrom. Em `B.png` o núcleo da 07 segura a luz em 16 px. Suponho que o tray do macOS vai ser template monocromático,
  onde nenhum dos três sobrevive em cor.
- **Ideias:** (1) C mestre, com a crosta subindo meio passo (05 → entre 05 e 06) e o núcleo de B em ≤ 32 px, "o mesmo
  carvão, mais perto" `(ousadia: média)`; (2) tray monocromático com uma fagulha só: a chama em `#8E8C90` em repouso, e
  a fagulha em 07 quando o agente trabalha, se o tray permitir cor `(ousadia: média)`; (3) ícone do app no claro com o
  tile no carvão, como `brasa.png` já mostra: a brasa nunca pisa em fundo branco `(ousadia: baixa)`.
- **Risco:** dois desenhos por tamanho são dois ícones para manter, e a crosta clareada pode perder a diferença entre C e
  B, que é o argumento de escolher C.
- **Confiança:** 68/100

#### 4. A brasa viva na interface

- **Posição:** a brasa é o agente — a tela em repouso é carvão, e o calor só aparece onde alguém age: o Enviar laranja o
  tempo todo é a única brasa que não apaga.
- **Por quê:** li no artboard 7 o ponto do protótipo: com o primário laranja sempre, o foco muda menos. Para a marca isso
  é feature: uma brasa constante na tela é o que faz o usuário saber que o fogo não apagou, e o foco não precisa de mais
  cor, precisa de movimento. Li no artboard 5 que a chama de 18 px já tremula no trabalhando, e no 1 que a chama sem
  foco vai a `#8E8C90`. Suponho que animação em loop no cabeçalho cansa em sessão de horas; a brasa só "respira" quando
  há trabalho.
- **Ideias:** (1) "esfriar": ao terminar o turno, a chama vai de 07 para 05 e para `#8E8C90` em 1,2 s — o trabalho
  vira carvão, e esse é o único movimento de saída `(ousadia: média)`; (2) "fagulha": ao enviar, uma partícula de 2 px
  em 07 sobe do botão por 400 ms, e a cada tarefa concluída na lista, uma fagulha, no lugar do riscado `(ousadia:
  alta)`; (3) "pedir sopro": a caixa da pergunta com opções leva borda na 05 e a chama vira fole, pulsando 07↔06 a 2,4 s
  — o agente pede sopro; microcópia "Preciso de você aqui" `(ousadia: média)`; (4) foco sem cor nova: a borda vira o
  degradê 07 → 06 → 05 e o brilho a 12%, como o protótipo, e o Enviar não muda `(ousadia: baixa)`.
- **Risco:** movimento vira ruído com vários agentes em paralelo, e a fagulha na lista de tarefas é enfeite se o
  usuário não a liga à conclusão; precisa respeitar `prefers-reduced-motion` desde o primeiro commit.
- **Confiança:** 70/100

#### 5. Narrativa, voz e rollout

- **Posição:** a frase é "calmo por fora, quente por dentro"; os tokens de marca falam português e os semânticos
  inglês; o lançamento é um só, contado como história, e se mede no dock e na boca do usuário.
- **Por quê:** o território "fogo" no mercado é sempre velocidade (Hot, Blaze, Warp, Turbo); carvão em brasa é o
  contrário, é calor que dura — a única promessa que nenhum concorrente de memória ocupa, e a que combina com agente
  que trabalha horas. A brasilidade é ativo: brasa de churrasco é a imagem que todo brasileiro tem na mão, e "BrzA" se
  lê quase "brasa" — suponho, sem ter medido com ninguém, que essa leitura se ensina numa linha. Nome em português no
  código é memorável e diferencia; nome em inglês na camada semântica é o que o componente precisa.
- **Ideias:** (1) tokens em duas camadas: `--carvao-profundo`, `--carvao-queimado`, `--cinza-carbono`, `--cinza-aquecido`,
  `--brasa-oculta`, `--brasa-viva`, `--brasa-incandescente` na marca, e `--color-bg`, `--color-primary`,
  `--color-fg-muted` na semântica, que é o que o componente lê `(ousadia: média)`; (2) voz: a microcópia fica carvão,
  sóbria e curta, e o calor vai só nos verbos do agente — "Trabalhando", "Esfriando", "Pedindo sopro" — nunca em
  adjetivo `(ousadia: média)`; (3) rollout em uma release, em quatro passos na mesma semana: tokens e tema escuro,
  ícone, tema claro, site e README, com a release note contando a história em três parágrafos `(ousadia: baixa)`.
- **Métricas de sucesso:** teste do dock — 10 pessoas acham o ícone do BrzA entre Cursor, Warp, Zed e Claude em
  menos de 2 s, 8 de 10; teste dos 5 segundos — pelo menos metade descreve a marca com "brasa", "fogo", "calor" ou
  "carvão" sem ser induzida; zero texto abaixo de 4,5:1 na auditoria dos dois temas; e nenhum HEX do degradê antigo
  sobrevivendo fora dos tokens.
- **Risco:** a frase e a história ficam na release note e a interface não as sustenta — o vício que eu mesma vigio; e
  tokens em português afastam contribuidor que não lê a língua.
- **Confiança:** 74/100

#### A ideia mais ousada desta rodada

A quantidade de brasa na tela é a quantidade de trabalho do agente. Em repouso, só o Enviar queima; cada agente
trabalhando acende a chama dele, o anel do turno e a tarefa em curso em 07; quando o turno acaba, tudo esfria em 1,2 s
até o carvão. O usuário lê o calor da tela como lê a brasa da churrasqueira: sem olhar o número. Risco: quem abre o app
e vê só carvão acha que ele está morto, e três agentes em paralelo viram uma tela em chamas.

#### Issues candidatas

- **Oficializar a rampa de texto fora da paleta de sete** — a 03 não serve de texto e o protótipo usa `#BCBCBC`; os
  tokens `--fg-muted`/`--fg-faint` quentes precisam de dono — prioridade `high`
- **Tirar o erro do território da brasa** — `#ff6568` colide com a 07 e com o coral da Raycast; decidir o rosa frio
  `#FF6B8A` e escrever a semântica "brasa é vontade, não é alarme" — prioridade `high`
- **Esquentar a base: `#1A1B1E` frio ou `#1B1917` quente** — medir ao lado do chrome do macOS e em dois monitores
  antes de decidir — prioridade `medium`
- **Símbolo C com núcleo de B em ≤ 32 px, e o tray monocromático** — provar em 16 px no dock escuro e claro —
  prioridade `medium`
- **Tokens em duas camadas e a release note da história** — nomes em português na marca, inglês na semântica; o
  texto de lançamento — prioridade `low`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Carvão | Esquentar a base um grau (`#1B1917`), rampa de texto quente fora da paleta, tema claro "cinza da manhã" | 72 |
| 2. Brasa | A 07 é a única brasa, CTA com texto escuro, erro vai ao rosa frio, uma brasa por tela | 76 |
| 3. Símbolo | C como mestre, com o núcleo de B abaixo de 32 px; tray monocromático com uma fagulha | 68 |
| 4. Interface | A brasa é o agente: Enviar sempre aceso, o resto só esquenta quando age e esfria ao terminar | 70 |
| 5. Narrativa e rollout | "Calmo por fora, quente por dentro"; tokens PT na marca e EN na semântica; mede no dock e nos 5 s | 74 |

<!-- fim-rodada-1 -->

### Rodada 2: a confiança na proposta de plano

Li a v3.1 inteira, com a minha rodada 1 ao lado. Os números abaixo são meus, de contraprova, sem ver as outras sessões.

#### A confiança

| Parte | Confiança (0–100) | Uma linha |
| :---- | :---------------- | :-------- |
| O plano inteiro | 80 | A frase do objetivo ("carvão onde não há trabalho, brasa onde há") é a marca certa, e o plano a executa; perde pontos onde a narrativa escapa dele (ver o erro) |
| Tabela de tokens | 78 | O par efetivo depois do mix é o achado que mais vale do plano; o erro claro `#6E3C5A` "a testar" e o secundário claro "a medir" ainda são lacunas |
| Fases 0–3 (tokens, ações, movimento) | 84 | Flag reativa, `--action-brand` fora do `--primary` e o Enviar por disponibilidade são lidos no código; só a fase 3 (R9, índice 57,3) está abaixo das outras |
| Fase 4 (símbolo) | 70 | A B com rescaldo largo tem o melhor pior caso medido, mas a massa quente média segue mais escura que a de hoje (83 contra 96 a 16 px); a regra de saída é o que me segura |
| Fases 5–6 (portões, ativos) | 72 | Os quatro portões cobrem o que eu pedi; a fase 6 é a única irreversível e carrega o risco da vitrine, e o auditor que lê o app é estimativa da coordenação |
| As medições de sucesso | 66 | Cinco pessoas são sinal, e o plano admite; a atribuição à Claude com controle é a melhor medida da tabela, e a associação em 5 s tem dois critérios (≥ 4/5 e "comparado à marca de hoje") sem dizer qual manda |

#### Onde a proposta diverge da sua rodada 1

1. **O fundo.** Defendi esquentar a base para `#1B1917`; a sala ficou no `#1A1B1E` (R1, 5/6) e levou o calor à rampa de
   texto (`#E8E2DC`, `#C4BEB9`) e à 04 na borda do tile. **Me convenceu:** o meu ganho medido era 4,94 contra 4,85, nada;
   e o calor no texto é o que o usuário lê, o fundo ele só sente. O risco do marrom ao lado do chrome do macOS era meu.
2. **O símbolo.** Defendi a C com o núcleo da B; a folha de contato (R6) mostrou a C como a pior a 16, 32 e 64 px e ficou
   a B com o rescaldo largo. **Me convenceu**, porque confirma o risco que eu mesma declarei (a crosta come a luz) e
   porque o que sobreviveu da minha ideia foi justamente o núcleo claro. Perde-se a história "a chama virou carvão";
   a interface conta ela no lugar do ícone.
3. **O Enviar e o movimento.** Defendi o Enviar aceso o tempo todo como "a brasa que não apaga" e a fagulha ao enviar;
   a proposta acende por disponibilidade (R8, índice 88) e corta a fagulha (R9). **Meio convencida:** por
   disponibilidade é mais coerente com "brasa onde há trabalho" e é a regra mais forte da reunião; o custo é o que a
   própria proposta chama de vitrine apagada, e a regra de captura (todo print mostra um turno vivo) cobre o marketing,
   não a primeira abertura do app. A fagulha aceito perder: era ousadia alta com índice baixo.

#### O erro que a proposta ainda tem

**A assinatura "BrzA — código em brasa" (R10) contradiz o conceito do plano.** O objetivo diz que a brasa é o
trabalho — "o agente trabalhando, a mensagem pronta para ir, a pergunta que espera" — e a interface inteira (R5, R8,
R9) acende pelo agente, nunca pelo código. A assinatura diz que o que queima é o código, que é o território de Hot,
Blaze e Firebase, o fogo-velocidade que a rodada 1 mandou evitar. A medição de associação em 5 s testa "brasa, fogo,
carvão ou calor", e não "código"; a assinatura não é testada por nada. Proposta de correção: "BrzA — calmo por fora,
quente por dentro", ou "BrzA — carvão em brasa", literal, e o teste da fase 0 leva a assinatura junto do wordmark.

#### O seu voto nas decisões de Anderson

| Decisão | Opção | Confiança |
| :------ | :---- | :-------- |
| 1. Tray e Dock | O núcleo do Dock acende enquanto trabalha; o tray fica template e adiado, porque já tem o âmbar de atenção | 58 |
| 2. Símbolo | B com o rescaldo largo em todos os tamanhos, e o topo claro só como segundo braço do teste da fase 0 | 72 |
| 3. Flag | Duas semanas no uso de Anderson, com o ensaio de reversão | 85 |
| 4. Fundo | `#1A1B1E`, com o calor na rampa de texto | 70 |
| 5. Onde o plano mora | `brand`, ao lado do PLN-007 | 90 |
| 6. Norma do rótulo da ação | WCAG 2.x com rótulo escuro (4,85) e o APCA como aviso | 82 |

<!-- fim-rodada-2 -->

## O que ficou

## Fora do workspace

Nada.
