---
status: open
description: A issue #37832 e os PRs #37063 e #37781 corrigem sessões ocultas de titulação ACP que comitam no worktree, sinalizam atenção quando workers param sem worker_done e limpam esperas de permissão.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-03
tags:
  - chat
  - tooling
---

# Isolamento de sessões de titulação ACP e status de conclusão de workers

Rastreado da issue aberta no upstream [`stablyai/orca#37832`](https://github.com/stablyai/orca/issues/37832) e dos PRs
[`stablyai/orca#37063`](https://github.com/stablyai/orca/pull/37063) (Issue
[`stablyai/orca#37040`](https://github.com/stablyai/orca/issues/37040)) e
[`stablyai/orca#37781`](https://github.com/stablyai/orca/pull/37781), além da issue
[`stablyai/orca#37815`](https://github.com/stablyai/orca/issues/37815).

## O problema

1. **Sessões ocultas de titulação ACP executando modificações no worktree (`#37832`):** ao abrir um chat do OpenCode 2
   (ou agente ACP equivalente) com prompt substancial, o runtime dispara requisições em segundo plano para gerar o
   título da conversa ("Name this chat"). Por um defeito grave de atribuição de perfil, essas requisições spawnaram
   três processos filhos com privilégios plenos de agente de `build`, que receberam o prompt original embutido,
   executaram ferramentas no disco e chegaram a fazer dois commits não autorizados no repositório.
2. **Workers de orquestração que encerram sem `worker_done` (`#37063`, `#37040`):** quando o turno de um worker
   termina (por parada normal ou erro) sem que o modelo chame formalmente a ferramenta `worker_done`, o coordenador
   ficava indefinidamente esperando ou presumia um estado inconsistente, sem apontar a ação seguinte necessária.
3. **Persistência indevida de aviso de permissão de Claude (`#37781`):** o indicador de atenção "?" permanecia na
   aba mesmo após Claude recusar ou concluir um lote de chamadas sem resposta, porque o runtime não observava o fim do
   lote de ferramentas.
4. **Rejeição de workers em terminais WSL rastreados (`#37815`):** painéis de terminal OpenCode em WSL no Windows eram
   rastreados pelo host, mas o comando `worker-start --terminal` rejeitava com erro `agent_unconfigured`.

## O que o upstream implementa e corrige

- **Isolamento de sessões utilitárias (`#37832`):** restringe subprocessos auxiliares (como geradores de título ou
  resumos de histórico) a perfis estritamente sem permissões de execução de ferramentas, impedindo acesso a arquivos e
  ao git.
- **Detecção de atenção em workers (`#37063`):** introduz a categoria de atenção `stopped_without_worker_done` com
  `requiresAction: true`, inclui o `lastAssistantMessage` na projeção do worker e aponta `nextAction` para
  `worker-read`, desbloqueando o supervisor.
- **Hook de término de lote de ferramentas (`#37781`):** escuta o hook `PostToolBatch` do Claude Code para limpar o
  estado de espera de permissão imediatamente quando o lote se resolve.

## O que fazer

Revisar o lançamento de sessões secundárias ACP no `brza-studio` para isolar títulos de abas e incorporar as melhorias
de detecção de conclusão de workers no ciclo de supervisão do `brza-workflow`.
