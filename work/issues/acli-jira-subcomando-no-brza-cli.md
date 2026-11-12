---
status: done
description: Adicionar o subcomando brza jira para despachar operações e consultas do Jira Cloud via Atlassian CLI.
scope:
  - brza-studio
  - workspace
opened: 2026-11-12
completed: 2026-11-12
priority: medium
tags:
  - tooling
---

# O subcomando `brza jira` despacha operações do Jira Cloud via Atlassian CLI (`acli`)

**Resolvida em 2026-11-12** com a criação do executável `scripts/brza/brza-jira`, inclusão de `jira` em `KNOWN_SUBCOMMANDS` em `scripts/brza/brza` e 11 testes de unidade em `scripts/brza/tests/test_brza_jira.py`. Validado ao vivo com a instância Atlassian Cloud conectada (`fixfy.atlassian.net`).

## O contexto

A Atlassian lançou sua CLI oficial moderna (`acli`), unificando a interação com produtos Atlassian Cloud diretamente no terminal. Dentro do domínio `acli jira`, a ferramenta oferece suporte completo para consultas JQL, visualização, criação, edição e transição de itens de trabalho (`acli jira workitem`), além de gestão de sprints, boards, dashboards e filtros.

No ecossistema BrzA, o CLI unificado `brza` (definido em `scripts/brza/brza`) já atua despachando subcomandos internos (`tree`, `dev`, `test`, `note`, `sessions`, etc.) e subcomandos externos no padrão `brza-<subcomando>`. Ter `brza jira` como comando de primeira classe permite que desenvolvedores consultem e atualizem o Jira sem sair do terminal e sem decorar a sintaxe verbosa de argumentos do `acli`.

## A proposta

Criar o subcomando `brza jira` (via executável `scripts/brza/brza-jira` ou despacho automático no `brza`):

1. **Despacho direto:** Repassar comandos para o binário `acli jira`, preservando flags (`--json`, `--csv`, `-j/--jql`, etc.), streams de entrada/saída e códigos de retorno.
2. **Atalhos e helpers de produtividade:**
   - `brza jira my-work`: Executa `acli jira workitem search --jql "assignee = currentUser() AND statusCategory != Done"`.
   - `brza jira view <KEY>`: Abre ou exibe o resumo do item.
   - `brza jira done <KEY>`: Transiciona o item de trabalho para a categoria concluída sem necessidade de prompts interativos (`--yes`).
3. **Detecção de ambiente:** Informar de forma clara caso a `acli` não esteja instalada no PATH ou precise de autenticação ativa (`acli jira auth login`).

## O que conferir na sessão que fizer

- Criar `scripts/brza/brza-jira` com testes de unidade cobrindo o despacho de comandos e tratamento de ausência do `acli`.
- Adicionar `jira` à lista `KNOWN_SUBCOMMANDS` em `scripts/brza/brza`.
- Garantir suporte completo à passagem de flags arbitrárias (`--json`, `--csv`).
- Documentar o uso no `README.md` e em guias pertinentes.
