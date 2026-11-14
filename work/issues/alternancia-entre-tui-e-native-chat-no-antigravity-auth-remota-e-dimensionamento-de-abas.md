---
status: open
description: Os PRs #40986, #40980, #40867, #40201 trazem skills no picker do Antigravity, injeção de regras GEMINI/AGENTS, modelos dinâmicos e toggle TUI/Chat.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#42357`](https://github.com/stablyai/orca/pull/42357) (resolve Issue [`#42356`](https://github.com/stablyai/orca/issues/42356)),
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

## O que o upstream implementa e corrige

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

## O que fazer no BrzA Studio

1. Habilitar a alternância entre TUI e Native Chat para o Antigravity (`#40201`), permitindo alternar via `⌘⇧J` entre a interface de linha de comando e o chat estruturado sem perder o processo ativo.
2. Sincronizar títulos de resumo da conversa do Antigravity com as abas de terminal (`#42357`, resolve `#42356`).
3. Emitir `decision: allow` no hook `PreToolUse` para ferramentas auto-aprovadas (`#42323`, resolve `#42116`).
4. Derivar opções de esforço de raciocínio dinamicamente a partir de `availableModels` no cliente ACP (`#42282`, resolve `#42280`).
5. Adotar a descoberta de skills do Antigravity no menu slash (`/`) do Native Chat (`#40986`).
5. Implementar a injeção de regras `AGENTS.md` e `GEMINI.md` via `_meta.antigravity.systemPrompt.append` nas sessões ACP (`#40867`).
6. Habilitar a descoberta dinâmica de modelos da CLI `agy` (`#40980`) e o composer desbloqueado no primeiro chat de novos worktrees (`#40912`).
7. Adotar o `AgentSignInCard` com túnel de callback de autenticação (`#40228`) para inicialização de Claude e Codex em servidores remotos e SSH sem atrito.
8. Incorporar os controles de dimensionamento de abas (`tabSizing`, `tabSizingMinWidth`, `tabSizingMaxWidth`) em `Settings → General → Navigation` (`#40229`).
9. Incluir o fluxo guiado de instalação de agentes a partir do chat (`#40208`).
10. Sincronizar os seletores de modelo de configurações e criação de workspace com o catálogo dinâmico da conta do host (`#40175`).
11. Incorporar as otimizações de memória para sessões com muitos subagentes (`#40171`) e a reconciliação de tarefas pendentes via transcript (`#40183`).
