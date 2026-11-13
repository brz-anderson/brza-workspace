---
status: open
description: Os PRs #41979, #41757, #41746, #41702, #41729 trazem baixa automática de perguntas respondidas na orquestração, retenção de Runs e despertar de coordenadores.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#41979`](https://github.com/stablyai/orca/pull/41979) (resolve Issue [`#41975`](https://github.com/stablyai/orca/issues/41975)),
[`stablyai/orca#41757`](https://github.com/stablyai/orca/pull/41757) (resolve Issue [`#41756`](https://github.com/stablyai/orca/issues/41756)),
[`stablyai/orca#41746`](https://github.com/stablyai/orca/pull/41746),
[`stablyai/orca#41702`](https://github.com/stablyai/orca/pull/41702),
[`stablyai/orca#41729`](https://github.com/stablyai/orca/pull/41729) (resolve Issue [`#41726`](https://github.com/stablyai/orca/issues/41726)) e
[`stablyai/orca#41754`](https://github.com/stablyai/orca/pull/41754) (resolve Issue [`#40838`](https://github.com/stablyai/orca/issues/40838)).

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

## O que o upstream implementa

1. **Expurgo periódico e retenção configurável no banco de orquestração (`#41757`, resolve `#41756`):**
   - Implementa uma rotina horária de limpeza (com execução inicial 1 minuto após o boot) que deleta Runs resolvidos e não tocados pelo período de `orchestrationRunRetentionHours` (padrão 24 horas; 0 desativa a retenção);
   - Executa a deleção em transações isoladas `BEGIN IMMEDIATE` com yield para o event loop, preservando cuidadosamente Runs com Tasks pendentes, despachos ativos, workers vivos, perguntas abertas ou coordenadores ainda ativos.
2. **Despertar automático de coordenadores em repouso ao receber correio (`#41746`):**
   - Acorda automaticamente o processo PTY e a sessão do agente coordenador quando novas mensagens (como `worker_done`, respostas de perguntas ou resultados de tarefas) entram em sua caixa de correio (`wakeSleptCoordinatorForMail`);
   - Garante que a entrega de mensagens ocorra imediatamente sem depender de foco manual do usuário no workspace.
3. **Detecção e notificação de inatividade prolongada de workers mid-turn (`#41702`):**
   - Varre a cada minuto os workers em execução e detecta ausência de progresso real (hooks, status reports ou streaming) por mais de 15 minutos (ou 60 minutos se uma ferramenta longa estiver rodando);
   - Envia uma mensagem informativa discreta ao coordenador avisando que o worker está quieto há X minutos e qual ferramenta está ativa, sem interromper ou matar prematuramente o processo do worker.
4. **Comando CLI `orca text generate` e RPC `text.generate` para respostas sem ferramentas (`#41729`, resolve `#41726`):**
   - Introduz o método RPC `text.generate` e o comando CLI `orca text generate --agent <id> (--prompt <text> | --prompt-file <path|->) [--model] [--effort] [--timeout-ms] [--json]`;
   - Executa a inferência em um diretório temporário isolado descartável, desativando ferramentas (`--tools ""`) e hooks pesados, reutilizando a autenticação local do agente selecionado para fornecer respostas rápidas e limpas.
5. **Suporte a entrada por stdin e arquivo em `terminal send` (`#41754`, resolve `#40838`):**
   - Estende o comando com as opções `terminal send --text -` (leitura via stdin até EOF) e `--text-file <path>` (leitura de arquivo UTF-8);
   - Preserva quebras de linha e caracteres de controle, mantendo prompts confidenciais fora da lista de processos do SO.
6. **Marcação atômica de pergunta como lida ao submeter resposta (`#41979`, resolve `#41975`):**
   - Executa `markAsRead([question.message_id])` dentro da mesma transação em `answerQuestion`, eliminando a necessidade de consultas `orchestration check` subsequentes para limpar mensagens já respondidas.

## O que fazer

- Marcar perguntas de workers automaticamente como lidas no ato da resposta (`#41979`, resolve `#41975`).
- Adotar o ciclo de retenção e limpeza periódica do banco `orchestration.db` (`#41757`, resolve `#41756`).
- Implementar o despertar automático de coordenadores em repouso diante de mensagens de workers (`#41746`).
- Adotar o monitor de inatividade mid-turn de workers com notificação ao coordenador (`#41702`).
- Incorporar o comando CLI `brza text generate` e RPC `text.generate` (`#41729`, resolve `#41726`) para geração rápida de respostas sem ferramentas.
- Suportar leitura por stdin (`--text -`) e arquivo (`--text-file`) no comando de envio para terminais (`#41754`, resolve `#40838`).
