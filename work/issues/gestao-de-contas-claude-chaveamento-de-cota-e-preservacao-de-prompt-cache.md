---
status: open
description: Gestão de contas Claude, switcher de rate limit (#48071/#48027), recuperação de sign-in (#48134) e restart de conta Codex (#48133).
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-03
tags:
  - chat
  - tooling
references:
  - https://github.com/stablyai/orca/pull/48218
  - https://github.com/stablyai/orca/pull/48253
  - https://github.com/stablyai/orca/pull/48238
  - https://github.com/stablyai/orca/pull/48239
  - https://github.com/stablyai/orca/issues/48249
  - https://github.com/stablyai/orca/pull/48323
  - https://github.com/stablyai/orca/pull/48208
  - https://github.com/stablyai/orca/pull/48071
  - https://github.com/stablyai/orca/issues/48027
  - https://github.com/stablyai/orca/pull/48134
  - https://github.com/stablyai/orca/pull/48133
  - https://github.com/stablyai/orca/pull/48082
  - https://github.com/stablyai/orca/pull/48187
  - https://github.com/stablyai/orca/pull/48160
  - https://github.com/stablyai/orca/pull/47341
  - https://github.com/stablyai/orca/pull/47983
  - https://github.com/stablyai/orca/pull/47948
  - https://github.com/stablyai/orca/pull/47928
  - https://github.com/stablyai/orca/pull/47910
  - https://github.com/stablyai/orca/pull/47866
  - https://github.com/stablyai/orca/pull/47933
  - https://github.com/stablyai/orca/issues/47954
  - https://github.com/stablyai/orca/issues/47020
  - https://github.com/stablyai/orca/issues/45090
  - https://github.com/stablyai/orca/issues/44117
  - https://github.com/stablyai/orca/commit/56b2f9e44a4
  - https://github.com/stablyai/orca/commit/ee135b48486
  - https://github.com/stablyai/orca/commit/d1916137334
  - https://github.com/stablyai/orca/commit/b2065bb81ed
---

# Gestão de contas Claude, chaveamento de cota e preservação de prompt cache

<!-- pln-014-despacho -->
> **Despacho (PLN-014/R1.1):** classe `ausente` · casa `studio`
> Merge no upstream não muda `status`. PLN-014/R1, 2026-11-12.

Rastreado dos PRs abertos no upstream [`stablyai/orca#47983`](https://github.com/stablyai/orca/pull/47983),
[`stablyai/orca#47948`](https://github.com/stablyai/orca/pull/47948),
[`stablyai/orca#47928`](https://github.com/stablyai/orca/pull/47928),
[`stablyai/orca#47910`](https://github.com/stablyai/orca/pull/47910),
[`stablyai/orca#47866`](https://github.com/stablyai/orca/pull/47866),
[`stablyai/orca#47933`](https://github.com/stablyai/orca/pull/47933) (reverte `#47778`),
[`stablyai/orca#47858`](https://github.com/stablyai/orca/pull/47858) (commit `56b2f9e44a4`),
[`stablyai/orca#47834`](https://github.com/stablyai/orca/pull/47834) (commit `ee135b48486`),
[`stablyai/orca#47804`](https://github.com/stablyai/orca/pull/47804) (commit `d1916137334`),
além das issues [`stablyai/orca#47954`](https://github.com/stablyai/orca/issues/47954),
[`stablyai/orca#47020`](https://github.com/stablyai/orca/issues/47020),
[`stablyai/orca#45090`](https://github.com/stablyai/orca/issues/45090),
[`stablyai/orca#44117`](https://github.com/stablyai/orca/issues/44117),
[`stablyai/orca#45294`](https://github.com/stablyai/orca/pull/45294),
[`stablyai/orca#47737`](https://github.com/stablyai/orca/pull/47737) (refs Issue [`#47718`](https://github.com/stablyai/orca/issues/47718)),
[`stablyai/orca#47778`](https://github.com/stablyai/orca/pull/47778) (refs Issue [`#42644`](https://github.com/stablyai/orca/issues/42644)),
[`stablyai/orca#47764`](https://github.com/stablyai/orca/pull/47764) (resolve Issue [`#47763`](https://github.com/stablyai/orca/issues/47763)),
[`stablyai/orca#47689`](https://github.com/stablyai/orca/pull/47689),
além da issue [`stablyai/orca#47829`](https://github.com/stablyai/orca/issues/47829),
[`stablyai/orca#47155`](https://github.com/stablyai/orca/pull/47155),
[`stablyai/orca#47540`](https://github.com/stablyai/orca/pull/47540),
[`stablyai/orca#47209`](https://github.com/stablyai/orca/pull/47209) (refs Issue [`#47146`](https://github.com/stablyai/orca/issues/47146)),
[`stablyai/orca#47079`](https://github.com/stablyai/orca/pull/47079),
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
23. **Re-escaneamento, re-análise e re-indexação redundante de transcripts em múltiplos perfis Claude (`#47209`, refs `#47146`):**
    Quando múltiplos perfis do Claude compartilham a pasta global de projetos através de links simbólicos (ou quando as raízes de perfis apontam para destinos equivalentes), o indexador de transcripts varria e processava repetidamente os mesmos diretórios de projetos para cada perfil, consumindo CPU e I/O desnecessários.
24. **Falta de fluxo direto de re-autenticação para contas Codex revogadas ou expiradas na visualização de uso (`#47155`):**
    Quando uma conta Codex perdia autorização ou expirava, o painel de uso exibia erro de cota bloqueado sem opção direta de sign-in para renovar as credenciais, forçando o desenvolvedor a navegar pelas configurações para se autenticar novamente.
25. **Falsos positivos de ausência de assinatura em respostas de rate limit do OpenCode Go (`#47540`):**
    Qualquer erro retornado na consulta de limites de cota do OpenCode Go era classificado como "no subscription" pelo app, mesmo quando se tratava apenas de pico momentâneo de requisições ou indisponibilidade temporária do serviço.
26. **Sobrescrita de chats e perda de histórico de prompts na migração do Codex (`#45294`):**
    A migração de versões antigas do Codex sobrescrevia conversas ou descartava o histórico `history.jsonl` de contas removidas, arriscando perda permanente de prompts do usuário.
27. **Sobrescrita de respostas de assistente por reutilização de `message_id` em turnos futuros (`#47737`, refs `#47718`):**
    Quando um provedor LLM compatível com a API de mensagens do Codex reutilizava um `message_id` em turnos subsequentes da mesma thread, a resposta mais recente herdava a identidade do turno anterior e sobrescrevia a mensagem antiga no transcript.
28. **Poluição de métricas de uso na barra de status durante foco ativo no chat (`#47778`, refs `#42644`):**
    A barra de status mantinha widgets de uso de cota visíveis mesmo enquanto a superfície principal em foco era uma conversa de chat, competindo por atenção visual e espaço.
29. **Truncamento de argumentos JSON e falha de listagem de modelos Claude no Windows via Bun (`#47764`, resolve `#47763`):**
    Em shims `.cmd` baseados no runtime Bun no Windows, o escape `""` para argumentos JSON em linha de comando era quebrado pelo `CommandLineToArgvW`. Flags como `--settings {"disableAllHooks":true}` engoliam argumentos subsequentes e causavam falha silenciosa na descoberta de modelos do Claude.

30. **Re-leitura redundante de todos os transcripts a cada mudança de worktree (`#47858`, commit `56b2f9e44a4`):**
    O serviço de cálculo de uso re-processava todos os arquivos de transcrição do histórico do zero sempre que o worktree em foco alternava, consumindo I/O desnecessário de disco.
31. **Falta de botão direto de reautenticação no cartão de conta Claude que requer novo login (`#47834`, commit `ee135b48486`):**
    Quando um token de conta Claude expirava ou necessitava de renovação de credenciais, o cartão de status exibia aviso de erro mas carecia de um botão "Sign in" contextual, forçando navegação por menus externos.
32. **Rótulos obsoletos de planos Claude Max na interface (`#47804`, commit `d1916137334`):**
    A interface de gerenciamento de cotas exibia os planos renomeados da Anthropic como `Max 5x` e `Max 20x`, em vez das denominações atuais `Max` e `Ultra`.
33. **Bloqueio da thread principal ao ler histórico inicial de conversas do Claude (`#47983`):**
    A leitura do primeiro histórico de sessões do Claude na abertura do chat era executada na thread de UI/renderização, gerando engasgos momentâneos na interface gráfica.
34. **Concorrência entre edições manuais de itens e esperas por limite de cota de bots (`#47948`):**
    Quando um bot aguardava a liberação de cota de uso, modificações concorrentes no item podiam corromper ou anular o timer de espera, desestabilizando o fluxo de execução.
35. **Ausência de modelos de contingência para failover sob exaustão de cota de bots (`#47910`):**
    Ao esgotar a cota de uso de um modelo primário configurado para um bot, não havia definição de modelos de backup para failover automático, interrompendo tarefas não supervisionadas.
36. **Falta de orquestração unificada de pools de contas e distribuição de cotas entre agentes (`#47954`, refs `#47020`, `#45090`, `#44117`):**
    Falta de suporte para cadastrar pools de contas de provedores (Anthropic, OpenAI, etc.), definir limites configuráveis por conta e balancear a distribuição de agentes, bots e workers entre contas corporativas e individuais.
37. **Falsos limites de uso por throttling temporário no Codex (`#48218`):**
    Respostas transitórias de limitação de taxa (throttling/HTTP 429 sem header de retry) emitidas pela API do Codex eram interpretadas pelo frontend como exaustão definitiva de cota (`usage limit`), desativando o agente incorretamente em vez de aplicar backoff exponencial.
38. **Seleção de contas vinculadas em Orca Account (`#48253`):**
    Ao conectar contas organizacionais vinculadas (linked accounts) no painel de Orca Account, a interface não permitia chavear explicitamente qual identidade de faturamento secundária associar ao workspace ativo.
39. **Seletor de contas Google dedicado para agentes e subagentes (`#48238`, `#48239`):**
    Ambientes com múltiplos perfis Google Workspace / Cloud careciam de um seletor visual na barra de contexto para definir qual conta de serviço ou OAuth Google deve autorizar as ferramentas executadas por agentes e subagentes de pesquisa e automação.
40. **Prevalência indevida de `ANTHROPIC_AUTH_TOKEN` sobre contas gerenciadas do Claude (`#48249`):**
    A presença estática da variável de ambiente `ANTHROPIC_AUTH_TOKEN` no terminal ou profile do sistema impedia o chaveamento de contas gerenciadas no app, sobrescrevendo a credencial selecionada no switcher e debitando silenciosamente na conta da chave estática.
41. **Falhas na autenticação Google causadas por suspensão de dispositivos móveis (`#48323`):**
    O handshake de login OAuth com o Google em clientes web/móveis falhava com erro de timeout ou interrupção de socket quando o aparelho entrava em sleep durante a autorização externa no navegador.
42. **Ausência de detalhamento da causa raiz em falhas de login do Google Connector (`#48208`):**
    Erros de permissão, recusa de consentimento ou bloqueio de domínio corporativo no Google Connector eram apresentados com mensagem genérica de erro de conexão, dificultando o diagnóstico pelo operador.

## O que o upstream propõe e implementa

- **Diferenciação de throttling transitório e rate limit definitivo no Codex (`#48218`):**
  - Trata respostas HTTP 429 sem janela formal de reset como throttling momentâneo com backoff exponencial automático, prevenindo a marcação falsa da conta como esgotada.
- **Suporte a linked accounts na Orca Account (`#48253`):**
  - Permite visualizar, selecionar e desvincular contas secundárias associadas à conta principal do usuário no painel de contas.
- **Seletor de perfis Google para agentes (`#48238`, `#48239`):**
  - Adiciona seletor de contas Google ativas para vincular agentes e subagentes à identidade correta de ferramentas em nuvem.
- **Precedência de contas gerenciadas frente a `ANTHROPIC_AUTH_TOKEN` (`#48249`):**
  - Garante que a seleção de perfis Claude no app tenha prioridade determinística sobre variáveis estáticas de ambiente no runtime do processo.
- **Resiliência do fluxo de sign-in Google contra suspensão do sistema (`#48323`):**
  - Mantém o estado do callback OAuth em espera tolerante a congelamentos e reconexões de rede após wake-up de dispositivos.
- **Exibição do motivo específico de falha no Google Connector (`#48208`):**
  - Extrai e renderiza mensagens explicativas de erro (escopo negado, domínio restrito, cancelamento) no card de setup.
- **Cessação de releituras de transcripts na mudança de worktree (`#47858`, commit `56b2f9e44a4`):**
  - Mantém o cache de transcripts estável entre trocas de worktrees, atualizando apenas deltas reais.
- **Botão direto de Sign-in no cartão de conta Claude pendente (`#47834`, commit `ee135b48486`):**
  - Adiciona o botão de login direto no próprio card da conta com sessão expirada.
- **Atualização das nomenclaturas de planos Claude para Max e Ultra (`#47804`, commit `d1916137334`):**
  - Reflete os nomes oficiais Max e Ultra para os planos de alta capacidade.
- **Leitura do histórico inicial do Claude em background worker (`#47983`):**
  - Transfere a leitura de histórico na primeira inicialização para um worker thread assíncrono fora da thread de renderização.
- **Proteção de esperas de cota contra edições concorrentes de itens (`#47948`):**
  - Sincroniza o ciclo de vida do timer de limite de cota com mutações concorrentes nos itens de bots.
- **Suporte a modelos de backup para failover de uso em bots (`#47910`):**
  - Permite configurar modelos secundários para assumir a execução do bot automaticamente quando a cota do modelo principal é atingida.
- **Orquestração de pools de contas multi-provedor (`#47954`):**
  - Especificação para agrupamento de contas em pools com roteamento por repositório, tipo de agente e cotas configuráveis.
- **Reversão da ocultação de uso na barra de status com chat em foco (`#47933`, commit `b2065bb81ed`):**
  - Reverte a alteração `#47778` para restabelecer a visibilidade das métricas de consumo de tokens enquanto uma conversa detém o foco.

- **Preservação durável de históricos de prompt `history.jsonl` na migração do Codex (`#45294`, commit `231551f9f65`):**
  - Garante que a migração de upgrade copie o histórico de cada conta (`history.jsonl`) para a home do runtime em modo de criação exclusiva antes de gravar marcadores ou realizar cópias de sessão, e preserva o arquivo na remoção de contas;
  - Nunca sobrescreve prompts existentes e realiza mesclagens assíncronas do histórico compartilhado com tolerância a hard links ausentes.
- **Geração de novas identidades para respostas com `message_id` reutilizado em turnos distintos (`#47737`, commit `6e4ebc83d00`):**
  - Mapeia identidades de itens do Codex considerando tanto o ID de mensagem quanto o identificador do turno; ao encontrar um `message_id` já existente pertencente a outro turno, emite uma nova identidade distinta sem sobrescrever a resposta histórica.
- **Ocultação de métricas de uso na barra de status com chat em foco (`#47778`, commit `85d8985d9e0`):**
  - Oculta o indicador de uso da barra de status enquanto um chat ou terminal em visualização de chat detiver o foco ativo na interface gráfica.
- **Escape libuv (`\"`) para argumentos JSON em shims Bun `.cmd` no Windows (`#47764`, commit `da839538408`):**
  - Utiliza escape estilo libuv (`\"`) quando argumentos possuem número par de aspas e apenas caracteres ASCII imprimíveis seguros, garantindo que o Bun decodifique parâmetros JSON de hooks e modelos Claude sem truncamentos.
- **Exibição de permissões do Claude pré-aprovadas por hooks como `allowed` em vez de `cancelled` (`#47689`):**
  - Ajusta a sinalização de autorização para refletir permissões previamente concedidas por hooks automáticos sem confundi-las com cancelamentos pelo usuário.
- **Fluxo guiado de Sign-in para contas Codex expiradas ou revogadas na tela de uso (`#47155`):**
  - Oferece botão imediato de login/sign-in nas linhas de uso com credenciais revogadas, vinculando o estado de erro estritamente à conta e ao runtime específico (incluindo WSL distros) e limpando confirmações de reset obsoletas.
- **Restrição de reporte de falta de assinatura estritamente para `EntitlementError` no OpenCode Go (`#47540`):**
  - Trata como "no-subscription" apenas respostas explícitas de `EntitlementError`, evitando que limitações transitórias de taxa ou erros de conexão bloqueiem o acesso com avisos falsos de assinatura ausente.
- **Varredura única de pastas de projetos entre perfis Claude via `realpath` (`#47209`, refs `#47146`):**
  - Resolve os caminhos canônicos das raízes de perfis através de `realpath` e desduplica diretórios de projetos antes da indexação, garantindo que transcripts em pastas compartilhadas sejam processados apenas uma vez.
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
- Resolver caminhos reais via `realpath` e deduplicar pastas de projetos compartilhadas entre perfis Claude na indexação de transcripts (`#47209`, refs `#47146`).
- Oferecer ação de sign-in direto para contas Codex revogadas ou expiradas nas visões de uso (`#47155`).
- Mapear status de ausência de assinatura no OpenCode Go estritamente diante de `EntitlementError` (`#47540`).
- Preservar histórico `history.jsonl` de contas em migrações do Codex sem sobrescrever chats ou prompts (`#45294`, commit `231551f9f65`).
- Emitir novas identidades para respostas quando o provedor LLM reutilizar `message_id` em turnos futuros da mesma thread (`#47737`, refs `#47718`).
- Ocultar métricas de uso da barra de status enquanto um chat detiver o foco ativo (`#47778`, refs `#42644`).
- Utilizar citação estilo libuv (`\"`) para parâmetros JSON em shims `.cmd` baseados em Bun no Windows (`#47764`, resolve `#47763`).
- Tratar permissões do Claude pré-aprovadas por hooks como `allowed` em vez de `cancelled` (`#47689`).
- Cessar releituras completas de transcripts durante a alternância de worktree (`#47858`).
- Incluir botão direto de "Sign in" no cartão de conta Claude quando nova autenticação for necessária (`#47834`).
- Atualizar a exibição dos planos da Anthropic para Max e Ultra na tela de quotas (`#47804`).
- Delegar a leitura de histórico inicial do Claude para um worker assíncrono em background (`#47983`).
- Proteger timers de espera por cota contra mutações concorrentes nos itens de bots (`#47948`).
- Implementar configuração de modelos de backup para failover automático sob exaustão de cota de bots (`#47910`).
- Avaliar a arquitetura de multi-account orchestration com pools de contas e limites distribuídos (`#47954`, `#47020`, `#45090`, `#44117`).
- Restabelecer a visibilidade dos contadores de uso na barra de status mesmo com chat em foco (`#47933`).
- Permitir re-tentativa imediata de contas Claude inativas marcadas como Limited via abertura explícita do switcher (`#48071`, resolve Issue `#48027`).
- Adicionar fluxo de recuperação de login/autenticação diretamente dentro da interface de chat (`#48134`).
- Reiniciar o Codex sob nova conta credenciada parando e retomando a mesma conversa sem perder contexto (`#48133`).
- Impedir que prompts posicionais do Claude sejam consumidos como argumentos de flags variádicas (`#48082`, commit `907b43c0465`).
- Adicionar ação de Stop para interromper processos de setup do Google Connector em andamento (`#48187`).
- Concluir setup do Google cuja etapa de autorização foi realizada externamente fora do card (`#48160`, commit `50d506df9e3`).
- Preservar a lista completa de modelos do Antigravity quando o comando `agy models` retornar lista truncada (`#47341`, commit `43133540259`).
- Tratar respostas 429 de throttling no Codex com backoff sem desativar a conta por suposto esgotamento de cota (`#48218`).
- Adotar o gerenciamento de linked accounts no painel de contas do `brza-studio` (`#48253`).
- Implementar o seletor de credenciais Google para agentes com acesso a conectores e ferramentas em nuvem (`#48238`, `#48239`).
- Assegurar precedência estrita das contas Claude configuradas no app sobre variáveis de ambiente como `ANTHROPIC_AUTH_TOKEN` (`#48249`).
- Proteger fluxos de autenticação OAuth contra interrupções de sleep e troca de redes em clientes remotos (`#48323`).
- Apresentar detalhes explicativos de falha na autorização do Google Connector (`#48208`).




