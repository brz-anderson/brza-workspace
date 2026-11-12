---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-12
completed: 2026-11-12
tags:
  - tooling
refs:
  - issue:aprovacao-de-permissoes-de-workers-pelo-coordenador-identidade-duravel-e-id-de-requisicao
  - issue:badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes
  - issue:cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat
  - issue:indicador-de-uso-de-contexto-virtualizacao-de-ferramentas-e-opcoes-de-chat
  - issue:melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream
  - issue:notificacao-de-perda-de-workers-desengasgo-de-correio-e-tipo-notice
  - issue:protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-12)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-11T21:00:00Z` e `2026-11-12T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Aprovação de permissões de workers pelo coordenador, identidade durável e ID de requisição](../issues/aprovacao-de-permissoes-de-workers-pelo-coordenador-identidade-duravel-e-id-de-requisicao.md):
     rastreia o PR `#41306` (configuração opt-in em Settings → Orchestration para permitir que coordenadores aprovem prompts de permissão de workers via CLI `orchestration approve --reason "<motivo>"` ou `deny`, mantendo salvaguarda estrita para verificações `personOnly`),
     PR `#41304` (`worker-start --request-id <uuid>` com ledger idempotente evitando duplicação de workers por perda de respostas RPC, além de inspeção estruturada de opções aceitas vs relatadas),
     PR `#41286` (identificador persistente `Copy Agent ID` / `orca_session_id:<agent>_<uuid>` para agentes de terminal salvo em `agent-identities.db`, preservado em sleep/wake, reinicializações e exposto em `orca worktree ps --json`) e
     PR `#41301` / issue `#40914` (ações de cópia de comando, saída ou ambos no menu de contexto do terminal delimitadas por marcadores semânticos OSC 133).
3. **Atualização de 3 issues existentes em `work/issues/`:**
   - [Melhorias de Native Chat, ACP do Gemini CLI, abas e diff no upstream](../issues/melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream.md):
     adicionados o PR `#41314` (unificação abrangente de Antigravity ACP no Windows com binário host `agy >= 1.5.2` e runtime gerenciado 1.4.5, streaming reativo ao vivo de turnos de wakeup de subagentes/tarefas concluídas a partir de `.system_generated`, descoberta sessionless `agy models`, injeção de regras `GEMINI.md`/`AGENTS.md` e suporte a skills no slash `/`, consolidando e resolvendo as issues `#40321` e `#41298`).
   - [Cartões de Pull Request, feedback de Steer e atalhos no Native Chat](../issues/cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat.md):
     adicionados o PR `#41333` / issue `#37005` (envio de imagens e screenshots > 5 MB no chat Claude sem erro de recusa, delegando a redução de tamanho para o auto-shrink nativo do Claude Code e elevando o teto do despachador para 50 MB / 64 MB) e
     o PR `#41337` / issue `#41134` (abertura com Cmd/Ctrl-click de wikilinks `[[wikilink]]` e citações sobrescritas em qualquer ponto do rótulo no editor ProseMirror).
   - [Badges de worktree para plugins, cadência de PR e redesenho de automações](../issues/badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes.md):
     adicionados o PR `#41332` (eliminação de 500 fetches e 422 merge checks repetidos no watch de status de CI/PR checks),
     o PR `#41268` / issue `#41269` (suspensão imediata de consultas de rate limit em segundo plano para Claude e Codex quando desativados em configurações, evitando vazamentos fora de VPN) e
     o PR `#41325` (descoberta assíncrona de caminhos de setup e atribuição de demanda Git).

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-12)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-12T03:00:00Z` e `2026-11-12T09:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     rastreia o PR `#41446` (aviso prévio e bloqueio antes de excluir workspaces com arquivos ignorados locais não replicados, como `.env` e configs locais, através de `readWorktreeAtRiskLocalFiles`),
     PR `#41392` (compactação em tempo real do histórico SQLite de chat com gatilho `journal_outcome_item_supersede` e worker thread dedicada retendo apenas primeiro e último registro de cada mensagem, reduzindo o banco em 528 MB sem travar o loop principal),
     PR `#41366` / STA-14925 (corroboração de prontidão `tui-idle` exigindo o marcador de composer `❯` do Claude também para terminais adotados identificados por título OSC, prevenindo despacho prematuro de comandos) e
     PR `#41384` (remoção de refetches cíclicos de badges do Linear por foco de janela, reduzindo requisições em 83,3%).
3. **Atualização de 2 issues existentes em `work/issues/`:**
   - [Cartões de Pull Request, feedback de Steer e atalhos no Native Chat](../issues/cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat.md):
     adicionado o PR `#41359` (roteamento de pré-visualizações de PRs privados do GitHub em chats de pastas avulsas sem repositório Git através de clones locais existentes no mesmo host, eliminando erros 404 e "No preview for this page").
   - [Notificação de perda de workers, desengasgo de correio e tipo notice](../issues/notificacao-de-perda-de-workers-desengasgo-de-correio-e-tipo-notice.md):
     adicionados o PR `#41426` / STA-14936 (encerramento do loop de busca de correio remoto em servidores pareados quando todas as conexões terminam),
     o PR `#41424` / STA-14935 (reconstrução preguiçosa da saída de terminal apenas quando um relatório de saída de worker for emitido),
     o PR `#41423` / STA-14934 (descarte do bookkeeping de turnos no `worker stop reporter` no fechamento de chats para evitar vazamento de memória) e
     o PR `#41422` / STA-14933 (encerramento automático de cartões de aprovação órfãos no startup da aplicação).

### 3. Ciclo de 6h (12:00 BRT / 15:00 UTC em 2026-11-12)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-12T09:00:00Z` e `2026-11-12T15:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Indicador de uso de contexto, virtualização de ferramentas e opções de chat](../issues/indicador-de-uso-de-contexto-virtualizacao-de-ferramentas-e-opcoes-de-chat.md):
     rastreia o PR `#41546` (indicador persistente com anel gráfico e leitura de tokens ocupados na janela de contexto no Native Chat desktop e mobile, atendendo às issues `#29995` e `#41119`),
     PR `#41552` (virtualização de linhas de execução de ferramentas abertas no leitor de chat, renderizando apenas linhas no viewport e eliminando engasgos com saídas longas),
     PR `#41544` / STA-14534 e STA-14532 (associação isolada de opções de modelo/esforço por conversa e bloqueio preventivo contra submissão involuntária de rascunhos no terminal) e
     PR `#41491` / tickets 5122 e 5141 (preservação de processos filhos de OMP e retenção de saídas de background durante varreduras periódicas de ociosidade do chat).
3. **Atualização de 3 issues existentes em `work/issues/`:**
   - [Melhorias de Native Chat, ACP do Gemini CLI, abas e diff no upstream](../issues/melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream.md):
     adicionados o PR `#41504` / issue `#40865` (injeção automática de regras `GEMINI.md`/`AGENTS.md` e estabilização de opções restauradas em chats gerenciados Antigravity),
     o PR `#41511` (exclusões explícitas de loopback no ambiente de proxy para impedir erros SOCKS na conexão privada local do Antigravity) e
     o PR `#41531` (redesenho de configurações de contas Antigravity em cartões dedicados para terminal e chat).
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionados o PR `#41483` (tabela durável de exclusão e ocultação imediata de linha na UI durante cleanup em background com recuperação após reinicialização),
     o PR `#41480` (proprietário único para o catálogo de worktrees de cada repositório, compartilhando observações e eliminando `git worktree list` redundantes) e
     o PR `#41457` (restrição estrita dos atalhos de exclusão de workspace à seleção na barra lateral, evitando acionamentos a partir de foco no terminal ou editor).
   - [Aprovação de permissões de workers pelo coordenador, identidade durável e ID de requisição](../issues/aprovacao-de-permissoes-de-workers-pelo-coordenador-identidade-duravel-e-id-de-requisicao.md):
     adicionados o PR `#41498` (inspeção de linha de comando de processos para preservar flags de permissão total `--yolo`/`bypassPermissions` em split-panes e retomadas não gravadas) e
     o PR `#41476` (enfileiramento atômico de mensagens e configurações do Codex, retendo o despacho até que os parâmetros atualizados sejam aceitos pelo provedor).


