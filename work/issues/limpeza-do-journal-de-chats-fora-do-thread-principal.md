---
status: open
description: A limpeza do histórico no SQLite do journal de chats sai do thread principal, pelo #37802 do upstream, para que as ações do chat não travem de 5 a 10 segundos.
scope:
  - brza-studio
priority: medium
opened: 2026-11-03
trigger: o stablyai/orca#37802 integrado no upstream
tags:
  - chat
---

# A limpeza do journal de chats sai do thread principal

Frente `medium` da issue de origem
[Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md),
do `playground`. Era a fase 3 do
[PLN-011: Os chats do BrzA Studio se coordenam pela CLI, aparecem na navegação e chegam aos plugins](../../plans/PLN-011-chats-pela-cli-e-plugins/PLN-011-plan.md),
e saiu do plano em 2026-11-03, pela R11.4: fica aqui até o gatilho, e volta por plano ou por sync.

## O recorte

A limpeza de histórico no SQLite do journal trava a interface de 5 a 10 segundos no thread principal, segundo o relato
do upstream. O caminho apontado lá é mover as operações pesadas do journal a um background writer compartilhado.

**Espera a integração no upstream**, como respondido em 2026-11-03 na sessão "Plano: chat via CLI e plugins" do
`playground`: a frente vem depois que o `#37802` for integrado, e não como porte do PR aberto.

## As fontes do upstream

- **[`stablyai/orca#37802`](https://github.com/stablyai/orca/pull/37802)** — "Keep journal cleanup from freezing chat
  actions", aberto, atualizado em 2026-11-03 21:20 UTC: 459 arquivos, +11167/−4389, com entradas de build novas
  (`config/build-plugins/plain-node-worker-entry-names.ts`).

## O que fecha

O `#37802` no `brza-studio`, pelo sync do upstream ou pelo porte, decidido quando o gatilho valer: o PR integrado no
upstream (`gh api repos/stablyai/orca/pulls/37802 --jq .merged_at` diferente de `null`).
