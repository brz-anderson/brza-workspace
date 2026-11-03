---
status: done
description: O wrapper brza sessions não implementa o argumento --agent e o BrzA Studio reconhece antigravity mas rejeita o alias agy.
scope:
  - brza-workflow
  - workspace
opened: 2026-11-03
completed: 2026-11-03
owner: Anderson
tags:
  - tooling
---

# brza sessions sem suporte ao argumento --agent e alias agy não reconhecido

## O contexto

Anderson solicitou na rodada de execução do PLN-008:
*"abra as sessões que precisar, utilizando `brza sessions --agent agy`"*.

Ao executar o comando indicado, dois desvios técnicos foram constatados:
1. `brza sessions` recusou os argumentos:
   ```text
   usage: brza sessions [-h] [--title TITLE] [--rename] [--checkout CHECKOUT]
                        [--prompt PROMPT | --prompt-file PROMPT_FILE] [--wait]
                        [--dry-run]
                        name
   brza sessions: error: unrecognized arguments: --agent agy
   ```
2. Ao invocar diretamente o backend pelo `brza agent launch --agent agy`, o serviço retornou erro de validação:
   ```json
   {
     "code": "invalid_argument",
     "message": "Unknown TUI agent \"agy\""
   }
   ```

## O problema e o desvio

- **Ausência de `--agent` no `brza-sessions`:** O script em `packages/client/bin/brza-sessions` foi desenhado inicialmente apenas para sessões do Claude Code (`CHAT_COMMAND = 'claude-brza'` e chamada fixa a `brza agent launch --agent claude`). O suporte a `--agent` estava previsto no levantamento do PLN-004, mas ainda não foi implementado no wrapper.
- **Identificador do agente no BrzA Studio:** O enum `TuiAgent` em `src/shared/tui-agent.ts` registra o agente pelo nome canônico `'antigravity'` (e `'gemini'`), não registrando o apelido `'agy'`.
- **Desvio contornado na rodada:** A sessão de implementação no repositório `brza-workflow` foi aberta diretamente pela interface RPC do Studio com o comando:
  ```bash
  brza agent launch --agent antigravity --surface chat --worktree path:/Users/andepb/Projects/brza-workflow
  ```
  e teve sua aba renomeada para `PLN-008: Implementação P1-P5 (brza-workflow)` com o despacho da instrução dos passos P1 a P5.

## A resolução em 2026-11-03

O wrapper passou a aceitar `--agent <id>` e repassar o agente ao `agent launch`, preservando `claude` como padrão.
O alias `agy` é normalizado para `antigravity` no wrapper, sem alteração no app. As checagens de hooks, processos e
transcripts Claude ficam restritas a Claude; `--rename` e `--wait` com outros agentes são recusados antes do launch.
O mapa continua permitindo `list`, `send`, `title` e `close`, com os mesmos JSON públicos.

Implementação e resultados no worklog [Correção do agente no brza sessions](../worklogs/2026-11-03-correcao-do-agente-no-brza-sessions.md),
em tarefa separada do P5 do PLN-008.
