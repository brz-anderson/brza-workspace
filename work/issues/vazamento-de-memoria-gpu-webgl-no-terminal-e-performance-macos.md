---
status: open
description: O PR #38120 e as issues #38108 e #38150 do upstream corrigem vazamento crítico de 20+ GB de memória GPU no terminal WebGL no macOS e travamentos na thread principal.
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

Rastreado do PR aberto no upstream [`stablyai/orca#38120`](https://github.com/stablyai/orca/pull/38120) (Issue
[`#38108`](https://github.com/stablyai/orca/issues/38108)), além das issues
[`#38150`](https://github.com/stablyai/orca/issues/38150) e
[`#38096`](https://github.com/stablyai/orca/issues/38096) (PR [`#38098`](https://github.com/stablyai/orca/pull/38098)).

## O problema

1. **Vazamento de mais de 20 GB de memória GPU no Apple Silicon (`#38120`, `#38108`):** ao rodar sessões interativas de
   terminal com fontes Nerd Font, caracteres CJK e saída TUI colorida (como Claude Code, Antigravity CLI e dashboards de
   monitoramento), o processo `Orca Helper (GPU)` acumulava dezenas de gigabytes de memória `IOAccelerator (graphics)`.
   O `@xterm/addon-webgl` permitia que texturas de glifos se fundissem até 16.384 × 16.384 pixels (consumindo 1,33 GiB de
   VRAM por textura), e quando as páginas eram limpas ou mescladas, as texturas antigas não eram liberadas na GPU.
2. **Conflito de cache de atlas entre camadas de renderização (`#38120`):** `BaseRenderLayer` usava tamanho máximo de
   textura de 2.048, enquanto `WebglRenderer` passava 16.384, forçando ambos a invalidarem continuamente o cache compartilhado
   `charAtlasCache` a cada redimensionamento da janela (`handleResize`).
3. **Bloqueio da thread principal em acessos a arquivos com prompts do sistema pendentes (`#38150`):** no macOS, se outro
   aplicativo estiver exibindo um modal de permissões de privacidade do sistema, operações síncronas de I/O de arquivos na
   thread principal do app bloqueiam a interface gráfica inteira até a dispensa do prompt.

## O que o upstream propõe e implementa

- **Limitação de textura e retração imediata de slots de GPU (`#38120`):**
  - Limita o tamanho máximo de páginas de atlas WebGL a 2.048 × 2.048 pixels (~21 MiB por página, alinhado com `BaseRenderLayer`);
  - Implementa `shrinkClearedWebglAtlasTextures` e `boundXtermWebglAtlasMemory`: reduz slots de textura não utilizados para
    1 × 1 pixels imediatamente após fusão, limpeza ou ocultação de abas;
  - Zera largura e altura de canvases 2D removidos do atlas, liberando memória de buffers imediatamente;
  - Elimina o vazamento de 20+ GB no Apple Silicon sem exigir rebuild das patches compiladas do xterm.
- **Abertura direta via Finder no macOS (`#38098`, `#38096`):**
  - Registra tratadores de tipos de arquivos de texto e código para permitir abrir arquivos e repositórios diretamente pelo
    Finder no macOS.

## O que fazer

Portar com urgência o módulo `terminal-webgl-atlas-memory.ts` e o PR `#38120` para o `brza-studio`, protegendo o consumo
de GPU e memória unificada no macOS durante longas sessões de desenvolvimento com múltiplos terminais de agentes.
