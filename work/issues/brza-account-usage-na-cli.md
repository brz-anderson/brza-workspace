---
status: open
description: O brza-studio ganha brza account usage, que imprime o uso dos limites por conta, pelo porte do #37467 do upstream.
scope:
  - brza-studio
priority: low
opened: 2026-11-03
tags:
  - tooling
---

# O `brza account usage` mostra o uso dos limites por conta

Frente `low` da issue de origem
[Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md),
do `playground`. Conduzida pelo
[PLN-011: Os chats do BrzA Studio se coordenam pela CLI, aparecem na navegação e chegam aos plugins](../../plans/PLN-011-chats-pela-cli-e-plugins/PLN-011-plan.md),
na fase dela.

## O recorte

Portar `src/cli/handlers/account-usage-command.ts` e `src/cli/handlers/account-usage-format.ts`, com os testes, a spec
`src/cli/specs/account.ts` e as entradas de ajuda, para que `brza account usage` imprima o uso dos limites de cada conta.

## As fontes do upstream

- **[`stablyai/orca#37467`](https://github.com/stablyai/orca/pull/37467)** — "feat(cli): add orca account usage to
  print rate-limit usage per account", aberto, atualizado em 2026-11-02: 12 arquivos, +774/−1, os 8 modificados
  presentes no `brza-studio@8f41dd56a33`.

## O que fecha

O `brza account usage` no `brza-studio`, com testes. O como fica no PLN-011.
