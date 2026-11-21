---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-21
completed: 2026-11-21
tags:
  - tooling
refs:
  - issue:abertura-de-agentes-no-chat-ui-pela-cli-e-superficie-chat-na-orquestracao
  - issue:alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas
  - issue:chaveamento-automatico-de-contas-claude-por-limite-de-uso-e-planos-observados
  - issue:comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais
  - issue:cursor-no-chat-via-acp-previa-de-links-de-imagem-bifurcacao-resiliente-e-leitura-por-voz
  - issue:gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache
  - issue:leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:progresso-de-revisao-no-diff-backend-de-metricas-e-abertura-de-pastas
  - issue:protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle
  - issue:retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-21)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e commits criados ou atualizados entre `2026-11-20T21:00:00Z` e `2026-11-21T03:15:00Z` (range upstream `912e284e05f..6862ac9b9cb`), comparando com os registros em `work/issues/` e o índice `.brza/index.jsonl`.
2. **Atualização de 5 issues rastreadas em `work/issues/`:**
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     adicionados os PRs `#46002`, que desacopla a migração de configurações de conta do Claude da reconciliação de credenciais ativas, eliminando mutações espúrias e race conditions de escrita em `settings.json`; e `#46099`, que normaliza a resolução de tokens OAuth do Claude para ler perfis configurados no escopo do usuário antes de recorrer ao keyring corporativo padrão.
   - [Leitura antecipada e preservação de skills no arranque e nos plugins](../issues/leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins.md):
     adicionados os PRs `#45822`, que protege o catálogo de skills contra falhas de parse de frontmatter corrompido ou YAML malformado emitindo aviso consultivo e mantendo as demais skills carregadas; e `#45966`, que indexa skills locais antecipadamente no worker de background antes da inicialização de instâncias TUI, eliminando travamentos de 3s no spawn de novos chats.
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados os PRs `#46101`, que fixa a versão estável 1.5.2 do pacote do servidor ACP do Google (`@google/antigravity-acp`) para assegurar robustez nas transmissões de turnos e orquestração de subagentes; e `#39769`, que introduz o suporte completo ao agente Kiro como backend nativo de chat estruturado no Native Chat UI via ACP V3.
   - [Comandos shell no chat, recibos de perguntas e foco espacial em terminais](../issues/comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais.md):
     adicionados os PRs `#45068`, provendo fallback suave de permissões do Claude de Full access para Approve for me ou Ask quando diretivas locais bloqueiam o bypass; `#45713`, que otimiza a inspeção de processos de terminal no macOS substituindo chamadas periódicas pesadas de `ps` por consultas estruturadas de `kinfo_proc` compartilhadas; `#44954`, isolando as re-renderizações e leituras de abas de terminal ao respectivo bucket no renderer; `#45978`, que redige argumentos e sanitiza saídas de erro completas em falhas de comandos customizados de agentes; e `#45907`, que retém notificações e correio de workers enquanto houver rascunho de texto não enviado no editor do terminal Pi.
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionados os PRs `#45986`, corrigindo mensagem de ajuda na criação de worktrees para recomendar a flag oficial `--base-branch`; `#45988`, que trata submódulos no comando "Stage All" do Git na presença de links compartilhados; `#45506`, que protege checkouts substitutos contra remoção indevida em limpezas residuais e no WSL; `#45912`, impedindo que a exclusão de um workspace acorde workspaces irmãos adormecidos (*slept siblings*); `#45749`, adotando busca indexada direta de worktrees para eliminar re-indexações globais frequentes; `#45031`, despachando a execução de comandos Git capturados para worker de processos no macOS e Linux; e `#46043`, preservando o status de sessões de agentes abertas em painéis além do TTL de 7 dias.

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-21)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e commits criados ou atualizados entre `2026-11-21T03:00:00Z` e `2026-11-21T09:15:00Z` (range upstream `6862ac9b9cb..16437ccfb17`), comparando com os registros em `work/issues/` e o índice `.brza/index.jsonl`.
2. **Atualização de 5 issues rastreadas em `work/issues/`:**
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     adicionado o PR `#46119`, que otimiza a leitura de logins do Claude para uma única consulta por ciclo de sincronização e propaga as métricas de uso da conta System default para clientes remotos e app móvel.
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados os PRs `#46125` e `#46175`, integrando a seleção de login Google no Antigravity com validação prévia de credenciais antes do chat; `#46109`, `#46040`, `#45985`, `#46018`, `#45962` e `#46039`, trazendo suporte no Native Chat e bots para Qwen Code, Factory Droid, Gemini CLI, Kilo Code, MiMo Code, Auggie e Goose sobre ACP; `#46130`, que renderiza card de arquivos modificados para ferramentas do Pi; `#46221`, enfileirando requisições no Home após falhas de turno em vez de abrir novo chat; e `#46228`, removendo o sufixo redundante "Folder" do chip de workspace no composer.
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados os PRs `#46235`, roteando envios para computadores pareados quando o agente solicitado reside remotamente; `#46196`, permitindo grupos de bots híbridos com membros locais e remotos; `#46086`, garantindo que retornos de workers locais alcancem a thread exata que iniciou a tarefa; `#46155`, notificando o coordenador caso o brief do worker falhe na submissão; `#46117`, exibindo respostas entre pares de agentes gerenciados na sala do grupo; `#46139`, eliminando lookups quadráticos $O(N^2)$ na ordenação e runtime de bots; e `#46207`, impedindo a exclusão de bots enquanto seu workspace contiver rascunhos de editor não salvos.
   - [Comandos shell no chat, recibos de perguntas e foco espacial em terminais](../issues/comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais.md):
     adicionados os PRs `#46105`, implementando suporte a fragmentos `#L<linha>` e intervalos de linhas em links de arquivo OSC 8 no terminal; `#45759`, desacoplando alterações de título de terminais de re-varreduras da barra lateral e Activity; `#46156`, restringindo o sublinhado visual de aba ativa exclusivamente ao split focado; `#44476`, padronizando o alinhamento de opções do menu de contexto de abas com ícones dedicados; `#46206`, limitando o recenseamento de terminais em falhas de status ao host local; e `#46168`, `#46157` e `#46145`, melhorando a ergonomia da caixa de comentários em perguntas de itens e destacando opções recomendadas e retomadas.
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionados os PRs `#45969`, fixando a linha de status no modal Delete para eliminar saltos visuais; `#46211` e `#46202`, adotando junctions no Windows para viabilizar testes de IPC e git safety; `#46028`, isolando regras do Cursor em arquivo exclusivo sem apagar customizações do usuário; `#46185`, desacoplando o arranque do profiler da main thread estagnada no watchdog; `#46024`, lendo status de agentes diretamente da memória sem re-parsing JSON repetido; `#45690`, preservando todos os turnos de chats antigos clonados do Codex; e `#46003`, isolando diretórios de bots para não serem adotados automaticamente como workspaces pais.

### 3. Ciclo de 6h (12:00 BRT / 15:00 UTC em 2026-11-21)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e commits criados ou atualizados entre `2026-11-21T09:00:00Z` e `2026-11-21T15:15:00Z` (range upstream `16437ccfb17..1e8546eadfc`), comparando com os registros em `work/issues/` e o índice `.brza/index.jsonl`.
2. **Atualização de 5 issues rastreadas em `work/issues/`:**
   - [Chaveamento automático de contas Claude por limite de uso, planos observados e resgate de cota](../issues/chaveamento-automatico-de-contas-claude-por-limite-de-uso-e-planos-observados.md):
     adicionados os PRs `#46296`, emitindo notificação estruturada ao coordenador quando um worker Claude no terminal atinge o limite de uso de cota; `#46277`, aguardando que o composer do Claude com flags especiais esteja pronto antes de submeter o prompt inicial; e `#46144`, mantendo visível o card de dados e consumo da conta System default quando uma conta salva está ativa.
   - [Cursor no Chat via ACP, prévia de links de imagem, bifurcação resiliente e leitura por voz](../issues/cursor-no-chat-via-acp-previa-de-links-de-imagem-bifurcacao-resiliente-e-leitura-por-voz.md):
     adicionados os PRs `#46142`, introduzindo suporte a "Approve for me" (`--auto-review`) em terminais do Cursor enquanto mantém isolamento dos modos de chat; e `#46284` (resolve `#46163`), mapeando identificadores de modelos salvos da CLI do Cursor para os modelos, esforço e flags de thinking compatíveis com o servidor nativo de chat.
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados os PRs `#46360`, implementando Tidy-up atômico e verificável em memórias de bots com movimentação de status para diário `memory/journal/YYYY-MM.md` em vez de reescrita destrutiva de `MEMORY.md`; `#46286`, solicitando repaint de interface para agentes ociosos reconectados com correio retido; `#46120`, consolidando a resolução de identidades de workers de side-chats em duas consultas indexadas no SQLite em lote; `#46140`, indexando links de sessão e mitigando contenção do banco em buscas de notificações do Slack; e `#46372`, unificando flags de envio estruturado na CLI em payload JSON único.
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados os PRs `#46127`, suportando diretórios e pastas no popover de menções `@` do composer; `#46362`, renderizando seleções capturadas via "Add to chat" como chips visuais clicáveis; `#46281`, exibindo capturas de tela e imagens de comentários de itens inline no chat; `#46311`, suprimindo mensagens vazias de assistente no desktop e mobile; `#46316`, compactando linhas de atividades em uma única linha com link para o item; `#46368` (resolve `#46367`), realizando merge em camadas de `_meta` para preservar diretivas permanentes (`SOUL.md` e `MEMORY.md`) em chats gerenciados do Antigravity; e `#46309`, identificando visualmente o modelo autoselecionado no Antigravity.
   - [Progresso de revisão no diff, backend de métricas e abertura de pastas](../issues/progresso-de-revisao-no-diff-backend-de-metricas-e-abertura-de-pastas.md):
     adicionados os PRs `#46334` (resolve `#46332`), reconciliando os modelos Monaco do diff com edições realizadas no modo Edit; `#46333` (resolve `#46331`), ajustando o wrapper do banner de arquivo alterado no disco para flex column e impedindo o colapso do editor de diff; `#46381`, mantendo `EditorEditFileSurface` sob o limite de 400 linhas de lint; `#46225` (refs `#46113`), reutilizando grupos de scan na barra lateral com caminhos-mãe idênticos para evitar duplicações; e `#46276`, introduzindo scrim em tela cheia com fechamento por clique externo no visualizador de imagens.
   - [Abertura de agentes no Chat UI pela CLI e superfície chat na orquestração](../issues/abertura-de-agentes-no-chat-ui-pela-cli-e-superficie-chat-na-orquestracao.md):
     adicionados os PRs `#45594`, priorizando agentes prontos no host no seletor de nova aba da interface e CLI; `#46346`, impedindo a submissão residual de prompts no shell quando o processo CLI encerra prematuramente; `#46129`, disponibilizando "Resume in New CLI" no cabeçalho do chat; e a issue `#46365`, alinhando comandos de criação de workspace e arranque por plugins para seguir a preferência `Chat | CLI` e aceitar `surface`.


