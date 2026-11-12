---
name: skill-with-scripts-review
description: Onde erram as skills do playground que trazem scripts com contrato JSON entre si (meeting-runner, 2026-11-08 e 11-09), e quais hipóteses de revisão costumam cair
metadata:
  type: project
---

Na revisão da `meeting-runner` (tally → estado-rN.json → panel; wait_round sobre o `brza orchestration`), o erro real
morou em cinco lugares, todos achados por comando e não por leitura:

- **Dois scripts calculam o mesmo número, ou leem o mesmo arquivo, de jeitos diferentes.** O tally e o painel davam
  médias da sala diferentes a partir do mesmo JSON. O molde do `sintese-N.json` aninhava `sala.revisor`, e um dos
  leitores só lia o nível de cima. Rode os dois sobre o mesmo insumo e compare a saída.
- **O molde muda, e quem o consome não acompanha.** O pedido passou de "prazo" a "duração", e o painel seguiu lendo
  `(prazo: …)`. Os testes passaram porque a fixture ainda era do molde velho. Alimente cada parser com o molde
  **atual** da reference.
- **O comando do SKILL.md com caminho relativo e `--root` = cwd.** De um dos diretórios plausíveis, o comando quebra; de
  outro, responde "todos falta" com rc 0. Rode cada comando como está escrito, da raiz, da pasta do artefato e do
  diretório da skill.
- **Parâmetro opcional que muda o significado do número.** Sem `--opened/--closed`, o "custo da rodada" virava o da
  sessão inteira, e o painel nem tinha a flag. Procure flag opcional que tira a janela ou o filtro.
- **A leitura tolerante de um formato não sondado falha em silêncio.** A atribuição por nome em qualquer string pegou
  a persona errada (nomes que são palavras comuns). A chave de dedupe incluía um id de lote. A caixa vazia sem Run
  ligado dava `ok`. A `--help` do CLI instalado (`brza orchestration <verbo> --help`) é a fonte barata, e muitas vezes
  já contradiz o script: `worker-release` só vale para worker settled; `--terminal` pede `--worktree`; `worker_done`
  sem `--to`.

**Na 3ª revisão (transporte v2 do `brza sessions`, 2026-11-09), o erro voltou nos mesmos lugares, com três formas novas:**

- **A mesma flag de subconjunto com regra de casamento diferente em cada script.** `--send`/`--personas` aceitavam
  slug sem caixa; `--participantes` só o nome exato, e o slug deixava todos "fora da rodada" com rc 0 e "0 de 0". Rode
  cada flag de subconjunto com o slug em minúsculas e com um nome que não existe.
- **Vazio declarado × ausente.** O molde permitia "nenhum novo"; o parser dava `[]`, e o `not` tratava como ausente
  (aviso falso). Procure `not x` onde o molde tem uma resposta "vazia" legítima.
- **Histórico sem data devolvido inteiro.** O `wait` do v2 devolve todos os eventos do Run, sem `createdAt`; a dedupe
  por processo repete a pergunta da R1 em toda rodada seguinte. Confira se o evento traz hora e se a dedupe sobrevive
  à próxima invocação.
- **Abreviação que colide com rótulo novo:** o painel abreviava apoio/ressalva/contra como A/R/C, e o molde novo passou
  a aceitar propostas A/B ("voto A 0" de quem votou A). Leia o PNG, não só o HTML.

**Na 4ª revisão (painel automático, R10, 2026-11-09), o padrão voltou no subcomando irmão.** O `publish` ganhou o
padrão `$ORCA_CHAT_SCRATCH_DIR`; o `sintese`, escrito junto, não ganhou, e o comando da skill imprimia um caminho com
rc 0 no lugar da linha `::orca-visual`. Quando dois subcomandos nascem juntos, rode os dois com o env do chat, e não só
com as flags. Outras duas formas novas:
- **Epoch convertido em HH:MM:SS** perde a data que outro script reconstrói por um campo do manifesto (`data`).
- **O docstring do `--once` diverge do ramo "todas chegaram"**, que ninguém lê.

Mutantes que sobrevivem: flag repassada a outro script (`participantes`) e o relógio do teste, que não avança entre
dois momentos que o código distingue (`closed` = última chegada × agora).

Mutação barata para medir os testes: copie `scripts/`, troque uma linha por `sed`/Python e conte as falhas contra a
linha de base da cópia (a cópia já perde 2 testes de raiz git). Na 3ª revisão, as dez mutações caíram.

**Na reverificação, a correção abre um buraco vizinho.** Isso aconteceu três vezes na mesma rodada:
- A dedupe persistida marcava como visto o evento de quem estava fora do subconjunto, que nunca era narrado.
- O "ignorar o que está em crase" deixou passar o número escrito entre crases.
- O "liberada vence falhou" escondeu o worker `failed` que o host libera sozinho.

Em cada correção, pergunte o que ela passa a dar como tratado sem ter tratado, e rode o caso de borda que a exclusão
nova cria.

**Nos testes:** procure `except Exception: skipTest` e teste cujo invariante outra linha do código já garante (o teste
de dedupe passava sem a dedupe). O aceite "contra o gabarito" costuma conferir só as colunas fáceis; confira se a
medição (latência, custo) entra.

**Hipóteses que caíram (não gastar confiança alta):** XSS no HTML gerado (escapava tudo), `shell=True`, o teto de
512 KB, `:root` no tema, laço infinito, a mensagem de rodada antiga contando na nova (havia o `m < n`), a corrida
entre a escrita parcial e o marcador na última linha. Na 3ª: "o teste integrado não roda o v2 real" (roda, por
`SourceFileLoader`); "`reclaimable` deixa o veredito ativo" (é `terminalState`, não `stage`); "o `--operation` muda
o texto" (o v2 anexa o mesmo protocolo); laço quente no limite (sai com 2). Na 4ª caíram: "o painel muda o rc ou trava a espera" (o `except Exception` cobre,
nada chama `sys.exit`, e o `subprocess.run` com timeout, no POSIX, só espera o processo), "o corte do anexo aceita
texto a mais" (os 9 casos saíram certos) e "chave do JSON sem documentação" (o docstring lista todas). Deram 85–90 de partida e caíram por
leitura direta do código do CLI e do studio.

**Na 5ª revisão (P8 do PLN-021, plan-runner v2 e screen-artboards, 2026-11-10), o erro morou de novo no contrato com o
`brza` real. Os testes passam porque o `brza` é falso e a fixture inventa a forma:**

- **A forma do JSON:** o `brza quota --json` é `accounts[].windows[]`, e o script lia `{runtime: {session_pct}}`.
- **A combinação de flags:** o `--effort` exige o `--model`.
- **A conferência barata:** o `brza sessions <nome> … --dry-run` valida as flags sem abrir nada, e o `wait` num nome que
  não existe sai rc 1 com `error`. Rode os dois antes de ler o código.
- **O ramo de erro que não dorme:** o `if error and rc not in (0, 1, 75)` deixa o rc 1 girar o laço a ~0,3 s por
  chamada. Procure o rc que o filtro "tolera" e veja se o ramo de espera cobre esse caso.
- **O estado que sobrevive à reabertura:** o worklog com o marcador velho fazia o `wait` devolver na hora. Toda vez que
  um verbo "reabre", confira o arquivo que o detector lê.
- **O verbo que muda estado antes da validação:** o `brza tree` rodava antes da recusa do pedido.
- **A conferência que executa:** o comando do worklog rodava já na proposta.

No plano, a resposta da rodada nova (R5 respondendo a R4) não chegou aos `D`, e a `Origem` não a cita. O gerador de
pedido copiava o "Em aberto" velho ao executor. Teste: rode o `step_request` do passo e leia o que sai. A Evidência do
`[x]` era anterior ao retrabalho que estava no diff. Teste: compare o mtime do código com o do plano e conte os testes de
HEAD contra os do disco.

Caíram de novo, deram 95 de partida: as contagens de teste da Evidência (bateram), os testes novos que não discriminariam
(5 falharam no código de HEAD) e o `:root` vazado no artboard publicado. Rodar a mutação é o que derruba ou confirma.

**Na 6ª revisão (P11.1 do PLN-021, a reverificação do REV-026, 2026-11-10), a correção cobriu um verbo e deixou o
vizinho com o mesmo defeito.** O padrão "a correção abre um buraco vizinho" voltou, em quatro formas:

- **O estado velho:** o `open` passou a apagar o marcador velho, e o `send` a um passo `feito` não apagou. O `wait`
  seguinte voltou na hora. Para cada verbo que retoma o executor (`open`, `send`), rode o `wait` logo depois.
- **O ramo do `brza` que o falso nunca devolve:** o `sessions` falso sempre "abre", e o `running:` (rc 0, sem mandar o
  prompt) passou sem teste. Leia o CLI real (`brza-workflow/packages/client/bin/brza-sessions`) atrás dos ramos de rc 0
  que não fazem o que o nome diz.
- **A igualdade de caminho no lugar de mesmo repositório:** o `realpath(checkout) != realpath(raiz)` deixou passar o
  checkout da `master` e as subpastas. Rode com três caminhos do mesmo repositório.
- **O argv sem shell:** trocar `shell=True` por argv quebra glob, `~`, `VAR=` e `cd &&`, e vira "NÃO confere" falso. O
  filtro não barra `bash -c`.

O `--marker` do `brza` faz `re.search` no arquivo inteiro, e o molde do worklog cita o marcador na prosa. Confira se a
conferência do CLI pode casar com o texto do molde.

Caíram de novo, com 90–97 de partida: o laço que gira (agora dorme e para no 5º), os testes que não discriminam
(`PR_SCRIPTS`/`SKILLKIT` contra o HEAD no scratch: 25 falhas e 3 erros), a cota e o filtro recusando o comando simples.
A contraproposta "Lida como contraproposta" também ficou fora, como devia. O `PR_SCRIPTS` e o `SKILLKIT` dos `_paths.py`
são o atalho barato para rodar a suíte nova contra o HEAD.

**Na rodada 2 do P11.1, o parser de comando caseiro errou nos detalhes do shell que ele imita.** O
`shlex(posix=False)` com `#` como comentário cortava `echo a#b` em `echo a`, e a conferência dava "confere" a outro
comando. O `~` era expandido nas palavras, mas não no `cd ~/… &&`. A mensagem de recusa mandava um verbo (`executor.py
close`) que só funciona com a entrada do manifesto. Quando alguém imita o shell, rode `#`, `~` em cada posição, aspas
com espaço e `cd`. Quando a mensagem de erro manda rodar um comando, rode esse comando no mesmo estado.

**Na rodada 3, o estado novo herdou o buraco antigo.** O `cobre:` parcial deixou o passo em `evidencia-gravada` com
subpasso `[ ]`. O `open` recusa esse estado, o `send` não o reabre, e o `wait` devolve o `feito` velho. Toda vez que um
recurso cria um estado parcial, siga o ciclo inteiro dali: `open`, `send`, `wait`, `close` e de novo `open`. Não ponha
na sonda um comando que grava fora do scratch: o `npm` rodado como amostra deixou um log em `~/.npm/_logs`.

**Na 7ª revisão (P13 do PLN-021, 2026-11-12), o teste confirmou a conta com uma sequência de eventos que o código
nunca grava.** O teste do X12 montou `aberto → feito(hora do worklog)`, mas o `wait` grava o `feito` na hora em que vê
o marcador; com o manifesto real do P12 a janela dava 0.01 h, e não os 0.005 h do aceite. Teste: passe o `events`
real do `.sessions/<plano>/execucao.json` pela função (90, confirmado por replay). Outras duas formas:
- **O teste chama o helper, e não o verbo.** Apagar a atribuição no `cmd_open` deixou os 205 testes verdes (95).
- **A continuação de linha só para na linha em branco.** O leitor juntou `Estimado:`, lista, cerca e `**Evidência:**`
  colados; o `_parse_d` vizinho já parava em `^[-*#]`. Rode cinco entradas coladas contra o HEAD (95).

Na rodada 2 do P13, as cinco correções fecharam, e o buraco ficou no vizinho, de novo:
- **O fato novo do desvio torna alcançável um defeito antigo.** O X12 provou que o executor fecha o passo dentro do
  `--wait` do `open`. Mas o `open` neutraliza o "último marcador" depois do `--wait`, e na reabertura apagava o `feito`
  novo. Quando um desvio muda a premissa de tempo, rode o verbo vizinho sob a premissa nova (95, por teste-sonda no
  scratch herdando a classe de teste dele).
- **A mesma correção em dois sítios, e o teste cobre um só.**
- **A regex de parada sem o espaço do marcador de lista** (`[-*+]` no lugar de `[-*+]\s`) corta a continuação que abre
  com `**negrito**`.

O conjunto de mutações num script só (`mutate.py`: cópia, `replace`, `PR_SCRIPTS`) mede a rodada inteira em segundos.

Caíram, de 80–85 de partida: a regressão nos planos reais (o leitor do HEAD e o do disco sobre os `plans/` de todos os
workstreams, por `git archive` de cada branch: 0 pioras, 16 melhoras), o `open` de reabertura antiga e o fuso.

**Why:** a skill nasce de protótipos de scratch, e cada script é endurecido em separado; o contrato entre eles e os
moldes das references é o que ninguém roda junto.
**How to apply:** em toda revisão de skill com `scripts/`, rode os comandos do SKILL.md como estão escritos, passe o
molde atual de cada reference pelo parser e compare os dois consumidores do mesmo JSON, antes de ler o mérito.

Ver também [[meeting-plan-review-patterns]].
