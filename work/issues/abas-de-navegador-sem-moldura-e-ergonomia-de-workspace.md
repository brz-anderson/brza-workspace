---
status: open
description: O PR #37708 e as issues #37700, #37713 e #37746 do upstream trazem abas de navegador chromeless no workspace, recolhimento global de projetos e ajustes de foco no arranque.
scope:
  - brza-studio
  - workspace
priority: low
opened: 2026-11-03
tags:
  - design
  - tooling
---

# Abas de navegador sem moldura e ergonomia de workspace

Rastreado do PR aberto no upstream [`stablyai/orca#37708`](https://github.com/stablyai/orca/pull/37708) e das issues
[`stablyai/orca#37700`](https://github.com/stablyai/orca/issues/37700),
[`stablyai/orca#37713`](https://github.com/stablyai/orca/issues/37713) e
[`stablyai/orca#37746`](https://github.com/stablyai/orca/issues/37746), além dos PRs
[`stablyai/orca#37718`](https://github.com/stablyai/orca/pull/37718) e
[`stablyai/orca#37716`](https://github.com/stablyai/orca/pull/37716).

## O problema e as melhorias

1. **Abas de navegador ocupando espaço desnecessário no workspace (`#37700`, `#37708`):** páginas web abertas em abas
   dedicadas do workspace (como documentações ou dashboards locais) mostravam sempre a barra de ferramentas/navegação
   (URL, botões de recarga e ferramentas de inspeção), reduzindo a área útil mesmo quando a navegação interna do
   workspace já está disponível.
2. **Carregamento tardio de novas pastas de projetos (`#37713`):** uma nova pasta de projeto adicionada ao host não era
   recarregada automaticamente no painel de Projetos aberto até que o app fosse reiniciado.
3. **Ergonomia e controle da árvore de projetos e editor (`#37718`, `#37716`, `#37746`):**
   - `#37718`: adiciona comando associável a atalho para recolher ou expandir todos os projetos na barra lateral;
   - `#37716`: introduz opção opt-in de format-on-save no editor;
   - `#37746`: configuração do local de abertura da aba de Setup ao criar novo workspace.

## O que o upstream implementa

- Adiciona a flag `--chromeless` ao `orca tab create --url <url> --chromeless` e opção correspondente no menu de
  contexto da aba do navegador para exibir/ocultar a barra de navegação sem fechar a página.
- Registra comandos de atalho para expansão/recolhimento unificado de projetos na barra lateral.

## O que fazer

Avaliar a inclusão do modo chromeless e comandos de ergonomia do workspace em versões futuras do `brza-studio`.
