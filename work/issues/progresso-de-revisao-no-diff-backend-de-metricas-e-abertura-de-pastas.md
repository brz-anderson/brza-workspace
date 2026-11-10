---
status: open
description: Os PRs #40776, #40792, #40818, #40627 e as issues #40789, #40786 trazem progresso de revisão no diff, backend de métricas e abertura de pastas.
scope:
  - brza-studio
  - brza-workflow
  - workspace
priority: high
opened: 2026-11-10
tags:
  - tooling
  - infra
  - design
---

# Progresso de revisão no diff, backend de métricas e abertura de pastas

Rastreado dos PRs abertos no upstream [`stablyai/orca#40776`](https://github.com/stablyai/orca/pull/40776) (resolve Issue [`#40768`](https://github.com/stablyai/orca/issues/40768)),
[`stablyai/orca#40792`](https://github.com/stablyai/orca/pull/40792),
[`stablyai/orca#40818`](https://github.com/stablyai/orca/pull/40818) (resolve Issue [`#40675`](https://github.com/stablyai/orca/issues/40675)),
[`stablyai/orca#40627`](https://github.com/stablyai/orca/pull/40627),
[`stablyai/orca#40790`](https://github.com/stablyai/orca/pull/40790) (resolve Issue [`#40789`](https://github.com/stablyai/orca/issues/40789)),
[`stablyai/orca#40816`](https://github.com/stablyai/orca/pull/40816) e das issues
[`#40786`](https://github.com/stablyai/orca/issues/40786) e
[`#40787`](https://github.com/stablyai/orca/issues/40787).

## O problema

1. **Ausência de mapa e progresso de revisão arquivo a arquivo no diff (`#40776`, resolve `#40768`):**
   Ao revisar branches longos ou grandes pull requests no visualizador de diff do Studio, o revisor não dispunha de
   indicador de progresso persistente nem controle para marcar arquivos já inspecionados ("Viewed"). A cada recarregamento
   da aba ou alternância de arquivos, o fluxo reiniciava do zero, sem integração entre o diff e a lista de arquivos alterados
   no painel de Source Control.
2. **Contenção no processo principal e latência de timers por sondagem de métricas de uso (`#40792`, relacionado a `#40682`):**
   A coleta de métricas de uso (Claude, Codex, tokens e analytics) executava diretamente no processo principal do Electron,
   com mais de 30 handlers e varreduras bloqueando o event loop. Em frotas grandes, a latência de timers do processo principal
   chegava a mais de 1.800 ms, provocando engasgos gerais na digitação e na interface.
3. **Falha silenciosa ao clicar em links de pastas gerados pela IA no chat (`#40818`, resolve `#40675`):**
   Quando o modelo de IA citava um diretório (ex.: `src/components/` ou `/srv/repo/docs`), o link exibia o rótulo incorreto
   "Open file" e o clique não realizava nenhuma ação perceptível. Em workspaces remotos/pareados, a resolução de arquivos locais
   falhava silenciosamente e deixava o usuário sem feedback.
4. **Sobrecarga de I/O de disco por regravação completa do profile em movimentos de janela (`#40627`):**
   Cada movimentação de janela, redimensionamento ou pequena alteração visual disparava a serialização e gravação integral do
   snapshot de perfil no disco, gerando escritas desnecessárias e concorrência com o banco SQLite.
5. **Escape do comando Select All (Cmd+A) fora de notas Markdown focadas (`#40790`, resolve `#40789`):**
   Ao pressionar Cmd+A para selecionar todo o texto de uma nota Markdown aberta no editor, o foco vazava para elementos
   externos da janela ou selecionava o canvas inteiro em vez de restringir a seleção ao buffer do documento ativo.
6. **Perda da última aba fechada ao tentar reabrir a partir da tela de boas-vindas (`#40816`):**
   Após fechar todas as abas e cair na landing surface (*welcome screen*), acionar o atalho `Cmd+Shift+T` ("Reopen Closed Tab")
   não encontrava a última aba encerrada no histórico recente da sessão.
7. **Demanda por personas persistentes com governança, custos e segredos integrados (`#40786`):**
   Desenvolvedores e equipes demandam suporte nativo a personas persistentes de agentes com papéis explícitos, tarefas especializadas,
   árvore hierárquica e controle de custos e segredos por agente.

## O que o upstream implementa e corrige

- **Progresso de revisão por arquivo no diff compartilhado com Source Control (`#40776`):**
  - Adiciona controle `[x] Viewed` nos cabeçalhos individuais de diff e no cabeçalho do combined diff ("View all"), com atalho `Ctrl+V` no macOS (ou `Alt+Shift+V`);
  - Arquivos marcados como vistos são automaticamente recolhidos no modo combined diff e atenuados visualmente na árvore do Source Control;
  - Persiste em `orca.reviewed-diffs.v1` com invalidação barata baseada em assinatura de conteúdo, entry signature e modified time (até 5.000 registros e poda de 90 dias).
- **Serviços de métricas de uso em processo de backend supervisionado (`#40792`):**
  - Extrai os coletores de telemetria, cache de uso e analytics para um processo de backend dedicado via MessagePort;
  - Reduz a latência de timers do processo principal de 1.836 ms para 833 ms e o atraso p99 do event loop de 10,4 ms para 5,5 ms;
  - Reconexão transparente em caso de falha do processo secundário sem derrubar o Electron principal.
- **Abertura e revelação de links de diretórios no Chat UI (`#40818`, resolve `#40675`):**
  - Detecta caminhos terminados em barra como diretórios (`isDirectoryHint`), exibindo o rótulo "Open folder";
  - Revela a pasta no explorer do worktree correspondente (suportando ambientes locais e remotos pareados) ou foca a raiz do workspace;
  - Emite notificação de erro explícita caso o caminho não exista em vez de falha silenciosa.
- **Otimização de persistência de perfil em manipulações de janela (`#40627`):**
  - Desacopla mudanças transitórias de posição de janela e redimensionamento de gravações imediatas de perfil no disco.
- **Confinamento de Select All ao editor Markdown (`#40790`):**
  - Restringe o escopo de Cmd+A estritamente ao editor de notas ativo.
- **Restauração de abas fechadas a partir da tela de boas-vindas (`#40816`):**
  - Preserva a pilha de abas fechadas acessível mesmo quando a janela estiver vazia, permitindo que `Cmd+Shift+T` reabra a última aba.

## O que fazer no BrzA Studio

1. Adotar o controle de arquivos revisados `[x] Viewed` no diff e Source Control (`#40776`).
2. Avaliar a migração dos serviços de uso para processo de backend supervisionado (`#40792`) para sanar travamentos no macOS.
3. Adotar o reconhecimento e revelação de pastas a partir de links no chat (`#40818`).
4. Confinar o Select All ao editor Markdown (`#40790`) e habilitar reabertura de abas a partir do welcome screen (`#40816`).
5. Acompanhar a modelagem de Personas persistentes (`#40786`) para alinhar com o ecossistema `brza-sessions` e `meeting-runner`.
