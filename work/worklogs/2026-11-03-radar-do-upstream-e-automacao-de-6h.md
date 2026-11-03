---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-03
completed: 2026-11-03
tags:
  - tooling
refs:
  - issue:abas-de-navegador-sem-moldura-e-ergonomia-de-workspace
  - issue:abertura-de-agentes-no-chat-ui-pela-cli-e-superficie-chat-na-orquestracao
  - issue:adaptadores-acp-customizados-e-isolamento-de-permissoes-de-sessao
  - issue:gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache
  - issue:isolamento-de-sessoes-de-titulacao-acp-e-status-de-conclusao-de-workers
  - issue:leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins
  - issue:ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins
  - issue:melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream
  - issue:plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados
  - issue:preservar-o-dono-do-painel-do-antigravity-em-subagentes-aninhados
  - issue:repositorios-vinculados-no-source-control-e-escopo-de-worktree-na-cli
  - issue:seguranca-macos-remocao-de-allow-dyld-environment-variables-dos-entitlements
  - issue:subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent
  - issue:workers-de-plugins-em-hosts-remotos-e-gerenciamento-cli-de-ssh
---

# Radar de issues e PRs do upstream e automação de 6h

## O que foi feito

### 1. Varredura inicial e configuração (03:00 BRT)

1. **Varredura de issues e PRs abertos em `stablyai/orca`:** consultadas 530 issues e PRs abertos nas categorias
   `workflow`, `workspace`, `studio`, `cli`, `skills` e `ferramental` via API do GitHub (`gh api search/issues`).
2. **Criação de 6 issues priorizadas em `work/issues/`** (commit `d8100ec` em `workstream/playground` e registradas no
   `.brza/index.jsonl` da `master`):
   - `priority: high` — [Preservar o dono do painel do Antigravity em subagentes aninhados](../issues/preservar-o-dono-do-painel-do-antigravity-em-subagentes-aninhados.md) (`#37507`, `#37505`)
   - `priority: high` — [Leitura antecipada e preservação de skills no arranque e nos plugins](../issues/leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins.md) (`#35220`, `#36897`, `#19680`)
   - `priority: high` — [Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](../issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md) (`#33114`, `#37615`, `#37467`)
   - `priority: medium` — [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md) (`#37574`, `#33403`, `#37407`, `#37637`)
   - `priority: medium` — [Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados](../issues/plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados.md) (`#37650`–`#37664`, `#37557`, `#37510`)
   - `priority: low` — [Melhorias de Native Chat, ACP do Gemini CLI, abas e diff no upstream](../issues/melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream.md) (`#33360`, `#37480`, `#37532`, `#37494`, `#37503`)
3. **Loop de 6h em `Automações` do BrzA Studio:** criada a automação `Radar do upstream (stablyai/orca)`
   (`f75b8281-8ae3-4558-afe4-7ab5bbc35601`) com cron `0 */6 * * *` (00:00, 06:00, 12:00, 18:00 em `America/Sao_Paulo`),
   `provider: antigravity`, `surface: chat`, `workspaceMode: existing` apontando para `.worktrees/playground` e
   `reuseSession: true`.

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisadas 42 issues e dezenas de PRs criados ou
   atualizados desde `2026-11-03T03:00:00Z`.
2. **Atualização de 3 issues existentes em `work/issues/`:**
   - [Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados](../issues/plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados.md):
     adicionados PR `#37696` (fase 4 / expressividade, i18n, timestamps dinâmicos e spoofing guards), PR `#37730` e issue `#37761`;
   - [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md):
     adicionadas issues `#37741` ("Work together..." / conexão entre chats), `#37702` (fechamento de worker transferido),
     `#37693` (permissões Full access em reabertura), `#37731` (entrega a workers Hermes), `#37683` / `#37684` (filtros e host reads de Runs)
     e PR `#37703` (identidade de agente retida);
   - [Leitura antecipada e preservação de skills no arranque e nos plugins](../issues/leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins.md):
     adicionado PR `#37659` (renomeação de `computer use` para `orca-computer-use` para isolamento de namespace).
3. **Criação de 3 novas issues priorizadas em `work/issues/`:**
   - `priority: high` — [Abertura de agentes no Chat UI pela CLI e superfície chat na orquestração](../issues/abertura-de-agentes-no-chat-ui-pela-cli-e-superficie-chat-na-orquestracao.md) (`#37710`, `#37701`, `#37707`, `#37733`);
   - `priority: medium` — [Segurança no macOS: remoção de allow-dyld-environment-variables dos entitlements](../issues/seguranca-macos-remocao-de-allow-dyld-environment-variables-dos-entitlements.md) (`#37674`, `#37685`);
   - `priority: low` — [Abas de navegador sem moldura e ergonomia de workspace](../issues/abas-de-navegador-sem-moldura-e-ergonomia-de-workspace.md) (`#37708`, `#37700`, `#37718`, `#37716`, `#37713`, `#37746`).

### 3. Ciclo de 6h (12:00 BRT / 15:00 UTC)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisadas 27 novas issues e 25 novos PRs criados
   ou atualizados desde `2026-11-03T09:00:00Z`.
2. **Atualização de 2 issues existentes em `work/issues/`:**
   - [Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](../issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md):
     adicionadas issues `#37801` (comando CLI para focar/abrir chat específico e sincronização de seleção na barra lateral)
     e `#37807` (inclusão de native chats na Jump Palette), além dos PRs `#37774` (isolamento de drafts) e `#37802` (escrita de journal em background);
   - [Abas de navegador sem moldura e ergonomia de workspace](../issues/abas-de-navegador-sem-moldura-e-ergonomia-de-workspace.md):
     adicionados PR `#37810` / issue `#37808` (recolhimento e restauração de splits de navegador) e issue `#37784` / PR `#37803`
     (chaveamento de status de workspace via `Cmd+J`).
3. **Criação de 3 novas issues priorizadas em `work/issues/`:**
   - `priority: high` — [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md) (`#37833`, `#37567`, `#37568`, `#37569`);
   - `priority: high` — [Isolamento de sessões de titulação ACP e status de conclusão de workers](../issues/isolamento-de-sessoes-de-titulacao-acp-e-status-de-conclusao-de-workers.md) (`#37832`, `#37063`, `#37781`, `#37815`);
   - `priority: medium` — [Workers de plugins em hosts remotos e gerenciamento CLI de SSH](../issues/workers-de-plugins-em-hosts-remotos-e-gerenciamento-cli-de-ssh.md) (`#37788`, `#37826`, `#37806`).

### 4. Ciclo de 6h (18:00 BRT / 21:00 UTC)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisadas 32 novas issues e 25 novos PRs criados
   ou atualizados desde `2026-11-03T15:00:00Z`.
2. **Atualização de 2 issues existentes em `work/issues/`:**
   - [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md):
     adicionados PR `#37868` / issue `#37867` (espera agendada `--wait-until` e supressão de alertas falsos de parada ociosa),
     PR `#37866` / issue `#37865` (preservação de tail de saída de workers que morrem no arranque), PR `#37891` (mensagens
     de orquestração limpas sem envelope nem boilerplate) e PR `#37850` / issue `#37849` (desduplicação de stub da skill);
   - [Leitura antecipada e preservação de skills no arranque e nos plugins](../issues/leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins.md):
     adicionadas issues `#37875` e `#32573` (suporte a pontos de contribuição `skills` e `subagents` em plugins de terceiros).
3. **Criação de 2 novas issues priorizadas em `work/issues/`:**
   - `priority: high` — [Adaptadores ACP customizados e isolamento de permissões de sessão](../issues/adaptadores-acp-customizados-e-isolamento-de-permissoes-de-sessao.md) (`#37842`, `#37895`, `#37889`, `#37861`, `#37859`, `#37862`, `#37883`);
   - `priority: high` — [Repositórios vinculados no Source Control e escopo de worktree na CLI](../issues/repositorios-vinculados-no-source-control-e-escopo-de-worktree-na-cli.md) (`#37896`, `#37892`, `#37899`, `#37838`, `#37903`).

## Fora do workspace

- **O quê e onde:** automação `Radar do upstream (stablyai/orca)` (`id: f75b8281-8ae3-4558-afe4-7ab5bbc35601`) criada
  no estado persistido do runtime do BrzA Studio (`~/Library/Application Support/brza-studio/`, via `brza automations
  create` e `automation.update` com `launchSetupPatch: { surface: "chat" }`).
- **O risco:** a cada 6h o agendador do BrzA Studio dispara um turno de Native Chat do Antigravity no worktree
  `.worktrees/playground`, consumindo tokens da conta configurada e fazendo commit/push em `workstream/playground` (e no
  índice da `master`) quando encontrar issues ou PRs novos relevantes no upstream.
- **Estado:** ativo (`enabled: true`, próxima execução em `2026-11-03T06:00:00-03:00` / `2026-11-03T09:00:00.000Z`).
- **Como desfazer:** pausar com `"/Applications/BrzA Studio.app/Contents/Resources/bin/brza" automations edit
  f75b8281-8ae3-4558-afe4-7ab5bbc35601 --disabled` ou remover com `"/Applications/BrzA Studio.app/Contents/Resources/bin/brza"
  automations remove f75b8281-8ae3-4558-afe4-7ab5bbc35601`.
