---
name: plan-runner
description: >-
  Conduz um plano como sessão coordenadora: decide se o trabalho vira worklog ou PLN em plans/, entrevista em rodadas,
  desenha (com consultores por Agent ou em sessões, e artboards de tela pela screen-artboards), planeja, abre e
  acompanha as sessões executoras de cada passo pelo brza sessions, traz a evidência de volta ao plano, publica o painel
  de andamento e fecha. Use sempre que alguém falar em plano — "vamos planejar X", "retomar o PLN-001", "onde isso
  parou?", "execute o P3", "abre a sessão do passo" —, quando um plano de implementação for aceito, ou o trabalho tiver
  lacuna a entrevistar ou não couber numa sessão. Não use para trabalho de uma sessão só e sem lacuna (vai direto ao
  worklog), conserto de uma linha nem auditoria. Não use se você é a sessão executora de um passo (o seu prompt começa
  com "Você executa o passo Pn do PLN-NNN") nem consultor do Desenho (o prompt diz "Você é consultor do Desenho"):
  esses só seguem o pedido que receberam.
---

# Plano — decidir, abrir, coordenar a execução e fechar

Um plano responde a uma pergunta só: **como estou fazendo este trabalho**. Ele guarda o que foi perguntado e decidido,
como fica o que vai ser construído, o que fazer em que ordem e com que prova, e se o entregue cumpre. Mora em `plans/`,
na raiz do brza-workspace, e lá fica: o `PLN` fechado ganha `status: done` e continua citável por `PLN-NNN/R2.1`, depois
que o durável saiu para a casa dona — a decisão em `work/decisions/`, a norma do `brza-studio` — e o resumo foi ao commit
ou ao pull request.

Estado: **v2, protótipo** — reescrita do PLN-021, vive só na branch `workstream/playground` (PLN-021/R3.1); a master e os
outros workstreams seguem com a v1 do core até a promoção. A v1 conduzia tudo na mesma sessão e deixava o passo de código
"numa sessão nova" sem quem a abrisse nem lesse a evidência; a v2 coordena essas sessões por script, como a
`meeting-runner` coordena as personas.

**A norma é a do [`plans/README.md`](../../../plans/README.md)** — o número pelo `brza note plan-open`, o mapa de
`phase` e `status`, as origens, o que fecha — e a do [`work/README.md`](../../../work/README.md), para as propriedades
comuns, os links, o commit e o worklog. A norma das rodadas é a do `AGENTS.md` ("Decisões pendentes vão em rodadas de
perguntas", "Quem pergunta e grava é a sessão principal"); esta skill não a repete.

## Quem é quem

- **A coordenação** é a sessão principal, a que Anderson abriu: pergunta, desenha, abre e acompanha executores e
  consultores, confere a evidência por comando e **é a única que grava o plano**.
- **O executor** é uma sessão aberta pelo `executor.py` para um passo — código no `brza-studio`, protótipo, revisão. Grava
  só o que o passo pede e o worklog dele; nunca o plano, nunca pergunta a Anderson, e para no desvio que muda um `D`.
- **O consultor** é um `Agent` ou, no gatilho de decisão cara, uma sessão aberta pelo `consult.py`. Devolve alternativas
  com custo; não grava o plano, não decide.
- **Anderson decide** e ordena cada passo. Plano aceito não autoriza execução.

## Os arquivos e quando ler

| Preciso de… | Leia / rode |
| :-- | :-- |
| situar o trabalho, decidir se é plano e onde mora | esta SKILL.md, Passos 0 a 2 |
| o molde, antes da primeira linha do plano | `references/plan-template.md` |
| abrir, entrevistar, planejar | `references/open-and-plan.md` |
| gravar a rodada respondida na Entrevista | `$S/round_log.py PLN-NNN --from rodada.json` (o número: `--next`) |
| desenhar: Terreno, itens `D`, a rodada das alternativas | `references/design.md` |
| uma alternativa que muda o que se vê | a skill `screen-artboards` |
| consultores: `Agent` ou sessão, e a rodada lado a lado | `references/consultants.md`; `$S/consult.py open\|wait\|table\|close PLN-NNN D<n>` |
| retomar: onde o plano está, o próximo passo, o que não confere | `$S/plan_state.py PLN-NNN` (`--fix` reescreve as três horas) |
| executar um passo por sessão | `references/conduct.md` e `references/step-request.md`; `$S/executor.py open PLN-NNN P<n>` |
| esperar o executor, ler a evidência, fechar a sessão | `$S/executor.py wait\|evidence\|close\|status PLN-NNN …` |
| o painel do plano | sai sozinho dos scripts que mudam o estado; à mão, `$S/plan_panel.py publish PLN-NNN` |
| o que dizer no chat | `references/narration.md` |
| pedir a revisão, a forma do achado | `references/review.md` |
| fechar | `references/close.md`; `$S/close_check.py PLN-NNN` |
| conferir as notas, mover o plano | `../notes-checker/SKILL.md` |

**Convenção dos comandos:** da raiz do worktree, `python3 -I .claude/skills/plan-runner/scripts/<script>.py`; `$S` é só
abreviação nesta skill, e o comando se escreve por extenso (no zsh, a variável com espaço não se divide e falha). O plano se resolve pelo `PLN-NNN` (`plans/PLN-NNN-*/PLN-NNN-plan.md`, junto do `-interview` e dos `-design` quando
dividido) ou pelo caminho. O estado da execução é `.sessions/pln-nnn/execucao.json`, fora do git; a identidade das
sessões (Dispatch, Run, id do provedor) é a do `.sessions/sessions.jsonl` da raiz comum, que o `brza sessions` mantém.
O código de sessão, medição e visual é o de `.claude/scripts/skillkit/`, o mesmo da `meeting-runner`.

**Por que script, e não prosa:** soma de horas, `[x]` sem evidência, ID citado que não existe e a narração de chegada
eram regras escritas que falhavam em silêncio — na `meeting-runner`, a regra do painel escrita faltou em 3 aberturas e
em todas as chegadas antes de virar script (PLN-017/R10.1). Quando o script existe, o número e a conferência saem dele.

## Passo 0 — situar o trabalho

- **Ache a raiz do workspace**: `git rev-parse --show-toplevel`, de dentro do `brza-workspace`. Todo caminho desta skill
  — `plans/...`, `work/...` — é relativo a ela. Sem `plans/` ali, não abra plano em caminho inventado: diga que falta a
  pasta e pare.
- **Leia a norma de planos** — o `plans/README.md` e a seção de `work/worklogs/` do `work/README.md` — e o molde,
  `references/plan-template.md`. **O molde mora só nesta skill.**
- **O trabalho já tem plano?** Procure pelo assunto antes de abrir outro: `ls plans`, `grep -rli "<assunto>" plans
  work/worklogs`. Plano duplicado é o primeiro passo para dois estados do mesmo trabalho.
- **Veja o que trava agora**: as notas com `blocks` e `status` fora de `done` e `dropped`:

  ```bash
  grep -rl '^blocks:' work plans wiki | xargs grep -LE '^status: (done|dropped)'
  ```

- **Se o trabalho toca o código**, leia a norma do `brza-studio` (`~/Projects/brza-studio`, o `AGENTS.md` ou o
  `CLAUDE.md` dele) antes de desenhar.
- **Plano que já existe** — "retomar o PLN-NNN", "onde isso parou?", "execute o P3" — pula os Passos 1 e 2: rode
  `$S/plan_state.py PLN-NNN` e vá a `references/conduct.md`, "Retomar".

## Passo 1 — isso é plano?

**Plano é o documento de um trabalho que não cabe numa sessão só.** Abre quando qualquer um destes vale:

- há **lacuna a entrevistar** antes de alguém poder escrever — requisito aberto, escolha de desenho;
- o passo **precisa de detalhamento** — arquivos nomeados, subpassos com o teste que falha antes, o comando que prova;
- uma proposta **precisa de desenho** antes de virar decisão ou código — o plano pode parar no Desenho.

| Não abre plano                                  | Vai para                                                                          |
| :---------------------------------------------- | :-------------------------------------------------------------------------------- |
| Trabalho de uma sessão só, sem lacuna           | O worklog: o plano de implementação aceito abre a seção `## Plano aceito em …`    |
| Bifurcação com as opções já claras              | Uma nota em `work/decisions/`, `open`, sem desenho antes                          |
| Pergunta cuja resposta existe no mundo          | Uma issue `type: unknown` em `work/issues/`                                       |
| Auditoria de um artefato                        | Um parecer em `work/reviews/`                                                     |
| Conserto de uma linha                           | O commit                                                                          |

Quando a resposta for "não é plano", diga para onde vai e por quê. Plano de implementação já aceito não volta por este
filtro: vai ao Passo 2.

## Passo 2 — uma sessão ou várias

| O trabalho                                                                               | Onde o plano mora                                                                              |
| :--------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| Fecha nesta sessão, no mesmo dia                                                         | No worklog do trabalho, que o plano aceito abre: seção nomeada, com a data do aceite, imutável |
| Atravessa sessões — não fecha no dia, ou espera resposta ou entrega de fora desta sessão | Num `PLN` em `plans/`, com o `## Worklogs` citando o worklog de cada sessão                    |

O destino vai à primeira rodada, com a sua leitura como primeira opção. Plano que chega já aceito vai ao destino como
foi aceito, com a data e a frase de aprovação citada. Plano de worklog que passa a atravessar sessões é promovido a
`PLN`: o `PLN` nasce da seção datada, copiada com os mesmos IDs, e o worklog ganha a linha "promovido a `PLN-NNN`".
**Passo executado por sessão própria atravessa sessões por definição**: plano com executor vai a `PLN`.

## Quem grava — a coordenação

**Só esta skill decide o conteúdo do plano, e só a coordenação grava e commita em `plans/` e `work/`**, nos caminhos da
tarefa, pelo `brza note commit`, na branch do workstream, sem PR, com a identidade do `brz-anderson`.

1. **Grave só os caminhos da tarefa**: o plano, o worklog da sessão e os worklogs dos executores que ela abriu. O número
   do `PLN` sai do `brza note plan-open`. Confira com o checador
   (`python3 ${CLAUDE_SKILL_DIR}/../notes-checker/scripts/check_notes.py`) e com o `$S/plan_state.py` antes de commitar.
2. **O executor não grava o plano.** A evidência chega pelo worklog dele, e o `executor.py evidence --apply` a leva ao
   `### Pn` depois que você a leu e conferiu. Duas mãos no plano produzem dois estados dele.
3. **O que é de outra tarefa, esta sessão não executa** — outro plano, o trabalho de outra issue. Grava só o pedido, numa
   issue ou no `Retomar` do plano dono.
4. **A rodada vai com a resposta** nas palavras de quem respondeu, a data e a sessão, pelo `round_log.py`; respondida em
   outra sessão, entra sem perguntar de novo. Só a nota de `work/decisions/` passa pela confirmação de Anderson.

## O nome, a pasta e os IDs

**Todo `PLN` é uma pasta**: `plans/PLN-NNN-assunto/`, com o número que o `brza note plan-open` reservou.

| Arquivo                | O que guarda                                                                                                                                         |
| :--------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PLN-NNN-plan.md`      | Sempre. O frontmatter — só aqui —, o `Retomar`, o Pedido, os Passos, os Desvios, as seções de ponteiro e o Fechamento: é o arquivo lido para retomar |
| `PLN-NNN-interview.md` | A Entrevista, quando o `-plan` passa de ~400 linhas                                                                                                  |
| `PLN-NNN-design.md`    | O Desenho, pelo mesmo teto; `PLN-NNN-design-<assunto>.md` quando passa de ~800 linhas ou divide por assunto                                          |

O worklog é `work/worklogs/AAAA-MM-DD-assunto-em-kebab.md`. O do executor de um passo é
`AAAA-MM-DD-pln-nnn-pN-<assunto>.md`, criado pelo `executor.py open`.

| ID     | O que é                                       | Regra                                                |
| :----- | :-------------------------------------------- | :--------------------------------------------------- |
| `R3.2` | Rodada 3, pergunta 2 — o histórico da decisão | A Entrevista só cresce; nunca renumera               |
| `D3`   | Item do Desenho — o artefato vigente, escrito | Declara `origem: R3.2`; no `PLN`, reescrito no lugar |
| `P3`   | Passo                                         | Cita o `D` que executa                               |
| `X1`   | Desvio da execução                            | Curto; o passo cita o desvio                         |
| `A1`   | Achado da revisão                             | Na forma de `references/review.md`                   |
| `C1`   | Caso manual                                   | Só com o gatilho do teste em aparelho                |

Citação de fora: `PLN-NNN/D3`. Decisão reaberta ganha, na linha antiga, "→ reaberta em R10.1" (o `round_log.py` faz
isso com `reabre`), e o `D` passa a declarar a origem nova. O `plan_state.py` aponta o ID citado que não existe.

## Os consultores, em resumo

Leitura pesada e rascunho vão a um `Agent` — `collector` para o Terreno, `designer` para os itens `D` —, uma entrega por
chamada, e o laço é pedir, receber os pontos, fazer a rodada aqui, retomar o mesmo subagente com as respostas, até
cinco rodadas por lacuna. **A bifurcação com 3 ou mais alternativas e escolha cara de reverter** (contrato entre partes,
formato de dado gravado, norma), ou quando Anderson pede, abre os consultores **em sessões**, em modelos e runtimes
diferentes, pelo `consult.py` (PLN-021/R2.3): a diversidade de modelo só vale o tempo e a cota quando errar custa refazer.
O resto do detalhe — o pedido, a devolução, a tabela lado a lado — está em `references/consultants.md`.

## Operações

| Operação                                      | Quando                                                   | Reference                                              |
| :-------------------------------------------- | :------------------------------------------------------- | :----------------------------------------------------- |
| **Abrir → entrevistar → planejar**            | Trabalho novo, ou plano parado antes dos Passos          | `references/open-and-plan.md`                          |
| **Desenhar**                                  | O gatilho do Desenho vale                                | `references/design.md`, `references/consultants.md`    |
| **Conduzir** (retomar, executar por sessão)   | "Continuar", "execute o P3", "onde parou?"               | `references/conduct.md`, `references/step-request.md`  |
| **Pedir a revisão**                           | Todo passo `[x]` ou `[-]`                                | `references/review.md`                                 |
| **Fechar**                                    | Todo passo feito e todo achado com destino               | `references/close.md`                                  |

Leia `references/narration.md` antes de abrir o primeiro executor: é ela que diz o que Anderson vê no chat enquanto as
sessões rodam.

## Invariantes

**Só esta skill decide o conteúdo do plano, e só a coordenação grava.** O executor e o consultor devolvem; a coordenação
lê, confere e grava.

**`[x]` sem evidência não conta.** Evidência é o que outra pessoa refaz: o commit, o comando e o resultado,
`arquivo:linha`. "Os testes passam" não é evidência; `<comando> → 42 passed` é, e o commit vem com o repositório:
`brza-studio@a1b2c3d`. **O passo que tem `Estimado` fecha também com o `Executado`**, e o `plan_state.py --fix` reescreve
`executed_h` e `remaining_h` no mesmo ato. O `Executado` de um passo por sessão é a janela medida da abertura ao marcador
do executor, que o `executor.py evidence` calcula.

**A Entrevista só cresce; o Desenho é reescrito no lugar.** A crítica e a resposta vão para a Entrevista; o Desenho
mostra só o que vale, e a alternativa que perdeu sai com uma linha **Descartada** e o porquê.

**O trecho de código no plano é instrução, não fonte.** Fechado o passo, o código em disco é a verdade, e divergência é
um desvio `X`, registrado.

**Passo só executa a pedido explícito de Anderson, passo a passo.** Plano revisado ou aceito não autoriza execução, e
o `executor.py open` só roda depois do pedido daquele passo.

**Quem recomenda não decide.** Nem esta skill, nem o consultor, nem o executor escolhem entre alternativas.

**A narração e o painel saem dos scripts, não da memória.** A linha de chegada, a tabela de abertura e a linha
`::orca-visual` do painel são o que os scripts imprimem, coladas como estão; a hora sai de `date '+%H:%M:%S'`.

**Nada se reabre, reenvia ou fecha às cegas.** `pending`, `unknown`, `closing`, `ended_without_marker` e `bloqueado` se
conferem (`executor.py status`, `brza sessions read <nome> --last`) antes da próxima ação.

**O plano fecha, não se apaga.** A numeração `PLN` é sequencial e não reusada; o fechado fica `done`, o abandonado
`dropped`, com a linha do porquê.
