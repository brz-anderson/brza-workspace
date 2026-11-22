---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-22
completed: 2026-11-22
tags:
  - tooling
refs:
  - issue:alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas
  - issue:badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes
  - issue:conectores-de-linhagem-na-sidebar-cores-de-grupos-e-isolamento-de-extensoes
  - issue:cursor-no-chat-via-acp-previa-de-links-de-imagem-bifurcacao-resiliente-e-leitura-por-voz
  - issue:fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks
  - issue:gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache
  - issue:leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle
  - issue:redesenho-de-cartoes-de-resposta-progresso-por-etapas-e-fila-de-mensagens
  - issue:retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-22)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e commits criados ou atualizados entre `2026-11-21T21:00:00Z` e `2026-11-22T03:15:00Z` (range upstream `3b8cbe221f2..f5b017a8f16`), comparando com os registros em `work/issues/` e o índice `.brza/index.jsonl`.
2. **Atualização de 4 issues rastreadas em `work/issues/`:**
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados os PRs `#46287`, gravando o responsável por assumir cada pergunta de agente (`taker`) e vinculando tarefas `--for <messageId>` no `worker-start`; `#46446`, ordenando `worker-read` newest-first dentro do teto de 512 KiB para não descartar mensagens recentes em logs longos; `#46448`, notificando o coordenador e liquidando o worker quando o agente em terminal encerra com shell PTY mantido aberto; `#46273`, comitando atomicamente respostas e avisos de perguntas junto com seu correio em savepoint único do SQLite; `#46517`, eliminando o teto de 6 repasses e continuando hand-offs em salas de grupos através de `@mentions` sem mensagens duplicadas; `#46602` (STA-16956), forçando permissões estritas `0600` em arquivos de instruções e contexto de bots; e `#46478`, cessando a re-leitura contínua de workers concluídos na atualização da árvore de chats de bots.
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionados os PRs `#46138`, protegendo checkouts restaurados no cleanup e validando o marcador `.git` pré e pós-prova com checagem de identidade do diretório raiz via `lstatBigInt` e parse linear de padding em `gitdir`; `#46581`, adotando índice de turnos para buscas rápidas de texto e prosa por turno no journal de conversas; e `#46201`, compactando o layout do diálogo de confirmação de exclusão de workspaces.
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados os PRs `#45876`, implementando exclusão atômica de chat via RPC `agentSession.delete.v1` com fechamento de abas e gravação de tombstone permanente no SQLite; `#45881`, tornando as linhas de chat mais limpas com chevron dinâmico no hover e status na prévia; `#46592`, limpando a faixa de mensagens enfileiradas com ações visíveis apenas sob hover, foco ou toque; `#46570`, equipando a caixa de comentários de itens com os mesmos seletores de menções `@` e comandos slash `/` do composer; `#46583`, exibindo nomes amigáveis de agentes do catálogo no seletor de Nova Aba; e `#46608`, renderizando esqueleto (*skeleton loader*) durante o carregamento de detalhes de itens de bots.
   - [Badges de worktree para plugins, cadência de PR e redesenho de automações](../issues/badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes.md):
     adicionados os PRs `#46624` (refs `#46564`) e `#46584` (resolve `#46564`), identificando duravelmente a fonte de disparo de automações em `triggeredBy` e rotulando a origem real (Webhook, GitHub, Slack) em vez de `Scheduled`; `#46593`, provendo mensagens de erro descritivas e ajuda clara na validação de agendamentos cron de automações; e `#46522`, promovendo a ação 'Import Cookies' para o topo do menu do navegador integrado.

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-22)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e commits criados ou atualizados entre `2026-11-22T03:00:00Z` e `2026-11-22T09:15:00Z` (range upstream `f5b017a8f16..5bbb4ed9d56`), comparando com os registros em `work/issues/` e o índice `.brza/index.jsonl`.
2. **Atualização de 4 issues rastreadas em `work/issues/`:**
   - [Leitura antecipada e preservação de skills no arranque e nos plugins](../issues/leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins.md):
     adicionados os PRs `#46756` (refs `#46706`), retendo skills conhecidas em cache e marcando a raiz como `unavailable` em caso de erro transitório de I/O (`EACCES`, `EIO`, `EPERM`) sem purgar o catálogo; `#46724`, unificando a instalação de skills do Gemini CLI exclusivamente em `~/.agents/skills` e aposentando cópias redundantes em `~/.gemini/skills`; `#46747` (resolve `#46708`), tratando qualquer formato de `--dry-run` (incluindo `--dry-run=true`) como modo simulação nos comandos de skills; `#46751` (resolve `#46713`), rejeitando seletores inválidos (`--ref` em catálogo/pasta ou `--catalog` em pasta) com `invalid_argument` no `plugin install`; `#46749` (resolve `#46698`), saindo com código 1 e listando comandos individuais de repetição quando algum plugin falha em `plugin update --all`; e `#46718` (resolve `#46701`), associando registros de comandos a seus wrappers únicos para que o descarte de uma inscrição anterior não apague um comando recém-substituído.
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados os PRs `#46793`, finalizando inicializações de workers que atingem prontidão tardiamente com as mesmas garantias de binding de inicializações no prazo; `#46562`, notificando workers e liberando chamadas `ask --wait` imediatamente quando o coordenador para sem responder ou quando o chat do Run é substituído (`/new`, troca de agente) ou excluído; `#46541`, emitindo aviso de abandono de pergunta de agente no momento em que o tomador (`taker`) para sem responder nem deixar worker `--for` ativo; e `#46571`, notificando agentes imediatamente em falhas de entrega de perguntas para computadores pareados ou runs órfãos.
   - [Conectores de linhagem na sidebar, cores de grupos de projeto e isolamento de extensões em perfis](../issues/conectores-de-linhagem-na-sidebar-cores-de-grupos-e-isolamento-de-extensoes.md):
     incorporado o PR `#42312`, que implementa guias de árvore (`tree guides`) para workspaces aninhados e worktrees filhas, otimizando o cálculo de trilhos ancestrais via lista encadeada compartilhada para custo linear proporcional aos trilhos visíveis e ajustando a medição de largura via hook dedicado.
   - [Redesenho de cartões de resposta, progresso por etapas e fila de mensagens](../issues/redesenho-de-cartoes-de-resposta-progresso-por-etapas-e-fila-de-mensagens.md):
     incorporado o PR `#42515`, trazendo o redesign completo do *Answer Card* com ladrilhos preenchidos, barra de etapas segmentada clicável, destaques em pill para opções recomendadas, navegação estruturada e fila de mensagens integrada ao composer com menus de ação rápida.

### 3. Ciclo de 6h (12:00 BRT / 15:00 UTC em 2026-11-22)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e commits criados ou atualizados entre `2026-11-22T09:00:00Z` e `2026-11-22T15:15:00Z` (range upstream `5bbb4ed9d56..f2f0cce6e42`), comparando com os registros em `work/issues/` e o índice `.brza/index.jsonl`.
2. **Atualização de 4 issues rastreadas em `work/issues/`:**
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados os PRs `#46941`, mapeando IDs de modelo Antigravity qualificados com nível para suas famílias canônicas para reter controle de esforço; `#46851`, permitindo escolher o esforço de raciocínio no Kiro antes do envio da primeira mensagem; `#46963` (resolve `#46957`), suportando cards de formulário estruturado para elicitação `AskUser` do Factory Droid; e `#46866` (resolve `#46727`, `#46729`), tratando respostas finais de child runs e retries resilientes de provedor no OpenCode via ACP.
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados os PRs `#46901`, integrando store de anexos da sessão para renderizar imagens de ferramentas ACP sem arquivo em disco; `#46930`, implementando leitura em blocos (`readTextChunk` com ranges) para streaming de imagens > 3MB em clientes pareados; `#46974` (resolve `#46953`), suportando colagem com botão do meio do mouse em editores ProseMirror no Linux/desktop; e `#46739`, exibindo a primeira linha de conteúdo e chevron permanentemente visível em linhas de agentes.
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionado o PR `#46955` (resolve `#46944`), sinalizando avisos de retenção (delivery hold) em recibos de mensagens despachadas com `send --on` para servidores pareados.
   - [Badges de worktree para plugins, cadência de PR e redesenho de automações](../issues/badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes.md):
     adicionados os PRs `#46945` (resolve `#46919`), roteando a abertura de automações de bots para o host real (WSL ou nós SSH); `#46933` (resolve `#46932`), evitando que dark-wake holds congelem a janela de carência de execuções atrasadas; `#46908` (refs `#46027`), reportando `runtime_access_denied` em vez de falso "not running" sob falha de permissão de socket no daemon; e `#46846`, executando validações de hooks de workspace em threads assíncronas para eliminar congelamentos da UI.

### 4. Ciclo de 6h (18:00 BRT / 21:00 UTC em 2026-11-22)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e commits criados ou atualizados entre `2026-11-22T15:00:00Z` e `2026-11-22T21:01:00Z` (range upstream `f2f0cce6e42..2178e7cd95a`), comparando com os registros em `work/issues/` e o índice `.brza/index.jsonl`.
2. **Atualização de 6 issues rastreadas em `work/issues/`:**
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados os PRs `#46999` (resolve `#46992`), marcando turnos do Antigravity no terminal interrompidos por cota ou erro formalmente como falhas com mensagem real do assistente; `#46889`, integrando CodeBuddy Code via ACP (`codebuddy --acp`) com instruções `CODEBUDDY.local.md`; `#46878`, integrando Devin nativo com isolamento `in-process`, modos Ask/Code/Smart/Bypass e instruções `AGENTS.local.md`; e `#46896`, suportando Cline via ACP com marcação estrita de falhas em ferramentas em lote.
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados os PRs `#47016` (resolve `#47021`), delimitando diffs via ACP apenas às linhas alteradas em arquivos grandes > 256 KiB; `#47080` (refs `#47055`), retendo correspondências por título no histórico e `/resume` quando a busca FTS não encontrar acertos no corpo; `#47076`, exibindo integralmente comentários de perguntas abertas de agentes em itens sem truncamento em 8 linhas; `#47084`, preservando largura e legibilidade de chips de itens em linhas "Started"; e `#46740`, exibindo estado de repouso ("all-clear") com avatar cinza de bot na aba Items.
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados os PRs `#46842`, `#46826`, `#46797` e `#46757`, viabilizando mensageria federada bidirecional com cartões de aprovação `NativeChatClientAskRequestCard` e envio via `--on-client`; `#47072`, roteando correio de worker liquidado diretamente para a thread conectora de origem; `#46643`, suportando retomada atômica de workers de terminal pós-reinício sob *Resume work on restart*; e `#47048`, resolvendo o handle em workers ainda em inicialização para evitar falso erro de não encontrado.
   - [Cursor no Chat via ACP, prévia de links de imagem, bifurcação resiliente e leitura por voz](../issues/cursor-no-chat-via-acp-previa-de-links-de-imagem-bifurcacao-resiliente-e-leitura-por-voz.md):
     adicionados os PRs `#47071`, descobrindo e indexando sessões ACP nativas de `cursor-agent acp` no Agent Session History; e `#47093`, otimizando a inspeção de atividade de conversas do Cursor via `stat` direto em `store.db`.
   - [Fontes web em plugins, isolamento de atalhos e resiliência de hooks](../issues/fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks.md):
     adicionados os PRs `#47102` (resolve `#47074`), centralizando verticalmente rótulos em formulários declarativos de plugins com a variante `control` de `Label`; e `#47067` (resolve `#47066`), resolvendo com `realpath` a raiz de staging na instalação de plugins locais para prevenir erros EPERM e links mutáveis.
   - [Leitura antecipada e preservação de skills no arranque e nos plugins](../issues/leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins.md):
     adicionado o PR `#47019` (resolve `#47018`), adicionando `<repo>/.prime/agent/skills` ao escopo de varredura e descoberta de skills locais do Prime Agent.
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     adicionados os PRs `#47079`, habilitando continuação automática de chats após chaveamento de conta mesmo quando o horário de reset é desconhecido; e `#46984` (resolve `#46978`), liquidando prompts cancelados por Stop durante a inicialização do Claude como `unrun` para resguardar Rewind e Fork.
