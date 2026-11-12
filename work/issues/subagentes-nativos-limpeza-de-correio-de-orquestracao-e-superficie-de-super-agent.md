---
status: open
description: Os PRs #39804, #39802, #39599, #39564, #39501 trazem liveness honesto de workers, recusa de reply a worker_done e retenção de worker-list.
scope:
  - brza-studio
  - brza-workflow
priority: medium
opened: 2026-11-03
tags:
  - chat
  - tooling
---

# Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent

<!-- pln-014-despacho -->
> **Despacho (PLN-014/R1.1):** classe `ausente` · casa `studio`
> Merge no upstream não muda `status`. PLN-014/R1, 2026-11-12.

Rastreado dos PRs abertos no upstream [`stablyai/orca#39804`](https://github.com/stablyai/orca/pull/39804),
[`stablyai/orca#39802`](https://github.com/stablyai/orca/pull/39802),
[`stablyai/orca#39599`](https://github.com/stablyai/orca/pull/39599) (resolve Issue [`#39598`](https://github.com/stablyai/orca/issues/39598)),
[`stablyai/orca#39564`](https://github.com/stablyai/orca/pull/39564),
[`stablyai/orca#39501`](https://github.com/stablyai/orca/pull/39501) (resolve Issue [`#39499`](https://github.com/stablyai/orca/issues/39499)),
[`stablyai/orca#39283`](https://github.com/stablyai/orca/pull/39283),
[`stablyai/orca#38901`](https://github.com/stablyai/orca/pull/38901),
[`stablyai/orca#38899`](https://github.com/stablyai/orca/pull/38899),
[`stablyai/orca#38814`](https://github.com/stablyai/orca/pull/38814),
[`stablyai/orca#38713`](https://github.com/stablyai/orca/pull/38713),
[`stablyai/orca#38768`](https://github.com/stablyai/orca/pull/38768),
[`stablyai/orca#38464`](https://github.com/stablyai/orca/pull/38464),
[`stablyai/orca#38461`](https://github.com/stablyai/orca/pull/38461),
[`stablyai/orca#38460`](https://github.com/stablyai/orca/pull/38460) (Issue [`#38446`](https://github.com/stablyai/orca/issues/38446)),
[`stablyai/orca#38494`](https://github.com/stablyai/orca/pull/38494),
além da issue [`stablyai/orca#39631`](https://github.com/stablyai/orca/issues/39631),
[`stablyai/orca#38529`](https://github.com/stablyai/orca/pull/38529) (Issue [`#38539`](https://github.com/stablyai/orca/issues/38539)),
[`stablyai/orca#38445`](https://github.com/stablyai/orca/pull/38445),
[`stablyai/orca#38416`](https://github.com/stablyai/orca/pull/38416),
[`stablyai/orca#38451`](https://github.com/stablyai/orca/pull/38451),
[`stablyai/orca#38348`](https://github.com/stablyai/orca/pull/38348),
[`stablyai/orca#38379`](https://github.com/stablyai/orca/pull/38379),
[`stablyai/orca#38376`](https://github.com/stablyai/orca/pull/38376),
[`stablyai/orca#38373`](https://github.com/stablyai/orca/pull/38373),
[`stablyai/orca#38239`](https://github.com/stablyai/orca/pull/38239),
[`stablyai/orca#38236`](https://github.com/stablyai/orca/pull/38236),
[`stablyai/orca#38259`](https://github.com/stablyai/orca/pull/38259),
[`stablyai/orca#38174`](https://github.com/stablyai/orca/pull/38174),
[`stablyai/orca#38207`](https://github.com/stablyai/orca/pull/38207),
[`stablyai/orca#38159`](https://github.com/stablyai/orca/pull/38159),
[`stablyai/orca#38222`](https://github.com/stablyai/orca/pull/38222) (Issue [`#38172`](https://github.com/stablyai/orca/issues/38172)),
[`stablyai/orca#37757`](https://github.com/stablyai/orca/pull/37757),
[`stablyai/orca#38077`](https://github.com/stablyai/orca/pull/38077),
[`stablyai/orca#38079`](https://github.com/stablyai/orca/pull/38079),
[`stablyai/orca#37744`](https://github.com/stablyai/orca/pull/37744),
[`stablyai/orca#34895`](https://github.com/stablyai/orca/pull/34895),
[`stablyai/orca#37918`](https://github.com/stablyai/orca/pull/37918),
[`stablyai/orca#37966`](https://github.com/stablyai/orca/pull/37966),
[`stablyai/orca#37974 (MERGED no upstream; não está no fork)`](https://github.com/stablyai/orca/pull/37974),
[`stablyai/orca#37574`](https://github.com/stablyai/orca/pull/37574),
[`stablyai/orca#33403`](https://github.com/stablyai/orca/pull/33403),
[`stablyai/orca#21333`](https://github.com/stablyai/orca/pull/21333),
[`stablyai/orca#37703 (MERGED no upstream; não está no fork)`](https://github.com/stablyai/orca/pull/37703),
[`stablyai/orca#37868`](https://github.com/stablyai/orca/pull/37868),
[`stablyai/orca#37866`](https://github.com/stablyai/orca/pull/37866),
[`stablyai/orca#37891 (MERGED no upstream; não está no fork)`](https://github.com/stablyai/orca/pull/37891),
[`stablyai/orca#37850`](https://github.com/stablyai/orca/pull/37850) e
[`stablyai/orca#11279`](https://github.com/stablyai/orca/pull/11279), além das issues
[`stablyai/orca#39807`](https://github.com/stablyai/orca/issues/39807),
[`stablyai/orca#39694`](https://github.com/stablyai/orca/issues/39694),
[`stablyai/orca#39517`](https://github.com/stablyai/orca/issues/39517),
[`stablyai/orca#39499`](https://github.com/stablyai/orca/issues/39499),
[`stablyai/orca#39300`](https://github.com/stablyai/orca/issues/39300),
[`stablyai/orca#39263`](https://github.com/stablyai/orca/issues/39263),
[`stablyai/orca#39262`](https://github.com/stablyai/orca/issues/39262),
[`stablyai/orca#39042`](https://github.com/stablyai/orca/issues/39042),
[`stablyai/orca#38951`](https://github.com/stablyai/orca/issues/38951),
[`stablyai/orca#39021`](https://github.com/stablyai/orca/issues/39021),
[`stablyai/orca#38850`](https://github.com/stablyai/orca/issues/38850),
[`stablyai/orca#38720`](https://github.com/stablyai/orca/issues/38720),
[`stablyai/orca#38687`](https://github.com/stablyai/orca/issues/38687),
[`stablyai/orca#38386`](https://github.com/stablyai/orca/issues/38386),
[`stablyai/orca#38258`](https://github.com/stablyai/orca/issues/38258),
[`stablyai/orca#38210`](https://github.com/stablyai/orca/issues/38210),
[`stablyai/orca#38111`](https://github.com/stablyai/orca/issues/38111),
[`stablyai/orca#38123`](https://github.com/stablyai/orca/issues/38123),
[`stablyai/orca#38131`](https://github.com/stablyai/orca/issues/38131),
[`stablyai/orca#38015`](https://github.com/stablyai/orca/issues/38015),
[`stablyai/orca#38000`](https://github.com/stablyai/orca/issues/38000),
[`stablyai/orca#37741`](https://github.com/stablyai/orca/issues/37741),
[`stablyai/orca#37702`](https://github.com/stablyai/orca/issues/37702),
[`stablyai/orca#37693`](https://github.com/stablyai/orca/issues/37693),
[`stablyai/orca#37731`](https://github.com/stablyai/orca/issues/37731),
[`stablyai/orca#37867`](https://github.com/stablyai/orca/issues/37867),
[`stablyai/orca#37865`](https://github.com/stablyai/orca/issues/37865),
[`stablyai/orca#37849`](https://github.com/stablyai/orca/issues/37849),
[`stablyai/orca#37907`](https://github.com/stablyai/orca/issues/37907),
[`stablyai/orca#37683`](https://github.com/stablyai/orca/issues/37683),
[`stablyai/orca#37684`](https://github.com/stablyai/orca/issues/37684),
[`stablyai/orca#37407`](https://github.com/stablyai/orca/issues/37407),
[`stablyai/orca#37637`](https://github.com/stablyai/orca/issues/37637) e
[`stablyai/orca#19388`](https://github.com/stablyai/orca/issues/19388).

## Os pontos do upstream

1. **Prevenção de aborto acidental em turnos OMP ao entregar correio (`#39042`):**
   - Ao enviar mensagens de orquestração (`orca orchestration send`) para uma pane rodando OMP enquanto um steer já estava
     enfileirado, a tentativa de injeção de `Enter` no PTY podia acidentalmente interpretar como sinal de interrupção,
     abortando o turno ativo com "Interrupted by user". A entrega precisa aguardar a conclusão do turno ou usar a extensão OMP.
2. **Invasão de digitação de ponteiro de correio no terminal (`#38951`):**
   - Quando um agente coordenador Claude recebe mensagens de correio, o texto do aviso era digitado no meio do buffer
     que o operador estava editando no momento, enviando comandos truncados com `Enter`. Requer uso do canal dedicado `$.prompt.submit`.
3. **Identificação anônima de hooks do Codex como "Hook 1" a "Hook 9" (`#39021`):**
   - No diálogo de revisão de hooks (`/hooks`) do Codex, os 9 hooks instalados pelo app apareciam anonimamente porque faltava
     o campo descritivo `statusMessage` no `~/.codex/hooks.json`.
4. **Falha rápida de prontidão de worker Antigravity quando a CLI está deslogada (`#38901`):**
   - O PR `#38901` aborta imediatamente com erro explícito `Agent startup blocked: agent-sign-in-prompt`, mantendo a pane
     aberta para que o operador faça login e use `--retry-of <dispatch>`.
5. **Reparo automático de ganchos de status do Antigravity (`#38899`):**
   - O PR `#38899` faz a verificação contínua e permite restaurar os ganchos com `orca agent hooks on`.
6. **Travas determinísticas FIFO de recursos e quadro compartilhado de colaboração (`#38850`):**
   - Proposta de mecanismos transacionais em SQLite (`orca orchestration lock-acquire`, `lock-release`, `lock-list`) com
     concessão FIFO, renovação de leases com TTL e quadro de colaboração para coordenar subagentes concorrentes em DAGs sem race conditions.
7. **Modularização de donos de correio e transcrições de workers (`#38814`):**
   - Refatoração do banco de dados de orquestração, caixas de correio e federação por donos de recursos no runtime.
8. **Entrega de correio em terminais OMP via extensão em vez de digitação no PTY (`#38720`):**
   - Propõe entregar ponteiros de orquestração através da extensão instalada do OMP como canal limpo.
9. **Suporte a roles de modelo, seletores e effort em chats e workers OMP (`#38713`):**
   - Configura parâmetros de reasoning effort, papéis de modelo e seleção precisa em sessões e workers do OMP.
10. **Proteção de abas ativas em clientes pareados contra sleep automático (`#38768`):**
    - Garante que workspaces e agentes não entrem em modo sleep se um cliente móvel ou desktop pareado estiver visualizando
      ou digitando ativamente naquela aba.
11. **Continuação de worker finalizado mediante resposta do coordenador (`#38464`):**
    - Reativa workers terminados quando o coordenador envia follow-up antes da liberação do terminal.
12. **Herança da conta Claude do chamador para subagentes CLI (`#38461`):**
    - Garante que invocações de subagentes herdem automaticamente a conta e o `CLAUDE_CONFIG_DIR` do processo pai.
13. **Classificação explícita de decisões em `orchestration reply` (`#39263`):**
    - Introdução do parâmetro `--decision user|technical` no subcomando `orca orchestration reply`. Permite que agentes
      coordenadores classifiquem se a resposta a uma dúvida de worker exigiu decisão de produto/humana ou se tratava-se de
      orientação puramente técnica/arquitetural, gravando o metadado no registro de Run/Dispatch para auditoria e redução de
      perguntas evitáveis.
14. **Mitigação de perda silenciosa de mensagens de correio aceitas (`#39262`):**
    - Mensagens enviadas a workers remotos com retorno `accepted: true` podiam ser descartadas silenciosamente caso a
      desanexação de Dispatch ocorresse antes da persistência final na caixa de entrada do worker. Proposta para exigir
      confirmação durável de gravação em disco antes de retornar sucesso ao coordenador.
15. **Sobrecarga de CPU por polling fixo a cada segundo em federation relays com falha (`#39283`):**
    - Cada worker remoto ativo mantinha um `setInterval` rígido de 1 segundo para sincronização de correio com seu host.
      Em ambientes com dezenas de workers em servidores deletados ou inacessíveis, o aplicativo executava centenas de
      tentativas por segundo, relendo arquivos de registro até 727 vezes/s e consumindo de 40% a 110% de CPU contínua no processo principal;
    - O PR `#39283` substitui o timer fixo por backoff exponencial com teto de 1 minuto (2s, 4s, …, 60s) em falhas, resetando
      imediatamente para 1s sob novas mensagens ou ações explícitas do coordenador (reply, start, stop).
16. **Travamento de coordenadores por processos Codex terminados com PTY remanescente (`#39300`):**
    - Quando um processo nativo do Codex supervisionado finaliza sua execução (por saída, erro ou interrupção) mas o PTY
      alocado permanece conectado ao shell padrão, o coordenador não era notificado do término, ficando indefinidamente aguardando;
    - A issue `#39300` introduz o observador `observeSupervisedCodex`, detectando o fim do processo filho e disparando
      `reportWorkerTurnStop` com causa explícita.
17. **Papéis pré-configurados de workers para `orchestration worker-start` (`#39517`):**
    - Coordenadores precisam especificar `--agent`, `--model` e `--effort` a cada invocação de worker, gerando inconsistências
      e uso acidental de modelos inadequados para tarefas específicas (ex.: revisão vs. implementação rápida);
    - A issue `#39517` propõe papéis nomeados em Configurações (`--role <name>`, ex.: research, implementation, review)
      pré-validando a combinação de modelo e esforço no catálogo do host antes da criação da tarefa.
18. **Linhas obsoletas de "Done" retidas na barra lateral após término do agente (`#39501`, resolve `#39499`):**
    - A barra lateral de workspaces retinha a linha do agente no estado "Done" mesmo após o processo do agente ter saído
      completamente de volta para o prompt do shell, gerando poluição visual e falsos indicativos de sessões em execução;
    - O PR `#39501` introduz `retireConfirmedShellAgent` e a flag `suppressRetention` em `dropAgentStatus`, descartando a linha no renderer
      assim que o retorno ao shell for confirmado e impedindo que snapshots posteriores de retenção recriem a linha obsoleta.
19. **Exibição de native background workers no chat para agentes Pi (`#39564`):**
    - Agentes Pi que disparavam subprocessos de background workers não possuíam representação no chat nativo, tornando o trabalho
      secundário invisível ao usuário;
    - O PR `#39564` adiciona suporte a workers nativos em background na interface do chat com Pi (pacote `pi-subagents`),
      oferecendo indicador compacto/expandido, status assíncrono em tempo real e recuperação de IDs de workers através de recarregamentos
      do renderer sem poluir a lista de workspaces ou criar abas redundantes.
20. **Configuração de auto-release de workers em tempo de execução headless (`#39599`, resolve `#39598`):**
    - Em servidores headless (`orca serve`), workers consolidados eram automaticamente liberados após um tempo rígido de 2 minutos (`WORKER_TERMINAL_AUTO_RELEASE_GRACE_MS`),
      fechando terminais antes que serviços externos registrassem o desfecho;
    - O PR `#39599` adiciona suporte a variáveis de ambiente `ORCA_WORKER_AUTO_RELEASE=on|off` e `ORCA_WORKER_AUTO_RELEASE_GRACE_SECONDS=<n>`
      lidas pelo banco de terminais (`bindWorkerTerminalAutoRelease`), permitindo desligar a liberação automática ou estender a carência.
21. **Falha `run_home_unreachable` em `orchestration reply` para mensagens de status (`#39631`):**
    - Ao responder com `orchestration reply --id <msg>` a uma mensagem do tipo `status` a partir de um worker local, o comando falha
      incorretamente acusando `run_home_unreachable` e citando um Dispatch inexistente no banco local (`ctx_...`);
    - Ocorre porque a rota de resposta a mensagens que não são perguntas aciona indevidamente a verificação de Run remoto quando há
      registros remotos residuais.
22. **Sobrecarga crítica em `worker-list` por retenção indefinida de registros (`#39807`):**
    - Registros de workers finalizados nunca são purgados ou arquivados da tabela de workers (`worker-list`), acumulando um volume
      massivo de linhas ao longo do tempo. Como resultado, uma leitura completa da lista de workers passa a demorar até 35 minutos,
      degradando severamente a inicialização e a responsividade de orquestração;
    - É necessária uma estratégia de retenção/purgador periódico (TTL/tombstone pruning) para workers concluídos há mais de um intervalo configurado.
23. **Rejeição espúria `worker_identity_changed` ao finalizar workers reabertos (`#39694`):**
    - Quando um worker em chat que foi auto-liberado (*auto-released*) por inatividade é reaberto pelo usuário ou pelo coordenador,
      chamadas posteriores a `worker_done` são rejeitadas de forma intermitente com o erro `worker_identity_changed`;
    - Isso decorre de uma discrepância entre o token de identidade/sessão recriado na interface e o registro original retido no banco de orquestração.
24. **Falsos alertas de liveness 'unverifiable' em workers em modo chat (`#39804`):**
    - Ao listar workers de orquestração com `orca orchestration worker-list`, qualquer worker executando como chat nativo (Codex, Claude,
      OpenCode) recebia o status `liveness=unverifiable attention=unverifiable`, mesmo enquanto trabalhava ativamente em um comando.
      Isso ocorria porque a projeção da frota avaliava apenas linhas de gancho de terminal, que nunca são vinculadas a handles `structworker_`;
    - O PR `#39804` integra as observações estruturadas de sessão (`session-worker-liveness.ts`), permitindo que workers de chat relatem
      fielmente `liveness=live activity=working` ou `activity=idle`, restringindo `unverifiable` a falhas reais de contato com o host.
25. **Perda silenciosa de mensagens de `reply` a relatórios de workers concluídos (`#39802`):**
    - Sob relatórios `worker_done`, coordenadores visualizavam sugestões de resposta como `[Reply: orca orchestration reply --id …]`.
      No entanto, ao executar o comando, a mensagem era aceita com ID mas nunca lida pelo worker (que já havia encerrado o turno),
      sendo entregue horas depois a tarefas não relacionadas no mesmo terminal;
    - O PR `#39802` recusa formalmente `orchestration reply` em relatórios concluídos (`dispatch_inactive`, `effectsApplied: false`) e
      orienta explicitamente o uso de `orca orchestration send --to dispatch:<id>`, que inicia um follow-up rastreado no mesmo worker.

## O que fazer

- Integrar o reporte honesto de liveness e activity para workers em modo chat (`#39804`), eliminando alertas espúrios de `unverifiable`.
- Adotar a recusa de `orchestration reply` em relatórios de workers concluídos e sugerir `send --to dispatch:<id>` para follow-ups (`#39802`).
- Implementar política de expurgo periódico (*pruning*) para registros antigos de workers em `worker-list` (`#39807`).
- Corrigir a sincronização de identidade de workers auto-released e reabertos ao processar `worker_done` (`#39694`).
- Suportar as variáveis de ambiente de auto-release (`ORCA_WORKER_AUTO_RELEASE` e `ORCA_WORKER_AUTO_RELEASE_GRACE_SECONDS`)
  em daemons e servidores de background (`#39599`).
- Corrigir a validação de Run local em `orchestration reply` para mensagens de status (`#39631`).
- Integrar o suporte a native background workers no chat para agentes Pi (`#39564`), permitindo acompanhar subagentes em segundo plano.
- Bloquear a injeção cega de `Enter` em terminais OMP quando houver turnos em execução ou steers enfileirados (`#39042`).
- Adicionar `statusMessage` legíveis aos hooks do Codex (`#39021`) para clareza na auditoria de segurança.
- Incorporar a detecção imediata de bloqueio de autenticação do Antigravity em workers (`#38901`).
- Avaliar a introdução de locks FIFO e quadro de colaboração de recursos para o `brza-workflow` (`#38850`).
- Adotar a classificação de decisão `--decision user|technical` no subcomando de resposta de orquestração (`#39263`).
- Garantir a confirmação durável de entrega de correio a workers remotos (`#39262`).
- Adotar o backoff exponencial em federation relays com falha (`#39283`) para eliminar consumo excessivo de CPU.
- Implementar a detecção de término de processos Codex em PTYs abertos (`#39300`).
- Adotar papéis pré-configurados de workers (`--role`) na CLI de orquestração (`#39517`).
- Corrigir a limpeza de linhas "Done" de agentes na sidebar quando o terminal retornar ao shell (`#39501`, `#39499`).
