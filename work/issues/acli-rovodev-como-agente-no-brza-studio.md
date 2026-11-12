---
status: open
description: Integrar o agente Rovo Dev CLI como um launcher de agente e runtime orquestrável no BrzA Studio.
scope:
  - brza-studio
opened: 2026-11-12
priority: medium
tags:
  - tooling
  - chat
---

# Rovo Dev CLI (`acli rovodev`) como agente e runtime de execução no `BrzA Studio`

## O contexto

O `BrzA Studio` (evolução do Orca) suporta múltiplos agentes e runtimes para conduzir sessões de codificação e automação (`claude`, `codex`, `antigravity`, `grok`), permitindo disparar workers em abas de chat ou terminais isolados via RPC (`worker-start`, `sessions`).

A Atlassian lançou o **Rovo Dev CLI** (`acli rovodev`), seu agente oficial de codificação assistida por IA. O Rovo Dev possui características altamente compatíveis com a arquitetura do BrzA Studio:
- Execução interativa no terminal (`acli rovodev run`) e modo headless / instrução única (`acli rovodev run "<prompt>"`).
- Suporte nativo a **Git Worktrees** (`acli rovodev run --worktree <nome>`), alinhando-se com a estrutura de worktrees do `brza-workspace`.
- Conexão nativa ao Atlassian Teamwork Graph, permitindo que o agente consuma contexto rico de tickets do Jira, páginas de documentação do Confluence e histórico de PRs.
- Modo autônomo sem bloqueio (`--yolo`), hooks de eventos e suporte ao Model Context Protocol (MCP).

## A proposta

Adicionar o `rovodev` como opção de agente executável no ecossistema do BrzA Studio:

1. **Launcher no BrzA Studio (`worker-start`):**
   - Configurar o adaptador de terminal/CLI para o binário `acli rovodev run`.
   - Permitir que o usuário escolha "Rovo Dev" na seleção de agentes do chat ou via flags de orquestração (`--agent rovodev`).
2. **Coordenação de Worktree:**
   - Aproveitar o isolamento de worktrees do BrzA Studio em conjunto com o suporte nativo do Rovo Dev (`--worktree`).
3. **Casos de uso dedicados:**
   - Utilizar o Rovo Dev primariamente em tarefas que exigem contexto profundo de projetos Atlassian (ex: "implemente os critérios de aceitação do ticket PROJ-456").

## O que conferir na sessão que fizer

- Avaliar se a comunicação será via adaptador TUI/terminal ou se o Rovo Dev expõe protocolo ACP / JSON-RPC.
- Testar o comportamento de passagem de flags de permissão (`--yolo` ou arquivo `~/.rovodev/config.yml`).
- Atualizar a matriz de runtimes e catálogo de modelos do BrzA Studio.
- Conferir coexistência do PATH do `acli` dentro dos terminais do app.
