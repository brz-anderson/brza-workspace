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

# Reunião tev1 nos fluxos: a participação de Balança, cética medidora

O pedido de Anderson, em 2026-11-09, na sessão da coordenação (meeting-runner, chat do BrzA Studio): "classificar, com fatos medidos, os melhores usos do `tev1:4b` local nas seis frentes — CLI, Studio, MCP, meeting-runner, plan-runner, migration-runner —, em estilo brainstorm; saída: proposta de plano e o plano criado neste workstream, mapeando para onde ele pode evoluir". Este é o
registro de **Balança** — persona cética medidora, no Grok `grok-4.7` `xhigh` —, aberto pela coordenação. A pauta e as
regras estão no briefing da reunião; cada rodada é uma seção abaixo, acrescentada no fim do arquivo.

## O que se fez

Às 21:32, `python3 -I .sessions/reuniao-tev1/material/balanca/tev1_pares.py`. O rótulo foi gravado em
`pares.json` antes do HTTP. 34 chamadas em série a `tev1:4b` em `/v1/systemone`, pergunta `gatilho` igual à do
probe. Primário: 23 pares (6 sim, 17 nao). Fora da tabela: 4 limítrofes, 3 confirma, 4 sintéticos de controle.

### Rodada 1: opinião inicial

- **Posição:** O tev1 não filtra gatilho: em 6 sim reais, 3 erros, e o limiar que os tira esvazia o uso.

#### 1. O ranking dos usos

- **Posição:** Alarme de gatilho, sombra do resolver, log; nenhum dos três age sozinho.
- **Por quê:** *Medido*, o comando acima. No limiar 0, acerto 18/23 e falso negativo 3/6. Os três erros são taxa-base: Relance R1 "poupa cliques" × M6 (nao, 0,115), Relance R1 "CI do PR" × M6 (nao, 0,054), Trava R2 "sete dias de would_fire" × M6 (nao, 0,013). Os sim certos são frase factual: cartão × M4 (0,74), nome de arquivo (0,57), "commit no PR" × M7 (0,36). *Medido*, controle sintético 4/4, com 0,16 / 0,57 / 0,41 / 0,80, como na issue. O 4/4 não atravessa. Dois FP no limiar 0 (0,002 e 0,028) morrem em 0,15. Uso 1, meeting-runner, script ao lado de `tally.py` (não escrito hoje): pergunta `gatilho`, opções sim/nao; só vira candidato se sim e confidence ≥ 0,50 — nesta amostra, 2/6 sim, e nenhum nao passou de 0,39. Uso 2, MCP `resolver.py` `classify`: pergunta `layer`, opções alta/media/rapida; *lido* no levantamento, 7 resoluções e 0 pelo tev1. Esta tabela é de outra pergunta, então a sombra loga e não escolhe. Uso 3: não há. O log em `material/balanca/` é o uso que age zero.
- **Ideias:** Regra assimétrica num `gatilho_tev1.py` imaginado: abaixo de 0,50 não age; em 0,50 ou mais, só publica `candidatos` se choice=sim `(ousadia: média)`. Segunda chave `evento` (ocorre/nao-ocorre) na mesma chamada, porque o erro caro é "o evento não existe", não "a frase está falsa" `(ousadia: alta)`.
- **Risco:** O limiar 0,15 dá FN 0/3 e acerto 10/10 só porque os três erros caíram na dúvida (13/23). O limítrofe Relance R2 × M6, rótulo sim e fora da tabela, veio nao com 0,217: se entrasse, o 0,15 teria FN aceito. n_sim=6, uma reunião.
- **Confiança:** 78/100

#### 2. A régua de entrada

- **Posição:** Entra com FN=0 nos sim de taxa-base e n_sim>=30; abaixo disso, dúvida.
- **Por quê:** *Medido*: o erro caro é sim dito nao. No limiar 0, 3/6. O par canônico (M6 × "poupa cliques") tem confidence 0,115: limiar ≤ 0,11 aceita o FN; a tabela mostra 1/4 em 0,10 e 0/3 em 0,15. *Lido* no briefing: confidence é 1 − entropia binária, conta da coordenação, inferida. Baixa não é "certeza de nao"; é moeda. A dúvida sobe à coordenação, não ao Haiku: não medi Haiku neste par. *Suposto* (60): Haiku pegaria a taxa-base. O n mínimo de 30 sim de taxa-base, com o limítrofe dentro e mais de uma reunião, é corte meu, não cálculo. Acerto 18/23 não é régua.
- **Ideias:** A tabela que vale é a de `tabela.json`, com n_sim e fp separados, não só o acerto `(ousadia: baixa)`. O limiar mora num arquivo de medição; sem o arquivo o script não age `(ousadia: média)`.
- **Risco:** n_sim≥30 é o vício desta persona, paralisia. O alarme que nunca apaga par pode entrar com n=6; o filtro que diz "não há gatilho" não pode.
- **Confiança:** 82/100

#### 3. Onde mora o cliente

- **Posição:** Um cliente no resolver; a reunião chama; sem Ollama, não classifica.
- **Por quê:** *Lido* no levantamento: `resolver.py` já faz tev1 → Haiku → fallback, e sem `resolver.tev1_min_confidence` tudo vai ao Haiku. O meeting-runner chama esse módulo; não abre HTTP próprio. *Lido* no briefing: acima de 2048 tokens a resposta é HTTP 400, sem truncar. O contrato recusa o state grande e devolve dúvida; não medi esse corte hoje. *Lido* no briefing: 8 em paralelo não dão vazão. O cliente é um por vez. Fila cheia espera ou desiste para a dúvida. Sem Ollama, a saída é "não sei", nunca um sim default. *Suposto*: Studio, plan-runner e migration-runner não chamam até terem tabela da pergunta deles.
- **Ideias:** `classify(state, questions)` no `brza-workflow`, e `_tev1` vira caller. Verbo `brza classify` só depois da régua `(ousadia: baixa)`. Meeting-runner passa `gatilho`; o resolver passa `layer`; limiares em chaves distintas `(ousadia: média)`.
- **Risco:** Um limiar único no cliente carrega o 0,50 do gatilho para a camada. A pergunta mudou; o número não viaja.
- **Confiança:** 74/100

#### 4. Além do óbvio

- **Posição:** Segunda pergunta evento na mesma chamada; não retreinar com n=6.
- **Por quê:** *Medido*: os 3 FN são "não há PR para o voto vigiar"; os sim certos são contradição literal (PR errado, nome de arquivo, regra de push). A pergunta do probe não é a do erro caro. *Lido* no briefing: 3 perguntas na mesma chamada somam ~60–90 ms, então a chave extra é barata e continua sem rótulo. Nos 3 `confirma`, o modelo disse nao (0,015, 0,040, 0,126): o critério escrito "não toca" não é o que ele faz; "não derruba" é. Ficaram fora da tabela de propósito. Não fazer: ligar o limiar do resolver com esta tabela; pré-filtrar 1.564 `fact_check` e US$ 7,16 (*lido*, levantamento) sem rótulo; classificar tela do Studio, onde a regex já decide (*lido*, levantamento); retreinar ou sentar outro modelo ao lado com 6 sim; usar o tev1 como persona, síntese ou revisor (*lido*, issue).
- **Ideias:** Alarme só se `gatilho` e `evento` forem sim, as duas com confidence ≥ 0,50 `(ousadia: alta)`. Reescrever o critério nao para "não derruba", e rerrotular, antes de crescer o n `(ousadia: baixa)`.
- **Risco:** A segunda pergunta, sem pares marcados, repete o 4/4 sintético e eu acredito.
- **Confiança:** 70/100

#### 5. O plano e para onde evolui

- **Posição:** Fase 0 é esta tabela; fase 1 só alarme sim>=0,50; o resto espera.
- **Por quê:** Fase 0, esta rodada, *medido*: pares, rótulo à mão, tabela, zero efeito em reunião. Pronto = `tabela.md` mais o comando. Fase 1: alarme no gatilho, só sim com confidence ≥ 0,50, candidato no estado, coordenação confirma. Pronto = 0 FP em mais 20 pares e nenhum nao automático. Fase 2: sombra do resolver, log sem limiar, até 30 rótulos de camada e tabela própria. Fase 3: se o taxa-base seguir como FN, medir a pergunta `evento`; senão, o tev1 sai desse uso. Evoluções abertas: retreino no log; segundo modelo só se o FN de taxa-base não cair; Studio, auditoria e migration-runner fechados; várias perguntas só na fase 3.
- **Ideias:** O plano deste workstream cita `material/balanca/` como a régua, não um número solto `(ousadia: baixa)`. Critério de morte: mais 20 sim de taxa-base ainda respondidos nao, e o uso 1 sai, fica o log `(ousadia: média)`.
- **Risco:** A fase 1, com 2 acertos em 6 sim, ensina confiança que o taxa-base não merece. O alarme não dispensa a leitura.
- **Confiança:** 76/100

#### A ideia mais ousada desta rodada

Duas perguntas no mesmo state, `gatilho` e `evento`, e o alarme só sai se as duas forem sim com confidence ≥ 0,50.
O erro que medi é taxa-base (3/6), e a pergunta atual não o vê. Risco: não rodei a segunda chave; coincidência
viraria régua. Até lá, o tev1 não apaga par nenhum.

#### Issues candidatas

- **Calibrar o gatilho com par real antes de limiar** — limiar 0 deu FN 3/6 no sim, n_sim=6 — prioridade `high`
- **Não herdar o limiar do gatilho no resolver** — a pergunta é `layer`; 0 das 7 resoluções passou pelo tev1 — prioridade `high`
- **Medir a pergunta `evento` (ocorre/nao-ocorre) à parte** — os três FN são "o evento não existe" — prioridade `medium`
- **Um cliente em cima de `_tev1`, limiares por pergunta** — HTTP espalhado transfere número entre perguntas — prioridade `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. O ranking dos usos | Alarme sim≥0,50, sombra do resolver, log; ninguém filtra sozinho | 78 |
| 2. A régua de entrada | FN=0 no sim de taxa-base e n_sim≥30; senão, dúvida à coordenação | 82 |
| 3. Onde mora o cliente | Módulo do resolver, uma chamada por vez; sem Ollama, não classifica | 74 |
| 4. Além do óbvio | Segunda pergunta `evento`; não retreinar, não auditar fato, não ler tela | 70 |
| 5. O plano e para onde evolui | Fase 0 tabela; fase 1 só alarme; taxa-base que não cair mata o uso | 76 |

<!-- fim-rodada-1 -->

### Rodada 2: debate

- **Posição:** Virei: nada liga. M12 mata o evento, M5 o None, M11 o alarme.

#### As disputas

- **D1 · o envelope do cliente:** c — módulo único (`Classifier.ask`, o desenho da Bitola) e verbo `brza classify` só como casca do hook, que não mora no pacote. *Lido* M2: quem serializa é o Ollama. Não medi processo contra import. — 68/100
- **D2 · o primeiro uso depois da sombra:** e — nada liga. *Lido* `material/coord/voto_cells.out`: None em 4/98, os 4 como ressalva (M5). *Lido* M6: 7 resoluções, 0 pelo tev1. *Medido* às 21:38, `ls` de `.measurements/fact-audit/` na raiz do repo: pasta vazia; *lido* `fact_audit.py:430` `os.remove` (M8). *Lido* `evento.out`: alarme ≥0,50 pega 2/6 sim e perde os 3 de taxa-base; `evento` é sim em 23/23 (0,82–0,88 nos três FN). E herda o erro; OU alarma tudo. — 86/100
- **D3 · a régua:** e: (a) com FP na conta e corte fora da amostra — n_sim≥30 e FN 0 no erro caro, mais o FP: `evento` teria FN 0 nos 6 sim e FP 17/17. O limiar 0,15 nasceu nestes 23. Sem pares novos, não liga. — 80/100
- **D4 · o diálogo de startup do Studio:** b — M9 diz que o volume não foi medido. Regex quebrar em 4 commits não é taxa de erro. Fora até haver n. — 78/100
- **D5 · retreino:** b — não agora (n_sim=6 no M11; sem corpus no M8). Fica aberto se a sombra guardar o parágrafo que o hook apaga. O (c) não tem de onde sair. — 84/100

#### Os ataques

- **Faro, pré-filtro e LoRA nos 1.564.** A pasta medida às 21:38 está vazia e a linha 430 apaga o parágrafo: 1.564 é contagem de evento, não par. M7: a classe cara, `fails`, são 17. M12: critério vago responde sim sempre. Os 60–80% são paper, já divergentes na síntese. Derruba este ataque um diretório que eu não abri, com parágrafo, evidência e os 17 fails, e um FN medido nessa classe.
- **Bitola, ligar o voto no `None`.** São 4 células em 98, e o out não mostra o texto, só "ressalva". Os 22/37 de apoio→ressalva ainda não condenam o modelo: `voto_cells.py:28` põe a coluna de ressalva no state, e o critério trata condição como ressalva. Derruba este ataque os 4 textos com esperado à mão, state só da célula de voto, e os 22/37 caindo quando a coluna sai.

#### A concessão

M12, a coordenação rodou a pergunta que eu lancei e não medi. O `evento` vê a taxa-base (0,82, 0,84 e 0,88 nos três FN do gatilho) e também os 17 não. Largo o alarme como primeiro uso e a segunda pergunta como portão. D2 era (a); agora é (e).

#### "Sim, e…"

Sobre a fase 0 da Fagulha, que só grava: o jsonl do `classify` copia o parágrafo antes do `os.remove` em `fact_audit.py:430`, com o veredito do Haiku quando existir. Sem essa cópia o M8 não acaba e a fase 1 dela não tem corpus. `(ousadia: média)`

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem ou o que te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :--------------------- |
| 1. O ranking dos usos | Só sombra até tabela; alarme e voto None não ligam | 78 | 84 | virou | M5, M8, M11, M12 |
| 2. A régua de entrada | n_sim≥30, FN 0, FP declarado, corte fora da amostra | 82 | 80 | ajustou | M12, Ferrolho |
| 3. Onde mora o cliente | Módulo único mais verbo-casca; fila é do Ollama | 74 | 68 | ajustou | Bitola, M2 |
| 4. Além do óbvio | `evento` não é portão: sim em 23/23, inclusive nos não | 70 | 82 | virou | M12 |
| 5. O plano e para onde evolui | Fase 0 grava, inclusive o parágrafo apagado; nada liga | 76 | 83 | virou | M8, M12, Fagulha |

<!-- fim-rodada-2 -->

### Rodada 3: voto final

- **Posição:** Apoio gravar já; nada decide. O layer medido não é o texto do request.
- **Fatos lidos:** M13, M14, M15 e o limite do M5.

#### O voto em cada proposta

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| P1 | apoio com ressalva | O log do POST que já existe não espera o módulo novo | 76 |
| P2 | apoio | O texto fora do git é o corpus; hash sem texto não calibra | 86 |
| P3 | apoio | Copiar no `finally`: o parágrafo está em `data`, o veredito nasce no `try` | 88 |
| P4 | apoio com ressalva | `voto` sem a coluna de ressalva; `layer` no `task`, não na description | 74 |
| P5 | apoio com ressalva | O holdout traz a classe que já errou, não um sorteio que a esvazia | 84 |
| P6 | apoio com ressalva | 80% e 10% são corte da sala; o portão usa o texto do request | 82 |
| P7 | apoio | Nenhuma. Diálogo só depois de contar os misses | 85 |
| P8 | apoio com ressalva | O `layer` destrava no `task` inteiro que passe o P6, não num n genérico | 80 |

#### O que me faria mudar de ideia

- **P3:** achar o parágrafo do fato num arquivo que sobreviva ao `os.remove`. *Lido* `fact_audit.py:405-411`: o `fact_check` leva id, veredito, `why` e `read`, não o texto do fato.
- **P2:** Anderson recusar por escrito o task em disco, ou um evento `route` que já guarde esse texto. *Medido* às 21:44, varredura de `.measurements/measurements.jsonl`: 7 `route` com `tev1_confidence`; `request` é número; o texto não está lá.

#### A última ideia

"Nada liga antes da tabela" mistura decidir com gravar. O `classify` já faz POST do `task` (`resolver.py:92`, `policy.py:251`) e descarta o texto: fica a `tev1_confidence`. O M13 (216/252 "alta", 13/60 no `general-purpose`, *lido* `ordem.out` e `layer2.out`) usou `description` de poucas palavras, com ou sem o papel — não é esse `task`. Esperar n≥30 para começar a guardar é o que impede os 30. Liga já o arquivo local do P2 ao lado desse POST, sem limiar e sem mudar a rota. Erro barato: disco e privacidade, 30 dias, fora do git. `(ousadia: média)`

#### Os colegas

| Persona | A contribuição mais útil dela, em uma linha | Nota de 0 a 10 |
| :------ | :------------------------------------------ | :------------- |
| Ferrolho | O corte do limiar sai de outra amostra, e o negativo também se revisa | 8 |
| Bitola | O contrato `Classifier.ask` e o `on_doubt` por pergunta, não um limiar só | 8 |
| Fagulha | A fase 0 que guarda o parágrafo que a auditoria apaga | 9 |
| Faro | O custo dos 1.564 e o arquivo de calibração; o corpus do LoRA não existia | 7 |
| Lida | O `tev1` não pode calar o que ela precisa ver; o limiar do `layer` recuou | 7 |

#### Autoavaliação

Fiel ao número: não deixei o 22% da description vetar o request, e não liguei rota. Saí da persona ao aceitar o task inteiro em disco, o risco que o Ferrolho nomeou, com 30 dias que eu não medi.

<!-- fim-rodada-3 -->

### Rodada 4: a confiança final

- **Posição:** O plano grava e não decide. A ordem do M17 deixa a taxa-base fora do topo.
- **Fatos lidos:** M16, M17, M18, M19.

| Parte do plano | Confiança na versão anterior | Confiança na versão atual | Uma linha de porquê |
| :------------- | :------------------------- | :------------------------ | :------------------ |
| O cliente (P1) | 76 | 82 | A linha zero não espera o módulo; a folha e o `too_long` seguem sem teste meu |
| A sombra, o corpus e a linha zero (P2, P3) | 86 | 88 | P3 era 88; o POST que já existe passa a guardar o `task` (M18) |
| A sugestão visível e a ordem | — | 70 | *Lido* `ranking.out`: o topo acerta 3; a taxa-base está em 11, 15 e 16; AUC 0,74 |
| A régua e o portão (P5, P6) | 82 | 86 | O probe é no texto do pedido e o holdout guarda a classe que já errou |
| As evoluções (P8) | 80 | 76 | M16 corta o dinheiro do pré-filtro; o sugestor dos 494 ancora e não foi medido |
| **O plano inteiro** | 74 | 76 | R3 não tinha nota única; 74 era o piso (P4). Sobe pouco: a ordem é da mesma amostra |

- **A sua mudança da rodada anterior entrou?** sim — "O primeiro passo, que não espera o módulo" e a fase 0; o probe no texto real, o hash que não calibra, a cópia no `finally` e o holdout da classe que errou.
- **O que ainda está errado:** em "A sugestão visível", a lista inteira está dita, mas não há a marca "não calibrado, n_sim=6". *Lido* `ranking.out`: ler os 10 primeiros pega 3 de 6 sim. Se o painel cortar a cauda, a taxa-base some.
- **A pergunta que Anderson precisa responder:** por quanto tempo o texto do `state` fica em disco — recomendo segurar o da pergunta até ela passar ou falhar a régua, não apagar em 30 dias.
- **Autoavaliação:** Fiel ao conferir o 0,74 (as posições fecham em 75/102) e ao não tratar o topo como gatilho. Saí ao subir nota sem rodar de novo: li a saída, não repeti o comando.

<!-- fim-rodada-4 -->

### Rodada 5: a confiança na v4

- **Posição:** A v4 fecha os furos do revisor. 76 vira 82; a fase 2b ainda não tem número.
- **Fatos lidos:** M3 revisto, M20 e o parecer do revisor sobre a v2.

| Parte do plano | Confiança na versão anterior | Confiança na versão atual | Uma linha de porquê |
| :------------- | :------------------------- | :------------------------ | :------------------ |
| **O plano inteiro** | 76 | 82 | A cópia e o `task` vão à fase 0; o `layer` sai do catálogo; o painel espera o replay no `state` do `tally` |

- **O revisor acertou ou errou onde?** Acertou nos achados 1, 2, 3 e 4: a v2 contradizia a própria régua, e o M17 era o meu resumo, não o texto do pedido. O 0,74 ele conferiu certo (75/102).
- **O que ainda está errado:** em "As fases", a 2b passa se "a leitura ordenada não perde a cauda", sem dizer quantos dos "sim" de taxa-base têm de aparecer. *Suposto:* eu leio isso como os três da cauda do M17, e sem esse número o replay aprova qualquer ordem.

<!-- fim-rodada-5 -->

## Custo da tarefa

Corrido 7 min — agente 5 min, quem pediu 3 min, pausa 0 s · US$ 2,48 (turnos 1,87, subagentes 0,61) · CPU 8,62 s do `claude` e 65,70 s dos comandos, RSS até 425 MB · 22 turnos, 1 sessão · dividida com 6 outros worklogs do commit · até 22:02 de 2026-11-09, pelo `brza note commit`
