---
status: open
description: Os PRs #44791, #43529, #39831 trazem foco no split ao cancelar fechamento, retenção de conversas através de sleep/wake e delimitação de links entre parênteses.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#44791`](https://github.com/stablyai/orca/pull/44791) (resolve Issue [`#44783`](https://github.com/stablyai/orca/issues/44783)),
[`stablyai/orca#43529`](https://github.com/stablyai/orca/pull/43529),
[`stablyai/orca#39831`](https://github.com/stablyai/orca/pull/39831),
[`stablyai/orca#44624`](https://github.com/stablyai/orca/pull/44624) (refs Issue [`#44586`](https://github.com/stablyai/orca/issues/44586)),
[`stablyai/orca#43901`](https://github.com/stablyai/orca/pull/43901),
[`stablyai/orca#43896`](https://github.com/stablyai/orca/pull/43896),
[`stablyai/orca#43889`](https://github.com/stablyai/orca/pull/43889),
[`stablyai/orca#43593`](https://github.com/stablyai/orca/pull/43593),
[`stablyai/orca#43574`](https://github.com/stablyai/orca/pull/43574) (resolve Issue [`#43573`](https://github.com/stablyai/orca/issues/43573)),
[`stablyai/orca#43479`](https://github.com/stablyai/orca/pull/43479),
[`stablyai/orca#43431`](https://github.com/stablyai/orca/pull/43431),
[`stablyai/orca#42651`](https://github.com/stablyai/orca/pull/42651),
[`stablyai/orca#43388`](https://github.com/stablyai/orca/pull/43388) (resolve Issue [`#43387`](https://github.com/stablyai/orca/issues/43387)),
[`stablyai/orca#43393`](https://github.com/stablyai/orca/pull/43393),
[`stablyai/orca#41015`](https://github.com/stablyai/orca/pull/41015) (resolve Issue [`#41010`](https://github.com/stablyai/orca/issues/41010)),
[`stablyai/orca#40870`](https://github.com/stablyai/orca/pull/40870) (resolve Issue [`#40868`](https://github.com/stablyai/orca/issues/40868)),
[`stablyai/orca#40620`](https://github.com/stablyai/orca/pull/40620) (resolve Issue [`#32165`](https://github.com/stablyai/orca/issues/32165)),
[`stablyai/orca#40432`](https://github.com/stablyai/orca/pull/40432),
[`stablyai/orca#40424`](https://github.com/stablyai/orca/pull/40424),
[`stablyai/orca#40420`](https://github.com/stablyai/orca/pull/40420) (resolve Issue [`#40408`](https://github.com/stablyai/orca/issues/40408)),
[`stablyai/orca#40404`](https://github.com/stablyai/orca/pull/40404),
[`stablyai/orca#40412`](https://github.com/stablyai/orca/pull/40412) (resolve Issue [`#39864`](https://github.com/stablyai/orca/issues/39864)),
[`stablyai/orca#40405`](https://github.com/stablyai/orca/pull/40405) (resolve Issue [`#40402`](https://github.com/stablyai/orca/issues/40402)) e
[`stablyai/orca#40398`](https://github.com/stablyai/orca/pull/40398) (resolve Issue [`#12572`](https://github.com/stablyai/orca/issues/12572)),
além da issue [`stablyai/orca#44012`](https://github.com/stablyai/orca/issues/44012) (resolvida no commit `1615e5c`) e
da issue [`stablyai/orca#41009`](https://github.com/stablyai/orca/issues/41009).

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
11. **Falta de flexibilidade para mover abas para splits em qualquer direção (`#43431`):**
    O comando de mover aba para divisão não permitia associar atalhos direcionais customizados para cada sentido cardeal (esquerda, direita, acima ou abaixo).
12. **Processos de terminal persistindo ao fechar aba via CLI se a janela não confirmar (`#43479`):**
    Ao invocar o comando de fechamento de terminal via CLI, caso a janela não confirmasse o fechamento por estar ocupada ou em segundo plano, o processo do terminal continuava vivo consumindo recursos.
13. **Ausência de suporte CLI para fechar aba de terminal parada por ID (`#42651`):**
    Não havia instrução CLI para localizar e encerrar diretamente abas de terminais já parados indicando seu identificador único.
14. **Congelamento de entrada de teclado no terminal Unix sob sobrecarga de I/O workers (`#43593`):**
    No Unix, os dados de digitação do teclado enviados ao PTY eram despachados pela fila comum de workers de I/O. Caso operações pesadas em disco ou tarefas de background saturassem o pool de workers, a digitação travava e caracteres eram engolidos ou entregues com atrasos severos.
15. **Retomada concorrente espúria de conversas de agente ao restaurar abas salvas (`#43574`, resolve `#43573`):**
    Ao reabrir ou restaurar abas salvas de terminal, o ambiente tentava retomar automaticamente a sessão do agente salva, mesmo que essa mesma conversa já estivesse ativa em outra aba ou janela, gerando conflitos de concorrência e corrupção de estado.
16. **Perda ou corrupção de entradas enfileiradas de terminal antes do agente estar pronto (`#43896`):**
    Entradas enviadas para o terminal via CLI (`orca terminal wait --for tui-idle` seguido de `send`) ou mensagens de correio de orquestração eram consumidas antes do agente estar apto a recebê-las. Hooks lentos de shell (como zsh preexec) ou inicializações a frio faziam com que o texto fosse interpretado pelo shell ou descartado.
17. **Corrupção de tela em terminais ocultos após descarte de buffer (`#43889`):**
    Quando um terminal em aba oculta gerava grande volume de saída rapidamente, o daemon descartava pacotes para evitar buffer bloat. Ao voltar para a aba, o estado da tela ficava corrompido ou com linhas cortadas.
18. **Consumo contínuo de CPU por polling acelerado de processos em painéis de agentes ociosos (`#43901`):**
    O renderer mantinha um loop de polling de foreground process a cada 750 ms em todas as abas onde um agente já havia rodado, gerando drenagem de bateria desnecessária mesmo com agentes em repouso absoluto.
19. **Dupla submissão de respostas em perguntas assíncronas do Codex durante o handoff da fila (`#44012`, commit `1615e5c`):**
    Quando o usuário respondia a uma pergunta interativa assíncrona (`ask_question`) do Codex e a mensagem entrava no handoff de enfileiramento (*queue handshake*), o card de pergunta não travava imediatamente o estado dos botões. Clicar novamente ou submeter em rápida sucessão permitia enviar respostas duplicadas ou respostas conflitantes antes da confirmação da fila, corrompendo o fluxo conversacional do agente.
20. **Fechamento e perda indevida da aba de terminal ao reiniciar o painel PTY (`#44624`, refs `#44586`):**
    Quando um painel de terminal era reiniciado e a instância anterior do PTY era descartada antes que o novo processo de substituição estivesse totalmente instanciado, o renderer enviava uma mensagem genérica `pty:kill`. O processo principal tratava esse encerramento como uma solicitação voluntária de fechamento por parte do usuário e aposentava a aba correspondente, fechando a aba sem que o desenvolvedor tivesse pedido.
21. **Perda de foco e fechamento em cascata de abas após cancelar fechamento de terminal split (`#44791`, resolve `#44783`):**
    O modal de confirmação de fechamento de terminal (`CloseTerminalDialog`) era aberto pelo estado do React sem gatilho de foco do Radix. Ao clicar em Cancelar, apertar Escape ou fechar clicando fora, o foco do teclado caía no `document.body`. Ao pressionar Cmd+W / Ctrl+W em seguida, o atalho caía no manipulador de nível de aba e fechava todos os splits de uma vez.
22. **Perda do vínculo de conversas de agentes em painéis de terminal através de ciclos de repouso e despertar (*sleep/wake*) (`#43529`):**
    Quando um workspace entrava em repouso (*workspace sleep*), o PTY do terminal era terminado. Ao despertar o workspace, os ganchos do agente não conseguiam reconectar a linha de status e o identificador da conversa ao novo PTY, gerando painéis zumbis desconectados do histórico do agente.
23. **Detecção incorreta de links clicáveis de arquivos englobando texto em prosa adjacente a parênteses (`#39831`):**
    Quando caminhos de arquivo apareciam delimitados por parênteses no terminal (ex.: `(src/auth/session.ts)` ou `(ver detalhes em src/index.ts:25)`), a regex de detecção de links OSC 8 incluía os parênteses de fechamento ou a prosa subsequente na URL do link, quebrando a navegação por clique.

## O que o upstream implementa e corrige

- **Restauração de foco no split ativo após cancelamento de modal de terminal (`#44791`, resolve `#44783`):**
  - Integra o hook `useModalReturnFocus` ao `CloseTerminalDialog`, assegurando que Cancelar, Escape ou dismiss fora do modal retornem o foco exatamente para o painel de terminal dividido ativo em vez de vazar para o body.
- **Continuidade de conversas de agentes em painéis de terminal através de sleep e wake (`#43529`):**
  - Implementa registro durável de turnos e identificadores de conversa (`pane-agent-identity.ts` e `worktree-sleep-resume-recording.ts`), permitindo que a reconexão pós-despertar re-vincule a conversa do agente ao novo PTY do painel sem perda de contexto ou linhas de status.
- **Delimitação estrita de caminhos de arquivos entre parênteses no terminal (`#39831`):**
  - Ajusta o detector de links (`terminal-file-link-detection-ranges.ts`) para encerrar a captura do caminho no parêntese de fechamento não correspondido sem exigir espaço anterior, ignorando prosa subsequente.
- **Preservação de abas de terminal ao reiniciar marcando PTY como `replacedByRestart` (`#44624`, refs `#44586`):**
  - O renderer passa o parâmetro `replaced: true` durante o descarte de PTYs vinculados a um reinício de painel;
  - O processo principal roteia o encerramento através de `stopReplacedPanePty`, marcando a saída do processo antigo como `replacedByRestart` e mantendo a aba intacta na interface enquanto o novo PTY é inicializado.
- **Bloqueio imediato de cartões de pergunta assíncrona durante o queue handoff (`#44012`, commit `1615e5c`):**
  - Trava os controles e botões de resposta imediatamente após o primeiro envio, mantendo-os desabilitados durante todo o aperto de mão da fila (*queued-handshake*);
  - Impede submissões concorrentes ou cliques repetidos enquanto o turno do Codex está sendo despachado.
- **Escrita direta não bloqueante para entrada de teclado em PTYs Unix (`#43593`):**
  - Escreve caracteres do teclado diretamente no file descriptor do PTY Unix de forma síncrona e não bloqueante (`O_NONBLOCK`), desacoplando o pipeline de digitação do pool geral de workers de I/O e garantindo resposta instantânea mesmo sob carga pesada do sistema.
- **Prevenção de auto-resume duplicado ao restaurar abas salvas (`#43574`, resolve `#43573`):**
  - Ao restaurar uma aba salva que referenciava uma sessão de agente, verifica se a conversa correspondente já está ativa em qualquer outra aba ou superfície; se estiver, abre um shell limpo no diretório de trabalho em vez de forçar um segundo resume concorrente.
- **Atalhos customizáveis para mover abas para splits em todas as direções (`#43431`):**
  - Torna a ação `Move Tab to Split` configurável com direções explícitas (esquerda, direita, cima e baixo) no mapa de atalhos.
- **Encerramento forçado de processos de terminal no fechamento CLI sem confirmação (`#43479`):**
  - Interrompe o processo PTY subjacente diretamente caso a janela da aplicação não confirme o fechamento da aba.
- **Fechamento de abas paradas via CLI por ID (`#42651`):**
  - Adiciona suporte no CLI para fechar abas de terminais parados fornecendo o ID da aba correspondente.
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
- **Retenção de entrada de terminal enfileirada até prontidão real do agente (`#43896`):**
  - Segura o buffer de digitação e mensagens de orquestração enfileiradas até que o agente em execução confirme prontidão, evitando que comandos sejam engolidos por inicializações a frio, hooks de preexec do shell ou reaproveitamento de painéis.
- **Reconstrução de tela de terminal oculto a partir do daemon (`#43889`):**
  - Ao reativar uma aba oculta que sofreu descarte de frames sob alta vazão de saída, reconstrói o frame completo a partir do buffer durável mantido pelo daemon do terminal.
- **Polling adaptativo de 15s para processos em painéis ociosos (`#43901`):**
  - Reduz a frequência de verificação de processos de 750 ms para 15 s quando o painel do agente está em repouso, reduzindo significativamente o consumo de CPU em background.
- **Execução em um clique de linhas `! command` sugeridas por agentes (`#43388`, `#43393`, resolve `#43387`):**
  - No terminal integrado e no aplicativo móvel, detecta linhas no formato `! command` emitidas pelo agente como sugestões executáveis;
  - Renderiza um botão de ação rápida/chip que permite ao usuário disparar o comando no terminal com um único clique ou toque, sem copiar/colar manualmente.

## O que fazer no BrzA Studio

1. Habilitar a execução em um clique de linhas `! command` sugeridas por agentes no terminal e no mobile (`#43388`, `#43393`, resolve `#43387`).
2. Preservar o foco no painel dividido ativo ao selecionar abas via `Cmd+J` (`#41015`).
3. Manter divisões de terminal por RPC em segundo plano com `activate: false` (`#40870`).
4. Resetar modos de escape de mouse e foco em PTYs restaurados a frio (`#41009`).
5. Adotar a execução inline de comandos shell `!` no Chat UI com streaming, cancelamento e injeção opcional de contexto via "Add to chat" (`#40620`), mantendo transbordo opcional para aba de terminal (`#40432`).
6. Adotar os recibos expansíveis para prompts de perguntas com alternativas (`#40424`).
7. Disponibilizar a ação `workspace.sleep` nos atalhos globais de teclado (`#40420`).
8. Implementar a navegação direcional espacial entre splits de terminais via `Cmd+Option+Setas` (`#40404`).
9. Incorporar a verificação de múltiplas janelas de cota antes do auto-continue em Native Chat (`#40412`).
10. Aplicar a atualização de modelo em sessões ociosas do Claude (`#40405`) e o upload automático de anexos em sessões pareadas (`#40398`).
11. Permitir atalhos direcionais customizados para mover abas para divisões (Move Tab to Split) em todas as direções cardeais (`#43431`).
12. Forçar a interrupção de processos de terminal na CLI de fechamento quando a janela gráfica não responder (`#43479`).
13. Suportar comando de CLI para fechar diretamente abas de terminais parados por ID (`#42651`).
14. Adotar escrita direta não bloqueante para entrada de teclado em PTYs Unix desacoplando do pool de I/O workers (`#43593`).
15. Evitar auto-resume duplicado ao restaurar abas salvas caso a conversa já esteja ativa em outra aba ou janela (`#43574`, resolve `#43573`).
16. Reter entradas enfileiradas de terminal até confirmação de prontidão do agente em execução (`#43896`).
17. Reconstruir tela de terminais ocultos a partir do histórico do daemon após descartes de saída (`#43889`).
18. Adotar polling adaptativo de 15s para processos de primeiro plano em abas ociosas de agentes (`#43901`).
19. Travar cartões de perguntas assíncronas imediatamente no clique inicial para evitar submissões duplicadas durante o queue handoff do Codex (`#44012`, commit `1615e5c`).
20. Preservar abas de terminais durante reinicializações de painéis marcando o descarte do PTY antigo como `replacedByRestart` (`#44624`, refs `#44586`).
21. Retornar foco ao split de terminal ativo após cancelar ou fechar o diálogo de confirmação de fechamento (`#44791`, resolve `#44783`).
22. Preservar a identidade e linha de status de conversas de agentes em terminais através de repouso e despertar (*sleep/wake*) (`#43529`).
23. Ajustar limites de detecção de links de arquivos no terminal para ignorar parênteses de fechamento e prosa adjacente (`#39831`).


