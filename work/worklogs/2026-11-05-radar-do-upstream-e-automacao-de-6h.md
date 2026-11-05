---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-05
completed: 2026-11-05
tags:
  - tooling
refs:
  - issue:gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache
  - issue:modos-build-e-plan-e-ferramentas-de-artifacts-no-native-chat
  - issue:plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados
  - issue:seguranca-macos-remocao-de-allow-dyld-environment-variables-dos-entitlements
  - issue:subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent
---

# Radar de issues e PRs do upstream e automação de 6h (00h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-05)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados mais de 40 novos PRs e issues criados ou
   atualizados entre `2026-11-04T21:00:00Z` e `2026-11-05T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl` para evitar duplicações.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Modos Build e Plan e ferramentas de artifacts no Native Chat](../issues/modos-build-e-plan-e-ferramentas-de-artifacts-no-native-chat.md)
     (PRs `#38286`, `#38248`, `#38251`, `#38253` e `#38272`): seletor de modo operacional Build (construção) vs. Plan
     (arquitetura/planejamento) no chat composer para Claude e Codex com persistência entre reinicializações; injeção de
     `CLAUDE_CODE_ARTIFACT=1` habilitando o ferramental de artifacts em chats nativos; menus de contexto "Add to chat"
     a partir do editor, terminal e markdown preview; indicador visual do branch da conversa logo abaixo da caixa de texto;
     e manutenção da edição de esforço de raciocínio após o primeiro turno de conversa.
3. **Atualização de 4 issues existentes em `work/issues/`:**
   - [Segurança no macOS: remoção de allow-dyld-environment-variables dos entitlements e colisão de LC_UUID](../issues/seguranca-macos-remocao-de-allow-dyld-environment-variables-dos-entitlements.md):
     adicionada a issue `#38247` sobre bloqueio de rede local no macOS Sequoia decorrente de colisão de `LC_UUID` com outros
     apps Electron e compartilhamento indevido de bundle ID com o `Terminal Host`.
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     adicionados a issue `#38254` (propagação de `CLAUDE_CONFIG_DIR` em todas as panes de terminal e background na troca de conta)
     e o PR `#38298` (ações automáticas de "Continue" e "Switch Account" em limites de uso no cliente móvel).
   - [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md):
     adicionados os PRs `#38239` (admissão da resposta final em hooks de turnos e rastreamento de saídas no launcher),
     `#38236` e `#38259` (linhagem cross-machine entre sessões de agentes pai-filho distribuídos via CLI e wire) e issue
     `#38258` (negociação prévia de capacidades de workers).
   - [Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados](../issues/plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados.md):
     adicionados os PRs `#38281` (interface para limpeza de workspaces inativos e indicador de repositório), `#38282`
     (API com permissão para controle dinâmico de temas/aparência desktop em plugins) e `#38296` (fallback inteligente com
     detecção de binários para editores de plugins).
