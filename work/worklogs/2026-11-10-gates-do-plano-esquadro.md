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

# Reunião gates do plano: a participação de Esquadro, regra e consistência

O pedido de Anderson, em 2026-11-10, na sessão da coordenação (`01a1c81f-d759-7593-8aca-ce78f6ea32cd`): "Gates até o plano, corte 00:45 (Recomendado)". Este é o registro de **Esquadro** — persona regra e consistência, no Claude `claude-sonnet-5-5` `medium` —, aberto pela coordenação. A pauta e as regras estão no briefing da reunião; cada rodada é uma seção abaixo, acrescentada no fim do arquivo.

## O que se fez

### Rodada 1: opinião inicial

- **Posição:** Gate com id estável e campo que o checador barra; nome novo, sem colidir com phase, P ou D.

Suposição: gate é campo de leitura fixa na tarefa, não letra de heading. Hora de fechamento: 22:30 (relógio).

#### 1. Pendência e dono

- **Posição:** Variante de A: o gate mora na tarefa, com id `T<n>` dentro da fase `F<n>`, e a fase só declara `bloqueia:`/`bloqueada_por:` entre ids de fase.
- **Por quê:** `phase` do frontmatter é o ciclo do plano (*lido*, `plans/README.md`, tabela phase/status, ~l.25). O parser da `plan_md.py` só aceita a letra `P` no heading, e dependência é prosa (*lido*, briefing). O checador já valida `depends_on` por ID de plano com ciclo (`_find_dependency_cycle`, *lido*, `check_notes.py`:468), então bloqueio entre ids tem precedente barrável. Dono em prosa livre vira sinônimo para o mesmo id (*suposto*, 70).
- **Ideias:** (1) campo fixo na tarefa `pendente: <o quê> · dono: <Anderson|sessão|papel>`, com vocabulário fechado de dono, que o checador barra se faltar numa tarefa aberta (ousadia: baixa). (2) `bloqueada_por: [F1]` na fase, com o checador barrando id inexistente e ciclo, copiando o `_find_dependency_cycle` (ousadia: média). (3) Nome do gate: `gate`, nunca `phase`/`fase` no frontmatter; a "fase" da leva ganha outro substantivo se colidir (ousadia: baixa).
- **Risco:** Confundir fase-leva com `phase` do frontmatter mesmo com nome distinto; exige renomear a leva (ex.: `leva`) — custo de migração só em plano novo.
- **Confiança:** 72/100

#### 2. Unidade de autorização

- **Posição:** A tarefa, com o pedido de Anderson, hora e evidência em campos fixos; o passo interno é roteiro sem autorização própria.
- **Por quê:** Hoje hora, evidência e pedido estão no passo (*lido*, `plan-template.md`, seção Passos, via briefing). Duas unidades de autorização, tarefa e passo, dão dois lugares para o mesmo fato e sinônimo na prosa (*suposto*, 75). Loop inteiro em toda tarefa não tem id para citar (*suposto*, 60). O checkbox do passo continua, mas sem valor de gate.
- **Ideias:** (1) `autorizada: <frase literal de Anderson> · <HH:MM do date>` na tarefa, que o checador exige antes de marcar a tarefa feita (ousadia: média). (2) `evidência:` na tarefa aponta para o ID/link por definição já decidido, rótulo igual ao H1 (ousadia: baixa). (3) Passo vira lista numerada `P1.1` sem parser, só prosa (ousadia: baixa).
- **Risco:** Tarefa grande demais autoriza passo arriscado de carona; mitigação é teto de passos por tarefa, e isso é regra nova sem molde hoje.
- **Confiança:** 68/100

#### 3. Quem executa

- **Posição:** No plano só a linha `executor:` com papel e camada; sessão, runtime, modelo e esforço continuam no `execucao.json`.
- **Por quê:** `executor.py open` já grava `--agent`, `--model`, `--effort` no manifesto (*lido*, briefing, `executor.py`); duplicar no plano cria dois ids para o mesmo fato e desvio garantido (*suposto*, 80). O plano guarda a intenção (papel e camada, como a tabela de modelos do AGENTS.md), o manifesto guarda o fato.
- **Ideias:** (1) `executor: <papel>/<camada>` com vocabulário fechado (`implementer/média`, `reviewer/alta`), barrável (ousadia: baixa). (2) O checador compara o `executor:` do plano com o `execucao.json` quando existir e avisa divergência (ousadia: alta).
- **Risco:** O texto do plano não responde "quem pode executar agora" sem abrir o manifesto; aceita-se, pois o gate de leitura rápida é a tarefa.
- **Confiança:** 66/100

#### A ideia mais ousada desta rodada

Um comando/regra do checador que lê o grafo `bloqueada_por` entre fases e as tarefas pendentes e imprime, por plano, a "fronteira executável" (tarefas cujas fases estão livres). Risco: vira código novo que está fora do tema desta reunião (a proposta sai antes do código); fica como issue.

#### Issues candidatas

- **Regra de checagem de gate (id, dono, ciclo)** — o gate só vale se o checador barrar o que falta — prioridade `high`
- **Vocabulário único: leva/fase vs `phase` do frontmatter** — evita colisão de nome na norma — prioridade `high`
- **Divergência plano × `execucao.json`** — dois lugares para o mesmo fato — prioridade `low`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Pendência e dono | Gate na tarefa, ids `F`/`T`, bloqueio entre fases barrável | 72 |
| 2. Unidade de autorização | Tarefa autoriza; passo é roteiro | 68 |
| 3. Quem executa | Plano guarda papel/camada; manifesto guarda o fato | 66 |

<!-- fim-rodada-1 -->

### Rodada 2: debate

- **Posição:** Mantenho D1a e D2a; em D3 ajusto: papel e camada no plano, política só se checável. (22:40)

#### As disputas

- **D1** (onde mora o gate): `D1a` — mantém — cinco das seis personas votam na tarefa (*lido*, `sintese-1.md`). O `corte:` da Centelha é um terceiro nível sem destino no molde, e a letra nova só vale com checagem. Aceito o bloco só como cabeçalho da fase para `bloqueada_por:`, nunca como dono do gate. — 74/100
- **D2** (o que Anderson autoriza): `D2a` — mantém — um pedido por fase junta tarefas de risco diferente numa só frase de Anderson, e a evidência passa a apontar para a fase, não para o que mudou. Concedo à Lamina o bloco só quando a leva é declarada no pedido, citando os ids `T` autorizados. — 70/100
- **D3** (o que o plano guarda de quem executa): `D3a` — ajusta — o runtime sai do plano (D3b/D3c): é fato que muda com a cota (*lido*, briefing: cota medida às 22:22) e vira divergência permanente com o `execucao.json`. Guardo `executor: <papel>/<camada>`, e a restrição só entra se for um campo de vocabulário fechado que o checador barra. — 72/100

#### Os ataques

- **Centelha, D3c (só `runtime:` no corte):** é o único dado do executor que o manifesto grava depois por conta própria (`--agent`, `--model`, `--effort` no `executor.py open`, *lido*) e o único que muda com a cota; vira dois ids para um fato, e o plano nasce desatualizado. Derruba o ataque: mostrar que o `executor.py` não grava runtime, ou que o checador compara plano e manifesto.
- **Lamina, D3b (papel, runtime, modelo e esforço no plano):** quatro campos copiados são quatro chances de sinônimo para o mesmo valor (`opus` / `claude-opus-5-5` / `alta`), sem vocabulário no molde (*suposto*, 75). Derruba: vocabulário fechado publicado no `plans/README.md` e checado, mesmo custo que eu já pago em D1.

#### A concessão

Calibre, M1: a frase de ordem não é dependência (`P10 depends []` medido pela coordenação, *lido* na síntese). Mudou: a ideia de `bloqueada_por:` em ids de fase só vale se for campo, nunca prosa, e o checador deve barrar a fase sem ele quando há "depende" em texto. Concedi que o nome e a regra vêm antes do parser.

#### "Sim, e…"

Oficio: "lista curta do que é meu" — sobre ela, o gate de tarefa ganha `dono:` com vocabulário fechado (`Anderson`, `sessão`, `papel`), e a lista de Oficio vira consulta do checador, não texto escrito à mão. (ousadia: média)

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem ou o que te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :--------------------- |
| 1. Pendência e dono | D1a, bloqueio por campo | 72 | 74 | ajustou | Calibre, M1 |
| 2. Unidade de autorização | D2a, bloco só com ids citados | 68 | 70 | ajustou | Lamina |
| 3. Quem executa | D3a com `executor: papel/camada` | 66 | 72 | ajustou | síntese: C3 |

<!-- fim-rodada-2 -->

### Rodada 3: voto final

- **Posição:** Apoio P1 com ressalva: `Pendente:`/`Pronto:` só com vocabulário fechado que o checador barre. (22:44)
- **Fatos lidos:** M1, M2 e M3 (`sintese-2.md`, *lido*); M3 reforça a ressalva: modelo no corpo da tarefa pode mentir.

#### O voto em cada proposta

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| P1 | apoio com ressalva | As duas linhas são o gate; sem barra no checador (id citado existe, versão presente, `F` sem ciclo) viram prosa; o plano nasce com a regra escrita no `plans/README.md` do playground, e a barra é issue de dependência (M2). | 76 |
| P2 | contra | `corte:` é nível novo sem destino no molde; um pedido por fase cobre tarefa criada depois sem citação; a Centelha já cedeu a lista de ids, que é o que P1 faz por tarefa. | 78 |

#### O que me faria mudar de ideia

- **P1:** se o teste mostrar que o parser da `plan_md.py` não passa uma linha livre sob o heading sem quebrar (*suposto*, não medi), o gate teria de ir a campo no heading.
- **P2:** se Anderson disser que prefere um clique por fase e aceitar a tarefa nova fora de cobertura sem aviso; ou se o checador barrar o corte com a mesma força que a tarefa.

#### A última ideia

`Pronto:` grava o pedido literal de Anderson, a hora do `date` e os ids com versão; o checador barra `Pronto:` cujo id citado mudou depois (versão velha vira `Pendente:` de novo). Fecha o buraco "tarefa editada depois do aceite". Risco: exige hash ou data por tarefa, que o molde não tem. (ousadia: média)

#### Os colegas

| Persona | A contribuição mais útil dela, em uma linha | Nota de 0 a 10 |
| :------ | :------------------------------------------ | :------------- |
| Calibre | M1: a seta `P9 → P10` não é dependência, medido no PLN-021 | 9 |
| Turno | Política visível e abertura registrada por tentativa | 8 |
| Lamina | M3: o papel já traz modelo default; o fato fica no manifesto | 9 |
| Centelha | O corte listando ids e a pergunta sobre um clique por fase | 7 |
| Oficio | "Lista do que é meu", que dá o dono com vocabulário fechado | 8 |

#### Autoavaliação

Fiel: votei pela colisão de nome e pelo que o checador barra, e contra o nível novo sem destino no molde. Saí dela ao aceitar o pedido em bloco (Lamina), que é regra nova; aceitei só com ids citados. Não medi o parser com linha livre; declarei como suposição.

<!-- fim-rodada-3 -->

## Custo da tarefa

Não medida — sessão sem turno medido · até 23:37 de 2026-11-10, pelo `brza note commit` · sem o turno do commit
