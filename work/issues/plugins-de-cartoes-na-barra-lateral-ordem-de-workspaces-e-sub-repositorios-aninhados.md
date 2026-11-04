---
status: open
description: Os PRs #38089, #38092, #38078, #38049, #37650 e as issues #38017 e #15323 trazem hierarquia de projetos na barra lateral, reorganização de boards e reapontamento de pastas.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#38089`](https://github.com/stablyai/orca/pull/38089),
[`stablyai/orca#38092`](https://github.com/stablyai/orca/pull/38092),
[`stablyai/orca#38078`](https://github.com/stablyai/orca/pull/38078),
[`stablyai/orca#38049`](https://github.com/stablyai/orca/pull/38049),
[`stablyai/orca#37650`](https://github.com/stablyai/orca/pull/37650),
[`stablyai/orca#37654`](https://github.com/stablyai/orca/pull/37654),
[`stablyai/orca#37661`](https://github.com/stablyai/orca/pull/37661),
[`stablyai/orca#37664`](https://github.com/stablyai/orca/pull/37664),
[`stablyai/orca#37696`](https://github.com/stablyai/orca/pull/37696),
[`stablyai/orca#37730`](https://github.com/stablyai/orca/pull/37730),
[`stablyai/orca#37557`](https://github.com/stablyai/orca/pull/37557) e
[`stablyai/orca#37510`](https://github.com/stablyai/orca/pull/37510), além das issues
[`stablyai/orca#38017`](https://github.com/stablyai/orca/issues/38017),
[`stablyai/orca#15323`](https://github.com/stablyai/orca/issues/15323) e
[`stablyai/orca#37761`](https://github.com/stablyai/orca/issues/37761).

## O que está entrando no upstream

1. **Clarificação visual da hierarquia da barra lateral (`#38089`, `#38017`):**
   - Introduz rótulos de grupos de projetos, blocos delimitados de projetos e ênfase visual em atividade recente,
     permitindo distinguir grupos, projetos e workspaces individuais de relance;
   - Resolve confusão visual em workspaces com muitos repositórios e branches vinculadas.
2. **Organização de listas de workspaces, boards e catálogos por proprietário (`#38092`):**
   - Agrupa listas de workspaces e boards de acompanhamento segundo seus proprietários/origens, facilitando a navegação
     multiprojeto.
3. **Reapontamento de projetos baseados em pastas movidas (`#38078`):**
   - Ao mover ou renomear uma pasta de projeto em disco, o app reaponta a entrada existente em vez de criar um projeto
     duplicado com configurações zeradas (corrige `#30807`).
4. **Supressão de resíduos de escape codes em terminais (`#38049`):**
   - Elimina sequências de escape incompletas (ex.: `"43B"`) impressas na linha de comando logo após a troca de workspace ativo.
5. **Workspace card plugins e seções na barra lateral (`#37650`, `#37654`, `#37661`, `#37664`):**
   - `sidebarCards` como ponto de contribuição declarativa de plugins (fase 2);
   - Card Studio e painel de customização de cartões (fase 3);
   - catálogo oficial de cartões e galeria de estados (fase 4);
   - organização da lista de workspaces da barra lateral em seções (fase L).
6. **Expressividade, workers em tempo real e segurança de cartões (`#37696`, `#37730`, `#37761`):**
   - renderização customizada de agentes por plugins, tempos relativos dinâmicos ("2m ago"), i18n e campos vivos;
   - travas anti-spoofing para impedir que cartões disfarcem status de agentes;
   - `#37730` preserva cor roxa para PRs mesclados em cartões e `#37761` permite ações secundárias dentro de `ListItem`.
7. **Ordem manual de workspaces ao redor do checkout primário (`#37557`):** corrige a ordenação para respeitar a posição
   manual definida pelo usuário sem forçar o checkout primário a desfazer o arranjo dos worktrees.
8. **Descoberta de sub-repositórios Git em raízes guarda-chuva (`#37510`):** ajusta detecção de repositórios filhos em
   estruturas monorepo/guarda-chuva, ignorando contêineres `.worktrees`.
9. **Ocultar worktrees sem apagar (`#15323`):** pedido de feature para recolher ou esconder worktrees inativos.

## O que fazer

- Adotar as melhorias de agrupamento e hierarquia de projetos da barra lateral (`#38089`, `#38092`) no `brza-studio`.
- Incorporar os consertos de reapontamento de pastas (`#38078`) e limpeza de escape tails (`#38049`) para estabilizar a
  ergonomia de trabalho diária nos worktrees.
