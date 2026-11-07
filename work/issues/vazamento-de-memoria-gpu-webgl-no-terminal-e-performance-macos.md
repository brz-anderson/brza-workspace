---
status: open
description: Os PRs #39465, #39445, #38861, #38857 e #38120 corrigem vazamento de portas Mach no macOS, sobrecarga de ps, alto consumo de CPU/GPU em terminais e atlas WebGL.
scope:
  - brza-studio
  - tooling
priority: high
opened: 2026-11-04
tags:
  - tooling
  - infra
---

# Vazamento de memória GPU WebGL no terminal e performance no macOS

Rastreado dos PRs abertos no upstream [`stablyai/orca#39465`](https://github.com/stablyai/orca/pull/39465) (Issue [`#39405`](https://github.com/stablyai/orca/issues/39405)),
[`stablyai/orca#39445`](https://github.com/stablyai/orca/pull/39445),
[`stablyai/orca#38861`](https://github.com/stablyai/orca/pull/38861) (Issue
[`stablyai/orca#38860`](https://github.com/stablyai/orca/issues/38860)),
[`stablyai/orca#38857`](https://github.com/stablyai/orca/pull/38857) (Issue
[`stablyai/orca#38856`](https://github.com/stablyai/orca/issues/38856)),
[`stablyai/orca#38858`](https://github.com/stablyai/orca/pull/38858),
[`stablyai/orca#38859`](https://github.com/stablyai/orca/pull/38859),
[`stablyai/orca#38120`](https://github.com/stablyai/orca/pull/38120) (Issue
[`stablyai/orca#38108`](https://github.com/stablyai/orca/issues/38108)), além das issues
[`stablyai/orca#38150`](https://github.com/stablyai/orca/issues/38150) e
[`stablyai/orca#38096`](https://github.com/stablyai/orca/issues/38096) (PR [`stablyai/orca#38098`](https://github.com/stablyai/orca/pull/38098)).

## O problema

1. **Renderização invisível e alto consumo de CPU/GPU de terminais ocultos sob chats nativos (`#38861`, `#38860`):**
   Quando uma aba de Native Chat cobre uma pane de terminal, o xterm/WebGL continuava executando loops de redesenho a 60fps
   em background, consumindo ciclos massivos de GPU/CPU, processando rajadas TUI sem coalescência e mantendo WebViews quentes
   ilimitadas na memória.
2. **Painel de terminal em branco por dessincronização do glyph-atlas WebGL (`#38857`, `#38856`):**
   Ao alternar entre abas pausadas ou estacionadas (*parked tabs*), o atlas de texturas de glifos do `@xterm/addon-webgl`
   perdia sincronia de versão com a pane renderizada, fazendo com que o terminal reaparecesse completamente vazio ou com
   caracteres invisíveis até um redimensionamento forçado.
3. **Rajadas de redimensionamento e storm de sinais SIGWINCH redundantes (`#38858`):**
   Redimensionamentos contínuos de janelas e rotações emitiam múltiplos sinais SIGWINCH em rajada sem debouncing, causando
   redesenhos redundantes e travamentos momentâneos nos processos PTY acoplados.
4. **Vazamento de mais de 20 GB de memória GPU no Apple Silicon (`#38120`, `#38108`):** ao rodar sessões interativas de
   terminal com fontes Nerd Font, caracteres CJK e saída TUI colorida, o processo `Orca Helper (GPU)` acumulava dezenas
   de gigabytes de memória `IOAccelerator (graphics)` por não liberar texturas de glifos antigas na GPU.
5. **Conflito de cache de atlas entre camadas de renderização (`#38120`):** `BaseRenderLayer` usava tamanho máximo de
   textura de 2.048, enquanto `WebglRenderer` passava 16.384, forçando ambos a invalidarem continuamente o cache compartilhado
   `charAtlasCache` a cada redimensionamento da janela (`handleResize`).
6. **Bloqueio da thread principal em acessos a arquivos com prompts do sistema pendentes (`#38150`):** no macOS, se outro
   aplicativo estiver exibindo um modal de permissões de privacidade do sistema, operações síncronas de I/O de arquivos na
   thread principal do app bloqueiam a interface gráfica inteira até a dispensa do prompt.
7. **Spawns contínuos de helper de teclado e vazamento de portas Mach no WindowServer (`#39465`, `#39405`):**
   A cada vez que uma janela recebia foco no macOS, o app disparava um subprocesso `orca-keyboard-layout` para consultar
   o layout ativo. Cada execução efêmera estabelecia conexão com o WindowServer e vazava portas Mach no sistema operacional,
   causando crescimento contínuo de portas e desperdício de CPU.
8. **Invocação de subshells desnecessárias para comando `ps` no Resource Manager (`#39445`):**
   O monitor de recursos invocava um shell intermediário (`/bin/sh -c ps ...`) a cada ciclo de polling para inspecionar
   processos de terminais, gerando criação e destruição contínua de processos no host.

## O que o upstream propõe e implementa

- **Cache de layout de teclado no macOS e invalidação por TIS notification (`#39465`):**
  - Armazena em cache no processo principal o último snapshot de layout obtido com sucesso;
  - Descarta o cache e incrementa a época somente quando o sistema emitir `com.apple.Carbon.TISNotifySelectedKeyboardInputSourceChanged`,
    eliminando execuções redundantes de `orca-keyboard-layout` em eventos de foco de janela.
- **Execução direta de `ps` sem shell intermediário (`#39445`):**
  - Invoca o binário `ps` diretamente via `execFile` com argumentos estruturados, eliminando a sobrecarga de subshells.
- **Suspensão de renderização oculta e coalescência de streaming de terminais (`#38861`):**
  - Trata panes de terminal sob coberturas de Native Chat como estritamente ocultas para visibilidade PTY e WebGL;
  - Retém quadros sincronizados DEC `?2026` cross-platform e agrupa rajadas de saída foreground não atendidas (`scheduleDrain(0)`
    acima de 4 KiB / 500ms);
  - Pausa loops `requestAnimationFrame` e timers de animação enquanto em segundo plano (`document.hidden`);
  - Limita caches de abas quentes (*warm tab caches*) a 3 abas / 2 worktrees no desktop e 3 handles LRU no mobile.
- **Detecção e recuperação automática de desync de glyph-atlas (`#38857`):**
  - Detecta a perda de sincronia de versão do atlas WebGL ao reexibir o painel de terminal e reinicializa a textura sem
    necessidade de recarregar a sessão ou fechar o terminal.
- **Supressão de redraws SIGWINCH e contenção dinâmica de redimensionamento (`#38858`):**
  - Contém rajadas de streaming durante redimensionamentos de terminal, suprimindo redesenhos duplicados.
- **Consistência de temas Light/Dark entre terminais, chat e WebViews (`#38859`):**
  - Encaminha cores ativas de fundo e primeiro plano para queries de cores PTY (`OSC 10/11`, `CSI ?996n`), garantindo que
    sessões em modo claro não renderizem fundos pretos indesejados.
- **Limitação de textura e retração imediata de slots de GPU (`#38120`):**
  - Limita o tamanho máximo de páginas de atlas WebGL a 2.048 × 2.048 pixels (~21 MiB por página);
  - Implementa `shrinkClearedWebglAtlasTextures` e `boundXtermWebglAtlasMemory`: reduz slots de textura não utilizados para
    1 × 1 pixels imediatamente após fusão, limpeza ou ocultação de abas;
  - Zera largura e altura de canvases 2D removidos do atlas, liberando memória de buffers imediatamente.

## O que fazer

- Portar as melhorias de `terminal-hidden-view-parking.ts`, contenção de DEC `?2026` e recuperação de atlas WebGL do PR `#38861`
  e `#38857` para o `brza-studio`, protegendo o consumo de CPU e GPU durante sessões simultâneas de chat e terminais de agentes.
- Adotar o cache do snapshot de layout de teclado com invalidação TIS (`#39465`) para estancar vazamentos de portas Mach no macOS.
- Utilizar a execução direta de `ps` sem shell intermediário no monitor de recursos (`#39445`).
