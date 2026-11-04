---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-04
completed: 2026-11-04
tags:
  - tooling
refs:
  - issue:abertura-de-agentes-no-chat-ui-pela-cli-e-superficie-chat-na-orquestracao
  - issue:gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache
  - issue:melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream
  - issue:seguranca-de-hooks-em-worktrees-e-integridade-de-setup-em-automacoes
  - issue:subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent
  - issue:workers-de-plugins-em-hosts-remotos-e-gerenciamento-cli-de-ssh
---

# Radar de issues e PRs do upstream e automação de 6h (00:00 BRT)

## O que foi feito

### Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-04)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisadas 43 novos PRs e 17 novas issues criados ou
   atualizados entre `2026-11-03T21:00:00Z` e `2026-11-04T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl` para evitar duplicações.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Segurança de hooks em worktrees e integridade de setup em automações](../issues/seguranca-de-hooks-em-worktrees-e-integridade-de-setup-em-automacoes.md)
     (PRs `#37977`, `#37978`, `#37979`, `#37941` e `#37931`): validação de hash SHA-256 de scripts de setup antes da
     execução em novos worktrees, isolamento contra RCE em branches untrusted, homologação explícita de hooks em automações
     e seletor compartilhado de modelos/esforço/permissões.
3. **Atualização de 5 issues existentes em `work/issues/`:**
   - [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md):
     adicionados PR `#37918` (entrega de correio durante turnos ativos via steering sem espera ociosa), PR `#37966` (origem
     limpa de avisos de conclusão de background sem avatar artificial), PR `#37974` (limpeza de alertas desktop reconhecidos)
     e issue `#38000` (diferenciação visual entre Coordenador e workers na árvore de sessões);
   - [Abertura de agentes no Chat UI pela CLI e superfície chat na orquestração](../issues/abertura-de-agentes-no-chat-ui-pela-cli-e-superficie-chat-na-orquestracao.md):
     adicionados PR `#38001` (abertura limpa de novo chat caso sessão CLI retomada não tenha transcript salvo) e PR `#37984`
     (split de aba Chat UI abre terminal shell de apoio em vez de clonar sessão de IA);
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     adicionados PR `#37943` (reinício imediato de sessões e workers na nova conta ao alternar), PR `#37998` (login limpo no
     Antigravity Chat sem reusar cache local) e PR `#38010` (opção Ultracode no seletor de esforço);
   - [Workers de plugins em hosts remotos e gerenciamento CLI de SSH](../issues/workers-de-plugins-em-hosts-remotos-e-gerenciamento-cli-de-ssh.md):
     adicionados PR `#37971` / issue `#37949` (subcomando `orca host rm` para remoção de servidores SSH salvos) e PR `#37926`
     (aplicação estrita de `IdentitiesOnly` no transporte SSH nativo);
   - [Melhorias de Native Chat, ACP do Gemini CLI, abas e diff no upstream](../issues/melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream.md):
     adicionados PR `#37965` (recuperação de respostas bloqueadas e isolamento de UI de plugins), PR `#37960` (exibição de
     arquivos propostos e diffs em aprovações Codex), PR `#37952` (navegação de abas de chat por `Ctrl+PageUp`/`PageDown`),
     PR `#37932` (cache persistente de imagens em chats) e issue `#37983` (ranking unificado no menu `/` entre skills e comandos).

## Fora do workspace

- **O quê e onde:** automação `Radar do upstream (stablyai/orca)` (`id: f75b8281-8ae3-4558-afe4-7ab5bbc35601`) ativa no
  runtime do BrzA Studio rodando a cada 6h (`0 */6 * * *`).
- **Estado:** executando normalmente em conformidade com o cronograma estabelecido.
