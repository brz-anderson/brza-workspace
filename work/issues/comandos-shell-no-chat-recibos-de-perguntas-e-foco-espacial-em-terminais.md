---
status: open
description: Os PRs #41015, #40870, #40620, #40432 e a issue #41009 trazem foco no split ativo via Cmd+J, splits RPC em background, reset de mouse em PTY e shell ! no chat.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#41015`](https://github.com/stablyai/orca/pull/41015) (resolve Issue [`#41010`](https://github.com/stablyai/orca/issues/41010)),
[`stablyai/orca#40870`](https://github.com/stablyai/orca/pull/40870) (resolve Issue [`#40868`](https://github.com/stablyai/orca/issues/40868)),
[`stablyai/orca#40620`](https://github.com/stablyai/orca/pull/40620) (resolve Issue [`#32165`](https://github.com/stablyai/orca/issues/32165)),
[`stablyai/orca#40432`](https://github.com/stablyai/orca/pull/40432),
[`stablyai/orca#40424`](https://github.com/stablyai/orca/pull/40424),
[`stablyai/orca#40420`](https://github.com/stablyai/orca/pull/40420) (resolve Issue [`#40408`](https://github.com/stablyai/orca/issues/40408)),
[`stablyai/orca#40404`](https://github.com/stablyai/orca/pull/40404),
[`stablyai/orca#40412`](https://github.com/stablyai/orca/pull/40412) (resolve Issue [`#39864`](https://github.com/stablyai/orca/issues/39864)),
[`stablyai/orca#40405`](https://github.com/stablyai/orca/pull/40405) (resolve Issue [`#40402`](https://github.com/stablyai/orca/issues/40402)) e
[`stablyai/orca#40398`](https://github.com/stablyai/orca/pull/40398) (resolve Issue [`#12572`](https://github.com/stablyai/orca/issues/12572)),
além da issue [`stablyai/orca#41009`](https://github.com/stablyai/orca/issues/41009).

## O problema

1. **Submissão inadvertida ou execução desconectada de comandos shell `!` no chat (`#40620`, `#40432`, resolve `#32165`):**
   No TUI do Claude Code, digitar `! <comando>` executa a linha diretamente na bash local. No Native Chat estruturado do Orca,
   linhas iniciadas por `!` eram enviadas ao modelo como mensagens normais, gastando um turno de raciocínio da IA,
   poluindo o transcript da conversa e arriscando vazar credenciais ou segredos emitidos na saída do comando. Além disso,
   apenas abrir uma aba de terminal externa quebrava o fluxo de conversação do usuário, exigindo alternância de abas para
   inspecionar o resultado do comando e copiar manualmente o output de volta para a IA.
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
8. **Perda de foco do painel dividido ativo ao selecionar aba de terminal via `Cmd+J` (`#41015`, resolve `#41010`):**
   Ao navegar para uma aba de terminal que possui splits usando o seletor `Cmd+J`, o foco era atribuído cegamente ao primeiro
   painel (`first pane`) em vez de restaurar o painel que estava ativo antes da abertura da paleta.
9. **Captura indevida de foco por splits de terminal criados via RPC (`#40870`, resolve `#40868`):**
   Quando agentes ou scripts de extensão invocavam o método RPC `terminal.split`, a nova divisão ativava imediatamente a aba
   e o painel, roubando o foco do teclado do desenvolvedor enquanto este digitava em outra aba.
10. **Injeção de sequências de escape de mouse no prompt após restauração a frio de painéis (`#41009`):**
    Quando um painel de terminal era restaurado a frio após a terminação inesperada de um agente, os modos de rastreamento de mouse
    e foco (`\e[?1000h`, `\e[?1002h`, etc.) permaneciam ativados no PTY, fazendo com que movimentos do mouse ou cliques
    injetassem sequências brutas como `^[[<35;20;10M` no prompt do shell.

## O que o upstream implementa e corrige

- **Execução inline de comandos shell `!` diretamente no Chat UI (`#40620`, estende `#40432`):**
  - Implementa modo shell inline acionado por `!` no composer do chat;
  - Executa o comando via pipes no processo local/remoto do workspace sem abrir abas extras de terminal;
  - Exibe streaming de saída em tempo real no próprio chat com botão "Stop" (cancelamento via sinal de processo), ordenação estrita entre stdout/stderr (com stderr colorido) e virtualização de listas com `content-visibility` para buffers gigantes (até 60k–100k linhas sem engasgos);
  - Mantém persistência de diretório de trabalho (`cd`) dentro do workspace ao longo de comandos subsequentes;
  - Adiciona cartão com botão opcional "Add to chat", permitindo injetar o resultado do comando como contexto do próximo prompt para o agente apenas se o usuário desejar, preservando tokens e sigilo de credenciais.
- **Execução de comandos shell `!` em aba de terminal dedicada a partir do chat (`#40432`):**
  - O analisador `nativeChatShellCommand` detecta drafts iniciados por `!` no composer estruturado e permite transbordar a execução para uma nova aba de terminal caso o comando exija PTY interativo ou longa duração (>120s).
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
- **Restauração de foco na folha ativa de split via Cmd+J (`#41015`, resolve `#41010`):**
  - Ao ativar uma aba de terminal dividida através da paleta de abas do workspace (`Cmd+J`), passa `terminalLayoutsByTabId[entityId].activeLeafId`
    para `focusTerminalTabSurface`, preservando exatamente o painel de terminal ativo anterior.
- **Criação de splits de terminal via RPC em background (`#40870`, resolve `#40868`):**
  - Define `activate: false` na fronteira de chamadas RPC de `terminal.split`, garantindo que divisões requisitadas por scripts,
    ferramentas ou agentes ocorram em segundo plano sem desviar o foco do usuário.
- **Reset de modos de escape de mouse e foco em PTYs restaurados (`#41009`):**
  - Propõe emitir sequências de desarme de mouse (`\e[?1000l`, `\e[?1002l`, `\e[?1006l`) e foco (`\e[?1004l`) ao reiniciar
    ou restaurar a frio terminais cujos agentes morreram, evitando poluição de caracteres de coordenadas no prompt.

## O que fazer no BrzA Studio

1. Preservar o foco no painel dividido ativo ao selecionar abas via `Cmd+J` (`#41015`).
2. Manter divisões de terminal por RPC em segundo plano com `activate: false` (`#40870`).
3. Resetar modos de escape de mouse e foco em PTYs restaurados a frio (`#41009`).
4. Adotar a execução inline de comandos shell `!` no Chat UI com streaming, cancelamento e injeção opcional de contexto via "Add to chat" (`#40620`), mantendo transbordo opcional para aba de terminal (`#40432`).
5. Adotar os recibos expansíveis para prompts de perguntas com alternativas (`#40424`).
6. Disponibilizar a ação `workspace.sleep` nos atalhos globais de teclado (`#40420`).
7. Implementar a navegação direcional espacial entre splits de terminais via `Cmd+Option+Setas` (`#40404`).
8. Incorporar a verificação de múltiplas janelas de cota antes do auto-continue em Native Chat (`#40412`).
9. Aplicar a atualização de modelo em sessões ociosas do Claude (`#40405`) e o upload automático de anexos em sessões pareadas (`#40398`).
