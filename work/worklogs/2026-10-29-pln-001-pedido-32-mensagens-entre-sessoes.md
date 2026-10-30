---
scope:
  - brza-studio
date: 2026-10-29
tags:
  - chat
---

# O pedido 32 do PLN-001, as mensagens entre sessões no chat

Anderson fez o pedido 32 do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md)
na sessão do `brza-workspace` que gravou o pedido 31: a mensagem entre sessões deve aparecer no chat como "Mensagem
de…", como no Orca mais novo. Sem código nesta sessão.

## O que se fez

- **O levantamento, nesta sessão, por `git grep` no `brza-studio`.**
  - A mensagem de outra sessão nem aparece no chat. O Claude Code a grava num turno `isMeta`, e o leitor descarta esse
    turno (`transcript-line-decoders-claude.ts:108`).
  - O chat já tem a linha "Message from", mas só para o correio do Orca, e o `pt.json` não tem a tradução.
  - O upstream de 2026-10-29 (`7321b066e83`, #34824) troca essa linha por um cartão, também só para o correio do Orca.
- **As rodadas.** A R50 e a R51, pelo AskUserQuestion.
  - A abordagem é um leitor do BrzA mais o cartão do upstream trazido agora.
  - Entram o correio entre sessões e a devolução de subagente, esta com "Devolução de <nome>".
  - O clique no remetente abre a aba da sessão dele.
  - O trabalho roda agora, em paralelo com o pedido 31.
- **O plano.** O pedido 32, a Cobertura, o D48 ao D50, o P62 ao P65 e o C18 ao C20. O estimado sobe 16,3 h.
- **A execução.** A sessão `pln-001-pedido-32`, no worktree `.worktrees/pln-001-pedido-32` do `brza-studio`, faz o P62
  ao P64 em sequência. O P65 e os casos manuais ficam com Anderson.
