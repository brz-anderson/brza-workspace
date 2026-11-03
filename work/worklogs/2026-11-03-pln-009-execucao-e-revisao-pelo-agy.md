---
scope:
  - workspace
refs:
  - PLN-003
  - PLN-009
  - issue:o-mcp-propoe-a-conta-do-pedido
  - issue:os-passos-do-mcp-no-pln-003-passam-ao-pln-009
  - issue:testes-do-brza-workflow-falham-dentro-do-chat-do-app
---

# O PLN-009: a execução do P1 a P6 e a revisão pelo `agy`, com a medição Flash × Opus

A pedido de Anderson, em 2026-11-03: "`Retomar PLN-009` execute todos os passos que não dependem de decisões minhas, se
encontrar problemas e desvios, crie `issues` e registre nos `worklogs`". No meio da sessão vieram três regras: "para cada
passo executado, acione um `reviewer` utilizando o `agy`, o passo só será considerado `pronto` ao final da revisão, com
os achados encaminhados conforme manda a norma, escolha o encaminhamento dos achados sempre pela opção `recomendada`";
"prefira sempre optar por `corrigir aqui`, na devolução dos achados, já encaminhe os de código a um agente
`implementer`, que ao final, chama outro `reviewer`, assim por diante, até 3 rodadas"; e "compare os achado do `Gemini
Flash 3.8` e do `Opus 5.5`, registre como medição".

O plano é o [PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../../plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md).

## O que se fez

- **R1:** o código do MCP mora no `brza-workflow`, em `packages/mcp/` ("brza-workflow (Recomendado)"), e o PLN-009 é o
  dono do trabalho do MCP ("PLN-009 (Recomendado)"). O pedido ao PLN-003 está na issue
  [Os passos do MCP no PLN-003 passam ao PLN-009](../issues/os-passos-do-mcp-no-pln-003-passam-ao-pln-009.md).
- **A revisão do Desenho antes da execução:** um `reviewer` (Opus) deu 14 achados,
  [REV: o Desenho do PLN-009 antes da execução](../reviews/pln-009-o-desenho-antes-da-execucao.md). A R2 os encaminhou
  pela regra de Anderson, e o plano foi reescrito: um D6 novo (o ciclo e a conta), o P5 e o P6, os achados do P0 do
  PLN-003 no Desenho, a forma do molde. Estimativa de 22,5 h para 30 h.
- **Os passos, no `brza-workflow`** (worktree `.worktrees/pln-009-mcp`, branch `feat/pln-009-mcp`, sem push), cada um
  por um `implementer`:

| Passo | Commit | `tests/mcp` |
| :---- | :----- | :---------- |
| P1 — o servidor e o `launchd` | `1dfc9d9`, correção `f8829f4` | 48 |
| P2 — a fila e os tetos | `084cc62` | 85 |
| P3 — as ferramentas e os gates | `e7d8fa6` | 120 |
| P4 — a política e o desempatador | `8801c77` | 150 |
| P5 — o ciclo e a conta | `a4ff8db` | 177 |
| P6 — a linha `route` | `1fa3e60` | 205 |

  O merge `944fa27` juntou o P2 a P5 às correções do P1; o P6 avançou a branch até o `1fa3e60`. O `tests/cli` num
  ambiente limpo deu 445 OK, e o `tests/hooks`, 290 OK.
- **O laço de revisão:** o `agy -p` em `--mode plan`, com o corpo do `.claude/agents/reviewer.md` e um pedido por passo
  (o script e os pareceres ficam no scratch). A rodada 1 do P1 foi pelo Gemini 4 Argon, com 6 achados, todos corrigidos
  no `f8829f4`. Depois a cota do `agy` acabou: o Argon volta em ~164 h e o Opus em ~5 h. A R3 respondeu "Flash agora,
  Opus depois (Recomendado)".

## A medição Flash × Opus

O Gemini 3.8 Flash (pelo `agy`) e o Opus 5.5 (pelo subagente `reviewer`) revisaram os mesmos commits do P2 a P5, com o
mesmo prompt, palavra por palavra (R4.1, "Opus pelo reviewer, agora"). Um `collector` casou os achados e abriu o código
de cada achado exclusivo. O P1 ficou de fora porque o worktree recebeu o merge durante a revisão do Flash. Cada revisão
virou uma linha `event: "review"` no `.measurements/measurements.jsonl` (R4.2, "Log e worklog (Recomendado)").

| | Flash | Opus |
| :-- | --: | --: |
| Achados reais | 17 | 50 |
| — importantes | 12 | 26 |
| — sugestões | 5 | 24 |
| Em comum com o outro | 6 | 6 |
| Parciais | 4 | 4 |
| Exclusivos | 9 | 40 |
| — que se sustentam no código | 7 | 40 |
| Falsos (hipóteses que caíram) | 12 | 17 |
| Tempo por passo | 13 a 18 min | 10 a 13 min |
| Tokens por passo | não informa | 128 a 175 mil |

- **O Opus achou o triplo**, e todo achado exclusivo dele se sustentou. Dos 9 exclusivos do Flash, 2 não se sustentam,
  ambos no P5: um `IndexError` com `task` vazia, que o `dispatch` já recusa, e um pedido `None`, sem caminho de produção.
- **O Flash pegou 6 dos 26 importantes do Opus.** Na correção de gate e de concorrência, os dois acharam a corrida do
  `approve` do P3.
- **Nenhum conflito de fato.** Na leitura dos desvios propostos, os dois divergem por julgamento, sem hipótese contraditória.
- **A leitura para a política:** o Flash como único revisor perde a maior parte dos achados; como triagem rápida antes
  do Opus, acerta o que acha. O `AGENTS.md` manda revisar na camada alta "até a medição dizer que média basta", e esta
  medição diz que a rápida não basta.
- **A ressalva:** um runtime é o `agy` e o outro, o Claude Code; o prompt é o mesmo, mas o ambiente das ferramentas não.

A tabela por passo, com o casamento achado a achado, ficou no scratch da sessão (`medicao-flash-opus.md`). Os números
estão nas linhas `review` do log.

## Problemas e desvios

- **Os testes do `tests/cli` falham no chat:** 20 falhas, que passam no ambiente limpo; emenda na issue
  [Os testes do brza-workflow falham quando rodam dentro do chat do BrzA Studio](../issues/testes-do-brza-workflow-falham-dentro-do-chat-do-app.md).
- **A cota do `agy` acabou** no meio do laço (X6 e R3 do plano). O `--mode plan` sem `--add-dir` não lê fora do
  worktree, e no `-p` o pedido de permissão fica sem resposta; a rodada 2 do P1 se perdeu assim.
- **Issue nova:** [O MCP propõe a conta do pedido](../issues/o-mcp-propoe-a-conta-do-pedido.md), de R4.3.
- **Os desvios X1 a X31** estão no plano.

## A rodada de correção

Um `implementer` aplicou, na `feat/pln-009-mcp`, as 53 correções do P2 a P5, as 2 do P1 e a do P6, mais os
encaminhamentos da R4: `brza-workflow@77b917f`. Para cada item, escreveu antes o teste e o viu falhar (74 testes), ou
provou por mutante o teste que guarda sem falhar antes. O gate ficou verde: `tests/mcp` 286, `tests/hooks` 290,
`tests/cli` limpo 445, e o `brza-mcp` e o `brza-quota` sobem no 3.9 do sistema.

No fim, ele mesmo chamou a próxima rodada do Flash em cada passo. A do P2 achou que a reserva de vaga só segurava o
escolhido e não os seguintes; corrigido, a rodada 3 aprovou. A do P4 pediu reforçar um caso da fixture do M11, que não
barrava o teto inclusivo; corrigido. As outras aprovaram sem achado novo. Os desvios dessa rodada são o X32 a X39 do
plano.

Ficaram de fora: a fixture do `orca account list` segue com o formato, e não com uma captura real; o
`ORCA_CLI_COMMAND` no header do client; e "o MCP propõe a conta", que é issue.

- **Um tropeço do `implementer`:** ele usou `git stash push -- packages` no `brza-workflow` para medir o "falhou antes".
  A pilha do `stash` é compartilhada com as outras sessões; conferida depois, estava vazia. Ele também gravou a memória
  no scratch do chat, e não no worktree; a sessão a moveu para `.claude/agent-memory/`.

## A rodada final e o `[x]`

Anderson avisou que o Opus semanal do `agy` estava em 93%, com reset em 3 dias. A R5 escolheu "reviewer Opus, por passo
(Recomendado)": seis subagentes `reviewer`, um por passo, sobre o `77b917f`. Eles deram, ao todo, 31 achados
`corrigido aqui`, 4 pontos para rodada e 3 achados que iam a issue. A R6 os encaminhou pela regra: as opções
recomendadas, e as issues corrigidas na branch integrada. O mais grave era o Haiku do desempate, que não autenticava sem
o `USER` no env, e por isso todo desempate caía no `fallback`; o revisor o provou com duas chamadas reais ao `claude -p`
(~US$ 0,005), o que reabriu um achado que a rodada 1 tinha derrubado só pela leitura.

Com isso, o P2 a P6 completaram as 3 rodadas do teto, e o P1, quatro. A última correção (`brza-workflow@b2c87a6`) não
teve revisão própria; a prova é o gate, com cada teste visto falhando antes: `tests/mcp` 346, `tests/hooks` 290 e
`tests/cli` limpo 445, todos OK. Os seis passos ganharam o `[x]`, e o plano foi a `phase: review`. O parecer
consolidado é [REV: os passos P1 a P6 do PLN-009, revisados pelo agy e pelo Opus](../reviews/pln-009-a-revisao-dos-passos.md).

- **A cota de 5 h do Claude:** Anderson pediu para parar a 90% e voltar às 8h. A vigia lê o `orca account list --json`,
  que o app só renova de tempos em tempos (a leitura das 06:30 era das 06:05, em 58%): ela não vê o uso em tempo real.

## Retomar

A revisão da entrega contra o `## Pedido` e a Cobertura, por um revisor que não executou; os casos C1 a C4, com
Anderson; e o merge da `feat/pln-009-mcp` na `master` do `brza-workflow`, com a confirmação dele.

## Fora do workspace

- **O quê e onde:** os worktrees `~/Projects/brza-workflow/.worktrees/pln-009-mcp` e `pln-009-p2` a `p6`, com as
  branches locais `feat/pln-009-*`; só a `feat/pln-009-mcp` foi ao `origin` (ver o item seguinte). **Risco:** nenhum; a `master` do `brza-workflow` não foi tocada.
  **Estado:** ativos. **Como desfazer:** `git -C ~/Projects/brza-workflow worktree remove .worktrees/<nome>` e
  `git branch -D feat/<nome>`.
- **O quê e onde:** `git push -u origin feat/pln-009-mcp` (`b2c87a6`), a pedido de Anderson, para
  `brz-anderson/brza-workflow`. **Risco:** nenhum; branch nova, a `master` não foi tocada. **Estado:** publicada.
  **Como desfazer:** `git push origin --delete feat/pln-009-mcp`.
- **O quê e onde:** a cota individual do `agy`, gasta nas revisões: o Gemini 4 Argon e o Claude Opus esgotaram.
  **Risco:** o `agy` fica sem esses modelos até o reset, também para outro trabalho. **Estado:** o Argon volta em ~164 h
  e o Opus em ~5 h, a partir de ~03:50. **Como desfazer:** não se desfaz; espera o reset.
- **O quê e onde:** duas chamadas reais ao `claude -p --model haiku` pelo revisor da rodada final do P4, para provar o
  achado do `USER`. **Risco:** custo, ~US$ 0,005. **Estado:** encerradas. **Como desfazer:** não se desfaz.
- **O quê e onde:** as sondas do `implementer` do P4 ao `tev1:4b` do Ollama local (`/v1/systemone`, `keep_alive` de
  1 min). **Risco:** nenhum. **Estado:** o modelo se descarrega sozinho. **Como desfazer:** já desfeito.
