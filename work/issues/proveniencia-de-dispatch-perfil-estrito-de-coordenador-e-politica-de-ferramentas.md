---
status: open
description: Os PRs #43234 e as issues #43229, #43230, #43227, #43226, #43225, #43203, #43201 e #43194 trazem rastreamento de proveniência de dispatch, perfis restritos de coordenadores, exibição de conta e políticas de ferramentas por chat na orquestração.
scope:
  - brza-studio
  - brza-workflow
  - brza-cli
priority: high
opened: 2026-11-16
tags:
  - tooling
  - infra
---

# Proveniência de dispatch, perfil estrito de coordenador e política de ferramentas por chat

Rastreado do PR aberto no upstream [`stablyai/orca#43234`](https://github.com/stablyai/orca/pull/43234)
(resolve issue [`#43224`](https://github.com/stablyai/orca/issues/43224)) e das issues
[`stablyai/orca#43229`](https://github.com/stablyai/orca/issues/43229),
[`stablyai/orca#43230`](https://github.com/stablyai/orca/issues/43230),
[`stablyai/orca#43227`](https://github.com/stablyai/orca/issues/43227),
[`stablyai/orca#43226`](https://github.com/stablyai/orca/issues/43226),
[`stablyai/orca#43225`](https://github.com/stablyai/orca/issues/43225),
[`stablyai/orca#43203`](https://github.com/stablyai/orca/issues/43203),
[`stablyai/orca#43201`](https://github.com/stablyai/orca/issues/43201) e
[`stablyai/orca#43194`](https://github.com/stablyai/orca/issues/43194).

## O problema

1. **Falta de proveniência de requisição nos despachos de workers (`#43229`):**
   No motor de orquestração, quando múltiplos workers são disparados em paralelo, o registro de `Dispatch` não armazena quem solicitou o início da execução (se foi uma ação manual do usuário, um agente coordenador pai, um subagente intermediário, um workflow agendado ou um plugin externo). Isso dificulta auditorias de governança, cancelamentos em cascata e depuração de árvores de delegação complexas.
2. **Ausência de perfil restrito de coordenador imposto pelo host (`#43230`):**
   Agentes no papel de coordenadores muitas vezes deveriam atuar estritamente em planejamento, decomposição de tarefas, delegação a workers e consolidação de resultados. No entanto, por terem acesso irrestrito às mesmas ferramentas de edição de código e comandos de terminal que os workers, frequentemente tentam implementar mudanças diretamente em vez de orquestrar, gerando conflitos de worktree e desperdício de contexto.
3. **Falta de informação sobre a conta de IA na inspeção de workers (`#43234`, resolve `#43224`):**
   O comando `worker-show` na CLI e na API de orquestração detalhava o status, worktree e parâmetros do worker, mas não informava qual conta de provedor (Claude ou Codex account) foi efetivamente atribuída àquela execução, dificultando a auditoria de consumo e rate limits entre contas corporativas e pessoais.
4. **Visão concisa de `worker-list` sem horário de início, esforço e atividade recente (`#43227`):**
   Ao listar dezenas de workers em execução, o formato tabular conciso omitia o timestamp de início (`start time`), o nível de esforço de raciocínio configurado (`effort: low/medium/high`) e o momento da última atividade registrada, forçando o operador a inspecionar worker por worker com chamadas detalhadas.
5. **Falta de recibo de aquisição de conta para sessões Codex (`#43226`):**
   Enquanto as sessões do Claude emitiam recibos formais de atribuição de conta para conciliação contábil e rate limits, os chats e workers do Codex não gravavam o recibo de conta adquirida, criando uma assimetria na rastreabilidade entre provedores.
6. **Ausência de política granular de ferramentas por chat estruturado (`#43225`):**
   Chats estruturados de agentes não permitiam declarar políticas estritas de ferramentas por sessão (lista de ferramentas permitidas ou bloqueadas, imposição de schemas estritos de MCP e limite máximo de turnos), expondo o ambiente a execuções acidentais de comandos perigosos em tarefas que deveriam ser puramente analíticas.
7. **Travamento de continuações de worker na fila de pausa após erros (`#43203`):**
   Quando um worker estruturado encontrava um erro e tentava continuar após recuperação, a continuação ficava retida indefinidamente na fila de pausa, enquanto a chamada `orchestration send` retornava status de sucesso prematuramente.
8. **Títulos genéricos de terminais e cards de "Started worker" (`#43201`, `#43194`):**
   As abas de terminal de workers e os cards de notificação exibiam IDs internos de despacho em vez do nome legível da tarefa (`task display name`), e mensagens de correio enviadas por plugins não mostravam o nome do plugin emissor.

## O que o upstream propõe e implementa

1. **Rastreamento de proveniência de requisição (`#43229`):**
   - Inclui o campo `requested_by` (com tipo de entidade e identificador: `user`, `agent:<id>`, `plugin:<id>`, `cron:<id>`) na tabela de despachos do `orchestration.db`;
   - Permite que o orquestrador mapeie a cadeia causal completa desde o gatilho inicial até cada folha da árvore de workers.
2. **Perfil estrito de coordenador (`coordinator-only`) imposto pelo host (`#43230`):**
   - Cria um perfil de agente no qual o host bloqueia ferramentas de modificação de sistema de arquivos e comandos shell com efeitos colaterais;
   - Restringe o coordenador às primitivas de orquestração (`task`, `dispatch`, `ask`, `worker_done`, `decision_gate`), garantindo disciplina arquitetural na delegação.
3. **Exibição da conta real do worker no `worker-show` (`#43234`, resolve `#43224`):**
   - O comando `orca worker show <id>` passa a exibir explicitamente o campo `Account: <provider>:<account_id>` sob o qual o processo do worker foi lançado.
4. **Metadados operacionais no `worker-list` conciso (`#43227`):**
   - Adiciona colunas compactas com hora de inicialização, nível de esforço (`effort`) e tempo decorrido desde a última atividade de I/O na saída de `worker-list`.
5. **Recibos de conta adquirida padronizados para Codex (`#43226`):**
   - Grava eventos de aquisição de conta no ciclo de vida de sessões do Codex, unificando a telemetria com a já existente no Claude.
6. **Política declarativa de ferramentas por sessão de chat (`#43225`):**
   - Suporte a manifestos de política por chat: `allowed_tools`, `denied_tools`, `strict_mcp: true` e `max_turns: N`, aplicados como middleware na execução de tool calls.
7. **Correção de continuador de worker pausado (`#43203`):**
   - Desempaca a fila de continuadores pós-erro, garantindo que o despacho só confirme sucesso após o worker retomar o processamento de fato.
8. **Títulos legíveis em terminais de workers e correio de plugins (`#43201`, `#43194`):**
   - Nomeia abas de PTY e cards com o `task.display_name`;
   - Exibe o display name do plugin remetente na caixa de correio da orquestração.

## O que fazer no BrzA Studio

- Incorporar no módulo de orquestração (`brza-workflow` e `brza sessions`) o registro de proveniência (`requested_by`) em todos os despachos (`#43229`).
- Adotar a flag/perfil `--coordinator-only` para coordenadores de multiagentes no Studio, evitando execuções concorrentes indevidas no workspace principal (`#43230`).
- Atualizar a CLI `brza worker show` e os cartões visuais de orquestração para exibir a conta do provedor e metadados operacionais (`#43234`, `#43227`).
- Estender os recibos de auditoria contábil de contas para sessões e workers do Codex (`#43226`).
- Adicionar suporte a políticas restritivas de ferramentas por sessão no Native Chat e workers subordinados (`#43225`).
- Aplicar a correção no despachador de workers pós-recuperação de erro (`#43203`) e os títulos contextuais amigáveis nos terminais (`#43201`, `#43194`).
