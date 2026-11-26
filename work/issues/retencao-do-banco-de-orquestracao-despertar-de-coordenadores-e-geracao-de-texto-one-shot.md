---
status: open
description: Configuracoes de lancamento em preambulos (#49636), agrupamento de workers de servidores pareados (#49624) e sleep via CLI (#49609).
scope:
  - brza-studio
  - brza-workflow
  - brza-cli
priority: high
opened: 2026-11-13
tags:
  - tooling
  - infra
references:
  - https://github.com/stablyai/orca/pull/41041
  - https://github.com/stablyai/orca/pull/48888
  - https://github.com/stablyai/orca/pull/48871
  - https://github.com/stablyai/orca/pull/48916
  - https://github.com/stablyai/orca/issues/49035
  - https://github.com/stablyai/orca/issues/49043
  - https://github.com/stablyai/orca/issues/49038
  - https://github.com/stablyai/orca/pull/48738
  - https://github.com/stablyai/orca/pull/48684
  - https://github.com/stablyai/orca/pull/48683
  - https://github.com/stablyai/orca/pull/48664
  - https://github.com/stablyai/orca/pull/48686
  - https://github.com/stablyai/orca/pull/48782
  - https://github.com/stablyai/orca/pull/48794
  - https://github.com/stablyai/orca/pull/47953
  - https://github.com/stablyai/orca/issues/48841
  - https://github.com/stablyai/orca/issues/48840
  - https://github.com/stablyai/orca/pull/48562
  - https://github.com/stablyai/orca/pull/48202
  - https://github.com/stablyai/orca/pull/48518
  - https://github.com/stablyai/orca/pull/42264
  - https://github.com/stablyai/orca/pull/48427
  - https://github.com/stablyai/orca/issues/48594
  - https://github.com/stablyai/orca/issues/48593
  - https://github.com/stablyai/orca/issues/48592
  - https://github.com/stablyai/orca/issues/48614
  - https://github.com/stablyai/orca/pull/48011
  - https://github.com/stablyai/orca/pull/48411
  - https://github.com/stablyai/orca/pull/48387
  - https://github.com/stablyai/orca/pull/47428
  - https://github.com/stablyai/orca/pull/48435
  - https://github.com/stablyai/orca/pull/48390
  - https://github.com/stablyai/orca/issues/48434
  - https://github.com/stablyai/orca/issues/48444
  - https://github.com/stablyai/orca/pull/48274
  - https://github.com/stablyai/orca/pull/49263
  - https://github.com/stablyai/orca/pull/49262
  - https://github.com/stablyai/orca/pull/49221
  - https://github.com/stablyai/orca/pull/49238
  - https://github.com/stablyai/orca/pull/49160
  - https://github.com/stablyai/orca/pull/48943
  - https://github.com/stablyai/orca/pull/49127
  - https://github.com/stablyai/orca/issues/49254
  - https://github.com/stablyai/orca/issues/49220
  - https://github.com/stablyai/orca/issues/49218
  - https://github.com/stablyai/orca/issues/49183
  - https://github.com/stablyai/orca/issues/49125
  - https://github.com/stablyai/orca/issues/44184
  - https://github.com/stablyai/orca/issues/46425
  - https://github.com/stablyai/orca/issues/46406
  - https://github.com/stablyai/orca/pull/49445
  - https://github.com/stablyai/orca/pull/49441
  - https://github.com/stablyai/orca/pull/49458
  - https://github.com/stablyai/orca/pull/49350
  - https://github.com/stablyai/orca/pull/49300
  - https://github.com/stablyai/orca/pull/49312
  - https://github.com/stablyai/orca/pull/49280
  - https://github.com/stablyai/orca/pull/44113
  - https://github.com/stablyai/orca/issues/49308
  - https://github.com/stablyai/orca/issues/49307
  - https://github.com/stablyai/orca/issues/49274
  - https://github.com/stablyai/orca/issues/49273
  - https://github.com/stablyai/orca/issues/49271
  - https://github.com/stablyai/orca/issues/45187
  - https://github.com/stablyai/orca/issues/43668
  - https://github.com/stablyai/orca/pull/49636
  - https://github.com/stablyai/orca/pull/49624
  - https://github.com/stablyai/orca/pull/49413
  - https://github.com/stablyai/orca/pull/49587
  - https://github.com/stablyai/orca/issues/49623
  - https://github.com/stablyai/orca/issues/49609
  - https://github.com/stablyai/orca/issues/49606
  - https://github.com/stablyai/orca/issues/49602
  - https://github.com/stablyai/orca/issues/49564
  - https://github.com/stablyai/orca/issues/49550
  - https://github.com/stablyai/orca/issues/41962
  - https://github.com/stablyai/orca/issues/19980
---

# Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot

Rastreado dos PRs no upstream [`stablyai/orca#48274`](https://github.com/stablyai/orca/pull/48274),
[`stablyai/orca#48263`](https://github.com/stablyai/orca/pull/48263),
[`stablyai/orca#48271`](https://github.com/stablyai/orca/pull/48271),
[`stablyai/orca#48255`](https://github.com/stablyai/orca/pull/48255),
[`stablyai/orca#48256`](https://github.com/stablyai/orca/pull/48256),
[`stablyai/orca#48277`](https://github.com/stablyai/orca/pull/48277),
[`stablyai/orca#48283`](https://github.com/stablyai/orca/pull/48283),
além das issues [`stablyai/orca#48312`](https://github.com/stablyai/orca/issues/48312),
[`stablyai/orca#48295`](https://github.com/stablyai/orca/issues/48295),
[`stablyai/orca#48290`](https://github.com/stablyai/orca/issues/48290),
[`stablyai/orca#48262`](https://github.com/stablyai/orca/issues/48262),
[`stablyai/orca#48146`](https://github.com/stablyai/orca/pull/48146),
[`stablyai/orca#48153`](https://github.com/stablyai/orca/pull/48153) (commit `31274053e71`),
[`stablyai/orca#48178`](https://github.com/stablyai/orca/pull/48178) (commit `d69b00a84a4`),
[`stablyai/orca#48080`](https://github.com/stablyai/orca/pull/48080),
[`stablyai/orca#48087`](https://github.com/stablyai/orca/pull/48087),
[`stablyai/orca#45882`](https://github.com/stablyai/orca/pull/45882) (commit `28a6043afa3`),
além das issues [`stablyai/orca#48086`](https://github.com/stablyai/orca/issues/48086),
[`stablyai/orca#48019`](https://github.com/stablyai/orca/issues/48019),
[`stablyai/orca#48010`](https://github.com/stablyai/orca/issues/48010),
[`stablyai/orca#47973`](https://github.com/stablyai/orca/pull/47973),
[`stablyai/orca#47914`](https://github.com/stablyai/orca/pull/47914),
[`stablyai/orca#47951`](https://github.com/stablyai/orca/pull/47951),
[`stablyai/orca#47953`](https://github.com/stablyai/orca/pull/47953),
[`stablyai/orca#47892`](https://github.com/stablyai/orca/pull/47892) (refs Issue [`#47891`](https://github.com/stablyai/orca/issues/47891)),
[`stablyai/orca#47947`](https://github.com/stablyai/orca/pull/47947) (commit `06f0ca1a8bd`),
[`stablyai/orca#47887`](https://github.com/stablyai/orca/pull/47887) (commit `b5b84ae3d27`),
[`stablyai/orca#47779`](https://github.com/stablyai/orca/pull/47779) (commit `3a53a931aff`),
[`stablyai/orca#47898`](https://github.com/stablyai/orca/pull/47898) (commit `d8747bb5bb4`),
[`stablyai/orca#47877`](https://github.com/stablyai/orca/pull/47877) (commit `ab59c53f6ad`),
[`stablyai/orca#47893`](https://github.com/stablyai/orca/pull/47893) (commit `15b0e99c035`),
[`stablyai/orca#47554`](https://github.com/stablyai/orca/pull/47554) (commit `2467e89de8c`),
[`stablyai/orca#47548`](https://github.com/stablyai/orca/pull/47548) (commit `b7c38c4f684`),
[`stablyai/orca#47818`](https://github.com/stablyai/orca/pull/47818) (commit `9a9290d4697`),
além das issues [`stablyai/orca#47868`](https://github.com/stablyai/orca/issues/47868),
[`stablyai/orca#47852`](https://github.com/stablyai/orca/issues/47852),
[`stablyai/orca#45906`](https://github.com/stablyai/orca/issues/45906) e
[`stablyai/orca#41179`](https://github.com/stablyai/orca/issues/41179),
[`stablyai/orca#47828`](https://github.com/stablyai/orca/pull/47828) (resolve Issue [`#46100`](https://github.com/stablyai/orca/issues/46100)),
[`stablyai/orca#47819`](https://github.com/stablyai/orca/pull/47819) (resolve Issue [`#46100`](https://github.com/stablyai/orca/issues/46100)),
[`stablyai/orca#47783`](https://github.com/stablyai/orca/pull/47783) (resolve Issue [`#46100`](https://github.com/stablyai/orca/issues/46100)),
[`stablyai/orca#47536`](https://github.com/stablyai/orca/pull/47536),
[`stablyai/orca#47575`](https://github.com/stablyai/orca/pull/47575),
além da issue [`stablyai/orca#47817`](https://github.com/stablyai/orca/issues/47817),
[`stablyai/orca#47562`](https://github.com/stablyai/orca/pull/47562),
[`stablyai/orca#46045`](https://github.com/stablyai/orca/pull/46045),
[`stablyai/orca#47543`](https://github.com/stablyai/orca/pull/47543),
[`stablyai/orca#47503`](https://github.com/stablyai/orca/pull/47503),
[`stablyai/orca#47370`](https://github.com/stablyai/orca/pull/47370),
[`stablyai/orca#47371`](https://github.com/stablyai/orca/pull/47371),
[`stablyai/orca#47364`](https://github.com/stablyai/orca/pull/47364),
[`stablyai/orca#47363`](https://github.com/stablyai/orca/pull/47363),
[`stablyai/orca#47355`](https://github.com/stablyai/orca/pull/47355),
[`stablyai/orca#47469`](https://github.com/stablyai/orca/pull/47469) (resolve Issue [`#47440`](https://github.com/stablyai/orca/issues/47440)),
[`stablyai/orca#47135`](https://github.com/stablyai/orca/pull/47135),
[`stablyai/orca#47081`](https://github.com/stablyai/orca/pull/47081),
[`stablyai/orca#46842`](https://github.com/stablyai/orca/pull/46842),
[`stablyai/orca#46826`](https://github.com/stablyai/orca/pull/46826),
[`stablyai/orca#46797`](https://github.com/stablyai/orca/pull/46797),
[`stablyai/orca#46757`](https://github.com/stablyai/orca/pull/46757),
[`stablyai/orca#47072`](https://github.com/stablyai/orca/pull/47072),
[`stablyai/orca#46643`](https://github.com/stablyai/orca/pull/46643),
[`stablyai/orca#47048`](https://github.com/stablyai/orca/pull/47048),
[`stablyai/orca#46955`](https://github.com/stablyai/orca/pull/46955) (resolve Issue [`#46944`](https://github.com/stablyai/orca/issues/46944)),
[`stablyai/orca#46793`](https://github.com/stablyai/orca/pull/46793),
[`stablyai/orca#46571`](https://github.com/stablyai/orca/pull/46571),
[`stablyai/orca#46562`](https://github.com/stablyai/orca/pull/46562),
[`stablyai/orca#46541`](https://github.com/stablyai/orca/pull/46541),
[`stablyai/orca#46287`](https://github.com/stablyai/orca/pull/46287),
[`stablyai/orca#46446`](https://github.com/stablyai/orca/pull/46446),
[`stablyai/orca#46448`](https://github.com/stablyai/orca/pull/46448),
[`stablyai/orca#46273`](https://github.com/stablyai/orca/pull/46273),
[`stablyai/orca#46517`](https://github.com/stablyai/orca/pull/46517),
[`stablyai/orca#46602`](https://github.com/stablyai/orca/pull/46602) (STA-16956),
[`stablyai/orca#46478`](https://github.com/stablyai/orca/pull/46478),
[`stablyai/orca#46477`](https://github.com/stablyai/orca/pull/46477),
[`stablyai/orca#46402`](https://github.com/stablyai/orca/pull/46402) (resolve Issue [`#33634`](https://github.com/stablyai/orca/issues/33634)),
[`stablyai/orca#46412`](https://github.com/stablyai/orca/pull/46412),
[`stablyai/orca#46397`](https://github.com/stablyai/orca/pull/46397),
[`stablyai/orca#46450`](https://github.com/stablyai/orca/pull/46450),
[`stablyai/orca#46360`](https://github.com/stablyai/orca/pull/46360),
[`stablyai/orca#46286`](https://github.com/stablyai/orca/pull/46286),
[`stablyai/orca#46120`](https://github.com/stablyai/orca/pull/46120),
[`stablyai/orca#46140`](https://github.com/stablyai/orca/pull/46140),
[`stablyai/orca#46372`](https://github.com/stablyai/orca/pull/46372),
[`stablyai/orca#46235`](https://github.com/stablyai/orca/pull/46235),
[`stablyai/orca#46196`](https://github.com/stablyai/orca/pull/46196),
[`stablyai/orca#46086`](https://github.com/stablyai/orca/pull/46086),
[`stablyai/orca#46155`](https://github.com/stablyai/orca/pull/46155),
[`stablyai/orca#46117`](https://github.com/stablyai/orca/pull/46117),
[`stablyai/orca#46080`](https://github.com/stablyai/orca/pull/46080),
[`stablyai/orca#46068`](https://github.com/stablyai/orca/pull/46068),
[`stablyai/orca#46139`](https://github.com/stablyai/orca/pull/46139),
[`stablyai/orca#46207`](https://github.com/stablyai/orca/pull/46207),
[`stablyai/orca#45751`](https://github.com/stablyai/orca/pull/45751) (refs Issue [`#14570`](https://github.com/stablyai/orca/issues/14570)),
[`stablyai/orca#45507`](https://github.com/stablyai/orca/pull/45507) (STA-16556, STA-16557, STA-16590),
[`stablyai/orca#45744`](https://github.com/stablyai/orca/pull/45744) (refs Issue [`#45701`](https://github.com/stablyai/orca/issues/45701)),
[`stablyai/orca#45435`](https://github.com/stablyai/orca/pull/45435),
[`stablyai/orca#45819`](https://github.com/stablyai/orca/pull/45819),
[`stablyai/orca#45426`](https://github.com/stablyai/orca/pull/45426),
[`stablyai/orca#45370`](https://github.com/stablyai/orca/pull/45370),
[`stablyai/orca#45462`](https://github.com/stablyai/orca/pull/45462),
[`stablyai/orca#45194`](https://github.com/stablyai/orca/pull/45194),
[`stablyai/orca#44472`](https://github.com/stablyai/orca/pull/44472),
[`stablyai/orca#45290`](https://github.com/stablyai/orca/pull/45290),
[`stablyai/orca#45330`](https://github.com/stablyai/orca/pull/45330),
[`stablyai/orca#44919`](https://github.com/stablyai/orca/pull/44919),
[`stablyai/orca#44590`](https://github.com/stablyai/orca/pull/44590) (resolve Issue [`#43875`](https://github.com/stablyai/orca/issues/43875)),
[`stablyai/orca#44332`](https://github.com/stablyai/orca/pull/44332),
[`stablyai/orca#44475`](https://github.com/stablyai/orca/pull/44475),
[`stablyai/orca#44327`](https://github.com/stablyai/orca/pull/44327),
[`stablyai/orca#43953`](https://github.com/stablyai/orca/pull/43953),
[`stablyai/orca#43550`](https://github.com/stablyai/orca/pull/43550),
[`stablyai/orca#43467`](https://github.com/stablyai/orca/pull/43467) (resolve Issue [`#43039`](https://github.com/stablyai/orca/issues/43039)),
além das issues [`stablyai/orca#43957`](https://github.com/stablyai/orca/issues/43957),
[`stablyai/orca#43925`](https://github.com/stablyai/orca/issues/43925),
[`stablyai/orca#43875`](https://github.com/stablyai/orca/issues/43875),
[`stablyai/orca#43874`](https://github.com/stablyai/orca/issues/43874),
[`stablyai/orca#43869`](https://github.com/stablyai/orca/issues/43869),
[`stablyai/orca#43618`](https://github.com/stablyai/orca/issues/43618),
[`stablyai/orca#43016`](https://github.com/stablyai/orca/pull/43016),
[`stablyai/orca#42839`](https://github.com/stablyai/orca/pull/42839) (resolve STA-15101),
[`stablyai/orca#42747`](https://github.com/stablyai/orca/pull/42747) (resolve Issue [`#42732`](https://github.com/stablyai/orca/issues/42732)),
[`stablyai/orca#42708`](https://github.com/stablyai/orca/pull/42708),
[`stablyai/orca#42707`](https://github.com/stablyai/orca/pull/42707),
[`stablyai/orca#42535`](https://github.com/stablyai/orca/pull/42535) (resolve Issue [`#42148`](https://github.com/stablyai/orca/issues/42148)),
[`stablyai/orca#42338`](https://github.com/stablyai/orca/pull/42338) (resolve Issue [`#42103`](https://github.com/stablyai/orca/issues/42103)),
[`stablyai/orca#42264`](https://github.com/stablyai/orca/pull/42264) (resolve Issue [`#19166`](https://github.com/stablyai/orca/issues/19166)),
[`stablyai/orca#42284`](https://github.com/stablyai/orca/pull/42284) (resolve Issue [`#42230`](https://github.com/stablyai/orca/issues/42230)),
[`stablyai/orca#42122`](https://github.com/stablyai/orca/pull/42122) (resolve STA-15102),
[`stablyai/orca#42114`](https://github.com/stablyai/orca/pull/42114),
[`stablyai/orca#42112`](https://github.com/stablyai/orca/pull/42112),
[`stablyai/orca#42111`](https://github.com/stablyai/orca/pull/42111),
[`stablyai/orca#41979`](https://github.com/stablyai/orca/pull/41979) (resolve Issue [`#41975`](https://github.com/stablyai/orca/issues/41975)),
[`stablyai/orca#41757`](https://github.com/stablyai/orca/pull/41757) (resolve Issue [`#41756`](https://github.com/stablyai/orca/issues/41756)),
[`stablyai/orca#41746`](https://github.com/stablyai/orca/pull/41746),
[`stablyai/orca#41702`](https://github.com/stablyai/orca/pull/41702),
[`stablyai/orca#41729`](https://github.com/stablyai/orca/pull/41729) (resolve Issue [`#41726`](https://github.com/stablyai/orca/issues/41726)) e
[`stablyai/orca#41754`](https://github.com/stablyai/orca/pull/41754) (resolve Issue [`#40838`](https://github.com/stablyai/orca/issues/40838)),
além das issues [`stablyai/orca#42731`](https://github.com/stablyai/orca/issues/42731),
[`stablyai/orca#42719`](https://github.com/stablyai/orca/issues/42719),
[`stablyai/orca#42733`](https://github.com/stablyai/orca/issues/42733),
[`stablyai/orca#42734`](https://github.com/stablyai/orca/issues/42734) e
[`stablyai/orca#42084`](https://github.com/stablyai/orca/issues/42084).

## O problema

1. **Crescimento ilimitado e ausência de retenção no banco SQLite de orquestração (`#41757`, resolve `#41756`):**
   - O banco `orchestration.db` acumulava indefinidamente registros de execuções (*Runs*), tarefas (*Tasks*), despachos (*Dispatches*) e mensagens de correio de coordenação sem nenhuma rotina de expurgo automático;
   - Em operações contínuas com múltiplos agentes e pipelines diários, o banco crescia descontroladamente gerando contenção de I/O em locks SQLite até que o desenvolvedor deletasse o arquivo manualmente.
2. **Coordenadores em modo sleep nunca acordavam para receber resultados de workers (`#41746`):**
   - Quando a funcionalidade experimental *Agent sleep* estava habilitada, o orquestrador colocava o agente coordenador em modo de repouso (desalocando seu terminal/PTY) enquanto seus workers ainda executavam em paralelo;
   - Ao concluir a tarefa e postar a mensagem `worker_done`, o despachador de correio tentava digitar no terminal e falhava silenciosamente porque a aba estava dormindo;
   - As mensagens ficavam represadas na caixa de correio sem sino ou notificação até que o usuário clicasse manualmente na aba do coordenador.
3. **Agentes trabalhadores travados silenciosamente no meio de um turno sem aviso ao coordenador (`#41702`):**
   - Quando um subagente ou worker congelava durante a chamada de modelo (ex.: conexões de API pendentes sem timeout) ou em ferramentas externas bloqueadas, o orquestrador não enviava nenhum sinal porque só notificava o coordenador no encerramento formal do turno;
   - O coordenador aguardava indefinidamente e tarefas orquestradas ficavam congeladas por mais de 12h sem nenhuma visibilidade na árvore de tarefas.
4. **Ausência de método leve e direto para geração one-shot de texto por agentes via CLI (`#41729`, resolve `#41726`):**
   - Scripts e ferramentas de automação que precisavam apenas de uma resposta textual direta de um modelo (ex.: resumir um diff, gerar mensagem de commit ou avaliar um JSON) eram forçados a inicializar um worktree completo, alocar terminais PTY e subir todo o harness de ferramentas e hooks do agente, impondo latência e desperdício de recursos.
5. **Incapacidade de enviar textos longos via stdin ou arquivo no comando `terminal send` (`#41754`, resolve `#40838`):**
   - O comando de automação de terminal aceitava apenas strings passadas como argumento de linha de comando (`terminal send --text "..."`), expondo prompts confidenciais e conteúdos extensos na tabela pública de processos do sistema operacional (`ps`) e estourando limites de tamanho de argumentos (`ARG_MAX`).
6. **Perguntas de workers respondidas continuavam retidas como não lidas na caixa de correio do coordenador (`#41979`, resolve `#41975`):**
   - Quando um coordenador respondia à pergunta de um worker através de `answerQuestion`, a mensagem da pergunta original não era marcada como lida (`read = 1`);
   - O coordenador precisava rodar chamadas extras de `orchestration check --run <run>` exclusivamente para limpar a pendência da pergunta respondida, gerando centenas de transações e recibos redundantes no banco.
7. **Sobrecarga do pull-loop de servidores pareados com conjunto temporário no SQLite (`#42122`, resolve STA-15102):**
   - A consulta de links abertos no pull-loop (`state IN ('open', 'cancel_owed')`) obrigava o SQLite a construir um conjunto temporário em cada iteração, e a checagem de home-conversation rodava como instrução separada;
   - Servidores com apenas um link ativo pagavam mais caro a cada pull do que a varredura global legada.
8. **Timeout de 60s em `worker-start --terminal` ao reutilizar agente que segue ativo pós-conclusão (`#42114`):**
   - O comando `worker-start --terminal <pane>` passava uma nova tarefa a um agente já rodando na aba, mas sua verificação de prontidão aguardava `tui-idle`;
   - Como agentes frequentemente continuam executando tarefas em background após `worker_done` (ex.: observando CI), o reuso falhava com `agent_readiness: timeout` após 60s em vez de entregar a instrução no correio do agente.
9. **Estado inconsistente e ausência do nome do agente em falhas de binding no reuse-start (`#42112`, `#42111`):**
   - Quando um início de reuso de worker falhava antes da conclusão do binding, o registro marcava o worker como iniciado incorretamente e omitia o nome do agente reutilizado nos metadados.
10. **Omissão do objeto `run` e perda de acesso ao coordenador na saída concisa `--json` (`#42338`, resolve `#42103`):**
    - A versão 1.4.258 removeu o nó `run` da saída concisa de `run-show`, `run-current` e `run-use`, impossibilitando que scripts de CLI obtenham o `coordinator_handle` sem exigir o despejo `--full`.
11. **Bloqueio no comando `worker-release` quando o terminal PTY do worker já encerrou (`#42264`, resolve `#19166`):**
    - Se o terminal do worker saísse prematuramente ou fosse fechado sem emitir um código de saída capturado pelo orchestrator, o comando `worker-release` falhava com erro de terminal indisponível, deixando o worker em estado zumbi no banco.
12. **Falta de identificadores de sessão de chat vinculados ao worker no output JSON (`#42284`, resolve `#42230`):**
    - Scripts que coordenavam múltiplos workers a partir do chat não conseguiam correlacionar a sessão de chat que solicitou o worker (`creatorOrcaSessionId`) nem a sessão atribuída a ele (`assigneeOrcaSessionId`).
13. **Aceite inadvertido de relatórios vazios em `worker_done` (`#42535`, resolve `#42148`):**
    - Quando um script de worker falhava ao ler o arquivo de relatório (ex.: `cat missing-file` vazio), o comando `orchestration send --type worker_done` aceitava `--body ""` como se o corpo tivesse sido omitido, concluindo a tarefa prematuramente e perdendo o relatório de execução.
14. **Listagem indiscriminada de todas as caixas postais da máquina em `orchestration inbox` (`#42747`, resolve `#42732`):**
    - O comando `orca orchestration inbox` listava todas as mailboxes da máquina por padrão sem expor o parâmetro `--run`, embora o backend RPC já oferecesse suporte a filtragem por Run.
15. **Prompts de terminal aprovados não marcados como respondidos durante a execução de ferramentas (`#42708`):**
    - Enquanto a ferramenta aprovada pelo usuário ainda estava em execução, o prompt interativo continuava aparecendo como pendente no orquestrador, arriscando duplicidade de aprovação.
16. **Truncamento de leituras de workers de chat e perda de projeção de frota (`#42707`):**
    - Leituras massivas de mensagens de workers saturavam buffers em consultas não paginadas, corrompendo a projeção consolidada da frota de agentes.
17. **Refugos indevidos de `decision_gate` e escalações entregues na mailbox do destinatário (`#42731`, `#43016`):**
    - Quando um `decision_gate` ou escalação de permissão era recusada por um agente ou autoridade não-atribuída, a recusa era persistida e despachada para a caixa de correio do destinatário original como mensagem de erro urgente, gerando falsos positivos e poluindo o fluxo da conversa.
18. **Poluição de abas com terminais coordenadores de Runs e saídas JSON inchadas (`#42719`, `#42733`, `#42734`):**
    - Execuções de automação criavam abas de terminal visíveis obrigatórias para coordenadores; saídas de `worktree ps/list --json` despejavam ~0.5 MB (~130k tokens) de campos nulos e duplicados sem visão concisa; e recibos de `worker-start` omitiam o caminho do worktree e título da tarefa.
19. **Inchaço do banco `orchestration.db` por cópias estáticas redundantes de chat e falta de auto_vacuum incremental (`#42839`, resolve STA-15101):**
    - O banco de orquestração acumulava cópias integrais de chats de workers resolvidos (~120 KB por cópia em milhares de tarefas), atingindo mais de 1.6 GB com centenas de megabytes de espaço interno desperdiçado, sem capacidade de redução automática de tamanho físico em disco.
20. **Falha na parada e fechamento de workers federados iniciados remotamente (`#42852`):**
    - Quando um worker era iniciado em um host remoto pareado a partir de outro host, a solicitação de Stop/Close pelo host receptor não era roteada de volta ao host de origem (*home-routed*), deixando o processo do worker rodando indefinidamente na máquina remota.
21. **Travamento da thread principal durante expurgo massivo de Runs resolvidos (`#43550`):**
    - A rotina de expurgo de execuções concluídas no `orchestration.db` processava todos os registros elegíveis em uma única transação síncrona, causando congelamentos de centenas de milissegundos na main thread do Electron.
22. **Rejeição de `worker_done` de workers em servidores conectados como despacho desconhecido (`#43618`):**
    - Workers supervisionados disparados em servidores Orca conectados (`worker-start --on <server>`) tinham suas mensagens de conclusão `worker_done` recusadas pelo coordenador sob pretexto de despacho não reconhecido, impedindo a liquidação automática do despacho.
23. **Reserva de inicialização estruturada de Codex retida indefinidamente (`#43467`, resolve `#43039`):**
    - Quando um worker estruturado era abortado ou liberado precocemente via `worker-release`, a reserva de recursos alocada para o início do Codex ficava órfã e bloqueava despachos subsequentes.
24. **Terminais de workers retidos após prova de saída (`#43953`):**
    - Quando um worker recebia ordem de parada (`worker-stop`), o recurso de terminal PTY não era liberado mesmo após o encerramento comprovado do processo, pois a rotina `settleWorkerStop` falhava em desalocar o handle de terminal associado.
25. **Perda de receita de inicialização ao retomar worker finalizado (`#44590`, resolve `#43875`):**
    - A receita de inicialização (comando, argumentos e variáveis de ambiente) gravada pelo Orca no início de um worker era perdida se uma captura subsequente de contexto não conseguisse ler o processo finalizado. Ao reativar o worker ou despachar follow-up via `orchestration send`, o ambiente perdia o contexto de execução original.
26. **Omissão do ID de sessão do provedor (Claude Code) vinculado ao worker (`#43957`):**
    - O comando `worker-read --source transcript` retornava transcrições vinculadas, mas a API e a CLI de orquestração não expunham o session ID nativo do provedor (`providerSessionId`), impedindo a correlação direta de logs e ferramentas externas.
27. **Impossibilidade de recriar terminal substituto condicionalmente para um Run ativo (`#43925`):**
    - Quando o terminal de um coordenador sofria encerramento inesperado em seu worktree, não havia comando ou condição suportada para criar um terminal de substituição mantendo o mesmo identificador de Run.
28. **Ausência de deep link `orca://` para abas de chat e mensagens de orquestração (`#43874`):**
    - Ferramentas externas, scripts de automação e notificações não tinham esquema de URI (`orca://chat/...`) para focar diretamente a aba de chat ou abrir o thread de uma mensagem de orquestração entregue.
29. **Rejeição de `worker_done` de workers rodando em host WSL (`#43869`):**
    - Workers supervisionados disparados com `--on <WSL host>` tinham suas mensagens de finalização `worker_done` rejeitadas com erro de despacho desconhecido ("unknown dispatch") pelo coordenador rodando no host principal.
30. **Incapacidade de responder a pedidos de permissão de subagentes auxiliares pelo coordenador (`#44475`):**
    - Quando um worker Claude disparava um subagente auxiliar (*helper agent*) que solicitava permissão para executar uma ferramenta (ex.: Bash), o prompt recebia resposta vazia `{}` automaticamente caso o desenvolvedor não estivesse diretamente no terminal do worker;
    - O coordenador não tinha visibilidade do diálogo de permissão e o fluxo ficava travado ou abortava silenciosamente.
31. **Congelamento da thread principal por checkpoints síncronos de WAL no banco de orquestração (`#44327`):**
    - Transações pequenas de atualização de status (como contagem regressiva de auto-close de workers sendo suspensa ou reiniciada) que cruzavam o limiar de auto-checkpoint do SQLite (1.000 frames) disparavam o checkpoint síncrono do WAL diretamente na thread principal, gerando travamentos de até 500 ms no Electron.
32. **Falta de especificação e documentação dos tipos de mail suportados entre agentes e sobre `--on` (`#44332`):**
    - Agentes orquestradores e workers tinham dificuldades para selecionar os tipos corretos de correio ao enviar mensagens via `orca orchestration send` ou `orca-cli` (especialmente em ambientes com servidores pareados via `--on`), enviando formatos genéricos e falhando em distinguir `task_result`, `ask`, `reply`, `worker_done` e `status`.
33. **Ausência ou falha no roteamento de pedidos de permissão de workers em chats de coordenador em servidores pareados (`#44919`):**
    - Quando um chat de coordenador é executado em um servidor pareado ou ambiente remoto gerenciado, os prompts de autorização/aprovação (*worker approval prompts*) de subagentes e workers ficavam inacessíveis ou falhavam ao rotear a resposta pelo host proprietário da sessão de chat;
    - Faltava também suporte para que janelas ou dispositivos pareados (como clientes móveis) pudessem encerrar streams de aprovação ou aceitar emparelhamentos como a pessoa operadora.
34. **Incapacidade de enviar arquivos e anexos em mensagens de correio sobre itens gerenciados (`#45194`):**
    - Ao despachar mensagens de correio de orquestração sobre itens ou tarefas de agentes gerenciados (localmente ou em servidores conectados), não era possível anexar caminhos de arquivos legíveis pelos destinatários, impedindo a entrega de relatórios ou evidências anexas.
35. **Perda de identificação de remetentes de mensagens de workers após o fechamento do painel (`#44472`):**
    - Assim que o terminal ou chat de um worker encerrava e seu painel era descartado, qualquer mensagem anteriormente enviada por ele passava a exibir como remetente o texto genérico "an agent" em vez do nome da tarefa, agente e servidor remoto associados ao despacho original.
36. **Congelamento da aplicação por até 32 segundos ao abrir chats nativos com bancos volumosos (`#45290`):**
    - Cada chat nativo visível realizava subscrição síncrona em `orchestration.crewSubscribe`, forçando a reconstrução completa de snapshots de equipe na thread principal mesmo quando o painel de tripulação (*crew panel*) estava em repouso.
37. **Lentidão em varreduras de coordenadores legados (`#45330`):**
    - A recuperação de coordenadores legados no banco SQLite consultava a tabela `dispatch_contexts` sem filtro por tarefa, gerando varreduras desnecessárias de linhas em bases com histórico extenso.
38. **Consulta de correio de coordenador legado varrendo todos os dispatches em vez de filtrar por endereço (`#45426`):**
    - A recuperação de mensagens de correio destinadas a coordenadores legados realizava uma junção ampla com a tabela de Dispatches inteira em vez de sondar diretamente por endereço via índice composto `(run_id, to_address)` no SQLite;
    - Isso causava degradação de performance proporcional ao volume acumulado de dispatches no `orchestration.db`.
39. **Envio prematuro de mensagens de correio cancelando turnos em andamento de agentes ACP que controlam steering por cancelamento (`#45370`):**
    - Mensagens rotineiras de status ou atualizações de correio entregues a agentes ACP (como Antigravity) no meio de um turno ativo provocavam o cancelamento do turno em execução caso o provedor declarasse `steering: 'queue'`;
    - Faltava reter e enfileirar o correio de orquestração até o término do turno corrente para agentes com modelo de fila estrita.
40. **Aspas desnecessárias em tokens seguros de recuperação no cmd do Windows (`#45462`):**
    - Na montagem de comandos de recuperação para o `cmd.exe` no Windows, tokens alfanuméricos seguros (`[A-Za-z0-9_.-]+`) eram envolvidos por aspas desnecessárias, causando problemas de parsing e quebras em scripts de terminal.
41. **Preâmbulo de workers exibindo o handle do terminal coordenador gerando mistura em `--from` (`#45751`, refs `#14570`):**
    - O preâmbulo de inicialização de workers imprimia o handle `term_` do coordenador logo acima dos comandos sugeridos ao worker, que usam o próprio handle do worker em `--from`;
    - Workers acabavam copiando partes do identificador errado para o remetente, fazendo com que mensagens de heartbeat e `worker_done` fossem rejeitadas como vindas do painel errado.
42. **Vazamento e crescimento ilimitado do ledger de orquestração sob crash-cuts (`#45507`):**
    - Em interrupções abruptas ou falhas de processo (*crash-cut*), o livro-razão automático de orquestração acumulava registros de continuação indefinidamente sem teto de bytes, arriscando estourar limites de leitura na retomada;
    - Além disso, faltava expor primitivas de liquidação e descarte de tarefas reiniciáveis (`restartLaunchSettled`, `restartResumableDismiss`) para clientes pareados.
43. **Nível de esforço de raciocínio de modelos Antigravity estruturados sobrescrito por opções salvas (`#45744`, refs `#45701`):**
    - Ao disparar um worker Antigravity estruturado com um ID de modelo que carrega sufixo de nível (ex.: `--model gemini-4-hydrogen-medium`) omitindo `--effort`, o runtime mesclava as opções sobre a seleção salva de chat do usuário, substituindo o nível explícito do modelo pelo esforço previamente salvo.
44. **Reconstrução completa do host de tripulação (crew host) a cada alternância de abas (`#45435`):**
    - Assim que a última aba ouvinte deixava de monitorar a tripulação, o host era destruído imediatamente na thread principal do Electron;
    - Ao retornar à aba ou reconectar, a aplicação reconstruía o host inteiro do zero, congelando a interface por vários segundos em execuções com grande volume de tarefas.
45. **Relatórios finais `worker_done` de workers não acordando membros do grupo em chats de bots (`#45819`):**
    - A varredura de correio de grupos procurava o worker por seu sender handle, mas relatórios finais vindos de terminais assentavam o Dispatch no ato da entrega, fazendo com que a mensagem ficasse sem requisição de grupo associada e permanecesse não lida.
46. **Falha de envio a agentes remotos não instalados localmente em ambientes pareados (`#46235`):**
    - Quando um coordenador despachava tarefas ou mensagens para um agente específico não instalado na máquina local, o envio falhava com erro de agente ausente em vez de rotear o comando para o computador pareado que possui o agente registrado.
47. **Confinamento de grupos de bots a um único computador local (`#46196`):**
    - Grupos de bots (*bot groups*) não suportavam membros heterogêneos distribuídos entre diferentes hosts, impedindo a colaboração entre bots executando no computador local e em servidores pareados.
48. **Extravio de resultados de workers locais para threads incorretas (`#46086`):**
    - Em sessões multithread, os resultados de um worker local eram entregues à thread ativa no momento em vez de retornarem especificamente para a thread cujo turno disparou a execução original.
49. **Silêncio de falha quando o resumo (*brief*) de um worker não era submetido (`#46155`):**
    - Quando a submissão do brief de tarefa de um worker falhava antes do início do processamento, o coordenador ficava aguardando indefinidamente sem receber aviso de que o brief não foi entregue.
50. **Omissão da resposta de agentes gerenciados a requisições de pares na sala de grupo (`#46117`):**
    - Quando um agente gerenciado respondia à solicitação de um par dentro de um grupo de bots, a resposta ficava restrita ao contexto privado do par e não era projetada na sala do grupo (*group room*), quebrando a visibilidade coletiva da tripulação.
51. **Sobrecarga de $O(N^2)$ na ordenação e consulta em tempo de execução de bots (`#46139`):**
    - Varreduras de catálogo e ordenação de bots executavam buscas quadráticas repetidas a cada ciclo de renderização e dispatch, gerando engasgos de interface em workspaces com dezenas de bots configurados.
52. **Perda de rascunhos de editor ao permitir exclusão de bot com arquivos não salvos (`#46207`):**
    - A ação de exclusão de bots não validava a existência de buffers de editor abertos e não salvos em seu workspace/home, apagando diretórios e causando perda irreversível de código em rascunho.
53. **Reescrita destrutiva integral de `MEMORY.md` em bots corrompendo regras do usuário e segredos (`#46360`):**
    - A rotina de organização de memória de bots (*Tidy-up*) tentava regerar o arquivo `MEMORY.md` inteiro a partir de texto gerado pelo modelo, causando falhas catastróficas em arquivos extensos, perda de diretivas do operador, remoção indevida de regras e vazamento de segredos.
54. **Agente ocioso reconectado sem atualização visual de tela quando mensagens estão retidas na mailbox (`#46286`):**
    - Ao reconectar um agente ocioso cuja caixa postal mantinha mensagens retidas durante execução anterior, a UI não emitia evento de repaint, deixando a tela congelada sem refletir o estado de entrega.
55. **Milhares de consultas individuais no SQLite por atualização para ler identidades de workers de side-chats (`#46120`):**
    - Classificar os chats laterais de um bot e construir a base de conversas disparava buscas individuais de terminal e registros de worker chat por chat, gerando milhares de leituras SQLite síncronas na thread principal a cada refresh.
56. **Contenção no banco por buscas irrestritas em notificações do Slack e links de sessão sem índice (`#46140`):**
    - A ausência de índice em links de conversação de sessão e a busca de respostas do Slack sem filtros prévios geravam contenção de locks no SQLite e lentidão nas notificações de bots.
57. **Fragmentação de flags de envio estruturado na CLI da orquestração sem agrupamento atômico em JSON payload (`#46372`, `#46355`, `#46356`, `#46339`):**
    - Disparos via CLI que combinavam múltiplas flags de comando estruturado enviavam parâmetros dispersos para o daemon, corrompendo argumentos de payload, deixando chats estruturados temporários órfãos e impedindo a configuração de tiers de contexto em `worker-start`.
58. **Varredura completa e custosa de todas as mensagens para ler a caixa postal de um Run (`#46477`):**
    - O comando `inbox` ou a verificação de correio de um Run executava varreduras lineares em toda a tabela de mensagens em vez de utilizar o índice específico de Run, gerando contenção de I/O em bancos com histórico volumoso.
59. **Identificação incorreta do coordenador no preâmbulo de workers ao inspecionar tarefas (`#46402`, resolve `#33634`):**
    - `dispatch-show --preamble` derivava a linha do coordenador a partir do remetente (`from`) de quem inspecionava a tarefa. Quando um worker inspecionava sua própria atribuição, a mensagem informava incorretamente que o worker era o seu próprio coordenador.
60. **Poluição de `MEMORY.md` com status de PRs e tarefas e falta de diário estruturado para itens concluídos (`#46412`, `#46397`, `#46450`):**
    - Bots acumulavam linhas voláteis de tarefas e links de PRs diretamente em `MEMORY.md`, inflando o contexto de inicialização e dificultando a recuperação de lições duradouras quando itens eram encerrados.
61. **Perda de autoria e falta de vinculação entre perguntas e workers iniciados (`#46287`):**
    - Perguntas de agentes (`agent-questions`) não gravavam quem efetivamente as assumiu (`taker`), gerando ambiguidade na entrega de respostas. Além disso, `worker-start` não vinculava explicitamente a tarefa à pergunta que o worker deveria responder.
62. **Truncamento de mensagens recentes e salto de páginas em `worker-read` (`#46446`):**
    - Quando um transcript de worker atingia o orçamento de resposta de 512 KiB na primeira página, o backend descartava as mensagens mais novas em vez das mais antigas, e o cursor avançava para o fim do arquivo, impossibilitando a leitura das mensagens truncadas.
63. **Workers em terminal com processo encerrado reportados indefinidamente como vivos (`#46448`):**
    - Se o agente em execução num terminal sofresse crash, fosse morto ou encerrasse retornando ao shell, o terminal PTY permanecia aberto. O coordenador nunca era notificado da saída do agente e o despacho permanecia aberto indefinidamente até o reboot do aplicativo.
64. **Desconexão transacional entre respostas/notices de perguntas e entrega de correio (`#46273`):**
    - O registro de respostas a perguntas e notificações de queda comitavam separadamente do correio produzido. Falhas ou crashes entre as etapas geravam respostas órfãs sem entrega ou notices perdidas.
65. **Interrupção arbitrária após 6 repasses de turnos em salas de grupos de bots (`#46517`):**
    - Conversas encadeadas em salas de grupos de bots eram forçadas a pausar após 6 hand-offs sucessivos e turnos disparados por correio de colegas não despertavam os membros mencionados via `@`.
66. **Vazamento de instruções confidenciais (`SOUL.md`/`MEMORY.md`) por permissões permissivas em arquivos de contexto (`#46602`, STA-16956):**
    - Ao mesclar instruções permanentes de bots em arquivos existentes (`QWEN.md`, `.hermes.md`, `GEMINI.md`, etc.), o modo original `0644` era preservado, expondo instruções do operador no workspace.
67. **Divergência de finalização em workers que atingem prontidão com atraso (`#46793`):**
    - Quando um `worker-start` demorava além da janela síncrona e atingia o estado pronto tardiamente, o runtime não finalizava a inicialização com as mesmas garantias de binding e vinculação de mailbox concedidas a inicializações no prazo, gerando tarefas em limbo.
68. **Trabalhadores e perguntas travados indefinidamente quando o coordenador para sem responder (`#46562`):**
    - Se um coordenador lia a pergunta de um worker (`worker ask`) e parava ou encerrava sem responder nem despachar worker `--for`, a chamada `ask --wait` permanecia bloqueada indefinidamente. O mesmo ocorria quando o chat coordenador do Run era substituído por `/new` ou excluído.
69. **Perguntas de agentes sem retorno quando o tomador (`taker`) para sem responder (`#46541`):**
    - Após assumir uma pergunta (`agent-question`), se o tomador parasse ou sofresse crash sem submeter a resposta, o perguntador ficava aguardando para sempre, pois a decisão de abandono dependia exclusivamente do encerramento geral do turno.
70. **Silêncio perpétuo em perguntas trocadas com computadores pareados quando o destinatário ou Run não coordena (`#46571`):**
    - Perguntas enviadas para ou originadas de servidores pareados ficavam retidas em caixas postais sem aviso de cancelamento caso o nó remoto perdesse a conexão, sofresse reset ou o Run não tivesse coordenador ativo localmente.
71. **Ausência de aviso de retenção (delivery hold) ao despachar mensagens com `send --on` para servidores pareados (`#46955`, resolve `#46944`):**
    - Ao utilizar `orca orchestration send --on <event>` com destino a instâncias ou servidores pareados, quando uma entrega era retida aguardando a ocorrência do gatilho ou confirmação de rota, o recibo de comando emitido pela CLI e logs omitiam a indicação de retenção ativa (*delivery hold*), dificultando o diagnóstico de mensagens pendentes em trânsito cross-host.
72. **Impossibilidade de agentes em servidores pareados enviarem mensagens e perguntas para agentes locais (`#46842`, `#46826`, `#46797`, `#46757`):**
    - A mensageria federada de orquestração funcionava apenas em sentido unidirecional ou restrito. Agentes rodando em servidores pareados não podiam disparar asks ou enviar correio para agentes neste computador com cartões de aprovação visual e introduções `@mention`, limitando a cooperação em clusters distribuídos.
73. **Extravio de correio de workers liquidados ao não rotear para a thread conectora de origem (`#47072`):**
    - Quando um worker encerrava e liquidava sua execução (*settled worker*), o correio residual emitido era roteado de forma genérica no pull loop em vez de ser devolvido diretamente à thread do conector que o havia iniciado, resultando em respostas perdidas para conectores síncronos.
74. **Perda permanente de workers em terminais após reboot ou crash do daemon de terminal (`#46643`):**
    - Se a máquina reiniciava ou o terminal daemon sofria crash, workers que executavam tarefas de orquestração em terminais eram considerados irrecuperáveis, mesmo com a opção *Resume work on restart* habilitada, deixando tarefas incompletas e forçando reexecução manual.
75. **Erro de "worker não encontrado" ao tentar abrir worker ainda em inicialização (`#47048`):**
    - Ao tentar inspecionar ou focar em um worker que ainda estava no processo inicial de arranque (*still-starting worker*), a rotina de localização de parte falhava com erro de destinatário inexistente em vez de utilizar o handle reservado e abrir a interface correspondente.
76. **Perguntas de workers bloqueadas indefinidamente ao fechar terminal ou pane de coordenador (`#47135`):**
    - Quando o terminal ou pane de um coordenador era fechado ou esvaziado, a desvinculação do Run ativo não era propagada prontamente, fazendo com que perguntas abertas de workers aguardassem indefinidamente por um leitor inexistente.
77. **Ausência de visibilidade e notificação em esperas longas de tarefas em background de workers (`#47081`):**
    - Quando um worker executava uma tarefa prolongada em segundo plano, a árvore de execução não exibia o estado de espera ativo e o coordenador não recebia nenhum alerta após períodos estendidos de bloqueio.
78. **Acúmulo de terminais e abas de setup abertas após encerramento ou liberação de workers (`#47370`, `#47371`):**
    - Terminais de configuração, abas de startup ou novos terminais criados dinamicamente por um worker durante a execução de ferramentas não eram desalocados no encerramento ou em `worker-release`, acumulando terminais órfãos no painel.
79. **Reversão para terminais crus de workers disparados a partir de chats persistentes ou servidores pareados (`#47364`, `#47363`):**
    - Sub-workers iniciados a partir de chats persistentes de agentes ou despachados para servidores pareados (`--on`) perdiam a linhagem de chat, iniciando como abas de terminal genéricas sem o formato conversacional.
80. **Retenção perene de relatórios de conclusão `worker_done` em despachos de follow-up (`#47469`, resolve `#47440`):**
    - Despachos do tipo *follow-up* constituíam um novo registro de Dispatch sem amarração direta à operação original do worker, fazendo com que seu `worker_done` ficasse retido indefinidamente sem chegar à requisição da sala atendida.
81. **Janela excessiva de 60 minutos para alertar coordenador sobre workers travados em background (`#47355`):**
    - O prazo de 60 minutos estabelecido no PR `#47081` para emitir alerta único ao coordenador era excessivamente longo para fluxos interativos de orquestração, atrasando intervenções quando processos entravam em deadlock.
82. **Ausência de contrato explícito de ciclo de vida e teardown de workers distribuídos (`#47562`):**
    - A orquestração não formalizava a distinção crítica entre workers assentados (*settled* - desfecho de tarefa), encerrados (*ended* - sessão dormente) e destruídos (*destroyed* - término comprovado de processo), nem critérios claros de colocação em hosts (`--environment`, `--repo`, validação de `setupState: ready`) e regras de recuperação entre `lost` e `exited`.
83. **Polling periódico de saída de agentes em terminais ociosos consumindo CPU e atrasando detecção (`#46045`):**
    - Terminais monitoravam o encerramento de processos em primeiro plano via timers periódicos de polling (a cada 200–500ms). Isso gerava consumo desnecessário de CPU em máquinas com dezenas de abas abertas e atrasava a percepção de conclusões ou saídas silenciosas de agentes até o próximo tick do timer.
84. **Omissão da causa real de término de workers e confusão entre interrupção solicitada e perda de host (`#47543`):**
    - Quando um worker encerrava por queda do host remoto ou perda de conexão SSH, o sistema reportava apenas saída genérica com código `-1` ("stop was requested but never confirmed"), mascarando a indisponibilidade de infraestrutura sob a aparência de cancelamento do usuário.
85. **Descarte de relatórios de workers ao interromper ou fechar salas de grupos (`#47503`):**
    - Relatórios e entregas parciais emitidos por workers após um comando Stop ou no momento da remoção de uma sala de grupo eram sumariamente descartados no banco de dados relacional, e os chats dos membros perdiam a vinculação de nomenclatura da sala de origem.
86. **Encerramento forçado de chats e perda de trabalho em voo ao reiniciar ou atualizar o app (`#47828`, `#47819`, `#47783`, resolve `#46100`):**
    - Fechar ou atualizar o aplicativo finalizava todos os processos de agentes de chat ativos (Codex, Claude e agentes ACP como Gemini, Copilot, Goose, Grok) e marcava os turnos em voo como cortados, forçando o usuário a reiniciar conversas com processos limpos e perdendo comandos em execução, servidores MCP e aprovações em aberto.
87. **Recusa opaca de inicialização de workers ao atingir a capacidade de terminais do host (`#47536`):**
    - Quando o daemon atingia o limite configurado de terminais do host, novas tentativas de `worker-start` falhavam com erro genérico sem detalhar a contagem de terminais em uso (`N of M`), a causa `terminal_host_cap` ou instruções para liberar instâncias concluídas.
88. **Workers de inicialização lenta classificados erroneamente como não observados (`#47575`):**
    - Se um worker levasse alguns segundos para responder ao handshake de inicialização, a árvore de orquestração o rotulava como `unobserved` em vez de identificá-lo em fase de arranque (`starting`), induzindo o coordenador a abortos prematuros.
89. **Turno de sessão travado aberto com 0% de CPU após resposta 503 do provedor (`#47817`):**
    - Quando a API de um modelo retornava erro HTTP 503 temporário, a sessão ficava travada em aberto sem consumo de CPU, ignorando o botão Stop da interface gráfica e chamadas de cancelamento via CLI.
90. **Comunicação opaca quando workers entram em silêncio prolongado (`#47947`, commit `06f0ca1a8bd`):**
    - Quando um worker em execução para de emitir mensagens ou heartbeats, o orquestrador passa a reportar explicitamente o que é comprovado no sistema (se o processo continua vivo, PID ativo ou socket de controle em espera) em vez de permanecer em silêncio indeterminado.
91. **Persistência sub-segundo de turnos de painel para continuidade de correio pós-crash (`#47887`, commit `b5b84ae3d27`):**
    - Grava alterações de estado de turnos de cada painel em até 1 segundo, assegurando que um crash ou relaunch não interrompa nem perca mensagens de correio ociosas destinadas ao agente.
92. **Injeção de caracteres de correio no shell após encerramento do OpenCode (`#47877`, commit `ab59c53f6ad`):**
    - Quando o OpenCode saía inesperadamente do ar, o handler de orquestração continuava digitando dados de mensagens na entrada PTY do shell que assumia o terminal; o commit `#47877` interrompe a digitação imediatamente ao detectar a saída do processo do agente.
93. **Execução de queries SQL da work store em thread de banco dedicada de bots (`#47554`, commit `2467e89de8c`):**
    - Transfere as operações SQL da loja de trabalho de bots para a thread worker dedicada de bots, eliminando contenções de I/O na main thread.
94. **Registro de workers iniciados a partir de chats in-app sob a conversa de origem (`#47548`, commit `b7c38c4f684`):**
    - Garante que trabalhadores iniciados a partir de qualquer chat interno do aplicativo fiquem duravelmente registrados e associados àquele chat de origem no histórico.
95. **Classificação incorreta de agente com worker próprio ativo como Waiting (`#47818`, commit `9a9290d4697`):**
    - Quando um agente disparava e executava seu próprio worker, seu status na interface caía indevidamente para `Waiting`; agora permanece claramente como `In progress`.
96. **Preservação de contexto de handoff e contenção de fan-out de workers (`#47973`):**
    - Retém o contexto integral durante passagens de tarefa (*handoff*) entre agentes e impõe limites ao número de sub-workers disparados em cascata (*worker fan-out*).
97. **Transferência de custódia ao reabrir chat de worker retido (`#47914`):**
    - Ao reabrir uma conversa de worker retido, a custódia do canal de mensagens e eventos é transferida atomicamente para o novo leitor ativo.
98. **Paginação histórica reversa com `--cursor` em `orca agent read` (`#47953`):**
    - Introduz o parâmetro `--cursor` no comando CLI para permitir navegação histórica paginada de trás para frente em transcripts volumosos.
99. **Falso diagnóstico de worker travado quando o transcript continua avançando (`#48011`, commit `5467349715b`):**
    - O orquestrador reportava workers como travados após chamadas de ferramentas mesmo quando a escrita no transcript continuava progredindo.
100. **Bloqueio de comandos de leitura definidos nas regras do bot pelo Look around (`#48411`, commit `99385200a80`):**
    - A checagem de inspeção ambiental Look around impedia a execução de comandos somente leitura customizados configurados para o bot.
101. **Item de trabalho não relido após recusa de resposta a uma pergunta substituída (`#48387`, commit `af1293c8156`):**
    - Ao recusar resposta a uma pergunta que foi reformulada ou substituída, o orquestrador mantinha o item desatualizado na memória do coordenador.
102. **Controle de presença de bots em threads do Slack (`#47428`, commit `4aecba8ccf6`):**
    - Falta de comando nativo para instruir o bot a sair da thread até nova menção `@` explícita.
103. **Ausência de `--wait-for-reply` e `--timeout` em `orca agent send` (`#48435`, Issue `#48434`):**
    - O envio via CLI não permitia esperar de forma síncrona pelo encerramento do turno com retorno formatado em JSON.
104. **Silêncio visual em conversas de grupo com coordenador bloqueado (`#48444`):**
    - Chats com múltiplos agentes não sinalizavam na interface quando o coordenador estava pausado aguardando entrada humana.
105. **Fechamento precoce de chat em workers de chat quando o workspace adormece (`#48562`):**
    - Quando um workspace era colocado em repouso/adormecido (*asleep*), os chat workers tinham a aba e o processo do chat encerrados sumariamente em vez de pausar e reter o estado dormente do workspace, destruindo o histórico ativo do worker.
106. **Instabilidade no arranque de workers estruturados aguardando término de setup (`#48202`):**
    - Disparar workers em workspaces em fase de inicialização concorrente causava corridas de setup, falhando o handshake inicial de orquestração se o lock do workspace demorasse a ser adquirido.
107. **Subagente interrompido pelo Codex retido em memória sem descarte (`#48518`):**
    - Quando o Codex cancelava ou interrompia um subagente em execução, a referência ao subagente permanecia ativa na tabela de tarefas em andamento, impedindo que o coordenador identificasse o descarte.
108. **Falha na liberação limpa de workers de terminal prematuramente encerrados (`#42264`):**
    - Se o terminal PTY do worker caísse abruptamente, chamadas subsequentes de liberação bloqueavam no lock de terminal; o upstream aperfeiçoou o descarte incondicional.
109. **Falhas assentadas de workers retidas permanentemente no Home Chat dock (`#48427`, Issues `#48594`, `#48593`, `#48592`, `#48614`):**
    - Notificações de falha de workers liquidados ficavam presas na barra inferior do Home Chat sem botão de limpeza, acumulando poluição visual após intervenção do desenvolvedor.

## O que o upstream implementa

- **Chat workers adormecem o workspace em vez de fechar a aba de chat (`#48562`):**
  - Altera a rotina de suspensão de workspaces para preservar abas e instâncias de chat workers, colocando o workspace em repouso sem abortar o canal de comunicação do agente.
- **Sincronização de workers estruturados sob wait-for-setup (`#48202`):**
  - Faz com que `worker-start` aguarde a prontidão de setup do workspace antes de disparar o handshake de orquestração, prevenindo timeouts espúrios de arranque.
- **Descarte imediato de subagentes cancelados ou interrompidos pelo Codex (`#48518`):**
  - Notifica o orquestrador no momento em que o Codex emite sinal de interrupção para um subagente, marcando o worker como retirado (*retired*) e liberando os recursos alocados.
- **Ação de Clear para falhas de workers assentados no dock do Home Chat (`#48427`, Issues `#48594`, `#48593`, `#48592`, `#48614`):**
  - Disponibiliza botão de descarte direto para limpar erros de workers concluídos retidos na barra inferior do Home Chat.
- **Sobrevivência de chats ativos a reinicializações e atualizações via terminal host (`#47828`, `#47819`, `#47828`, resolve `#46100`):**
  - No macOS e Linux, delega os processos de agentes de chat (Codex, Claude e agentes ACP) para execução sob o host de terminais daemon (`providerRelayKeep`);
  - Ao fechar o app, os processos continuam em execução em background em vez de serem abortados; na reabertura do aplicativo, o chat reconecta ao mesmo processo com replay ordenado de saídas, preservação de subprocessos e ferramentas, e restauração de pedidos de aprovação mantidos como prompts interativos normais.
- **Identificação tipada de capacidade de terminais e avisos preventivos em `worker-start` (`#47536`, commit `21aa900d9c0`):**
  - Implementa o erro tipado `TerminalHostCapError` com o detalhamento `(N of M terminals in use)` e orientações de liberação;
  - Exibe no recibo de `worker-start` avisos preventivos de capacidade assim que o uso de terminais atinge 80% (ou 90%) do teto do host.
- **Classificação precisa de workers lentos em inicialização como `starting` (`#47575`):**
  - Marca workers cujo agente demora para inicializar como `starting` na árvore de tarefas em vez do alarmista `unobserved`.
- **Formalização do contrato de teardown e posicionamento host-aware de workers (`#47562`):**
  - Documenta a descoberta de hosts e setups de projeto (`orca host list --json`, `orca project setups --environment local|<server-id> --json`) e regras estritas de prontidão (`setupState: ready`, `hostId: local`, `--repo id:<repoId>`);
  - Separa formalmente o ciclo de vida de término em três estados: assentado (*settled* - desfecho de tarefa), encerrado (*ended* - sessão dormente) e destruído (*destroyed* - processo finalizado comprovadamente no SO);
  - Define regras de recuperação e diferenciação entre `lost` (queda transitória de rede ou host) e `exited` (processo terminou);
  - Remove restrições desatualizadas em servidores pareados modernos com suporte a `orchestration.remote-owned-workers.v1`.
- **Detecção orientada a eventos do SO para término de agentes em terminais ociosos (`#46045`):**
  - Substitui o polling periódico em timer por notificações diretas de saída de processo entregues pelo sistema operacional;
  - Desativa verificações periódicas em terminais ociosos, poupando CPU e acordando leituras apenas quando eventos reais do SO ocorrerem;
  - Mantém leitura ativa com backoff exponencial se houver perguntas interativas aguardando liquidação.
- **Identificação precisa de término de workers e diagnóstico de perda de host (`#47543`):**
  - Propaga a razão real de encerramento registrada em `worker_dock_facts.reason` para a linha de status do worker;
  - Introduz a causa `host_lost` para saídas com código `-1` originadas de desconexão da sessão ou queda do host do terminal, distinguindo falhas de infraestrutura de interrupções manuais voluntárias.
- **Persistência de relatórios de workers e nomenclatura de salas em grupos de bots (`#47503`):**
  - Garante que relatórios parciais ou finais pós-Stop sobrevivam à interrupção ou remoção de salas de grupos via transações de escrita seguras no banco de dados;
  - Nomeia chats de membros diretamente com o nome da respectiva sala gravada no momento da escrita.

- **Fechamento automático de terminais de setup, abas e terminais criados com o worker (`#47370`, `#47371`):**
  - Vincula terminais de setup, abas de inicialização e terminais abertos pelo worker diretamente ao handle do worker, encerrando-os atomicamente em `worker-stop` e `worker-release` (preservando o terminal de setup apenas caso a inicialização falhe para auditoria).
- **Propagação de linhagem de chat para sub-workers e servidores pareados (`#47364`, `#47363`):**
  - Carrega a linhagem de conversa estruturada (`orchestration.chat-lineage.v1`) para trabalhadores criados a partir de um persistent agent home e repassa a flag para servidores conectados, garantindo que workers e sub-workers iniciem sempre como chats.
- **Roteamento de relatório de follow-up para a requisição de grupo atendida (`#47469`, resolve `#47440`):**
  - Resolve a operação do worker a partir do Dispatch vinculado mais recente na linhagem de acompanhamento, entregando o relatório `worker_done` sem retenção em limbo.
- **Redução do limiar de alerta de worker travado em background para 20 minutos (`#47355`):**
  - Reduz de 60 minutos para 20 minutos o tempo de espera contínua em tarefa de segundo plano necessário para acionar a notificação ao coordenador.
- **Desassociação imediata de Runs e aviso de sem leitor ao fechar terminal do coordenador (`#47135`):**
  - Desvincula (*unbinds*) Runs ativos imediatamente quando o terminal do coordenador encerra ou tem sua pane fechada/esvaziada, notificando perguntas abertas com aviso explícito de *no reader* para liberar workers bloqueados.
- **Indicador de espera na árvore e notificação após 60 minutos de espera em background (`#47081`):**
  - Reflete o status de espera na árvore de tarefas quando um worker aguarda sua própria tarefa em segundo plano e dispara notificação única ao coordenador caso a espera contínua atinja 60 minutos.
- **Federação bidirecional completa de mensageria com servidores pareados (`#46842`, `#46826`, `#46797`, `#46757`):**
  - Permite que agentes em servidores pareados enviem mensagens e perguntas para agentes deste computador com flag `--on-client`, renderização de cartões `NativeChatClientAskRequestCard`, aprovações de introdução seguras por impressão digital de chave de host e resposta direta via mobile e desktop.
- **Roteamento direto de correio de worker liquidado para o conector de origem (`#47072`):**
  - Assegura que mensagens emitidas no encerramento de um worker sejam entregues com precisão à thread do conector responsável pela inicialização.
- **Retomada resiliente de workers de terminal pós-reinício (*Resume work on restart*) (`#46643`):**
  - Implementa recuperação e re-vinculação atômica de workers de terminal interrompidos por crash ou reboot sob a política de reinício, oferecendo ofertas de retomada contextualizadas e prevenindo perda de estado.
- **Resolução de handle em workers em processo de inicialização (`#47048`):**
  - Utiliza o identificador alocado provisoriamente para localizar e abrir a visão de workers ainda em fase de startup sem disparar falso erro de inexistência.
- **Indicação explícita de delivery holds em recibos de `send --on` para servidores pareados (`#46955`, resolve `#46944`):**
  - Informa no recibo do despacho e na inspeção de status quando a entrega de uma mensagem inter-servidores está em retenção programada aguardando o evento disparador, evitando falsos positivos de perda de mensagens.
- **Finalização idêntica para inicializações tardias de workers (`#46793`):**
  - Trata o término da inicialização de um worker que atinge prontidão tardia exatamente da mesma forma que uma inicialização no prazo, garantindo consistência em bindings e registros de despacho.
- **Notificação e liberação imediata de workers quando o coordenador para (`#46562`):**
  - Envia aviso de `unanswered` ao worker no momento em que seu coordenador para sem responder nem deixar worker em execução, destravando chamadas `ask --wait`;
  - Aposenta Runs e desassocia coordenadores em uma única escrita quando chats são substituídos (`/new`, troca de agente) ou deletados, notificando perguntas abertas imediatamente.
- **Notificação de abandono de perguntas quando o tomador encerra sem responder (`#46541`):**
  - Avalia dinamicamente o estado de execução do tomador (`taker`) e dispara notificação de abandono ao autor da pergunta assim que comprovado que o tomador parou e nenhum worker `--for` está ativo.
- **Resolução determinística de perguntas entre computadores pareados (`#46571`):**
  - Informa os agentes imediatamente caso uma pergunta direcionada a computador pareado não possa ser entregue ou caso chegue a um Run que perdeu seu coordenador local, eliminando correios órfãos.
- **Registro de assunção de perguntas (`taker`) e vinculação `--for` no arranque de workers (`#46287`):**
  - Grava atomicamente quem assumiu a pergunta do agente no ato do aceite ou leitura (`markAsRead` / `markAsReadAndDelivered`), indexando na tabela de perguntas emparelhadas;
  - Introduz a flag `worker-start --for <messageId>` para vincular deterministicamente o worker à pergunta que ele foi disparado para responder.
- **Paginação de `worker-read` ordenada pelas mensagens mais recentes (`#46446`):**
  - Ordena a primeira página de leitura de trás para frente (`newest-first`) limitando ao orçamento de 512 KiB e ajusta o cursor de retomada para continuar exatamente a partir da última mensagem servida sem perder histórico recente.
- **Detecção de término de agente em terminal com PTY aberto e notificação ao coordenador (`#46448`):**
  - Monitora o encerramento do processo do agente no terminal via probes no hook server, identificando processos ausentes ou shells órfãos e liquidando o status do worker para alertar o coordenador sem depender do fechamento do terminal.
- **Commit atômico de respostas e avisos com correio em savepoint único (`#46273`):**
  - Unifica a gravação da resposta a perguntas, notificações de descarte e envio do e-mail resultante dentro da mesma transação/savepoint no SQLite, impedindo inconsistências pós-crash.
- **Eliminação do teto de 6 repasses e continuidade por `@mentions` em salas de grupos (`#46517`):**
  - Remove o limite arbitrário de 6 hand-offs em salas de grupos de bots, permitindo que turnos disparados por correio continuem acordando membros citados via `@mention` e suprimindo disparos duplicados para membros já notificados.
- **Permissões seguras `0600` em arquivos de contexto de diretório de bots (`#46602`, STA-16956):**
  - Força o modo de arquivo estrito `0600` ao criar ou atualizar arquivos de instruções embutidas de bots (`QWEN.md`, `.hermes.md`, `GEMINI.md`, etc.), prevenindo a exposição pública de diretivas no sistema de arquivos.
- **Otimização de leitura da árvore de chat de bots evitando re-leituras de workers concluídos (`#46478`):**
  - Interrompe a re-leitura contínua de workers já liquidados a cada atualização da árvore de conversas do bot, aliviando o tráfego do SQLite.
- **Leitura da caixa postal de Run através de índice dedicado (`#46477`):**
  - Otimiza a leitura da mailbox de um Run específico consultando diretamente pelo índice de Run em vez de varrer toda a tabela de mensagens da orquestração, mitigando contenção de I/O em bancos com histórico volumoso.
- **Identificação do coordenador gravado no preâmbulo de `dispatch-show` (`#46402`, resolve `#33634`):**
  - Ajusta a geração do preâmbulo (`dispatch-show --preamble`) para extrair e nomear o coordenador registrado na atribuição da tarefa em vez de usar o remetente da chamada de inspeção, garantindo que workers inspecionando suas próprias tarefas visualizem o coordenador correto.
- **Diário de itens concluídos e PRs em `memory/journal/YYYY-MM.md` (`#46412`, `#46397`, `#46450`):**
  - Implementa registro automático de tarefas e PRs finalizados no diário mensal de bots (`memory/journal/YYYY-MM.md`) em vez de manter essas linhas em `MEMORY.md`, mantendo a memória principal enxuta e retendo o histórico com timestamp e resumo estruturado.
- **Tidy-up atômico e seguro de memórias de bots com movimentação para diário (`#46360`):**
  - Substitui a reescrita destrutiva do `MEMORY.md` por operações atômicas verificadas linha a linha (`move`, `merge`, `retire`) calculadas sobre linhas numeradas e com hash;
  - Preserva integralmente regras ditadas pelo operador, proibições e linhas sem data, limitando a perda a no máximo 25% e arquivando cópias retiradas;
  - Move linhas de status datado (PRs, hashes, rodadas de revisão) palavra por palavra para `memory/journal/YYYY-MM.md` em transação única e reversível via History/Undo.
- **Repaint de interface para agentes ociosos reconectados com correio retido (`#46286`):**
  - Solicita ao agente reconectado uma re-renderização imediata de tela quando sua caixa de correio contiver mensagens retidas, mantendo a fidelidade da UI.
- **Resolução em lote de identidades de workers de bots via consultas indexadas (`#46120`):**
  - Consolida milhares de leituras individuais no SQLite em duas consultas indexadas em lote com subqueries de saída antecipada, ignorando chats remotos e reduzindo drasticamente o tempo na main thread.
- **Indexação de links de sessão e controle de buscas de respostas no Slack (`#46140`):**
  - Cria índice dedicado para links de conversação de sessão e condiciona buscas de respostas do Slack, prevenindo sobrecarga no banco.
- **Unificação de flags estruturadas de envio via CLI em payload JSON (`#46372`):**
  - Consolida flags estruturadas dispersas em um payload JSON íntegro para despachos confiáveis na orquestração.
- **Roteamento de envios para agentes residentes em computadores pareados (`#46235`):**
  - Direciona despachos e mensagens para o host pareado remoto correspondente quando o agente solicitado não estiver presente no host local.
- **Grupos de bots híbridos com membros de computadores pareados (`#46196`):**
  - Permite agrupar bots locais e remotos em um mesmo bot group com orquestração transparente de mensagens e tarefas.
- **Entrega determinística de resultados de workers locais à thread de origem (`#46086`):**
  - Assegura que o retorno de workers locais seja roteado estritamente para a thread de conversa que iniciou o turno de trabalho.
- **Notificação de brief não submetido ao coordenador (`#46155`):**
  - Emite aviso explícito ao coordenador informando caso a submissão do brief do worker encontre falha na entrega.
- **Visibilidade de respostas entre pares na sala do grupo de bots (`#46117`):**
  - Projeta a resposta de agentes gerenciados na sala do grupo quando a requisição partir de outro membro da equipe.
- **Otimização linear $O(N)$ em lookups e ordenação de bots (`#46139`):**
  - Elimina buscas quadráticas no catálogo e runtime de bots, tornando ordenações e despachos instantâneos.
- **Bloqueio de exclusão de bots com rascunhos de editor não salvos (`#46207`):**
  - Impede a exclusão de qualquer bot enquanto seu home contiver rascunhos pendentes de salvamento no editor.
- **Omissão do handle do terminal coordenador no preâmbulo de workers (`#45751`, refs `#14570`):**
  - Descreve o coordenador de terminal como receptor padrão de correios enviados sem destinatário explícito (`--to`), impedindo que workers copiem handles misturados em `--from` e garantindo aceitação de heartbeats e `worker_done`.
- **Controle de tamanho do ledger automático e APIs de reinicialização para pareamento (`#45507`):**
  - Aplica limite estrito em bytes no livro-razão automático descartando continuações antigas e preservando janelas de rate-limit, além de expor `restartLaunchSettled` e `restartResumableDismiss` para clientes pareados.
- **Preservação de nível em modelos Antigravity estruturados (`#45744`, refs `#45701`):**
  - Cria sessões de despacho com `optionsMode: 'replace-model-selection'` quando o modelo solicitado possuir sufixo de nível, impedindo que preferências de esforço do usuário sobreponham a especificação do despacho.
- **Retenção do crew host por 30s após saída do último ouvinte e tracing de rebuilds (`#45435`):**
  - Mantém o host de tripulação vivo por 30 segundos após a saída do último listener no Electron main, permitindo trocas de abas e reconexões instantâneas sem reconstrução custosa, registrando métricas de rebuild no trace.
- **Despertar de membros de grupos por relatórios finais via proveniência gravada (`#45819`):**
  - Resolve a identidade do worker a partir da proveniência gravada do remetente antes da liquidação do despacho, acordando imediatamente o membro do grupo solicitante.
- **Sonda de correio de coordenador legado por endereço via índice composto (`#45426`):**
  - Utiliza o índice composto `(run_id, to_address)` para sondar mensagens diretamente no SQLite, eliminando o join completo sobre todos os dispatches e acelerando a checagem de correio de coordenadores legados.
- **Retenção de correio de orquestração até o fim do turno para provedores com steering em fila (`#45370`):**
  - Adiciona retenção de mensagens de correio até a conclusão do turno ativo para provedores que especificam `steering: 'queue'`, impedindo que mensagens rotineiras de status cancelem turnos em andamento de agentes como o Antigravity.
- **Tokens de recuperação seguros desaspados no cmd do Windows (`#45462`):**
  - Remove aspas de tokens alfanuméricos seguros correspondentes a `[A-Za-z0-9_.-]+` em scripts de inicialização e recuperação no terminal Windows.
- **Envio de arquivos em mensagens de correio de itens gerenciados (`#45194`):**
  - Permite anexar arquivos locais e remotos em comunicações entre agentes gerenciados (`bot-item-mail-files.ts` e `peer-mail-files.ts`), cuidando do upload para staging de sessões em servidores pareados.
- **Nomeação durável de remetentes de workers pelo registro de Dispatch (`#44472`):**
  - Grava no banco a tarefa, agente e host do worker no exato instante em que o correio é emitido;
  - Exibe "Tarefa · Agente [Servidor]" em cartões de mensagem mesmo quando a aba do worker já foi fechada.
- **Suspensão de subscrição de crew em chats nativos durante repouso do painel (`#45290`):**
  - Compartilha o controle de suspensão do painel de tripulação com as abas de chat nativo, eliminando recálculos síncronos redundantes e travamentos de 32s.
- **Consulta otimizada de contextos de despacho por tarefa (`#45330`):**
  - Aplica filtro direto por tarefa em `dispatch_contexts`, acelerando a resolução de handles duráveis de coordenação.
- **Roteamento de aprovações de workers através do host proprietário do chat em servidores pareados (`#44919`):**
  - Encaminha pedidos e streams de aprovação de workers através do host proprietário do chat em conexões remotas;
  - Permite que janelas pareadas ou clientes conectados encerrem com segurança fluxos de aprovação e aceitem emparelhamentos como a pessoa operadora;
  - Rejeita códigos de pareamento de dispositivos móveis no comando CLI `environment add`.
- **Retenção durável da receita de lançamento de workers mesmo sob falhas de captura posterior (`#44590`, resolve `#43875`):**
  - Mantém a linha de receita original armazenada no banco em vez de sobrescrevê-la ou limpá-la caso uma captura de contexto subsequente falhe ou não consiga ler o processo finalizado;
  - Assegura que workers finalizados possam ser recriados ou receber mensagens subsequentes de follow-up com os parâmetros originais preservados.
- **Instrução formal de tipos de mail suportados para agentes e suporte sobre `--on` (`#44332`):**
  - Documenta e orienta no manifesto de skills e nas ferramentas de coordenação quais tipos de mensagem (`task_result`, `ask`, `reply`, `worker_done`, `status`) devem ser utilizados em cada cenário, inclusive em despachos remotos via `--on`;
  - Garante compatibilidade retroativa para que servidores mais antigos ainda aceitem o tipo `status` e aponta agentes para `orca-cli` na comunicação peer-to-peer.
- **Resposta a permissões de subagentes de workers pelo coordenador com hold de 2 minutos (`#44475`):**
  - Retém o prompt de permissão do subagente auxiliar (*helper agent*) quando o coordenador puder responder ou exibi-lo (aprovações de coordenador ativas ou coordenador de chat), localizando a chamada diretamente no transcript do helper (`<session>/subagents/agent-<id>.jsonl`);
  - Cria um cartão dedicado de aprovação com identificação de origem ("Allow Bash? · from the worker's general-purpose helper");
  - Caso não seja respondido no Studio em 2 minutos, encerra a espera de forma limpa e permite que o Claude exiba o diálogo no terminal do próprio worker.
- **Checkpoints do WAL do banco de orquestração fora da thread principal (`#44327`):**
  - Move os checkpoints do WAL do `orchestration.db` para uma thread dedicada durante todo o ciclo de vida do banco;
  - Executa checkpoints em lote apenas quando 1.000 frames estiverem pendentes e drena o residual em pausas de 100 ms, impedindo que escritas de status congelem a main thread.
- **Isolamento de escalações e decision gates recusados fora da mailbox (`#43016`):**
  - Assegura que solicitações de escalation ou decision_gate recusadas não sejam injetadas na caixa postal do destinatário, registrando o encerramento da decisão apenas nos metadados de governança da tarefa.
- **Expurgo de cópias resolvidas de chat e auto_vacuum incremental com botão de reclaim (`#42839`, resolve STA-15101):**
  - Converte cópias de chat de workers em referências leves (`{ chatRef: { sessionId, ... } }`) assim que o Run é concluído há mais de 24h, liberando até 99% do volume ocupado por outputs arquivados;
  - Cria novos bancos com `auto_vacuum = INCREMENTAL` e devolve páginas livres ao sistema operacional periodicamente;
  - Adiciona a seção *Settings › Agent orchestration › Orchestration storage* com medição de espaço e o botão **Reclaim space**, executando limpeza e `VACUUM` atômico durante reinicialização segura.
- **Roteamento doméstico para parada de workers federados remotos (`#42852`):**
  - Garante que eventos de encerramento (`stop` / `close`) de workers federados sejam roteados para o host criador original, finalizando adequadamente o processo remoto.
- **Suporte a `--run` em `orchestration inbox` (`#42747`, resolve `#42732`):**
  - Expõe a flag `--run <runId>` na CLI `orca orchestration inbox` e encaminha o filtro ao backend RPC, permitindo inspecionar apenas a caixa postal vinculada à execução ativa.
- **Contabilização de prompt aprovado como respondido durante ferramenta em execução (`#42708`):**
  - Marca prompts interativos como respondidos no ato da aprovação para que não reapareçam como pendentes durante a execução de ferramentas lentas.
- **Paginação de leituras de workers de chat e projeção estável de frota (`#42707`):**
  - Aplica paginação eficiente na recuperação de mensagens de workers antes de aplicar limites rígidos, mantendo a consistência da projeção agregada da frota de agentes.
- **Terminais coordenadores ocultos e compactação de payloads (`#42719`, `#42731`, `#42733`, `#42734`):**
  - Introduz modo de terminal coordenador sem aba dedicada no editor para orquestrações autônomas;
  - Descarta notificações urgentes para decisões recusadas por terceiros;
  - Reduz em mais de 70% o payload JSON de `worktree ps/list` omitindo campos redundantes e expõe o worktree e título nos recibos de `worker-start`.
- **Rejeição de relatórios vazios ou whitespace em `worker_done` (`#42535`, resolve `#42148`):**
  - Valida `--body` na CLI e parâmetros de envio no RPC para rejeitar corpos vazios em `worker_done`, retornando `invalid_argument` e mantendo a tarefa aberta para reenvio sem perda de relatórios.
- **Preservação de `run` e `coordinator_handle` na saída concisa `--json` (`#42338`, resolve `#42103`):**
  - Restaura o objeto `run` com `coordinator_handle` no JSON compacto retornado por `run-show`, `run-current` e `run-use`.
- **Liberação resiliente de workers com terminal fechado em `worker-release` (`#42264`, resolve `#19166`):**
  - Permite que o comando `worker-release` conclua a liberação com sucesso mesmo se o terminal PTY do worker já tiver saído ou sido destruído.
- **Exposição de `creatorOrcaSessionId` e `assigneeOrcaSessionId` no JSON de workers (`#42284`, resolve `#42230`):**
  - Expõe os IDs de sessão de chat vinculados ao criador e ao destinatário do worker na resposta `--full`.
- **Consulta otimizada do pull-loop sem tabela temporária (`#42122`, resolve STA-15102):**
  - Reformula a checagem de pull em uma única consulta SQL compacta, unificando estados de link e verificação de home conversation sem construir temporary sets no SQLite.
- **Reutilização imediata de workers mid-turn via entrega em mailbox (`#42114`):**
  - Permite que `worker-start --terminal` despache a tarefa subsequente diretamente na caixa de correio do agente ativo, dispensando a espera por `tui-idle` e prevenindo falsos timeouts de 60s em workers que monitoram processos pós-turno.
- **Resiliência e nomeação em falhas pré-binding de reuse-starts (`#42112`, `#42111`):**
  - Trata abortos antes do binding marcando a tarefa como nunca iniciada e preservando o identificador e nome do agente reutilizado nos registros.
- **Marcação atômica de pergunta como lida ao submeter resposta (`#41979`, resolve `#41975`):**
  - Executa `markAsRead([question.message_id])` dentro da mesma transação em `answerQuestion`, eliminando a necessidade de consultas `orchestration check` subsequentes para limpar mensagens já respondidas.
- **Ciclo de retenção e limpeza do banco `orchestration.db` (`#41757`, resolve `#41756`):**
  - Implementa rotina horária de limpeza (com execução inicial 1 minuto após o boot) que deleta Runs resolvidos e não tocados pelo período de retenção configurado.
- **Despertar automático de coordenadores em repouso (`#41746`):**
  - Acorda automaticamente o processo PTY e a sessão do agente coordenador quando novas mensagens entram em sua caixa postal.
- **Monitor de inatividade mid-turn de workers (`#41702`):**
  - Detecta ausência de progresso real por mais de 15 minutos e envia aviso discreto ao coordenador.
- **Comando CLI `orca text generate` e RPC `text.generate` (`#41729`, resolve `#41726`):**
  - Executa inferência one-shot rápida sem ferramentas em diretório temporário isolado.
- **Suporte a stdin e arquivo em `terminal send` (`#41754`, resolve `#40838`):**
  - Permite envio seguro de payloads longos sem expor argumentos em `ps`.
- **Expurgo paginado de Runs resolvidos sem travar a thread principal (`#43550`):**
  - Aposenta execuções antigas em lotes paginados no SQLite, evitando que a limpeza de histórico volumoso cause stalls no loop de eventos principal.
- **Reconciliação de reservas estruturadas órfãs em `worker-release` (`#43467`, resolve `#43039`):**
  - Libera automaticamente reservas de início estruturado pendentes quando o worker é dispensado prematuramente.
- **Liberação de terminais de workers após saída comprovada (`#43953`):**
  - Executa a liberação do terminal associado em `settleWorkerStop` imediatamente após comprovar a saída do processo PTY, eliminando o vazamento de recursos de terminal de workers encerrados.
- **Preservação de receitas de launch na retomada de workers (`#43875`):**
  - Mantém duravelmente o registro de comando, argumentos e variáveis de ambiente originais mesmo após o término do worker, permitindo que retomadas via `orchestration send` restaurem a receita com fidelidade.
- **Exposição de `providerSessionId` de workers de orquestração (`#43957`):**
  - Expõe o identificador nativo de sessão do provedor (`providerSessionId`, ex.: sessão Claude Code) nos metadados retornados pela CLI e RPC de orquestração.
- **Deep links `orca://` para abas de chat e mensagens entregues (`#43874`):**
  - Implementa suporte ao esquema de protocolo `orca://chat/<workspace>/<sessionId>` e `orca://orchestration/message/<messageId>` para navegação direta externa.

## O que fazer

- Finalizar inicializações de workers que atingem prontidão tardiamente com as mesmas garantias de binding (`#46793`).
- Notificar workers e liberar `ask --wait` imediatamente quando o coordenador parar ou for substituído/deletado (`#46562`).
- Disparar aviso de abandono de pergunta de agente no momento em que o tomador parar sem responder (`#46541`).
- Resolver e avisar imediatamente falhas de entrega em perguntas emparelhadas com servidores remotos (`#46571`).
- Registrar o identificador de quem assumiu cada pergunta de agente (`taker`) e aceitar `worker-start --for <messageId>` (`#46287`).
- Paginar `worker-read` newest-first dentro do teto de 512 KiB sem descartar mensagens recentes em logs longos (`#46446`).
- Notificar o coordenador e liquidar o worker quando o agente em terminal encerrar com o shell PTY mantido aberto (`#46448`).
- Comitar atomicamente respostas e avisos de perguntas junto com seu correio em savepoint único do SQLite (`#46273`).
- Eliminar o teto de 6 repasses e continuar hand-offs em salas de grupos através de `@mentions` sem mensagens duplicadas (`#46517`).
- Garantir permissões estritas `0600` em arquivos de instruções embutidas e contexto de diretórios de bots (`#46602`, STA-16956).
- Evitar re-leitura contínua de workers concluídos na atualização da árvore de chats de bots (`#46478`).
- Consultar caixa postal de um Run via índice dedicado para evitar varredura sequencial em tabelas de correio volumosas (`#46477`).
- Exibir o coordenador gravado no despacho em `dispatch-show --preamble` ao inspecionar tarefas por workers (`#46402`, resolve `#33634`).
- Registrar automaticamente tarefas encerradas e PRs mesclados no diário mensal `memory/journal/YYYY-MM.md` dos bots (`#46412`, `#46397`, `#46450`).
- Adotar rotina segura de Tidy-up de memórias de bots com operações atômicas (move, merge, retire) e diário histórico (`#46360`).
- Forçar repaint de agente ocioso reconectado com mensagens retidas na mailbox (`#46286`).
- Otimizar leituras de identidades de workers de bots com queries em lote indexadas no SQLite (`#46120`).
- Indexar links de conversas de sessões para mitigar contenção de banco em notificações (`#46140`).
- Consolidar flags estruturadas de envio via CLI em payload JSON único (`#46372`).
- Rotear despachos para computadores pareados quando o agente solicitado não estiver presente no host local (`#46235`).
- Suportar grupos de bots híbridos contendo membros distribuídos entre hosts locais e servidores pareados (`#46196`).
- Entregar resultados de workers locais determinística e estritamente à thread de conversa que disparou o turno (`#46086`).
- Notificar o coordenador imediatamente caso a submissão do brief de tarefa do worker falhe (`#46155`).
- Projetar respostas entre pares na sala do grupo de bots para visibilidade compartilhada da equipe (`#46117`).
- Otimizar para $O(N)$ buscas e ordenação no catálogo e runtime de bots (`#46139`).
- Bloquear a exclusão de bots enquanto seu workspace contiver rascunhos de editor não salvos (`#46207`).
- Omitir o handle do terminal coordenador no preâmbulo de workers para evitar mistura de identificadores em `--from` (`#45751`, refs `#14570`).
- Limitar o tamanho em bytes do ledger automático de orquestração sob crash-cuts e expor APIs de descarte e reinicialização para pareamento (`#45507`).
- Preservar o nível de esforço de raciocínio de modelos Antigravity estruturados criando despachos com `optionsMode: 'replace-model-selection'` (`#45744`, refs `#45701`).
- Reter o crew host na memória do processo principal por 30 segundos após a saída de ouvintes para evitar congelamentos em trocas de abas (`#45435`).
- Despertar membros de grupos em chats de bots através da proveniência gravada do remetente de relatórios finais de workers (`#45819`).
- Sondar correio de coordenadores legados diretamente por endereço no SQLite via índice composto `(run_id, to_address)` (`#45426`).
- Reter mensagens de orquestração até o fim do turno para provedores com `steering: 'queue'`, evitando o cancelamento indevido de turnos ativos (`#45370`).
- Omitir aspas em tokens seguros de recuperação de linha de comando no Windows (`#45462`).
- Suportar envio de arquivos e anexos em mensagens de correio de itens gerenciados localmente ou em hosts remotos (`#45194`).
- Reter o nome e metadados de remetentes de workers gravando o Dispatch no momento do envio da mensagem (`#44472`).
- Suspender a subscrição síncrona `orchestration.crewSubscribe` nos chats nativos enquanto o painel de tripulação estiver em repouso (`#45290`).
- Otimizar consultas de coordenadores legados filtrando `dispatch_contexts` por tarefa (`#45330`).
- Rotear pedidos de autorização de workers através do host proprietário do chat em servidores pareados e clientes remotos (`#44919`).
- Responder a pedidos de permissão de subagentes de workers diretamente pela interface do coordenador com retenção de 2 minutos (`#44475`).
- Executar checkpoints de WAL do banco de orquestração em thread dedicada fora da main thread (`#44327`).
- Desalocar recursos de terminal de workers imediatamente após comprovação de saída em `settleWorkerStop` (`#43953`).
- Reter a receita de lançamento original de workers mesmo quando capturas posteriores falharem (`#44590`, resolve `#43875`).
- Padronizar e documentar a especificação dos tipos de mail suportados em comunicações inter-agentes e flags `--on` (`#44332`).
- Expor `providerSessionId` nos metadados de workers de orquestração (`#43957`).
- Suportar recriação condicional de terminal substituto para Run ativo (`#43925`).
- Adotar deep links `orca://` para foco em abas de chat e mensagens de orquestração (`#43874`).
- Aceitar e liquidar `worker_done` emitidos por workers em host WSL (`#43869`).
- Implementar expurgo paginado de Runs resolvidos no banco de orquestração para eliminar stalls na thread principal (`#43550`).
- Aceitar e liquidar corretamente mensagens `worker_done` oriundas de workers rodando em servidores conectados (`#43618`).
- Reconciliar e liberar reservas estruturadas de inicialização órfãs ao executar `worker-release` (`#43467`, resolve `#43039`).
- Manter escalações e decision gates recusados fora da caixa postal do destinatário (`#43016`).
- Adotar o expurgo de cópias resolvidas de chat e `auto_vacuum = INCREMENTAL` no `orchestration.db` com ação 'Reclaim space' (`#42839`, resolve STA-15101).
- Rotear ordens de parada de workers federados remotos ao host de origem (`#42852`).
- Adicionar o parâmetro `--run` em `brza orchestration inbox` para filtrar caixas postais por execução (`#42747`, resolve `#42732`).
- Marcar prompts de terminal aprovados como respondidos durante a execução da ferramenta (`#42708`).
- Adotar a paginação de leituras de workers de chat e projeção estável de frota (`#42707`).
- Suportar terminais coordenadores ocultos em execuções de orquestração (`#42719`) e compactar saídas de worktree (`#42733`, `#42734`).
- Rejeitar relatórios vazios em `worker_done` para impedir conclusão prematura sem sumário (`#42535`, resolve `#42148`).
- Adotar a preservação do nó `run` e `coordinator_handle` no output conciso `--json` (`#42338`, resolve `#42103`).
- Suportar a liberação resiliente em `worker-release` de workers cujo terminal PTY já encerrou (`#42264`, resolve `#19166`).
- Expor `creatorOrcaSessionId` e `assigneeOrcaSessionId` nos metadados completos de workers (`#42284`, resolve `#42230`).
- Adotar a consulta compacta do pull-loop sem temporary sets no SQLite (`#42122`, resolve STA-15102).
- Permitir reutilização de workers mid-turn via correio direto sem esperar `tui-idle` (`#42114`).
- Adotar tratamento consistente e preservação de nome em falhas pré-binding de reuse-starts (`#42112`, `#42111`).
- Marcar perguntas de workers automaticamente como lidas no ato da resposta (`#41979`, resolve `#41975`).
- Adotar o ciclo de retenção e limpeza periódica do banco `orchestration.db` (`#41757`, resolve `#41756`).
- Implementar o despertar automático de coordenadores em repouso diante de mensagens de workers (`#41746`).
- Adotar o monitor de inatividade mid-turn de workers com notificação ao coordenador (`#41702`).
- Incorporar o comando CLI `brza text generate` e RPC `text.generate` (`#41729`, resolve `#41726`) para geração rápida de respostas sem ferramentas.
- Suportar leitura por stdin (`--text -`) e arquivo (`--text-file`) no comando de envio para terminais (`#41754`, resolve `#40838`).
- Exibir indicação de retenção ativa (delivery hold) em recibos e consultas de `send --on` cross-host (`#46955`, resolve `#46944`).
- Habilitar mensageria bidirecional federada permitindo que agentes em servidores pareados enviem perguntas e mensagens via `--on-client` com aprovação segura (`#46842`, `#46826`, `#46797`, `#46757`).
- Rotear o correio emitido por workers liquidados diretamente para a thread conectora de origem (`#47072`).
- Retomar e re-vincular atomicamente workers de terminais interrompidos por reinício sob a política Resume work on restart (`#46643`).
- Utilizar o handle reservado de workers em fase de startup para permitir abertura da interface sem falso erro de inexistência (`#47048`).
- Desvincular Runs e notificar workers com erro no-reader quando a pane do terminal coordenador for fechada (`#47135`).
- Exibir estado de espera na árvore e alertar o coordenador após 20 minutos de espera em background (`#47355`, reduzindo os 60 min do `#47081`).
- Encerrar automaticamente terminais de setup, abas de startup e terminais secundários criados pelo worker em sua finalização (`#47370`, `#47371`).
- Propagar a linhagem estruturada de chat para workers filhos e servidores pareados conectados (`#47364`, `#47363`).
- Resolver requisições de follow-up garantindo entrega de relatórios `worker_done` à sala de chat de origem (`#47469`, resolve `#47440`).
- Implementar o contrato formal de posicionamento e teardown de workers separando desfechos settled, ended e destroyed (`#47562`).
- Substituir o polling de processos em terminais por notificações orientadas a eventos do sistema operacional (`#46045`).
- Identificar e exibir o motivo exato de encerramento de workers diferenciando cancelamento de perda de host (`host_lost`) (`#47543`).
- Preservar relatórios parciais e finais de workers e nomenclatura de chats em salas de grupos mesmo após comando Stop (`#47503`).
- Implementar sobrevivência de chats ativos a reinicializações e atualizações através do terminal host (`providerRelayKeep`) para Codex, Claude e ACP (`#47828`, `#47819`, `#47783`, resolve `#46100`).
- Emitir erro tipado `TerminalHostCapError` e avisos preventivos a partir de 80%/90% de ocupação do cap de terminais do host em `worker-start` (`#47536`, commit `21aa900d9c0`).
- Classificar workers com arranque lento como `starting` em vez de `unobserved` na árvore de tarefas (`#47575`).
- Reportar o estado conhecido de processos e conexões quando workers entrarem em silêncio prolongado (`#47947`, commit `06f0ca1a8bd`).
- Salvar atualizações de turno de painéis em até 1 segundo para manter o correio ocioso fluindo através de crashes e reinícios (`#47887`, commit `b5b84ae3d27`).
- Suprimir a injeção contínua de caracteres de mensagens no shell após a finalização do OpenCode (`#47877`, commit `ab59c53f6ad`).
- Executar operações SQL da loja de trabalho no worker SQLite dedicado de bots (`#47554`, commit `2467e89de8c`).
- Associar workers iniciados a partir de chats embutidos diretamente à conversa de origem no histórico (`#47548`, commit `b7c38c4f684`).
- Refletir o status `In progress` para agentes que possuem workers próprios ativos (`#47818`, commit `9a9290d4697`).
- Preservar o contexto de handoff e limitar o fan-out de workers em cascata (`#47973`).
- Transferir atomicamente a custódia de mensagens ao reabrir chats de workers retidos (`#47914`).
- Suportar paginação histórica reversa com `--cursor` em `orca agent read` (`#47953`).
- Implementar filtro por `--worktree` e documentação de campos JSON em `orchestration inbox` (`#47868`).
- Continuar postando turnos mantidos no Pi enquanto workers filhos assíncronos estiverem rodando (`#48146`).
- Bifurcar (fork) conversas do Claude a partir de transcrições que não possuem `apiBlockIndex` (`#48153`, commit `31274053e71`).
- Aguardar aquisição de lock em vez do início de setup em cenários de arranque lento de orquestração (`#48178`, commit `d69b00a84a4`).
- Preservar a atribuição de autoria humana de commits em ações executadas por workers (`#48080`).
- Registrar o identificador de requisição de origem (`origin`) em itens transversais entre bots (`#48086`).
- Recuperar execuções de automações de falhas temporárias de inferência de modelo (`#48087`).
- Permitir que rotinas de Look around e manutenção de memória sigam fusos horários configurados (`#48019`).
- Expor API de plugins para leitura, eventos de itens e respostas como proprietário de itens de bots (`#48010`).
- Exibir mensagens aguardando de outros agentes no final do chat em vez de acumulá-las na fila própria (`#45882`, commit `28a6043afa3`).
- Entregar mensagens retidas de colegas a um agente compartilhado quando o computador voltar online (`#48274`).
- Garantir que mensagens enviadas por colegas em agentes compartilhados postem e ajam com a identidade deles, nunca do proprietário (`#48263`).
- Manter lista de compartilhamento no host e responder a entregas de agentes compartilhados (`#48255`, `#48256`).
- Exibir o ator coordenador corrente de runs pertencentes ao chat em `run-show` (`#48312`).
- Permitir que integrações acordem o chat próprio do bot quando self-mail for recusado (`#48295`).
- Prevenir roteamento indevido de respostas de orquestração cross-server para terminais flutuantes em vez do Home Chat do bot (`#48290`).
- Expor API de host de plugin para ler itens entre bots e atuar sobre eles com permissão delegada (`#48262`).
- Reportar workers quietos como travados após chamada de ferramenta apenas se o transcript comprovar ausência de atividade (`#48011`, commit `5467349715b`).
- Habilitar a execução de comandos somente leitura declarados nas regras do bot durante Look around (`#48411`, commit `99385200a80`).
- Re-ler o item de trabalho após recusa de resposta a uma pergunta substituída (`#48387`, commit `af1293c8156`).
- Suportar comando de saída de bots em threads do Slack com retorno sob menção `@` (`#47428`, commit `4aecba8ccf6`).
- Adicionar flags `--wait-for-reply`, `--timeout` e saída JSON no comando `orca agent send` (`#48435`, Issue `#48434`).
- Permitir reconexão do dock coordinator a workers pausados sem perda de canal de eventos (`#48427`).
- Reter o contexto do repositório pai quando bots criam worktrees filhos (`#48390`).
- Sinalizar visualmente em chats de grupo quando o coordenador estiver aguardando input humano (`#48444`).
- Adotar o adormecimento de workspaces preservando instâncias de chat workers sem encerrar o chat (`#48562`).
- Sincronizar arranque de workers estruturados aguardando o término de setup do workspace (`#48202`).
- Descartar imediatamente subagentes interrompidos ou cancelados pelo Codex (`#48518`).
- Assegurar a liberação incondicional de workers em `worker-release` quando o terminal PTY já encerrou (`#42264`).
- Permitir limpeza de falhas de workers assentados no dock do Home Chat com ação de Clear (`#48427`, Issues `#48594`, `#48593`, `#48592`, `#48614`).
- Interpretar no dock de orquestração a parada deliberada de workers como parada normal e intencional (`#48738`, `#48684`).
- Preservar o script de setup de workspace em execução ao interromper um worker manualmente (`#48683`).
- Não exibir workers parados pelo coordenador como falhas inesperadas no histórico de orquestração (`#48664`).
- Identificar workers assentados cujo terminal foi transferido para tarefa seguinte como 'handed on' (`#48686`).
- Otimizar leitura de terminais transferidos em cadeia de handoff para leitura única por cadeia (`#48782`).
- Centralizar o botão Stop da linha de worker no alinhamento do título (`#48794`).
- Permitir paginação reversa no comando `orca agent read` com o parâmetro `--cursor` (`#47953`).
- Preservar histórico retido e transcrições ao reabrir workers finalizados em worktrees filhos reutilizados (`#48841`).
- Respeitar padrões de workspace para workers criados por bots (Chat vs Terminal, aprovação vs acesso total) (`#48840`).
- Aceitar relatórios de workers mesmo após reinício do runtime com reemissão do identificador/handle (`#41041`).
- Aninhar visualmente workers de hosts remotos sob o respectivo coordenador no painel de status (`#48888`).
- Descartar payloads de cursor excedentes e limitar subagentes interrompidos no Codex (`#48871`).
- Permitir configuração para ocultar avisos e notices de orquestração da visualização principal (`#48916`).
- Garantir que workers Antigravity acordem prontamente ao receber resposta de orquestração via ask (`#49035`).
- Disponibilizar comando CLI para alterar modelo e nível de esforço de chats em execução (`#49043`).
- Impedir desaparecimento de chats de bots ativos na barra lateral após reinicialização do aplicativo (`#49038`).
- Manter rascunhos e sessões OMP em execução quando o usuário aplicar intervenção/steering no chat (`#49263`).
- Entregar mensagens de correio de orquestração no meio do turno via `_session/steering` do OMP (`#49262`, Issue `#49125`).
- Rejeitar `worker_done` referenciando Dispatch já encerrado enquanto houver um Dispatch mais recente ativo (`#49221`, resolve Issue `#49220`).
- Validar a instalação e autenticação do agente no host remoto antes de provisionar a worktree do worker (`#49238`).
- Reportar o coordenador atual na saída do comando de orquestração `orca orchestration run-show` (`#49160`).
- Reenviar automaticamente relatórios de conclusão de workers (`worker completion reports`) que sofreram timeout (`#48943`).
- Rejeitar comandos de inicialização `worker-start --item --on` antes do roteamento para servidores pareados (`#49127`).
- Configurar política de retenção para expurgar automaticamente sessões de agentes de workers concluídos (`#49218`).
- Permitir despertar workers ou bots em contexto limpo com novo resumo e ponteiro para a transcrição anterior (`#49254`).
- Desbloquear a resolução e descarte de Dispatches com falha após retentativa bem-sucedida (`#49183`).
- Marcar automaticamente sessões de workers como lidas no momento em que o coordenador recebe `worker_done` (`#44184`).
- Implementar watchdog para escalonar e abortar workers que ficarem silenciosos ou esgotarem cota (`#46425`).
- Notificar e despertar workers do Claude quando jobs iniciados em background no shell terminarem (`#46406`).
- Inicializar workers de checkpoint de orquestração de forma preguiçosa (lazy spawn) e desativá-los na ociosidade (`#49445`).
- Inicializar workers de checkpoint de journal sob demanda com aposentadoria automática pós-inatividade (`#49441`).
- Desduplicar paradas de ociosidade pós-resposta e tornar passiva a presença em background-wait (`#49458`).
- Sondar estritamente o agente do worker ao validar sua instalação em hosts de orquestração (`#49350`).
- Cessar contabilização de worker com falha assim que sua tarefa for concluída com sucesso por retry (`#49300`).
- Esclarecer para workers que status 'failed' significa apenas impossibilidade de conclusão (`#49312`).
- Apresentar na bandeja de workers o motivo da falha ao passar o cursor sobre linhas com erro (`#49280`).
- Permitir que agentes em suspensão (slept) pareçam ociosos e acordem no local ao receberem mensagens (`#44113`).
- Preservar o relatório exato submetido com `--report-path` através de rotinas de limpeza de worktree (`#49308`).
- Registrar agente efetivo, modelo e esforço de raciocínio em dispatches de acompanhamento (`#49307`).
- Retomar automaticamente workers Claude quando limites de cota forem redefinidos (`#49274`).
- Permitir que coordenadores marquem perguntas como "waiting on a human" sem forçar decisão autônoma pelo worker (`#49273`).
- Retirar automaticamente solicitações "Needs-you" quando PR, worker ou prazo vinculado forem liquidados (`#49271`).
- Mensageria atômica para dispatches ativos sem forçar retomada desnecessária de workers (`#43668`).
- Reportar configurações efetivas de inicialização nos preâmbulos de workers despachados (`#49636`, Issue `#19980`).
- Agrupar workers iniciados em servidor pareado sob a conversa proprietária que os disparou (`#49624`).
- Omitir rotinas de despertar para agentes em suspensão (sleeping) diante de entradas recusadas ou hosts não relacionados (`#49413`).
- Permitir que coordenadores escolham explicitamente entre enfileirar (`queue`) ou intervir (`steer`) ao enviar mensagem a um Dispatch ativo (`#49623`).
- Disponibilizar comando de CLI para colocar um chat de agente em hibernação/sleep (`#49609`).
- Limpar adequadamente painéis de sessões finalizadas em servidores pareados evitando travamento de conclusões (`#49606`).
- Liberar Dispatches de coordenadores órfãos após reinicialização do runtime em servidores macOS pareados (`#49602`).
- Evitar que o fallback de perguntas sem resposta crie uma nova Task após a conclusão do Dispatch requisitante (`#49564`).
- Ajustar reconciliador de perguntas quando o destinatário for um terminal de caixa de correio sem agente anexado (`#49550`).
- Suportar modo orquestrador nativo para o Antigravity com execução direta em auto e plan (`#41962`).
