---
status: open
description: Os PRs #37650, #37654, #37661, #37664, #37557 e #37510 do upstream trazem plugins de cartões na barra lateral, ordenação manual ao redor do checkout primário e descoberta de sub-repos git.
scope:
  - brza-studio
  - workspace
priority: medium
opened: 2026-11-03
tags:
  - design
  - tooling
---

# Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados

Rastreado dos PRs abertos no upstream [`stablyai/orca#37650`](https://github.com/stablyai/orca/pull/37650),
[`stablyai/orca#37654`](https://github.com/stablyai/orca/pull/37654),
[`stablyai/orca#37661`](https://github.com/stablyai/orca/pull/37661),
[`stablyai/orca#37664`](https://github.com/stablyai/orca/pull/37664),
[`stablyai/orca#37557`](https://github.com/stablyai/orca/pull/37557) e
[`stablyai/orca#37510`](https://github.com/stablyai/orca/pull/37510), além da issue
[`stablyai/orca#15323`](https://github.com/stablyai/orca/issues/15323).

## O que está entrando no upstream

1. **Workspace card plugins e seções na barra lateral (`#37650`, `#37654`, `#37661`, `#37664`):**
   - `sidebarCards` como ponto de contribuição declarativa de plugins (fase 2);
   - Card Studio e painel de customização de cartões (fase 3);
   - catálogo oficial de cartões e galeria de estados (fase 4);
   - organização da lista de workspaces da barra lateral em seções (fase L).
2. **Ordem manual de workspaces ao redor do checkout primário (`#37557`):** corrige a ordenação para respeitar a posição
   manual definida pelo usuário sem forçar o checkout primário a desfazer o arranjo dos worktrees.
3. **Descoberta de sub-repositórios Git em raízes guarda-chuva (`#37510`):** ajusta
   `src/main/project-groups/nested-repo-discovery.ts` para achar repositórios filhos mesmo quando a raiz é um repositório
   Git cujo `.gitignore` ignora subpastas, ignorando contêineres de worktree como `.worktrees`.
4. **Ocultar worktrees sem apagar (`#15323`):** pedido de feature para recolher ou esconder worktrees inativos na árvore
   do projeto sem remover o diretório em disco.

## O que fazer

- Acompanhar o merge da série de **Workspace card plugins** (`#37650`–`#37664`) no upstream para usá-la nos cartões de
  status de planos (`PLN-*`) e workstreams do `brza-workspace` dentro do `brza-studio`.
- Avaliar o cherry-pick de `#37557` para estabilizar a ordem dos worktrees (`.worktrees/studio`, `.worktrees/tools-kit`,
  `.worktrees/workspace`, `.worktrees/brand`, `.worktrees/playground`) na barra lateral.
