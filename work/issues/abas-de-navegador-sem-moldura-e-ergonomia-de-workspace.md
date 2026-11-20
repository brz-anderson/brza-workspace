---
status: open
description: Os PRs #44742 e #44598 trazem diagnóstico de páginas travadas no navegador e notificação de Memory Saver para abas inativas.
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

<!-- pln-014-despacho -->
> **Despacho (PLN-014/R1.1):** classe `ausente` · casa `studio`
> Merge no upstream não muda `status`. PLN-014/R1, 2026-11-12.

Rastreado dos PRs abertos no upstream [`stablyai/orca#44742`](https://github.com/stablyai/orca/pull/44742),
[`stablyai/orca#44598`](https://github.com/stablyai/orca/pull/44598),
[`stablyai/orca#44744`](https://github.com/stablyai/orca/pull/44744),
[`stablyai/orca#44428`](https://github.com/stablyai/orca/pull/44428),
[`stablyai/orca#37708`](https://github.com/stablyai/orca/pull/37708),
[`stablyai/orca#37810`](https://github.com/stablyai/orca/pull/37810),
[`stablyai/orca#37803`](https://github.com/stablyai/orca/pull/37803),
[`stablyai/orca#37718`](https://github.com/stablyai/orca/pull/37718) e
[`stablyai/orca#37716 (MERGED no upstream; não está no fork)`](https://github.com/stablyai/orca/pull/37716), além das issues
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
5. **Ergonomia e controle da árvore de projetos e editor (`#37718`, `#37716 (MERGED no upstream; não está no fork)`, `#37746`):**
   - `#37718`: adiciona comando associável a atalho para recolher ou expandir todos os projetos na barra lateral;
   - `#37716 (MERGED no upstream; não está no fork)`: introduz opção opt-in de format-on-save no editor;
   - `#37746`: configuração do local de abertura da aba de Setup ao criar novo workspace.
6. **Vazamento de `webRequest` listeners e perda de título/favicon baselines em abas hibernadas (`#44428`):**
   Múltiplos componentes registravam listeners de requisições web (`webRequest`) de forma concorrente em sessões de navegador sem proprietário único, gerando vazamento de memória e listeners duplicados. Além disso, quando o Memory Saver descartava ou hibernava abas em segundo plano, os baselines de título e favicon da página eram perdidos entre trocas de contexto.
7. **Impossibilidade de aplicar zoom em páginas de navegador remoto transmitidas por stream (`#44744`):**
   Ao visualizar abas de navegador hospedadas em servidores remotos ou headless via screencast, gestos de pinça (*pinch*), rolagem com `Ctrl+scroll` ou atalhos de teclado de zoom (`Cmd/Ctrl+=`, `Cmd/Ctrl+-`, `Cmd/Ctrl+0`) não tinham efeito na página remota ou causavam descalibração na posição de cliques e ponteiros do mouse.
8. **Ausência de diagnóstico e feedback visual quando o carregamento de páginas web trava (`#44742`):**
   Quando uma página web aberta no navegador embutido demorava para responder ou travava durante o carregamento, a interface exibia apenas um spinner genérico sem explicar a causa raiz (ex.: contenção no pool de 6 conexões simultâneas do Chromium, lentidão de DNS/TLS ou bloqueio por política).
9. **Desperdício de memória RAM por abas inativas de navegador esquecidas em segundo plano (`#44598`):**
   Usuários acumulavam dezenas de abas de documentação ou preview abertas em segundo plano consumindo gigabytes de memória, sem que o Studio notificasse proativamente sobre a economia obtida ao ligar o Memory Saver.

## O que o upstream implementa

- **Diagnóstico e watchdog de travamento no carregamento de páginas web (`#44742`):**
  - Implementa `browser-navigation-stall-watchdog`, monitorando carregamentos estagnados por mais de 10 segundos;
  - Exibe na barra de status a razão real da retenção ("Waiting for <host>…") e quantas outras abas compartilham o mesmo host em segundo plano, registrando os eventos no trace de performance para auditoria.
- **Notificações de desempenho com sugestão proativa do Memory Saver (`#44598`):**
  - Monitora abas inativas do navegador que permanecem carregadas em memória;
  - Dispara notificação discreta (*toast*) informando quantas abas e há quanto tempo estão sem uso, oferecendo ativar o Memory Saver com um único clique.
- **Controle de zoom em páginas de navegador remoto com ajuste de geometria de toque/ponteiro (`#44744`):**
  - Implementa `useRemoteBrowserPageZoom`, interceptando atalhos `Cmd+=`/`Cmd+-`/`Cmd+0`, `Ctrl+wheel` e gestos de pinça no viewport transmitido;
  - Despacha o nível de zoom via comando RPC (`browser.zoom`) para a instância remota e propaga a escala nos frames de screencast, mapeando coordenadas de clique e toque com precisão tanto no desktop quanto no mobile.
- **Proprietário único para listeners de requisição e persistência de baselines de título/favicon (`#44428`):**
  - Centraliza a instalação de listeners de requisições web (`webRequest`) nas sessões de navegador em um único proprietário gerenciado, evitando vazamentos e execuções duplicadas;
  - Preserva os baselines de título e favicon das páginas entre atualizações e ciclos de hibernação pelo Memory Saver.
- Adiciona a flag `--chromeless` ao `orca tab create --url <url> --chromeless` e opção correspondente no menu de
  contexto da aba do navegador para exibir/ocultar a barra de navegação sem fechar a página.
- Adiciona controle de recolher/expandir split de navegador mantendo a página montada e foco no grupo adjacente.
- Registra comandos de atalho para expansão/recolhimento unificado de projetos e chaveamento de status de workspace via `Cmd+J`.

## O que fazer

- Adotar o watchdog de carregamento travado no navegador com diagnóstico visual e registro em trace (`#44742`).
- Incorporar notificações de desempenho sugerindo ativar o Memory Saver quando abas inativas acumularem memória RAM em excesso (`#44598`).
- Suportar zoom em abas de navegador remoto via Ctrl+scroll, pinch e atalhos de teclado com mapeamento de coordenadas (`#44744`).
- Centralizar a instalação de listeners de requisições de navegador em proprietário único e preservar baselines de título/favicon durante a hibernação de abas pelo Memory Saver (`#44428`).
- Avaliar a inclusão do modo chromeless, recolhimento de splits e comandos de ergonomia do workspace em versões futuras do `brza-studio`.
