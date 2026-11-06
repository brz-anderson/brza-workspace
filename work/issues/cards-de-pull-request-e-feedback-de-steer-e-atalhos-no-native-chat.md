---
status: open
description: Os PRs #38877, #38848, #38892, #38879, #38883, #38750 e #38749 aprimoram cartões de PR e repositórios remotos, atalhos de envio/fila vazia, streaming e busca de transcrições no Native Chat.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#38877`](https://github.com/stablyai/orca/pull/38877),
[`stablyai/orca#38848`](https://github.com/stablyai/orca/pull/38848),
[`stablyai/orca#38892`](https://github.com/stablyai/orca/pull/38892),
[`stablyai/orca#38879`](https://github.com/stablyai/orca/pull/38879),
[`stablyai/orca#38883`](https://github.com/stablyai/orca/pull/38883),
[`stablyai/orca#38895`](https://github.com/stablyai/orca/pull/38895),
[`stablyai/orca#38750`](https://github.com/stablyai/orca/pull/38750),
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
2. **Cartões de link restritos apenas ao repositório do workspace (`#38892`):**
   Quando a conversa no chat referenciava um PR ou issue de outro repositório no mesmo host (ex.: upstream de um fork ou repositório
   irmão da mesma organização), o app exibia apenas uma prévia genérica sem detalhes, ignorando que o token do host já tinha
   permissão para ler os metadados completos.
3. **Inércia do teclado ao tentar enviar itens da fila após interrupção (<kbd>Stop</kbd>) (`#38877`):**
   Após pressionar Stop com mensagens enfileiradas na fila de espera, a combinação <kbd>Cmd/Ctrl</kbd>+<kbd>Enter</kbd> em um
   composer vazio não disparava o envio do primeiro cartão pausado, forçando o clique manual no botão Send.
4. **Envio acidental do item errado da fila ao limpar o composer (`#38848`):**
   Quando o usuário enfileirava acidentalmente uma mensagem de acompanhamento com <kbd>Enter</kbd> e tentava enviar com
   <kbd>Cmd/Ctrl</kbd>+<kbd>Enter</kbd> do composer já vazio, o atalho enviava a cabeça antiga da fila em vez da mensagem
   recém-enfileirada por engano.
5. **Degradação de renderização no streaming de respostas com tipos genéricos (`#38879`):**
   O analisador léxico de blocos tratava menções em prosa a tipos como `Vec<T>`, `Promise<void>` ou `<string>` como tags HTML
   brutas, forçando a resposta inteira a re-renderizar do início a cada novo token em vez de atualizar apenas o bloco ativo.
6. **Despertar desnecessário de todas as abas e instâncias de chat a cada evento de status (`#38883`):**
   Qualquer mudança de status em um único chat (uma resposta parcial, término de turno, renomeação) forçava a ponte de status
   a clonar resumos e despertar os leitores de todos os chats retidos na janela, degradando a performance da thread de UI.
7. **Varredura O(N) de histórico completo na restauração de transcrições por ID de sessão (`#38895`):**
   Para localizar uma transcrição de chat ao reabrir abas, o app percorria todo o histórico de sessões em disco sequencialmente.
8. **Ambiguidade sobre o comportamento de Cmd/Ctrl+Enter em chats ocupados (`#38749`):**
   Enquanto o agente está trabalhando, os usuários não tinham como saber o que a combinação Cmd/Ctrl+Enter executaria naquele
   instante: se iria injetar o texto no turno ativo (*Steer*), se enfileiraria a mensagem para o próximo turno (*Queue*)
   ou se enviaria o primeiro item da fila.
9. **Falhas espúrias de timeout de 60s em inicializações lentas de agentes (`#38727`):**
   O timer rígido de startup em native chat abortava inicializações normais que demorassem mais de 60s (ex.: Claude com ganchos
   pesados de 75s, ACP ou Pi), deixando o chat inoperante mesmo com o agente vivo.
10. **Atalhos globais do app bloqueados pelo foco no editor de mensagens do chat (`#38724`):**
    Ao digitar no composer do Chat UI, o despachante global interceptava qualquer tecla como entrada de texto puro, impedindo
    atalhos como renomear aba (<kbd>Cmd</kbd>+<kbd>R</kbd>) ou alternar workspaces.
11. **Inflexibilidade do cartão de arquivos alterados em turnos de edição (`#38756`):**
    Todo turno que editava arquivos inseria obrigatoriamente o bloco \"N changed files\" no diário, poluindo conversas longas.
12. **Lentidão ao abrir o seletor de modelos de chat em repositórios grandes (`#38660`):**
    O menu de escolha de modelos inspecionava recursivamente todos os worktrees do repositório, causando travamento perceptível.

## O que o upstream implementa

- **Envio do primeiro cartão pausado pós-Stop (`#38877`):**
  - Com a fila pausada após <kbd>Stop</kbd>, pressionar <kbd>Cmd/Ctrl</kbd>+<kbd>Enter</kbd> no composer vazio dispara imediatamente
    o primeiro cartão em espera e exibe a etiqueta "Steer queued" ao manter a tecla pressionada.
- **Roteamento correto de envio da fila com composer vazio (`#38848`):**
  - <kbd>Cmd/Ctrl</kbd>+<kbd>Enter</kbd> envia o último cartão enfileirado quando o composer estiver vazio, enquanto
    <kbd>Cmd/Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Enter</kbd> seleciona a cabeça da fila.
- **Cartões de PR e links em repositórios remotos arbitrários (`#38892`):**
  - Pré-visualizações de hover cards e cartões de PR abertos agora consultam qualquer repositório no mesmo host autenticado,
    expandindo a integração com forks e repositórios da mesma organização.
- **Streaming fluído para tipos genéricos (`#38879`):**
  - O analisador mantém a renderização de streaming incremental e isolada por bloco mesmo quando o texto contém `<T>`, `Vec<T>`
    ou parâmetros de tipos fora de backticks, reservando o fallback de mensagem completa apenas para HTML real (`<details>`, `<kbd>`).
- **Isolamento de eventos e indexação O(1) de transcrições (`#38883`, `#38895`):**
  - Notificações de mudança de status acordam estritamente o chat correspondente, poupando as demais abas em background;
  - A busca de transcrição por ID de sessão passa a utilizar índice direto O(1).
- **Cartão compacto de Pull Request no Native Chat (`#38750`):**
  - Renderiza um cartão dedicado no rodapé do turno em que o agente cria um PR: exibe ícone de estado, identificador,
    título e contagem de linhas alteradas com link direto para abertura;
  - Inclui botão discreto para ocultar o cartão caso o usuário prefira não visualizá-lo.
- **Feedback visual dinâmico em Cmd/Ctrl+Enter (`#38749`):**
  - Ao segurar <kbd>Cmd</kbd> (ou <kbd>Ctrl</kbd> no Windows/Linux) com o chat ativo e o agente trabalhando, o botão de
    envio altera dinamicamente seu rótulo exibindo exatamente a ação que será disparada: **Steer** (injetar no turno ativo)
    ou **Queue** (enfileirar mensagem).
- **Startup resiliente sem cancelamento prematuro por timer (`#38727`):**
  - Elimina timers curtos artificiais de 60s para Claude, ACP e Pi, permitindo que a inicialização conclua no tempo natural.
- **Pass-through de atalhos do aplicativo a partir do composer (`#38724`):**
  - Permite que atalhos de gerenciamento de abas, navegação de painéis e controle de workspaces funcionem normalmente a partir
    do campo de texto do chat.
- **Opção para ocultar sumário de arquivos alterados (`#38756`) e seletor rápido de modelos (`#38660`):**
  - Adiciona controle para ocultar o cartão de arquivos alterados e acelera o dropdown de modelos sem varreduras recursivas.

## O que fazer

- Incorporar os cartões ricos de PR (`#38750`, `#38892`) e as melhorias de teclado de Steer/Queue (`#38749`, `#38877`, `#38848`).
- Adotar as otimizações de streaming incremental de texto com genéricos (`#38879`) e despacho isolado de status (`#38883`).
