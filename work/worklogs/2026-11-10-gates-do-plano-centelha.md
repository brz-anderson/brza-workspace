---
scope:
  - workspace
tags:
  - planning
refs:
  - PLN-021
sessions:
  - 01a1c81f-d759-7593-8aca-ce78f6ea32cd
---

# Reunião gates do plano: a participação de Centelha, a provocadora

O pedido de Anderson, em 2026-11-10, na sessão da coordenação (`01a1c81f-d759-7593-8aca-ce78f6ea32cd`): "Gates até o plano, corte 00:45 (Recomendado)". Este é o registro de **Centelha** — persona a provocadora, no Grok `grok-4.7-build-fast` `low` —, aberto pela coordenação. A pauta e as regras estão no briefing da reunião; cada rodada é uma seção abaixo, acrescentada no fim do arquivo.

## O que se fez

### Rodada 1: opinião inicial

Hora: 22:30 (`date '+%H:%M'`).

- **Posição:** D, gate no corte: um pedido por fase, pendência com dono, runtime no plano.

#### 1. Pendência e dono

- **Posição:** Quarta forma, o corte: a fase não é o gate; um bloco `corte:` debaixo do heading da fase é.
- **Por quê:** A, B e C escondem a pendência no lugar errado. A põe dono em cada tarefa e a leva vira o `P` com outro nome. B espalha dono no passo. C dá um dono à fase inteira e a tarefa herda o bloqueio sem mostrar o que falta. *Lido:* o `phase` do frontmatter é o ciclo do plano (`interview`…`dropped`), com `blocked` já exigindo `blocks` e `owner` (`plans/README.md` linhas 25–32 e 36–37). *Lido no briefing:* fase é leva, sem dependência interna, e pode bloquear ou ser bloqueada; isso não é o `phase`. *Suposto:* o heading da leva ainda não existe no molde, então o `corte:` cabe nele sem colidir com `phase:`.
- **Ideias:** (1) Heading `## Fase N — <nome>` e, na linha seguinte, o bloco `corte:` com `pendente:`, `dono:` e `bloqueado-por:` / `bloqueia:` apontando outra fase, nunca o `phase:` (`ousadia: média`). (2) Cada item de `pendente:` é uma linha `- [ ] <o que falta> — dono: <papel>`, visível sem abrir a tarefa (`ousadia: baixa`).
- **Risco:** Dois donos convivem: o `owner` do `phase: blocked` e o `dono:` do corte. Quem lê o frontmatter acha que a pendência já está lá.
- **Confiança:** 78/100

#### 2. Unidade de autorização

- **Posição:** Anderson autoriza o corte, uma vez; tarefa é o trabalho, passo continua roteiro.
- **Por quê:** Autorizar cada tarefa (A) multiplica pedido. Autorizar cada passo (B) piora. Autorizar a fase inteira (C) esconde qual corte liberou o quê. *Lido:* "Passo de plano só executa a pedido explícito de Anderson, passo a passo" (`plans/README.md` linhas 36–37). *Lido no briefing:* o checkbox do passo não tem id nem hora; hora, evidência e o pedido estão no passo; a unidade (tarefa, passo ou loop) ficou para esta sala. *Suposto:* um pedido no corte, com hora e evidência, cobre a leva; o passo deixa de repetir o pedido.
- **Ideias:** (1) No `corte:`, as linhas `pedido:`, `hora:` e `evidencia:` — as únicas da leva (`ousadia: média`). (2) A tarefa vira `### T1` sem `pedido:`; o `Pn` fica prosa de roteiro, como o parser já só aceita essa letra (*lido no briefing*, `plan_md.py`) (`ousadia: alta`).
- **Risco:** A norma de hoje exige pedido no passo. O corte único fica ilegal até a norma mudar, e alguém executa a leva inteira com um sim.
- **Confiança:** 74/100

#### 3. Quem executa

- **Posição:** O plano guarda no corte só o `runtime:`; sessão, agente, modelo e esforço continuam no `execucao.json`.
- **Por quê:** A e B copiam para o plano o que o `executor.py open` já grava fora dele. C deixa "quem executa" na tarefa e o gate não escolhe nada. *Lido no briefing:* `executor:` é a linha de quem executa no texto; sessão, runtime, modelo e esforço nascem em `--agent`, `--model`, `--effort` e ficam no `execucao.json`. *Lido no briefing, medido pela coordenação às 22:22:* `brza quota --json` já escolhe runtime (claude 46, codex 0, grok 34, antigravity 3). *Suposto:* repetir os cinco campos no plano divide a verdade; o corte só crava o runtime que a cota escolheu.
- **Ideias:** (1) Linha `runtime:` dentro do `corte:`, um valor, sem sessão nem modelo (`ousadia: baixa`). (2) A linha `executor:` da tarefa sai do molde; o dono da pendência não é o runtime (`ousadia: alta`).
- **Risco:** Sem sessão no plano, duas aberturas no mesmo runtime disputam a leva e o `execucao.json` é a única prova — quem lê só o plano não vê o conflito.
- **Confiança:** 72/100

#### A ideia mais ousada desta rodada

Matar o `executor:` e o pedido dentro do `Pn`. O que A, B e C não são: um bloco `corte:` por fase, com `pendente`/`dono`, um `pedido`/`hora`/`evidencia` e um `runtime`. O `Pn` volta a ser roteiro. Risco: o checador e a frase "passo a passo" (`plans/README.md` 36–37) quebram no mesmo dia, e a leva inteira sai com um sim só.

#### Issues candidatas

- **O molde ganha `## Fase` e o bloco `corte:`** — A, B e C não separam pendência de `phase` nem de `Pn` — prioridade `high`
- **Pedido, hora e evidência saem do passo e vão ao corte** — o checkbox do passo não tem id nem hora, e repetir pedido em cada `Pn` é o custo que a sala quer cortar — prioridade `high`
- **`executor:` sai da tarefa; `runtime:` fica no corte** — sessão, agente, modelo e esforço já moram no `execucao.json` — prioridade `medium`
- **O checador distingue `owner` do `phase: blocked` e `dono:` do corte** — dois campos de dono no mesmo arquivo mentem um para o outro — prioridade `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Pendência e dono | Bloco `corte:` na fase, com pendência e dono | 78 |
| 2. Unidade de autorização | Um pedido no corte; passo é roteiro | 74 |
| 3. Quem executa | Só `runtime:` no plano; o resto no `execucao.json` | 72 |

<!-- fim-rodada-1 -->

### Rodada 2: debate

Hora: 22:40 (`date '+%H:%M'`).

- **Posição:** Corte segue, mas lista as tarefas do pedido; o plano guarda papel, não runtime.

#### As disputas

- **D1** (onde mora o gate): voto `D1b` — ajusta — O corte continua o gate. O M1 derruba a prosa: `P9 → P10` não entra em `depends`, e o `plan_md.load` devolve `P10 depends []`. Cada `pendente:` do corte nomeia o id da tarefa; senão o bloqueio da fase mente como a seta. — 76/100
- **D2** (o que Anderson autoriza): voto `e: D2b com a lista de ids autorizados` — ajusta — Um pedido por fase, e o corte escreve quais tarefas ele cobre. Tarefa nascida depois da hora, ou que saia do `playground` (M2), fica de fora e pede de novo. Autorizar a fase muda sem nome é o cheque que a Lamina já temeu. — 70/100
- **D3** (o que o plano guarda de quem executa): voto `D3a` — concede — Abandono o `D3c`. A Lamina mediu: `--agent` é runtime, não papel (`executor.py`). Cravar runtime no corte repete a mentira que ela descreveu (plano diz Sonnet, a cota abre Codex). O plano guarda papel e agente sugerido; sessão, runtime, modelo e esforço ficam no `execucao.json` (C3). — 80/100

#### Os ataques

- **Lamina, D1.** A linha de gate debaixo do `### Pn` é o `P` com outro nome. O M1 mostra que a frase ao lado do passo não é dependência. O que derrubaria: a linha ser campo que o `plan_md.py` lê, não prosa fundida no `executor:`.
- **Oficio, D2.** O cansaço de 11 pedidos no PLN-021 é o passo, não a prova de que a tarefa é o grão certo. Se cada `Pn` virar tarefa, o clique único volta a ser onze. O que derrubaria: a contagem de tarefas ficar bem menor que a de passos.

#### A concessão

A Lamina, no risco do pedido da leva, e o M2. O corte deixa de autorizar "a fase" e passa a listar os ids escritos antes da hora. O `runtime:` sai do plano.

#### "Sim, e…"

Sobre a fila de um clique do Oficio: o `corte:` da fase é essa fila, com três marcas nas linhas de `pendente:` — `sua`, `roda`, `bloqueada` — sem reescrever o `Retomar` a cada abertura (`ousadia: média`).

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem ou o que te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :--------------------- |
| 1. Pendência e dono | `D1b`: corte nomeia o id da tarefa | 78 | 76 | ajustou | M1, Calibre |
| 2. Unidade de autorização | Um pedido no corte, com a lista de ids | 74 | 70 | ajustou | Lamina; M2 |
| 3. Quem executa | `D3a`: papel e agente sugerido | 72 | 80 | virou | Lamina; C3; Oficio |

<!-- fim-rodada-2 -->

### Rodada 3: voto final

Hora: 22:44 (`date '+%H:%M'`).

- **Posição:** Voto P2: o corte da fase lista os ids; contra P1, que espalha o pedido.
- **Fatos lidos:** M1, M2, M3.

#### O voto em cada proposta

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| P1 | contra | O gate volta para debaixo de cada tarefa e cada uma copia o pedido; isso é o `P` com a linha `Pendente:` | 72 |
| P2 | apoio | O corte lista só os ids já escritos; tarefa nova ou fora do `playground` não entra (M2) | 74 |

#### O que me faria mudar de ideia

- **P1:** eu apoiaria se um comando mostrasse que a linha `Pendente:`/`Pronto:` é campo que o checador barra quando falta, e que o número de tarefas fica bem menor que o de `Pn`. Sem isso, a linha é a seta do M1: prosa que `plan_md.load` não vê.
- **P2:** eu viraria contra se o corte autorizasse um id que não está na lista, ou se a abertura não recusasse tarefa de outro workstream. Aí o pedido único mente, e o M2 ficou só no texto.

#### A última ideia

O `executor.py open` recusa a tarefa cujo id não está num `corte:` com `Pronto`, e recusa de novo se o corpo da tarefa mudou depois da hora do pedido. O M3 mostra que o papel já traz `model:` (`implementer` e `collector` sonnet; `reviewer` e `designer` opus): o plano não repete modelo. A trava é na abertura, não mais uma linha. (`ousadia: alta`)

#### Os colegas

| Persona | A contribuição mais útil dela, em uma linha | Nota de 0 a 10 |
| :------ | :------------------------------------------ | :------------- |
| Calibre | O M1: a seta não é `depends`, medido no `plan_md.load` | 9 |
| Lamina | O M3 e o risco do pedido que cobre tarefa nascida depois | 8 |
| Esquadro | Id estável e restrição só quando o checador barra | 7 |
| Oficio | Papel no plano e o fato da abertura fora dele, com a fila visível | 7 |
| Turno | A configuração efetiva fica no manifesto, por tentativa | 6 |

#### Autoavaliação

Fiel ao manter o corte contra cinco: A, B e C, e agora o P1, ainda deixam o pedido grudado na unidade que o parser já chama de passo. Saí da provocação no D3, e mantenho: cravar runtime no plano era ousadia que o M3 e a cota desmentem.

<!-- fim-rodada-3 -->

## Custo da tarefa

Não medida — sessão sem turno medido · até 23:37 de 2026-11-10, pelo `brza note commit` · sem o turno do commit
