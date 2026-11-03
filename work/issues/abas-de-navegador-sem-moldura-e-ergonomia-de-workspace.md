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

Rastreado dos PRs abertos no upstream [`stablyai/orca#37708`](https://github.com/stablyai/orca/pull/37708),
[`stablyai/orca#37810`](https://github.com/stablyai/orca/pull/37810),
[`stablyai/orca#37803`](https://github.com/stablyai/orca/pull/37803),
[`stablyai/orca#37718`](https://github.com/stablyai/orca/pull/37718) e
[`stablyai/orca#37716`](https://github.com/stablyai/orca/pull/37716), além das issues
[`stablyai/orca#37700`](https://github.com/stablyai/orca/issues/37700),
[`stablyai/orca#37808`](https://github.com/stablyai/orca/issues/37808),
[`stablyai/orca#37784`](https://github.com/stablyai/orca/issues/37784),
[`stablyai/orca#37713`](https://github.com/stablyai/orca/issues/37713) e
[`stablyai/orca#37746`](https://github.com/stablyai/orca/issues/37746).

## O problema e as melhorias

1. **Abas de navegador ocupando espaço desnecessário no workspace (`#37700`, `#37708`):** páginas web abertas em abas
   dedicadas do workspace (como documentações ou dashboards locais) mostravam sempre a barra de ferramentas/navegação
   (URL, botões de recarga e ferramentas de inspeção), reduzindo a área útil mesmo quando a navegação interna do
   workspace já está disponível.
2. **Recolhimento e restauração de splits de navegador (`#37808`, `#37810`):** ao trabalhar com split horizontal de
   navegador ao lado de um terminal, faltava um botão para recolher temporariamente a página e ler logs na largura total
   sem desmontar a webview, preservando formulários em preenchimento e a proporção salva do split.
3. **Controle de status de workspace via teclado (`#37784`, `#37803`):** permite definir ou alterar o status de um
   workspace diretamente pela paleta de comandos (`Cmd+J` / `Ctrl+Shift+J`) sem precisar interagir com o mouse.
4. **Carregamento tardio de novas pastas de projetos (`#37713`):** uma nova pasta de projeto adicionada ao host não era
   recarregada automaticamente no painel de Projetos aberto até que o app fosse reiniciado.
5. **Ergonomia e controle da árvore de projetos e editor (`#37718`, `#37716`, `#37746`):**
   - `#37718`: adiciona comando associável a atalho para recolher ou expandir todos os projetos na barra lateral;
   - `#37716`: introduz opção opt-in de format-on-save no editor;
   - `#37746`: configuração do local de abertura da aba de Setup ao criar novo workspace.

## O que o upstream implementa

- Adiciona a flag `--chromeless` ao `orca tab create --url <url> --chromeless` e opção correspondente no menu de
  contexto da aba do navegador para exibir/ocultar a barra de navegação sem fechar a página.
- Adiciona controle de recolher/expandir split de navegador mantendo a página montada e foco no grupo adjacente.
- Registra comandos de atalho para expansão/recolhimento unificado de projetos e chaveamento de status de workspace via `Cmd+J`.

## O que fazer

Avaliar a inclusão do modo chromeless, recolhimento de splits e comandos de ergonomia do workspace em versões futuras do `brza-studio`.
