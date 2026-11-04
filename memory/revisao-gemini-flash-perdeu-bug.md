---
name: revisao-gemini-flash-perdeu-bug
description: "No P3 do PLN-011, a revisão em Gemini 3.8 Flash aprovou sem achados, e a do Grok 4.7 Alto achou um bug importante"
metadata:
  node_type: memory
  type: project
  originSessionId: 7658422d-3d2c-4c64-9883-9f4588ea9518
  modified: 2026-11-04T02:34:19.128Z
---

Em 2026-11-03, o P3 do PLN-011 (`brza-studio@77a1cca1af2`) teve duas revisões do mesmo pedido. A do worker
Antigravity com `gemini-3.8-flash-high` aprovou "sem achados". A da sessão Grok 4.7, no esforço Alto, achou o A1, um bug
importante (o `nextCursor` sem `--cursor` saía da página `before`). Ela o provou com um `tsx` que chamava o handler, e
achou também dois achados de sugestão.

**Why:** a revisão leve confere o que o pedido lista, mas não exercita o código fora dos testes que já existem.

**How to apply:** revisão de passo de código não vai à camada rápida só porque a cota do modelo forte acabou. Se for,
vale a segunda revisão por um modelo forte de outro fornecedor. Liga com [[rodadas-com-agy-as-cegas]].
