---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-23
completed: 2026-11-23
tags:
  - tooling
refs:
  - issue:alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas
  - issue:badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes
  - issue:consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks
  - issue:fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks
  - issue:gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache
  - issue:leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados
  - issue:progresso-de-revisao-no-diff-backend-de-metricas-e-abertura-de-pastas
  - issue:protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle
  - issue:retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot
  - issue:vazamento-de-memoria-gpu-webgl-no-terminal-e-performance-macos
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-23)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e commits criados ou atualizados entre `2026-11-22T21:00:00Z` e `2026-11-23T03:00:00Z` (range upstream `2178e7cd95a..15407c8854f`), comparando com os registros em `work/issues/` e o índice `.brza/index.jsonl`.
2. **Atualização de 4 issues rastreadas em `work/issues/`:**
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados os PRs `#47200`, migrando mensagens enfileiradas ordenadamente ao substituir sessões de chat e drenando mensagens de conectores com aviso explícito de parada; `#47220`, liberando a execução do correio de terceiros no próximo turno após falhas operacionais não causadas por limite de cota (*usage limit*); e `#47191`, permitindo que agentes anexem tarefas, PRs, URLs, arquivos e comandos `worker-start --item` a itens em aberto de outros agentes na árvore do workspace com atribuição amigável ("Another agent").
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados os PRs `#47135`, desvinculando (*unbinds*) Runs ativos e notificando perguntas de workers com aviso de *no reader* imediatamente quando o terminal do coordenador é encerrado ou sua pane esvaziada; e `#47081`, exibindo o estado de espera na árvore de tarefas quando um worker aguarda sua própria tarefa em segundo plano e disparando notificação única ao coordenador após 60 minutos de espera contínua.
   - [Fontes web em plugins, isolamento de atalhos e resiliência de hooks](../issues/fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks.md):
     adicionado o PR `#47107` (resolve `#47104`), reconhecendo rotas `/src/{branch,tag,commit}/<ref>` em repositórios Codeberg, Gitea e Forgejo no instalador Git de plugins, extraindo a URL base de clone e o ref correto.
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     adicionado o PR `#47209` (refs `#47146`), resolvendo raízes de perfis Claude via `realpath` para desduplicar a varredura, análise e indexação de transcripts em diretórios compartilhados de projetos globais.

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-23)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e commits criados ou atualizados entre `2026-11-23T03:00:00Z` e `2026-11-23T09:00:00Z` (range upstream `15407c8854f..ebe35b9edb6`), comparando com os registros em `work/issues/` e o índice `.brza/index.jsonl`.
2. **Atualização de 5 issues rastreadas em `work/issues/`:**
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados os PRs `#47308`, `#47309` e `#47429`, introduzindo o estado formal `Waiting` para itens retidos por fatores externos (CI, deploy, review, usage limit) com explicação no hover card, janela desktop e mobile ("N needs you"); `#47359` (resolve `#47358`), aplicando `overflow-wrap: anywhere` para conter sumários longos de tarefas em background sem forçar barra de rolagem horizontal no chat; `#47346`, exibindo botões Edit e Delete no hover/foco e retendo Steer na fila de envio; `#47337`, preservando opções completas (modo Plan/Build, modelo, esforço, personality e steer) ao migrar mensagens enfileiradas; e `#47464`, `#47461`, `#47385`, `#47372`, sincronizando respostas de formulários multi-pergunta em itens para evitar despertar precoce de agentes.
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados os PRs `#47370` e `#47371`, vinculando e fechando automaticamente terminais de setup, abas de startup e terminais secundários criados pelo worker quando este encerra ou é liberado; `#47364` e `#47363`, propagando a linhagem de conversa estruturada (`orchestration.chat-lineage.v1`) para sub-workers e servidores pareados conectados; `#47355`, reduzindo de 60 para 20 minutos o tempo de espera contínua em background antes de alertar o coordenador; e `#47469` (resolve `#47440`), resolvendo operações de despachos de follow-up a partir da linhagem para entregar relatórios `worker_done` sem retenção perene.
   - [Badges de worktree para plugins, cadência de PR e redesenho de automações](../issues/badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes.md):
     adicionados os PRs `#47189`, introduzindo o comando `orca automations watch-pr owner/repo#n` para monitoramento one-shot de PRs com prazo padrão de 2 horas sobre múltiplos eventos e registrando o gatilho `github.ci_finished`; e `#47483`, detalhando justificativas e contabilidade de chamadas ignoradas em diagnósticos de webhooks.
   - [Fontes web em plugins, isolamento de atalhos e resiliência de hooks](../issues/fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks.md):
     adicionados os PRs `#42473`, implementando drag-and-drop para reordenação de abas na Activity Bar, opções Hide, Move e Reset no menu de contexto e menu "More" de overflow; e `#47296` (refs `#47310`), preservando segmentos `-` em branches e refs ao analisar URLs de instalação Git de plugins no GitHub e Codeberg.
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados os PRs `#47331`, atualizando em background o servidor ACP empacotado do Antigravity com backoff e checagem de espaço livre; `#47329`, preservando o acesso a Claude e GPT-OSS em contas Google no Antigravity sob ACP 1.5.2; `#47314` (resolve `#47202`), listando modelos dinâmicos do Cursor nos seletores com esforço e modo Fast; e `#47459` (refs `#47454`), limpando saídas de ferramentas em eventos `done` sem resposta do Kiro 3.
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionados os PRs `#45918`, mantendo ativo o helper de checkpoint/tidy-up do chat store sem travar salvamentos; e `#42532`, estabilizando a ordem das linhas na listagem de cleanup enquanto o diálogo de exclusão estiver aberto.

### 3. Ciclo de 6h (12:00 BRT / 15:00 UTC em 2026-11-23)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e commits criados ou atualizados entre `2026-11-23T09:00:00Z` e `2026-11-23T15:00:00Z` (range upstream `ebe35b9edb6..59f3122bc8c`), totalizando 80 commits e comparando com os registros em `work/issues/` e o índice `.brza/index.jsonl`.
2. **Atualização de 11 issues rastreadas em `work/issues/`:**
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados os PRs `#42129`, introduzindo o pill Side chat no composer ao digitar `/btw` ou `/side`; `#47564`, mapeando perguntas interativas abertas para o estado visual `waiting` em vez do alarmista `blocked`; `#47432`, corrigindo a contagem de workers no composer e permitindo scroll nativo fluido sem snap agressivo na faixa de workers; `#47553` (resolve `#47552`), assegurando iluminação contínua do marcador lateral de turno (rail tick) entre linhas consecutivas; `#47587`, mantendo o modal seletor de modelos aberto ao clicar ou arrastar o scrollbar; `#47485`, restaurando rascunhos de resposta na caixa de comentários quando o agente reformular uma pergunta em itens; `#45168`, preservando mensagens paged-in anteriores ao receber atualizações de snapshot de transcrição; e `#47559`, confinando a abertura de hover cards estritamente à navegação por teclado.
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados os PRs `#47562`, documentando o contrato formal de ciclo de vida e teardown de workers (settled, ended, destroyed) e posicionamento host-aware (`--environment`, `--repo`); `#46045`, substituindo polling periódico de processos por notificações orientadas a eventos do sistema operacional em terminais ociosos; `#47543`, identificando a causa real de encerramento de workers e distinguindo cancelamentos de perda de host (`host_lost`); e `#47503`, persistindo relatórios parciais e finais de workers pós-Stop em salas de grupos e amarrando nomenclatura de chats à sala de origem.
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados os PRs `#47400`, executando chats via Gemini API key e gcloud ADC no `agy` sob home própria do Orca com regras de `~/.gemini` e skills locais; `#47525`, repassando configurações de proxy do app para os probes de cota da CLI Go do `agy`; e `#47546`, enfileirando ações concorrentes de gestão de contas Antigravity (Save, Refresh, Select, Remove) durante leituras em background sem descarte silencioso de cliques.
   - [Leitura antecipada e preservação de skills no arranque e nos plugins](../issues/leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins.md):
     adicionados os PRs `#47582`, introduzindo a flag `skipsSharedSkillFolders` para ocultar `~/.agents/skills` nos seletores do Claude Code; `#47158`, trazendo clareza visual e destino de backup na substituição de cópias locais divergentes de skills empacotadas; e `#47154`, cacheando a listagem de skills no diálogo de compartilhamento de bots para eliminar mais de 32.800 chamadas redundantes a `lstat`.
   - [Consumo de recursos em agentes: reaper de LSP e overhead de hooks](../issues/consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks.md):
     adicionado o PR `#45844`, registrando o PID de processos de agentes de chat (Claude, Codex) para contabilizar toda a árvore de subprocessos e LSPs associados sob a seção Agents no Resource Manager, atribuindo-os ao workspace correspondente e eliminando falsos avisos amarelos em listagens concorrentes de terminais.
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionado o PR `#47629`, adicionando o código de erro `ENOTEMPTY` à lista de retry seguro na remoção recursiva de diretórios somente leitura gerados no macOS sob o runtime Bun durante rotinas de reclaim space.
   - [Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados](../issues/plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados.md):
     adicionados os PRs `#47683`, preservando a visibilidade do workspace ativo através do virtualizador ao alternar a exibição de workspaces suspensos; `#47542`, adotando a grafia canônica do backlink `.git/worktrees/<name>/gitdir` em volumes APFS/NTFS para evitar worktrees órfãos; `#47249`, medindo a janela de frescor de repositórios a partir da conclusão da varredura e respondendo do cache publicado durante atualizações; e `#47679`, reportando chats de projetos excluídos como `agent_session_workspace_removed`.
   - [Badges de worktree para plugins, cadência de PR e redesenho de automações](../issues/badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes.md):
     adicionados os PRs `#47491`, gravando o motivo real tipado de recusa inicial de agentes em execuções de automação; e `#47479` (resolve `#47386`), apresentando webhooks de automação recém-criados em setup cards destacados com ação imediata "Copy URL".
   - [Fontes web em plugins, isolamento de atalhos e resiliência de hooks](../issues/fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks.md):
     adicionados os PRs `#47561`, tratando listas de fontes separadas por vírgula com aspas individuais em CSS para preservar fallbacks tipográficos; e `#47586`, suprimindo atalhos de gerenciamento de abas (Cmd+W e Cmd+T) quando telas cheias de sobreposição (Settings, Activity) ocultam o workspace.
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     adicionados os PRs `#47155`, oferecendo ação direta de re-autenticação para contas Codex expiradas ou revogadas na tela de uso; e `#47540`, restringindo alertas de falta de assinatura no OpenCode Go estritamente a respostas com `EntitlementError`.
   - [Progresso de revisão no diff, backend de métricas e abertura de pastas](../issues/progresso-de-revisao-no-diff-backend-de-metricas-e-abertura-de-pastas.md):
     adicionado o PR `#47639` (resolve `#47631`), incorporando `ctime` aos carimbos de arquivos para invalidar o cache de diff do Git em regravações in-place com mtime idêntico.

### 4. Ciclo de 6h (18:00 BRT / 21:00 UTC em 2026-11-23)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs, issues e commits criados ou atualizados entre `2026-11-23T15:00:00Z` e `2026-11-23T21:00:00Z` (range upstream `59f3122bc8c..dbb1cf1bc41`, 48 commits mesclados), comparando contra o catálogo `work/issues/` e o índice `.brza/index.jsonl` para evitar duplicatas.
2. **Atualização de 10 issues existentes em `work/issues/`:**
   - [Vazamento de memória GPU WebGL no terminal e performance macOS](../issues/vazamento-de-memoria-gpu-webgl-no-terminal-e-performance-macos.md):
     adicionado o PR `#43465` (resolve `#43464`, commit `1560ff5b55e`), implementando rebuild periódico do renderizador WebGL do terminal ao atingir página de atlas de 4096², com intervalo de 60s, validação de 2s de PTY ocioso e 2s de pausa na digitação, além de desacoplar painéis encobertos.
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados os PRs `#47784` (resolve `#47780`), `#47774`, `#47724` (resolve `#47715`), `#47667`, `#47719`, `#47457` (refs `#41800`), `#43521` (commit `dbb1cf1bc41`), e as issues `#47807` e `#47781`, tratando badges de status de subagentes no cabeçalho, auto-scroll do chat com ancoragem no rodapé, drag-and-drop de anexos e renderização de diagramas.
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados os PRs `#47828`, `#47819`, `#47783` (resolve `#46100`), `#47536` (commit `21aa900d9c0`), `#47575` e a issue `#47817`, garantindo sobrevivência de coordenadores após reinício do daemon via `providerRelayKeep`, tratamento do erro de capacidade `TerminalHostCapError` e despertar resiliente de workers.
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionados o PR `#47716` (resolve `#47703`), commits `15830ffd7e7` (`#47409`), `ee8d885823a` (`#45854`) e PR `#47657`, introduzindo compactação ociosa no Claude (`idleCompaction`), guarda de espaço em disco e mitigação de contenção no cleanup de workspaces.
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     adicionados os commits `231551f9f65` (`#45294`), `6e4ebc83d00` (`#47737`), `85d8985d9e0` (`#47778`), `da839538408` (`#47764`), PR `#47689` e issue `#47829`, preservando `history.jsonl` em migrações do Codex e aprimorando o chaveamento automático de cotas e prompt cache.
   - [Fontes web em plugins, isolamento de atalhos e resiliência de hooks](../issues/fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks.md):
     adicionados os commits `63930784bb2` (`#47767`, resolve `#47766`), `c73dce43060` (`#47710`, resolve `#47709`) e PR `#47702`, tratando URLs com `/blob/` na instalação de plugins Git, parsing de caracteres literais `+` e `,` em atalhos e suporte a `CodeInput`.
   - [Badges de worktree para plugins, cadência de PR e redesenho de automações](../issues/badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes.md):
     adicionados o PR `#47726` e as issues `#47796`, `#47795`, `#47794`, `#47793`, tratando motivos tipados de skip (`skipped_needs_interactive_auth`), recuperação pós-restart do daemon e tratamento de ocorrências perdidas em cron schedules com DST.
   - [Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados](../issues/plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados.md):
     adicionados os PRs `#47805` (resolve `#47776`), `#47750`, `#47816`, `#47743` (fecha `#47747`) e `#47739`, implementando quebra de linha de erros Git no Source Control, contenção de foco no branch dialog, aninhamento de grupos de projetos, contadores de bots e projetos e rastreamento automático do arquivo ativo no File Explorer.
   - [Consumo de recursos em agentes: reaper de LSP e overhead de hooks](../issues/consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks.md):
     adicionados os commits `6e0805a2e1f` (`#47769`), `64eb525c558` (`#47757`), `64a57263cf4` (`#47529`), `e2c8f4756e8` (`#47705`, refs `#19792`), PR `#47765` e issues `#47826` e `#47825`, consolidando leituras em lote de frotas de bots, indexação de turnos ancorados no journal SQLite, saneamento do Chromium Crashpad herdado e suporte a hooks do Droid.
   - [Leitura antecipada e preservação de skills no arranque e nos plugins](../issues/leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins.md):
     adicionadas as issues `#47785` (invocação de skills restritas a usuários via especificação `worker-start --spec-file`) e `#47813` (gravação de tarefas no navegador embutido para síntese de skills).
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados os commits `9948925bbd1` (`#47721`, resolve `#47707`), `8144d7881bb` (`#46518`), e os PRs de browser `#47806`, `#47787`, `#47803`, `#47791`, `#47782`, `#47777`, com suporte a hooks do zcode em `setting.json`, servidores Codex compartilhados no Windows em Job objects kill-on-close e isolamento de segurança e proxy do navegador.



