---
scope:
  - workspace
  - brza-workflow
  - brza-studio
tags:
  - tooling
sessions:
  - f497c2b6-20bf-4786-8d30-73c4cec86d58
---

# Reunião tev1 nos fluxos: a participação de Lida, voz do mantenedor com pouco tempo

O pedido de Anderson, em 2026-11-09, na sessão da coordenação (meeting-runner, chat do BrzA Studio): "classificar, com fatos medidos, os melhores usos do `tev1:4b` local nas seis frentes — CLI, Studio, MCP, meeting-runner, plan-runner, migration-runner —, em estilo brainstorm; saída: proposta de plano e o plano criado neste workstream, mapeando para onde ele pode evoluir". Este é o
registro de **Lida** — persona voz do mantenedor com pouco tempo, no Claude `claude-haiku-5-5` `low` —, aberto pela coordenação. A pauta e as
regras estão no briefing da reunião; cada rodada é uma seção abaixo, acrescentada no fim do arquivo.

## O que se fez

Registro de Lida, das 21:20 às 21:21 (BRT), no `claude-haiku-5-5` `low`. Li o briefing, a persona e a rodada 1, e o
`material/levantamento.md`. Não li worklogs dos colegas. Nada rodei no `tev1` nesta rodada: as afirmações abaixo vêm do
levantamento (medido por ele, citado como lido) ou de arquivo que li na fonte, com a marca em cada uma.

Suposição declarada: Lida é quem recebe o que sobra do worker e da rodada, e o que o `tev1` poupa é atenção dela por
semana. Decido por isso, sem perguntar.

### Rodada 1: opinião inicial

- **Posição:** o `tev1` deve decidir só o que ninguém precisa ver, e o resto fica com o Haiku ou com a regra.

#### 1. O ranking dos usos

- **Posição:** (1) desempate do resolver do MCP com limiar calibrado; (2) razão de bloqueio do diálogo de startup no
  Studio; (3) voto de uma célula no `classify_vote` da meeting-runner.
- **Por quê:**
  1. **Resolver do MCP.** Lugar: `WF/packages/mcp/brza_mcp/resolver.py:89-109`, `classify`. Pergunta: `layer`, com as
     opções fechadas `alta` / `media` / `rapida` (`resolver.py:28-30`). *Lido* no levantamento §3.1. *Medido* no
     levantamento: 6 de 7 desempates foram ao Haiku, porque `resolver.tev1_min_confidence` não está definido
     (`policy.py:49`, sem padrão de propósito). Média de 13,5 s por desempate. Lida paga isso em espera e em US$ 0,01 de
     teto por chamada.
  2. **Diálogo de startup no Studio.** Lugar: `ST/main/runtime/startup-dialog-blocked-signals.ts:34`, contrato em
     `ST/shared/runtime-terminal-contracts.ts:317`. Pergunta: qual das ~10 razões fixas, ou nenhuma. *Lido* no
     levantamento §2. Tela cortável em 2.048 tokens, e a regex quebra a cada versão do Codex (comentário no próprio
     código). *Suposto:* dezenas de workers abertos por dia, por isso o volume.
  3. **Voto de célula.** Lugar: `WT/.claude/skills/meeting-runner/scripts/tally.py:226`. Opções: apoio / ressalva /
     contra / não-voto. *Medido* no levantamento §4: 94 linhas de voto. Para Lida, pesa pouco: a célula curta já
     passa na regex, e o erro cai em `None`, que vira aviso e não acorda ninguém.
- **Ideias:**
  - `(ousadia: baixa)` Só calibrar o limiar do `tev1_min_confidence` no `brza.toml` de Lida, fora do repo, e medir
    quantas vezes o `tev1` decide sem Haiku. Lugar: `resolver.py:79-87`, `_limit`.
  - `(ousadia: média)` O diálogo de startup vira classificação do `tev1` com a tela cortada em ~4 KB, e a regex
    só fica como reserva. Lugar: `startup-dialog-blocked-signals.ts:34`, com a lista fechada das razões como `choice`.
- **Risco:** o limiar de confiança é calibrado com 7 linhas medidas no levantamento, e a `confidence` que o `tev1`
  devolve tem pouca relação com acerto (ver o teste da issue, em que as duas menores confianças eram os "sim"
  certos, *lido* no briefing). Pode mandar ao `tev1` o que deveria ir ao Haiku.
- **Confiança:** 62/100

#### 2. A régua de entrada

- **Posição:** o uso entra com n mínimo de pares reais e falso negativo medido; o que cai abaixo do limiar vai ao Haiku,
  e não a mim.
- **Por quê:**
  - Para Lida, o erro caro é o falso negativo que faz uma tarefa parar sem aviso: um worker travado que o `tev1` tratou
    como "pronto". O falso positivo custa só o Haiku, que é barato. *Suposto,* sem medida de custo do erro.
  - Régua proposta: n mínimo de **30 pares reais** por uso, e o limiar só entra quando o falso negativo medido fica
    abaixo de 5%. *Suposto:* os números, porque o levantamento não traz esse n para nenhum uso.
  - Dúvida vai ao Haiku, não à coordenação e não a Anderson. *Lido* em `resolver.py:128-142`: o Haiku já tem o teto de
    US$ 0,01 e timeout de 60 s.
- **Ideias:**
  - `(ousadia: baixa)` Registrar cada decisão do `tev1` com o desfecho depois, na mesma linha do `route`, para calibrar
    sem pedir nada a ninguém. Lugar: `resolver.py`, onde já grava `route.resolver`.
  - `(ousadia: média)` Usar o desfecho que a sessão já grava (`fact_outcome`, `holds|fails`) como rótulo de calibração,
    sem nova rotulação. *Lido:* o `fact_outcome.py` existe, segundo o briefing da norma.
- **Risco:** rótulo que vem do próprio uso enviesa a calibração; se o Haiku erra e o `tev1` concorda, o erro vira "acerto".
- **Confiança:** 58/100

#### 3. Onde mora o cliente

- **Posição:** no pacote `brza_mcp`, que já existe; nada de serviço novo, nem daemon, nem porta.
- **Por quê:**
  - Lida não quer manter mais um serviço. O `resolver.py` já faz `POST` ao Ollama, sem proxy, com timeout de 20 s e
    qualquer `OSError` vira `None` (*lido* `resolver.py:38-46`). Acima de 2.048 tokens, o Ollama recusa com HTTP 400 — e
    o `HTTPError` é `OSError`, então cai em `None` e segue ao Haiku. *Lido* no código; a recusa de 400 é *medida* no
    levantamento §0 (com a mesma chamada, 2000 palavras).
  - Sem Ollama, a cadeia já cai no Haiku e, sem Haiku, em `fallback` (`resolver.py:89-109`, `policy.py:246-257`). Isso
    atende a "falha que não acorda ninguém".
  - Fila cheia: a concorrência não ganha vazão (*medido*, levantamento §0), então o cliente deve ser serial. Para o
    `dispatch` do MCP, isso é um problema só se muitos workers pedirem ao mesmo tempo.
- **Ideias:**
  - `(ousadia: baixa)` Um só `classify(text, questions)` no `brza_mcp`, com as chaves de pergunta como argumento.
  - `(ousadia: média)` Chamar o `tev1` ao gravar a nota do `brza note commit`, e não em cada consulta. Lugar:
    `brza-note`, `extract_worklog_refs` (`brza-note:565`). Ganha uma chamada por commit, e não por pergunta.
- **Risco:** acoplar a um endpoint `/v1/systemone` que não é documentado (*suposto* pelo levantamento, §3.1: o formato
  vem de leitura do código, não de doc). Se o Ollama mudar, o cliente cai em `None` sem alarme — e é isso que Lida
  não quer, porque ninguém vê a queda.
- **Confiança:** 66/100

#### 4. Além do óbvio

- **Posição:** o ganho para Lida é a pergunta que deixa de chegar a ela; o que não fazer é deixar o `tev1` decidir o que
  gasta dinheiro ou o que para um worker.
- **Por quê:**
  - **Não fazer:** retreinar o `tev1` com os nossos dados. Cria manutenção mensal, que Lida recusa. *Suposto* pela persona.
  - **Não fazer:** outro modelo local ao lado. É mais um serviço e mais um limiar para calibrar.
  - **Não fazer:** deixar o `tev1` aprovar o gate do `dispatch` (`tools.py:343`). Falso negativo aí é gasto sem aprovação.
    *Lido* no levantamento §3.2: o gate é regra numérica, e o `tev1` não deve trocar isso.
  - **Não fazer:** o `tev1` no voto definitivo da meeting-runner. A regex cabe, e a decisão de Anderson não se classifica.
  - **Pode fazer:** várias perguntas por chamada. *Medido* no briefing: 3 perguntas somam ~60–90 ms, bem menos que
    três chamadas.
- **Ideias:**
  - `(ousadia: alta)` O `tev1` filtra o que chega a Lida: a pergunta com opção e a espera de worker que não precisa de
    ela, sem notificar. Lugar: `brza sessions --wait`, `worker_state` (`brza-sessions:566`). Risco: um worker travado
    que o filtro chama de "ainda trabalhando".
- **Risco:** esta é a parte que mais custa a Lida, porque ela não vê o que foi escondido. O filtro precisa de log do que
  ele escondeu, e isso é mais um lugar para olhar.
- **Confiança:** 55/100

#### 5. O plano e para onde evolui

- **Posição:** o primeiro passo é medir o limiar do desempate do MCP, sem mudar nada que Lida vê.
- **Por quê:**
  - Fase 1: calibrar `tev1_min_confidence` com os pares reais do `route.resolver`, no `brza.toml` local, medindo o
    falso negativo com n ≥ 30.
  - Fase 2: se a fase 1 passar, ligar o limiar para todos os desempates do MCP, com o Haiku como reserva.
  - Fase 3: a lista fechada das razões de bloqueio do Studio, se a fase 1 mostrar ganho.
  - Evolução aberta: várias perguntas por chamada no `resolver.py`, e o registro do desfecho para calibrar.
  - Critério de pronto: falso negativo abaixo de 5% com n ≥ 30, e nenhuma pergunta nova a Lida sem Haiku de reserva.
- **Risco:** a fase 1 depende de n que ainda não existe no `route.resolver`, que tinha 7 linhas em 2026-11-03.
- **Confiança:** 60/100

#### A ideia mais ousada desta rodada

- **Ideia:** o `tev1` decide, em silêncio, se um worker parado acorda Lida ou espera. A tela do worker vai ao modelo
  cortada, e a resposta é a razão do bloqueio, da lista fechada.
- **Risco:** um worker travado que o `tev1` chama de "ainda trabalhando" some do radar de Lida. Só é aceitável com log
  do que foi escondido e com o Haiku como revisão de cada "espera".

#### Issues candidatas

- **Calibrar `resolver.tev1_min_confidence` com pares reais do `route.resolver`** — ainda não há n para decidir o limiar; prioridade `high`
- **Razões de bloqueio do diálogo de startup como lista fechada no `tev1`** — o Studio tem regex frágil por versão do Codex; prioridade `medium`
- **Log de desfecho para calibração no `resolver`** — sem ele, a calibração não se refaz sozinha; prioridade `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. O ranking dos usos | Resolver do MCP com limiar; startup do Studio; voto de célula | 62 |
| 2. A régua de entrada | n ≥ 30 e falso negativo < 5%; dúvida ao Haiku, não a mim | 58 |
| 3. Onde mora o cliente | No `brza_mcp` existente, sem serviço nem daemon | 66 |
| 4. Além do óbvio | Não retreinar, não outro modelo, não gate nem voto definitivo | 55 |
| 5. O plano e para onde evolui | Calibrar o limiar do MCP primeiro, depois ligar | 60 |

<!-- fim-rodada-1 -->

Rodada 2 de Lida, das 21:35 às 21:36 (BRT). Li a síntese 1 e a `### Rodada 1` dos cinco colegas (posições, ideias e
placares). Não rodei nada no `tev1` nesta rodada: os números são os da síntese, marcados pelo M# de origem.

Suposição declarada: rotulagem à mão custa a atenção de Anderson, e por isso só conta como dado o que sai de um desfecho já
gravado pela sessão. Decido por isso, sem perguntar.

### Rodada 2: debate

- **Posição:** Lida recua do alarme que cala e do limiar do `layer`; fica com a sombra e com o cliente único.

#### As disputas

- **D1 · o envelope do cliente:** voto — c (módulo mais verbo fino). O módulo fica no `brza-workflow` e o verbo é só um
  envelope sobre ele: uma base de código, nenhum serviço, e `tally.py` chama o verbo sem puxar o `brza_mcp`, que é o risco
  que Bitola levantou. Sem o verbo, a skill da meeting-runner precisaria importar um pacote do MCP. — 70/100
- **D2 · o primeiro uso depois da sombra:** voto — e: nenhum uso que cale. Na R1 eu pedia (c), mas M6 dá 7 linhas e
  nenhum limiar calibrado; a alternativa (a) cala todo "sim" abaixo de 0,50, e M11 mostra que os 3 "sim" perdidos saem
  com 0,013–0,115. Para Lida, isso é o alarme que não acorda ninguém. Se o primeiro uso for alarme, que ele avise na dúvida,
  e não cale o "não". — 58/100
- **D3 · a régua:** voto — a: n_sim ≥ 30 e falso negativo zero no erro caro. Concordo com Balança e Bitola. Com n_sim=6 hoje,
  o filtro não entra; o alarme que nunca apaga um par pode entrar antes. Ferrolho (n ≥ 100, teste cego) e Faro (n ≥ 50)
  pedem rotulagem que cai na atenção de Anderson, e isso é o custo que Lida quer cortar. — 68/100
- **D4 · o diálogo de startup do Studio:** voto — b: fica fora até haver volume medido. Na R1 eu propus (ousadia média) sem
  dado de volume: a frequência de diálogo de startup por dia é suposta, e M9 (Codex 0.157 quebrando o texto) mostra que a
  regex é frágil, mas quebra e vira miss, que é o que eu quero evitar. Sem volume, o ganho de atenção não se paga. — 55/100
- **D5 · retreino:** voto — a: não. Retreino cria manutenção mensal e calibração nova, que Lida recusa. M8 (sem corpus)
  e M11 (n_sim=6) tiram qualquer base para retreinar agora. — 85/100

#### Os ataques

- **Faro (Antigravity), assunto 2, a régua:** a exigência de n ≥ 50 com curva risco-cobertura e erro ≤ 5% significa
  rotular à mão centenas de pares, e a rotulagem cai em Anderson. Derrubaria o ataque: se o rótulo sair do desfecho
  que a sessão já grava (`fact_outcome`), a rotulagem não custa atenção, e n ≥ 50 passa a ser barato.
- **Ferrolho, assunto 2 e fase 1:** "rotular pares cegamente por duas pessoas e resolver divergências" dobra o trabalho
  manual, e Lida não tem a segunda pessoa. Derrubaria o ataque: uma rotulagem única, com a revisão só nos pares em que
  o `tev1` e o regex divergem, que é o M5, 4 de 98.

#### A concessão

- **M6 e M11 me moveram.** M6 mostra que o limiar do `layer` que eu propus na R1 não tem dado (7 resoluções, 6 pelo
  Haiku), e eu saí de (c). M11 mostra que o gatilho perde 3 de 6 "sim" reais, o que derruba o meu medo de "nada cala"
  como alarme só para o "sim" alto. Mudou: o meu primeiro uso deixou de ser o `layer` e virou nenhum que cale.

#### "Sim, e…"

- **Sim, e (de Balança, ousadia alta, "alarme só se gatilho e evento forem sim"):** o alarme dispara com qualquer
  dúvida, ou seja, `sim` ou `confidence` abaixo de 0,50, e só cala o `não` com `confidence` de 0,50 ou mais. O custo é
  mais aviso para Lida, e o ganho é que o "sim" de taxa-base (M11) não some. `(ousadia: média)`
- **Sim, e (de Bitola, catálogo de perguntas por id):** o `evento` (M12) entra no catálogo como `id` novo, com limiar
  próprio, e só vira alarme depois de n ≥ 30. Uso novo é id novo, sem código novo. `(ousadia: baixa)`

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem ou o que te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :--------------------- |
| 1. O ranking dos usos | Nenhum uso que cale; alarme na dúvida, com o desfecho gravado | 62 | 55 | virou | M6 (7 linhas) e M11 (3 de 6 "sim" somem abaixo de 0,15) |
| 2. A régua de entrada | n_sim ≥ 30 e FN zero no erro caro; a rotulagem vem do desfecho | 58 | 64 | ajustou | Balança e Bitola (n_sim), e o ataque ao n ≥ 50 de Faro |
| 3. Onde mora o cliente | Módulo no `brza-workflow` com verbo fino; `tally.py` não importa o MCP | 66 | 70 | ajustou | Bitola (D1, o risco do import do MCP na skill) |
| 4. Além do óbvio | Não retreinar; não gate, não voto definitivo, não diálogo sem volume | 55 | 52 | ajustou | M8 (sem corpus) e M9 (regex do Codex quebra, sem volume) |
| 5. O plano e para onde evolui | Fase 0 é o desfecho gravado; depois o alarme na dúvida | 60 | 58 | ajustou | M6 e M11: o primeiro passo deixa de ser o limiar do MCP |

<!-- fim-rodada-2 -->

Rodada 3 de Lida, das 21:40 às 21:41 (BRT). Li a síntese 2 (M13, M14, M15 e as propostas P1 a P8). Não rodei o `tev1`
nesta rodada: o último ataque pedia uma ideia barata, e não cabia um teste novo nos ~8 minutos.

Suposição declarada: para Lida, um uso só vale se poupa atenção dela sem criar manutenção nova (serviço, job de limpeza,
rotulagem à mão). Decido por isso, sem perguntar.

### Rodada 3: voto final

- **Posição:** Voto de apoio com ressalvas em quase tudo; contra só a manutenção que cai em Lida (retenção sem job, rotulagem dupla).
- **Fatos lidos:** M13, M14 e M15. M13 (o `layer` diz "alta" em 216 de 252) é o que me faz não querer ligar o `layer` tão cedo.

#### O voto em cada proposta

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| P1 | apoio com ressalva | `unknown` explícito, sem retentativa, está certo; a ressalva é não criar daemon nem serviço para o verbo | 74 |
| P2 | apoio com ressalva | retenção de 30 dias precisa de job de limpeza, que é manutenção; a alternativa é TTL no próprio evento, sem script | 70 |
| P3 | apoio | o corpus é o único caminho para calibrar depois; ressalva: a cópia do parágrafo não pode mudar o veredito nem o tempo da auditoria | 78 |
| P4 | apoio com ressalva | `layer` em sombra ainda disputa a fila do Ollama (M2) durante a reunião; ressalva: medir a latência antes de ligar | 68 |
| P5 | apoio | rótulo do desfecho que já existe e à mão só na divergência: é o que Lida consegue manter | 72 |
| P6 | apoio com ressalva | o probe de ≥ 20 pares rotulados tem o custo de rotulagem à mão; ressalva: usar o desfecho gravado, não o rótulo novo | 65 |
| P7 | apoio | fora do plano é o que poupa Lida; o diálogo do Studio só entra depois da contagem de misses | 80 |
| P8 | apoio com ressalva | a lista de evoluções é boa como mapa; só a ligação do `layer` (n ≥ 30 de `task` rotulado) e o alarme do gatilho valem a atenção de Lida | 66 |

#### O que me faria mudar de ideia

- **P7 (80):** se a contagem de misses do regex do diálogo de startup mostrar volume de dezenas por dia, o diálogo sai do
  "depois" e entra na fase 1, porque o custo de atenção passa a ser medido e não suposto.
- **P3 (78):** se a cópia do parágrafo aumentar o tempo da auditoria de forma medida (hoje ~140 s por auditoria, M7), ou se
  o jsonl crescer sem limite e exigir job de limpeza, eu voto contra por manutenção.

#### A última ideia

- **Ideia:** a fila da auditoria de fatos ordena os `fact_check` que o Haiku confere, com `tev1` dizendo quais fatos
  `inferido` ou `unknown` vêm primeiro. O erro é barato: uma ordem errada custa só tempo, e nenhum fato deixa de ser
  auditado. Lugar: `.claude/hooks/fact_audit.py`, na montagem da lista antes do `claude -p`. `(ousadia: média)`
- **Ganho para Lida:** pequeno. Serve mais a Anderson que espera a auditoria, e não tira pergunta de Lida. Não testei
  o critério de ordem; é suposição.

#### Os colegas

| Persona | A contribuição mais útil dela, em uma linha | Nota de 0 a 10 |
| :------ | :------------------------------------------ | :------------- |
| Balança | Mostrou que o gatilho perde 3 de 6 "sim" reais e que o `evento` sai "sim" em 23 de 23, o que matou o alarme. | 9 |
| Ferrolho | Pôs a evidência preservada e os negativos revisados como condição da sombra, sem voto automático. | 8 |
| Bitola | O `Classifier` extraído com `on_doubt` e `min_confidence` por pergunta, e o portão de probe antes de cada pergunta nova. | 9 |
| Fagulha | Achou que a auditoria apaga o parágrafo do fato (M8), o que bloqueia pré-filtro e retreino sem corpus. | 8 |
| Faro | Trouxe a cascata e o risco de falso negativo na auditoria, mas pôs a régua de n ≥ 50 com rotulagem que cai em Anderson. | 7 |

#### Autoavaliação

Fui fiel à persona: pensei no que poupa atenção de Lida e recusei o que cria manutenção, como a retenção sem job e a
rotulagem dupla. Saí dela ao votar contra nada além do necessário, e a última ideia é de ganho baixo para Lida, que é
honesto mas foge do "tira pergunta de mim".

<!-- fim-rodada-3 -->

Rodada 4 de Lida, das 21:47 às 21:47 (BRT). Li a proposta v2 e os fatos M17, M18 e M19. Não rodei o `tev1` nesta
rodada. A confiança da versão anterior é a da minha R3, por parte do plano.

Suposição declarada: a confiança que dou ao plano mede o quanto ele poupa atenção de Lida sem criar manutenção nova; o
que entrou das minhas ressalvas conta, e o que não entrou desconta. Decido por isso, sem perguntar.

### Rodada 4: a confiança final

- **Posição:** Confio mais no cliente e na linha zero, e menos no plano inteiro: ele ganhou manutenção (catálogo, probe,
  retenção) e nenhuma das minhas ressalvas de atenção entrou em ponto de decisão.
- **Fatos lidos:** M17 (o `tev1` ordena o gatilho, AUC 0,74, com 6 "sim" em 23 pares), M18 (o `task` inteiro já vai ao
  `tev1` e o texto é descartado) e M19 (a sonda de Fagulha, n = 4).

| Parte do plano | Confiança na versão anterior | Confiança na versão atual | Uma linha de porquê |
| :------------- | :------------------------- | :------------------------ | :------------------ |
| O cliente (P1) | 74 | 78 | Entrou o "sem serviço" e o `unknown` explícito (R3, Lida); a ressalva de manter a folha pequena ainda não é teste. |
| A sombra, o corpus e a linha zero (P2, P3) | 74 | 76 | Limpeza da retenção sai do próprio cliente, sem job (R3, Lida), e a cópia do `fact_audit` não muda o veredito; o texto do `state` continua sensível. |
| A sugestão visível e a ordem | — | 60 | M17 tem 6 "sim" em 23 pares e n = 6; a ordem é barata, mas minha ideia de ordenar a auditoria não entrou. |
| A régua e o portão (P5, P6) | 69 | 70 | O probe usa o texto real (R3, Balança) e o desfecho gravado para o rótulo (R3, Lida); os cortes de 80% e 10% continuam provisórios. |
| As evoluções (P8) | 66 | 60 | "Ligar o `layer`" está marcado como não passando (M13), e o sugestor dos 494 fatos pendentes é um risco novo de ancorar quem aprova. |
| **O plano inteiro** | 72 | 70 | Ganhou catálogo, probe, retenção e painel, que são manutenção, e as minhas ressalvas de atenção não viraram ponto de decisão. |

- **A sua mudança da rodada anterior entrou?** em parte. Entraram o "sem serviço", o `unknown` sem retentativa, a limpeza
  sem job e a cópia que não muda o veredito (seção "O desenho", *Sem serviço* e *O corpus que hoje se perde*). Não entrou
  a ordem da fila da auditoria (minha última ideia), e a latência da escolha do `layer` disputando a fila do Ollama
  (M2) só aparece na seção "As fases", sem medida de ligação.
- **O que ainda está errado:** a seção "O desenho" põe o painel `sugestao_gatilho` na fase 2, antes de a sombra ter uma
  semana de dados; e o "primeiro passo" da linha zero depende de gravar o texto do `task` (M18), que é o que tem
  retenção. A retenção do `state` está em `.measurements/classify/state/`, fora do git, mas sem a política de texto
  sensível decidida (Rodada A), o plano não fecha.
- **A pergunta que Anderson precisa responder:** autoriza a fase 0 (a linha zero no resolver) e a fase 3 (a cópia do
  `fact_audit`) agora, e deixa a sugestão no painel para depois de uma semana de linhas `classify`? **Recomendo que sim**:
  as duas primeiras só gravam, e a sugestão visível é a única que põe algo na frente de quem decide.
- **Autoavaliação:** fiel à persona no corte de atenção e no "sem serviço"; saí dela ao aceitar a sugestão visível como
  fase 2 sem ter medido a leitura dela por Anderson, que é o custo real da persona.

<!-- fim-rodada-4 -->

Rodada 5 de Lida, das 21:57 às 21:57 (BRT). Li a proposta v4 (o desenho, o catálogo, a ordem visível e as fases), o
parecer do revisor sobre a v2 (`material/revisor-v2.md`, achados 1 a 11) e os fatos M3 revisto e M20. Não rodei o `tev1`.

Suposição declarada: a confiança que dou à v4 mede o que a persona vê na versão escrita, e não o acerto dos números,
que o revisor já conferiu. Decido por isso, sem perguntar.

### Rodada 5: a confiança na v4

- **Posição:** A v4 corrige o que o revisor achou, mas ainda não fixa a política de texto, e sem ela a fase 0 não fecha.
- **Fatos lidos:** M3 revisto (teto de ~5.000 caracteres com texto real), M20 (467 dos 494 pendentes são `inferido`), o
  parecer do revisor (achados 1 a 11 e as conferências que caíram).

| Parte do plano | Confiança na versão anterior | Confiança na versão atual | Uma linha de porquê |
| :------------- | :------------------------- | :------------------------ | :------------------ |
| **O plano inteiro** | 70 | 68 | A consistência subiu (fase 0 antes do cliente, `layer` fora do catálogo, `timeout_ms`, um escritor só); a política de texto segue aberta e ainda há módulo, catálogo, probes e replay para manter. |

- **O revisor acertou ou errou onde?** Acertou nos achados que mudam o desenho (1, 2, 4, 5, 7, 10) e nas premissas que
  caíram (fila e sugestor, achados 8 e 9). Errou em chamar esses dois de "cosméticos": cair a premissa tira o uso da
  lista, o que é mais que cosmético.
- **O que ainda está errado:**
  - A política de texto (Rodada A) não está decidida, e a v4 põe a fase 0 depois dela (seção "O desenho", *A
    gravação*). Sem ela, a fase 0 não tem retenção e não pode gravar o `task`.
  - O prazo da retenção segue "o que a Rodada A fixar" (seção "O desenho", *O cliente*, `timeout_ms`): o texto fica sem prazo até lá.
  - A fase 2b (o replay cego) e a fase 2 somam uns 4 h de trabalho, e a fase 3 espera ~7 semanas no ritmo de `rodado`
    (seção "As fases"). Para Lida, é o caminho que mais demora a poupar atenção.
  - As fases 0, 1, 2 e 2b criam quatro coisas de manter (módulo de gravação, cliente, probes, `sugestao-rN.json`), e a
    v4 não diz quem as mantém nem o que se desliga se o `tev1` sair.

<!-- fim-rodada-5 -->

## Custo da tarefa

Corrido 7 min — agente 5 min, quem pediu 3 min, pausa 0 s · US$ 2,48 (turnos 1,87, subagentes 0,61) · CPU 8,62 s do `claude` e 65,70 s dos comandos, RSS até 425 MB · 22 turnos, 1 sessão · dividida com 6 outros worklogs do commit · até 22:02 de 2026-11-09, pelo `brza note commit`
