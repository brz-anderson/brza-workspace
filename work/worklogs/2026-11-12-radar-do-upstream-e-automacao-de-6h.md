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
  - issue:melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream
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
