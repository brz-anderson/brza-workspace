---
status: open
scope:
  - brza-studio
opened: 2026-11-02
description: Conferir num build que o cartão de entrega do chat sai sem o /rename do brza sessions --rename.
tags:
  - chat
  - cli
---

# O cartão de entrega sem o `/rename`, a conferir num build

O `brza-studio@d3d636fcef2` tira o `/rename <nome>` do cartão "Entregue a um agente"; o detalhe está em
[O `/rename` no cartão de entrega do chat, depois do sync da v1.4.246](../worklogs/2026-11-02-o-rename-no-cartao-de-entrega-do-chat.md).

**A conferir, com Anderson, no próximo build:** `brza sessions algum-nome --rename` num chat deixa o cartão só com o
título e o link, sem o `/rename`, e o chat novo continua sem o balão do `/rename`.
