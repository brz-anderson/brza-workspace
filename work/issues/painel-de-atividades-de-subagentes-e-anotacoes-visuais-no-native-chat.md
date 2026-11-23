---
status: open
description: Os PRs #47308, #47309 e #47429 adicionam o estado Waiting a itens externos, #47359 evita alargamento do chat e #47337 preserva modo Plan/Build na fila.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-05
tags:
  - chat
  - tooling
---

# Painel de atividades de subagentes e anotações visuais no Native Chat

Rastreado dos PRs abertos no upstream [`stablyai/orca#47308`](https://github.com/stablyai/orca/pull/47308),
[`stablyai/orca#47309`](https://github.com/stablyai/orca/pull/47309),
[`stablyai/orca#47429`](https://github.com/stablyai/orca/pull/47429),
[`stablyai/orca#47359`](https://github.com/stablyai/orca/pull/47359) (resolve Issue [`#47358`](https://github.com/stablyai/orca/issues/47358)),
[`stablyai/orca#47346`](https://github.com/stablyai/orca/pull/47346),
[`stablyai/orca#47337`](https://github.com/stablyai/orca/pull/47337),
[`stablyai/orca#47464`](https://github.com/stablyai/orca/pull/47464),
[`stablyai/orca#47200`](https://github.com/stablyai/orca/pull/47200),
[`stablyai/orca#47220`](https://github.com/stablyai/orca/pull/47220),
[`stablyai/orca#47191`](https://github.com/stablyai/orca/pull/47191),
[`stablyai/orca#47016`](https://github.com/stablyai/orca/pull/47016) (resolve Issue [`#47021`](https://github.com/stablyai/orca/issues/47021)),
[`stablyai/orca#47080`](https://github.com/stablyai/orca/pull/47080) (refs Issue [`#47055`](https://github.com/stablyai/orca/issues/47055)),
[`stablyai/orca#47076`](https://github.com/stablyai/orca/pull/47076),
[`stablyai/orca#47084`](https://github.com/stablyai/orca/pull/47084),
[`stablyai/orca#46740`](https://github.com/stablyai/orca/pull/46740),
[`stablyai/orca#46901`](https://github.com/stablyai/orca/pull/46901),
[`stablyai/orca#46930`](https://github.com/stablyai/orca/pull/46930),
[`stablyai/orca#46974`](https://github.com/stablyai/orca/pull/46974) (resolve Issue [`#46953`](https://github.com/stablyai/orca/issues/46953)),
[`stablyai/orca#46739`](https://github.com/stablyai/orca/pull/46739),
[`stablyai/orca#45876`](https://github.com/stablyai/orca/pull/45876),
[`stablyai/orca#45881`](https://github.com/stablyai/orca/pull/45881),
[`stablyai/orca#46592`](https://github.com/stablyai/orca/pull/46592),
[`stablyai/orca#46570`](https://github.com/stablyai/orca/pull/46570),
[`stablyai/orca#46583`](https://github.com/stablyai/orca/pull/46583),
[`stablyai/orca#46608`](https://github.com/stablyai/orca/pull/46608),
[`stablyai/orca#45410`](https://github.com/stablyai/orca/pull/45410),
[`stablyai/orca#46165`](https://github.com/stablyai/orca/pull/46165),
[`stablyai/orca#46009`](https://github.com/stablyai/orca/pull/46009),
[`stablyai/orca#46127`](https://github.com/stablyai/orca/pull/46127),
[`stablyai/orca#46362`](https://github.com/stablyai/orca/pull/46362),
[`stablyai/orca#46281`](https://github.com/stablyai/orca/pull/46281),
[`stablyai/orca#46311`](https://github.com/stablyai/orca/pull/46311),
[`stablyai/orca#46316`](https://github.com/stablyai/orca/pull/46316),
[`stablyai/orca#46368`](https://github.com/stablyai/orca/pull/46368) (resolve Issue [`#46367`](https://github.com/stablyai/orca/issues/46367)),
[`stablyai/orca#46309`](https://github.com/stablyai/orca/pull/46309),
[`stablyai/orca#44461`](https://github.com/stablyai/orca/pull/44461) (resolve Issue [`#40998`](https://github.com/stablyai/orca/issues/40998)),
[`stablyai/orca#44808`](https://github.com/stablyai/orca/pull/44808),
[`stablyai/orca#43994`](https://github.com/stablyai/orca/pull/43994),
[`stablyai/orca#44413`](https://github.com/stablyai/orca/pull/44413),
[`stablyai/orca#44508`](https://github.com/stablyai/orca/pull/44508),
[`stablyai/orca#44203`](https://github.com/stablyai/orca/pull/44203),
[`stablyai/orca#42965`](https://github.com/stablyai/orca/pull/42965),
[`stablyai/orca#43908`](https://github.com/stablyai/orca/pull/43908) (resolve Issue [`#43988`](https://github.com/stablyai/orca/issues/43988)),
[`stablyai/orca#43954`](https://github.com/stablyai/orca/pull/43954),
[`stablyai/orca#43607`](https://github.com/stablyai/orca/pull/43607) (resolve Issue [`#43599`](https://github.com/stablyai/orca/issues/43599)),
[`stablyai/orca#43600`](https://github.com/stablyai/orca/pull/43600) (resolve Issue [`#43595`](https://github.com/stablyai/orca/issues/43595)),
[`stablyai/orca#43567`](https://github.com/stablyai/orca/pull/43567),
[`stablyai/orca#43562`](https://github.com/stablyai/orca/pull/43562),
[`stablyai/orca#43521`](https://github.com/stablyai/orca/pull/43521),
[`stablyai/orca#43516`](https://github.com/stablyai/orca/pull/43516),
[`stablyai/orca#43474`](https://github.com/stablyai/orca/pull/43474),
[`stablyai/orca#43456`](https://github.com/stablyai/orca/pull/43456),
[`stablyai/orca#43425`](https://github.com/stablyai/orca/pull/43425) (resolve Issue [`#43424`](https://github.com/stablyai/orca/issues/43424)),
além das issues [`stablyai/orca#44003`](https://github.com/stablyai/orca/issues/44003),
[`stablyai/orca#43983`](https://github.com/stablyai/orca/issues/43983),
[`stablyai/orca#43610`](https://github.com/stablyai/orca/issues/43610),
[`stablyai/orca#43597`](https://github.com/stablyai/orca/issues/43597),
[`stablyai/orca#43549`](https://github.com/stablyai/orca/issues/43549),
[`stablyai/orca#43462`](https://github.com/stablyai/orca/issues/43462) e
[`stablyai/orca#43461`](https://github.com/stablyai/orca/issues/43461),
[`stablyai/orca#43385`](https://github.com/stablyai/orca/pull/43385),
[`stablyai/orca#43380`](https://github.com/stablyai/orca/pull/43380),
além da issue [`stablyai/orca#43366`](https://github.com/stablyai/orca/issues/43366),
[`stablyai/orca#42455`](https://github.com/stablyai/orca/pull/42455),
[`stablyai/orca#42448`](https://github.com/stablyai/orca/pull/42448),
[`stablyai/orca#42305`](https://github.com/stablyai/orca/pull/42305) (resolve Issue [`#42099`](https://github.com/stablyai/orca/issues/42099)),
[`stablyai/orca#42307`](https://github.com/stablyai/orca/pull/42307),
[`stablyai/orca#42287`](https://github.com/stablyai/orca/pull/42287) (resolve Issue [`#42286`](https://github.com/stablyai/orca/issues/42286)),
[`stablyai/orca#42254`](https://github.com/stablyai/orca/pull/42254),
[`stablyai/orca#41955`](https://github.com/stablyai/orca/pull/41955),
[`stablyai/orca#41766`](https://github.com/stablyai/orca/pull/41766),
[`stablyai/orca#40935`](https://github.com/stablyai/orca/pull/40935),
[`stablyai/orca#39649`](https://github.com/stablyai/orca/pull/39649) (resolve Issue [`#39619`](https://github.com/stablyai/orca/issues/39619)),
[`stablyai/orca#39606`](https://github.com/stablyai/orca/pull/39606) (resolve Issue [`#37379`](https://github.com/stablyai/orca/issues/37379)),
[`stablyai/orca#39276`](https://github.com/stablyai/orca/pull/39276) (Issue [`#39275`](https://github.com/stablyai/orca/issues/39275)),
[`stablyai/orca#39082`](https://github.com/stablyai/orca/pull/39082) (Issue [`#39074`](https://github.com/stablyai/orca/issues/39074)),
[`stablyai/orca#39079`](https://github.com/stablyai/orca/pull/39079) (Issue [`#39073`](https://github.com/stablyai/orca/issues/39073)),
além das issues [`stablyai/orca#41008`](https://github.com/stablyai/orca/issues/41008) e
[`stablyai/orca#39619`](https://github.com/stablyai/orca/issues/39619),
[`stablyai/orca#38995`](https://github.com/stablyai/orca/pull/38995) (Issue [`#38994`](https://github.com/stablyai/orca/issues/38994)),
[`stablyai/orca#38963`](https://github.com/stablyai/orca/pull/38963),
[`stablyai/orca#38945`](https://github.com/stablyai/orca/pull/38945),
[`stablyai/orca#39013`](https://github.com/stablyai/orca/pull/39013) (Issue [`#39010`](https://github.com/stablyai/orca/issues/39010)),
[`stablyai/orca#38632`](https://github.com/stablyai/orca/pull/38632),
[`stablyai/orca#38633`](https://github.com/stablyai/orca/pull/38633),
[`stablyai/orca#38640`](https://github.com/stablyai/orca/pull/38640),
[`stablyai/orca#38470`](https://github.com/stablyai/orca/pull/38470),
[`stablyai/orca#38452`](https://github.com/stablyai/orca/pull/38452),
[`stablyai/orca#38594`](https://github.com/stablyai/orca/pull/38594) (Issue [`#38592`](https://github.com/stablyai/orca/issues/38592)),
[`stablyai/orca#38627`](https://github.com/stablyai/orca/pull/38627),
[`stablyai/orca#38649`](https://github.com/stablyai/orca/pull/38649) e
[`stablyai/orca#38625`](https://github.com/stablyai/orca/pull/38625) (Issue [`#38624`](https://github.com/stablyai/orca/issues/38624)).

## O problema

1. **Incapacidade de visualizar transcrições de chats estruturados no Agent Dashboard (`#39082`, `#39074`):**
   No painel Agent Dashboard, cartões de sessões de chat estruturado não possuíam PTY associado, exibindo apenas uma mensagem
   estática de que nenhuma pré-visualização estava disponível. O usuário precisava abrir o worktree e carregar a aba para
   ler o histórico ou acompanhar o progresso.
2. **Excesso de notificações intrusivas e falta de filtro por perguntas de agentes (`#39079`, `#39073`):**
   O canal de notificações do sistema tratava qualquer evento ("Agent Needs Input", conclusões de tarefas e campainhas de
   terminal) de forma idêntica. Desenvolvedores que desejavam ser avisados apenas quando o agente realmente precisava de
   uma resposta ou esclarecimento eram inundados por alertas repetitivos de aprovações rotineiras de ferramentas.
3. **Sessões flutuantes e de subagentes dispersas na barra lateral (`#38995`, `#38994`):**
   Subagentes e sessões ad-hoc abertas fora da hierarquia primária de worktrees misturavam-se de forma plana na lista de
   workspaces da barra lateral, sem indicação visual compacta do número de subagentes trabalhando em tempo real.
4. **Travamento do chat aguardando ferramentas ou comandos Bash longos do Claude (`#38963`):**
   Comandos demorados ou subagentes executados via Claude Bash bloqueavam a continuidade do chat até o término da invocação,
   sem opção para despachar o comando em segundo plano e permitir que o operador ou o agente seguissem a conversa.
5. **Travamentos e congelamentos em históricos massivos de sessões (`#38945`):**
   O indexador e motor de busca do Agent Session History executava transações SQLite síncronas pesadas na mesma thread do
   Node/servidor, travando a UI por minutos em históricos com mais de 20.000 transcrições.
6. **Processos órfãos fora de terminais invisíveis no monitor de recursos (`#39013`, `#39010`):**
   O popover Resource Usage monitorava apenas a árvore direta de processos de terminais ativos, omitindo servidores de
   desenvolvimento desanexados iniciados pelo agente.
7. **Invisibilidade e falta de inspeção de subagentes no Native Chat (`#38632`, `#38633`, `#38470`):**
   Falta de elenco estruturado (*roster*) dos subagentes em execução no chat desktop e mobile.
8. **Subagentes do OpenCode 2.x não renderizados no Chat UI (`#39276`, `#39275`):**
   Quando um agente OpenCode delegava tarefas a subagentes auxiliares (`subagent` no 2.x ou `task` no 1.x), as ações do filho
   apareciam como ferramentas genéricas na conversa principal, sem identificação do subagente, sem cartão dedicado de estado
   (running/done/stopped) e sem presença na faixa de agentes ativos acima do composer.
9. **Sessões irmãs do OpenCode em serviço compartilhado tratadas como subagentes (`#39619`):**
   Ao conectar múltiplos terminais ao mesmo serviço `opencode serve --service`, o hook do OpenCode considerava qualquer sessão ativa
   no fluxo de eventos como subagente da pane observada. Isso fazia com que abas ociosas exibissem o spinner `working` continuamente
   enquanto uma sessão irmã trabalhava.
10. **Poluição de títulos de abas do Claude Code com texto de aviso após `/clear` (`#39606`, resolve `#37379`):**
    Após rodar `/clear`, o título da aba no Orca assumia o texto bruto `<local-command-caveat>The command below was run directly in Claude Code...`
    em vez de preservar o título ao vivo (`✳ Claude Code`), permanecendo ilegível até o envio do próximo prompt real.
11. **Sobrescrita, duplicação e desaparecimento de imagens geradas no Native Chat (`#40935`):**
    Quando agentes geravam imagens (artboards, mockups ou diagramas), a entrega do artefato sobrescrevia o texto em prosa da
    resposta final quando chegava com atraso, aparecia duplicada caso a resposta já a incorporasse, ou desaparecia completamente
    ao navegar de volta pelo histórico de sessões anteriores.
12. **Invisibilidade do modelo e nível de esforço de subagentes no painel de agentes (`#41008`):**
    No painel de agentes da sessão do Claude ("1 agent — working", com nome, ferramenta ativa, tokens e tempo), não havia exibição
    do modelo e esforço de raciocínio de cada subagente. Quando agentes customizados ou chamadas dinâmicas utilizavam modelos
    discrepantes do pai (ex.: subagente executando em Opus no esforço high em sessão pai Sonnet), o operador ficava no escuro sobre
    os parâmetros de execução e custos correspondentes.
13. **Incompatibilidade para importar transcrições do Kimi Code e adotar conversas iniciadas via CLI (`#41955`):**
    Sessões e transcrições geradas pela CLI do Kimi Code permaneciam isoladas no filesystem, impossibilitando que desenvolvedores
    adotassem essas conversas dentro do Native Chat no desktop para continuar a interação com histórico estruturado,
    ferramental gráfico e inspeção de passos.
14. **Retenção de memória de subagentes após o fechamento da aba de chat (`#42254`):**
    Ao inspecionar um subagente dentro de uma conversa, o aplicativo guardava o registro de qual subagente estava aberto.
    Quando a aba de chat era fechada, esse registro continuava retido em memória até o reinício do aplicativo, acumulando
    vazamentos sutis em sessões de longa duração.
15. **Ausência da barra de subagentes ativos no mobile para chats baseados em terminal (`#42305`, resolve `#42099`):**
    No cliente mobile, chats orientados a terminal ou com subagentes delegados não exibiam a barra horizontal compacta de subagentes ativos, impedindo acompanhar workers em tempo real pelo smartphone.
16. **Perda ou reexecução espúria de perguntas interativas após reinicialização do app (`#42307`):**
    Perguntas pendentes de agentes interativos sofriam reinvocação ou disparavam novas requisições de modelo caso o app fosse reiniciado antes da resposta do usuário.
17. **Divergência na identificação de versão pontual do Claude no banner (`#42287`, resolve `#42286`):**
    O banner do chat truncava versões minoritárias pontuais do Claude (ex.: Opus 5.5 caindo incorretamente para Opus 5), gerando confusão sobre a real versão do modelo em execução.
18. **Substituição da tela inteira de chat ao inspecionar subagentes (`#42455`):**
    Clicar em um subagente na barra ou transcrição trocava toda a conversa principal pela visualização do subagente, ocultando o contexto da conversa pai, perdendo a posição de rolagem e bloqueando o rascunho ativo no composer.
19. **Invisibilidade de subagentes nas conversas do Pi Native Chat (`#42448`):**
    Enquanto Claude e Codex exibiam subagentes e ferramentas delegadas de forma visual, o agente Pi não renderizava a presença de subagentes no chat nativo.
20. **Falta de faixa de worker temporário no topo de chat workers (`#43521`):**
    Workers temporários disparados no chat não exibiam o banner no topo avisando sobre a natureza efêmera da tarefa, ao contrário do que já ocorria em abas de terminal.
21. **Ausência de identificador de plugin em mensagens e mails enviados (`#43425`, resolve `#43424`):**
    Mensagens geradas ou despachadas por plugins no chat nativo não exibiam nome nem ícone do plugin de origem, prejudicando a rastreabilidade das ações automatizadas.
22. **Incapacidade de referenciar outros chats e terminais via `@` no composer (`#43462`):**
    O compositor de mensagens não oferecia autocompletar com `@` para menções direcionadas a outras sessões de chat ou abas de terminal abertas no workspace.
23. **Citações "Add to chat" sem chips navegáveis de retorno (`#43461`):**
    Textos capturados do terminal ou editor para o chat ficavam colados como texto puro sem transformar-se em chips interativos capazes de saltar para a linha ou arquivo de origem ao clicar.
24. **Auto-retomada indevida de chats aguardando operador após reinício (`#43474`):**
    Ao reiniciar o aplicativo, conversas esperando confirmação ou entrada humana eram retomadas cegamente em vez de permanecerem listadas na fila de restart pendente.
25. **Consumo de memória sem limites em entregas e leituras atrasadas de chat (`#43456`):**
    Filas de eventos de chat e leituras de histórico acumulavam mensagens na memória sem limite quando o receptor ficava atrasado, elevando o heap do runtime.
26. **Montagem eager e pesada de abas de chat ocultas no arranque (`#43516`):**
    O componente de visualização de chat era montado imediatamente para todas as abas no carregamento, degradando a performance inicial de workspaces com muitos chats.
27. **Falta de seletores rápidos de presets de modelo, esforço de raciocínio e velocidade no Chat (`#43607`, resolve `#43599`):**
    Ajustar modelo, esforço de raciocínio e velocidade exigia abrir menus suspensos ou configurações em múltiplos níveis. Não havia presets rápidos de um clique posicionados diretamente abaixo do controle de velocidade.
28. **Inflexibilidade da tecla de envio de mensagens no Native Chat (`#43600`, resolve `#43595`):**
    O composer do chat disparava o envio fixamente ao pressionar Enter (exigindo Shift+Enter para quebra de linha), sem uma configuração que permitisse inverter o comportamento para operadores acostumados a usar Enter para parágrafos e Shift+Enter para envio.
29. **Omissão de painéis de agentes recém-iniciados no seletor "Send notes to" (`#43562`):**
    O menu "Send notes to" só listava painéis de agentes após o primeiro relatório de status formal ter sido emitido. Painéis recém-criados permaneciam invisíveis até que o agente executasse seu primeiro turno, impossibilitando o envio precoce de anotações.
30. **Dessincronização do destaque na visualização de Activity com a aba ativa (`#43567`):**
    O item de Activity na barra lateral esquerda não sincronizava seu realce de seleção visual ao alternar entre abas e workspaces de agentes, deixando o operador desorientado sobre qual agente estava selecionado no painel.
31. **Supressão ou aglutinação de resumos de raciocínio (thinking) entre chamadas de ferramentas (`#43610`):**
    Trechos intermediários de raciocínio emitidos pelo Claude entre chamadas sucessivas de ferramentas eram mesclados ou ocultados no Chat UI, dificultando acompanhar a linha lógica do modelo durante a execução sequencial de comandos.
32. **Exibição de tags brutas `<advisory>` de conselhos de modelo como texto de usuário (`#43549`):**
    Tags de aviso de harness/OMP como `<advisory>` eram despejadas diretamente na área de conversa como se fossem texto digitado pelo usuário, poluindo a visualização.
33. **Ocupação permanente de espaço de tela pela barra lateral esquerda (`#43597`):**
    A barra lateral esquerda não possuía modo auto-hide com revelação ao passar o cursor pela borda (edge-hover reveal), sacrificando espaço útil de tela em telas menores ou monitores secundários.
34. **Travamento em "Sending..." de novos chats sob concorrência de streaming múltiplo (`#43908`, resolve `#43988`):**
    Quando dezenas de chats eram retomados simultaneamente após um restart, o envio de mensagens em um novo chat ficava travado em "Sending..." por dezenas de segundos sem indicador de trabalho. O gravador único de journal no SQLite compartilhava uma única fila FIFO e o limite de backpressure do WAL travava todas as novas escritas.
35. **Vazamento de memória por retenção vitalícia de status de chats fechados (`#43954`):**
    O feed de status de chats no processo principal retinha o sumário de cada sessão já aberta ou encerrada durante todo o ciclo de vida do aplicativo, impedindo a desalocação de memória de conversas fechadas.
36. **Omissão de árvores de processos do Native Chat no Resource Manager (`#43983`):**
    O monitor de recursos contava apenas processos de terminais PTY locais e processos internos do Orca, ignorando as árvores de processos dos agentes em execução nas abas de chat nativo.
37. **Reaparecimento de registros falhados limpos da view de Activity após hidratação (`#44003`):**
    Linhas de atividades com falha previamente limpas pelo desenvolvedor voltavam a aparecer na interface após a hidratação de estado e geravam erros ao tentar abrir worktrees já removidos.
38. **Supressão do menu de contexto nativo de cópia ao selecionar texto do chat na web móvel (`#42965`):**
    No cliente web para dispositivos móveis (smartphones), ao selecionar trechos de texto em mensagens do chat, o menu de contexto nativo do navegador/sistema operacional (com a ação "Copiar" / "Copy") era suprimido ou desabilitado por manipuladores de eventos de seleção do chat, impedindo que o operador copiasse facilmente partes das respostas do assistente no telefone.
39. **Mensagens entre agentes e atualizações de workers ocupando turnos inteiros de conversa no chat (`#44413`):**
    Quando agentes trocavam mensagens de coordenação ou emitiam atualizações de tarefas no chat, cada aviso era exibido como uma mensagem de chat completa e inchada. Reinicializações de workers alteravam linhas antigas e geravam confusão sobre o estado gravado da tarefa.
40. **Tremulação e reflow visual da faixa de agentes no Native Chat durante atualizações de sessão (`#44508`):**
    A cada atualização de estado da sessão do agente, a barra horizontal de agentes (*agents strip*) sofria remontagem e saltos de renderização (layout shifts), gerando cintilação visual na área superior do composer.
41. **Esgotamento de memória ao exportar contexto de chat com saídas extensas de ferramentas (`#44203`):**
    Ao exportar o contexto da conversa ou transferir dados para o modelo, saídas extensas de ferramentas de terminal eram carregadas inteiramente em strings na memória heap, provocando travamentos e quedas por falta de memória (OOM).
42. **Consumo ilimitado de memória no processo principal com streaming de texto em múltiplos chats (`#43994`):**
    Quando múltiplos chats nativos ou assinantes (*subscribers*) lentos realizavam streaming simultâneo de respostas volumosas, o processo principal do Electron acumulava cópias não entregues de snapshots de texto ao vivo sem teto delimitado por subscriber. Em conexões lentas ou renderers ocupados, a retenção gerava picos de centenas de megabytes no heap do main process antes de desalocar a memória.
43. **Descompasso de título de chat ao renomear sessão Claude via comando `/rename` ou `/name` (`#44461`, resolve `#40998`):**
    Ao digitar `/rename <novo-nome>` ou `/name` em um chat Claude, o nome interno da conversa era alterado na CLI, mas a aba do Native Chat e a lista do Session History mantinham o nome autogerado pelo Studio (que tem precedência sobre o título do transcript). A interface não interceptava o evento `session_title_changed` emitido pela CLI, mantendo o título antigo visível.
44. **Desaparecimento de respostas de comandos locais `/recap` ao reabrir chats Claude (`#44808`):**
    Respostas geradas pelo comando `/recap` eram gravadas pelo Claude Code em registros do tipo `system/local_command` no transcript, enquanto no streaming ao vivo eram enviadas como frames sintéticos de assistente. Como a rotina de reidratação/catch-up e os decodificadores legados só liam linhas `user` e `assistant`, o conteúdo de resumos do `/recap` desaparecia da conversa ao reabrir a aba ou retomar o chat via "Resume in New Chat".
45. **Impossibilidade de citar pastas no menu de menções `@` do chat (`#46127`):**
    O menu popover de autocompletar com `@` suportava apenas arquivos e agentes, forçando o operador a digitar caminhos de pastas inteiros manualmente ao instruir agentes sobre diretórios do projeto.
46. **Citações "Add to chat" poluindo o composer como blocos Markdown brutos (`#46362`):**
    Ações de adicionar trechos selecionados de código ou notas ao chat colavam o texto cru no composer, ocupando espaço excessivo e sem indicador de origem navegável.
47. **Imagens anexadas a comentários de itens e perguntas não exibidas inline no chat (`#46281`):**
    Quando um usuário ou subagente anexava capturas de tela ou imagens de referência em respostas de perguntas de itens, a imagem não era renderizada inline na conversa, quebrando a inspeção visual.
48. **Mensagens vazias de assistente poluindo o histórico de conversa (`#46311`):**
    Em turnos com saídas parciais ou desvios de ferramentas que não geravam texto final, o frontend registrava e exibia mensagens de assistente totalmente em branco no desktop e mobile.
49. **Perda de instruções permanentes (`SOUL.md` / `MEMORY.md`) em chats gerenciados do Antigravity via ACP (`#46368`, resolve `#46367`):**
    A configuração de sessão sobrescrevia o campo `sessionMeta` do arranque com `setup._meta`, fazendo com que chats gerenciados do Antigravity descartassem silenciosamente as instruções permanentes e diretivas de alma e memória.
50. **Parada prematura de chats após atingir limite de uso por perfil desatualizado (`#45410`):**
    - Quando um agente atinge o limite de uso temporário (rate limit ou cota de provedor), a retomada automática dependia de `nativeChatAutoContinueAfterUsageLimit`, que vinha desabilitada por padrão, forçando o operador a intervir manualmente quando os limites expiravam. Além disso, redefinições simultâneas de cotas podiam disparar muitos agentes ao mesmo tempo sem escalonamento.
51. **Dificuldade de busca no menu de menção `@` de bots e perda de hierarquia de comandos (`#46165`):**
    - A lista de menções `@` de bots no Native Chat não filtrava por início de palavras nem considerava seleções recentes. Além disso, o disparo de `/` ou `$` após nomes espaçados de bots abria menus de forma inconsistente, e o cabeçalho 'Bots' desaparecia se houvesse apenas bots pausados na lista.
52. **Competição desordenada na reinicialização de chats interrompidos mid-turn versus tarefas concluídas (`#46009`):**
    - Ao reiniciar o aplicativo após crash ou reboot, chats com agentes interrompidos no meio de uma resposta competiam na mesma fila de inicialização com chats que já haviam concluído a resposta do agente e tinham apenas comandos em background pendentes, atrasando o retorno do agente ao operador.
53. **Incapacidade de excluir chats permanentemente e poluição do histórico de sessões (`#45876`):**
    - Usuários não tinham opção para deletar conversas desnecessárias no Native Chat e Session History; chats descartados permaneciam gravados no SQLite, poluíam buscas e podiam ser re-adotados acidentalmente.
54. **Poluição visual e colisão de controles nas linhas de chat e abas (`#45881`):**
    - Linhas de chat na lista da sidebar e na aba de chats exibiam múltiplos botões simultâneos; no hover, o botão `⋯` colidia com o timestamp e o status ao vivo ficava oculto em mensagens longas.
55. **Faixa de mensagens enfileiradas intrusiva e desconectada da linha de atividade (`#46592`):**
    - A faixa de mensagens enfileiradas (*queued-message strip*) exibia botões permanentes de ação que desviavam o foco da leitura e não se alinhavam com a linha de atividade do chat.
56. **Falta de menções `@` e comandos `/` na caixa de comentários de itens (`#46570`):**
    - A caixa de comentários em itens e issues não dispunha dos recursos de autocompletar do composer principal, impedindo citar agentes/arquivos via `@` ou invocar skills e comandos `/` diretamente.
57. **Falta de feedback visual no carregamento de itens de bots e identificadores opacos em Nova Aba (`#46583`, `#46608`):**
    - Ao abrir detalhes de itens de bots, a tela permanecia em branco antes da resposta do servidor em vez de exibir um esqueleto (*skeleton loader*); no seletor de Nova Aba, agentes apareciam com IDs internos opacos em vez dos nomes configurados no catálogo.
58. **Falha na renderização de imagens retornadas por ferramentas ACP sem caminho físico no disco (`#46901`):**
    - Ferramentas executadas por agentes ACP podem retornar imagens diretamente como payloads base64 sem caminho de arquivo gravado no workspace. O visualizador de anexos do Native Chat buscava carregar apenas arquivos a partir do caminho físico, resultando em imagens quebradas ou ausentes no card de saída da ferramenta.
59. **Quebra de transferência e lentidão em imagens de chat superiores a 3MB em clientes pareados (`#46930`):**
    - Quando clientes móveis ou instâncias pareadas tentavam visualizar imagens ou capturas com tamanho superior a 3MB anexadas no chat, o envio de payload monobloco causava estouro de buffer RPC ou timeouts de rede, inviabilizando a inspeção remota de imagens pesadas.
60. **Bloqueio de colagem via botão do meio do mouse (middle-click paste) em editores ProseMirror (`#46974`, resolve `#46953`):**
    - Em ambientes Linux e navegadores X11/Wayland, o clique com o botão do meio no composer baseado em ProseMirror (tanto no chat principal quanto em caixas de anotação) não disparava a colagem do buffer de seleção primária, quebrando o comportamento esperado da plataforma desktop.
61. **Omissão de pré-visualização de texto e chevron dinâmico confuso em linhas de mensagens de agentes (`#46739`):**
    - As linhas representativas de agentes no histórico de conversas exibiam apenas indicadores genéricos sem revelar a primeira linha de texto do turno e ocultavam o chevron de expansão, tornando difícil discernir o contexto rápido e saber se a linha era expansível.
62. **Inflação de diffs e substituição inteira de arquivo em edições de arquivos grandes via ACP (`#47016`, resolve `#47021`):**
    - Edições em arquivos grandes cuja soma do texto antigo e novo superava 256 KiB eram reportadas como substituição completa do arquivo, transformando uma edição de uma única linha em milhares de linhas removidas e readicionadas.
63. **Desaparecimento instantâneo de resultados de título ao concluir busca sem correspondência FTS (`#47080`, refs `#47055`):**
    - No Session History e no seletor `/resume`, enquanto o usuário digitava, sessões com títulos correspondentes apareciam na tela; se a busca full-text subsequente não encontrava correspondências no corpo das conversas, a lista era substituída por tela vazia, fazendo os resultados sumirem abruptamente.
64. **Truncamento prematuro em 8 linhas de perguntas abertas de agentes em itens (`#47076`):**
    - Quando um agente postava uma pergunta aberta em um item aguardando resposta humana, o comentário era cortado arbitrariamente em 8 linhas, ocultando o contexto da dúvida até que a pergunta fosse respondida ou substituída.
65. **Ocultação e ilegibilidade de item pills em linhas "Started" de mensagens com nomes longos (`#47084`):**
    - Em linhas de mensagens do tipo "Started" contendo remetente e chip de item vinculado, o nome do remetente possuía `flex-basis: auto` enquanto o chip do item tinha `flex-basis: 0`, fazendo com que o nome ocupasse todo o espaço horizontal e esmagasse o pill do item.
66. **Ausência de estado visual de repouso ("all-clear") na aba Items quando nada requer atenção (`#46740`):**
    - Quando todas as tarefas, perguntas e itens de um grupo de bots eram concluídos, a aba Items exibia uma lista vazia sem indicação visual de que a operação estava em dia (*all-clear*).
67. **Migração ordenada de mensagens enfileiradas e cancelamento com aviso de mensagens de conectores ao substituir chat (`#47200`):**
    - Quando um chat era substituído por uma nova conversa, mensagens enfileiradas aguardando a conclusão do turno ativo se perdiam ou ficavam órfãs, enquanto mensagens originadas de conectores ficavam retidas em limbo sem confirmação de cancelamento.
68. **Bloqueio total de correio de outros agentes por turnos com falhas transitórias (`#47220`):**
    - Mensagens enfileiradas de outros agentes eram suspensas indefinidamente quando o turno do agente principal falhava por qualquer motivo operacional, mesmo que a falha não fosse por esgotamento de cota de uso (*usage limit*).
69. **Impossibilidade de agentes anexarem itens, URLs e arquivos a itens abertos de outros agentes (`#47191`):**
    - Agentes ficavam impossibilitados de associar tarefas filhas, links de PRs, arquivos e comandos `worker-start --item` a itens de trabalho criados por outros agentes no mesmo workspace, limitando a colaboração entre bots na árvore de itens.
70. **Alargamento horizontal forçado do chat por sumários contínuos de tarefas em background (`#47359`, resolve `#47358`):**
    - Quando um comando em segundo plano (como `worker-start`) emitia uma linha de resultado ou JSON sem quebras, o token contínuo definia a largura mínima (`min-content`) do transcript, forçando barra de rolagem horizontal em todo o Native Chat.
71. **Ausência de estado formal `Waiting` para itens retidos por fatores externos (`#47308`, `#47309`, `#47429`):**
    - Itens aguardando conclusão externa (CI, deploy, revisão, resposta ou reset de cota de uso) permaneciam ambiguamente como `In progress`, sem sinalização clara do motivo da espera no hover card e janelas de desktop/mobile.
72. **Perda de modo Plan/Build e configurações de entrega ao migrar mensagens enfileiradas (`#47337`):**
    - Ao transferir a fila para uma conversa substituta, apenas o texto bruto era copiado; opções congeladas no enfileiramento (modo Plan/Build, modelo, esforço, personality, fast mode e modo steer) eram descartadas, revertendo envios planejados para o modo padrão.
73. **Perda de alinhamento e respostas precipitadas em itens com múltiplas perguntas (`#47464`, `#47461`, `#47385`, `#47372`):**
    - Respostas digitadas a uma única pergunta de um conjunto acordavam o agente imediatamente deixando as demais perguntas pendentes; além disso, respostas retidas não recuperavam o indicador `Replying to`, publicando como comentário comum fora de contexto.

## O que o upstream implementa

- **Quebra automática de linha para sumários de tarefas em background no chat (`#47359`, resolve `#47358`):**
  - Aplica `overflow-wrap: anywhere` aos textos de sumários de resultados de tarefas em segundo plano, contendo o fluxo dentro da coluna e evitando barras de rolagem horizontais espúrias.
- **Estado `Waiting` e detalhamento de espera em itens de trabalho (`#47308`, `#47309`, `#47429`):**
  - Introduz o status formal `--status waiting --note "<o que aguarda>"`, exibindo o motivo no hover card no desktop, abaixo do título no mobile e atualizando a contagem da sidebar para "N needs you"; reverte para `In progress` automaticamente quando workers retomam.
- **Preservação integral de opções e modo Plan/Build na migração da fila de mensagens (`#47337`):**
  - Preserva modo de interação (Plan/Build), modelo, esforço de raciocínio, personality, fast mode, service tier e modo steer ao mover mensagens enfileiradas para chats substitutos.
- **Sincronização de respostas a perguntas e controle de contexto em comentários de itens (`#47464`, `#47461`, `#47385`, `#47372`):**
  - Aguarda o preenchimento de todas as respostas em conjuntos de perguntas antes de acordar o agente, vincula respostas digitadas deterministicamente à pergunta correspondente e mantém o comentário de pergunta aberto até reabertura do item.
- **Exibição sob demanda de ações de edição e exclusão na fila de mensagens (`#47346`):**
  - Revela botões Edit e Delete no hover do mouse, foco ou toque, mantendo o botão Steer permanentemente acessível em cada linha da fila de envio.
- **Migração ordenada de filas de envio e cancelamento limpo de conectores na substituição de chats (`#47200`):**
  - Ao substituir uma sessão de chat, transfere mensagens enfileiradas atrás do turno em execução diretamente para a nova conversa, mantendo autor, ordem e anexos; drena mensagens de conectores na sessão antiga emitindo aviso de parada.
- **Liberação de correio entre agentes em turnos falhos que não sejam por limite de uso (`#47220`):**
  - Executa o correio enfileirado de outros agentes no próximo turno se a falha anterior não tiver sido causada por limite de cota de uso, restringindo a pausa estrita apenas a cenários que aguardam redefinição de cota ou ação humana.
- **Anexação colaborativa de itens, PRs e arquivos entre agentes em itens abertos (`#47191`):**
  - Permite que um agente anexe URLs, PRs, arquivos e inicie workers vinculados a itens abertos por outro agente no workspace da máquina local, atribuindo os anexos ao autor chamador com rotulagem amigável ("Another agent").
- **Diffs compactos delimitados ao trecho modificado para arquivos grandes em ACP (`#47016`, resolve `#47021`):**
  - Mantém o caminho `createPatch` para textos até 256 KiB e, para textos maiores, descarta linhas compartilhadas nas extremidades gerando diff apenas sobre o trecho alterado (com tetos de 64 KiB e 256 edições), recalculando as posições originais das linhas.
- **Retenção de correspondências por título durante buscas full-text sem acertos (`#47080`, refs `#47055`):**
  - Mantém a exibição de sessões que casam por título enquanto a busca FTS está pendente ou quando não retorna acertos no texto, informando aviso suave sem zerar a lista nem perder foco e rolagem.
- **Exibição integral de comentários de perguntas abertas enquanto aguardam resposta (`#47076`):**
  - Mantém o texto completo da pergunta do agente sem truncamento em 8 linhas enquanto a pergunta estiver pendente de resposta humana, preservando espaçamento entre parágrafos.
- **Dimensionamento proporcional e prioritário de item pills em linhas Started (`#47084`):**
  - Ajusta a hierarquia flex para que a primeira linha de texto dê espaço primeiro, seguida do nome do remetente, garantindo que o chip do item e o nome preservem caracteres mínimos legíveis.
- **Linha de all-clear com avatar cinza de bot na aba Items (`#46740`):**
  - Exibe no topo da aba Items uma linha limpa de "tudo resolvido" com avatar monocromático de bot quando nenhum item demandar atenção humana imediata.
- **Store de anexos na sessão para pré-visualização de imagens ACP em memória (`#46901`):**
  - Armazena imagens geradas sem caminho em disco no attachment store da sessão ACP, expondo URIs temporárias seguras para renderização inline imediata no Native Chat UI.
- **Leitura em chunks particionados para imagens acima de 3MB em clientes pareados (`#46930`):**
  - Implementa transferência particionada via `readTextChunk` com ranges para streaming resiliente de imagens grandes entre servidor e clientes pareados sem estourar limites de mensagem.
- **Suporte a middle-click paste em editores ProseMirror no composer (`#46974`, resolve `#46953`):**
  - Conecta o manipulador nativo de `auxclick` e eventos de seleção primária ao ProseMirror, permitindo colar seleções do sistema operacional com o botão do meio do mouse.
- **Primeira linha informativa e chevron sempre visível em linhas de agentes (`#46739`):**
  - Exibe a primeira linha de texto do turno na linha do agente com truncamento elegante e mantém o chevron de expansão permanentemente visível para clareza de navegação.
- **Exclusão atômica de chats com tombstone permanente no SQLite (`#45876`):**
  - Introduz o método RPC `agentSession.delete.v1` e a opção Delete chat no menu de linha e Session History;
  - Interrompe a execução ativa com segurança, fecha abas abertas em todos os clientes pareados, exclui a linhagem de sessões `/clear` e grava tombstone permanente no SQLite para impedir re-adoção ou poluição de busca;
  - Suporta confirmação com opção de memorização "Don't ask again" configurável em Settings.
- **Linhas de chat serenas com chevron dinâmico e status na prévia (`#45881`):**
  - Posiciona o ícone da fonte à esquerda com transição suave para chevron de colapso no hover;
  - Desloca status ao vivo ("N running, N waiting") para a linha de prévia e substitui o timestamp pelo botão de menu `⋯` no hover, evitando conflitos visuais.
- **Faixa de mensagens enfileiradas limpa com ações no hover (`#46592`):**
  - Oculta botões permanentes da fila de envio, revelando ações somente no hover do mouse, foco por teclado ou toque em telas touch, alinhando a faixa à linha de atividade.
- **Menções `@` e comandos slash `/` na caixa de comentários de itens (`#46570`):**
  - Equipa a caixa de comentários de itens com os mesmos seletores de autocompletar do composer principal do chat, viabilizando menções diretas e envio de skills dedicadas.
- **Exibição de nomes canônicos do catálogo no seletor de Nova Aba (`#46583`):**
  - Resolve e exibe os nomes amigáveis dos agentes cadastrados no catálogo no picker de Nova Aba em vez de IDs internos.
- **Esqueleto (*skeleton loader*) no carregamento de itens de bots (`#46608`):**
  - Renderiza animação estruturada de esqueleto durante o carregamento assíncrono dos detalhes de itens de bots, eliminando telas vazias.
- **Continuação automática de chats após limite de uso como padrão (`#45410`):**
  - Habilita `nativeChatAutoContinueAfterUsageLimit` ativada por padrão com migração one-shot de perfis existentes no carregamento;
  - Limita a varredura pós-redefinição de cota a dois envios por rodada (mais antigos primeiro), prevenindo picos de concorrência ao reabrir múltiplos chats simultaneamente.
- **Busca por início de palavra e ordenação no autocompletar `@` de bots (`#46165`):**
  - Ranqueia menções de bots no composer do Native Chat priorizando início de palavras e escolhas recentes;
  - Preserva o prefixo `For:` antes do propósito destacado, mantém o cabeçalho de bots mesmo para bots pausados e abre menus contextuais `/` ou `$` após nomes compostos somente quando suportados pelo agente.
- **Priorização de chats interrompidos mid-turn na reinicialização (`#46009`):**
  - Ordena a retomada de chats após reinício priorizando conversas onde o agente estava no meio de um turno (`mid-reply`) para assumirem as vagas de inicialização primeiro;
  - Conversas finalizadas com apenas comandos de fundo pendentes recebem oferta de retomada sem consumir slots de agentes prioritários.
- **Suporte a pastas no menu de menções `@` do chat (`#46127`):**
  - Lista diretórios do repositório/workspace no menu suspenso de autocompletar ao digitar `@`, inserindo caminhos normalizados de pastas diretamente no composer.
- **Citações "Add to chat" renderizadas como chips compactos (`#46362`):**
  - Exibe seleções de código e texto capturadas via "Add to chat" como chips interativos com rótulo de arquivo e linha, despoluindo o composer e permitindo clique para abrir a origem.
- **Visualização inline de imagens em comentários de itens e perguntas (`#46281`):**
  - Renderiza capturas de tela e arquivos de imagem anexados a comentários de itens diretamente no feed de chat.
- **Ocultação de mensagens vazias de assistente no desktop e mobile (`#46311`):**
  - Suprime a renderização de bolhas e cartões de mensagens de assistente vazias em turnos sem saída de texto.
- **Linhas compactas de atividade com fusão de worker e link de item (`#46316`):**
  - Mantém linhas de atividade em layout de linha única e funde a indicação de inicialização de worker com o link direto para o item.
- **Preservação de instruções permanentes e `_meta` em sessões Antigravity (`#46368`, resolve `#46367`):**
  - Realiza o merge em camadas de `_meta` no servidor ACP, assegurando que `setup._meta` não destrua `launch.sessionMeta` e garantindo que `SOUL.md` e `MEMORY.md` permaneçam ativos durante a sessão.
- **Identificação visual de modelo autoselecionado no Antigravity (`#46309`):**
  - Exibe no cabeçalho e na barra de status o modelo exato escolhido automaticamente pelo Antigravity.
- **Sincronização imediata de `/rename` e `/name` do Claude com o título da aba do chat (`#44461`, resolve `#40998`):**
  - Monitora o envio de comandos `/rename` ou `/name` no Native Chat e captura o frame `session_title_changed` emitido pelo Claude durante a resposta para atualizar atômica e diretamente o nome de usuário da conversa (`setUserName`), refletindo o novo título na aba e no Session History.
- **Restauração de saídas de `/recap` na reabertura de chats Claude (`#44808`):**
  - Reconstitui o frame sintético de assistente a partir das linhas salvas `system/local_command` do transcript durante a reidratação, decodificando o comando como `command-output` e preservando a saída do `/recap` após reboots ou reaberturas de aba.
- **Teto de 8 MiB de live-text por subscriber e encerramento limpo de streams lentos (`#43994`):**
  - Implementa um limite rígido de 8 MiB para o texto ao vivo acumulado (em entrega + aguardando) em cada assinante (`subscriber-live-text-cap.ts`);
  - Quando um subscriber ultrapassa esse teto, seu stream é finalizado de forma autônoma sem afetar outros chats ou o orçamento global, permitindo que o cliente frontend restabeleça a conexão e continue a leitura suavemente a partir do seu cursor de histórico;
  - Desacopla leitores hospedados (*hosted readers*) para processos utilitários externos com retenção limitada e anotações diagnósticas de crash (`orca-retained-bytes`).
- **Linhas compactas de status para mensagens entre agentes com estado gravado do worker (`#44413`):**
  - Condensa avisos de início, tarefas e atualizações de workers em linhas compactas de status com o ícone do agente emissor, texto `"Update from <name>"`, botão de cópia e detalhes expansíveis sob demanda;
  - Vincula o badge ao estado real gravado do despacho (*dispatch state*), exibindo spinner durante execução e badge vermelho em falha, sem que restarts de workers corrompam linhas de histórico prévias.
- **Estabilização da faixa de agentes durante atualizações de sessão (`#44508`):**
  - Mantém a barra de agentes estática e imune a saltos visuais durante updates de sessão no Native Chat, eliminando reflows indesejados.
- **Streaming de grandes saídas de ferramentas na exportação de contexto (`#44203`):**
  - Transmite saídas volumosas de ferramentas diretamente em streaming durante a exportação do contexto da conversa, sem alocação do conteúdo integral na memória heap.
- **Renderização e ciclo de vida de subagentes OpenCode no Chat UI (`#39276`):**
  - Implementa o gancho de dialeto ACP `childSession` para capturar frames filhos marcados com `_meta["opencode/child-session"]`,
    vinculando o ID do agente filho à linha do tempo da conversa;
  - Cria um cartão dedicado com o nome da tarefa delegada, exibe o status ao vivo na faixa de agentes acima do composer e
    alinha as ferramentas e comandos do filho sob o seu próprio cartão.
- **Pré-visualização read-only de chats no Agent Dashboard (`#39082`):**
  - Carrega a transcrição da conversa sob demanda em modo somente leitura reutilizando o protocolo de histórico e os
    componentes de renderização de mensagens, sem inicializar provedores pesados nem interferir nas observações de PR links.
- **Notificações opt-in exclusivamente para perguntas de agentes (`#39079`):**
  - Adiciona o controle "Questions Only" nas preferências de notificação do desktop e push móvel;
  - Discrimina perguntas reais de pedidos comuns de permissão de ferramentas, notificando o operador apenas quando sua
    resposta for indispensável para o agente avançar.
- **Agrupamento de subagentes na sidebar e badges de atividade ao vivo (`#38995`):**
  - Categoriza sessões flutuantes e subagentes filhos em agrupamentos colapsáveis na barra lateral de workspaces com badges ao vivo.
- **Ação "Background" para ferramentas e subagentes Claude (`#38963`):**
  - Adiciona o botão "Background" ao lado da ferramenta em execução no chat e na barra expandida de tarefas, liberando a conversa.
- **Worker threads dedicadas para o SQLite de Session History (`#38945`):**
  - Isola a gravação do banco em uma thread dedicada e leituras/buscas FTS em conexões WAL em threads de leitura separadas com timeout de 10s.
- **Contabilização de processos fora de terminais no Resource Usage (`#39013`):**
  - Lê as tags de ambiente `ORCA_WORKTREE_ID` e `ORCA_PANE_KEY` para rastrear processos desanexados, computando como `outsideTerminals`.
- **Barra de atividade e visualizador de subagentes no Native Chat (`#38632`, `#38633`, `#38640`):**
  - Barra de atividade no desktop e folha expansível (*sheet*) no mobile listando todos os subagentes da conversa com estado vivo.
- **Supressão de textos de harness do Claude nos títulos de abas (`#39606`, resolve `#37379`):**
  - Impede que marcações de meta/harness (como `<local-command-caveat>`) sejam promovidas a título de sessão de fallback,
    preservando o título ao vivo (`✳ Claude Code`) após execuções de `/clear`.
- **Prevenção de falso status 'working' por OSC 7501 do OpenCode (`#39649`, resolve `#39619`):**
  - Filtra as sequências de escape OSC 7501 emitidas pelo OpenCode em instâncias compartilhadas (`opencode serve --service`),
    impedindo que o broadcast de status marque abas ociosas como em execução e garantindo que apenas a aba dona do comando
    exiba o status `working`.
- **Preservação de imagens geradas integradas à resposta final (`#40935`):**
  - Mantém imagens concluídas acopladas ao cartão da resposta final do assistente no desktop e cliente móvel, mesmo quando o
    artefato chega após o início do streaming de prosa;
  - Desduplica artefatos já referenciados no corpo Markdown e assegura que a projeção de histórico do SQLite retenha as
    imagens e seus controles intactos ao revisitar a sessão.
- **Exibição de modelo e nível de esforço de subagentes no painel (`#41008`):**
  - Propõe exibir badge compacto (ex.: `Opus · high`) ao lado da contagem de tokens na linha de cada subagente ativo no
    painel de agentes, extraindo a informação de `.claude/projects/.../subagents/agent-<id>.meta.json` e dos cabeçalhos de mensagens.
- **Exibição de modelo, ferramenta corrente e resultado de subagentes no chat (`#41766`):**
  - Expande as linhas de subagentes no Native Chat ("Kicked off N subagents") e Mobile: adiciona pill com modelo e nível de esforço (`Opus 5.5 · High`, `GPT-5.5 · XHigh`), linha secundária com a ferramenta ativa (ex.: `Read: src/auth/session.ts`) e, ao concluir, o texto do resultado final;
  - Adiciona hover card com role (`General purpose`, `Explore`), modelo, esforço, estado, tempo decorrido, tokens e prévia do texto;
  - Estende `NativeChatSubagentEntry` com campos opcionais `agentType`, `model`, `effort`, `operation` e `lastMessage` reconciliados do registro de child-work de Claude e Codex.
- **Importação de transcrições Kimi Code e adoção de conversas CLI (`#41955`):**
  - Implementa `kimi-transcript-import.ts` e parseador de eventos de conversas CLI do Kimi Code (`session_index.jsonl`), convertendo turnos, chamadas de ferramenta e raciocínio em mensagens nativas estruturadas;
  - Adiciona suporte no fluxo `structured-agent-cli-conversation-adoption.ts` para que sessões CLI ativas ou salvas do Kimi Code sejam importadas ou adotadas pelo Native Chat com reconciliação transparente de estado.
- **Descarte de referências de subagentes ao fechar abas de chat (`#42254`):**
  - Limpa imediatamente o mapa `activeSubagentByTab` ao fechar uma aba de chat, liberando referências em memória de subagentes abertos.
- **Barra de subagentes ativos no mobile para chats em terminal (`#42305`, resolve `#42099`):**
  - Renderiza a faixa de subagentes ativos também no cliente mobile para sessões baseadas em terminal, mantendo paridade com o chat estruturado.
- **Persistência estável de perguntas pendentes através de reinicializações (`#42307`):**
  - Restaura o estado de perguntas de escolha ou texto interativo sem disparar nova inferência ou acordar precocemente o agente antes da entrada do usuário.
- **Correspondência exata de versão do modelo Claude no banner (`#42287`, resolve `#42286`):**
  - Ajusta a regex de parse do modelo para reconhecer com precisão versões pontuais completas (exibindo `Claude Opus 5.5` em vez de simplificar para `Opus 5`).
- **Abertura de subagentes em painel deslizante (*slide-up sheet*) dentro do chat (`#42455`):**
  - Em vez de substituir toda a página de conversa, clicar em um subagente abre um painel modal deslizante ocupando 80% do painel de chat, com cantos arredondados e scrim suave sobre a conversa pai;
  - Mantém o chat principal, sua posição de rolagem e o rascunho do composer montados e intactos por baixo;
  - Exibe cabeçalho contextual com link de retorno hierárquico, seletor de subagentes aninhados, status, tokens, tempo e botão Stop;
  - Fecha facilmente com <kbd>Esc</kbd>, clique no scrim ou no botão fechar, retornando o foco diretamente para a linha de origem.
- **Suporte a subagentes no Pi Native Chat (`#42448`):**
  - Habilita a detecção e renderização visual de subagentes também em conversas estruturadas conduzidas pelo agente Pi.
- **Faixa de worker temporário no topo de chat workers (`#43521`):**
  - Renderiza uma faixa destacada no topo da interface de chat workers indicando que se trata de uma tarefa efêmera/temporária, equiparando à exibição em terminais.
- **Identificação de plugin em mensagens enviadas (`#43425`, resolve `#43424`):**
  - Exibe nome e ícone de plugins em badges dedicados nas mensagens e e-mails despachados por eles dentro do Native Chat.
- **Autocompletar com menções `@` para outros chats e terminais (`#43462`):**
  - Propõe suporte a menções digitadas com `@` no composer do chat para referenciar diretamente conversas e terminais ativos.
- **Chips navegáveis para citações "Add to chat" (`#43461`):**
  - Propõe exibir citações adicionadas ao chat como chips visuais com clique de navegação direta para a posição de origem no terminal ou arquivo.
- **Retenção de chats aguardando na restart list (`#43474`):**
  - Mantém chats que dependem de ação humana na lista de reinício pendente após reboot do app, em vez de retomá-los de modo automático.
- **Limitação de memória em filas de entrega e histórico de chat (`#43456`):**
  - Aplica teto máximo a filas de eventos de entrega e buffers de leitura histórica, prevenindo consumo descontrolado de RAM quando consumidores ficam lentos.
- **Montagem tardia (lazy) de abas de chat ocultas (`#43516`):**
  - Adia a montagem pesada do DOM e da árvore React da view de chat até o momento em que a aba correspondente é efetivamente exibida pelo usuário.
- **Indicação e acompanhamento de worktree quando o agente migra (`#43385`, Issue `#43366`):**
  - Quando um agente associado a um chat migra ou é transferido para outro worktree, o chat exibe uma faixa de contexto informando para qual worktree o agente se moveu e oferece atalho para seguir ou alternar para o novo espaço de trabalho.
- **Entrega direta de mensagens entre agentes no Native Chat (`#43380`):**
  - Restaura a entrega direta e síncrona de mensagens emitidas por outros agentes e subagentes diretamente para a sessão de chat ativa, eliminando intermediários bloqueantes.
- **Presets rápidos de modelo, esforço e velocidade no Chat (`#43607`, resolve `#43599`):**
  - Adiciona botões de atalho/chips de presets configuráveis posicionados diretamente abaixo do slider de velocidade do Native Chat, permitindo alternar combinações frequentes de modelo e esforço de raciocínio com um único clique.
- **Configuração de tecla de envio `nativeChatSendKey` (`#43600`, resolve `#43595`):**
  - Introduz a configuração `nativeChatSendKey` (`"enter"` ou `"shiftEnter"`), permitindo configurar Shift+Enter para enviar a mensagem e Enter para criar nova linha sem envio acidental.
- **Listagem de painéis de agentes antes do primeiro status report em anotações (`#43562`):**
  - No menu "Send notes to", faz fallback para o título do terminal de todos os painéis, permitindo direcionar anotações visuais para agentes logo após a criação da aba, mesmo antes do primeiro turno ou status report.
- **Sincronização do realce de Activity com o workspace e aba ativa (`#43567`):**
  - Sincroniza o highlight da view de Activity na barra lateral esquerda com o agente ou workspace atualmente em foco na área de abas.
- **Formatação de resumos de raciocínio Claude entre execuções de ferramentas (`#43610`):**
  - Propõe exibir os resumos de pensamento do Claude como linhas independentes e colapsáveis intercaladas entre as chamadas de ferramentas no Chat UI.
- **Parse e estilização de tags `<advisory>` (`#43549`):**
  - Trata tags de conselho `<advisory>` do harness OMP com componente visual dedicado em vez de exibi-las como mensagem crua de usuário.
- **Auto-hide com revelação por hover da barra lateral esquerda (`#43597`):**
  - Propõe opção para ocultar automaticamente a barra lateral e revelá-la suavemente ao passar o cursor pela margem esquerda da janela.
- **Desacoplamento de streaming e eliminação de contenção em "Sending..." (`#43908`, resolve `#43988`):**
  - Separa as filas de escrita do journal de chat para que novas mensagens e prompts não compitam diretamente na mesma fila FIFO de chats em streaming simultâneo;
  - Ajusta os checkpoints do WAL para evitar que picos de escrita congelem novos turnos de conversa.
- **Expurgo automático de linhas de status de chats encerrados (`#43954`):**
  - Limpa imediatamente as entradas de status de sessões fechadas do feed do processo principal, eliminando o acúmulo contínuo de memória durante a vida útil do host.
- **Contabilização de árvores de processos de Chat no Resource Manager (`#43983`):**
  - Rastreia e agrega o consumo de CPU e RAM das árvores de processos dos agentes em execução no Native Chat, integrando-as à exibição do Resource Manager.
- **Persistência de limpeza de atividades falhadas na view de Activity (`#44003`):**
  - Grava duravelmente o descarte de linhas de falha na view de Activity, evitando seu retorno espúrio após reidratação de estado.
- **Preservação do menu Copy nativo para texto de chat selecionado em navegadores móveis (`#42965`):**
  - Ajusta os manipuladores de toque e seleção CSS/DOM no cliente mobile web para reter o menu de contexto nativo do sistema operacional ao selecionar texto de conversa, garantindo acesso direto à ação "Copy".

## O que fazer

- Suportar exclusão de chat via RPC `agentSession.delete.v1` com tombstone permanente no SQLite (`#45876`).
- Implementar linhas de chat limpas com chevron colapsável no ícone da fonte e status na prévia (`#45881`).
- Suprimir botões permanentes na faixa de mensagens enfileiradas revelando ações sob hover ou foco (`#46592`).
- Adicionar autocompletar com menções `@` e comandos `/` na caixa de comentários de itens (`#46570`).
- Exibir nomes canônicos de catálogo de agentes no seletor de Nova Aba (`#46583`).
- Renderizar skeleton loader durante o carregamento de detalhes de itens de bots (`#46608`).
- Ativar continuação automática de chats após limites de uso por padrão com limite de dois envios concorrentes pós-reset (`#45410`).
- Adotar busca por início de palavras e seleções recentes no menu de menções `@` de bots (`#46165`).
- Priorizar a retomada de chats interrompidos mid-turn no reinício do sistema antes de tarefas finalizadas em background (`#46009`).
- Listar pastas e diretórios no popover de menções `@` do composer (`#46127`).
- Renderizar trechos de código de "Add to chat" como chips visuais clicáveis (`#46362`).
- Exibir imagens de comentários de itens inline no fluxo de conversa do chat (`#46281`).
- Ocultar mensagens vazias de assistente no desktop e mobile (`#46311`).
- Compactar linhas de atividade de chat em uma única linha com link do item (`#46316`).
- Preservar instruções permanentes do Antigravity mesclando metadados de sessão no ACP (`#46368`, resolve `#46367`).
- Exibir o modelo selecionado dinamicamente pelo Antigravity (`#46309`).
- Sincronizar comandos `/rename` e `/name` do Claude diretamente com o título da aba e do Session History (`#44461`, resolve `#40998`).
- Restaurar saídas do comando local `/recap` na reabertura de chats Claude e no Resume in New Chat (`#44808`).
- Limitar a 8 MiB o buffer de texto ao vivo de cada subscriber no processo principal com retomada por cursor (`#43994`).
- Exibir mensagens entre agentes como linhas compactas de status vinculadas ao estado do despacho (`#44413`).
- Estabilizar a faixa de agentes contra cintilações durante atualizações de sessão no Native Chat (`#44508`).
- Transmitir saídas volumosas de ferramentas em streaming na exportação de contexto do chat (`#44203`).
- Preservar o menu de contexto nativo de cópia para texto de chat selecionado no cliente móvel (`#42965`).
- Isolar filas de escrita de novos prompts do streaming de chats concorrentes para evitar travamentos em "Sending..." (`#43908`, resolve `#43988`).
- Desalocar registros de status de chats fechados do processo principal (`#43954`).
- Contabilizar processos de sessões do Native Chat no Resource Manager (`#43983`).
- Assegurar que linhas de atividade com falha descartadas permaneçam limpas após reidratação (`#44003`).
- Adicionar presets rápidos de modelo, esforço de raciocínio e velocidade no Native Chat (`#43607`, resolve `#43599`).
- Suportar a configuração `nativeChatSendKey` para permitir envio via Shift+Enter (`#43600`, resolve `#43595`).
- Listar painéis de agentes recém-iniciados no menu "Send notes to" via fallback de título de terminal (`#43562`).
- Sincronizar o destaque visual do item de Activity na barra lateral esquerda com a aba e workspace ativos (`#43567`).
- Exibir resumos de pensamento (thinking) do Claude intercalados entre ferramentas no chat nativo (`#43610`).
- Tratar e estilizar tags `<advisory>` do harness OMP com componente dedicado (`#43549`).
- Avaliar auto-hide da barra lateral com reveal por hover na borda (`#43597`).
- Exibir faixa de worker temporário no topo de chat workers (`#43521`).
- Identificar plugin de origem com nome e ícone em mensagens e mails do chat (`#43425`, resolve `#43424`).
- Adotar autocompletar com menções `@` para chats e terminais no composer (`#43462`).
- Renderizar citações "Add to chat" como chips clicáveis de navegação para a fonte (`#43461`).
- Reter conversas aguardando confirmação humana na restart list sem retomada cega (`#43474`).
- Limitar memória de buffers de entrega e leitura histórica no Native Chat (`#43456`).
- Implementar montagem tardia (lazy) da view de chat apenas quando a aba for exibida (`#43516`).
- Exibir faixa indicadora e navegação de worktree quando o agente de um chat migrar para outro workspace (`#43385`, Issue `#43366`).
- Assegurar a entrega direta de mensagens entre agentes e subagentes no Native Chat (`#43380`).
- Abrir subagentes em sheet deslizante sobre o chat nativo preservando o contexto pai (`#42455`).
- Renderizar subagentes no Pi Native Chat (`#42448`).
- Exibir barra de subagentes ativos no mobile para chats de terminal (`#42305`, resolve `#42099`).
- Preservar perguntas pendentes em reinicializações sem disparos espúrios de modelo (`#42307`).
- Exibir versão pontual exata do modelo Claude no banner (`#42287`, resolve `#42286`).
- Descartar referências e estado de subagentes abertos imediatamente ao fechar a respectiva aba de chat (`#42254`).
- Suportar importação de transcrições e adoção de conversas CLI do Kimi Code no Native Chat (`#41955`), permitindo transição contínua entre terminal e UI nativa.
- Exibir modelo, ferramenta ativa e resultado final de cada subagente nas linhas de subagentes do Native Chat e Mobile (`#41766`), com pills e hover card informativo.
- Integrar imagens geradas ao cartão da resposta final no chat nativo (`#40935`), evitando perdas e duplicações.
- Adotar badges de identificação de modelo e esforço de raciocínio de subagentes no painel de agentes (`#41008`).
- Adotar a supressão de textos de harness em títulos de abas do Claude (`#39606`).
- Isolar sessões irmãs do OpenCode no mesmo serviço (`#39649`, `#39619`), contendo sequências OSC 7501 e computando `working` apenas para a sessão ativa e seus filhos reais.
- Adotar a pré-visualização read-only de chats no Agent Dashboard (`#39082`) e o filtro de notificações de perguntas (`#39079`).
- Adotar o suporte nativo a subagentes OpenCode no Chat UI (`#39276`).
- Adotar o agrupamento visual de subagentes na sidebar (`#38995`) e a ação de backgrounding de ferramentas (`#38963`) no `brza-studio`.
- Portar o isolamento em threads de workers para o SQLite de histórico (`#38945`) e o rastreamento de processos órfãos (`#39013`).
- Integrar store de anexos da sessão para renderizar imagens de ferramentas ACP sem caminho físico (`#46901`).
- Suportar leitura particionada em faixas (chunked ranges) para anexos de imagens > 3MB em sessões pareadas (`#46930`).
- Tratar evento de paste com botão do meio do mouse no composer ProseMirror no Linux/desktop (`#46974`, resolve `#46953`).
- Exibir a primeira linha de conteúdo e chevron sempre visível nas linhas de agentes do chat (`#46739`).
- Gerar diffs delimitados apenas às linhas alteradas em arquivos grandes > 256 KiB via ACP (`#47016`, resolve `#47021`).
- Reter resultados por correspondência de título em buscas de sessões quando o FTS retornar vazio (`#47080`, refs `#47055`).
- Exibir perguntas abertas de agentes em comentários de itens sem truncamento antes da resposta (`#47076`).
- Garantir legibilidade mínima de item pills em linhas Started de mensagens do chat (`#47084`).
- Renderizar linha de all-clear com avatar monocromático de bot na aba Items quando não houver pendências (`#46740`).
- Migrar mensagens enfileiradas e encerrar com aviso itens de conectores ao trocar de chat ativo (`#47200`).
- Liberar o processamento de correio de outros agentes após falhas de turno não relacionadas a limite de uso (`#47220`).
- Suportar anotação e vinculação de itens e workers entre diferentes agentes na árvore de itens (`#47191`).
- Aplicar `overflow-wrap: anywhere` em sumários de tarefas em background para evitar alargamento da coluna de chat (`#47359`, resolve `#47358`).
- Adotar o status `Waiting` e respectivo detalhamento no hover card e telas de itens (`#47308`, `#47309`, `#47429`).
- Reter opções completas (modo Plan/Build, modelo, esforço e steer) ao migrar mensagens enfileiradas (`#47337`).
- Sincronizar envio de respostas compostas em itens aguardando resposta humana (`#47464`, `#47461`, `#47385`, `#47372`).
- Exibir botões Edit e Delete no hover/foco e reter Steer em todas as linhas da fila de envio (`#47346`).




