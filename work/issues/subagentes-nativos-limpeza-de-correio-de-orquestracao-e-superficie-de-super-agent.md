---
status: open
description: Os PRs #38464, #38461, #38529, #38713 e as issues #38720 e #38687 trazem entrega de correio via extensão OMP sem digitar no PTY, continuação de workers e herança de conta.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#38713`](https://github.com/stablyai/orca/pull/38713),
[`stablyai/orca#38768`](https://github.com/stablyai/orca/pull/38768),
[`stablyai/orca#38464`](https://github.com/stablyai/orca/pull/38464),
[`stablyai/orca#38461`](https://github.com/stablyai/orca/pull/38461),
[`stablyai/orca#38460`](https://github.com/stablyai/orca/pull/38460) (Issue [`#38446`](https://github.com/stablyai/orca/issues/38446)),
[`stablyai/orca#38494`](https://github.com/stablyai/orca/pull/38494),
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

1. **Entrega de correio em terminais OMP via extensão em vez de digitação no PTY (`#38720`):**
   - Em terminais com OMP (Open Multi-Processing / OpenCode), a entrega de aviso de correio por digitação direta no PTY
     splicava o texto da notificação no meio de frases que o usuário estava digitando;
   - Propõe entregar ponteiros de orquestração através da extensão instalada do OMP como canal limpo, seguindo o padrão
     implementado para o Claude (`#38529`).
2. **Suporte a roles de modelo, seletores e effort em chats e workers OMP (`#38713`):**
   - Configura parâmetros de reasoning effort, papéis de modelo e seleção precisa em sessões e workers do OMP.
3. **Proteção de abas ativas em clientes pareados contra sleep automático (`#38768`):**
   - Garante que workspaces e agentes não entrem em modo sleep se um cliente móvel ou desktop pareado estiver visualizando
     ou digitando ativamente naquela aba.
4. **Continuação de worker finalizado mediante resposta do coordenador (`#38464`):**
   - Quando um worker emite seu `worker_done`, o app mantinha o processo em estado terminal imutável. Agora, caso o
     coordenador envie um follow-up ou responda ao relatório antes da liberação do terminal, o worker é reativado
     continuando o fluxo de raciocínio na mesma sessão sem exigir novo bootstrap.
5. **Herança da conta Claude do chamador para subagentes CLI (`#38461`):**
   - Garante que invocações de subagentes disparadas a partir de um terminal Orca herdem automaticamente a conta e o
     `CLAUDE_CONFIG_DIR` do processo pai, eliminando o débito involuntário de cotas na conta padrão global.
6. **Validação estrita de chamadores em `orchestration check` (`#38460`, resolve `#38446`):**
   - Recusa chamadas de checagem de orquestração ambíguas onde a identidade do chamador não pode ser verificada com precisão.
7. **Aninhamento visual de workers sob coordenadores no cliente móvel (`#38494`):**
   - Agrupa hierarquicamente workers remotos sob seus respectivos coordenadores mesmo quando distribuídos entre múltiplos
     worktrees.
8. **Entrega de correio sem invasão do prompt via canal do Claude (`#38529`, `#38539`):**
   - Substitui a injeção cega de texto e `\r` (Enter) no PTY do terminal pelo canal de prompt dedicado do plugin Claude
     (`$.prompt.submit`), submetendo avisos de correio como turnos limpos e independentes sem sujar a digitação do usuário;
   - Para outros agentes sem plugin, não envia `Enter` caso o usuário tenha digitado teclas após o início da escrita do ponteiro
     e retém entregas por 5 segundos após a última digitação do operador.
9. **Amarração de retomada de perguntas e sessões de chat ao worker correto (`#38445`):**
   - Garante que perguntas abertas (`ask --resume`) só possam ser retomadas e respondidas pelo exato Dispatch ou follow-up
     legítimo que a formulou, impedindo que novos workers executando no mesmo terminal sequestrem respostas alheias.
10. **Workers remotos iniciando em child worktrees aninhados (`#38416`):**
    - Permite que workers despachados para servidores remotos sejam criados dentro de worktrees filhos dedicados aninhados
      sob o workspace do coordenador, garantindo isolamento de branch em pipelines distribuídos.
11. **Retenção de correio diante de rascunhos digitados no OpenCode (`#38451`):**
    - Estende a trava de entrega de correio para respeitar rascunhos em digitação também em terminais do agente OpenCode.
12. **Permissão padrão para workers criarem seus próprios workers até profundidade 4 (`#38348`):**
    - A configuração `Settings → Orchestration → Nested worker depth` é elevada de 1 para 4 por padrão;
    - Cadeias de delegação profunda (`Coordenador → Worker 1 → Worker 2 → Worker 3 → Worker 4`) agora são executadas
      naturalmente sem bloqueio imediato, com roteamento de `worker_done` diretamente para o worker pai imediato de cada nível
      e liberação automática de recursos finalizados sem deixar instâncias órfãs.
13. **Wake de coordenador Claude mesmo com subagentes ativos em background (`#38379`):**
    - Corrige cenário onde o aviso de `worker_done` ficava represado por até 5 minutos quando o app reiniciava enquanto
      um coordenador Claude possuía subagentes locais de background repintando a linha de progresso do terminal;
    - A entrega não exige mais tela quieta quando os próprios hooks do agente reportam um turno ao vivo sem diálogo pendente.
14. **Comunicação persistente de workers concluídos em hosts remotos pareados (`#38376`):**
    - Introduz o protocolo de federação v4 (`orchestration.federation-finished-worker-mail.v1`) permitindo que um worker
      remoto em um servidor pareado continue enviando mensagens (`send`) ou perguntas (`ask`) ao coordenador mesmo após
      emitir seu `worker_done`, com janela de tolerância de 2 minutos e backoff de sincronização.
15. **Interrupção de helpers auxiliares ao parar worker (`#38373`):**
    - Garante que todos os processos e auxiliares filhos iniciados por um worker sejam finalizados imediatamente no cancelamento
      ou parada do worker, impedindo vazamento de processos zumbis em segundo plano.
16. **Anexos nativos de imagem em tarefas de workers (`#38386`):**
    - Proposta para permitir anexação direta de imagens em payloads de dispatch de workers, enriquecendo tarefas visuais e de front-end.
17. **Admissão da resposta final em hooks e registro de saídas comprovadas (`#38239`):**
    - O sistema de hooks agora admite a resposta final do agente líder junto ao payload do seu turno de orquestração.
    - O launcher passa a registrar prompts não entregues e saídas comprovadas de subprocessos, impedindo que falhas de
      comunicação descartem silenciosamente o raciocínio ou a conclusão do agente.
18. **Linhagem cross-machine e links pai-filho distribuídos (`#38236`, `#38259`):**
    - Implementa links de linhagem cross-machine conectando sessões de agentes pai e filhos entre máquinas distintas através
      do protocolo wire, CLI, clientes móveis e retomada de chat (`chat resume`), preservando a cadeia de causa e efeito
      mesmo em frotas distribuídas.
19. **Negociação de capacidades na preparação de workers (`#38258`):**
    - Proposta para validar previamente se o host/ambiente do worker atende às capacidades exigidas pelo coordenador antes
      de iniciar o spawn do processo.
20. **Correção de falha de rollback e preservação do erro real em `worker_done` (`#38174`, resolve `#38123`):**
    - Validação de `db.isTransaction` antes de rollback em sqlite no daemon headless.

## O que fazer

- Implementar entrega de correio via extensão OMP (`#38720`) eliminando injeção em terminais OMP.
- Adotar a reativação de workers finalizados sob resposta do coordenador (`#38464`) no `brza-workflow`.
- Assegurar a herança da conta do chamador para novos subagentes CLI (`#38461`).
- Adotar o canal de entrega limpa de correio via plugin (`#38529`) e o travamento estrito de digitação em `brza-workflow`.
- Implementar as amarras seguras de resume de workers (`#38445`) e criação de worktrees aninhados em hosts remotos (`#38416`).
- Adotar o limite de aninhamento de workers em profundidade 4 (`#38348`) no `brza-workflow` e `brza-studio`.
