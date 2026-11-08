---
status: open
description: Os PRs #39590, #39635, #39597 e as issues #34835, #39634, #39596, #39627 trazem títulos de janela customizáveis, fit-to-width de PDF/HTML e cancelamento de saída.
scope:
  - brza-studio
  - workspace
priority: high
opened: 2026-11-08
tags:
  - design
  - tooling
---

# Títulos de janela para time trackers, ajuste de visualizadores e resiliência de saída

Rastreado do PR aberto no upstream [`stablyai/orca#39590`](https://github.com/stablyai/orca/pull/39590) (resolve Issue [`#34835`](https://github.com/stablyai/orca/issues/34835)),
do PR [`stablyai/orca#39635`](https://github.com/stablyai/orca/pull/39635) (resolve Issue [`#39634`](https://github.com/stablyai/orca/issues/39634)),
do PR [`stablyai/orca#39597`](https://github.com/stablyai/orca/pull/39597) (resolve Issue [`#39596`](https://github.com/stablyai/orca/issues/39596)) e
da issue [`stablyai/orca#39627`](https://github.com/stablyai/orca/issues/39627).

## O problema

1. **Invisibilidade do contexto de projeto, workspace e tarefas em rastreadores de tempo externos (`#39590`, `#34835`):**
   Softwares externos de rastreamento de horas (como Timeular, Toggl, RescueTime, Clockify) e gerenciadores de janelas
   do sistema operacional leem exclusivamente o título da janela nativa do Electron (`document.title`). Como o aplicativo
   exibia apenas um nome estático (`Orca` ou `BrzA Studio`), usuários e automações não conseguiam diferenciar checkouts
   paralelos do mesmo repositório nem associar automaticamente horas gastas à issue vinculada (`issueKey`) sem recorrer a
   plugins proprietários complexos.
2. **Visualizadores de PDF e HTML sem ajuste de largura em divisões de tela (*splits*) (`#39635`, `#39634`):**
   Ao trabalhar com páginas web ou documentações PDF em abas divididas ao lado de terminais e chats de código, o conteúdo
   abria em escala rígida de 100%, forçando rolagem horizontal exaustiva. No caso do PDF, a escala `'page-width'` era
   descartada pelo pdf.js se configurada antes da inicialização das páginas (`pagesinit`) e nunca recalculada sob
   redimensionamento da divisão. No painel de navegador (HTML), o zoom nativo do Electron é global por origem e desconhece a
   largura real dos elementos da página.
3. **Cancelamento de confirmação de saída mantendo o processo principal em estado perpétuo de encerramento (`#39597`, `#39596`):**
   Ao acionar `Cmd+Q` (ou fechar uma janela com agentes em execução) e clicar em Cancel no diálogo de confirmação ("Save changes?"
   ou "Close Window?"), a janela permanecia aberta na tela, mas a flag `isQuitting` no processo principal continuava `true`.
   Com isso, qualquer fechamento posterior de abas ou janelas descartava processos locais sem aviso prévio, e eventuais
   falhas do processo de renderização não eram recuperadas, travando a interface gráfica em uma tela branca permanente.
4. **Falta de arrasto nativo de arquivos do explorador para o sistema operacional (`#39627`):**
   Arquivos listados no gerenciador lateral do workspace não suportam drag-and-drop para fora da janela do app em direção
   ao Finder (macOS) ou outros aplicativos do host.

## O que o upstream implementa

- **Modelo customizável de título de janela (`#39590`, resolve `#34835`):**
  - Introduz a configuração `showWorkspaceInWindowTitle` (opcional, desativada por padrão para preservar privacidade em
    compartilhamentos de tela) e o template `windowTitle`;
  - Suporta as variáveis `${appName}`, `${repo}`, `${worktree}`, `${branch}`, `${issueKey}`, `${tab}` e `${separator}` (padrão: ` — ` entre blocos preenchidos);
  - Formatação defensiva via `lib/window-title-template.ts`: remove separadores e caracteres adjacentes a campos vazios,
    purifica caracteres de controle ou formatação bidi (`stripUnsafeDisplayCharacters`) e limita o texto a 120 bytes UTF-8;
  - Execução desacoplada no `ActiveWorkspaceSyncGate`, evitando re-renderizações desnecessárias da árvore raiz da interface
    quando títulos de terminais alternam.
- **Ajuste automático de largura (*Fit to Width*) em PDF e HTML (`#39635`, resolve `#39634`):**
  - **PDF:** reaplica a escala `'page-width'` no evento `pagesinit` do pdf.js e observa mudanças de largura com `ResizeObserver`,
    fazendo zoom com `Ctrl+Wheel` ou gestos de pinça pausar exatamente no patamar de preenchimento da divisão;
  - **HTML:** nova flag `fitWidth` persistida por site via `browser:setPageSiteFitWidth`, injetando script no frame principal para
    medir a largura renderizada e ajustar `documentElement.style.zoom` dinamicamente sob redimensionamento, carregamento de fontes
    e mutações de DOM;
  - Adiciona controle "Fit to Width" no menu de opções do navegador e ícone de atalho na barra de ferramentas.
- **Cancelamento atômico de encerramento de janela (`#39597`, resolve `#39596`):**
  - Cria o canal IPC `window:close-cancelled` (exposto no preload via `ui.cancelWindowClose`), acionado pelo botão Cancel em diálogos
    de fechamento, teclas Escape e vetos de checkpoint de shutdown;
  - O processo principal (`main-window-close-lifecycle.ts`) limpa a trava `isQuitting`, restaura a proteção contra crashes e
    reabilita avisos de encerramento em fechamentos futuros.

## O que fazer no BrzA Studio

1. Incorporar as configurações de título de janela e o motor de interpolação `${appName}${separator}${repo} / ${worktree} [${issueKey}]`
   no `brza-studio`, facilitando integração com time trackers de desenvolvimento.
2. Portar o ajuste dinâmico de largura para visualizadores de PDF e painéis de documentação HTML em abas divididas.
3. Adotar a sinalização `window:close-cancelled` para evitar travamentos silenciosos ao cancelar fechamentos de janelas no macOS.
