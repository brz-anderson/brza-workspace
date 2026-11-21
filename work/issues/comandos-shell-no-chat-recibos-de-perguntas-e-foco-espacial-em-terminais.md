---
status: open
description: Os PRs #46105, #45759, #46156, #44476, #46206, #46168, #46157, #46145, #45068 e #45713 trazem suporte a #L em OSC 8, isolamento de abas e melhorias ergonômicas no terminal.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#46105`](https://github.com/stablyai/orca/pull/46105),
[`stablyai/orca#45759`](https://github.com/stablyai/orca/pull/45759),
[`stablyai/orca#46156`](https://github.com/stablyai/orca/pull/46156),
[`stablyai/orca#44476`](https://github.com/stablyai/orca/pull/44476),
[`stablyai/orca#46206`](https://github.com/stablyai/orca/pull/46206),
[`stablyai/orca#46168`](https://github.com/stablyai/orca/pull/46168),
[`stablyai/orca#46157`](https://github.com/stablyai/orca/pull/46157),
[`stablyai/orca#46145`](https://github.com/stablyai/orca/pull/46145),
[`stablyai/orca#45068`](https://github.com/stablyai/orca/pull/45068),
[`stablyai/orca#45713`](https://github.com/stablyai/orca/pull/45713),
[`stablyai/orca#44954`](https://github.com/stablyai/orca/pull/44954),
[`stablyai/orca#45978`](https://github.com/stablyai/orca/pull/45978),
[`stablyai/orca#45907`](https://github.com/stablyai/orca/pull/45907),
[`stablyai/orca#45472`](https://github.com/stablyai/orca/pull/45472),
[`stablyai/orca#45871`](https://github.com/stablyai/orca/pull/45871),
[`stablyai/orca#45837`](https://github.com/stablyai/orca/pull/45837),
[`stablyai/orca#45385`](https://github.com/stablyai/orca/pull/45385),
[`stablyai/orca#45702`](https://github.com/stablyai/orca/pull/45702),
[`stablyai/orca#45571`](https://github.com/stablyai/orca/pull/45571) (refs Issue [`#45563`](https://github.com/stablyai/orca/issues/45563)),
[`stablyai/orca#45783`](https://github.com/stablyai/orca/pull/45783) (resolve Issue [`#19595`](https://github.com/stablyai/orca/issues/19595)),
[`stablyai/orca#43785`](https://github.com/stablyai/orca/pull/43785),
[`stablyai/orca#45363`](https://github.com/stablyai/orca/pull/45363),
[`stablyai/orca#45446`](https://github.com/stablyai/orca/pull/45446),
[`stablyai/orca#45449`](https://github.com/stablyai/orca/pull/45449),
[`stablyai/orca#45454`](https://github.com/stablyai/orca/pull/45454),
[`stablyai/orca#45480`](https://github.com/stablyai/orca/pull/45480) (resolve Issue [`#45455`](https://github.com/stablyai/orca/issues/45455)),
[`stablyai/orca#45100`](https://github.com/stablyai/orca/pull/45100),
[`stablyai/orca#45101`](https://github.com/stablyai/orca/pull/45101),
[`stablyai/orca#45006`](https://github.com/stablyai/orca/pull/45006),
[`stablyai/orca#45064`](https://github.com/stablyai/orca/pull/45064),
[`stablyai/orca#45110`](https://github.com/stablyai/orca/pull/45110),
[`stablyai/orca#44460`](https://github.com/stablyai/orca/pull/44460) (refs Issue [`#31281`](https://github.com/stablyai/orca/issues/31281)),
[`stablyai/orca#44916`](https://github.com/stablyai/orca/pull/44916),
[`stablyai/orca#44673`](https://github.com/stablyai/orca/pull/44673),
[`stablyai/orca#44791`](https://github.com/stablyai/orca/pull/44791) (resolve Issue [`#44783`](https://github.com/stablyai/orca/issues/44783)),
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
24. **Perda do nome customizado de abas de terminal ao fechar e na retomada via histórico (`#44460`, refs `#31281`):**
    Renomear uma aba de terminal atribuía o nome apenas à aba aberta naquele momento. Ao fechar a aba, o histórico de sessões do agente (*Session History* / AI Vault) revertia para o título padrão do agente, e ao retomar a sessão (`/resume`), uma aba anônima e sem nome era criada, perdendo a identificação configurada pelo usuário.
25. **Rejeição de arquivos arrastados ou colados em chats de terminal em servidores pareados (`#44916`):**
    Em chats com backend de terminal executados em servidores pareados ou gerenciados, arrastar ou colar arquivos locais era rejeitado com a mensagem *"Local attachments are not available for remote sessions."*, enquanto o terminal adjacente conseguia fazer upload desses mesmos arquivos para `.orca/drops`.
26. **Loop de polling prematuro e inicialização desnecessária do app-server do Codex por MCPs não iniciados (`#44673`):**
    Antes de um chat do Codex ser iniciado, servidores MCP configurados eram colocados em estado pendente, disparando o polling de backoff do painel; cada verificação em um chat sem thread inicializava a frio o `codex app-server`, consumindo recursos e mantendo a lista travada.
27. **Comando de colar (Cmd+V) caindo no composer oculto do chat durante perguntas ativas (`#45100`):**
    Quando um card de pergunta interativa (`ask_question`) substituía o composer do chat, o editor oculto permanecia registrado como alvo de entrada do painel. Ao pressionar Cmd+V ou colar via menu de contexto, o texto era inserido no composer invisível e o campo de resposta da pergunta permanecia em branco.
28. **Atalhos de alternância de workspace bloqueados pelo editor de mensagens do chat (`#45101`):**
    Os acordes de navegação entre workspaces (`Mod+Shift+Up/Down`) ficavam presos no composer do chat como seletores de texto até o início/fim, impedindo ciclar workspaces rapidamente por teclado enquanto o foco estivesse no chat.
29. **Perda do botão "Approve once" em recusas de ferramentas do Codex acima de 16 KB (`#45006`):**
    Quando uma resposta de ferramenta ou recusa emitida pelo Codex excedia 16 KB, o payload bruto quebrava o limite de processamento de frames, removendo o botão "Approve once" e forçando o desenvolvedor a lidar com prompts não recuperáveis.
30. **Sobrescrita da linha superior do terminal por perda de pending-wrap no replay de snapshots (`#45064`):**
    Ao restaurar um snapshot de terminal gravado enquanto o cursor aguardava wrap na borda direita, o cursor era posicionado na linha home após a restauração dos modos de rolagem/origem, fazendo com que a saída subsequente sobrescrevesse as primeiras linhas da tela.
31. **Sequências de escape incompletas ou gigantes vazando texto bruto no terminal (`#45110`):**
    Sequências parciais de escape maiores que 4.096 caracteres (como imagens DCS ou payloads Base64 de OSC 52) eram truncadas para um carry vazio em cortes de fluxo ou snapshots, fazendo com que o restante do payload alcançasse o parser de texto e poluísse o terminal como prosa ilegível.
32. **Nomes de workers em linhas de chat sem botão ou chip direto de abertura (`#45363`):**
    Quando um chat coordenador ou mensagem referenciava um worker, o nome aparecia como texto puro sem permitir navegação direta ou abertura rápida do painel do worker associado.
33. **Deslocamento do ponto de ancoragem IME do Cursor Agent no terminal (`#45446`):**
    Durante a composição de caracteres via IME (Input Method Editor) no terminal do Cursor Agent, a caixa de candidatos do IME perdia a ancoragem espacial no prompt entre re-renderizações consecutivas, saltando para o topo ou fora da área visível.
34. **Sugestão esmaecida do prompt do Claude aparecendo como texto digitado sob o preedit IME (`#45449`):**
    Quando o usuário compunha caracteres em idiomas asiáticos/acentuados usando IME sobre o prompt do Claude, a sugestão esmaecida (*dim prompt suggestion*) permanecia visível sob o texto de composição pré-editado (*preedit*), gerando sobreposição visual e confusão de caracteres.
35. **Typeahead digitado antes do terminal estar pronto corrompendo comando de launch do agente (`#45454`):**
    Teclas digitadas precocemente pelo usuário (*typeahead*) antes da inicialização completa do PTY e injeção do comando de launch do agente ficavam no buffer de entrada, misturando-se com a linha de comando do agente e provocando erros de sintaxe no shell.
36. **Falha na leitura do token Cursor armazenado no Secret Service no Linux (`#45480`, resolve `#45455`):**
    No Linux, quando o arquivo de configuração `auth.json` do Cursor indicava armazenamento no cofre do sistema (`os-secret-store`), o Studio falhava em recuperar o token de autenticação por não consultar o Secret Service via `secret-tool search`.
37. **Dificuldade de responder sequencialmente a múltiplas perguntas em itens de tarefas (`#45472`, `#45871`):**
    Itens de agentes gerenciados que emitiam várias perguntas obrigavam o usuário a enviar respostas fragmentadas em comentários isolados; respostas mantidas no buffer eram descartadas ou atribuídas à linha errada caso mensagens intermediárias fossem enviadas antes da confirmação.
38. **Caixa de comentários de itens gerenciados com largura fixa estreita (`#45837`):**
    O campo de digitação de comentários em itens de agentes gerenciados não aproveitava o espaço horizontal disponível, dificultando a revisão e edição de textos compridos e respostas detalhadas.
39. **Pílula de modelo desatualizada após recusa com fallback no Claude Code (`#45385`):**
    Quando o Claude Code acionava fallback de modelo por recusa de segurança na thread principal, o seletor visual continuava mostrando o modelo original salvo; além disso, selecionar o modelo original novamente no composer não enviava o comando de reativação para tirar o Claude do modo de fallback.
40. **Modo Plan revertendo indevidamente chats do Claude para modo de permissão restritivo (`#45702`):**
    Após aprovar um plano em chats iniciados no modo Plan, o Studio lia o modo inicial a partir do frame tardio de inicialização (que já reportava "plan"), forçando `set_permission_mode default` e disparando confirmações manuais em todos os comandos do terminal subsequentes mesmo quando o modo padrão era automático.
41. **Truncamento de slash commands e skills no menu do Claude após 512 itens (`#45571`, refs `#45563`):**
    O catálogo de comandos do Claude cortava entradas após a 512ª linha, omitindo skills e comandos customizados do menu slash do Native Chat e causando lentidão ao filtrar emojis complexos.
42. **Contagem duplicada de bytes de saída no daemon ao reanexar terminais com overlay de histórico (`#45783`, resolve `#19595`):**
    Ao reconectar a um terminal PTY usando snapshot com overlay de histórico, o daemon retornava a sequência do snapshot em vez da sequência real de conexão, fazendo com que bytes gerados durante o overlay fossem computados duas vezes e descalibrassem a contagem de saída do runtime.
43. **Falha de inicialização do Claude ao solicitar Full Access quando configurações locais proíbem bypass (`#45068`):**
    Quando configurações organizacionais ou locais do Claude (`settings.json` ou managed settings) proíbem a concessão de acesso irrestrito (*Full access* / bypass de permissões), a inicialização do Claude falhava ao tentar aplicar o modo sem aprovação em vez de rebaixar suavemente para *Approve for me* ou *Ask*.
44. **Alto consumo de CPU no macOS por terminais ociosos varrendo periodicamente a tabela global de processos com `ps` (`#45713`):**
    A rotina de monitoramento de status de terminais no Mac invocava `ps -axo pid,ppid,command` ciclicamente para inspecionar os processos filhos de cada terminal ocioso, gerando varreduras repetidas e desnecessárias de toda a tabela de processos do sistema e impactando a duração da bateria.
45. **Re-renderizações e leituras desnecessárias de todos os buckets de abas ao alterar o título de um único terminal (`#44954`):**
    No processo renderer, qualquer evento de alteração de título ou status de uma aba de terminal invalidava e relia o estado de todos os agrupamentos (*buckets*) de abas do workspace, em vez de isolar a mutação estritamente ao bucket onde a aba reside.
46. **Vazamento de argumentos confidenciais e saídas de erro completas em falhas de comandos customizados de agentes (`#45978`):**
    Quando comandos customizados de launch de agentes falhavam no arranque, as mensagens de erro exibidas na interface podiam conter argumentos sensíveis de linha de comando (chaves, URLs internas ou tokens) e blocos brutos de `stderr`, expondo dados confidenciais nos logs e toasts de erro.
47. **Entrega de mensagens de correio de workers sobrescrevendo rascunhos não enviados no terminal Pi (`#45907`):**
    Quando um worker enviava notificações ou correspondências para um terminal executando o agente Pi, a mensagem era injetada imediatamente no prompt mesmo que o usuário estivesse com um rascunho de texto digitado no editor, sobrescrevendo a entrada não enviada.
48. **Links OSC 8 de arquivos no terminal ignorando fragmentos `#L<linha>` e intervalos (`#46105`):**
    Ao clicar em links de arquivos emitidos no terminal via sequências de escape OSC 8 contendo sufixos de linha (ex.: `#L42` ou `#L10-L20`), o editor abria o documento sempre no topo, ignorando a navegação para a linha ou seleção especificada.
49. **Alteração de título de terminal disparando varreduras redundantes em toda a barra lateral e Activity (`#45759`):**
    Cada atualização de título em um terminal PTY disparava a re-varredura completa do estado de todos os workspaces na barra lateral e no painel Activity, provocando overhead desnecessário de CPU e re-renderizações.
50. **Sublinhado visual de aba ativa aparecendo em grupos de split desfocados (`#46156`):**
    Em layouts com múltiplos splits de abas, o sublinhado visual indicador de aba ativa continuava exibido em todos os grupos simultaneamente, impedindo identificar qual split detinha o foco do teclado.
51. **Desalinhamento visual das opções no menu de contexto de abas (`#44476`):**
    No menu de contexto das abas do terminal e do editor, linhas sem ícones ficavam desalinhadas em relação às opções que possuíam ícones, gerando irregularidade visual.
52. **Recenseamento de terminais remotos em falhas de status de workers locais (`#46206`):**
    Ao detectar ausência de status de um worker local, o runtime executava varreduras de recenseamento também em terminais de servidores remotos pareados, gerando tráfego de rede e latências espúrias.
53. **Caixa de comentários de perguntas de itens muito estreita e sem destaque para opções recomendadas (`#46168`, `#46157`, `#46145`):**
    Ao responder perguntas em itens de tarefas, a caixa de texto abria com altura inicial de apenas uma linha; além disso, opções recomendadas não tinham distinção visual com estrela, e ações de retomada na fila de mensagens pausadas ficavam pouco evidentes.

## O que o upstream implementa e corrige

- **Suporte a fragmentos `#L<linha>` e intervalos em links OSC 8 no terminal (`#46105`):**
  - Faz o tratador de cliques em links de arquivos no terminal interpretar sufixos `#L<linha>` e ranges de linha, posicionando o cursor ou destacando o trecho no editor.
- **Supressão de varredura global de workspaces na mudança de título de terminal (`#45759`):**
  - Desacopla atualizações de título de terminal das rotinas de varredura de workspaces da barra lateral e Activity.
- **Sublinhado de aba ativa restrito ao grupo de split focado (`#46156`):**
  - Renderiza o sublinhado indicador de aba ativa exclusivamente no painel dividido que possui o foco do teclado no momento.
- **Alinhamento do menu de contexto de abas com ícones dedicados (`#44476`):**
  - Atribui ícones estruturados para cada entrada do menu de contexto de abas, padronizando a largura e o alinhamento visual.
- **Recenseamento restrito a terminais locais em falhas de status de workers (`#46206`):**
  - Limita a verificação de processos aos terminais do host local quando o status de um worker estiver ausente, eliminando requisições a servidores remotos.
- **Melhorias de interação e ergonomia em itens e filas pausadas (`#46168`, `#46157`, `#46145`):**
  - Abre o campo de comentário com 4 linhas de altura ao responder perguntas de itens, destaca a opção recomendada com ícone de estrela e evidencia o botão "Resume" na fila de mensagens pausadas.
- **Fallback resiliente de permissão do Claude de Full access para Approve for me / Ask (`#45068`):**
  - Implementa degradação suave quando `bypassPermissions` é bloqueado pelas configurações do Claude, rebaixando automaticamente a sessão para o modo de aprovação permitido mais próximo em vez de abortar o chat.
- **Leitura eficiente de processos de terminal no macOS via kinfo compartilhada (`#45713`):**
  - Substitui as invocações periódicas de `ps` por consultas estruturadas de `kinfo_proc` compartilhadas entre os terminais, eliminando picos de CPU causados por varreduras globais em terminais ociosos no Mac.
- **Isolamento de atualizações de título de terminal por bucket de abas no renderer (`#44954`):**
  - Restringe o disparo de atualizações de estado exclusivamente ao bucket da aba modificada, impedindo refetches e re-renderizações em outros painéis de abas do workspace.
- **Redação de argumentos e sanitização de stderr em mensagens de erro de agentes (`#45978`):**
  - Sanitiza as mensagens de falha de launch de comandos customizados, ocultando argumentos e parâmetros potencialmente sensíveis e exibindo apenas diagnósticos seguros.
- **Retenção de correio de workers durante edição de rascunho no terminal Pi (`#45907`):**
  - Enfileira as mensagens de correspondência de workers em segundo plano enquanto o editor do Pi tiver caracteres não submetidos no buffer de entrada, entregando o correio apenas quando o prompt estiver livre.

- **Respostas em lote a múltiplas perguntas de itens em um único comentário (`#45472`, `#45871`):**
  - Permite responder sequencialmente a várias perguntas de itens de agentes mantendo as respostas no buffer e publicando-as agrupadas no próximo envio com citações exatas de linhas e sem perda de contexto.
- **Largura total para caixas de comentários de itens gerenciados (`#45837`):**
  - Expande o contêiner de entrada de comentários para utilizar 100% da largura disponível no card do item gerenciado.
- **Exibição e reversão de modelos em fallback de recusa no Claude (`#45385`):**
  - Atualiza dinamicamente a pílula do composer para refletir o modelo de fallback ativo e permite que a seleção manual do modelo original envie `set_model` no turno seguinte para desarmar o fallback.
- **Restauração de modo de permissão nativo após aprovação de planos (`#45702`):**
  - Lê o modo inicial a partir de `current_permission_mode` da resposta de inicialização do Claude, garantindo que o chat retorne ao modo de trabalho normal configurado (auto/default) após aprovar planos.
- **Expansão do catálogo de comandos do Claude para até 1024 entradas (`#45571`, refs `#45563`):**
  - Eleva o limite para 1024 entradas (ou 512 KiB de JSON) mantendo skills e slash commands acessíveis no Native Chat, além de adotar regex global para sanitização rápida de emojis.
- **Preservação da sequência de saída no attach de terminais com overlay (`#45783`, resolve `#19595`):**
  - Mantém a sequência de saída obtida no momento exato do `createOrAttach`, evitando contagem duplicada de bytes live e histórico.
- **Exibição de checagens de metas na linha expansível de objetivos (`#43785`):**
  - Renderiza indicadores visuais de progresso e validações de metas diretamente na linha recolhível de objetivos do agente.
- **Chips clicáveis com abertura direta para nomes de workers no chat (`#45363`):**
  - Converte nomes de workers em linhas de chat em chips interativos que abrem diretamente a visualização do worker.
- **Ancoragem contínua do candidato IME no terminal do Cursor Agent (`#45446`):**
  - Mantém o ponto de ancoragem da janela de candidatos do IME alinhado ao prompt em todas as re-renderizações durante a composição ativa.
- **Mascaramento da sugestão esmaecida do Claude sob o preedit IME (`#45449`):**
  - Oculta a sugestão esmaecida do prompt enquanto houver composição ativa no buffer de preedit do IME.
- **Descarga de typeahead antes da injeção do comando de launch de agentes (`#45454`):**
  - Emite sequência de limpeza (`\x15` / `^U`) para esvaziar o buffer de typeahead antes de injetar o comando de inicialização do agente no PTY.
- **Leitura do token do Cursor via Secret Service no Linux (`#45480`, resolve `#45455`):**
  - Executa `secret-tool search` para extrair as credenciais do Cursor quando `auth.json` aponta para `os-secret-store`.
- **Roteamento de colagem para o campo de resposta de perguntas interativas (`#45100`):**
  - Desconsidera o composer de chat quando este estiver sob elemento oculto ou inerte, direcionando atalhos de colar diretamente para o campo de resposta focado.
- **Liberação de atalhos de alternância de workspace no composer de chat (`#45101`):**
  - Faz o composer de chat ceder os acordes `Mod+Shift+Up/Down` para o gerenciador global de workspaces, mantendo a seleção tradicional apenas em campos de formulários genéricos.
- **Manutenção de "Approve once" com limite de 256 KB para recusas do Codex (`#45006`):**
  - Eleva o teto de captura para 256 KB preservando a opção de aprovação individual sem corromper a persistência do diário.
- **Preservação de cursor pending-wrap no replay de snapshots de terminal (`#45064`):**
  - Reimprime a linha do cursor após a restauração dos modos de terminal, rearmando o pending-wrap na célula de borda antes de aplicar o estilo do cursor.
- **Neutralização de sequências de escape parciais gigantes (>4096 caracteres) (`#45110`):**
  - Insere um prefixo inerte que mantém o xterm em estado de descarte até o final da sequência (ESC]x; para OSC, ESC P0< para DCS), evitando vazamento de Base64 em snapshots.
- **Retenção do nome de abas de terminal após fechamento e na retomada (`#44460`, refs `#31281`):**
  - Grava o nome customizado por sessão de agente no cliente local e sincroniza em segundo plano;
  - Exibe o nome customizado nas linhas do Session History / AI Vault mesmo após a aba ser fechada;
  - Ao retomar a sessão a partir do histórico (por clique ou arraste, em host local ou pareado), nomeia a nova aba com o nome salvo.
- **Staging unificado de arquivos para chats de terminal em servidores pareados (`#44916`):**
  - Unifica o envio de arquivos arrastados, selecionados ou colados via `stageClientFilesForAgent`, enviando os anexos para `.orca/drops` no worktree remoto e fornecendo um caminho legível pelo agente (inclusive em conexões SSH).
- **Listagem de servidores MCP configurados como "not started" antes do início do chat (`#44673`):**
  - Lista servidores MCP configurados com o status "not started" antes da inicialização do chat, exibindo-os na interface sem disparar polling prematuro nem acordar o `codex app-server`.
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
24. Reter o nome customizado de abas de terminal após o fechamento e aplicá-lo ao retomar sessões a partir do histórico (`#44460`, refs `#31281`).
25. Unificar o staging de arquivos arrastados ou colados em chats de terminal em servidores pareados para `.orca/drops` via `stageClientFilesForAgent` (`#44916`).
26. Exibir servidores MCP configurados com o estado "not started" antes do início do chat Codex sem polling ou inicialização prematura de app-server (`#44673`).
27. Direcionar colagens de texto diretamente para o campo de resposta de perguntas interativas ativas no chat (`#45100`).
28. Liberar atalhos de alternância de workspace (`Mod+Shift+Up/Down`) através do composer de chat (`#45101`).
29. Reter a opção "Approve once" em recusas de ferramentas do Codex de até 256 KB (`#45006`).
30. Repintar o estado de pending-wrap do cursor na restauração de snapshots de terminal (`#45064`).
31. Neutralizar caudas parciais de sequências de escape superiores a 4096 caracteres em cortes de streaming e snapshots (`#45110`).
32. Converter nomes de workers em linhas de chat em chips interativos para abertura direta (`#45363`).
33. Manter a ancoragem espacial da janela de candidatos do IME no terminal do Cursor Agent durante a composição (`#45446`).
34. Ocultar sugestões esmaecidas de prompt sob a caixa de preedit do IME em chats do Claude (`#45449`).
35. Limpar typeahead prévio antes de injetar comandos de inicialização de agentes no terminal (`#45454`).
36. Suportar a extração de credenciais do Cursor no Secret Service do Linux via `secret-tool` (`#45480`, resolve `#45455`).
37. Permitir responder a múltiplas perguntas sequenciais em itens em um único comentário agrupado (`#45472`, `#45871`).
38. Expandir o campo de comentários de itens gerenciados para ocupar a largura total do contêiner (`#45837`).
39. Indicar o modelo de fallback ativo no composer do Claude e permitir o retorno ao modelo selecionado via `set_model` (`#45385`).
40. Restaurar o modo de permissão nativo após a aprovação de planos no Claude via `current_permission_mode` (`#45702`).
41. Expandir a capacidade do catálogo de comandos do Claude para até 1024 entradas no menu slash (`#45571`, refs `#45563`).
42. Preservar a sequência de saída obtida no momento da conexão ao reanexar terminais com overlay de histórico (`#45783`, resolve `#19595`).
43. Exibir checagens de metas na linha expansível de objetivos de agentes (`#43785`).
44. Implementar fallback automático de permissões do Claude para Approve for me ou Ask quando Full access for bloqueado por configurações locais (`#45068`).
45. Otimizar a checagem de processos filhos de terminais no macOS usando leitura compartilhada de kinfo em substituição a `ps` contínuo (`#45713`).
46. Isolar as notificações de alteração de título de terminal no renderer para ler apenas o bucket de abas correspondente (`#44954`).
47. Redigir argumentos de comandos customizados e sanitizar saídas de erro exibidas em falhas de agentes (`#45978`).
48. Reter notificações e correios de workers enquanto houver rascunho não enviado no terminal Pi (`#45907`).
49. Interpretar fragmentos `#L<linha>` e intervalos de linhas em links de arquivo OSC 8 no terminal (`#46105`).
50. Desacoplar atualizações de título de terminal de re-varreduras da barra lateral e Activity (`#45759`).
51. Restringir o sublinhado visual de aba ativa exclusivamente ao split focado (`#46156`).
52. Alinhar opções do menu de contexto de abas com ícones dedicados (`#44476`).
53. Restringir o recenseamento de terminais em falhas de status de workers estritamente ao host local (`#46206`).
54. Abrir caixa de comentários de perguntas de itens com 4 linhas, destacar opção recomendada e ressaltar botão Resume (`#46168`, `#46157`, `#46145`).




