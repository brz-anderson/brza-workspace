---
status: open
description: Os PRs #38744, #38773, #37896, #38086, #38063 e #38055 trazem bloqueio de checkout inseguro, preparações de worktrees com timeout, repositórios vinculados e escopo de worktree na CLI.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#38744`](https://github.com/stablyai/orca/pull/38744),
[`stablyai/orca#38773`](https://github.com/stablyai/orca/pull/38773),
[`stablyai/orca#38086`](https://github.com/stablyai/orca/pull/38086),
[`stablyai/orca#38063`](https://github.com/stablyai/orca/pull/38063),
[`stablyai/orca#38055`](https://github.com/stablyai/orca/pull/38055),
[`stablyai/orca#38072`](https://github.com/stablyai/orca/pull/38072),
[`stablyai/orca#37896`](https://github.com/stablyai/orca/pull/37896) (Issue [`#37892`](https://github.com/stablyai/orca/issues/37892))
e das issues [`stablyai/orca#37899`](https://github.com/stablyai/orca/issues/37899),
[`stablyai/orca#37838`](https://github.com/stablyai/orca/issues/37838) e
[`stablyai/orca#37903`](https://github.com/stablyai/orca/issues/37903).

## O problema

1. **Trocas de branch inseguras no mobile e desktop corrompendo estados (`#38744`):**
   Ao solicitar troca de branch via ação "Switch branch", o app executava `git checkout` cego sem validar se havia arquivos
   modificados ou não rastreados, rebases/merges em andamento ou agentes trabalhando ativamente no checkout, arriscando
   perda silenciosa de trabalho ou colisões de estado.
2. **Preparações de worktree travadas indefinidamente sem expiração (`#38773`):**
   A criação de worktrees herdava checkouts especulativos em background. Ao reivindicar o checkout, o app removia o timeout,
   fazendo com que a criação do worktree ficasse pendente para sempre mesmo após nenhum processo git estar rodando.
3. **Desvio de abas para worktrees alheios fora do cwd gerenciado (`#37899`, `#38086`):** quando um agente no terminal
   executava `cd /tmp && brza tab create ...` ou outros comandos de navegador/terminal, o comando não conseguia resolver
   um worktree pelo diretório atual e caía silenciosamente no worktree atualmente focado na janela do usuário, em vez de
   permanecer no worktree do terminal que fez a chamada.
4. **Inconsistências de membership entre abas e workspaces (`#38063`):** atrasos na gravação de janelas, criação de
   terminais e visibilidade de chat podiam divergir sobre a qual workspace uma aba pertencia, gerando reabertura incorreta
   de abas fechadas ou substituição de abas durante reinicializações e restaurações.
5. **Perda de escopo de workspace em comandos de browser e links remotos (`#38055`, `#38072`):** comandos CLI de navegador
   disparados fora de checkouts perdiam o contexto do workspace do terminal, e links clicados a partir de terminais de
   servidores pareados podiam abrir no workspace errado da janela desktop.
6. **Alterações multi-repositório invisíveis no Source Control (`#37896`, `#37892`):** quando um agente operando em um
   workspace modifica arquivos em outro repositório aberto no app (ex.: uma biblioteca compartilhada, sub-repositório
   ou pasta irmã), essas mudanças não apareciam no painel de controle de versão do workspace ativo.
7. **Falta de opção de abertura de documentos em split na CLI (`#37838`):** ao pedir que o agente abra notas ou
   documentações de pesquisa via `brza file open`, as abas se acumulavam no mesmo grupo de abas dos chats ativos.

## O que o upstream implementa e corrige

- **Validação de segurança antes de alternar branches (`#38744`):**
  - Compartilha uma única rotina de verificação no desktop e cliente móvel: recusa a troca de branch e informa com clareza
    quando houver alterações pendentes ("Commit or discard N changed files before switching branches"), operações em curso
    (merge, rebase, cherry-pick) ou agentes trabalhando no worktree.
- **Ciclo de vida delimitado para preparações de worktrees (`#38773`):**
  - Estabelece prazos de expiração para checkouts especulativos em background, garantindo fallback para criação normal e
    evitando que comandos de criação fiquem travados.
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

- Adotar as travas de segurança em troca de branch (`#38744`) no `brza-studio`.
- Incorporar o controle de timeout de preparações de worktrees (`#38773`).
- Implementar o `callerTerminalWorkspaceSelector` (`#38086`) e repositórios vinculados (`#37896`).
