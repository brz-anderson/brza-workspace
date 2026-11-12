---
status: open
description: Os PRs #39096, #39089, #39087, #38744 e as issues #38940, #37896 trazem histórico zsh por worktree, snapshots headless limpos e status de perguntas Codex.
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

<!-- pln-014-despacho -->
> **Despacho (PLN-014/R1.1):** classe `parcial` · casa `studio`
> Merge no upstream não muda `status`. PLN-014/R1, 2026-11-12.

Rastreado dos PRs abertos no upstream [`stablyai/orca#39096`](https://github.com/stablyai/orca/pull/39096) (resolve Issue [`#38940`](https://github.com/stablyai/orca/issues/38940)),
[`stablyai/orca#39089`](https://github.com/stablyai/orca/pull/39089),
[`stablyai/orca#39087`](https://github.com/stablyai/orca/pull/39087),
[`stablyai/orca#38744`](https://github.com/stablyai/orca/pull/38744),
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

1. **Histórico zsh isolado por worktree não carregado na abertura do terminal (`#39096`, `#38940`):**
   No macOS, ao abrir um novo terminal com histórico zsh configurado por worktree, o shell salvava novos comandos no arquivo
   específico do workspace, mas não lia os comandos gravados anteriormente porque a restauração da variável `HISTFILE` ocorria
   após o zsh já ter carregado o histórico global na inicialização.
2. **Resíduos de sequências de escape ANSI em restaurações de terminais headless (`#39089`):**
   Ao restaurar o buffer de um terminal que executava em modo headless, sequências parciais de escape ficavam pendentes no
   fluxo de escrita e eram cuspidas como caracteres literais de controle (`^[[...`) na reconexão da interface.
3. **Falta de indicação quando o Codex aguarda resposta em perguntas assíncronas no meio do turno (`#39087`):**
   Quando o agente Codex faz uma pergunta ao usuário no meio do turno e segue executando em background, a barra lateral e o
   cliente móvel continuavam exibindo o status genérico "working", sem alertar o operador de que sua resposta estava pendente.
4. **Trocas de branch inseguras no mobile e desktop corrompendo estados (`#38744`):**
   Ao solicitar troca de branch via ação "Switch branch", o app executava `git checkout` cego sem validar se havia arquivos
   modificados ou não rastreados, rebases/merges em andamento ou agentes trabalhando ativamente no checkout.
5. **Preparações de worktree travadas indefinidamente sem expiração (`#38773`):**
   A criação de worktrees herdava checkouts especulativos em background sem timeout.
6. **Desvio de abas para worktrees alheios fora do cwd gerenciado (`#37899`, `#38086`):**
   Comandos de terminal fora de pastas de worktree caíam no workspace atualmente focado na janela.
7. **Inconsistências de membership entre abas e workspaces (`#38063`):**
   Atrasos na gravação de layouts podiam misturar abas entre diferentes workspaces.
8. **Alterações multi-repositório invisíveis no Source Control (`#37896`, `#37892`):**
   Modificações em submódulos ou repositórios irmãos não apareciam no Source Control do workspace ativo.

## O que o upstream implementa e corrige

- **Carregamento correto de histórico zsh por worktree (`#39096`):**
  - Após definir o `HISTFILE` específico do workspace no gancho de inicialização diferida do shell, executa `builtin fc -RI`
    para carregar incrementalmente as linhas do arquivo de histórico do worktree sem descartar o histórico global já presente.
- **Captura atômica de snapshots em terminais headless (`#39089`):**
  - Sincroniza a captura de estados do buffer entre ciclos completos de escrita PTY, garantindo que o snapshot nunca seja
    congelado no meio de uma sequência de controle ANSI.
- **Status "Waiting for user" em perguntas assíncronas do Codex (`#39087`):**
  - Mapeia o estado de perguntas mid-turn do Codex para que a barra lateral, o cabeçalho e as notificações reflitam com
    precisão que o agente está aguardando a entrada do usuário.
- **Validação de segurança antes de alternar branches (`#38744`):**
  - Recusa a troca de branch quando houver alterações pendentes, operações em curso (merge, rebase) ou agentes trabalhando.
- **Ciclo de vida delimitado para preparações de worktrees (`#38773`):**
  - Prazos de expiração para checkouts especulativos em background.
- **Resolução de worktree pelo terminal chamador (`#38086`, resolve `#37899`):**
  - Direciona comandos ao workspace correto via `ORCA_WORKTREE_ID` e `ORCA_WORKSPACE_ID`.
- **Canonicidade e transacionalidade de membership de workspaces (`#38063`):**
  - Registro canônico durável de pertença de terminais e native-chats.
- **Repositórios vinculados no Source Control (`#37896`):**
  - Seção "Linked repositories" no painel de Source Control.

## O que fazer

- Adotar o carregamento de histórico zsh por worktree (`#39096`) no script de inicialização do terminal do `brza-studio`.
- Incorporar a captura de snapshots headless sem escape tails (`#39089`) e a indicação de perguntas Codex (`#39087`).
- Adotar as travas de segurança em troca de branch (`#38744`) e repositórios vinculados (`#37896`).
