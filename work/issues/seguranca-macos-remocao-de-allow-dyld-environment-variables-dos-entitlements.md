---
status: open
description: Os PRs #42245, #42136, #37685 e as issues #37674, #38247 tratam de UUID de executável do terminal host, layout de teclado in-process e entitlements no macOS.
scope:
  - brza-studio
priority: medium
opened: 2026-11-03
tags:
  - tooling
---

# Segurança no macOS: remoção de allow-dyld-environment-variables dos entitlements e colisão de LC_UUID

<!-- pln-014-despacho -->
> **Despacho (PLN-014/R1.1):** classe `ausente` · casa `studio`
> Merge no upstream não muda `status`. PLN-014/R1, 2026-11-12.

Rastreado dos PRs abertos no upstream [`stablyai/orca#42245`](https://github.com/stablyai/orca/pull/42245),
[`stablyai/orca#42136`](https://github.com/stablyai/orca/pull/42136),
[`stablyai/orca#37685`](https://github.com/stablyai/orca/pull/37685),
além das issues [`stablyai/orca#38247`](https://github.com/stablyai/orca/issues/38247),
[`stablyai/orca#39405`](https://github.com/stablyai/orca/issues/39405) e
[`stablyai/orca#37674`](https://github.com/stablyai/orca/issues/37674).

## O problema

1. **Permissão desnecessária de injeção de bibliotecas (`#37674`, `#37685`):**
   O build de distribuição macOS (1.4.246) incluía em `resources/build/entitlements.mac.plist` a permissão
   `com.apple.security.cs.allow-dyld-environment-variables`. Essa permissão permite que variáveis como `DYLD_INSERT_LIBRARIES`
   injetem código no processo principal, sendo classificada por softwares corporativos como violação do Hardened Runtime.
2. **Bloqueio de rede local no macOS Sequoia por colisão de LC_UUID e bundle ID compartilhado (`#38247`, `#42245`):**
   No macOS 15+ (Sequoia), processos filhos gerados pelo app principal perdem acesso à rede local (Local Network) ou
   apresentam diálogos de autorização inconsistentes quando o auxiliar `Terminal Host` é uma cópia genérica do binário Node
   compartilhando o mesmo identificador de executável de outros aplicativos do sistema.
3. **Proliferação de processos e vazamento de portas Mach por checagem externa de layout de teclado (`#42136`, resolve `#39405`):**
   A cada ganho de foco da janela e a cada troca de fonte de entrada no macOS, o aplicativo disparava um novo processo auxiliar
   `orca-keyboard-layout`. Em sessões ativas com frequente alternância de janelas, centenas de processos eram gerados, acumulando
   portas Mach no `WindowServer` e degradando a responsividade gráfica do sistema.

## O que o upstream faz e propõe

- **No PR `#37685`:** remove `com.apple.security.cs.allow-dyld-environment-variables` do arquivo
  `resources/build/entitlements.mac.plist`.
- Mantém `allow-jit` (necessário para o terminal host baseado em Node em `config/scripts/macos-terminal-host-bundle.cjs`)
  e preserva `allow-unsigned-executable-memory` para testes subsequentes.
- **UUID dedicado de executável para o Terminal Host (`#42245`, resolve `#38247`):**
  - Assina o binário do terminal host no macOS com seu próprio UUID e identidade de executável isolada;
  - Assegura que o sistema operacional conceda e retenha permissões de Local Network de forma independente, permitindo que servidores locais de desenvolvimento (`localhost:3000`) funcionem estavelmente nos terminais.
- **Leitura in-process do layout de teclado no macOS (`#42136`, resolve `#39405`):**
  - Migra a consulta de layout de teclado para chamada nativa in-process via APIs do sistema operacional;
  - Elimina o disparo contínuo do executável auxiliar `orca-keyboard-layout`, estancando o crescimento de portas Mach e economizando ciclos de CPU em cada foco de janela.

## O que fazer

- Aplicar a remoção de `com.apple.security.cs.allow-dyld-environment-variables` em `resources/build/entitlements.mac.plist`.
- Garantir UUID e identidade de executável dedicada para o Terminal Host no macOS (`#42245`), estabilizando permissões de Local Network no macOS Sequoia.
- Adotar a leitura nativa in-process do layout de teclado no macOS (`#42136`), eliminando processos `orca-keyboard-layout` a cada foco.
