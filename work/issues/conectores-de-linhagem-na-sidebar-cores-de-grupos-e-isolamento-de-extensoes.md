---
scope:
  - brza-studio
  - brza-workflow
  - workspace
description: Os PRs #42346, #42312, #42303, #42324 e #42261 trazem conectores de linhagem na sidebar, cores de grupos, rodapé de sleeping e alívio de memória em perfis.
opened: 2026-11-14
status: open
priority: high
tags:
  - design
  - tooling
  - infra
---

# Conectores de linhagem na sidebar, cores de grupos de projeto e isolamento de extensões em perfis

Rastreia melhorias de ergonomia visual na árvore de workspaces e grupos de projetos da sidebar do BrzA Studio / Orca, além de otimizações de recursos no gerenciamento de perfis de navegador inativos e estabilidade de menus de abas, introduzidas no upstream:

1. **Conectores de linhagem em árvore na sidebar para child workspaces ([PR #42312](https://github.com/stablyai/orca/pull/42312)):**
   - Adiciona guias de linhagem com conectores de galho (`├`, `╰`) e linhas verticais conectando os child workspaces diretamente ao workspace pai na sidebar.
   - Melhora significativamente o discernimento hierárquico quando múltiplos workspaces aninhados ou worktrees secundárias estão abertos simultaneamente.
2. **Cores de identificação para grupos de projetos e guias estilo thread de e-mail ([PR #42303](https://github.com/stablyai/orca/pull/42303)):**
   - Introduz suporte a `Group color` configurável para pastas e projetos na barra lateral.
   - Aplica linhas verticais coloridas de agrupamento contínuo (no estilo visual de citações/threads de e-mail), unificando visualmente todos os workspaces e itens pertencentes ao mesmo grupo de projeto.
3. **Suspensão de extensões em background para perfis inativos de navegador ([PR #42324](https://github.com/stablyai/orca/pull/42324) — resolve [Issue #41906](https://github.com/stablyai/orca/issues/41906)):**
   - Evita que perfis de navegador inativos (não renderizados ou sem janelas ativas) continuem executando workers de extensões, timers e alarmes em background.
   - Elimina um consumo ocioso crônico de 2 a 4 GB de memória RAM gerado por extensões rodando desnecessariamente em perfis adormecidos.
4. **Fixação e estabilidade de menus de contexto durante o fechamento de abas na sidebar ([PR #42261](https://github.com/stablyai/orca/pull/42261)):**
   - Garante que o menu popover ou contexto de opções de uma aba/worktree permaneça na posição correta e funcional mesmo se outra aba for fechada concorrentemente na lista da sidebar.
5. **Rodapé expansível de workspaces adormecidos na sidebar ([PR #42346](https://github.com/stablyai/orca/pull/42346) — resolve [Issue #42345](https://github.com/stablyai/orca/issues/42345)):**
   - Quando o filtro "Hide sleeping" estiver ativado, exibe uma linha de rodapé discreta `Sleeping (N)` ao final da lista de workspaces.
   - Ao expandir o rodapé, o usuário pode clicar diretamente em qualquer workspace adormecido para acordá-lo e torná-lo ativo, sem precisar desativar e reativar o filtro global na barra lateral.

## Impacto no BrzA Studio

- **Visual e Hierarquia:** A navegação por workspaces complexos, monorepos e worktrees paralelas fica muito mais limpa e intuitiva com conectores visuais explícitos, identificação colorida por projeto e acesso direto a workspaces adormecidos sem perder a filtragem limpa.
- **Eficiência de Recursos:** Perfis de navegação isolados (usados pelo studio e automações web) não drenam mais memória da máquina quando colocados em segundo plano.
- **Polimento de UI:** Elimina pequenos saltos ou fechamentos involuntários de menus de abas durante operações rápidas de limpeza de workspaces.
