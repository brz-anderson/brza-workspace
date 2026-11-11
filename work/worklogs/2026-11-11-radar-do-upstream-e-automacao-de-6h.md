---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-11
completed: 2026-11-11
tags:
  - tooling
refs:
  - issue:agente-kiro-no-native-chat-janela-flutuante-e-enderecamento-de-workspaces
  - issue:alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas
  - issue:autenticacao-mcp-no-chat-alerta-de-turnos-ativos-e-cache-de-orquestracao
  - issue:cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat
  - issue:comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais
  - issue:exclusao-de-repositorios-bare-como-alvos-de-arranque-e-criacao-de-pastas
  - issue:hidratacao-de-repositorios-no-arranque-cache-de-sessao-e-navegacao-de-abas
  - issue:leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins
  - issue:melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream
  - issue:notificacao-de-perda-de-workers-desengasgo-de-correio-e-tipo-notice
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:seguranca-de-hooks-em-worktrees-e-integridade-de-setup-em-automacoes
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-11)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-10T21:00:00Z` e `2026-11-11T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Notificação de perda de workers, desengasgo de correio e tipo notice](../issues/notificacao-de-perda-de-workers-desengasgo-de-correio-e-tipo-notice.md):
     rastreia o PR `#40983` (alerta unificado `lost` ao coordenador quando workers falham no startup, sofrem fechamento de painel, queda de PTY ou encerramento inesperado, prevenindo esperas infinitas),
     PR `#40972` (introdução do tipo de mensagem `notice` para despachos interagentes com `--to`, eliminando interrupções espúrias e comandos reply desnecessários),
     PR `#40977` / issue `#40968` (desengasgo de filas de relay ao responder a `send --type question` de workers remotos em servidores pareados),
     PR `#40967` e PR `#40963` (recuperação de workers de chat e reabertura de terminais interrompidos com o restart da aplicação),
     PR `#40949` (encerramento limpo de sessões e relato de pareamento desfeito ao remover servidores remotos) e
     PR `#40962` / issue `#40956` (substituição de subshell intermediário por `exec` no profile do Claude, evitando falhas `agent_not_in_foreground` sob bash).
3. **Atualização de 3 issues existentes em `work/issues/`:**
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados o PR `#40986` / issue `#40984` (descoberta e exibição de skills instaladas do Antigravity no menu slash `/` do Native Chat),
     o PR `#40980` / issue `#40979` (descoberta dinâmica de modelos recém-lançados via CLI host `agy` para o picker de novos chats),
     o PR `#40867` / issue `#40865` (injeção automática de regras de usuário e workspace `AGENTS.md` e `GEMINI.md` no prompt ACP via `_meta.antigravity.systemPrompt.append`) e
     o PR `#40912` (composer e escolha de modelos desbloqueados no primeiro chat de novos worktrees).
   - [Autenticação MCP no chat, alerta de turnos ativos e cache de orquestração](../issues/autenticacao-mcp-no-chat-alerta-de-turnos-ativos-e-cache-de-orquestracao.md):
     adicionados o PR `#40953` / issue `#40640` (diálogo de aviso antes de fechar janela com agentes em turno ativo no Native Chat `mid-turn`) e
     o PR `#40923` / issue `#40607` (remoção definitiva de hook incompatível no Factory Droid).
   - [Segurança de hooks em worktrees e integridade de setup em automações](../issues/seguranca-de-hooks-em-worktrees-e-integridade-de-setup-em-automacoes.md):
     adicionados o PR `#40978` / issue `#40974` (comando `/hooks` para revisão e homologação criptográfica de hooks do Codex diretamente no chat) e
     o PR `#40976` (cartão unificado e condensado para hooks de worktree nas configurações).

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-11)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-11T03:00:00Z` e `2026-11-11T09:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Exclusão de repositórios bare como alvos de arranque e criação de pastas](../issues/exclusao-de-repositorios-bare-como-alvos-de-arranque-e-criacao-de-pastas.md):
     rastreia o PR `#41018` / issue `#40698` e STA-14647 (eliminação de diretórios Git `.bare` como alvos de lançamento executáveis, prevenindo chats e terminais em pastas vazias sem arquivos de checkout, e seleção automática de checkouts reais vinculados como default workspace),
     PR `#40999` / issue `#40995` (dispensa da exigência de identidade Git `user.name`/`user.email` na criação de folder projects locais ou remotos via SSH),
     PR `#40774` (remoção da retenção em memória de instâncias e PTYs de agentes cujas tarefas foram concluídas) e
     PR `#40852` (resultados diretos em lista navegável na pesquisa de configurações do Studio).
3. **Atualização de 3 issues existentes em `work/issues/`:**
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados o PR `#40935` (preservação de imagens geradas acopladas ao cartão da resposta final no chat, impedindo sobrescrita de texto, duplicação e perda em histórico) e
     a issue `#41008` (exibição de badges de modelo e nível de esforço de raciocínio, e.g. `Opus · high`, na listagem de subagentes do painel de agentes).
   - [Comandos shell no chat, recibos de perguntas e foco espacial em terminais](../issues/comandos-shell-no-chat-recibos-de-perguntas-e-foco-espacial-em-terminais.md):
     adicionados o PR `#41015` / issue `#41010` (restauração de foco na folha/split ativa ao navegar via paleta `Cmd+J`),
     o PR `#40870` / issue `#40868` (criação de divisões de terminal via RPC com `activate: false` em segundo plano para não roubar foco) e
     a issue `#41009` (emissão de sequências de escape para reset de rastreamento de mouse e foco em restauração a frio de PTYs).
   - [Leitura antecipada e preservação de skills no arranque e nos plugins](../issues/leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins.md):
     adicionada a issue `#41017` (invalidação e ciclo de vida de `paneDiscoveryCache` para permitir descoberta imediata de skills recém-instaladas em chats existentes).

### 3. Ciclo de 6h (12:00 BRT / 15:00 UTC em 2026-11-11)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-11T09:00:00Z` e `2026-11-11T15:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Hidratação de repositórios no arranque, cache de sessão e navegação de abas](../issues/hidratacao-de-repositorios-no-arranque-cache-de-sessao-e-navegacao-de-abas.md):
     rastreia o PR `#41088` / STA-14831 (eliminação de reconstrução redundante de objetos de repositório em Smart-order save, reduzindo CPU do processo principal em 89,9% nos primeiros 5 min e tempo de listagem da CLI de >30s com timeout para 140ms em 1.000 workspaces),
     PR `#41091` (banco de cache versionado por formato `session-parse-cache.vN.sqlite` para histórico de sessões, evitando re-leituras massivas de transcripts em trocas de build e adotando silêncio em cargas menores que 64MB),
     PR `#41068` / issue `#41062` (ação "Go to Workspace" no menu de contexto de abas de chat e terminal) e
     issues `#41107` e `#41115` (preservação de prompt em `agent.launch` e persistência do nome real da sessão retomada na lista de agentes).
3. **Atualização de 3 issues existentes em `work/issues/`:**
   - [Cartões de Pull Request, feedback de Steer e atalhos no Native Chat](../issues/cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat.md):
     adicionados o PR `#41099` / issue `#41097` (confirmação em dois toques deliberados de Escape em janela de 2s antes de cancelar turnos ativos no chat, prevenindo paradas acidentais) e
     o PR `#41100` (prova Git local via `merge-tree --write-tree` e `diff-tree` para certificar que o branch rebaseado contém apenas o PR mergeado, mantendo o cartão no Source Control com opção de exclusão segura).
   - [Agente Kiro no Native Chat, janela flutuante e endereçamento de workspaces](../issues/agente-kiro-no-native-chat-janela-flutuante-e-enderecamento-de-workspaces.md):
     adicionado o PR `#40858` / issue `#13302` (abertura de novos terminais e agentes em servidores remotos pareados diretamente a partir do submenu "Open on another host" no botão "+" do Floating Workspace).
   - [Melhorias de Native Chat, ACP do Gemini CLI, abas e diff no upstream](../issues/melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream.md):
     adicionado o PR `#40932` / issue `#40321` (suporte a Antigravity ACP no Windows a partir de `%LOCALAPPDATA%\agy\bin\agy.exe`, catálogo dinâmico de modelos via `agy models` e streamer reativo `antigravity-reactive-turn-streamer.ts` para exibição instantânea de turnos de wakeup de subagentes/tarefas a partir de `transcript.jsonl`).

