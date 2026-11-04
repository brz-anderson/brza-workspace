---
status: open
description: O --session do brza chat read e send corta o valor no primeiro ":", e o endereço orca_session_id:<id> das mensagens da orquestração vira uma sessão inexistente, com erro enganoso.
scope:
  - brza-studio
opened: 2026-11-03
priority: low
trigger: o primeiro uso real que falhe por isso, ou o sync do upstream que trouxer o stablyai/orca#33115 fundido
tags:
  - chat
  - tooling
---

# O `--session` do `brza chat` recusa o endereço `orca_session_id:<id>`

## O pedido

A revisão do P2 do
[PLN-011: Os chats do BrzA Studio se coordenam pela CLI, aparecem na navegação e chegam aos plugins](../../plans/PLN-011-chats-pela-cli-e-plugins/PLN-011-plan.md)
observou, fora do escopo dela, um ponto no código do porte do `stablyai/orca#33115`. O destino saiu da R17.1, às cegas,
pelo `agy`. Ele escolheu primeiro "Corrigir no P3, em src/cli/brza/", e mudou na volta 1 para "Issue no workstream
studio, com gatilho": "o gatilho na issue garante que o caso será revisitado exatamente quando o upstream fundir o PR ou
se surgir um uso concreto, sem acumular código especulativo no fork".

## O que se sabe

- O `parseChatSessionSelector` (`src/cli/chat-sessions.ts:29-42`, no `brza-studio@f633ec3e307`) corta o valor no
  primeiro `:`, porque trata `<handle>:<leaf>` como pane key (linha 34).
- Por isso, `--session orca_session_id:<id>`, a forma de endereço das mensagens da orquestração
  (`src/shared/orchestration-party-identity.ts:3-10`, `src/shared/open-structured-agent-session.ts:83`), vira a sessão
  `orca_session_id`. O host a recusa por não achá-la: a falha é fechada, mas o erro engana.
- O `chat list --json` devolve o `session` como id cru, que é o que o `brza sessions` do PLN-010 passa. Hoje nenhum
  consumidor usa a forma com prefixo.

## O que fazer

No gatilho, decidir entre aceitar o prefixo no parse do upstream (se o `#33115` fundido ainda cortar) e um helper em
`src/cli/brza/` que o tire antes do parse, com um teste por forma: id cru, handle, pane key e `orca_session_id:<id>`.
