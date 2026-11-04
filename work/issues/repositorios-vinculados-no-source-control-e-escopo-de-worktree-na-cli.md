---
status: open
description: Os PRs #37896, #38086, #38063 e #38055 e as issues #37892, #37899 e #37838 trazem suporte a repositórios vinculados, escopo canônico de worktree na CLI e membership durável de abas.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#38086`](https://github.com/stablyai/orca/pull/38086),
[`stablyai/orca#38063`](https://github.com/stablyai/orca/pull/38063),
[`stablyai/orca#38055`](https://github.com/stablyai/orca/pull/38055),
[`stablyai/orca#38072`](https://github.com/stablyai/orca/pull/38072),
[`stablyai/orca#37896`](https://github.com/stablyai/orca/pull/37896) (Issue [`#37892`](https://github.com/stablyai/orca/issues/37892))
e das issues [`stablyai/orca#37899`](https://github.com/stablyai/orca/issues/37899),
[`stablyai/orca#37838`](https://github.com/stablyai/orca/issues/37838) e
[`stablyai/orca#37903`](https://github.com/stablyai/orca/issues/37903).

## O problema

1. **Desvio de abas para worktrees alheios fora do cwd gerenciado (`#37899`, `#38086`):** quando um agente no terminal
   executava `cd /tmp && brza tab create ...` ou outros comandos de navegador/terminal, o comando não conseguia resolver
   um worktree pelo diretório atual e caía silenciosamente no worktree atualmente focado na janela do usuário, em vez de
   permanecer no worktree do terminal que fez a chamada.
2. **Inconsistências de membership entre abas e workspaces (`#38063`):** atrasos na gravação de janelas, criação de
   terminais e visibilidade de chat podiam divergir sobre a qual workspace uma aba pertencia, gerando reabertura incorreta
   de abas fechadas ou substituição de abas durante reinicializações e restaurações.
3. **Perda de escopo de workspace em comandos de browser e links remotos (`#38055`, `#38072`):** comandos CLI de navegador
   disparados fora de checkouts perdiam o contexto do workspace do terminal, e links clicados a partir de terminais de
   servidores pareados podiam abrir no workspace errado da janela desktop.
4. **Alterações multi-repositório invisíveis no Source Control (`#37896`, `#37892`):** quando um agente operando em um
   workspace modifica arquivos em outro repositório aberto no app (ex.: uma biblioteca compartilhada, sub-repositório
   ou pasta irmã), essas mudanças não apareciam no painel de controle de versão do workspace ativo.
5. **Falta de opção de abertura de documentos em split na CLI (`#37838`):** ao pedir que o agente abra notas ou
   documentações de pesquisa via `brza file open`, as abas se acumulavam no mesmo grupo de abas dos chats ativos.

## O que o upstream implementa e corrige

- **Resolução de worktree pelo terminal chamador (`#38086`, resolve `#37899`):**
  - Implementa `callerTerminalWorkspaceSelector`: quando o lookup por `cwd` não encontra nenhum worktree gerenciado, a CLI
    recorre a `ORCA_WORKTREE_ID` e `ORCA_WORKSPACE_ID` para direcionar a criação de abas e comandos (`tab create`,
    `open-url`, etc.) ao workspace do terminal chamador.
- **Canonicidade e transacionalidade de membership de workspaces (`#38063`):**
  - Estabelece um registro canônico durável de pertença de terminais e native-chats por host;
  - Gravações de layout comparam o estado observado antes de aplicar modificações, impedindo que saves atrasados
    substituam abas mais novas ou reabram conteúdos fechados;
  - Serve como alicerce transacional para a alternância de superfícies entre Chat UI e Terminal (`#31595`).
- **Retenção de workspace em browser e links remotos (`#38055`, `#38072`):**
  - Mantém o workspace do terminal para comandos de browser e garante que links de arquivos abram no workspace exato do clique.
- **Repositórios vinculados no Source Control (`#37896`):**
  - Adiciona a seção "Linked repositories" no painel de Source Control, listando projetos modificados e permitindo diff,
    stage e commit sem chavear de janela.

## O que fazer

Portar os PRs `#38086` e `#38063` para o `brza-studio` para blindar a integridade de workspaces em comandos CLI de
background do `brza-workflow` e viabilizar a alternância in-place entre terminais e chat.
