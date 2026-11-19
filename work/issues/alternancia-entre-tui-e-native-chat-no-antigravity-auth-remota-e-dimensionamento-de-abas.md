---
status: open
description: O PR #44430 (resolve #42512) usa armazenamento de token em arquivo quando o keyring Linux headless está inacessível; PRs #43939, #43571, #43564 trazem autenticação via Gemini API key/ADC e chat TRAE CLI.
scope:
  - brza-studio
  - workspace
  - brza-workflow
priority: high
opened: 2026-11-09
tags:
  - auth
  - chat
  - tooling
---

# Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas

Rastreado dos PRs abertos no upstream [`stablyai/orca#44430`](https://github.com/stablyai/orca/pull/44430) (resolve Issue [`#42512`](https://github.com/stablyai/orca/issues/42512)),
[`stablyai/orca#43939`](https://github.com/stablyai/orca/pull/43939),
[`stablyai/orca#43571`](https://github.com/stablyai/orca/pull/43571),
[`stablyai/orca#43564`](https://github.com/stablyai/orca/pull/43564),
[`stablyai/orca#43363`](https://github.com/stablyai/orca/pull/43363),
[`stablyai/orca#43217`](https://github.com/stablyai/orca/pull/43217),
[`stablyai/orca#43049`](https://github.com/stablyai/orca/pull/43049),
[`stablyai/orca#43101`](https://github.com/stablyai/orca/pull/43101),
[`stablyai/orca#42933`](https://github.com/stablyai/orca/pull/42933),
[`stablyai/orca#42940`](https://github.com/stablyai/orca/pull/42940),
[`stablyai/orca#42847`](https://github.com/stablyai/orca/pull/42847) (resolve Issue [`#40321`](https://github.com/stablyai/orca/issues/40321)),
além das issues [`stablyai/orca#43183`](https://github.com/stablyai/orca/issues/43183),
[`stablyai/orca#43154`](https://github.com/stablyai/orca/issues/43154),
[`stablyai/orca#43155`](https://github.com/stablyai/orca/issues/43155),
[`stablyai/orca#42759`](https://github.com/stablyai/orca/issues/42759),
[`stablyai/orca#42460`](https://github.com/stablyai/orca/pull/42460) (resolve Issue [`#41961`](https://github.com/stablyai/orca/issues/41961)),
[`stablyai/orca#42464`](https://github.com/stablyai/orca/pull/42464),
[`stablyai/orca#42357`](https://github.com/stablyai/orca/pull/42357) (resolve Issue [`#42356`](https://github.com/stablyai/orca/issues/42356)),
[`stablyai/orca#42323`](https://github.com/stablyai/orca/pull/42323) (resolve Issue [`#42116`](https://github.com/stablyai/orca/issues/42116)),
[`stablyai/orca#42282`](https://github.com/stablyai/orca/pull/42282) (resolve Issue [`#42280`](https://github.com/stablyai/orca/issues/42280)),
[`stablyai/orca#40986`](https://github.com/stablyai/orca/pull/40986) (resolve Issue [`#40984`](https://github.com/stablyai/orca/issues/40984)),
[`stablyai/orca#40980`](https://github.com/stablyai/orca/pull/40980) (resolve Issue [`#40979`](https://github.com/stablyai/orca/issues/40979)),
[`stablyai/orca#40867`](https://github.com/stablyai/orca/pull/40867) (resolve Issue [`#40865`](https://github.com/stablyai/orca/issues/40865)),
[`stablyai/orca#40912`](https://github.com/stablyai/orca/pull/40912),
[`stablyai/orca#40901`](https://github.com/stablyai/orca/pull/40901),
[`stablyai/orca#40201`](https://github.com/stablyai/orca/pull/40201) (resolve Issue [`#40192`](https://github.com/stablyai/orca/issues/40192)),
[`stablyai/orca#40228`](https://github.com/stablyai/orca/pull/40228),
[`stablyai/orca#40229`](https://github.com/stablyai/orca/pull/40229) (resolve Issue [`#40227`](https://github.com/stablyai/orca/issues/40227)),
[`stablyai/orca#40208`](https://github.com/stablyai/orca/pull/40208),
[`stablyai/orca#40175`](https://github.com/stablyai/orca/pull/40175),
[`stablyai/orca#40171`](https://github.com/stablyai/orca/pull/40171) e
[`stablyai/orca#40183`](https://github.com/stablyai/orca/pull/40183) (resolve Issue [`#15317`](https://github.com/stablyai/orca/issues/15317)).

## O problema

1. **Incapacidade de alternar abas do Antigravity entre terminal TUI e Native Chat (`#40201`, resolve `#40192`):**
   Sessões de terminal com Claude e Codex já possuíam a capacidade de alternar bidirecionalmente entre o terminal e a visão
   estruturada de chat sem reiniciar o processo do agente. No entanto, abas rodando o Antigravity (`agy`) ficavam restritas
   ao modo terminal: a ação "Continue in Chat UI" e o atalho `⌘⇧J` / `Ctrl+Shift+J` não tinham efeito, e no cliente mobile
   não havia o botão "Switch to chat view".
2. **Falha de login de Claude e Codex em servidores remotos e SSH (`#40228`):**
   Ao iniciar Claude ou Codex em hosts pareados, SSH ou VMs onde o agente ainda não estava autenticado, o terminal
   falhava imediatamente com erro de login ou exigia copiar tokens manualmente pelo shell, travando o prompt do usuário.
3. **Falta de flexibilidade na largura das abas no cabeçalho (`#40229`, resolve `#40227`):**
   O aplicativo impunha uma regra rígida de largura de abas (máximo de 300px e mínimo de 144px). Desenvolvedores com
   muitas abas abertas não conseguiam condensá-las na tela, enquanto outros com títulos longos sofriam truncamento prematuro.
4. **Dificuldade de instalar e autenticar agentes ausentes a partir do chat (`#40208`):**
   Quando um agente configurado não estava presente no host da sessão, o usuário precisava abrir manualmente um terminal,
   descobrir o comando de instalação e rodar a autenticação de forma isolada antes de poder usar o chat.
5. **Divergência entre modelos visíveis no composer e nas configurações (`#40175`):**
   A tela de `Settings > Agents` e o seletor de lançamento podiam exibir apenas modelos estáticos empacotados na release,
   enquanto o composer de chat acessava os modelos reais da conta conectada no host. Isso impedia selecionar modelos recém-lançados
   como padrão ou ao iniciar tarefas pelo Source Control.
6. **Consumo excessivo de memória em sessões longas com helpers e subagentes (`#40171`):**
   Conversas extensas com múltiplos helpers e comandos acumulavam payloads completos de respostas finalizadas e varriam
   desnecessariamente todo o histórico de subagentes a cada atualização de estado.
7. **Painéis remotos presos em "Working" por perda de notificação de parada (`#40183`, resolve `#15317`):**
   Quando eventos assíncronos de `SubagentStop` eram perdidos na rede entre o host remoto e o app, o painel do agente
   permanecia indefinidamente marcado como executando, mesmo com o Claude já ocioso.
8. **Omissão de skills do Antigravity no menu slash (`/`) do Native Chat (`#40986`, resolve `#40984`):**
   Ao digitar `/` em chats do Antigravity, a interface listava apenas comandos embutidos de ACP (`/model`, `/effort`, `/clear`,
   `/plan`, etc.). As skills instaladas em `~/.gemini/config/skills` e `~/.agents/skills` ficavam omitidas porque a falta de um
   perfil de picker dedicado fazia o relatório de comandos embutidos do ACP suprimir a varredura das pastas de skills.
9. **Descarte de regras de usuário e workspace (`GEMINI.md` / `AGENTS.md`) pelo Antigravity ACP (`#40867`, resolve `#40865`):**
   O servidor ACP do Antigravity omitia `rules_config` durante a criação de sessão ACP, ignorando instruções personalizadas
   globais (`~/.gemini/GEMINI.md` ou `AGENTS.md`) e locais do workspace (`<cwd>/AGENTS.md` ou `GEMINI.md`).
10. **Descoberta estática de modelos do Antigravity no novo chat (`#40980`, resolve `#40979`):**
    O seletor de modelos ao criar novos chats do Antigravity não consultava dinamicamente a CLI host `agy`, impedindo o uso imediato
    de modelos recém-lançados disponíveis na máquina.
11. **Bloqueio de envio e seleção no primeiro chat de um novo worktree (`#40912`):**
    O primeiro chat aberto em um novo worktree travava o composer e a escolha de modelos enquanto o runtime do agente inicializava,
    forçando o desenvolvedor a aguardar o término do bootstrap para redigir o primeiro prompt.
12. **Bloqueio indevido de ferramentas em modo sempre permitido pelo hook `PreToolUse` (`#42323`, resolve `#42116`):**
    O hook de permissão de ferramentas pré-execução (`PreToolUse`) emitia por padrão a resposta `ask` em vez de `decision: allow`, interceptando indevidamente ferramentas já configuradas com flag `always-proceed` ou auto-aprovadas.
13. **Ausência de opções de esforço de raciocínio para modelos agrupados no ACP (`#42282`, resolve `#42280`):**
    O client ACP não derivava corretamente a lista de opções de raciocínio (*reasoning effort*) a partir do nó `availableModels`, fazendo com que modelos com capacidades graduadas de raciocínio ficassem travados na configuração padrão.
14. **Abas de terminal do Antigravity mantendo o comando bruto da CLI em vez do título de resumo da conversa (`#42357`, resolve `#42356`):**
    Quando uma sessão do Antigravity era iniciada no terminal, a aba exibia apenas o comando bruto invocado (`antigravity run` ou `agy`), ignorando o título de resumo contextual presente em `conversation_metadata.json` e dificultando a identificação da tarefa em workspaces com múltiplas abas.
15. **Incompatibilidade com novos modelos Gemini 4 e esforços estendidos no Antigravity (`#42460`, resolve `#41961`):**
    O mapeamento de modelos do Antigravity restringia a seleção aos modelos pré-definidos antigos (Gemini 3 Pro/Flash), omitindo variantes como Gemini 4 Hydrogen, Carbon e Argon, além de não suportar níveis de raciocínio profundo (`xhigh` e `max`), resultando em erros ou quedas para configurações padrão.
16. **Inoperância do runtime e chat nativo do Antigravity no Windows (`#42464`):**
    O runtime gerenciado e as rotas de IPC do Antigravity no desktop assumiam caminhos e sinais POSIX, impedindo a inicialização do daemon ACP e a alternância para chat nativo no Windows.
17. **Falso fallback para prompt de download de 337 MB no Antigravity Chat por cooldown do chaveiro e keyring inacessível no Linux headless (`#44430`, resolve `#42512`):**
    Quando `agy` registrava um timeout temporário de 5s no chaveiro do sistema durante o boot ou quando o daemon de Secret Service/keyring estava indisponível em Linux headless, deixava o arquivo `antigravity-keyring-unavailable` no cache. O app interpretava isso como ausência definitiva de credencial em vez de inspecionar o arquivo de token salvo pelo próprio `agy` (`agy`'s file-based token storage) ou validar que `agy acp` estava ativo e autenticado, forçando o prompt de download desnecessário do runtime gerenciado de 337 MB.
18. **Crash e perda irrecuperável de sessão ao alternar de terminal para chat (`#42589`):**
    Sessões de agentes longas abertas no terminal sofriam crash ao acionar "Continue in Chat UI", corrompendo o registro de sessão e impossibilitando a retomada em ambos os modos.
19. **Impossibilidade de escolher dinamicamente a conta em novos lançamentos (`#42506`):**
    Usuários com múltiplas contas e perfis de Claude ou Codex ficavam restritos à conta ativa global do host, sem poder selecionar a conta alvo diretamente no lançamento de novos chats ou terminais.
20. **Ocultação de modelos não-Gemini no Antigravity Chat por filtro estrito de `clientInfo` (`#42759`):**
    O servidor `agy_acp_server.par` do Antigravity filtra os modelos disponíveis com base no campo `clientInfo` transmitido durante o handshake ACP. Quando acionado pelo Native Chat embutido do Studio, apenas modelos Gemini são expostos no seletor, ocultando modelos como Claude Opus 4.5, Sonnet 5.5 e GPT-OSS 120B autorizados na conta corporativa, que funcionam normalmente na CLI `agy acp`.
21. **Ausência de suporte ao Antigravity Native Chat no Windows por falta de pacote gerenciado (`#42847`, resolve `#40321`):**
    No Windows, o Antigravity caía forçosamente para o terminal porque não havia pacote pré-empacotado gerenciado do servidor ACP para a plataforma, mesmo quando o usuário já possuía a CLI `agy.exe acp` instalada e compatível no host.
22. **Exclusão de token incorreto em falha de login do Gemini Enterprise e vazamento de `ELECTRON_RUN_AS_NODE` (`#42896`):**
    Se uma nova conexão ACP falhava ao autenticar com Gemini Enterprise, a rotina de limpeza apagava `acp_token.json` (login pessoal) deixando para trás o `acp_business_token.json` inutilizado; além disso, a variável de ambiente `ELECTRON_RUN_AS_NODE=1` vazava no macOS e Linux para comandos executados pelo servidor gerenciado, quebrando execuções de comandos Electron.
23. **Falta de suporte aos modos nativos Orchestrator e execução auto/plan no Antigravity (`#42933`):**
    O Antigravity era tratado apenas como agente executor pontual no chat, sem capacidade de operar no modo Orchestrator (coordenando tarefas de múltiplos subagentes) ou alternar entre os modos de execução nativos de plano (`plan`) e autônomo (`auto`), limitando pipelines complexos que utilizam o harness de ferramentas do Gemini.
24. **Identificadores de novos agentes heterogêneos e propensos a colisões (`#42940`):**
    Agentes recém-instanciados utilizavam formatos variados de ID derivados de timestamps ou prefixos locais, dificultando rastreabilidade consistente entre sessões de orquestração e logs.
25. **Falta de suporte a flags de agente remoto e execução headless SSH/WSL no Antigravity (`#43049`):**
    O Antigravity só podia ser invocado em sessões locais com terminal gráfico interativo, falhando em deploys remotos via SSH headless ou em distribuições WSL sem display gráfico.
26. **Subnotificação de métricas de uso e estimativas de API do Antigravity no AI Vault (`#43101`):**
    O AI Vault não media nem estimava os custos de tokens das conversas do Antigravity, registrando zero ou valores nulos nos relatórios de uso.
27. **Erro "tModel: model is empty" ao resumir conversas do Antigravity (`#43154`, `#43155`):**
    Ao executar follow-up ou retomar uma sessão prévia (`agy --conversation <id>`), o comando omitia a flag de modelo original ou configurada em Default Args, resultando no erro fatal `tModel: model is empty` e falhas repetidas 502.
28. **Perda de flags de modelo e esforço no resume e congelamento de 40–55s em erros de saída (`#43217`, `#43183`):**
    Ao retomar uma sessão do Antigravity por meio da receita de launch, os parâmetros resolvidos de modelo e nível de esforço de raciocínio eram descartados, voltando para os defaults (`#43217`). Além disso, durante erros de saída do modelo em chamadas ACP, a interface permanecia travada em "Sending..." ou "Working" por até 55 segundos durante tentativas silenciosas de retry e reinicialização de ~7.5s, sem feedback ao usuário (`#43183`).
29. **Lacunas no seletor de esforço xhigh/max e mensagens de commit no Antigravity (`#43571`):**
    Mesmo com a descoberta prévia de modelos Antigravity, o gerador de mensagens de commit exibia linhas brutas por nível (`claude-opus-4-6-xhigh`, `claude-opus-4-6-max`) sem opções estruturadas de nível de pensamento, os fallbacks de raciocínio não contemplavam `xhigh`/`max` e a invalidação de catálogo de modelos permanecia incompleta.
30. **Falta de integração ao Chat UI para conversas da TRAE CLI (`#43564`):**
    A CLI do agente Trae ficava limitada ao terminal TUI, sem suporte para prosseguir conversas no Native Chat com controles nativos de tarefas e aprovações.
31. **Dependência exclusiva de login via conta Google no navegador para Antigravity Chat (`#43939`):**
    O Antigravity no Native Chat só permitia autenticação via OAuth pessoal ou corporativo do Google no navegador. Desenvolvedores que utilizam chave de API própria do Gemini ou credenciais padrão de aplicação do Google Cloud (ADC / Google Agent Platform) em ambientes headless ou de infraestrutura eram incapazes de autenticar o chat nativo.

## O que o upstream implementa e corrige

- **Listagem de modelos no agent picker a partir da conta ativa do chat (`#43363`):**
  - No menu de seleção de modelos do Antigravity, consulta os modelos disponíveis com base na conta configurada para a nova sessão de chat em vez de consultar cegamente a conta global do host, evitando exibir modelos não autorizados ou omitir modelos corporativos.
- **Preservação de modelo e esforço na receita de retomada do Antigravity (`#43217`):**
  - Mantém o modelo resolvido e as flags de reasoning effort na receita de lançamento de retomada de sessão (`resume launch recipe`), assegurando coerência no raciocínio ao dar prosseguimento a chats existentes.
- **Detecção de stalls em erros de saída e timeouts transparentes no ACP (`#43183`):**
  - Trata falhas de saída de modelo de forma explícita com mensagem imediata de erro em vez de engasgar a UI em retries opacos de 50s.
- **Flags remotas e execução headless em SSH/WSL para Antigravity (`#43049`):**
  - Permite invocar Antigravity em servidores remotos sem interface gráfica, repassando flags e argumentos headless de forma transparente.
- **Relatório e medição de uso do Antigravity no AI Vault (`#43101`):**
  - Mede tokens consumidos por sessões do Antigravity e estima custos nos relatórios do AI Vault.
- **Preservação de flag de modelo em follow-up e retomada de conversas (`#43154`):**
  - Assegura que `agy --conversation <id>` receba o modelo original ou configurado em Default Args, eliminando o erro `tModel: model is empty`.
- **Suporte ao modo Orchestrator e modos auto/plan no Antigravity (`#42933`):**
  - Implementa capacidade nativa para o Antigravity assumir o papel de coordenador/orquestrador, despachando subagentes e avaliando tarefas estruturadas;
  - Introduz os seletores de modo de execução nativos `plan` (modo somente plano sem execução direta de mutações) e `auto` (execução contínua autônoma com aprovações por checkpoint);
  - Integra as capacidades aos envelopes ACP e controles de interface do chat.
- **Identificadores universais UUID para novos agentes (`#42940`):**
  - Padroniza a geração de identificadores de agentes como UUIDs puros v4, simplificando o roteamento e eliminando colisões de sessões.
- **Alternância fluida entre TUI e Native Chat para Antigravity (`#40201`):**
  - Adiciona `antigravity` à lista `NATIVE_CHAT_SUPPORTED_AGENT_LIST`, compartilhada entre desktop e cliente móvel;
  - Cria o decodificador `transcript-line-decoders-antigravity.ts` para ler diretamente `transcript_full.jsonl` de `~/.gemini/antigravity-cli/brain/<id>/.system_generated/logs/`, garantindo preservação de argumentos completos de ferramentas;
  - Trata envelopes `<USER_REQUEST>`, divide `PLANNER_RESPONSE` em blocos de raciocínio (*reasoning*) e assistente, e normaliza diffs de edições de arquivo;
  - Converte chamadas MCP (`call_mcp_tool` e `mcp_<server>_<tool>`) para a representação unificada de ferramentas do chat;
  - Suporta o componente de perguntas interativas para `ask_question` (incluindo `is_multi_select`) e prompts de aprovação prévia para `ask_permission`;
  - Obtém o catálogo de modelos disponíveis via `agy models` e mapeia comandos de barra (`/`).
- **Autenticação em um clique no navegador para hosts remotos (`#40228`):**
  - Introduz o card inline `AgentSignInCard` sobreposto ao painel do agente quando o host relata status desconectado;
  - Ao clicar em "Sign in with browser", o daemon do host inicia `claude auth login --claudeai` ou `codex login` e abre um túnel efêmero seguro (`network.authCallbackTunnel`) para a porta de callback local;
  - O navegador da máquina local completa a autorização e transmite a resposta de volta ao host remoto sem transitar tokens ou credenciais pelo cliente Orca;
  - Introduz as capabilities `accounts.agent-sign-in-status.v1` e `accounts.host-sign-in-callback.v1`.
- **Configurações de dimensionamento de abas estilo VS Code (`#40229`):**
  - Adiciona `Settings → General → Navigation`:
    - `Tab Sizing` (`tabSizing`): `auto` (padrão atual), `fit` (título completo com rolagem), `shrink` (encolhe até o mínimo antes de rolar) e `fixed` (largura idêntica para todas as abas);
    - `Tab Min Width` (`tabSizingMinWidth`, padrão 144px) e `Tab Max Width` (`tabSizingMaxWidth`, padrão 300px), configuráveis entre 60px e 800px e aplicados via variáveis CSS `--tab-min-width` e `--tab-max-width`.
- **Instalação guiada de agentes a partir do chat (`#40208`):**
  - Oferece opção de abrir uma sessão de setup diretamente no menu de novas abas quando o agente selecionado não estiver instalado no host;
  - Executa as rotinas de instalação e login em terminal acoplado e revalida automaticamente a disponibilidade do agente ao concluir.
- **Catálogo de modelos em tempo real por host e conta (`#40175`):**
  - Unifica a regra de aquisição de modelos entre o composer de chat, `Settings > Agents` e diálogos de lançamento;
  - Lê a listagem do host ativo mantendo o nível de esforço de raciocínio (*reasoning effort*) configurado e retém opções salvas mesmo se temporariamente não listadas.
- **Liberação de payloads concluídos e eliminação de varreduras de histórico (`#40171`):**
  - Libera previews de respostas consumidas, mantém helpers ativos em índices dedicados e substitui o payload integral de ACP por digests de 64 caracteres, eliminando a lentidão em turnos avançados.
- **Reconciliação de tarefas pendentes via transcript (`#40183`):**
  - Ao detectar o prompt ocioso, inspeciona atômica e assincronamente os limites do transcript da tarefa do Claude para confirmar a conclusão, eliminando o travamento do estado "Working".
- **Descoberta de skills do Antigravity no menu slash (`/`) do Native Chat (`#40986`, resolve `#40984`):**
  - Concede ao Antigravity um perfil de menu de barra (`slash profile`) que preserva a varredura das pastas de skills (`~/.gemini/config/skills` e `~/.agents/skills`) enquanto a sessão relata comandos embutidos de ACP;
  - Exibe no picker tanto comandos embutidos (`/model`, `/clear`, etc.) quanto skills instaladas com autocomplete.
- **Injeção de regras de usuário e workspace no Antigravity ACP (`#40867`, resolve `#40865`):**
  - Localiza arquivos de instrução globais (`~/.gemini/GEMINI.md` ou `AGENTS.md`) e do workspace (`<cwd>/AGENTS.md` ou `GEMINI.md`) com desduplicação por caminho real (`realpath`);
  - Injeta as regras formatadas sob `<user_rules>` no parâmetro `_meta.antigravity.systemPrompt.append` durante a inicialização (`session/new`, `session/load`, `session/resume`), garantindo obediência às normas de projeto sem alterar binários.
- **Descoberta dinâmica de modelos da CLI Antigravity (`#40980`, resolve `#40979`):**
  - Consulta dinamicamente a CLI host `agy` para alimentar o picker de criação de novo chat com todos os modelos disponíveis.
- **Composer e seletor desbloqueados no primeiro chat de novos worktrees (`#40912`):**
  - Permite digitar, enviar mensagens e selecionar modelos imediatamente no primeiro chat de um worktree, enfileirando o prompt até o término da inicialização do runtime.
- **Hook `PreToolUse` emitindo `decision: allow` para ferramentas auto-aprovadas (`#42323`, resolve `#42116`):**
  - Corrige a resposta do hook de autorização prévia de ferramentas para retornar `decision: allow` em vez de `ask` quando a ferramenta estiver configurada com política permissiva ou `always-proceed`, impedindo diálogos de aprovação bloqueantes desnecessários.
- **Derivação de opções de esforço de raciocínio a partir de `availableModels` no ACP (`#42282`, resolve `#42280`):**
  - Extrai dinamicamente as opções suportadas de reasoning effort para modelos agrupados a partir dos metadados de `availableModels` do servidor ACP, habilitando a graduação de raciocínio na UI do chat.
- **Sincronização de títulos de resumo do Antigravity para abas de terminal (`#42357`, resolve `#42356`):**
  - Lê o título contextual gerado pelo assistente em `conversation_metadata.json` (ou metadados da sessão) e sincroniza diretamente com o rótulo da aba do terminal, substituindo nomes genéricos e estáticos como `antigravity run` pelo assunto real da conversa.
- **Suporte a modelos Gemini 4 completos, esforços `xhigh`/`max` e catalogação dinâmica (`#42460`, resolve `#41961`):**
  - Expande o catálogo nativo do Antigravity para incluir variantes Gemini 4 (Hydrogen, Carbon e Argon);
  - Adiciona suporte aos níveis de raciocínio estendido `xhigh` e `max`;
  - Aprimora o parse de `agy models` com retenção de preferências de esforço por modelo e fallback resiliente via backend do host em fases de pré-descoberta.
- **Suporte a chat UI e runtime gerenciado do Antigravity no Windows (`#42464`):**
  - Adapta caminhos de sockets nomeados, tratamento de processos filhos e normalização de caminhos de arquivos para Windows.
- **Seletor dinâmico de conta para Claude e Codex no lançamento (`#42506`):**
  - Permite escolher qual perfil ou conta autenticada (`claude-accounts` ou `codex-accounts`) utilizar ao instanciar cada novo chat ou terminal;
  - Introduz o seletor visual em `dynamic-account-launch-setting.tsx` e suporte na CLI via `--account`.
- **Leitura do armazenamento de token em arquivo do `agy` quando o keyring Linux headless está inacessível (`#44430`, resolve `#42512`):**
  - Quando o keyring do Linux headless está inacessível ou atinge timeout, o runtime lê diretamente o arquivo de token mantido pelo `agy`, contornando a falha de Secret Service sem exibir o prompt de download de 337 MB do runtime gerenciado.
- **Validação resiliente de credenciais do Antigravity contra falsos timeouts de keyring (`#42512`):**
  - Verifica ativamente a disponibilidade de sessões autenticadas via `antigravityHostAcpReady()` em vez de abortar cegamente pela simples existência do marcador `antigravity-keyring-unavailable`.
- **Alinhamento de `clientInfo` para exibição de modelos multi-provedor no Antigravity ACP (`#42759`):**
  - Identifica que o servidor `agy_acp_server.par` restringe o retorno de modelos a apenas Gemini quando `clientInfo.name` identifica a UI do Studio;
  - Sugere configurar `clientInfo` de modo análogo ao cliente CLI autônomo para liberar modelos adicionais configurados na conta (Claude Opus/Sonnet 5.5, GPT-OSS).
- **Habilitação do Antigravity Native Chat no Windows via host ACP (`#42847`, resolve `#40321`):**
  - Permite que o Studio utilize diretamente o backend do host (`agy.exe acp`) no Windows mesmo sem pacote gerenciado pré-empacotado, liberando o chat estruturado nativo na plataforma.
- **Correção de remoção de tokens de autenticação e contenção de `ELECTRON_RUN_AS_NODE` (`#42896`):**
  - Passa o tipo de conta exato (pessoal vs business) para a rotina de verificação, garantindo que falhas em contas Gemini Enterprise apaguem apenas `acp_business_token.json`;
  - Restringe `ELECTRON_RUN_AS_NODE=1` estritamente ao ambiente Windows onde o helper precisa, eliminando vazamento para subprocessos no macOS e Linux.
- **Normalização de fallbacks de raciocínio xhigh/max e mensagens de commit no Antigravity (`#43571`):**
  - Trata `xhigh` e `max` como níveis estruturados de reasoning effort no seletor de modelos e mensagens de commit em vez de expor sufixos brutos;
  - Conclui a invalidação limpa do catálogo de modelos quando parâmetros de esforço são alterados.
- **Suporte ao TRAE CLI no Native Chat UI (`#43564`):**
  - Permite instanciar conversas com o agente Trae diretamente no Chat UI estruturado, preservando streaming de respostas e histórico de tarefas.
- **Autenticação de chats Antigravity com API key do Gemini ou Google Agent Platform (ADC) (`#43939`):**
  - Introduz os métodos de autenticação `gemini-api-key` e `gcp-service-account` / ADC em `Settings → AI Accounts → Antigravity`;
  - Permite colar a Gemini API key diretamente nas preferências com armazenamento seguro criptografado local em `<userData>/antigravity-chat/`;
  - Suporta credenciais do Google Cloud Application Default Credentials (ADC) com resolução dinâmica de projeto GCP via `gcloud` ou variável de ambiente;
  - Executa o chat nativo no servidor Antigravity bundled sem exigir o fluxo de callback no navegador do OAuth.

## O que fazer no BrzA Studio

1. Habilitar flags remotas e execução headless do Antigravity em SSH e WSL (`#43049`).
2. Exibir métricas reais e estimativas de uso do Antigravity no AI Vault (`#43101`).
3. Preservar o parâmetro de modelo ao resumir conversas antigas do Antigravity (`#43154`).
4. Habilitar o modo Orchestrator e os modos de execução nativos auto/plan para o Antigravity (`#42933`).
5. Adotar IDs no formato UUID puro para agentes recém-instanciados (`#42940`).
6. Habilitar a alternância entre TUI e Native Chat para o Antigravity (`#40201`), permitindo alternar via `⌘⇧J` entre a interface de linha de comando e o chat estruturado sem perder o processo ativo.
4. Incorporar a seleção dinâmica de conta no lançamento de Claude e Codex (`#42506`).
5. Eliminar o falso fallback para o runtime gerenciado no Antigravity Chat lendo o arquivo de tokens do `agy` e validando `antigravityHostAcpReady` quando o keyring Linux headless estiver inacessível (`#44430`, resolve `#42512`).
6. Blindar o chaveamento TUI ↔ Chat contra crashes irrecuperáveis de sessão (`#42589`).
7. Incorporar o catálogo expandido de modelos Gemini 4 e esforços `xhigh`/`max` para Antigravity (`#42460`, resolve `#41961`).
8. Suportar o runtime gerenciado e chat nativo do Antigravity no Windows (`#42464`, `#42847`, resolve `#40321`).
9. Sincronizar títulos de resumo da conversa do Antigravity com as abas de terminal (`#42357`, resolve `#42356`).
10. Emitir `decision: allow` no hook `PreToolUse` para ferramentas auto-aprovadas (`#42323`, resolve `#42116`).
11. Derivar opções de esforço de raciocínio dinamicamente a partir de `availableModels` no cliente ACP (`#42282`, resolve `#42280`).
12. Adotar a descoberta de skills do Antigravity no menu slash (`/`) do Native Chat (`#40986`).
13. Implementar a injeção de regras `AGENTS.md` e `GEMINI.md` via `_meta.antigravity.systemPrompt.append` nas sessões ACP (`#40867`).
14. Habilitar a descoberta dinâmica de modelos da CLI `agy` (`#40980`) e o composer desbloqueado no primeiro chat de novos worktrees (`#40912`).
15. Adotar o `AgentSignInCard` com túnel de callback de autenticação (`#40228`) para inicialização de Claude e Codex em servidores remotos e SSH sem atrito.
16. Incorporar os controles de dimensionamento de abas (`tabSizing`, `tabSizingMinWidth`, `tabSizingMaxWidth`) em `Settings → General → Navigation` (`#40229`).
17. Incluir o fluxo guiado de instalação de agentes a partir do chat (`#40208`).
18. Sincronizar os seletores de modelo de configurações e criação de workspace com o catálogo dinâmico da conta do host (`#40175`).
19. Incorporar as otimizações de memória para sessões com muitos subagentes (`#40171`) e a reconciliação de tarefas pendentes via transcript (`#40183`).
20. Ajustar a declaração de `clientInfo` na conexão ACP com o Antigravity para expor modelos multi-provedor (Claude, GPT-OSS) autorizados (`#42759`).
21. Permitir o Antigravity Native Chat no Windows usando a CLI host `agy acp` (`#42847`, resolve `#40321`).
22. Assegurar remoção correta de tokens Enterprise e isolamento de `ELECTRON_RUN_AS_NODE` (`#42896`).
23. Reter modelo e flags de esforço de raciocínio na receita de retomada do Antigravity (`#43217`).
24. Mitigar congelamentos de 55s no ACP exibindo erros de saída imediatamente (`#43183`).
25. Consultar modelos disponíveis para o Antigravity baseando-se na conta configurada para a nova sessão (`#43363`).
26. Incorporar fallbacks de raciocínio `xhigh`/`max` e formatação limpa de opções de pensamento em mensagens de commit do Antigravity (`#43571`).
27. Suportar TRAE CLI como agente com superfície no Native Chat UI (`#43564`).
28. Habilitar a autenticação de chats Antigravity via chave de API Gemini ou Google Agent Platform (ADC) em Settings (`#43939`).
