---
scope:
  - brza-studio
tags:
  - design
refs:
  - PLN-007
---

# Reunião Carvão em Brasa: a contraprova de Fogareiro, o Advogado do Usuário, em outro modelo

O pedido de Anderson, em 2026-11-07, na sessão da coordenação ("Rebranding BrzA: Carvão em Brasa"), depois das sete
rodadas: "ajuste o modelo/esforço do agente/sessão, para ficar condizente com o papel dele na reunião; tente
diversificar o máximo o uso de modelo/esforço". Esta é uma sessão nova, de contexto limpo, da persona **Fogareiro** — o Advogado do Usuário —
no agente Claude, com o modelo `claude-haiku-5-5` e esforço `low` (na reunião, Antigravity com Gemini 3.8 Flash high; o chat do Antigravity no app recusou todo modelo explícito). Ela refaz às cegas a rodada 1 e mede a
confiança na proposta de plano, para comparar a mesma persona em outro modelo.

## O que se fez

### Rodada 1: opinião inicial

Material lido: `briefing.md`, `personas/fogareiro.md` e as imagens `material/brasa/brasa.png` e `simbolo/A.png`, `B.png`, `C.png`. Não abri os chats 1 a 8 nem `levantamento/componentes.md`; as posições de interface abaixo vêm do briefing e da visão geral. Não li os outros worklogs da reunião.

#### 1. Carvão, a base neutra

- **Posição:** manter o `#1A1B1E` como fundo, com subtom levemente quente, e tirar a Cinza Carbono (03) de qualquer texto.
- **Por quê:** o briefing mediu 1,8:1 para a 03 sobre a 01, e o protótipo recorreu a `#BCBCBC` (9,1:1), fora da paleta. Quem lê código às 2h da manhã precisa de um texto secundário que passe e não brilhe demais. Um fundo frio e quase preto cansa mais a vista em sessão longa. Suponho que o subtom quente reduz esse cansaço, mas não medi.
- **Ideias:**
  - Token `--carvao-text-muted: #9A9AA0` para texto secundário, ~4,5:1 sobre a 01 (estimativa, a medir) `(ousadia: baixa)`.
  - Fundo do tema claro `#F5F3F0`, quente e não branco puro, para não cegar em ambiente claro `(ousadia: média)`.
- **Risco:** um neutro quente pode ficar lamacento ao lado do `#79c0ff` do link. O tema claro sem rampa testada pode ficar pior que o escuro.
- **Confiança:** 72/100

#### 2. Brasa, a escala quente, a semântica e o contraste

- **Posição:** o CTA (07) leva texto `#1A1B1E`, não branco. Branco sobre a 07 dá 3,5:1 e não serve para texto normal. A 06 não recebe texto branco. A 07 aparece em um ponto por tela.
- **Por quê:** o briefing mediu 4,9:1 para o texto escuro sobre a 07 e 4,4:1 para o branco sobre a 06, abaixo de 4,5. O erro `#ff6568` está perto demais da 07 para quem tem daltonismo vermelho-verde, e quem tem enxaqueca com laranja saturado sente o excesso de brasa. Suponho que o usuário daltônico não distingue erro de CTA só pela cor; não tenho dado para isso.
- **Ideias:**
  - Erro em rosa frio `#FF6B9A` com ícone e texto, nunca só cor `(ousadia: média)`.
  - Regra: a 07 só no CTA primário e no foco de campo; aviso (`#eab308`) sempre com ícone `(ousadia: baixa)`.
- **Risco:** trocar o erro para rosa pode soar a outra marca. O rosa `#FF6B9A` ainda não foi medido contra o fundo.
- **Confiança:** 70/100

#### 3. O símbolo

- **Posição:** B, com uma versão sem halo para 32 px e 16 px.
- **Por quê:** no material, o A tem brilho por baixo do tile, e isso some em 16 px e vira mancha na bandeja do macOS. O B mantém o núcleo legível e o tile só no grafite, o que funciona no claro e no escuro. O C tem fagulhas que não aparecem em 16 px. Vi o tamanho 16 px na visão geral, não no tray real.
- **Ideias:**
  - B sem halo como variante de tamanho pequeno, a mesma silhueta com contorno `#FF3D00` `(ousadia: baixa)`.
  - Em 16 px, só o contorno da chama e os três pontos do circuito `(ousadia: média)`.
- **Risco:** o B pode ficar apagado demais no tray, perdendo o calor que é o ponto do rebranding.
- **Confiança:** 60/100

#### 4. A brasa viva na interface

- **Posição:** o Enviar em repouso fica cinza, com a seta `#8E8C90`. Ganha a 07 quando há texto no campo ou quando o campo está em foco. A chama sem foco continua apagada.
- **Por quê:** o Enviar laranja o tempo todo ocupa o ponto de maior atenção da tela, e o usuário que lê muito o vê sempre. O estado que importa, "trabalhando" ou "pergunta", deve ser o que chama a atenção. Suponho que o cinza em repouso não confunde o usuário sobre o que fazer; o protótipo mostrou o Enviar já em 07, e não sei se alguém testou o cinza.
- **Ideias:**
  - Movimento de brasa que respira só no estado "trabalhando", com `prefers-reduced-motion` respeitado e sem respiração contínua na tela `(ousadia: média)`.
  - Foco com borda em degradê 07 → 06 e brilho externo de 12%, como o protótipo, mas sem brilho em outros estados `(ousadia: baixa)`.
- **Risco:** se o Enviar cinza parecer desativado, o usuário deixa de enviar. Isso precisa de teste de usabilidade, não de opinião.
- **Confiança:** 65/100

#### 5. Narrativa, voz e rollout

- **Posição:** a voz é calma e concreta, sem metáfora de fogo na microcópia. O rollout vai atrás de uma preferência de tema e de intensidade, com o tom padrão mais contido.
- **Por quê:** quem passa 10 horas no app não quer ler "queimando" no aviso de erro. A brasa fica na imagem, não no texto. A preferência de intensidade atende a enxaqueca sem tirar a marca de quem gosta do calor. Suponho que a maioria aceita o tom padrão mais contido, e isso precisa ser medido.
- **Ideias:**
  - Métrica de sucesso: tempo médio para localizar um erro numa sessão de teste, medido antes e depois, com meta de queda, e o percentual de usuários que ativam a intensidade mais baixa `(ousadia: baixa)`.
  - Métrica de guarda: queixas de fadiga visual e uso do tema claro por semana `(ousadia: baixa)`.
- **Risco:** a preferência de intensidade pode virar mais uma configuração que ninguém abre, e o rollout fica sem o efeito que se queria.
- **Confiança:** 68/100

#### A ideia mais ousada desta rodada

A brasa esfria com o tempo de sessão: depois de quatro horas, o acento sobe um degrau para baixo (07 para 06 nos botões e no foco), para aliviar quem está cansado. Risco: o estado da interface muda sem o usuário perceber, e a mesma ação pode parecer diferente no fim do dia.

#### Issues candidatas

- **Trocar o erro `#ff6568` por rosa frio, com ícone obrigatório** — o erro hoje colide com a 07 e pode não ser lido por daltônicos — prioridade `high`
- **Texto secundário com token de contraste AA, sem a 03 como texto** — o protótipo usou um cinza fora da paleta — prioridade `high`
- **Testar o Enviar cinza em repouso com usuários** — a hipótese de que não parece desativado precisa de teste — prioridade `medium`
- **Variante do símbolo sem halo para 16 e 32 px, medida na bandeja do macOS** — o A e o C perdem detalhe no tamanho pequeno — prioridade `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Carvão | Fundo `#1A1B1E` quente e texto secundário sem a 03 | 72 |
| 2. Brasa | CTA com texto escuro, 07 em um ponto, erro em rosa frio | 70 |
| 3. Símbolo | B, com versão sem halo para tamanho pequeno | 60 |
| 4. Interface | Enviar cinza em repouso, brasa só no foco e no trabalho | 65 |
| 5. Narrativa e rollout | Voz contida, preferência de intensidade, métrica de tempo | 68 |

<!-- fim-rodada-1 -->

### Rodada 2: a confiança na proposta de plano

Li `plano-proposta.md` inteiro, como Fogareiro e com a minha rodada 1 ao lado. Abri as imagens que ela cita só pelo texto: as variantes em `entregas/simbolo/` ficaram de fora. Não li os worklogs das outras sessões.

#### A confiança

| Parte | Confiança (0–100) | Uma linha |
| :---- | :---------------- | :-------- |
| O plano inteiro | 74 | Sólido no que mede; a parte que me toca (fadiga e enxaqueca) não tem medida própria. |
| Tabela de tokens | 78 | O par efetivo depois do mix é o certo; a tabela mostra a origem e o efetivo, como pedi. |
| Fases 0–3 (tokens, ações, movimento) | 70 | O Enviar por disponibilidade e o halo que respira só no foco fazem o que eu pedi. Falta medir a área de brasa. |
| Fase 4 (símbolo) | 72 | A regra de saída protege o 16 px, que era a minha dúvida; a B com rescaldo largo só fica firme se passar no teste. |
| Fases 5–6 (portões, ativos) | 66 | O portão 3 é Anderson sozinho, por duas semanas; quem tem enxaqueca com laranja não entra no teste. |
| As medições de sucesso | 62 | Mede contraste, reconhecimento e atribuição; não mede desconforto visual de quem usa o app todo dia. |

#### Onde a proposta diverge da sua rodada 1

- **Preferência de intensidade, não convenceu.** Eu pedi uma preferência de intensidade para quem tem enxaqueca. A proposta diz "sem modo noturno" e não prevê preferência alguma. O argumento da coordenação é a consistência da marca, e isso não responde à cena das 2h da manhã.
- **Enviar, convenceu.** Eu queria o cinza em repouso e a brasa com texto ou no foco. A R8 acende o Enviar por disponibilidade, sem depender do foco, e isso resolve a minha cena melhor que a minha proposta.
- **Texto secundário, convenceu.** Eu sugeri `#9A9AA0`. A proposta usa `#C4BEB9`, que é o par efetivo depois do mix de 83%, e o revisor mostrou que o chat pinta os dois textos com a mesma origem. Mudei de ideia: a medição do efetivo vale mais que o meu número.

#### O erro que a proposta ainda tem

A cota é de uma brasa sólida por região (R5, linha 57), e a região é contada, não a área. Cabeçalho, transcript, composer e cartão de aprovação podem acender ao mesmo tempo na mesma tela, e o portão 2 confere "zero regiões com duas", não quanto da tela está em brasa. A meta de desconforto (portão 3, "perguntado, não espontâneo") não diz quanto de brasa uma tela aguenta. É exatamente o ponto que eu levantei na rodada 1, e a proposta não o fechou.

#### O seu voto nas decisões de Anderson

| Decisão | Opção | Confiança |
| :------ | :---- | :-------- |
| 1. Tray e Dock | Adiar; ponto estático no tray só se não duplicar o estado âmbar já existente | 62 |
| 2. Símbolo | B com o rescaldo largo, sem halo abaixo de 128 px, com a regra de saída | 68 |
| 3. Flag | Duas semanas, com o desconforto anotado a cada dia | 80 |
| 4. Fundo | `#1A1B1E` | 65 |
| 5. Onde o plano mora | `brand`, ao lado do PLN-007 | 50 |
| 6. Norma do rótulo da ação | WCAG 2.x, com rótulo escuro (4,85) e o APCA como aviso | 75 |

<!-- fim-rodada-2 -->

## O que ficou

## Fora do workspace

Nada.
