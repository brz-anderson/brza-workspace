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
  - issue:fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks
  - issue:gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle
  - issue:retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot
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

