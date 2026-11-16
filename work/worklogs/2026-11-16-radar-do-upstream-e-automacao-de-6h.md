---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-16
completed: 2026-11-16
tags:
  - tooling
refs:
  - issue:alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas
  - issue:aprovacao-de-planos-abc-feedback-de-revisao-inline-e-resiliencia-de-composer-no-chat
  - issue:chaveamento-automatico-de-contas-claude-por-limite-de-uso-e-planos-observados
  - issue:consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks
  - issue:execucao-em-lote-no-computer-use-e-protecao-de-digitacao-segura
  - issue:protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle
  - issue:retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot
  - issue:servidor-mcp-stdio-na-cli-e-otimizacoes-de-captura-no-computer-use
  - issue:workers-de-plugins-em-hosts-remotos-e-gerenciamento-cli-de-ssh
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-16)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-15T21:00:00Z` e `2026-11-16T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 2 novas issues priorizadas em `work/issues/`:**
   - `priority: high` — [Execução em lote de ações no Computer Use, proteção de digitação segura e otimizações de acessibilidade](../issues/execucao-em-lote-no-computer-use-e-protecao-de-digitacao-segura.md):
     rastreia o PR `#42859` (resolve Issue `#42850` — execução em lote de até 50 ações sequenciais com `orca computer batch` mantendo diff baseline e economizando turnos),
     o PR `#42861` (resolve Issue `#42849` — bloqueio de injeção de teclas automatizadas se o operador estiver digitando ativamente ou sobre campos seguros de senha `NSSecureTextField`),
     o PR `#42855` (resolve Issue `#42848` — truncamento de nós fora da tela em listas e textos longos de snapshots de acessibilidade no macOS),
     o PR `#42842` (resolve Issue `#42843` — desativação de screenshots padrão após micro-ações de GUI, exigindo flag explícita `--screenshot`),
     os PRs `#42863` e `#42826` (resolvem Issues `#42846` e `#42825` — substituição de polling fixo de 200ms por subscrição direta a notificações de acessibilidade `AXUIElementRegisterForNotification`),
     o PR `#42816` (resolve Issue `#42815` — extração consolidada de atributos AX em chamada única via `AXUIElementCopyMultipleAttributeValues`),
     e os PRs `#42853` e `#42814` (resolvem Issues `#42841` e `#42813` — guias enxutos para orientar modelos ao caminho de menor custo de tokens em Computer Use).
   - `priority: high` — [Chaveamento automático de contas Claude por limite de uso, planos observados e resgate de cota](../issues/chaveamento-automatico-de-contas-claude-por-limite-de-uso-e-planos-observados.md):
     rastreia o PR `#42856` (chaveamento automático e transparente de conta do Claude ao atingir 100% da cota, selecionando a conta salva com reset mais próximo e reiniciando tarefas sem perda de contexto),
     o PR `#42917` (exibição da categoria de plano Free/Pro/Team/Enterprise em contas salvas de Claude e Codex),
     e o PR `#42891` (resolve Issue `#42887` — resgate de resets de cota do Claude diretamente pelo menu de contas do app).
3. **Atualização de 6 issues existentes em `work/issues/`:**
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados o PR `#42839` (resolve STA-15101 — expurgo de cópias resolvidas de chat de workers convertendo-as em referências leves, `auto_vacuum = INCREMENTAL` e ação 'Reclaim space' em *Settings › Agent orchestration*)
     e a Issue `#42852` (roteamento para o host criador original de ordens de Stop/Close em workers federados iniciados remotamente).
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados o PR `#42847` (resolve Issue `#40321` — suporte a Antigravity Native Chat no Windows conectando diretamente ao host `agy acp`)
     e o PR `#42896` (correção na deleção de tokens de autenticação garantindo que falhas em contas Gemini Enterprise apaguem `acp_business_token.json` e isolamento da variável `ELECTRON_RUN_AS_NODE=1`).
   - [Aprovação de planos A/B/C, feedback de revisão inline e resiliência de composer no Native Chat](../issues/aprovacao-de-planos-abc-feedback-de-revisao-inline-e-resiliencia-de-composer-no-chat.md):
     adicionados o PR `#42907` (Issues `#22316` e `#42609` — renderização de sugestão do próximo prompt do Claude como ghost text no composer vazio, aceita com <kbd>Tab</kbd> ou <kbd>→</kbd>)
     e o PR `#42895` (suporte completo ao Hermes Agent no Native Chat via servidor ACP com cartões de aprovação de edições e comandos).
   - [Workers de plugins em hosts remotos e gerenciamento CLI de SSH](../issues/workers-de-plugins-em-hosts-remotos-e-gerenciamento-cli-de-ssh.md):
     adicionado o PR `#42898` (resolve Issue `#37826` — comando `orca host add` na CLI para cadastro explícito e persistente de alvos SSH com retorno de seletor `--host ssh:<id>`).
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionados o PR `#42877` (exclusão segura e opt-in de histórico, rollouts do Codex e transcrições de agentes ao deletar workspaces)
     e o PR `#42905` / Issue `#42909` (reorganização visual de regras em seções manuais e automáticas e declaração de pastas regeneráveis em `orca.yaml`).
   - [Consumo de recursos em agentes: reaper de LSP e overhead de hooks](../issues/consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks.md):
     adicionados o PR `#42889` (resolve Issue `#42601` — remoção profunda e atômica de hooks, scripts, binários da PATH e serviços em background via `orca uninstall` e *Settings › Advanced*)
     e o PR `#42890` (política de aprovação única *Always trust* para comandos de setup em `orca.yaml` por repositório).
   - [Servidor MCP stdio na CLI, métricas com orca stats usage e automação de documentação](../issues/servidor-mcp-stdio-na-cli-e-otimizacoes-de-captura-no-computer-use.md):
     adicionado o PR `#42812` (resolve Issue `#41618` — subcomando `orca stats usage` e RPC `stats.usage` para consumo direto e conciso de métricas agregadas de tokens e custos estimados por modelo e projeto).
