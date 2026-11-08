---
status: open
description: O PR #39882 e as issues #39841, #39844, #39856, #39830 trazem toolbar flutuante no chat, foco em Add to chat, recents no Cmd+J e anotações.
scope:
  - brza-studio
  - workspace
priority: high
opened: 2026-11-08
tags:
  - chat
  - design
  - tooling
---

# Barra flutuante de ações de chat, retenção de foco e recents no Native Chat

Rastreado do PR aberto no upstream [`stablyai/orca#39882`](https://github.com/stablyai/orca/pull/39882) (resolve Issue [`#39872`](https://github.com/stablyai/orca/issues/39872)),
além das issues [`stablyai/orca#39841`](https://github.com/stablyai/orca/issues/39841),
[`stablyai/orca#39844`](https://github.com/stablyai/orca/issues/39844),
[`stablyai/orca#39856`](https://github.com/stablyai/orca/issues/39856) e
[`stablyai/orca#39830`](https://github.com/stablyai/orca/issues/39830).

## O problema

1. **Botões de ações de chat soltos e sobrepostos ao texto das mensagens (`#39882`, `#39872`):**
   No canto superior direito de abas de Native Chat, os botões de ação (handoff, resume na CLI, split e configurações de chat)
   utilizavam o mesmo estilo sem moldura (*chromeless*) das panes de terminal: ícones diminutos de 12px com traço de 2.75px em
   slots redondos soltos diretamente sobre as mensagens. Além de conferir aspecto desorganizado e difícil de clicar, os botões
   ficavam sobrepostos à primeira linha do texto inicial da conversa.
2. **Abas de Native Chat ignoradas na ordenação por recência do Cmd+J (`#39841`):**
   Ao usar a paleta de navegação rápida (*jump palette*, `Cmd+J`), chats nativos recém-utilizados eram empurrados para o
   final da seção "Recent Chats & Terminals", exibindo o horário de criação da aba em vez da última interação. Isso ocorria
   porque, embora `activateTab` atribuísse `lastFocusedAt = Date.now()`, snapshots posteriores do host reconstruíam a aba
   através de `terminal-surfaces.ts` sem copiar `lastFocusedAt`, zerando o timestamp e quebrando a ordenação cronológica.
3. **Perda de foco na caixa de texto ao usar "Add to chat" em texto selecionado (`#39844`):**
   Ao selecionar um trecho de texto em uma resposta do agente e clicar no botão flutuante "Add to chat", a citação era inserida
   no composer em formato markdown, mas o cursor permanecia fora da caixa de entrada. O usuário precisava clicar manualmente
   com o mouse dentro do composer antes de digitar. O problema decorria do método `focusMountedNativeChatEditor` retornar
   antecipadamente enquanto o popover de seleção (`SelectionAddToChatPopover`, com `role="dialog"`) ainda retinha o foco.
4. **Anotações pendentes no navegador embutido invisíveis ao agente e perdidas ao fechar aba (`#39856`):**
   Quando o usuário insere comentários e anotações visuais em páginas web abertas pelo agente no navegador embutido do app
   mas não aciona o envio imediato, essas anotações não ficam acessíveis via nenhum comando da CLI do agente (ex.: `orca annotations list`).
   Ao fechar a aba ou reiniciar a sessão do agente, todas as anotações não salvas são descartadas permanentemente sem aviso prévio.
5. **Captura indevida de texto e sufixos após parênteses de fechamento em links de arquivo no terminal (`#39830`):**
   No terminal integrado, caminhos de arquivo envolvidos por parênteses e seguidos imediatamente por texto ou pontuação
   (ex.: `(records/review/report.txt)text` ou `(records/review/report.docx)에`) tinham o sufixo capturado como parte do nome
   do arquivo durante o `Cmd+Click`, impedindo a abertura correta do arquivo.

## O que o upstream implementa

- **Floating Toolbar unificada para ações de Native Chat (`#39882`):**
  - Agrupa as ações do cabeçalho da pane em uma barra de ferramentas flutuante opaca com acabamento padrão (`rounded-md`, `shadow-xs`, borda e fundo sólido);
  - Aumenta os ícones para 16px com traço padrão em alvos de clique ergonômicos de 28px;
  - Eleva o espaçamento do topo da transcrição (`pt-10` / gap) de 40px para 42px constantes, garantindo que a primeira mensagem comece
    abaixo da barra e nunca seja obstruída ou desloque sob hover/foco;
  - Preserva o estilo compacto e chromeless exclusivo para as abas de terminal PTY.
- **Preservação de `lastFocusedAt` em snapshots de abas de chat (`#39841`):**
  - Propõe que `terminal-surfaces.ts` copie explicitamente `existing?.lastFocusedAt` ao sintetizar a aba unificada de chat,
    assegurando que o histórico de navegação do `Cmd+J` priorize chats ativos recentemente.
- **Liberação síncrona do popover para foco imediato no composer (`#39844`):**
  - Ajusta a sequência de fechamento de `SelectionAddToChatPopover` com `flushSync` antes de invocar o foco do editor,
    colocando o cursor na linha em branco abaixo da citação markdown.
- **Exposição de anotações do navegador e persistência defensiva (`#39856`):**
  - Proposta para comando CLI `orca annotations list --page <id> --json` e retenção de rascunhos de anotações no estado do workspace.
- **Delimitação estrita de parênteses envolventes em links de terminal (`#39830`):**
  - Normaliza o parser de caminhos para reconhecer o delimitador de parêntese de fechamento `)` e descartar sufixos de texto subsequentes.

## O que fazer

- Adotar a toolbar flutuante opaca (`#39882`) no cabeçalho de chats do `brza-studio`.
- Preservar `lastFocusedAt` nas rotinas de sincronização de abas de chat (`#39841`) para corrigir o ordenamento do `Cmd+J`.
- Ajustar o fluxo de "Add to chat" (`#39844`) para garantir foco automático do cursor no composer abaixo da citação.
- Planejar suporte CLI para leitura de anotações de páginas no navegador integrado (`#39856`).
- Corrigir a extração de caminhos com parênteses envolventes no detector de links do terminal (`#39830`).
