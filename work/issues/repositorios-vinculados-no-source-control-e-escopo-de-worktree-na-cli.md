---
status: open
description: O PR #37896 e as issues #37892, #37899, #37838 e #37903 trazem suporte a repositórios vinculados no Source Control, respeito a ORCA_WORKTREE_ID na CLI e abertura de arquivos em split.
scope:
  - brza-studio
  - workspace
priority: high
opened: 2026-11-03
tags:
  - tooling
  - design
---

# Repositórios vinculados no Source Control e escopo de worktree na CLI

Rastreado do PR aberto no upstream [`stablyai/orca#37896`](https://github.com/stablyai/orca/pull/37896) (Issue
[`#37892`](https://github.com/stablyai/orca/issues/37892)) e das issues
[`stablyai/orca#37899`](https://github.com/stablyai/orca/issues/37899),
[`stablyai/orca#37838`](https://github.com/stablyai/orca/issues/37838) e
[`stablyai/orca#37903`](https://github.com/stablyai/orca/issues/37903).

## O problema

1. **Alterações multi-repositório invisíveis no Source Control (`#37896`, `#37892`):** quando um agente operando em um
   workspace modifica arquivos em outro repositório aberto no app (ex.: uma biblioteca compartilhada, sub-repositório
   ou pasta irmã), essas mudanças não apareciam no painel de controle de versão do workspace ativo. Era necessário
   trocar manualmente de workspace para revisar, preparar (stage) e commitar as alterações, quebrando o fluxo de trabalho.
2. **Desvio de abas para worktrees alheios fora do cwd gerenciado (`#37899`):** comandos CLI como `brza tab create`
   decidiam o worktree de destino estritamente com base no diretório atual (`cwd`). Se um agente executasse comandos fora
   de um worktree gerenciado (ex.: após `cd /tmp`), o comando ignorava as variáveis de ambiente exportadas
   `ORCA_WORKTREE_ID` e `ORCA_WORKSPACE_ID` e criava a aba silenciosamente no worktree ativo da janela no momento,
   misturando contextos de projetos.
3. **Falta de opção de abertura de documentos em split na CLI (`#37838`):** ao pedir que o agente abra notas ou
   documentações de pesquisa via `brza file open`, as abas se acumulavam no mesmo grupo de abas dos chats ativos,
   misturando conversas e documentos sem opção de abrir diretamente em um split lateral dedicado de leitura.
4. **Impossibilidade de abrir novo worktree em modo Chat quando o padrão é Terminal (`#37903`):** o modal de criação de
   worktree oferecia apenas linhas `(CLI)` se o padrão global do agente estivesse em Terminal, sem permitir selecionar
   superfície Chat para aquele worktree específico.

## O que o upstream implementa

- **Repositórios vinculados no Source Control (`#37896`):** adiciona a seção "Linked repositories" no painel de Source
  Control, listando automaticamente projetos detectados com modificações e permitindo diff, stage, descarte e commit
  direto na interface do workspace em foco, com opção de ligar/desligar em configurações (`Settings → Git → Linked Repositories`).
- **Respeito às variáveis de ambiente de worktree (`#37899`):** faz `tab create` e comandos semelhantes honrarem
  `ORCA_WORKTREE_ID` mesmo quando o `cwd` do processo estiver em `/tmp` ou fora da árvore do projeto.
- **Abertura em split e seleção de superfície (`#37838`, `#37903`):** propõe `file open --split right|left|down` para
  manter painéis de leitura de artefatos ao lado do chat e introduz controle de superfície individual na criação de worktrees.

## O que fazer

Portar a funcionalidade de repositórios vinculados (`#37896`) para o `brza-studio`, corrigir a resolução de
`ORCA_WORKTREE_ID` em scripts e automações do `brza-workflow` e adotar a abertura em split para visualização de relatórios.
