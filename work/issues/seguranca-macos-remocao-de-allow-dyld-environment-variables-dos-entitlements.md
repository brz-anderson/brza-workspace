---
status: open
description: As issues #37674 e #38247 e o PR #37685 tratam de fortalecimento de entitlements e isolamento de LC_UUID e bundle ID no macOS contra bloqueios de rede local.
scope:
  - brza-studio
priority: medium
opened: 2026-11-03
tags:
  - tooling
---

# Segurança no macOS: remoção de allow-dyld-environment-variables dos entitlements e colisão de LC_UUID

Rastreado das issues abertas no upstream [`stablyai/orca#37674`](https://github.com/stablyai/orca/issues/37674) e
[`stablyai/orca#38247`](https://github.com/stablyai/orca/issues/38247), além do PR
[`stablyai/orca#37685`](https://github.com/stablyai/orca/pull/37685).

## O problema

1. **Permissão desnecessária de injeção de bibliotecas (`#37674`, `#37685`):**
   O build de distribuição macOS (1.4.246) incluía em `resources/build/entitlements.mac.plist` a permissão
   `com.apple.security.cs.allow-dyld-environment-variables`. Essa permissão permite que variáveis como `DYLD_INSERT_LIBRARIES`
   injetem código no processo principal, sendo classificada por softwares corporativos como violação do Hardened Runtime.
2. **Bloqueio de rede local no macOS Sequoia por colisão de LC_UUID e bundle ID compartilhado (`#38247`):**
   No macOS 15+ (Sequoia), processos filhos gerados pelo app principal perdem acesso à rede local (Local Network) ou
   apresentam diálogos de autorização inconsistentes quando o `LC_UUID` do executável compilado coincide com outro app
   Electron ou quando o auxiliar `Terminal Host` reutiliza o mesmo bundle ID do executável principal sem entitlements de
   rede próprios, gerando bloqueios silenciosos de portas em dev servers locais (ex.: `localhost:3000`).

## O que o upstream faz e propõe

- **No PR `#37685`:** remove `com.apple.security.cs.allow-dyld-environment-variables` do arquivo
  `resources/build/entitlements.mac.plist`.
- Mantém `allow-jit` (necessário para o terminal host baseado em Node em `config/scripts/macos-terminal-host-bundle.cjs`)
  e preserva `allow-unsigned-executable-memory` para testes subsequentes.
- **Na issue `#38247`:** recomenda separar o bundle identifier do `Orca Terminal Host` (ex.: `.helper` ou `.terminal-host`),
  assegurar flags de build que forcem `LC_UUID` único por release e adicionar o entitlement explícito para redes locais
  se necessário para subprocessos spawned.

## O que fazer

- Aplicar a remoção de `com.apple.security.cs.allow-dyld-environment-variables` em `resources/build/entitlements.mac.plist`.
- Revisar a configuração de empacotamento do `brza-studio` no macOS para garantir bundle ID isolado e entitlement correto
  para o terminal host, evitando bloqueios de rede local no macOS Sequoia.
