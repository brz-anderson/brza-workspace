---
status: done
phase: closed
origin: request
ready: sim
estimate_h: 10.5
executed_h: 4.1
remaining_h: 0
scope:
  - workspace
opened: 2026-10-31
completed: 2026-10-31
owner: Anderson
tags:
  - tooling
---

# PLN-005: A confiança dos fatos do desenho se mede contra o que se sustentou

- **Retomar:** fechado em 2026-10-31; o acerto se lê com `python3 scripts/summarize_measurements.py --facts`.

## Pedido

- **Origem:** pedido livre, na sessão do workstream `workspace` de 2026-10-31.

> "encontrar um mecanismo de medir tbm a confiança dos fatos coletados das sugestões de desenho"

### Cobertura

| Origem             | Critério de aceite                                                                                                                               | Passo | Teste (nível)                                                     |
| :----------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- | :---- | :---------------------------------------------------------------- |
| `Pedido 1`, R1.1–2 | Cada fato do `designer` e do `collector`, e cada custo e "se paga" das opções do `designer`, sai com a marca de id, tipo de evidência e confiança | P2 | o parser de marcas sobre uma devolução de fixture (unidade)       |
| `Pedido 1`, R1.3   | Cada marca da devolução vira uma linha no `measurements.jsonl`, com o `agent_id`, o tipo e a confiança                                           | P3 | o hook sobre um transcript de fixture (unidade)                   |
| R1.3, R2.1         | A devolução do `designer` e do `collector` solta a auditoria Haiku em segundo plano, sem segurar o hook                                          | P4, P8 | o disparo com o `claude` trocado por um espião (unidade); uma devolução real gera o veredito (manual) |
| R1.3, R2.2         | A sessão registra o desfecho de um fato "a conferir" ou de um custo pelo `scripts/fact_outcome.py`                                              | P5, P7 | o script grava a linha e recusa id que não existe (unidade)       |
| `Pedido 1`         | O resumo mostra o acerto por faixa de confiança, por papel e por tipo de evidência                                                               | P6 | o resumo sobre um log de fixture (unidade)                        |

### Fora de escopo

- **A marca nos achados do `reviewer`.** Ele já dá a confiança em número (`.claude/agents/reviewer.md:17`); medir o
  acerto dele fica para depois que este mecanismo tiver amostra:
  [A confiança dos achados do reviewer se mede contra o desfecho deles](../../work/issues/a-confianca-do-reviewer-medida-contra-o-desfecho.md).
- **A marca nos agentes do Codex e do `agy`.** Os papéis deles são do
  [PLN-004: O Codex e o `agy` trabalham no fluxo do workspace como o Claude](../PLN-004-o-codex-e-o-agy-no-fluxo/PLN-004-plan.md).

## Entrevista

### Rodada 1 — escopo, marca e desfecho (enviada 2026-10-31)

**Apresentado antes**, na sessão do workstream `workspace`:
- Só o `reviewer` dá confiança em número, de 0 a 100, com corte em 80 (`.claude/agents/reviewer.md:17`). O `designer`
  e o `collector` dão só a fonte; fato sem fonte é "inferência" (`.claude/agents/collector.md:15`) ou "a conferir"
  (`.claude/agent-memory/designer/feedback_medir-antes-de-desenhar.md`). Ninguém confere depois se o fato se
  sustentou.
- O melhor argumento contra a confiança do `reviewer` foi o número dado pelo mesmo modelo que escreve o achado
  (`work/worklogs/2026-10-31-o-porte-das-skills-da-fixfy.md:49`): medir o acerto responde a ele.
- O único fato errado registrado do `designer` foi uma estimativa de custo: o symlink do `hooks.json` saiu "barato" e
  não rodou (`.claude/agent-memory/designer/feedback_custo-de-symlink-com-confianca.md`).
- O evento `subagent` não guarda o conteúdo da devolução (`.claude/hooks/measure.py:434-476`), mas já lê o transcript
  do subagente.
- Volume: 5 rodadas do `designer` (média de US$ 1,79) e 6 do `collector` (US$ 1,71) no log até 2026-10-31; com uns 10
  fatos por rodada, umas 100 amostras em uma ou duas semanas.
- O mecanismo proposto: a marca `F3 · lido · 90` em cada fato; o hook grava um evento por marca; um Haiku refaz a
  evidência; o resumo mostra o acerto por faixa.

Respondida em 2026-10-31.

1. **Escopo**, seleção múltipla. Opções:
   - fatos do `designer` (recomendada) — custo: uma regra no `designer.md` e umas 10 marcas por devolução, quase sem
     token a mais; se paga: com umas 50 amostras, quando se vê se o 90 dele acerta 9 em 10;
   - fatos do `collector` — custo: a mesma regra no `collector.md`, o papel de mais volume; se paga: na mesma fase, mais
     cedo, porque dá mais amostra;
   - custos e "se paga" das opções — custo: a marca em cada opção, com o desfecho só conhecido na fase em que o custo se
     cobra; se paga: tarde, mas é o único erro já registrado.

   **Decidido — as três.**

2. **Marca.** Opções:
   - número e tipo, como `F3 · lido · 90`, na régua do `reviewer` (recomendada) — custo: uma regra no papel e um parser
     simples no hook; se paga: na primeira leitura de calibração, porque o número é o que se compara com o acerto;
   - só o tipo de evidência — custo: menor, e foge do número dado pelo mesmo modelo; se paga: mede o acerto por tipo,
     mas nunca diz se a confiança está calibrada.

   **Decidido — "Número e tipo (Recomendado)".**

3. **Desfecho.** Opções:
   - um Haiku audita e a sessão registra (recomendada) — custo: uns US$ 0,02 por auditoria, estimados pela tabela do
     Haiku 5.5 (~450 mil tokens, quase todos em cache), e um comando novo; se paga: em umas duas semanas, com amostra
     sem viés;
   - só a sessão registra — custo: zero em tokens, e depende de disciplina; se paga: talvez nunca, porque só o fato que
     caiu aparece e o acerto sai inflado;
   - só na revisão do `reviewer` — custo: aproveita a revisão (~US$ 2,27 em Opus), só nos planos revisados; se paga:
     devagar, com uma revisão até hoje.

   **Decidido — "Haiku audita + sessão (Recomendado)".**

### Rodada 2 — disparo, comando e caminho (enviada 2026-10-31)

**Apresentado antes:** o auditor não refaz o comando de um fato `rodado`, porque refazer o comando de outro agente em
segundo plano pode mudar estado; ele confere a saída que ficou no transcript do subagente. O `brza` é do `tools-kit`
(`AGENTS.md`, "Os de agora"), e um `brza fact` seria pedido a outra sessão.

Respondida em 2026-10-31.

1. **Disparo.** Opções:
   - o hook, em segundo plano (recomendada) — o `SubagentStop` do `designer` e do `collector` solta um
     `claude -p --model haiku` só de leitura, sem bloquear; custo: uns US$ 0,02–0,05 por auditoria, porque a sessão
     `-p` carrega a norma (~25 mil tokens), e o cuidado de não auditar a auditoria; se paga: desde a primeira devolução,
     porque toda devolução é auditada sem depender de disciplina;
   - um papel `auditor` acionado pela sessão — custo: uma chamada a mais por devolução, no mesmo custo de tokens, e
     depende de a sessão lembrar; se paga: só se a disciplina se mantiver, porque a devolução esquecida é amostra
     perdida.

   **Decidido — "O hook, em segundo plano (Recomendado)".**

2. **Comando do desfecho.** Opções:
   - um script deste workstream, `scripts/fact_outcome.py`, ao lado do `summarize_measurements.py`, que grava
     `fact_outcome` no `measurements.jsonl` (recomendada) — custo: um script pequeno com testes, nesta frente; se paga:
     agora, sem esperar o `tools-kit`;
   - `brza fact`, no `tools-kit` — custo: pedido a outra sessão, e espera; se paga: quando o `tools-kit` o fizer, e até
     lá o desfecho fica sem registro.

   **Decidido — "Script deste workstream (Recomendado)".**

3. **Caminho.** Opções:
   - PLN novo, pelo `plan-runner` (recomendada) — custo: o arranque do plano, uns 15–20 min; se paga: na segunda sessão,
     ou quando a calibração for lida, daqui a umas duas semanas, e precisar do porquê;
   - worklog direto, nesta sessão — custo: menor agora; se paga: agora, mas sem `Retomar` nem Cobertura para o que
     ficar pendente na auditoria em segundo plano.

   **Decidido — "PLN novo, pelo plan-runner (Recomendado)".**

### Rodada 3 — onde mora o disparo, o que o parser lê e o lembrete (enviada 2026-10-31)

**Apresentado antes:** o `measure.py` promete "Só mede: nunca bloqueia nem escreve fora de .measurements/"
(`.claude/hooks/measure.py:22`); o `collector` grava o agregado no scratch e devolve só o resumo
(`.claude/agents/collector.md:16`); o desfecho de um fato "a conferir" ou de um custo chega dias depois.

Respondida em 2026-10-31.

1. **Onde mora o disparo.** Opções:
   - um `.claude/hooks/fact_audit.py` com entrada própria no `SubagentStop` (recomendada) — custo: um arquivo e uma
     entrada a mais, e o transcript lido duas vezes, em milissegundos; se paga: agora, porque o `measure.py` segue só
     medindo e a falha da auditoria não vira `hook_error` da medição;
   - dentro do `measure.py` — custo: menos código agora, mas quebra a promessa do docstring; se paga: só na economia de
     um arquivo, nunca no isolamento.

   **Decidido — "fact_audit.py separado (Recomendado)".**

2. **O que o parser lê.** Opções:
   - a devolução e os arquivos que o subagente gravou com `Write` (recomendada) — custo: umas 20 linhas a mais no
     parser e uma auditoria maior, talvez US$ 0,05; se paga: na primeira devolução do `collector`, cujos fatos ficam
     quase todos no agregado;
   - só a mensagem final — custo: menor; se paga: no `designer`, com o `collector` de amostra rasa.

   **Decidido — "Devolução + arquivos gravados (Recomendado)".**

3. **O lembrete do desfecho.** Opções:
   - o `close-task` lista os pendentes, pelo `fact_outcome.py --pending` (recomendada) — custo: um passo na skill e uma
     opção no script, uns segundos por fechamento; se paga: no primeiro fechamento em que uma sonda ou rodada respondeu a
     um fato;
   - sem lembrete — custo: zero; se paga: nunca para os custos, cujo desfecho chega em outra sessão.

   **Decidido — "O close-task lista os pendentes (Recomendado)".**

### Rodada 4 — o aceite do Desenho e do corte (enviada 2026-10-31)

**Apresentado antes:** o plano inteiro, na mensagem, com D1–D6, P1–P9 e a Regressão.

Respondida em 2026-10-31.

1. **Aceite.** Opções:
   - aceitar D1–D6 e P1–P9 como estão (recomendada) — custo: 9 h estimadas e uns US$ 0,02–0,05 por devolução
     auditada, a confirmar no P1; se paga: em umas duas semanas, com ~100 fatos medidos, e o commit sai por passo verde;
   - juntar P3–P6 numa entrega só do `implementer` — custo: um passo de 6 h revisado de uma vez, sem commit por parte;
     se paga: agora, em menos ida e volta, mas a falha do P4 segura o P5 e o P6;
   - só o P1 agora, e o corte depois da sonda — custo: uma rodada a mais; se paga: só se a sonda desmentir o D2.

   **Decidido — "1"**: o plano está aceito em 2026-10-31. A execução segue passo a passo, a pedido.

### Rodada 5 — as escolhas do `implementer` no P3 (enviada 2026-10-31)

**Apresentado antes:** a devolução do `implementer` no P3, com quatro escolhas que a especificação não fixou; a quarta
(a última mensagem de texto) caiu no X1.

Respondida em 2026-10-31.

1. **Quando o `unmarked` sai verdadeiro.** Opções:
   - sem marca válida no trecho (recomendada) — custo: nenhum; se paga: agora, com o indicador fiel à devolução, e o
     `malformed` separa quem marcou errado;
   - literal, nenhum `fact` gravado — custo: a retomada que só repete ids conta como "sem marca"; se paga: nunca;
   - a malformada não é "sem marca" — custo: uma regra a mais para o script e o resumo; se paga: só se for preciso
     separar "não marcou" de "marcou errado" além do `malformed`.

   **Decidido — "Sem marca válida no trecho (Recomendado)".**

2. **Sem transcript.** Opções:
   - sair sem gravar (recomendada) — custo: nenhum; se paga: agora, porque o `measure.py subagent` já grava o erro;
   - gravar `fact_capture` com `error` — custo: uma linha e um teste; se paga: só se o `--facts` precisar contar a
     devolução perdida sem cruzar com a linha `subagent`.

   **Decidido — "Sair sem gravar (Recomendado)".**

3. **A malformada repetida.** Opções:
   - por ocorrência (recomendada) — custo: o número pode dobrar quando o `collector` repete o fato no resumo; se paga:
     agora, porque o indicador é alerta, não taxa;
   - deduplicar pelo texto da marca — custo: uma chave e um teste; se paga: só se o resumo usar as malformadas como taxa.

   **Decidido — "Por ocorrência (Recomendado)".**

### Rodada 6 — a citação errada de um fato verdadeiro (enviada 2026-10-31)

**Apresentado antes:** na sonda do P1, o Haiku deu `holds` ao F1, de conteúdo certo e linha errada (`measure.py:22`, o
texto na 23); o prompt da auditoria, que o P4 escreve, precisa dizer o que fazer nesse caso.

Respondida em 2026-10-31.

1. **A citação errada.** Opções:
   - `holds` e um campo `cite: ok|off` (recomendada) — custo: um campo a mais na linha do auditor, no `fact_check` e
     numa coluna do `--facts`; se paga: na primeira leitura do resumo, que separa fato errado de citação errada, e a
     sessão segue a citação para conferir;
   - `holds`, com a nota no `why` — custo: nenhum; se paga: agora, mas a citação errada nunca vira número;
   - `fails` — custo: pune o fato verdadeiro, e a faixa 90+ parece pior do que é; se paga: só se o alvo for a disciplina
     de citação, e não a verdade do fato.

   **Decidido — "holds + campo cite (Recomendado)".**

### Rodada 7 — as escolhas do `implementer` no P4 (enviada 2026-10-31)

**Apresentado antes:** a devolução do `implementer` no P4, com três escolhas que a especificação não fixou.

Respondida em 2026-10-31.

1. **A cerca na resposta do Haiku.** Opções:
   - ignorar a linha de cerca sem contar (recomendada) — custo: 2 linhas e 1 teste ajustado; se paga: no P8, porque sem
     isso o `ignored` de toda resposta cercada nasce poluído;
   - contar a cerca no `ignored` — custo: nenhum agora; se paga: só para medir se o Haiku obedece ao formato.

   **Decidido — "Ignorar a cerca sem contar (Recomendado)".**

2. **O id repetido na resposta.** Opções:
   - a primeira vale, e a repetida vai ao `ignored` (recomendada) — custo: nenhum; se paga: agora, porque dois
     `fact_check` do mesmo fato inflariam o acerto por faixa;
   - a última vale — custo: 3 linhas e 1 teste; se paga: só se o Haiku costumar se corrigir no fim, o que não se mediu.

   **Decidido — "A primeira vale (Recomendado)".**

3. **Os `runs` sem fato `rodado`.** Opções:
   - só com fato `rodado` (recomendada) — custo: nenhum; se paga: agora, no tamanho do arquivo e no que o Haiku lê;
   - sempre — custo: arquivo maior e mais tokens; se paga: só se o `lido` ou o `doc` dependerem de saída gravada.

   **Decidido — "Só com fato 'rodado' (Recomendado)".**

### Rodada 8 — as escolhas do `implementer` no P5 (enviada 2026-10-31)

**Apresentado antes:** a devolução do `implementer` no P5, com quatro escolhas que a especificação não fixou; duas sem
alternativa defensável ficaram fora da rodada — o `fact` duplicado, que o `fact_audit.py` já não grava, e o id exato
que é também prefixo de outro, que não é ambíguo.

Respondida em 2026-10-31.

1. **O `--pending` com o cwd fora de workstream.** Opções:
   - avisar no stderr e filtrar o workstream vazio (recomendada) — custo: um aviso e uma lista quase sempre vazia; se
     paga: agora, sem esconder nada e com a saída 0 que o `close-task` espera;
   - tratar como `all` — custo: lista todos os workstreams sem aviso; se paga: só se o `--pending` rodar fora de
     workstream de propósito.

   **Decidido — "Avisar e filtrar o vazio (Recomendado)".**

2. **O uso fora da especificação.** Opções:
   - recusar com saída 2 (recomendada) — custo: o `--list` não aceita `--workstream`; se paga: agora, porque erro de
     digitação não vira desfecho sem porquê nem filtro ignorado;
   - aceitar e ignorar — custo: desfecho sem porquê e flag perdida sem aviso; se paga: nunca.

   **Decidido — "Recusar com saída 2 (Recomendado)".**

### Rodada 9 — os custos no resumo (enviada 2026-10-31)

**Apresentado antes:** o D4 agrupa por papel, faixa e tipo; os custos (`C…`), quase sempre `inferido`, cairiam na
mesma linha dos fatos inferidos, e o erro que motivou o pedido foi uma estimativa de custo.

Respondida em 2026-10-31.

1. **Os custos no `--facts`.** Opções:
   - uma coluna classe, `fato` ou `custo` (recomendada) — custo: uma coluna e um teste a mais no P6, e o D4 reescrito;
     se paga: na primeira leitura em que um custo tiver desfecho, com o acerto das estimativas à parte;
   - como o D4 estava — custo: nenhum; se paga: nunca para os custos, que somem na média dos inferidos.

   **Decidido — "Coluna classe: fato ou custo (Recomendado)".**

### Rodada 10 — o que a primeira auditoria real mostrou (enviada 2026-10-31)

**Apresentado antes:** um `collector` do workstream `studio` (agente `ab5aa7e0d74df08e7`, 10:05) devolveu 25 fatos
marcados e 10 marcas fora da forma — a premissa dentro da marca, um qualificador no tipo e referências agrupadas no
resumo —, e 7 fatos se perderam; a auditoria dele custou US$ 0,157 por 24 fatos, e com o teto fixo de US$ 0,25 uma
devolução de mais de ~38 fatos seria cortada com o `result` nulo. Do P6, duas escolhas do `implementer`.

Respondida em 2026-10-31.

1. **As marcas fora da forma.** Opções:
   - parser tolerante e regra mais clara (recomendada) — custo: a expressão e uns 6 testes, e 2 linhas nos papéis; se
     paga: agora, recuperando os 7 fatos perdidos e os próximos;
   - só a regra mais clara — custo: 2 linhas; se paga: na próxima devolução, se o modelo obedecer;
   - só o parser tolerante — custo: a expressão e os testes; se paga: agora, mas a forma segue variando.

   **Decidido — "Parser tolerante + regra clara (Recomendado)".**

2. **O teto da auditoria.** Opções:
   - US$ 0,012 por fato, mínimo 0,25 (recomendada) — custo: uma linha e um teste; se paga: na primeira devolução com
     mais de ~38 fatos;
   - fixo em US$ 1 — custo: uma linha, e uma auditoria em laço gasta até US$ 1; se paga: igual;
   - manter US$ 0,25 — custo: nenhum; se paga: nunca para as devoluções grandes.

   **Decidido — "US$ 0,012 por fato, mínimo 0,25 (Recomendado)".**

3. **A dica dos pendentes no `--facts`.** Opções:
   - a dica com `--workstream all`, que bate com a contagem global (recomendada) — custo: uma linha; se paga: agora;
   - contar só o workstream do cwd — custo: o resumo passa a depender do cwd; se paga: só se for lido sempre de dentro
     de um workstream.

   **Decidido — "Dica com --workstream all (Recomendado)".**

4. **O `--facts` com `--by-workstream` ou `--denials`.** Opções:
   - erro de uso, saída 2 (recomendada) — custo: nenhum; se paga: agora;
   - o `--facts` vence — custo: o outro flag some em silêncio; se paga: nunca.

   **Decidido — "Erro de uso, saída 2 (Recomendado)".**

### Rodada 11 — os destinos da revisão (enviada 2026-10-31)

**Apresentado antes:** o parecer do `reviewer` (P9), com dez achados reais e cinco falsos; a sessão refez a evidência
do A1 (22 dos 115 `fact` do log cortados em 300 caracteres, sem a marca), do A2 (o F28 com `holds` e nenhuma das 14
chamadas do auditor ao arquivo citado), do A3 e do A4 (o `CLAUDE.md:125` com 161 colunas e o teto fixo), do A6 e do
A7 (o `--pending` silencioso da `master` e de um terminal sem a `BRZA_WORKSPACE`) e do A10 (a segunda auditoria a
US$ 0,0098 por fato).

Respondida em 2026-10-31.

1. **O texto do fato (A1).** Opções:
   - o parágrafo inteiro da marca ao auditor, e no log os 300 caracteres que terminam nela (recomendada) — custo: umas
     10 linhas e 2 testes, e mais tokens nos fatos longos; se paga: na próxima devolução do `collector`;
   - os 300 que terminam na marca, nos dois — custo: 3 linhas; se paga: agora, mas o fato longo segue cortado;
   - manter — custo: nenhum; se paga: nunca.

   **Decidido — "Parágrafo inteiro ao auditor (Recomendado)".**

2. **O `holds` sem leitura (A2).** Opções:
   - conferir a leitura: o Haiku devolve o `read`, o `run` confere no `stream-json`, e sem casar o veredito vira
     `unknown` (recomendada) — custo: umas 40 linhas e 4 testes; se paga: na próxima leitura do `--facts`;
   - só endurecer o prompt — custo: 2 linhas; se paga: só se o Haiku obedecer;
   - anotar o viés e manter — custo: 1 linha; se paga: nunca para a calibração.

   **Decidido — "Conferir a leitura (Recomendado)".**

3. **O teto (A10).** Opções:
   - US$ 0,02 por fato, mínimo 0,25 (recomendada) — custo: 1 linha, e uma auditoria em laço de 21 fatos gasta até
     US$ 0,42; se paga: na primeira devolução acima de 0,0119 por fato;
   - manter US$ 0,012 — custo: nenhum agora, e a rodada cortada perde tudo; se paga: só se o corte nunca vier.

   **Decidido — "US$ 0,02 por fato, mínimo 0,25 (Recomendado)".** A R10.2 fica substituída.

4. **Os achados menores**, seleção múltipla; o que não fosse marcado iria a issue. Opções:
   - A3 e A4, o `CLAUDE.md` (recomendada) — custo: 2 linhas; se paga: agora;
   - A5, os desvios no Desenho, reescritos com a origem nova e aceitos nesta rodada (recomendada) — custo: uns 10 min;
     se paga: agora;
   - A6 e A7, o aviso no stderr e a raiz pelo `git --git-common-dir` (recomendada) — custo: umas 15 linhas e 4 testes;
     se paga: na primeira vez que o comando rodar do lugar errado;
   - A8 e A9, o teste do timeout e a Regressão (recomendada) — custo: 1 teste e a Regressão reescrita; se paga: no
     primeiro conserto do `run`.

   **Decidido — as quatro.** O X1, o X2 e o X4 ficam aceitos aqui, e o D1 a D3 declaram a origem nova.

### Rodada 12 — as escolhas do `implementer` no P11 (enviada 2026-10-31)

**Apresentado antes:** a devolução do `implementer` no P11 e três auditorias reais novas, entre elas o primeiro
`designer` (`af143be9`), com 27 e 21 marcas malformadas — quase todas o id solto (`[F5].`), que a regra dos papéis
manda usar para citar um fato já marcado; a sessão passou a tratá-lo como referência, pela R10.1.

Respondida em 2026-10-31.

1. **O `:linha` no `read`.** Opções:
   - tolerar (recomendada) — custo: uma expressão; se paga: na primeira auditoria, sem rebaixar `holds` verdadeiro pelo
     formato;
   - exigir o caminho puro — custo: nenhum; se paga: só se o Haiku obedecer.

   **Decidido — "Tolerar o ':linha' (Recomendado)".**

2. **O `Grep` sem `path`.** Opções:
   - não conta como leitura (recomendada) — custo: nenhum; se paga: agora, e o caso aparece no `downgraded`;
   - conta como busca no cwd — custo: 2 linhas e 1 teste, e afrouxa a conferência; se paga: só se o `downgraded`
     mostrar `Grep` legítimo caindo.

   **Decidido — "Não conta (Recomendado)".**

3. **Os rebaixados no `--facts`.** Opções:
   - a coluna agora (recomendada) — custo: umas 15 linhas e um teste; se paga: na próxima leitura do `--facts`;
   - issue para depois — custo: nenhum agora, e o rebaixado fica escondido no `unknown`; se paga: quando a issue for
     feita.

   **Decidido — "Coluna agora (Recomendado)".**

## Desenho

### O que este desenho assume

- **R1.1:** levam a marca os fatos do `designer`, os do `collector` e os custos e "se paga" das opções do `designer`.
- **R1.2:** a marca é número e tipo, na régua do `reviewer`.
- **R6:** o veredito diz se o fato é verdadeiro; o `cite: ok|off`, se a fonte aponta o lugar certo.
- **R1.3:** um Haiku refaz a evidência dos fatos `rodado`, `lido` e `doc`; a sessão registra o desfecho dos `inferido`,
  dos abaixo de 80 e dos custos.
- **R2.1, R3.1:** o disparo é do hook, em segundo plano, num `fact_audit.py` separado do `measure.py`.
- **R2.2, R3.3:** o desfecho da sessão vai pelo `scripts/fact_outcome.py`, e o `close-task` lista os pendentes.
- **R3.2:** o parser lê a mensagem final e os arquivos gravados com `Write` no trecho do subagente.

### Terreno

#### A medição

- **O evento `subagent` não guarda a devolução.** `.claude/hooks/measure.py:434-476` — soma tokens e custo do
  transcript, que acha por `agent_transcript` (`:425-431`), e lê a partir do offset do `.measurements/state.json`.
- **O hook só mede.** `.claude/hooks/measure.py:23` — e engole toda exceção num `hook_error` (`:723-737`).
- **O `SubagentStop` tem uma entrada só**, `measure.py subagent || true`, com `timeout: 30`
  (`.claude/settings.json`, `hooks.SubagentStop`).
- **O resumo** lê o log de `DEFAULT_DIR` (`scripts/summarize_measurements.py:32`), com `--since`, `--json` e
  `--by-workstream` (`:349-360`); os testes ficam em `.claude/hooks/tests/test_summarize_measurements.py`.
- **O preço do Haiku 5.5** é US$ 0,10/M de entrada e US$ 0,01/M de leitura de cache até 100 mil tokens por pedido
  (`.claude/hooks/measure.py:47-56`).

#### O `claude -p`

- **A sessão `-p` da auditoria**, sondada no P1 com o `claude` 2.1.316, no worktree do `workspace`:
  - **O modelo** é o `claude-haiku-5-5` com `--model haiku`.
  - **As ferramentas** são as do `--tools` (`Glob`, `Grep`, `Read`, `WebFetch`) mais as duas do MCP do `context7`, que
    o projeto habilita; todas são de leitura. O `permissionMode` herdado é `auto`.
  - **O custo** de três fatos foi US$ 0,0056, em 4 turnos e 9,6 s — abaixo dos US$ 0,02–0,05 estimados na R1.3.
  - **A saída** `--output-format json` é um objeto com `result`, `total_cost_usd`, `num_turns`, `duration_ms`,
    `is_error`, `subtype` e `modelUsage`.
  - **O `--max-budget-usd`** corta depois do pedido que passa do teto: saída 1, `subtype: error_max_budget_usd`,
    `terminal_reason: budget_exhausted`, `result` nulo e o custo gasto no `total_cost_usd` (US$ 0,0029 num teto de
    US$ 0,001).
  - **Os hooks do projeto rodam** na sessão `-p` e enxergam o `BRZA_FACT_AUDIT=1`; o `Stop` dela gravou um `turn`
    `claude-haiku-5-5` de US$ 0,01 no `workstream` `workspace` — o custo em dobro que o D6 tira do resumo.
- **A primeira auditoria real**, de um `collector` do `studio` em 2026-10-31 (agente `ab5aa7e0d74df08e7`): 24 fatos
  enviados e 24 conferidos em 92 s e 15 turnos, por US$ 0,157 — uns US$ 0,0065 por fato, acima dos US$ 0,02–0,05 por
  auditoria da R1.3 quando a devolução é grande. 21 `holds`, 3 `unknown`, nenhum `fails`; 4 `cite: off`.

#### Os papéis e a skill

- **A régua de confiança** está em `.claude/agents/reviewer.md:17-19`. O `designer` pede a fonte só no levantamento
  (`.claude/agents/designer.md:21-23`); o `collector`, em cada fato (`.claude/agents/collector.md:15`).
- **O `close-task`** tem o passo `## 3. O pendente` (`.claude/skills/close-task/SKILL.md:39-43`).

### D1 — A marca — `.claude/agents/designer.md`, `.claude/agents/collector.md` (P2)

- **Origem:** R1.1, R1.2, R3.2, R10.1; a marca "logo depois do que afirma" é o X4, aceito na R11.4
- **Contexto:** o hook só mede o que acha escrito numa forma fixa; a régua é a do `reviewer`, para que as duas
  confianças se leiam igual.

#### Como fica

No `designer.md`, depois de "A recomendação leva o argumento…"; no `collector.md`, no lugar de "Cada fato vai com a
fonte…", sem a parte dos custos. O texto como está em disco, no `designer.md`:

```markdown
- **Cada fato e cada custo levam a marca** `[F3 · lido · 90]` logo depois do que afirmam, também no rascunho e no
  agregado do scratch:
  - o id: `F` para fato, `C` para o custo e para o "se paga" de cada opção, numerados na devolução e continuados na
    retomada;
  - o tipo de evidência: `rodado`, o comando rodou nesta execução; `lido`, o `arquivo:linha` foi aberto nesta
    execução; `doc`, a URL ou a documentação foi lida nesta execução; `inferido`, sem fonte direta;
  - a confiança, de 0 a 100: 90 ou mais, verificado direto; de 80 a 89, com a premissa escrita na frase do fato,
    fora da marca; abaixo de 80, a conferir. O `inferido` fica abaixo de 80.

  Uma marca por fato, só com o id, o tipo e o número: o resumo que retoma fatos já marcados cita o id sem a marca.

  Um Haiku refaz a evidência dos `rodado`, `lido` e `doc` depois da devolução, e a sessão registra o desfecho dos
  outros quando a sonda ou a rodada responde: o acerto de cada faixa se mede, e a marca fora dessa forma não conta.
```

A régua ficou nos papéis, sem subir ao `AGENTS.md`, que carrega em toda sessão (P2).

### D2 — A captura e a auditoria — `.claude/hooks/fact_audit.py` (P3, P4)

- **Origem:** R1.3, R2.1, R3.1, R3.2, R6, R7, R10.1, R10.2, R11.1–R11.3; a devolução pelo `SubagentHandback` é o X1,
  aceito na R11.4
- **Contexto:** o hook não pode segurar o fim do subagente; a auditoria leva minutos.

#### Como fica

Uma entrada a mais no `SubagentStop`, depois da do `measure.py`:

```json
{"type": "command", "command": "${BRZA_PYTHON:-python3} \"${BRZA_WORKSPACE:-$CLAUDE_PROJECT_DIR}/.claude/hooks/fact_audit.py\" stop || true", "timeout": 10}
```

O script tem dois modos e importa do `measure.py` o `agent_transcript`, o `read_from`, o `write`, o `now` e o
`workstream_of`:

- **`stop`**, no hook:
  1. sai sem nada com `BRZA_FACT_AUDIT` no ambiente (a própria auditoria) ou com `agent_type` fora de `designer` e
     `collector`;
  2. lê o trecho novo do transcript, pelo offset próprio em `.measurements/fact-audit-state.json`;
  3. tira as marcas da devolução — o `input.message` do último `SubagentHandback` do trecho, ou, sem ele, a última
     mensagem com bloco `text` (X1) — e do `content` de cada `Write` do trecho, pela expressão
     `\[([FC])(\d+) · (rodado|lido|doc|inferido)(?: \([^)\]\n]*\))? · (\d{1,3})(?:[;,][^\]\n]*)?\]`, que aceita um
     parêntese depois do tipo e um texto de `;` ou `,` depois do número (R10.1); a referência agrupada,
     `\[[FC]\d+\s*[,\-–]\s*[FC]\d+`, é ignorada; o resto que começa por `[F` ou `[C` e dígito é marca malformada;
  4. grava um evento `fact` por marca — `agent_id`, `agent_type`, `session_id`, `workstream`, `fact_id`, `kind`,
     `confidence`, `text` (a linha da marca, até 300 caracteres), `source` (`reply` ou o caminho do arquivo) — e um
     `fact_capture` por trecho, com o total, as malformadas e se a devolução veio sem marca;
  5. com algum `rodado`, `lido` ou `doc`, grava em `.measurements/fact-audit/<agent_id>-<offset>.json` os fatos, o
     `cwd` do subagente e, para os `rodado`, o comando e a saída de cada `Bash` do trecho (até 4 mil caracteres cada), e
     solta `fact_audit.py run <arquivo>` com `start_new_session=True` e a saída no `/dev/null`. Sai.
- **`run`**, em segundo plano:
  1. roda, no `cwd` do subagente, com `BRZA_FACT_AUDIT=1` e limite de 10 min:
     `claude -p --model haiku --tools Read,Grep,Glob,WebFetch --add-dir <dir do arquivo> --output-format json --max-budget-usd <teto> "<prompt>"`,
     com o teto `max(0.25, 0.012 × fatos)` (R10.2);
  2. o prompt manda refazer a evidência de cada fato — abrir o `arquivo:linha`, a URL, ou ler a saída gravada do
     comando — e devolver uma linha JSON por fato: `{"id": "F3", "verdict": "holds|fails|unknown", "cite": "ok|off", "why": "…"}`
     — `cite: off` quando a fonte não aponta o lugar em que o fato se confere, mesmo verdadeiro (R6);
  3. grava um `fact_check` por veredito, com o `cite`, e um `fact_audit` por rodada, com o custo e a duração do JSON de saída, o número
     de fatos e o erro, quando houver. A falha nunca levanta: vira `fact_audit` com `error`.

### D3 — O desfecho da sessão — `scripts/fact_outcome.py` (P5)

- **Origem:** R1.3, R2.2, R3.3, R8, R11.4; o `workstream` do fato é o X2, aceito na R11.4

#### Como fica

```bash
python3 scripts/fact_outcome.py <agent_id>:F3 fails "a sonda do R8.1 não rodou o hook" --ref PLN-004/R8.1
python3 scripts/fact_outcome.py --pending [--workstream <nome>] [--since AAAA-MM-DD]
python3 scripts/fact_outcome.py --list <agent_id>
```

- **Registrar:** aceita o prefixo único do `agent_id`; recusa, com saída 2, o fato que não está no log; grava
  `fact_outcome` com o `verdict` (`holds` ou `fails`), o porquê, a `ref` e o `workstream` do fato (X2). Registrar de
  novo vale: o último desfecho conta.
- **`--pending`:** os `fact` `inferido`, abaixo de 80 ou `C`, sem `fact_outcome`, do workstream do cwd por padrão, com
  o id, a data, a confiança e o texto.
- **`--list`:** todos os fatos da devolução, com o veredito do Haiku e o da sessão.

### D4 — O acerto por faixa — `scripts/summarize_measurements.py --facts` (P6)

- **Origem:** Pedido 1, R1.2, R6, R9

#### Como fica

Uma tabela por papel, classe (`fato` para `F…`, `custo` para `C…`), faixa (90+, 80–89, <80) e tipo: fatos, com desfecho, `holds` em %, a confiança média, a
distância entre as duas e o `cite: off` em % (R6). O desfecho da sessão vence o do Haiku; `unknown` conta à parte e fica fora do acerto. Abaixo,
as devoluções sem marca, as marcas malformadas, o custo somado das auditorias e os pendentes, com a dica
`fact_outcome.py --pending --workstream all` (R10.3). Com `--json`, o mesmo em JSON. Com `--by-workstream` ou
`--denials`, erro de uso (R10.4).

### D5 — O lembrete — `.claude/skills/close-task/SKILL.md` (P7)

- **Origem:** R3.3

#### Como fica

No `## 3. O pendente`, um item a mais:

```markdown
- **Os fatos a conferir:** `python3 scripts/fact_outcome.py --pending` lista os fatos `inferido`, abaixo de 80 e os
  custos do workstream sem desfecho. O que a sonda, a rodada ou a execução da tarefa respondeu vai ao
  `fact_outcome.py` com a `--ref`; o resto fica.
```

### D6 — A norma e a sessão da auditoria — `CLAUDE.md`, `.claude/hooks/measure.py` (P4, P7)

- **Origem:** R2.1
- **Contexto:** a sessão `-p` da auditoria roda no workspace e o `Stop` dela vira uma linha `turn`, que somaria o custo
  da auditoria duas vezes.

#### Como fica

- O `measure.py` marca `"fact_audit": true` no `turn` com `BRZA_FACT_AUDIT` no ambiente, e o resumo deixa essa linha
  fora do custo da sessão principal.
- A tabela do hook de medição, no `CLAUDE.md`, ganha as linhas `fact`, `fact_capture`, `fact_check`, `fact_audit` e
  `fact_outcome`, e a seção diz que o `fact_audit.py` é o único hook que solta processo.

## Passos

### P1 — A sonda do `claude -p`

Executa D2 · executor: a sessão que conduz

Estimado: 0.5 h · Executado: 0.2 h

- [x] **1.** No scratch, rodar a linha do D2 com um fato `lido` de fixture e conferir: o modelo é o Haiku 5.5, o JSON
  traz o custo e o resultado, só as ferramentas dadas existem, o `--max-budget-usd` corta, e o `Stop` do projeto roda
  e enxerga `BRZA_FACT_AUDIT`.
- [x] **2.** O que divergir do D2 volta à Entrevista antes do P3. Nada desmente o D2: o MCP do `context7` entra junto,
  só de leitura, e a saída 1 do teto é a falha que o D2 já manda gravar como `fact_audit` com `error`.

**Evidência:** fixture com três fatos em `/private/tmp/pln005-p1/facts.json` (`F1 lido` verdadeiro, `F2 lido` falso,
`F3 rodado` com a saída gravada). `BRZA_FACT_AUDIT=1 claude -p --model haiku --tools Read,Grep,Glob,WebFetch --add-dir
… --settings <espião do Stop> --output-format stream-json --verbose --max-budget-usd 0.25` → `success`, US$ 0,0056,
`F1 holds`, `F2 fails` ("o timeout é 30, não 60"), `F3 holds` sem rodar o comando; espião: `audit=1`. O mesmo com
`--max-budget-usd 0.001` → saída 1, `error_max_budget_usd`. O `F1` voltou `holds` com a nota "na linha 23 e não na
22": a citação `measure.py:22` deste plano estava errada, e o Terreno foi corrigido.

### P2 — A marca nos papéis

Executa D1 · executor: a sessão que conduz, pela `agent-instructions-writer`, na `master`

Estimado: 0.5 h · Executado: 0.2 h

- [x] **1.** A régua fica nos dois papéis, e não sobe ao `AGENTS.md`: só pesa quando eles rodam, e o `AGENTS.md` paga
  em toda sessão. Nenhuma outra linha da norma cita a marca (`git grep` por `inferência`, `a conferir` e `[F`).
- [x] **2.** A marca vai "logo depois do que afirma", e não "no fim da linha" do D1, porque o custo e o "se paga" de uma
  opção dividem a linha `Custo: … Se paga: …`; no `collector`, a regra substitui "Fato sem fonte é inferência".

**Evidência:** `master@68a925c` — `.claude/agents/designer.md:19-29` e `.claude/agents/collector.md:15-24`; a expressão
do D2 casa o exemplo `[F3 · lido · 90]` dos dois arquivos, e a maior linha tem 118 colunas; `brza note sync` →
`studio`, `tools-kit` e `workspace` mesclados e enviados.

### P3 — A captura

Executa D2 (`stop`, sem soltar o processo) · executor: `implementer`, com os testes em
`.claude/hooks/tests/test_fact_audit.py`

Estimado: 2 h · Executado: 0.4 h

- [x] **1. Teste que falha:** um transcript de fixture com marcas na devolução e num `Write` gera os `fact` e o
  `fact_capture`; um papel fora da lista e o ambiente com `BRZA_FACT_AUDIT` não geram nada; a marca malformada conta.
- [x] **2. Implementar.** Com o X1, e as escolhas da R5.
- [x] **3. Rodar** — `python3 -m unittest discover .claude/hooks/tests`.

**Evidência:** `master@8d22660` — `.claude/hooks/fact_audit.py` (158 linhas; o `measure.py` intocado) e
`.claude/hooks/tests/test_fact_audit.py` (24 testes). Antes do código, os 18 primeiros falharam com `FileNotFoundError`;
`python3 -m unittest discover -s .claude/hooks/tests` → `Ran 97 tests … OK`. Sobre o transcript real
`agent-a4e396c649819d3fd.jsonl`, do `designer`, anterior ao P2: `fact_capture` com `facts: 0`, `unmarked: true`,
`segment: first`, saída 0.

### P4 — A auditoria em segundo plano

Executa D2 (o arquivo, o disparo e o `run`) e D6 (o `turn` marcado) · executor: `implementer`

Estimado: 2 h · Executado: 0.6 h

- [x] **1. Teste que falha:** com o `claude` trocado por um espião no `PATH`, o `stop` volta antes do espião terminar,
  e o `run` grava um `fact_check` por linha do espião e o `fact_audit` com o custo; com o espião falhando, só o
  `fact_audit` com `error`.
- [x] **2. Implementar**, com a entrada no `.claude/settings.json`, o `cite` da R6 e as escolhas da R7.
- [x] **3. Rodar** — `python3 -m unittest discover .claude/hooks/tests`.

**Evidência:** `master@3e123f0` — `.claude/hooks/fact_audit.py` (`stop` solta o `run`; `run` com o `PROMPT` do
auditor), `.claude/hooks/measure.py` (`fact_audit: true` no `turn`), `scripts/summarize_measurements.py` (o `turn` de
auditoria fora dos agregados) e a segunda entrada do `SubagentStop` no `.claude/settings.json`. Antes do código, 6
falhas e 16 erros em 119; `python3 -m unittest discover -s .claude/hooks/tests` → `Ran 119 tests … OK`. O `stop` volta
em menos de 1 s com o espião dormindo 2 s. Na primeira rodada dos testes, o `Popen` dos testes antigos ainda não
estava trocado e pode ter chamado o `claude` real: nenhum transcript com o prompt do auditor nem `turn` em Haiku além
do P1 apareceu, e nenhum processo ficou vivo.

### P5 — O desfecho da sessão

Executa D3 · executor: `implementer`, com os testes em `.claude/hooks/tests/test_fact_outcome.py`

Estimado: 1 h · Executado: 0.4 h

- [x] **1.** Testes antes (os 28 falharam com o script ausente), o script, e as escolhas da R8.

**Evidência:** `master@98a60d3` — `scripts/fact_outcome.py` e `.claude/hooks/tests/test_fact_outcome.py` (28 testes);
`python3 -m unittest discover -s .claude/hooks/tests` → `Ran 147 tests … OK`; contra o log real,
`fact_outcome.py --pending --workstream all` → "nenhum fato a conferir", saída 0; num log temporário com `F1 lido 95`,
`F2 inferido 70` e `C1 inferido 60`, o `--pending` lista F2 e C1, `abc:F2 fails … --ref PLN-004/R8.1` grava com o
`workstream` do fato, o `--pending` fica só com C1, e o `--list` mostra `Haiku holds (cite off)` e
`sessão fails (PLN-004/R8.1)`.

### P6 — O acerto por faixa

Executa D4 · executor: `implementer`, nos testes de `test_summarize_measurements.py`

Estimado: 1 h · Executado: 0.4 h

- [x] **1.** Testes antes (22 de 34 com erro, `aggregate_facts` ausente), o `--facts`, a classe da R9 e a dica da
  R10.3, aplicada pela sessão.

**Evidência:** `master@72f684a` — `scripts/summarize_measurements.py` e `test_summarize_measurements.py` (25 testes
novos); `python3 -m unittest discover -s .claude/hooks/tests` → `Ran 172 tests … OK`; contra o log real,
`summarize_measurements.py --facts` → saída 0, com a linha `collector fato 90+ lido`: 31 fatos, 17 com desfecho,
`holds` 100%, confiança média 92,8, distância -7,2, `cite off` 11,8%.

### P7 — O lembrete e a norma

Executa D5 e D6 (o `CLAUDE.md`) · executor: a sessão que conduz, pela `agent-instructions-writer`, na `master`

Estimado: 0.5 h · Executado: 0.3 h

- [x] **1.** O `close-task` ganhou "Os fatos a conferir" no `## 3. O pendente`; o `CLAUDE.md`, a seção "A auditoria da
  confiança dos fatos", com os cinco eventos, e o `--facts` no "Resumo"; o `README.md`, os três comandos. O `AGENTS.md`
  ficou de fora: a mecânica é do runtime, e a marca mora nos papéis.

**Evidência:** `master@4c92097` — `CLAUDE.md`, `README.md` e `.claude/skills/close-task/SKILL.md`; nenhuma linha nova
de prosa passa de 120 colunas; `brza note sync` → os três workstreams mesclados.

### P8 — A prova numa devolução real

Executa D1–D4 · executor: a sessão que conduz

Estimado: 0.5 h · Executado: 0.2 h

- [x] **1.** Uma devolução do `designer` com marcas gera os `fact`, e em até 10 min os `fact_check` e o `fact_audit`;
  o `--facts` mostra a linha dela. Provado com um `collector` (X3).

**Evidência:** a devolução do `collector` `ab5aa7e0d74df08e7`, da sessão `46242dd1` do `studio`, às 10:05:07 →
`fact_capture` com 25 fatos e 10 malformadas (10:05:08); `fact_audit` às 10:06:40 com 24 enviados, 24 conferidos, 0
ignorados, US$ 0,157, 92,3 s, `success`; nenhum arquivo sobrou em `.measurements/fact-audit/`; o `--facts` mostra a
linha do `collector`. As malformadas abriram a R10 e o P10.

### P10 — A marca tolerante e o teto por fato

Executa D2 (R10.1, R10.2) e D1 (a regra) · executor: `implementer` (o parser e o teto) e a sessão (os papéis)

Estimado: 0.5 h · Executado: 0.3 h

- [x] **1.** Os papéis: a premissa vai na frase do fato, fora da marca, e o resumo cita só o id — `master@b3e3efd`.
- [x] **2.** O parser aceita `; …` depois do número e um parêntese depois do tipo, e ignora a referência agrupada;
  o teto é `max(0.25, 0.012 × fatos)`; testes com as 10 marcas do `collector` real.

**Evidência:** `master@13a291a` — `.claude/hooks/fact_audit.py` e `test_fact_audit.py` (4 testes novos; antes, 5 falhas e 1
erro); `python3 -m unittest discover -s .claude/hooks/tests` → `Ran 176 tests … OK`; `marks_of(sources_of(…))` sobre o
transcript real do `collector` `ab5aa7e0d74df08e7` → F1–F28, 0 malformadas (eram 10); `budget_usd(3)` → `0.25`,
`budget_usd(50)` → `0.60`. Os dois pontos do `implementer` têm lastro na R10.1: `F7-9` não é "outro id" e segue
malformada; duas marcas num colchete não apareceram nas 46 reais.

### P9 — A revisão

Executa D1–D6 · executor: `reviewer`, com o parecer em `work/reviews/pln-005-a-confianca-dos-fatos.md`

Estimado: 1 h · Executado: 0.3 h

- [x] **1.** O parecer, com dez achados reais e cinco falsos; a sessão refez a evidência dos que pesavam, e a R11 deu
  o destino de cada um: todos `corrigido aqui`.

**Evidência:** [REV: PLN-005 — a confiança dos fatos do desenho](../../work/reviews/pln-005-a-confianca-dos-fatos.md).

### P11 — As correções da revisão

Executa D2, D3 e D6 (A1, A2, A6, A7, A8, A10) · executor: `implementer` (o código) e a sessão (A3, A4, A5, A9)

Estimado: 1 h · Executado: 0.8 h

- [x] **1.** A5: o D1 com o texto em disco, as origens do D1 ao D3 e o X4; A9: a Regressão reescrita.
- [x] **2.** A3 e A4: o `CLAUDE.md` com o teto por fato, a leitura conferida e a linha de 161 colunas quebrada.
- [x] **3.** A1, A2, A6, A7, A8 e A10, pelo `implementer`, com testes; e o id solto (`[F5]`) como referência, pela
  sessão.
- [x] **4.** A coluna `rebaixados` do `--facts` (R12.3), pelo `implementer` — `master@cfa058e`,
  `Ran 213 tests … OK`; no log real, 0 rebaixados, porque as 5 auditorias são anteriores ao `read_ok`.

**Evidência:** `master@2c9a546` — `python3 -m unittest discover -s .claude/hooks/tests` → `Ran 208 tests … OK` (eram
176). A1: no transcript do `collector` `ab5aa7e0d74df08e7`, as 28 marcas têm o `text` terminando na marca (eram 24
cortadas), e o maior `context` tem 2.000 caracteres. A2: o `run` lê o `stream-json` e rebaixa a `unknown` o veredito sem
leitura casada. A8: numa cópia, trocar o `killpg` por `process.kill()` ou tirar o `start_new_session` faz o teste novo
levar 25 s e falhar; o original passa em 2 s. A10: `budget_usd(21)` → `0.42`. A6: da raiz da `master`, o `--pending`
escreve "lendo …/measurements.jsonl; workstream master" e o aviso. A7: do worktree, sem a `BRZA_WORKSPACE`, o script
lê o log da `master` e lista 67 pendentes. O id solto: no transcript do `designer` `af143be9be6175443`, 80 marcas e 0
malformadas; sem o ramo novo da `REFERENCE`, o teste `test_a_bare_id_cites_a_marked_fact_and_is_not_malformed` falha.
O `implementer` fez uma chamada real ao `claude` (Haiku, US$ 0,002) para ver a forma do `stream-json`.

## Regressão

- **O `measure.py` segue só medindo, e o `stop` não segura o fim do subagente.** Como se confere: os testes de
  `.claude/hooks/tests/test_measure.py`; o teste do `stop` que volta em menos de 1 s com o espião dormindo; e, nas
  devoluções reais, o `fact_capture` no mesmo segundo, ou no seguinte, da linha `subagent` do mesmo agente. O
  `duration_s` não serve: é a duração do subagente, tirada do transcript (A9).
- **O resumo sem `--facts` não muda.** Como se confere: `test_summarize_measurements.py`.

## Desvios

- **X1 — A devolução mora no `SubagentHandback`.** A especificação dizia "a última mensagem de texto", sem conferir:
  nos 40 transcripts de subagente mais recentes, 4 de 4 devoluções do `designer` e 4 de 5 do `collector` chegam como
  `tool_use` `SubagentHandback`, com o texto em `input.message`. O parser lê o handback e cai no `text` sem ele. Afeta
  P3 e D2; aceito na R11.4 (A5).
- **X2 — O desfecho leva o `workstream` do fato, e não o do cwd.** O desfecho chega em outra sessão, às vezes em outro
  worktree; com o do cwd, o `--pending` do workstream dono nunca o veria. Afeta D3 e P5; aceito na R11.4 (A5).
- **X3 — A prova do P8 veio de um `collector`, e não de um `designer`.** O primeiro subagente marcado depois do P4 foi
  um `collector` de outra sessão; o caminho do `designer` só difere no filtro do `agent_type` e nas marcas `C`, que os
  testes do P3 e do P6 cobrem. Afeta P8.
- **X4 — A marca vai "logo depois do que afirma", e não "no fim da linha".** O custo e o "se paga" de uma opção
  dividem a linha `Custo: … Se paga: …`, e cada um leva a sua marca. Afeta D1 e P2; aceito na R11.4 (A5). É o que
  levou ao A1: a marca no meio de linha longa ficava além dos 300 caracteres.

## Revisões

- [REV: PLN-005 — a confiança dos fatos do desenho](../../work/reviews/pln-005-a-confianca-dos-fatos.md) — 2026-10-31,
  dez achados e cinco falsos, todos com destino (R11).

## Pendências conhecidas

- [A confiança dos achados do reviewer se mede contra o desfecho deles](../../work/issues/a-confianca-do-reviewer-medida-contra-o-desfecho.md)
  — do `### Fora de escopo`; espera amostra no `--facts`.

## Documentação

- `.claude/agents/designer.md` e `.claude/agents/collector.md` — a marca de confiança, em P2 e P10 (`68a925c`,
  `b3e3efd`).
- `CLAUDE.md`, "A auditoria da confiança dos fatos" e o "Resumo" do hook de medição — em P7 e P11 (`4c92097`,
  `2c9a546`).
- `README.md`, os comandos do `--facts` e do `fact_outcome.py` — em P7 (`4c92097`).
- `.claude/skills/close-task/SKILL.md`, "Os fatos a conferir" — em P7 (`4c92097`).

## Worklogs

- 2026-10-31 — aberto, conduzido e fechado: R1–R12; D1–D6; P1–P11; X1–X4; a revisão com dez achados, todos
  corrigidos no P11.
  [PLN-005: a abertura da confiança dos fatos do desenho](../../work/worklogs/2026-10-31-pln-005-a-abertura-da-confianca-dos-fatos.md)

## Fechamento

- [x] Todo passo `[x]` com evidência: P1–P11.
- [x] Todo achado com destino que existe: A1–A10 corrigidos no P11; A11–A15 `→ falso` no parecer.
- [x] Sem resumo a publicar: a entrega são commits diretos na `master` do `brza-workspace`, sem pull request.
- [x] O durável saiu para a casa dona e está em `## Documentação`: a marca nos papéis, a auditoria no `CLAUDE.md`, os
      comandos no `README.md` e o lembrete no `close-task`. Nenhuma rodada decidiu algo além do plano que peça nota em
      `work/decisions/`.
- [x] Nenhuma decisão de `work/decisions/` foi respondida pelo plano.
- [x] `status: done`, `phase: closed` e `completed` no frontmatter.
