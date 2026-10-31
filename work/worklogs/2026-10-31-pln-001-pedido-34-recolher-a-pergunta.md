---
scope:
  - brza-studio
date: 2026-10-31
tags:
  - chat
---

# O pedido 34 do PLN-001, recolher a pergunta no chat estruturado

Anderson pediu, na sessão do workstream `studio` do `brza-workspace`: "ferramenta de pergunta do chat deve poder ser
minimizada, para que eu possa ler a conversa no chat". O pedido entrou no
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md)
como o pedido 34, com a R60, a R61, o D52, o P69 e o C22, sem código.

## A causa

O recolher já existe no chat do terminal: a seta ou o Esc recolhem o cartão a uma faixa acima do composer
(`NativeChatResolvedView.tsx:375-392`). O chat estruturado, o do Claude pelo Agent SDK, que é o de Anderson, não passa o
`onCollapse` ao cartão de pergunta nem ao de aprovação (`NativeChatStructuredSession.tsx:366-388`). O celular exclui
esse caminho de propósito.

## As rodadas

- **R60.** Recolhem a pergunta e a aprovação, só no desktop, e com o cartão recolhido o composer fica usável. O P69 roda
  agora, num worktree.
- **R61.** Um `collector` mediu o envio com a pergunta pendente. A mensagem vai à fila do host e não cancela o prompt;
  a fila só drena com o turno parado. O "Steer" da fila fica desabilitado enquanto há pergunta pendente, porque o host
  o recusa. O C22 confere também o ramo sem fila, em que o repo não diz o que o CLI faz com a pergunta.

## Próximo

O P69, na sessão `pln-001-pedido-34`, no worktree `.worktrees/pln-001-pedido-34` do `brza-studio`; depois, o C22 num
build, com Anderson.
