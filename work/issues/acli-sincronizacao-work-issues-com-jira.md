---
status: open
description: Permitir sincronizar notas locais em work/issues/ com workitems do Jira Cloud através da Atlassian CLI.
scope:
  - workspace
opened: 2026-11-12
priority: medium
tags:
  - tooling
  - planning
---

# Sincronização entre `work/issues/` do workspace e Jira Cloud via `acli`

## O contexto

O `brza-workspace` gerencia pendências, dívidas técnicas e investigações em arquivos Markdown dentro de `work/issues/` seguindo uma norma rigorosa (frontmatter YAML com `status`, `description`, `scope`, `priority` e tags).

Em projetos e times que usam Atlassian Jira como ferramenta corporativa de tracking, existe atrito manual constante: desenvolvedores precisam copiar descrições do Jira para o workspace ou manualmente transicionar tickets no Jira para "In Progress" e "Done" conforme avançam no código.

A Atlassian CLI (`acli`) disponibiliza APIs via linha de comando para criar (`acli jira workitem create`), ler (`acli jira workitem view --json`) e alterar o estado (`acli jira workitem transition`) de itens no Jira.

## A proposta

Integrar a gestão de notas com a CLI do Jira, viabilizando:

1. **Importação (`brza note import-jira <KEY>`):**
   - Faz a leitura via `acli jira workitem view <KEY> --json`.
   - Gera um arquivo de issue em `work/issues/<slug>.md` com os metadados mapeados: título no H1, sumário em `description`, prioridade mapeada e link para o Jira no corpo.
2. **Exportação / Abertura remota (`brza note export-jira <caminho>`):**
   - Cria o item correspondente no Jira a partir de uma nota local pré-existente via `acli jira workitem create --from-file` ou `--json`.
3. **Conclusão coordenada no `brza note commit`:**
   - Se uma issue do workspace possuir o identificador Jira no frontmatter ou corpo (ex: `jira_key: PROJ-123`), ao commitar o fechamento da issue (`status: done`), o script pode opcionalmente transicionar o ticket no Jira para `Done`.

## O que conferir na sessão que fizer

- Criar o comando `brza note import-jira` compatível com a norma do `work/README.md`.
- Mapeamento determinístico de prioridades do Jira (`Highest`, `High`, `Medium`, `Low`, `Lowest`) para o vocabulário do workspace (`high`, `medium`, `low`).
- Tratamento de falhas de rede e casos de sessão desautenticada sem quebrar notas locais.
- Testes cobrindo a conversão de JSON retornado pelo `acli` para o formato Markdown exigido pelo checador `check_notes.py`.
