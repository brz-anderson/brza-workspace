---
status: open
description: Expor ferramentas de consulta e atualização do Jira via Atlassian CLI no servidor MCP do brza-workflow.
scope:
  - brza-studio
  - workspace
opened: 2026-11-12
priority: medium
tags:
  - tooling
---

# Ferramentas Atlassian Jira no servidor MCP do `brza-workflow` (PLN-009)

## O contexto

No PLN-009, o ecossistema BrzA estabeleceu um servidor residente MCP (Model Context Protocol) em `packages/mcp/` do repositório `brza-workflow`. Esse servidor orquestra tarefas, gerencia limites de taxa, coordena filas e provê ferramentas padronizadas para qualquer agente conectado nas sessões do BrzA Studio (Claude, Antigravity, Grok, Codex).

Atualmente, quando um agente precisa de informações sobre um ticket Jira, ele depende de colar texto manualmente no chat ou de requisições REST ad-hoc com tokens transitórios.

Ao mesmo tempo, o novo **Rovo Dev CLI** (`acli rovodev`) suporta o consumo de servidores MCP externos via arquivo `~/.rovodev/mcp.json`.

## A proposta

Criar uma ponte MCP em duas direções:

1. **Ferramentas Atlassian para os agentes do BrzA:**
   - Adicionar ferramentas ao MCP do BrzA que encapsulam comandos do `acli`:
     - `jira_get_workitem`: Obtém detalhes e critérios de aceitação de uma issue via `acli jira workitem view <KEY> --json`.
     - `jira_search_workitems`: Realiza buscas JQL via `acli jira workitem search --jql <QUERY> --json`.
     - `jira_transition_workitem`: Altera o status do item após aprovação de gates de teste ou revisão.
   - Qualquer agente do BrzA Studio ganha visibilidade instantânea do Jira sem reinventar a roda de autenticação.
2. **Integração do MCP BrzA no Rovo Dev:**
   - Documentar e automatizar o registro do servidor MCP do BrzA dentro de `~/.rovodev/mcp.json`.
   - Isso permite que o próprio agente Rovo Dev utilize ferramentas especializadas do BrzA (leitura de notas, execução de testes, inspeção de worktrees).

## O que conferir na sessão que fizer

- Implementar as ferramentas MCP usando execução de subprocesso chamando `acli jira` com saída formatada em JSON.
- Assegurar que falhas de autenticação retornem mensagens de erro acionáveis pelo agente.
- Adicionar cobertura de testes de unidade para as chamadas MCP.
