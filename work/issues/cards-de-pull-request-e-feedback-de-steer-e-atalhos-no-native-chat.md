---
status: open
description: Os PRs #38750, #38749, #38727, #38724, #38756 e #38660 trazem cartões de PR no chat, indicador dinâmico de Steer/Queue, startup sem limite artificial e atalhos no editor.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-06
tags:
  - chat
  - tooling
---

# Cartões de Pull Request, feedback de Steer e atalhos no Native Chat

Rastreado dos PRs abertos no upstream [`stablyai/orca#38750`](https://github.com/stablyai/orca/pull/38750),
[`stablyai/orca#38749`](https://github.com/stablyai/orca/pull/38749),
[`stablyai/orca#38727`](https://github.com/stablyai/orca/pull/38727),
[`stablyai/orca#38724`](https://github.com/stablyai/orca/pull/38724),
[`stablyai/orca#38756`](https://github.com/stablyai/orca/pull/38756),
[`stablyai/orca#38660`](https://github.com/stablyai/orca/pull/38660) e das issues
[`stablyai/orca#38792`](https://github.com/stablyai/orca/issues/38792) e
[`stablyai/orca#38780`](https://github.com/stablyai/orca/issues/38780).

## O problema

1. **Ausência de cartão estruturado quando o agente abre um Pull Request (`#38750`):**
   Ao instruir o agente a criar um PR durante uma sessão de chat, a única evidência visível era a chamada crua da ferramenta
   `gh pr create`. Faltava um cartão compacto e clicável no chat informando o número do PR, título, status (aberto, rascunho,
   mesclado) e as linhas adicionadas/removidas (`+18 −15`).
2. **Ambiguidade sobre o comportamento de Cmd/Ctrl+Enter em chats ocupados (`#38749`):**
   Enquanto o agente está trabalhando, os usuários não tinham como saber o que a combinação Cmd/Ctrl+Enter executaria naquele
   instante: se iria injetar o texto no turno ativo (*Steer*), se enfileiraria a mensagem para o próximo turno (*Queue*)
   ou se enviaria o primeiro item da fila. A única dica ficava oculta no tooltip do botão Send.
3. **Falhas espúrias de timeout de 60s em inicializações lentas de agentes (`#38727`):**
   Embora o timeout de handshake tenha sido elevado para alguns provedores, o timer rígido de startup em native chat
   ainda abortava inicializações normais que demorassem mais de 60s (ex.: Claude com ganchos pesados de 75s, ACP ou Pi),
   deixando o chat inoperante mesmo com o agente vivo.
4. **Atalhos globais do app bloqueados pelo foco no editor de mensagens do chat (`#38724`):**
   Ao digitar no composer do Chat UI, o despachante global interceptava qualquer tecla como entrada de texto puro,
   impedindo atalhos como renomear aba (<kbd>Cmd</kbd>+<kbd>R</kbd>), alternar workspaces em repouso ou atalhos de navegação.
5. **Inflexibilidade do cartão de arquivos alterados em turnos de edição (`#38756`):**
   Todo turno que editava arquivos inseria obrigatoriamente o bloco "N changed files" no diário, poluindo conversas longas
   sem permitir que o usuário desativasse o sumário.
6. **Lentidão ao abrir o seletor de modelos de chat em repositórios grandes (`#38660`):**
   O menu de escolha de modelos inspecionava recursivamente todos os worktrees do repositório para carregar configurações,
   causando travamento perceptível ao clicar no dropdown de modelos.

## O que o upstream implementa

- **Cartão compacto de Pull Request no Native Chat (`#38750`):**
  - Renderiza um cartão dedicado no rodapé do turno em que o agente cria um PR: exibe ícone de estado, identificador,
    título e contagem de linhas alteradas com link direto para abertura;
  - Inclui botão discreto para ocultar o cartão caso o usuário prefira não visualizá-lo.
- **Feedback visual dinâmico em Cmd/Ctrl+Enter (`#38749`):**
  - Ao segurar <kbd>Cmd</kbd> (ou <kbd>Ctrl</kbd> no Windows/Linux) com o chat ativo e o agente trabalhando, o botão de
    envio altera dinamicamente seu rótulo exibindo exatamente a ação que será disparada: **Steer** (injetar no turno ativo)
    ou **Queue** (enfileirar mensagem).
- **Startup resiliente sem cancelamento prematuro por timer (`#38727`):**
  - Elimina timers curtos artificiais de 60s para Claude, ACP e Pi, permitindo que a inicialização conclua no tempo natural
    do processo, mantendo apenas cancelamento explícito do usuário (<kbd>Stop</kbd>), falhas de autenticação ou o teto de 10 minutos.
- **Pass-through de atalhos do aplicativo a partir do composer (`#38724`):**
  - Permite que atalhos de gerenciamento de abas, navegação de painéis e controle de workspaces funcionem normalmente
    a partir do campo de texto do chat quando a combinação não colidir com comandos de edição.
- **Opção para ocultar sumário de arquivos alterados (`#38756`):**
  - Adiciona controle em `Settings → Chat → Behavior → Changed files summary` e botão de ocultar no próprio cartão.
- **Otimização no carregamento do seletor de modelos (`#38660`):**
  - Elimina a varredura desnecessária de worktrees secundários, abrindo o dropdown de modelos instantaneamente.

## O que fazer

- Incorporar os cartões ricos de PR (`#38750`) e o feedback visual de Steer/Queue (`#38749`) no `brza-studio`.
- Adotar o startup sem interrupção precoce (`#38727`) no runtime de Native Chat do `brza-studio`.
- Habilitar o repasse de atalhos de teclado (`#38724`) e a configuração de ocultar arquivos alterados (`#38756`).
