---
status: open
description: Os PRs #42253, #42247, #42189, #41976, #41948 trazem I/O assíncrono de conexões de servidores e extensões, isolamento de probes de modelos e chats sob host independente.
scope:
  - brza-studio
  - brza-workflow
  - workspace
priority: high
opened: 2026-11-13
tags:
  - tooling
  - infra
---

# Alocação de chats locais sob host independente, admissão de Git e cache de modelos

Rastreado dos PRs abertos no upstream [`stablyai/orca#42253`](https://github.com/stablyai/orca/pull/42253),
[`stablyai/orca#42247`](https://github.com/stablyai/orca/pull/42247),
[`stablyai/orca#42189`](https://github.com/stablyai/orca/pull/42189),
[`stablyai/orca#41976`](https://github.com/stablyai/orca/pull/41976) (resolve STA-13482),
[`stablyai/orca#41948`](https://github.com/stablyai/orca/pull/41948),
[`stablyai/orca#41946`](https://github.com/stablyai/orca/pull/41946) (resolve Issue [`#41934`](https://github.com/stablyai/orca/issues/41934)),
[`stablyai/orca#41927`](https://github.com/stablyai/orca/pull/41927) (resolve STA-14967) e
[`stablyai/orca#41917`](https://github.com/stablyai/orca/pull/41917).

## O problema

1. **Esgotamento de memória e contenção no processo Electron por chats nativos e agentes (`#41917`):**
   No macOS, agentes em background e múltiplos chats nativos concorrentes executavam acoplados ao processo principal do Electron.
   Trabalhos volumosos com árvores de contexto extensas elevavam o consumo de memória do aplicativo, causando engasgos na interface
   e degradação de desempenho durante tarefas paralelas longas.
2. **Contenção e travamentos de I/O por rajadas de Git durante criação de worktrees (`#41927`):**
   Quando múltiplos agentes ou automações criavam e inicializavam worktrees concorrentemente, comandos de leitura Git
   (`git status`, `git branch`, checagens de HEAD) competiam sem limite de admissão contra operações pesadas de checkout. Isso
   gerava picos de concorrência que bloqueavam a fila de I/O e causavam travamentos em operações interativas de interface.
3. **Timeouts repetitivos de inicialização e probes de catálogo de modelos ACP (`#41976`):**
   A cada inicialização de agente ou sessão de modelo, o app executava probes síncronos de ~2s por executável e configuração para
   descobrir capacidades e catálogo de modelos. Quando agentes invocavam ferramentas rápidas em sequência, a latência acumulada
   desencadeava timeouts na camada ACP e atrasava a primeira resposta ao operador.
4. **Degradação e travamento na inicialização por retenção do histórico FTS (`#41948`):**
   A rotina de retenção de busca do Session History varria a tabela completa de mensagens do SQLite FTS sem paginação fixa durante
   o startup, retendo locks no banco e atrasando a prontidão do aplicativo em instalações com dezenas de milhares de turnos indexados.
5. **Incapacidade de controlar rolagem de abas e terminais programaticamente via RPC (`#41946`, `#41934`):**
   Clientes locais, utilitários de CLI, painéis de plugins e dispositivos externos (como stream decks ou rotaries) não dispunham
   de um método RPC dedicado para rolar programaticamente abas de terminal, logs ou visualizações de chat ativas, forçando
   interações frágeis baseadas em teclas simuladas.
6. **Travamentos no loop de eventos por leitura/gravação síncrona de servidores remotos salvos (`#42253`):**
   O aplicativo lia e salvava repetidamente arquivos de configuração de servidores SSH/pareados na thread principal do processo
   desktop e do daemon do servidor, congelando a interface gráfica quando operações de disco local ou rede apresentavam lentidão.
7. **Bloqueio de descoberta de modelos para todos os agentes por travamento em uma CLI (`#42247`):**
   Durante checagens de catálogos de modelos, se dois comandos de agentes demorassem a responder ou congelassem, todas as vagas
   compartilhadas de descoberta eram consumidas, impedindo que outros agentes e contas carregassem seus modelos.
8. **I/O síncrono de extensões bloqueando o processo principal (`#42189`):**
   Extensões do navegador que gravavam configurações via `chrome.storage.sync` ou regras de bloqueio via `declarativeNetRequest`
   forçavam gravações em disco síncronas com dupla confirmação na thread principal, travando a renderização do app.

## O que o upstream implementa

- **Host independente para chats nativos e agentes locais (`#41917`):**
  - Migra a execução de chats locais no macOS e workers de subagentes para o processo de host independente ("Orca Agents" / `BrzA Agents`);
  - Isola o consumo de heap e a gestão de ciclo de vida de memória dos agentes fora da thread do Electron, mantendo o Studio responsivo mesmo com dezenas de sessões ativas.
- **Admissão e cotas de leitura Git com priorização (`#41927`, resolve STA-14967):**
  - Implementa semáforos de admissão de Git que limitam a concorrência de leituras durante rajadas de criação de worktrees;
  - Separa workers de checkout em filas de menor prioridade e concede preferência imediata a requisições interativas da UI.
- **Cache durável do catálogo de modelos por executável/config (`#41976`, resolve STA-13482):**
  - Adiciona cache durável indexado pela tupla executável/configuração, eliminando sondagens repetidas de 2 segundos;
  - Revalida apenas mediante alteração de binário ou expiração do TTL, extinguindo timeouts frequentes da camada ACP.
- **Varredura bounded de retenção de histórico FTS em páginas de 256 (`#41948`):**
  - Divide a limpeza e expiração de turnos de busca do Session History em lotes limitados de 256 itens;
  - Evita bloqueios de inicialização no SQLite WAL e garante que a UI suba sem atrasos perceptíveis.
- **Método RPC `session.tabs.scroll` para rolagem programática (`#41946`, resolve `#41934`):**
  - Expõe endpoint RPC `session.tabs.scroll` suportando deslocamentos direcionais e absolutos em abas visíveis de terminal e chat;
  - Permite controle fluido via CLI, scripts de automação e integrações de hardware.
- **I/O assíncrono para leitura e gravação de servidores salvos (`#42253`):**
  - Move as operações de leitura e gravação de servidores pareados para workers fora da thread principal do desktop e servidor, impedindo que I/O lento congele a UI.
- **Isolamento de probes de modelos para evitar bloqueio global (`#42247`):**
  - Garante que probes demorados ou travados em uma CLI de agente não monopolizem os slots de descoberta, permitindo que outros agentes e contas obtenham suas listas normalmente.
- **Gravação em background de armazenamento de extensões do navegador (`#42189`):**
  - Desacopla as gravações de `chrome.storage.sync` e `declarativeNetRequest` do processo principal, eliminando travamentos de renderização causados por extensões.

## O que fazer

- Mover leitura e escrita de servidores salvos para fora da thread principal (`#42253`).
- Isolar probes de modelos de agentes para que travamentos em uma CLI não impeçam descoberta dos demais (`#42247`).
- Deslocar a persistência de configurações de extensões do navegador para background I/O (`#42189`).
- Adotar a separação de chats e agentes sob o host independente (`#41917`), alinhando o `brza-studio` ao modelo de isolamento de memória de subprocessos.
- Incorporar o controle de admissão e filas de leitura Git (`#41927`) nas rotinas de criação e clone de workspaces do `brza-workflow`.
- Adotar o cache persistente de modelos por executável (`#41976`) para acelerar a inicialização de agentes e conexões ACP.
- Portar a paginação limitada (256 itens) na retenção do Session History FTS (`#41948`).
- Expor e documentar o método RPC `session.tabs.scroll` (`#41946`) no ecossistema de ferramental e CLI do BrzA.
