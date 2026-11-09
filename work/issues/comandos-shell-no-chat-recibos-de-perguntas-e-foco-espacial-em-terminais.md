---
status: open
description: Os PRs #40432, #40424, #40420, #40404, #40412 trazem execução de shell ! no chat, recibos expansíveis de perguntas, foco espacial e atalho de repouso.
scope:
  - brza-studio
  - workspace
  - brza-workflow
priority: high
opened: 2026-11-09
tags:
  - chat
  - tooling
  - design
---

# Comandos shell no chat, recibos de perguntas e foco espacial em terminais

Rastreado dos PRs abertos no upstream [`stablyai/orca#40432`](https://github.com/stablyai/orca/pull/40432) (resolve Issue [`#32165`](https://github.com/stablyai/orca/issues/32165)),
[`stablyai/orca#40424`](https://github.com/stablyai/orca/pull/40424),
[`stablyai/orca#40420`](https://github.com/stablyai/orca/pull/40420) (resolve Issue [`#40408`](https://github.com/stablyai/orca/issues/40408)),
[`stablyai/orca#40404`](https://github.com/stablyai/orca/pull/40404),
[`stablyai/orca#40412`](https://github.com/stablyai/orca/pull/40412) (resolve Issue [`#39864`](https://github.com/stablyai/orca/issues/39864)),
[`stablyai/orca#40405`](https://github.com/stablyai/orca/pull/40405) (resolve Issue [`#40402`](https://github.com/stablyai/orca/issues/40402)) e
[`stablyai/orca#40398`](https://github.com/stablyai/orca/pull/40398) (resolve Issue [`#12572`](https://github.com/stablyai/orca/issues/12572)).

## O problema

1. **Submissão inadvertida de comandos shell `!` como prompts para a LLM (`#40432`, resolve `#32165`):**
   No TUI do Claude Code, digitar `! <comando>` executa a linha diretamente na bash local. No Native Chat estruturado do Orca,
   linhas iniciadas por `!` eram enviadas ao modelo como mensagens normais, gastando um turno de raciocínio da IA,
   poluindo o transcript da conversa e arriscando vazar credenciais ou segredos emitidos na saída do comando.
2. **Perda de visibilidade das alternativas não selecionadas em perguntas interativas (`#40424`):**
   Após responder a uma pergunta de múltipla escolha (`ask_question`), o recibo de resolução na conversa exibia apenas a resposta
   escolhida. Usuários e revisores não tinham como inspecionar o leque de opções originalmente ofertadas pelo agente.
3. **Ausência de atalho de teclado para colocar workspaces em repouso (`#40420`, resolve `#40408`):**
   Para liberar memória e suspender processos de um workspace sem fechá-lo, o desenvolvedor era forçado a usar o mouse, clicar
   com botão direito no cartão da barra lateral e selecionar "Sleep". Não havia atalho configurável para suspender o workspace ativo
   ou o cartão sob o cursor.
4. **Navegação rígida e não espacial entre splits de terminais (`#40404`):**
   A única forma de alternar entre divisões de terminal pelo teclado era `Cmd+[` / `Cmd+]`, que navega na ordem cronológica de
   criação das abas, ignorando o arranjo visual na tela. Atalhos espaciais intuitivos (`Cmd+Option+Setas`) não existiam para focar
   painéis adjacentes (esquerda, direita, cima, baixo).
5. **Retomada automática cega em chats limitados colidindo com janelas semanais (`#40412`, resolve `#39864`):**
   Ao atingir limite de cota com "Continue automatically" ativo, o chat enviava a retomada imediatamente ao reset da janela de 5 horas,
   mesmo que a cota semanal da conta continuasse esgotada. Isso disparava um novo erro de rate limit imediato e desnecessário.
6. **Reversão espúria de seleção de modelo em sessões ociosas do Claude (`#40405`, resolve `#40402`):**
   Ao alterar o modelo de IA no seletor do Native Chat enquanto o Claude estava ocioso, o adaptador não repassava a escolha
   (`canSetOptionWhileIdle` ausente), e o combobox revertia para o modelo anterior na leitura de opções seguinte.
7. **Recusa de arquivos locais arrastados para chats remotos pareados (`#40398`, resolve `#12572`):**
   Em chats vinculados a terminais rodando em servidores Orca remotos, arrastar um arquivo ou usar o botão `+` era recusado com
   "Local attachments are not available for remote sessions", obrigando transferências manuais via SCP/SSH.

## O que o upstream implementa e corrige

- **Execução de comandos shell `!` em aba de terminal dedicada a partir do chat (`#40432`):**
  - O analisador `nativeChatShellCommand` detecta drafts iniciados por `!` no composer estruturado;
  - Ao pressionar Enter, abre automaticamente uma nova aba de terminal no workspace correspondente com o comando como startup command;
  - O comando nunca é transmitido para a LLM nem registrado no transcript, preservando tokens e sigilo de saídas sensíveis.
- **Recibos de resolução expansíveis com histórico de opções (`#40424`):**
  - Armazena metadados de todas as opções oferecidas em `NativeChatReceiptAnswers`;
  - Renderiza o recibo como um disclosure expansível inline, permitindo abrir a lista completa de escolhas com a selecionada marcada em negrito e checkmark.
- **Atalho configurável `workspace.sleep` para suspender workspaces (`#40420`):**
  - Adiciona o comando `workspace.sleep` em `Settings → Shortcuts` (grupo Global, customizável em todas as plataformas);
  - Suspende o workspace sob o cursor do mouse, os cartões selecionados em lote ou o workspace ativo, reutilizando a confirmação unificada `requestWorkspaceSleep`.
- **Navegação espacial entre splits de terminal (`#40404`):**
  - Introduz `terminal.focusPaneLeft/Right/Up/Down`, mapeados por padrão para `Mod+Alt+Setas` (`Cmd+Option+Setas` no macOS);
  - Adota o algoritmo de adjacência do Windows Terminal, focando o painel visualmente adjacente na borda compartilhada e delegando para o histórico de navegação apenas nos extremos do layout.
- **Retenção de auto-continue até liberação comprovada de cota de conta (`#40412`):**
  - O loop de monitoramento verifica as leituras reais de cota nas janelas de 5h, semanal e mensal da conta antes de disparar o "Continue where you left off", recalculando a espera caso a janela semanal permaneça bloqueada.
- **Aplicação imediata de troca de modelo em sessões ociosas do Claude (`#40405`):**
  - Habilita `canSetOptionWhileIdle` no adaptador estruturado do Claude, invocando `connection.setModel` em repouso e mantendo o seletor sincronizado.
- **Upload transparente de arquivos arrastados para sessões remotas pareadas (`#40398`):**
  - Implementa `fs:uploadPathsToRuntimeTempFiles`, transmitindo arquivos arrastados para pastas temporárias seguras do servidor remoto pareado e inserindo os caminhos remotos válidos no prompt do agente.

## O que fazer no BrzA Studio

1. Integrar o despacho de comandos shell `!` do chat para novas abas de terminal (`#40432`), evitando vazamento de dados locais para modelos de IA.
2. Adotar os recibos expansíveis para prompts de perguntas com alternativas (`#40424`).
3. Disponibilizar a ação `workspace.sleep` nos atalhos globais de teclado (`#40420`).
4. Implementar a navegação direcional espacial entre splits de terminais via `Cmd+Option+Setas` (`#40404`).
5. Incorporar a verificação de múltiplas janelas de cota antes do auto-continue em Native Chat (`#40412`).
6. Aplicar a atualização de modelo em sessões ociosas do Claude (`#40405`) e o upload automático de anexos em sessões pareadas (`#40398`).
