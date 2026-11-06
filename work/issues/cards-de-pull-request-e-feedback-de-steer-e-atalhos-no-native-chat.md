---
status: open
description: Os PRs #39050, #39141, #38877, #38848, #38892 e #38879 trazem auto-shrink de imagens coladas, limpeza de cards /model do picker, cartões de PR e atalhos de envio no Native Chat.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#39050`](https://github.com/stablyai/orca/pull/39050) (Issue [`#37855`](https://github.com/stablyai/orca/issues/37855)),
[`stablyai/orca#39141`](https://github.com/stablyai/orca/pull/39141),
[`stablyai/orca#38877`](https://github.com/stablyai/orca/pull/38877),
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
[`stablyai/orca#39060`](https://github.com/stablyai/orca/issues/39060),
[`stablyai/orca#38792`](https://github.com/stablyai/orca/issues/38792) e
[`stablyai/orca#38780`](https://github.com/stablyai/orca/issues/38780).

## O problema

1. **Rejeição com erro fatal ao colar capturas de tela e fotos em alta resolução (`#39050`, `#37855`):**
   Ao colar imagens grandes ou capturas de tela retina no composer do chat, a recodificação interna em PNG ultrapassava o
   limite de bytes/pixels e abortava com `Clipboard image is too large`, forçando o usuário a redimensionar a imagem manualmente
   em editores externos antes de anexar.
2. **Poluição do diário com cartões sintéticos "Ran /model" ao trocar de modelo pelo picker (`#39141`):**
   Ao trocar de modelo de IA pelo dropdown visual do composer, o app enviava o comando para o terminal e gravava um cartão
   local `Ran /model <id>` no meio da conversa. Trocas consecutivas preenchiam o histórico de chat com mensagens redundantes.
3. **Ausência de cartão estruturado quando o agente abre um Pull Request (`#38750`):**
   Ao instruir o agente a criar um PR durante uma sessão de chat, a única evidência visível era a chamada crua da ferramenta
   `gh pr create`. Faltava um cartão compacto e clicável no chat informando o número do PR, título, status e linhas `+18 −15`.
4. **Cartões de link restritos apenas ao repositório do workspace (`#38892`):**
   Quando a conversa no chat referenciava um PR ou issue de outro repositório no mesmo host (ex.: upstream de um fork), o app
   exibia apenas uma prévia genérica sem detalhes, ignorando que o token do host já tinha permissão para ler os metadados.
5. **Inércia do teclado ao tentar enviar itens da fila após interrupção (<kbd>Stop</kbd>) (`#38877`):**
   Após pressionar Stop com mensagens enfileiradas na fila de espera, a combinação <kbd>Cmd/Ctrl</kbd>+<kbd>Enter</kbd> em um
   composer vazio não disparava o envio do primeiro cartão pausado.
6. **Envio acidental do item errado da fila ao limpar o composer (`#38848`):**
   Quando o usuário enfileirava acidentalmente uma mensagem com <kbd>Enter</kbd> e tentava enviar com <kbd>Cmd/Ctrl</kbd>+<kbd>Enter</kbd>
   do composer vazio, o atalho enviava a cabeça antiga da fila em vez da mensagem recém-enfileirada.
7. **Degradação de renderização no streaming de respostas com tipos genéricos (`#38879`):**
   O analisador léxico de blocos tratava menções em prosa a tipos como `Vec<T>` ou `<string>` como tags HTML brutas, forçando
   a resposta inteira a re-renderizar do início a cada novo token em vez de atualizar apenas o bloco ativo.
8. **Despertar desnecessário de todas as abas e instâncias de chat a cada evento de status (`#38883`):**
   Qualquer mudança de status em um único chat forçava a ponte de status a clonar resumos e despertar todos os chats da janela.
9. **Varredura O(N) de histórico completo na restauração de transcrições por ID de sessão (`#38895`):**
   Para localizar uma transcrição de chat ao reabrir abas, o app percorria todo o histórico de sessões em disco sequencialmente.
10. **Ambiguidade sobre o comportamento de Cmd/Ctrl+Enter em chats ocupados (`#38749`):**
    Falta de indicação sobre se Cmd/Ctrl+Enter acionaria Steer ou Queue.
11. **Falhas espúrias de timeout de 60s em inicializações lentas de agentes (`#38727`):**
    O timer rígido de startup abortava inicializações normais que demorassem mais de 60s.
12. **Atalhos globais do app bloqueados pelo foco no editor de mensagens do chat (`#38724`):**
    O composer interceptava teclas de navegação e atalhos de workspace.
13. **Renderização excessivamente pesada de texto em negrito no Chat UI (`#39060`):**
    Fontes bold renderizavam com peso de traço desproporcional sob certos temas.

## O que o upstream implementa

- **Redimensionamento automático de imagens coladas (*auto-shrink*) (`#39050`):**
  - Implementa `encodeClipboardImageWithinLimit`: se a imagem recodificada em PNG ultrapassar os tetos de bytes ou resolução,
    aplica um ciclo de redução proporcional suave até que caiba perfeitamente no limite permitido, garantindo colagem fluida.
- **Supressão de cartões sintéticos de modelo pelo dropdown (`#39141`):**
  - Desassocia a emissão de `onSlashCommand` da seleção visual pelo seletor de modelos. Apenas comandos explicitamente
    digitados (`/model ...`) geram entradas registradas no diário.
- **Envio do primeiro cartão pausado pós-Stop (`#38877`):**
  - Com a fila pausada após <kbd>Stop</kbd>, <kbd>Cmd/Ctrl</kbd>+<kbd>Enter</kbd> no composer vazio dispara imediatamente o primeiro cartão em espera.
- **Roteamento correto de envio da fila com composer vazio (`#38848`):**
  - <kbd>Cmd/Ctrl</kbd>+<kbd>Enter</kbd> envia o último cartão enfileirado quando o composer estiver vazio, enquanto
    <kbd>Cmd/Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Enter</kbd> seleciona a cabeça da fila.
- **Cartões de PR e links em repositórios remotos arbitrários (`#38892`):**
  - Pré-visualizações de hover cards e cartões de PR abertos agora consultam qualquer repositório no mesmo host autenticado.
- **Streaming fluído para tipos genéricos (`#38879`):**
  - O analisador mantém a renderização de streaming incremental mesmo quando o texto contém `<T>`, `Vec<T>` ou parâmetros fora de backticks.
- **Isolamento de eventos e indexação O(1) de transcrições (`#38883`, `#38895`):**
  - Notificações de mudança de status acordam estritamente o chat correspondente, e a busca usa índice direto O(1).
- **Cartão compacto de Pull Request no Native Chat (`#38750`):**
  - Renderiza um cartão dedicado com link direto, contagem de linhas e status no rodapé do turno.
- **Feedback visual dinâmico em Cmd/Ctrl+Enter (`#38749`):**
  - Ao segurar <kbd>Cmd/Ctrl</kbd>, o botão de envio exibe **Steer** ou **Queue**.
- **Startup resiliente sem cancelamento prematuro por timer (`#38727`):**
  - Elimina timeouts curtos artificiais de 60s para Claude, ACP e Pi.
- **Pass-through de atalhos do aplicativo a partir do composer (`#38724`):**
  - Permite acionar atalhos de janelas e navegação mesmo com foco no editor de texto do chat.

## O que fazer

- Incorporar o auto-shrink de imagens coladas (`#39050`) e a limpeza de cartões de modelo redundantes (`#39141`) no `brza-studio`.
- Incorporar os cartões ricos de PR (`#38750`, `#38892`) e as melhorias de teclado de Steer/Queue (`#38749`, `#38877`, `#38848`).
- Adotar as otimizações de streaming incremental de texto com genéricos (`#38879`) e despacho isolado de status (`#38883`).
