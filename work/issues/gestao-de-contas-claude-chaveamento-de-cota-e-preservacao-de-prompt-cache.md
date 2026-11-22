---
status: open
description: Os PRs #47079 e #46984 trazem continuidade automática de chat após troca de conta mesmo com reset desconhecido e liquidação unrun de prompt cancelado por Stop no Claude.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-03
tags:
  - chat
  - tooling
---

# Gestão de contas Claude, chaveamento de cota e preservação de prompt cache

<!-- pln-014-despacho -->
> **Despacho (PLN-014/R1.1):** classe `ausente` · casa `studio`
> Merge no upstream não muda `status`. PLN-014/R1, 2026-11-12.

Rastreado dos PRs abertos no upstream [`stablyai/orca#47079`](https://github.com/stablyai/orca/pull/47079),
[`stablyai/orca#46984`](https://github.com/stablyai/orca/pull/46984) (resolve Issue [`#46978`](https://github.com/stablyai/orca/issues/46978)),
[`stablyai/orca#46119`](https://github.com/stablyai/orca/pull/46119),
[`stablyai/orca#46002`](https://github.com/stablyai/orca/pull/46002),
[`stablyai/orca#46099`](https://github.com/stablyai/orca/pull/46099) (refs Issue [`#45979`](https://github.com/stablyai/orca/issues/45979)),
[`stablyai/orca#38581`](https://github.com/stablyai/orca/pull/38581),
[`stablyai/orca#39169`](https://github.com/stablyai/orca/pull/39169),
[`stablyai/orca#38654`](https://github.com/stablyai/orca/pull/38654),
[`stablyai/orca#38509`](https://github.com/stablyai/orca/pull/38509),
[`stablyai/orca#38298`](https://github.com/stablyai/orca/pull/38298),
[`stablyai/orca#38227`](https://github.com/stablyai/orca/pull/38227),
[`stablyai/orca#38149`](https://github.com/stablyai/orca/pull/38149),
[`stablyai/orca#38026`](https://github.com/stablyai/orca/pull/38026),
[`stablyai/orca#38201`](https://github.com/stablyai/orca/pull/38201) (Issue [`#38195`](https://github.com/stablyai/orca/issues/38195)),
[`stablyai/orca#37943`](https://github.com/stablyai/orca/pull/37943),
[`stablyai/orca#37998`](https://github.com/stablyai/orca/pull/37998),
[`stablyai/orca#38010`](https://github.com/stablyai/orca/pull/38010),
[`stablyai/orca#37567`](https://github.com/stablyai/orca/pull/37567),
[`stablyai/orca#37568`](https://github.com/stablyai/orca/pull/37568) e
[`stablyai/orca#37569`](https://github.com/stablyai/orca/pull/37569), além das issues
[`stablyai/orca#39495`](https://github.com/stablyai/orca/issues/39495),
[`stablyai/orca#39502`](https://github.com/stablyai/orca/issues/39502),
[`stablyai/orca#38618`](https://github.com/stablyai/orca/issues/38618),
[`stablyai/orca#38547`](https://github.com/stablyai/orca/issues/38547),
[`stablyai/orca#38528`](https://github.com/stablyai/orca/issues/38528),
[`stablyai/orca#38254`](https://github.com/stablyai/orca/issues/38254),
[`stablyai/orca#38224`](https://github.com/stablyai/orca/issues/38224),
[`stablyai/orca#38134`](https://github.com/stablyai/orca/issues/38134),
[`stablyai/orca#38116`](https://github.com/stablyai/orca/issues/38116),
[`stablyai/orca#38052`](https://github.com/stablyai/orca/issues/38052),
[`stablyai/orca#38024`](https://github.com/stablyai/orca/issues/38024),
[`stablyai/orca#38085`](https://github.com/stablyai/orca/issues/38085) e
[`stablyai/orca#37833`](https://github.com/stablyai/orca/issues/37833).

## O problema

1. **Mistura acidental de contas pessoais e corporativas entre projetos (`#38581`):**
   A escolha de conta Claude e Codex era puramente global no aplicativo. Ao alternar de conta para um projeto específico,
   todas as sessões abertas e novos disparos em outros repositórios passavam a consumir a nova conta. Desenvolvedores não
   conseguiam vincular um projeto de trabalho à conta corporativa e um projeto open-source ou pessoal à conta individual.
2. **Falha imediata de geradores de texto auxiliares em limites de cota (`#38654`, `#38528`):**
   Tarefas pontuais de IA (sugestão de nomes de branch, resumos de issues, mensagens de commit) falhavam silenciosamente
   ou deixavam placeholders ao bater no limite de assinatura da conta ativa, mesmo quando o usuário possuía outras contas
   válidas configuradas no sistema.
3. **Ausência de compartilhamento de logins OAuth de servidores MCP entre contas Codex (`#38618`):**
   Ao criar ou chavear contas Codex, os logins OAuth de servidores MCP não eram compartilhados, deixando todas as ferramentas
   MCP desconectadas na nova conta.
4. **Divergência entre contagem de tokens do app e `/stats` do Claude Code (`#38509`):**
   O painel Claude Usage Tracking computa totais apenas a partir dos transcripts do próprio app. O total de vida útil
   reportado nativamente pelo Claude Code via `/stats` (armazenado em `~/.claude/stats-cache.json`) não era visível, gerando
   confusão sobre o consumo histórico global da conta em múltiplos ambientes (WSL, servidores remotos).
5. **Panes limitadas por cota com crons ativos não reiniciam na troca de conta (`#38547`):**
   Ao configurar reinício automático na troca de conta ("Always restart"), uma pane do Claude que bateu no limite de 5h
   e possui agendamentos/crons de sessão fica travada aguardando indefinidamente um estado `done` que nunca chega,
   impossibilitando o chaveamento automático até que o usuário mate manualmente o processo com `/exit`.
6. **Inexistência de seleção CLI para contas Claude (`#38227`):** o comando `orca account select` aceitava apenas OpenCode
   e Devin. Não era possível alternar ou automatizar via scripts e agentes qual conta Claude ativa deve ser usada para novos
   disparos, nem rotear a seleção para hosts remotos (`--environment`).
7. **Panes de longa duração mantêm `CLAUDE_CONFIG_DIR` antigo após troca de conta (`#38254`):**
   Ao alternar a conta Claude ativa pelo app ou CLI, apenas a aba em foco ou processos recém-criados recebiam o novo ambiente;
   panes em execução contínua ou terminais abertos em segundo plano continuavam apontando para o diretório de perfil antigo,
   causando consumo fantasma na conta anterior.
8. **Parada sem ação ao atingir limite de cota no cliente mobile (`#38298`):**
   Ao receber notificações de limite de uso no app mobile, o usuário não dispunha de atalhos rápidos para alternar para uma
   conta secundária ou programar retomada automática ("Automatic continue") assim que a janela de cota resetar.
9. **Consumo desproporcional de cota em abas de chat vs. terminal (`#38224`):** usuários observaram que conversas conduzidas
   em abas de Chat UI consomem cerca de 1,5× mais da janela de 5 horas do Claude do que as mesmas tarefas em abas de
   terminal cru, devido a diferenças na injeção de preâmbulos e repasse de histórico não compactado.
10. **Subcontagem de tokens em transcripts bifurcados (`#38201`, `#38195`):** ao chavear sessões ou forkar transcrições, a
    contabilidade de tokens de saída descartava valores maiores computados por outros arquivos de transcrição compartilhados.
11. **Perfis customizados de Claude atrelados a diretórios do usuário (`#38149`):** desenvolvedores que mantêm múltiplas
    instalações/contas locais de Claude (ex.: `~/.claude-trabalho`, `~/.claude-pessoal`) não tinham como cadastrá-las no app
    como opções persistentes no menu de agentes da barra de abas sem sobrescrever o diretório padrão `~/.claude`.
12. **Parada sem feedback em usage limits de terminais (`#38026`):** agentes Claude e Codex rodando em terminais paravam
    abruptamente ao bater no teto de uso da conta sem exibir quando a cota seria resetada nem oferecer um meio interativo de
    retomada sem ter que digitar novamente no terminal ou reiniciar o processo.
13. **Subagentes disparados via CLI não herdam a conta do chamador (`#38052`):** quando um agente coordenador dispara um
    subagente ou revisor via CLI, o novo agente inicia na conta globalmente selecionada no app, arriscando debitar cotas
    pessoais em tarefas de trabalho.
14. **Perda de prompt cache em chats ociosos (`#37833`):** uma aba de Native Chat com Claude deixada ociosa perde a
    janela de cache de prompt (1 hora em contextos ≥ 200k tokens), multiplicando custos e tempo de resposta.
15. **Sessão parada em stop após troca de conta durante limite de cota (`#39169`):**
    Ao alternar para uma nova conta no Claude switcher com uma sessão pausada por limite de uso (5h usage limit), a interface
    não disparava a continuação automática (`continueUsageLimit`), exigindo que o usuário clicasse manualmente em botões de retomada
    ou perdesse o fluxo de trabalho.
16. **Interrupção de agentes autônomos por esgotamento de limites semanais e de modelos (`#39495`):**
    Desenvolvedores que mantêm múltiplas assinaturas Claude enfrentam paradas não assistidas de tarefas longas quando uma conta
    bate no limite de 5h ou limite semanal. Além disso, quando a cota semanal de modelos específicos (ex.: Fable) se esgota,
    o Claude Code interrompe o terminal com uma pergunta interativa ("Switch to fallback model and continue"), paralisando
    agentes autônomos por falta de detecção e rotação automática de contas entre hosts locais e remotos SSH.
17. **Requisições de rede em background indesejadas pelo medidor de cota OAuth (`#39502`):**
    O painel de monitoramento de uso realizava chamadas periódicas em background para endpoints da Anthropic (`api.anthropic.com`),
    gerando consumo indesejado de rede e alertas em ambientes corporativos com restrições estritas de telemetria.
18. **Omissão de métricas de uso da conta System default do Claude quando uma conta salva está selecionada (`#46002`):**
    A barra de status anexava medições de contas inativas apenas a contas que possuíam ID salvo; como a conta "System default" não possui ID salvo, suas leituras eram omitidas da lista inativa, deixando o desenvolvedor sem visibilidade do consumo da conta principal do sistema.
19. **Perda de telemetria de uso e exibição de "Not checked" ao alternar de conta System default para conta salva (`#46099`, refs `#45979`):**
    Ao alternar da conta System default para uma conta salva em um menu que permanece aberto, a leitura da conta padrão não era armazenada sob sua respectiva chave de cache, fazendo com que a linha exibisse *"Not checked"* em vez do uso recém-consultado.
20. **Leituras redundantes de logins do Claude e ausência de consumo de System default em clientes móveis (`#46119`):**
    A rotina de verificação de autenticação lia repetidamente os arquivos de login de cada perfil do Claude a cada ciclo, gerando I/O desnecessário; além disso, a visualização remota em dispositivos móveis não recebia os dados de uso da conta System default do host.
21. **Travamento permanente de continuações de chat após troca de conta quando o horário de reset é desconhecido (`#47079`):**
    Quando um chat pausava por usage limit sem que o provedor informasse o horário exato de reset da cota, a sessão nunca prosseguia automaticamente, mesmo após o operador alternar para uma conta limpa. Além disso, paradas manuais via Stop não revogavam a retomada pendente, provocando retomadas indevidas em chaveamentos posteriores.
22. **Quebra de Rewind e Fork por registro falso de prompt dropado em Stop no Claude (`#46984`, resolve `#46978`):**
    Quando o comando Stop era acionado antes do Claude gravar o prompt (por exemplo durante o gancho `UserPromptSubmit`), o resultado `error_during_execution` com `terminal_reason: aborted_streaming` referenciava o UUID sintético do frame de resultado em vez do prompt real, quebrando funções de Rewind e Fork por apontar para um UUID inexistente no transcript.

## O que o upstream propõe e implementa

- **Continuação de chat limitado após troca de conta mesmo com reset desconhecido (`#47079`):**
  - Trata o momento da troca de conta como substituto do horário de reset para contas não impactadas pelo limite, permitindo que a nova leitura decida a retomada; lê o horário de reset no texto de erro do Codex em execução local e revoga o agendamento de retomada caso Stop tenha sido acionado.
- **Liquidação correta como não executado (*unrun*) para prompts cancelados por Stop (`#46984`, resolve `#46978`):**
  - Seta o garçom do prompt cancelado no arranque como rejeitado e não executado (*unrun*), eliminando referências a UUIDs fantasmas do frame de erro e preservando a integridade das operações de Rewind e Fork.
- **Leitura única de logins do Claude e exibição de uso de System default no app móvel (`#46119`):**
  - Otimiza a rotina para ler cada login do Claude uma única vez por ciclo de sincronização e expõe as métricas de consumo da conta System default para clientes pareados e app móvel.
- **Exibição do uso de System default do Claude enquanto outra conta salva está ativa (`#46002`):**
  - Roteia a chave System default através de `claudeAccountUsagePreparation`, lendo o uso da conta padrão do host diretamente em seu diretório base e exibindo-o na linha correspondente mesmo com contas salvas selecionadas.
- **Retenção de métricas de System default após alternância de conta (`#46099`, refs `#45979`):**
  - Alimenta o cache de uso da conta System default de saída sob sua chave específica, mantendo as medições visíveis na linha em vez de reverter para "Not checked".
- **Motor de rotação automática de contas Claude e monitoramento por modelo (`#39495`):**
  - Proposta de diálogo unificado de contas Claude no status bar e menu de contexto de worktrees;
  - Rotação por host: chaveia automaticamente para a próxima conta cadastrada quando o limite de 5h ou semanal atinge um limiar crítico;
  - Barras de visualização de cota com janelas semanais discriminadas por modelo e watcher opt-in para responder automaticamente
    ao prompt de fallback de modelo no terminal sem cobrança adicional;
  - Sincronização opcional de contas e preferências de rotação entre dispositivos conectados.
- **Configuração para desativar polling OAuth do medidor de uso (`#39502`):**
  - Adiciona chave de configuração permitindo desligar completamente as requisições em background à API de limites de uso.
- **Continuação automática de chats ao trocar de conta no switcher (`#39169`):**
  - Conecta o evento `onSwitched` do seletor de contas do Claude diretamente ao dispatch de `continueUsageLimit`;
  - Ao selecionar uma nova conta válida, retoma instantaneamente a execução da tarefa pausada por cota sem requerer intervenção manual.
- **Fixação de conta por projeto (`#38581`):**
  - Adiciona o campo "Account" no painel de setup do agente no projeto, permitindo amarrar sessões Claude e Codex a uma
    conta salva específica (local, WSL ou servidor remoto pareado);
  - Garante que terminais, chats nativos, nomeação de sessões e geração de commits naquele projeto iniciem sempre na conta
    fixada, independentemente de qual conta estiver ativa globalmente no app.
- **Retentativa automática em contas alternativas para helpers pontuais (`#38654`):**
  - Helpers automáticos de texto (geração de mensagens de commit, nomes de branch/chat, resumos de PR) passam a tentar
    silenciosamente outras contas secundárias configuradas caso a conta principal esgote sua cota.
- **Exibição de tokens vitalícios do `/stats` do Claude Code (`#38509`):**
  - Lê `<config home>/stats-cache.json` e renderiza ao lado do título do painel a contagem vitalícia (ex.: `58.6B lifetime tokens`),
    discriminando por histórico de conta/host sem misturar filtros locais de transcript.
- **Detecção e destravamento de panes em limite com crons ativos (`#38547`):**
  - Destrava o reinício de panes do Claude com crons sob limite de cota quando solicitado um chaveamento de conta.
- **Seleção CLI de contas Claude (`#38227`):**
  - Estende `orca account select --agent claude --account <id|system>`;
  - Permite direcionar a seleção para instâncias remotas usando `--environment <selector>`.
- **Propagação consistente de conta entre todas as panes (`#38254`):**
  - Proposta para sinalizar e reiniciar uniformemente todas as panes atreladas ao runtime de Claude quando houver troca de
    conta, atualizando `CLAUDE_CONFIG_DIR` em tempo real.
- **Ações de retomada e troca de conta em avisos de limite (`#38298`):**
  - Suporte a "Automatic continue" e "Switch Account" nos avisos de usage limit mobile e notificações push.
- **Preservação de contagem cheia de tokens (`#38201`):** retém o maior valor medido entre transcrições concorrentes.
- **Lançamento de Claude em perfis locais definidos pelo usuário (`#38149`):**
  - Suporte a `claudeConfigProfiles` nas configurações e isolamento de `ORCA_CLAUDE_CONFIG_PROFILE_DIR`.
- **Recuperação de usage-limit direto na pane do terminal (`#38026`):**
  - Cartão integrado informando horário de reset e botão "Continue now".

## O que fazer

- Exibir o consumo da conta System default do Claude na status bar mesmo quando uma conta salva estiver selecionada (`#46002`).
- Reter as medições da conta System default no cache após a alternância para outra conta, evitando o estado "Not checked" (`#46099`, refs `#45979`).
- Otimizar a leitura de credenciais e logins do Claude para uma única consulta por ciclo e sincronizar o uso de System default com clientes móveis (`#46119`).
- Adotar a fixação de conta por projeto (`#38581`) no `brza-studio`, separando contas corporativas de pessoais.
- Habilitar o fallback de cota em helpers de texto (`#38654`) para fluxos de commit e PR no `brza-workflow`.
- Incorporar o disparo imediato de continuação de limites ao chavear contas Claude (`#39169`).
- Integrar a leitura de `stats-cache.json` (`#38509`) no `brza-studio`.
- Portar o comando `orca account select --agent claude` (`#38227`) para a CLI do `brza`.
- Avaliar a introdução de motor de rotação automática de contas Claude por host e janelas por modelo (`#39495`).
- Disponibilizar a opção para desativar chamadas periódicas em background da cota OAuth (`#39502`).
- Permitir retomada de chats sob limite de uso após chaveamento de conta mesmo sem horário de reset formal informado pelo provedor (`#47079`).
- Liquidar prompts cancelados por Stop durante a inicialização do Claude como `unrun` para resguardar Rewind e Fork (`#46984`, resolve `#46978`).

