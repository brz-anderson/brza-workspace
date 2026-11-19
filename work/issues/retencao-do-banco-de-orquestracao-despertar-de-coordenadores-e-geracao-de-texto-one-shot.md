---
status: open
description: Os PRs #44590 e #44332 retêm receita de lançamento de workers em falha de captura e orientam tipos de mail explícitos sobre --on.
scope:
  - brza-studio
  - brza-workflow
  - brza-cli
priority: high
opened: 2026-11-13
tags:
  - tooling
  - infra
---

# Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot

Rastreado dos PRs abertos no upstream [`stablyai/orca#44590`](https://github.com/stablyai/orca/pull/44590) (resolve Issue [`#43875`](https://github.com/stablyai/orca/issues/43875)),
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

## O que o upstream implementa

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
