---
status: open
description: A issue #37674 e o PR #37685 do upstream removem allow-dyld-environment-variables dos entitlements no macOS, fortalecendo o Hardened Runtime do app empacotado.
scope:
  - brza-studio
priority: medium
opened: 2026-11-03
tags:
  - tooling
---

# Segurança no macOS: remoção de allow-dyld-environment-variables dos entitlements

Rastreado da issue aberta no upstream [`stablyai/orca#37674`](https://github.com/stablyai/orca/issues/37674) e do PR
[`stablyai/orca#37685`](https://github.com/stablyai/orca/pull/37685).

## O problema

O build de distribuição macOS (1.4.246) do upstream e do `brza-studio` é assinado com Hardened Runtime, mas incluía em
`resources/build/entitlements.mac.plist` a permissão:

- `com.apple.security.cs.allow-dyld-environment-variables`

Essa permissão permite que variáveis de ambiente como `DYLD_INSERT_LIBRARIES` injetem bibliotecas em tempo de carga no
processo principal. Ferramentas de segurança corporativa tratam esse entitlement como enfraquecimento do Hardened
Runtime e consideram o aplicativo um launcher não verificado, bloqueando políticas de conformidade. Nenhuma parte do
código do app consome ou necessita de variáveis `DYLD_*`.

## O que o upstream faz

- **No PR `#37685`:** remove `com.apple.security.cs.allow-dyld-environment-variables` do arquivo
  `resources/build/entitlements.mac.plist`.
- Mantém `allow-jit` (necessário para o terminal host baseado em Node em `config/scripts/macos-terminal-host-bundle.cjs`)
  e preserva `allow-unsigned-executable-memory` para testes subsequentes.

## O que fazer

Aplicar a mesma remoção em `resources/build/entitlements.mac.plist` no repositório do `brza-studio`, assegurando que a
assinatura dos próximos releases não carregue o entitlement enfraquecido.
