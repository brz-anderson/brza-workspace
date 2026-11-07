---
scope:
  - brza-studio
tags:
  - design
---

# Reunião Carvão em Brasa: a participação de Fole, a Estrategista de Marca

O pedido de Anderson, em 2026-11-07, na sessão da coordenação ("Rebranding BrzA: Carvão em Brasa"): "coordenar uma
reunião de rebranding da marca BrzA (…) se aproximar mais do tom Carvão em Brasa, com um grafite mais próximo ao carvão e
tons em brasa incandescente". Este é o registro de **Fole** — persona a Estrategista de Marca, no agente Claude —, aberto pela coordenação com
`brza sessions reuniao-brasa-fole`. A pauta e as regras estão no briefing da reunião; cada rodada é uma seção abaixo.

## O que se fez

### Rodada 1: opinião inicial

Material: abri `brasa/brasa.png`, `brasa/simbolo/A.png`, `B.png`, `C.png` e `brasa/chat/brasa-chat-5`, `-7` e `-8`.
Os contrastes que não estão no briefing são cálculo meu, pela fórmula de luminância da WCAG 2.x. O que digo sobre os
concorrentes vem da minha memória de mercado e não foi conferido em fonte nesta rodada: está marcado como suposição.

#### 1. Carvão, a base neutra

- **Posição:** carvão de verdade é quente por baixo: aquecer um pouco o 01, montar a rampa de texto dentro da família
  e fazer do tema claro uma "cinza de fogueira", e não um branco.
- **Por quê:** _Lido:_ o 01 tem o azul como maior canal, e a 03 dá 1,8:1 como texto (briefing). O protótipo usou
  `#BCBCBC`, fora da paleta. _Medido (cálculo meu):_ `#A8A29E`, quente, dá 6,8:1 no 01, e `#9A928C` dá 5,6:1. Os dois
  cobrem o salto da 03 para a 04 sem sair da família. _Suposto:_ o grafite frio e neutro é o território de Cursor,
  Vercel, Codex e Zed. Um carvão quente nos separa deles sem gastar laranja.
- **Ideias:**
  - Tokens `carvao-0` `#1C1A19` (o fundo, com subtom quente), mais a 02 e a 03 como estão, e uma rampa de texto
    `cinza-1` `#E8E2DC` (primário), `cinza-2` `#A8A29E` (secundário, 6,8:1) e `cinza-3` `#7A746F` (placeholder e
    desabilitado, 3,7:1, nunca texto corrido) (ousadia: baixa)
  - Tema claro **Cinza de Fogueira**: fundo `#F6F1EC`, texto `#1A1B1E` (15,3:1) e acento na Brasa Oculta `#A83E15`
    (5,6:1). No claro, a brasa da marca é a que já esfriou. A Incandescente dá só 3,2:1 nesse fundo, então fica para
    ícone e preenchimento (ousadia: média)
  - **Carvão vivo:** enquanto o agente trabalha, o fundo da coluna do chat ganha um radial da 07 a 3% junto do
    composer, como carvão que esquenta por baixo (ousadia: alta)
- **Risco:** carvão quente demais vira marrom "café", e a troca de `#1A1B1E` por `#1C1A19` só um designer vê. O valor
  real está na rampa de texto. Sem ela, a mudança no fundo é cosmética.
- **Confiança:** 70/100

#### 2. Brasa, a escala quente, a semântica e o contraste

- **Posição:** a 07 é rara e cara: o CTA leva texto escuro e aparece uma vez por tela. O erro sai do vermelho para um
  rosa frio, porque a brasa e o erro não podem dividir o matiz.
- **Por quê:** _Medido (cálculo meu):_ `#1A1B1E` sobre a 07 dá 4,85:1, que passa AA em texto normal, e o branco dá
  3,55:1. O erro `#ff6568` fica a uns 15° de matiz da 07. Um `#FF6B9A` dá 6,4:1 no 01. A 07 tem matiz de 14,4° e o
  laranja da Claude (`#D97757`, de memória) tem ~14,8°: **é o mesmo matiz**, e nos separa só a saturação (100% contra
  ~63%) e o brilho. _Suposto:_ o Raycast ocupa o coral-vermelho.
- **Ideias:**
  - Regra **uma brasa por tela**: `--acao-principal` `#FF3D00` com texto `#1A1B1E`, no máximo um elemento sólido na 07
    por viewport, e o resto em tint da 06 ou da 05 (ousadia: média)
  - `--sinal-erro` `#FF6B9A`, rosa frio com 6,4:1, e `--sinal-aviso` `#F5B841`, âmbar com 9,7:1, que afastam o erro do
    vermelho e o aviso do laranja. Na narrativa: "brasa é energia, não perigo" (ousadia: média)
  - A 06 nunca leva texto branco pequeno. Vira `--acao-ativa` só para ícone ativo, onde os 3,9:1 no 01 passam o 3:1 de
    elemento gráfico (ousadia: baixa)
- **Risco:** o rosa no erro quebra o reflexo "vermelho = erro" e pode lembrar a paleta de outra marca. Ninguém fiscaliza
  "uma brasa por tela" sem um lint de tokens.
- **Confiança:** 75/100

#### 3. O símbolo

- **Posição:** **C**. Das três, só ela conta o nome "Carvão em Brasa". No pequeno, cai para um glifo de núcleo,
  derivado da B.
- **Por quê:** _Visto nos PNG:_ a A e a B são uma chama laranja, o "antes" com outra temperatura. Em 64 e 32 px, quase
  não se distinguem do símbolo de hoje. A C muda a história: a chama vira carvão com o calor por dentro, e as fagulhas
  são a parte que se lembra. _Visto:_ em 16 px, as três viram uma mancha laranja e as fagulhas somem. _Suposto:_ a C
  mais escura perde força no dock, ao lado de ícones claros.
- **Ideias:**
  - **Sistema de duas leituras:** a C no ícone do app (64 px ou mais) e na abertura. Em 32 px ou menos e no favicon,
    um glifo **núcleo**, a B sem halo e sem fagulha (ousadia: média)
  - Tray do macOS: um template monocromático da silhueta com o `{}` vazado. Quando o agente trabalha, ganha um ponto
    na 07, a única cor do tray (ousadia: média)
  - **As três fagulhas como assinatura**: saem do símbolo e viram um elemento gráfico solto, no loader, na marca-d'água
    do estado vazio e no favicon animado (ousadia: alta)
- **Risco:** a C escura fica com contraste fraco contra o dock escuro. Manter duas leituras exige disciplina, e o
  glifo pequeno pode virar uma terceira marca.
- **Confiança:** 60/100

#### 4. A brasa viva na interface

- **Posição:** a brasa vive no estado, e não na decoração. O Enviar fica no carvão em repouso e acende quando há o
  que mandar. O "trabalhando" respira como brasa.
- **Por quê:** _Lido:_ o protótipo mesmo aponta que, com o Enviar laranja sempre, o foco muda menos (briefing, ponto
  do composer). _Estratégia:_ se a 07 é rara (assunto 2), um Enviar laranja em repouso gasta a cor mais cara num
  elemento que não tem nada a dizer. _Suposto:_ acender quando há algo a mandar é a metáfora do fole, o sopro que
  acende.
- **Ideias:**
  - Enviar **Sopro**: vazio, em `#2C2D31` com a seta `#8E8C90`. Com texto, na 07 com a seta escura. Ao enviar, um pulso
    de 180 ms, com o brilho da 07 de 24% a 0 (ousadia: média)
  - **Brasa que respira:** a chama de 18 px troca o tremular por uma respiração de luminância de 2,4 s (05 → 07 → 05).
    Cada ferramenta concluída solta uma fagulha de 600 ms, no máximo uma por segundo. Com `prefers-reduced-motion`,
    a chama fica parada na 06 (ousadia: média)
  - **Cinza que esfria:** o cartão de ferramenta que acaba de terminar passa 1,5 s com a borda na 05, esfriando até a
    02. A trilha de calor mostra o que acabou de acontecer (ousadia: alta)
- **Risco:** movimento demais cansa numa sessão de duas horas, e um turno com 40 chamadas vira chuva de fagulha. O teto
  de uma por segundo é obrigatório.
- **Confiança:** 65/100

#### 5. Narrativa, voz e rollout

- **Posição:** o conceito é **"o calor fica onde o trabalho está"**: a interface é carvão, e a brasa marca onde a
  pessoa e o agente agem. O ativo que ninguém tem é a origem do nome: Brasil vem de brasa, pelo pau-brasil.
- **Por quê:** _Lido/conhecido:_ "Brasil" vem do pau-brasil, a madeira cor de brasa. É fato histórico corrente, que não
  conferi em fonte nesta rodada. BrzA já soa Brasa e Brasil. _Suposto, de memória:_ Cursor, Vercel e Codex são
  monocromo, a Linear é índigo, o Zed é azul, o Warp tem gradiente frio, a Claude é terracota e o Raycast é coral.
  Ninguém ocupa o calor contido sobre carvão.
- **Ideias:**
  - Frase: **"BrzA — código em brasa."** Manifesto: "Carvão é o que fica do trabalho. Brasa é o que ainda está vivo."
    (ousadia: média)
  - Tokens em duas camadas. Os primitivos contam a história: `carvao-0..3`, `cinza-1..3`, `brasa-oculta`,
    `brasa-viva`, `brasa-incandescente`. Os semânticos protegem o código: `--acao-principal`, `--acao-ativa`,
    `--sinal-erro`, `--sinal-aviso` (ousadia: baixa)
  - Microcópia de estado com três termos e nada mais: "Acendendo…" ao iniciar, "Em brasa" ao trabalhar e "Pronto" no
    fim, sem trocadilho nos erros (ousadia: média)
  - Rollout: duas semanas atrás da flag `brand.brasa`, no uso do próprio Anderson. Depois vira o padrão, com uma nota
    de changelog "Carvão em Brasa" e o antes/depois do símbolo (ousadia: baixa)
- **Métricas de sucesso:**
  - Contraste: um script confere que 100% dos pares de tokens texto/fundo passam 4,5:1 e os de ícone, 3:1.
  - Reconhecimento: num teste de 5 s com 5 devs, pelo menos 4 descrevem a marca com "brasa", "fogo", "carvão" ou
    "quente", e nenhum a confunde com a Claude.
  - Semântica: num teste de 5 telas, ninguém lê o CTA como erro.
- **Risco:** a microcópia temática vira fofura e envelhece rápido, e a etimologia pode soar forçada fora do Brasil.
- **Confiança:** 70/100

#### A ideia mais ousada desta rodada

**O ícone guarda o calor do dia.** O ícone do app no dock (via `NSDockTile`) esquenta com o uso: o núcleo vai da 05 à
07 conforme os turnos do dia e esfria de madrugada. A marca vira um registro do trabalho, o carvão que guarda o calor.
Risco: custo de render e de bateria, ser lido como badge de notificação e distrair. Pode também brigar com o ícone
estático que a loja e o Finder mostram.

#### Issues candidatas

- **Rampa de texto e carvão quente nos tokens (`carvao-0`, `cinza-1..3`)** — a 03 não serve como texto e o protótipo
  saiu da paleta para resolver — prioridade `high`
- **Erro e aviso fora do matiz da brasa** — `#ff6568` e a 07 estão a ~15° de matiz, e o CTA não pode parecer erro —
  prioridade `high`
- **Tema claro "Cinza de Fogueira"** — a paleta não tem tons claros, e a 07 dá 3,2:1 num fundo claro quente —
  prioridade `medium`
- **Símbolo C em duas leituras, com o glifo núcleo e o template do tray** — em 16 px as três propostas viram mancha —
  prioridade `medium`
- **Teste de reconhecimento de 5 s contra Claude e Raycast** — a 07 tem o mesmo matiz do laranja da Claude —
  prioridade `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Carvão | Carvão quente por baixo: rampa de texto `cinza-1..3` na família e tema claro "Cinza de Fogueira" | 70 |
| 2. Brasa | A 07 é rara, com texto escuro e uma por tela; erro em rosa frio e aviso em âmbar, fora do matiz da brasa | 75 |
| 3. Símbolo | C, por contar o nome, com um glifo núcleo em 32 px ou menos e um template no tray | 60 |
| 4. Interface | A brasa vive no estado: Enviar acende quando há texto, a chama respira e o que terminou esfria | 65 |
| 5. Narrativa e rollout | "O calor fica onde o trabalho está"; Brasil vem de brasa; flag de 2 semanas e teste de 5 s | 70 |

<!-- fim-rodada-1 -->

### Rodada 2: debate

Li a síntese e a rodada 1 de Tição, Cinza, Lenha e Fogareiro. A de Faísca estava vazia quando escrevi. Os ΔE2000 novos
são cálculo meu, com a mesma fórmula que reproduz os 11,8 da coordenação entre a 07 e `#D97757`.

#### As disputas

- **D1:** (a) — Tição me convenceu: o ganho do `#1C1A19` é nulo, e o frio do fundo faz a brasa saltar. O calor que
  diferencia vai para o texto (D2) e para a 04 nas bordas do tile, não para o canvas — 65/100
- **D2:** (b), `#A8A29E` — dá 6,83 no 01 e 5,45 no cartão 02. O `#BCBCBC` é neutro e de ninguém: o texto quente é o
  único lugar em que o carvão quente aparece o tempo todo, a custo zero de contraste — 75/100
- **D3:** (b), `#FF75A0` — ΔE 22,4 contra a 07 em deuteranopia, e o carmesim cai para 11,4. Troco o meu `#FF6B9A`
  pelo de Cinza, que tem mais contraste (6,81) com o mesmo ganho. "Brasa é energia, não perigo" — 85/100
- **D4:** (c), perto de `#FACC15` — o dado derruba o meu `#F5B841` (13,7 em deuteranopia, contra 17,3). O aviso deixa
  de ser parente da chama, e isso é bom para a marca: o âmbar da chama de hoje sai de cena junto — 75/100
- **D5:** (d) — a B é a menos memorável, e o próprio Tição admite. A C é a única que conta o nome, mas perde a crosta
  em 32 px (Tição leu em `C.png`). Então: C a partir de 64 px (Dock, "Sobre", site) e o núcleo chapado da B abaixo — 65/100
- **D6:** outra: (a), mais **uma** fagulha só quando o turno termina — cedo a fagulha por ferramenta, que vira chuva
  num turno de 40 chamadas. Uma fagulha por turno é a assinatura de "pronto", e não um ruído — 55/100
- **D7:** outra: (b) dentro do app, mais a frase "BrzA — código em brasa" fora dele (site, README, changelog) — cedo os
  estados temáticos, que eu mesmo marquei como risco de fofura. A voz da marca mora onde a pessoa não está trabalhando — 70/100
- **D8:** (d), com a regra de decisão escrita antes — **medi que deslocar para o vermelho quase não ajuda**: `#FF2E1A`
  (5°) fica a ΔE 12,4 da Claude, contra 11,8 da 07. Se 2 em 5 ligarem a brasa à Claude, a saída é o papel (a 07 rara,
  a brasa só no vivo), não o matiz — 70/100
- **D9:** (a), com o piloto em cinza de Cinza **dentro** das duas semanas: é um `filter: grayscale(1)` de um dia, e
  não um portão antes de tudo — 70/100

#### Os ataques

1. **Tição, assunto 5 — "uma versão direto, sem barulho".** Um rebranding sem barulho paga todo o custo (tokens,
   ícone, QA) e não leva nada à marca. Pior: o app mostra "Claude" na tela o tempo todo, e a 07 está a ΔE 11,8 do
   laranja dela. Sem uma história que diga "isto é brasa, isto é BrzA", a cor nova vai ser lida como emprestada.
   _Derruba o ataque:_ se o público hoje for só Anderson e uns poucos, o barulho não tem para quem falar.
2. **Fogareiro, assunto 4 — a Brasa Noturna.** Uma marca que muda de cor às 22h quebra toda captura de tela, e o
   tom arrefecido piora o problema da D8: **`#E05A20` fica a ΔE 8,7 da Claude** (cálculo meu), mais perto que a 07
   (11,8). O conforto noturno é do tema e do sistema (Night Shift), e não da cor da marca.
   _Derruba o ataque:_ um tom noturno que se afaste da Claude e um dado de fadiga que justifique o custo.

#### A concessão

**Tição, D1:** fica o `#1A1B1E`. Eu mesmo escrevi na rodada 1 que a diferença "só um designer vê". O argumento de
Tição, de que o frio do fundo faz a brasa saltar por oposição, é melhor que o meu. **Muda na minha posição:** o
"carvão quente" sai do fundo e vai para a rampa de texto e para a 04, e a frase da marca para de prometer um fundo
quente. **Também cedo à medição na D4**, e a Tição, Lenha e Fogareiro no movimento (D6) e na microcópia (D7).

#### "Sim, e…"

- **Lenha, uma única brasa por painel ativo — sim, e uma brasa só no sistema inteiro:** a brasa que respira no painel,
  o ponto no tray (ideia de Fogareiro) e o núcleo do ícone no Dock acendem juntos enquanto algum agente trabalha, e
  apagam juntos. É a minha ideia do Dock rebaixada a um estado binário, sem gráfico de uso (ousadia: média)
- **Cinza, o piloto sem cor — sim, e ele vira a história do lançamento:** o changelog e o post mostram primeiro a
  interface em cinza ("o carvão") e depois acesa ("a brasa"). O ensaio de estrutura vira a peça de marca, e as
  mesmas telas servem ao teste de 5 s da D8 (ousadia: média)

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :------------ |
| 1. Carvão | Fica o `#1A1B1E`; o calor vai para o texto `#A8A29E` e a 04 | 70 | 70 | virou | Tição |
| 2. Brasa | A 07 rara; erro `#FF75A0` e aviso perto de `#FACC15`; o vermelho não separa da Claude | 75 | 80 | ajustou | Cinza, coordenação |
| 3. Símbolo | Duas leituras: C a partir de 64 px, núcleo chapado da B abaixo | 60 | 65 | ajustou | Tição |
| 4. Interface | Respirar e esfriar; uma fagulha só no fim do turno; uma brasa no sistema | 65 | 60 | ajustou | Lenha, Tição |
| 5. Narrativa e rollout | Microcópia literal; voz fora do app; flag de 2 semanas com o piloto em cinza | 70 | 70 | ajustou | Cinza, Lenha |

<!-- fim-rodada-2 -->

### Rodada 3: voto final

Li a síntese 2 e a rodada 2 de Tição, Cinza, Lenha e Fogareiro. Faísca não tinha rodada 2, então li a rodada 1 dela.

#### O voto em cada proposta

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| P1 | apoio | O frio do fundo faz a brasa saltar; o calor vive no texto e na 04 | 75 |
| P2 | apoio | — | 80 |
| P3 | apoio | — | 85 |
| P4 | apoio | — | 80 |
| P5 | apoio | O token próprio é obrigatório pelo F61 de Faísca; a regra "uma brasa por região" é a que guarda a 07 rara | 85 |
| P6 | apoio com ressalva | Nomear o token `--brasa-rescaldo` no primitivo: é a única brasa que vira texto, e merece o nome | 75 |
| P7 | apoio com ressalva | B agora, mas a C entra como um braço do teste de 5 s (P13): se for mais reconhecida em ≥ 4/5, volta à mesa no ícone grande | 55 |
| P8 | apoio com ressalva | No Dock, acende o núcleo do ícone, e não um ponto: um ponto no Dock se lê como badge de notificação | 70 |
| P9 | apoio | — | 75 |
| P10 | apoio | Cedo a fagulha no fim do turno: o esfriar já é a assinatura do "pronto" | 75 |
| P11 | apoio | Tirar o "Ask Claude…" da cópia (achado de Faísca) vale mais para a marca do que qualquer cor | 80 |
| P12 | apoio | — | 70 |
| P13 | apoio com ressalva | Separar associação ("o que lembra?") de atribuição ("de quem é?"), como propôs Cinza, e incluir a marca atual como base | 80 |
| P14 | apoio | — | 80 |
| P15 | apoio com ressalva | Alinhar com a P13: a P15 exige 0/5 na Claude, e a P13 só age com 2/5. Proponho: 0/5 é sucesso, 1/5 segue em observação, 2/5 aciona a P13 | 70 |

#### O que me faria mudar de ideia

- **P3 (erro em `#FF75A0`):** no teste de tarefas com 5 pessoas, uma ou mais não lerem o rosa como erro sem ler o
  texto. Também derrubaria o voto alguém com deuteranopia confundir o rosa com a 07 nos fundos reais, apesar do
  ΔE 22,4 simulado.
- **P5 (token próprio e uma brasa por região):** o lint encontrar, nas 8 cenas, uma região que precisa de duas ações de
  marca ao mesmo tempo, como o Allow e o Submit lado a lado. Também derrubaria o voto o `--action-brand` ser lavado
  pelo tema de outro jeito que não o do `--primary`.

#### A última ideia

**A brasa no terminal, nas filhas que não são o app** (ousadia: média). Ninguém falou do BrzA CLI nem do Workspace,
e a arquitetura de marca é das quatro filhas. O CLI ganha a mesma brasa: a 07 em truecolor, com o ANSI 202 (`#ff5f00`)
de reserva, só no prompt e no spinner, que respira como no app. Erro e aviso no CLI seguem a P3 e a P4, e o resto fica
na cor do terminal da pessoa. Sem isso, "Carvão em Brasa" é tema de um app, e não marca. Risco: o terminal claro e os
temas da pessoa, que a auditoria da P14 não cobre.

#### Os colegas

| Persona | A contribuição mais útil dela, em uma linha | Nota de 0 a 10 |
| :------ | :------------------------------------------ | :------------- |
| Tição | Mediu que o laranja de hoje já está a 7,9 da Claude: a brasa afasta. E me virou no fundo | 9 |
| Faísca | Os fatos de código: o tema reescreve o `--primary`, o diff a 1,03:1 da 06 e o "Ask Claude…" | 9 |
| Cinza | O ensaio sem cor, que virou portão permanente no CI, e a separação entre associação e atribuição | 8 |
| Lenha | Uma brasa por painel ativo, esfriando em 600 ms, e a matriz de 32 capturas | 8 |
| Fogareiro | O usuário cansado às 3h como critério; mas não cedeu e trouxe o único número divergente | 6 |

#### Autoavaliação

**Fiel:** liguei cada cor a um território, a 07 ao da Claude, e dei o nome e a frase. Medi o ΔE para não ficar em
abstração, e isso derrubou o "deslocar para o vermelho". **Saí:** caí no vício da persona, a narrativa que a
interface não sustenta, com os estados temáticos e a fagulha, e foi a sala que me trouxe de volta.

<!-- fim-rodada-3 -->

### Rodada 4: entrega — o guia de narrativa

**O conceito em uma frase:** o BrzA é carvão onde não há trabalho e brasa onde há. A cor acende no que está vivo (o
agente trabalhando, a mensagem pronta para ir, a pergunta que espera) e apaga quando termina.

#### Três assinaturas

| Assinatura | Território | Vizinho mais perto (suposição, de memória) | Onde usar |
| :--------- | :--------- | :----------------------------------------- | :-------- |
| **"BrzA — código em brasa."** | ofício e calor: o trabalho que está aceso | ninguém em ferramentas de dev ocupa o fogo; a Claude ocupa o terracota, mas com o território do "pensar junto" | **a assinatura** (recomendada): site, README, changelog, lockup de lançamento |
| **"O calor fica onde o trabalho está."** | foco e atenção: a interface que não grita | Linear (rigor), Zed (velocidade), Cursor e Vercel (monocromo, ausência) | princípio interno do guia de design e a régua de toda revisão de tela |
| **"Feito no Brasil, mantido em brasa."** | origem e brasilidade | vazio: nenhum concorrente do briefing fala de origem | a página "Sobre" e a história da marca, nunca no app |

A terceira depende de "Brasil vem de brasa", pelo pau-brasil. É etimologia corrente, mas **ainda não conferida em
fonte**: confere-se antes de qualquer publicação.

#### O manifesto

> Carvão é o que fica do trabalho: a base escura e quieta, que não pede atenção. Brasa é o que ainda está vivo: o
> agente trabalhando, a mensagem pronta, a pergunta que espera você. O BrzA acende onde há trabalho e apaga quando
> ele termina. Não somos fogo de artifício; somos brasa — o calor que dura a noite inteira. Feito no Brasil.

#### A voz

A metáfora mora **fora do app**: no site, no README, no changelog e no "Sobre". **Dentro do app, a cópia é literal**
(P11). A brasa aparece pela cor e pelo movimento, nunca pela palavra.

| Faça | Não faça |
| :--- | :------- |
| Diga o estado: "Trabalhando", "Aguardando sua resposta" / "Working", "Waiting for your reply" | "Em brasa", "Acendendo…", "A brasa espera" |
| Diga o erro e a saída: "Falha ao enviar. Tentar novamente" / "Couldn't send. Retry" | "Algo pegou fogo", "Ops! 🔥" |
| Diga o que parou: "O agente parou antes de terminar. Continuar" | "A brasa apagou" — soa como perda definitiva |
| Botão com verbo no infinitivo: "Enviar", "Parar", "Permitir", "Continuar" | botão com metáfora: "Soprar", "Acender" |
| Estado vazio com o próximo passo: "Descreva uma tarefa para começar." | slogan no estado vazio, ou "A brasa está fria." |
| Uso e limite em números: "Você usou 90% do limite desta conta." | **nunca "queimar"** tokens ou créditos: lê-se como desperdício e punição |

**O nome do produto na cópia.** Se a string do composer for nossa, troca-se "Ask Claude to do anything…" por "Peça ao
BrzA…" / "Ask BrzA…". O provedor continua identificado no seletor de modelo ("Opus 5.5"), como pede a P11. Se a string
vier do upstream, fica como está. **Essa decisão é de Anderson.**

#### A nomenclatura dos tokens primitivos

Os primitivos dizem **o que a cor é**, o material; os semânticos dizem **o que ela faz** (`--action-brand`,
`--text-secondary`, `--status-error`). Os primitivos ficam em português, sem acento, porque a brasilidade é o ativo
da marca. Os semânticos ficam em inglês, como o código do app (`--primary`, `--action-brand`). Os nomes de exibição
"Brasa Oculta, Viva, Incandescente", de Anderson, ficam no guia.

| Família | Tokens primitivos | HEX | Regra |
| :------ | :---------------- | :-- | :---- |
| carvão (superfície) | `--brz-carvao-1` … `-4` | `#1A1B1E`, `#2C2D31`, `#454446`, `#6B554B` | nunca texto; a 4 só na borda do tile |
| cinza (texto no escuro) | `--brz-cinza-1` … `-4` | `#E8E2DC`, `#A8A29E`, `#99938E`, `#7A746F` | a 4 só em desabilitado |
| papel e tinta (claro) | `--brz-papel`, `--brz-tinta-1`, `--brz-tinta-2` | `#F6F1EC`, `#1A1B1E`, `#5C5650` | — |
| brasa | `--brz-brasa-oculta`, `-viva`, `-incandescente` | `#A83E15`, `#D84315`, `#FF3D00` | a incandescente só em `--action-brand`, uma por região |
| rescaldo | `--brz-rescaldo` | `#FFB088` | a única brasa que vira texto no escuro (código em linha) |
| sinais | `--brz-sinal-rosa`, `-rosa-escuro`, `-limao`, `-ceu` | `#FF75A0`, `#B4235A`, `#FACC15`, `#79c0ff` | **nunca "brasa" num sinal: brasa é energia, não perigo** |

Para as quatro filhas, o mesmo conjunto vai a um `brand.tokens.json`, com `ansi256` de reserva no CLI, por exemplo
`"brz-brasa-incandescente": {"hex": "#FF3D00", "ansi256": 202}`.

#### A nota de lançamento

> **BrzA Studio — Carvão em Brasa**
>
> O BrzA ficou mais escuro, e mais quente onde importa. A interface agora é carvão: quieta, com texto num cinza
> quente e mais legível. A brasa — o laranja incandescente — aparece só onde há trabalho: no Enviar quando há o que
> mandar, na chama que respira enquanto o agente trabalha e que esfria quando ele termina.
>
> - Erro em rosa e aviso em amarelo-limão, sempre com ícone: não se confundem mais com a cor de ação, nem para quem
>   tem daltonismo.
> - Todo texto passa de 4,5:1 de contraste, nos temas escuro e claro.
> - O tema claro ganhou papel quente: "Cinza de Fogueira".
>
> Antes de acender, testamos a interface inteira sem cor: tudo tinha de funcionar em cinza. Depois, a brasa.
> BrzA — código em brasa.

A peça visual do lançamento é **o par antes e depois:** a mesma tela em cinza ("o carvão") e acesa ("a brasa"),
com as capturas do portão 2. Ela sai depois do portão 4, e não no dia em que a flag liga.

#### O que ficou de fora e por quê

- **O símbolo, o estado no tray e no Dock (P8) e a string "Ask Claude…"** ficaram de fora: são decisões de Anderson.
  A nota de lançamento não promete nenhum dos três.
- **As assinaturas não foram testadas.** A pergunta "o que lembra?" do teste de 5 s (P13) pode avaliar a primeira.
- **A etimologia e os territórios dos concorrentes** vêm da minha memória e precisam de fonte antes de publicar.
- **O inglês da microcópia** não teve revisão de um falante nativo.
- **Primitivos em português e semânticos em inglês** é uma suposição minha; o mapa de Lenha diz se ela cabe no
  código.

**Confiança na peça:** 72/100

<!-- fim-rodada-4 -->

## O que ficou

## Fora do workspace

Nada.
