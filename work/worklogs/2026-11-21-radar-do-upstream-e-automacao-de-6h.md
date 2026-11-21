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
  - issue:alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas
  - issue:comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais
  - issue:gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache
  - issue:leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins
  - issue:protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle
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
