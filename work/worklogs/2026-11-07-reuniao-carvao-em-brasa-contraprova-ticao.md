---
scope:
  - brza-studio
tags:
  - design
refs:
  - PLN-007
---

# Reunião Carvão em Brasa: a contraprova de Tição, o Guardião, em outro modelo

O pedido de Anderson, em 2026-11-07, na sessão da coordenação ("Rebranding BrzA: Carvão em Brasa"), depois das sete
rodadas: "ajuste o modelo/esforço do agente/sessão, para ficar condizente com o papel dele na reunião; tente
diversificar o máximo o uso de modelo/esforço". Esta é uma sessão nova, de contexto limpo, da persona **Tição** — o Guardião —
no agente Claude, com o modelo `claude-sonnet-5-5` e esforço `medium` (na reunião, Opus 5.5 high). Ela refaz às cegas a rodada 1 e mede a
confiança na proposta de plano, para comparar a mesma persona em outro modelo.

## O que se fez

### Rodada 1: opinião inicial

Suposição: abri `brasa.png` e `simbolo/A.png`, `B.png`, `C.png`; não abri os `chat/` nem o `componentes.md`, então falo do chat pelo texto do briefing. Parto do PLN-007 como está no briefing: o degradê `--brand-gradient` (`#ffaa44 → #e04a2b`), a chama de 13/18/48 px e o "A" do wordmark.

#### 1. Carvão, a base neutra

- **Posição:** manter o `#1A1B1E` como fundo e aquecê-lo só um pouco; o carvão não precisa de outro nome de cor, precisa de uma rampa de texto que funcione.
- **Por quê:** lido no briefing: o `#1A1B1E` tem subtom frio (azul é o maior canal) e a 03 `#454446` dá 1,8:1 como texto, reprovada; o protótipo já usa `#BCBCBC` (9,1:1). Suponho que ninguém perceba um deslocamento de 2 a 3 pontos no canal azul, e que o grafite atual esteja nos 6 mil usuários e nas telas como "o escuro da BrzA" — mexer muito perde reconhecimento.
- **Ideias:**
  - Texto secundário vira token próprio, `--text-muted: #A8A6A3` (aquecido, ~7:1 sobre a 01), e a 03 fica só para divisória e ícone inativo (ousadia: baixa).
  - Fundo `#1B1B1D` (R=G≈B, sem azul dominante), diferença que o olho não vê mas que tira o frio (ousadia: baixa).
  - Tema claro "Cinza de Cinzas": fundo `#F4F1EE`, texto `#1A1B1E`, a brasa passa a `#D84315` como acento em vez de `#FF3D00` (ousadia: média).
- **Risco:** o "aquecer" vira desculpa para trocar o fundo inteiro e quebrar a CLI e o workspace, que herdam o grafite. Também confundo "conservar" com "não ter ousado".
- **Confiança:** 72/100

#### 2. Brasa, a escala quente, a semântica e o contraste

- **Posição:** a 07 só como CTA e foco, com texto escuro `#1A1B1E` (4,9:1); a 06 e a 05 em apoio; o erro sai do vermelho-laranja e vai para um rosa frio.
- **Por quê:** lido: branco sobre a 07 dá 3,5:1 e sobre a 06 4,4:1, ambos abaixo de 4,5; o escuro passa. O `#ff6568` do erro está perto da 07 (fonte: briefing). Se a brasa é a marca, o erro tem de ser outra coisa; suponho que o aviso `#eab308` (amarelo) já se distingue bem, sem mudança.
- **Ideias:**
  - Erro `#FF5C8A` (rosa-coral frio) com ícone de triângulo obrigatório, nunca só a cor (ousadia: média).
  - Regra "uma brasa por tela": só um elemento na 07 por vez; o resto vai na 06 ou 05 (ousadia: baixa).
  - Texto sobre a 06 só a partir de 18 px/negrito, e o Parar usa a 06 a 14% com ícone na 06 pleno (3,9:1 ≥ 3:1) (ousadia: baixa).
- **Risco:** o rosa cria um sexto matiz e parece "outra marca"; a regra de uma brasa por tela fica difícil de impor no código.
- **Confiança:** 68/100

#### 3. O símbolo

- **Posição:** B, o Núcleo incandescente — a silhueta e o circuito com `{}` ficam intactos, e só o calor muda.
- **Por quê:** visto nas imagens: A e B guardam exatamente o desenho atual e diferem na cor; C acrescenta fagulhas e crosta, e em 16 px a crosta some e as fagulhas viram sujeira. B mantém o tile grafite do PLN-007 (menor mudança no ícone do Dock) e o halo se reduz bem a 16 px. Suposição: no tray do macOS o ícone é monocromático (template), então o tratamento colorido só vale para o app e a janela.
- **Ideias:**
  - Manter o "dev" com a bolinha azul como está, e testar A/B/C em 16 px no Dock real e no tray antes de fechar (ousadia: baixa).
  - Versão mono 16 px própria, sem halo, com a chama preenchida e o circuito a 1 px (ousadia: baixa).
  - Tile do modo claro igual ao do escuro, sem inverter (ousadia: média).
- **Risco:** B é o menos distinto de "hoje" à primeira vista no 48 px, e a mudança pode parecer pequena demais para um rebranding.
- **Confiança:** 65/100

#### 4. A brasa viva na interface

- **Posição:** o Enviar fica cinza em repouso e laranja só no foco ou quando há texto; a brasa que respira entra só no "trabalhando".
- **Por quê:** lido: hoje o Enviar é neutro e ganha a marca no foco; o protótipo o deixa 07 o tempo todo e o próprio briefing admite que "o foco muda menos". Suposição: se tudo é brasa, nada é brasa; o laranja permanente reduz o valor do sinal.
- **Ideias:**
  - Respiração da chama: opacidade 0,85↔1 a 2,4 s com `ease-in-out`, desligada em `prefers-reduced-motion` (ousadia: baixa).
  - Enviar com texto digitado vira 07 (estado "pronto"), vazio fica `--text-muted` (ousadia: média).
  - Fagulha única ao concluir a resposta, 600 ms, na chama do cabeçalho; nada de cinza que esfria (ousadia: média).
- **Risco:** o Enviar cinza esconde a ação principal em primeira visita, e o estado "pronto" é mais um estado para testar.
- **Confiança:** 60/100

#### 5. Narrativa, voz e rollout

- **Posição:** "Carvão em Brasa" é o nome interno do tom, não um slogan; a voz muda pouco e o lançamento é um único release, sem campanha.
- **Por quê:** suposição, sem dado: o brasa-e-carvão só se sustenta se os nomes de token o dizem e o texto do app continua dizendo o que o app faz. Os tokens ganham nomes de camada, não de metáfora.
- **Ideias:**
  - Tokens `--ember-500`, `--ember-600`, `--ember-700` e `--coal-900…600`, com alias para os atuais `--brand-gradient` por uma versão (ousadia: baixa).
  - Microcópia: "Pensando…" fica; só o vazio ganha uma linha "A brasa está acesa. Pergunte." (ousadia: média).
  - Rollout em duas ondas: (1) cor e tokens atrás de uma flag `brandBrasa`, (2) símbolo no ícone do app, depois de duas semanas sem regressão (ousadia: baixa).
- **Risco:** microcópia poética em ferramenta de código vira ruído; a flag duplica o CSS por um tempo.
- **Métrica de sucesso:** 0 regressão de contraste (todo par texto/fundo ≥ 4,5:1, texto grande ≥ 3:1, conferido por teste automático) e nenhum aumento nas respostas "não achei o botão Enviar" no feedback das duas primeiras semanas.
- **Confiança:** 55/100

#### A ideia mais ousada desta rodada

O tema claro "Cinza de Cinzas": em vez de inverter o grafite, o claro é a própria cinza — `#F4F1EE`, a brasa no acento `#D84315` e o texto no carvão. Não é aquilo que o Guardião costuma propor, mas é o único jeito de o tema claro ser "Carvão em Brasa" sem um segundo conjunto de regras. Risco: o branco quente destoa dos lockups claros do PLN-007, feitos em branco puro.

#### Issues candidatas

- **Rampa de texto: token `--text-muted` e fim da 03 como texto** — a 03 dá 1,8:1 e hoje depende de um HEX fora da paleta — prioridade `high`
- **Erro fora da família da brasa, com ícone** — o `#ff6568` colide com a 07 — prioridade `high`
- **Tema claro "Cinza de Cinzas"** — o tema claro não está resolvido e o claro do PLN-007 não tem rampa — prioridade `medium`
- **Teste de 16 px do símbolo no Dock e no tray** — a escolha A/B/C deve sair de uma imagem real, não do mock — prioridade `medium`
- **Teste automático de contraste dos tokens** — impede a regressão que a métrica de sucesso mede — prioridade `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Carvão | Manter o `#1A1B1E`, aquecer sem azul, `--text-muted` novo | 72 |
| 2. Brasa | 07 só CTA/foco com texto escuro; erro em rosa frio | 68 |
| 3. Símbolo | B, a silhueta intacta, calor no núcleo | 65 |
| 4. Interface | Enviar laranja só no foco/pronto; respiração só no "trabalhando" | 60 |
| 5. Narrativa e rollout | Tom interno, tokens `ember/coal`, duas ondas atrás de flag | 55 |

<!-- fim-rodada-1 -->

### Rodada 2: a confiança na proposta de plano

Suposição: li a v3.1 inteira e as imagens da rodada 1; não conferi os números de contraste e de pico de luminância, que tomo como medidos pela coordenação.

#### A confiança

| Parte | Confiança (0–100) | Uma linha |
| :---- | :---------------- | :-------- |
| O plano inteiro | 79 | Muda a cor e o calor e deixa o traçado, o logotipo e as quatro filhas; é o que o PLN-007 pedia que se guardasse. |
| Tabela de tokens | 74 | Boa, e o "efetivo depois do mix" é honesto, mas são muitos HEX para um mini-rebranding e o claro ainda está "a testar". |
| Fases 0–3 (tokens, ações, movimento) | 80 | Flag, `--action-brand` fora do `--primary` e variante `brand` sem trocar o `default` são a menor mudança que entrega. |
| Fase 4 (símbolo) | 66 | O desenho fica, mas a B perde para o de hoje na massa quente a 16 px (83 contra 96) e os tiles mudam. |
| Fases 5–6 (portões, ativos) | 68 | Portões bem postos; 6–10 h e duas semanas de uso de uma só pessoa carregam muito. |
| As medições de sucesso | 62 | Mensuráveis, mas cinco pessoas são sinal, não prova, e o símbolo pequeno não tem métrica própria. |

#### Onde a proposta diverge da sua rodada 1

1. **Texto secundário:** eu dava `--text-muted: #A8A6A3` e fundo `#1B1B1D`; a proposta mantém o `#1A1B1E` e põe a origem `#C4BEB9` por causa do mix de 83%. Me convenceu: o fundo intacto é ainda menos mudança, e eu não tinha visto o mix.
2. **Enviar:** eu pedi laranja com texto digitado; a R8 acende por texto ou anexo válido, sem depender do foco. É a mesma ideia, com leitura no código (`native-chat-composer-send-state.ts:39-59`). Me convenceu.
3. **Símbolo:** eu escolhi B, intacta; a proposta escolhe B com o rescaldo largo, e a minha "chama intacta" vira "centro `#FFB088`". Me convenceu só pela regra de saída, que devolve o de hoje inteiro se a B não ler como ele. Sem a regra, não.

#### O erro que a proposta ainda tem

A regra de saída da R7 não tem critério: "se a B ajustada não ler como a de hoje a 16 e 32 px no teste" não diz que teste, nem quanto. A fase 4 só mede reconhecimento isolado entre seis chamas (≥ 4/5) e o pico de luminância, e nenhum dos dois é "ler como a de hoje". A regra que protege o meu valor mais caro, o símbolo, fica sem gatilho.

#### O seu voto nas decisões de Anderson

| Decisão | Opção | Confiança |
| :------ | :---- | :-------- |
| 1. Tray e Dock | Adiar; o tray já tem estado âmbar de atenção (`system-tray.ts:64-93`) e o símbolo ainda não saiu do teste | 78 |
| 2. Símbolo | B com o rescaldo largo, sem halo, com o topo claro como segundo braço do teste e um limite numérico na regra de saída | 62 |
| 3. Flag | Duas semanas no uso de Anderson | 76 |
| 4. Fundo | `#1A1B1E` | 85 |
| 5. Onde o plano mora | `brand`, ao lado do PLN-007 | 82 |
| 6. Norma do rótulo da ação | WCAG 2.x com rótulo escuro (4,85) e o APCA como aviso | 80 |

<!-- fim-rodada-2 -->

## O que ficou

## Fora do workspace

Nada.
