---
name: fechar-a-tarefa-apos-o-push
description: "Concluída a tarefa, sobretudo depois de um push, rodar o close-task sem esperar Anderson pedir; ele cobrou."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 50a7ec56-27f5-494a-b7f6-a3d4acea3899
  modified: 2026-11-03T06:13:04.603Z
---

Ao concluir uma tarefa — principalmente logo após um `push` —, rode o `close-task` (worklog, `Retomar`, memória e
`brza note commit`) na mesma resposta, sem perguntar se deve.

**Why:** em 2026-11-03, no PLN-007, a sessão fez o push do `BrzA Dark Theme` na `master` do `brza-studio` e só
ofereceu o `/close-task`. Anderson respondeu "rode, sempre rode `close-task` ao concluir uma tarefa, principalmente
após um `push`". A norma já diz que a sessão aciona a skill sozinha ao fechar uma tarefa.

**How to apply:** o push (ou o aceite de Anderson) é o sinal de que a tarefa fechou: devolva o resultado e rode o
`close-task` em seguida, e só depois diga que o `/compact` pode ser digitado.
