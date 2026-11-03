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
  - issue:leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins
  - issue:ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins
  - issue:melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream
  - issue:plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados
  - issue:preservar-o-dono-do-painel-do-antigravity-em-subagentes-aninhados
  - issue:subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent
---

# Radar de issues e PRs do upstream e automação de 6h

## O que foi feito

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
