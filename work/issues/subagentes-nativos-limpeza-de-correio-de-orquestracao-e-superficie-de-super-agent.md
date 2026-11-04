---
status: open
description: Os PRs #38174, #38207, #38159, #38077 e #37757 e as issues #38111, #38123 e #38210 refinam transações de orquestração, subagentes Pi e integridade de prompts.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#38174`](https://github.com/stablyai/orca/pull/38174),
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

1. **Correção de falha de rollback e preservação do erro real em `worker_done` (`#38174`, resolve `#38123`):**
   - No daemon headless `orcad`, quando uma instrução SQLite falhava ao liquidar um worker (`settleWorkerReport`), o app
     executava um comando `ROLLBACK` cego mesmo com a transação já finalizada, disparando `cannot rollback - no transaction is active`
     e mascarando a falha real. O PR `#38174` valida `db.isTransaction` antes de rodar o rollback e garante que o erro original
     seja propagado para o coordenador, destravando a liquidação de tarefas em servidores remotos.
2. **Subagentes Pi em background e keep-awake no chat nativo (`#38207`, `#38210`):**
   - Mantém chats nativos do Pi (`pi --mode rpc`) acordados enquanto subagentes em segundo plano estiverem rodando e propõe
     exibir as sessões filhas estruturadas na interface de Native Chat.
3. **Proteção contra sobreposição de prompts do CLI em rascunhos em digitação (`#38159`):**
   - Recusa a submissão de comandos/prompts automáticos via CLI caso o usuário humano tenha um rascunho de texto não enviado
     no composer, impedindo que o fluxo de IA apague a mensagem que estava sendo digitada.
4. **Replay da receita original de launch ao reabrir worker (`#37757`, resolve `#37693`):**
   - Ao enviar follow-up a um worker cujo terminal já encerrou, o app reinicia o processo na mesma conversa. Antes, o reinício
     recorria a uma receita vazia e perdia o modo `--dangerously-skip-permissions` / Full access. O PR `#37757` grava
     `launch_recipe` na tabela `worker_terminal_resources` (migração v47) e reutiliza exatamente a mesma configuração na reabertura.
5. **Preâmbulo fixo bloqueando push e criação de PRs por workers (`#38111`):**
   - A linha fixa "Don't post to Slack, GitHub, or other channels during the run" induz agentes (especialmente Codex) a
     recusarem o push de branch e abertura de PRs, mesmo quando a tarefa explícita exige entrega via PR. Propõe-se flag
     `--allow-github push,pr` ou configuração `worker.allowGitHub` no `orca.yaml`.
6. **Notificação de conclusão de turnos OpenCode sobre OSC 7501 (`#38222`, `#38172`):**
   - Emite alertas de sistema quando agentes OpenCode concluem turnos de trabalho, evitando que o estado ocioso seja
     confundido com término inesperado.
7. **Fim do atraso de até 10 minutos por ghost text no prompt (`#38077`, `#38015`):**
   - Corrige a leitura do composer para ignorar células de texto `dim` (como "Try this next" do Claude Code) sem texto real
     digitado, destravando a notificação imediata do coordenador.
8. **Emparelhamento direto entre chats locais ("Work together...", `#37744`, `#37741`):**
   - Vincula dois chats de agentes locais em worktrees diferentes com entrega de mensagens controlada pelo usuário,
     preservação de journal de troca e acordar sob demanda.
9. **Inspeção de histórico de child agents no chat pai (`#34895`):**
   - Permite expandir e inspecionar a trilha de raciocínio e histórico de subagentes filhos dentro da conversa do agente pai.
10. **Redução de poluição visual em status de orquestração (`#38079`):**
    - Encolhe os fundos e badges visuais de status das mensagens de correio de orquestração no chat.
11. **Entrega de correio durante turnos ativos via steering (`#37918`):**
    - Entrega mensagens da caixa postal de orquestração diretamente durante turnos de execução ativos via steering de agente.
12. **Diferenciação visual entre Coordenador e workers na UI (`#38000`):**
    - Hierarquia visual explícita na barra lateral / árvore de sessões entre o Coordenador e os workers.

## O que fazer

- Adotar o PR `#38174` no `brza-studio` para resolver definitivamente travamentos de `worker_done` em nós remotos.
- Incorporar o PR `#38159` para resguardar mensagens do usuário em digitação no `brza-workflow`.
- Implementar o replay de receita de lançamento (`#37757`) e suporte a keep-awake para subagentes Pi (`#38207`).
