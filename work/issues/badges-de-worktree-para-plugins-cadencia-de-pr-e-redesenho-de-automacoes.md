---
status: open
description: Suporte a Hermes e Droid (#49463, #49461, #49456), roteamento de lembretes (#49452) e fan-out de bots em grupos (#49436).
scope:
  - brza-studio
  - workspace
  - brza-workflow
priority: high
opened: 2026-11-10
tags:
  - tooling
  - design
  - infra
references:
  - https://github.com/stablyai/orca/pull/49005
  - https://github.com/stablyai/orca/pull/48931
  - https://github.com/stablyai/orca/pull/48897
  - https://github.com/stablyai/orca/pull/48872
  - https://github.com/stablyai/orca/pull/48722
  - https://github.com/stablyai/orca/pull/48827
  - https://github.com/stablyai/orca/pull/48876
  - https://github.com/stablyai/orca/issues/49051
  - https://github.com/stablyai/orca/issues/49045
  - https://github.com/stablyai/orca/issues/48978
  - https://github.com/stablyai/orca/issues/48941
  - https://github.com/stablyai/orca/issues/48927
  - https://github.com/stablyai/orca/pull/48837
  - https://github.com/stablyai/orca/pull/48390
  - https://github.com/stablyai/orca/pull/48813
  - https://github.com/stablyai/orca/pull/48630
  - https://github.com/stablyai/orca/pull/48673
  - https://github.com/stablyai/orca/pull/48660
  - https://github.com/stablyai/orca/pull/48774
  - https://github.com/stablyai/orca/pull/48087
  - https://github.com/stablyai/orca/issues/48700
  - https://github.com/stablyai/orca/issues/48790
  - https://github.com/stablyai/orca/issues/48826
  - https://github.com/stablyai/orca/pull/47907
  - https://github.com/stablyai/orca/pull/47901
  - https://github.com/stablyai/orca/pull/46794
  - https://github.com/stablyai/orca/pull/48487
  - https://github.com/stablyai/orca/pull/47381
  - https://github.com/stablyai/orca/pull/48496
  - https://github.com/stablyai/orca/pull/48477
  - https://github.com/stablyai/orca/pull/47789
  - https://github.com/stablyai/orca/pull/48621
  - https://github.com/stablyai/orca/issues/48615
  - https://github.com/stablyai/orca/pull/48413
  - https://github.com/stablyai/orca/pull/48454
  - https://github.com/stablyai/orca/pull/48393
  - https://github.com/stablyai/orca/pull/48348
  - https://github.com/stablyai/orca/pull/48431
  - https://github.com/stablyai/orca/issues/48446
  - https://github.com/stablyai/orca/pull/48243
  - https://github.com/stablyai/orca/commit/9233301cd74
  - https://github.com/stablyai/orca/pull/48215
  - https://github.com/stablyai/orca/commit/96692d810c8
  - https://github.com/stablyai/orca/pull/48142
  - https://github.com/stablyai/orca/issues/48138
  - https://github.com/stablyai/orca/pull/48087
  - https://github.com/stablyai/orca/pull/48005
  - https://github.com/stablyai/orca/pull/48007
  - https://github.com/stablyai/orca/issues/48085
  - https://github.com/stablyai/orca/issues/48136
  - https://github.com/stablyai/orca/pull/47938
  - https://github.com/stablyai/orca/pull/47897
  - https://github.com/stablyai/orca/issues/47888
  - https://github.com/stablyai/orca/commit/4bd55254c3a
  - https://github.com/stablyai/orca/commit/7a7b8b981dc
  - https://github.com/stablyai/orca/commit/b73ce0a1619
  - https://github.com/stablyai/orca/commit/1e56e0fc6a3
  - https://github.com/stablyai/orca/pull/49155
  - https://github.com/stablyai/orca/pull/49069
  - https://github.com/stablyai/orca/issues/49269
  - https://github.com/stablyai/orca/issues/49134
  - https://github.com/stablyai/orca/issues/49159
  - https://github.com/stablyai/orca/issues/44132
  - https://github.com/stablyai/orca/pull/49463
  - https://github.com/stablyai/orca/pull/49461
  - https://github.com/stablyai/orca/pull/49456
  - https://github.com/stablyai/orca/pull/49452
  - https://github.com/stablyai/orca/pull/49438
  - https://github.com/stablyai/orca/pull/49436
  - https://github.com/stablyai/orca/pull/49423
  - https://github.com/stablyai/orca/pull/49352
  - https://github.com/stablyai/orca/pull/48439
  - https://github.com/stablyai/orca/issues/49462
  - https://github.com/stablyai/orca/issues/49460
  - https://github.com/stablyai/orca/issues/49397
  - https://github.com/stablyai/orca/issues/49299
  - https://github.com/stablyai/orca/issues/47183
---

# Badges de worktree para plugins, cadência de PR e redesenho de automações

Rastreado dos PRs abertos no upstream [`stablyai/orca#47938`](https://github.com/stablyai/orca/pull/47938),
[`stablyai/orca#47897`](https://github.com/stablyai/orca/pull/47897),
[`stablyai/orca#47879`](https://github.com/stablyai/orca/pull/47879) (commit `4bd55254c3a`),
[`stablyai/orca#47865`](https://github.com/stablyai/orca/pull/47865) (commit `7a7b8b981dc`),
[`stablyai/orca#47876`](https://github.com/stablyai/orca/pull/47876) (commit `b73ce0a1619`),
[`stablyai/orca#47855`](https://github.com/stablyai/orca/pull/47855) (commit `1e56e0fc6a3`),
além da issue [`stablyai/orca#47888`](https://github.com/stablyai/orca/issues/47888),
[`stablyai/orca#47726`](https://github.com/stablyai/orca/pull/47726),
além das issues [`stablyai/orca#47796`](https://github.com/stablyai/orca/issues/47796),
[`stablyai/orca#47795`](https://github.com/stablyai/orca/issues/47795),
[`stablyai/orca#47794`](https://github.com/stablyai/orca/issues/47794) e
[`stablyai/orca#47793`](https://github.com/stablyai/orca/issues/47793),
[`stablyai/orca#47491`](https://github.com/stablyai/orca/pull/47491),
[`stablyai/orca#47479`](https://github.com/stablyai/orca/pull/47479) (resolve Issue [`#47386`](https://github.com/stablyai/orca/issues/47386)),
[`stablyai/orca#47189`](https://github.com/stablyai/orca/pull/47189),
[`stablyai/orca#47483`](https://github.com/stablyai/orca/pull/47483),
[`stablyai/orca#46945`](https://github.com/stablyai/orca/pull/46945) (resolve Issue [`#46919`](https://github.com/stablyai/orca/issues/46919)),
[`stablyai/orca#46933`](https://github.com/stablyai/orca/pull/46933) (resolve Issue [`#46932`](https://github.com/stablyai/orca/issues/46932)),
[`stablyai/orca#46908`](https://github.com/stablyai/orca/pull/46908) (refs Issue [`#46027`](https://github.com/stablyai/orca/issues/46027)),
[`stablyai/orca#46846`](https://github.com/stablyai/orca/pull/46846),
[`stablyai/orca#46624`](https://github.com/stablyai/orca/pull/46624) (refs Issue [`#46564`](https://github.com/stablyai/orca/issues/46564)),
[`stablyai/orca#46584`](https://github.com/stablyai/orca/pull/46584) (resolve Issue [`#46564`](https://github.com/stablyai/orca/issues/46564)),
[`stablyai/orca#46593`](https://github.com/stablyai/orca/pull/46593),
[`stablyai/orca#46522`](https://github.com/stablyai/orca/pull/46522),
[`stablyai/orca#41598`](https://github.com/stablyai/orca/pull/41598) (resolve Issue [`#41369`](https://github.com/stablyai/orca/issues/41369)),
[`stablyai/orca#41620`](https://github.com/stablyai/orca/pull/41620),
[`stablyai/orca#41332`](https://github.com/stablyai/orca/pull/41332),
[`stablyai/orca#41268`](https://github.com/stablyai/orca/pull/41268) (resolve Issue [`#41269`](https://github.com/stablyai/orca/issues/41269)),
[`stablyai/orca#41325`](https://github.com/stablyai/orca/pull/41325),
[`stablyai/orca#40557`](https://github.com/stablyai/orca/pull/40557),
[`stablyai/orca#40541`](https://github.com/stablyai/orca/pull/40541) (atendendo STA-8667),
[`stablyai/orca#40507`](https://github.com/stablyai/orca/pull/40507),
[`stablyai/orca#40534`](https://github.com/stablyai/orca/pull/40534),
[`stablyai/orca#40539`](https://github.com/stablyai/orca/pull/40539) (resolve STA-2380) e
[`stablyai/orca#40540`](https://github.com/stablyai/orca/pull/40540) (resolve Issue [`#40510`](https://github.com/stablyai/orca/issues/40510)).

## O problema

1. **Incapacidade de plugins adicionarem badges contextuais e ações nos cartões de workspace (`#40557`):**
   Plugins de workspace não tinham como sinalizar visualmente nos cartões da barra lateral que determinado checkout
   contém um projeto específico (ex.: Unity, Godot, Rust, monorrepositórios) nem oferecer atalhos diretos associados ao
   workspace sem que o usuário recorra ao Command Palette ou abra terminais manuais.
2. **Sobrecarga de CPU e taxa de requisições por sondagem contínua de PRs e CI checks (`#40541`):**
   O aplicativo revalida todos os Pull Requests e verificações de CI visíveis a cada 1–2 minutos. Em ambientes compartilhados
   com múltiplos desenvolvedores conectados via `orca serve` ou contra servidores corporativos GitHub Enterprise, essa sondagem
   em segundo plano consome núcleos de CPU e esgota limites de cota da API sem que haja ninguém olhando para a tela.
3. **Visão poluída e ações arriscadas no detalhe de automações (`#40507`):**
   A tela de detalhes de automações reunia agendamento, host, métricas de execução e custos em grids densos de difícil leitura,
   enquanto ações potencialmente destrutivas (Pausar e Deletar) ficavam expostas ao lado do botão primário de execução ("Run Now"),
   propiciando cliques acidentais.
4. **Varredura global em rajada de issues do GitHub ao restaurar/focar a janela (`#40534`):**
   Sempre que a janela do app retornava ao foco (ao desminimizar, voltar de outro Space ou reativar de tela cheia), o Orca
   disparava leituras `gh` em segundo plano para todas as issues vinculadas de cada workspace cadastrado. Em workspaces
   com centenas de issues, isso saturava a fila compartilhada de 4 slots do GitHub por minutos, travando a abertura de PRs e abas de CI.
5. **Falso pronto (`tui-idle`) em inicializações a frio do Claude Code no terminal (`#40539`):**
   Ao iniciar o Claude Code, o shell emitia imediatamente o título da janela (`claude`). Se o startup a frio do Claude
   demorasse mais de 3 segundos em silêncio, o orquestrador interpretava o terminal como pronto para entrada e injetava
   a tarefa (`orchestration dispatch --inject`) com a tela ainda em branco, perdendo a instrução.
6. **Perda do estado de tela cheia nativo após reiniciar o aplicativo (`#40540`, resolve `#40510`):**
   No macOS e Linux, se o usuário estivesse usando o aplicativo em modo tela cheia nativo do sistema operacional, qualquer
   reinício (ou atualização automática) restaurava a janela em modo janela comum, exigindo novo acionamento manual.
7. **Rotulagem genérica e errônea de gatilhos em execuções de automações (`#46624`, `#46584`, resolve `#46564`):**
   Na visão de detalhes da execução (desktop e mobile), qualquer execução de automação disparada por eventos (Webhook, GitHub, Slack) era rotulada genericamente como "Trigger: Scheduled". Além disso, quando eventos subsequentes se agrupavam em uma execução em andamento, o campo `run.event` era sobrescrito, corrompendo a identificação do gatilho original.
8. **Mensagens crípticas de ajuda e erros de sintaxe em agendamentos de automação (`#46593`):**
   A sintaxe e os erros de agendamento de automações (`automation schedule`) emitiam mensagens genéricas do parser cron sem orientar sobre formatos aceitos ou apontar o campo com erro.
9. **Dificuldade de acesso a cookies de autenticação no navegador embutido (`#46522`):**
   A opção "Import Cookies" ficava oculta no submenu profundo do navegador embutido, dificultando a importação de sessões para testes autenticados de automação e web scraping.
10. **Abertura de automação de bots apontando para o host local em vez do host de execução (`#46945`, resolve `#46919`):**
    Ao navegar para os detalhes ou editar uma automação associada a bots executando em nós remotos (WSL ou SSH), o link da interface abria o contexto no host local da UI em vez do host onde o bot reside, provocando falhas de carregamento e comandos apontando para caminhos inexistentes.
11. **Retenções de dark-wake congelando a janela de carência de execuções perdidas (`#46933`, resolve `#46932`):**
    Quando um computador acordava em modo dark-wake (suspensão parcial do sistema operacional com tela desligada), automações com hold ativo paralisavam a contagem do período de tolerância (*grace period*) para execuções agendadas atrasadas, resultando em acúmulo e disparo desordenado de tarefas quando o sistema despertava por completo.
12. **Classificação enganosa de falhas de permissão como daemons inativos no `orca status` (`#46908`, refs `#46027`):**
    Quando comandos `orca status` ou diagnósticos de runtime encontravam recusa de permissão de leitura nos descritores ou sockets do daemon, o comando reportava falsamente que o daemon não estava em execução ("not running"), em vez de sinalizar explicitamente erro de acesso de permissão.
13. **Travamentos e congelamentos da interface durante execução de hooks de workspace (`#46846`):**
    As validações de hooks de workspace executavam checagens síncronas diretamente na thread principal (main thread) do aplicativo, causando travamentos e congelamentos momentâneos no renderer durante a alternância ou abertura de workspaces volumosos.
14. **Inexistência de comando único para monitoramento de PRs com prazo limite (`#47189`):**
    Acompanhar o ciclo de vida de um Pull Request até aprovação ou término de CI exigia compor automações manuais com múltiplos gatilhos encadeados ou polling periódico, sem prazo de expiração (*deadline*) pré-estabelecido.
15. **Omissão de justificativa e contabilidade para requisições ignoradas em webhooks (`#47483`):**
    Quando um webhook recebia uma requisição não mapeada ou descartada pelas regras ativas, o log de diagnóstico não informava a razão da ausência de corpo e as chamadas ignoradas não eram contabilizadas nos comandos de inspeção.
16. **Mensagem genérica de falha em automações quando o agente falha antes do primeiro turno (`#47491`):**
    Quando um agente recusava o prompt de execução de uma automação antes do primeiro turno (por exemplo, erro de configuração no arquivo de MCP do Codex), o relatório gravava apenas "The bot's turn ended without finishing (failure)". O sistema agora registra o motivo real tipado fornecido pelo provedor (ex.: "Codex couldn't start: failed to load configuration: url is not supported for stdio...").
17. **Ocultação da URL de recebimento de webhook em linhas colapsadas de automações (`#47479`, resolve `#47386`):**
    Automações de webhook recém-criadas eram desenhadas como linhas dobradas com a opção "Copy URL" enterrada no menu de detalhes, dificultando a configuração inicial. O webhook agora se apresenta como um card de configuração com a ação "Copy URL" em destaque na frente, no menu da linha e na página de detalhes.
18. **Ausência de configuração para suprimir respostas automáticas "Fixing..." em revisões de PR (`#47726`):**
    Em fluxos acionados por revisões de pull request, agentes respondiam automaticamente a cada comentário com confirmações ruidosas ("Fixing..."), sem que o usuário pudesse configurar o agente para atuar silenciosamente.
19. **Falha genérica em execuções de automação que exigem autenticação interativa (`#47796`):**
    O estado `skipped_needs_interactive_auth` nunca era atribuído quando uma automação encontrava bloqueio por falta de sign-in, falhando de maneira genérica sem guiar o operador para a autenticação necessária.
20. **Reclassificação errônea de automações concluídas com sucesso como `dispatch_failed` após reinício (`#47795`):**
    Ao fechar e reabrir o Orca, execuções de automação que já haviam concluído seu trabalho com êxito eram indevidamente re-rotuladas como `dispatch_failed` pelo reconciliador de inicialização.
21. **Omissão de registros históricos para ocorrências perdidas enquanto o aplicativo estava fechado (`#47794`):**
    Quando o computador ou aplicativo permanecia desligado durante múltiplas execuções agendadas, apenas a ocorrência mais recente era gravada, descartando os registros das demais instâncias perdidas.
22. **Falhas de agendamento cron em transições de horário de verão (DST) e tolerância a timezones inválidos (`#47793`):**
    Agendamentos de automação baseados em cron pulavam ou duplicavam turnos durante a entrada ou saída do horário de verão e aceitavam strings de fuso horário inválidas sem validação prévia.
23. **Regra de automação `from=me` ignorando PRs criados sob a conta do proprietário (`#47879`, commit `4bd55254c3a`):**
    A regra de pull request `from=me` falhava em disparar para pull requests abertos diretamente sob a conta do dono do repositório devido a inconsistências na resolução do autor.
24. **Transbordamento visual de rótulos longos de resultado de execução na barra de workspaces (`#47865`, commit `7a7b8b981dc`):**
    Quando o resultado de uma execução de automação produzia uma mensagem de status longa, o rótulo transbordava os limites do card de automação e sobrepunha a visualização de workspaces.
25. **Execuções de automação abortadas e perdidas ao fechar o aplicativo (`#47855`, commit `1e56e0fc6a3`):**
    Ao fechar o aplicativo, execuções em andamento eram descartadas prematuramente em vez de permanecerem abertas para reavaliação no próximo boot.
26. **Execuções de automação paralisadas em telas de sign-in (`#47938`):**
    Quando uma automação exigia autenticação interativa ou oauth, a execução permanecia presa indefinidamente em vez de assentar graciosamente como `skip`.
27. **Perda de ocorrências agendadas ocorridas durante períodos de desligamento (`#47897`, refs `#47888`):**
    Ocorrências agendadas de automações que deveriam disparar durante o desligamento eram descartadas no boot em vez de serem retidas e reconciliadas.
28. **Incapacidade de remover automações de bots diretamente no painel de Atividade (`#48243`, commit `9233301cd74`):**
    No painel de Atividade / Activity panel de bots, o operador conseguia pausar automações, mas não havia opção de exclusão direta de automações obsoletas ou descontinuadas sem navegar para as telas profundas de configuração do bot.
29. **Diálogo "Add apps" desatualizado e pouco ergonômico (`#48215`, commit `96692d810c8`):**
    A tela modal para adicionar aplicativos, integrações e plugins ("Add apps") apresentava layout denso com filtros pouco intuitivos e falta de agrupamento por categoria ou contexto de uso.
30. **Espaçamento condensado e ilegível entre 'Next run' e 'Last run' no card de automações (`#48413`):**
    Os horários da próxima e da última execução colidiam visualmente em telas médias, dificultando a leitura rápida da cadência agendada.
31. **Extravasamento do botão 'Run' no cabeçalho do bot em larguras estreitas (`#48454`):**
    Em painéis de bot redimensionados, o botão 'Run' extrapolava os limites do header ou cortava outros controles sem realizar quebra suave de linha.
32. **Falta de alternador visual de família de modelos por automação de bot (`#48393`):**
    Configurar o modelo (Claude 3.5 Sonnet, Haiku, GPT-4o, etc.) exigia edição manual de texto no JSON/YAML em vez de um seletor visual de família de modelos integrado.
33. **Invisibilidade e corte de campos de webhook na barra lateral estreita (`#48348`):**
    Parâmetros e URLs de conectores webhook eram truncados sem opção de expansão quando a barra lateral estava comprimida.
34. **Atribuição incorreta de mensagens em turnos de webhook sem tipagem de proprietário (`#48431`):**
    Conectores de webhook despachavam payloads sem marcar a titularidade (`owner-typed turns`), misturando mensagens de agentes com respostas de bots externos.
35. **Despertar de bot no Slack criando novas threads em vez de responder na thread de origem (`#48446`):**
    Ao ser invocado no Slack, o bot abria um novo canal/thread separado, perdendo o histórico e contexto da conversa onde a solicitação foi feita.
36. **Turnos do Slack com respostas vazias ou nulas descartadas sem re-tentativa (`#47907`):**
    Quando o bot de Slack retornava um turno vazio por lentidão ou atraso do modelo, a integração desistia imediatamente sem retentativa, deixando a menção do usuário sem retorno.
37. **Silêncio opaco em turnos do Slack quando o bot não produz resposta final (`#47901`):**
    Se a invocação de um bot via Slack terminasse sem texto de saída (ex.: apenas chamadas de ferramentas internas), o canal permanecia sem mensagem explicativa de conclusão.
38. **Falta de timer de curta duração com descarte garantido (`#46794`):**
    Automações não tinham primitivas para agendar timers rápidos de execução única (`--once --by <duration>`) sem criar cron jobs duráveis que precisassem ser limpos manualmente.
39. **Propósito do bot invisível ou oculto logo após a criação (`#48487`):**
    Ao concluir o assistente de criação de um bot, seu propósito (*purpose*) e escopo de atuação ficavam escondidos, gerando incerteza no operador sobre a configuração inicial.
40. **Mascote e cor customizada do bot não refletidos no perfil de usuário do Slack (`#47381`):**
    Mensagens enviadas pelo bot para o Slack usavam ícones genéricos em vez de adotar a cor e mascote selecionados na interface do Orca Studio.
41. **Poluição de chats em grupo por tokens de controle `NO_REPLY` (`#48496`):**
    Bots participantes de grupos que decidiam não responder postavam a string crua `NO_REPLY` no chat da equipe em vez de suprimir silenciosamente a mensagem.
42. **Perda de cabeçalhos MCP estruturados no relay de bots e follow-ups em threads separadas (`#48477`, `#47789`, `#48621`, `#48615`):**
    O relay de bots descartava headers `Mcp-Method`, `Name` e `Param-*`, quebrando invocações contextuais de ferramentas de terceiros; ademais, follow-ups de bots abriam conversas soltas em vez de manterem-se na thread pai.

## O que o upstream implementa e corrige

- **Retentativa inteligente de turnos vazios no Slack antes de falhar (`#47907`):**
  - Re-envia o turno do Slack até duas vezes caso a resposta retorne em branco, assegurando entrega confiável.
- **Aviso explícito e claro em turnos do Slack sem resposta textual (`#47901`):**
  - Posta mensagem informativa discreta quando o agente conclui ações de ferramentas sem gerar prosa explicativa final.
- **Timer de disparo único de alta precisão (`#46794`):**
  - Introduz o parâmetro `--once --by` em agendamentos de automação, liquidando o timer atomicamente após o disparo.
- **Exibição destacada do propósito do bot na tela de conclusão (`#48487`):**
  - Apresenta card com o propósito estruturado e instruções principais logo após o assistente de criação do bot.
- **Sincronização de mascote e paleta visual do bot com o avatar do Slack (`#47381`):**
  - Renderiza o ícone e a cor oficial do bot nos envios da integração com o Slack.
- **Supressão transparente de tokens `NO_REPLY` em chats de grupo (`#48496`):**
  - Intercepta e descarta emissões de `NO_REPLY` em conversas de equipe sem gerar bolhas visuais vazias.
- **Propagação de cabeçalhos MCP no bot relay e continuidade em thread (`#48477`, `#47789`, `#48621`, `#48615`):**
  - Encaminha headers `Mcp-*` intactos pelo relay e ancora follow-ups de agentes na mesma thread de conversa original.
- **Espaçamento e tipografia clara entre horários Next run e Last run (`#48413`):**
  - Ajusta o gap e hierarquia visual dos indicadores de execução em cartões de rotinas automáticas.
- **Quebra flexível (wrap) para o botão Run no cabeçalho de bots (`#48454`):**
  - Aplica flex-wrap responsivo no cabeçalho do bot, acomodando botões de disparo mesmo em janelas compactas.
- **Seletor visual de família de modelos nas automações de bots (`#48393`):**
  - Integra dropdown com ícones e famílias de modelos (Anthropic, OpenAI, Google) diretamente no formulário de automações.
- **Campos de webhook expansíveis e legíveis na barra lateral estreita (`#48348`):**
  - Permite expandir URLs e parâmetros de webhook em popovers flutuantes em larguras reduzidas de sidebar.
- **Tipagem de proprietário em turnos de webhook (`#48431`):**
  - Identifica explicitamente o remetente em eventos recebidos por conectores de webhook para isolar mensagens.
- **Despertar contextual em threads do Slack (`#48446`):**
  - Encaminha respostas de bots diretamente para a thread de origem no Slack, mantendo o fluxo unificado.
- **Exclusão direta de automações de bots a partir do painel de Atividade (`#48243`, commit `9233301cd74`):**
  - Adiciona ação de delete no menu contextual de cada automação no Activity panel.
- **Redesenho do diálogo Add Apps (`#48215`, commit `96692d810c8`):**
  - Redesenha a experiência de descoberta e instalação de integrações e apps com categorização clara, busca aprimorada e cartões ilustrados.
- **Disparo de regras `from=me` para todos os PRs sob a conta do proprietário (`#47879`, commit `4bd55254c3a`):**
  - Corrige a checagem de autor para que regras com filtro `from=me` disparem confiavelmente para qualquer PR aberto sob a conta do dono.
- **Truncamento de rótulos de resultado de execução longos (`#47865`, commit `7a7b8b981dc`):**
  - Aplica truncamento visual nos rótulos de resultado para prevenir que mensagens longas invadam o painel de workspaces.
- **Preservação de execuções abertas através do encerramento do app (`#47855`, commit `1e56e0fc6a3`):**
  - Mantém execuções abertas gravadas no banco durante o encerramento para que o arranque do daemon as reavalie apropriadamente.
- **Assentamento de execuções bloqueadas por sign-in como skip (`#47938`):**
  - Converte automações retidas em telas de autenticação interativa no estado `skip` sem travar a fila.
- **Retenção de ocorrências agendadas perdidas entre reinicializações (`#47897`, refs `#47888`):**
  - Preserva o registro e despacho ordenado de ocorrências agendadas não executadas durante o período em que o app esteve desligado.

- **Configuração para suprimir respostas "Fixing..." em comentários de revisão (`#47726`):**
  - Adiciona configuração permitindo desativar respostas automáticas de confirmação em comentários de review de PRs, mantendo o histórico limpo e focando apenas nas correções efetivas de código.
- **Sinalização explícita de `skipped_needs_interactive_auth` em automações (`#47796`):**
  - Identifica quando uma automação é impedida por pendência de autenticação interativa, registrando o estado tipado correspondente e apresentando ação direta de sign-in na interface.
- **Preservação de status de conclusão de automações pós-reinício (`#47795`):**
  - Evita que execuções previamente finalizadas sejam marcadas como `dispatch_failed` durante o bootstrap de inicialização do aplicativo.
- **Gravação de histórico de ocorrências perdidas durante fechamento do app (`#47794`):**
  - Mantém o registro individualizado de todas as execuções de automação cron que foram perdidas enquanto o Orca esteve fechado.
- **Suporte estrito a fusos horários e transições de horário de verão (DST) em automações (`#47793`):**
  - Garante execução pontual em mudanças de horário de verão sem duplicações ou omissões e valida formalmente parâmetros `--timezone` na CLI.
- **Diagnóstico com motivo real de recusa de agente em execuções de automação (`#47491`):**
  - Grava a causa tipada emitida pelo provedor (ex.: erro de sintaxe ou configuração MCP) quando o agente recusa o prompt antes de iniciar qualquer turno, em vez de emitir mensagem genérica de falha.
- **Card de configuração e destaque da ação Copy URL em webhooks de automação (`#47479`, resolve `#47386`):**
  - Desenha webhooks recém-criados como setup cards com botão Copy URL imediato, além de adicionar a ação no menu de opções da linha e na barra de cabeçalho da página de automações.

- **Comando `orca automations watch-pr` para monitoramento completo de PRs com prazo limite (`#47189`):**
  - Adiciona o comando `orca automations watch-pr owner/repo#n`, configurando espera one-shot (`--once`) sobre os eventos `github.ci_finished`, `pr_conflicted`, `pr_merged`, `pr_closed`, `review`, `review_comment` e `comment`, com prazo padrão de 2 horas (customizável via `--for` ou `--by`);
  - Registra o gatilho `github.ci_finished` cobrindo tanto aprovações quanto falhas, cancelamentos e aprovações manuais pendentes.
- **Detalhamento e contabilidade de chamadas ignoradas em webhooks (`#47483`):**
  - Explica explicitamente no log de diagnóstico a razão de requisições ignoradas não possuírem corpo processado e inclui essas chamadas no cômputo total da verificação de integridade de webhooks.
- **Navegação de automações de bots roteada para o host correto (`#46945`, resolve `#46919`):**
  - Roteia a abertura de automações vinculadas a bots para o host proprietário (WSL, SSH ou runtime host remoto), garantindo visualização correta de logs e paths.
- **Isolamento de dark-wake holds e proteção ao período de carência de agendamentos (`#46933`, resolve `#46932`):**
  - Impede que retenções temporárias de dark-wake congelem o relógio de grace period de execuções perdidas, garantindo despacho ordenado de tarefas atrasadas ao despertar.
- **Sinalização explícita de `runtime_access_denied` em verificações de status (`#46908`, refs `#46027`):**
  - Reporta o estado específico `runtime_access_denied` em vez de falso negativo de processo parado quando houver falha de permissão no socket ou arquivo de lock do daemon.
- **Execução assíncrona de checagens de hooks de workspace fora da thread principal (`#46846`):**
  - Move a verificação e resolução de hooks de workspace para worker threads em background, preservando a fluidez de 60fps da UI durante transições de workspace.
- **Identificação real e durável de gatilhos em execuções de automação (`#46624`, `#46584`, resolve `#46564`):**
  - Registra e preserva o campo imutável `triggeredBy` no ato de criação da execução, evitando que eventos agrupados posteriormente substituam a fonte original;
  - Exibe a fonte real do evento (Webhook, GitHub, Slack, etc.) em Run Details e clientes móveis em vez de marcar genericamente como `Scheduled`.
- **Ajuda e mensagens de erro descritivas para agendamento de automações (`#46593`):**
  - Clarifica a sintaxe esperada nas mensagens de ajuda e detalha os motivos de recusa em cron expressions inválidas na CLI de automações.
- **Opção 'Import Cookies' no topo do menu do navegador embutido (`#46522`):**
  - Promove "Import Cookies" para o primeiro item do menu de opções `⋯` do navegador integrado, acelerando fluxos de autenticação em automações e testes.

- **Ponto de contribuição `contributes.worktreeBadges` para plugins (`#40557`):**
  - Permite que manifestos de plugins (`engines.orca >=1.4.256`) declarem badges condicionais nos cartões de workspace;
  - Avalia condições `when.pathExists` (com profundidade `searchDepth: 0..3` e filtro de `host`) de forma assíncrona, em lote e com cache no processo principal, sem expor dados do workspace ao worker até que uma ação seja disparada;
  - Renderiza o ícone SVG diretamente ao lado do nome do workspace e disponibiliza as ações associadas em menu dedicado e no menu de contexto do workspace;
  - Repassa contexto seguro `{ worktree, folder }` para os comandos do worker.
- **Cadência configurável de atualização de PRs (`#40541`):**
  - Adiciona `Settings → Git & Source Control → PR Auto-Refresh`:
    - `Default`: 1 min (selecionado) / 2 min (visíveis);
    - `Reduced (5×)`: 5 min / 10 min;
    - `Minimal (10×)`: 10 min / 20 min;
    - `Off`: desliga os timers em segundo plano;
  - Em servidores `orca serve`, clientes pareados compartilham a resposta em cache até a expiração do intervalo do host, desacoplando o consumo de rede do número de clientes conectados.
- **Redesenho hierárquico da visão de automações (`#40507`):**
  - Reorganiza a página de detalhes com fluxo vertical: cabeçalho com status badge e botão destacado `Run Now`, seguido de faixa de saúde (`Last run`, `Next run` e custo estimado com contagem de tokens);
  - Painéis laterais limpos para agendamento e parâmetros de execução;
  - Seção expansível para o prompt da automação com botão dedicado de cópia para a área de transferência;
  - Ações de pausa e exclusão movidas com segurança para menu dropdown "…".
- **Desativação de varreduras globais de issues no retorno da janela (`#40534`):**
  - Elimina a varredura indiscriminada de issues ao focar a janela, restringindo o refresh exclusivamente a cartões visíveis no viewport (`visible-only` com janela de 5 minutos);
  - Libera a fila concorrente do GitHub CLI para respostas imediatas em PRs, checks e merges.
- **Verificação estrita de pintura de comando (`hasTerminalCommandPainted`) no `tui-idle` (`#40539`):**
  - Exige que o processo em execução tenha efetivamente desenhado texto após o marcador de comando OSC 133;C antes de declarar o terminal como ocioso e pronto para injeção de tarefas.
- **Persistência do estado de tela cheia nativa (`#40540`):**
  - Registra a flag de fullscreen nativo nas preferências de restauração de janela e aplica `setFullScreen(true)` logo após a inicialização no desktop.
- **Eliminação de trabalho Git repetido no watch de checks de CI (`#41332`):**
  - Desacopla o monitoramento contínuo de status de CI do cálculo prévio de arquivos em conflito e detalhes de stack da branch base: 500 leituras de watch passaram de 500 fetches e 422 verificações de mesclagem (2.688 comandos Git) para zero;
  - Preserva o enriquecimento completo de arquivos conflitantes estritamente para leituras explícitas, ativas ou disparadas no mobile.
- **Suspensão de requisições de rate limit para agentes desativados (`#41268`, resolve `#41269`):**
  - Ao desativar Claude ou Codex em Settings > Agents, desconecta o `RateLimitService` do polling de cota (`api.anthropic.com` / `chatgpt.com`), prevenindo emissão de pacotes fora de túneis VPN/proxy e protegendo contas contra suspensões geográficas.
- **Atribuição de demanda Git e descoberta assíncrona de caminhos de setup (`#41325`):**
  - Substitui o spawn síncrono de processos Git no processo principal durante a preparação de scripts de setup pelo executor assíncrono com timeout de 15s, além de etiquetar demandas de catalogação e leituras de status.
- **Configurações nativas de integração e handoff escopado por workspace para plugins (`#41598`, resolve `#41369`):**
  - Adiciona painel nativo de configurações de integração para plugins (`IntegrationsPane`), permitindo parametrização direta sem abrir janelas de navegador externas;
  - Suporta handoff escopado de workspaces para agentes de plugins, validando seletores de rotas e proprietários no processo hospedeiro sem expor credenciais ou chaves sensíveis.
- **Unificação da experiência visual e navegação de páginas de automações (`#41620`):**
  - Consolida as diferentes telas de automações em uma interface unificada (Opção D do redesign), agrupando listagem de rotinas, histórico de execuções e formulário de criação em abas fluidas e consistentes com o design system.
- **API mínima de diagnósticos de plugins para o editor nativo ([`#41616`](https://github.com/stablyai/orca/issues/41616)):**
  - Propõe interface enxuta para que plugins de linter e extensões de linguagem publiquem marcadores e diagnósticos diretamente na calha e nos painéis do editor sem sobrecarga de protocolos LSP completos.

## O que fazer no BrzA Studio

1. Preservar o gatilho original de automações em `triggeredBy` e rotular execuções de eventos pela sua fonte real (`#46624`, `#46584`, resolve `#46564`).
2. Adotar mensagens de erro detalhadas e ajuda clara na validação de agendamentos cron (`#46593`).
3. Posicionar a ação 'Import Cookies' no topo do menu de contexto do navegador embutido (`#46522`).
4. Adotar as configurações nativas de integração e handoff de workspaces para plugins (`#41598`, resolve `#41369`).
5. Incorporar a navegação unificada de páginas de automações (`#41620`).
6. Avaliar a API mínima de diagnósticos de plugins para o editor nativo (`#41616`).
7. Eliminar o trabalho repetido de Git (fetches e merge checks) durante o monitoramento de checks de PR (`#41332`).
8. Desligar o polling em segundo plano de rate limits para provedores desativados em configurações (`#41268`, resolve `#41269`).
9. Tornar assíncrona a descoberta de caminhos de setup e atribuição de spans Git (`#41325`).
10. Adotar o ponto de extensão `contributes.worktreeBadges` (`#40557`) no runtime de plugins do `brza-studio`, permitindo que skills e ferramentas especializadas exibam seus badges e menus contextuais na sidebar.
11. Incorporar a configuração `prAutoRefresh` em `Settings` (`#40541`) para aliviar carga de CPU e API rate limits em máquinas compartilhadas.
12. Atualizar o layout do painel de automações (`#40507`) para melhor ergonomia de inspeção e prevenção de cliques destrutivos.
13. Adotar a atualização sob demanda (`visible-only`) de issues do GitHub ao reativar a janela (`#40534`), desobstruindo a fila da CLI.
14. Incorporar a checagem `hasTerminalCommandPainted` em `tui-idle` (`#40539`) para garantir entrega segura de comandos via `orchestration dispatch`.
15. Garantir persistência de fullscreen nativo pós-reinício (`#40540`).
16. Rotear a navegação e edição de automações de bots para o host real de execução em nós remotos e WSL (`#46945`, resolve `#46919`).
17. Manter a integridade do período de carência de automações agendadas sob despertares em dark-wake (`#46933`, resolve `#46932`).
18. Distinguir falhas de permissão de acesso ao runtime reportando `runtime_access_denied` no `brza status` (`#46908`, refs `#46027`).
19. Mover a checagem de hooks de workspace para worker threads para eliminar congelamentos na UI (`#46846`).
20. Incorporar o comando `brza automations watch-pr` com gatilho `github.ci_finished` e prazo de 2 horas (`#47189`).
21. Exibir justificativa e contagem de chamadas ignoradas em diagnósticos de webhooks (`#47483`).
22. Gravar e exibir a causa tipada real de recusa inicial de agentes em execuções de automação (`#47491`).
23. Apresentar automações de webhook em setup card com ação Copy URL destacada (`#47479`, resolve `#47386`).
24. Adicionar configuração para suprimir respostas automáticas "Fixing..." em comentários de revisão de PRs (`#47726`).
25. Atribuir o estado `skipped_needs_interactive_auth` quando automações demandarem login interativo (`#47796`).
26. Preservar o status de sucesso de automações finalizadas após reinicializações do app (`#47795`).
27. Registrar integralmente todas as ocorrências de automação cron perdidas com o app fechado (`#47794`).
28. Assegurar precisão de horários de verão (DST) e validação de `--timezone` no agendamento cron (`#47793`).
29. Ativar regras `from=me` de pull requests para qualquer PR aberto sob a conta do dono (`#47879`, commit `4bd55254c3a`).
30. Truncar rótulos compridos de resultado de automação para evitar invasão na área de workspaces (`#47865`, commit `7a7b8b981dc`).
31. Reter execuções abertas de automação durante o encerramento do app para reavaliação no boot (`#47855`, commit `1e56e0fc6a3`).
32. Concluir automações retidas em telas de autenticação como `skip` para não travar a fila (`#47938`).
33. Reconciliar e executar ocorrências agendadas perdidas entre reinicializações do aplicativo (`#47897`, refs `#47888`).
34. Ajustar layout responsivo do editor de automações para comportar painéis laterais estreitos (`#48142`, resolve Issue `#48138`).
35. Recuperar e retentar execuções de automações diante de falhas transitórias de inferência do modelo (`#48087`).
36. Exibir apenas o link permanente do PR, e não seu estado em cache, em listas de trabalho e notas de turnos (`#48005`, commit `ad96411db85`).
37. Atualizar automaticamente a listagem de PRs abertos em páginas de itens como linhas visíveis do workspace (`#48007`, commit `56e27bb625c`).
38. Resolver contenção em hover card de workspace quando referências incluem número isolado de PR vinculado (`#48085`).
39. Sincronizar bidirecionalmente o status de itens de bots com suas respectivas issues vinculadas no Linear (`#48136`).
40. Adicionar ação de exclusão de automações de bots diretamente no painel de Atividade (`#48243`, commit `9233301cd74`).
41. Incorporar o redesign moderno do diálogo Add Apps para instalação de plugins e integrações (`#48215`, commit `96692d810c8`).
42. Refinar espaçamento e hierarquia tipográfica entre Next run e Last run no card de rotinas (`#48413`).
43. Aplicar flex-wrap para acomodar o botão Run no cabeçalho de bots em larguras comprimidas (`#48454`).
44. Disponibilizar o seletor visual de famílias de modelos na configuração de automações de bots (`#48393`).
45. Tornar campos e URLs de conectores webhook expansíveis em popovers na sidebar estreita (`#48348`).
46. Incluir tipagem de proprietário (`owner-typed turns`) em mensagens recebidas via webhooks (`#48431`).
47. Reter contexto de threads originais em respostas de bots no Slack (`#48446`).
48. Reenviar turnos do Slack que retornem vazios antes de registrar falha de entrega (`#47907`).
49. Emitir aviso explicativo no Slack quando turnos do bot concluírem sem prosa final (`#47901`).
50. Suportar agendamento de timers únicos rápidos com `--once --by` (`#46794`).
51. Exibir com destaque o propósito e escopo do bot na tela pós-criação (`#48487`).
52. Sincronizar mascote e cor do bot como avatar oficial em mensagens do Slack (`#47381`).
53. Suprimir mensagens `NO_REPLY` em conversas de grupo de bots (`#48496`).
54. Propagar cabeçalhos MCP estruturados no relay e manter follow-ups de bots na mesma thread (`#48477`, `#47789`, `#48621`, `#48615`).
55. Permitir silenciar (mute) notificações de forma individual por bot (`#48837`).
56. Reler visualização aberta de itens de bot quando respostas recusadas forem emitidas de views fechadas (`#48390`).
57. Restringir paginação de cartões de itens de bots estritamente à sua seção de status (`#48813`).
58. Desobrigar helper de postar na thread do requisitante ao processar emails de status ou perguntas de bots (`#48630`).
59. Exibir modal de confirmação de troca de agente posicionado acima do seletor aberto (`#48673`).
60. Aceitar wrappers de shell com aspas no padrão shlex no comando Look around para salvar sugestões do Codex (`#48660`).
61. Garantir que atribuição de propriedade de bot ocorra exclusivamente sob proveniência verificada (`#48774`).
62. Recuperar automaticamente falhas de modelo em páginas de execução de automações (`#48087`).
63. Permitir que rotinas de automação agendadas publiquem resultados diretamente em grupos de bots (`#48700`).
64. Corrigir falha em disparos de eventos de automação de bots (pr_opened, review_requested) (`#48790`).
65. Ajustar destaque de seleção de cards na lista de bots para não invadir a barra de rolagem (`#48826`).
66. Incluir membros pareados nos itens do Home de grupos de bots e no contador do badge (`#49005`).
67. Pré-selecionar o agente padrão ao abrir o formulário New bot (`#48931`).
68. Excluir demandantes de workspaces compartilhados e assentamentos sem data de 'Show N older' (`#48897`).
69. Quebrar linhas longas em notas de fechamento e critérios de Done na página do item (`#48872`).
70. Agrupar chats de bots concluídos e sem atividade por 1 dia sob 'Show N older' (`#48722`).
71. Afastar highlights de seleção de cartões da barra de rolagem na lista de bots (`#48827`).
72. Permitir opt-in para atualização automática do Codex antes do disparo de rotinas (`#48876`).
73. Configuração para desligar mensagem introdutória automática de bots ao serem adicionados a canais do Slack (`#49051`).
74. Preservar nomes de exibição não-ASCII (ex.: coreano) em bots do Slack sem sobrescrever configurações manuais (`#49045`).
75. Permitir que bots acordados por DM no Slack façam download de imagens enviadas na conversa (`#48978`).
76. Suportar indicação explícita de líder de equipe em grupos de bots (`#48941`).
77. Permitir agrupamento de bots por Projeto com contexto específico do projeto (`#48927`).
- Suportar badges dinâmicos (contadores numéricos ou pontos de alerta) nos ícones de painéis de plugins na Activity Bar (`#49269`).
- Exibir texto declarativo truncado de plugins em tooltip flutuante ao passar o cursor (hover) (`#49155`).
- Repassar variáveis de ambiente `USER`, `LOGNAME` e `USERNAME` para workers despachados por plugins (`#49069`).
- Fornecer mensagem clara de confirmação pendente em vez de código de saída de erro quando `orca plugin install` for invocado sem `--approve` (`#49134`).
- Informar aos plugins com hook `agent.launch.before` qual shell executará o comando (`#44132`).
- Estruturar fluxo de auditoria automatizada para desbloqueio de versões de plugins em análise (`#49159`).
- Instalar plugins do Hermes mesmo quando `config.yaml` possuir chaves sem valor atribuído (`#49463`, Issue `#49462`).
- Eliminar retornos de carro espúrios (`\r\r\n`) ao editar listas em arquivos CRLF no Hermes (`#49461`, Issue `#49460`).
- Preservar comandos de hooks de usuário e edições remotas concorrentes no Droid (`#49456`).
- Rotear lembretes de itens de bots diretamente para o chat proprietário correspondente (`#49452`).
- Adotar diálogo de importação de bots em linha única destacando a fonte no cabeçalho (`#49438`).
- Otimizar regressões de fan-out de membros pareados na Home de grupos de bots (`#49436`).
- Suprimir autodespertar por eco em `orca:items` para chats irmãos pertencentes ao mesmo bot (`#49423`).
- Garantir que histórico colapsado de bots releia apenas workspaces modificados (`#49352`).
- Atribuir autoria de bots estritamente baseada em proveniência verificada (`#48774`).
- Abrir links de tópicos remotos diretamente a partir das respostas do servidor (`#48439`).
- Implementar deep link para abertura direta de item específico de bot (`#49397`).
- Garantir despertar de bots do Slack em canais compartilhados externamente via Slack Connect (`#49299`).
- Adicionar comandos de CLI para arquivar e consolidar tópicos de bots no Home Chat (`#47183`).
