# O pedido de rodada

Um arquivo por rodada, `.sessions/<reuniao>/rodada-N.md`. A coordenação o envia com
`python3 -I .claude/skills/meeting-runner/scripts/launch_persona.py $R --send todas --round N`, que chama
`brza sessions send <sessões…> --text "Faça a rodada N: .sessions/<reuniao>/rodada-N.md"`. O CLI anexa ao texto o
protocolo da rodada (o status com o `round_id` daquele envio e o Dispatch da persona), e a mensagem chega como turno do
coordenador: a persona ocupada a recebe na virada do turno. Recibo `pending` ou `unknown` (saída 75) não autoriza envio
novo: espere com o `wait_round.py`, ou repita só aquela persona com `--operation <a mesma>` e o mesmo texto (R2.1).

## O molde comum (todas as rodadas)

```markdown
# Rodada N — ‹título› (prazo: ‹hh›h‹mm›)  ou  (duração: ~‹M› min)

‹O que ler antes, com caminho: a síntese anterior, a proposta, os worklogs dos colegas — ou "você ainda não vê o que os
outros escreveram" na R1.›  ‹O que fazer, em uma ou duas frases, como a persona.›

**Acrescente no fim** do seu worklog esta estrutura; a **última linha do arquivo** fica `<!-- fim-rodada-N -->`:

‹o molde markdown do tipo da rodada›

No máximo ~‹L› linhas. Não pergunte nada; decida e declare a suposição. Não faça commit. Hora no worklog só a de
`date '+%H:%M'`, rodado na hora. Depois de gravar a seção e o marcador, envie uma vez o status do protocolo abaixo
(o sinal de fim); não responda por mensagem e não envie `worker_done` agora.
```

**Dois sinais de fim.** O status do protocolo, com o `round_id` e o Dispatch daquele envio e do remetente da persona,
é o que a coordenação espera (R6.2): o `brza sessions wait` só conclui a rodada por ele, nunca por um status genérico ou
de outra rodada. O marcador na última linha do worklog é o registro que o `tally.py` lê. O `wait_round.py` avisa quando
uma persona mandou o status sem fechar o worklog.

**Duração é o padrão; o painel entende as duas formas** (com `(duração: ~5 min)` o prazo vira a abertura mais a duração). Os prazos em hora das duas reuniões não eram monotônicos (a R4 da Carvão tinha prazo anterior ao
da R3) e ninguém os cobrou. A duração anunciada também é o piso da espera: o `wait_round.py` não encerra antes dela
mais 2 min, contados do envio (X6).

**Toda seção traz `**Posição:**`** — uma linha de até 100 caracteres, a mais importante da rodada, em português claro.
`tally.py` a lê e o painel a mostra antes de a coordenação sintetizar; a coordenação a sobrepõe no `sintese-N.json`
quando não serve. Na tabela de assuntos a linha vira a coluna "Posição em uma linha"; nos tipos 3 e 4 é uma linha à parte
acima da tabela.

## Tipo 1 — opinião independente (R1)

```markdown
### Rodada 1: opinião inicial

- **Posição:** a sua tese da rodada, em até 100 caracteres.

#### 1. ‹assunto da pauta›

- **Posição:** a alternativa em uma frase.
- **Por quê:** até cinco linhas; cada fato marcado *medido*, *lido* (com a fonte) ou *suposto*.
- **Ideias:** no mínimo duas, concretas (comando, arquivo, componente), cada uma `(ousadia: baixa|média|alta)`.
- **Risco:** o que pode dar errado com a sua posição.
- **Confiança:** NN/100

(um bloco por assunto da pauta; ~12 linhas cada)

#### A ideia mais ousada desta rodada

Uma só, em até cinco linhas, com o risco.

#### Issues candidatas

- **Título** — o porquê em uma linha — prioridade `high|medium|low` (de duas a quatro)

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. ‹assunto› | … | NN |

<!-- fim-rodada-1 -->
```

Isolamento: "Você ainda não vê o que os outros escreveram. **Não leia os worklogs dos colegas.**" A coordenação confere por
`grep` do nome das outras personas na seção de cada uma.

## Tipo 2 — debate (R2)

Leia antes a `### Rodada 1` dos outros worklogs e a síntese da coordenação (ela traz dados medidos M# que podem mudar a
posição). "Dado medido pesa mais que argumento."

```markdown
### Rodada 2: debate

- **Posição:** o que mudou ou ficou, em até 100 caracteres.

#### As disputas

- **D1:** voto (letra, ou "e: …") — argumento em até três linhas — NN/100

#### Os ataques

Dois ataques, a posições de personas diferentes: quem, o assunto, o argumento e o que derrubaria o seu ataque.

#### A concessão

Pelo menos uma ideia ou dado que te moveu: quem (ou qual M# da síntese), o quê, e o que mudou. Se nada, diga por quê.

#### "Sim, e…"

Uma ideia nova construída sobre a de outra persona (diga o autor), `(ousadia: …)`.

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem ou o que te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :--------------------- |

<!-- fim-rodada-2 -->
```

~40 linhas no total. A coluna "Mudou?" alimenta `virada` no `estado-rN.json`.

## Tipo 3 — voto e notas (R3)

```markdown
### Rodada 3: voto final

- **Posição:** o seu voto central, em até 100 caracteres.
- **Fatos lidos:** os M# da síntese anterior que você leu antes de votar (M1, M4…), ou "nenhum novo".

#### O voto em cada proposta

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| P1 | … | … | NN |

#### O que me faria mudar de ideia

Para as duas propostas de maior confiança: o fato ou o teste que derrubaria o seu voto.

#### A última ideia

A ideia que ninguém trouxe e que você levaria ao plano, `(ousadia: …)`, em até cinco linhas.

#### Os colegas

| Persona | A contribuição mais útil dela, em uma linha | Nota de 0 a 10 |
| :------ | :------------------------------------------ | :------------- |
(as outras N−1 personas)

#### Autoavaliação

Em até três linhas: em que você foi fiel à sua persona, e em que saiu dela.

<!-- fim-rodada-3 -->
```

~45 linhas. Quando a rodada 3 é de confiança no plano (sem voto), use no lugar do voto a tabela da MCP: "Parte do plano |
Confiança (0–100) | Uma linha de porquê", com a linha final **`**O plano inteiro**`** — é dela que `tally.py` tira a
confiança —, e o erro que você vê, a mudança que mais subiria a confiança, a decisão que é de Anderson e a nota aos
colegas.

## Tipo 4 — confiança final e autoavaliação (última)

```markdown
### Rodada N: a confiança final

- **Posição:** a sua posição final, em até 100 caracteres.
- **Fatos lidos:** os M# da síntese anterior que você leu antes desta confiança (M1, M4…), ou "nenhum novo".

| Parte do plano | Confiança na versão anterior | Confiança na versão atual | Uma linha de porquê |
| :------------- | :------------------------- | :------------------------ | :------------------ |
| **O plano inteiro** | NN | NN | … |

- **A sua mudança da rodada anterior entrou?** sim/em parte/não, com a fonte.
- **O que ainda está errado:** o que falta, com a seção.
- **Autoavaliação:** até três linhas: fiel à persona e onde saiu dela.

<!-- fim-rodada-N -->
```

## Antes de toda rodada com voto: a síntese com os fatos

Os tipos 3, 4 e 5 só se enviam **depois** da síntese da rodada anterior (`references/synthesis.md`), e o pedido diz o que
ler: "Leia antes `.sessions/<reuniao>/sintese-‹N−1›.md`, os fatos M‹…› (os novos desta rodada estão marcados)". A persona
declara a linha `**Fatos lidos:**`; o `tally.py` avisa quem votou sem ela. Na P7 o fato decisivo (0 PRs, medido pelo
Prumo) nasceu na rodada do voto, e duas personas votaram sem ele (X10).

## Tipo 5 — voto informado (rodada extra, para parte da sala)

A rodada extra é **automática quando o gatilho vale** (R8 de Anderson, 2026-11-09): um fato novo, nascido na própria
rodada de voto e conferido pela coordenação, contradiz a premissa de algum voto. A coordenação sintetiza o fato, publica a
síntese e envia esta rodada sem pedir licença para a extensão; sem gatilho, não há rodada extra. O pedido cita o M# e a
premissa que ele contradiz. **A quem ela vai, a coordenação escolhe caso a caso e registra o motivo antes do disparo** (R9 de
Anderson), no `sintese-N.json` e na narração: parte da sala ou a sala inteira, sem composição fixa. Quando for parte da
sala, ela vai só a essas personas (`--send Trava Relance
--round N`, `wait_round.py N --personas Trava Relance`, `tally.py N --participantes Trava Relance`). O molde reusa o
cabeçalho que o `tally.py` lê; o improvisado da P7 (`#### O voto`, propostas `A`/`B`) não era lido (X17).

```markdown
### Rodada N: o voto informado

- **Posição:** o seu voto, em até 100 caracteres.
- **Fatos lidos:** os M# que motivaram esta rodada (M6, M6b…).

#### O voto em cada proposta

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| A | … | … | NN |
| B | … | … | NN |

- **O que o fato mudou em você:** até três linhas; "nada" vale, com o porquê.
- **O que te faria mudar de novo:** o fato ou o teste que derrubaria o seu voto.

| Parte do plano | Confiança na versão anterior | Confiança na versão atual | Uma linha de porquê |
| :------------- | :------------------------- | :------------------------ | :------------------ |
| **O plano inteiro** | NN | NN | … |

<!-- fim-rodada-N -->
```

~20 linhas. As propostas podem ser `P1…` ou as letras das alternativas.

## Limites de linha de referência

R1 ~12 por assunto; R2 ~40; R3 ~45 (voto) ou ~30 (confiança no plano); última ~15–25. Rodada de contraprova (opcional):
ver `references/proposal.md`.
