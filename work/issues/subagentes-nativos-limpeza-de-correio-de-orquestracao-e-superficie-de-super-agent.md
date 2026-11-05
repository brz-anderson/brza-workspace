---
status: open
description: Os PRs #38348, #38379, #38376, #38373, #38174 e #38239 tratam de workers aninhados (profundidade 4), wake de coordenador Claude, federação v4 de correio e isolamento de helpers.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#38348`](https://github.com/stablyai/orca/pull/38348),
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
[`stablyai/orca#37974`](https://github.com/stablyai/orca/pull/37974),
[`stablyai/orca#37574`](https://github.com/stablyai/orca/pull/37574),
[`stablyai/orca#33403`](https://github.com/stablyai/orca/pull/33403),
[`stablyai/orca#21333`](https://github.com/stablyai/orca/pull/21333),
[`stablyai/orca#37703`](https://github.com/stablyai/orca/pull/37703),
[`stablyai/orca#37868`](https://github.com/stablyai/orca/pull/37868),
[`stablyai/orca#37866`](https://github.com/stablyai/orca/pull/37866),
[`stablyai/orca#37891`](https://github.com/stablyai/orca/pull/37891),
[`stablyai/orca#37850`](https://github.com/stablyai/orca/pull/37850) e
[`stablyai/orca#11279`](https://github.com/stablyai/orca/pull/11279), além das issues
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

1. **Permissão padrão para workers criarem seus próprios workers até profundidade 4 (`#38348`):**
   - A configuração `Settings → Orchestration → Nested worker depth` é elevada de 1 para 4 por padrão;
   - Cadeias de delegação profunda (`Coordenador → Worker 1 → Worker 2 → Worker 3 → Worker 4`) agora são executadas
     naturalmente sem bloqueio imediato, com roteamento de `worker_done` diretamente para o worker pai imediato de cada nível
     e liberação automática de recursos finalizados sem deixar instâncias órfãs.
2. **Wake de coordenador Claude mesmo com subagentes ativos em background (`#38379`):**
   - Corrige cenário onde o aviso de `worker_done` ficava represado por até 5 minutos quando o app reiniciava enquanto
     um coordenador Claude possuía subagentes locais de background repintando a linha de progresso do terminal;
   - A entrega não exige mais tela quieta quando os próprios hooks do agente reportam um turno ao vivo sem diálogo pendente.
3. **Comunicação persistente de workers concluídos em hosts remotos pareados (`#38376`):**
   - Introduz o protocolo de federação v4 (`orchestration.federation-finished-worker-mail.v1`) permitindo que um worker
     remoto em um servidor pareado continue enviando mensagens (`send`) ou perguntas (`ask`) ao coordenador mesmo após
     emitir seu `worker_done`, com janela de tolerância de 2 minutos e backoff de sincronização.
4. **Interrupção de helpers auxiliares ao parar worker (`#38373`):**
   - Garante que todos os processos e auxiliares filhos iniciados por um worker sejam finalizados imediatamente no cancelamento
     ou parada do worker, impedindo vazamento de processos zumbis em segundo plano.
5. **Anexos nativos de imagem em tarefas de workers (`#38386`):**
   - Proposta para permitir anexação direta de imagens em payloads de dispatch de workers, enriquecendo tarefas visuais e de front-end.
6. **Admissão da resposta final em hooks e registro de saídas comprovadas (`#38239`):**
   - O sistema de hooks agora admite a resposta final do agente líder junto ao payload do seu turno de orquestração.
   - O launcher passa a registrar prompts não entregues e saídas comprovadas de subprocessos, impedindo que falhas de
     comunicação descartem silenciosamente o raciocínio ou a conclusão do agente.
7. **Linhagem cross-machine e links pai-filho distribuídos (`#38236`, `#38259`):**
   - Implementa links de linhagem cross-machine conectando sessões de agentes pai e filhos entre máquinas distintas através
     do protocolo wire, CLI, clientes móveis e retomada de chat (`chat resume`), preservando a cadeia de causa e efeito
     mesmo em frotas distribuídas.
8. **Negociação de capacidades na preparação de workers (`#38258`):**
   - Proposta para validar previamente se o host/ambiente do worker atende às capacidades exigidas pelo coordenador antes
     de iniciar o spawn do processo.
9. **Correção de falha de rollback e preservação do erro real em `worker_done` (`#38174`, resolve `#38123`):**
   - No daemon headless `orcad`, quando uma instrução SQLite falhava ao liquidar um worker (`settleWorkerReport`), o app
     executava um comando `ROLLBACK` cego mesmo com a transação já finalizada, disparando `cannot rollback - no transaction is active`
     e mascarando a falha real. O PR `#38174` valida `db.isTransaction` antes de rodar o rollback e garante que o erro original
     seja propagado para o coordenador, destravando a liquidação de tarefas em servidores remotos.
10. **Subagentes Pi em background e keep-awake no chat nativo (`#38207`, `#38210`):**
    - Mantém chats nativos do Pi (`pi --mode rpc`) acordados enquanto subagentes em segundo plano estiverem rodando e propõe
      exibir as sessões filhas estruturadas na interface de Native Chat.
11. **Proteção contra sobreposição de prompts do CLI em rascunhos em digitação (`#38159`):**
    - Recusa a submissão de comandos/prompts automáticos via CLI caso o usuário humano tenha um rascunho de texto não enviado
      no composer, impedindo que o fluxo de IA apague a mensagem que estava sendo digitada.
12. **Replay da receita original de launch ao reabrir worker (`#37757`, resolve `#37693`):**
    - Ao enviar follow-up a um worker cujo terminal já encerrou, o app reinicia o processo na mesma conversa. Antes, o reinício
      recorria a uma receita vazia e perdia o modo `--dangerously-skip-permissions` / Full access. O PR `#37757` grava
      `launch_recipe` na tabela `worker_terminal_resources` (migração v47) e reutiliza exatamente a mesma configuração na reabertura.
13. **Preâmbulo fixo bloqueando push e criação de PRs por workers (`#38111`):**
    - A linha fixa "Don't post to Slack, GitHub, or other channels during the run" induz agentes (especialmente Codex) a
      recusarem o push de branch e abertura de PRs, mesmo quando a tarefa explícita exige entrega via PR. Propõe-se flag
      `--allow-github push,pr` ou configuração `worker.allowGitHub` no `orca.yaml`.
14. **Notificação de conclusão de turnos OpenCode sobre OSC 7501 (`#38222`, `#38172`):**
    - Emite alertas de sistema quando agentes OpenCode concluem turnos de trabalho, evitando que o estado ocioso seja
      confundido com término inesperado.
15. **Fim do atraso de até 10 minutos por ghost text no prompt (`#38077`, `#38015`):**
    - Corrige a leitura do composer para ignorar células de texto `dim` (como "Try this next" do Claude Code) sem texto real
      digitado, destravando a notificação imediata do coordenador.
16. **Emparelhamento direto entre chats locais ("Work together...", `#37744`, `#37741`):**
    - Vincula dois chats de agentes locais em worktrees diferentes com entrega de mensagens controlada pelo usuário,
      preservação de journal de troca e acordar sob demanda.
17. **Inspeção de histórico de child agents no chat pai (`#34895`):**
    - Permite expandir e inspecionar a trilha de raciocínio e histórico de subagentes filhos dentro da conversa do agente pai.
18. **Redução de poluição visual em status de orquestração (`#38079`):**
    - Encolhe os fundos e badges visuais de status das mensagens de correio de orquestração no chat.
19. **Entrega de correio durante turnos ativos via steering (`#37918`):**
    - Entrega mensagens da caixa postal de orquestração diretamente durante turnos de execução ativos via steering de agente.
20. **Diferenciação visual entre Coordenador e workers na UI (`#38000`):**
    - Hierarquia visual explícita na barra lateral / árvore de sessões entre o Coordenador e os workers.

## O que fazer

- Adotar o limite de aninhamento de workers em profundidade 4 (`#38348`) no `brza-workflow` e `brza-studio`.
- Incorporar o fix de wake de coordenador Claude sob subagentes ativos (`#38379`) e encerramento de helpers (`#38373`).
- Implementar o protocolo de federação v4 para mensagens pós-término de workers remotos (`#38376`).
- Adotar o PR `#38174` no `brza-studio` para resolver definitivamente travamentos de `worker_done` em nós remotos.
- Incorporar as proteções de hooks e registro de saídas do PR `#38239`.
- Integrar os identificadores de linhagem cross-machine (`#38236`, `#38259`) no `brza-workflow` e no `brza-cli`.
