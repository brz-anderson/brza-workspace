---
status: open
description: Os PRs #38077, #37757 e #37918 e as issues #38111, #38123, #38015 e #38000 refinam o correio de orquestração, replay de permissões de workers e fluxos de PR.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#37757`](https://github.com/stablyai/orca/pull/37757),
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

1. **Replay da receita original de launch ao reabrir worker (`#37757`, resolve `#37693`):**
   - Ao enviar follow-up a um worker cujo terminal já encerrou, o app reinicia o processo na mesma conversa. Antes, o reinício
     recorria a uma receita vazia e perdia o modo `--dangerously-skip-permissions` / Full access. O PR `#37757` grava
     `launch_recipe` na tabela `worker_terminal_resources` (migração v47) e reutiliza exatamente a mesma configuração na reabertura.
2. **Preâmbulo fixo bloqueando push e criação de PRs por workers (`#38111`):**
   - A linha fixa "Don't post to Slack, GitHub, or other channels during the run" induz agentes (especialmente Codex) a
     recusarem o push de branch e abertura de PRs, mesmo quando a tarefa explícita exige entrega via PR. Propõe-se flag
     `--allow-github push,pr` ou configuração `worker.allowGitHub` no `orca.yaml`.
3. **Falha de rollback em `worker_done` no orcad headless (`#38123`):**
   - Em servidores Linux remotos com `orcad`, chamadas `orchestration send --type worker_done` falhavam com erro enganoso
     `cannot rollback - no transaction is active`, mascarando o erro real de gravação SQLite e deixando Dispatches presos
     em `in_progress` indefinidamente.
4. **Fim do atraso de até 10 minutos por ghost text no prompt (`#38077`, `#38015`):**
   - Corrige a leitura do composer para ignorar células de texto `dim` (como "Try this next" do Claude Code) sem texto real
     digitado, destravando a notificação imediata do coordenador.
5. **Emparelhamento direto entre chats locais ("Work together...", `#37744`, `#37741`):**
   - Vincula dois chats de agentes locais em worktrees diferentes com entrega de mensagens controlada pelo usuário,
     preservação de journal de troca e acordar sob demanda.
6. **Inspeção de histórico de child agents no chat pai (`#34895`):**
   - Permite expandir e inspecionar a trilha de raciocínio e histórico de subagentes filhos dentro da conversa do agente pai.
7. **Redução de poluição visual em status de orquestração (`#38079`):**
   - Encolhe os fundos e badges visuais de status das mensagens de correio de orquestração no chat.
8. **Entrega de correio durante turnos ativos via steering (`#37918`):**
   - Entrega mensagens da caixa postal de orquestração diretamente durante turnos de execução ativos via steering de agente.
9. **Origem limpa de mensagens de conclusão em background (`#37966`):**
   - Exibe o comando original disparado como fonte, em vez de fabricar avatar artificial de agente.
10. **Diferenciação visual entre Coordenador e workers na UI (`#38000`):**
    - Hierarquia visual explícita na barra lateral / árvore de sessões entre o Coordenador e os workers.
11. **Limpeza de alertas de desktop já visualizados (`#37974`):**
    - Limpa notificações de conclusão de tarefa da central do sistema operacional assim que o usuário foca a aba.
12. **Espera agendada e eliminação de falsos alertas de parada (`#37868`, `#37867`):**
    - `orchestration send --type status --wait-until <duration|ISO time>` para workers de longa duração.
13. **Preservação de logs de falha no arranque e limpeza de mensagens (`#37866`, `#37865`, `#37891`, `#37850`, `#37849`):**
    - Retenção de tail de terminal em falhas de startup e simplificação de stubs da skill `orchestration`.

## O que fazer

- Adotar o PR `#37757` no `brza-studio` para garantir que workers reabertos não percam permissões de execução.
- Ajustar os preâmbulos do `brza-workflow` permitindo push de branches e abertura de PRs (`#38111`) sem bloqueio por guardrails.
- Incorporar a correção de transação SQLite em orquestração remota (`#38123`).
